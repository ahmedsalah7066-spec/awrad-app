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

def list_dalail():
    print("Listing ALL documents in 'content' collection to find Dalail...")
    # Query for type == 'awrad'
    docs = db.collection('content').where('type', '==', 'awrad').stream()
    
    count = 0
    dalail_ids = []
    
    print("Documents with type='awrad':")
    for doc in docs:
        data = doc.to_dict()
        title = data.get('uz', {}).get('title', 'No Title')
        content_snippet = data.get('uz', {}).get('content', '')[:50]
        print(f"Doc ID: {doc.id}, Title: {str(title).encode('utf-8', 'replace')}, Content: {str(content_snippet).encode('utf-8', 'replace')}...")
        dalail_ids.append(doc.id)
        count += 1
        
    print(f"\nTotal 'awrad' docs count: {count}")
    print(f"IDs: {dalail_ids}")

if __name__ == "__main__":
    list_dalail()
