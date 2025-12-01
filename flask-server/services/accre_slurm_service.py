#! python3
# -*- encoding: utf-8 -*-
'''
Vanderbilt University ACCRE Slurm correspondence.

@File    :   accre_slurm_service.py
@Created :   2024/10/10 14:38
@Author  :   Zhong, Yinjie
@Contact :   yinjie.zhong@vanderbilt.edu
'''

# Here put the import lib.
from __future__ import annotations  # To enable the annotation that a staticmethod/classmethod of a class returns an instance of the class.
from io import TextIOWrapper
from json import dumps
from os.path import basename, isfile
from datetime import datetime, timedelta
from typing import Any, List, Union, Tuple
from werkzeug.datastructures import FileStorage
from json import loads, dumps
from requests import (
    get as req_get, 
    post as req_post, 
    delete as req_delete,
)
import jwt

from config import SLURM_API_URL, SLURM_HOST, SLURM_ACCOUNT, SLURM_PARTITION
from context import mongo

db = mongo.db

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
    SLURM_TOKEN_NAME = "slurm_token"

    def __init__(self, account: str = SLURM_ACCOUNT, 
            partition: str = SLURM_PARTITION, 
            job_name: str = "mutexa_web", 
            nodes: int = 1, mem: int = 6144, 
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
            mem (int): Minimum amount of real Memory in Megabytes (MB). Default 6144MB (6GB).
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
        dict_to_serialize["time"] = self.time.days * 1440 + self.time.seconds // 60
        # dict_to_serialize["time"] = f"{self.time.days}-{self.time.seconds//3600}:{(self.time.seconds % 3600) // 60}:{self.time.seconds%60}"
        return dumps(dict_to_serialize)
    
    @classmethod
    def get_slurm_token(cls) -> Tuple[bool, str, str]:
        """Get the slurm token dict from database.
        
        Returns:
            if_exist (bool): A flag indicating the existence of the record in the database.
            token (str): The token string.
            refresh_token (str): The refresh_token string.
        """
        token_dict: dict = db.tokens.find_one({"name": cls.SLURM_TOKEN_NAME})
        if (token_dict is not None):
            token = token_dict.get("token", str())
            refresh_token = token_dict.get("refresh_token", str())
            return True, token, refresh_token
        else:
            return False, str(), str()

    @classmethod
    def is_token_newer(cls, new_token: str, old_token: str = str()) -> bool:
        """Compare the issue time between the new token and the old token (JWT).
        
        Args:
            new_token (str): The new jwt.
            old_token (str, optional): The old jwt.

        Returns:
            A bool value indicating if the new_token is newer than the old_token.
        """
        jwt_decode_options = {"verify_signature": False}
        if (not old_token):
            try:
                payload_new = jwt.decode(jwt=new_token, options=jwt_decode_options)
                return True
            except Exception as exc:
                # print(exc)
                return False
        try:
            payload_old = jwt.decode(jwt=old_token, options=jwt_decode_options)
            payload_new = jwt.decode(jwt=new_token, options=jwt_decode_options)

            # Get the issue date of the token.
            iat_old = int(payload_old["iat"])
            iat_new = int(payload_new["iat"])

            if (iat_new > iat_old):
                return True
            else:
                return False
        except Exception as exc:
            print(exc)
            return False
        
    @classmethod
    def newer_token(cls, new_token: str, old_token: str = str()) -> Tuple[str, bool]:
        """Return the newer token between the 2 tokens.
        
        Args:
            new_token (str): The new jwt.
            old_token (str, optional): The old jwt.

        Returns:
            token (str): The newerly-issued token.
            is_updated (bool): A flag indicating if the token is updated.
        """
        if (cls.is_token_newer(new_token, old_token)):
            # Keep the newer token.
            return new_token, True
        else:
            return old_token, False

    @classmethod
    def update_slurm_tokens(cls, token: str = str(), refresh_token: str = str()) -> Tuple[bool, ]:
        """Update the token and refresh_token of Vanderbilt ACCRE Slurm API.

        Args:
            token (str, optional): The new token string.
            refresh_token (str, optional): The new refresh_token string.

        Returns:
            is_updated (bool): Flag indicating if any updates take place.
            message (str): Message describing the result.
        """
        if_exist, old_token, old_refresh_token = cls.get_slurm_token()
        token_dict = {"name": cls.SLURM_TOKEN_NAME}
        is_token_updated = False    # Indicate if `token` is updated.
        is_refresh_updated = False  # Indicate if `refresh_token` is updated.
        if (if_exist):  # If record exists, update it.
            token_dict["token"], is_token_updated = cls.newer_token(token, old_token)
            token_dict["refresh_token"], is_refresh_updated = cls.newer_token(refresh_token, old_refresh_token)
            db.tokens.update_one({"name": cls.SLURM_TOKEN_NAME}, {"$set": token_dict})
        else:       # If no record, insert a new one.
            if (token):
                token_dict["token"], is_token_updated = cls.newer_token(token)
            if (refresh_token):
                token_dict["refresh_token"], is_refresh_updated = cls.newer_token(refresh_token)
            db.tokens.insert_one(token_dict)
        if (not is_token_updated and not is_refresh_updated):
            return False, "Neither token nor refresh_token is updated."
        elif (is_token_updated and not is_refresh_updated):
            return True, "Token is updated."
        elif (not is_token_updated and is_refresh_updated):
            return True, "Refresh_token is updated."
        elif (is_token_updated and is_refresh_updated):
            return True, "Both token and refresh_token are updated."

    @classmethod
    def refresh_slurm_token(cls) -> Tuple[bool, int, str]:
        """Refresh the SLURM token with refresh_token.
        
        Returns:
            is_updated (bool): Flag indicating if any updates take place.
            status_code (int): Status code from the Slurm API.
            message (str): Message describing the result.
        """
        refresh_token_url = f"{SLURM_HOST}/auth/token/refresh"
        _, old_token, old_refresh_token = cls.get_slurm_token()
        if (not old_token or not old_refresh_token):
            return False, 403, "Empty token or refresh_token."
        headers = {
            "Authorization": f"Bearer {old_token}"
        }
        payload = {"refresh_token": old_refresh_token}
        response = req_post(refresh_token_url, headers=headers, data=payload, timeout=30)
        if (response.ok):
            response_dict: dict = loads(response.text)
            if (response_dict.get("success", False) == True):
                refresh_token_data_dict = response_dict.get("data", dict())
                new_refresh_token = refresh_token_data_dict.get("refresh_token", "")
                new_token = refresh_token_data_dict.get("token", "")
                is_updated, message = cls.update_slurm_tokens(token=new_token, refresh_token=new_refresh_token)
                return is_updated, response.status_code, message
            else:
                return False, 200, response_dict.get("message")
        elif (response.status_code == 403):
            response_dict: dict = loads(response.text)
            message = response_dict.get("detail", "")
            return False, response.status_code, message
        else:
            return False, response.status_code, "Unable to refresh the token."

class SlurmJobData:
    """The information from the slurm job."""

    def __init__(self, job_uuid: str = str(),
            job_name: str = str(), user: str = str(),
            job_details: Union[dict, str] = dict(), job_state: str = str(), 
            created_at: datetime = None, alternate_user: str = str(),
            remote_job_id: str = None, failure_reason: str = str(), **kwargs) -> None:
        """The information from the slurm job.
        
        Args:
            job_uuid (str, optional): The UUID of the slurm job.
            job_name (str, optional): The name of the slurm job.
            user (str, optional): The ACCRE user of the slurm job.
            job_details (Union[dict, str], optional): The detailed description of the slurm job.
            job_state (str, optional): The status of the slurm job.
        """
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
        
    @classmethod
    def get(cls, id: str) -> Tuple[int, SlurmJobData] | None:
        """Get the information of a specific slurm job.
        
        Args:
            id (str): The `uuid` of a specific slurm job.

        Returns:
            status (int): The status from the response.
            job_data (SlurmJobData): The Slurm Job Data instance.
        """
        _, token, _ = SlurmJobRequest.get_slurm_token()
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = req_get(f"{SLURM_API_URL}/{id}", headers=headers)
        if (response.ok):
            response_dict: dict = loads(response.text)
            slurm_job_data_dict = response_dict.get("data", dict())
            slurm_job_data = cls(**slurm_job_data_dict)
            return 200, slurm_job_data
        else:
            return response.status_code, None
    
    @classmethod
    def post_files_pack(cls, file_list: List[Union[str, TextIOWrapper, FileStorage]]) -> List[Tuple]:
        """Pack files or filepaths as a list of tuples required for POST request.
        
        Args:
            file_list (List[str | TextIOWrapper | FileStorage]): A list of files or filepaths or their mixture.

        Returns:
            file_data (List[Tuple]): A list of tuple containing: "files" str, filename, buffered file content and mimetype.
        """
        file_data: List[tuple] = list()
        for file in file_list:
            if (isinstance(file, str) and isfile(file)):
                file_io = open(file=file, mode="r")
                file_io.seek(0)
                file_data.append(
                    ("files", (basename(file), file_io, "application/octet-stream"))
                )
                continue
            elif (isinstance(file, TextIOWrapper)):
                file.seek(0)
                file_data.append(
                    ("files", (basename(file.name), file, "application/octet-stream"))
                )
                continue
            elif (isinstance(file, FileStorage)):
                file.stream.seek(0)
                file_data.append(
                    ("files", (basename(file.filename), file.stream, "application/octet-stream"))
                )
                continue
            else:
                continue
        return file_data

    @classmethod
    def post(cls, slurm_request: SlurmJobRequest, 
        file_list: List[Union[str, TextIOWrapper, FileStorage]], 
        entry_script_content: str, 
        # entry_script_filename: str = SLURM_MD_JOB_ENTRY_SCRIPT
    ) -> Tuple[int, str, str]:
        """Submit a slurm job to the Vanderbilt ACCRE Slurm.
        
        Args:
            slurm_request (SlurmJobRequest): The configuration of the slurm request.
            file_list (list): A list of files to be sent to the working directory on Vanderbilt ACCRE.
            entry_script_content (str): The content of the `entry_script` to be placed as a .

        Returns:
            status (int): The status from the response.
            message (str): The Slurm Job Data instance.
            job_uuid (str): The UUID of the Slurm Job.
        """
        if_exist, token, _ = SlurmJobRequest.get_slurm_token()
        if (if_exist):
            headers = {
                "Authorization": f"Bearer {token}"
            }
            payload = {
                "slurm_request": slurm_request.serialize(),
                # "entry_script": f"bash input/{basename(entry_script_filename)}",
                "entry_script": entry_script_content,
            }
            file_data = cls.post_files_pack(file_list=file_list)

            response = req_post(f"{SLURM_API_URL}", headers=headers, data=payload, files=file_data)
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
        else:
            message = "Slurm token doesn't exist. Please contact the website administrator."
            return 403, message, None

    @classmethod
    def delete(cls, id: str) -> Tuple[int, str]:
        """Delete a specific slurm job.
        
        Args:
            id (str): The `uuid` of a specific slurm job.
        
        Returns:
            status (int): The status code from the response.
            message (str): The message to describe the consequence.
        """
        _, token, _ = SlurmJobRequest.get_slurm_token()
        headers = {
            "Authorization": f"Bearer {token}"
        }
        status, job_data = cls.get(id)
        if (status != 200):
            return 404, "Unable to delete the Slurm Job. The target job doesn't exist."

        cancel_response = req_post(f"{SLURM_API_URL}/{id}/cancel", headers=headers)
        delete_response = req_delete(f"{SLURM_API_URL}/{id}", headers=headers)
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
