import os
import sys
import tempfile
from pathlib import Path

import speech_recognition as sr


venv_dir = Path(sys.executable).resolve().parents[1]
site_packages = venv_dir / "Lib" / "site-packages"

dll_dirs = [
    site_packages / "nvidia" / "cublas" / "bin",
    site_packages / "nvidia" / "cudnn" / "bin",
    site_packages / "nvidia" / "cuda_nvrtc" / "bin",
]

_dll_handles = []

for dll_dir in dll_dirs:
    if dll_dir.exists():
        _dll_handles.append(os.add_dll_directory(str(dll_dir)))
        os.environ["PATH"] = (
            str(dll_dir) + os.pathsep + os.environ.get("PATH", "")
        )


from faster_whisper import WhisperModel


class SpeechRecognizer:
    def __init__(self):
        self.model = WhisperModel(
            "tiny",
            device="cuda",
            compute_type="float16",
        )

        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 1.0
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5

    def listen(self) -> str:
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.4,
                )

                print("Listening...")

                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=20,
                )

        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

        except (OSError, AttributeError) as exc:
            print(f"Microphone error: {exc}")
            return ""

        try:
            audio_data = audio.get_wav_data()

            with tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False,
            ) as temp_file:
                temp_file.write(audio_data)
                temp_audio_path = temp_file.name

        except Exception as exc:
            print(f"Audio processing error: {exc}")
            return ""

        try:
            print("Processing with Whisper...")

            segments, info = self.model.transcribe(
                temp_audio_path,
                language="en",
                task="transcribe",
                beam_size=5,
                vad_filter=True,
                condition_on_previous_text=False,
            )

            text = " ".join(
                segment.text.strip()
                for segment in segments
                if segment.text.strip()
            )

            text = text.lower().strip()

            print("You said:", text)
            print("Language:", info.language)

            return text

        except Exception as exc:
            print(f"Whisper error: {exc}")
            return ""

        finally:
            try:
                os.remove(temp_audio_path)
            except OSError:
                pass


_speech = SpeechRecognizer()


def take_command() -> str:
    return _speech.listen()