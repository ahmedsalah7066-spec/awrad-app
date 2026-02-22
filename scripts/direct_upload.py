#!/usr/bin/env python3
"""
Direct Firebase Upload - Uploads Arabic content directly to Firestore
Uses the existing hardcoded data structure
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
        print("Please place the file in the scripts/ directory")
        return None
    except Exception as e:
        print(f"[ERROR] Firebase initialization failed: {e}")
        return None

def upload_sample_data(db):
    """Upload sample Arabic content to demonstrate structure"""
    print("\n[INFO] Uploading sample data to Firestore...")
    
    # Upload Categories
    print("[INFO] Creating categories...")
    categories_data = [
        {"id": "morning", "titleResId": "hisn_morning", "iconResId": 0, "orderIndex": 0, "type": "hisn"},
        {"id": "evening", "titleResId": "hisn_evening", "iconResId": 0, "orderIndex": 1, "type": "hisn"},
        {"id": "sleep", "titleResId": "hisn_sleep", "iconResId": 0, "orderIndex": 2, "type": "hisn"},
        {"id": "prayer", "titleResId": "hisn_prayer", "iconResId": 0, "orderIndex": 3, "type": "hisn"},
        {"id": "munajat", "titleResId": "munajat_title", "iconResId": 0, "orderIndex": 100, "type": "munajat"},
        {"id": "awrad", "titleResId": "dalail_title", "iconResId": 0, "orderIndex": 101, "type": "awrad"},
        {"id": "daily_essentials", "titleResId": "daily_essentials_title", "iconResId": 0, "orderIndex": 102, "type": "essential"},
    ]
    
    batch = db.batch()
    for cat_data in categories_data:
        cat_id = cat_data.pop("id")
        doc_ref = db.collection("categories").document(cat_id)
        batch.set(doc_ref, cat_data)
    batch.commit()
    print(f"[OK] Created {len(categories_data)} categories")
    
    # Upload Sample Duas (Daily Essentials)
    print("[INFO] Creating Daily Essentials...")
    
    istiftah_text = """اللَّهُمَّ بَاعِدْ بَيْنِي وَبَيْنَ خَطَايَايَ كَمَا بَاعَدْتَ بَيْنَ الْمَشْرِقِ وَ الْمَغْرِبِ، اللَّهُمَّ نَقِّنِي مِنَ الْخَطَايَا كَمَا يُنَقَّى الثَّوْبُ الأَبْيَضُ مِنَ الدَّنَسِ، اللَّهُمَّ اغْسِلْ خَطَايَايَ بِالْمَاءِ وَالثَّلْجِ وَالْبَرَدِ"""
    
    ibrahimi_text = """اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ وَعَلَى آلِ مُحَمَّدٍ كَمَا صَلَّيْتَ عَلَى إِبْرَاهِيمَ وَعَلَى آلِ إِبْرَاهِيمَ إِنَّكَ حَمِيدٌ مَجِيدٌ، اللَّهُمَّ بَارِكْ عَلَى مُحَمَّدٍ وَعَلَى آلِ مُحَمَّدٍ كَمَا بَارَكْتَ عَلَى إِبْرَاهِيمَ وَعَلَى آلِ إِبْرَاهِيمَ إِنَّكَ حَمِيدٌ مَجِيدٌ"""
    
    daily_duas = [
        {
            "categoryId": "daily_essentials",
            "title": "دعاء الاستفتاح",
            "arabicText": istiftah_text,
            "count": 1,
            "orderIndex": 0
        },
        {
            "categoryId": "daily_essentials",
            "title": "الصلاة الإبراهيمية",
            "arabicText": ibrahimi_text,
            "count": 1,
            "orderIndex": 1
        }
    ]
    
    for dua in daily_duas:
        db.collection("duas").add(dua)
    print(f"[OK] Created {len(daily_duas)} Daily Essentials")
    
    # Upload Sample Morning Adhkar
    print("[INFO] Creating sample Morning Adhkar...")
    
    ayatul_kursi = """أَعُوذُ بِاللَّهِ مِنَ الشَّيْطَانِ الرَّجِيمِ
بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ
اللَّهُ لَا إِلَهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ لَهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ مَنْ ذَا الَّذِي يَشْفَعُ عِنْدَهُ إِلَّا بِإِذْنِهِ يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ وَلَا يُحِيطُونَ بِشَيْءٍ مِنْ عِلْمِهِ إِلَّا بِمَا شَاءَ وَسِعَ كُرْسِيُّهُ السَّمَاوَاتِ وَالْأَرْضَ وَلَا يَئُودُهُ حِفْظُهُمَا وَهُوَ الْعَلِيُّ الْعَظِيمُ"""
    
    morning_sample = [
        {
            "categoryId": "morning",
            "arabicText": ayatul_kursi,
            "count": 1,
            "orderIndex": 0,
            "fadlArabic": "من قالها حين يصبح أجير من الجن حتى يمسي ومن قالها حين يمسي أجير من الجن حتى يصبح."
        }
    ]
    
    for dua in morning_sample:
        db.collection("duas").add(dua)
    print(f"[OK] Created {len(morning_sample)} Morning Adhkar samples")
    
    # Upload Metadata
    print("[INFO] Creating metadata...")
    metadata = {
        "latestDataVersion": "1.0.0",
        "lastUpdated": firestore.SERVER_TIMESTAMP,
        "availableLanguages": ["ar"],
        "minAppVersion": "2.3.2",
        "dataSource": "Local hardcoded content",
        "uploadedAt": datetime.now().isoformat()
    }
    db.collection("metadata").document("app_info").set(metadata)
    print("[OK] Created metadata")
    
    print("\n[SUCCESS] Sample data uploaded successfully!")
    print("\n[NOTE] This is sample data only.")
    print("To upload full content:")
    print("1. Run the app on Android device/emulator")
    print("2. Use the Export button in Settings")
    print("3. Copy exported JSON files to firebase_data_export/")
    print("4. Run upload_to_firebase.py")

def verify_upload(db):
    """Verify data was uploaded correctly"""
    print("\n[INFO] Verifying data...")
    
    categories = db.collection("categories").get()
    print(f"[OK] Found {len(categories)} categories")
    
    duas = db.collection("duas").limit(10).get()
    print(f"[OK] Found {len(duas)} duas (showing first 10)")
    
    metadata = db.collection("metadata").document("app_info").get()
    if metadata.exists:
        print("[OK] Metadata exists")
        data = metadata.to_dict()
        print(f"    - Version: {data.get('latestDataVersion')}")
        print(f"    - Languages: {data.get('availableLanguages')}")
    
    print("\n[INFO] Firestore Console URL:")
    print(f"https://console.firebase.google.com/project/awrad-7da3e/firestore")

def main():
    print("=" * 60)
    print("Direct Firebase Upload")
    print("=" * 60)
    
    db = initialize_firebase()
    if not db:
        return
    
    print("[OK] Firebase initialized")
    print("[INFO] Project: awrad-7da3e")
    print("[INFO] Database: (default)")
    
    # Ask for confirmation
    print("\n[WARNING] This will upload sample data to Firestore")
    response = input("Continue? (yes/no): ").strip().lower()
    
    if response not in ['yes', 'y']:
        print("[INFO] Upload cancelled")
        return
    
    # Upload data
    upload_sample_data(db)
    
    # Verify
    verify_upload(db)
    
    print("\n" + "=" * 60)
    print("[DONE] Upload complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Check Firestore Console to verify data")
    print("2. Update Android app to read from Firestore")
    print("3. Test the app with Firebase data")

if __name__ == "__main__":
    main()
