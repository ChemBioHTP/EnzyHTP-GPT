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
ACCRE_SLURM_AUTHORIZATION = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJJaU1HWHVrWjlxY01WX25Yb1JreXpSeVQ1VEFMYkk3Yy1Pa1BsNjFwS1RVIn0.eyJleHAiOjE3MTcyMDkyOTMsImlhdCI6MTcxNjAwMDU4MywiYXV0aF90aW1lIjoxNzE1OTk5NjkzLCJqdGkiOiJjNWI1ZGJlMy03ZmMxLTQyZjEtOGU4OS1iNWQ0NmRhYWNmMTAiLCJpc3MiOiJodHRwczovL2tleWNsb2FrLms4cy5hY2NyZS52YW5kZXJiaWx0LmVkdS9yZWFsbXMvcHVibGljIiwiYXVkIjpbIm1sZmxvdyIsImFjY291bnQiXSwic3ViIjoiY2IzMDI3ZDktZDcwZC00NWQxLThjMDUtOTExYTliZTQwM2Y0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoibWxmbG93Iiwic2Vzc2lvbl9zdGF0ZSI6IjM0YzJiYTA5LWQ2ZjEtNDVkMC05OWZmLTY1ZjBjNzNlMjQ5MyIsImFjciI6IjAiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJkZWZhdWx0LXJvbGVzLXB1YmxpYyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgZW1haWwgZ3JvdXBzIHByb2ZpbGUiLCJzaWQiOiIzNGMyYmEwOS1kNmYxLTQ1ZDAtOTlmZi02NWYwYzczZTI0OTMiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJ6aG9uZ3k4IiwicHJlZmVycmVkX3VzZXJuYW1lIjoiemhvbmd5OCIsImdpdmVuX25hbWUiOiJ6aG9uZ3k4In0.Dr6wNr_KYcR3f62KsSkgeHGpb5738o5xnmyLl2Md7xZNhr6EwbfBvUDzu19UqsBXz3t5gN48e5S8fCgc_KwG9S9g65ptlLLMXVnVD9o-w4au2qISl9TyJeWVLSwgOD7QpsSHNs1jcPhslU2o-x7P2nR3W5nDNDzZrYlkwrbRd2Qwn8eFVFBVBtbZYtl7HxRGWj0U8X1__Nu5bfksVGAk-FxZpmRunvVSrdVdwFe2ahyKpCrw-r-o1LZKi9rNkvLaY6Bb_VLwBMPsRMx6O2PAdR99YOtaq5D2IC_HIzGYEIsyNxJg8hJbmRmzTPw2LWa0Bfij4ZPKlTQz_dFZcIHnJQ"
