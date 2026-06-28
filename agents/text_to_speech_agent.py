"""
Text-to-Speech Agent

Purpose:
Convert interview questions into speech.

Pipeline:

Question Text
        ↓
Text Validation
        ↓
gTTS Voice Generation
        ↓
MP3 Audio
        ↓
Playback
"""

from pathlib import Path
import os
import platform

from gtts import gTTS


class TextToSpeechAgent:
    """
    Convert interview questions into speech.
    """

    def validate_text(
        self,
        text: str,
    ) -> bool:
        """
        Validate input text.
        """

        if text is None:
            return False

        if not isinstance(
            text,
            str,
        ):
            return False

        if not text.strip():
            return False

        return True

    def generate_audio(
        self,
        text: str,
        output_path=(
            "generated_audio/"
            "interview_question.mp3"
        ),
    ) -> str:
        """
        Generate MP3 audio.
        """

        if not self.validate_text(
            text
        ):
            raise ValueError(
                "Invalid text supplied."
            )

        output = Path(
            output_path
        )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        tts = gTTS(
            text=text,
            lang="en",
            slow=False,
        )

        tts.save(
            str(output)
        )

        return str(output)

    def play_audio(
        self,
        audio_path: str,
    ) -> None:
        """
        Play generated audio.

        Uses OS default player.
        """

        audio = Path(
            audio_path
        )

        if not audio.exists():
            raise FileNotFoundError(
                audio_path
            )

        system = (
            platform.system()
        )

        if system == "Windows":
            os.startfile(audio)

        elif system == "Darwin":
            os.system(
                f'open "{audio}"'
            )

        else:
            os.system(
                f'xdg-open "{audio}"'
            )


if __name__ == "__main__":

    agent = (
        TextToSpeechAgent()
    )

    question = (
        "Explain Kafka architecture."
    )

    audio = (
        agent.generate_audio(
            question
        )
    )

    print(
        f"\nGenerated Audio:\n{audio}"
    )

    agent.play_audio(audio)