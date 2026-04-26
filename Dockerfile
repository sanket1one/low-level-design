FROM python:3.11-alpine3.22@sha256:a4fc589b32e824f3f02ed9d7e7be19518aa47e105b80416336af9f202275a489

# Set working directory
WORKDIR /app

# Install system dependencies if needed
RUN apk add --no-cache \
    git \
    bash

# Copy requirements file if it exists
COPY requirements.txt* ./

# Install Python dependencies if requirements.txt exists
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Default command - keep container running for interactive use
CMD ["/bin/bash"]
