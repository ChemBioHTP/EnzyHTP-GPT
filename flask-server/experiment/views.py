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
from flask import Response, request, redirect
from flask_login import login_required, current_user

# Here put local imports.
from . import experiment
from .models import Experiment
from auth.models import User
from context import login_manager

class ExperimentListResponse():
    """Experiment List Information Response Body."""
    
    def __init__():
        """Experiment List Information Response Body."""
        pass

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
    return redirect("/")

@login_required
@experiment.route("", methods=["GET"])
@experiment.route("/", methods=["GET"])
def index():
    """Get the experiment list belonging to `current_user`.
    
    TODO (Zhong): Return the list of a specific page.
    """
    page_index = int(request.args.get("page", 0))       # Which page to get? Default 0.
    items_on_page = int(request.args.get("items", 20))  # How many items to be displayed on each page? Default 20.
    user: User = current_user

    experiment_list = Experiment.get_user_experiments(user=user)
    return experiment_list

@login_required
@experiment.route("/<experiment_id>", methods=["GET"])
def detail(experiment_id: str):
    """Get the detailed information of a selected experiment instance."""
    experiment = Experiment.get(experiment_id)
    if experiment:
        return Response(experiment.serialize(), status=200, mimetype='application/json')
    else:
        return Response(experiment, status=404)

