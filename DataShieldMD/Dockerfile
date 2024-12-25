# syntax=docker/dockerfile:1.4

FROM python:3.9-alpine AS builder

# Expose the application port
EXPOSE 8000

# Set the working directory
WORKDIR /DataShieldMD

# Copy the requirements file and install Python dependencies
COPY requirements.txt /DataShieldMD
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy my modified local version of anonypy into the image
COPY libs/anonypy /usr/local/lib/python3.9/site-packages/anonypy

# Copy the application source code
COPY . /DataShieldMD

# Entry point for the application
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
