import numpy as np
import pyaudio
from openwakeword.model import Model


model = Model(wakeword_models=["hey_jarvis"])

audio = pyaudio.PyAudio()

stream = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=1280,
)

print("Listening for: Hey Jarvis")

try:
    while True:
        audio_data = stream.read(
            1280,
            exception_on_overflow=False,
        )

        audio_array = np.frombuffer(
            audio_data,
            dtype=np.int16,
        )

        prediction = model.predict(audio_array)

        score = prediction["hey_jarvis"]

        if score > 0.5:
            print(f"JARVIS DETECTED | score: {score:.2f}")
            break 

except KeyboardInterrupt:
    print("\nStopping...")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()