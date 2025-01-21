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

**ATTENTION: Please ask [Zhong, Yinjie](mailto:yinjie.zhong@vanderbilt.edu) for detailed information!!**

We use docker container to deploy the website to ensure environmental independence.

## 2.1 Node Server (Frontend)

To build the `enzyhtp.web.flask` (i.e., backend) docker image, enter and run the following `docker build` command.

```bash
.../EnzyHTP-GPT$ docker build -t enzyhtp.web.node:2024.04.v02 .
```

To run the docker container, enter and execute the following `docker run` command.

In this command, port 443 of the host is mapped to port 3000 of the container, and the flask-server folder on the host is mapped to the working directory in the container, that is, any modifications in this folder will be instantly synchronized to the working directory, so that the service manager only needs to restart the container to complete the update.

```bash
docker run -d --name enzyhtp.web.node -v /path/to/EnzyHTP-GPT/src:/usr/src/app/src -v /path/to/EnzyHTP-GPT/public:/usr/src/app/public -p 12580:3000 enzyhtp.web.node:2024.04.v02
```

## 2.2 Flask Server (Backend)

To deploy the flask server for production environment using docker, please follow the instructions in [Production Deployment (Flask Server)](./flask-server/README.md#5-production-deployment-flask-server).

## 2.3 Nginx Server (Web Server)

Fetch the docker image `nginx`, and then execute the command as follows.

```bash
.../EnzyHTP-GPT$ docker pull nginx
.../EnzyHTP-GPT$ docker run -d --name enzyhtp.web.nginx -p 80:80 -p 443:443 \
-v /path/to/EnzyHTP-GPT/nginx.conf:/etc/nginx/nginx.conf \
-v /path/to/ssl:/etc/nginx/ssl \
-v /path/to/log:/var/log/nginx \
-v /path/to/EnzyHTP-GPT/web-client:/usr/share/nginx/html nginx
# -v /path/to/EnzyHTP-GPT/alternative_pages:/usr/share/nginx/html nginx
```

Note that

1. `/path/to/ssl` is a folder which contains `server.crt` and `server.key` file for SSL.
2. `/path/to/log` should grant write permission to all users by `chmod g+w /path/to/log` and `chmod o+w /path/to/log` commands.

A practical example of use is as follows:

```bash
.../EnzyHTP-GPT$ docker pull nginx
.../EnzyHTP-GPT$ docker run -d --name enzyhtp.web.nginx -p 80:80 -p 443:443 \
-v /home/zhongy8/bin/EnzyHTP-GPT/nginx.conf:/etc/nginx/nginx.conf \
-v /mutexa/raid5/data/enzyhtp_gpt/ssl:/etc/nginx/ssl \
-v /mutexa/raid5/data/enzyhtp_gpt/nginx/log:/var/log/nginx \
-v /home/zhongy8/bin/EnzyHTP-GPT/web-client:/usr/share/nginx/html nginx
# -v /home/zhongy8/bin/EnzyHTP-GPT/alternative_pages:/usr/share/nginx/html nginx
```
