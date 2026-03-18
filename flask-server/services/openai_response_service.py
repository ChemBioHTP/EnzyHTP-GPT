#! python3
# -*- encoding: utf-8 -*-
"""OpenAI Responses runtime implementation."""

from __future__ import annotations

import logging
from inspect import signature
from json import JSONDecodeError, dumps, loads
from types import SimpleNamespace
from typing import Any, Callable, Dict, List, Tuple

from openai import (
    APIError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    NotFoundError,
    OpenAI,
    RateLimitError,
)

from config import OPENAI_RUNTIME
from .openai_observability import OpenAIMeta, log_openai_meta
from .openai_service import AssistantFunction, OpenAIChat, DEFAULT_OPENAI_API_KEY

LOGGER = logging.getLogger(__name__)
MAX_TOOL_LOOP = 8


class ResponseRunError(RuntimeError):
    """Represents a Responses API run that ended without a usable reply."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


class OpenAIResponsesService(OpenAIChat):
    """Handles interactions with OpenAI's Responses API."""

    functions: List[AssistantFunction]
    response_tools: List[dict]
    latest_tool_call_result: Dict[str, bool]
    latest_response_id: str | None

    def __init__(
        self,
        openai_secret_key: str,
        assistant_name: str = str(),
        instructions: str = str(),
        model: str = "gpt-4o",
        tools: List[dict] = list(),
        tool_function_mapper: Dict[str, Callable] = dict(),
        tool_function_callable_kwargs: Dict[str, Any] = dict(),
        thread_id: str = str(),
        conversation_mode: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(openai_secret_key=openai_secret_key, model=model, conversation_mode=conversation_mode)
        self.assistant_name = assistant_name
        self.instructions = instructions
        self.tools = tools
        self.response_tools = self._normalize_tools_for_responses(tools)
        self.conversation_id = self._normalize_conversation_id(thread_id) if thread_id else None
        self.latest_response_id = None
        if (self._is_legacy_assistant_thread_id(self.conversation_id)):
            self.conversation_id = None
        if (thread_id):
            self.conversation_mode = True

        openai_param_list = [param_name for param_name in signature(self.client.responses.create).parameters]
        self.openai_args_dict = {key: value for key, value in kwargs.items() if key in openai_param_list}

        function_tools = filter(lambda tool: tool.get("type") == "function", tools)
        self.functions = [
            AssistantFunction(
                function_definition_dict=(function.get("function", function)),
                tool_function_mapper=tool_function_mapper,
                tool_function_callable_kwargs=tool_function_callable_kwargs,
            )
            for function in function_tools
        ]
        self.latest_tool_call_result = dict()

    @staticmethod
    def _as_text(value: Any) -> str:
        if (value is None):
            return ""
        if (isinstance(value, str)):
            return value
        try:
            return dumps(value, ensure_ascii=False, default=str)
        except Exception:
            return str(value)

    @staticmethod
    def _normalize_conversation_id(value: Any) -> str | None:
        if (value is None):
            return None
        if (isinstance(value, str)):
            return value
        conversation_id = getattr(value, "id", None)
        if (conversation_id is None and isinstance(value, dict)):
            conversation_id = value.get("id")
        if (isinstance(conversation_id, str)):
            return conversation_id
        if (conversation_id is not None):
            return str(conversation_id)
        return None

    @staticmethod
    def _is_legacy_assistant_thread_id(value: str | None) -> bool:
        return isinstance(value, str) and value.startswith("thread_")

    @staticmethod
    def _normalize_tools_for_responses(tools: List[dict]) -> List[dict]:
        normalized_tools: List[dict] = []
        for tool in tools:
            tool_type = tool.get("type", None)
            if (tool_type != "function"):
                normalized_tools.append(tool)
                continue
            function_definition = tool.get("function", tool)
            if (not isinstance(function_definition, dict)):
                continue
            function_payload = {key: value for key, value in function_definition.items() if key != "type"}
            normalized_tools.append({
                "type": "function",
                **function_payload,
            })
        return normalized_tools

    @staticmethod
    def _extract_text_from_message_output(content: Any) -> str:
        # Best-effort parse across SDK item structures.
        if (content is None):
            return ""
        if (isinstance(content, str)):
            return content
        if (isinstance(content, list)):
            parts = []
            for c in content:
                ctype = getattr(c, "type", None) or (c.get("type") if isinstance(c, dict) else None)
                if (ctype in ("output_text", "text")):
                    part = getattr(c, "text", None)
                    if (part is None and isinstance(c, dict)):
                        part = c.get("text")
                    parts.append(OpenAIResponsesService._as_text(part))
                    continue
                text_value = getattr(c, "value", None)
                if (text_value is None and isinstance(c, dict)):
                    text_value = c.get("value")
                if (text_value is not None):
                    parts.append(OpenAIResponsesService._as_text(text_value))
            return "\n".join([p for p in parts if p])
        return OpenAIResponsesService._as_text(content)

    @classmethod
    def _extract_messages_from_items(cls, items: list) -> List[Dict[str, str]]:
        messages: List[Dict[str, str]] = []
        for item in items:
            role = getattr(item, "role", None)
            if (role is None and isinstance(item, dict)):
                role = item.get("role")
            if (role not in ("user", "assistant")):
                continue
            content = getattr(item, "content", None)
            if (content is None and isinstance(item, dict)):
                content = item.get("content")
            messages.append({
                "role": role,
                "text_value": cls._extract_text_from_message_output(content),
            })
        return messages

    def _create_response(self, input_payload: Any, conversation_id: str = None):
        normalized_conversation_id = self._normalize_conversation_id(conversation_id)
        if (self._is_legacy_assistant_thread_id(normalized_conversation_id)):
            normalized_conversation_id = None
        kwargs = {
            "model": self.model,
            "input": input_payload,
            "instructions": self.instructions,
            "tools": self.response_tools,
            **self.openai_args_dict,
        }
        if (normalized_conversation_id):
            kwargs["conversation"] = normalized_conversation_id
        elif (self.latest_response_id):
            kwargs["previous_response_id"] = self.latest_response_id
        return self.client.responses.create(**kwargs)

    def _ensure_conversation_context(self) -> None:
        if (self._is_legacy_assistant_thread_id(self.conversation_id)):
            self.conversation_id = None
        if (not self.conversation_mode or self.conversation_id):
            return
        conversations = getattr(self.client, "conversations", None)
        if (not conversations or not hasattr(conversations, "create")):
            return
        conversation = conversations.create()
        self.conversation_id = self._normalize_conversation_id(
            getattr(conversation, "id", None) or getattr(conversation, "conversation", None) or conversation
        )

    @property
    def thread(self):
        if (self.conversation_mode and self.conversation_id):
            return SimpleNamespace(id=self.conversation_id)
        return None

    @thread.setter
    def thread(self, value):
        if (value is None):
            self.conversation_id = None
            self.latest_response_id = None
            return
        value_id = getattr(value, "id", None)
        if (value_id):
            self.conversation_id = self._normalize_conversation_id(value_id)

    def _extract_text_and_calls(self, response: Any) -> Tuple[str, List[dict]]:
        output_text = getattr(response, "output_text", None)
        tool_calls: List[dict] = []

        output_items = getattr(response, "output", []) or []
        for item in output_items:
            item_type = getattr(item, "type", None)
            if (item_type is None and isinstance(item, dict)):
                item_type = item.get("type")

            if (item_type == "function_call"):
                tool_calls.append({
                    "name": (getattr(item, "name", None) or (item.get("name") if isinstance(item, dict) else None)),
                    "arguments": (getattr(item, "arguments", None) or (item.get("arguments") if isinstance(item, dict) else "{}")),
                    "call_id": (getattr(item, "call_id", None) or getattr(item, "id", None) or (item.get("call_id") if isinstance(item, dict) else None)),
                })
                continue

            if (item_type == "message" and not output_text):
                content = getattr(item, "content", None)
                if (content is None and isinstance(item, dict)):
                    content = item.get("content")
                output_text = self._extract_text_from_message_output(content)

        output_text = self._as_text(output_text)
        return output_text, tool_calls

    def _find_function(self, name: str) -> AssistantFunction | None:
        matched = list(filter(lambda func: func.name == name, self.functions))
        if (matched):
            return matched[0]
        return None

    def _run_tool_loop(self, response: Any) -> Any:
        current_response = response
        loop_count = 0

        while True:
            _, tool_calls = self._extract_text_and_calls(current_response)
            if (not tool_calls):
                return current_response

            loop_count += 1
            if (loop_count > MAX_TOOL_LOOP):
                raise ResponseRunError("tool_loop_limit", "Exceeded tool-calling loop limit.")

            tool_outputs = []
            for call in tool_calls:
                func_name = call.get("name")
                call_id = call.get("call_id")
                raw_args = call.get("arguments") or "{}"
                tool_arguments = dict()
                try:
                    tool_arguments = loads(raw_args)
                except (JSONDecodeError, TypeError):
                    tool_arguments = dict()

                matched_function = self._find_function(func_name)
                if (matched_function and matched_function.mapped_callable):
                    tool_arguments.update(matched_function.tool_function_callable_kwargs)
                    is_successful, function_output = matched_function.mapped_callable(**tool_arguments)
                else:
                    is_successful = False
                    function_output = f"Function '{func_name}' is not available."

                self.latest_tool_call_result[func_name] = is_successful
                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": call_id,
                    "output": self._as_text(function_output),
                })

            conversation_id = self._normalize_conversation_id(getattr(current_response, "conversation", None)) or self.conversation_id
            current_response = self._create_response(
                input_payload=tool_outputs,
                conversation_id=conversation_id,
            )
            self.conversation_id = self._normalize_conversation_id(getattr(current_response, "conversation", None)) or self.conversation_id
            self.latest_response_id = getattr(current_response, "id", None) or self.latest_response_id

    def ask_gpt(self, prompt: str) -> Tuple[bool, int, str]:
        if (self.client.api_key == DEFAULT_OPENAI_API_KEY):
            return False, 500, "OpenAI Secret Key does not exist."

        try:
            self.latest_tool_call_result.clear()
            self._ensure_conversation_context()
            log_openai_meta(
                LOGGER,
                "openai_responses.request",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    conversation_id=self.conversation_id,
                ),
            )
            input_payload: Any = prompt
            if (self.conversation_mode):
                self.messages.append({"role": "user", "content": prompt})

            response = self._create_response(
                input_payload=input_payload,
                conversation_id=(self.conversation_id if self.conversation_mode else None),
            )
            self.conversation_id = self._normalize_conversation_id(getattr(response, "conversation", None)) or self.conversation_id
            self.latest_response_id = getattr(response, "id", None) or self.latest_response_id

            response = self._run_tool_loop(response)
            response_text, _ = self._extract_text_and_calls(response)

            if (self.conversation_mode):
                self.messages.append({"role": "assistant", "content": response_text})

            response_id = getattr(response, "id", None)
            self.conversation_id = self._normalize_conversation_id(getattr(response, "conversation", None)) or self.conversation_id
            self.latest_response_id = response_id or self.latest_response_id
            log_openai_meta(
                LOGGER,
                "openai_responses.success",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    response_id=response_id,
                    conversation_id=self.conversation_id,
                    tool_call_count=len(self.latest_tool_call_result),
                ),
            )
            return True, 200, response_text
        except ResponseRunError as e:
            log_openai_meta(
                LOGGER,
                "openai_responses.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    conversation_id=self.conversation_id,
                    tool_call_count=len(self.latest_tool_call_result),
                    openai_error_code=e.code,
                ),
                error=str(e),
            )
            return False, 500, f"OpenAI response run failed: {str(e)}"
        except RateLimitError as e:
            log_openai_meta(
                LOGGER,
                "openai_responses.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    conversation_id=self.conversation_id,
                    openai_error_code="rate_limit_exceeded",
                ),
                error=str(e),
            )
            return True, 429, "Rate Limit Error: You exceeded your current OpenAI API quota or Rate Limit, please check your plan and billing details."
        except BadRequestError as e:
            log_openai_meta(
                LOGGER,
                "openai_responses.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    conversation_id=self.conversation_id,
                    openai_error_code="bad_request",
                ),
                error=str(e),
            )
            return True, 400, "Bad Request: Your OpenAI API Key is valid, but you sent a bad request."
        except APITimeoutError as e:
            log_openai_meta(
                LOGGER,
                "openai_responses.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    conversation_id=self.conversation_id,
                    openai_error_code="timeout",
                ),
                error=str(e),
            )
            return False, 504, "OpenAI Responses API Timeout."
        except AuthenticationError as e:
            log_openai_meta(
                LOGGER,
                "openai_responses.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    conversation_id=self.conversation_id,
                    openai_error_code="authentication_error",
                ),
                error=str(e),
            )
            return False, 401, "Authentication Failed: Invalid OpenAI Secret Key."
        except InternalServerError as e:
            log_openai_meta(
                LOGGER,
                "openai_responses.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    conversation_id=self.conversation_id,
                    openai_error_code="internal_server_error",
                ),
                error=str(e),
            )
            return False, 500, "OpenAI Internal Server Error. Unable to verify."
        except APIError as e:
            log_openai_meta(
                LOGGER,
                "openai_responses.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    conversation_id=self.conversation_id,
                    openai_error_code="api_error",
                ),
                error=str(e),
            )
            return False, 500, "API Error: " + str(e)
        except Exception as e:
            log_openai_meta(
                LOGGER,
                "openai_responses.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    conversation_id=self.conversation_id,
                    openai_error_code="unexpected_error",
                ),
                error=str(e),
            )
            return False, 500, "An unexpected error occurred: " + str(e)

    def pre_process(self, input_prompt: str) -> str:
        """Process the input prompt before sending to OpenAI."""
        return input_prompt

    def post_process(self, response_content: str, is_finishing: bool) -> str:
        """Process response content after receiving model output."""
        _ = is_finishing
        return response_content

    def detect_vicious_output(self, initial_processed_response_content: str):
        _ = initial_processed_response_content
        return

    def refresh_thread(self) -> bool:
        if (not self.conversation_mode):
            return False
        self.conversation_id = None
        self.latest_response_id = None
        return True

    def clear_thread(self) -> bool:
        if (not self.conversation_mode):
            return False
        if (not self.conversation_id):
            return True
        is_successful = self.delete_session(
            openai_secret_key=self.client.api_key,
            session_id=self.conversation_id,
        )
        if (is_successful):
            self.conversation_id = None
            self.latest_response_id = None
        return is_successful

    @classmethod
    def get_messages(cls, openai_secret_key: str, session_id: str, limit: int = 20) -> Tuple[bool, List[Dict[str, str]]]:
        try:
            client = OpenAI(api_key=openai_secret_key)
            conversations = getattr(client, "conversations", None)
            if (not conversations):
                return False, list()
            items_api = getattr(conversations, "items", None)
            if (not items_api or not hasattr(items_api, "list")):
                return False, list()
            result = items_api.list(conversation_id=session_id, limit=limit)
            items = getattr(result, "data", []) or []
            messages = cls._extract_messages_from_items(items)
            return True, messages
        except Exception:
            return False, list()

    @classmethod
    def get_thread_messages(cls, openai_secret_key: str, thread_id: str, limit: int = 20) -> Tuple[bool, List[Dict[str, str]]]:
        return cls.get_messages(openai_secret_key=openai_secret_key, session_id=thread_id, limit=limit)

    @classmethod
    def get_summary(cls, openai_secret_key: str, session_id: str) -> Tuple[bool, str]:
        is_successful, messages = cls.get_messages(openai_secret_key, session_id)
        assistant_messages = [message for message in messages if message.get("role", None) == "assistant"]
        summary = assistant_messages[-1].get("text_value", str()) if assistant_messages else str()
        return is_successful, summary

    @classmethod
    def get_thread_summary(cls, openai_secret_key: str, thread_id: str) -> Tuple[bool, str]:
        return cls.get_summary(openai_secret_key=openai_secret_key, session_id=thread_id)

    @classmethod
    def delete_session(cls, openai_secret_key: str, session_id: str) -> bool:
        if (not session_id):
            return True
        try:
            client = OpenAI(api_key=openai_secret_key)
            conversations = getattr(client, "conversations", None)
            if (not conversations or not hasattr(conversations, "delete")):
                return False
            _ = conversations.delete(conversation_id=session_id)
            return True
        except NotFoundError:
            return True
        except Exception:
            return False

    @classmethod
    def delete_thread(cls, openai_secret_key: str, thread_id: str) -> bool:
        return cls.delete_session(openai_secret_key=openai_secret_key, session_id=thread_id)

    @classmethod
    def delete_threads(
        cls,
        openai_secret_key: str,
        thread_id_list: List[str] = None,
        thread_id: List[str] = None,
    ) -> Tuple[bool, List[str]]:
        if (thread_id_list is None):
            thread_id_list = thread_id if isinstance(thread_id, list) else list()
        is_successful = True
        deleted_thread_id_list = list()
        for thread_id in thread_id_list:
            is_deleted = cls.delete_thread(openai_secret_key=openai_secret_key, thread_id=thread_id)
            if (is_deleted):
                deleted_thread_id_list.append(thread_id)
            else:
                is_successful = False
        return is_successful, deleted_thread_id_list
