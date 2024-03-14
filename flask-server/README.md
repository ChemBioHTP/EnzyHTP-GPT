# Flask-server

[TOC]

## 1. Introduction

The backend of EnzyHTP Web Application.

This **README** describes some general information about how to deal with the configuration, settings, certificates and oauth clients so as to enable the flask-server to run properly.

## 2. Configuration

### 2.1 Environment Configuration

* First, clone this repository onto your local machine.
  * Use git command `git clone https://github.com/ChemBioHTP/EnzyHTP-GPT.git`

* Then, We need to create a conda environment to run the flask backend.
  * There is an existing `environment.yml` file for you to make new anaconda environment automatically.
    * `conda env create -f environment.yml`. This command can be followed by `-n` or `--name` option to specify the environment name.

* We will also install EnzyHTP (by cloning it onto your local machine for now).
  * To do this, run `git clone https://github.com/ChemBioHTP/EnzyHTP.git <path/to/save>` Here, we take `~/bin/EnzyHTP` as an example, i.e., run `git clone https://github.com/ChemBioHTP/EnzyHTP.git ~/bin/EnzyHTP`
  * Then, back to this directory, and then follow the instructions in the `enzyhtp_env_config.sh` script to adjust and run it. `bash enzyhtp_env_config.sh`
  * You should now be able to use EnzyHTP with the site.

The `settings.py` and `context.py` files in the `/flask-server` directory are to support database and user authentication.

### 2.2 Runtime Configuration

#### 2.2.1 Settings

- Filepath: `/flask-server/settings.py`

This file is cited as an object to inject the runtime configurations of the flask server so as to protect the main file `/flask-server/server.py` from getting 'contaminated'.

#### 2.2.2 Context

- Filepath: `/flask-server/context.py`

This file is to declare the `SQLAlchemy` database instance (named `db`) and the `LoginManager` instance (named `login_manager`) for the whole flask server.

SSL Context (named `ssl_context`) is also declared here to enable HTTPS Protocol, which requires the existence of `/flask-server/certs/server/server.crt` and `/flask-server/certs/server/server.key`. See [SSL Certificates](#3-ssl-certificates).

Those instances can only be declared in an individual file and imported into the main file and anywhere else in the server. Otherwise, a number of "Exception(s)", and a "Warning" prompt which will be set to "Exception" in the next version, will be triggered.

## 3. SSL Certificates

- Filepath: `/flask-server/settings.py`

Social Login(s), such as *Google Login*, require **HTTPS Protocol** to complete its login workflow for the sake of security, thus, the `certs` directory is made to save some self-signed certificates generated with OpenSSL.

There is a bash script `generate_cert.sh` in the `certs` directory. Its usage is as follows, whose default setting works, i.e., you can just run `bash generate_cert.sh` and three subfolders may appear.

```bash
Usage: generate_cert.sh [--cn COMMON_NAME] [--days VALID_DATE]

Generate Self-signed X509 Certificate using OpenSSL.

   --cn    Specify the common name (domain name). Defaults 'localhost'.
   --days        Specify the validity period of the certificate. Defaults '365'.
   -h, --help    Display this help and exit.
```

## 4. OAuth Clients

Currently, only Google Login is available in our backend. There's a template json file in `oauth_clients` directory entitled `template_login_client.json`, derived from google's format, showing the schema of a login client json file.

Please reach out to `yinjie.zhong@vanderbilt.edu` if you need a `google_login_client.json` file. The file should be saved in the `oauth_clients` directory. Any questions are welcome about authentication module.

## 5. Production Deployment (Flask Server)

In the production environment, we use uWSGI to run the Flask Server. Thus, we build `uwsgi.ini` config file and `start.sh` script to run it.

To build the `enzyhtp.web.flask` (i.e., backend) docker image, enter and run the following `docker build` command. 

```bash
.../EnzyHTP-GPT/flask-server$ docker build -t enzyhtp.web.flask:2024.02.v02 .                                         
(enzyhtp-gpt) (base) yinjie@LAPTOP-U8L2I5V9:~/EnzyHTP-GPT/flask-server$ docker build -t enzyhtp.web.flask:2024.02.v02 .
[+] Building 1143.1s (10/10) FINISHED                                                                   docker:default
 => [internal] load .dockerignore                                                                                 0.0s
 => => transferring context: 2B                                                                                   0.0s
 => [internal] load build definition from Dockerfile                                                              0.0s
 => => transferring dockerfile: 485B                                                                              0.0s
 => [internal] load metadata for docker.io/continuumio/anaconda3:main                                             0.0s
 => CACHED [1/5] FROM docker.io/continuumio/anaconda3:main                                                        0.0s
 => [internal] load build context                                                                                 0.0s
 => => transferring context: 28.69kB                                                                              0.0s
 => [2/5] RUN mkdir -p /var/www/flask-server && cd /var/www/flask-server                                          0.2s
 => [3/5] WORKDIR /var/www/flask-server                                                                           0.0s
 => [4/5] ADD . /var/www/flask-server                                                                             0.0s
 => [5/5] RUN bash ./docker_env_config.sh                                                                      1106.7s
 => exporting to image                                                                                           36.2s 
 => => exporting layers                                                                                          36.2s 
 => => writing image sha256:588b70bf27016a19e797962caad54df91ae31f586767c4a9707bcecf17c60599                      0.0s 
 => => naming to docker.io/library/enzyhtp.web.flask:2024.02.v02                                                  0.0s
```

To run the docker container, enter and execute the following `docker run` command.

In this command, port 12306 of the host is mapped to port 8000 of the container, and the flask-server folder on the host is mapped to the working directory in the container, that is, any modifications in this folder will be instantly synchronized to the working directory, so that the service manager only needs to restart the container to complete the update.

```bash
docker run -d --name enzyhtp.web.flask -v .../EnzyHTP-GPT/flask-server:/var/www/flask-server -p 12306:8000 enzyhtp.web.flask:2024.02.v02
```

To test the backend, please set the address to the host server and the port to 12306.

Functions that require HTTPS, such as Google Login, need to work with a website server loaded with an SSL certificate and use a reverse proxy to test and run.

**Attention:** You must have your database instance and oauth_client files ready before running the docker container!
