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
NCAA_LIB_PATH = os.path.join(EXPERIMENT_FILE_DIRECTORY, "ncaa_lib")
SCRATCH_FOLDER = os.path.join(FILE_SYSTEM_FOLDER, "scratch")
TEMP_FOLDER = os.path.join(FILE_SYSTEM_FOLDER, "temp")

for folder in [FILE_SYSTEM_FOLDER, EXPERIMENT_FILE_DIRECTORY, NCAA_LIB_PATH, SCRATCH_FOLDER, TEMP_FOLDER]:
    if (not os.path.isdir(folder)):
        os.mkdir(folder)

eh_config['system.SCRATCH_DIR'] = SCRATCH_FOLDER
eh_config['system.NCAA_LIB_PATH'] = NCAA_LIB_PATH
os.environ.setdefault("TMPDIR", TEMP_FOLDER)
eh_config['amber.DEFAULT_NCAA_PARAM_LIB_PATH'] = NCAA_LIB_PATH
eh_config['amber.DEFAULT_PARAMETERIZER_TEMP_DIR'] = SCRATCH_FOLDER

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
SLURM_ACCOUNT = "yang_lab"
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

DEFAULT_MD_LENGTH = 50.0  # MD Production Timespan in ns.
MANUAL_MD_DEPLOY_TIMEOUT = int(os.environ.get("MANUAL_MD_DEPLOY_TIMEOUT", "600"))

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
OPENAI_RUNTIME_CANDIDATES = {"assistants", "responses"}
OPENAI_RUNTIME = os.environ.get("OPENAI_RUNTIME", "assistants").strip().lower()
if (OPENAI_RUNTIME not in OPENAI_RUNTIME_CANDIDATES):
    OPENAI_RUNTIME = "assistants"

OPENAI_PROVIDER_CANDIDATES = {"openai", "fireworks"}
OPENAI_DEFAULT_PROVIDER = os.environ.get("OPENAI_DEFAULT_PROVIDER", "openai").strip().lower()
if (OPENAI_DEFAULT_PROVIDER not in OPENAI_PROVIDER_CANDIDATES):
    OPENAI_DEFAULT_PROVIDER = "openai"

OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "").strip()
_OPENAI_FIREWORKS_BASE_URL = os.environ.get("OPENAI_FIREWORKS_BASE_URL", "").strip()
OPENAI_FIREWORKS_BASE_URL = _OPENAI_FIREWORKS_BASE_URL or "https://api.fireworks.ai/inference/v1"
OPENAI_FIREWORKS_API_KEY = os.environ.get("OPENAI_FIREWORKS_API_KEY", "").strip()

_OPENAI_MODEL_VERSION = os.environ.get("OPENAI_MODEL_VERSION", "").strip()
OPENAI_MODEL_VERSION = _OPENAI_MODEL_VERSION or "gpt-4o-2024-11-20"
_OPENAI_FIREWORKS_MODEL_VERSION = os.environ.get("OPENAI_FIREWORKS_MODEL_VERSION", "").strip()
OPENAI_FIREWORKS_MODEL_VERSION = _OPENAI_FIREWORKS_MODEL_VERSION or "accounts/fireworks/models/kimi-k2p5"
OPENAI_PROVIDER_DEFAULT_MODELS = {
    "openai": OPENAI_MODEL_VERSION,
    "fireworks": OPENAI_FIREWORKS_MODEL_VERSION,
}

_OPENAI_KEY_VALIDATION_MODEL = os.environ.get("OPENAI_KEY_VALIDATION_MODEL", "").strip()
OPENAI_KEY_VALIDATION_MODEL = _OPENAI_KEY_VALIDATION_MODEL or OPENAI_MODEL_VERSION

_OPENAI_RESPONSES_STRICT_CONVERSATIONS = os.environ.get(
    "OPENAI_RESPONSES_STRICT_CONVERSATIONS",
    "false",
).strip().lower()
OPENAI_RESPONSES_STRICT_CONVERSATIONS = (
    _OPENAI_RESPONSES_STRICT_CONVERSATIONS in {"1", "true", "yes", "on"}
)

# Request-level assistant timeout controls (seconds).
# Default requests follow uWSGI harakiri (see uwsgi.ini), while Fireworks can be
# substantially slower and may require a larger per-request budget.
OPENAI_ASSISTANTS_REQUEST_TIMEOUT = int(os.environ.get("OPENAI_ASSISTANTS_REQUEST_TIMEOUT", "180"))
OPENAI_ASSISTANTS_FIREWORKS_REQUEST_TIMEOUT = int(
    os.environ.get("OPENAI_ASSISTANTS_FIREWORKS_REQUEST_TIMEOUT", "480")
)

# Placeholder Result Images
# PLHD_RESULT_IMG_DIR = os.path.join(BASEDIR, "templates", "result_images")
# PLHD_RESULT_IMG_PATHS = [
#     # os.path.join(PLHD_RESULT_IMG_DIR, "workflow.prep.png"),
#     # os.path.join(PLHD_RESULT_IMG_DIR, "workflow.sim.png"),
#     # os.path.join(PLHD_RESULT_IMG_DIR, "workflow.analysis.png"),
#     os.path.join(PLHD_RESULT_IMG_DIR, "dsi.png"),
# ]
# PLHD_RESULT_INTERPRETATION = """Hi, I've completed the computational simulations to ..."""
