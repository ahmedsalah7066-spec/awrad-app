import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import re
import os

# --- CONFIGURATION ---
# Path to your Firebase service account key
SERVICE_ACCOUNT_KEY = 'serviceAccountKey.json' 

# Paths to Kotlin files (adjust if running from a different directory)
BASE_PATH = r'c:\Users\ahmed\AndroidStudioProjects\awrad\app\src\main\java\com\example\awrad'
AWRAD_FILE = os.path.join(BASE_PATH, 'Awrad.kt')
MUNAJAT_FILE = os.path.join(BASE_PATH, 'Munajat.kt')
HISN_FILE = os.path.join(BASE_PATH, 'HisnContent.kt')
WIRD_FILE = os.path.join(BASE_PATH, 'WirdContent.kt')

def initialize_firebase():
    if not os.path.exists(SERVICE_ACCOUNT_KEY):
        print(f"Error: {SERVICE_ACCOUNT_KEY} not found. Please place your Firebase service account JSON file in this directory.")
        return None
    
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
    firebase_admin.initialize_app(cred)
    return firestore.client()

def parse_awrad(file_path):
    print(f"Parsing {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex matching: Awrad(R.string.day, """content""", translation = """trans""")
    # Note: translation is optional in the regex to be safe, though we added it to all
    # Using non-greedy match for content and translation
    pattern = re.compile(r'Awrad\(R\.string\.(\w+),\s*"""(.*?)"""(?:,\s*translation\s*=\s*"""(.*?)""")?', re.DOTALL)
    matches = pattern.findall(content)
    
    results = []
    days_map = {
        'dalail_saturday': 'saturday', 'dalail_sunday': 'sunday', 'dalail_monday': 'monday',
        'dalail_tuesday': 'tuesday', 'dalail_wednesday': 'wednesday', 'dalail_thursday': 'thursday',
        'dalail_friday': 'friday'
    }
    
    for i, (day_res, text, trans) in enumerate(matches):
        day_key = days_map.get(day_res, f"day_{i}")
        results.append({
            'id': day_key,
            'titleResId': day_res,
            'content': text.strip(),
            'translation': trans.strip() if trans else "",
            'order': i
        })
    return results

def parse_munajat(file_path):
    print(f"Parsing {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Regex: Munajat(R.string.(name), """(content)""", translation = """(trans)""")
    pattern = re.compile(r'Munajat\(R\.string\.(\w+),\s*"""(.*?)"""(?:,\s*translation\s*=\s*"""(.*?)""")?', re.DOTALL)
    matches = pattern.findall(content)
    
    results = []
    for i, (title_res, text, trans) in enumerate(matches):
        results.append({
            'id': f"munajat_{i+1}",
            'titleResId': title_res,
            'content': text.strip(),
            'translation': trans.strip() if trans else "",
            'order': i
        })
    return results

def parse_wird(file_path):
    print(f"Parsing {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Regex: const val ISTIFTAH = """..."""
    pattern = re.compile(r'const val (\w+) = """(.*?)"""', re.DOTALL)
    matches = pattern.findall(content)
    
    # Dictionary to hold merged results: name -> {content: ..., translation: ...}
    merged_data = {}
    
    for name, text in matches:
        clean_text = text.strip()
        if name.endswith('_EN'):
            base_name = name[:-3].lower() # ISTIFTAH_EN -> istiftah
            if base_name not in merged_data:
                merged_data[base_name] = {'id': base_name}
            merged_data[base_name]['translation'] = clean_text
        else:
            base_name = name.lower()
            if base_name not in merged_data:
                 merged_data[base_name] = {'id': base_name}
            merged_data[base_name]['content'] = clean_text

    return list(merged_data.values())

def parse_map(text, map_name):
    # Find mapOf block: explanation = mapOf( ... )
    # This is a bit tricky with nested parenthesis, but let's assume standard formatting
    pattern = re.compile(rf'{map_name}\s*=\s*mapOf\s*\((.*?)\)', re.DOTALL)
    match = pattern.search(text)
    if not match:
        return {}
    
    content = match.group(1)
    # Parse "key" to "value"
    # value can be multiline string, so we need to be careful.
    # Regex: "(\w+)"\s*to\s*"(.*?)"(?=\s*,|\s*$) => fails on strings with quotes
    # Let's try matching simple strings first since the file seems to have simple strings
    
    entries = {}
    # Split by comma, but not inside quotes... hard.
    # Let's simple regex for "code" to "text"
    # Regex that handles escaped quotes: " key " to " value "
    # The value part matches: ( [^"\\] | \\. )*
    item_pattern = re.compile(r'"(\w+)"\s*to\s*"((?:[^"\\]|\\.)*?)"', re.DOTALL)
    
    # We need to be careful about not over-matching. 
    # The content is a list of entries separated by commas.
    # A robust way is to find all "xx" to "yy" inside the block.
    # Assuming the text doesn't contain unescaped quotes that break this simple model.
    
    # Issue: "text" might contain " inside it? Kotlin uses \" for that.
    # Simple regex \"(.*?)\" might stop early.
    
    # Let's assume standard format: "code" to "text"
    # Find all occurrences of valid language codes
    for m in item_pattern.finditer(content):
        code = m.group(1)
        text = m.group(2).replace(r'\"', '"').replace(r'\n', '\n')
        entries[code] = text.strip()
        
    return entries

def parse_hisn(file_path):
    print(f"Parsing {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    cat_id_map = {
        'MORNING': 'hisn_morning', 'EVENING': 'hisn_evening', 'SLEEP': 'hisn_sleep',
        'PRAYER': 'hisn_prayer', 'FOOD': 'hisn_food', 'TRAVEL': 'hisn_travel', 
        'MOSQUE': 'hisn_mosque', 'TASBEEHAT': 'hisn_tasbeehat'
    }

    # Split content into category blocks based on `val X_ADHKAR = listOf(`
    # We need to capture the variable name properly
    
    # Strategy: Find all start indices of `val X_ADHKAR`
    cat_starts = []
    for m in re.finditer(r'val (\w+)_ADHKAR = listOf\(', content):
        cat_starts.append((m.start(), m.group(1)))
        
    dhikr_collection = []
    
    for i in range(len(cat_starts)):
        start_idx, cat_var = cat_starts[i]
        # End index is the start of next category or end of file
        end_idx = cat_starts[i+1][0] if i+1 < len(cat_starts) else len(content)
        
        block = content[start_idx:end_idx]
        
        cat_key = cat_var.replace('_ADHKAR', '')
        cat_id = cat_id_map.get(cat_key, cat_var.lower())
        
        # Now find DhikrItem blocks inside this category block
        # We can split by `DhikrItem(`
        items_splits = block.split('DhikrItem(')
        
        # The first split is garbage (preamble of the list)
        for idx, item_text in enumerate(items_splits[1:]):
            # item_text contains the arguments and then `),` or `)`
            # We need to extract fields.
            
            # 1. Arabic: arabic = "..."
            # Use non-greedy match for string content?
            # It's safer to rely on the parameter name: `arabic = "` up to `",` ? 
            # Or just `arabic = "(.*?)"` but careful with multiline.
            
            arabic_match = re.search(r'arabic\s*=\s*"(.*?)"', item_text, re.DOTALL)
            count_match = re.search(r'count\s*=\s*(\d+)', item_text)
            
            if arabic_match:
                arabic = arabic_match.group(1).replace(r'\"', '"').replace(r'\n', '\n')
                count = int(count_match.group(1)) if count_match else 1
                
                # Parse explanation map
                explanation = parse_map(item_text, 'explanation')
                
                # Parse fadl map
                fadl = parse_map(item_text, 'fadl')
                
                item_id = f"dhikr_{cat_id}_{idx+1}_{abs(hash(arabic))}"
                
                dhikr_collection.append({
                    'id': item_id,
                    'categoryId': cat_id,
                    'arabicText': arabic,
                    'count': count,
                    'orderIndex': idx,
                    'explanation': explanation,
                    'fadl': fadl
                })

    return dhikr_collection


def upload_data(db):
    batch = db.batch()
    
    # 1. Upload Awrad
    awrad_items = parse_awrad(AWRAD_FILE)
    print(f"Found {len(awrad_items)} Awrad items.")
    for item in awrad_items:
        doc_ref = db.collection('daily_awrad').document(item['id'])
        batch.set(doc_ref, item)
        
    # 2. Upload Munajat
    munajat_items = parse_munajat(MUNAJAT_FILE)
    print(f"Found {len(munajat_items)} Munajat items.")
    for item in munajat_items:
        doc_ref = db.collection('munajat').document(item['id'])
        batch.set(doc_ref, item)
        
    # 3. Upload Static Wird
    wird_items = parse_wird(WIRD_FILE)
    print(f"Found {len(wird_items)} Static items.")
    for item in wird_items:
        doc_ref = db.collection('static_content').document(item['id'])
        batch.set(doc_ref, item)

    # 4. Upload Hisn
    # Need to be careful about batch size limit (500)
    # Commit previous batch first
    batch.commit()
    print("Batch 1 (Awrad, Munajat, Static) committed.")
    
    batch = db.batch()
    hisn_items = parse_hisn(HISN_FILE)
    print(f"Found {len(hisn_items)} Hisn items.")
    
    count = 0
    for item in hisn_items:
        doc_ref = db.collection('hisn_items').document(str(item['id']))
        batch.set(doc_ref, item)
        count += 1
        
        if count >= 400:
            batch.commit()
            print(f"Committed batch of {count} Hisn items.")
            batch = db.batch()
            count = 0
            
    if count > 0:
        batch.commit()
        print(f"Committed final batch of {count} Hisn items.")

if __name__ == "__main__":
    db = initialize_firebase()
    if db:
        upload_data(db)
        print("Done!")
