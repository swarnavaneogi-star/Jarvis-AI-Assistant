from datetime import datetime
from core.tts import speak


def handle_command(command: str) -> bool:
    if not command:
        speak("I didn't catch that, sir.")
        return True

    command = command.lower().strip()

    if command in ("hello", "hi", "hey"):
        speak("Hello sir. How can I help you?")

    elif "good morning" in command:
        speak("Good morning, sir. I hope you have a great day.")

    elif "good afternoon" in command:
        speak("Good afternoon, sir. How can I assist you?")

    elif "good evening" in command:
        speak("Good evening, sir. How can I help you?")

    elif "good night" in command:
        speak("Good night, sir. Have a peaceful night.")

    elif "how are you" in command:
        speak("I am doing great, sir.")

    elif (
        "thank you" in command
        or "thanks" in command
        or "thank u" in command
    ):
        speak("You're welcome, sir.")

    elif (
        "what time" in command
        or "what is the time" in command
        or "time is it" in command
        or "tell me the time" in command
    ):
        speak(datetime.now().strftime("The time is %I:%M %p, sir."))

    elif "who are you" in command or "what is your name" in command:
        speak("I am JARVIS, your personal AI assistant.")

    elif "bye" in command or "goodbye" in command:
        speak("Goodbye, sir. Standing by.")
        return False

    else:
        speak("I heard you, sir, but I don't know that command yet.")

    return True