from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

if __name__ == "__main__":
    # Create database tables
    app.app_context().push()
    db.init_app(app=app)
    db.create_all()

    # Initialize LoginManager.
    login_manager.init_app(app)
    app.run(debug=True)