#! python3
# -*- encoding: utf-8 -*-
'''
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
from typing import List, Union, Tuple
from json import loads, dumps
from plum import dispatch
from werkzeug.datastructures import FileStorage
import os
import uuid

# Here put local imports.
from context import mongo
from config import EXPERIMENT_FILE_DIRECTORY, SCRATCH_FOLDER
from auth.models import User

# Here put enzy_htp modules.
from enzy_htp.core.general import CaptureLogging, _LOGGER
from enzy_htp.core import (
    exception as core_exc, 
    file_system as fs
)
from enzy_htp.structure import PDBParser
from enzy_htp.preparation.validity import is_structure_valid
from enzy_htp.mutation.mutation_pattern import api as pattern_api
from enzy_htp.mutation_class import get_mutant_name_str, get_mutant_name_tag
from enzy_htp.mutation.api import mutate_stru
from enzy_htp.workflow.config import StatusCode

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

    __tablename__ = 'experiments'
    # id = db.Column(db.String(36), primary_key=True, unique=True)
    # type = db.Column(db.Integer, nullable=False, default=0)
    # name = db.Column(db.String(128), nullable=False, default="Experiment")
    # slurm_job_uuid = db.Column(db.String(36), nullable=True)
    # _status = db.Column("status", db.Integer, nullable=False, default=StatusCode.CREATED)
    # _progress = db.Column("progress", db.Float, nullable=False, default=0.0)
    # mutation_pattern = db.Column(db.String(256), nullable=True, default="WT")
    # metrics = db.Column(db.String(64), nullable=True)
    # description = db.Column(db.String(128), nullable=True)
    # created_time = db.Column(db.DateTime, nullable=False)
    # updated_time = db.Column(db.DateTime, nullable=False)
    # pdb_filepath = db.Column(db.String(1024), nullable=True)
    # user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    # user = db.relationship('User', backref=db.backref('experiments'))

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
        self.id = kwargs.get("id", str(uuid.uuid4()))
        self.created_time = kwargs.get("created_time", datetime.now())
        self.updated_time = kwargs.get("updated_time", datetime.now())
        self.pdb_filepath = kwargs.get("pdb_filepath", None)
        self.results = kwargs.get("results", list())
        self.slurm_job_uuid = kwargs.get("slurm_job_uuid", None)
        self._status = kwargs.get("status", StatusCode.CREATED)
        self._progress = kwargs.get("progress", 0.0)
        self.mutation_pattern = kwargs.get("mutation_pattern", "WT")
    
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

    def as_dict(self, stringfy_time: bool = False) -> str:
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
        from json import dumps

        dict_data = self.as_dict()
        del dict_data["_sa_instance_state"]
        dict_data["created_time"] = str(self.created_time)
        dict_data["updated_time"] = str(self.updated_time)
        dict_data["status"] = str(self._status)
        dict_data["progress"] = str(self._progress)
        dict_data["status_text"] = StatusCode.status_text_mapper.get(self.status, self.status)
        del dict_data["_status"]
        del dict_data["_progress"]
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
                sp = PDBParser()
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

        protein_stru = PDBParser().get_structure(self.pdb_filepath)
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
                sp = PDBParser()
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
            sp = PDBParser()
            for tag, structure in tag_structure_pairs.items():
                pdb_string = sp.get_file_str(structure)
                tag_string_pairs[tag] = pdb_string
            message = "Getting Mutant PDB file string succeeded!"
        return is_successful, tag_string_pairs, message

    def get_mutants_string_list(self) -> Tuple[bool, str, str]:
        """Get a list of mutant string concerning the current experiment instance.

        Returns:
            is_successful (bool): Flag indicating if the update is successful.
            mutant_string_list (str): A list of mutant string assigned by the mutation pattern. None if the pattern is invalid.
            message (str): The message describing the updating.
        """
        mutant_string_list = list()
        is_successful, mutants, message = self.get_mutants()
        if (is_successful):
            for mut in mutants:
                mutant_string_list.append(get_mutant_name_str(mut))
        return is_successful, mutant_string_list, message

    def update_mutation_pattern(self, mutation_pattern: str, freeze: bool = False) -> Tuple[bool, str, str]:
        """Update the mutation pattern of the current experiment instance.
        If the mutation pattern can be successfully parsed, the update to mutation_pattern takes place; otherwise the mutation pattern is not updated.
        
        Args:
            mutation_pattern (str): The updated mutation pattern to be assigned to the experiment.
            freeze (bool): A flag indicating whether to convert a valid random mutation pattern to the mutation pattern of the specified target mutant.

        Returns:
            is_successful (bool): Flag indicating if the update is successful.
            mutant_string (str): The mutants assigned by the mutation pattern. None if the pattern is invalid.
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

    def post_result(self, result_record: dict):
        """Add new result record to the experiment.
        
        Args:
            result_record_dict (dict): A dict containing the result information of one mutant.
        """
        self.results.append(result_record)
        return

#region Slurm Jobs

from os.path import basename
from requests import (
    get as req_get, 
    post as req_post, 
    delete as req_delete,
)

from config import ACCRE_SLURM_URL, ACCRE_SLURM_AUTHORIZATION, SLURM_ACCOUNT, SLURM_PARTITION, SLURM_JOB_ENTRY_SCRIPT_FILENAME

class SlurmJobRequest:
    """The configuration information to start a slurm job on Vanderbilt ACCRE.
    
    Attributes:
        partition (str): Partition requested.
        nodes (str): Number of Nodes on which to run (N = min[-max]).
        job_name (str): Name of Job.
        mem (str): Minimum amount of real Memory.
        account (str): Charge job to specified Account.
        time (timedelta): Time limit.
        tasks_per_node (int): Number of Tasks to invoke on each Node.
        ntasks (int): Number of Tasks to run.
        cpus_per_task (int): Number of CPUs required per spawned task.
        nodelist (list): Request a specific list of hosts.
        exclude (list): Exclude a specific list of hosts.
        array (list): Job array index values.
        mail_user (str): Who to send email notification for job state changes.
        mail_type (str): Notify on state change: BEGIN, END, FAIL or ALL.
        depend (str): Defer job until condition on jobid is satisfied. Format: type:jobid[:time]
        constraint (str): Specify a list of Constraints.
        gres (str): Flags related to GRES management.
    """

    def __init__(self, account: str = SLURM_ACCOUNT, 
            partition: str = SLURM_PARTITION, 
            job_name: str = "EnzyHTP-Web", 
            nodes: int = 1, mem: str = "6G", 
            time: timedelta = timedelta(days=10), 
            tasks_per_node: int = 1, ntasks: int = 1, 
            cpus_per_task: int = 1, nodelist: List[str] = list(),
            exclude: List[str] = list(), array: list = list(),
            mail_user: str = None, mail_type: str = None,
            depend: str = str(), constraint: str = str(),
            gres: str = str(), **kwargs):
        """The configuration information to start a slurm job on Vanderbilt ACCRE.
        
        Args:
            account (str): Charge job to specified Account.
            partition (str): Partition requested.
            job_name (str): Name of Job. Default "EnzyHTP Workflow".
            nodes (int): Number of Nodes on which to run (N = min[-max]).
            mem (str): Minimum amount of real Memory. Default "6G".
            time (timedelta): Time limit. Default 10 days.
            tasks_per_node (int): Number of Tasks to invoke on each Node. Default 1.
            ntasks (int): Number of Tasks to run. Default 1.
            cpus_per_task (int): Number of CPUs required per spawned task. Default 1.
            nodelist (list): Request a specific list of hosts. Default Empty.
            exclude (list): Exclude a specific list of hosts. Default Empty.
            array (list): Job array index values. Default Empty.
            mail_user (str): Who to send email notification for job state changes. Default None.
            mail_type (str): Notify on state change: BEGIN, END, FAIL or ALL. Default None.
            depend (str): Defer job until condition on jobid is satisfied. Format: type:jobid[:time]. Default Empty.
            constraint (str): Specify a list of Constraints. Default Empty.
            gres (str): Flags related to GRES management. Default Empty.
        """
        self.account = account
        self.partition = partition
        self.job_name = job_name
        self.time = time
        self.nodes = nodes
        self.mem = mem
        self.tasks_per_node = tasks_per_node
        self.ntasks = ntasks
        self.cpus_per_task = cpus_per_task
        self.nodelist = nodelist
        self.exclude = exclude
        self.array = array
        self.mail_user = mail_user
        self.mail_type = mail_type
        self.depend = depend
        self.constraint = constraint
        self.gres = gres

    def serialize(self) -> str:
        """Serialize the current instance to json string, None or Empty value will be omitted."""
        from json import dumps

        dict_to_serialize = dict()
        for key, value in self.__dict__.items():
            if value:
                dict_to_serialize[key] = value
        
        dict_to_serialize["time"] = f"{self.time.days}-{self.time.seconds//3600}:{(self.time.seconds % 3600) // 60}:{self.time.seconds%60}"
        return dumps(dict_to_serialize)

class SlurmJobData:
    """The information from the slurm job."""

    def __init__(self, job_uuid: str = str(),
            job_name: str = str(), user: str = str(),
            job_details: Union[dict, str] = dict(), job_state: str = str(), 
            created_at: datetime = None, alternate_user: str = str(),
            remote_job_id: str = None, failure_reason: str = str(), **kwargs) -> None:
        self.job_uuid = job_uuid
        self.job_name = job_name
        self.user = user
        if (isinstance(job_details, dict)):
            self.job_details = job_details
        else:
            self.job_details = loads(job_details)
        self.job_state = job_state
        if (created_at is None):
            self.created_at = datetime.now()
        else:
            self.created_at = created_at
        self.alternate_user = alternate_user
        self.remote_job_id = remote_job_id
        self.failure_reason = failure_reason
        self.kwargs = kwargs
        
    @staticmethod
    def get(id: str) -> Tuple[int, SlurmJobData] | None:
        """Get the information of a specific slurm job.
        
        Args:
            id (str): The `uuid` of a specific slurm job.

        Returns:
            status (int): The status from the response.
            job_data (SlurmJobData): The Slurm Job Data instance.
        """
        headers = {
            "Authorization": ACCRE_SLURM_AUTHORIZATION
        }
        response = req_get(f"{ACCRE_SLURM_URL}/{id}", headers=headers)
        if (response.ok):
            response_dict: dict = loads(response.text)
            slurm_job_data_dict = response_dict.get("data", dict())
            slurm_job_data = __class__(**slurm_job_data_dict)
            return 200, slurm_job_data
        else:
            return response.status_code, None
    
    @staticmethod
    def submit(slurm_request: SlurmJobRequest, files: List[BufferedReader]) -> Tuple[int, str, str]:
        """Submit a slurm job to the Vanderbilt ACCRE Slurm.
        
        Args:
            slurm_request (SlurmJobRequest): The configuration of the slurm request.
            files (list): A list of files to be sent to the working directory on Vanderbilt ACCRE.

        Returns:
            status (int): The status from the response.
            message (str): The Slurm Job Data instance.        
            job_uuid (str): The UUID of the Slurm Job.
        """
        headers = {
            "Authorization": ACCRE_SLURM_AUTHORIZATION
        }
        payload = {
            'slurm_request': slurm_request.serialize(),
            'entry_script': f"bash input/{SLURM_JOB_ENTRY_SCRIPT_FILENAME}",
        }
        files = [("files", (basename(fobj.name), fobj, "application/octet-stream")) for fobj in files]

        response = req_post(f"{ACCRE_SLURM_URL}", headers=headers, data=payload, files=files)
        if (response.ok):
            response_dict: dict = loads(response.text)
            message = response_dict.get("message", str())
            if (response_dict.get("success", False)):
                job_uuid = response_dict.get("data", dict()).get("job_uuid", str())
                return 201, message, job_uuid
            else:
                return 400, message, None
        else:
            message = str()
            try:
                print(response.text)
                response_dict: dict = loads(response.text)
                message = response_dict.get("message", str())
            except:
                message = "The Slurm Job submission is failed."
            return response.status_code, message, None

    @staticmethod
    def delete(id: str) -> Tuple[int, str]:
        """Delete a specific slurm job.
        
        Args:
            id (str): The `uuid` of a specific slurm job.
        
        Returns:
            status (int): The status code from the response.
            message (str): The message to describe the consequence.
        """
        headers = {
            "Authorization": ACCRE_SLURM_AUTHORIZATION
        }
        status, job_data = __class__.get(id)
        if (status != 200):
            return status, "Unable to delete the Slurm Job. The target job doesn't exist."

        cancel_response = req_post(f"{ACCRE_SLURM_URL}/{id}/cancel", headers=headers)
        delete_response = req_delete(f"{ACCRE_SLURM_URL}/{id}", headers=headers)
        if (delete_response.status_code == 200):
            return 200, "The Slurm Job has successfully be deleted."
        else:
            return delete_response.status_code, "Unable to delete the Slurm Job."

    def __bool__(self):
        return bool(self.job_uuid)
    
    def as_dict(self):
        """Serialize the current instance to a dictionary."""
        dict_data = self.__dict__
        for key, value in self.kwargs.items():
            dict_data[key] = value
        del dict_data["kwargs"]
        return dict_data

    def serialize(self) -> str:
        """Serialize the current instance to json string."""
        serialized_data = self.as_dict()
        return dumps(serialized_data)

#endregion