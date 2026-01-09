# ==========================================
# API STAGE (Python + FastAPI)
# ==========================================
FROM python:3.11-slim as api-base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# Prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Builder stage to install dependencies
FROM api-base as api-builder
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    build-essential

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# workdir for dependencies
WORKDIR $PYSETUP_PATH
COPY api/pyproject.toml api/poetry.lock ./

# Install runtime dependencies (no dev)
RUN poetry install --no-dev --no-root # --no-root because we copy code later

# Final Run Stage
FROM api-base as api
WORKDIR /app

# Copy venv from builder
COPY --from=api-builder $VENV_PATH $VENV_PATH

# Copy application code
COPY api/ ./api/

# Create a non-root user
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 appuser
USER appuser

# Expose port
EXPOSE 8000

# Command
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]


# ==========================================
# WEB STAGE (Node.js + Next.js) - Placeholder
# ==========================================
# FROM node:20-slim as web-base
# ...
