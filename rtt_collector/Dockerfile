FROM python:3.9-slim

WORKDIR /app

COPY ./udp_listener.py /app/udp_listener.py

EXPOSE 161/udp

CMD ["python", "udp_listener.py"]
