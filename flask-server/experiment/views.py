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
import re
import prompts
import pandas as pd
from flask import Response, request, send_file
from flask_login import login_required, current_user
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restful import Resource
from json import JSONDecodeError, dumps, loads
from typing import Any, List, Tuple
from string import Template
from datetime import datetime
from werkzeug.datastructures import ImmutableMultiDict

# Here put local imports.
from .models import Experiment, Result
from auth.models import User
from auth.views import (
    unauth_handler as unauth_handler_in_auth, 
    notadmin_handler
)
from context import mongo, login_manager
from config import (
    BASEDIR,
    TOKEN_EXPIRES_DELTA,
    WORKSHEET_MUTATION_COLUMN_NAME,
    APP_HOST,
    JSONIFY_MIMETYPE
)
from services import OpenAIChat, OpenAIAssistant
from .agents import AGENT_MAPPER, DefinedAgent

# Here put enzy_htp modules.
from enzy_htp.workflow.config import StatusCode
from enzy_htp.core import (
    file_system as fs,
    _LOGGER
)

db = mongo.db

#region Experiment Response Body and Handlers.

class ExperimentIndexResponse():
    """Experiment Index Information Response Body."""
    
    def __init__(self, experiments: List[Experiment]):
        """Experiment Index Information Response Body."""
        user: User = current_user
        self.user_id = user.id
        self.email = user.email
        self.username = user.username
        self.timestamp = str(datetime.now())
        self.experiments = list()
        for exp in experiments:
            exp_dict = exp.as_dict(stringfy_time=True)
            del exp_dict["user_id"]
            exp_dict["status_text"] = StatusCode.status_text_mapper[exp.status]
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
    return unauth_handler_in_auth()

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
        serialized_data = self.__dict__.copy()
        for key, value in self.kwargs.items():
            serialized_data[key] = value
        del serialized_data["kwargs"]
        return dumps(serialized_data)

def notfound_response(user: User, experiment_id: str = str()) -> Response:
    """Generate a 404 NOT FOUND Response if the specified experiment instance doesn't exist.
    
    Args:
        user (User): Current user.
        experiment_id (str): The `experiment_id` which is sought for.

    Returns:
        A 404 NOT FOUND Response instance.
    """
    if (experiment_id):
        response_info = ExperimentBehaviourResponseInfo(
            experiment=None,
            user=user,
            is_successful=False,
            message=f"Unable to find the experiment with id '{experiment_id}'.",
            is_authenticated=True
        )
        return Response(response=response_info.serialize(), status=404, mimetype=JSONIFY_MIMETYPE)
    else:
        response_info = ExperimentBehaviourResponseInfo(
            user=user,
            is_successful=False,
            message=f"No experiment specified.",
            is_authenticated=True
        )
        return Response(response=response_info.serialize(), status=404, mimetype=JSONIFY_MIMETYPE)

def forbidden_response(user: User, experiment: Experiment) -> Response:
    """Generate a 403 FORBIDDEN Response when the user doesn't have the permission to the experiment.
    
    Args:
        user (User): Current user.
        experiment (experiment): The experiment record associated to the `experiment_id`.

    Returns:
        A 403 FORBIDDEN Response instance.
    """
    response_info = ExperimentBehaviourResponseInfo(
        experiment=experiment,
        user=user,
        is_successful=False,
        message="The current user doesn't have the permission to the experiment.",
        is_authenticated=True
    )
    return Response(response=response_info.serialize(), status=403, mimetype=JSONIFY_MIMETYPE)

def no_pdb_response(user: User, experiment: Experiment) -> Response:
    """Generate a 404 NOT FOUND Response when the experiment isn't associated with any PDB file.
    
    Args:
        user (User): Current user.
        experiment (experiment): The experiment record associated to the `experiment_id`.

    Returns:
        A 404 NOT FOUND Response instance.
    """
    response_info = ExperimentBehaviourResponseInfo(
        experiment=experiment,
        user=user,
        is_successful=False,
        message="The current experiment isn't associated with any PDB file.",
        is_authenticated=True
    )
    return Response(response=response_info.serialize(), status=404, mimetype=JSONIFY_MIMETYPE)

#endregion

class IndexApi(Resource):
    """Route: `/`"""
    
    @login_required
    def get(self):
        """Get the experiment list belonging to `current_user`.
        
        TODO (Zhong): Return the list of a specific page.
        """
        page_index = int(request.args.get("page", 0))       # Which page to get? Default 0.
        items_on_page = int(request.args.get("items", 20))  # How many items to be displayed on each page? Default 20.
        user: User = current_user

        experiments = Experiment.get_user_experiments(user=user)
        response_body = ExperimentIndexResponse(experiments)
        return Response(response=response_body.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)

    @login_required
    def post(self):
        """Create new experiment instance."""
        user: User = current_user
        
        name = request.form.get("name", f"{user.username}'s experiment")
        experiment_type = int(request.form.get("type", -1))
        description = request.form.get("description")

        experiment = Experiment(user_id=user.id, name=name, type=experiment_type, description=description)
        db.experiments.insert_one(experiment.as_dict())
        response_info = ExperimentBehaviourResponseInfo(experiment=experiment, user=user)

        file = request.files.get("file", None)
        force_update = False if request.form.get("force", "").lower() in ["false", "0", "no", ""] else True # Whether to skip verification and force update of PDB files.

        if (file is not None):
            has_pdb_file, is_supported, pdb_file_description = experiment.update_pdb(file, force_update=force_update)

            response_info = ExperimentBehaviourResponseInfo(
                experiment=experiment,
                user=user,
                message="You have successfully created a new experiment.",
                is_authenticated=True,
                has_pdb_file=has_pdb_file,
                pdb_file_description=pdb_file_description
            )
        else:
            response_info = ExperimentBehaviourResponseInfo(
                experiment=experiment,
                user=user,
                message="You have successfully created a new experiment.",
                is_authenticated=True,
                has_pdb_file=False
            )
        return Response(response=response_info.serialize(), status=201, mimetype=JSONIFY_MIMETYPE)

    @login_required
    def delete(self):
        """Delete an existing experiment instance."""
        user: User = current_user
        
        experiment_id = request.form.get("experiment_id", None)
        experiment = Experiment.get(experiment_id)

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (experiment.user_id != user.id):
            return forbidden_response(user, experiment)
        
        if (experiment.status in StatusCode.queued_status):
            response_info = ExperimentBehaviourResponseInfo(experiment, user,
                is_successful=False, 
                message=f"The experiment instance '{experiment_id}' is {StatusCode.status_text_mapper[experiment.status]}, which is unable to be deleted.")
            return Response(response=response_info.serialize(), status=400, mimetype=JSONIFY_MIMETYPE)
        else:
            OpenAIAssistant.delete_thread(
                openai_secret_key=user.openai_secret_key, 
                thread_id=experiment.current_thread_id
            )
            experiment.clear_folder(remove_folder=True)
            db.experiments.delete_one({"id": experiment.id})
            db.results.delete_many({"experiment_id": experiment_id})
            # db.session.delete(experiment)
            # db.session.commit()
            response_info = ExperimentBehaviourResponseInfo(experiment, user,
                is_successful=True, message=f"The experiment instance '{experiment.id}' is successfully deleted.")
            return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)

from config import (
    SLURM_MD_JOB_ENTRY_SCRIPT,
    SLURM_MD_JOB_ENTRY_SCRIPT_CONTENT,
    SLURM_MD_JOB_MAIN_SCRIPT_FILEPATH,
    SLURM_ANALYSIS_JOB_ENTRY_CONTENT,
    SLURM_ANALYSIS_JOB_MAIN_SCRIPT_FILEPATH,
    
    SLURM_DEPLOY_SCRIPT_FILENAME, 
    SLURM_DEPLOY_SCRIPT, 
    MAX_MUTANT_COUNT
)

class ExperimentApi(Resource):
    """Route: `/<experiment_id>`"""

    @login_required
    def get(self, experiment_id: str):
        """Get the detailed information of a selected experiment instance.
        
        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        user: User = current_user
        experiment = Experiment.get(experiment_id)

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (experiment.user_id != user.id):
            return forbidden_response(user, experiment)
        
        # TODO (Zhong): Experiment Results.
        
        return Response(experiment.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)

    @jwt_required()
    def post(self, experiment_id: str):
        """Post the result of the experiment back to the database.
        
        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        user: User = User.get(get_jwt_identity())
        experiment = Experiment.get(experiment_id)

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (user is None or experiment.user_id != user.id):
            return forbidden_response(user, experiment)
        
        mutant_name = request.form.get("mutant", None)
        replica_id = request.form.get("replica_id", 0)
        trajectory_file = request.files.get("trajectory", None)
        topology_file = request.files.get("topology", None)

        is_mutant_constructed, mutant_pdb_filepath, make_mutant_message = experiment.make_mutant_pdb_file(mutant_name=mutant_name)

        if (mutant_name is None or trajectory_file is None or topology_file is None):
            response_info = ExperimentBehaviourResponseInfo(experiment, user,
                is_successful=False, 
                message=f"'mutant' string, 'replica_id' code, 'trajectory' file and 'topology' file are all required.")
            return Response(response=response_info.serialize(), status=400, mimetype=JSONIFY_MIMETYPE)
        elif (not is_mutant_constructed):
            response_info = ExperimentBehaviourResponseInfo(experiment, user,
                is_successful=False, 
                message=make_mutant_message)
            return Response(response=response_info.serialize(), status=501, mimetype=JSONIFY_MIMETYPE)
        else:
            entry_script_str_io = StringIO()
            entry_script_str_io.write(Template(SLURM_ANALYSIS_JOB_ENTRY_CONTENT).safe_substitute({
                "app_host": APP_HOST,
                "experiment_id": experiment.id,
                "access_token": create_access_token(identity=user.id, expires_delta=TOKEN_EXPIRES_DELTA),
                "pdb_filename": experiment.pdb_filename,
                "metrics": dumps(experiment.metrics),
                "topology_filename": topology_file.filename,
                "trajectory_filename": trajectory_file.filename,
            }))
            entry_script_str_io.name = SLURM_MD_JOB_ENTRY_SCRIPT
            entry_script_str_io.mode = "r"
            entry_script_str_io.seek(0)

            analysis_main_script_io = open(SLURM_ANALYSIS_JOB_MAIN_SCRIPT_FILEPATH)
            analysis_main_script_io.seek(0)

            mutant_pdb_io = open(mutant_pdb_filepath)
            mutant_pdb_io.seek(0)

            trajectory_file_io = BytesIO()
            trajectory_file.save(trajectory_file_io)
            trajectory_file_io.name = trajectory_file.filename
            trajectory_file_io.mode = "r"
            trajectory_file_io.seek(0)

            topology_file_io = BytesIO()
            topology_file.save(topology_file_io)
            topology_file_io.name = topology_file.filename
            topology_file_io.mode = "r"
            topology_file_io.seek(0)
            
            files = [
                entry_script_str_io,
                analysis_main_script_io,
                mutant_pdb_io,
                trajectory_file_io,
                topology_file_io,
            ]
            slurm_request = SlurmJobRequest()
            status, message, job_uuid = SlurmJobData.post(slurm_request=slurm_request, files=files)
            
            # TODO: Submit Analysis Slurm Job.
            
            if (job_uuid):
                result = Result(
                    experiment_id=experiment.id,
                    pdb_filename=experiment.pdb_filename,
                    mutant=mutant_name,
                    replica_id=replica_id,
                    slurm_job_uuid=job_uuid,
                )
                result.insert_or_update()

            response_info = ExperimentBehaviourResponseInfo(
                experiment=experiment,
                user=user,
                message=message,
                is_successful=(True if job_uuid else False),
                slurm_job_uuid=job_uuid
            )
            return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)

    @login_required
    def put(self, experiment_id: str):
        """Update experiment information and configuration.
        
        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        user: User = current_user
        experiment = Experiment.get(experiment_id)

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (experiment.user_id != user.id):
            return forbidden_response(user, experiment)
        
        editable_attrs = ["name", "description", "metrics", "constraints"] # Only fields in the list are editable.
        stringfied_list_attrs = ["metrics", "constraints"]
        
        info_mapper = dict()
        for key, value in request.form.items():
            if (key in stringfied_list_attrs):
                try:
                    loaded_value = loads(value)
                    info_mapper[key] = loaded_value
                except:

                    pass
            else:
                info_mapper[key] = value
            continue

        updated_attrs, blocked_attrs, nonexistent_attrs, message = experiment.update_attributes(
            mapper=info_mapper, editable_attrs=editable_attrs
        )

        if (not (updated_attrs or blocked_attrs or nonexistent_attrs)):
            response_info = ExperimentBehaviourResponseInfo(
                experiment, user,
                is_successful=True,
                message="Nothing to be updated.",
                updated_attrs=updated_attrs,
                blocked_attrs=blocked_attrs,
                nonexistent_attrs=nonexistent_attrs,
            )
            return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)
        elif (updated_attrs):
            response_info = ExperimentBehaviourResponseInfo(
                experiment, user,
                is_successful=True,
                message=message,
                updated_attrs=updated_attrs,
                blocked_attrs=blocked_attrs,
                nonexistent_attrs=nonexistent_attrs,
            )
            return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)
        else:
            response_info = ExperimentBehaviourResponseInfo(
                experiment, user,
                is_successful=False,
                message=message,
                updated_attrs=updated_attrs,
                blocked_attrs=blocked_attrs,
                nonexistent_attrs=nonexistent_attrs,
            )
            return Response(response=response_info.serialize(), status=400, mimetype=JSONIFY_MIMETYPE)

    @jwt_required()
    def patch(self, experiment_id: str):
        """Update the status and progress of the experiment, with JWT authentication.
        
        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        user: User = User.get(get_jwt_identity())
        experiment = Experiment.get(experiment_id)

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (user is None or experiment.user_id != user.id):
            return forbidden_response(user, experiment)
        
        editable_attrs = ['status', 'progress'] # Only fields in the list are editable.
        
        updated_attrs, blocked_attrs, nonexistent_attrs, message = experiment.update_attributes(
            experiment, mapper=request.form, editable_attrs=editable_attrs
        )

        if (not (updated_attrs or blocked_attrs or nonexistent_attrs)):
            response_info = ExperimentBehaviourResponseInfo(
                experiment, user,
                is_successful=True,
                message='Nothing to be updated.',
                updated_attrs=updated_attrs,
                blocked_attrs=blocked_attrs,
                nonexistent_attrs=nonexistent_attrs,
            )
            return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)
        elif (updated_attrs):
            # experiment.updated_time = datetime.now()
            # db.session.commit()
            response_info = ExperimentBehaviourResponseInfo(
                experiment, user,
                is_successful=True,
                message=message,
                updated_attrs=updated_attrs,
                blocked_attrs=blocked_attrs,
                nonexistent_attrs=nonexistent_attrs,
            )
            return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)
        else:
            response_info = ExperimentBehaviourResponseInfo(
                experiment, user,
                is_successful=False,
                message=message,
                updated_attrs=updated_attrs,
                blocked_attrs=blocked_attrs,
                nonexistent_attrs=nonexistent_attrs,
            )
            return Response(response=response_info.serialize(), status=400, mimetype=JSONIFY_MIMETYPE)

class ResultApi(Resource):
    """Route: `/<experiment_id>/result`."""
    
    @login_required
    def get(self, experiment_id: str):
        """(TODO) Get the analysis result of a selected experiment instance.

        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        user: User = current_user
        experiment = Experiment.get(experiment_id)

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (experiment.user_id != user.id):
            return forbidden_response(user, experiment)
        pass

    @jwt_required
    def post(self, experiment_id: str):
        """Post new analysis result to a selected experiment instance.
        
        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        user: User = User.get(get_jwt_identity())
        experiment = Experiment.get(experiment_id)

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (user is None or experiment.user_id != user.id):
            return forbidden_response(user, experiment)
        
        result_record = dict()
        for key, value in request.form.items():
            result_record[key] = value
            continue
        experiment.post_result(result_record=result_record)

class PdbFileApi(Resource):
    """Route: `/<experiment_id>/pdb_file`"""

    @login_required
    def get(self, experiment_id: str):
        """Download the PDB file attached to the experiment.
        If the desired experiment doesn't exist or the selected experiment instance does not have PDB file attached, 404 NOT FOUND will be the response.
            
        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        user: User = current_user
        experiment = Experiment.get(experiment_id)

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (experiment.user_id != user.id):
            return forbidden_response(user, experiment)    
        if not experiment.has_pdb_file:
            return no_pdb_response()
        else:
            return send_file(path_or_file=experiment.pdb_filepath, mimetype="text/plain",
                as_attachment=False, 
                download_name=experiment.pdb_filename, 
                attachment_filename=experiment.pdb_filename)

    @login_required
    def post(self, experiment_id: str):
        """Upload and Validate PDB File from the user.
        
        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        user: User = current_user
        experiment = Experiment.get(experiment_id)
        message = str()
        is_updated = False

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (experiment.user_id != user.id):
            return forbidden_response(user, experiment)
        
        pdb_file = request.files.get("file")
        force_update = False if request.form.get("force", "").lower() in ["false", "0", "no", ""] else True # Whether to skip verification and force update of PDB files.
        is_updated, is_supported, message = experiment.update_pdb(pdb_file=pdb_file, force_update=force_update)

        response_info = ExperimentBehaviourResponseInfo(experiment=experiment, user=user,
            is_successful=is_updated,
            message=message)
        return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)

class MutationApi(Resource):
    """Route: `/<experiment_id>/mutations`."""

    @login_required
    def get(self, experiment_id: str):
        """Return the current mutation space information of the experiment.
            
        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        user: User = current_user
        experiment = Experiment.get(experiment_id)

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (experiment.user_id != user.id):
            return forbidden_response(user, experiment)
        
        is_successful, mutant_string_list, message = experiment.get_mutants_string_list()
        
        response_info = ExperimentBehaviourResponseInfo(
            experiment=experiment,
            user=user,
            is_successful=is_successful,
            message=message,
            mutant_string_list=mutant_string_list,
        )
        return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)

    @login_required
    def post(self, experiment_id: str):
        """Generate mutation space (mutation pattern) based on natural language inputs.
        
        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        user: User = current_user
        experiment = Experiment.get(experiment_id)

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (experiment.user_id != user.id):
            return forbidden_response(user, experiment)
        if not experiment.has_pdb_file:
            return no_pdb_response(user, experiment)

        mutation_request = request.form.get("mutation_request")

        instructions = open(os.path.join(BASEDIR, "prompts", "mutant_planner-v1.txt")).read()
        service = OpenAIAssistant(user.openai_secret_key, 
            assistant_name="Mutant Planner", 
            instructions=instructions, 
            model="gpt-4o", 
            conversation_mode=False
        )
        is_openai_key_valid, status_code, response_content = service.ask_gpt(prompt=mutation_request)

        response_content = response_content.replace("Output: ", "").strip('"')
        
        if (status_code != 200):
            response_info = ExperimentBehaviourResponseInfo(experiment=experiment, user=user, is_successful=False, message=response_content)
            return Response(response_info.serialize(), status=status_code, mimetype=JSONIFY_MIMETYPE)
        mutation_pattern = response_content

        is_successful, mutant_string_list, message = experiment.update_mutation_pattern(mutation_pattern=mutation_pattern, freeze=True)

        response_info = ExperimentBehaviourResponseInfo(experiment=experiment, user=user,
            is_successful=is_successful, message=f"Received response from OpenAI. {message}",
            mutation_pattern=mutation_pattern, mutant_string_list=mutant_string_list)
        return Response(response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)

    @login_required
    def put(self, experiment_id: str):
        """Update the mutation space according to formdata mutation_pattern or the uploaded .csv/.xlsx/.xls files.
        
        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        allowed_extensions = [".csv", ".xlsx", ".xls"]
        column_name = WORKSHEET_MUTATION_COLUMN_NAME

        user: User = current_user
        experiment = Experiment.get(experiment_id)

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (experiment.user_id != user.id):
            return forbidden_response(user, experiment)
        if not experiment.has_pdb_file:
            return no_pdb_response(user, experiment)

        mutation_pattern = request.form.get("mutation_pattern", None)
        if (mutation_pattern):
            is_successful, mutant_string_list, message = experiment.update_mutation_pattern(mutation_pattern=mutation_pattern, freeze=True)
            response_info = ExperimentBehaviourResponseInfo(
                experiment=experiment,
                user=user,
                is_successful=is_successful,
                message=message,
                mutation_pattern=mutation_pattern,
                mutant_string_list=mutant_string_list,
            )
            return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)
        else:
            file = request.files.get("file", None)
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                response_info = ExperimentBehaviourResponseInfo(
                    experiment=experiment,
                    user=user,
                    is_successful=False,
                    message="The selected/uploaded file doesn't exist.",
                    is_authenticated=True,
                )
                return Response(response=response_info.serialize(), status=400, mimetype=JSONIFY_MIMETYPE)
            
            file_ext = fs.get_file_ext(file.filename).lower()
            
            if file and (file_ext in allowed_extensions):
                # Check the file extension to determine the file type
                df = pd.DataFrame(None)
                try:
                    if file_ext in ['.xlsx', '.xls']:
                        df = pd.read_excel(file, engine='openpyxl')
                    else:
                        df = pd.read_csv(file)
                except Exception as e:
                    response_info = ExperimentBehaviourResponseInfo(
                        experiment=experiment,
                        user=user,
                        is_successful=False,
                        message="The file you uploaded is damaged, or the file content does not match its extension.",
                        is_authenticated=True,
                    )
                    return Response(response=response_info.serialize(), status=415, mimetype=JSONIFY_MIMETYPE)

                # Try to read the column containing mutation info from the DataFrame.
                if column_name in df.columns:
                    # Convert the column to a list and send it back
                    mutation_list = df[column_name].tolist()
                    mutation_pattern = (",".join(["{}{}{}".format("{", mutation, "}") for mutation in mutation_list])).replace(" ", "")
                    is_successful, mutant_string_list, message = experiment.update_mutation_pattern(mutation_pattern=mutation_pattern, freeze=True)
                    response_info = ExperimentBehaviourResponseInfo(
                        experiment=experiment,
                        user=user,
                        is_successful=is_successful,
                        message=message,
                        mutation_pattern=mutation_pattern,
                        mutant_string_list=mutant_string_list,
                    )
                    return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)
                else:
                    # Column not found in the DataFrame.
                    response_info = ExperimentBehaviourResponseInfo(
                        experiment=experiment,
                        user=user,
                        is_successful=False,
                        message=f"Column '{column_name}' is not found.",
                    )
                    return Response(response=response_info.serialize(), status=404, mimetype=JSONIFY_MIMETYPE)
            else:
                # File extension is not allowed
                response_info = ExperimentBehaviourResponseInfo(
                    experiment=experiment,
                    user=user,
                    is_successful=False,
                    message=f"{file_ext} is an unsupported file format. Only {', '.join(allowed_extensions)} files are supported.",
                    is_authenticated=True,
                )
                return Response(response=response_info.serialize(), status=415, mimetype=JSONIFY_MIMETYPE)

#region OpenAI Assistants

class AssistantsApi(Resource):
    """Route: `/<experiment_id>/assistants`"""

    @login_required
    def get(self, experiment_id: str):
        """Get the messages of the OpenAI Thread instance associated with the specific experiment instance.
        
        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        user: User = current_user
        experiment = Experiment.get(experiment_id)

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (user is None or experiment.user_id != user.id):
            return forbidden_response(user, experiment)
        
        is_successful, assistant_messages = OpenAIAssistant.get_thread_messages(
            openai_secret_key=user.openai_secret_key,
            thread_id=experiment.current_thread_id,
            limit=50
        )
        _, mutant_string_list, _ = experiment.get_mutants_string_list()
        configuration_stages = [
            {
                "title": "Wild Type",
                "content": experiment.pdb_filename if experiment.has_pdb_file else str(),
                "is_completed": experiment.has_pdb_file,
            },
            {
                "title": "Research Question",
                "content": assistant_messages[0]["text_value"] if len(assistant_messages) else str(),
                "is_completed": experiment.current_assistant_type > 0,
            },
            {
                "title": "Target Metrics",
                "content": ", ".join([metric.get("name") for metric in experiment.metrics]),
                "is_completed": experiment.current_assistant_type > 1,
            },
            {
                "title": "Target Mutants",
                "content": ", ".join(mutant_string_list),
                "is_completed": experiment.current_assistant_type > 2,
            }
        ]
        response_info = ExperimentBehaviourResponseInfo(experiment=experiment, user=user,
            is_successful=is_successful,
            configuration_stages=configuration_stages,
            assistant_messages=assistant_messages,
        )
        return Response(response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)

    @login_required
    def post(self, experiment_id: str):
        """Call the virtual assistants to analyze questions and plan the experiment.
        
        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        # When the response_content contains any element in the list, the task of this agent is confirmable.
        confirm_signals = ["please confirm", "can finalize", "final output", "can proceed", "will proceed", "further", "to review"]

        user: User = current_user
        experiment = Experiment.get(experiment_id)

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (user is None or experiment.user_id != user.id):
            return forbidden_response(user, experiment)
        
        user_prompt = request.form.get("prompt", str())
        current_assistant_class = AGENT_MAPPER[experiment.current_assistant_type % len(AGENT_MAPPER)]
        # print([current_assistant_class])
        current_assistant: DefinedAgent = current_assistant_class(
            openai_secret_key=user.openai_secret_key, 
            thread_id=experiment.current_thread_id, 
            conversation_mode=True,
            experiment=experiment,
        )
        # print(f"Current Assistant: {current_assistant.assistant.name}")
        
        is_openai_key_valid, status_code, response_content = current_assistant.ask_gpt(prompt=user_prompt)
        
        if (status_code != 200):
            response_info = ExperimentBehaviourResponseInfo(experiment=experiment, user=user, is_successful=False, message=response_content)
            return Response(response_info.serialize(), status=status_code, mimetype=JSONIFY_MIMETYPE)

        configuration_updated, updated_attributes = experiment.parse_agent_response_content(response_content=response_content)
        response_info = ExperimentBehaviourResponseInfo(experiment=experiment, user=user,
            is_successful=is_openai_key_valid, 
            message=f"Received response from OpenAI. Updates to the experiment configuration may be triggered.",
            response_content=response_content,
            has_pdb_file=experiment.has_pdb_file,
            confirm_button=(status_code == 200 and any(signal in response_content.lower() for signal in confirm_signals)),
            tool_call_result=current_assistant.latest_tool_call_result,
            configuration_updated=configuration_updated,
            updated_attributes=updated_attributes,
        )

        # Update the current_assistant_type and current_thread_id to database.
        _ = experiment.update_attributes(
            mapper={
                "current_assistant_type": experiment.current_assistant_type,
                "current_thread_id": current_assistant.thread.id,
            },
            # editable_attrs=editable_attributes,
        )
        return Response(response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)

    @login_required
    def put(self, experiment_id: str):
        """Toggle to the next the virtual assistants when the job of one assistant is completed.
        
        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        user: User = current_user
        experiment = Experiment.get(experiment_id)

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (user is None or experiment.user_id != user.id):
            return forbidden_response(user, experiment)
        
        experiment.current_assistant_type += 1
        updated_attrs, blocked_attrs, nonexistent_attrs, message = experiment.update_attributes(
            mapper={
                "current_assistant_type": experiment.current_assistant_type,
            },
        )
        if (updated_attrs):
            response_info = ExperimentBehaviourResponseInfo(
                experiment, user,
                is_successful=True,
                message=message)
            return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)
        else:
            response_info = ExperimentBehaviourResponseInfo(
                experiment, user,
                is_successful=False,
                message=message)
            return Response(response=response_info.serialize(), status=400, mimetype=JSONIFY_MIMETYPE)

    @login_required
    def delete(self, experiment_id: str):
        """Clear all the thread context associated with the experiment.
        
        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        user: User = current_user
        experiment = Experiment.get(experiment_id)

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (user is None or experiment.user_id != user.id):
            return forbidden_response(user, experiment)
        
        is_successful = False
        if (experiment.current_thread_id):
            is_successful = OpenAIAssistant.delete_thread(
                openai_secret_key=user.openai_secret_key, 
                thread_id=experiment.current_thread_id
            )
        else:
            is_successful = True
        
        if (is_successful):
            experiment.update_attributes(
                mapper={
                    "current_assistant_type": 0,
                    "current_thread_id": "",
                }
            )
            response_info = ExperimentBehaviourResponseInfo(
                experiment, user,
                is_successful=is_successful,
                message="Your conversation is successfully cleared.")
            return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)
        else:
            response_info = ExperimentBehaviourResponseInfo(
                experiment, user,
                is_successful=is_successful,
                message="Your conversation is unable to be cleared at present.")
            return Response(response=response_info.serialize(), status=403, mimetype=JSONIFY_MIMETYPE)

#endregion

#region Slurm Jobs.

from io import StringIO, BytesIO
from os.path import basename
from zipfile import ZipFile, ZIP_DEFLATED

from services import SlurmJobRequest, SlurmJobData

class SlurmCorrespondenceApi(Resource):
    """Route: `/<experiment_id>/slurm`."""

    @login_required
    def get(self, experiment_id: str):
        """Fetch the information of the job relevant to this experiment from the slurm cluster.
        
        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        user: User = current_user
        experiment = Experiment.get(experiment_id)

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (experiment.user_id != user.id):
            return forbidden_response(user, experiment)
        
        if (not experiment.slurm_job_uuid):
            response_info = ExperimentBehaviourResponseInfo(
                experiment=experiment,
                user=user,
                message="Slurm job information is not contained in the current experiment.",
                is_authenticated=True,
                is_successful=False,
            )
            return Response(response=response_info.serialize(), status=404, mimetype=JSONIFY_MIMETYPE)

        status, slurm_job_data = SlurmJobData.get(experiment.slurm_job_uuid)
        if (slurm_job_data):
            if (slurm_job_data.job_state == "FAILED"):
                experiment.status = StatusCode.EXIT_WITH_ERROR
                db.experiments.update_one({"id": experiment.id}, {"$set": {"status": experiment.status}})
                # db.session.commit()
            response_info = ExperimentBehaviourResponseInfo(
                experiment=experiment,
                user=user,
                message="Slurm job information is successfully fetched.",
                is_authenticated=True,
                data=slurm_job_data.as_dict(),
            )
        elif (status == 404):
                response_info = ExperimentBehaviourResponseInfo(
                    experiment=experiment,
                    user=user,
                    message="The Slurm Job record exists in the database but was erased in the cluster. You can delete this slurm job record and submit a new one.",
                    is_authenticated=True,
                    is_successful=False,
                )
        else:
            response_info = ExperimentBehaviourResponseInfo(
                experiment=experiment,
                user=user,
                message="Slurm job information is not able to be fetched.",
                is_authenticated=True,
                is_successful=False,
            )
        return Response(response=response_info.serialize(), status=status, mimetype=JSONIFY_MIMETYPE)

    @login_required
    def post(self, experiment_id: str):
        """Submit Slurm jobs to the cluster.
        
        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        user: User = current_user
        experiment = Experiment.get(experiment_id)

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (experiment.user_id != user.id):
            return forbidden_response(user, experiment)
        
        if (experiment.slurm_job_uuid):
            response_info = ExperimentBehaviourResponseInfo(
                experiment=experiment,
                user=user,
                message="Slurm job is already submitted. You cannot submit another job unless you delete the current one.",
                is_authenticated=True,
                is_successful=False,
            )
            return Response(response=response_info.serialize(), status=409, mimetype=JSONIFY_MIMETYPE)
        elif not experiment.has_pdb_file:
            return no_pdb_response()
        else:
            experiment_mutant_count = experiment.mutant_count
            if (experiment_mutant_count > MAX_MUTANT_COUNT):
                response_info = ExperimentBehaviourResponseInfo(
                    experiment=experiment,
                    user=user,
                    message=f"The experiment contains {experiment_mutant_count} mutants, which exceeds the number that our server can support (no more than {MAX_MUTANT_COUNT}). Please deploy it to your or your institution's own cluster for computation.",
                    is_authenticated=True,
                    is_successful=False,
                )
                return Response(response=response_info.serialize(), status=429, mimetype=JSONIFY_MIMETYPE)
            else:
                # is_successful, mutant_count, message = experiment.make_mutants_pdb_files()
                pass

            slurm_request = SlurmJobRequest()

            entry_script_str_io = StringIO()
            entry_script_str_io.write(Template(SLURM_MD_JOB_ENTRY_SCRIPT_CONTENT).safe_substitute({
                "username": user.username,
                "app_host": APP_HOST,
                "experiment_id": experiment.id,
                "pdb_filename": experiment.pdb_filename,
                "metrics": dumps(experiment.metrics),
                "access_token": create_access_token(identity=user.id, expires_delta=TOKEN_EXPIRES_DELTA),
                "mutation_pattern": experiment.mutation_pattern,
                "constraints_str": dumps(experiment.constraints)
            }))
            entry_script_str_io.name = SLURM_MD_JOB_ENTRY_SCRIPT
            entry_script_str_io.mode = "r"
            entry_script_str_io.seek(0)

            pdb_file_io = open(experiment.pdb_filepath)
            pdb_file_io.seek(0)

            md_main_script_io = open(SLURM_MD_JOB_MAIN_SCRIPT_FILEPATH)
            md_main_script_io.seek(0)
            analysis_main_script_io = open(SLURM_ANALYSIS_JOB_MAIN_SCRIPT_FILEPATH)
            analysis_main_script_io.seek(0)

            files = [
                entry_script_str_io,
                md_main_script_io,
                analysis_main_script_io,
                pdb_file_io,
            ]
            status, message, job_uuid = SlurmJobData.post(slurm_request=slurm_request, files=files)
            
            if (job_uuid):
                experiment.slurm_job_uuid = job_uuid
                experiment.status = StatusCode.PENDING
            db.experiments.update_one({"id": experiment.id}, {"$set": {"status": experiment.status, "slurm_job_uuid": experiment.slurm_job_uuid}})
            # db.session.commit()

            response_info = ExperimentBehaviourResponseInfo(
                experiment=experiment,
                user=user,
                message=message,
                is_authenticated=True,
                is_successful=True if job_uuid else False,
                slurm_job_uuid=job_uuid
            )
            return Response(response=response_info.serialize(), status=status, mimetype=JSONIFY_MIMETYPE)

    @login_required
    def delete(self, experiment_id: str):
        """Delete the Slurm jobs relevant to this experiment.
        
        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        user: User = current_user
        experiment = Experiment.get(experiment_id)

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (experiment.user_id != user.id):
            return forbidden_response(user, experiment)

        if (experiment.slurm_job_uuid):
            status, message = SlurmJobData.delete(experiment.slurm_job_uuid)
            if (status == 200):
                response_info = ExperimentBehaviourResponseInfo(
                    experiment=experiment,
                    user=user,
                    message=message,
                    is_authenticated=True,
                    is_successful=True,
                )
                experiment.slurm_job_uuid = None
                experiment.status = StatusCode.CANCELLED
                db.experiments.update_one({"id": experiment.id}, {"$set": {"status": experiment.status, "slurm_job_uuid": experiment.slurm_job_uuid}})
                # db.session.commit()
            elif (status == 404):
                response_info = ExperimentBehaviourResponseInfo(
                    experiment=experiment,
                    user=user,
                    message="The Slurm Job record exists in the database but was erased in the cluster. Set Job UUID to None.",
                    is_authenticated=True,
                    is_successful=True,
                )
                status = 200
                experiment.slurm_job_uuid = None
                experiment.status = StatusCode.CANCELLED
                db.experiments.update_one({"id": experiment.id}, {"$set": {"status": experiment.status, "slurm_job_uuid": experiment.slurm_job_uuid}})
                # db.session.commit()
            else:
                response_info = ExperimentBehaviourResponseInfo(
                    experiment=experiment,
                    user=user,
                    message=message,
                    is_authenticated=True,
                    is_successful=False,
                )
            return Response(response=response_info.serialize(), status=status, mimetype=JSONIFY_MIMETYPE)
        else:
            response_info = ExperimentBehaviourResponseInfo(
                experiment=experiment,
                user=user,
                message="Slurm job information is not contained in the current experiment.",
                is_authenticated=True,
                is_successful=False,
            )
            return Response(response=response_info.serialize(), status=404, mimetype=JSONIFY_MIMETYPE)

class SlurmTokenApi(Resource):
    """Route: `/slurm/token`."""

    @login_required
    def get(self):
        """Get the current `token` and `refresh_token` for Vanderbilt ACCRE Slurm API."""
        user: User = current_user
        if (not user.admin):
            return notadmin_handler(user=user)

        if_exist, token, refresh_token = SlurmJobRequest.get_slurm_token()
        response_info = ExperimentBehaviourResponseInfo(
            experiment=None,
            user=user,
            message="The token and refresh_token is as follows.",
            is_authenticated=True,
            is_successful=True,
            if_exist=if_exist,
            token=token,
            refresh_token=refresh_token,
        )
        return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)

    @login_required
    def post(self):
        """Update the `token` and/or `refresh_token` for Vanderbilt ACCRE Slurm API."""
        user: User = current_user
        if (not user.admin):
            return notadmin_handler(user=user)

        token = request.form.get("token", "")
        refresh_token = request.form.get("refresh_token", "")
        is_updated, message = SlurmJobRequest.update_slurm_tokens(token=token, refresh_token=refresh_token)
        response_info = ExperimentBehaviourResponseInfo(
            experiment=None,
            user=user,
            message=message,
            is_authenticated=True,
            is_successful=is_updated,
        )
        return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)

    @login_required
    def put(self):
        """Refresh the `token` and/or `refresh_token` for Vanderbilt ACCRE Slurm API."""
        user: User = current_user
        if (not user.admin):
            return notadmin_handler(user=user)

        is_updated, status_code, message = SlurmJobRequest.refresh_slurm_token()
        response_info = ExperimentBehaviourResponseInfo(
            experiment=None,
            user=user,
            message=message,
            is_authenticated=True,
            is_successful=is_updated,
        )
        return Response(response=response_info.serialize(), status=status_code, mimetype=JSONIFY_MIMETYPE)

class SlurmDeployApi(Resource):
    """Route: `/<experiment_id>/deploy`."""

    @login_required
    def get(self, experiment_id: str):
        """Download the MD simulation script to run MD by the users themselves.
        
        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        user: User = current_user
        experiment = Experiment.get(experiment_id)

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (experiment.user_id != user.id):
            return forbidden_response(user, experiment)
        
        # is_successful, mutant_count, message = experiment.make_mutants_pdb_files()
        
        deploy_script = Template(SLURM_DEPLOY_SCRIPT).safe_substitute({
            "pdb_filename": experiment.pdb_filename
        })

        deploy_pack_io = BytesIO()
        deploy_pack_zip = ZipFile(deploy_pack_io, "w")

        deploy_pack_zip.writestr(SLURM_DEPLOY_SCRIPT_FILENAME, deploy_script.encode("utf-8"), compress_type=ZIP_DEFLATED)       # Add bash into zip.
        deploy_pack_zip.write(experiment.pdb_filepath, arcname=experiment.pdb_filename, compress_type=ZIP_DEFLATED)   # Add PDB file into zip.
        
        deploy_pack_zip.close()
        deploy_pack_io.seek(0)
        zipfile_prefix = re.sub(r'[\\/:"*?<>|]', '', experiment.name)
        return send_file(deploy_pack_io, mimetype="application/zip", as_attachment=True, download_name=f"{zipfile_prefix} Deploy Pack.zip")

#endregion