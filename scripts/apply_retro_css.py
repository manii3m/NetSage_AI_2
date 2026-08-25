import re

with open('src/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Headings weight
text = text.replace('font-weight: 500 !important;\n    color: {heading} !important;\n    letter-spacing: -0.01em;', 
                    'font-weight: 800 !important;\n    color: {heading} !important;\n    letter-spacing: -0.02em;')

text = text.replace('font-size: 1.75rem !important;\n    margin: 0;\n    font-weight: 600;',
                    'font-size: 2.25rem !important;\n    margin: 0;\n    font-weight: 800;')

# 2. Add bold borders and hard shadows to cards and headers
text = text.replace('border-bottom: 1px solid {border};\n    padding: 24px 32px;\n    margin-bottom: 32px;\n    margin-top: 0;\n    display: flex;\n    justify-content: space-between;\n    align-items: center;\n    border-radius: 4px;',
                    'border: 3px solid {border};\n    padding: 24px 32px;\n    margin-bottom: 32px;\n    margin-top: 0;\n    display: flex;\n    justify-content: space-between;\n    align-items: center;\n    border-radius: 8px;\n    box-shadow: 6px 6px 0px {border};')

text = text.replace('border: 1px solid {border};\n    border-radius: 4px;\n    padding: 20px;\n    flex: 1;\n    min-width: 200px;\n    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);',
                    'border: 3px solid {border};\n    border-radius: 8px;\n    padding: 20px;\n    flex: 1;\n    min-width: 200px;\n    box-shadow: 5px 5px 0px {border};\n    transition: transform 0.1s ease;')

text = text.replace('border: 1px solid {border};\n    border-radius: 4px;\n    padding: 24px;\n    margin-bottom: 24px;\n    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);',
                    'border: 3px solid {border};\n    border-radius: 8px;\n    padding: 24px;\n    margin-bottom: 24px;\n    box-shadow: 6px 6px 0px {border};')

text = text.replace('border: 1px solid {border_dark};\n    white-space: pre-wrap;',
                    'border: 2px solid {border_dark};\n    border-radius: 6px;\n    white-space: pre-wrap;')

text = text.replace('border: 1px solid {border_dark};',
                    'border: 2px solid {border_dark};')

# 3. Badges border
text = text.replace('border: 1px solid transparent;',
                    'border: 2px solid {border};')
text = text.replace('border-color: {b_succ_bd};', 'border-color: {border};')
text = text.replace('border-color: {b_warn_bd};', 'border-color: {border};')
text = text.replace('border-color: {b_dang_bd};', 'border-color: {border};')
text = text.replace('border-color: {b_info_bd};', 'border-color: {border};')
text = text.replace('border-color: {b_neut_bd};', 'border-color: {border};')
text = text.replace('padding: 4px 10px;', 'padding: 4px 10px;\n    box-shadow: 2px 2px 0px {border};')

# 4. Buttons
text = text.replace('border: 1px solid {border_dark} !important;\n    border-radius: 4px !important;',
                    'border: 2px solid {border_dark} !important;\n    border-radius: 6px !important;\n    box-shadow: 3px 3px 0px {border_dark} !important;')

text = text.replace('div.stButton > button[kind="primary"] {\n    background-color: {text_muted} !important;\n    color: {bg_card} !important;\n    border: 1px solid {text_main} !important;\n}',
                    'div.stButton > button[kind="primary"] {\n    background-color: {text_main} !important;\n    color: {bg_card} !important;\n    border: 2px solid {text_main} !important;\n    box-shadow: 3px 3px 0px {text_main} !important;\n}')

# 5. Tables
text = text.replace('border: 1px solid {border};\n    border-radius: 4px;\n    overflow: hidden;',
                    'border: 3px solid {border};\n    border-radius: 8px;\n    overflow: hidden;\n    box-shadow: 5px 5px 0px {border};')

with open('src/app.py', 'w', encoding='utf-8') as f:
    f.write(text)
