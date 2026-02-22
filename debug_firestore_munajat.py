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

def list_munajat():
    print("Listing 'munajat' documents in 'content' collection...")
    # Query for type == 'munajat'
    docs = db.collection('content').where('type', '==', 'munajat').stream()
    
    count = 0
    ids = []
    for doc in docs:
        ids.append(doc.id)
        # Safe print
        data = doc.to_dict()
        title = data.get('uz', {}).get('title', 'No Title')
        print(f"Doc ID: {doc.id}, Title: {str(title).encode('utf-8', 'replace')}")
        count += 1
    
    print(f"\nTotal Munajat Docs: {count}")
    print(f"IDs: {ids}")

if __name__ == "__main__":
    list_munajat()
