import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import json

# Initialize Firebase
cred_path = "scripts/serviceAccountKey.json"
if not os.path.exists(cred_path):
    print(f"Error: Credentials not found at {cred_path}")
    exit(1)

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Failed to initialize Firebase: {e}")
        exit(1)

db = firestore.client()

json_path = "turkish_full_content.json"
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    exit(1)

def upload_turkish_content():
    print("Reading Turkish content from JSON...")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            turkish_content = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        exit(1)

    print(f"Direct uploading {len(turkish_content)} documents to localized paths...")
    
    batch = db.batch()
    count = 0
    
    # Path format: languages/tr/translations/{doc_id}
    # This matches the structure expected by the app for localized content
    base_collection = db.collection("languages").document("tr").collection("translations")
    
    # Munajat Mapping (Order from assets/data/munajat.json)
    munajat_order = [
        "munajat_muftaqirin",    # 0
        "munajat_mutawassilin",  # 1
        "munajat_muhibbin",      # 2
        "munajat_muridin",       # 3
        "munajat_dhakirin",      # 4
        "munajat_raghibin_1",    # 5
        "munajat_mutiin",        # 6
        "munajat_zahidin",       # 7
        "munajat_arifin",        # 8
        "munajat_shakirin",      # 9
        "munajat_rajin",         # 10
        "munajat_raghibin_2",    # 11
        "munajat_khaifin",       # 12
        "munajat_shakin",        # 13
        "munajat_taibin"         # 14
    ]
    
    munajat_map = {name: f"munajat_{i}" for i, name in enumerate(munajat_order)}
    
    for doc_id, text in turkish_content.items():
        # Determine the target ID(s)
        # If it's a Munajat key, map it to the index-based ID
        target_ids = []
        if doc_id in munajat_map:
            target_ids.append(munajat_map[doc_id])
            # Optional: Also keep the named ID if we want to support future named lookup
            # target_ids.append(doc_id) 
        else:
            target_ids.append(doc_id)
            
        for db_id in target_ids:
            ref = base_collection.document(db_id)
            
            # We merge so we don't destroy other potential fields, 
            # but primarily we are setting the mainText.
            data = {
                "mainText": text.strip()
            }
            
            batch.set(ref, data, merge=True)
            count += 1
            
            if count % 400 == 0:
                try:
                    batch.commit()
                    print(f"Committed batch of {count} documents...")
                    batch = db.batch()
                except Exception as e:
                    print(f"Error committing batch: {e}")

    if count > 0:
        try:
            batch.commit()
            print(f"Successfully finished uploading {count} Turkish translation documents.")
        except Exception as e:
            print(f"Error committing final batch: {e}")

if __name__ == "__main__":
    upload_turkish_content()
