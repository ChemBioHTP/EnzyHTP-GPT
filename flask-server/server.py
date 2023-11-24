from flask import Flask, request, jsonify, render_template
import openai
import config
import enzy_htp.structure
import enzy_htp.mutation.api as mapi
import enzy_htp.mutation.mutation_pattern.api as pattern_api
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# import settings
# app = Flask(__name__)
# app.config.from_object(settings)

# from context import db, login_manager
# login_manager.login_message_category = "info"



# # Example API route - to start server, run "python server.py"
# # @app.route("/members")
# # def members():
# #     return {"members": ["Member1", "Member2"]}

# # Import and define your routes and views
# from auth import auth as auth_blueprint
# app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

# Generate Patterns
@app.route("/api/generate_pattern", methods=["POST"])
def generate_pattern():
    data = request.json
    mutation_request = data.get('mut_request')
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

    return jsonify({"mutations": message})

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
        name_tag = ""
        for single_mut in mut:
            name_tag += str(single_mut) + "_"
        name_tag = name_tag[:-1]
        res.append((res_file, name_tag))

    return res
 
@app.route("/")
def home():
    return render_template("../client/public/index.html")

@app.route("/api/key")
def api_key():
    return {'foo': 'bar'}

if __name__ == "__main__":
    # Create database tables
    # app.app_context().push()
    # db.init_app(app=app)
    # db.create_all()

    # # Initialize LoginManager.
    # login_manager.init_app(app)
    app.run(debug=True)