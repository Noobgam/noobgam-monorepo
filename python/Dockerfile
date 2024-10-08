# Build Stage
FROM python:3.12-alpine AS build
LABEL authors="Noobgam"

RUN apk update && \
    apk add --no-cache gcc musl-dev libffi-dev openssl-dev cargo make bash curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /monorepo

COPY pyproject.toml poetry.lock* /monorepo/

# Configure Poetry to create the virtual environment inside the project directory
# --no-root to keep venv stable
RUN poetry config virtualenvs.in-project true && \
    poetry install --only main --no-root

COPY noobgam noobgam

# Runtime Stage
FROM python:3.12-alpine
LABEL authors="Noobgam"

RUN apk add --no-cache openssl-dev libffi-dev

WORKDIR /monorepo

# copy venv separately to separate layers
COPY --from=build /monorepo/.venv /monorepo/.venv

COPY --from=build /monorepo/noobgam /monorepo/noobgam

ENV PATH="/monorepo/.venv/bin:$PATH"

EXPOSE 5000

ENTRYPOINT ["python", "-m", "noobgam.local_server.main_server"]
