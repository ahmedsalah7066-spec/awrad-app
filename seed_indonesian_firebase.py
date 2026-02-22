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

def seed_content(collection_name, file_path, lang_code='id'):
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
            # Fix: Prepend 'awrad_' to match SimpleContentRepository expectation
            # JSON id is 'saturday', expected is 'awrad_saturday'
            raw_id = item['id']
            # Ensure we don't double prefix if run multiple times or if logic changes
            if not raw_id.startswith('awrad_'):
                doc_id = f"awrad_{raw_id}"
            else:
                doc_id = raw_id
            
            doc_ref = db.collection('content').document(doc_id)
            
            update_data = {
                'type': 'awrad',
                'order': index,
                lang_code: {
                    'title': item.get('title', ''),
                    'content': item.get('content', ''), # Indonesian text (monolingual)
                    'translation': item.get('translation', '') # Empty
                }
            }
            batch.set(doc_ref, update_data, merge=True)
            count += 1

    elif collection_name == 'munajat':
        # List of items
        for index, item in enumerate(data):
            # Fix: Use 1-based index ID to match SimpleContentRepository expectation
            # repository queries 'munajat_1', 'munajat_2'...
            doc_id = f"munajat_{index + 1}"
            
            doc_ref = db.collection('content').document(doc_id)
            update_data = {
                'type': 'munajat',
                'order': index,
                lang_code: {
                    'title': item.get('title', ''),
                    'content': item.get('content', ''), # Indonesian text (monolingual)
                    'translation': item.get('translation', '') # Empty
                }
            }
            batch.set(doc_ref, update_data, merge=True)
            count += 1

    elif collection_name == 'hisn':
        # deeply nested structure: categories -> items
        for cat_index, category in enumerate(data):
            cat_id = category['id']
            
            # 1. Seed Category Title
            # ID must be 'hisn_category_{id}' to match getByType("hisn_category")
            cat_doc_id = f"hisn_category_{cat_id}"
            cat_doc_ref = db.collection('content').document(cat_doc_id)
            
            # We need to set the 'type' field at the top level so it can be queried
            cat_update_data = {
                'type': 'hisn_category',
                'categoryId': cat_id, # Optional but good for consistency
                'order': cat_index,
                lang_code: {
                    'title': category.get('title', ''),
                    'content': '',
                    'translation': ''
                }
            }
            batch.set(cat_doc_ref, cat_update_data, merge=True)
            count += 1

            # 2. Seed Items
            for index, item in enumerate(category['items']):
                 # Fix: Use constructed ID 'hisn_{catId}_{index+1}' to match SimpleContentRepository
                 doc_id = f"hisn_{cat_id}_{index + 1}"
                 doc_ref = db.collection('content').document(doc_id)
                 
                 update_data = {
                    'type': 'hisn',
                    'categoryId': cat_id,
                    'count': item.get('count', 1),
                    'order': index,
                    lang_code: {
                        'content': item.get('content', ''), # Arabic (bilingual)
                        'translation': item.get('translation', ''), # Indonesian
                        'fadl': item.get('fadl', '') # Indonesian Virtue
                    }
                 }
                 batch.set(doc_ref, update_data, merge=True)
                 count += 1
                 
                 if count >= 400: # Batches limit is 500
                     batch.commit()
                     batch = db.batch()
                     count = 0

    if count > 0:
        batch.commit()
    print(f"Seeding {collection_name} complete. Total operations: {count} (in last batch)")


if __name__ == "__main__":
    seed_content('awrad', 'app/src/main/assets/id/dalail.json')
    seed_content('munajat', 'app/src/main/assets/id/munajat.json')
    seed_content('hisn', 'app/src/main/assets/id/hisn.json')
    print("All seeding complete.")
