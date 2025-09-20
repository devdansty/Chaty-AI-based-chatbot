import json
import random
import spacy
from nltk.tokenize import word_tokenize
import os

# Load Spacy NLP model
nlp = spacy.load("en_core_web_sm")

# Load intents (UTF-8 safe)
with open("intents.json", encoding="utf-8") as file:
    intents = json.load(file)

# Task file
TASK_FILE = "tasks.json"

# Create tasks.json if it doesn't exist
if not os.path.exists(TASK_FILE):
    with open(TASK_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)


def save_tasks(tasks):
    """Save tasks to file (UTF-8 safe)."""
    with open(TASK_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def load_tasks():
    """Load tasks from file (UTF-8 safe)."""
    with open(TASK_FILE, encoding="utf-8") as f:
        return json.load(f)


def get_response(message):
    """Process user message and return a response."""
    message_tokens = [token.text.lower() for token in nlp(message)]

    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            pattern_tokens = [token.text.lower() for token in nlp(pattern)]
            if any(word in message_tokens for word in pattern_tokens):
                if intent["tag"] == "tasks":
                    return handle_tasks(message)
                return random.choice(intent["responses"])

    return "I am sorry, I don't understand. Can you rephrase?"


def handle_tasks(message):
    """Handle task-related commands (add, delete, show)."""
    tasks = load_tasks()
    message_lower = message.lower()

    if "add" in message_lower:
        task_name = message_lower.replace("add task", "").strip()
        if task_name:
            tasks.append(task_name)
            save_tasks(tasks)
            return f"Task '{task_name}' added!"
        return "Please specify a task to add."

    elif "delete" in message_lower:
        task_name = message_lower.replace("delete task", "").strip()
        if task_name in tasks:
            tasks.remove(task_name)
            save_tasks(tasks)
            return f"Task '{task_name}' deleted!"
        return "Task not found."

    elif "show" in message_lower or "list" in message_lower:
        if tasks:
            return "Your tasks:\n" + "\n".join([f"- {t}" for t in tasks])
        return "No tasks found!"

    else:
        return "Task commands: add task, delete task, show tasks."
