#! python3
# -*- encoding: utf-8 -*-
'''
OpenAI (ChatGPT) correspondence.

@File    :   openai_service.py
@Created :   2024/06/23 20:25
@Author  :   Zhong, Yinjie
@Contact :   yinjie.zhong@vanderbilt.edu
'''

# Here put the import lib.
from __future__ import annotations
import time
import logging
from typing import Any, Callable, Tuple, Dict, List
from typing_extensions import override

from inspect import signature
from time import sleep
from json import loads, JSONDecodeError

from openai import (
    OpenAI,

    # Separator. All the followings are exceptions.
    APIError,
    OpenAIError,
    ConflictError,
    NotFoundError,
    APIStatusError,
    RateLimitError,
    APITimeoutError,
    BadRequestError,
    APIConnectionError,
    AuthenticationError,
    InternalServerError,
    PermissionDeniedError,
    UnprocessableEntityError,
    APIResponseValidationError,
)
import re
from config import OPENAI_RUNTIME
from .openai_observability import OpenAIMeta, log_openai_meta

# Here put local imports.
from .json_to_tree import JsonToTree

# from config import DEFAULT_OPENAI_API_KEY
DEFAULT_OPENAI_API_KEY = "5511667"
DEFAULT_OPENAI_BASE_URL = "https://api.openai.com/v1"
DEFAULT_TIMEOUT_LIMIT = 60      # The timeout waiting for response. Unit: Seconds.
LOGGER = logging.getLogger(__name__)


def normalize_openai_base_url(base_url: str = None) -> str:
    """Normalize provider base URL and ensure it always has protocol."""
    if (base_url is None):
        return DEFAULT_OPENAI_BASE_URL
    if (not isinstance(base_url, str)):
        base_url = str(base_url)
    normalized = base_url.strip()
    if (not normalized):
        return DEFAULT_OPENAI_BASE_URL
    if (not re.match(r"^https?://", normalized, re.IGNORECASE)):
        normalized = f"https://{normalized.lstrip('/')}"
    return normalized.rstrip("/")


def build_openai_client(openai_secret_key: str, base_url: str = None) -> OpenAI:
    """Create OpenAI client with sanitized base_url to avoid malformed endpoint issues."""
    normalized_base_url = normalize_openai_base_url(base_url)
    return OpenAI(api_key=openai_secret_key, base_url=normalized_base_url)

#region OpenAI Chatbot

class OpenAIChat:
    """Handles interactions with OpenAI's Chat API, particularly GPT models."""

    client: OpenAI
    conversation_mode: bool

    def __init__(self, openai_secret_key: str, model: str = "gpt-3.5-turbo", conversation_mode: bool = False, base_url: str = None, **kwargs) -> None:
        """Initializes the service with the OpenAI API key and configuration for using specific GPT models.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            model (str, optional): ID of the GPT model to use.
                See the [model endpoint compatibility](https://platform.openai.com/docs/models/model-endpoint-compatibility)
                table for details on which models work with the Chat API. Default "gpt-3.5-turbo".
            conversation_mode (bool): If True, retains the conversation context. Default is False.
            **kwargs: Additional arguments to customize the API calls.
        """
        self.model = model
        self.base_url = normalize_openai_base_url(base_url)
        if (openai_secret_key):
            self.client = build_openai_client(openai_secret_key, base_url=self.base_url)
        else:
            self.client = build_openai_client(DEFAULT_OPENAI_API_KEY, base_url=self.base_url)
        self.conversation_mode = conversation_mode
        self.messages = list() if self.conversation_mode else None
        
        # Prepare the additional API arguments by filtering out irrelevant parameters.
        openai_param_list = [param_name for param_name in signature(self.client.chat.completions.create).parameters]
        self.openai_args_dict = {key: value for key, value in kwargs.items() if key in openai_param_list}

    def ask_gpt(self, prompt: str) -> Tuple[bool, int, str]:
        """
        Sends a prompt to GPT and retrieves the response.

        Args:
            prompt (str): The prompt or question to send to GPT.

        Returns:
            is_valid (bool): Whether the API key is valid.
            status_code (int): The HTTP status code from the API response.
            response_content (str): The actual response from GPT or an error message.
        """
        if (self.client.api_key == DEFAULT_OPENAI_API_KEY):
            return False, 500, "OpenAI Secret Key does not exist."

        base_meta = OpenAIMeta(
            openai_runtime=OPENAI_RUNTIME,
            model=self.model,
        )
        log_openai_meta(
            LOGGER,
            "openai_chat.request",
            base_meta,
            endpoint=self.base_url,
            conversation_mode=self.conversation_mode,
            prompt_char_count=len(prompt or ""),
            openai_args=self.openai_args_dict,
            request_payload={
                "path": "/chat/completions",
                "model": self.model,
                "messages_count": (len(self.messages) + 1) if self.conversation_mode else 1,
                "has_timeout_arg": ("timeout" in self.openai_args_dict),
            },
        )

        try:
            response_content = str()
            response_id = None
            if (self.conversation_mode):
                messages = self.messages + [{"role": "user", "content": prompt}]

                self.messages.append({
                    "role": "user",
                    "content": prompt,
                })
                response = self.client.chat.completions.create(
                    messages=messages,
                    model=self.model,
                    timeout=DEFAULT_TIMEOUT_LIMIT,
                    **self.openai_args_dict
                )
                response_id = getattr(response, "id", None)
                response_msg = response.choices[0].message
                response_content = response_msg.content

                # Update the messages of the service after the prompt is successfully processed and parsed.
                messages.append({
                    "role": response_msg.role,
                    "content": response_msg.content,
                })
                self.messages = messages
            else:
                response = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model=self.model,
                    **self.openai_args_dict
                )
                response_id = getattr(response, "id", None)
                response_content = response.choices[0].message.content

            log_openai_meta(
                LOGGER,
                "openai_chat.success",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    response_id=response_id,
                ),
            )

            # Successfully received a response from OpenAI.
            return (True, 200, response_content)
        except RateLimitError as e:
            log_openai_meta(
                LOGGER,
                "openai_chat.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    openai_error_code="rate_limit_exceeded",
                ),
                error=str(e),
            )
            return (True, 429, "Rate Limit Error: You exceeded your current OpenAI API quota or Rate Limit, please check your plan and billing details.")
        except BadRequestError as e:
            log_openai_meta(
                LOGGER,
                "openai_chat.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    openai_error_code="bad_request",
                ),
                error=str(e),
            )
            return (True, 400, "Bad Request: Your OpenAI Secret Key is valid, but you sent a bad request.")
        except AuthenticationError as e:
            log_openai_meta(
                LOGGER,
                "openai_chat.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    openai_error_code="authentication_error",
                ),
                error=str(e),
            )
            return (False, 401, "Authentication Failed: Invalid OpenAI Secret Key.")
        except InternalServerError as e:
            log_openai_meta(
                LOGGER,
                "openai_chat.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    openai_error_code="internal_server_error",
                ),
                error=str(e),
            )
            return (False, 500, "OpenAI Internal Server Error. Unable to verify.")
        except APIConnectionError as e:
            log_openai_meta(
                LOGGER,
                "openai_chat.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    openai_error_code="api_connection_error",
                ),
                error=str(e),
            )
            endpoint = self.base_url
            return (
                False,
                500,
                f"API Connection Error: Unable to reach endpoint `{endpoint}`. detail: {str(e)}"
            )
        except APIError as e:
            log_openai_meta(
                LOGGER,
                "openai_chat.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    openai_error_code="api_error",
                ),
                error=str(e),
            )
            return (False, 500, "API Error: " + str(e))
        except Exception as e:
            log_openai_meta(
                LOGGER,
                "openai_chat.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    openai_error_code="unexpected_error",
                ),
                error=str(e),
            )
            return (False, 500, "An unexpected error occurred: " + str(e))

    # @classmethod
    # def humanize_text_value(cls, text_value: str):
    #     # Try to extract text between triple backticks (with or without json)
    #     pattern = re.compile(
    #         r"```(?:json)?\s*\n([\s\S]*?)\n?```",  # group 1: json content
    #         re.IGNORECASE
    #     )
    #     match = pattern.search(text_value)

    #     if match:
    #         json_block = match.group(0).strip()    # full block with markers
    #         json_content = match.group(1).strip()  # content without markers
    #         json_data = dict()
    #         try:
    #             json_data = loads(json_content)
    #             tree_content = JsonToTree.tree_text(json_data=json_data, contain_value=True)
    #             tree_block = f"""```txt\n{tree_content}\n```"""
    #             text_value = text_value.replace(json_block, tree_block)
    #         except:
    #             pass
    #     return text_value

#endregion

#region OpenAI Assistant
from openai import AssistantEventHandler
from openai.types.beta.threads import (
    Run,
    Text,
    Message,
    ImageFile,
    TextDelta,
    MessageDelta,
    MessageContent,
    MessageContentDelta,
)
from openai.types.beta.threads.runs import RunStep, RunStepDelta, ToolCall, ToolCallDelta
from openai.types.beta import Assistant, Thread
from openai.types.beta.assistant_stream_event import ThreadRunRequiresAction, AssistantStreamEvent

DEFAULT_REFRESH_INTERVAL = 2    # The interval to refresh the response status. Unit: Seconds.

TERMINAL_STATUS_LIST = ["cancelled", "failed", "completed", "expired", "incomplete"]
COMPLETED_STATUS = "completed"

PENDING_STATUS_LIST = ["queued", "in_progress", "requires_action", "cancelling"]
ACTION_REQUIRED_STATUS = "requires_action"


class AssistantRunError(RuntimeError):
    """Represents an Assistant run that ended without a usable reply."""

    def __init__(self, code: str, message: str, status: str = None):
        super().__init__(message)
        self.code = code
        self.status = status

class FunctionParameter():
    """Function Tool Parameter."""

    key: str
    param_type: str
    description: str
    required: bool
    value: Any

    def __init__(self, key: str, param_type: str, description: str, required: bool):
        self.key = key
        self.param_type = param_type
        self.description = description
        self.required = required

    @property
    def name(self):
        """The name of the parameter."""
        return self.key
    
    @name.setter
    def name(self, value):
        """Set the name of the parameter."""
        self.key = value

    @classmethod
    def parse_function_parameters(cls, parameters_dict: dict) -> List[FunctionParameter]:
        """Read the parameters information from the 'parameters' field of the function dictionary.
        
        Args:
            parameters_dict (dict): The 'parameters' inner dictionary of the function dictionary.

        Returns:
            parameters (List[FunctionParameter]): A list of FunctionParameter instances.
        """
        properties: Dict[str, dict] = parameters_dict.get("properties", dict())
        required_params: list = parameters_dict.get("required", list())
        
        parameters = list()
        for key, value in properties.items():
            param_type = value.get("type", "string")
            description = value.get("description", "")
            required = (key in required_params)
            parameters.append(FunctionParameter(key=key, param_type=param_type, description=description, required=required))
            continue

        return parameters

class AssistantFunction():
    """OpenAI Assistant Function Tool."""

    name: str
    description: str
    parameters: List[FunctionParameter]
    mapped_callable: Callable
    tool_function_callable_kwargs: Dict[str, Any]

    def __init__(self, function_definition_dict: dict, tool_function_mapper: Dict[str, Callable] = dict(), tool_function_callable_kwargs: Dict[str, Any] = dict()):
        """Initialize OpenAI Assistant Function Tool with definition dictionary.
        
        Args:
            function_definition_dict (dict): The definition dictionary of OpenAI Assistant Function Tool.
            tool_function_mapper (Dict[str, Callable]): A mapper to associate a `tool_function` defined in the Assistant with a python function produces the output value.
            tool_function_callable_kwargs (Dict[str, Callable]): A dict of additional keyword arguments to be passed to the tool function callables.
        """
        self.name = function_definition_dict.get("name", str())
        self.description = function_definition_dict.get("description", str())
        self.parameters = FunctionParameter.parse_function_parameters(parameters_dict=function_definition_dict.get("parameters", dict()))
        self.mapped_callable = tool_function_mapper.get(self.name)
        self.tool_function_callable_kwargs = tool_function_callable_kwargs
        return

    def keyword_arguments(self) -> Dict[str, Any]:
        """Export a dictionary containing keyword arguments associated with the function."""
        kwargs_dict = dict()
        for param in self.parameters:
            kwargs_dict[param.key] = param.value
            continue
        return kwargs_dict
    
    def __str__(self):
        return f"AssistantFunction({self.name})"

class EventHandler(AssistantEventHandler):
    functions: List[AssistantFunction]
    assistant_service: OpenAIAssistant

    def __init__(self, assistant_service: OpenAIAssistant):
        super().__init__()
        self.assistant_service = assistant_service
        return

    @override
    def on_event(self, event: AssistantStreamEvent):
        """Callback that is fired for every Server-Sent-Event"""
        # Retrieve events that are denoted with 'requires_action'
        # since these will have our tool_calls
        if event.event == "thread.run.requires_action":
            # print("Require action!")
            run_id = event.data.id  # Retrieve the run ID from the event data
            self.handle_requires_action(event.data, run_id)
        else:
            return super().on_event(event)

    @override
    def on_exception(self, exception: Exception):
        raise exception
    
    @override
    def on_timeout(self):
        raise APITimeoutError() # pylint: disable=no-value-for-parameter
    
    @override
    def on_text_created(self, text: Text) -> None:
        """Callback that is fired when a run step is created"""
        # print(f"\nassistant > ", end="", flush=True)
        pass
    
    @override
    def on_text_delta(self, delta: TextDelta, snapshot: Text):
        """Callback that is fired whenever a run step delta is returned from the API

        The first argument is just the delta as sent by the API and the second argument
        is the accumulated snapshot of the run step. For example, a tool calls event may
        look like this:

        # delta
        tool_calls=[
            RunStepDeltaToolCallsCodeInterpreter(
                index=0,
                type='code_interpreter',
                id=None,
                code_interpreter=CodeInterpreter(input=' sympy', outputs=None)
            )
        ]
        # snapshot
        tool_calls=[
            CodeToolCall(
                id='call_wKayJlcYV12NiadiZuJXxcfx',
                code_interpreter=CodeInterpreter(input='from sympy', outputs=[]),
                type='code_interpreter',
                index=0
            )
        ],
        """
        # print(delta.value, end="", flush=True)
        pass
        
    def on_tool_call_created(self, tool_call: ToolCall):
        """Callback that is fired when a tool call is created."""
        # print(f"\nassistant > {tool_call.type}\n", flush=True)
        pass
    
    def on_tool_call_delta(self, delta: ToolCallDelta, snapshot: ToolCall):
        """Callback that is fired when a tool call delta is encountered"""
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                # print(delta.code_interpreter.input, end="", flush=True)
                pass
            if delta.code_interpreter.outputs:
                # print(f"\n\noutput >", flush=True)
                pass
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        # print(f"\n{output.logs}", flush=True)
                        pass
 
    def handle_requires_action(self, data: Run, run_id: str):
        tool_outputs = []
        for tool in data.required_action.submit_tool_outputs.tool_calls:
            # print(tool)
            tool_arguments = dict()
            raw_arguments = getattr(tool.function, "arguments", "{}")
            try:
                parsed_arguments = loads(raw_arguments)
                if (isinstance(parsed_arguments, dict)):
                    tool_arguments = parsed_arguments
            except (JSONDecodeError, TypeError):
                tool_arguments = dict()
            filtered_functions = list(filter(lambda func: func.name==tool.function.name, self.assistant_service.functions))
            if (len(filtered_functions) > 0):
                called_function = filtered_functions[0]
                # print(f"Mapped functions: {called_function}")
                # print(f"Arguments: {called_function.tool_function_callable_kwargs}")
                callable_tool_arguments = tool_arguments.copy()
                callable_tool_arguments.update(called_function.tool_function_callable_kwargs)
                is_successful, function_output = called_function.mapped_callable(**callable_tool_arguments)
                function_output_text = str(function_output)
                tool_outputs.append({"tool_call_id": tool.id, "output": function_output})
                self.assistant_service.latest_tool_call_result[tool.function.name] = is_successful
                self.assistant_service.latest_tool_call_trace.append({
                    "function_name": tool.function.name,
                    "function_call_id": tool.id,
                    "is_successful": is_successful,
                    "arguments": tool_arguments,
                    "output_chars": len(function_output_text),
                    "output_preview": function_output_text[:400],
                })
            else:
                self.assistant_service.latest_tool_call_trace.append({
                    "function_name": tool.function.name,
                    "function_call_id": tool.id,
                    "is_successful": False,
                    "arguments": tool_arguments,
                    "output_chars": 0,
                    "output_preview": f"Function '{tool.function.name}' is not available.",
                })
            continue
        # Submit all tool_outputs at the same time
        # print(f"Tool outputs: {tool_outputs}")
        self.submit_tool_outputs(tool_outputs, run_id)
 
    def submit_tool_outputs(self, tool_outputs: list, run_id: str):
        # Use the submit_tool_outputs_stream helper
        with self.assistant_service.client.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=self.current_run.thread_id,
            run_id=self.current_run.id,
            tool_outputs=tool_outputs,
            event_handler=EventHandler(self.assistant_service),
        ) as stream:
            # for text in stream.text_deltas:
            #     print(text, end="", flush=True)
            #     print()
            stream.until_done()

class OpenAIAssistant(OpenAIChat):
    """Handles interactions with OpenAI's Assistant API, particularly GPT models."""

    # TODO (Zhong): Handle possible errors caused by invalid openai_secret_key.

    assistant: Assistant
    __thread: Thread

    functions: List[AssistantFunction]
    latest_tool_call_result: Dict[str, bool]
    latest_tool_call_trace: List[dict]
    completion_message: str = str()

    def __init__(self, openai_secret_key: str, assistant_name: str = str(), 
            instructions: str = str(), model: str = "gpt-3.5-turbo", tools: List[dict] = list(), 
            tool_function_mapper: Dict[str, Callable] = dict(), tool_function_callable_kwargs: Dict[str, Any] = dict(), 
            thread_id: str = str(), conversation_mode: bool = False, base_url: str = None, **kwargs) -> None:
        """
        Initializes the service with the OpenAI API key and configuration for using specific GPT models.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            assistant_name (str): The name of the assistant, no more than 256 characters.
            instructions (str, optional): The system instructions that the assistant uses, no more than 256,000 characters.
            model (str, optional): ID of the GPT model to use.
                See the [model endpoint compatibility](https://platform.openai.com/docs/models/model-endpoint-compatibility)
                table for details on which models work with the Chat API. Default "gpt-3.5-turbo".
            tools (list, optional) : A list of tool enabled on the assistant. There can be a maximum of 128 tools per assistant.
                Tools can be of types code_interpreter, file_search, or function.
            tool_function_mapper (Dict[str, Callable]): A mapper to associate a `tool_function` defined in the Assistant with a python function produces the output value.
            tool_function_callable_kwargs (Dict[str, Callable]): A dict of additional keyword arguments to be passed to the tool function callables.
            thread_id (str, optional): The identifier of a context thread, which can be referenced in OpenAI API endpoints.
            conversation_mode (bool): If True, retains the conversation context. If `thread_id` is provided, this value is set to True. Default is False.
            **kwargs: Additional arguments to customize the API calls.
        """
        super().__init__(
            openai_secret_key=openai_secret_key,
            model=model,
            conversation_mode=conversation_mode,
            base_url=base_url,
            **kwargs,
        )
        
        # Prepare the additional API arguments by filtering out irrelevant parameters.
        openai_param_list = [param_name for param_name in signature(self.client.beta.assistants.create).parameters]
        self.openai_args_dict = {key: value for key, value in kwargs.items() if key in openai_param_list}
        self.assistant = self.client.beta.assistants.create(
            name=assistant_name,
            instructions=instructions,
            model=model,
            tools=tools,
            **kwargs,
        )

        function_tools = filter(lambda tool: tool.get("type")=="function", tools)
        self.functions = [
            AssistantFunction(function_definition_dict=function["function"], tool_function_mapper=tool_function_mapper,
                tool_function_callable_kwargs=tool_function_callable_kwargs)
            for function in function_tools
        ]
        self.latest_tool_call_result = dict()
        self.latest_tool_call_trace = list()

        if (thread_id):
            conversation_mode = True
            self.conversation_mode = True
            self.__thread = self.client.beta.threads.retrieve(thread_id=thread_id)
        elif (conversation_mode):
            self.__thread = self.client.beta.threads.create()
        else:
            self.__thread = None

    @property
    def thread(self) -> Thread:
        """Return the current mounted thread."""
        if (self.conversation_mode):
            return self.__thread
        else:
            return None
    
    @thread.setter
    def thread(self, value):
        if (self.conversation_mode or value == None):
            self.__thread = value
        else:
            raise RuntimeWarning("The assistant with `conversation_mode=False` does not have thread instance. Nothing happened.")

    def refresh_thread(self) -> bool:
        """Clear the current thread and create a new one. 
        If `conversation_mode` is False, nothing will happen.
        
        Returns:
            is_successful (bool): Indidate if the thread is refreshed.
        """
        try:
            if (self.clear_thread()):
                self.__thread = self.client.beta.threads.create()
                return True
            else:
                return False
        except:
            return False
        
    def clear_thread(self):
        """Clear the current thread. 
        If `conversation_mode` is False, nothing will happen.
        
        Returns:
            is_successful (bool): Indidate if the thread is cleared.
        """
        try:
            if (self.conversation_mode):
                is_successful = self.delete_thread(
                    openai_secret_key=self.client.api_key,
                    thread_id=self.__thread.id,
                    base_url=str(self.client.base_url),
                )
                if (is_successful):
                    self.thread = None
                return is_successful
        except:
            return False


    @classmethod
    def get_thread_messages(
        cls,
        openai_secret_key: str,
        thread_id: str,
        limit: int = 20,
        base_url: str = None,
    ) -> Tuple[bool, List[Dict[str, str]]]:
        """Get the messages of a thread with the given ID.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            thread_id (str): The ID of the thread the messages belong to.
            limit (str): A limit on the number of messages to be returned. Limit can range between 1 and 100, and the default is 20.
        
        Returns:
            is_successful (bool): Indidate if the messages are successfully retrieved.
            messages (list): A list of simplified messages retrieved from the OpenAI server.
        """
        # TODO (Zhong): Apply a unified exception handler?
        try:
            client = build_openai_client(openai_secret_key, base_url=base_url)
            thread_messages = client.beta.threads.messages.list(thread_id=thread_id, limit=limit).data
            
            simplified_messages = list()
            for thread_message in thread_messages:
                message = {
                    "role": thread_message.role,
                    "text_value": thread_message.content[0].text.value,
                }
                simplified_messages.append(message)
                continue

            return True, simplified_messages[::-1]
        except:
            return False, list()
        
    @classmethod
    def get_thread_summary(cls, openai_secret_key: str, thread_id: str, base_url: str = None) -> Tuple[bool, str]:
        """Summarize the information of a thread and extract key information.
        TODO (Zhong): Use regular expression to better extracting key information.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            thread_id (str): The ID of the thread the messages belong to.
        
        Returns:
            is_successful (bool): Indidate if the messages are successfully retrieved and summarized.
            summary (str): The summarized message of the thread.
        """
        is_successful, messages = cls.get_thread_messages(openai_secret_key, thread_id, base_url=base_url)
        assistant_messages = [message for message in messages if message.get("role", None) == "assistant"]
        summary = assistant_messages[-1].get("text_value", str())
        return is_successful, summary

    @classmethod
    def delete_thread(cls, openai_secret_key: str, thread_id: str, base_url: str = None):
        """Delete a thread with the given ID.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            thread_id (str): The ID of the thread to delete.
        
        Returns:
            is_successful (bool): Indidate if the thread is deleted.
        """
        client = build_openai_client(openai_secret_key, base_url=base_url)
        try:
            response = client.beta.threads.delete(thread_id=thread_id)
            response_dict = response.to_dict()
            is_successful = response_dict.get("deleted", False)
            return is_successful
        except (NotFoundError):
            return True
        except (Exception):
            return False
        
    @classmethod
    def delete_threads(cls, openai_secret_key: str, thread_id_list: List[str], base_url: str = None):
        """Delete a thread with the given ID.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            thread_id_list (List[str]): A list of the thread ID of those to be deleted.
        
        Returns:
            is_successful (bool): Indidate if the threads are all deleted.
            deleted_thread_id_list (list): Indidate if the threads are deleted.
        """
        is_successful = True
        deleted_thread_id_list = list()
        for thread_id in thread_id_list:
            is_deleted = cls.delete_thread(
                openai_secret_key=openai_secret_key,
                thread_id=thread_id,
                base_url=base_url,
            )
            if (is_deleted):
                deleted_thread_id_list.append(thread_id)
            else:
                is_successful = False
            continue
        return is_successful, deleted_thread_id_list
    
    def __run_thread(self, prompt: str, thread: Thread = None) -> None:
        """Sends a prompt to GPT assistant and retrieves the response.

        Args:
            prompt (str): The prompt or question to send to GPT.
            thread (Thread, optional): The thread instance where the conversation to be held. Default None.
                                    If the assistant is not in conversation_mode, the thread instance should be provided.
        """
        if (thread == None and self.conversation_mode):
            thread = self.thread
        elif (thread == None and not self.conversation_mode):
            raise Exception("The Thread instance should be provided if the assistant is not in conversation_mode.")
        
        runs: List[Run] = self.client.beta.threads.runs.list(thread_id=thread.id).data
        if (runs):
            latest_run = runs[0]
            if (latest_run.status in PENDING_STATUS_LIST): # If the latest Run instance is in progress, cancel it.
                _ = self.client.beta.threads.runs.cancel(run_id=latest_run.id, thread_id=thread.id)

        out_message = self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )
        with self.client.beta.threads.runs.stream(
            assistant_id=self.assistant.id,
            thread_id=thread.id,
            event_handler=EventHandler(self)
        ) as stream:
            stream.until_done()
            run = getattr(stream, "current_run", None)

        if run is None:
            raise AssistantRunError(
                code="run_missing",
                message="Assistant run missing after streaming",
                status=None,
            )
        if run.status not in [COMPLETED_STATUS] + PENDING_STATUS_LIST:
            last_error = getattr(run, "last_error", None)
            error_code = getattr(last_error, "code", None) or getattr(last_error, "type", None) or "run_failed"
            error_message = getattr(last_error, "message", None) or f"Assistant run ended with status '{run.status}'."
            raise AssistantRunError(code=error_code, message=error_message, status=run.status)

        return run

    def __retrieve_response_content(
            self, 
            thread: Thread = None, 
            wait_seconds: float = 0.5,
            num_tol: int = 3,
        ):
        """Block until an assistant message appears in the thread or timeout.

        Args:
            thread (Thread, optional): The thread whose messages to inspect.
            wait_seconds (float): Max seconds to wait for assistant reply.
            num_tol (float): number of trials for getting assistant reply.

        Returns:
            str: The text content of the first assistant message (most-recent).

        Raises:
            RuntimeError: If no assistant message is found within `timeout`.
        """
        if (thread == None and self.conversation_mode):
            thread = self.thread
        elif (thread == None and not self.conversation_mode):
            raise ValueError("The Thread instance should be provided if the assistant is not in conversation_mode.")

        msgs = self.client.beta.threads.messages.list(
            thread_id=thread.id,
            order="desc"
        ).data

        if msgs and msgs[0].role == "assistant":
            return msgs[0].content[0].text.value

        for i in range(num_tol):
            # wait for the msg to sync
            time.sleep(wait_seconds)

            msgs = self.client.beta.threads.messages.list(
                thread_id=thread.id,
                order="desc"
            ).data

            if msgs and msgs[0].role == "assistant":
                return msgs[0].content[0].text.value

        # raise if the last message is not from assistant
        latest_role = msgs[0].role if msgs else "none"
        raise AssistantRunError(
            code="no_reply",
            message=(
                f"No assistant reply received within {wait_seconds:.1f}s; "
                f"latest message role: {latest_role}"
            ),
            status="no_reply",
        )

    def ask_gpt(self, prompt: str) -> Tuple[bool, int, str]:
        """Sends a prompt to GPT assistant and retrieves the response.

        Args:
            prompt (str): The prompt or question to send to GPT.

        Returns:
            is_valid (bool): Whether the API key is valid.
            status_code (int): The HTTP status code from the API response.
            response_content (str): The actual response from GPT or an error message.
        """
        if (self.client.api_key == DEFAULT_OPENAI_API_KEY):
            return False, 500, "OpenAI Secret Key does not exist."

        log_openai_meta(
            LOGGER,
            "openai_assistant.request",
            OpenAIMeta(
                openai_runtime=OPENAI_RUNTIME,
                model=self.model,
            ),
        )

        try:
            response_content = str()
            run_id = None
            conversation_id = None
            self.latest_tool_call_result.clear()
            self.latest_tool_call_trace.clear()
            if (self.conversation_mode):
                user_message = {
                    "role": "user",
                    "content": prompt,
                }
                run = self.__run_thread(prompt=prompt)
                run_id = getattr(run, "id", None)
                conversation_id = getattr(run, "thread_id", None)

                response_content = self.__retrieve_response_content()
                self.messages.append(user_message)
                self.messages.append({
                    "role": "assistant",
                    "content": response_content,
                })
            else:
                thread = self.client.beta.threads.create()
                conversation_id = getattr(thread, "id", None)
                run = self.__run_thread(prompt=prompt, thread=thread)
                run_id = getattr(run, "id", None)
                response_content = self.__retrieve_response_content(thread=thread)
                _ = self.delete_thread(
                    openai_secret_key=self.client.api_key,
                    thread_id=thread.id,
                    base_url=str(self.client.base_url),
                )

            log_openai_meta(
                LOGGER,
                "openai_assistant.success",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    response_id=run_id,
                    conversation_id=conversation_id,
                    tool_call_count=len(self.latest_tool_call_result),
                ),
            )

            # Successfully received a response from OpenAI.
            return (True, 200, response_content)
        except AssistantRunError as e:
            error_code = getattr(e, "code", None) or "run_failed"
            is_valid = False
            status_code = 500
            user_message = str(e)

            if error_code in ("insufficient_quota", "billing_hard_limit_exceeded"):
                is_valid = True
                status_code = 429
                user_message = "OpenAI balance appears exhausted. Please check billing or try again later."
            elif error_code in ("rate_limit_exceeded", "rate_limit"):
                is_valid = True
                status_code = 429
                user_message = f"OpenAI: {user_message}"
            elif error_code in ("authentication_error", "invalid_api_key", "permission_denied"):
                is_valid = False
                status_code = 401
                user_message = "Authentication Failed: Invalid OpenAI Secret Key."
            elif error_code in ("server_error", "internal_server_error"):
                is_valid = False
                status_code = 500
                user_message = "OpenAI Internal Server Error. Unable to verify."
            elif error_code == "no_reply":
                is_valid = False
                status_code = 504
                user_message = "OpenAI Assistant did not return a reply. Please try again shortly."
            else:
                user_message = f"OpenAI Assistant run failed: {user_message}"

            log_openai_meta(
                LOGGER,
                "openai_assistant.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    tool_call_count=len(self.latest_tool_call_result),
                    openai_error_code=error_code,
                ),
                error=str(e),
                status_code=status_code,
            )

            return (is_valid, status_code, user_message)
        except RateLimitError as e:
            log_openai_meta(
                LOGGER,
                "openai_assistant.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    openai_error_code="rate_limit_exceeded",
                ),
                error=str(e),
            )
            return (True, 429, "Rate Limit Error: You exceeded your current OpenAI API quota or Rate Limit, please check your plan and billing details.")
        except BadRequestError as e:
            log_openai_meta(
                LOGGER,
                "openai_assistant.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    openai_error_code="bad_request",
                ),
                error=str(e),
            )
            return (True, 400, "Bad Request: Your OpenAI API Key is valid, but you sent a bad request.")
            # raise e
        except APITimeoutError as e:
            log_openai_meta(
                LOGGER,
                "openai_assistant.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    openai_error_code="timeout",
                ),
                error=str(e),
            )
            return (False, 500, "OpenAI Assistant API Timeout.")
        except AuthenticationError as e:
            log_openai_meta(
                LOGGER,
                "openai_assistant.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    openai_error_code="authentication_error",
                ),
                error=str(e),
            )
            return (False, 401, "Authentication Failed: Invalid OpenAI Secret Key.")
        except InternalServerError as e:
            log_openai_meta(
                LOGGER,
                "openai_assistant.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    openai_error_code="internal_server_error",
                ),
                error=str(e),
            )
            return (False, 500, "OpenAI Internal Server Error. Unable to verify.")
        except APIError as e:
            log_openai_meta(
                LOGGER,
                "openai_assistant.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    openai_error_code="api_error",
                ),
                error=str(e),
            )
            return (False, 500, "API Error: " + str(e))
        except Exception as e:
            log_openai_meta(
                LOGGER,
                "openai_assistant.error",
                OpenAIMeta(
                    openai_runtime=OPENAI_RUNTIME,
                    model=self.model,
                    openai_error_code="unexpected_error",
                ),
                error=str(e),
            )
            return (False, 500, "An unexpected error occurred: " + str(e))
    
    def pre_process(self, input_prompt: str) -> str:
        """Process the input prompt before sending to OpenAI.
        
        Args:
            input_prompt (str): The input prompt to be processed.

        Returns:
            str: The processed prompt text.
        """
        pass
        return input_prompt

    def post_process(self, response_content: str, is_finishing: bool) -> str:
        """Process the `response_content` from the agent.

        Args:
            response_content (str): The response from GPT.
            is_finishing (bool): A flag indicating if the job of current agent can be completed.
        
        Returns:
            processed_response_content (str): The response content after process.
        """
        # remember we want to be able to hide output from user
        # response_content = response_content.strip("```")
        # response_content = response_content.strip("\"\"\"")
        pass
        return response_content

    def detect_vicious_output(self, initial_processed_response_content: str):
        pass

    def __repr__(self):
        return f"OpenAIAssistant('{self.assistant.name}', '{self.assistant.model}')"

    def __del__(self):
        try:
            _ = self.client.beta.assistants.delete(self.assistant.id)
        except:
            pass

#endregion
