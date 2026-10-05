import os
import re

# 1. Read templates/index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 2. Replace absolute static paths with relative paths
# e.g., href="/static/... -> href="./static/...
# src="/static/... -> src="./static/...
html_static = re.sub(r'href=["\']/static/', 'href="./static/', html)
html_static = re.sub(r'src=["\']/static/', 'src="./static/', html_static)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_static)

# Also create a docs/ directory copy if user selects /docs in GitHub Pages
os.makedirs('docs', exist_ok=True)
with open('docs/index.html', 'w', encoding='utf-8') as f:
    # in docs, static is in ../static or we can copy static to docs/static
    pass

print(f"Generated root index.html ({len(html_static)} bytes)")
