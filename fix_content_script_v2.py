import re
from collections import defaultdict

def fix_content():
    file_path = 'generate_uzbek_content.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the dictionary
    dict_match = re.search(r'hisn_translations = \{(.*?)\}', content, re.DOTALL)
    if not dict_match:
        print("Dictionary not found!")
        return

    # Start index of the dictionary content within the full file
    dict_start_offset = dict_match.start(1)
    dict_content = dict_match.group(1)
    
    # Find all entries
    pattern = re.compile(r'("dhikr_hisn_[^"]+_\d+")\s*:\s*("""(?:[^"]|"(?!"""))*"""|"(?:[^"\\]|\\.)*")', re.DOTALL)
    
    print(f"Found {len(list(pattern.finditer(dict_content)))} matches in regex.")
    
    for match in pattern.finditer(dict_content):
        key_quote = match.group(1)
        value_quote = match.group(2)
        
        # Calculate absolute indices in the file
        # match.start(2) is the start of the value group relative to dict_content
        value_start_abs = dict_start_offset + match.start(2)
        value_end_abs = dict_start_offset + match.end(2)

        key = key_quote.strip('"')
        parts = key.split('_')
        numeric_id = parts[-1]
        
        if value_quote.startswith('"""'):
             text = value_quote[3:-3]
        else:
             text = value_quote[1:-1]
             
        entries.append({
            'key_quote': key_quote,
            'value_quote': value_quote,
            'numeric_id': numeric_id,
            'text': text,
            'start': value_start_abs,
            'end': value_end_abs
        })

    # Group by ID
    id_groups = defaultdict(list)
    for entry in entries:
        id_groups[entry['numeric_id']].append(entry)

    replacements = []

    for num_id, group in id_groups.items():
        if len(group) > 1:
            # Find longest text
            best_entry = max(group, key=lambda x: len(x['text']))
            best_value_quote = best_entry['value_quote']
            
            for entry in group:
                if entry['value_quote'] != best_value_quote:
                    print(f"Replacing content for {entry['key_quote']}")
                    replacements.append({
                        'start': entry['start'],
                        'end': entry['end'],
                        'new_text': best_value_quote
                    })

    # Sort replacements by start index descending
    replacements.sort(key=lambda x: x['start'], reverse=True)
    
    new_content = content
    for r in replacements:
        new_content = new_content[:r['start']] + r['new_text'] + new_content[r['end']:]
        
    if replacements:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Applied {len(replacements)} replacements.")
    else:
        print("No replacements needed.")

if __name__ == "__main__":
    fix_content()
