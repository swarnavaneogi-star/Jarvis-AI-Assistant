WAKE_WORDS = ("jarvis",)


def is_wake_word_detected(text: str) -> bool:
    normalized = text.lower().strip()
    return any(word in normalized for word in WAKE_WORDS)
