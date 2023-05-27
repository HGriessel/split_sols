# Use a base image with Python installed
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the server script to the image
COPY udp_listener.py /app/udp_listener.py


EXPOSE 161/udp

CMD ["python", "udp_listener.py.py"]
