import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        # Check if already initialized
        firebase_admin.get_app()
    except ValueError:
        # Initialize with your service account key
        # Make sure to place your serviceAccountKey.json in the project root
        cred = credentials.Certificate('awrad-a1b9d-firebase-adminsdk-hswnt-d3cc6823ca.json')
        firebase_admin.initialize_app(cred)
    return firestore.client()

def seed_russian_data(db):
    """Seed Russian translations to Firestore"""
    print("Starting to seed Russian data...")
    
    # 1. Dalail
    print("\nProcessing Dalail...")
    with open('app/src/main/assets/ru/dalail.json', 'r', encoding='utf-8') as f:
        dalail_data = json.load(f)
        
    for item in dalail_data:
        doc_id = item['id']
        doc_ref = db.collection('languages').document('ru').collection('translations').document(doc_id)
        doc_ref.set({
            'title': item['title'],
            'content': item.get('content', ''), # Use content field for translated text to match others
            'translation': item.get('translation', ''), 
            'type': item['type']
        }, merge=True)
        print(f"Updated ru translation for: {doc_id}")
        
    # 2. Munajat
    print("\nProcessing Munajat...")
    with open('app/src/main/assets/ru/munajat.json', 'r', encoding='utf-8') as f:
        munajat_data = json.load(f)
        
    for item in munajat_data:
        doc_id = item['id']
        doc_ref = db.collection('languages').document('ru').collection('translations').document(doc_id)
        doc_ref.set({
            'title': item['title'],
            'content': item.get('content', ''),
            'translation': item.get('translation', ''),
        }, merge=True)
        print(f"Updated ru translation for: {doc_id}")
        
    # 3. Hisn
    print("\nProcessing Hisn...")
    with open('app/src/main/assets/ru/hisn.json', 'r', encoding='utf-8') as f:
        hisn_data = json.load(f)
        
    for category in hisn_data:
        # Update category title
        cat_id = category['id']
        doc_ref = db.collection('languages').document('ru').collection('translations').document(cat_id)
        doc_ref.set({
            'title': category['title']
        }, merge=True)
        print(f"Updated ru category: {cat_id}")
        
        # Update category items
        for item in category['items']:
            item_id = item['id']
            item_ref = db.collection('languages').document('ru').collection('translations').document(item_id)
            item_ref.set({
                'content': item['content'],
                'fadl': item.get('fadl', '')
            }, merge=True)
            print(f"Updated ru item: {item_id}")

    print("\nUploading to Firestore completed successfully!")

if __name__ == "__main__":
    try:
        db = initialize_firebase()
        seed_russian_data(db)
    except Exception as e:
        print(f"Error occurred: {str(e)}")
