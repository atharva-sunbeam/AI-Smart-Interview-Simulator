# Voice Interview Integration

## Purpose

Enable candidates to answer interview questions using speech.

## Pipeline

Audio Upload
        ↓
SpeechToTextAgent
        ↓
Transcript Generation
        ↓
Interview Session
        ↓
Answer Evaluation

## Components

### Backend

- InterviewSession
- SpeechToTextAgent

### Frontend

- Streamlit File Uploader
- Transcript Preview

## Supported Formats

- WAV
- MP3
- M4A
- OGG

## Future Enhancements

- Real-time microphone input
- Live transcription
- Multilingual interviews