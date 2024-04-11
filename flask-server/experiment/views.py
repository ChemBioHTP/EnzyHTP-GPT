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
import os
import prompts
from flask import Response, request, redirect, jsonify
from flask_login import login_required, current_user
from json import dumps
from typing import List
from string import Template
from datetime import datetime
from werkzeug.datastructures import FileStorage
from openai import OpenAI

# Here put local imports.
from . import experiment as experiment_blueprint
from .models import Experiment
from auth.models import User
from context import db, login_manager
from config import EXPERIMENT_FILE_DIRECTORY, DEFAULT_FILE_PATH

# Here put enzy_htp modules.
import enzy_htp.structure
import enzy_htp.mutation.api as mapi
import enzy_htp.mutation.mutation as mt
import enzy_htp.mutation.mutation_pattern.api as pattern_api
from enzy_htp.preparation.validity import is_structure_valid
from enzy_htp.core import (
    general as eg,
    _LOGGER,
    file_system as fs,
    exception as core_exc
)

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

@experiment_blueprint.route("", methods=["GET"])
@experiment_blueprint.route("/", methods=["GET"])
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

@experiment_blueprint.route("/<experiment_id>", methods=["GET"])
@login_required
def detail(experiment_id: str):
    """Get the detailed information of a selected experiment instance.
    
    Args:
        experiment_id (str): The identifier of an experiment instance.
    """
    experiment = Experiment.get(experiment_id)
    if experiment:
        return Response(experiment.serialize(), status=200, mimetype='application/json')
    else:
        return Response(experiment.serialize(), status=404)

################# Experiment Behaviour #################

class ExperimentBehaviourResponseInfo():
    """Experiment Behaviour Response Information.
    
    Attributes:
        id: Experiment id.
        name: Experiment name.
        user_id: User identifier.
        email: User Email Address.
        is_successful: Has the request successfully achieved its purpose?
        message: The message to be sent.
        timestamp: Time when the operation is completed.
    """

    def __init__(self,
            experiment: Experiment,
            user: User,
            is_successful: bool = True,
            message: str = str(),
            timestamp = datetime.__new__(datetime, 1970, 1, 1),
            is_authenticated: bool = True,
            **kwargs) -> None:
        """Experiment Behaviour Response Information.
        
        Args:
            experiment (Experiment): The experiment instance.
            user (User): The current user instance.
            email: User Email Address.
            is_successful: Has the request successfully achieved its purpose?
            message: The message to be sent.
            timestamp: Time when the operation is completed.
            is_authenticated (bool): Show if a user is authenticated.
            **kwargs: Any other attributes to be sent.
        """
        if (experiment):
            self.id = experiment.id
            self.name = experiment.name
        else:
            self.id = None
            self.name = None
            
        self.email = user.email
        self.user_id = user.id
        self.is_successful = is_successful
        self.message = message
        self.is_authenticated = is_authenticated
        if (timestamp == datetime.__new__(datetime, 1970, 1, 1)):
            # Here we might as well assume that 1970-01-01 is a time that will not be triggered in actual business.
            self.timestamp = str(datetime.now())
        else:        
            self.timestamp = str(timestamp)
        
        self.kwargs = kwargs
    
    def serialize(self) -> str:
        """Serialize the current instance to json string."""
        from json import dumps
        serialized_data = self.__dict__.copy()
        for key, value in self.kwargs.items():
            serialized_data[key] = value
        del serialized_data["kwargs"]
        return dumps(serialized_data)

@experiment_blueprint.route("/create", methods=["POST"])
@login_required
def create_experiment():
    """Create new experiment instance."""
    user: User = current_user
    
    name = request.form.get("name", f"{user.username}'s experiment")
    experiment_type = int(request.form.get("type", 0))
    description = request.form.get("description")

    experiment = Experiment(user_id=user.id, name=name, type=experiment_type, description=description)
    db.session.add(experiment)
    db.session.commit()
    response_info = ExperimentBehaviourResponseInfo(
        experiment=experiment,
        user=user,
        message="You have successfully created a new experiment.",
        is_authenticated=True
    )
    return Response(response=response_info.serialize(), status=201, mimetype="application/json")

@experiment_blueprint.route("/<experiment_id>/update_information", methods=["POST", "PUT"])
@login_required
def update_information(experiment_id: str):
    """Update experiment information.
    
    Args:
        experiment_id (str): The identifier of an experiment instance.
    """
    user: User = current_user
    experiment = Experiment.get(experiment_id)

    name = request.form.get("name")
    description = request.form.get("description")

    if name:
        experiment.name = name
    if description:
        experiment.description = description
    db.session.commit()
    
    response_info = ExperimentBehaviourResponseInfo(experiment, user,
        is_successful=True, message="The information is successfully updated.")
    return Response(response=response_info.serialize(), status=200, mimetype="application/json")

@experiment_blueprint.route("/<experiment_id>/upload_pdb_file", methods=["POST"])
@login_required
def upload_pdb_file(experiment_id: str):
    """Upload and Validate PDB File from the user.
    
    Args:
        experiment_id (str): The identifier of an experiment instance.
    """
    user: User = current_user
    experiment = Experiment.get(experiment_id)
    result = None
    message = str()
    is_valid = False

    if not experiment:
        response_info = ExperimentBehaviourResponseInfo(experiment=experiment, user=user,
            is_successful=False,
            message=f"The experiment with id '{experiment_id}' doesn't exist.")
        return Response(response=response_info.serialize(), status=404, mimetype="application/json")

    if experiment.user_id != user.id:
        message = "You are not allowed to upload file to this experiment."
        response_info = ExperimentBehaviourResponseInfo(experiment=experiment, user=user,
            is_successful=False,
            message=message)
        return Response(response=response_info.serialize(), status=403, mimetype="application/json")
    
    fs.safe_mkdir(EXPERIMENT_FILE_DIRECTORY)
    
    save_folder = os.path.join(EXPERIMENT_FILE_DIRECTORY, experiment_id)
    fs.safe_mkdir(save_folder)
    
    with eg.CaptureLogging(_LOGGER) as log_str:
        try:
            file = request.files.get("file")

            if not file:
                is_valid = False
                message = "No selected file."
            else:
                filepath = os.path.join(save_folder, file.filename)
                file.save(filepath)

                sp = enzy_htp.structure.PDBParser()
                stru = sp.get_structure(filepath)
                if (stru.num_atoms > 0):
                    result = is_structure_valid(stru, print_report=True)
                    is_valid = result[0]
                    intermediate_message = result[1]
                    message += "The following errors were found in the PDB file: \n"
                    for reason, source, suggestion in intermediate_message:
                        message += f"Reason: {str(reason)}\tSource: {str(source)}\tSuggestion: {str(suggestion)};\n"
                    
                    if is_valid:
                        message = "The PDB file is valid."
                        if (experiment.pdb_filepath and fs.check_file_exists(experiment.pdb_filepath)):
                            fs.safe_rm(experiment.pdb_filepath) # Delete existing file.
                        experiment.pdb_filepath = filepath
                        db.session.commit()
                    else:
                        fs.safe_rm(filepath)
                else:
                    is_valid = False
                    message = "This is not a PDB file."
                    fs.safe_rm(filepath)
        except:
            is_valid = False
            fs.safe_rm(filepath)
        finally:
            message += f"\n{log_str.getvalue()}"
    response_info = ExperimentBehaviourResponseInfo(experiment=experiment, user=user,
        is_successful=is_valid,
        message=message)
    return Response(response=response_info.serialize(), status=200, mimetype="application/json")

@experiment_blueprint.route("/<experiment_id>/generate_mutation_pattern", methods=["POST"])
@login_required
def generate_mutation_pattern(experiment_id: str):
    """Generate mutation patterns based on natural language inputs.
    
    Args:
        experiment_id (str): The identifier of an experiment instance.
    """
    user: User = current_user
    experiment = Experiment.get(experiment_id)

    filepath = experiment.pdb_filepath

    if experiment.user_id != user.id:
        message = "You are not allowed to access this experiment."
        response_info = ExperimentBehaviourResponseInfo(experiment=experiment, user=user,
            is_successful=False,
            message=message)
        return Response(response=response_info.serialize(), status=403, mimetype="application/json")

    mutation_request = request.form.get("mutation_request")
    openai_client = OpenAI(api_key=user.openai_secret_key)

    prompt = Template(prompts.prompt_skeleton).safe_substitute({
        "question": mutation_request
    })
    
    # TODO: how to improve prompt in prompts.py?
    try:
        completions = openai_client.completions.create(
            prompt=prompt,
            model="gpt-3.5-turbo-instruct",
            max_tokens=70,
            frequency_penalty=-0.5,
            temperature=0.01,
        )
        pattern = completions.choices[0].text
    except Exception as e:
        raise Exception(f'API Error: {str(e)}')
    
    # pattern = "r:3[resi 1 around 4:all not self]*10"
    sp = enzy_htp.structure.PDBParser()
    stru = sp.get_structure(filepath)

    mut_string = ""
    try:
        mutations = pattern_api.decode_mutation_pattern(stru, pattern)
        for mut in mutations:
            mut_string += mt.get_mutant_name_str(mut) + ";"
    except pattern_api.InvalidMutationPatternSyntax as e:
        # raise Exception(f'Invalid mutation: {str(e)}')
        _LOGGER.error(f"InvalidMutationPatternSyntax: {e}")
    except core_exc.InvalidResidueCode as e:
        _LOGGER.error(f"InvalidResidueCode: {e}")
    except Exception as e:
        _LOGGER.error(f"Uncategorized General Exception: {e}")
    
    mut_string = mut_string[:-1]

    # TODO: generate mutants with "generate_mut" function and save it

    response_info = ExperimentBehaviourResponseInfo(experiment=experiment, user=user,
        is_successful=(bool(pattern) and bool(mut_string)), message="Received response from OpenAI. Please check its output.",
        pattern=pattern, mut_string=mut_string)
    return Response(response_info.serialize(), status=200, mimetype="application/json")

def generate_muts(file: FileStorage, pattern):
    """Generate Mutants."""
    sp = enzy_htp.structure.PDBParser()
    stru = sp.get_structure(file.name)

    # checks to make sure mutation is valid before continuing
    try:
        mutations = pattern_api.decode_mutation_pattern(stru, pattern)
    except pattern_api.InvalidMutationPatternSyntax as e:
        raise Exception(f'Invalid mutation: {str(e)}')

    res = []
    # mutates the PDB file with PyMOL
    for mut in mutations:
        try:
            mutant_stru = mapi.mutate_stru(stru, mut, engine="pymol")
            res_file = sp.get_file_str(mutant_stru)
        except Exception as e:
            raise Exception(f'API Error: {str(e)}')
    name_tag = mt.get_mutant_name_tag(mutations)
    res.append((res_file, name_tag))

    return res