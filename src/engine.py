from src.checker import check_rules
from src.ai_client import get_diagnosis

def run_diagnosis(case_data):
    # Run deterministic rule checker
    checker_result = check_rules(case_data)
    
    # Run AI diagnosis
    ai_result = get_diagnosis(case_data, checker_result.get("findings", []))
    
    return {
        "checker_result": checker_result,
        "ai_result": ai_result
    }
