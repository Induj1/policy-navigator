# Use Python 3.11 which has more pre-built wheels
FROM python:3.11-slim

# Install system dependencies including Rust
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Set Cargo environment variables
ENV CARGO_HOME=/app/.cargo \
    RUSTUP_HOME=/app/.rustup \
    PATH="/app/.cargo/bin:${PATH}"

# Create cargo directories
RUN mkdir -p /app/.cargo /app/.rustup

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | \
    sh -s -- -y --default-toolchain stable --no-modify-path

# Create a cargo wrapper script to always use our paths
RUN echo '#!/bin/bash\nCARGO_HOME=/app/.cargo RUSTUP_HOME=/app/.rustup /app/.cargo/bin/cargo "$@"' > /usr/local/bin/cargo && \
    chmod +x /usr/local/bin/cargo && \
    echo '#!/bin/bash\nCARGO_HOME=/app/.cargo RUSTUP_HOME=/app/.rustup /app/.cargo/bin/rustc "$@"' > /usr/local/bin/rustc && \
    chmod +x /usr/local/bin/rustc

# Copy requirements
COPY requirements.txt .

# Upgrade pip and install packages
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
