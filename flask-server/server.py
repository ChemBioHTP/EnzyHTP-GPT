from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import openai
import prompt
import enzy_htp
from enzy_htp._interface import amber_interface
from new_enzy_htp.enzy_htp.core.clusters.accre import Accre
from new_enzy_htp.enzy_htp.geometry.sampling import equi_md_sampling
import enzy_htp.structure
import enzy_htp.mutation.api as mapi
import enzy_htp.mutation.mutation_pattern.api as pattern_api

import config
app = Flask(__name__)
app.config.from_object(config)

from context import db, login_manager
login_manager.login_message_category = "info"

# Import and define your routes and views
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

# Generate Patterns - done to show user what mutations they generated
@app.route("/api/generate_pattern", methods=["POST"])
def generate_pattern():
    mutation_request = request.json['mut_request']
    api_key = request.json['api_key']

    input_prompt = ""
    input_prompt += prompt.prompt_skeleton
    input_prompt += f"Query:{mutation_request}\nAnswer:"
    
    openai.api_key = api_key

    # TODO: how to improve prompt in config.py?
    try:
        completions = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=input_prompt,
            max_tokens=70,
            frequency_penalty=-0.5,
            temperature=0.01,
        )
        message = completions.choices[0].text
    except Exception as e:
        raise Exception(f'API Error: {str(e)}')

    #TODO: make this return the mutations generated and NOT the mutation pattern itself
    return jsonify({"mutations": message})

# Generates mutants with EnzyHTP and mutation pattern
def generate_muts(file, pattern):
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
        except Exception as e:
            raise Exception(f'API Error: {str(e)}')
        name_tag = ""
        for single_mut in mut:
            name_tag += str(single_mut) + "_"
        name_tag = name_tag[:-1]
        res.append((mutant_stru, name_tag))

    return res

# Runs MD simulation with EnzyHTP
def run_simulation(stru):
    is_prepare_only = request.json["prepare"]

    parallel_method_input = "cluster_job"
    if is_prepare_only:
        parallel_method_input = "prepare_only"

    stru.assign_ncaa_chargespin({"H5J" : (0,1)}) # TODO: What should go here?
    test_param_method = amber_interface.build_md_parameterizer(
        ncaa_param_lib_path="TODO" # TODO: What should go here?
    )
    cluster_job_config = {
        "cluster" : Accre(),
        "period" : 600,
        "res_setting" : {"account" : "csb_gpu_acc"}
    }
    return equi_md_sampling(stru = stru,
                     param_method = test_param_method,
                     parallel_method = parallel_method_input,
                     cluster_job_config = cluster_job_config,)

# Runs a complete workflow with EnzyHTP and pattern
    # First generates mutants based on file and pattern
    # Then runs MD simulation for each of the mutants
@app.route("/api/run_workflow", methods=["POST"])
def run_workflow():
    mutation_pattern = request.json["pattern"]
    file = request.json["file"]

    list_of_mut_strus = generate_muts(file, mutation_pattern)
    simulation_results = []

    for mut in list_of_mut_strus:
        simulation_results += run_simulation(mut)

    # Call mutant gen fn to get file/list of mutants,
    # then run each through simulation and return results
    return simulation_results

 
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