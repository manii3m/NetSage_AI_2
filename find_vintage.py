import json

target_step = 296
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
                if call['name'] in ['write_to_file', 'replace_file_content'] and call['args'].get('TargetFile', '').endswith('app.py'):
                    if 'update_' not in call['args'].get('TargetFile', ''):
                        if 'CodeContent' in call['args']:
                            app_py_content = call['args']['CodeContent']
                        elif 'ReplacementContent' in call['args']:
                            # This gets complicated if it was replace_file_content. We might miss the full content.
                            pass
                        
if app_py_content:
    with open('vintage_app.py', 'w', encoding='utf-8') as out:
        out.write(app_py_content)
    print("Found full write_to_file for app.py and saved to vintage_app.py")
else:
    print("Did not find a full write_to_file before step 296.")
