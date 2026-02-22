import firebase_admin
from firebase_admin import credentials, firestore
import os
import re

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

def clean_munajat():
    print("Cleaning duplicate 'munajat' documents...")
    docs = db.collection('content').where('type', '==', 'munajat').stream()
    
    deleted_count = 0
    pattern = re.compile(r'^munajat_\d+$')
    
    batch = db.batch()
    batch_count = 0

    for doc in docs:
        doc_id = doc.id
        if pattern.match(doc_id):
            print(f"Deleting duplicate: {doc_id}")
            batch.delete(doc.reference)
            batch_count += 1
            deleted_count += 1
            
            if batch_count >= 400:
                batch.commit()
                batch = db.batch()
                batch_count = 0

    if batch_count > 0:
        batch.commit()
        
    print(f"Deleted {deleted_count} duplicate documents.")

if __name__ == "__main__":
    clean_munajat()
