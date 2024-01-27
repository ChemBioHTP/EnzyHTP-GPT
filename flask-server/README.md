# Flask-server

[TOC]

## 1. Introduction

The backend of EnzyHTP Web Application.

This **README** describes some general information about how to deal with the configuration, settings, certificates and oauth clients so as to enable the flask-server to run properly.

## 2. Configuration

The `settings.py` and `context.py` files in the `/flask-server` directory are to support database and user authentication.

### 2.1 Settings

- Filepath: `/flask-server/settings.py`

This file is cited as an object to inject the runtime configurations of the flask server so as to protect the main file `/flask-server/server.py` from getting 'contaminated'.

### 2.2 Context

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
