# Use Python 3.12 slim image
FROM python:3.12-slim

# Set Cargo home to writable location BEFORE installing anything
ENV CARGO_HOME="/tmp/cargo"
ENV RUSTUP_HOME="/tmp/rustup"
ENV PATH="/tmp/cargo/bin:${PATH}"

# Install system dependencies including Rust
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create cargo directories with proper permissions
RUN mkdir -p /tmp/cargo /tmp/rustup && \
    chmod -R 777 /tmp/cargo /tmp/rustup

# Install Rust with custom home
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
