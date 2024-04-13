#!/bin/bash

# Activate conda environment.
source activate enzyhtp-gpt

export ENV="production"
export DEBUG=false
export APP_HOST="enzyhtp.app.vanderbilt.edu"
export SECRET_KEY=$(cat /proc/sys/kernel/random/uuid)

export FILE_SYSTEM_FOLDER="/var/www/files"
export OAUTH_VENDOR_LOGIN_CALLBACK_REDIRECT_URI="/key"

# Start the flask service using `uwsgi`.
uwsgi --ini uwsgi.ini
# uwsgi --ini uwsgi.ssl.ini
