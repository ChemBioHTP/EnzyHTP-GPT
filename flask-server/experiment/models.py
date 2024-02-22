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
from flask_login import UserMixin
from context import db
from datetime import datetime
from typing import List
import uuid

# Here put local imports.
from auth.models import User

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
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', backref=db.backref('experiments'))

    def __init__(self, user_id: str, name: str, type: int = 0, status: int = 0, metrics: List[float] = list(), description: str = None, id: str = None, **kwargs):
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
        self.created_time = datetime.utcnow()
        self.updated_time = datetime.utcnow()
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
        
