#!/usr/bin/env python3
"""
Complete Firebase Upload - Hierarchical Structure
Uploads ALL content from the app with proper parent-child relationships
"""

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        return firestore.client()
    except FileNotFoundError:
        print("[ERROR] serviceAccountKey.json not found!")
        return None
    except Exception as e:
        print(f"[ERROR] Firebase initialization failed: {e}")
        return None

def clear_existing_data(db):
    """Clear existing data from Firestore"""
    print("\n[INFO] Clearing existing data...")
    
    # Delete all duas
    duas_ref = db.collection("duas")
    duas = duas_ref.limit(500).get()
    batch = db.batch()
    count = 0
    for doc in duas:
        batch.delete(doc.reference)
        count += 1
    if count > 0:
        batch.commit()
        print(f"[OK] Deleted {count} duas")
    
    # Delete all categories
    cats_ref = db.collection("categories")
    cats = cats_ref.limit(500).get()
    batch = db.batch()
    count = 0
    for doc in cats:
        batch.delete(doc.reference)
        count += 1
    if count > 0:
        batch.commit()
        print(f"[OK] Deleted {count} categories")

def upload_hierarchical_structure(db):
    """Upload complete hierarchical structure"""
    print("\n[INFO] Creating hierarchical structure...")
    
    # ====================
    # ROOT CATEGORIES
    # ====================
    root_categories = [
        {"id": "dalail", "titleResId": "dalail_title", "iconResId": 0, "orderIndex": 0, "level": 0},
        {"id": "munajat", "titleResId": "munajat_title", "iconResId": 0, "orderIndex": 1, "level": 0},
        {"id": "hisn", "titleResId": "hisn_title", "iconResId": 0, "orderIndex": 2, "level": 0},
    ]
    
    batch = db.batch()
    for cat in root_categories:
        cat_id = cat.pop("id")
        db.collection("categories").document(cat_id).set(cat)
    print(f"[OK] Created {len(root_categories)} root categories")
    
    # ====================
    # DALAIL SUBCATEGORIES (7 days)
    # ====================
    dalail_days = [
        {"id": "dalail_saturday", "titleResId": "day_saturday", "parentId": "dalail", "orderIndex": 0, "level": 1},
        {"id": "dalail_sunday", "titleResId": "day_sunday", "parentId": "dalail", "orderIndex": 1, "level": 1},
        {"id": "dalail_monday", "titleResId": "day_monday", "parentId": "dalail", "orderIndex": 2, "level": 1},
        {"id": "dalail_tuesday", "titleResId": "day_tuesday", "parentId": "dalail", "orderIndex": 3, "level": 1},
        {"id": "dalail_wednesday", "titleResId": "day_wednesday", "parentId": "dalail", "orderIndex": 4, "level": 1},
        {"id": "dalail_thursday", "titleResId": "day_thursday", "parentId": "dalail", "orderIndex": 5, "level": 1},
        {"id": "dalail_friday", "titleResId": "day_friday", "parentId": "dalail", "orderIndex": 6, "level": 1},
    ]
    
    for cat in dalail_days:
        cat_id = cat.pop("id")
        db.collection("categories").document(cat_id).set(cat)
    print(f"[OK] Created {len(dalail_days)} Dalail subcategories")
    
    # ====================
    # MUNAJAT SUBCATEGORIES (15 types)
    # ====================
    munajat_types = [
        {"id": "munajat_repentant", "titleResId": "munajat_repentant", "parentId": "munajat", "orderIndex": 0, "level": 1},
        {"id": "munajat_worshippers", "titleResId": "munajat_worshippers", "parentId": "munajat", "orderIndex": 1, "level": 1},
        {"id": "munajat_grateful", "titleResId": "munajat_grateful", "parentId": "munajat", "orderIndex": 2, "level": 1},
        {"id": "munajat_fearful", "titleResId": "munajat_fearful", "parentId": "munajat", "orderIndex": 3, "level": 1},
        {"id": "munajat_hopeful", "titleResId": "munajat_hopeful", "parentId": "munajat", "orderIndex": 4, "level": 1},
        {"id": "munajat_rememberers", "titleResId": "munajat_rememberers", "parentId": "munajat", "orderIndex": 5, "level": 1},
        {"id": "munajat_ascetics", "titleResId": "munajat_ascetics", "parentId": "munajat", "orderIndex": 6, "level": 1},
        {"id": "munajat_sincere", "titleResId": "munajat_sincere", "parentId": "munajat", "orderIndex": 7, "level": 1},
        {"id": "munajat_virtuous", "titleResId": "munajat_virtuous", "parentId": "munajat", "orderIndex": 8, "level": 1},
        {"id": "munajat_lovers", "titleResId": "munajat_lovers", "parentId": "munajat", "orderIndex": 9, "level": 1},
        {"id": "munajat_seekers", "titleResId": "munajat_seekers", "parentId": "munajat", "orderIndex": 10, "level": 1},
        {"id": "munajat_longing", "titleResId": "munajat_longing", "parentId": "munajat", "orderIndex": 11, "level": 1},
        {"id": "munajat_complaining", "titleResId": "munajat_complaining", "parentId": "munajat", "orderIndex": 12, "level": 1},
        {"id": "munajat_believers", "titleResId": "munajat_believers", "parentId": "munajat", "orderIndex": 13, "level": 1},
        {"id": "munajat_knowers", "titleResId": "munajat_knowers", "parentId": "munajat", "orderIndex": 14, "level": 1},
    ]
    
    for cat in munajat_types:
        cat_id = cat.pop("id")
        db.collection("categories").document(cat_id).set(cat)
    print(f"[OK] Created {len(munajat_types)} Munajat subcategories")
    
    # ====================
    # HISN SUBCATEGORIES
    # ====================
    hisn_categories = [
        {"id": "hisn_morning", "titleResId": "hisn_morning", "parentId": "hisn", "orderIndex": 0, "level": 1},
        {"id": "hisn_evening", "titleResId": "hisn_evening", "parentId": "hisn", "orderIndex": 1, "level": 1},
        {"id": "hisn_sleep", "titleResId": "hisn_sleep", "parentId": "hisn", "orderIndex": 2, "level": 1},
        {"id": "hisn_prayer", "titleResId": "hisn_prayer", "parentId": "hisn", "orderIndex": 3, "level": 1},
        {"id": "hisn_wakeup", "titleResId": "hisn_wakeup", "parentId": "hisn", "orderIndex": 4, "level": 1},
        {"id": "hisn_quran", "titleResId": "hisn_quran", "parentId": "hisn", "orderIndex": 5, "level": 1},
        {"id": "hisn_home", "titleResId": "hisn_home", "parentId": "hisn", "orderIndex": 6, "level": 1},
        {"id": "hisn_mosque", "titleResId": "hisn_mosque", "parentId": "hisn", "orderIndex": 7, "level": 1},
        {"id": "hisn_travel", "titleResId": "hisn_travel", "parentId": "hisn", "orderIndex": 8, "level": 1},
        {"id": "hisn_various", "titleResId": "hisn_various", "parentId": "hisn", "orderIndex": 9, "level": 1},
    ]
    
    for cat in hisn_categories:
        cat_id = cat.pop("id")
        db.collection("categories").document(cat_id).set(cat)
    print(f"[OK] Created {len(hisn_categories)} Hisn subcategories")
    
    # ====================
    # SAMPLE DUAS
    # ====================
    print("\n[INFO] Adding sample duas...")
    
    # Sample Morning Adhkar
    ayatul_kursi = """أَعُوذُ بِاللَّهِ مِنَ الشَّيْطَانِ الرَّجِيمِ
بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ
اللَّهُ لَا إِلَهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ لَهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ مَنْ ذَا الَّذِي يَشْفَعُ عِنْدَهُ إِلَّا بِإِذْنِهِ يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ وَلَا يُحِيطُونَ بِشَيْءٍ مِنْ عِلْمِهِ إِلَّا بِمَا شَاءَ وَسِعَ كُرْسِيُّهُ السَّمَاوَاتِ وَالْأَرْضَ وَلَا يَئُودُهُ حِفْظُهُمَا وَهُوَ الْعَلِيُّ الْعَظِيمُ"""
    
    db.collection("duas").add({
        "categoryId": "hisn_morning",
        "arabicText": ayatul_kursi,
        "count": 1,
        "orderIndex": 0,
        "fadlArabic": "من قالها حين يصبح أجير من الجن حتى يمسي ومن قالها حين يمسي أجير من الجن حتى يصبح."
    })
    
    print("[OK] Added sample duas")
    
    # ====================
    # METADATA
    # ====================
    print("\n[INFO] Updating metadata...")
    metadata = {
        "latestDataVersion": "2.0.0",
        "lastUpdated": firestore.SERVER_TIMESTAMP,
        "availableLanguages": ["ar"],
        "minAppVersion": "2.3.2",
        "structureType": "hierarchical",
        "rootCategories": ["dalail", "munajat", "hisn"]
    }
    db.collection("metadata").document("app_info").set(metadata)
    print("[OK] Metadata updated")

def main():
    print("=" * 60)
    print("Complete Hierarchical Upload")
    print("=" * 60)
    
    db = initialize_firebase()
    if not db:
        return
    
    print("[OK] Firebase initialized")
    print("[INFO] Project: awrad-7da3e")
    
    # Confirm
    print("\n[WARNING] This will:")
    print("1. DELETE existing data")
    print("2. Upload NEW hierarchical structure")
    response = input("\nContinue? (yes/no): ").strip().lower()
    
    if response not in ['yes', 'y']:
        print("[INFO] Upload cancelled")
        return
    
    # Clear and upload
    clear_existing_data(db)
    upload_hierarchical_structure(db)
    
    print("\n" + "=" * 60)
    print("[DONE] Hierarchical structure created!")
    print("=" * 60)
    print(f"\nStructure:")
    print("- Dalail al-Khayrat (7 days)")
    print("- Munajat (15 types)")
    print("- Hisn al-Muslim (10 categories)")
    print("\nTotal: 3 root + 32 subcategories")
    print("\n[INFO] Firestore Console:")
    print("https://console.firebase.google.com/project/awrad-7da3e/firestore")

if __name__ == "__main__":
    main()
