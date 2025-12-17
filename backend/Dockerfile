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

# Create our writable cargo directory FIRST
RUN mkdir -p /app/.cargo /app/.rustup

# Remove read-only cargo directory if it exists and symlink to our writable one
RUN rm -rf /usr/local/cargo /usr/local/rustup && \
    ln -s /app/.cargo /usr/local/cargo && \
    ln -s /app/.rustup /usr/local/rustup

# Set Cargo environment variables
ENV CARGO_HOME=/app/.cargo \
    RUSTUP_HOME=/app/.rustup \
    PATH="/app/.cargo/bin:${PATH}"

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | \
    sh -s -- -y --default-toolchain stable --no-modify-path

# Copy requirements
COPY requirements.txt .

# Upgrade pip and install packages (newer versions have pre-built wheels)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
