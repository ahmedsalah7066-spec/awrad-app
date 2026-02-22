import firebase_admin
from firebase_admin import credentials, firestore
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

def clean_dalail():
    print("Cleaning duplicate 'awrad' documents...")
    # Get all documents with type 'awrad'
    docs = db.collection('content').where('type', '==', 'awrad').stream()
    
    deleted_count = 0
    batch = db.batch()
    batch_count = 0

    for doc in docs:
        doc_id = doc.id
        # We want to delete IDs that start with 'awrad_' followed by day name
        # Valid IDs are: saturday, sunday, monday, tuesday, wednesday, thursday, friday
        # Invalid/Duplicate IDs are: awrad_saturday, etc.
        
        if doc_id.startswith('awrad_'):
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
    clean_dalail()
