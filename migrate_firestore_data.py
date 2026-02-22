
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import time

# --- CONFIGURATION ---
CRED_PATH = "scripts/serviceAccountKey.json"

def recursive_delete(coll_ref, batch_size=50):
    """
    Recursively deletes a collection and all its subcollections.
    """
    print(f"  Scanning collection: {coll_ref.id}...")
    docs = list(coll_ref.limit(batch_size).stream())
    deleted_count = 0

    while docs:
        for doc in docs:
            print(f"    Deleting document: {doc.id}")
            # 1. Recursively delete subcollections of this document
            for sub_coll in doc.reference.collections():
                print(f"      -> Found subcollection: {sub_coll.id} inside {doc.id}")
                recursive_delete(sub_coll, batch_size)
            
            # 2. Delete the document itself
            doc.reference.delete()
            deleted_count += 1
        
        # Fetch next batch
        docs = list(coll_ref.limit(batch_size).stream())

    if deleted_count > 0:
        print(f"  Deleted {deleted_count} documents from {coll_ref.id}")

def purge_all_collections(db):
    """
    Dynamically finds ALL collections and wipes them out.
    """
    print("Fetching all top-level collections...")
    collections = list(db.collections())
    
    if not collections:
        print("[INFO] No top-level collections found. Database is already empty.")
        return

    print(f"\n[WARNING] Found {len(collections)} collections to PURGE:")
    for col in collections:
        print(f" - {col.id}")
    
    print("\nBeginning Full Recursive Purge in 5 seconds...")
    time.sleep(5)

    for col in collections:
        recursive_delete(col)

    print("\n[SUCCESS] All collections have been processed.")

if __name__ == "__main__":
    # --- INITIALIZATION ---
    if not os.path.exists(CRED_PATH):
        print(f"Error: Credentials not found at {CRED_PATH}")
        exit(1)

    try:
        cred = credentials.Certificate(CRED_PATH)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print(f"Connected to Firestore Project: {db.project}")
        
        # EXECUTE PURGE
        purge_all_collections(db)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
