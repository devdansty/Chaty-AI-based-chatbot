import json
import random
import spacy
import os

# Load Spacy NLP model
nlp = spacy.load("en_core_web_sm")

# Load intents.json safely with UTF-8
with open("intents.json", encoding="utf-8") as file:
    intents = json.load(file)

# Task file
TASK_FILE = "tasks.json"
if not os.path.exists(TASK_FILE):
    with open(TASK_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)


# ------------------------------
# Task Management Functions
# ------------------------------
def save_tasks(tasks):
    with open(TASK_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def load_tasks():
    with open(TASK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ------------------------------
# Chatbot Response Function
# ------------------------------
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


# ------------------------------
# Task Handling Function
# ------------------------------
def handle_tasks(message):
    tasks = load_tasks()
    msg = message.lower().strip()

    # Add Task
    if msg.startswith("add"):
        task_name = msg.replace("add task", "").replace("add", "").strip()
        if task_name:
            tasks.append(task_name)
            save_tasks(tasks)
            return f"✅ Task '{task_name}' added!"
        return "⚠️ Please specify a task to add."

    # Delete Task
    elif msg.startswith("delete") or msg.startswith("remove"):
        task_name = msg.replace("delete task", "").replace("remove task", "").replace("delete", "").replace("remove", "").strip()
        if task_name in tasks:
            tasks.remove(task_name)
            save_tasks(tasks)
            return f"🗑️ Task '{task_name}' deleted!"
        return "⚠️ Task not found."

    # Show Tasks
    elif "show" in msg or "list" in msg:
        if tasks:
            return "📋 Your tasks:\n" + "\n".join([f"- {t}" for t in tasks])
        return "⚠️ No tasks found!"

    else:
        return "ℹ️ Task commands: 'add task', 'delete task', 'show tasks'."