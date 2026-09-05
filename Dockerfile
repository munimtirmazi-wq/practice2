# Use a small, fixed Python runtime instead of the much larger full image.
FROM python:3.12-slim

# Python logs appear immediately and Python does not create .pyc files.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Create an unprivileged account. The API should not run as root.
RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser \
    && chown appuser:appgroup /app

# Copy and install dependencies before source code to improve build caching.
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy only the application package and give the runtime user ownership.
COPY --chown=appuser:appgroup app ./app

USER appuser

EXPOSE 8000

# ENTRYPOINT selects the executable; CMD supplies overridable defaults.
ENTRYPOINT ["python", "-m", "uvicorn"]
CMD ["app.main:app", "--host", "0.0.0.0", "--port", "8000"]
