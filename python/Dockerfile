FROM python:3.12-alpine
LABEL authors="Noobgam"

RUN apk update && \
    apk add --no-cache gcc musl-dev libffi-dev openssl-dev cargo make bash curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /monorepo

COPY pyproject.toml poetry.lock* /monorepo/

RUN poetry config virtualenvs.create false && poetry install --only main --no-root

COPY noobgam noobgam

# OPENAI_API_KEY, OPENAI_ORGANIZATION, NOOBGAM_PERSONAL_PASSWORD_SHA256 are required at runtime

EXPOSE 5000

ENTRYPOINT ["python", "-m", "noobgam.local_server.main_server"]
