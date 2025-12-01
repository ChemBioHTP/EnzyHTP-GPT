# Frontend Setup (web-client)

This document provides instructions for setting up and running the Vue.js frontend for EnzyHTP-GPT.

## 1. Environment Setup

1.  **Node.js**: Ensure you have Node.js v18.x or higher installed.
2.  **Dependencies**: Install the frontend dependencies using npm:
    ```bash
    cd web-client
    npm install
    ```

## 2. Running the Frontend

### Development Mode

To run the frontend in development mode with hot-reloading:

```bash
cd web-client
npm run dev
```

The application will be available at `http://localhost:3000`.

### Production Build

To build the frontend for production:

```bash
cd web-client
npm run build
```

The production-ready static files will be generated in the `web-client/dist` directory. These files are then served by the Nginx container in the production deployment.

## 3. Project Structure

-   `public/`: Static assets that are copied directly to the build output.
-   `src/`: The main source code for the Vue application.
    -   `api/`: Logic for making API calls to the backend.
    -   `assets/`: Static assets like images and stylesheets.
    -   `components/`: Reusable Vue components.
    -   `views/`: Application pages/routes.
    -   `router/`: Frontend routing configuration.
    -   `stores/`: Pinia state management stores.
    -   `main.js`: The entry point of the application.
-   `vite.config.js`: Configuration for the Vite build tool.
