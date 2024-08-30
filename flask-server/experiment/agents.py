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
from json import load
from typing import List

from config import BASEDIR
from services import OpenAIAssistant

PROMPTS_DIRECTORY = path.join(BASEDIR, "prompts")
MODEL_VERSION = "gpt-4o"
# MODEL_VERSION = "gpt-4o-2024-05-13"

class QuestionAnalyzerAssistant(OpenAIAssistant):
    """The agent acting as a Question Analyzer."""

    def __init__(self, openai_secret_key: str, thread_id: str = str(), conversation_mode: bool = False) -> None:
        """
        Initializes the QuestionAnalyzerAssistant agent with the OpenAI API key.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            thread_id (str, optional): The identifier of a context thread, which can be referenced in OpenAI API endpoints.
            conversation_mode (bool): If True, retains the conversation context. Default is False.
        """
        instructions = open(path.join(PROMPTS_DIRECTORY, "question_analyzer-v3.txt")).read()
        tool_functions: List[dict] = load(open(path.join(PROMPTS_DIRECTORY, "question_analyzer_functions.json")))
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
            thread_id=thread_id,
            conversation_mode=conversation_mode,
        )

class MetricsPlannerAssistant(OpenAIAssistant):
    """The agent acting as a Question Analyzer."""

    def __init__(self, openai_secret_key: str, thread_id: str = str(), conversation_mode: bool = False) -> None:
        """
        Initializes the QuestionAnalyzerAssistant agent with the OpenAI API key.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            thread_id (str, optional): The identifier of a context thread, which can be referenced in OpenAI API endpoints.
            conversation_mode (bool): If True, retains the conversation context. Default is False.
        """
        instructions = open(path.join(PROMPTS_DIRECTORY, "metrics_planner-v2.txt")).read()
        super().__init__(openai_secret_key, 
            assistant_name="Question Analyzer", 
            instructions=instructions, 
            model=MODEL_VERSION,
            thread_id=thread_id,
            conversation_mode=conversation_mode,
        )

class MutantPlannerAssistant(OpenAIAssistant):
    """The agent acting as a Mutant Planner."""

    def __init__(self, openai_secret_key: str, thread_id: str = str(), conversation_mode: bool = False) -> None:
        """
        Initializes the MutantPlannerAssistant agent with the OpenAI API key.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            thread_id (str, optional): The identifier of a context thread, which can be referenced in OpenAI API endpoints.
            conversation_mode (bool): If True, retains the conversation context. Default is False.
        """
        instructions = open(path.join(PROMPTS_DIRECTORY, "mutant_planner-v1.txt")).read()
        super().__init__(openai_secret_key, 
            assistant_name="Mutant Planner", 
            instructions=instructions, 
            model=MODEL_VERSION,
            thread_id=thread_id,
            conversation_mode=conversation_mode,
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
        instructions = open(path.join(PROMPTS_DIRECTORY, "timezone_consultant.txt")).read()
        super().__init__(openai_secret_key, 
            assistant_name="Time Zone Consultant", 
            instructions=instructions, 
            model=MODEL_VERSION,
            thread_id=thread_id,
            conversation_mode=conversation_mode,
        )


AGENT_MAPPER = {
    -1: TimezoneConsultantAssistant,
    0: QuestionAnalyzerAssistant,
    1: MetricsPlannerAssistant,
    2: MutantPlannerAssistant,
}