#!/usr/bin/env python3
"""
Intelligent Content Extractor
Extracts Arabic content from DatabaseModule hardcoded data
"""

import firebase_admin
from firebase_admin import credentials, firestore
import re

def initialize_firebase():
    try:
        cred = credentials.Certificate("serviceAccountKey.json")
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except:
        return None

def read_file(filepath):
    """Read file with UTF-8 encoding"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"[ERROR] Could not read {filepath}: {e}")
        return None

def extract_hisn_categories():
    """Extract Hisn categories from HisnContent.kt"""
    print("\n[INFO] Extracting Hisn Al-Muslim categories...")
    
    # Based on the hierarchical structure we created
    categories_mapping = {
        "hisn_morning": 0,
        "hisn_evening": 1,
        "hisn_sleep": 2,
        "hisn_prayer": 3,
        "hisn_wakeup": 4,
        "hisn_quran": 5,
        "hisn_home": 6,
        "hisn_mosque": 7,
        "hisn_travel": 8,
        "hisn_various": 9,
    }
    
    return list(categories_mapping.keys())

def extract_munajat_list():
    """Extract Munajat from Munajat.kt"""
    print("\n[INFO] Extracting Munajat content...")
    
    filepath = "../app/src/main/java/com/example/awrad/Munajat.kt"
    content = read_file(filepath)
    
    if not content:
        return []
    
    # Find all Munajat(...) entries
    pattern = r'Munajat\(R\.string\.([^,]+),\s*"""(.*?)"""\)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    munajat_mapping = [
        ("munajat_zahidin", "munajat_ascetics"),
        ("munajat_raghibin", "munajat_seekers"),
        ("munajat_dhakirin", "munajat_rememberers"),
        ("munajat_arifin", "munajat_knowers"),
        ("munajat_muhibbin", "munajat_lovers"),
        ("munajat_muta", "munajat_worshippers"),  
        ("munajat_qa", "munajat_fearful"),
        ("munajat_shak", "munajat_grateful"),
        ("munajat_mush", "munajat_longing"),
        ("munajat_mukhbitin", "munajat_sincere"),
        ("munajat_muhsin", "munajat_virtuous"),
        ("munajat_mutawakkil", "munajat_hopeful"),
        ("munajat_taabbin", "munajat_repentant"),
        ("munajat_mutashakkictin", "munajat_complaining"),
        ("munajat_mumineen", "munajat_believers"),
    ]
    
    duas = []
    for idx, (res_id, arabic_text) in enumerate(matches):
        # Map to correct category
        category_id = f"munajat_{idx}" if idx < len(munajat_mapping) else "munajat_believers"
        
        # Clean category ID
        for old, new in munajat_mapping:
            if old in res_id or res_id in old:
                category_id = new
                break
        
        duas.append({
            "categoryId": category_id,
            "arabicText": arabic_text.strip(),
            "count": 1,
            "orderIndex": 0
        })
    
    print(f"[OK] Found {len(duas)} Munajat")
    return duas

def extract_awrad_list():
    """Extract Awrad (Dalail) from Awrad.kt"""
    print("\n[INFO] Extracting Dalail Al-Khayrat content...")
    
    filepath = "../app/src/main/java/com/example/awrad/Awrad.kt"
    content = read_file(filepath)
    
    if not content:
        return []
    
    # Find all Awrad(...) entries
    pattern = r'Awrad\(R\.string\.dalail_([^,]+),\s*"""(.*?)"""\)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    days = ["saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday"]
    
    duas = []
    for idx, (day_name, arabic_text) in enumerate(matches):
        if idx < len(days):
            category_id = f"dalail_{days[idx]}"
        else:
            category_id = "dalail_saturday"
        
        duas.append({
            "categoryId": category_id,
            "arabicText": arabic_text.strip(),
            "count": 1,
            "orderIndex": 0
        })
    
    print(f"[OK] Found {len(duas)} Dalail")
    return duas

def upload_complete_content(db):
    """Upload all content to Firebase"""
    print("\n[INFO] Starting full content upload...")
    
    # Extract content
    munajat = extract_munajat_list()
    awrad = extract_awrad_list()
    
    # Upload Munajat
    print("\n[INFO] Uploading Munajat...")
    for dua in munajat:
        db.collection("duas").add(dua)
    print(f"[OK] Uploaded {len(munajat)} Munajat")
    
    # Upload Dalail
    print("\n[INFO] Uploading Dalail...")
    for dua in awrad:
        db.collection("duas").add(dua)
    print(f"[OK] Uploaded {len(awrad)} Dalail")
    
    # For Hisn, we need the actual data from HisnContent.kt
    # Since it's complex, we'll add just structure for now
    print("\n[INFO] Note: Hisn content requires manual extraction")
    print("    Run the app and use RoomToJsonExporter for full content")
    
    print(f"\n[SUCCESS] Uploaded {len(munajat) + len(awrad)} duas total")

def main():
    print("=" * 60)
    print("Complete Content Upload")
    print("=" * 60)
    
    db = initialize_firebase()
    if not db:
        print("[ERROR] Failed to initialize Firebase")
        return
    
    print("[OK] Firebase initialized")
    
    response = input("\nContinue with upload? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("[INFO] Cancelled")
        return
    
    upload_complete_content(db)
    
    print("\n" + "=" * 60)
    print("[DONE]")
    print("=" * 60)

if __name__ == "__main__":
    main()
