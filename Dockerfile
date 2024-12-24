FROM python:3.12-bookworm as poetry
ENV POETRY_VERSION=1.3.2
RUN curl -sSL https://install.python-poetry.org | python
WORKDIR /app

FROM python:3.12-bookworm as venv
COPY --from=poetry /root/.local /root/.local
ENV PATH="/root/.local/bin:$PATH"
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN python -m venv --copies /app/venv && \
    . /app/venv/bin/activate && \
    poetry install --no-root

FROM python:3.12-slim-bookworm as prod
RUN apt -y update && apt -y install iputils-ping
WORKDIR /app
COPY --from=venv /app/venv /app/venv/
ENV PATH="/app/venv/bin:$PATH"
COPY ./run.sh /app/run.sh
COPY ./fly_fastapi_example /app/fly_fastapi_example
CMD ["uvicorn", "fly_fastapi_example.main:app", "--host", "0.0.0.0", "--port", "443"]