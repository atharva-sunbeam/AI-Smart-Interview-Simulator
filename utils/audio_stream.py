"""
Audio Stream Utility

Purpose:
Capture continuous microphone audio and
store it as fixed-duration chunks.

Pipeline:

Microphone
      ↓
PCM Audio
      ↓
Chunk Queue
"""

from queue import Queue

import numpy as np
import sounddevice as sd
import soundfile as sf


class AudioStream:
    """
    Continuous microphone audio stream.
    """

    def __init__(
        self,
        sample_rate=16000,
        channels=1,
        chunk_duration=2,
    ):

        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_duration = chunk_duration

        self.chunk_size = (
            self.sample_rate
            * self.chunk_duration
        )

        self.audio_queue = Queue()

        self.running = False

        self.stream = None

    def audio_callback(
        self,
        indata,
        frames,
        time,
        status,
    ):
        """
        Callback executed by sounddevice.
        """

        if status:
            print(status)

        self.audio_queue.put(
            np.copy(indata)
        )

    def start(self):
        """
        Start microphone stream.
        """

        if self.running:
            return

        self.running = True

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=self.audio_callback,
            blocksize=self.chunk_size,
            dtype="float32",
        )

        self.stream.start()

    def stop(self):
        """
        Stop microphone stream.
        """

        self.running = False

        if self.stream:

            self.stream.stop()

            self.stream.close()

            self.stream = None

    def read_chunk(self):
        """
        Retrieve next audio chunk.
        """

        if self.audio_queue.empty():
            return None

        return self.audio_queue.get()

    def queue_chunk(
        self,
        chunk,
    ):
        """
        Testing helper.
        """

        self.audio_queue.put(
            chunk
        )

    def save_chunk(
        self,
        chunk,
        output_path,
    ):
        """
        Save one audio chunk as a WAV file.

        Parameters
        ----------
        chunk : numpy.ndarray
            Audio samples.

        output_path : str
            Destination WAV file.
        """

        if chunk is None:
            return

        sf.write(
            file=output_path,
            data=chunk,
            samplerate=self.sample_rate,
        )