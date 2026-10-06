# ScriptumX

Web-based Script Editor and Production Planner.

## Run with Docker

```bash
cd ScriptumX
docker compose up --build
```

Open http://localhost:8000/ — local demo admin `admin` / `admin` (dev compose only).

**Production:** use `docker-compose.prod.yml` + `.env.prod` (see Context `docs/server-install-plan.md`). Do not expose the default admin on a shared host.

Legacy Azure / Visual Studio files (`web.config`, PTVS) are historical — see `ScriptumX/LEGACY_DEPLOY.md`.
