#!/bin/bash

# Activate conda environment.
source activate enzyhtp-gpt
export PYTHONPATH=$PYTHONPATH:/var/bin/EnzyHTP

export TIME_ZONE="US/Central"
export FLASK_ENV="production"
export DEBUG=0
export APP_HOST="enzyhtp.app.vanderbilt.edu"
export SECRET_KEY="48c0e116-f078-4fa4-a290-0cffe8e3945c"

export MONGO_URI="mongodb://10.2.192.25:27017/enzyhtp_gpt"
export FILE_SYSTEM_FOLDER="/var/www/files"
export TMPDIR="${FILE_SYSTEM_FOLDER}/temp"
export OAUTH_VENDOR_LOGIN_CALLBACK_REDIRECT_URI="/#/"
export AMBERHOME="/sb/apps/amber22"

export PATH=$PATH:$AMBERHOME/bin

# Start the flask service using `uwsgi`.
uwsgi --ini uwsgi.ini
# uwsgi --ini uwsgi.ssl.ini
