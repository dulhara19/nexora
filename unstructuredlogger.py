# unstructuredlogger.py

import json
from datetime import datetime

def log_result(
    query,
    final_answer,
    retrieved_context,
    log_file="unstructured_logs.json"
):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "retrieved_context": retrieved_context,
        "final_answer": final_answer,
        
    }

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    logs.append(log_entry)

    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4)
