import os
import json
import google.generativeai as genai
from pathlib import Path

def get_diagnosis(case_data, checker_findings):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key.strip() == "" or api_key == "your_gemini_api_key_here":
        return get_mock_diagnosis(case_data, checker_findings)

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash", generation_config={"response_mime_type": "application/json"})
        
        prompt_path = Path(__file__).parent.parent / "prompts" / "diagnose_prompt.md"
        with open(prompt_path, "r") as f:
            system_prompt = f.read()

        prompt = f"""
        {system_prompt}
        
        INPUT DATA:
        Symptom: {case_data.get('symptom')}
        Topology Note: {case_data.get('topology_note')}
        Show Command Output: {case_data.get('show_command_output')}
        Deterministic Rule Findings: {json.dumps(checker_findings)}
        """
        
        response = model.generate_content(prompt)
        result = json.loads(response.text)
        result['is_demo'] = False
        return result
    except Exception as e:
        print(f"Gemini API Error: {e}")
        mock = get_mock_diagnosis(case_data, checker_findings)
        mock['root_cause'] = f"API Error / Demo Mode (Details: {str(e)[:50]}...)"
        return mock

def get_mock_diagnosis(case_data, checker_findings):
    root_cause = "Simulated: " + str(case_data.get('expected_fault', 'Unknown fault'))
    osi_layer = str(case_data.get('osi_layer', 'Unknown Layer'))
    
    evidence = []
    if checker_findings:
        evidence = [f['evidence'] for f in checker_findings]
    else:
        evidence = [str(case_data.get('show_command_output', 'No evidence provided'))]

    return {
        "root_cause": root_cause,
        "osi_layer": osi_layer,
        "confidence": 85.5,
        "evidence": evidence,
        "next_command": ["show ip interface brief", "show running-config"],
        "fix_steps": ["Simulated step 1: enter global config", "Simulated step 2: apply simulated fix"],
        "reasoning_summary": "This is a mock simulated response because the Gemini API key was not configured or an error occurred.",
        "safety_note": "Human review required before applying any fix.",
        "is_demo": True
    }
