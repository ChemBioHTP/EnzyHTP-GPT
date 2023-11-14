#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   settings.py
@Created :   2023/10/29 21:44
@Author  :   Zhong, Yinjie
@Version :   1.0
@Contact :   yinjie.zhong@vanderbilt.edu
'''

# Here put the import lib.


# Configuration file.
import os

__basedir=os.getcwd()

ENV='development'
DEBUG='True'

SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(__basedir, "instance", "enzyhtp_gpt.db")}'
SQLALCHEMY_TRACK_MODIFICATIONS=False
SECRET_KEY='9131-0120-MA1H' # A custom value but mandatory.