from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import openai
import config

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

# Generate Patterns
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


if __name__ == "__main__":
    # Create database tables
    app.app_context().push()
    db.init_app(app=app)
    db.create_all()

    # Initialize LoginManager.
    login_manager.init_app(app)
    app.run(debug=True)