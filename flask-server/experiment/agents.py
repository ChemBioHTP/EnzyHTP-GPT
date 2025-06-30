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
import re
from string import Template
from json import load, dumps
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

        with open(path.join(PROMPTS_DIRECTORY, "question_analyzer-v5.txt")) as fobj:
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
                metrics_reference_text = ref_fobj.read()
                instructions = Template(instructions).safe_substitute({
                    "REPLACEMARK": metrics_reference_text,
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
        
    def post_process(self, response_content: str, is_finishing: bool) -> str:
        """Process the `response_content` from the agent.

        Args:
            response_content (str): The response from GPT.
            is_finishing (bool): A flag indicating if the job of current agent can be completed.
        
        Returns:
            processed_response_content (str): The response content after process.
        """
        initial_processed_response_content = super().post_process(response_content, is_finishing)

        processed_response_content = initial_processed_response_content.replace(
            "substrate_selection_pattern", "ligand"
        ).replace(
            "pocket_selection_pattern", "region_pattern"
        )
        return processed_response_content


    def pre_process(self, input_prompt: str):
        """Process the input prompt before sending to Metrics Planner Agent.
        
        Args:
            input_prompt (str): The input prompt to be processed.

        Returns:
            str: The processed prompt text.
        """
        pre_process_template = "Please use the following information to config metrics, and print the compiled information in json format. \n$summary"
        processed_prompt = Template(pre_process_template).safe_substitute({
            "summary": input_prompt,
        })
        return processed_prompt
        
    def post_process(self, response_content: str, is_finishing: bool) -> str:
        """Process the `response_content` from the agent.

        Args:
            response_content (str): The response from GPT.
            is_finishing (bool): A flag indicating if the job of current agent can be completed.
        
        Returns:
            processed_response_content (str): The response content after process.
        """
        initial_processed_response_content = super().post_process(response_content, is_finishing)

        processed_response_content = initial_processed_response_content.replace(
            "substrate_selection_pattern", "ligand"
        )
        processed_response_content = processed_response_content.replace(
            "ligand_selection_pattern", "ligand"
        )
        processed_response_content = processed_response_content.replace(
            "pocket_selection_pattern", "region_pattern"
        )
        return processed_response_content

class MutantPlannerAssistant(OpenAIAssistant):
    """The agent acting as a Mutant Planner."""
    
    experiment: Experiment
    completion_message: str = "Experiment has been set up successfully!"

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
    
    def pre_process(self, input_prompt: str):
        """Process the input prompt before sending to Mutant Planner Agent.
        
        Args:
            input_prompt (str): The input prompt to be processed.

        Returns:
            str: The processed prompt text.
        """
        input_prompt = super().pre_process(input_prompt)
        pattern = "Mutations: (.+)\n"
        mutation_request = re.search(pattern, input_prompt, re.DOTALL)
        if (mutation_request is not None):
            return mutation_request[0].replace("Mutations:", "Input:").replace("\n", "")
        else:
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
        initial_processed_response_content = super().post_process(response_content, is_finishing)
        
        pattern = "Output: *(.+)"
        initial_processed_response_content = initial_processed_response_content.strip("`")
        if is_finishing or initial_processed_response_content.startswith("Output"):
            try:
                mutation_pattern = re.match(pattern, initial_processed_response_content).group(1).strip("\"")
                result_dict = {
                    "mutation_pattern": mutation_pattern
                }
                processed_response_content = f"```json\n{dumps(result_dict)}\n```"
                return processed_response_content
            except Exception as exc:
                _LOGGER.error(f"Failed to process `response_content`: {exc}")
                return response_content
        else:
            self.detect_vicious_output(initial_processed_response_content)  # This is about detecting potential attach, we will finish this when need it.
            processed_response_content = initial_processed_response_content   # by default result as is after stripping
            return processed_response_content

class ResultExplainerAssistant(OpenAIAssistant):
    """The agent acting as a Result Explainer."""
    
    experiment: Experiment
    # completion_message: str = "Experiment has been set up successfully!"

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
        with open(path.join(PROMPTS_DIRECTORY, "result_explainer.txt")) as fobj:
            instructions = fobj.read()
        with open(path.join(PROMPTS_DIRECTORY, "result_explainer_functions.json")) as json_fobj:
            tool_functions: List[dict] = load(json_fobj)
            tools = [
                {
                    "type": "function",
                    "function": tool_function
                } for tool_function in tool_functions
            ]
        super().__init__(openai_secret_key, 
            assistant_name="Result Explainer", 
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
