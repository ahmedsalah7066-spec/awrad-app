import json
import os
from deep_translator import GoogleTranslator
import time
import re

# To avoid repeating work, we will maintain a cache of translations.
TRANSLATION_CACHE_FILE = 'translation_cache_hi.json'
translation_cache = {}
if os.path.exists(TRANSLATION_CACHE_FILE):
    with open(TRANSLATION_CACHE_FILE, 'r', encoding='utf-8') as f:
        translation_cache = json.load(f)

def save_cache():
    with open(TRANSLATION_CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(translation_cache, f, ensure_ascii=False, indent=2)

translator = GoogleTranslator(source='en', target='hi')

def contains_latin_chars(text):
    return bool(re.search('[a-zA-Z]', text))

def translate_to_hindi(text):
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
            
        # We only want to translate lines that carry English text. Arabic text should remain Arabic.
        if contains_latin_chars(line):
            try:
                time.sleep(0.3) # API rate limit protection
                translated_chunk = translator.translate(line)
                translated_lines.append(translated_chunk)
            except Exception as e:
                print(f"Error translating line: {line[:30]}... - {e}")
                translated_lines.append(line) # Fallback to original
        else:
            translated_lines.append(line) # Keep Arabic or symbols intact
            
    result = '\n'.join(translated_lines)
    translation_cache[text] = result
    save_cache()
    return result

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# 1. GENERATE DALAIL
def generate_dalail():
    print("Generating Dalail (HI)...")
    with open('app/src/main/assets/en/dalail.json', 'r', encoding='utf-8') as f:
        dalail = json.load(f)
        
    for item in dalail:
        item['title'] = translate_to_hindi(item['title'])
        item['content'] = translate_to_hindi(item['content'])
        item['translation'] = "" # We merge into content for simplicity, UI handles it ok
        
    with open('app/src/main/assets/hi/dalail.json', 'w', encoding='utf-8') as f:
        json.dump(dalail, f, ensure_ascii=False, indent=2)

# 2. GENERATE MUNAJAT
def generate_munajat():
    print("Generating Munajat (HI)...")
    with open('app/src/main/assets/en/munajat.json', 'r', encoding='utf-8') as f:
        munajat = json.load(f)
        
    for item in munajat:
        item['title'] = translate_to_hindi(item['title'])
        item['content'] = translate_to_hindi(item['content'])
        item['translation'] = ""
        
    with open('app/src/main/assets/hi/munajat.json', 'w', encoding='utf-8') as f:
        json.dump(munajat, f, ensure_ascii=False, indent=2)

# 3. GENERATE HISN
def generate_hisn():
    print("Generating Hisn (HI)...")
    with open('app/src/main/assets/en/hisn.json', 'r', encoding='utf-8') as f:
        hisn = json.load(f)
        
    for cat in hisn:
        cat['title'] = translate_to_hindi(cat['title'])
        for item in cat['items']:
            if 'content' in item and item['content']:
                item['content'] = translate_to_hindi(item['content'])
                
            if 'fadl' in item and item['fadl']:
                item['fadl'] = translate_to_hindi(item['fadl'])
                
            item['translation'] = ""

    with open('app/src/main/assets/hi/hisn.json', 'w', encoding='utf-8') as f:
        json.dump(hisn, f, ensure_ascii=False, indent=2)

# 4. GENERATE STATIC
def generate_static():
    print("Generating Static (HI)...")
    static_data = [
        {
            "id": "terms_and_conditions",
            "title": "नियम और शर्तें",
            "content": "इस एप्लिकेशन का उपयोग करके, आप निम्नलिखित नियमों और शर्तों से सहमत हैं..."
        }
    ]
    with open('app/src/main/assets/hi/static.json', 'w', encoding='utf-8') as f:
        json.dump(static_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    ensure_dir('app/src/main/assets/hi')
    generate_dalail()
    generate_munajat()
    generate_hisn()
    generate_static()
    print("Successfully generated all Hindi JSON files!")
