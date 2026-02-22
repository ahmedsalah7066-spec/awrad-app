
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# Use the service account key
CRED_PATH = r"c:\Users\ahmed\AndroidStudioProjects\awrad\serviceAccountKey.json"

if not os.path.exists(CRED_PATH):
    print(f"Error: Service account key not found at {CRED_PATH}")
    exit(1)

try:
    cred = credentials.Certificate(CRED_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firestore initialized successfully.")
except Exception as e:
    print(f"Error initializing Firestore: {e}")
    exit(1)

def delete_collection(coll_ref, batch_size=50):
    docs = list(coll_ref.limit(batch_size).stream())
    deleted = 0

    if len(docs) > 0:
        for doc in docs:
            # Recursive delete for subcollections
            for subcoll in doc.reference.collections():
                delete_collection(subcoll)
            
            print(f"Deleting doc: {doc.id} in {coll_ref.id}")
            doc.reference.delete()
            deleted += 1

        if deleted >= batch_size:
            return delete_collection(coll_ref, batch_size)
            
    return deleted

def clean_languages():
    languages_ref = db.collection("languages")
    
    # 1. Delete Arabic (ar)
    ar_doc = languages_ref.document("ar")
    if ar_doc.get().exists:
        print("Found active 'ar' document. Deleting...")
        # Check for subcollections (e.g. translations)
        for subcoll in ar_doc.collections():
            delete_collection(subcoll)
        ar_doc.delete()
        print("Deleted 'languages/ar'.")
    else:
        print("'languages/ar' does not exist.")

    # 2. Delete English (en)
    en_doc = languages_ref.document("en")
    if en_doc.get().exists:
        print("Found active 'en' document. Deleting...")
        for subcoll in en_doc.collections():
            delete_collection(subcoll)
        en_doc.delete()
        print("Deleted 'languages/en'.")
    else:
        print("'languages/en' does not exist.")

    # 3. Clean Turkish (tr) - Keep metadata, delete everything else
    tr_doc = languages_ref.document("tr")
    doc_snapshot = tr_doc.get()
    
    if doc_snapshot.exists:
        print("Found 'tr' document. Cleaning content...")
        
        # Delete any subcollections if they exist (just in case)
        for subcoll in tr_doc.collections():
            delete_collection(subcoll)

        # Get current data
        data = doc_snapshot.to_dict()
        
        # Prepare clean data (only metadata)
        clean_data = {}
        if "metadata" in data:
            clean_data["metadata"] = data["metadata"]
        else:
            # Fallback if metadata is missing
            clean_data["metadata"] = {
                "id": "tr",
                "name": "Türkçe",
                "direction": "ltr"
            }
            
        # Overwrite the document with ONLY metadata
        tr_doc.set(clean_data)
        print("Reset 'languages/tr' to only contain metadata.")
        
    else:
        print("'languages/tr' does not exist. Creating empty structure...")
        tr_doc.set({
            "metadata": {
                "id": "tr",
                "name": "Türkçe",
                "direction": "ltr"
            }
        })
        print("Created empty 'languages/tr'.")

if __name__ == "__main__":
    clean_languages()
