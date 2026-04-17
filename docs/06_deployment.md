# Deployment Guide

This guide is for server maintainers and provides instructions for deploying the EnzyHTP-GPT application in a production environment.

The recommended deployment method is using the provided `docker-compose.yml` file, which orchestrates the frontend, backend, database, and web server.

## 1. All-in-One Deployment with Docker Compose

This stack runs:

-   **Frontend**: Built with Node (Vite) inside the `web-builder` container and served by Nginx.
-   **Backend**: Flask app listening on port 8000.
-   **Database**: MongoDB container with data persisted to the host.
-   **Nginx**: Reverse proxy that serves the frontend and routes API requests to the backend.

### 1.1. Prerequisites

Create the required directories on the host machine:

```bash
mkdir -p /mutexa/raid5/data/mongodb
mkdir -p /mutexa/raid5/data/enzyhtp_gpt/ssl
mkdir -p /mutexa/raid5/data/enzyhtp_gpt/files
mkdir -p /mutexa/raid5/data/enzyhtp_gpt/nginx/log
```

Grant the necessary permissions:

```bash
chmod o+w /mutexa/raid5/data/mongodb
chmod g+w /mutexa/raid5/data/mongodb
chmod o+w ./web-client
chmod g+w ./web-client
```

Setup SSL Certificates

```bash
cd flask-server/certs
bash generate_cert.sh
```

Setup OAuth

Configuration files for OAuth clients should be put under `flask-server/oauth_clients`. These are not included in the repository and must be obtained from the project maintainers.

### 1.2. Environment Variables

Copy the `.env.example` file to `.env` and customize the environment variables as needed.

```bash
cp .env.example .env
```

Key variables for backend runtime:

- `MONGO_URI`: MongoDB connection string.
- `OPENAI_RUNTIME`: `responses` (recommended) or `assistants` (legacy fallback).

Runtime precedence:

1. value in `.env`
2. fallback value in `docker-compose.yml`
3. backend code fallback in `flask-server/config.py`

In most cases, editing `.env` is sufficient; you do not need to modify `docker-compose.yml`.

### 1.3. Start, Stop, and Monitor

-   **Build and start in the background:**
    ```bash
    docker compose --env-file ./.env up -d --build
    ```

-   **Show status:**
    ```bash
    docker compose ps
    ```

-   **Tail logs:**
    ```bash
    docker compose logs -f <service_name>  # e.g., flask, nginx
    ```

-   **Stop all services:**
    ```bash
    docker compose down
    ```

### 1.4. Frontend Rebuild

To build/rebuild the frontend in a new development (or after making changes to the `web-client` code):

```bash
docker compose exec web-builder bash -lc "npm run build"
```

## 2. Manual Deployment (Legacy)

While Docker Compose is recommended, it is also possible to run the services as separate Docker containers.

### Flask Server (Backend)

1.  **Build the image:**
    ```bash
    cd flask-server
    docker build -t enzyhtp.web.flask:latest .
    ```

2.  **Run the container:**
    ```bash
    docker run -d --name enzyhtp.web.flask \
      -v /path/to/EnzyHTP-GPT/flask-server:/var/www/flask-server \
      -v /path/to/ssl:/var/www/ssl \
      -v /path/to/files:/var/www/files \
      -v /path/to/EnzyHTP:/var/bin/EnzyHTP \
      -p 12306:8000 \
      enzyhtp.web.flask:latest
    ```

### Nginx Server

1.  **Pull the image:**
    ```bash
    docker pull nginx
    ```

2.  **Run the container:**
    ```bash
    docker run -d --name enzyhtp.web.nginx -p 80:80 -p 443:443 \
      -v /path/to/EnzyHTP-GPT/nginx.conf:/etc/nginx/nginx.conf \
      -v /path/to/ssl:/etc/nginx/ssl \
      -v /path/to/log:/var/log/nginx \
      -v /path/to/EnzyHTP-GPT/web-client/dist:/usr/share/nginx/html \
      nginx
    ```

## 3. Troubleshooting

-   **Frontend build fails with `EACCES: permission denied`**: This is likely a host permission issue on the `./web-client/dist` directory. Ensure the user running the Docker container has write permissions. Avoid manually creating an empty dist, the builder will create it with the right permission.
-   **Nginx serves the welcome page or 403 errors**: Ensure the `web-client/dist` directory is not empty and contains the built frontend assets. Verify the volume mount in your Nginx container points to the correct directory.
-   **Flask can't connect to Mongo**: Ensure the MongoDB container is healthy before the Flask container starts. The `docker-compose.yml` file uses `depends_on` to manage service startup order.
