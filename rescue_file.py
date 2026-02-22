import re

def rescue_file():
    file_path = 'generate_uzbek_content.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern: triple quote, optional whitespace, then "dhikr
    # we want to insert comma and newline
    # Note: the file uses 4 spaces indentation typically
    
    # We look for """ followed immediately by whitespace and then a key start
    # captured group 1: """
    # captured group 2: whitespace
    # captured group 3: "dhikr
    
    # We want to replace with """,\n    "dhikr
    
    pattern = r'("""\s*)("dhikr)'
    
    # Check matches
    matches = re.findall(pattern, content)
    print(f"Found {len(matches)} places potentially missing comma.")
    
    # We should only replace if there isn't a comma already
    # But checking for negative lookbehind is tricky with whitespace.
    
    # Better pattern: """ followed by whitespace (including no newline?) followed by "dhikr
    # If there is a comma, it would be """, ...
    
    # So we search for """ [no comma] ... "dhikr
    
    # Pattern: """ followed by whitespace characters EXCEPT comma, then "dhikr
    regex = r'("""[^,]*?)("dhikr)'
    
    # But wait, [^,]*? might match newlines correctly.
    # The issue is we saw `"""    "dhikr` on the same line.
    
    def replacer(match):
        # match.group(0) is the whole thing like """    "dhikr
        # We want """,\n    "dhikr
        # But we need to be careful about what was matched.
        
        # simple heuristic: if no comma in the whitespace, add it.
        text = match.group(0)
        if ',' not in text:
             return match.group(1) + ',\n    ' + match.group(2)
        return text

    new_content = re.sub(r'(""")(\s*)("dhikr)', lambda m: m.group(1) + ',\n    ' + m.group(3), content)
    
    # also check for single quotes if any
    new_content = re.sub(r'(")(\s*)("dhikr)', lambda m: m.group(1) + ',\n    ' + m.group(3), new_content)

    # Wait, the second regex might match "key": "value" ... "next_key"
    # value ending in " needs comma.
    # But we need to ensure we don't assume every " followed by "dhikr is a missing comma.
    # e.g. "key": "value" is fine.
    # But "key": "value" "next_key" is missing comma.
    
    # Focus on the Triple quotes first as that's where I mainly edited.
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Rescued file.")

if __name__ == "__main__":
    rescue_file()
