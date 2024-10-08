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
RUN poetry config virtualenvs.in-project true && \
    poetry install --only main --no-root

COPY noobgam noobgam

# Runtime Stage
FROM python:3.12-alpine
LABEL authors="Noobgam"

RUN apk add --no-cache openssl-dev libffi-dev

WORKDIR /monorepo

# Copy the project and the virtual environment from the build stage
COPY --from=build /monorepo /monorepo

# Set the virtual environment as the default Python environment
ENV PATH="/monorepo/.venv/bin:$PATH"

EXPOSE 5000

ENTRYPOINT ["python", "-m", "noobgam.local_server.main_server"]
