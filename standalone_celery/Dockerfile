FROM python:3.11.1

ENV PYTHONUNBUFFERED 1

ARG DEV=false

# COPY pyproject.toml /app/
# COPY poetry.lock /app/
COPY . /app/

WORKDIR /app
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
