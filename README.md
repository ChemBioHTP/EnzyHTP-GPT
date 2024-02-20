# EnzyHTP-GPT

A web application that serves as an interface between a user and EnzyHTP's workflows.

[TOC]

# 1. Developers: First Time Install

## 1.1 Environment Configuration.

* To configure the environment of the flask server, please follow the instructions in [Flask Server Environment Configuration](./flask-server/README.md#21-environment-configuration).

* We also need to install `npm`.
  - Taking Ubuntu (or WSL Ubuntu) for instance, install `npm` using command `sudo apt-get install npm`.

## 1.2 Launch.

* To run the website, open two terminals on VSCode.
  * On one, `cd` into the `flask-server` folder and run `python server.py` to start the backend.
    * Before launching the backend, please check the configuration (see [Flask-server Configuration](./flask-server/README.md#22-runtime-configuration)).
    * The backend should begin running on `localhost:5000`.
  * On the other, if you need to run the frontend, run `npm start` in the `client` folder.
    * If you are faced with `sh: 1: react-scripts: Permission denied` error, use `sudo npm start`.
    * If you are faced with `sh: 1: react-scripts: not found` error:
      * Use `npm install react-scripts`.
* To stop the website run:
  * kill %1;kill %2
* That's it! The website should begin running on `localhost:3000`.
  * If you use WSL or virtual machine, the address should be `<ip.to.your.vm>:3000`.

# 2. Server Manager: Production Deployment

We are to use docker container to deploy the website to ensure environmental independence.

## 2.1 Nginx Server (Website and Frontend)

... To be continued.

## 2.2 Flask Server (Backend)

To deploy the flask server for production environment using docker, please follow the instructions in [Production Deployment (Flask Server)](./flask-server/README.md#5-production-deployment-flask-server).