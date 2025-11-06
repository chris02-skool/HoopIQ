# User authentification

import streamlit as st
import json
import hashlib
from pathlib import Path

USER_FILE = Path("users.json")

def load_users():
    if USER_FILE.exists():
        with open(USER_FILE, "r") as f:
            return json.load(f)
    else:
        return {"users": {}}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login(username, password):
    users = load_users()
    if username in users["users"]:
        return users["users"][username]["password_hash"] == hash_password(password)
    return False

def register(username, password):
    users = load_users()
    if username in users["users"]:
        return False  # User exists
    users["users"][username] = {"password_hash": hash_password(password), "sessions": []}
    save_users(users)
    return True

def get_user_sessions(username):
    users = load_users()
    return users["users"][username]["sessions"]

def add_user_session(username, session_data):
    users = load_users()
    sessions = users["users"][username]["sessions"]
    sessions.insert(0, session_data)  # Newest first
    if len(sessions) > 10:             # Keep max 10 sessions
        sessions = sessions[:10]
    users["users"][username]["sessions"] = sessions
    save_users(users)
