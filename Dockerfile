
# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME

COPY . ./

# Install production dependencies. The spaCy model used by Presidio
# (en_core_web_lg) is pinned in requirements.txt, so no separate
# `spacy download` step is needed.
RUN pip install --no-cache-dir -r requirements.txt


# Run the web service on container startup with uvicorn.
# Listens on $PORT when provided (e.g. Cloud Run); defaults to 7860 for
# Hugging Face Spaces.
CMD uvicorn app.main.main:app --host 0.0.0.0 --port ${PORT:-7860}
