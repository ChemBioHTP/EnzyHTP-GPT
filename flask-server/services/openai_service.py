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
import openai

from inspect import signature

# Here put local imports.
from config import DEFAULT_OPENAI_API_KEY

class OpenAIService:
    """Handles interactions with OpenAI's API, particularly GPT models."""

    client: openai.OpenAI

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
