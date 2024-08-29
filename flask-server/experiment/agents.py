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
from config import BASEDIR
from os import path
from services import OpenAIAssistant

MODEL_VERSION = "gpt-4o"
# MODEL_VERSION = "gpt-4o-2024-05-13"

class QuestionAnalyzerAssistant(OpenAIAssistant):
    """The agent acting as a Question Analyzer."""

    def __init__(self, openai_secret_key: str, conversation_mode: bool = False) -> None:
        """
        Initializes the QuestionAnalyzerAssistant agent with the OpenAI API key.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            conversation_mode (bool): If True, retains the conversation context. Default is False.
        """
        instructions = open(path.join(BASEDIR, "prompts", "question_analyzer-v3.txt")).read()
        super().__init__(openai_secret_key, 
            assistant_name="Question Analyzer", 
            instructions=instructions, 
            model=MODEL_VERSION, 
            conversation_mode=False
        )

class MetricsPlannerAssistant(OpenAIAssistant):
    """The agent acting as a Question Analyzer."""

    def __init__(self, openai_secret_key: str, conversation_mode: bool = False) -> None:
        """
        Initializes the QuestionAnalyzerAssistant agent with the OpenAI API key.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            conversation_mode (bool): If True, retains the conversation context. Default is False.
        """
        instructions = open(path.join(BASEDIR, "prompts", "metrics_planner-v2")).read()
        super().__init__(openai_secret_key, 
            assistant_name="Question Analyzer", 
            instructions=instructions, 
            model=MODEL_VERSION, 
            conversation_mode=False
        )

class MutantPlannerAssistant(OpenAIAssistant):
    """The agent acting as a Mutant Planner."""

    def __init__(self, openai_secret_key: str, conversation_mode: bool = False) -> None:
        """
        Initializes the MutantPlannerAssistant agent with the OpenAI API key.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            conversation_mode (bool): If True, retains the conversation context. Default is False.
        """
        instructions = open(path.join(BASEDIR, "prompts", "mutant_planner-v1.txt")).read()
        super().__init__(openai_secret_key, 
            assistant_name="Mutant Planner", 
            instructions=instructions, 
            model=MODEL_VERSION, 
            conversation_mode=False
        )
