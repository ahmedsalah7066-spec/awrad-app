import json
import os
import time
import re
from deep_translator import GoogleTranslator

TRANSLATION_CACHE_FILE = 'translation_cache_fa.json'
translation_cache = {}
if os.path.exists(TRANSLATION_CACHE_FILE):
    with open(TRANSLATION_CACHE_FILE, 'r', encoding='utf-8') as f:
        translation_cache = json.load(f)

def save_cache():
    with open(TRANSLATION_CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(translation_cache, f, ensure_ascii=False, indent=2)

translator = GoogleTranslator(source='en', target='fa')

def contains_latin_chars(text):
    return bool(re.search('[a-zA-Z]', text))

def translate_to_persian(text):
    if not text or not text.strip():
        return text
    
    if text in translation_cache:
        return translation_cache[text]

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
                print(f"Error translating line: {line[:30]}... - {e}")
                translated_lines.append(line)
        else:
            translated_lines.append(line)
            
    result = '\n'.join(translated_lines)
    translation_cache[text] = result
    save_cache()
    return result

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# 1. GENERATE DALAIL
def generate_dalail():
    print("Generating Dalail (FA)...")
    with open('app/src/main/assets/en/dalail.json', 'r', encoding='utf-8') as f:
        dalail = json.load(f)
        
    for item in dalail:
        item['title'] = translate_to_persian(item['title'])
        item['content'] = translate_to_persian(item['content'])
        item['translation'] = ""
        
    with open('app/src/main/assets/fa/dalail.json', 'w', encoding='utf-8') as f:
        json.dump(dalail, f, ensure_ascii=False, indent=2)

# 2. GENERATE MUNAJAT
def generate_munajat():
    print("Generating Munajat (FA)...")
    with open('app/src/main/assets/en/munajat.json', 'r', encoding='utf-8') as f:
        munajat = json.load(f)
        
    for item in munajat:
        item['title'] = translate_to_persian(item['title'])
        item['content'] = translate_to_persian(item['content'])
        item['translation'] = ""
        
    with open('app/src/main/assets/fa/munajat.json', 'w', encoding='utf-8') as f:
        json.dump(munajat, f, ensure_ascii=False, indent=2)

# 3. GENERATE HISN
def generate_hisn():
    print("Generating Hisn (FA)...")
    with open('app/src/main/assets/en/hisn.json', 'r', encoding='utf-8') as f:
        hisn = json.load(f)
        
    for cat in hisn:
        cat['title'] = translate_to_persian(cat['title'])
        for item in cat['items']:
            if 'content' in item and item['content']:
                item['content'] = translate_to_persian(item['content'])
                
            if 'fadl' in item and item['fadl']:
                item['fadl'] = translate_to_persian(item['fadl'])
                
            item['translation'] = ""

    with open('app/src/main/assets/fa/hisn.json', 'w', encoding='utf-8') as f:
        json.dump(hisn, f, ensure_ascii=False, indent=2)

# 4. GENERATE STATIC
def generate_static():
    print("Generating Static (FA)...")
    with open('app/src/main/assets/data/static.json', 'r', encoding='utf-8') as f:
        static_data = json.load(f)
        
    final_static = []
    for item in static_data:
        # Translate the English translation text.
        hi_translation = ""
        eng_translation = item.get('translation', '')
        if eng_translation:
            hi_translation = translate_to_persian(eng_translation)
            
        final_static.append({
            "id": item['id'],
            "content": item['content'],
            "translation": hi_translation
        })
        
    with open('app/src/main/assets/fa/static.json', 'w', encoding='utf-8') as f:
        json.dump(final_static, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    ensure_dir('app/src/main/assets/fa')
    generate_dalail()
    generate_munajat()
    generate_hisn()
    generate_static()
    print("Successfully generated all Persian JSON files!")
