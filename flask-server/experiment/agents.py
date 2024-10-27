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
from typing import List, Union

from config import BASEDIR
from services import OpenAIAssistant

from models import Experiment

from enzy_htp import PDBParser
from enzy_htp.core import _LOGGER
from enzy_htp.structure import Residue
from enzy_htp.mutation.mutation_pattern import decode_position_pattern

PROMPTS_DIRECTORY = path.join(BASEDIR, "prompts")
MODEL_VERSION = "gpt-4o"
# MODEL_VERSION = "gpt-4o-2024-05-13"

class QuestionAnalyzerAssistant(OpenAIAssistant):
    """The agent acting as a Question Analyzer."""
    
    experiment: Experiment

    def __init__(self, openai_secret_key: str, thread_id: str = str(), conversation_mode: bool = False, experiment: Experiment = None) -> None:
        """
        Initializes the QuestionAnalyzerAssistant agent with the OpenAI API key.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            thread_id (str, optional): The identifier of a context thread, which can be referenced in OpenAI API endpoints.
            conversation_mode (bool): If True, retains the conversation context. Default is False.
            experiment (Experiment): The Experiment instance calling this assistant.
        """
        tool_function_mapper = {
            "find_residue_around": self.find_residue_around,
            "find_residue_by_name": self.find_residue_by_name,
        }
        self.experiment = experiment
        instructions = str()
        tools = list()

        with open(path.join(PROMPTS_DIRECTORY, "question_analyzer-v3.txt")) as fobj:
            instructions = fobj.read()
        with open(path.join(PROMPTS_DIRECTORY, "question_analyzer_functions.json")) as json_fobj:
            tool_functions: List[dict] = load(json_fobj)
            tools = [
                {
                    "type": "function",
                    "function": tool_function.update(
                        {
                            "mapped_callable": tool_function_mapper.get(tool_function.get("name"), None)
                        }
                    )
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

    def find_residue_around(self, target_residue: str, distance: Union[int, str]) -> list:
        """Find the residues around a specific residue.
        
        Args:
            target_residue (str): The chain id and residue index of the target residue. Example: A.100.
            distance (int | str): The distance cutoff for finding the surrounding residues. Unit: Angstrom.
        
        Returns:
            residues_key_list: A list of included residues.
        """
        structure = PDBParser().get_structure(self.experiment.pdb_filepath)
        try:
            chain_id = target_residue.split(".")[0]
            res_id = target_residue.split(".")[1]
            target_residue_instance = structure.find_residue_with_key((chain_id, int(res_id)))
            if (target_residue_instance is None):
                return str()
            else:
                position_pattern = f"resi {res_id} around {distance}"
                selected_residue_tuples: List[tuple] = decode_position_pattern(position_pattern)
                residues_key_list = [f"{residue_tuple[0]}.{residue_tuple[1]}" for residue_tuple in selected_residue_tuples]
                return residues_key_list
        except Exception as e:
            _LOGGER.error(e)
            return str()

    def find_residue_by_name(self, name: str) -> str:
        """Find the key of a residue by its name.
        
        Args:
            name (str): The 3-letter PDB name of the residue.
        
        Returns:
            residue_key_str (str): The key of a residue.
        """
        structure = PDBParser().get_structure(self.experiment.pdb_filepath)
        residues = structure.find_residue_name(name=name)
        if (len(residues) > 0):
            residue_key_str = residues[0].key_str
            return residue_key_str
        else:
            return str()

class MetricsPlannerAssistant(OpenAIAssistant):
    """The agent acting as a Metrics Planner."""
    
    experiment: Experiment

    def __init__(self, openai_secret_key: str, thread_id: str = str(), conversation_mode: bool = False, experiment: Experiment = None) -> None:
        """
        Initializes the MetricsPlannerAssistant agent with the OpenAI API key.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            thread_id (str, optional): The identifier of a context thread, which can be referenced in OpenAI API endpoints.
            conversation_mode (bool): If True, retains the conversation context. Default is False.
            experiment (Experiment): The Experiment instance calling this assistant.
        """
        tool_function_mapper = {
            "find_target_protein_path": self.find_target_protein_path,
            "find_residue_by_name": self.find_residue_by_name,
        }
        self.experiment = experiment
        instructions = str()
        tools = list()

        with open(path.join(PROMPTS_DIRECTORY, "metrics_planner-v2.txt")) as txt_fobj:
            instructions = txt_fobj.read()
        with open(path.join(PROMPTS_DIRECTORY, "metrics_planner_functions.json")) as json_fobj:
            tool_functions: List[dict] = load(json_fobj)
            tools = [
                {
                    "type": "function",
                    "function": tool_function.update(
                        {
                            "mapped_callable": tool_function_mapper.get(tool_function.get("name"), None)
                        }
                    )
                } for tool_function in tool_functions
            ]
        super().__init__(openai_secret_key, 
            assistant_name="Metrics Planner", 
            instructions=instructions, 
            model=MODEL_VERSION,
            tools=tools,
            thread_id=thread_id,
            conversation_mode=conversation_mode,
        )

    def find_target_protein_path(self) -> str:
        """Return the PDB filepath of the protein.
        
        Returns:
            pdb_filepath (str): The PDB filepath of the protein.
        """
        return self.experiment.pdb_filepath
    
    def find_residue_by_name(self, name: str) -> str:
        """Find the key of a residue by its name.
        
        Args:
            name (str): The 3-letter PDB name of the residue.
        
        Returns:
            residue_key_str (str): The key of a residue.
        """
        structure = PDBParser().get_structure(self.experiment.pdb_filepath)
        residues = structure.find_residue_name(name=name)
        if (len(residues) > 0):
            residue_key_str = residues[0].key_str
            return residue_key_str
        else:
            return str()

class MutantPlannerAssistant(OpenAIAssistant):
    """The agent acting as a Mutant Planner."""
    
    experiment: Experiment

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
        with open(path.join(PROMPTS_DIRECTORY, "mutant_planner-v1.txt")) as fobj:
            instructions = fobj.read()
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