import re
from collections import defaultdict

def check_duplicates():
    # Read the content file
    with open('generate_uzbek_content.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract the dictionary content using regex
    # We look for hisn_translations = { ... }
    match = re.search(r'hisn_translations = \{(.*?)\}', content, re.DOTALL)
    if not match:
        print("Could not find hisn_translations dictionary")
        return

    dict_content = match.group(1)
    
    # Parse entries manually to avoid import issues or executing the whole script
    # We look for "key": """value""", or "key": "value"
    entries = re.findall(r'"([^"]+)"\s*:\s*"""(.*?)"""', dict_content, re.DOTALL)
    
    # Group by numeric ID
    # Keys look like: dhikr_hisn_morning_1_7079504423173924192
    # The ID is the last part: 7079504423173924192
    
    id_groups = defaultdict(list)
    
    for key, value in entries:
        parts = key.split('_')
        # The ID is typically the last part, but let's be robust
        # Format is usually: dhikr_hisn_SECTION_INDEX_ID
        if len(parts) >= 1:
            numeric_id = parts[-1]
            if numeric_id.isdigit() and len(numeric_id) > 10: # Simple check for long IDs
                id_groups[numeric_id].append({
                    'key': key,
                    'text': value,
                    'length': len(value)
                })

    # Analyze groups
    issues_found = 0
    for num_id, items in id_groups.items():
        if len(items) > 1:
            # Check for length discrepancies
            lengths = [item['length'] for item in items]
            max_len = max(lengths)
            min_len = min(lengths)
            
            # If there's a significant difference (e.g. > 50 chars), it's likely a short vs long version
            if max_len - min_len > 50:
                print(f"ID: {num_id} has inconsistent translations:")
                sorted_items = sorted(items, key=lambda x: x['length'], reverse=True)
                for item in sorted_items:
                    print(f"  - {item['key']}: {item['length']} chars")
                    # Safe print for Windows console
                    safe_preview = item['text'][:50].encode('ascii', 'replace').decode('ascii')
                    print(f"    Preview: {safe_preview}...")
                print("-" * 40)
                issues_found += 1

    if issues_found == 0:
        print("No significant duplicates found.")
    else:
        print(f"Found {issues_found} IDs with inconsistent translation lengths.")

if __name__ == "__main__":
    check_duplicates()
