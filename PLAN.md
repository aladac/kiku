# Kiku - AI IVR Chatbot

## Overview

Self-hosted AI-powered IVR chatbot running entirely on junkpile. Call a phone number, talk to an AI. No cloud dependencies.

## Stack

| Layer | Tool | Host | Notes |
|-------|------|------|-------|
| SIP Trunk | VoIP.ms | external | DID number, SIP registration |
| PBX | Asterisk (Docker) | junkpile | SIP termination, AudioSocket |
| Voice Framework | Pipecat (Docker) | junkpile | Pipeline orchestration |
| STT | faster-whisper | junkpile | GPU-accelerated |
| LLM | Ollama (llama3.2) | junkpile | Already running |
| TTS | Piper | junkpile | Docker container |

## Architecture

```
Phone -> VoIP.ms SIP -> Asterisk -> AudioSocket -> Pipecat
                                                     |
                                               faster-whisper (GPU)
                                                     |
                                                   Ollama
                                                     |
                                                   Piper
                                                     |
                                               AudioSocket -> Caller
```

All containers on junkpile, networked via docker compose.

## Phases

### Phase 1 - Voice Pipeline on Junkpile

Deploy Pipecat + faster-whisper + Piper as Docker containers on junkpile. Test via WebSocket from browser.

- [ ] Docker compose with all services
- [ ] faster-whisper container (GPU, whisper API)
- [ ] Piper TTS container (HTTP API)
- [ ] Pipecat container with pipeline app
- [ ] WebSocket transport + simple HTML test client
- [ ] Define system prompt for chatbot personality
- [ ] Test end-to-end voice conversation via browser

### Phase 2 - Asterisk + SIP

Add Asterisk container, replace WebSocket with AudioSocket transport.

- [ ] Asterisk container in compose
- [ ] VoIP.ms account + DID number
- [ ] SIP trunk config (pjsip.conf)
- [ ] AudioSocket dialplan (extensions.conf)
- [ ] Switch Pipecat to AudioSocket transport
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

## Project Structure

```
kiku/
  docker/
    pipecat/
      Dockerfile
    piper/
      Dockerfile
    faster-whisper/
      Dockerfile
    asterisk/          # Phase 2
      Dockerfile
      pjsip.conf
      extensions.conf
  src/
    kiku/
      __init__.py
      pipeline.py      # Pipecat pipeline
      config.py         # Settings
      prompts.py        # System prompts
  client/
    index.html          # Browser test client
  docker-compose.yml
  pyproject.toml
  README.md
  PLAN.md
```

## Deployment

All on junkpile via SSH. Docker compose up from the repo.

```bash
ssh junkpile "cd ~/kiku && docker compose up -d"
```

## Key Decisions

- **All on junkpile**: Single deployment target, GPU available for STT, Ollama already there
- **Pipecat over LiveKit**: More control over telephony, Asterisk AudioSocket is battle-tested
- **faster-whisper over Whisper**: 4x faster inference, lower VRAM
- **Piper HTTP over local**: Runs as separate container, reusable across services
- **Ollama over direct model loading**: Already running, model management handled
- **WebSocket for Phase 1**: Browser-testable without phone setup, easy to swap for AudioSocket
