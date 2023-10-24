#!/bin/bash

set -x

sudo rm -rf ./src/data/git

docker-compose exec fastapi python -Xfrozen_modules=off -m debugpy --wait-for-client --listen 0.0.0.0:5678 src/startup.py