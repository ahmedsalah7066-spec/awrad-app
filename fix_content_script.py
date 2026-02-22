import re

def fix_content():
    file_path = 'generate_uzbek_content.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # regex to find the dictionary
    dict_match = re.search(r'hisn_translations = \{(.*?)\}', content, re.DOTALL)
    if not dict_match:
        print("Dictionary not found!")
        return

    dict_content = dict_match.group(1)
    
    # Find all entries: key and value
    # We use a capture group for key and value
    # Value is captured including the quotes
    pattern = re.compile(r'("dhikr_hisn_[^"]+_\d+")\s*:\s*("""(?:[^"]|"(?!"""))*"""|"(?:[^"\\]|\\.)*")', re.DOTALL)
    
    entries = []
    for match in pattern.finditer(dict_content):
        full_match = match.group(0)
        key_quote = match.group(1)
        value_quote = match.group(2)
        
        # Extract ID
        key = key_quote.strip('"')
        parts = key.split('_')
        numeric_id = parts[-1]
        
        # Extract Text Content (remove quotes)
        if value_quote.startswith('"""'):
             text = value_quote[3:-3]
        else:
             text = value_quote[1:-1]
             
        entries.append({
            'full_match': full_match,
            'key_quote': key_quote,
            'value_quote': value_quote,
            'numeric_id': numeric_id,
            'text': text,
            'start': match.start(0) + dict_match.start(1),
            'end': match.end(0) + dict_match.start(1)
        })

    # Group by ID
    from collections import defaultdict
    id_groups = defaultdict(list)
    for entry in entries:
        id_groups[entry['numeric_id']].append(entry)

    # Determine replacements
    new_content = content
    # We process from end to start to avoid offsetting indices
    # But string replacement is tricky with indices if we do it iteratively on a changing string
    # Easier strategy: Build a new dictionary string
    
    # Let's map key -> best_value_quote
    key_to_new_value = {}
    
    for num_id, group in id_groups.items():
        if len(group) > 1:
            # Find longest text
            best_entry = max(group, key=lambda x: len(x['text']))
            best_value_quote = best_entry['value_quote']
            
            for entry in group:
                if entry['value_quote'] != best_value_quote:
                    print(f"Fixing {entry['key_quote']} -> Using content from {best_entry['key_quote']}")
                    key_to_new_value[entry['key_quote']] = best_value_quote

    # Now replace in the original content
    # We'll use simple string replacement for safety, but we must be careful about context
    # Since keys are unique and distinct, we can replace 'key": old_value' with 'key": new_value'
    
    for key_quote, new_value in key_to_new_value.items():
        # Sanitize regex for key
        # We look for the specific line in the file
        # Regex: key matches, whitespace, colon, whitespace, ANY value, comma or newline
        
        # Construct a precise find pattern for this entry
        # We need to find the entry in the original file content to replace it
        
        # Search for: "key": """old_value""" or "key": "old_value"
        # We previously parsed this, so we know the EXACT old full match is in the group? 
        # Actually my parsing might be slightly off on whitespace.
        
        # Let's use the 'entries' list again, it has the span in the original file!
        # Wait, the span was relative to dict_content, plus offset.
        pass

    # Better approach: Reconstruct the dictionary body
    # But preserving comments and formatting is hard.
    
    # Approach 3: Just use `replace` on the specific strings if they are unique enough.
    # The keys are definitely unique.
    
    for num_id, group in id_groups.items():
        if len(group) > 1:
             # Find longest
            best_entry = max(group, key=lambda x: len(x['text']))
            best_value = best_entry['value_quote']
            
            for entry in group:
                if entry['value_quote'] != best_value:
                    # We need to replace entry['value_quote'] with best_value BUT only where it follows entry['key_quote']
                    # Use regex sub
                    
                    # Pattern: (key_quote \s*:\s*) old_value
                    # Replace with: \1 new_value
                    
                    pattern_str = re.escape(entry['key_quote']) + r'\s*:\s*' + re.escape(entry['value_quote'])
                    replacement_str = entry['key_quote'] + ': ' + best_value
                    
                    # Check if pattern exists
                    if re.search(pattern_str, new_content):
                        new_content = re.sub(pattern_str, replacement_str, new_content, count=1)
                    else:
                        print(f"Could not find exact match for replacement: {entry['key_quote']}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Done fixing content.")

if __name__ == "__main__":
    fix_content()
