import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os

# CONFIGURATION
# Path to your service account key file
SERVICE_ACCOUNT_KEY_PATH = 'scripts/serviceAccountKey.json' 

def initialize_firebase():
    if not os.path.exists(SERVICE_ACCOUNT_KEY_PATH):
        print(f"Error: {SERVICE_ACCOUNT_KEY_PATH} not found.")
        print("Please place your Firebase Admin SDK private key JSON file in this directory (styles/serviceAccountKey.json).")
        return None

    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(cred)
        
    return firestore.client()

def upload_translations(db, collection_name, json_path, lang_code):
    if not os.path.exists(json_path):
        print(f"Warning: {json_path} not found. Skipping.")
        return

    print(f"Uploading {collection_name} ({lang_code}) to Firestore...")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    batch = db.batch()
    count = 0
    
    # Target Collection: languages/{langCode}/translations
    target_ref = db.collection('languages').document(lang_code).collection('translations')
    
    # Munajat Index Tracker
    munajat_index = 0
    
    for item in data:
        # Determine ID based on content type
        doc_id = item.get('id')
        
        # 1. Determine Final ID
        final_id = doc_id
        
        # Adjust IDs for Awrad
        if collection_name == 'awrad':
             if doc_id and not doc_id.startswith('awrad_'):
                 final_id = f"awrad_{doc_id}" # saturday -> awrad_saturday
        
        # Adjust IDs for Munajat
        if collection_name == 'munajat':
            # Map based on index to match SimpleContentRepository logic ("munajat_0", "munajat_1"...)
            final_id = f"munajat_{munajat_index}"
            munajat_index += 1
        
        if not final_id:
            continue

        doc_ref = target_ref.document(final_id)
        
        # 2. Determine Main Text based on Language
        main_text = ""
        if lang_code == 'tr':
             # For Turkish JSON, 'content' has Turkish text
             main_text = item.get('content', '')
        elif lang_code == 'ar':
             # For Base JSON, 'content' is Arabic
             main_text = item.get('content', '')
        elif lang_code == 'en':
             # For Base JSON, 'translation' is English
             main_text = item.get('translation', '')

        # Skip if empty text (unless we want to overwrite with empty)
        if not main_text:
            continue

        payload = {
            'mainText': main_text,
            'id': final_id,
            'languageCode': lang_code
        }
        
        batch.set(doc_ref, payload)
        count += 1
        
        # Commit in batches of 400 to stay under limit
        if count % 400 == 0:
            batch.commit()
            batch = db.batch()
            print(f"  Committed batch of {count}...")

    batch.commit()
    print(f"Uploaded {count} documents from {collection_name} ({lang_code}).")

def main():
    db = initialize_firebase()
    if not db:
        return

    # Upload Turkish
    upload_translations(db, 'awrad', 'app/src/main/assets/data/tr/awrad.json', 'tr')
    upload_translations(db, 'munajat', 'app/src/main/assets/data/tr/munajat.json', 'tr')

    # Upload Arabic (Source of Truth)
    # We use the base files for Arabic content
    upload_translations(db, 'awrad', 'app/src/main/assets/data/awrad.json', 'ar')
    upload_translations(db, 'munajat', 'app/src/main/assets/data/munajat.json', 'ar')

    # Upload English (Source of Truth)
    # We use the base files but extract translation as main text
    upload_translations(db, 'awrad', 'app/src/main/assets/data/awrad.json', 'en')
    upload_translations(db, 'munajat', 'app/src/main/assets/data/munajat.json', 'en')
    
    print("Seeding complete.")

if __name__ == "__main__":
    main()
