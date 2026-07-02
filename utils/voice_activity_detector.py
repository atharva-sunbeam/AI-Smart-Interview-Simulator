"""
Voice Activity Detector

Purpose:
Detect whether an incoming audio chunk
contains speech or silence.

Current implementation:
Simple RMS energy detector.
"""

import numpy as np


class VoiceActivityDetector:
    """
    Energy-based Voice Activity Detector.
    """

    def __init__(
        self,
        threshold=0.01,
    ):

        self.threshold = threshold

    def is_speech(
        self,
        audio_chunk,
    ):
        """
        Return True if the audio chunk
        contains speech.
        """

        if audio_chunk is None:
            return False

        energy = np.sqrt(
            np.mean(
                np.square(audio_chunk)
            )
        )

        # Convert NumPy bool -> Python bool
        return bool(
            energy > self.threshold
        )