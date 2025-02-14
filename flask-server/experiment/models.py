#! python3
# -*- encoding: utf-8 -*-
'''
The entities for the Experiment module.

@File    :   models.py
@Created :   2024/01/07 17:00
@Author  :   Zhong, Yinjie
@Version :   1.0
@Contact :   yinjie.zhong@vanderbilt.edu
'''

# Here put the import lib.
from __future__ import annotations  # To enable the annotation that a staticmethod of a class returns an instance of the class.
from io import BufferedReader
from flask_login import UserMixin
from datetime import datetime, timedelta
from typing import Any, Dict, List, Union, Tuple, Callable, Literal
from json import loads, dumps
from plum import dispatch
from werkzeug.datastructures import FileStorage, ImmutableMultiDict
from pandas import DataFrame
from os import path
import os
import uuid
import re

# Here put local imports.
from context import mongo
from config import EXPERIMENT_FILE_DIRECTORY, SCRATCH_FOLDER
from auth.models import User
from .analysis import METRICS_MAPPER
from services.openai_service import OpenAIAssistant

# Here put enzy_htp modules.
from enzy_htp import interface
from enzy_htp.core.general import CaptureLogging, _LOGGER
from enzy_htp.core import (
    exception as core_exc, 
    file_system as fs
)
from enzy_htp.structure import PDBParser, StructureEnsemble
from enzy_htp.preparation.validity import is_structure_valid
from enzy_htp.mutation.mutation_pattern import api as pattern_api
from enzy_htp.mutation_class import get_mutant_name_str, get_mutant_name_tag, generate_from_mutation_flag
from enzy_htp.mutation.api import mutate_stru
from enzy_htp.workflow.config import StatusCode

sp = PDBParser()

db = mongo.db

class Experiment():
    """Experiment Model: Experiment information."""

    __tablename__ = "experiments"
    mutant_pdb_filename = "ref_stru.pdb"

    def __init__(self, user_id: str, name: str, type: int = 0, metrics: List[Dict[str, Any]] = list(), description: str = None, **kwargs):
        """Initializes an instance of Experiment with the provided parameters.

        Args:
            user_id (str): The user ID associated with this experiment.
            name (str): The name of the experiment.
            type (int, optional): The type of the experiment (default is 0).
            metrics (List[Dict[str, Any]], optional): Metrics information about kinds of analysis to be performed and their arguments (default is an empty list).
            description (str, optional): A description of the experiment (default is None).
            kwargs: Other keyword arguments.
        """
        self.type = type
        self.name = name
        self.description = description
        self.user_id = user_id
        self.metrics = metrics
        self.constraints = kwargs.get("constraints", list())
        self.id = kwargs.get("id", str(uuid.uuid4()))
        self.created_time = kwargs.get("created_time", datetime.now())
        self.updated_time = kwargs.get("updated_time", datetime.now())
        self.pdb_filename = kwargs.get("pdb_filename", None)
        # self.results: List[dict] = kwargs.get("results", list())
        self.slurm_job_uuid = kwargs.get("slurm_job_uuid", None)
        self._status = kwargs.get("status", StatusCode.CREATED)
        self._progress = kwargs.get("progress", 0.0)
        self.mutation_pattern = kwargs.get("mutation_pattern", "WT")
        self.current_assistant_type = kwargs.get("current_assistant_type", 0)  # 0: Question Analyzer; 1: Metrics Planner; 2: Mutant Planner.
        self.thread_id_list: List[str] = kwargs.get("thread_id_list", list())
        self.current_thread_id = kwargs.get("current_thread_id", str())
        self.chat_messages: List[Dict[str, str]] = kwargs.get("thread_messages", list())
        self.summon_next_agent = kwargs.get("summon_next_agent", False)
        self.summon_upload_pdb = kwargs.get("summon_upload_box", False)
    
    @staticmethod
    def get(id: str) -> Experiment | None:
        """Get experiment instance with given ID.
        
        Args:
            id (str): The `id` to identify an experiment.

        Returns:
            Matched Experiment instance or None.
        """
        experiment = Experiment.from_dict(db.experiments.find_one({"id": id}))
        # experiment = Experiment.query.filter_by(id=id).first()
        if (experiment):
            return experiment
        else:
            return None

    # @overload
    @staticmethod
    def get_user_experiments(user: User) -> List[Experiment]:
        """Get a list of Experiment instance of the certain user by `user_id`.
        
        Args:
            user: A `User` instance.
        """
        if hasattr(user, 'id'):
            experiment_query_result = db.experiments.find({"user_id": user.id})
            experiments = [Experiment.from_dict(experiment_dict) for experiment_dict in experiment_query_result]
            # experiment_query_result = Experiment.query.filter_by(user_id=user.id).order_by(Experiment.created_time).all()
            # experiments = [experiment for experiment in experiment_query_result]
            return experiments
        else:
            return []

    def update_attributes(self, mapper: Dict[str, Any], editable_attrs: list = list()) -> Tuple[list, list, list, str]:
        """Update the attribute of a specified instance.
        
        Args:
            instance: The instance of a class who has attributes to be updated.
            mapper (Dict[str, Any]): A dict-like mapper which contains the fields/attributes and values.
            editable_attrs (list): A list of editable attributes of the instance.

        Returns:
            updated_attrs (list): A list of updated attributes.
            blocked_attrs (list): A list of blocked attributes (Fields that are not editable).
            nonexistent_attrs (list): A list of nonexistent attributes (Fields that the instance does not have).
            message (str): A string value describing the updating.
        """
        updated_attrs = list()
        blocked_attrs = list()
        nonexistent_attrs = list()

        for field_name, field_value in mapper.items():
            if (hasattr(self, field_name)):
                if (not editable_attrs) or (field_name in editable_attrs):
                    if (field_value != None):
                        setattr(self, field_name, field_value)
                        db.experiments.update_one({"id": self.id}, {"$set": {field_name: field_value, "updated_time": datetime.now()}})
                        updated_attrs.append(field_name)
                    continue
                else:
                    blocked_attrs.append(field_name)
                    continue
            else:
                nonexistent_attrs.append(field_name)
                continue

        message = str()
        if (updated_attrs):
            message += f"Updated attribute(s): {', '.join(updated_attrs)}. "
        if (blocked_attrs):
            message += f"Uneditable attribute(s): {', '.join(blocked_attrs)}. "
        if (nonexistent_attrs):
            message += f"Nonexistent attribute(s): {', '.join(nonexistent_attrs)}. "

        return updated_attrs, blocked_attrs, nonexistent_attrs, message

    def as_dict(self, stringfy_time: bool = False) -> dict:
        """Serialize the current instance to a dictionary.
        
        Args:
            stringfy_time (bool, optional): Flag indicating if to convert datetime fields to string value.
        """
        dict_data = self.__dict__
        if (stringfy_time):
            dict_data["created_time"] = str(self.created_time)
            dict_data["updated_time"] = str(self.updated_time)
        return dict_data
    
    @staticmethod
    def from_dict(experiment_dict: dict | None) -> Experiment:
        """Build an experiment instance from a dict.
        
        Args:
            experiment_dict (dict): A dictionary containing data of the experiment.
        """
        if (experiment_dict is None):
            return None
        experiment = Experiment(**experiment_dict)
        return experiment

    def serialize(self) -> str:
        """Serialize the current instance to json string."""

        dict_data = self.as_dict()
        fields_to_delete = ["_sa_instance_state", "_status", "_progress"]

        dict_data["created_time"] = str(self.created_time)
        dict_data["updated_time"] = str(self.updated_time)
        dict_data["status"] = str(self._status)
        dict_data["progress"] = str(self._progress)
        dict_data["status_text"] = StatusCode.status_text_mapper.get(self.status, self.status)
        dict_data["assistant_conversation_completed"] = self.assistant_conversation_completed

        for field_key in fields_to_delete:
            if (field_key in dict_data.keys()):
                del dict_data[field_key]
        return dumps(dict_data)
    
    def __repr__(self):
        return f"Experiment(Id: '{self.id}', Name: '{self.name}', PDB file: {self.pdb_filename if self.has_pdb_file else 'None'})"

    @property
    def pdb_filepath(self):
        if (self.pdb_filename):
            return path.join(self.directory, self.pdb_filename)
        else:
            return None

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        # if (value == StatusCode.CANCELLED):
        #     self.results.clear()
        self._status = value
        self.updated_time = datetime.now()
        return
    
    @property
    def assistant_conversation_completed(self) -> bool:
        """Indicate if the conversation with OpenAI Assistant is completed."""
        if (self.current_assistant_type > 2):
            return True
        else:
            return False
    
    @property
    def progress(self):
        return self._progress
    
    @progress.setter
    def progress(self, value):
        self._progress = value
        self.updated_time = datetime.now()
        return
    
    @property
    def mutant_count(self) -> int:
        is_successful, mutants, message = self.get_mutants()
        return len(mutants)

    @property
    def has_pdb_file(self) -> bool:
        if (self.pdb_filepath and os.path.isfile(self.pdb_filepath)):
            return True
        else:
            return False

    @property
    def directory(self) -> str:
        """The directory where the file of this experiment is saved."""
        directory_path = path.join(EXPERIMENT_FILE_DIRECTORY, self.id)
        return directory_path

    def clear_folder(self, remove_folder: bool = False):
        """Remove the folder of the current directory.
        
        Args:
            remove_folder (bool): If true, remove the folder itself as well; otherwise leave the empty folder.
        """
        fs.safe_rmdir(self.directory)
        if (remove_folder):
            return
        else:
            fs.safe_mkdir(self.directory)
    
    #region Experiment - PDB File

    @staticmethod
    def __validate_pdb(pdb_file: str | FileStorage) -> Tuple[bool, bool, str]:
        """Validate PDB file.

        Args:
            pdb_file (str or FileStorage): The filepath or FileStorage instance of the PDB file.
        
        Returns:
            is_valid (bool): Flag indicating the validity of the PDB file.
            is_supported (bool): Flag indicating if the structure is supported by EnzyHTP.
            message (str): The message describing the validity status.
        """
        pdb_filepath = str()

        from_filestorage = isinstance(pdb_file, FileStorage)
        if (from_filestorage):
            pdb_filepath = path.join(SCRATCH_FOLDER, pdb_file.filename)
            pdb_file.save(pdb_filepath)
        else:
            pdb_filepath = pdb_file
        
        is_valid = False
        is_supported = False
        message = str()
        
        with CaptureLogging(_LOGGER) as log_str:
            if (not path.isfile(pdb_filepath)):
                message = "No selected file."
            else:
                try:
                    stru = sp.get_structure(pdb_filepath)
                    is_valid = True
                except ValueError as e:
                    is_valid = False
                    message = f"Unreadable PDB file: {e}\n"
                if (stru.num_atoms > 0):
                    is_supported, intermediate_message = is_structure_valid(stru, print_report=False)
                    message = "The following errors were found in the PDB file: \n"
                    for reason, source, suggestion in intermediate_message:
                        message += f"Reason: {str(reason)}\tSource: {str(source)}\tSuggestion: {str(suggestion)};\n"
                    
                    if is_valid:
                        message = "The PDB file is valid."
                    else:
                        pass
                else:
                    is_valid = False
                    message = "This is not a PDB file."
            if (is_valid):
                message += f"\n{log_str.getvalue()}"

        if (from_filestorage):
            os.remove(pdb_filepath)
            pdb_file.stream.seek(0) # Reset the cursor for further use.
            pass
        
        return is_valid, is_supported, message

    def update_pdb(self, pdb_file: FileStorage, force_update: bool = False) -> Tuple[bool, bool, str]:
        """Update PDB file. Invalid PDB file will not be updated.

        Args:
            pdb_file (FileStorage): The FileStorage instance of the new PDB file.
            force_update (bool): Whether to skip verification and force update of PDB files.
                If True, PDB file will be updated even if the PDB file is not supported (but the PDB file must be valid).
        
        Returns:
            is_updated (bool): Flag indicating if the PDB file is updated.
            is_supported (bool): Flag indicating if the structure is supported by EnzyHTP.
            message (str): The message describing the updating.
        """
        is_updated = False
        if (fs.get_file_ext(pdb_file.filename).lower() != ".pdb"):
            return False, "This is not a PDB file."
        fs.safe_mkdir(self.directory)

        is_valid, is_supported, message = Experiment.__validate_pdb(pdb_file)
        if (is_valid and force_update):
            message = f"Force the update of PDB file. {message}"

        if (is_supported or force_update):
            is_updated = True
            if (self.pdb_filepath and path.isfile(self.pdb_filepath)):
                fs.safe_rm(self.pdb_filepath) # Delete existing file.
            self.pdb_filename = pdb_file.filename
            self.summon_upload_pdb = False
            pdb_file.save(self.pdb_filepath)
            message = f"The PDB file of the experiment {self.id} is updated. " + message
            db.experiments.update_one({"id": self.id}, {"$set": {"pdb_filename": self.pdb_filename, "summon_upload_pdb": self.summon_upload_pdb}})

        return is_updated, is_supported, message
    
    #endregion

    #region Experiment - Analysis

    def __analyze_structure_ensemble_result(
            self, stru_esm: StructureEnsemble,
        ) -> Tuple[Dict[str, bool], Dict[str, bool]]:
        """Perform the analysis based on the given StructureEnsemble instance.
        
        Args:
            stru_esm (StructureEnsemble): The StructureEnsemble instance for analysis.

        Returns:
            analysis_record_dict (Dict[str, bool]): A dictionary recording success and failure of each analysis.
            analysis_result_dict (Dict[str, bool]): A dictionary recording the result of each analysis.
        """
        analysis_result_dict = dict()   # Record analysis result.
        analysis_record_dict = dict()   # Record success or failure.
        for metric in self.metrics:
            analysis_tag = metric.get("name")   # The name of the analysis to be performed.
            try:
                analysis_params: Dict[str, Any] = metric.get("arguments", dict())
                if (analysis_tag):
                    analysis_callable = METRICS_MAPPER.get(analysis_tag)    # Get analysis callable.
                    if (isinstance(analysis_callable, Callable)):
                        analysis_params.update({    # Compose analysis arguments.
                            "stru_esm": stru_esm,
                        })
                        analysis_result_dict[analysis_tag] = analysis_callable(**analysis_params)    # Perform analysis and record result.
                        analysis_record_dict[analysis_tag] = True
            except Exception as e:
                message = f"Exception raised when analyzing '{analysis_tag}': {e}"
                analysis_record_dict[analysis_tag] = False
                _LOGGER.error(message)
            finally:
                continue

        return analysis_record_dict, analysis_result_dict
    
    def update_ensemble_and_analysis(self, mutant_name: str, topology_file: FileStorage, traj_file: FileStorage) -> Tuple[bool, str, dict, dict]:
        """Update the structure ensemble of the mutant and perform analysis.
        Invalid Trajectory file will not trigger updates to the results.
        Trajectory files will be removed after the completion of analysis.

        Args:
            mutant_name (str): The name of the mutant associated with the trajectory. e.g.: 'A##B C##D'
            topology_file (FileStorage): The FileStorage instance of the Amber prmtop file.
            traj_file (FileStorage): The FileStorage instance of the new trajectory file.
        
        Returns:
            is_valid (bool): Flag indicating the validity of the PDB file.
            message (str): The message describing the validation.
            analysis_record_dict (Dict[str, bool]): A dictionary recording success and failure of each analysis.
            analysis_result_dict (Dict[str, bool]): A dictionary recording the result of each analysis.
        """
        is_valid = False
        validation_message = str()
        analysis_record_dict = dict()
        analysis_result_dict = dict()

        save_folder = path.join(self.directory, mutant_name.replace(" ", "_"))
        fs.safe_mkdir(save_folder)
        prmtop_file_path = path.join(save_folder, topology_file.filename)
        traj_file_path = path.join(save_folder, traj_file.filename)
        ref_pdb_path = path.join(save_folder, __class__.mutant_pdb_filename)
        try:
            # Construct the reference structure PDB file.
            mutant = [generate_from_mutation_flag(mutation_str) for mutation_str in mutant_name.split("_")]
            ref_stru = mutate_stru(sp.get_structure(self.pdb_filepath), mutant=mutant)
            sp.save_structure(outfile=ref_pdb_path, stru=ref_stru)
        except Exception as e:
            _LOGGER.error(f"Exception raised when constructing mutant structure: {e}")
            # raise e
        
        topology_file.save(prmtop_file_path)
        _LOGGER.info(f"Prmtop: {prmtop_file_path}")
        traj_file.save(traj_file_path)
        _LOGGER.info(f"Trajectory: {traj_file_path}")
        try:
            stru_esm = interface.amber.load_traj(
                prmtop_path=prmtop_file_path, traj_path=traj_file_path,
                ref_pdb=ref_pdb_path
            )
            analysis_record_dict, analysis_result_dict = self.__analyze_structure_ensemble_result(stru_esm=stru_esm)
        except Exception as e:
            _LOGGER.error(f"Exception raised when parsing the structure ensemble: {e}")
            # raise e
        finally:
            fs.safe_rm(prmtop_file_path)
            fs.safe_rm(traj_file_path)
            fs.safe_rm(ref_pdb_path)
        return is_valid, validation_message, analysis_record_dict, analysis_result_dict

    def post_result(self, result_record: dict):
        """Add new result record to the experiment.
        
        Args:
            result_record_dict (dict): A dict containing the result information of one mutant.
        """
        result_record.update({
            "experiment_id": self.id,
            "pdb_filename": self.pdb_filename,
        })
        result = Result(**result_record)
        result.insert_or_update()
        return

    #endregion

    #region Experiment - Mutation TODO: Deduplication.

    def get_mutants(self) -> Tuple[bool, list, str]:
        """Get the mutant list of the current experiment instance.

        Returns:
            is_successful (bool): Flag indicating if the update is successful.
            mutants (str): The mutants assigned by the mutation pattern. None if the pattern is invalid.
            message (str): The message describing the updating.
        """
        is_successful = False
        mutants = list()
        message = str()
        if not self.has_pdb_file:
            message = "The current experiment isn't associated with any PDB file."
            return is_successful, mutants, message

        protein_stru = sp.get_structure(self.pdb_filepath)
        try:
            mutants = pattern_api.decode_mutation_pattern(protein_stru, self.mutation_pattern)
        except pattern_api.InvalidMutationPatternSyntax as e:
            message = f"Mutation pattern parsing failed due to InvalidMutationPatternSyntax: {e}"
        except core_exc.InvalidResidueCode as e:
            message = f"Mutation pattern parsing failed due to InvalidResidueCode: {e}"
        except Exception as e:
            message = f"Mutation pattern parsing failed due to Uncategorized General Exception: {e}"
        finally:
            if (not message):
                message = "Mutation pattern parsing succeeded!"
                is_successful = True
            else:
                _LOGGER.error(message)
        
        return is_successful, mutants, message

    def get_mutants_structure(self, engine: str = "pymol") -> Tuple[bool, dict, str]:
        """Get the PDB file string of the mutated structure.
        
        Args:
            engine (str, optional): The engine (method) used for determine the mutated structure
                (current available keywords): "tleap_min", "pymol" & "rosetta".
        
        Returns:
            is_successful (bool): Flag indicating if the update is successful.
            tag_structure_pairs (dict): A dictionary with mutant tags as keys and the corresponding structure as values.
            message (str): The message describing the updating.
        """
        tag_structure_pairs = dict()
        is_successful, mutants, message = self.get_mutants()
        if (is_successful):
            try:
                protein_stru = sp.get_structure(self.pdb_filepath)
                for mutant in mutants:
                    mutant_stru = mutate_stru(protein_stru, mutant, engine)
                    name_tag = get_mutant_name_str(mutant)
                    tag_structure_pairs[name_tag] = mutant_stru
                message = "Getting Mutant structure succeeded!"
            except Exception as e:
                is_successful = False
                message = f"Getting Mutant structure failed due to Exception: {e}"
        return is_successful, tag_structure_pairs, message

    def get_mutants_pdb_string(self, engine: str = "pymol") -> Tuple[bool, dict, str]:
        """Get the PDB file string of the mutated structure.
        
        Args:
            engine (str, optional): The engine (method) used for determine the mutated structure
                (current available keywords): "tleap_min", "pymol" & "rosetta".
        
        Returns:
            is_successful (bool): Flag indicating if the update is successful.
            tag_string_pairs (dict): A dictionary with mutant tags as keys and the corresponding PDB file string as values.
            message (str): The message describing the updating.
        """
        tag_string_pairs = dict()
        is_successful, tag_structure_pairs, message = self.get_mutants_structure(engine)
        if (is_successful):
            for tag, structure in tag_structure_pairs.items():
                pdb_string = sp.get_file_str(structure)
                tag_string_pairs[tag] = pdb_string
            message = "Getting Mutant PDB file string succeeded!"
        return is_successful, tag_string_pairs, message

    def make_mutant_pdb_file(self, mutant_name: str, engine: str = "pymol") -> Tuple[bool, str, str]:
        """Make the pdb file for a designated mutant associated with this experiment.
        
        Args:
            mutant_name (str): The name of the mutant associated with the trajectory. e.g.: 'A##B C##D'
            engine (str, optional): The engine (method) used for determine the mutated structure
                (current available keywords): "tleap_min", "pymol" & "rosetta".
        
        Returns:
            is_successful (bool): Flag indicating if the mutant PDB file is made.
            mutant_pdb_filepath (str): The path to the mutant PDB file.
            message (str): The message describing the mutant construction.
        """
        save_folder = path.join(self.directory, mutant_name.replace(" ", "_"))
        fs.safe_mkdir(save_folder)
        ref_pdb_path = path.join(save_folder, __class__.mutant_pdb_filename)
        try:
            # Construct the reference structure PDB file.
            mutant = [generate_from_mutation_flag(mutation_str) for mutation_str in mutant_name.split("_")]
            ref_stru = mutate_stru(sp.get_structure(self.pdb_filepath), mutant=mutant, engine=engine)
            sp.save_structure(outfile=ref_pdb_path, stru=ref_stru)
            return True, ref_pdb_path, f"The mutant `{mutant_name}` is constructed."
        except Exception as e:
            message = f"Exception raised when constructing the mutant `{mutant_name}`: {e}"
            _LOGGER.error(message)
            return False, str(), message

    def make_mutants_pdb_files(self, engine: str = "pymol") -> Tuple[bool, int, str]:
        """Make pdb files for all the mutants associated with this experiment.
        
        Args:
            engine (str, optional): The engine (method) used for determine the mutated structure
                (current available keywords): "tleap_min", "pymol" & "rosetta".
        
        Returns:
            is_successful (bool): Flag indicating if the update is successful.
            mutant_count (int): The number of mutants PDB file.
            message (str): The message describing the updating.
        """
        mutant_count = 0
        fail_count = 0
        is_successful, tag_structure_pairs, message = self.get_mutants_structure(engine)
        if (is_successful):
            for tag, structure in tag_structure_pairs.items():
                try:
                    pdb_filepath = sp.save_structure(
                        outfile=path.join(self.directory, tag, __class__.mutant_pdb_filename), 
                        stru=structure,
                    )
                    mutant_count += 1
                except:
                    _LOGGER.error(f"Failed to save file to {path.join(self.directory, tag, __class__.mutant_pdb_filename)}.")
                    fail_count += 1
                finally:
                    continue
            message = f"Mutant PDB file made: {mutant_count} success, {fail_count} failure."
        return is_successful, mutant_count, message
    
    def get_mutants_string_list(self) -> Tuple[bool, list, str]:
        """Get a list of mutant string concerning the current experiment instance.

        Returns:
            is_successful (bool): Flag indicating if the update is successful.
            mutant_string_list (list): A list of mutant string assigned by the mutation pattern. None if the pattern is invalid.
            message (str): The message describing the updating.
        """
        mutant_string_list = list()
        is_successful, mutants, message = self.get_mutants()
        if (is_successful):
            for mut in mutants:
                mutant_string_list.append(get_mutant_name_str(mut))
        return is_successful, mutant_string_list, message

    def update_mutation_pattern(self, mutation_pattern: str, freeze: bool = False) -> Tuple[bool, list, str]:
        """Update the mutation pattern of the current experiment instance.
        If the mutation pattern can be successfully parsed, the update to mutation_pattern takes place; otherwise the mutation pattern is not updated.
        
        Args:
            mutation_pattern (str): The updated mutation pattern to be assigned to the experiment.
            freeze (bool): A flag indicating whether to convert a valid random mutation pattern to the mutation pattern of the specified target mutant.

        Returns:
            is_successful (bool): Flag indicating if the update is successful.
            mutant_string_list (str): The mutants assigned by the mutation pattern. None if the pattern is invalid.
            message (str): The message describing the updating.
        """
        self.mutation_pattern = mutation_pattern
        is_successful, mutant_string_list, message = self.get_mutants_string_list()
        if (is_successful):
            if (freeze):
                self.mutation_pattern = ",".join(["{}{}{}".format("{", mutant.replace(" ", ","), "}") for mutant in mutant_string_list])
            db.experiments.update_one({"id": self.id}, {"$set": {"mutation_pattern": self.mutation_pattern, "updated_time": datetime.now()}})
        message = message.replace("parsing", "update")
        return is_successful, mutant_string_list, message

    #endregion

    #region Experiment Assistant Processing.
    def parse_agent_response_content(self, response_content: str) -> Tuple[bool, list]:
        """Update the experiment configuration information according to the response_content from GPT Agents.
        
        Args:
            response_content (str): The response content from GPT.

        Returns:
            configuration_updated (bool): Indicate if the experiment configuration is updated by the response_content from GPT Agents.
            updated_attrs (list): A list of updated attributes.
        """
        editable_attrs = ["metrics", "constraints"]

        match_rule = r"```json\n(.*?)\n```"

        match_results = re.search(match_rule, response_content, re.DOTALL)
        if (match_results):
            json_text = match_results[0].replace("```json\n", "").replace("\n```", "")
            configuration_mapper: Dict[str, Any] = loads(json_text)

            is_mutation_updated = False
            mutation_field_name = "mutation_pattern"
            if (mutation_pattern:=configuration_mapper.get(mutation_field_name)):
                is_mutation_updated, mutant_string_list, message = self.update_mutation_pattern(mutation_pattern=mutation_pattern, freeze=True)
                del configuration_mapper[mutation_field_name]

            updated_attrs, blocked_attrs, nonexistent_attrs, message = self.update_attributes(mapper=configuration_mapper, editable_attrs=editable_attrs)
            if (is_mutation_updated):
                updated_attrs.append(mutation_field_name)
            return True, updated_attrs
        else:
            return False, list()
        
    def append_thread_id_list(self, new_thread_id: str):
        """Append new chat `thread_id` to the experiment's `thread_ids` attribute, and update the `current_thread_id`.
        
        Args:
            new_thread_id (str): The new `thread_id` of the experiment.
        """
        if (new_thread_id != self.current_thread_id):
            thread_id_list = self.thread_id_list
            thread_id_list.append(new_thread_id)
            self.update_attributes(mapper={
                "thread_id_list": thread_id_list,
                "current_thread_id": new_thread_id,
            })
            return

    def append_chat_messages(self, role: Literal["user", "assistant"], text_value: str):
        """Append new chat message to the experiment.
        
        Args:
            role (Literal["user", "assistant"]): Determine if the message is from the `user` or the `assistant`.
            text_value (str): The message content.
        """
        chat_messages = self.chat_messages
        chat_messages.append({
            "role": role,
            "text_value": text_value,
        })
        self.update_attributes(mapper={
            "chat_messages": chat_messages,
        })
        return
    
    def clear_chat_threads(self, openai_secret_key: str):
        """Clear the `chat_messages` and `thread_id_list` of current experiment.
        
        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            
        Returns:
            is_successful (bool): Indidate if the threads are all deleted.
        """
        is_successful = OpenAIAssistant.delete_thread(
            openai_secret_key=openai_secret_key, 
            thread_id=self.current_thread_id
        )
        is_successful, deleted_thread_ids = OpenAIAssistant.delete_threads(
            openai_secret_key=openai_secret_key, 
            thread_id=self.thread_id_list
        )
        self.update_attributes(
            mapper={
                "current_assistant_type": 0,
                "current_thread_id": "",
                "thread_id_list": list()
            }
        )
        return is_successful

    #endregion


class Result():
    """Result Model: Record and Process experiment result."""

    __tablename__ = "results"

    def __init__(self, experiment_id: str, pdb_filename: str, mutant: str, replica_id: str, slurm_job_uuid: str = None, **kwargs):
        """Initializes an instance of Result with the provided parameters.

        Args:
            experiment_id (int): The experiment ID associated with this result.
            pdb_filename (str): The name of the PDB file of the result.
            mutant (str): The name of the mutant protein. e.g.: 'A##B C##D'
            replica_id (str): The ID of the MD simulation relica of one mutant.
            slurm_job_uuid (str, optional): The UUID of the slurm job.
            kwargs: Keyword arguments containing metrics and other attributes.
        """
        self.id = kwargs.get("id", str(uuid.uuid4()))
        self.experiment_id = experiment_id
        self.pdb_filename = pdb_filename
        self.mutant = mutant
        self.replica_id = replica_id
        self.slurm_job_uuid = slurm_job_uuid

        for metric in METRICS_MAPPER.keys():
            setattr(self, metric, kwargs.get(metric, None))
            continue

        self.created_time = kwargs.get("created_time", datetime.now())
        self.updated_time = kwargs.get("updated_time", datetime.now())

        return
    
    @staticmethod
    def get(id: str) -> Result | None:
        """Get a result instance with given ID.
        
        Args:
            id (str): The `id` to identify a result.

        Returns:
            Matched Result instance or None.
        """
        result = Result.from_dict(db.results.find_one({"id": id}))
        # experiment = Experiment.query.filter_by(id=id).first()
        if (result):
            return result
        else:
            return None

    @staticmethod
    def from_dict(result_dict: dict | None) -> Result:
        """Build a result instance from a dict.
        
        Args:
            result_dict (dict): A dictionary containing data of the result.

        Returns:
            Built Result instance or None.
        """
        if (result_dict is None):
            return None
        result = Result(**result_dict)
        return result
    
    def as_dict(self, stringfy_time: bool = False) -> dict:
        """Serialize the current instance to a dictionary.
        
        Args:
            stringfy_time (bool, optional): Flag indicating if to convert datetime fields to string value.
        """
        dict_data = self.__dict__
        if (stringfy_time):
            dict_data["created_time"] = str(self.created_time)
            dict_data["updated_time"] = str(self.updated_time)
        return dict_data
    
    @staticmethod
    def get_experiment_results(experiment_id: str) -> List[Dict[str, Any]]:
        """Get a list of results of an Experiment instance with designated `experiment_id`.
        For each mutant, the value of the analysis data will be the average of all its replica.
        
        Args:
            experiment_id (str): The `id` to identify an experiment.

        Returns:
            experiment_results (List[Dict[str, Any]]): A list of results of an Experiment instance.
        """
        results_cursor = db.results.find({"experiment_id": experiment_id})
        result_df = DataFrame([result for result in results_cursor])

        keep_columns = list(METRICS_MAPPER.keys())
        keep_columns.append("mutant")

        result_df = result_df[keep_columns]
        result_df_group = result_df.groupby(["mutant"]).mean()

        return result_df_group.agg(lambda x: x.tolist()).reset_index().to_dict(orient="records")

    def insert_or_update(self):
        """Insert or Update the current Result instance to the database."""
        matched_result = Result.from_dict(db.results.find_one(
            {
                "experiment_id": self.experiment_id,
                "mutant": self.mutant,
                "replica_id": self.replica_id,
            }
        ))
        if (matched_result == None):
            db.results.insert_one(self.as_dict())
        else:
            result_update_dict = dict()
            for metric in METRICS_MAPPER.keys():
                result_update_dict[metric] = self.as_dict().get(metric, None)
                continue
            result_update_dict["updated_time"] = datetime.now()
            db.results.update_one({"id": matched_result.id}, {"$set": result_update_dict})
        return
