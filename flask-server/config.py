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
    # os.path.join(PLHD_RESULT_IMG_DIR, "workflow.prep.png"),
    # os.path.join(PLHD_RESULT_IMG_DIR, "workflow.sim.png"),
    # os.path.join(PLHD_RESULT_IMG_DIR, "workflow.analysis.png"),
    os.path.join(PLHD_RESULT_IMG_DIR, "dsi.png"),
]
PLHD_RESULT_INTERPRETATION = """Hi,

I've completed the computational simulations to evaluate the effect of different linkers on cold-adaptation of your bidomain enzyme, specifically by calculating the Domain Separation Index (DSI), as defined in our reference study (DOI: 10.26434/chemrxiv-2024-rstbz).
The Domain Separation Index (DSI) quantitatively measures the spatial separation between the two domains of a bi-domain enzyme. Previous experimental and computational studies have demonstrated that higher DSI values strongly correlate with improved cold-adaptation and increased enzyme activity under cold conditions, as greater domain separation facilitates substrate recruitment and dynamic flexibility crucial for catalysis at low temperatures. (DOI: 10.26434/chemrxiv-2024-rstbz)
Here are the summarized results:

* Original linker (GSGDGGGNDGGEGGL):
  - DSI = 2.11 Å
  - Suggests domains remain closely associated, minimal separation observed.
* Linker LNRLDRL:
  - DSI = 24.85 Å
  - Significantly increased domain separation, potentially enabling greater domain seperation at lower temperatures, which strongly supports enhanced cold-adaptation.
* Linker AKLKQKTEQLQDRIAG:
  - DSI = 16.56 Å
  - Moderate increase in domain separation, indicating enhanced cold-adaption compared to the original linker but less pronounced than LNRLDRL.
* Linker DYGNSPLHRFKKPGSKNFQNIFPPSAT:
  - DSI = 4.23 Å
  - Slight increase in domain separation over the original linker, suggesting minor improvement in cold-adaption.
* Linker GTLSP:
  - DSI = 0.44 Å
  - Slight decrease in domain separation over the original linker, suggesting minor decrease in cold-adaption
* Based on these findings, the linker LNRLDRL shows the most pronounced domain separation, strongly indicating the highest potential for improved cold-adaptation. The linker AKLKQKTEQLQDRIAG also presents moderate beneficial effects.

I recommend experimentally test the activity of these enzyme variants at both 0°C and 45°C and compare the result with the DSI value.
You can also examine the provided simulation trajectories to further understand the structural dynamics underlying these DSI differences. Observing structural details, such as domain interactions and the flexibility of critical functional loops, will help elucidate how these structural variations directly impact the enzyme's cold-adaptive behavior."""
