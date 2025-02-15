# Use the official Python image as base
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Chainlit runs on
EXPOSE 8000

# Command to run the Chainlit app
# In your Dockerfile CMD:
    CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8000"]

