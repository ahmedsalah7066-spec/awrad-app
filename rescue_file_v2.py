import re

def rescue_file_v2():
    file_path = 'generate_uzbek_content.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern:
    # Group 1: """
    # Group 2: whitespace/comments (non-greedy, but must not contain comma)
    # Group 3: "dhikr
    
    regex = r'(""")([^,]*?)("dhikr)'
    
    count = 0
    def replacer(match):
        nonlocal count
        # match.group(0) is the full match
        # We want to insert comma after group 1
        
        # Double check there is no comma in group 2
        middle = match.group(2)
        if ',' in middle:
            return match.group(0) # Already has comma
            
        count += 1
        print(f"Fixing missing comma after: {match.group(0)[:20]}...")
        return match.group(1) + ',' + match.group(2) + match.group(3)

    new_content = re.sub(regex, replacer, content, flags=re.DOTALL)
    
    # Also handle single quotes if necessary, though triple quotes were the main edit
    # But wait, inconsistent keys might be "dhikr..." or "wednesday" etc?
    # The script mainly edited dhikr keys.
    
    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Rescued file: fixed {count} locations.")
    else:
        print("No missing commas found matching pattern.")

if __name__ == "__main__":
    rescue_file_v2()
