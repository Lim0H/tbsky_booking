# Base image for the build stage
FROM python:3.12.7-slim AS builder
ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.8.5

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    libssl-dev \
    libffi-dev \
    libgssapi-krb5-2 \
    libkrb5-dev \
    python3-dev \
    libsasl2-modules-gssapi-mit \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip setuptools wheel

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy Poetry files for dependency installation
COPY pyproject.toml poetry.lock ./

# Install dependencies for all environments in a virtual environment
RUN poetry config virtualenvs.create false && poetry config virtualenvs.in-project true
# --- Development Stage ---
FROM builder AS dev
# Set working directory
WORKDIR /app
# Copy project files for development
COPY . .
RUN "pip install git+https://github.com/NickJLange/fast-flights.git@license"
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
RUN poetry install --without dev --no-root 
RUN pip3 install "git+https://github.com/NickJLange/fast-flights.git@license"

ENTRYPOINT [ "poetry", "run", "initialize-database" ]

# Default command for production
CMD ["poetry", "run", "start"]