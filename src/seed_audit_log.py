import json
from pathlib import Path
from datetime import datetime, timedelta

def generate_mock_audit_log():
    audit_log = []
    base_time = datetime.now() - timedelta(days=30)
    
    # Generate 23 APPROVED cases
    for i in range(23):
        audit_log.append({
            "timestamp": (base_time + timedelta(days=i)).isoformat(),
            "case_id": f"HIST-{i+1:03d}",
            "ai_diagnosis": {"root_cause": "Historical simulated error", "confidence": 92.5},
            "rule_findings": [],
            "decision": "APPROVE",
            "edited_diagnosis": None,
            "reviewer_comment": ""
        })
        
    # Generate 7 OVERRIDES (5 EDITS, 2 REJECTS)
    overrides = [
        ("HIST-024", "EDIT", "AI incorrectly identified the OSI layer. Changed from Layer 3 to Layer 2.", {"root_cause": "VLAN tag mismatch", "next_command": ["show interface trunk"], "fix_steps": ["switchport trunk allowed vlan add 10"]}),
        ("HIST-025", "EDIT", "AI missed a critical fix step.", {"root_cause": "Subinterface disabled", "next_command": [], "fix_steps": ["interface gi0/0.10", "no shutdown"]}),
        ("HIST-026", "EDIT", "Commands recommended were deprecated.", {"root_cause": "NAT overload missing", "next_command": [], "fix_steps": ["ip nat inside source list 1 interface Gi0/1 overload"]}),
        ("HIST-027", "EDIT", "Adjusted subnet mask recommendation.", {"root_cause": "Incorrect subnet mask", "next_command": [], "fix_steps": ["interface gi0/0", "ip address 192.168.1.1 255.255.255.0"]}),
        ("HIST-028", "EDIT", "Added clear arp-cache step.", {"root_cause": "Duplicate IP", "next_command": [], "fix_steps": ["clear arp-cache", "no ip address"]}),
        ("HIST-029", "REJECT", "AI hallucinated a hardware failure when it was a simple configuration issue.", None),
        ("HIST-030", "REJECT", "AI recommended executing 'clear ip nat translation *' in production during peak hours. Unacceptable.", None)
    ]
    
    for i, (case_id, decision, comment, edited) in enumerate(overrides):
        audit_log.append({
            "timestamp": (base_time + timedelta(days=23+i)).isoformat(),
            "case_id": case_id,
            "ai_diagnosis": {"root_cause": "Original faulty AI logic", "confidence": 75.0},
            "rule_findings": [],
            "decision": decision,
            "edited_diagnosis": edited,
            "reviewer_comment": comment
        })
        
    log_file = Path(__file__).parent.parent / "data" / "audit_log.json"
    with open(log_file, "w") as f:
        json.dump(audit_log, f, indent=4)
        
if __name__ == "__main__":
    generate_mock_audit_log()
    print("Mock audit log populated.")
