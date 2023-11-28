FROM python:3.11-alpine
LABEL authors="Noobgam"

ENV VIRTUAL_ENV=/monorepo/venv
COPY requirements.txt /monorepo/requirements.txt
COPY noobgam monorepo/noobgam

WORKDIR /monorepo
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install -r requirements.txt

# OPENAI_API_KEY, OPENAI_ORGANIZATION, NOOBGAM_PERSONAL_PASSWORD_SHA256 are required at runtime

EXPOSE 5000
ENTRYPOINT ["python", "-m", "noobgam.local_server.main_server"]