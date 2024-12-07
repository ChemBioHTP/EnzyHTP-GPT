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
from typing import Any, Dict, List, Union, Tuple
from json import loads, dumps
from plum import dispatch
from werkzeug.datastructures import FileStorage, ImmutableMultiDict
import os
import uuid
import re

# Here put local imports.
from context import mongo
from config import EXPERIMENT_FILE_DIRECTORY, SCRATCH_FOLDER
from auth.models import User

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
    """Experiment Model: Experiment information.
    
    Attributes:
        user_id (int): The user ID associated with this experiment.
        name (str): The name of the experiment.
        type (int): The type of the experiment (default is 0).
        status (int): The status of the experiment (default is 0).
        metrics (list): Metrics information about what kind of analysis to be performed (default is an empty list).
        description (str): A description of the experiment (default is None).
    """

    __tablename__ = "experiments"

    def __init__(self, user_id: str, name: str, type: int = 0, metrics: List[str] = list(), description: str = None, **kwargs):
        """Initializes an instance of Experiment with the provided parameters.

        Args:
            user_id (int): The user ID associated with this experiment.
            name (str): The name of the experiment.
            type (int, optional): The type of the experiment (default is 0).
            metrics (list, optional): Metrics information about what kind of analysis to be performed (default is an empty list).
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
        self.pdb_filepath = kwargs.get("pdb_filepath", None)
        self.results = kwargs.get("results", list())
        self.slurm_job_uuid = kwargs.get("slurm_job_uuid", None)
        self._status = kwargs.get("status", StatusCode.CREATED)
        self._progress = kwargs.get("progress", 0.0)
        self.mutation_pattern = kwargs.get("mutation_pattern", "WT")
        self.current_assistant_type = kwargs.get("current_assistant_type", 0)  # 0: Question Analyzer; 1: Metrics Planner; 2: Mutant Planner.
        self.current_thread_id = kwargs.get("current_thread_id", str())
    
    @staticmethod
    def get(id: str) -> Experiment | None:
        """Get experiment instance.
        
        Args:
            id (str): The `id` to identify an experiment.
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

    def update_attributes(self, mapper: ImmutableMultiDict, editable_attrs: list = list()) -> Tuple[list, list, list, str]:
        """Update the attribute of a specified instance.
        
        Args:
            instance: The instance of a class who has attributes to be updated.
            mapper (ImmutableMultiDict): A dict-like mapper which contains the fields/attributes and values.
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
                        db.experiments.update_one({"id": self.id}, {"$set": {field_name: field_value}})
                        # db.session.commit()
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

        for field_key in fields_to_delete:
            if (field_key in dict_data.keys()):
                del dict_data[field_key]
        return dumps(dict_data)
    
    def __repr__(self):
        return f"Experiment('{self.id}', '{self.name}')"

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        if (value == StatusCode.CANCELLED):
            self.results.clear()
        self._status = value
        self.updated_time = datetime.now()
        return
    
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

    @staticmethod
    def validate_pdb(pdb_file: str | FileStorage) -> Tuple[bool, str]:
        """Validate PDB file.

        Args:
            pdb_file (str or FileStorage): The filepath or FileStorage instance of the PDB file.
        
        Returns:
            is_valid (bool): Flag indicating the validity of the PDB file.
            message (str): The message describing the validity status.
        """
        pdb_filepath = str()

        from_filestorage = isinstance(pdb_file, FileStorage)
        if (from_filestorage):
            pdb_filepath = os.path.join(SCRATCH_FOLDER, pdb_file.filename)
            pdb_file.save(pdb_filepath)
        else:
            pdb_filepath = pdb_file
        
        is_valid = False
        message = str()
        
        with CaptureLogging(_LOGGER) as log_str:
            if (not os.path.isfile(pdb_filepath)):
                message = "No selected file."
            else:
                stru = sp.get_structure(pdb_filepath)
                if (stru.num_atoms > 0):
                    is_valid, intermediate_message = is_structure_valid(stru, print_report=False)
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
        
        return is_valid, message

    def update_pdb(self, pdb_file: FileStorage) -> Tuple[bool, str]:
        """Update PDB file. Invalid PDB file will not be updated.

        Args:
            pdb_file (FileStorage): The FileStorage instance of the new PDB file.
        
        Returns:
            is_valid (bool): Flag indicating the validity of the PDB file.
            message (str): The message describing the updating.
        """
        if (fs.get_file_ext(pdb_file.filename).lower() != ".pdb"):
            return False, "This is not a PDB file."
        save_folder = os.path.join(EXPERIMENT_FILE_DIRECTORY, self.id)
        fs.safe_mkdir(save_folder)
        is_valid, message = Experiment.validate_pdb(pdb_file)

        if (is_valid):
            filepath = os.path.join(save_folder, pdb_file.filename)
            if (self.pdb_filepath and os.path.isfile(self.pdb_filepath)):
                fs.safe_rm(self.pdb_filepath) # Delete existing file.
            pdb_file.save(filepath)
            self.pdb_filepath = filepath
            message = f"The PDB file of the experiment {self.id} is updated. " + message
            db.experiments.update_one({"id": self.id}, {"$set": {"pdb_filepath": self.pdb_filepath}})
            # db.session.commit()

        return is_valid, message
    
    def analyze_ensemble(self, mutant_name: str, stru_esm: StructureEnsemble):
        """Perform the analysis based on the given StructureEnsemble instance.
        
        Args:
            mutant_name (str): The name of the mutant associated with the trajectory. e.g.: 'A##B C##D'.
            stru_esm (StructureEnsemble): The StructureEnsemble instance for analysis.
        """
        pass

    def validate_ensemble(self, prmtop_file: str | FileStorage, traj_file: str | FileStorage) -> Tuple[bool, str]:
        """Validate the prmtop file and trajectory file sent from the user or the computing cluster."""
        return True, "The trajectory file is valid."
    
    def update_ensemble_analysis(self, mutant_name: str, prmtop_file: FileStorage, traj_file: FileStorage) -> Tuple[bool, str]:
        """Update the structure ensemble of the mutant and perform analysis.
        Invalid Trajectory file will not trigger updates to the results.
        Trajectory files will be removed after the completion of analysis.

        Args:
            mutant_name (str): The name of the mutant associated with the trajectory. e.g.: 'A##B C##D'
            prmtop_file (FileStorage): The FileStorage instance of the Amber prmtop file.
            traj_file (FileStorage): The FileStorage instance of the new trajectory file.
        
        Returns:
            is_valid (bool): Flag indicating the validity of the PDB file.
            message (str): The message describing the updating.
        """
        save_folder = os.path.join(EXPERIMENT_FILE_DIRECTORY, self.id, mutant_name)
        fs.safe_mkdir(save_folder)
        prmtop_file_path = os.path.join(save_folder, prmtop_file.name)
        traj_file_path = os.path.join(save_folder, traj_file.name)
        ref_pdb_path = os.path.join(save_folder, "ref_stru.pdb")
        try:
            prmtop_file.save(prmtop_file_path)
            traj_file.save(traj_file_path)
            is_valid, validation_message = self.validate_ensemble(prmtop_file=prmtop_file_path, traj_file=traj_file_path)
            if (is_valid):
                # Construct the reference structure PDB file.
                mutant = [generate_from_mutation_flag(mutation_str) for mutation_str in mutant_name.split()]
                ref_stru = mutate_stru(sp.get_structure(self.pdb_filepath), mutant=mutant)
                sp.save_structure(outfile=ref_pdb_path, stru=ref_stru)

                stru_esm = interface.amber.load_traj(
                    prmtop_path=prmtop_file_path, traj_path=traj_file_path,
                    ref_pdb=ref_pdb_path
                )
                self.analyze_ensemble(mutant_name=mutant_name, stru_esm=stru_esm)
        finally:
            fs.safe_rm(prmtop_file_path)
            fs.safe_rm(traj_file_path)

    def clear_folder(self, remove_folder: bool = False):
        """Remove the folder of the current directory.
        
        Args:
            remove_folder (bool): If true, remove the folder itself as well; otherwise leave the empty folder.
        """
        save_folder = os.path.join(EXPERIMENT_FILE_DIRECTORY, self.id)
        fs.safe_rmdir(save_folder)
        if (remove_folder):
            return
        else:
            fs.safe_mkdir(save_folder)
    
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
        if (not os.path.isfile(self.pdb_filepath)):
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
            db.experiments.update_one({"id": self.id}, {"$set": {"mutation_pattern": self.mutation_pattern}})
            # db.session.commit()
        message = message.replace("parsing", "update")
        return is_successful, mutant_string_list, message

    def parse_agent_response_content(self, response_content: str) -> Tuple[bool, str]:
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

    def post_result(self, result_record: dict):
        """Add new result record to the experiment.
        
        Args:
            result_record_dict (dict): A dict containing the result information of one mutant.
        """
        self.results.append(result_record)
        return
