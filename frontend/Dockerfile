FROM node:20-slim

RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked

WORKDIR /app

COPY ./fishweb /app/

RUN npm install


