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
import openai
import prompts
from flask import Response, request, redirect, jsonify
from flask_login import login_required, current_user
from typing import List
from datetime import datetime
from werkzeug.datastructures import FileStorage

# Here put local imports.
from . import experiment
from .models import Experiment
from auth.models import User
from context import login_manager
from config import UPLOAD_FOLDER, DEFAULT_FILE_PATH

# Here put enzy_htp modules.
import enzy_htp.structure
import enzy_htp.mutation.api as mapi
import enzy_htp.mutation.mutation as mt
import enzy_htp.mutation.mutation_pattern.api as pattern_api
from enzy_htp.preparation import validity as vd
from enzy_htp.core import (
    general as eg,
    _LOGGER
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


# Validate File
@experiment.route("/validate_pdb_file", methods=["POST"])
def validate_pdb_file():
    """Validate the PDB file from the user."""
    result = None
    message = str()
    is_valid = False
    file_path = DEFAULT_FILE_PATH
    respose_body = str()
    with eg.CaptureLogging(_LOGGER) as log_str:
        try:
            file = request.files.get("file")

            if not file:
                is_valid = False
                message = "No selected file."
            else:
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                if (not os.path.isdir(UPLOAD_FOLDER)):
                    os.mkdir(UPLOAD_FOLDER)
                file.save(file_path)

                sp = enzy_htp.structure.PDBParser()
                stru = sp.get_structure(file_path)
                result = vd.is_structure_valid(stru, print_report=True)
                is_valid = result[0]
                intermediate_message = result[1]
                message += "The following errors were found in the PDB file: \n"
                for reason, source, suggestion in intermediate_message:
                    message += f"Reason: {str(reason)}\tSource: {str(source)}\tSuggestion: {str(suggestion)};\n"
                if is_valid:
                    message = "The PDB file is valid."
                else:
                    os.remove(file_path)
        except:
            is_valid = False
            message = log_str.getvalue()
            os.remove(file_path)
    respose_body = jsonify({"validity": is_valid, "message": message})
    return respose_body

# Generate Patterns
@experiment.route("/generate_pattern", methods=["POST"])
@login_required
def generate_pattern():
    user: User = current_user

    file_path = DEFAULT_FILE_PATH
    data = request.json
    mutation_request = data.get('mut_request')
    # api_key = data.get('api_key')
    api_key = user.openai_secret_key

    prompt = str()
    prompt += prompts.prompt_skeleton
    prompt += f"Query:{mutation_request}\nAnswer:"
    
    openai.api_key = api_key

    # TODO: how to improve prompt in prompts.py?
    # try:
    #     completions = openai.Completion.create(
    #         engine="gpt-3.5-turbo-instruct",
    #         prompt=prompt,
    #         max_tokens=70,
    #         frequency_penalty=-0.5,
    #         temperature=0.01,
    #     )
    #     pattern = completions.choices[0].text
    # except Exception as e:
    #     raise Exception(f'API Error: {str(e)}')
    
    pattern = "r:3[resi 1 around 4:all not self]*10"
    sp = enzy_htp.structure.PDBParser()
    stru = sp.get_structure(file_path)
    try:
        mutations = pattern_api.decode_mutation_pattern(stru, pattern)
    except pattern_api.InvalidMutationPatternSyntax as e:
        raise Exception(f'Invalid mutation: {str(e)}')
    
    mut_string = ""
    for mut in mutations:
        mut_string += mt.get_mutant_name_str(mut) + ";"
    
    mut_string = mut_string[:-1]

    os.remove(file_path)

    # TODO: generate mutants with "generate_mut" function and save it

    return jsonify({"pattern": pattern, "mut_string": mut_string})

def generate_muts(file: FileStorage, pattern):
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