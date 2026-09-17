from core.speech import take_command
from core.tts import speak
from core.wake_word import is_wake_word_detected


def handle_command(command: str) -> None:
    if not command:
        speak("I didn't catch that, sir.")
        return

    if "hello" in command:
        speak("Hello sir. How can I help you?")

    elif "how are you" in command:
        speak("I am doing great, sir.")

    elif "thank you" in command:
        speak("You're welcome, sir.")

    else:
        speak("I heard you, sir.")


def main() -> None:
    speak("Initialising JARVIS...")

    while True:
        heard = take_command()

        if not is_wake_word_detected(heard):
            continue

        print("WAKE WORD DETECTED")
        speak("Yes sir")

        command = take_command()
        handle_command(command)


if __name__ == "__main__":
    main()
