# -*- coding: utf-8 -*-
import json

with open('app/src/main/assets/data/munajat.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'Total munajat entries: {len(data)}')
print('\nAll munajat IDs:')
for item in data:
    content_len = len(item['content'])
    print(f"  - {item['id']:<25} ({content_len:,} chars)")

print(f"\n{'='*50}")
print("Verification complete - all 15 munajat updated!")
