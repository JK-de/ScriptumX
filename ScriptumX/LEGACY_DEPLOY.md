# Historical Azure / Visual Studio (PTVS) deploy artifacts
#
# These files are **not** part of the supported run path (Docker + gunicorn).
# Kept in-tree so old checkouts and Visual Studio solutions still open; do not
# use them for new deployments.
#
# | Path | What it was |
# |---|---|
# | `web.config` / `web.debug.config` | Azure App Service + IIS FastCGI for Python |
# | `ptvs_virtualenv_proxy.py` | Python Tools for Visual Studio virtualenv shim |
# | `ScriptumX.sln` / `ScriptumX.pyproj` | Visual Studio project files |
# | `.vs/` | Local VS cache (gitignored) |
#
# Current install: see Context `docs/server-install-plan.md` and root `README.md`.
