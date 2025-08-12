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

**ATTENTION: Please ask [Zhong, Yinjie](mailto:yinjie.zhong@outlook.com) for detailed information!!**

We use docker container to deploy the website to ensure environmental independence.

## 2.1 All-in-One Solution

If you adopt this solution to deploy this website on Mutexa CSB Workstation, you can omit all other `2.X` contents.

We have now facilitated an all-in-one solution with the `docker-compose.yml`. To use this, please follow the instructions below.

This stack runs:

* Frontend: Built with Node (Vite) inside the `web-builder` container (`npm ci && npm run build`) and outputs to `./web-client/dist`. Nginx serves that directory over ports 80/443. By default, the official Nginx image serves files from `/usr/share/nginx/html`. 
* Backend: Flask app built from `flask-server/Dockerfile`, listening on 8000, mapped to host 12306 (editable in .env).
* Database: MongoDB container with data persisted to your host via `MONGO_DATA_DIR`.
* Startup order is enforced so Flask waits for Mongo to be healthy via `depends_on: condition: service_healthy`.

### 2.1.1 Directories required.

```bash
mkdir -p /mutexa/raid5/data/mongodb
mkdir -p /mutexa/raid5/data/enzyhtp_gpt/ssl
mkdir -p /mutexa/raid5/data/enzyhtp_gpt/files
mkdir -p /mutexa/raid5/data/enzyhtp_gpt/nginx/log
```

> Permissions note: the frontend build writes to `./web-client/dist` via a bind mount, so write permissions are controlled by the host. If you see `EACCES` errors while building, grant your user write access to that directory or adjust ownership.

Grant permission as follows.

```bash
$ chmod o+w /mutexa/raid5/data/mongodb
$ chmod g+w /mutexa/raid5/data/mongodb
$ chmod o+w ./web-client
$ chmod g+w ./web-client
```

### 2.1.2 Environment File

Copy the `.env.example` to `.env` file in the project root.

### 2.1.3 Start and Stop

```bash
# Build and start in the background
$ docker compose --env-file ./.env up -d --build

# Show status (health, ports, etc.)
$ docker compose ps

# Tail logs
$ docker compose logs -f mongo
$ docker compose logs -f flask
$ docker compose logs -f web-builder
$ docker compose logs -f nginx

# Stop everything
$ docker compose down
```

Health checks are defined per service; `depends_on: service_healthy` ensures Mongo passes its healthcheck before Flask starts.

**Check if your website works now. If so, your deployment is done!**

#### 2.1.4 Frontend Rebuild

Rebuild after changing the frontend code:

```bash
$ docker compose exec web-builder bash -lc "npm run build"
```

Vite’s default build output directory is `dist`; you can change it via `build.outDir` in your Vite config if needed.

**Check if your website works now. If so, your rebuild is done!**
**The following is additional information, please refer to it when needed.**

## 2.1.5 Nginx notes

- Static files are served from `/usr/share/nginx/html` inside the official Nginx container, which we bind-mount from `./web-client/dist` (read-only).
- Put certs under `SSL_DIR` and reference them in `nginx.conf` as `/etc/nginx/ssl/...`.
- Reverse-proxy the backend to `http://flask:8000` (service DNS name within the Compose network).
- Optionally add a lightweight health endpoint (e.g., `/healthz`) in Nginx for stricter checks.

## 2.1.6 MongoDB notes

- Data persists to the host directory specified by `MONGO_DATA_DIR`.
- The healthcheck uses `mongosh` to run `db.adminCommand({ ping: 1 })` and mark the service healthy.
- When upgrading across major MongoDB versions, follow Mongo’s upgrade notes and back up first.

## 2.1.7 Troubleshooting

**Frontend build fails with `EACCES: permission denied, mkdir '/app/dist/...'`**  
`./web-client/dist` is a bind mount controlled by host permissions. Fix by adjusting ownership/permissions on the host so the container user can write.

**Nginx serves the welcome page or returns 403**

- Ensure `./web-client/dist` exists and contains the built assets.
- Verify the bind mount: `./web-client/dist:/usr/share/nginx/html:ro` (the official Nginx image serves from `/usr/share/nginx/html`).

**Flask can’t connect to Mongo on startup**  
Increase Mongo’s `healthcheck` `retries`/`start_period` and keep `depends_on: condition: service_healthy` so Flask starts only after Mongo is healthy.

**What does `:ro` do?**  
It mounts a bind/volume as read-only inside the container (host remains writable).

## 2.1.8 Day-2 operations

```bash
# Pull newer base images and restart
docker compose pull
docker compose up -d

# Rebuild frontend only
docker compose exec web-builder bash -lc "npm run build"
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
