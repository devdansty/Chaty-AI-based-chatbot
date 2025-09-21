import json
import random
import spacy
from nltk.tokenize import word_tokenize
import os

nlp = spacy.load("en_core_web_sm")
with open("intents.json") as file:
    intents = json.load(file)


TASK_FILE = "tasks.json"
if not os.path.exists(TASK_FILE):
    with open(TASK_FILE, "w") as f:
        json.dump([], f)

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f)

def load_tasks():
    with open(TASK_FILE) as f:
        return json.load(f)


def get_response(message):
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
    tasks = load_tasks()

    if "add" in message.lower():
        task_name = message.lower().replace("add task", "").strip()
        if task_name:
            tasks.append(task_name)
            save_tasks(tasks)
            return f"Task '{task_name}' added!"
        return "Please specify a task to add."

    elif "delete" in message.lower():
        task_name = message.lower().replace("delete task", "").strip()
        if task_name in tasks:
            tasks.remove(task_name)
            save_tasks(tasks)
            return f"Task '{task_name}' deleted!"
        return "Task not found."

    elif "show" in message.lower() or "list" in message.lower():
        if tasks:
            return "Your tasks:\n" + "\n".join([f"- {t}" for t in tasks])
        return "No tasks found!"

    else:
        return "Task commands: add task, delete task, show tasks."