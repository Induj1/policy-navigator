# Use Python 3.12 slim image
FROM python:3.12-slim

# Install system dependencies including Rust
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory early
WORKDIR /app

# Set Cargo/Rust environment variables to writable locations
ENV CARGO_HOME=/app/.cargo
ENV RUSTUP_HOME=/app/.rustup
ENV PATH="/app/.cargo/bin:${PATH}"

# Create directories with proper permissions
RUN mkdir -p /app/.cargo /app/.rustup && \
    chmod -R 777 /app/.cargo /app/.rustup

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | \
    sh -s -- -y --no-modify-path --default-toolchain stable

# Verify Rust installation
RUN . /app/.cargo/env && rustc --version && cargo --version

# Copy requirements first for better caching
COPY requirements.txt .

# Create pip.conf to disable build isolation and use our Cargo settings
RUN mkdir -p /root/.config/pip && \
    echo "[global]" > /root/.config/pip/pip.conf && \
    echo "no-build-isolation = True" >> /root/.config/pip/pip.conf

# Install build tools first
RUN . /app/.cargo/env && \
    pip install --no-cache-dir --upgrade pip setuptools wheel maturin

# Install Python dependencies with Cargo environment, no build isolation
RUN . /app/.cargo/env && \
    pip install --no-cache-dir --no-build-isolation -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
