import firebase_admin
from firebase_admin import credentials, firestore
import json
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

def seed_content(collection_name, file_path, lang_code='uz'):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"Seeding {collection_name} from {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    batch = db.batch()
    count = 0
    
    # Logic depends on file structure
    if collection_name == 'awrad':
        # List of items
        for index, item in enumerate(data):
            doc_id = item['id']
            doc_ref = db.collection('content').document(doc_id)
            # Update specific language field
            
            update_data = {
                'type': 'awrad',
                'order': index,
                lang_code: {
                    'title': item.get('title', ''),
                    'content': item.get('content', ''), # This is the translated content
                    'translation': item.get('translation', '') # Might be empty if content IS translation
                }
            }
            batch.set(doc_ref, update_data, merge=True)
            count += 1

    elif collection_name == 'munajat':
        # List of items
        for index, item in enumerate(data):
            doc_id = item['id']
            doc_ref = db.collection('content').document(doc_id)
            update_data = {
                'type': 'munajat',
                'order': index,
                lang_code: {
                    'title': item.get('title', ''),
                    'content': item.get('content', ''),
                    'translation': item.get('translation', '')
                }
            }
            batch.set(doc_ref, update_data, merge=True)
            count += 1

    elif collection_name == 'hisn':
        # deeply nested structure: categories -> items
        for category in data:
            for index, item in enumerate(category['items']):
                 doc_id = item['id']
                 doc_ref = db.collection('content').document(doc_id)
                 
                 update_data = {
                    'type': 'hisn',
                    'categoryId': category['id'],
                    'count': item.get('count', 1),
                    'order': index,
                    lang_code: {
                        'content': item.get('content', ''),
                        'translation': item.get('translation', ''), # likely empty/unused in hisn structure here if content has it
                        'fadl': item.get('fadl', '') # Virtue
                    }
                 }
                 batch.set(doc_ref, update_data, merge=True)
                 count += 1
                 
                 if count >= 400: # Batch limit
                     batch.commit()
                     batch = db.batch()
                     count = 0

    elif collection_name == 'static':
        # List of items (istiftah, ibrahimi)
        for item in data:
            doc_id = item['id']
            target_id = f"static_{doc_id}"
            doc_ref = db.collection('content').document(target_id)
            
            update_data = {
                'type': 'static',
                lang_code: {
                    'content': item.get('content', ''),
                    'translation': item.get('translation', '')
                }
            }
            batch.set(doc_ref, update_data, merge=True)
            count += 1

    if count > 0:
        batch.commit()
    print(f"Seeding {collection_name} complete.")


if __name__ == "__main__":
    seed_content('awrad', 'app/src/main/assets/uz/dalail.json')
    seed_content('munajat', 'app/src/main/assets/uz/munajat.json')
    seed_content('hisn', 'app/src/main/assets/uz/hisn.json')
    seed_content('static', 'app/src/main/assets/uz/static.json')
    print("All seeding complete.")
