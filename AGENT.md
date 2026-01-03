# EnzyHTP-GPT at a glance
- Full-stack app for conversational enzyme engineering. Backend is Flask (`flask-server/`) with OpenAI-driven agents and SLURM integration; main frontend is Vue 3/Vite (`web-client/`). A legacy React app still lives under `src/`.
- Key docs live in `docs/`: architecture (01), backend setup (02), frontend setup (03), API reference (04 + Postman collection), agent workflow (05), deployment (06). `CONTRIBUTING.md` covers contribution flow.
- Deploy stack via `docker-compose.yml` (services: `mongo`, `flask`, `web-builder` for Vite builds, `nginx` serving `web-client/dist`). Nginx config is `nginx.conf`.
- Configuration template: `.env.example` (image tag/ports plus host paths for Mongo data, SSL, file store, nginx logs, EnzyHTP/AMBER). Default ports: Mongo 27017, Flask exposed on `${FLASK_HOST_PORT:-12306}` -> 8000 in-container, Nginx on 80/443.

## How to run
- **Docker (preferred)**: `cp .env.example .env`, adjust host paths (`MONGO_DATA_DIR`, `SSL_DIR`, `FILES_DIR`, `NGINX_LOG_DIR`, `ENZYHTP_BIN`, `AMBER22_DIR`, optional `MONGO_URI`). Then `docker compose --env-file ./.env up -d --build`. Rebuild frontend: `docker compose exec web-builder bash -lc "npm run build"`. Logs: `docker compose logs -f flask` etc.
- **Backend dev (Flask)**: `conda env create -f flask-server/environment.yml`, configure EnzyHTP path with `bash flask-server/enzyhtp_env_config.sh --path ~/bin/EnzyHTP`, ensure Mongo reachable (`MONGO_URI` defaults to `mongodb://localhost:27017/enzyhtp_gpt`), then `cd flask-server && flask run` (serves on 5000 by default). File storage defaults to `flask-server/static/experiments` and `static/scratch` (set via env).
- **Frontend dev (Vue)**: `cd web-client && npm install && npm run dev` (Node 18+, served on 3000). Axios uses relative `baseURL`, so proxy/serve through same origin or dev proxy as needed. Production build: `npm run build` -> `web-client/dist`.
- **Legacy React app**: root `package.json` and `src/` are an older CRA UI; not wired into Docker. `npm run start-frontend` (CRA dev server) if you need to inspect it; `node_server.js` serves the CRA `build/` folder.

## Backend specifics
- Entry point: `flask-server/server.py` registers blueprints `auth` and `experiment`, sets Mongo, JWT, mail, APScheduler (daily SLURM token refresh via `services/accre_slurm_service.py`).
- Config: `flask-server/config.py` reads env (MONGO_URI, SECRET_KEY, etc.) but ships placeholder secrets (JWT/mail/OpenAI defaults) that must be overridden in real deployments. SSL context expects certs in `flask-server/certs/server/`.
- AI agents: `flask-server/experiment/agents.py` implements Question Analyzer -> Metrics Planner -> Mutant Planner -> Result Explainer; prompts in `flask-server/prompts/`. Tool functions live in `experiment/agent_tool_functions.py`; metrics mapping in `experiment/analysis.py`. OpenAI helper is `services/openai_service.py` (set a real API key; defaults are dummy).
- Experiments: Mongo models in `experiment/models.py` (stores mutation patterns, metrics, SLURM job info, files). SLURM submission via `services/accre_slurm_service.py` with job scripts/templates under `flask-server/templates/slurm_run` and `slurm_deploy`.
- Auth: Mongo-backed login/JWT (`auth/`), OAuth stubs expect client configs in `flask-server/oauth_clients/`. Password reset email template at `flask-server/templates/password_reset_email.html`.

## API surface
- Base path `/api`; auth routes under `/api/auth`, experiment routes under `/api/experiment` (CRUD, assistants, mutations, SLURM, downloads). See `docs/04_api_reference.md` and Postman collection `docs/20250419_Web APIs.postman_collection.json` for payloads. SLURM tokens managed via `/api/experiment/slurm/token` endpoints; tokens stored in Mongo (`tokens` collection).

## Testing/benchmarks
- No top-level automated test suite. Agent benchmarking and unit tests live in `flask-server/agent_benchmark/tests` (require OpenAI creds and EnzyHTP deps). No lint/format tooling configured beyond standard language defaults.

## Gotchas & tips
- Replace hardcoded secrets in `config.py` and `services/openai_service.py`; set real OpenAI keys via env/DB before exercising agents.
- Ensure required host dirs from `.env` exist and are writable; Docker build expects to write `web-client/dist` from inside the `web-builder` container.
- Frontend axios sends `Authorization` header from `pinia-plugin-persistedstate` token cache and uses `Content-Type: application/x-www-form-urlencoded` by default; file uploads use multipart on PUT.
- EnzyHTP dependency: backend assumes EnzyHTP (develop branch) is available and configured; `enzyhtp_env_config.sh` or `docker_env_config.sh` help wire it into the conda env/container.
- Use "init_mutexa" alias to activate the conda environment for EnzyHTP-GPT development.

