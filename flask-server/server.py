# Here put the import lib.
from flask import Flask, jsonify, render_template

app = Flask(__name__)

import config
app.config.from_object(config)

# Create MongoDB Connection.
from context import mongo
mongo.init_app(app=app)

from context import login_manager, jwt, mail, ssl_context
login_manager.login_message_category = "info"

# Import and define your routes and views
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix="/api/auth")
from experiment import experiment as experiment_blueprint
app.register_blueprint(experiment_blueprint, url_prefix="/api/experiment")

# Initialize Mail Engine.
mail.init_app(app)

# Create database tables
# from context import db
# app.app_context().push()
# db.init_app(app=app)
# db.create_all()

# Initialize LoginManager.
login_manager.init_app(app=app)

# Initialize JWTManager
jwt.init_app(app=app)
 
@app.route("/api/index")
def home():
    # return render_template("index.html")
    return jsonify({"message": "This is the homepage of the backend. Welcome!"})

@app.route("/api/key")
def api_key():
    return jsonify({'foo': 'bar'})

if __name__ == "__main__":

    # Set SSL Context and run server. For development only.
    app.run(host=config.APP_HOST,
        port=5000,
        debug=True,
        ssl_context=ssl_context)
