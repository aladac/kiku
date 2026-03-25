import os


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

WHISPER_BASE_URL = os.getenv("WHISPER_BASE_URL", "http://localhost:8100")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "Systran/faster-distil-whisper-large-v3")

PIPER_BASE_URL = os.getenv("PIPER_BASE_URL", "http://localhost:5000")
PIPER_VOICE = os.getenv("PIPER_VOICE", "en_US-ryan-high")

WS_HOST = os.getenv("WS_HOST", "0.0.0.0")
WS_PORT = int(os.getenv("WS_PORT", "8765"))
