EXIT_KEYWORDS = ["exit", "quit", "bye", "end", "stop"]

def get_tech_stack_note(user_input: str) -> str:
    """Detects tech stack keywords and returns steering instruction."""
    lower_input = user_input.lower()
    system_note = ""
    if "python" in lower_input:
        system_note += " [System: The candidate mentioned Python. Ask specific questions about Python generators, decorators, or GIL.]"
    if "django" in lower_input:
        system_note += " [System: The candidate mentioned Django. Ask about ORM, middleware, or signals.]"
    if "postgres" in lower_input or "postgresql" in lower_input or "sql" in lower_input:
        system_note += " [System: The candidate mentioned Database/SQL. Ask about indexing, normalization, or ACID properties.]"
    return system_note

def save_interview(messages: list) -> str:
    """Saves the interview transcript to a JSON file and returns the filename."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    directory = "data/interviews"
    os.makedirs(directory, exist_ok=True)
    filename = f"{directory}/interview_{timestamp}.json"
    
    with open(filename, "w") as f:
        json.dump(messages, f, indent=4)
    
    return filename

import json
import datetime
import os

def is_exit_keyword(user_input: str) -> bool:
    return any(word in user_input.lower() for word in EXIT_KEYWORDS)
