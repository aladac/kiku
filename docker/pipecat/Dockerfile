FROM python:3.13-slim

RUN pip install --no-cache-dir \
    "pipecat-ai[silero,websocket]" \
    ollama \
    aiohttp \
    loguru \
    python-dotenv \
    numpy

WORKDIR /app
COPY src/ ./src/
COPY client/ ./client/

EXPOSE 8765

CMD ["python", "-m", "kiku.pipeline"]

ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1
