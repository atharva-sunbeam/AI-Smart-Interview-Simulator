# Real-Time Audio Engine

## Purpose

The Real-Time Audio Engine provides continuous microphone
streaming support for the AI Smart Interview Simulator.

## Architecture

```
Microphone
      ↓
Audio Stream
      ↓
Voice Activity Detection
      ↓
Speech-to-Text
      ↓
Live Transcript
```

## Components

### AudioStream

Responsible for:

- Continuous microphone capture
- Audio chunk buffering
- Queue management

### RealtimeAudioAgent

Responsible for:

- Managing audio streaming
- Sending chunks to Speech-to-Text
- Maintaining live transcript
- Coordinating interviewer/candidate audio flow

## Future Enhancements

- WebRTC microphone streaming
- Voice Activity Detection (Silero VAD / WebRTC VAD)
- Streaming Faster-Whisper
- Interrupt detection
- Real-time transcript updates