# Use the official Python image
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files to the container
COPY . .

# Expose the port your Flask app will run on
EXPOSE 5000

# Set environment variables (you may also handle these via an external .env file)
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
