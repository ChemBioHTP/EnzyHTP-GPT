# EnzyHTP-GPT

A web application that serves as an interface between a user and EnzyHTP's workflows.

[TOC]

# 1. Developers: First Time Install

## 1.1 Environment Configuration.

* First, clone this repository onto your local machine.
  * Use git command `git clone https://github.com/ChemBioHTP/EnzyHTP-GPT.git`

* We will then need to create a conda environment to run the website.
  * There is an existing `environment.yml` file for you to make new anaconda environment.
    * `conda env create -f environment.yml`
  * You can also build the environment manually.
    * Create a new conda environment `conda create -n enzyhtp-gpt`. The name following `-n` flag could be anything you like.
    * Install Flask using the command `conda install -c anaconda flask flask-login flask-sqlalchemy`.
  * This is the only package we have to install as of now, but when we integrate EnzyHTP, we will need to install many more.

* We also need to install `npm`.
  * Taking Ubuntu (or WSL Ubuntu) for instance, install `npm` using command `sudo apt-get install npm`.

## 1.2 Launch.

* To run the website, open two terminals on VSCode.
  * On one, `cd` into the `flask-server` folder and run `python server.py` to start the backend.
  * On the other, run `npm start` in the `client` folder.
    * If you are faced with `sh: 1: react-scripts: Permission denied` error, use `sudo npm start`.
    * If you are faced with `sh: 1: react-scripts: not found` error:
      * Use `npm install react-scripts`.

* That's it! The website should begin running on `localhost:3000`.
  * If you use WSL or virtual machine, the address should be `<ip.to.your.vm>:3000`.

# 2. Configuration

The `settings.py` and `context.py` files in the `/flask-server` directory are to support database and user authentication.

## 2.1 Settings

- Filepath: `/flask-server/settings.py`

This file is cited as an object to inject the runtime configurations of the flask server so as to protect the main file `/flask-server/server.py` from getting 'contaminated'.

## 2.2 Context

- Filepath: `/flask-server/context.py`

This file is to declare the `SQLAlchemy` database instance (named `db`) and the `LoginManager` instance (named `login_manager`) for the whole flask server.

Those instances can only be declared in an individual file and imported into the main file and anywhere else in the server. Otherwise, a number of "Exception(s)", and a "Warning" prompt which will be set to "Exception" in the next version, will be triggered.