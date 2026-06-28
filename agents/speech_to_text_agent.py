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

from faster_whisper import WhisperModel


SUPPORTED_FORMATS = {
    ".wav",
    ".mp3",
    ".m4a",
    ".ogg"
}


class SpeechToTextAgent:
    """
    Speech Recognition Agent.
    """

    def __init__(
        self,
        model_size="base"
    ):

        self.model_size = model_size
        self.model = None

        self.load_model()

    def load_model(self):
        """
        Load Faster Whisper model.
        """

        self.model = WhisperModel(
            self.model_size,
            device="cpu",
            compute_type="int8"
        )

        print(
            f"Loaded Faster Whisper model: "
            f"{self.model_size}"
        )

    def validate_audio(
        self,
        audio_path
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
                "Unsupported audio format."
            )

        return True

    def transcribe_audio(
        self,
        audio_path
    ):
        """
        Convert speech to text.
        """

        self.validate_audio(
            audio_path
        )

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
                    2
                )
        }

    def clean_transcript(
        self,
        transcript
    ):
        """
        Clean transcript text.
        """

        transcript = (
            transcript.strip()
        )

        transcript = re.sub(
            r"\s+",
            " ",
            transcript
        )

        return transcript

    def run(
        self,
        audio_path
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

        print("\nResult:\n")

        print(result)

    except Exception as error:

        print(error)


if __name__ == "__main__":
    main()