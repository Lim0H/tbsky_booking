# Base image for the build stage
FROM python:3.12-slim AS builder

# Set environment variables
ENV POETRY_VERSION=1.8.3 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    libgssapi-krb5-2 \
    libkrb5-dev \
    libsasl2-modules-gssapi-mit \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set working directory
WORKDIR /app

# Copy Poetry files for dependency installation
COPY pyproject.toml poetry.lock ./

# Install dependencies for all environments in a virtual environment
RUN poetry config virtualenvs.create true

# --- Development Stage ---
FROM builder AS dev
# Set working directory
WORKDIR /app
# Copy project files for development
COPY . .
# Install development dependencies
RUN poetry install --with dev --no-interaction --no-ansi
# Default command for development
CMD ["poetry", "run", "start"]
# --- Production Stage ---
FROM builder AS prod
# Set working directory
WORKDIR /app
# Copy project files for production
COPY . .
# Install only runtime dependencies (no dev dependencies)
RUN poetry install --no-dev --no-interaction --no-ansi --without dev
ENTRYPOINT [ "poetry", "run", "start", "run", "initialize-database" ]
# Default command for production
CMD ["poetry", "run", "start"]