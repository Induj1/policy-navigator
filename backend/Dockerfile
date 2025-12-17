# Use Python 3.12 slim image
FROM python:3.12-slim

# Install system dependencies including Rust
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory early
WORKDIR /app

# Set Cargo/Rust environment variables globally
ENV CARGO_HOME=/app/.cargo \
    RUSTUP_HOME=/app/.rustup \
    PATH="/app/.cargo/bin:${PATH}" \
    CARGO_NET_GIT_FETCH_WITH_CLI=true

# Create directories with proper permissions
RUN mkdir -p /app/.cargo /app/.rustup && \
    chmod -R 777 /app/.cargo /app/.rustup

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | \
    sh -s -- -y --no-modify-path --default-toolchain stable

# Copy requirements
COPY requirements.txt .

# Install dependencies in stages to use cached wheels where possible
RUN /bin/bash -c "source /app/.cargo/env && \
    pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir fastapi==0.109.0 uvicorn[standard]==0.27.0 && \
    pip install --no-cache-dir pydantic==2.5.3 pydantic-settings==2.1.0 && \
    pip install --no-cache-dir python-dotenv==1.0.0 python-multipart==0.0.6 && \
    pip install --no-cache-dir langchain-openai==0.0.5 && \
    pip install --no-cache-dir pytesseract==0.3.10 pdf2image==1.16.3 python-docx==1.1.0 PyPDF2==3.0.1 Pillow==10.1.0 && \
    pip install --no-cache-dir deep-translator==1.11.4 langdetect==1.0.9 && \
    pip install --no-cache-dir zyndai-agent>=0.1.0"

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
