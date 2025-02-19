#! python3
# -*- encoding: utf-8 -*-
'''
Three OpenAI Assistant Agents:
- Question Analyzer: Decomposing and Revising scientific questions for protein simulations. 
- Metrics Planner: An expert in planning "target computational metrics" based on a user-provided natural language description of "the property of interest of the protein".
- Mutant Planner: An expert in translating natural language descriptions of mutation plans into precise EnzyHTP syntax.

@File    :   agents.py
@Created :   2024/08/28 15:07
@Author  :   Zhong, Yinjie
@Contact :   yinjie.zhong@vanderbilt.edu
'''

# Here put the import lib.
from os import path
from string import Template
from json import load
from typing import List, Tuple, Union
from typing_extensions import Annotated

from config import BASEDIR
from services import OpenAIAssistant

from .models import Experiment
from .agent_tool_functions import TOOL_FUNCTION_MAPPER

from enzy_htp import PDBParser
from enzy_htp.core import _LOGGER
from enzy_htp.structure import Residue
from enzy_htp.mutation.mutation_pattern import decode_position_pattern

PROMPTS_DIRECTORY = path.join(BASEDIR, "prompts")
# MODEL_VERSION = "gpt-4o"
MODEL_VERSION = "gpt-4o-2024-11-20"

class QuestionAnalyzerAssistant(OpenAIAssistant):
    """The agent acting as a Question Analyzer."""
    
    experiment: Experiment
    completion_message: str = "Question Confirmed!"
    starting_message_template = "Please start to analyze user questions."

    def __init__(self, openai_secret_key: str, thread_id: str = str(), conversation_mode: bool = False, experiment: Experiment = None) -> None:
        """
        Initializes the QuestionAnalyzerAssistant agent with the OpenAI API key.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            thread_id (str, optional): The identifier of a context thread, which can be referenced in OpenAI API endpoints.
            conversation_mode (bool): If True, retains the conversation context. Default is False.
            experiment (Experiment): The Experiment instance calling this assistant.
        """
        self.experiment = experiment
        instructions = str()
        tools = list()

        with open(path.join(PROMPTS_DIRECTORY, "question_analyzer-v4.txt")) as fobj:
            instructions = fobj.read()
        with open(path.join(PROMPTS_DIRECTORY, "question_analyzer_functions.json")) as json_fobj:
            tool_functions: List[dict] = load(json_fobj)
            tools = [
                {
                    "type": "function",
                    "function": tool_function
                } for tool_function in tool_functions
            ]
        super().__init__(openai_secret_key, 
            assistant_name="Question Analyzer", 
            instructions=instructions, 
            model=MODEL_VERSION,
            tools=tools,
            tool_function_mapper=TOOL_FUNCTION_MAPPER,
            thread_id=thread_id,
            conversation_mode=conversation_mode,
            tool_function_callable_kwargs={
                "experiment": experiment
            },
        )

class MetricsPlannerAssistant(OpenAIAssistant):
    """The agent acting as a Metrics Planner."""
    
    experiment: Experiment
    completion_message: str = "Computational Details Confirmed!"
    starting_message_template = "Please use the following information to config metrics. \n$summary"

    def __init__(self, openai_secret_key: str, thread_id: str = str(), conversation_mode: bool = False, experiment: Experiment = None) -> None:
        """
        Initializes the MetricsPlannerAssistant agent with the OpenAI API key.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            thread_id (str, optional): The identifier of a context thread, which can be referenced in OpenAI API endpoints.
            conversation_mode (bool): If True, retains the conversation context. Default is False.
            experiment (Experiment): The Experiment instance calling this assistant.
        """
        self.experiment = experiment
        instructions = str()
        tools = list()

        with open(path.join(PROMPTS_DIRECTORY, "metrics_planner-v3.txt")) as txt_fobj:
            instructions = txt_fobj.read()
            with open(path.join(PROMPTS_DIRECTORY, "supported_metrics_reference.txt")) as ref_fobj:
                instructions = Template(instructions).safe_substitute({
                    "REPLACEMARK": ref_fobj.read(),
                }) 
        with open(path.join(PROMPTS_DIRECTORY, "metrics_planner_functions.json")) as json_fobj:
            tool_functions: List[dict] = load(json_fobj)
            tools = [
                {
                    "type": "function",
                    "function": tool_function
                } for tool_function in tool_functions
            ]
        super().__init__(openai_secret_key, 
            assistant_name="Metrics Planner", 
            instructions=instructions, 
            model=MODEL_VERSION,
            tools=tools,
            tool_function_mapper=TOOL_FUNCTION_MAPPER,
            thread_id=thread_id,
            conversation_mode=conversation_mode,
            tool_function_callable_kwargs={
                "experiment": experiment
            },
        )

class MutantPlannerAssistant(OpenAIAssistant):
    """The agent acting as a Mutant Planner."""
    
    experiment: Experiment
    completion_message: str = "Experiment has been set up successfully!"
    starting_message_template = "Please use the following information to config mutants. \n$summary"

    def __init__(self, openai_secret_key: str, thread_id: str = str(), conversation_mode: bool = False, experiment: Experiment = None) -> None:
        """
        Initializes the MutantPlannerAssistant agent with the OpenAI API key.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            thread_id (str, optional): The identifier of a context thread, which can be referenced in OpenAI API endpoints.
            conversation_mode (bool): If True, retains the conversation context. Default is False.
            experiment (Experiment): The Experiment instance calling this assistant.
        """
        self.experiment = experiment
        instructions = str()
        tools = list()
        with open(path.join(PROMPTS_DIRECTORY, "mutant_planner-v2.txt")) as fobj:
            instructions = fobj.read()
        with open(path.join(PROMPTS_DIRECTORY, "mutant_planner_functions.json")) as json_fobj:
            tool_functions: List[dict] = load(json_fobj)
            tools = [
                {
                    "type": "function",
                    "function": tool_function
                } for tool_function in tool_functions
            ]
        super().__init__(openai_secret_key, 
            assistant_name="Mutant Planner", 
            instructions=instructions, 
            model=MODEL_VERSION,
            tools=tools,
            tool_function_mapper=TOOL_FUNCTION_MAPPER,
            thread_id=thread_id,
            conversation_mode=conversation_mode,
            tool_function_callable_kwargs={
                "experiment": experiment
            },
        )
    
    def post_process(self, response_content: str, is_finishing: bool) -> Tuple[str, str]:
        """post process every message of agent based on
        - response pattern
        - is_finishing
        
        Returns:
            response_content, response_content_user_see"""
        # here convert Output: xxx to the JSON you need in parse_agent_response_content
        # remember we want to be able to hide output from user
        

class TimezoneConsultantAssistant(OpenAIAssistant):
    """The agent acting as a Time Zone Consultant.
    The agent is for test use only.
    """

    def __init__(self, openai_secret_key: str, thread_id: str = str(), conversation_mode: bool = False) -> None:
        """
        Initializes the MutantPlannerAssistant agent with the OpenAI API key.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            thread_id (str, optional): The identifier of a context thread, which can be referenced in OpenAI API endpoints.
            conversation_mode (bool): If True, retains the conversation context. Default is False.
        """
        instructions = str()
        with open(path.join(PROMPTS_DIRECTORY, "timezone_consultant.txt")) as fobj:
            instructions = fobj.read()
        super().__init__(openai_secret_key, 
            assistant_name="Time Zone Consultant", 
            instructions=instructions, 
            model=MODEL_VERSION,
            thread_id=thread_id,
            conversation_mode=conversation_mode,
        )


AGENT_MAPPER = {
    # -1: TimezoneConsultantAssistant,
    0: QuestionAnalyzerAssistant,
    1: MetricsPlannerAssistant,
    2: MutantPlannerAssistant,
}

DefinedAgent = Annotated[
    Union[
        QuestionAnalyzerAssistant,
        MetricsPlannerAssistant,
        MutantPlannerAssistant,
    ],
    "DefinedAgent",
]
