"""
Speech-to-Text Agent

Purpose:
Convert candidate audio answers into text
for interview evaluation.

Pipeline:

Audio File
      ↓
Validation
      ↓
Speech Recognition
      ↓
Transcript Cleaning
      ↓
Interview Evaluation
"""

from pathlib import Path
import re

try:
    from faster_whisper import WhisperModel

    WHISPER_AVAILABLE = True

except ImportError:

    WHISPER_AVAILABLE = False


SUPPORTED_FORMATS = {
    ".wav",
    ".mp3",
    ".m4a",
    ".ogg",
}


class SpeechToTextAgent:
    """
    Speech Recognition Agent.
    """

    def __init__(
        self,
        model_size="base",
    ):
        """
        Initialize STT Agent.

        Model loading is lazy-loaded to avoid
        repeated loading during Streamlit reruns.
        """

        self.model_size = model_size
        self.model = None

        self.audio_directory = Path(
            "audio/candidate_answers"
        )

        self.audio_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def load_model(self):
        """
        Load Faster Whisper model.
        """

        if not WHISPER_AVAILABLE:

            print(
                "faster-whisper not installed. "
                "Using mock mode."
            )

            self.model = None

            return

        print(
            f"Loading Faster Whisper model: "
            f"{self.model_size}"
        )

        self.model = WhisperModel(
            self.model_size,
            device="cpu",
            compute_type="int8",
        )

        print(
            "Whisper model loaded successfully."
        )

    def validate_audio(
        self,
        audio_path,
    ):
        """
        Validate audio file.
        """

        audio_file = Path(audio_path)

        if not audio_file.exists():

            raise FileNotFoundError(
                f"Audio file not found: "
                f"{audio_path}"
            )

        if (
            audio_file.suffix.lower()
            not in SUPPORTED_FORMATS
        ):

            raise ValueError(
                "Unsupported audio format. "
                "Supported formats: "
                "wav, mp3, m4a, ogg"
            )

        return True

    def clean_transcript(
        self,
        transcript,
    ):
        """
        Clean transcript text.
        """

        transcript = transcript.strip()

        transcript = re.sub(
            r"\s+",
            " ",
            transcript,
        )

        return transcript

    def transcribe_audio(
        self,
        audio_path,
    ):
        """
        Convert speech to text.
        """

        self.validate_audio(
            audio_path
        )

        if self.model is None:

            self.load_model()

        if self.model is None:

            return {
                "transcript":
                    "Mock transcript generated.",

                "language":
                    "en",

                "duration":
                    0.0,
            }

        try:

            segments, info = (
                self.model.transcribe(
                    audio_path
                )
            )

            transcript = " ".join(
                segment.text
                for segment in segments
            )

            transcript = (
                self.clean_transcript(
                    transcript
                )
            )

            return {

                "transcript":
                    transcript,

                "language":
                    info.language,

                "duration":
                    round(
                        info.duration,
                        2,
                    ),
            }

        except Exception as error:

            raise RuntimeError(
                "Speech recognition failed: "
                f"{error}"
            )

    def run(
        self,
        audio_path,
    ):
        """
        Complete STT pipeline.
        """

        return self.transcribe_audio(
            audio_path
        )


def main():

    agent = (
        SpeechToTextAgent()
    )

    sample_audio = (
        "sample_answer.wav"
    )

    try:

        result = agent.run(
            sample_audio
        )

        print(
            "\nTranscription Result:\n"
        )

        print(result)

    except Exception as error:

        print(error)


if __name__ == "__main__":
    main()