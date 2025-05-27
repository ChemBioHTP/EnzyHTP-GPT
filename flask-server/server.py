# Here put the import lib.
from flask import Flask, jsonify, render_template

app = Flask(__name__)

from flask_restful import Api
api = Api(app=app)

import config
app.config.from_object(config)

from context import mongo, login_manager, jwt, mail, ssl_context, scheduler
login_manager.login_message_category = "info"  # Set login message category to info.

# Create MongoDB Connection.
mongo.init_app(app=app)

# Initialize Mail Engine.
mail.init_app(app)

# Initialize LoginManager.
login_manager.init_app(app=app)

# Initialize JWTManager
jwt.init_app(app=app)

# Import and define your routes and views
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix="/api/auth")
from experiment import experiment as experiment_blueprint
app.register_blueprint(experiment_blueprint, url_prefix="/api/experiment")

# Initialize APScheduler
scheduler.init_app(app)
scheduler.start()

# Schedule token update task to run daily at 2:00 AM
from services.accre_slurm_service import SlurmJobRequest
@scheduler.task('cron', id='update_slurm_tokens', hour=2, minute=0)
def update_slurm_tokens_task():
    try:
        updated, message = SlurmJobRequest.update_slurm_tokens()
        app.logger.info(f"SLURM token update task executed. Success: {updated}, Message: {message}")
    except Exception as e:
        app.logger.error(f"Failed to update SLURM tokens: {str(e)}")

@app.route("/api/index")
def home():
    # return render_template("index.html")
    return jsonify({"message": "This is the homepage of the backend. Welcome!"})

@app.route("/api/key")
def api_key():
    return jsonify({'foo': 'bar'})

if __name__ == "__main__":

    # Set SSL Context and run server. For development only.
    app.run(host="127.0.0.1",
        port=5000,
        debug=False,
        # ssl_context=ssl_context,
    )

# RESTful API referring https://www.geeksforgeeks.org/python-build-a-rest-api-using-flask/