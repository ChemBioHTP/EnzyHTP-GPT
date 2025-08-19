# EnzyHTP-GPT Development Documentation

## 1. Project Overview

EnzyHTP-GPT is a web application designed for enzyme high-throughput screening and protein engineering. It leverages large language models (LLMs) to provide a conversational interface for designing and analyzing protein mutations and their effects on enzyme function. The application consists of a Python Flask backend that handles the core scientific logic and a Node.js/Vue.js frontend for the user interface.

The system is designed to be deployed using Docker, with services for both the frontend and backend, as well as a MongoDB database. It also includes functionality to interface with a SLURM cluster for running computational tasks.

## 2. Technology Stack

### Backend

*   **Framework**: Flask
*   **Database**: MongoDB
*   **Authentication**: Flask-Login, JWT for API endpoints
*   **Deployment**: uWSGI, Docker
*   **Core Logic**: EnzyHTP library

### Frontend

*   **Framework**: Vue.js 3
*   **UI Library**: Ant Design Vue
*   **State Management**: Pinia
*   **Build Tool**: Vite
*   **HTTP Client**: Axios

### Other

*   **API Documentation**: Postman
*   **Containerization**: Docker, Docker Compose

## 3. Project Structure

The project is organized into the following main directories:

*   `flask-server/`: Contains the backend Flask application.
    *   `auth/`: Handles user authentication and authorization.
    *   `experiment/`: Manages experiment data, configurations, and results.
    *   `services/`: Contains services for interacting with external APIs like OpenAI and SLURM.
    *   `prompts/`: Stores prompts for the LLM agents.
    *   `agent_benchmark/`: Contains scripts and data for benchmarking the LLM agents.
*   `web-client/`: Contains the frontend Vue.js application.
    *   `src/api/`: Contains the logic for making API calls to the backend.
    *   `src/components/`: Reusable Vue components.
    *   `src/views/`: Application pages.
    *   `src/router/`: Frontend routing configuration.
    *   `src/stores/`: Pinia state management stores.
*   `docs/`: Contains API documentation, including a Postman collection.
*   `docker-compose.yml`: Defines the services, networks, and volumes for the Docker application.
*   `nginx.conf`: Configuration file for the Nginx reverse proxy.

## 4. Backend Setup & API

### 4.1. Environment Setup

1.  **Conda Environment**: Create a conda environment using the provided `environment.yml` file:
    ```bash
    conda env create -f flask-server/environment.yml
    ```
2.  **EnzyHTP Installation**: Clone the EnzyHTP library and configure it using the provided script:
    ```bash
    git clone https://github.com/ChemBioHTP/EnzyHTP.git ~/bin/EnzyHTP
    bash flask-server/enzyhtp_env_config.sh --path ~/bin/EnzyHTP
    ```
3.  **Database**: The application uses MongoDB. For local development, you can install it following the official documentation or use the containerized deployment method described in `flask-server/README.md`.

### 4.2. Running the Backend

*   **Development**:
    ```bash
    cd flask-server
    flask run
    ```
*   **Production (Docker)**:
    ```bash
    docker-compose up -d --build
    ```

### 4.3. API Endpoints

The backend exposes a RESTful API for managing users, experiments, and other resources. The base URL for all API endpoints is `/api`.

#### 4.3.1. Authentication (`/api/auth`)

*   `POST /register`: Register a new user.
*   `POST /login`: Log in a user.
*   `POST /logout`: Log out the current user.
*   `GET /profile`: Get the current user's profile.
*   `PUT /profile`: Update the current user's profile.
*   `PUT /password/change`: Change the current user's password.
*   `POST /password/reset/generate`: Generate a password reset verification code.
*   `PUT /password/reset`: Reset the password using a verification code.
*   `GET /oauth/<oauth_vendor>/login`: Initiate OAuth login with a specific vendor (e.g., `google`).
*   `GET /oauth/<oauth_vendor>/login/callback`: Callback URL for OAuth login.

#### 4.3.2. Experiments (`/api/experiment`)

*   `GET /`: Get a list of the current user's experiments.
*   `POST /`: Create a new experiment.
*   `DELETE /`: Delete an experiment.
*   `GET /<experiment_id>`: Get the details of a specific experiment.
*   `PUT /<experiment_id>`: Update an experiment's information.
*   `PATCH /<experiment_id>`: Update the status and progress of an experiment.
*   `GET /<experiment_id>/result`: Get the analysis results of an experiment.
*   `POST /<experiment_id>/result`: Post new analysis results to an experiment.
*   `GET /<experiment_id>/assistants`: Get the messages from the OpenAI Assistant thread.
*   `POST /<experiment_id>/assistants`: Interact with the OpenAI Assistant.
*   `PUT /<experiment_id>/assistants`: Toggle to the next assistant in the workflow.
*   `DELETE /<experiment_id>/assistants`: Clear the assistant thread.
*   `GET /<experiment_id>/downloadable`: Download a zip file of all downloadable files for an experiment.
*   `GET /<experiment_id>/downloadable/<filepath>`: Download a specific file from an experiment.
*   `GET /<experiment_id>/pdb_file`: Download the PDB file for an experiment.
*   `POST /<experiment_id>/pdb_file`: Upload a PDB file for an experiment.
*   `GET /<experiment_id>/mutations`: Get the mutation space for an experiment.
*   `POST /<experiment_id>/mutations`: Generate a mutation pattern from natural language.
*   `PUT /<experiment_id>/mutations`: Update the mutation space for an experiment.
*   `GET /<experiment_id>/slurm`: Get SLURM job information for an experiment.
*   `POST /<experiment_id>/slurm`: Submit a SLURM job for an experiment.
*   `DELETE /<experiment_id>/slurm`: Delete a SLURM job for an experiment.
*   `GET /<experiment_id>/deploy`: Download a deployment package for running simulations on a separate SLURM cluster.

For detailed information on request and response formats, please refer to the `docs/20250419_Web APIs.postman_collection.json` file.

## 5. Frontend Setup

### 5.1. Environment Setup

1.  **Node.js**: Ensure you have Node.js v18.x or higher installed.
2.  **Dependencies**: Install the frontend dependencies:
    ```bash
    cd web-client
    npm install
    ```

### 5.2. Running the Frontend

*   **Development**:
    ```bash
    cd web-client
    npm run dev
    ```
    The application will be available at `http://localhost:3000`.

*   **Production Build**:
    ```bash
    cd web-client
    npm run build
    ```
    The production-ready files will be generated in the `web-client/dist` directory.

## 6. Deployment

The application is designed to be deployed using Docker and Docker Compose. The `docker-compose.yml` file defines the following services:

*   `flask-server`: The backend Flask application.
*   `web-client`: The frontend Vue.js application, served by a Node.js server.
*   `nginx`: An Nginx reverse proxy to route traffic to the appropriate service.

To deploy the application, run:

```bash
docker-compose up -d --build
```

The application will be accessible at the address of the host machine.

## 7. Agent Workflow

The core of the application's intelligence lies in its AI agents, which are powered by OpenAI's GPT models. The workflow is orchestrated by a series of prompts and agents that guide the user through the process of designing and analyzing experiments.

The main agents are:

*   **Question Analyzer**: Decomposes and revises the user's scientific question to ensure it is clear, specific, and actionable.
*   **Metrics Planner**: Helps the user select the appropriate computational metrics to measure the desired properties of the protein.
*   **Mutant Planner**: Translates the user's natural language description of mutations into the precise EnzyHTP syntax.

The prompts for these agents can be found in the `flask-server/prompts` directory. The `flask-server/agent_benchmark` directory contains scripts and data for evaluating the performance of these agents.
