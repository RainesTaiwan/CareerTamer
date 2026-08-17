#!/usr/bin/env bash
# Attach to the always-on CareerTamer container and start the CLI.
set -e
docker compose exec -it careertamer python careertamer.py
