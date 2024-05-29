ARG UWSGI_VERSION=2.0.25.1
ARG BUILD_COMMIT="unknown"

FROM python:3.12.3-alpine AS base

WORKDIR /app


FROM base AS build

RUN apk add --no-cache gcc g++ musl-dev libffi-dev
RUN python3 -m venv --upgrade-deps /app/venv && /app/venv/bin/pip3 install wheel

ARG UWSGI_VERSION
RUN venv/bin/pip3 install uwsgi==${UWSGI_VERSION}

COPY requirements.txt .
RUN venv/bin/pip3 install -r requirements.txt


FROM node:20.13.1-alpine AS build-assets

WORKDIR /app

RUN corepack enable

COPY package.json yarn.lock .
RUN yarn install --immutable

COPY ./assets assets
RUN yarn build


FROM base as runtime

RUN apk add --no-cache libstdc++-dev

COPY --from=build /app/venv venv
COPY --from=build-assets /app/assets/dist assets/dist

COPY munera munera
COPY manage.py .
COPY docker/entrypoint.sh docker/uwsgi.ini .

ARG BUILD_COMMIT
RUN sed -i "s/\(__commit__ = \)\(.*\)/\1\"${BUILD_COMMIT}\"/g" munera/__init__.py

ENV MUNERA_INSTANCE_DIR=/var/lib/munera
RUN mkdir -p "${MUNERA_INSTANCE_DIR}"

ENV PATH="/app/venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MUNERA_DEBUG=0

RUN ./manage.py collectstatic --no-input

ENV MUNERA_PORT=8080
EXPOSE ${MUNERA_PORT}
ENTRYPOINT ["/app/entrypoint.sh"]
