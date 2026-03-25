# Kiku - AI IVR Chatbot

## Overview

Self-hosted AI-powered IVR chatbot. Call a phone number, talk to an AI. All components run locally with no cloud AI dependencies.

## Stack

| Layer | Tool | Notes |
|-------|------|-------|
| SIP Trunk | VoIP.ms | DID number, SIP registration |
| PBX | Asterisk (Docker) | SIP termination, AudioSocket |
| Voice Framework | Pipecat | Pipeline orchestration |
| STT | faster-whisper | GPU-accelerated on junkpile |
| LLM | Ollama (llama3.2) | Already running on junkpile |
| TTS | Piper | Already running via PSN |

## Architecture

```
Phone -> VoIP.ms SIP -> Asterisk -> AudioSocket -> Pipecat
                                                     |
                                               faster-whisper
                                                     |
                                                   Ollama
                                                     |
                                                   Piper
                                                     |
                                               AudioSocket -> Caller
```

## Phases

### Phase 1 - Local Voice Pipeline

Get Pipecat wired to Ollama + Piper + faster-whisper without telephony. Test with microphone input/speaker output.

- [ ] Python project setup (uv, pyproject.toml)
- [ ] Install pipecat with ollama, piper, faster-whisper extras
- [ ] Deploy faster-whisper on junkpile (Docker)
- [ ] Write Pipecat pipeline: mic -> STT -> LLM -> TTS -> speaker
- [ ] Define system prompt for chatbot personality
- [ ] Test end-to-end voice conversation locally

### Phase 2 - Asterisk + SIP

Replace mic/speaker with phone audio via Asterisk AudioSocket.

- [ ] Asterisk Docker container (docker-compose)
- [ ] VoIP.ms account + DID number
- [ ] SIP trunk config (pjsip.conf)
- [ ] AudioSocket dialplan (extensions.conf)
- [ ] Connect Pipecat AudioSocket transport to Asterisk
- [ ] Test inbound call end-to-end

### Phase 3 - Polish

- [ ] Greeting prompt on call pickup
- [ ] Silence/timeout handling
- [ ] Graceful hangup detection
- [ ] Conversation logging
- [ ] Basic error recovery (model timeout, STT failure)

### Phase 4 - Optional Enhancements

- [ ] Multiple personalities via system prompt selection (DTMF menu)
- [ ] Call recording
- [ ] Voicemail fallback if services are down
- [ ] Metrics / call duration tracking
- [ ] Web UI for conversation history

## Infrastructure

### junkpile (remote GPU host)

- faster-whisper container
- Ollama (already running)

### local

- Asterisk container
- Pipecat app
- Piper TTS (already running)

## Project Structure

```
kiku/
  docker/
    asterisk/
      Dockerfile
      pjsip.conf
      extensions.conf
    faster-whisper/
      Dockerfile
  src/
    kiku/
      __init__.py
      pipeline.py      # Pipecat pipeline
      config.py         # Settings
      prompts.py        # System prompts
  docker-compose.yml
  pyproject.toml
  README.md
  PLAN.md
```

## Key Decisions

- **Pipecat over LiveKit**: More control over telephony, Asterisk AudioSocket is battle-tested
- **faster-whisper over Whisper**: 4x faster inference, lower VRAM
- **Piper over Coqui**: Already deployed, low latency, good quality
- **Ollama over direct model loading**: Already running, model management handled
