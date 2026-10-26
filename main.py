from core.speech import take_command
from core.tts import speak
from core.wake_word import is_wake_word_detected
from core.brain import handle_command


def main() -> None:
    speak("Initialising JARVIS...")

    while True:
        if not is_wake_word_detected():
            continue

        speak("Yes sir")

        command = take_command()

        if not command:
            speak("Sorry sir, I couldn't understand you.")
            continue

        if not handle_command(command):
            break


if __name__ == "__main__":
    main()