EXIT_KEYWORDS = ["exit", "quit", "bye", "end", "stop"]

def is_exit_keyword(text):
    return any(word in text.lower() for word in EXIT_KEYWORDS)
