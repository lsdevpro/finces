import json
import os

input_path = r'C:\Users\52777\.gemini\antigravity\brain\7011d2a8-287a-45ed-be23-2a31577906c4\.system_generated\steps\4311\content.md'
output_path = 'categories_html.txt'

with open(input_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

json_str = [l for l in lines if l.strip().startswith('[')][0]
data = json.loads(json_str)

# Sort by name
data.sort(key=lambda x: x['name'].lower())

html_items = []
for c in data:
    html_items.append(f'                            <div class="m-dropdown-item" data-value="{c["category_id"]}">{c["name"]}</div>')

with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(html_items))
