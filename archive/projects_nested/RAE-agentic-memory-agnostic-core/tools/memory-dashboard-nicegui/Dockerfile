FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (8501 is what we set in ui.run)
EXPOSE 8501

# Run NiceGUI app
CMD ["python", "main.py"]
