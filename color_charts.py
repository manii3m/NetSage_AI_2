with open('src/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('color_map = {"CRITICAL": b_dang_tx, "HIGH": b_dang_tx, "MEDIUM": b_warn_tx, "LOW": b_succ_tx}', 'color_map = {"CRITICAL": "#E63946", "HIGH": "#E63946", "MEDIUM": "#F4A261", "LOW": "#2A9D8F"}')
text = text.replace('color_map2 = {"APPROVE": b_succ_tx, "EDIT": b_warn_tx, "REJECT": b_dang_tx}', 'color_map2 = {"APPROVE": "#2A9D8F", "EDIT": "#F4A261", "REJECT": "#E63946"}')
text = text.replace('color_discrete_sequence=[text_muted]', 'color_discrete_sequence=["#457B9D"]')
text = text.replace('color_discrete_sequence=[b_info_tx]', 'color_discrete_sequence=["#8ECAE6"]')

with open('src/app.py', 'w', encoding='utf-8') as f:
    f.write(text)
