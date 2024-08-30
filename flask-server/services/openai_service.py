#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   openai_service.py
@Created :   2024/06/23 20:25
@Author  :   Zhong, Yinjie
@Version :   1.0
@Contact :   yinjie.zhong@vanderbilt.edu
'''

# Here put the import lib.
from typing import Tuple
from openai.types.beta.threads.run import Run
from openai.types.beta import Assistant, Thread
import openai

from inspect import signature
from time import sleep

# Here put local imports.
# from config import DEFAULT_OPENAI_API_KEY
DEFAULT_OPENAI_API_KEY = "5511667"

class OpenAIChat:
    """Handles interactions with OpenAI's Chat API, particularly GPT models."""

    client: openai.OpenAI
    conversation_mode: bool

    def __init__(self, openai_secret_key: str, model: str = "gpt-3.5-turbo", conversation_mode: bool = False, **kwargs) -> None:
        """
        Initializes the service with the OpenAI API key and configuration for using specific GPT models.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            model (str, optional): ID of the GPT model to use.
                See the [model endpoint compatibility](https://platform.openai.com/docs/models/model-endpoint-compatibility)
                table for details on which models work with the Chat API. Default "gpt-3.5-turbo".
            conversation_mode (bool): If True, retains the conversation context. Default is False.
            **kwargs: Additional arguments to customize the API calls.
        """
        self.model = model
        if (openai_secret_key):
            self.client = openai.OpenAI(api_key=openai_secret_key)
        else:
            self.client = openai.OpenAI(api_key=DEFAULT_OPENAI_API_KEY)
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

        try:
            response_content = str()
            if (self.conversation_mode):
                messages = self.messages + [{"role": "user", "content": prompt}]

                self.messages.append({
                    "role": "user",
                    "content": prompt,
                })
                response = self.client.chat.completions.create(
                    messages=messages,
                    model=self.model,
                    **self.openai_args_dict
                )
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
                response_content = response.choices[0].message.content
            
            # Successfully received a response from OpenAI.
            return (True, 200, response_content)
        except openai.RateLimitError as e:
            return (True, 429, "Rate Limit Error: You exceeded your current OpenAI API quota or Rate Limit, please check your plan and billing details.")
        except openai.BadRequestError as e:
            return (True, 400, "Bad Request: Your OpenAI Secret Key is valid, but you sent a bad request.")
        except openai.AuthenticationError as e:
            return (False, 401, "Authentication Failed: Invalid OpenAI Secret Key.")
        except openai.InternalServerError as e:
            return (False, 500, "OpenAI Internal Server Error. Unable to verify.")
        except openai.APIError as e:
            return (False, 500, "API Error: " + str(e))
        except Exception as e:
            return (False, 500, "An unexpected error occurred: " + str(e))

class OpenAIAssistant(OpenAIChat):
    """Handles interactions with OpenAI's Assistant API, particularly GPT models."""

    TERMINAL_STATUS_LIST = ["cancelled", "failed", "completed", "expired", "incomplete"]
    COMPLETED_STATUS = "completed"

    assistant: Assistant
    __thread: Thread

    def __init__(self, openai_secret_key: str, assistant_name: str = str(), instructions: str = str(), model: str = "gpt-3.5-turbo", tools: list = list(), thread_id: str = str(), conversation_mode: bool = False, **kwargs) -> None:
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
            thread_id (str, optional): The identifier of a context thread, which can be referenced in OpenAI API endpoints.
            conversation_mode (bool): If True, retains the conversation context. If `thread_id` is provided, this value is set to True. Default is False.
            **kwargs: Additional arguments to customize the API calls.
        """
        super().__init__(openai_secret_key=openai_secret_key, model=model, conversation_mode=conversation_mode, kwargs=kwargs)
        
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
        if (self.conversation_mode):
            self.__thread = value
        else:
            raise RuntimeWarning("The assistant with `conversation_mode=False` does not have thread instance. Nothing happened.")

    def refresh_thread(self) -> bool:
        """Clear the current thread and create a new one. 
        If `conversation_mode` is False, nothing will happen.
        
        Returns:
            is_successful (bool): Indidate if the thread is cleared.
        """
        try:
            if (self.conversation_mode):
                _ = self.client.beta.threads.delete(self.__thread.id)
                self.__thread = self.client.beta.threads.create()
                return True
            else:
                return False
        except:
            return False

    def ask_gpt(self, prompt: str) -> Tuple[bool, int, str]:
        """Sends a prompt to GPT assistant and retrieves the response.

        Args:
            prompt (str): The prompt or question to send to GPT.

        Returns:
            is_valid (bool): Whether the API key is valid.
            status_code (int): The HTTP status code from the API response.
            response_content (str): The actual response from GPT or an error message.
        """
        timeout_limit = 180  # Set timeout (seconds).
        refresh_sep = 2     # Set refresh interval (seconds).
        
        if (self.client.api_key == DEFAULT_OPENAI_API_KEY):
            return False, 500, "OpenAI Secret Key does not exist."

        try:
            response_content = str()
            if (self.conversation_mode):
                user_message = {
                    "role": "user",
                    "content": prompt,
                }
                out_message = self.client.beta.threads.messages.create(
                    thread_id=self.__thread.id,
                    role="user",
                    content=prompt
                )
                run = self.client.beta.threads.runs.create_and_poll(
                    thread_id=self.__thread.id,
                    assistant_id=self.assistant.id,
                )
                for i in range(0, timeout_limit, refresh_sep):
                    if (run.status not in __class__.TERMINAL_STATUS_LIST):
                        sleep(refresh_sep)
                        if i == timeout_limit - refresh_sep:
                            raise TimeoutError("Waiting for response too long.")
                        continue
                    else:
                        break

                # Update the messages of the service after the prompt is successfully processed and parsed.
                retrived_messages = self.client.beta.threads.messages.list(
                    thread_id=self.__thread.id
                )
                response_content = retrived_messages.data[0].content[0].text.value                
                if (run.status == __class__.COMPLETED_STATUS):
                    self.messages.append(user_message)
                    self.messages.append({
                        "role": "assistant",
                        "content": response_content,
                    })
            else:
                thread = self.client.beta.threads.create()
                out_message = self.client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content=prompt
                )
                run = self.client.beta.threads.runs.create_and_poll(
                    thread_id=thread.id,
                    assistant_id=self.assistant.id,
                )
                for i in range(0, timeout_limit, refresh_sep):
                    if (run.status not in __class__.TERMINAL_STATUS_LIST):
                        sleep(refresh_sep)
                        if i == timeout_limit - refresh_sep:
                            raise TimeoutError("Waiting for response too long.")
                        continue
                    else:
                        break
                retrived_messages = self.client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                response_content = retrived_messages.data[0].content[0].text.value
                _ = self.client.beta.threads.delete(thread.id)
            
            # Successfully received a response from OpenAI.
            return (True, 200, response_content)
        except openai.RateLimitError as e:
            return (True, 429, "Rate Limit Error: You exceeded your current OpenAI API quota or Rate Limit, please check your plan and billing details.")
        except openai.BadRequestError as e:
            return (True, 400, "Bad Request: Your OpenAI Secret Key is valid, but you sent a bad request.")
        except openai.AuthenticationError as e:
            return (False, 401, "Authentication Failed: Invalid OpenAI Secret Key.")
        except openai.InternalServerError as e:
            return (False, 500, "OpenAI Internal Server Error. Unable to verify.")
        except openai.APIError as e:
            return (False, 500, "API Error: " + str(e))
        except Exception as e:
            return (False, 500, "An unexpected error occurred: " + str(e))

    def __del__(self):
        _ = self.client.beta.assistants.delete(self.assistant.id)