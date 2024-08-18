import pyaudio
import numpy as np
from typing import Generator, List

class MicrophoneStream:
    """
        Opens a recording stream as a generator. Based on Google's streaming speech
        recognition code - https://cloud.google.com/speech-to-text/docs/transcribe-streaming-audio
    """ 

    def __init__(self: object, sample_rate: int, frame_length: int) -> None:
        self.sample_rate = sample_rate
        self.frame_length = frame_length
        self.is_open = False
        self.audio_interface = None
        self.audio_stream = None

    def __enter__(self: object) -> object: 
        self.audio_interface = pyaudio.PyAudio()
        self.audio_stream = self.audio_interface.open(
                    rate=self.sample_rate, 
                    channels=1,
                    format=pyaudio.paInt16,
                    input_device_index=0, 
                    input=True, 
                    frames_per_buffer=self.frame_length
                )
        self.is_open = True
        return self

    def __exit__(self: object, type: object, value: object, traceback: object) -> None: 
        self.is_open = False
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.audio_interface.terminate() 

    def generator(self: object) -> Generator[List[int], None, None]:
        while True: 
            frame = self.audio_stream.read(self.frame_length)
            audio_chunk = np.frombuffer(frame, dtype=np.int16).tolist()
            yield audio_chunk
