import numpy as np
import pyaudio
from openwakeword.model import Model


class WakeWordDetector:
    def __init__(self):
        self.model = Model(
            wakeword_models=["hey_jarvis"],
            inference_framework="onnx",
        )

        self.audio = pyaudio.PyAudio()
        self.stream = None

    def wait_for_wake_word(self) -> bool:
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1280,
        )

        try:
            while True:
                audio_data = self.stream.read(
                    1280,
                    exception_on_overflow=False,
                )

                audio_array = np.frombuffer(
                    audio_data,
                    dtype=np.int16,
                )

                prediction = self.model.predict(audio_array)
                score = prediction["hey_jarvis"]

                print(f"Wake score: {score:.2f}", end="\r")

                if score >= 0.7:
                    print(f"\nWAKE WORD DETECTED | score: {score:.2f}")
                    self.model.reset()
                    return True

        finally:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def close(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()

        self.audio.terminate()


_wake_word = WakeWordDetector()


def is_wake_word_detected() -> bool:
    return _wake_word.wait_for_wake_word()