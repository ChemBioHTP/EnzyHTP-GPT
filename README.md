# EnzyHTP-GPT

A web application that serves as a conversational interface to EnzyHTP's workflows, leveraging Large Language Models (LLMs) to streamline enzyme engineering.

## Quick Start

The fastest way to get EnzyHTP-GPT running locally is with Docker Compose.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ChemBioHTP/EnzyHTP-GPT.git
    cd EnzyHTP-GPT
    ```

2.  **Set up environment variables:**
    ```bash
    cp .env.example .env
    # Modify .env as needed
    ```

3.  **Build and run the application:**
    ```bash
    docker compose up -d --build
    ```

The application will be available at `http://localhost` (or the host IP for your Docker machine).

## Documentation

For detailed information about the project architecture, development setup, deployment, and more, please refer to our comprehensive documentation in the `/docs` directory.

-   **[Architecture](./docs/01_architecture.md)**: A high-level overview of the system architecture and technology stack.
-   **[Backend Setup](./docs/02_backend_setup.md)**: Instructions for setting up and running the Flask backend.
-   **[Frontend Setup](./docs/03_frontend_setup.md)**: Instructions for setting up and running the Vue.js frontend.
-   **[API Reference](./docs/04_api_reference.md)**: A guide to the backend REST API.
-   **[AI Agent Workflow](./docs/05_agent_workflow.md)**: An explanation of the LLM-powered agent workflow.
-   **[Deployment Guide](./docs/06_deployment.md)**: Detailed instructions for deploying the application in a production environment.
-   **[Contributing](./CONTRIBUTING.md)**: Guidelines for contributing to the project.