#!/usr/bin/env python3
"""
Manual Data Upload Script
Directly creates and uploads basic data structure to Firestore
"""

import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
import json

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        return firestore.client()
    except FileNotFoundError:
        print("[ERROR] serviceAccountKey.json not found in scripts/ directory!")
        exit(1)
    except Exception as e:
        print(f"[ERROR] Failed to initialize Firebase: {e}")
        exit(1)

def upload_basic_structure(db):
    """Upload basic categories and placeholder data"""
    print("\n[INFO] Creating basic Firestore structure...")
    
    # Categories
    categories = [
        {"id": "morning", "titleResId": "hisn_morning", "orderIndex": 0},
        {"id": "evening", "titleResId": "hisn_evening", "orderIndex": 1},
        {"id": "sleep", "tidleResId": "hisn_sleep", "orderIndex": 2},
        {"id": "prayer", "titleResId": "hisn_prayer", "orderIndex": 3},
        {"id": "munajat", "titleResId": "munajat_title", "orderIndex": 100},
        {"id": "awrad", "titleResId": "dalail_title", "orderIndex": 101},
        {"id": "daily_essentials", "titleResId": "daily_essentials_title", "orderIndex": 102},
    ]
    
    print("\n[INFO] Uploading categories...")
    for cat in categories:
        cat_id = cat.pop("id")
        db.collection("categories").document(cat_id).set(cat)
    print(f"[OK] Uploaded {len(categories)} categories")
    
    # Upload metadata
    print("\n[INFO] Uploading metadata...")
    metadata = {
        "latestDataVersion": "1.0.0",
        "lastUpdated": firestore.SERVER_TIMESTAMP,
        "availableLanguages": ["ar"],
        "minAppVersion": "2.3.2"
    }
    db.collection("metadata").document("app_info").set(metadata)
    print("[OK] Uploaded metadata")
    
    print("\n[SUCCESS] Basic structure created!")
    print("Next: Manually add Arabic content from Android Studio using DatabaseModule")

def main():
    print("=" * 60)
    print("Manual Firebase Setup")
    print("=" * 60)
    
    # Initialize Firebase
    db = initialize_firebase()
    print("[OK] Firebase initialized\n")
    
    # Upload basic structure
    upload_basic_structure(db)
    
    print("\n" + "=" * 60)
    print("[DONE]")
    print("=" * 60)

if __name__ == "__main__":
    main()
