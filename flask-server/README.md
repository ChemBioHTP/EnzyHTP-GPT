# Flask-server

[TOC]

## 1. Introduction

The backend of EnzyHTP Web Application.

## 2. Configuration

The `settings.py` and `context.py` files in the `/flask-server` directory are to support database and user authentication.

### 2.1 Settings

- Filepath: `/flask-server/settings.py`

This file is cited as an object to inject the runtime configurations of the flask server so as to protect the main file `/flask-server/server.py` from getting 'contaminated'.

### 2.2 Context

- Filepath: `/flask-server/context.py`

This file is to declare the `SQLAlchemy` database instance (named `db`) and the `LoginManager` instance (named `login_manager`) for the whole flask server.

Those instances can only be declared in an individual file and imported into the main file and anywhere else in the server. Otherwise, a number of "Exception(s)", and a "Warning" prompt which will be set to "Exception" in the next version, will be triggered.