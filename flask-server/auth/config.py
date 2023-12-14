#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   config.py
@Created :   2023/12/07 02:39
@Author  :   Zhong, Yinjie
@Version :   1.0
@Contact :   yinjie.zhong@vanderbilt.edu
'''

# Here put the import lib.
from oauthlib.oauth2 import WebApplicationClient
from requests import get
import os

__basedir = os.path.join(os.getcwd())

# Configuration
from json import load

CLIENT_ID = dict()
CLIENT_SECRET = dict()
DISCOVERY_URL = dict()

__google_login_client = load(open(
    os.path.join(__basedir, 'oauth_clients/google_login_client.json')
    ))
CLIENT_ID['GOOGLE'] = __google_login_client.get('web', None).get("client_id", None)
CLIENT_SECRET['GOOGLE'] = __google_login_client.get('web', None).get("client_secret", None)
DISCOVERY_URL['GOOGLE'] = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# OAuth Client.
oauth_client_dict = dict()
provider_cfg_dict = dict()

def get_google_provider_cfg() -> str:
    get_response = get(DISCOVERY_URL['GOOGLE'])
    if get_response.status_code == 200:
        google_provider_cfg = get_response.json()
    else:
        google_provider_cfg = '\{\}'
    return google_provider_cfg

oauth_client_dict['GOOGLE'] = WebApplicationClient(CLIENT_ID['GOOGLE'])

provider_cfg_dict['GOOGLE'] = get_google_provider_cfg()
# google_provider_cfg = get_google_provider_cfg()

# Reference: https://realpython.com/flask-google-login/