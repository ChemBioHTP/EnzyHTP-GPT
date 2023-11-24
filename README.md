# EnzyHTP-GPT

A web application that serves as an interface between a user and EnzyHTP's workflows.

[TOC]

# 1. Developers: First Time Install

## 1.1 Environment Configuration.

- First, clone this repository onto your local machine.

  - Use git command `git clone https://github.com/ChemBioHTP/EnzyHTP-GPT.git`

- We will then need to create a conda environment to run the website.

  - There is an existing `environment.yml` file for you to make new anaconda environment.
    - `conda env create -f environment.yml`
  - You can also build the environment manually.
    - Create a new conda environment `conda create -n enzyhtp-gpt`. The name following `-n` flag could be anything you like.
    - Install Flask using the command `conda install -c anaconda flask flask-login flask-sqlalchemy`.

- We will also install EnzyHTP (by cloning it onto your local machine for now).

  - To do this, run `git clone https://github.com/ChemBioHTP/EnzyHTP.git new_enzy_htp`
  - Then, run `cd new_enzy_htp` and `git checkout develop_refactor`
  - Finally, run `sh dev-tools/install` to install all dependencies into your conda env.
  - You should now be able to use EnzyHTP with the site.

- We also need to install `npm`.
  - Taking Ubuntu (or WSL Ubuntu) for instance, install `npm` using command `sudo apt-get install npm`.

## 1.2 Launch.

- To run the website, open two terminals on VSCode.
  - On one, `cd` into the `flask-server` folder and run `python server.py` to start the backend.
    - Before launching the backend, please check the configuration (see [Flask-server Configuration](./flask-server/README.md#2-configuration)).
  - On the other, run `npm run start-frontend` in the `src` folder.
    - If you are faced with `sh: 1: react-scripts: Permission denied` error, use `sudo npm start`.
    - If you are faced with `sh: 1: react-scripts: not found` error:
      - Use `npm install react-scripts`.
- To stop the website run:
  - kill %1;kill %2
- That's it! The website should begin running on `localhost:3000`.
  - If you use WSL or virtual machine, the address should be `<ip.to.your.vm>:3000`.
