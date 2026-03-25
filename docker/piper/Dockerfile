FROM python:3.12-slim

RUN pip install --no-cache-dir piper-tts flask

WORKDIR /app
COPY docker/piper/server.py .

EXPOSE 5000

CMD ["python", "server.py"]

ENV PYTHONUNBUFFERED=1
