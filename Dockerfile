FROM python:3.12-slim AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app

WORKDIR $APP_HOME

# Install required packages and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    python3-dev \
    musl-dev \
    net-tools \
    && rm -rf /var/lib/apt/lists/*


# Copy requirements and install in /install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# Copy source code
COPY . .

# =========================
# Final stage
# =========================
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app

# Set the working directory in the container
WORKDIR $APP_HOME

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy source code
COPY --from=builder $APP_HOME $APP_HOME

# Copy the app code into the container
COPY . /app/

# Expose port 8000 (Uvicorn will run here)
EXPOSE 8000

# Run the Uvicorn server
CMD ["uvicorn", "com.mhire.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
