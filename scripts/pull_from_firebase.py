#!/usr/bin/env python3
"""
Firebase Complete Data Puller
Downloads ALL content from Firebase Firestore and updates local assets/data/ JSON files.
"""

import json
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

def initialize_firebase():
    try:
        key_path = Path("serviceAccountKey.json")
        if not key_path.exists():
            key_path = Path("../serviceAccountKey.json")
        
        if not key_path.exists():
            print("Error: serviceAccountKey.json not found!")
            return None
            
        cred = credentials.Certificate(str(key_path))
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        return None

def pull_all_data():
    db = initialize_firebase()
    if not db:
        return

    # Days mapping for ordering
    days_order = {
        "saturday": 0, "sunday": 1, "monday": 2, "tuesday": 3, 
        "wednesday": 4, "thursday": 5, "friday": 6
    }

    # Output path
    base_path = Path("app/src/main/assets/data")
    if not base_path.exists():
        base_path = Path("../app/src/main/assets/data")

    print("=" * 60)
    print("PULLING ALL DATA FROM FIREBASE")
    print("=" * 60)

    # 1. Pull Daily Awrad (Dalail al-Khayrat)
    print("\n[1/4] Fetching 'daily_awrad' collection...")
    
    # Arabic titles for each day
    dalail_titles = {
        "saturday": "صلوات يوم السبت",
        "sunday": "صلوات يوم الأحد",
        "monday": "صلوات يوم الإثنين",
        "tuesday": "صلوات يوم الثلاثاء",
        "wednesday": "صلوات يوم الأربعاء",
        "thursday": "صلوات يوم الخميس",
        "friday": "صلوات يوم الجمعة"
    }
    
    awrad_list = []
    awrad_ref = db.collection("daily_awrad")
    for doc in awrad_ref.stream():
        data = doc.to_dict()
        doc_id = data.get("id", "")  # Might be "saturday" or "dalail_saturday"
        
        # Extract day_name (remove dalail_ if present)
        if doc_id.startswith("dalail_"):
            day_name = doc_id.replace("dalail_", "")
        else:
            day_name = doc_id
            
        # Get title from Firebase, or use our mapping
        title = data.get("title") or dalail_titles.get(day_name, f"صلوات يوم {day_name}")
        
        awrad_list.append({
            "id": day_name,
            "day": day_name,
            "title": title,  # Add title field!
            "content": data.get("content", ""),
            "translation": data.get("translation", ""),
            "type": "dua"
        })
    awrad_list.sort(key=lambda x: days_order.get(x["day"], 99))
    print(f"   Downloaded {len(awrad_list)} awrad items")




    # 2. Pull Munajat
    print("\n[2/4] Fetching 'munajat' collection...")
    
    # Munajat ID mapping: Firebase numeric IDs to string resource names
    munajat_id_map = {
        "munajat_1": ("munajat_muftaqirin", 1),
        "munajat_2": ("munajat_mutawassilin", 2),
        "munajat_3": ("munajat_muhibbin", 3),
        "munajat_4": ("munajat_muridin", 4),
        "munajat_5": ("munajat_dhakirin", 5),
        "munajat_6": ("munajat_raghibin_1", 6),
        "munajat_7": ("munajat_mutiin", 7),
        "munajat_8": ("munajat_zahidin", 8),
        "munajat_9": ("munajat_arifin", 9),
        "munajat_10": ("munajat_shakirin", 10),
        "munajat_11": ("munajat_rajin", 11),
        "munajat_12": ("munajat_raghibin_2", 12),
        "munajat_13": ("munajat_khaifin", 13),
        "munajat_14": ("munajat_shakin", 14),
        "munajat_15": ("munajat_taibin", 15)
    }
    
    munajat_list = []
    munajat_ref = db.collection("munajat")
    for doc in munajat_ref.stream():
        data = doc.to_dict()
        original_id = data.get("id", "")
        
        # Map to correct resource ID and get order
        if original_id in munajat_id_map:
            mapped_id, order = munajat_id_map[original_id]
        else:
            # Fallback: keep original ID
            mapped_id = original_id
            order = 99
            
        munajat_list.append({
            "id": mapped_id,
            "content": data.get("content", ""),
            "translation": data.get("translation", ""),
            "type": "dua",
            "_order": order  # Temporary field for sorting
        })
    
    # Sort by order
    munajat_list.sort(key=lambda x: x.get("_order", 99))
    
    # Remove temporary order field
    for item in munajat_list:
        item.pop("_order", None)
        
    print(f"   Downloaded {len(munajat_list)} munajat items")

    # 3. Pull Static Content (Istiftah, Ibrahimi)
    print("\n[3/4] Fetching 'static_content' collection...")
    static_list = []
    static_ref = db.collection("static_content")
    for doc in static_ref.stream():
        data = doc.to_dict()
        static_list.append({
            "id": data.get("id", ""),
            "content": data.get("content", ""),
            "translation": data.get("translation", "")
        })
    print(f"   Downloaded {len(static_list)} static items")

    # 4. Pull Hisn items
    print("\n[4/4] Fetching 'hisn_items' collection...")
    hisn_list = []
    hisn_ref = db.collection("hisn_items")
    for doc in hisn_ref.stream():
        data = doc.to_dict()
        hisn_list.append(data)
    print(f"   Downloaded {len(hisn_list)} hisn items")

    # Save all files
    print("\n" + "=" * 60)
    print("SAVING FILES")
    print("=" * 60)

    if awrad_list:
        awrad_path = base_path / "awrad.json"
        with open(awrad_path, "w", encoding="utf-8") as f:
            json.dump(awrad_list, f, ensure_ascii=False, indent=2)
        print(f"[SAVED] {awrad_path} ({len(awrad_list)} items)")

    if munajat_list:
        munajat_path = base_path / "munajat.json"
        with open(munajat_path, "w", encoding="utf-8") as f:
            json.dump(munajat_list, f, ensure_ascii=False, indent=2)
        print(f"[SAVED] {munajat_path} ({len(munajat_list)} items)")

    if static_list:
        static_path = base_path / "static.json"
        with open(static_path, "w", encoding="utf-8") as f:
            json.dump(static_list, f, ensure_ascii=False, indent=2)
        print(f"[SAVED] {static_path} ({len(static_list)} items)")

    if hisn_list:
        hisn_path = base_path / "hisn.json"
        with open(hisn_path, "w", encoding="utf-8") as f:
            json.dump(hisn_list, f, ensure_ascii=False, indent=2)
        print(f"[SAVED] {hisn_path} ({len(hisn_list)} items)")

    print("\n" + "=" * 60)
    print("SYNC COMPLETE!")
    print("=" * 60)
    print(f"\nTotal synced: {len(awrad_list) + len(munajat_list) + len(static_list) + len(hisn_list)} items")

if __name__ == "__main__":
    pull_all_data()
