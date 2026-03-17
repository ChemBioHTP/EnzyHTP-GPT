# Here put the import lib.
import os
import subprocess
from flask import Flask, jsonify, render_template

app = Flask(__name__)

from flask_restful import Api
api = Api(app=app)

import config
app.config.from_object(config)

from context import mongo, login_manager, jwt, mail, ssl_context, scheduler
login_manager.login_message_category = "info"  # Set login message category to info.

# Force antechamber to run in a writable cwd for temp files.
try:
    from enzy_htp.core import env_manager as eh_env_manager
except Exception:
    eh_env_manager = None

if eh_env_manager and not getattr(eh_env_manager, "_antechamber_cwd_patched", False):
    antechamber_cwd = os.environ.get("ENZYHTP_ANTECHAMBER_CWD", getattr(config, "TEMP_FOLDER", ""))
    if antechamber_cwd:
        os.makedirs(antechamber_cwd, exist_ok=True)
        eh_env_manager._antechamber_cwd_patched = True

        def _run_with_antechamber_cwd(cmd, *args, **kwargs):
            if isinstance(cmd, str) and "antechamber" in cmd:
                kwargs.setdefault("cwd", antechamber_cwd)
            return subprocess.run(cmd, *args, **kwargs)

        eh_env_manager.run = _run_with_antechamber_cwd

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

# Schedule token refresh task to run daily at 2:00 AM
from services.accre_slurm_service import SlurmJobRequest
@scheduler.task('cron', id='update_slurm_tokens', hour=2, minute=0)
def update_slurm_tokens_task():
    try:
        refreshed, status_code, message = SlurmJobRequest.refresh_slurm_token()
        app.logger.info(
            f"SLURM token refresh task executed. Success: {refreshed}, "
            f"Status: {status_code}, Message: {message}"
        )
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
