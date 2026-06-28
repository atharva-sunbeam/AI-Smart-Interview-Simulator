# Text-to-Speech Design

## Purpose

The Text-to-Speech Agent converts interview questions into spoken audio so that the interview experience is more natural and interactive.

---

# Architecture

Interview Question

↓

Text Validation

↓

gTTS Voice Generation

↓

MP3 File

↓

Audio Playback

---

# Workflow

1. Receive interview question.
2. Validate text.
3. Generate speech using gTTS.
4. Save audio as MP3.
5. Play audio using the operating system.

---

# Output

Example:

generated_audio/interview_question.mp3

---

# Advantages

- Natural interview experience.
- Improves accessibility.
- Platform independent.
- Easy integration with Streamlit.

---

# Current Technology

gTTS (Google Text-to-Speech)

Benefits:

- Lightweight
- Easy to integrate
- Good English pronunciation

Limitations:

- Internet connection required
- Limited voice customization

---

# Future Enhancements

Replace gTTS with:

- Coqui TTS
- XTTS
- ElevenLabs
- Azure Neural TTS
- Google Cloud Text-to-Speech

These engines provide:

- Neural voices
- Multiple speakers
- Faster inference
- Offline deployment (Coqui)
- Emotion-aware speech

---

# Future Pipeline

Interview Question

↓

LLM Generated Question

↓

Neural Voice Generation

↓

Candidate Hears Question

↓

Candidate Responds

↓

Speech-to-Text (Future)

↓

Answer Evaluation