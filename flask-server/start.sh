#!/bin/bash

# Activate conda environment.
source activate enzyhtp-gpt

# Start the flask service using `uwsgi`.
uwsgi --ini uwsgi.ini
# uwsgi --ini uwsgi.ssl.ini
