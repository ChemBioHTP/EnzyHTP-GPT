#! python3
# -*- encoding: utf-8 -*-
'''
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
session.add(User(email='san.zhang@example.com', password='123456'))
session.add(User(email='tom.white@example.com', password='123456'))
session.add(User(email='lisa.green@example.com', password='123456'))
session.commit()

session.close()
