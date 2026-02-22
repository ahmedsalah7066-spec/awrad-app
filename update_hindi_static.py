import json
import os
import time
import re
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='en', target='hi')

def contains_latin_chars(text):
    return bool(re.search('[a-zA-Z]', text))

def translate_to_hindi(text):
    if not text or not text.strip():
        return text

    lines = text.split('\n')
    translated_lines = []
    
    for line in lines:
        if not line.strip():
            translated_lines.append(line)
            continue
            
        if contains_latin_chars(line):
            try:
                time.sleep(0.3)
                translated_chunk = translator.translate(line)
                translated_lines.append(translated_chunk)
            except Exception as e:
                print(f"Error: {e}")
                translated_lines.append(line)
        else:
            translated_lines.append(line)
            
    return '\n'.join(translated_lines)

def generate_static():
    print("Generating Static (HI)...")
    src_file = 'app/src/main/assets/data/static.json'
    if not os.path.exists(src_file):
        print(f"Source file not found: {src_file}")
        return
        
    with open(src_file, 'r', encoding='utf-8') as f:
        static_data = json.load(f)
        
    final_static = []
    for item in static_data:
        item_id = item['id']
        eng_translation = item.get('translation', '')
        
        hi_translation = ""
        if eng_translation:
            hi_translation = translate_to_hindi(eng_translation)
            
        final_static.append({
            "id": item_id,
            "content": item['content'],
            "translation": hi_translation
        })
        print(f"Translated {item_id}")
        
    with open('app/src/main/assets/hi/static.json', 'w', encoding='utf-8') as f:
        json.dump(final_static, f, ensure_ascii=False, indent=2)
    print("Saved hi/static.json")

if __name__ == "__main__":
    generate_static()
