import pyttsx3


class TTS:
    def __init__(self):
        self.rate = 175

    def speak(self, text: str) -> None:
        if not text:
            return

        try:
            engine = pyttsx3.init("sapi5")
            engine.setProperty("rate", self.rate)

            print(f"JARVIS: {text}")

            engine.say(text)
            engine.runAndWait()
            engine.stop()

        except Exception as exc:
            print(f"TTS error: {exc}")


_tts = TTS()


def speak(text: str) -> None:
    _tts.speak(text)