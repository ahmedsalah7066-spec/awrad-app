import json

with open('app/src/main/assets/data/turkish_full_content.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Turkish full content contains key-value pairs of IDs -> text.
# For Dalail, it's 'awrad_saturday' -> text.
# For Munajat, it's 'munajat_1' -> text.
# We also need hisn content if it's there.

# 1. Create tr/dalail.json based on en/dalail.json
with open('app/src/main/assets/en/dalail.json', 'r', encoding='utf-8') as f:
    dalail = json.load(f)

for item in dalail:
    doc_id = item['id']
    if doc_id.startswith('dalail_'):
        doc_id = doc_id.replace('dalail_', 'awrad_') # Map to old keys used in turkish_full_content
        
    if doc_id in data:
        item['translation'] = data[doc_id]
        item['content'] = "" # Original logic for other langs puts Arabic in content or target in content?
        # Actually for 'id', 'uz', 'bn', the target language text goes into 'content' and 'translation' depends on design.
        # But wait, looking at my previous work, for non-Arabic non-English, 'content' is Arabic and 'translation' is target language.
        # Wait, the user specifically requested recently (for Turkish/English Hisn) that Quranic verses are in Arabic, rest in translation.
        # For Munajat/Dalail, 'content' is Arabic, 'translation' is Turkish right? Let's check en/dalail.json.
        
# For safety, let's just dump out the keys and a sample.
print(f"Total keys: {len(data)}")
dalail_keys = [k for k in data.keys() if 'awrad' in k]
munajat_keys = [k for k in data.keys() if 'munajat' in k]
hisn_keys = [k for k in data.keys() if not k.startswith('awrad') and not k.startswith('munajat')]

print(f"Dalail keys: {len(dalail_keys)}, Munajat keys: {len(munajat_keys)}, Other keys: {len(hisn_keys)}")

