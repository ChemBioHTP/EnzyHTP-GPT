# EnzyHTP-GPT Architecture

## 1. System Overview

EnzyHTP-GPT is a full-stack web application designed to facilitate enzyme high-throughput screening and protein engineering. It provides a user-friendly, conversational interface powered by Large Language Models (LLMs) to help scientists design, run, and analyze computational experiments on protein mutations.

The application is composed of:
- A **Vue.js frontend** (`web-client`) for the user interface.
- A **Python Flask backend** (`flask-server`) that handles the core scientific logic, user management, and interaction with external services.
- A **MongoDB database** for data persistence.
- An **Nginx server** acting as a reverse proxy.

The entire system is designed to be containerized using Docker and Docker Compose for consistent deployment across different environments.

*(Placeholder for a high-level architecture diagram)*

## 2. Technology Stack

### Frontend (`web-client`)
- **Framework:** Vue.js 3
- **UI Library:** Ant Design Vue
- **State Management:** Pinia
- **Build Tool:** Vite
- **HTTP Client:** Axios

### Backend (`flask-server`)
- **Framework:** Flask
- **Core Logic:** Integrates with the `EnzyHTP` library for scientific computations.
- **AI Agents:** Uses OpenAI's GPT models to power a conversational workflow for experiment design.
- **Database:** MongoDB
- **Authentication:** Flask-Login for session management and JWT for APIs. Supports OAuth (Google Login).
- **External Services:** Interacts with SLURM clusters via a REST API for job submission and management.
- **Deployment:** Can be run directly with `flask run` for development or deployed with uWSGI and Docker for production.

### Deployment and Orchestration
- **Containerization:** `Docker` and `docker-compose.yml` are used to define and manage the application services.
- **Web Server:** Nginx is used as a reverse proxy to direct traffic to the frontend and backend services and to handle SSL termination.

## 3. Project Structure

The project is organized into the following main directories:

-   `flask-server/`: Contains the backend Flask application.
    -   `auth/`: Handles user authentication and authorization.
    -   `experiment/`: Manages experiment data, configurations, and results.
    -   `services/`: Contains services for interacting with external APIs like OpenAI and SLURM.
    -   `prompts/`: Stores prompts for the LLM agents.
    -   `agent_benchmark/`: Contains scripts and data for benchmarking the LLM agents.
-   `web-client/`: Contains the frontend Vue.js application.
    -   `src/api/`: Contains the logic for making API calls to the backend.
    -   `src/components/`: Reusable Vue components.
    -   `src/views/`: Application pages.
    -   `src/router/`: Frontend routing configuration.
    -   `src/stores/`: Pinia state management stores.
-   `docs/`: Contains all project documentation.
-   `docker-compose.yml`: Defines the services, networks, and volumes for the Docker application.
-   `nginx.conf`: Configuration file for the Nginx reverse proxy.
