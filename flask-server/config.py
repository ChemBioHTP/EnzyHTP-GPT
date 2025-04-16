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
from datetime import timedelta, timezone
from enzy_htp import config as eh_config

BASEDIR = os.getcwd()

# Configuration file.
DEVELOPMENT = "development"
# TIME_ZONE = timezone(os.environ.get("TIME_ZONE", "US/Central"))
ENV = os.environ.get("FLASK_ENV", DEVELOPMENT)
DEBUG = os.environ.get("DEBUG", True)
APP_HOST = os.environ.get("APP_HOST", "localhost")
SECRET_KEY = os.environ.get("SECRET_KEY", "91-310120-MA1H") # A custom value but mandatory.
MAX_CONTENT_LENGTH = 2 * 1000**3

# Enable Non-ASCII Characters.
JSON_AS_ASCII = False
JSONIFY_MIMETYPE = "application/json;charset=utf-8"

# Database.
# SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(__basedir, 'instance', 'enzyhtp_gpt.db')}"
# SQLALCHEMY_TRACK_MODIFICATIONS=False

# MongoDB
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/enzyhtp_gpt")

# File system
FILE_SYSTEM_FOLDER = os.environ.get("FILE_SYSTEM_FOLDER", os.path.join(BASEDIR, "static"))
EXPERIMENT_FILE_DIRECTORY = os.path.join(FILE_SYSTEM_FOLDER, "experiments")
SCRATCH_FOLDER = os.path.join(FILE_SYSTEM_FOLDER, "scratch")

for folder in [FILE_SYSTEM_FOLDER, EXPERIMENT_FILE_DIRECTORY, SCRATCH_FOLDER]:
    if (not os.path.isdir(folder)):
        os.mkdir(folder)

eh_config['system.SCRATCH_DIR'] = SCRATCH_FOLDER

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

MAIL_PASSWORD_RESET_HTML_TEMPLATE = open(os.path.join(BASEDIR, "templates", "password_reset_email.html")).read()

# Vanderbilt ACCRE Slurm
SLURM_HOST = "https://ssam.accre.vanderbilt.edu"
SLURM_API_URL = f"{SLURM_HOST}/api/slurm"
SLURM_USER = "yanglab_enzyhtp_app"
SLURM_ACCOUNT = "yang_lab_csb"
SLURM_PARTITION = "batch"

SLURM_MD_JOB_ENTRY_SCRIPT = "md_entry_script.sh"
SLURM_MD_JOB_ENTRY_SCRIPT_CONTENT = open(os.path.join(BASEDIR, "templates", "slurm_run", SLURM_MD_JOB_ENTRY_SCRIPT)).read()
SLURM_MD_JOB_MAIN_SCRIPT = "md_main_script.py"
SLURM_MD_JOB_MAIN_SCRIPT_FILEPATH = os.path.join(BASEDIR, "templates", "slurm_run", SLURM_MD_JOB_MAIN_SCRIPT)

SLURM_ANALYSIS_JOB_ENTRY_SCRIPT = "analysis_entry_script.sh"
SLURM_ANALYSIS_JOB_ENTRY_CONTENT = open(os.path.join(BASEDIR, "templates", "slurm_run", SLURM_ANALYSIS_JOB_ENTRY_SCRIPT)).read()
SLURM_ANALYSIS_JOB_MAIN_SCRIPT = "analysis_main_script.py"
SLURM_ANALYSIS_JOB_MAIN_SCRIPT_FILEPATH = os.path.join(BASEDIR, "templates", "slurm_run", SLURM_ANALYSIS_JOB_MAIN_SCRIPT)

MAX_MUTANT_COUNT = 6

# Run MD by Yourself.
SLURM_DEPLOY_SCRIPT_FILENAME = "perform_md_sim.sh"
SLURM_DEPLOY_SCRIPT = open(os.path.join(BASEDIR, "templates", "slurm_deploy", SLURM_DEPLOY_SCRIPT_FILENAME)).read()

# Mutation Column Name.
WORKSHEET_MUTATION_COLUMN_NAME = "clean_mut_wt"

# JSON Web Token.
JWT_SECRET_KEY = SECRET_KEY
TOKEN_EXPIRES_DELTA = timedelta(days=5)

# OpenAI Service
DEFAULT_OPENAI_API_KEY = "5111321231135666"

# Placeholder Result Images
PLHD_RESULT_IMG_DIR = os.path.join(BASEDIR, "templates", "result_images")
PLHD_RESULT_IMG_PATHS = [
    os.path.join(PLHD_RESULT_IMG_DIR, "workflow.prep.png"),
    os.path.join(PLHD_RESULT_IMG_DIR, "workflow.sim.png"),
    os.path.join(PLHD_RESULT_IMG_DIR, "workflow.analysis.png"),
]
PLHD_RESULT_INTERPRETATION = """Based on the simulation data for SARS-CoV-2 main protease (Mpro) in complex with nirmatrelvir, the EA166I mutant exhibits markedly enhanced binding affinity compared to the wild-type (WT), as indicated by a significantly more negative average MM/PBGBSA value (−12.3 kcal/mol vs. −1.96 kcal/mol). Although the EA166I mutant shows slightly higher active site RMSD and lower SPI values, suggesting minor structural perturbations and reduced active site packing, these changes appear to facilitate stronger ligand interactions. This finding implies that the EA166I substitution may confer increased inhibitor binding strength, potentially impacting resistance mechanisms or drug efficacy."""
