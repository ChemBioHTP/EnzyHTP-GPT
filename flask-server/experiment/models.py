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
from datetime import datetime
from typing import List, Tuple
from plum import dispatch
from flask_login import UserMixin
from werkzeug.datastructures import FileStorage
import os
import uuid

# Here put local imports.
from context import db
from config import EXPERIMENT_FILE_DIRECTORY, SCRATCH_FOLDER
from auth.models import User

# Here put enzy_htp modules.
from enzy_htp.core.general import CaptureLogging, _LOGGER
from enzy_htp.core import file_system as fs
from enzy_htp.structure import PDBParser
from enzy_htp.preparation.validity import is_structure_valid

class Experiment(db.Model):
    """Experiment Model: Experiment information."""

    __tablename__ = 'experiments'
    id = db.Column(db.String(36), primary_key=True, unique=True)
    type = db.Column(db.Integer, nullable=False, default=0)
    name = db.Column(db.String(128), nullable=False, default=0)
    status = db.Column(db.Integer, nullable=False, default=0)
    metrics = db.Column(db.String(64), nullable=True)
    description = db.Column(db.String(128), nullable=True)
    created_time = db.Column(db.DateTime, nullable=False)
    updated_time = db.Column(db.DateTime, nullable=False)
    pdb_filepath = db.Column(db.String(1024), nullable=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', backref=db.backref('experiments'))

    def __init__(self, user_id: str, name: str, type: int = 0, status: int = 0, metrics: List[float] = list(), description: str = None, **kwargs):
        """Initializes an instance of Experiment with the provided parameters.

        Args:
            user_id (int): The user ID associated with this experiment.
            name (str): The name of the experiment.
            type (int, optional): The type of the experiment (default is 0).
            status (int, optional): The status of the experiment (default is 0).
            metrics (str, optional): Additional metrics information (default is None).
            description (str, optional): A description of the experiment (default is None).
            kwargs: A placeholder to avoid TypeError caused by unexpected keyword arguments.
        """
        self.id = str(uuid.uuid4())
        self.type = type
        self.name = name
        self.status = status
        self.metrics = str(metrics)
        self.description = description
        self.created_time = datetime.now()
        self.updated_time = datetime.now()
        self.pdb_filepath = None
        self.user_id = user_id
    
    @staticmethod
    def get(id: str) -> Experiment | None:
        """Get experiment instance.
        
        Args:
            id (str): The `id` to identify an experiment.
        """
        experiment = Experiment.query.filter_by(id=id).first()
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
            experiment_query_result = Experiment.query.filter_by(user_id=user.id).order_by(Experiment.created_time).all()
            experiments = [experiment for experiment in experiment_query_result]
            return experiments
        else:
            return []

    def as_dict(self) -> str:
        """Serialize the current instance to a dictionary."""
        dict_data = self.__dict__
        del dict_data["_sa_instance_state"]
        dict_data["created_time"] = str(self.created_time)
        dict_data["updated_time"] = str(self.updated_time)
        return dict_data
    
    def serialize(self) -> str:
        """Serialize the current instance to json string."""
        from json import dumps
        serialized_data = self.as_dict()
        return dumps(serialized_data)
        
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
                    is_valid, intermediate_message = is_structure_valid(stru, print_report=True)
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
            db.session.commit()

        return is_valid, message
