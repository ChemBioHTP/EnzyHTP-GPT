# API Reference

The EnzyHTP-GPT backend exposes a RESTful API for managing users, experiments, and other resources. The base URL for all API endpoints is `/api`.

**Note:** For detailed information on request and response formats, please refer to the `docs/20250419_Web APIs.postman_collection.json` file. It is recommended to import this collection into Postman for easy testing and exploration. Some legacy examples in that collection may still use `thread` wording; backend runtime is now session-compatible (`thread` + `conversation`).

For improved developer experience, we plan to integrate a tool like `flasgger` to provide interactive Swagger/OpenAPI documentation in the future.

## Authentication (`/api/auth`)

-   `POST /register`: Register a new user.
-   `POST /login`: Log in a user.
-   `POST /logout`: Log out the current user.
-   `GET /profile`: Get the current user's profile.
-   `PUT /profile`: Update the current user's profile.
-   `PUT /password/change`: Change the current user's password.
-   `POST /password/reset/generate`: Generate a password reset verification code.
-   `PUT /password/reset`: Reset the password using a verification code.
-   `GET /oauth/<oauth_vendor>/login`: Initiate OAuth login with a specific vendor (e.g., `google`).
-   `GET /oauth/<oauth_vendor>/login/callback`: Callback URL for OAuth login.

## Experiments (`/api/experiment`)

-   `GET /`: Get a list of the current user's experiments.
-   `POST /`: Create a new experiment.
-   `DELETE /`: Delete an experiment.
-   `GET /<experiment_id>`: Get the details of a specific experiment.
-   `PUT /<experiment_id>`: Update an experiment's information.
-   `PATCH /<experiment_id>`: Update the status and progress of an experiment.
-   `GET /<experiment_id>/result`: Get the analysis results of an experiment.
-   `POST /<experiment_id>/result`: Post new analysis results to an experiment.
-   `GET /<experiment_id>/assistants`: Get workflow chat messages for the current OpenAI session.
-   `POST /<experiment_id>/assistants`: Interact with the current workflow assistant stage.
-   `PUT /<experiment_id>/assistants`: Toggle to the next assistant in the workflow.
-   `DELETE /<experiment_id>/assistants`: Clear workflow session context.
-   `GET /<experiment_id>/downloadable`: Download a zip file of all downloadable files for an experiment.
-   `GET /<experiment_id>/downloadable/<filepath>`: Download a specific file from an experiment.
-   `GET /<experiment_id>/pdb_file`: Download the PDB file for an experiment.
-   `POST /<experiment_id>/pdb_file`: Upload a PDB file for an experiment.
-   `GET /<experiment_id>/mutations`: Get the mutation space for an experiment.
-   `POST /<experiment_id>/mutations`: Generate a mutation pattern from natural language.
-   `PUT /<experiment_id>/mutations`: Update the mutation space for an experiment.
-   `GET /<experiment_id>/slurm`: Get SLURM job information for an experiment.
-   `POST /<experiment_id>/slurm`: Submit a SLURM job for an experiment.
-   `DELETE /<experiment_id>/slurm`: Delete a SLURM job for an experiment.
-   `GET /<experiment_id>/deploy`: Download a deployment package for running simulations on a separate SLURM cluster.

## Assistant Workflow Runtime and Compatibility

`/api/experiment/<experiment_id>/assistants` keeps the same route path, but the backend runtime is configurable:

- `OPENAI_RUNTIME=responses` (recommended): Responses + Conversations runtime.
- `OPENAI_RUNTIME=assistants`: legacy Assistants + Threads runtime.

### Session Fields During Migration

To support smooth migration and rollback, experiment records may contain both session tracks:

- Legacy track: `current_thread_id`, `thread_id_list`
- New track: `current_conversation_id`, `conversation_id_list`

When runtime is `responses`, the backend prioritizes conversation fields and local `chat_messages` metadata.

### `chat_messages` Schema Notes

`chat_messages` is the canonical display/audit source in current backend logic.  
Each message may include:

- `role`: `user` or `assistant`
- `text_value`: message text
- `assistant_type` (optional): workflow stage index
- `session_id` (optional): related conversation/thread ID

## SLURM API Tokens

The application interacts with the Vanderbilt ACCRE SLURM cluster via its API. To authenticate, you need to obtain a token from `https://ssam.accre.vanderbilt.edu/`.

-   **Username:** `yanglab_enzyhtp_app`
-   **Password:** `defuse/graffiti/doorbell/jubilance/managing/coastland`

Once logged in, create a token in the `Token` tab and use the following API endpoints to manage it in the application:

-   `POST /api/experiment/slurm/token`: Update the `token` and `refresh_token`.
-   `PUT /api/experiment/slurm/token`: Refresh the token.

The backend automatically refreshes the SLURM token daily via a scheduled task. Administrators typically only need to seed the initial `token` and `refresh_token` once using the POST endpoint.
