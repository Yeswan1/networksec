FROM python:3.10-slim

WORKDIR /app

# Copy only requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install AWS CLI
RUN pip install --no-cache-dir awscli

# Copy rest of the application
COPY . .

# Run the application
CMD ["python3", "app.py"]