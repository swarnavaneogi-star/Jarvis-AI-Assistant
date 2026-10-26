import os

cublas_dir = os.path.abspath(
    r".\.venv\Lib\site-packages\nvidia\cublas\bin"
)

cudnn_dir = os.path.abspath(
    r".\.venv\Lib\site-packages\nvidia\cudnn\bin"
)

nvrtc_dir = os.path.abspath(
    r".\.venv\Lib\site-packages\nvidia\cuda_nvrtc\bin"
)

os.add_dll_directory(cublas_dir)
os.add_dll_directory(cudnn_dir)
os.add_dll_directory(nvrtc_dir)

os.environ["PATH"] = (
    cublas_dir
    + os.pathsep
    + cudnn_dir
    + os.pathsep
    + nvrtc_dir
    + os.pathsep
    + os.environ["PATH"]
)
import speech_recognition as sr
from faster_whisper import WhisperModel

print("Loading Whisper...")
model = WhisperModel(
    "tiny",
    device="cuda",
    compute_type="float16"
)

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Calibrating microphone...")
    recognizer.adjust_for_ambient_noise(source, duration=0.4)

    print("\nSpeak something...")
    audio = recognizer.listen(
        source,
        timeout=5,
        phrase_time_limit=20
    )

print("Processing with Whisper...")

audio_data = audio.get_wav_data()

with open("whisper_test.wav", "wb") as file:
    file.write(audio_data)

segments, info = model.transcribe(
    "whisper_test.wav",
    beam_size=5
)

text = " ".join(segment.text for segment in segments).strip()

print("\nWhisper heard:")
print(text)
print("\nLanguage:", info.language)