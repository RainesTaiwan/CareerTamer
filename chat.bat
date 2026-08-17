@echo off
REM Attach to the always-on CareerTamer container and start the CLI.
docker compose exec -it careertamer python careertamer.py
