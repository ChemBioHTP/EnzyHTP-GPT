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
SECRET_KEY = os.environ.get("SECRET_KEY", "9131-0120-MA1H") # A custom value but mandatory.

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
DEFAULT_FILE_PATH = str()

# Uri
OAUTH_VENDOR_LOGIN_CALLBACK_REDIRECT_URI = os.environ.get("OAUTH_VENDOR_LOGIN_CALLBACK_REDIRECT_URI", "/api/auth/profile")
OPENAI_API_URI = "https://api.openai.com/v1/chat/completions"

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

# Vanderbilt ACCRE Slurm
ACCRE_SLURM_URL = "https://gateway-dev.mltf.k8s.accre.vanderbilt.edu/api/slurm/"
ACCRE_SLURM_AUTHORIZATION = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJuOUtsZ3V4VHdOc1o5VUFUVVlVcHVEb0wxa044V3Z3UVJDV3owUFptLUpRIn0.eyJleHAiOjE3MTgxNTI4ODUsImlhdCI6MTcxODE1MjU4NSwiYXV0aF90aW1lIjoxNzE4MTUxMDM3LCJqdGkiOiJmNjZhMDdkOC1kZTFlLTRjMjUtYjdkMy1mMjkxNjljMTA0NTQiLCJpc3MiOiJodHRwczovL2tleWNsb2FrLms4cy5hY2NyZS52YW5kZXJiaWx0LmVkdS9yZWFsbXMvcHVibGljIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6Ijk1NjNiNjQ3LWJkYWYtNDYxYy05YjdhLWE1MGRlNmRmYTc2YSIsInR5cCI6IkJlYXJlciIsImF6cCI6Im1sZmxvdyIsInNlc3Npb25fc3RhdGUiOiJkZGMxNDdhMi1mODM0LTQwYzMtOGM2Ny0zMGY2Yzk2NDhiZTgiLCJhY3IiOiIwIiwiYWxsb3dlZC1vcmlnaW5zIjpbIiIsImh0dHBzOi8vZ2F0ZXdheS1kZXYubWx0Zi5rOHMuYWNjcmUudmFuZGVyYmlsdC5lZHUqIiwiaHR0cHM6Ly9nYXRld2F5LWRldi5tbHRmLms4cy5hY2NyZS52YW5kZXJiaWx0LmVkdSIsImh0dHBzOi8vbWxmbG93LXRlc3QubWx0Zi5rOHMuYWNjcmUudmFuZGVyYmlsdC5lZHUqIiwiaHR0cHM6Ly9tbGZsb3ctdGVzdC5tbHRmLms4cy5hY2NyZS52YW5kZXJiaWx0LmVkdS8qIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsImRlZmF1bHQtcm9sZXMtcHVibGljIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwic2lkIjoiZGRjMTQ3YTItZjgzNC00MGMzLThjNjctMzBmNmM5NjQ4YmU4IiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJuYW1lIjoieWFuZ2xhYl9lbnp5aHRwX2FwcCIsInByZWZlcnJlZF91c2VybmFtZSI6InlhbmdsYWJfZW56eWh0cF9hcHAiLCJnaXZlbl9uYW1lIjoieWFuZ2xhYl9lbnp5aHRwX2FwcCJ9.RacCLTIyOX7XGF39CATwmM8He6Ji9qJHxEICrLRaYUmqBXZSl_SPur5mmXyhPFi_kQ5V6REFSC9wg7ZQcmNFYx78fe1eU6UDiNTn9gb2vpidvPmDDGG5-_HJN_Q-FQIVy3ti_r7pUWzVkMHNwlU04g5Gfjq-ZVwCH5mwcHGwTY9mWvyuF1Mbt1JPRRLThx71vpj9A4-Nz7STe6HDD-Rqw3KS3cJjEM15yk2Jh3oaxuSV73aqbiCxQeNEVriujxvtlQQI5iya1srvs9xGYI4BuZCLThzJ1anYoVsBJBSsT4gMWW6kvRgyEQSzJETWhBzkKnDIOTsEfRYqx127AQKvFQ"
SLURM_ACCOUNT = "yang_lab"
SLURM_PARTITION = "production"
SLURM_JOB_ENTRY_SCRIPT_FILENAME = "entry_script.sh"
SLURM_JOB_ENTRY_SCRIPT = open(os.path.join(__basedir, "templates", "slurm_run", SLURM_JOB_ENTRY_SCRIPT_FILENAME)).read()

# Run MD by Yourself.
SLURM_DEPLOY_SCRIPT_FILENAME = "perform_md_sim.sh"
SLURM_DEPLOY_SCRIPT = open(os.path.join(__basedir, "templates", "slurm_deploy", SLURM_DEPLOY_SCRIPT_FILENAME)).read()