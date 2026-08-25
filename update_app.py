import sys

with open('src/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_diag_block = False
for i, line in enumerate(lines):
    if line.strip() == 'diagnosis_results = run_diagnosis(selected_case.to_dict())':
        # Replace the RUN DIAGNOSTICS section setup
        new_lines.append('    st.markdown(\'<div class="section-header"><span class="section-num">[03]</span> DIAGNOSTIC ENGINE <span class="micro-label" style="font-size: 0.8rem; background: transparent; color: #111111; margin-left: auto;">ENGINE // DETERMINISTIC + AI</span></div>\', unsafe_allow_html=True)\n\n')
        new_lines.append('    if st.button("INITIATE DIAGNOSIS", key=f"init_diag_{selected_case_id}"):\n')
        new_lines.append('        with st.spinner("Contacting Gemini AI and running Deterministic Rules..."):\n')
        new_lines.append('            st.session_state[f"diagnosis_{selected_case_id}"] = run_diagnosis(selected_case.to_dict())\n\n')
        new_lines.append('    if f"diagnosis_{selected_case_id}" not in st.session_state:\n')
        new_lines.append('        st.markdown(\'<div style="background-color: #111111; color: #FFDE00; padding: 20px; font-family: IBM Plex Mono, monospace; border: 4px solid #FFDE00; box-shadow: 8px 8px 0px #111111; text-align: center; margin-bottom: 40px; font-weight: 700;">AWAITING DIAGNOSTIC INITIATION...</div>\', unsafe_allow_html=True)\n')
        new_lines.append('    else:\n')
        new_lines.append('        diagnosis_results = st.session_state[f"diagnosis_{selected_case_id}"]\n')
        in_diag_block = True
    elif line.strip() == '# ---------------------------------------------------------' and i > 590 and 'AUDIT LOG TABLE' in lines[i+1]:
        in_diag_block = False
        new_lines.append(line)
    elif in_diag_block:
        if line.strip() == '':
            new_lines.append(line)
        else:
            new_lines.append('    ' + line)
    else:
        new_lines.append(line)

# Add Reset button at the bottom
new_lines.append('\n')
new_lines.append('    # ---------------------------------------------------------\n')
new_lines.append('    # RESET SYSTEM\n')
new_lines.append('    # ---------------------------------------------------------\n')
new_lines.append('    st.markdown(\'<div class="section-header"><span class="section-num">[08]</span> SYSTEM CONTROLS <span class="micro-label" style="font-size: 0.8rem; background: transparent; color: #111111; margin-left: auto;">ADMIN ONLY</span></div>\', unsafe_allow_html=True)\n')
new_lines.append('    if st.button("RESET SYSTEM STATS (CLEAR AUDIT LOG)"):\n')
new_lines.append('        from src.audit import save_audit_log\n')
new_lines.append('        save_audit_log([])\n')
new_lines.append('        st.session_state.clear()\n')
new_lines.append('        st.rerun()\n')

with open('src/app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Updated app.py successfully')
