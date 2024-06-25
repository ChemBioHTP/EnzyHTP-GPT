#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   config.py
@Created :   2023/10/29 21:44
@Author  :   Zhong, Yinjie
@Version :   1.0
@Contact :   yinjie.zhong@vanderbilt.edu
'''

# Here put the import lib.
import os

__basedir = os.getcwd()

# Configuration file.
DEVELOPMENT = "development"
ENV = os.environ.get("FLASK_ENV", DEVELOPMENT)
DEBUG = os.environ.get("DEBUG", True)
APP_HOST = os.environ.get("APP_HOST", "localhost")
SECRET_KEY = os.environ.get("SECRET_KEY", "91-310120-MA1H") # A custom value but mandatory.

# Enable Non-ASCII Characters.
JSON_AS_ASCII =False
JSONIFY_MIMETYPE = "application/json;charset=utf-8"

# Database.
SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(__basedir, 'instance', 'enzyhtp_gpt.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS=False

# MongoDB
MONGODB_DATABASE_URI='mongodb://localhost:27017/enzyhtp_gpt'
MONGODB_TRACK_MODIFICATIONS=False

# File system
FILE_SYSTEM_FOLDER = os.environ.get("FILE_SYSTEM_FOLDER", os.path.join(__basedir, "static"))
EXPERIMENT_FILE_DIRECTORY = os.path.join(FILE_SYSTEM_FOLDER, "experiments")
SCRATCH_FOLDER = os.path.join(FILE_SYSTEM_FOLDER, "scratch")

for folder in [FILE_SYSTEM_FOLDER, EXPERIMENT_FILE_DIRECTORY, SCRATCH_FOLDER]:
    if (not os.path.isdir(folder)):
        os.mkdir(folder)

# Uri
OAUTH_VENDOR_LOGIN_CALLBACK_REDIRECT_URI = os.environ.get("OAUTH_VENDOR_LOGIN_CALLBACK_REDIRECT_URI", "/api/auth/profile")

# Email for password reset.
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = "website.enzyhtp@gmail.com"
MAIL_DEFAULT_SENDER = ("EnzyHTP Web Application", "website.enzyhtp@gmail.com")
MAIL_PASSWORD = "ymyiwgzhxxpnlqcg"
# https://mailtrap.io/blog/python-send-email-gmail/

MAIL_PASSWORD_RESET_HTML_TEMPLATE = open(os.path.join(__basedir, "templates", "password_reset_email.html")).read()

