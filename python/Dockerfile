FROM python:3.12-alpine
LABEL authors="Noobgam"

ENV VIRTUAL_ENV=/monorepo/venv
COPY requirements.txt /monorepo/requirements.txt

WORKDIR /monorepo
RUN pip install -r requirements.txt

COPY noobgam noobgam

# OPENAI_API_KEY, OPENAI_ORGANIZATION, NOOBGAM_PERSONAL_PASSWORD_SHA256 are required at runtime

EXPOSE 5000
ENTRYPOINT ["python", "-m", "noobgam.local_server.main_server"]