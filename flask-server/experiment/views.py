#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   views.py
@Created :   2024/02/20 02:44
@Author  :   Zhong, Yinjie
@Version :   1.0
@Contact :   yinjie.zhong@vanderbilt.edu
'''

# Here put the import lib.
from flask import Response, request, redirect, jsonify
from flask_login import login_required, current_user
from typing import List
from datetime import datetime

# Here put local imports.
from . import experiment
from .models import Experiment
from auth.models import User
from context import login_manager

class ExperimentIndexResponse():
    """Experiment List Information Response Body."""
    
    def __init__(self, experiments: List[Experiment]):
        """Experiment List Information Response Body."""
        user: User = current_user
        self.user_id = user.id
        self.email = user.email
        self.username = user.username
        self.timestamp = str(datetime.now())
        self.experiments = list()
        for exp in experiments:
            exp_dict = exp.as_dict()
            del exp_dict["user_id"]
            self.experiments.append(exp_dict)
            continue
        return
    
    def serialize(self) -> str:
        """Serialize the current instance to json string."""
        from json import dumps
        serialized_data = self.__dict__
        return dumps(serialized_data)

@login_manager.user_loader
def load_user(user_id: str) -> User:
    """A mandatory method to return a user instance based on user id.
    
    Args:
        user_id: User ID.
    """
    return User.get(id=user_id)

@login_manager.unauthorized_handler
def unauth_handler() -> Response:
    """Handle unauthorized requests toward an `@login_required` method."""
    return Response(response=None, status=401)

@experiment.route("", methods=["GET"])
@experiment.route("/", methods=["GET"])
@login_required
def index():
    """Get the experiment list belonging to `current_user`.
    
    TODO (Zhong): Return the list of a specific page.
    """
    page_index = int(request.args.get("page", 0))       # Which page to get? Default 0.
    items_on_page = int(request.args.get("items", 20))  # How many items to be displayed on each page? Default 20.
    user: User = current_user

    experiments = Experiment.get_user_experiments(user=user)
    response_body = ExperimentIndexResponse(experiments)
    return Response(response=response_body.serialize(), status=200, mimetype='application/json')

@experiment.route("/<experiment_id>", methods=["GET"])
@login_required
def detail(experiment_id: str):
    """Get the detailed information of a selected experiment instance."""
    experiment = Experiment.get(experiment_id)
    if experiment:
        return Response(experiment.serialize(), status=200, mimetype='application/json')
    else:
        return Response(experiment.serialize(), status=404)

