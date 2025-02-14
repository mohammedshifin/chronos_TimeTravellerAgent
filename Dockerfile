# Use an official Python slim image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port Chainlit will run on
EXPOSE 7860

# Start your Chainlit app ensuring it listens on all interfaces
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "7860"]
