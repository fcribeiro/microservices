# Use an official Python runtime as a parent image
FROM python:2.7-alpine


RUN apk add --update \
    python-dev \
    build-base \
  && rm -rf /var/cache/apk/*

# Set the working directory to /app
WORKDIR /app

# Add requirement first to prevent rebuild of this layer when only code is changed
ADD requirements.txt /app/
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
ADD . /app/

EXPOSE 8080

# Define environment variable
ENV USERSADDRESS localhost:5000
ENV SONGSADDRESS localhost:5001
ENV PLAYLISTSADDRESS localhost:5002
ENV PYTHONPATH /app/

# Run app.py when the container launches
CMD ["python", "business/Business.py"]
