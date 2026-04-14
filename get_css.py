import re

with open('D:/PROJECT/PASARKU/proposal.html', 'r', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'(\.terms-list\b.*?})', text, re.DOTALL)
if match:
    print(match.group(1))
match2 = re.search(r'(\.terms-list\s+li\b.*?})', text, re.DOTALL)
if match2:
    print(match2.group(1))

