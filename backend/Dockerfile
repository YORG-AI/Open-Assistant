# syntax = docker/dockerfile:experimental
FROM python:3.10-slim

WORKDIR /app

RUN cp /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list.d/debian.sources.bak
COPY sources_zh.sources /etc/apt/sources.list

# Install system-level dependencies
# use cache to speed up apt-get install:
# https://stackoverflow.com/questions/66808788/docker-can-you-cache-apt-get-package-installs
RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean \
    && apt-get update && apt-get upgrade -y && apt-get install -y \
    git \
    dos2unix \
    tree \
    python3-dev \
    gcc


# Install Python dependencies
COPY requirements.txt /app
# Use cache to speed up pip install:
# https://stackoverflow.com/questions/58018300/using-a-pip-cache-directory-in-docker-builds
RUN --mount=type=cache,target=/root/.cache/pip pip install -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Install jupyter nbextensions
RUN jupyter contrib nbextension install --user

# Copy the project files
COPY ./ /app

# Load kernel spec
COPY kernel.json /usr/local/share/jupyter/kernels/ykernel/

# Expose 8000 port from the docker image.
EXPOSE 8000

# Make the entrypoint script executable
RUN dos2unix ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

ENV PYTHONPATH=.
