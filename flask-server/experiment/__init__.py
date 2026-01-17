from flask import Blueprint
from flask_restful import Api
from . import views

experiment = Blueprint("experiment", __name__)
experiment_api = Api(app=experiment)

experiment_api.add_resource(views.IndexApi, "/")
experiment_api.add_resource(views.ExperimentApi, "/<experiment_id>")
experiment_api.add_resource(views.ResultApi, "/<experiment_id>/result")
experiment_api.add_resource(views.AssistantsApi, "/<experiment_id>/assistants")
experiment_api.add_resource(views.DownloadableApi, "/<experiment_id>/downloadable")
experiment_api.add_resource(views.DownloadableFileApi, "/<experiment_id>/downloadable/<filepath>")
experiment_api.add_resource(views.PdbFilesApi, "/<experiment_id>/pdb_files")
experiment_api.add_resource(views.PdbFileApi, "/<experiment_id>/pdb_file")
experiment_api.add_resource(views.MutationApi, "/<experiment_id>/mutations")
experiment_api.add_resource(views.SlurmCorrespondenceApi, "/<experiment_id>/slurm")
experiment_api.add_resource(views.SlurmTokenApi, "/slurm/token")
experiment_api.add_resource(views.SlurmDeployApi, "/<experiment_id>/deploy")
