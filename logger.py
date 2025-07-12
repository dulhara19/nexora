import json
import os
from datetime import datetime


def log_query_result(user_query, agent_used, data_source, final_answer, retrieved_docs, expected_keywords, used_fallback=False, success=True):
    log_file = "evaluation_logs.json"
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "query": user_query,
        "agent": agent_used,
        "data_source": data_source,
        "final_answer": final_answer,
        "retrieved_docs": retrieved_docs,
        "expected_keywords": expected_keywords,
        "used_fallback": used_fallback,
        "success": success
    }

    logs = []
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as file:
            try:
                logs = json.load(file)
            except json.JSONDecodeError:
                print("⚠️ Corrupt or empty log file. Resetting it...")
                logs = []

    logs.append(log_entry)

    with open(log_file, "w", encoding="utf-8") as file:
        json.dump(logs, file, indent=2)
