# Stage 1: Build stage
FROM python:3.13-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc pkg-config default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


# Stage 2: Final stage
FROM python:3.13-slim

WORKDIR /app

# Create a non-root user
RUN addgroup --system app && adduser --system --group app

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder stage
COPY --from=builder /wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy application code
COPY . .

# Set ownership to the non-root user
RUN chown -R app:app /app

# Ensure entrypoint is executable
RUN chmod +x /app/entrypoint.sh

# Switch to the non-root user
USER app

# Expose the port the app runs on
EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

# Set the default command to run the application
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "screenwatcher_project.asgi:application"]
