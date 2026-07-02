"""
Real-Time Audio Agent

Purpose:
Manage continuous microphone streaming,
voice activity detection, and live
speech transcription.

Pipeline:

Microphone
      ↓
Audio Stream
      ↓
Voice Activity Detection
      ↓
Save Temporary WAV
      ↓
Speech-to-Text
      ↓
Live Transcript
"""

import sys
import tempfile
import threading
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from agents.speech_to_text_agent import (
    SpeechToTextAgent,
)

from utils.audio_stream import (
    AudioStream,
)

from utils.voice_activity_detector import (
    VoiceActivityDetector,
)


class RealtimeAudioAgent:
    """
    Handles continuous microphone streaming
    and live transcription.
    """

    def __init__(self):

        self.audio_stream = (
            AudioStream()
        )

        self.vad = (
            VoiceActivityDetector()
        )

        self.stt_agent = (
            SpeechToTextAgent()
        )

        self.streaming = False

        self.interviewer_speaking = False

        self.transcript = ""

        #
        # Sprint 24 additions
        #

        self.worker_thread = None

        self.lock = threading.Lock()

    # --------------------------------------------------

    def start_stream(
        self,
    ):
        """
        Start microphone capture and launch
        background processing thread.
        """

        if self.streaming:
            return

        self.audio_stream.start()

        self.streaming = True

        self.worker_thread = threading.Thread(
            target=self.process_stream,
            daemon=True,
        )

        self.worker_thread.start()

    # --------------------------------------------------

    def stop_stream(
        self,
    ):
        """
        Stop microphone capture.
        """

        if not self.streaming:
            return

        self.streaming = False

        self.audio_stream.stop()

        if self.worker_thread:

            self.worker_thread.join(
                timeout=2
            )

            self.worker_thread = None

    # --------------------------------------------------

    def set_interviewer_state(
        self,
        speaking: bool,
    ):
        """
        Disable microphone while AI speaks.
        """

        self.interviewer_speaking = (
            speaking
        )

    # --------------------------------------------------

    def get_audio_chunk(
        self,
    ):
        """
        Read next microphone chunk.
        """

        return (
            self.audio_stream.read_chunk()
        )

    # --------------------------------------------------

    def process_next_chunk(
        self,
    ):
        """
        Process one microphone chunk.
        """

        #
        # Don't record while interviewer speaks.
        #

        if self.interviewer_speaking:

            return None

        chunk = (
            self.get_audio_chunk()
        )

        if chunk is None:

            return None

        #
        # Ignore silence.
        #

        if not self.vad.is_speech(
            chunk
        ):

            return None

        #
        # Save temporary wav.
        #

        with tempfile.NamedTemporaryFile(

            suffix=".wav",

            delete=False,

        ) as temp_audio:

            temp_path = (
                temp_audio.name
            )

        self.audio_stream.save_chunk(

            chunk,

            temp_path,

        )

        try:

            result = (

                self.stt_agent
                .transcribe_audio(
                    temp_path
                )

            )

            text = (

                result.get(
                    "transcript",
                    "",
                )

                .strip()

            )

            if text:

                with self.lock:

                    if self.transcript:

                        self.transcript += " "

                    self.transcript += text

            return text

        finally:

            Path(
                temp_path
            ).unlink(
                missing_ok=True
            )

    # --------------------------------------------------

    def process_stream(
        self,
        iterations=None,
    ):
        """
        Continuously process microphone.
        """

        processed = 0

        while self.streaming:

            self.process_next_chunk()

            processed += 1

            if (

                iterations
                is not None

                and

                processed
                >= iterations

            ):

                break

    # --------------------------------------------------

    def get_live_transcript(
        self,
    ):
        """
        Return transcript.
        """

        with self.lock:

            return (
                self.transcript
            )

    # --------------------------------------------------

    #
    # Dev A Integration API
    #

    def get_transcript(
        self,
    ):
        """
        Alias used by frontend.
        """

        return (
            self.get_live_transcript()
        )

    # --------------------------------------------------

    def clear_transcript(
        self,
    ):
        """
        Reset transcript.
        """

        with self.lock:

            self.transcript = ""

    # --------------------------------------------------

    def is_streaming(
        self,
    ):
        """
        Backward-compatible API.
        """

        return (
            self.streaming
        )

    # --------------------------------------------------

    def is_listening(
        self,
    ):
        """
        Frontend-friendly API.
        """

        return (
            self.streaming
        )


if __name__ == "__main__":

    agent = (
        RealtimeAudioAgent()
    )

    print(
        "Realtime Audio Agent Initialized."
    )