# Use Python 3.13 slim image as base
FROM python:3.13-rc-slim

# Set working directory
WORKDIR /app

# Install system dependencies and uv
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p ~/.local/bin \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv ~/.local/bin/uv /usr/local/bin/

# Copy project files
COPY pyproject.toml uv.lock README.md linkedIn.py .env ./

# Install Python dependencies using uv
RUN uv pip install --system .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "linkedIn.py"] 