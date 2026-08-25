import textwrap
import re

with open('src/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Add import if missing
if 'import textwrap' not in text:
    text = 'import textwrap\n' + text

# Replace multiline markdown calls
text = text.replace('st.markdown(f\"\"\"', 'st.markdown(textwrap.dedent(f\"\"\"')
text = text.replace('st.markdown(\"\"\"', 'st.markdown(textwrap.dedent(\"\"\"')

# Fix the closing tags
text = text.replace('\"\"\", unsafe_allow_html=True)', '\"\"\"), unsafe_allow_html=True)')

with open('src/app.py', 'w', encoding='utf-8') as f:
    f.write(text)
