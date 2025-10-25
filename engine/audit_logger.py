# audit_logger.py
# Step 3: Append audit logs for explainability

import json, datetime

def log_decision(txn_id, inputs, outputs, rationale_list, path="audit_log.json"):
    entry = {
        "txn_id": txn_id,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "inputs": inputs,
        "outputs": outputs,
        "rationale": rationale_list
    }
    try:
        logs = json.load(open(path, encoding="utf-8"))
    except Exception:
        logs = []
    logs.append(entry)
    json.dump(logs, open(path,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
