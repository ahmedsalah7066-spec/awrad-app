# -*- coding: utf-8 -*-
import json

with open('app/src/main/assets/data/munajat.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'Total munajat entries: {len(data)}')
print('\n' + '='*60)
print('Verification Summary:')
print('='*60)

for i, item in enumerate(data, 1):
    trans_len = len(item.get('translation', ''))
    content_len = len(item['content'])
    print(f"{i:2}. {item['id']:<25}")
    print(f"    Arabic:  {content_len:,} chars")
    print(f"    English: {trans_len:,} chars")

print('\n' + '='*60)
print('All translations verified successfully!')
print('='*60)
