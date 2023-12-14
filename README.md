# EnzyHTP-GPT

A web application that serves as an interface between a user and EnzyHTP's workflows.

[TOC]

# 1. Developers: First Time Install

## 1.1 Environment Configuration.

* First, clone this repository onto your local machine.
  * Use git command `git clone https://github.com/ChemBioHTP/EnzyHTP-GPT.git`

* We will then need to create a conda environment to run the website.
  * There is an existing `environment.yml` file for you to make new anaconda environment automatically.
    * `conda env create -f environment.yml`. This command can be followed by `-n` or `--name` option to specify the environment name.
  * If you want to install the environment without EnzyHTP, you can make use of the `environment_no_enzyhtp.yml` file. **(Don't do it at present since it's lack of some essential packages.)**
    * Run `conda env create -f environment_no_enzyhtp.yml`. This command can also be followed by `-n` or `--name` option to specify the environment name.

* We will also install EnzyHTP (by cloning it onto your local machine for now).
  * To do this, run `git clone https://github.com/ChemBioHTP/EnzyHTP.git <path/to/save>` Here, we take `~/bin/EnzyHTP` as an example, i.e., run `git clone https://github.com/ChemBioHTP/EnzyHTP.git ~/bin/EnzyHTP`
  * Then, run `cd ~/bin/EnzyHTP` and `git checkout develop_refactor` to switch to the **refactored EnzyHTP**.
  * Thirdly, follow the instructions in the `enzyhtp_env_config.sh` script to adjust and run it. `bash enzyhtp_env_config.sh`
  * You should now be able to use EnzyHTP with the site.

* You may faced with the error when running the `flask-server/server.py` as follows due to the bad update of `sqlalchemy`.
  
  > AttributeError: module 'sqlalchemy' has no attribute '\_\_all\_\_'
  
  * If so, run `conda install sqlalchemy=1.4.39=py39h5eee18b_0 --yes` in your `enzyhtp-gpt` conda environment.

* We also need to install `npm`.
  * Taking Ubuntu (or WSL Ubuntu) for instance, install `npm` using command `sudo apt-get install npm`.

## 1.2 Launch.

* To run the website, open two terminals on VSCode.
  * On one, `cd` into the `flask-server` folder and run `python server.py` to start the backend.
    * Before launching the backend, please check the configuration (see [Flask-server Configuration](./flask-server/README.md#2-configuration)).
    * The backend should begin running on `localhost:5000`.
  * On the other, if you need to run the frontend, run `npm start` in the `client` folder.
    * If you are faced with `sh: 1: react-scripts: Permission denied` error, use `sudo npm start`.
    * If you are faced with `sh: 1: react-scripts: not found` error:
      * Use `npm install react-scripts`.
* To stop the website run:
  * kill %1;kill %2
* That's it! The website should begin running on `localhost:3000`.
  * If you use WSL or virtual machine, the address should be `<ip.to.your.vm>:3000`.
