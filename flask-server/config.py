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
from datetime import timedelta

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

# Vanderbilt ACCRE Slurm
ACCRE_SLURM_URL = "https://gateway-dev.mltf.k8s.accre.vanderbilt.edu/api/slurm"
ACCRE_SLURM_AUTHORIZATION = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJuOUtsZ3V4VHdOc1o5VUFUVVlVcHVEb0wxa044V3Z3UVJDV3owUFptLUpRIn0.eyJleHAiOjE3MjE1MTQxODYsImlhdCI6MTcyMDMwNDYyNiwiYXV0aF90aW1lIjoxNzIwMzA0NTg2LCJqdGkiOiJmZTc1M2RmMi1lMjIzLTQxMGUtODg0MS0xOTMyMDI0MTJlMTAiLCJpc3MiOiJodHRwczovL2tleWNsb2FrLms4cy5hY2NyZS52YW5kZXJiaWx0LmVkdS9yZWFsbXMvcHVibGljIiwiYXVkIjpbIm1sZmxvdyIsImFjY291bnQiXSwic3ViIjoiOTU2M2I2NDctYmRhZi00NjFjLTliN2EtYTUwZGU2ZGZhNzZhIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoibWxmbG93Iiwic2Vzc2lvbl9zdGF0ZSI6ImJjNGIzMjM1LWZlYTMtNGU4Mi1hZDUxLTI3ZDc2NTU1ODdiZiIsImFjciI6IjAiLCJhbGxvd2VkLW9yaWdpbnMiOlsiIiwiaHR0cHM6Ly9nYXRld2F5LWRldi5tbHRmLms4cy5hY2NyZS52YW5kZXJiaWx0LmVkdSoiLCJodHRwczovL2dhdGV3YXktZGV2Lm1sdGYuazhzLmFjY3JlLnZhbmRlcmJpbHQuZWR1IiwiaHR0cHM6Ly9tbGZsb3ctdGVzdC5tbHRmLms4cy5hY2NyZS52YW5kZXJiaWx0LmVkdSoiLCJodHRwczovL21sZmxvdy10ZXN0Lm1sdGYuazhzLmFjY3JlLnZhbmRlcmJpbHQuZWR1LyoiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwiZGVmYXVsdC1yb2xlcy1wdWJsaWMiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJzaWQiOiJiYzRiMzIzNS1mZWEzLTRlODItYWQ1MS0yN2Q3NjU1NTg3YmYiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJ5YW5nbGFiX2VuenlodHBfYXBwIiwicHJlZmVycmVkX3VzZXJuYW1lIjoieWFuZ2xhYl9lbnp5aHRwX2FwcCIsImdpdmVuX25hbWUiOiJ5YW5nbGFiX2VuenlodHBfYXBwIn0.et3uNeyno4PMCudurZ7EUIywwElD3_f__P4NYmArKYA2PcTCF0hUxdH8jZCcq8OP8KGXQ-SOWu1CEmosOiuGsQOIOYqBbRcUS2CNJzf0xvm7zn3guMqtXRwCkMBberSDWJyjXMPD6trZnM2eh4wdsifDX1A5sfWpYLwa7LQrzgH4sqTc8hg_eE41obbINENyhUgy3aZOR54KbuoetgWJ8WZHsSDijgZiMRT_9rZtuWLyj0VMLA_E_XhG825xO32M7wJG8CsWekTZZHpT6nJ50aVQ1j6GHmp-4N77915M9nTA-Z3XaNUlqmafm_LAHGUXL1CY0Bi2IwJxgwpc0D8MRg"
SLURM_ACCOUNT = "yang_lab"
SLURM_PARTITION = "production"
SLURM_JOB_ENTRY_SCRIPT_FILENAME = "entry_script.sh"
SLURM_JOB_MAIN_SCRIPT_FILENAME = "main_script.py"
SLURM_JOB_ENTRY_SCRIPT = open(os.path.join(__basedir, "templates", "slurm_run", SLURM_JOB_ENTRY_SCRIPT_FILENAME)).read()
SLURM_JOB_MAIN_SCRIPT_FILEPATH = os.path.join(__basedir, "templates", "slurm_run", SLURM_JOB_MAIN_SCRIPT_FILENAME)
MAX_MUTANT_COUNT = 6

# Run MD by Yourself.
SLURM_DEPLOY_SCRIPT_FILENAME = "perform_md_sim.sh"
SLURM_DEPLOY_SCRIPT = open(os.path.join(__basedir, "templates", "slurm_deploy", SLURM_DEPLOY_SCRIPT_FILENAME)).read()

# Mutation Column Name.
WORKSHEET_MUTATION_COLUMN_NAME = "clean_mut_wt"

# JSON Web Token.
JWT_SECRET_KEY = SECRET_KEY
TOKEN_EXPIRES_DELTA = timedelta(days=5)
