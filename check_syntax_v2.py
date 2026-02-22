
import re

def check_syntax(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Simple state machine to ignore strings and comments
    in_triple_quote = False
    in_string = False
    in_char = False
    in_line_comment = False
    in_block_comment = False
    
    curly_depth = 0
    paren_depth = 0
    
    i = 0
    while i < len(content):
        char = content[i]
        
        # Handle state transitions
        if in_line_comment:
            if char == '\n':
                in_line_comment = False
        elif in_block_comment:
            if content[i:i+2] == '*/':
                in_block_comment = False
                i += 1
        elif in_triple_quote:
            if content[i:i+3] == '"""':
                in_triple_quote = False
                i += 2
        elif in_string:
            if char == '"' and content[i-1] != '\\':
                in_string = False
        elif in_char:
            if char == "'" and content[i-1] != '\\':
                in_char = False
        else:
            # Not in any string/comment
            if content[i:i+3] == '"""':
                in_triple_quote = True
                i += 2
            elif char == '"':
                in_string = True
            elif char == "'":
                in_char = True
            elif content[i:i+2] == '//':
                in_line_comment = True
                i += 1
            elif content[i:i+2] == '/*':
                in_block_comment = True
                i += 1
            else:
                # Check for braces/parens
                if char == '{':
                    curly_depth += 1
                elif char == '}':
                    curly_depth -= 1
                    if curly_depth < 0:
                        line_num = content[:i].count('\n') + 1
                        print(f"ERROR: Unmatched closing brace }} at line {line_num}")
                elif char == '(':
                    paren_depth += 1
                elif char == ')':
                    paren_depth -= 1
                    if paren_depth < 0:
                        line_num = content[:i].count('\n') + 1
                        print(f"ERROR: Unmatched closing parenthesis ) at line {line_num}")

        i += 1

    print(f"Final Curly Depth: {curly_depth}")
    print(f"Final Paren Depth: {paren_depth}")
    if curly_depth != 0:
        print("ERROR: Unbalanced curly braces!")
    if paren_depth != 0:
        print("ERROR: Unbalanced parentheses!")

check_syntax("app/src/main/java/com/example/awrad/HisnDetailActivity.kt")
