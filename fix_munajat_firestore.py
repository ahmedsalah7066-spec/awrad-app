import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

# Initialize Firebase Admin
cred_path = 'scripts/serviceAccountKey.json'
if not os.path.exists(cred_path):
    print(f"Error: {cred_path} not found.")
    exit(1)

cred = credentials.Certificate(cred_path)
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred)

db = firestore.client()

def fix_munajat_typo():
    json_path = 'app/src/main/assets/data/munajat.json'
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    target_id = "munajat_raghibin_2"
    target_item = None
    for item in data:
        if item['id'] == target_id:
            target_item = item
            break
    
    if target_item:
        print(f"Found item: {target_id}")
        content = target_item['content']
        # Double check if typo is fixed in the variable
        if "س تَرَ" in content:
             print("WARNING: Typo 'س تَرَ' still present in JSON content! Please fix file first.")
             return
        
        doc_ref = db.collection('content').document(target_id)
        
        # Update ar.content
        # We use dot notation for nested field update
        update_data = {
            'ar.content': content
        }
        
        doc_ref.update(update_data)
        print(f"Successfully updated 'ar.content' for document '{target_id}' in Firestore.")
    else:
        print(f"Item with id '{target_id}' not found in JSON.")

if __name__ == "__main__":
    fix_munajat_typo()
