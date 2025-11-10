import os, json
filepath = os.path.join(os.path.dirname(__file__), "dev_oldest_7_session.json")
with open(filepath) as f:
    data = json.load(f)
print(data[:2])  # just test
