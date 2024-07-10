#! python3
# -*- encoding: utf-8 -*-
'''
This script is only for development use when the database is SQLite.
After the database is migrated to MongoDB on 2024-07-10, this script is deprecated.

@File    :   init_db.py
@Created :   2023/12/13 22:17
@Author  :   Zhong, Yinjie
@Version :   1.0
@Contact :   yinjie.zhong@vanderbilt.edu
'''

# Here put the import lib.
import sqlite3
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define the SQLite database file
db_file = "enzyhtp_gpt.db"

# Create an SQLite engine
engine = create_engine(f"sqlite:///instance/{db_file}", echo=True)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Add users.
from auth.models import User
user_zhang = User(email='san.zhang@example.com', password_plaintext='123456')
session.add(user_zhang)
user_white = User(email='tom.white@example.com', password_plaintext='123456')
session.add(user_white)
session.add(User(email='lisa.green@example.com', password_plaintext='123456'))
# session.commit()

from experiment.models import Experiment
session.add(Experiment(user_id=user_zhang.id, name="exp-test-01", description="Let's start a test."))
session.add(Experiment(user_id=user_zhang.id, name="exp-test-02", description="Let's start a test."))
session.add(Experiment(user_id=user_white.id, name="exp-test-11", description="Let's start a test."))
session.add(Experiment(user_id=user_white.id, name="exp-test-12", description="Let's start a test."))
session.add(Experiment(user_id=user_white.id, name="exp-test-13", description="Let's start a test."))
session.add(Experiment(user_id=user_white.id, name="exp-test-14", description="Let's start a test."))

# print(type(user_zhang.id))

session.commit()
session.close()
