import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# --- CONFIGURATION ---
SERVICE_ACCOUNT_KEY = 'serviceAccountKey.json' 

def initialize_firebase():
    if not os.path.exists(SERVICE_ACCOUNT_KEY):
        print(f"Error: {SERVICE_ACCOUNT_KEY} not found.")
        return None
    
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(cred)
    return firestore.client()

def delete_collection(db, collection_name, batch_size):
    print(f"Deleting collection: {collection_name}...")
    coll_ref = db.collection(collection_name)
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(f'Deleting doc {doc.id} => {doc.to_dict()}')
        doc.reference.delete()
        deleted += 1

    if deleted >= batch_size:
        return delete_collection(db, collection_name, batch_size)
    else:
        print(f"Collection {collection_name} deleted successfully.")

if __name__ == "__main__":
    db = initialize_firebase()
    if db:
        # Delete possible category collections
        delete_collection(db, 'hisn_categories', 100)
        delete_collection(db, 'categories', 100)
        print("Cleanup operations completed.")
