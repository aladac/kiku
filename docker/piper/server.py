"""Simple Piper TTS HTTP server compatible with Pipecat's PiperHttpTTSService."""

import io
import wave

from flask import Flask, request, Response
from piper import PiperVoice
from piper.download_voices import download_voice
from pathlib import Path

app = Flask(__name__)

MODEL_DIR = Path("/data/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

voices: dict[str, PiperVoice] = {}


def get_voice(name: str) -> PiperVoice:
    if name not in voices:
        model_path = MODEL_DIR / f"{name}.onnx"
        if not model_path.exists():
            print(f"Downloading voice: {name}")
            download_voice(name, MODEL_DIR)
        print(f"Loading voice: {name}")
        voices[name] = PiperVoice.load(model_path)
    return voices[name]


@app.route("/", methods=["POST"])
def synthesize():
    data = request.json
    text = data.get("text", "")
    voice_name = data.get("voice", "en_US-ryan-high")

    if not text:
        return "No text provided", 400

    voice = get_voice(voice_name)

    buf = io.BytesIO()
    with wave.open(buf, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(voice.config.sample_rate)
        for chunk in voice.synthesize(text):
            wav.writeframes(chunk.audio_int16_bytes)

    buf.seek(0)
    return Response(buf.read(), mimetype="audio/wav")


if __name__ == "__main__":
    # Pre-load default voice
    get_voice("en_US-ryan-high")
    app.run(host="0.0.0.0", port=5000)
