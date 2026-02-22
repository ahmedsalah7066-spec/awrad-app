
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import upload_data
import os

# Configuration
SERVICE_ACCOUNT_KEY = 'serviceAccountKey.json' 

def delete_collection(coll_ref, batch_size):
    """Deletes all documents in a collection."""
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(f'Deleting doc {doc.id}')
        doc.reference.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

def reset_hisn():
    # Initialize Firebase
    if not os.path.exists(SERVICE_ACCOUNT_KEY):
        print(f"Error: {SERVICE_ACCOUNT_KEY} not found.")
        return

    # Use existing app if already initialized, else initialize
    try:
        app = firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    
    # 1. Delete existing collection
    print("Deleting existing 'hisn_items' collection...")
    hisn_ref = db.collection('hisn_items')
    delete_collection(hisn_ref, 50)
    print("Collection deleted.")

    # 2. Upload new data
    print("Uploading fresh clean data...")
    # parse_hisn returns a list of dictionaries
    hisn_items = upload_data.parse_hisn(upload_data.HISN_FILE)
    print(f"Found {len(hisn_items)} Hisn items to upload.")

    batch = db.batch()
    count = 0
    for item in hisn_items:
        doc_ref = db.collection('hisn_items').document(str(item['id']))
        batch.set(doc_ref, item)
        count += 1
        
        if count >= 400:
            batch.commit()
            print(f"Committed batch of {count} items.")
            batch = db.batch()
            count = 0
            
    if count > 0:
        batch.commit()
        print(f"Committed final batch of {count} items.")

if __name__ == "__main__":
    reset_hisn()
    print("Reset complete!")
