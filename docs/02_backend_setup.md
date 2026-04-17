# Backend Setup (flask-server)

This document provides instructions for setting up and running the Flask backend for EnzyHTP-GPT.

## 1. Environment Setup

### Using Conda

1.  **Create Conda Environment**: Create a conda environment from the provided `environment.yml` file:
    ```bash
    conda env create -f flask-server/environment.yml
    ```

2.  **Install EnzyHTP**: Clone the EnzyHTP library and configure it using the provided script:
    ```bash
    git clone https://github.com/ChemBioHTP/EnzyHTP.git ~/bin/EnzyHTP
    cd ~/bin/EnzyHTP
    git checkout develop
    cd /path/to/EnzyHTP-GPT
    bash flask-server/enzyhtp_env_config.sh --path ~/bin/EnzyHTP
    ```

### OpenAI SDK Version

The backend runtime supports both legacy Assistants API and Responses API paths.  
Use the OpenAI SDK version declared in `flask-server/environment.yml` (`openai==2.29.0`).

You can verify the installed version:

```bash
python - <<'PY'
import openai
print(openai.__version__)
PY
```

### Database

The application uses MongoDB. For local development, you can install it following the official documentation or use the containerized deployment method described in the [Deployment documentation](./06_deployment.md).

## 2. Running the Backend

### Development Mode

To run the backend in development mode with hot-reloading:

```bash
cd flask-server
flask run
```

The backend will be available at `http://localhost:5000`.

### Production Mode (Docker)

For production, the backend is run as a containerized service using Docker Compose. See the [Deployment documentation](./06_deployment.md) for more details.

## 3. Configuration

-   **`config.py`**: This file contains the runtime configurations for the Flask server.
-   **`context.py`**: This file declares the `SQLAlchemy` database instance, the `LoginManager` for authentication, and the SSL context.

### OpenAI Runtime Switch

Set `OPENAI_RUNTIME` to choose backend OpenAI runtime:

- `assistants`: legacy Assistants/Threads path (compatibility fallback)
- `responses`: new Responses/Conversations path (recommended)

Important defaults:

- `flask-server/config.py` fallback default: `assistants`
- `.env.example` and `docker-compose.yml` default: `responses`

In normal deployment, configure this in `.env` only; no `docker-compose.yml` change is required.

Quick runtime check:

```bash
cd flask-server
python dev-tools/check_openai_runtime.py
```

### Session Field Migration Script

For existing databases with thread-only historical records, run:

```bash
cd flask-server
python dev-tools/migrate_thread_to_conversation.py --dry-run
python dev-tools/migrate_thread_to_conversation.py --apply
```

This script is idempotent and safe to re-run.

### SSL Certificates

For features like Google Login, the backend requires HTTPS. The `flask-server/certs` directory contains a script to generate self-signed certificates for development:

```bash
cd flask-server/certs
bash generate_cert.sh
```

### OAuth Clients

The application supports OAuth for authentication (e.g., Google Login). Configuration files for OAuth clients are stored in the `flask-server/oauth_clients` directory. These are not included in the repository and must be obtained from the project maintainers.
