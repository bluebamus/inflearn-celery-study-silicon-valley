FROM python:3.11.1

ENV PYTHONUNBUFFERED 1

ARG DEV=false

COPY pyproject.toml /app/
COPY ./app /app/

WORKDIR /app
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

# RUN if [ $DEV = true ]; then poetry install --no-dev
# RUN if [ $DEV = true ]; then poetry install --E redis

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app.wsgi"]