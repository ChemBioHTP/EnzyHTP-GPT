#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   context.py
@Created :   2023/10/29 20:32
@Author  :   Zhong, Yinjie
@Version :   1.0
@Contact :   yinjie.zhong@vanderbilt.edu

This file is composed in order to deal with:
(1) KeyError: <weakref at ...; to 'Flask' at ...>
Reference: https://learnku.com/articles/74208

(2) Exception: Missing user_loader or request_loader. Refer to http://flask-login.readthedocs.io/#how-it-works for more info.


(3) /path/to/EnzyHTP-GPT/flask-server/auth/views.py:28: UserWarning: The setup method 'route' can no longer be called on the blueprint 'auth'. It has already been registered at least once, any changes will not be applied consistently.
Make sure all imports, decorators, functions, etc. needed to set up the blueprint are done before registering it.
This warning will become an exception in Flask 2.3.
  @auth.route('/register', methods=['POST'])

'''

# Here put the import lib.
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_login import LoginManager
login_manager = LoginManager()
