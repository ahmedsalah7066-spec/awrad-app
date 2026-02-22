# -*- coding: utf-8 -*-
import json

# 1. DALAIL AL-KHAYRAT (AWRAD.JSON)
with open('app/src/main/assets/data/awrad.json', 'r', encoding='utf-8') as f:
    arabic_awrad = json.load(f)

day_names = ["saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday"]
day_titles = ["1. ہفتہ کا ورد", "2. اتوار کا ورد", "3. پیر کا ورد", "4. منگل کا ورد", "5. بدھ کا ورد", "6. جمعرات کا ورد", "7. جمعہ کا ورد"]

urdu_awrad = []
for i, day_data in enumerate(arabic_awrad):
    urdu_awrad.append({
        "id": day_data["id"],
        "day": day_data["day"],
        "type": "dua",
        "title": day_titles[i],
        "title_en": day_data["title_en"],
        "content": day_data["content"],
        "translation": day_data["translation"]
    })

with open('app/src/main/assets/ur/awrad.json', 'w', encoding='utf-8') as f:
    json.dump(urdu_awrad, f, ensure_ascii=False, indent=2)
print(f"Created awrad.json: {len(urdu_awrad)} days")

# 2. HISN AL-MUSLIM (HISN.JSON)  
with open('app/src/main/assets/data/hisn.json', 'r', encoding='utf-8') as f:
    arabic_hisn = json.load(f)

cat_titles = {
    "hisn_morning": "صبح کے اذکار",
    "hisn_evening": "شام کے اذکار",
    "hisn_sleep": "سونے کے اذکار",
    "hisn_prayer": "نماز کے بعد کے اذکار",
    "hisn_food": "کھانے کی دعائیں",
    "hisn_travel": "سفر کی دعائیں",
    "hisn_mosque": "مسجد کی دعائیں"
}

urdu_hisn = []
total = 0
for category in arabic_hisn:
    cat_id = category["id"]
    items = []
    for item in category["items"]:
        items.append({
            "id": item["id"],
            "arabic": item["arabic"],
            "translation": item.get("translation", ""),
            "fadl": item.get("fadl", {}),
            "categoryId": item.get("categoryId", ""),
            "orderIndex": item.get("orderIndex", 0),
            "count": item.get("count", 1)
        })
        total += 1
    urdu_hisn.append({
        "id": cat_id,
        "title_res": category["title_res"],
        "icon_res": category["icon_res"],
        "title": cat_titles.get(cat_id, ""),
        "items": items
    })

with open('app/src/main/assets/ur/hisn.json', 'w', encoding='utf-8') as f:
    json.dump(urdu_hisn, f, ensure_ascii=False, indent=2)
print(f"Created hisn.json: {len(urdu_hisn)} categories, {total} items")
print("SUCCESS: All Urdu content files created!")
