#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   config.production.py
@Created :   2024/04/13 15:04
@Author  :   Zhong, Yinjie
@Version :   1.0
@Contact :   yinjie.zhong@vanderbilt.edu
'''

# Here put the import lib.
import os


# Configuration file.

ENV = "production"
DEBUG = False

# File system
FILE_SYSTEM_FOLDER = os.path.join("/home/zhongy8/data/flask", "static")
EXPERIMENT_FILE_DIRECTORY = os.path.join(FILE_SYSTEM_FOLDER, "experiments")

APP_HOST = "enzyhtp.app.vanderbilt.edu"

