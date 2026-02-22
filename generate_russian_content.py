import json
import os

from data_ru_dalail import dalail_titles, dalail_translations
from data_ru_munajat import munajat_titles_ru, munajat_translations
from data_ru_hisn import hisn_translations_ru, hisn_titles_ru

def process_dalail():
    en_file = "app/src/main/assets/en/dalail.json"
    ru_file = "app/src/main/assets/ru/dalail.json"

    with open(en_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for period in data:
        day_id = period.get('id')
        if day_id and day_id in dalail_titles:
            period['title'] = dalail_titles[day_id]
            period['content'] = dalail_translations.get(day_id, period['content'])
            period['translation'] = ""

    os.makedirs(os.path.dirname(ru_file), exist_ok=True)
    with open(ru_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def process_munajat():
    en_file = "app/src/main/assets/en/munajat.json"
    ru_file = "app/src/main/assets/ru/munajat.json"

    with open(en_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        munajat_id = item.get('id')
        if munajat_id and munajat_id in munajat_titles_ru:
            item['title'] = munajat_titles_ru[munajat_id]
            item['content'] = munajat_translations.get(munajat_id, item['content'])
            item['translation'] = ""

    os.makedirs(os.path.dirname(ru_file), exist_ok=True)
    with open(ru_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def process_hisn():
    fr_file = "app/src/main/assets/fr/hisn.json"
    ru_file = "app/src/main/assets/ru/hisn.json"

    with open(fr_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for category in data:
        category_id = category.get('id')
        if category_id and category_id in hisn_titles_ru:
            category['title'] = hisn_titles_ru[category_id]
            
        for item in category.get('items', []):
            item_id = item.get('id')
            if item_id and item_id in hisn_translations_ru:
                ru_data = hisn_translations_ru[item_id]
                item['content'] = ru_data.get('content', item['content'])
                item['fadl'] = ru_data.get('fadl', item['fadl'])

    os.makedirs(os.path.dirname(ru_file), exist_ok=True)
    with open(ru_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    print("Generating Russian Dalail content...")
    process_dalail()
    print("Generating Russian Munajat content...")
    process_munajat()
    print("Generating Russian Hisn content...")
    process_hisn()
    print("Russian content generation complete!")
