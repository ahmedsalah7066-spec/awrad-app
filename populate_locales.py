
import json
import os
import sys

# Paths
BASE_DIR = "app/src/main/assets"
DATA_DIR = os.path.join(BASE_DIR, "data")
AR_DIR = os.path.join(BASE_DIR, "ar")
EN_DIR = os.path.join(BASE_DIR, "en")

# Mappings for Hisn Titles (since JSON only has resource IDs)
HISN_TITLES = {
    "hisn_morning": {"ar": "أذكار الصباح", "en": "Morning Athkar"},
    "hisn_evening": {"ar": "أذكار المساء", "en": "Evening Athkar"},
    "hisn_sleep": {"ar": "أذكار النوم", "en": "Sleep Athkar"},
    "hisn_prayer": {"ar": "أذكار الصلاة", "en": "Prayer Athkar"},
    "hisn_food": {"ar": "أذكار الطعام", "en": "Food Athkar"},
    "hisn_travel": {"ar": "أذكار السفر", "en": "Travel Athkar"},
    "hisn_mosque": {"ar": "أذكار المسجد", "en": "Mosque Athkar"}
}

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {path}")

def process_dalail():
    print("Processing Dalail...")
    source = load_json(os.path.join(DATA_DIR, "awrad.json"))
    
    ar_data = []
    en_data = []
    
    for item in source:
        # AR
        ar_item = {
            "id": item.get("id"),
            "title": item.get("title", ""),
            "content": item.get("content", ""),
            "type": item.get("type", "dua")
        }
        ar_data.append(ar_item)
        
        # EN
        en_item = {
            "id": item.get("id"),
            "title": item.get("title_en", ""),
            "content": item.get("translation", ""), # Map translation to content
            "type": item.get("type", "dua")
        }
        en_data.append(en_item)
        
    save_json(os.path.join(AR_DIR, "dalail.json"), ar_data)
    save_json(os.path.join(EN_DIR, "dalail.json"), en_data)

def process_munajat():
    print("Processing Munajat...")
    source = load_json(os.path.join(DATA_DIR, "munajat.json"))
    
    ar_data = []
    en_data = []
    
    for item in source:
        # AR
        ar_item = {
            "id": item.get("id"),
            "title": item.get("title", ""),
            "content": item.get("content", ""),
            "type": item.get("type", "dua")
        }
        ar_data.append(ar_item)
        
        # EN
        en_item = {
            "id": item.get("id"),
            "title": item.get("title_en", ""),
            "content": item.get("translation", ""), # Map translation to content
            "type": item.get("type", "dua")
        }
        en_data.append(en_item)

    save_json(os.path.join(AR_DIR, "munajat.json"), ar_data)
    save_json(os.path.join(EN_DIR, "munajat.json"), en_data)

def process_hisn():
    print("Processing Hisn...")
    source = load_json(os.path.join(DATA_DIR, "hisn.json"))
    
    ar_data = []
    en_data = []
    
    for cat in source:
        cat_id = cat.get("id")
        titles = HISN_TITLES.get(cat_id, {"ar": cat_id, "en": cat_id})
        
        # AR Category
        ar_cat = {
            "id": cat_id,
            "title": titles["ar"],
            "icon": cat.get("icon_res"),
            "items": []
        }
        
        # EN Category
        en_cat = {
            "id": cat_id,
            "title": titles["en"],
            "icon": cat.get("icon_res"),
            "items": []
        }
        
        for item in cat.get("items", []):
            # Common fields
            count = item.get("count", 1)
            item_id = item.get("id")
            
            # AR Item
            ar_item = {
                "id": item_id,
                "content": item.get("arabic", ""),
                "count": count,
                "fadl": item.get("fadl", {}).get("ar", "")
            }
            ar_cat["items"].append(ar_item)
            
            # EN Item
            # Some items might not have translation, so we check
            trans = item.get("translation", "")
            # If no translation, maybe we keep arabic or empty? 
            # For EN user, seeing Arabic is better than nothing, but let's stick to translation field.
            
            en_item = {
                "id": item_id,
                "content": trans,
                "count": count,
                "fadl": item.get("fadl", {}).get("en", "")
            }
            en_cat["items"].append(en_item)
            
        ar_data.append(ar_cat)
        en_data.append(en_cat)

    save_json(os.path.join(AR_DIR, "hisn.json"), ar_data)
    save_json(os.path.join(EN_DIR, "hisn.json"), en_data)

if __name__ == "__main__":
    process_dalail()
    process_munajat()
    process_hisn()
    print("Population complete.")
