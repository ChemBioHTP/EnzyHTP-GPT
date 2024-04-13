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
[+] Building 32.0s (10/10) FINISHED                                                                            docker:default
 => [internal] load build definition from Dockerfile                                                                     0.0s
 => => transferring dockerfile:                                                                                          0.0s
 => [internal] load metadata for docker.io/library/node:16-alpine                                                        0.9s
 => [internal] load .dockerignore                                                                                        0.0s
 => => transferring context: 52B                                                                                         0.0s
 => [1/5] FROM docker.io/library/node:16-alpine@sha256:a1f9d027912b58a7c75be7716c97cfbc6d3099f3a97ed84aa490be9dee20e787  2.2s
 => => resolve docker.io/library/node:16-alpine@sha256:a1f9d027912b58a7c75be7716c97cfbc6d3099f3a97ed84aa490be9dee20e787  0.0s
 => => sha256:a1f9d027912b58a7c75be7716c97cfbc6d3099f3a97ed84aa490be9dee20e787 1.43kB / 1.43kB                           0.0s
 => => sha256:72e89a86be58c922ed7b1475e5e6f151537676470695dd106521738b060e139d 1.16kB / 1.16kB                           0.0s
 => => sha256:2573171e0124bb95d14d128728a52a97bb917ef45d7c4fa8cfe76bc44aa78b73 6.73kB / 6.73kB                           0.0s
 => => sha256:7264a8db6415046d36d16ba98b79778e18accee6ffa71850405994cffa9be7de 3.40MB / 3.40MB                           0.2s
 => => sha256:eee371b9ce3ffdbb8aa703b9a14d318801ddc3468f096bb6cfeabbeb715147f9 36.63MB / 36.63MB                         0.7s
 => => sha256:93b3025fe10392717d06ec0d012a9ffa2039d766a322aac899c6831dd93382c2 2.34MB / 2.34MB                           0.3s
 => => extracting sha256:7264a8db6415046d36d16ba98b79778e18accee6ffa71850405994cffa9be7de                                0.1s
 => => sha256:d9059661ce70092af66d2773666584fc8addcb78a2be63f720022f4875577ea9 452B / 452B                               0.3s
 => => extracting sha256:eee371b9ce3ffdbb8aa703b9a14d318801ddc3468f096bb6cfeabbeb715147f9                                1.3s
 => => extracting sha256:93b3025fe10392717d06ec0d012a9ffa2039d766a322aac899c6831dd93382c2                                0.1s
 => => extracting sha256:d9059661ce70092af66d2773666584fc8addcb78a2be63f720022f4875577ea9                                0.0s
 => [internal] load build context                                                                                        0.7s
 => => transferring context: 6.38MB                                                                                      0.6s
 => [2/5] WORKDIR /usr/src/app                                                                                           0.3s
 => [3/5] COPY package.json package-lock.json ./                                                                         0.1s
 => [4/5] RUN npm install                                                                                               24.3s
 => [5/5] COPY . .                                                                                                       0.2s
 => exporting to image                                                                                                   4.0s
 => => exporting layers                                                                                                  4.0s
 => => writing image sha256:4d487e49a58bd3aecbfcae9a6c86e124d25e3557c70e73cb7bb523c470ea5a65                             0.0s
 => => naming to docker.io/library/enzyhtp.web.node:2024.04.v02                                                          0.0s
```

To run the docker container, enter and execute the following `docker run` command.

In this command, port 443 of the host is mapped to port 3000 of the container, and the flask-server folder on the host is mapped to the working directory in the container, that is, any modifications in this folder will be instantly synchronized to the working directory, so that the service manager only needs to restart the container to complete the update.

```bash
docker run -d --name enzyhtp.web.node -v /path/to/EnzyHTP-GPT/src:/usr/src/app/src -p 12580:3000 enzyhtp.web.node:2024.04.v02
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
-v /path/to/log:/var/log/nginx nginx
```

Note that

1. `/path/to/ssl` is a folder which contains `server.crt` and `server.key` file for SSL.
2. `/path/to/log` should grant write permission to all users by `chmod g+w /path/to/log` and `chmod o+w /path/to/log` commands.