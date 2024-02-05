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
import uuid
from datetime import datetime

class Experiment(db.Model):
    """Experiment Model: Experiment information."""

    __tablename__ = 'experiments'
    id = db.Column(db.String(36), primary_key=True, unique=True)
    type = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Integer, nullable=False, default=0)
    metrics = db.Column(db.String(64), nullable=True)
    description = db.Column(db.String(128), nullable=True)
    created_time = db.Column(db.DateTime, nullable=False)
    updated_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', backref=db.backref('experiments'))

    def __init__(self, user_id: int, type: int = 0, status: int = 0, metrics: str = None, description: str = None):
        """Initializes an instance of Experiment with the provided parameters.

        Args:
            user_id (int): The user ID associated with this experiment.
            type (int, optional): The type of the experiment (default is 0).
            status (int, optional): The status of the experiment (default is 0).
            metrics (str, optional): Additional metrics information (default is None).
            description (str, optional): A description of the experiment (default is None).
        """
        self.user_id = user_id
        self.type = type
        self.status = status
        self.metrics = metrics
        self.description = description
        self.id = uuid.uuid4()
        self.created_time = datetime.utcnow()
        self.updated_time = datetime.utcnow()