import os
from flask import Flask, request, jsonify, render_template
import openai
import config
import enzy_htp.structure
import enzy_htp.mutation.api as mapi
import enzy_htp.mutation.mutation as mt
import enzy_htp.mutation.mutation_pattern.api as pattern_api
from enzy_htp.preparation import validity as vd
from flask import Flask
from enzy_htp.core import general as eg
from enzy_htp.core import _LOGGER

app = Flask(__name__)

# TODO: Update method for getting files - global variable for now, integrate into database
app.config['UPLOAD_FOLDER'] = 'uploads'
file_path = ""

import settings
app = Flask(__name__, template_folder='../public')
app.config.from_object(settings)

from context import db, login_manager, ssl_context
login_manager.login_message_category = "info"

# Create database tables
app.app_context().push()
db.init_app(app=app)
db.create_all()

# Initialize LoginManager.
login_manager.init_app(app)

# Example API route - to start server, run "python server.py"
# @app.route("/members")
# def members():
#     return {"members": ["Member1", "Member2"]}

# Import and define your routes and views
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

# Validate File
@app.route("/api/validate_file", methods=["POST"])
def validate_file():
    global file_path
    result = None
    message = """"""
    is_valid = None
    with eg.CaptureLogging(_LOGGER) as log_str:
        try:
            file = request.files['file']

            if file.filename == '':
                return 'No selected file'
            
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

            if file:
                file.save(file_path)

            sp = enzy_htp.structure.PDBParser()
            stru = sp.get_structure(file_path)
            result = vd.is_structure_valid(stru, print_report=True)
            is_valid = result[0]
            intermediate_message = result[1]
            message += "The following errors were found in the PDB file: \n"
            for reason, source, suggestion in intermediate_message:
                message += "Reason: " + str(reason) + " Source: " + str(source) + " Suggestion: " + str(suggestion) + "\n"
            if not is_valid:
                os.remove(file_path)
        except:
            is_valid = False
            message = log_str.getvalue()
            os.remove(file_path)

    return jsonify({"validity": is_valid, "message": message})

# Generate Patterns
@app.route("/api/generate_pattern", methods=["POST"])
def generate_pattern():
    global file_path
    data = request.json
    mutation_request = data.get('mut_request')
    api_key = data.get('api_key')

    prompt = ""
    prompt += config.prompt_skeleton
    prompt += f"Query:{mutation_request}\nAnswer:"
    
    openai.api_key = api_key

    # TODO: how to improve prompt in config.py?
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
            res_file = sp.get_file_str(mutant_stru)
        except Exception as e:
            raise Exception(f'API Error: {str(e)}')
    name_tag = mt.get_mutant_name_tag(mutations)
    res.append((res_file, name_tag))

    return res
 
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/key")
def api_key():
    return {'foo': 'bar'}

if __name__ == "__main__":

    # Set SSL Context and run server.
    app.run(host=settings.APP_HOST,
        port=5000,
        debug=True,
        ssl_context=ssl_context)
