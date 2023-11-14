from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import openai
import config
import enzy_htp
from enzy_htp._interface import amber_interface
from new_enzy_htp.enzy_htp.core.clusters.accre import Accre
from new_enzy_htp.enzy_htp.geometry.sampling import equi_md_sampling

import settings
app = Flask(__name__)
app.config.from_object(settings)

from context import db, login_manager
login_manager.login_message_category = "info"



# Example API route - to start server, run "python server.py"
# @app.route("/members")
# def members():
#     return {"members": ["Member1", "Member2"]}

# Import and define your routes and views
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

# Generate Patterns - done to show user what mutations they generated
@app.route("/api/generate_pattern", methods=["POST"])
def generate_pattern():
    mutation_request = request.json['mut_request']
    api_key = request.json['api_key']

    prompt = ""
    prompt += config.prompt_skeleton
    prompt += f"Query:{mutation_request}\nAnswer:"
    
    openai.api_key = api_key

    # TODO: how to improve prompt in config.py?
    try:
        completions = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=70,
            frequency_penalty=-0.5,
            temperature=0.01,
        )
        message = completions.choices[0].text
    except Exception as e:
        raise Exception(f'API Error: {str(e)}')

    #TODO: pass this response into EnzyHTP for further processing rather than returning it
    return jsonify({"mutations": message})

@app.route("/api/run_workflow", methods=["POST"])
def run_workflow():
    pass

@app.route("/api/run_md", methods=["POST"])
def run_simulation():
    mutant_file = request.json["file"]
    is_prepare_only = request.json["prepare"]

    parallel_method_input = "cluster_job"
    if is_prepare_only:
        parallel_method_input = "prepare_only"

    sp = enzy_htp.PDBParser()
    test_stru = sp.get_structure(mutant_file.name)
    test_stru.assign_ncaa_chargespin({"H5J" : (0,1)}) # TODO: What should go here?
    test_param_method = amber_interface.build_md_parameterizer(
        ncaa_param_lib_path="TODO" # TODO: What should go here?
    )
    cluster_job_config = {
        "cluster" : Accre(),
        "period" : 600,
        "res_setting" : {"account" : "csb_gpu_acc"}
    }
    return equi_md_sampling(stru = test_stru,
                     param_method = test_param_method,
                     parallel_method = parallel_method_input,
                     cluster_job_config = cluster_job_config,)

@app.route("/")
def home():
    return render_template("../client/public/index.html")

@app.route("/key")
def api_key():
    return {'foo': 'bar'}

if __name__ == "__main__":
    # Create database tables
    app.app_context().push()
    db.init_app(app=app)
    db.create_all()

    # Initialize LoginManager.
    login_manager.init_app(app)
    app.run(debug=True)