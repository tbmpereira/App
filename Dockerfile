# Use the official lightweight Python image
# https://hub.docker.com/_/python
FROM python:3.11-slim-buster

# Set environment variables
ENV APP_HOME=/app
ENV PYTHONUNBUFFERED=True
ENV PORT=8000

# Copy local code to the container image
WORKDIR $APP_HOME

# Install production dependencies and Gunicorn
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Create a non-root user and switch to it
RUN groupadd -r app && useradd -r -g app app
COPY --chown=app:app . ./

USER app

# Run the web service on container startup using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "--log-level", "info", "--workers", "1", "--threads", "8", "--timeout", "0", "app:server"]
