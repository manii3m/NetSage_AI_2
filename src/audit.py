import json
import os
from datetime import datetime
from pathlib import Path

AUDIT_LOG_FILE = Path(__file__).parent.parent / "data" / "audit_log.json"

def load_audit_log():
    if not AUDIT_LOG_FILE.exists():
        return []
    with open(AUDIT_LOG_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_audit_log(log_data):
    with open(AUDIT_LOG_FILE, "w") as f:
        json.dump(log_data, f, indent=4)

def log_decision(case_id, ai_diagnosis, rule_findings, decision, edited_diagnosis=None, reviewer_comment=""):
    log_data = load_audit_log()
    record = {
        "timestamp": datetime.now().isoformat(),
        "case_id": case_id,
        "ai_diagnosis": ai_diagnosis,
        "rule_findings": rule_findings,
        "decision": decision,
        "edited_diagnosis": edited_diagnosis,
        "reviewer_comment": reviewer_comment
    }
    log_data.append(record)
    save_audit_log(log_data)
    return record
    
def get_kpis():
    log_data = load_audit_log()
    total_audits = len(log_data)
    if total_audits == 0:
        return {"total": 0, "agreement_percent": 0.0, "overrides": 0}
        
    approved = sum(1 for r in log_data if r["decision"] == "APPROVE")
    overrides = total_audits - approved
    agreement_percent = round((approved / total_audits) * 100, 1)
    
    return {
        "total": total_audits,
        "agreement_percent": agreement_percent,
        "overrides": overrides
    }
