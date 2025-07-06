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
from .experiment_config import StatusCode
from .agents import ResultExplainerAssistant
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
    JSONIFY_MIMETYPE,

    # Slurm API.
    SLURM_USER,

    SLURM_MD_JOB_ENTRY_SCRIPT,
    SLURM_MD_JOB_ENTRY_SCRIPT_CONTENT,
    SLURM_MD_JOB_MAIN_SCRIPT_FILEPATH,
    SLURM_ANALYSIS_JOB_ENTRY_CONTENT,
    SLURM_ANALYSIS_JOB_MAIN_SCRIPT_FILEPATH,
    
    SLURM_DEPLOY_SCRIPT_FILENAME, 
    SLURM_DEPLOY_SCRIPT, 
    MAX_MUTANT_COUNT,

    PLHD_RESULT_IMG_PATHS,
    PLHD_RESULT_INTERPRETATION,
)
from services import image_path_to_src

# Here put enzy_htp modules.
from enzy_htp.core import (
    file_system as fs,
    _LOGGER
)

db = mongo.db

#region Experiment Response Body and Handlers.

class ExperimentIndexResponse():
    """Experiment Index Information Response Body."""

    default_order_by_field = "updated_time"
    default_items_on_page = 25
    default_reverse_option = True
    
    def __init__(self, experiments: List[Experiment], page_index: int = 1, 
            items_on_page: int = default_items_on_page,
            order_by: str = default_order_by_field,
            reverse: bool = default_reverse_option,
        ):
        """Experiment Index Information Response Body.
        
        Args:
            experiments (List[Experiment]): The list of user's experiments.
            page_index (int): The index of the page to get.
            items_on_page (int): Maximum number of items to be displayed on each page.
            order_by (str): The field by which to sort the results.
            reverse (bool): If to reverse the order of results.
        """
        user: User = current_user
        self.user_id = user.id
        self.email = user.email
        self.username = user.username
        self.timestamp = str(datetime.now())
        self.experiments = list()
        for exp in experiments:
            exp_dict = exp.as_dict(stringfy_time=True)
            del exp_dict["user_id"]
            if ("chat_messages") in exp_dict.keys():
                del exp_dict["chat_messages"]
            exp_dict["status_text"] = StatusCode.status_text_mapper.get(exp.status)
            self.experiments.append(exp_dict)
            continue

        items_on_page = items_on_page if (items_on_page > 0) else self.default_items_on_page
        self.page_count = (len(experiments)-1) // items_on_page + 1
        self.page_index = page_index if (page_index <= self.page_count) else self.page_count
        if (self.experiments):
            if (not hasattr(experiments[0], order_by)):
                order_by = self.default_order_by_field
            self.experiments = sorted(self.experiments, key=lambda x: x[order_by], reverse=reverse)
            starting_item_index = (self.page_index - 1) * items_on_page
            ending_item_index = (self.page_index * items_on_page + 1) if (self.page_index < self.page_count) else len(self.experiments)
            self.experiments = self.experiments[starting_item_index:ending_item_index]
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
        """Get the experiment list belonging to `current_user`."""
        page_index = int(request.args.get("page", 1))   # Which page to get?
        items_on_page = int(request.args.get(           # How many items to be displayed on each page?
            "items", ExperimentIndexResponse.default_items_on_page
        ))
        order_by = request.args.get(                    # The field by which to sort the results.
            "order_by", ExperimentIndexResponse.default_order_by_field
        )
        reverse = False if request.form.get("reverse", "True").lower() in ["false", "0", "no"] else True  # If to reverse the order of results.
        
        user: User = current_user
        experiments = Experiment.get_user_experiments(user=user)
        response_body = ExperimentIndexResponse(experiments, page_index, items_on_page, order_by, reverse)
        return Response(response=response_body.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)

    @login_required
    def post(self):
        """Create new experiment instance."""
        user: User = current_user
        
        name = request.form.get("name", f"{user.username}'s experiment")
        experiment_type = int(request.form.get("type", Experiment.INDIVIDUAL_TYPE))
        description = request.form.get("description")

        experiment = Experiment(user_id=user.id, name=name, experiment_type=experiment_type, description=description)
        db.experiments.insert_one(experiment.as_dict())
        response_info = ExperimentBehaviourResponseInfo(experiment=experiment, user=user)

        file = request.files.get("file", None)
        force_update = request.form.get("force", True) # Whether to skip verification and force update of PDB files.

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
        
        if (experiment.type == experiment.GROUP_TYPE):
            delete_flag = True
            for sub_exp in experiment.subordinate_experiments:
                if (sub_exp.status in StatusCode.queued_status):
                    delete_flag = False
                continue
            if (delete_flag):
                for sub_exp in experiment.subordinate_experiments:
                    sub_exp.clear_folder(remove_folder=True)
                    db.experiments.delete_one({"id": sub_exp.id})
                    db.results.delete_many({"experiment_id": sub_exp.id})
                    continue
            else:
                response_info = ExperimentBehaviourResponseInfo(experiment, user,
                    is_successful=False, 
                    message=f"The experiment instance '{experiment_id}' hasn't completed or exited, which is unable to be deleted.")
                return Response(response=response_info.serialize(), status=400, mimetype=JSONIFY_MIMETYPE)
        
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
            OpenAIAssistant.delete_threads(
                openai_secret_key=user.openai_secret_key, 
                thread_id_list=experiment.thread_id_list
            )
            experiment.clear_folder(remove_folder=True)
            db.experiments.delete_one({"id": experiment.id})
            db.results.delete_many({"experiment_id": experiment_id})
            # db.session.delete(experiment)
            # db.session.commit()
            response_info = ExperimentBehaviourResponseInfo(experiment, user,
                is_successful=True, message=f"The experiment instance '{experiment.id}' is successfully deleted.")
            return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)

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
        
        return Response(experiment.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)

    @jwt_required()
    def post(self, experiment_id: str):
        """Post the trajectory of MD simulation back into the website and send for analysis.
        
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
            # analysis_entry_script_path = os.path.join(experiment.directory, "analysis_entry_script.sh")
            # with open(analysis_entry_script_path, "w") as fobj:
            #     fobj.write(Template(SLURM_ANALYSIS_JOB_ENTRY_CONTENT).safe_substitute({
            #         "app_host": APP_HOST,
            #         "experiment_id": experiment.id,
            #         "access_token": create_access_token(identity=user.id, expires_delta=TOKEN_EXPIRES_DELTA),
            #         "pdb_filename": experiment.pdb_filename,
            #         "ref_pdb_filename": basename(mutant_pdb_filepath),
            #         "metrics": dumps(experiment.metrics),
            #         "topology_filename": topology_file.filename,
            #         "trajectory_filename": trajectory_file.filename,
            #     }))
            #     fobj.close()

            entry_script_content = Template(SLURM_ANALYSIS_JOB_ENTRY_CONTENT).safe_substitute({
                "slurm_user": SLURM_USER,
                "app_host": APP_HOST,
                "experiment_id": experiment.id,
                "access_token": create_access_token(identity=user.id, expires_delta=TOKEN_EXPIRES_DELTA),
                "pdb_filename": experiment.pdb_filename,
                "ref_pdb_filename": basename(mutant_pdb_filepath),
                "metrics": dumps(experiment.metrics),
                "topology_filename": topology_file.filename,
                "trajectory_filename": trajectory_file.filename,
            })
            
            file_list = [
                # analysis_entry_script_path,
                SLURM_ANALYSIS_JOB_MAIN_SCRIPT_FILEPATH,
                mutant_pdb_filepath,
                trajectory_file,
                topology_file,
            ]
            slurm_request = SlurmJobRequest()
            status, message, job_uuid = SlurmJobData.post(
                slurm_request=slurm_request, file_list=file_list, 
                # entry_script_filename=analysis_entry_script_path,
                entry_script_content=entry_script_content,
            )
            
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
        
        try:
            experiment.status = int(request.form.get("status", experiment.status))
        except (ValueError):
            pass
        try:
            experiment.progress = float(request.form.get("progress", experiment.progress))
        except (ValueError):
            pass
        
        updated_attrs, blocked_attrs, nonexistent_attrs, message = experiment.update_attributes(
            mapper={
                "status": experiment.status,
                "progress": experiment.progress,
            }
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
        """Get the analysis result of a selected experiment instance.

        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        user: User = current_user
        experiment = Experiment.get(experiment_id)

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (experiment.user_id != user.id):
            return forbidden_response(user, experiment)
        
        experiment_results = Result.get_experiment_results(experiment_id=experiment_id)

        # result_images = [image_path_to_src(path) for path in PLHD_RESULT_IMG_PATHS]
        result_images = []  # Set `result_images` to empty list.

        if (not experiment.result_interpretation):
            _ = AssistantsApi.get_scientific_question(user=user, experiment=experiment)
            result_explainer = ResultExplainerAssistant(
                openai_secret_key=user.openai_secret_key, 
                conversation_mode=False,
                experiment=experiment
            )
            is_valid, status, experiment.result_interpretation = result_explainer.ask_gpt()
            experiment.update_attributes({"result_interpretation": experiment.result_interpretation})

        response_info = ExperimentBehaviourResponseInfo(
            experiment=experiment,
            user=user,
            message="The experiment results are fetched.",
            is_successful=(True if experiment_results else False),
            experiment_results=experiment_results,
            result_images=result_images,
            result_interpretation=experiment.result_interpretation,
            downloadable_files=experiment.downloadable_files()
        )
        return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)

    @jwt_required()
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
        
        result_record = request.form.copy()
        result_record["slurm_job_uuid"] = experiment.slurm_job_uuid
        experiment.post_result(result_record=result_record)
        return

class DownloadableApi(Resource):
    """Route: `/<experiment_id>/downloadable`"""

    @login_required
    def get(self, experiment_id: str):
        """Get a .zip format compress file containing downloadable files.

        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        user: User = current_user
        experiment = Experiment.get(experiment_id)

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (experiment.user_id != user.id):
            return forbidden_response(user, experiment)
        
        deploy_pack_io = BytesIO()
        with ZipFile(deploy_pack_io, "w") as deploy_pack_zip:
            deploy_pack_zip.write(experiment.pdb_filepath, arcname=experiment.pdb_filename, compress_type=ZIP_DEFLATED)   # Add PDB file into zip.
        
        deploy_pack_io.seek(0)
        zipfile_prefix = re.sub(r'[\\/:"*?<>|]', "", experiment.name)
        return send_file(deploy_pack_io, mimetype="application/zip", as_attachment=True, download_name=f"{zipfile_prefix} Downloadables.zip")

class PdbFileApi(Resource):
    """Route: `/<experiment_id>/pdb_file`"""

    # @login_required
    def get(self, experiment_id: str):
        """Download the PDB file attached to the experiment.
        If the desired experiment doesn't exist or the selected experiment instance does not have PDB file attached, 404 NOT FOUND will be the response.
            
        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
        # user: User = current_user
        experiment = Experiment.get(experiment_id)

        # if (experiment is None):
        #     return notfound_response(user, experiment_id)
        # if (experiment.user_id != user.id):
        #     return forbidden_response(user, experiment)    
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
        experiment: Experiment = Experiment.get(experiment_id)
        message = str()
        is_updated = False

        if (experiment is None):
            return notfound_response(user, experiment_id)
        if (experiment.user_id != user.id):
            return forbidden_response(user, experiment)
        
        pdb_file = request.files.get("file")
        force_update = request.form.get("force", True) # Whether to skip verification and force update of PDB files.
        is_updated, is_supported, message = experiment.update_pdb(pdb_file=pdb_file, force_update=force_update)

        response_info = ExperimentBehaviourResponseInfo(
            experiment=experiment, user=user,
            is_successful=is_updated,
            message=message,
        )
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
from services import OpenAIChat, OpenAIAssistant
from .agents import QuestionAnalyzerAssistant, QuestionSummarizerAssistant, AGENT_MAPPER, DefinedAgent

class AssistantsApi(Resource):
    """Route: `/<experiment_id>/assistants`"""

    @classmethod
    def get_scientific_question(cls, user: User, experiment: Experiment):
        """Get the scientific question from the experiment instance.
        
        Args:
            user (User): The user instance.
            experiment (Experiment): The experiment instance.
        """
        is_successful, messages = OpenAIAssistant.get_thread_messages(
            openai_secret_key=user.openai_secret_key, 
            thread_id=(experiment.thread_id_list[0] if experiment.thread_id_list else experiment.current_thread_id)
        )
        if (is_successful):
            question_summarizer = QuestionSummarizerAssistant(
                openai_secret_key=user.openai_secret_key, conversation_mode=False, experiment=experiment
            )
            is_valid, status_code, experiment.scientific_question = question_summarizer.ask_gpt(
                prompt=dumps(messages)
            )
            experiment.update_attributes(mapper={
                "scientific_question": experiment.scientific_question
            })
        else:
            pass
        return experiment.scientific_question

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
        
        assistant_messages = list()
        if (experiment.chat_messages):
            assistant_messages = experiment.chat_messages
        else:
            # _LOGGER.info(f"Fetching thread ({experiment.current_thread_id}) messages now.")
            is_successful, assistant_messages = OpenAIAssistant.get_thread_messages(
                openai_secret_key=user.openai_secret_key,
                thread_id=experiment.current_thread_id,
                limit=50
            )
            if (is_successful):
                if (not experiment.thread_id_list):
                    experiment.append_thread_id_list(experiment.current_thread_id)
                # _LOGGER.info(f"Replacing the chat_messages {experiment.chat_messages} with value {assistant_messages}.")
                experiment.update_attributes(mapper={
                    "chat_messages": assistant_messages
                })

        response_info = ExperimentBehaviourResponseInfo(experiment=experiment, user=user,
            is_successful=True,
            configuration_stages=experiment.configuration_stages,
            assistant_messages=assistant_messages,
        )
        return Response(response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)

    @login_required
    def post(self, experiment_id: str):
        """Call the virtual assistants to analyze questions and plan the experiment.
        
        Args:
            experiment_id (str): The identifier of an experiment instance.
        """
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

        processed_response_content = current_assistant.post_process(response_content, experiment.summon_next_agent)
        
        # Append the chat message records.
        if (experiment.current_thread_id not in experiment.thread_id_list):
            experiment.append_thread_id_list(new_thread_id=current_assistant.thread.id)
        experiment.append_chat_messages(role="user", text_value=user_prompt)
        experiment.append_chat_messages(role="assistant", text_value=processed_response_content)

        configuration_updated, updated_attributes = experiment.parse_agent_response_content(response_content=processed_response_content)
        response_info = ExperimentBehaviourResponseInfo(experiment=experiment, user=user,
            is_successful=is_openai_key_valid, 
            message=f"Received response from OpenAI. Updates to the experiment configuration may be triggered.",
            response_content=processed_response_content,
            require_pdb_file=experiment.summon_upload_pdb,
            confirm_button=experiment.summon_next_agent,
            tool_call_result=current_assistant.latest_tool_call_result,
            configuration_updated=configuration_updated,
            updated_attributes=updated_attributes,
            configuration_stages=experiment.configuration_stages,
        )

        # Update the current_assistant_type and current_thread_id to database.
        _ = experiment.update_attributes(
            mapper={
                "current_assistant_type": experiment.current_assistant_type,
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
        
        completion_message = str()
        current_assistant_class = AGENT_MAPPER.get(experiment.current_assistant_type % len(AGENT_MAPPER))
        if (issubclass(current_assistant_class, OpenAIAssistant)):
            completion_message = current_assistant_class.completion_message
        
        # Update scientific question if needed.
        _ = self.get_scientific_question(user=user, experiment=experiment)

        updated_attrs, blocked_attrs, nonexistent_attrs, message = experiment.update_attributes(
            mapper={
                "current_assistant_type": experiment.current_assistant_type + 1,
                "summon_next_agent": False,
            },
        )

        if (updated_attrs):
            # Set the value for the last agent completion.
            response_content = "Please press the **Next** button to proceed your experiment configuration."
            configuration_updated = False
            updated_attributes_from_response = list()

            if (experiment.current_assistant_type < len(AGENT_MAPPER)): # If there's next agent, correspond with OpenAI.
                current_assistant_class = AGENT_MAPPER.get(experiment.current_assistant_type % len(AGENT_MAPPER))
                current_assistant: DefinedAgent = current_assistant_class(
                    openai_secret_key=user.openai_secret_key, 
                    conversation_mode=True,
                    experiment=experiment,
                )

                # Use the summary information of the question analyzer.
                is_successful, question_analyzer_summary = OpenAIAssistant.get_thread_summary(openai_secret_key=user.openai_secret_key, thread_id=(experiment.thread_id_list[0] if experiment.thread_id_list else experiment.current_thread_id))
                starting_message = current_assistant.pre_process(input_prompt=question_analyzer_summary)
                is_openai_key_valid, status_code, response_content = current_assistant.ask_gpt(prompt=starting_message)
                if (status_code == 200):
                    # _LOGGER.info("Message received after changing agent.")
                    response_content = current_assistant.post_process(response_content, experiment.summon_next_agent)
                    experiment.append_thread_id_list(current_assistant.thread.id)
                    experiment.append_chat_messages(role="assistant", text_value=response_content)  # Only the response from the assistant is recorded.
                configuration_updated, updated_attributes_from_response = experiment.parse_agent_response_content(response_content=response_content)
            response_info = ExperimentBehaviourResponseInfo(
                experiment, user,
                is_successful=True,
                completion_message=completion_message,
                message=f"{message} Received response from OpenAI.",
                response_content=response_content,
                require_pdb_file=experiment.summon_upload_pdb,
                confirm_button=experiment.summon_next_agent,
                configuration_updated=configuration_updated,
                updated_attributes=(updated_attrs+updated_attributes_from_response),
                configuration_stages=experiment.configuration_stages,
            )
            return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)
        else:
            response_info = ExperimentBehaviourResponseInfo(
                experiment, user,
                is_successful=False,
                message=message,
                require_pdb_file=experiment.summon_upload_pdb,
                confirm_button=experiment.summon_next_agent,
                configuration_stages=experiment.configuration_stages,
            )
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

        is_successful = experiment.clear_chat_threads(user.openai_secret_key)
        if (is_successful):
            response_info = ExperimentBehaviourResponseInfo(
                experiment, user,
                is_successful=is_successful,
                message="Your conversation is successfully cleared.",
                configuration_stages=experiment.configuration_stages,
            )
            return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)
        else:
            response_info = ExperimentBehaviourResponseInfo(
                experiment, user,
                is_successful=is_successful,
                message="Your conversation is unable to be cleared at present.",
                configuration_stages=experiment.configuration_stages
            )
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
        
        if (experiment.type == experiment.GROUP_TYPE):
            response_info = ExperimentBehaviourResponseInfo(
                experiment=experiment,
                user=user,
                message="Group experiment doesn't have Slurm job information.",
                is_authenticated=True,
                is_successful=False,
            )
            return Response(response=response_info.serialize(), status=404, mimetype=JSONIFY_MIMETYPE)

        
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
        
        if not experiment.has_pdb_file:
            return no_pdb_response()
        else:
            pass
        
        if (experiment.status in StatusCode.queued_status):
            response_info = ExperimentBehaviourResponseInfo(
                experiment=experiment,
                user=user,
                message="Slurm job is already submitted. You cannot submit another job unless you delete the current one.",
                is_authenticated=True,
                is_successful=False,
            )
            return Response(response=response_info.serialize(), status=409, mimetype=JSONIFY_MIMETYPE)
        else:   # When the existing slurm job is exited with error, delete the current one.
            is_successful, status, message = experiment.post_slurm_job()

        response_info = ExperimentBehaviourResponseInfo(
            experiment=experiment,
            user=user,
            message=message,
            is_authenticated=True,
            is_successful=is_successful,
            slurm_job_uuid=experiment.slurm_job_uuid if experiment.type != experiment.GROUP_TYPE else [exp.slurm_job_uuid for exp in experiment.subordinate_experiments]
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

        is_successful, status, message = experiment.delete_slurm_job()
        response_info = ExperimentBehaviourResponseInfo(
            experiment=experiment,
            user=user,
            message=message,
            is_authenticated=True,
            is_successful=is_successful,
        )
        return Response(response=response_info.serialize(), status=status, mimetype=JSONIFY_MIMETYPE)

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