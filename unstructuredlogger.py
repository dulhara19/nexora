import json
from datetime import datetime

def log_result(query, final_answer, expected_answer, used_fallback, success):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "final_answer": final_answer,
        "expected_answer": expected_answer,
        "used_fallback": used_fallback,
        "success": success
    }
    with open("agent_eval_logs.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
