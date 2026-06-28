# Speech-to-Text Interview Engine

## Purpose

The Speech-to-Text Engine allows candidates to answer interview questions using voice instead of typing.

The engine converts spoken responses into text, which can then be evaluated by the Answer Evaluation Agent.

---

# Architecture

```text
Candidate Audio
        ↓
Audio Validation
        ↓
Speech Recognition
        ↓
Transcript Cleaning
        ↓
Interview Evaluation
```

---

# Technology Used

Framework:

```text
faster-whisper
```

Model:

```text
Whisper Base Model
```

Reasons:

* Fast inference
* High accuracy
* Open source
* Supports multilingual speech recognition
* Production ready

---

# Whisper Architecture

Whisper is a transformer-based speech recognition model developed by OpenAI.

Pipeline:

```text
Audio Signal
        ↓
Feature Extraction
        ↓
Transformer Encoder
        ↓
Transformer Decoder
        ↓
Text Transcript
```

---

# Speech Recognition Pipeline

```text
Audio Upload
        ↓
Format Validation
        ↓
Whisper Model
        ↓
Transcription
        ↓
Text Cleaning
        ↓
Structured Output
```

Example Output:

```python
{
    "transcript":
        "Decorators modify the behaviour of functions.",

    "language":
        "en",

    "duration":
        18.3
}
```

---

# Supported Audio Formats

* WAV
* MP3
* M4A
* OGG

---

# Benefits

* Hands-free interview experience
* More realistic interview simulation
* Improved accessibility
* Supports spoken assessments

---

# Future Enhancements

## Multilingual Interviews

Future versions will support:

* English
* Hindi
* Marathi
* French
* German

---

## Real-Time Streaming

Current implementation:

```text
Upload Audio → Transcribe
```

Future implementation:

```text
Live Microphone
        ↓
Streaming Transcription
```

---

## Speaker Emotion Detection

Future versions may analyze:

* Confidence
* Hesitation
* Fluency
* Speaking pace

to enhance interview evaluation.
