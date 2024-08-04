# Using python image as the base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY . /app

# Install the required python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose to port 5000 for the Flask app
EXPOSE 5000

# Set the environment variables for the Flask app
ENV FLASK_APP=app.py

# Start the flask app and run as container
CMD ["flask", "run", "--host=0.0.0.0"]
