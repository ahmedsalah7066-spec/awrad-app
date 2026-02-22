import ast
from collections import defaultdict

def fix_content_ast():
    file_path = 'generate_uzbek_content.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"Syntax error parsing file: {e}")
        return

    # Find the assignment hisn_translations = { ... }
    target_dict = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == 'hisn_translations':
                    if isinstance(node.value, ast.Dict):
                        target_dict = node.value
                        break
        if target_dict:
            break

    if not target_dict:
        print("Dictionary hisn_translations not found via AST.")
        return

    # Extract entries
    entries = []
    
    # We need to map keys to their values and positions
    # ast.Dict has keys and values attributes (lists)
    
    for i, key_node in enumerate(target_dict.keys):
        value_node = target_dict.values[i]
        
        # Check if key is a string (Constant in py3.8+, Str in older)
        # Using ast.literal_eval for safety or just inspecting value
        if isinstance(key_node, ast.Constant): # Python 3.8+
            key_str = key_node.value
        elif isinstance(key_node, ast.Str): # Python 3.7
            key_str = key_node.s
        else:
            continue
            
        # Get value text
        if isinstance(value_node, ast.Constant):
            value_str = value_node.value
        elif isinstance(value_node, ast.Str):
            value_str = value_node.s
        else:
            continue

        # Check if ID matches format
        if not key_str.startswith("dhikr_hisn_"):
            continue
            
        parts = key_str.split('_')
        numeric_id = parts[-1]
        
        # Get source segment for value (to replace it later)
        # AST nodes have lineno and col_offset (start) and end_lineno/end_col_offset (end)
        # We need byte offsets or character offsets
        
        entries.append({
            'key': key_str,
            'value': value_str,
            'numeric_id': numeric_id,
            'node': value_node
        })

    # Group IDs
    id_groups = defaultdict(list)
    for entry in entries:
        id_groups[entry['numeric_id']].append(entry)

    replacements = []

    for num_id, group in id_groups.items():
        if len(group) > 1:
            # Find longest value
            best_entry = max(group, key=lambda x: len(x['value']))
            best_value = best_entry['value']
            
            for entry in group:
                if str(entry['value']) != str(best_value): # Comparison
                    # We need to replace this node's source with best_value
                    # Construct replacement string as a triple-quoted string
                    replacement_str = '"""' + best_value + '"""'
                    
                    replacements.append({
                        'node': entry['node'],
                        'new_text': replacement_str
                    })

    if not replacements:
        print("No replacements found via AST.")
        return

    print(f"Applying {len(replacements)} replacements.")
    
    # AST modification is hard because we need correct source ranges.
    # ast.get_source_segment might work if available (py3.8+)
    # Or strict line/col usage.
    
    # Let's use line/col.
    # We must sort replacements in reverse order (bottom-up) to not mess up offsets.
    # Primary sort key: lineno descending, col_offset descending
    
    replacements.sort(key=lambda x: (x['node'].lineno, x['node'].col_offset), reverse=True)
    
    lines = content.splitlines(keepends=True)
    
    for r in replacements:
        node = r['node']
        start_line = node.lineno - 1
        start_col = node.col_offset
        end_line = node.end_lineno - 1
        end_col = node.end_col_offset
        
        # We assume the value is a string node.
        # Check if single line or multiline
        if start_line == end_line:
            line = lines[start_line]
            # Replace safely
            new_line = line[:start_col] + r['new_text'] + line[end_col:]
            lines[start_line] = new_line
        else:
            # Multiline replacement
            # First line: keep prefix
            first_line_kept = lines[start_line][:start_col]
            # Last line: keep suffix
            last_line_kept = lines[end_line][end_col:]
            
            # Construct new full block
            new_block = first_line_kept + r['new_text'] + last_line_kept
            
            # Assign to start_line and clear intermediate lines
            lines[start_line] = new_block
            for i in range(start_line + 1, end_line + 1):
                lines[i] = "" # Clear deleted lines
    
    # Reconstruct content
    new_content = "".join(lines)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Fixed content successfully.")

if __name__ == "__main__":
    fix_content_ast()
