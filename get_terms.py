import re

with open('D:/PROJECT/PASARKU/proposal.html', 'r', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'(<ol class="terms-list">.*?</ol>)', text, re.DOTALL)
if match:
    print(match.group(1)[:500])
else:
    print("Not found ol terms")
