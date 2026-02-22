
import re

def check_syntax(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check triple quotes
    triple_quotes = len(re.findall(r'"""', content))
    print(f"Triple quotes count: {triple_quotes}")
    if triple_quotes % 2 != 0:
        print("ERROR: Odd number of triple quotes!")
        
        # Find locations
        for i, match in enumerate(re.finditer(r'"""', content)):
            line_num = content[:match.start()].count('\n') + 1
            print(f"Triple quote {i+1} at line {line_num}")

    # Check parentheses depth
    depth = 0
    for i, char in enumerate(content):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
            if depth < 0:
                line_num = content[:i].count('\n') + 1
                print(f"ERROR: Unmatched closing parenthesis at line {line_num}")
                return

    if depth != 0:
        print(f"ERROR: Unmatched opening parenthesis. Final depth: {depth}")

check_syntax("app/src/main/java/com/example/awrad/Munajat.kt")
