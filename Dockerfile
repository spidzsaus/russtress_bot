FROM python:3.12.1-alpine3.19

# Preparing the requirements for installing
FROM python:latest as requirements-stage

WORKDIR /tmp

RUN python3 -m pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN python3 -m poetry export -f requirements.txt --output requirements.txt --without-hashes

# Installing the requirements
FROM python:latest

WORKDIR /bot

COPY . /bot

# Installing the dependencies
COPY --from=requirements-stage /tmp/requirements.txt /bot/requirements.txt

RUN python3 -m pip install --no-cache-dir --upgrade -r /bot/requirements.txt

# Running the app
CMD ["sh", "-c", "python3 -m bot"]