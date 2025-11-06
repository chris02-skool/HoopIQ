# User authentification

import json
import os
import re

# Path for users.json in project folder
USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")

# Ensure JSON file exists
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

# Password validation
def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    return True

# Load users
def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

# Save users
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Register user
def register(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    if not is_valid_password(password):
        return False, "Password must be ≥8 chars, 1 uppercase, 1 lowercase, 1 number."
    users[username] = password
    save_users(users)
    return True, "Registration successful! Please login."

# Login user
def login(username, password):
    users = load_users()
    if username not in users:
        return False, "Incorrect username or password."
    if users[username] != password:
        return False, "Incorrect username or password."
    return True, ""
