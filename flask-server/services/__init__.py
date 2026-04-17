#! python3
# -*- encoding: utf-8 -*-
'''
This directory provides the application with services corresponding to external services and APIs.

@File    :   __init__.py
@Created :   2024/06/23 22:14
@Author  :   Zhong, Yinjie
@Contact :   yinjie.zhong@vanderbilt.edu
'''

# Here put the import lib.
from .openai_service import OpenAIChat, OpenAIAssistant as LegacyOpenAIAssistant
from .openai_response_service import OpenAIResponsesService
from .openai_runtime_facade import (
    OpenAIRuntimeFacade,
    build_openai_agent,
    get_openai_runtime,
)
OpenAIAssistant = OpenAIResponsesService if (get_openai_runtime() == "responses") else LegacyOpenAIAssistant

from .accre_slurm_service import SlurmJobData, SlurmJobRequest

from .image_service import image_path_to_src
