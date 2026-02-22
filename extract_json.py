import re
import json
import os

# Paths
BASE_DIR = r"c:/Users/ahmed/AndroidStudioProjects/awrad"
SRC_DIR = os.path.join(BASE_DIR, "app/src/main/java/com/example/awrad")
ASSETS_DIR = os.path.join(BASE_DIR, "app/src/main/assets/data")

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def extract_awrad():
    file_path = os.path.join(SRC_DIR, "Awrad.kt")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find Awrad items
    # Awrad(R.string.dalail_saturday, """CONTENT""", translation = """TRANSLATION"""
    pattern = re.compile(r'Awrad\(R\.string\.dalail_(\w+),\s*"""(.*?)""",\s*translation\s*=\s*"""(.*?)"""', re.DOTALL)
    
    matches = pattern.findall(content)
    data = []
    
    for day, arabic, translation in matches:
        data.append({
            "id": f"awrad_{day}",
            "day": day,
            "content": arabic.strip(),
            "translation": translation.strip(),
            "type": "dua" # Explicitly marking as dua/salawat
        })
        
    out_path = os.path.join(ASSETS_DIR, "awrad.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Extracted {len(data)} items to awrad.json")

def extract_munajat():
    file_path = os.path.join(SRC_DIR, "Munajat.kt")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find Munajat items
    # Munajat(R.string.munajat_zahidin, """CONTENT""", translation = """TRANSLATION"""
    # Note: the key name might vary (munajat_raghibin_1 etc)
    pattern = re.compile(r'Munajat\(R\.string\.(\w+),\s*"""(.*?)""",\s*translation\s*=\s*"""(.*?)"""', re.DOTALL)
    
    matches = pattern.findall(content)
    data = []
    
    for key, arabic, translation in matches:
        data.append({
            "id": key,
            "content": arabic.strip(),
            "translation": translation.strip(),
             "type": "dua" # Explicitly marking as dua
        })
        
    out_path = os.path.join(ASSETS_DIR, "munajat.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Extracted {len(data)} items to munajat.json")

def extract_hisn():
    file_path = os.path.join(SRC_DIR, "HisnContent.kt")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Categories regex
    # HisnCategory("morning", R.string.hisn_morning, R.drawable.ic_morning, MORNING_ADHKAR),
    cat_pattern = re.compile(r'HisnCategory\("(\w+)",\s*R\.string\.(\w+),\s*R\.drawable\.(\w+),\s*(\w+)\)', re.DOTALL)
    categories = cat_pattern.findall(content)
    
    # We need to extract the lists (MORNING_ADHKAR, etc.) separately first
    # This is a bit complex with regex because of nested objects.
    # We'll use a simpler approach: Extract the content of the lists by name
    
    json_categories = []
    
    for cat_id, title_res, icon_res, list_name in categories:
        # Find the list definition val NAME = listOf(...)
        list_regex = re.compile(f'val {list_name} = listOf\((.*?)\)\s*//', re.DOTALL) 
        # The list ends at the start of next val or end of file. 
        # Actually proper parsing of nested structures with regex is hard.
        # Let's try to match items inside the list block.
        
        # Approximate start of list
        start_idx = content.find(f"val {list_name} = listOf(")
        if start_idx == -1: continue
        
        # Find matching closing parenthesis? No, let's just use regex for DhikrItem inside the region.
        # We can limit the search region to be safe.
        next_val = content.find("val ", start_idx + 10)
        if next_val == -1: next_val = len(content)
        
        list_content = content[start_idx:next_val]
        
        # DhikrItem(
        #     arabic = "...",
        #     count = N,
        #     explanation = mapOf(
        #         "en" to "..."
        #     ),
        #     fadl = mapOf(...)
        # )
        
        # We will iterate over DhikrItem constructors in this block
        # Because of nesting strings, regex is tricky. 
        # Simplification: Assume 'DhikrItem(' starts an item.
        # We will parse each argument.
        
        items = []
        item_iter = re.finditer(r'DhikrItem\(', list_content)
        
        # This is getting complicated to do robustly with regex for the nested maps.
        # Alternative: The format is very consistent.
        # arabic = "..."
        # count = N
        # explanation = mapOf( "en" to "..." )
        # fadl = ...
        
        # Let's clean the string and define logical blocks
        
        # split by DhikrItem(
        chunks = list_content.split("DhikrItem(")
        for chunk in chunks[1:]: # skip first empty chunk
            # cleanup closing )
            # This is risky. 
            pass

    # RE-STRATEGY for Hisn:
    # Since HisnContent.kt formatting is very structured, we can match specific patterns.
    # arabic = "(.*?)" (DOTALL)
    # count = (\d+)
    # explanation = mapOf\s*\(\s*"en" to "(.*?)"\s*\)
    # fadl = mapOf\s*\(\s*"ar" to "(.*?)",\s*"en" to "(.*?)"\s*\) OR just "en"
    
    # Actually, let's just do a big findall on the whole file, but associating them with categories is key.
    
    # Let's process categories one by one mapping
    
    final_data = []
    
    for cat_id, title_res, icon_res, list_name in categories:
        cat_data = {
            "id": cat_id,
            "title_res": title_res,
            "icon_res": icon_res,
            "items": []
        }
        
        # Find the list body
        # val LIST_NAME = listOf( ... )
        # We assume the list ends before the next "val "
        pattern_list_body = re.search(f'val {list_name} = listOf\((.*?)(\n\s*//|\n\s*val|\Z)', content, re.DOTALL)
        if not pattern_list_body:
            print(f"Could not find list body for {list_name}")
            continue
            
        body = pattern_list_body.group(1)
        
        # Split by "DhikrItem("
        # This is a crude parser but might work given the file consistency
        item_chunks = body.split("DhikrItem(")
        
        for chunk in item_chunks:
            if not chunk.strip(): continue # Skip empty start
            
            # Extract arabic
            # arabic = "..."
            # We need to handle escaped quotes inside content if any? 
            # The file uses tripple quotes for long text? No, looks like normal quotes based on reading,
            # actually MORNING_ADHKAR uses "..." but has newlines \n.
            # Wait, reading step 192 output:
            # arabic = "أَعُوذُ ...", 
            # It uses normal double quotes.
            
            # Regex for arabic arg: arabic = "(.*?)"\s*,
            # Use non-greedy match. 
            # Problem: if string contains \", regex might break.
            # But the file content shows "..." without escaping " usually, or standard java escaping.
            
            arabic_match = re.search(r'arabic = "(.*?)"', chunk, re.DOTALL)
            count_match = re.search(r'count = (\d+)', chunk)
            
            # Explanation map
            # explanation = mapOf( "en" to "..." )
            expl_match = re.search(r'explanation = mapOf\(\s*"en" to "(.*?)"\s*\)', chunk, re.DOTALL)
            
            # Fadl map
            # fadl = mapOf(...)
            # It might have "ar" and "en" or just "en" or be missing.
            fadl_ar = ""
            fadl_en = ""
            
            if 'fadl = mapOf' in chunk:
                fadl_ar_m = re.search(r'"ar" to "(.*?)"', chunk, re.DOTALL)
                fadl_en_m = re.search(r'"en" to "(.*?)"', chunk, re.DOTALL)
                if fadl_ar_m: fadl_ar = fadl_ar_m.group(1)
                if fadl_en_m: fadl_en = fadl_en_m.group(1)
            
            if arabic_match:
                arabic_text = arabic_match.group(1).replace('\\n', '\n')
                count = int(count_match.group(1)) if count_match else 1
                translation = expl_match.group(1).replace('\\n', '\n') if expl_match else ""
                
                # Check if Quran
                # Heuristic: Contains "Surah" or "Ayat" in translation OR starts with "Bismi" + "Qul" (logic in python?)
                # User asked to hide non-Quranic Arabic in English.
                # We need to flag is_quran.
                # Heuristics:
                # 1. Translation mentions "Surah" or "Ayat".
                # 2. Arabic content is clearly Quran (Ayat Kursi, Muawwidhat).
                
                is_quran = False
                lower_trans = translation.lower()
                if "surah" in lower_trans or "ayat" in lower_trans:
                    is_quran = True
                
                cat_data["items"].append({
                    "arabic": arabic_text,
                    "count": count,
                    "translation": translation,
                    "fadl": {"ar": fadl_ar, "en": fadl_en} if fadl_ar or fadl_en else {},
                    "is_quran": is_quran
                })
        
        final_data.append(cat_data)
        
    out_path = os.path.join(ASSETS_DIR, "hisn.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
    print(f"Extracted {len(final_data)} categories to hisn.json")

if __name__ == "__main__":
    ensure_dir(ASSETS_DIR)
    extract_awrad()
    extract_munajat()
    # extract_hisn() # Disabled to prevent overwriting fixed JSON with empty data from HisnContent.kt
