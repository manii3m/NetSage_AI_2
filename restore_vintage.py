import textwrap
import re

with open('vintage_app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix Plotly font weight errors
text = text.replace('title_font_weight="900", tickfont_weight="700"', '')
text = text.replace('textfont_weight="900"', '')
text = text.replace('textfont_weight="600"', '')
text = text.replace('title_font_weight="700", tickfont_weight="600"', '')

# 2. Fix the color palette
palette_replacement = """if st.session_state.dark_mode:
    bg_app = "#000000"
    bg_card = "#111111"
    bg_alt = "#222222"
    border = "#FFFFFF"
    border_dark = "#FFDE00"
    text_main = "#FFFFFF"
    text_muted = "#FFFFFF"
    text_sub = "#FFFFFF"
    heading = "#FFFFFF"
    
    b_succ_bg, b_succ_tx, b_succ_bd = "#000000", "#FFDE00", "#FFDE00"
    b_warn_bg, b_warn_tx, b_warn_bd = "#FFDE00", "#000000", "#FFDE00"
    b_dang_bg, b_dang_tx, b_dang_bd = "#000000", "#FFFFFF", "#FFFFFF"
    b_info_bg, b_info_tx, b_info_bd = "#000000", "#FFFFFF", "#FFFFFF"
    b_neut_bg, b_neut_tx, b_neut_bd = "#000000", "#FFFFFF", "#FFFFFF"
else:
    bg_app = "#FFFFFF"
    bg_card = "#FFFFFF"
    bg_alt = "#FFDE00"
    border = "#000000"
    border_dark = "#000000"
    text_main = "#000000"
    text_muted = "#000000"
    text_sub = "#000000"
    heading = "#000000"
    
    b_succ_bg, b_succ_tx, b_succ_bd = "#FFFFFF", "#000000", "#000000"
    b_warn_bg, b_warn_tx, b_warn_bd = "#FFDE00", "#000000", "#000000"
    b_dang_bg, b_dang_tx, b_dang_bd = "#000000", "#FFFFFF", "#000000"
    b_info_bg, b_info_tx, b_info_bd = "#FFFFFF", "#000000", "#000000"
    b_neut_bg, b_neut_tx, b_neut_bd = "#FFFFFF", "#000000", "#000000"
"""

# Find where `if st.session_state.dark_mode:` starts and replace up to the end of the `else:` block
old_palette = text[text.find('if st.session_state.dark_mode:'):text.find('b_dang_bg, b_dang_tx, b_dang_bd = "#F9EBEA", "#8B3A3A", "#E0C2C2"') + len('b_dang_bg, b_dang_tx, b_dang_bd = "#F9EBEA", "#8B3A3A", "#E0C2C2"\n')]
text = text.replace(old_palette, palette_replacement)

# Also replace any stray colors in apply_minimal_style if there are hardcoded ones
text = text.replace("color_map = {'CRITICAL': '#8B3A3A', 'HIGH': '#D67474', 'MEDIUM': '#CCA752', 'LOW': '#3A5A3A'}", "color_map = {'CRITICAL': '#000000', 'HIGH': '#000000', 'MEDIUM': '#FFDE00', 'LOW': '#FFFFFF'}")
text = text.replace("color_map = {'CRITICAL': '#D67474', 'HIGH': '#D67474', 'MEDIUM': '#CCA752', 'LOW': '#86B386'}", "color_map = {'CRITICAL': '#FFFFFF', 'HIGH': '#FFFFFF', 'MEDIUM': '#FFDE00', 'LOW': '#000000'}")
text = text.replace("color_map2 = {'APPROVE': '#3A5A3A', 'EDIT': '#CCA752', 'REJECT': '#8B3A3A'}", "color_map2 = {'APPROVE': '#FFFFFF', 'EDIT': '#FFDE00', 'REJECT': '#000000'}")
text = text.replace("color_map2 = {'APPROVE': '#86B386', 'EDIT': '#CCA752', 'REJECT': '#D67474'}", "color_map2 = {'APPROVE': '#000000', 'EDIT': '#FFDE00', 'REJECT': '#FFFFFF'}")

# 3. Fix the markdown indentation bug
if 'import textwrap' not in text:
    text = 'import textwrap\n' + text

text = text.replace('st.markdown(f\"\"\"', 'st.markdown(textwrap.dedent(f\"\"\"')
text = text.replace('st.markdown(\"\"\"', 'st.markdown(textwrap.dedent(\"\"\"')
text = text.replace('\"\"\", unsafe_allow_html=True)', '\"\"\"), unsafe_allow_html=True)')

with open('src/app.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('Restored to src/app.py')
