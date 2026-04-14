import re

with open('D:/PROJECT/PASARKU/proposal.html', 'r', encoding='utf-8') as f:
    text = f.read()

match3 = re.search(r'(\.terms-list\s+li::before\b.*?})', text, re.DOTALL)
if match3:
    print(match3.group(1))

