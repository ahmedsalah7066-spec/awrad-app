#!/usr/bin/env python3
"""
Firebase Data Uploader
Uploads the exported JSON data to Firebase Firestore
Requires: pip install firebase-admin
"""

import json
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

# Initialize Firebase Admin SDK
# Note: You need to download service account key from Firebase Console
# Project Settings > Service Accounts > Generate New Private Key
def initialize_firebase():
    try:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        return firestore.client()
    except FileNotFoundError:
        print("❌ Error: serviceAccountKey.json not found!")
        print("Please download it from Firebase Console:")
        print("Project Settings > Service Accounts > Generate New Private Key")
        exit(1)

def upload_categories(db, data_dir):
    """Upload categories to Firestore"""
    print("\n📁 Uploading categories...")
    
    with open(data_dir / "categories.json", "r", encoding="utf-8") as f:
        categories = json.load(f)
    
    batch = db.batch()
    count = 0
    
    for category in categories:
        cat_id = category.pop("id")  # Remove id from data
        doc_ref = db.collection("categories").document(cat_id)
        batch.set(doc_ref, category)
        count += 1
        
        if count % 500 == 0:  # Firestore batch limit is 500
            batch.commit()
            batch = db.batch()
            print(f"   Uploaded {count} categories...")
    
    batch.commit()
    print(f"✅ Successfully uploaded {count} categories")

def upload_duas(db, data_dir, filename, collection_name="duas"):
    """Upload duas to Firestore"""
    print(f"\n📖 Uploading {filename}...")
    
    with open(data_dir / filename, "r", encoding="utf-8") as f:
        duas = json.load(f)
    
    batch = db.batch()
    count = 0
    
    for dua in duas:
        # Generate auto-ID or use provided ID
        if "id" in dua:
            doc_id = str(dua.pop("id"))
            doc_ref = db.collection(collection_name).document(doc_id)
        else:
            doc_ref = db.collection(collection_name).document()
        
        # Handle translations subcollection if exists
        translations = dua.pop("translations", None)
        
        batch.set(doc_ref, dua)
        count += 1
        
        # Add translations as subcollection
        if translations:
            for lang_code, translation in translations.items():
                trans_ref = doc_ref.collection("translations").document(lang_code)
                batch.set(trans_ref, translation)
        
        if count % 400 == 0:  # Leave room for translations
            batch.commit()
            batch = db.batch()
            print(f"   Uploaded {count} duas...")
    
    batch.commit()
    print(f"✅ Successfully uploaded {count} duas from {filename}")

def upload_metadata(db):
    """Upload app metadata"""
    print("\n⚙️ Uploading metadata...")
    
    metadata = {
        "latestDataVersion": "1.0.0",
        "lastUpdated": firestore.SERVER_TIMESTAMP,
        "availableLanguages": ["ar", "en", "ur", "hi", "ml"],
        "minAppVersion": "2.3.2"
    }
    
    db.collection("metadata").document("app_info").set(metadata)
    print("✅ Successfully uploaded metadata")

def main():
    print("=" * 60)
    print("🔥 Firebase Data Uploader")
    print("=" * 60)
    
    # Check if export directory exists
    data_dir = Path("firebase_data_export")
    if not data_dir.exists():
        print("❌ Error: firebase_data_export directory not found!")
        print("Please run DataExporter.kt first to generate JSON files.")
        exit(1)
    
    # Initialize Firebase
    db = initialize_firebase()
    print("✅ Firebase initialized successfully")
    
    # Upload data
    try:
        upload_categories(db, data_dir)
        upload_duas(db, data_dir, "hisn_duas.json")
        upload_duas(db, data_dir, "munajat.json")
        upload_duas(db, data_dir, "awrad_dalail.json")
        upload_duas(db, data_dir, "daily_essentials.json")
        upload_metadata(db)
        
        print("\n" + "=" * 60)
        print("🎉 Upload Complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Verify data in Firebase Console")
        print("2. Check Firestore indexes (create if needed)")
        print("3. Set up security rules")
        
    except Exception as e:
        print(f"\n❌ Error during upload: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
