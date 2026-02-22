import json
import os

# Create tr directory if not exists
os.makedirs('app/src/main/assets/tr', exist_ok=True)

# 1. Load turkish translations
with open('app/src/main/assets/data/turkish_full_content.json', 'r', encoding='utf-8') as f:
    tr_data = json.load(f)

# 2. Dalail
with open('app/src/main/assets/en/dalail.json', 'r', encoding='utf-8') as f:
    dalail_base = json.load(f)
with open('app/src/main/assets/ar/dalail.json', 'r', encoding='utf-8') as f:
    dalail_ar = json.load(f)

for item, item_ar in zip(dalail_base, dalail_ar):
    doc_id = item['id']
    if not doc_id.startswith('awrad_'):
        tr_key = 'awrad_' + doc_id
    else:
        tr_key = doc_id
    
    # We want Arabic content, Turkish translation
    item['content'] = item_ar.get('content', '')
    if tr_key in tr_data:
        item['translation'] = tr_data[tr_key]
    else:
        item['translation'] = ""

with open('app/src/main/assets/tr/dalail.json', 'w', encoding='utf-8') as f:
    json.dump(dalail_base, f, ensure_ascii=False, indent=2)

# 3. Munajat
with open('app/src/main/assets/en/munajat.json', 'r', encoding='utf-8') as f:
    munajat_base = json.load(f)
with open('app/src/main/assets/ar/munajat.json', 'r', encoding='utf-8') as f:
    munajat_ar = json.load(f)

for item, item_ar in zip(munajat_base, munajat_ar):
    doc_id = item['id'] # e.g. munajat_1
    
    # We want Arabic content, Turkish translation
    item['content'] = item_ar.get('content', '')
    if doc_id in tr_data:
        item['translation'] = tr_data[doc_id]
    else:
        item['translation'] = ""

with open('app/src/main/assets/tr/munajat.json', 'w', encoding='utf-8') as f:
    json.dump(munajat_base, f, ensure_ascii=False, indent=2)

print("Successfully generated tr/dalail.json and tr/munajat.json")
