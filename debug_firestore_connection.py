import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# --- CONFIGURATION ---
CRED_PATH = "scripts/serviceAccountKey.json"

def debug_connection():
    print("--- FIREBASE CONNECTION DEBUG ---")
    
    # 1. Initialize
    if not os.path.exists(CRED_PATH):
        print(f"CRITICAL ERROR: Credentials not found at {CRED_PATH}")
        return

    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(CRED_PATH)
            firebase_admin.initialize_app(cred)
            print("Firebase App Initialized Successfully.")
        else:
            print("Firebase App already initialized.")
    except Exception as e:
        print(f"CRITICAL ERROR initializing Firebase: {e}")
        return

    # 2. Check Project ID
    try:
        db = firestore.client()
        print(f"\n[CONNECTED] TO PROJECT ID: {db.project}")
        print("(Please compare this with your Firebase Console URL)")
    except Exception as e:
        print(f"Error getting Firestore client: {e}")
        return

    # 3. List Collections
    print("\n--- LISTING ROOT COLLECTIONS ---")
    try:
        collections = db.collections()
        found_any = False
        
        for coll in collections:
            found_any = True
            coll_id = coll.id
            print(f"\n[Collection]: {coll_id}")
            
            # 4. detailed check for first 5 docs
            docs = list(coll.limit(5).stream())
            count = len(docs)
            print(f"   - Visible Documents (Limit 5): {count}")
            for doc in docs:
                print(f"     - Doc ID: {doc.id}")
                
        if not found_any:
            print("\n[NO ROOT COLLECTIONS FOUND].")
            print("Possible reasons:")
            print("1. The database is actually empty.")
            print("2. You are connected to the wrong project.")
            print("3. Check 'serviceAccountKey.json' vs Console.")

    except Exception as e:
        print(f"Error listing collections: {e}")

    print("\n--- DEBUG COMPLETE ---")

if __name__ == "__main__":
    debug_connection()
