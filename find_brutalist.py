import json

target_step = 188
app_py_content = None

with open(r'C:\Users\vishw\.gemini\antigravity\brain\069233ce-4640-49b9-9eea-b4f28b97f139\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
        except:
            continue
            
        if data.get('step_index', 9999) >= target_step:
            break
            
        if 'tool_calls' in data:
            for call in data['tool_calls']:
                if call['name'] == 'write_to_file' and call['args'].get('TargetFile', '').endswith('app.py'):
                    if 'update_' not in call['args'].get('TargetFile', ''):
                        app_py_content = call['args'].get('CodeContent', '')
                        
        if 'content' in data and data.get('source') == 'MODEL' and 'File Path: `file:///c:/Users/vishw/OneDrive/Desktop/NetStage%20AI/src/app.py`' in data['content']:
            # Maybe it was viewed?
            pass

if app_py_content:
    with open('restored_app.py', 'w', encoding='utf-8') as out:
        out.write(app_py_content)
    print("Found write_to_file for app.py and saved to restored_app.py")
else:
    print("Did not find a full write_to_file. Let's look for the last view_file.")

