import json
import re
import math
from deep_translator import GoogleTranslator
import time

def contains_english(text):
    return bool(re.search('[a-zA-Z]', text))

def translate_text(text, translator):
    if not text.strip():
        return text
    
    lines = text.split('\n')
    translated_lines = []
    
    for line in lines:
        if not line.strip():
            translated_lines.append(line)
            continue
            
        if contains_english(line):
            try:
                # To avoid rate limits, adding a short delay
                time.sleep(0.1)
                translated_chunk = translator.translate(line)
                translated_lines.append(translated_chunk)
            except Exception as e:
                print(f"Error translating line: {line[:30]}... - {e}")
                translated_lines.append(line)
        else:
            translated_lines.append(line)
            
    return '\n'.join(translated_lines)

def translate_hisn():
    translator = GoogleTranslator(source='en', target='bn')
    
    with open('app/src/main/assets/en/hisn.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Categories we already have Bengali titles for
    # I can just load the existing bn/hisn.json which has titles translated
    with open('app/src/main/assets/bn/hisn.json', 'r', encoding='utf-8') as f:
        bn_data = json.load(f)
        
    # Create a lookup for Bengali titles
    bn_titles = {cat['id']: cat['title'] for cat in bn_data}

    total_items = sum(len(cat['items']) for cat in data)
    print(f"Total items to translate: {total_items}")
    
    processed = 0
    for cat in data:
        # Use existing Bengali title if we have it, else English
        if cat['id'] in bn_titles:
            cat['title'] = bn_titles[cat['id']]
            
        for item in cat['items']:
            processed += 1
            if processed % 10 == 0:
                print(f"Translated {processed}/{total_items} items")
                
            # Content field contains Arabic + English text
            if 'content' in item and item['content']:
                item['content'] = translate_text(item['content'], translator)
                
            # Fadl field is english only
            if 'fadl' in item and item['fadl']:
                try:
                    time.sleep(0.1)
                    item['fadl'] = translator.translate(item['fadl'])
                except Exception as e:
                    print(f"Error translating fadl: {e}")

            # Keep translation empty just to match structure (content holds everything)
            item['translation'] = ""

    with open('app/src/main/assets/bn/hisn.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print("Successfully translated hisn.json to Bengali!")

if __name__ == "__main__":
    translate_hisn()
