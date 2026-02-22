import json
import os

# Configuration
BASE_DIR = r"c:/Users/ahmed/AndroidStudioProjects/awrad"
ASSETS_DIR = os.path.join(BASE_DIR, "app/src/main/assets/data")
HISN_JSON_PATH = os.path.join(ASSETS_DIR, "hisn.json")

# Category Metadata Mapping
# Maps categoryId (from the item) to (title_res_name, icon_res_name)
CATEGORY_METADATA = {
    "hisn_morning": {"title": "hisn_morning", "icon": "ic_morning"},
    "hisn_evening": {"title": "hisn_evening", "icon": "ic_evening"},
    "hisn_sleep": {"title": "hisn_sleep", "icon": "ic_sleep"},
    "hisn_prayer": {"title": "hisn_prayer", "icon": "ic_prayer"},
    "hisn_food": {"title": "hisn_food", "icon": "ic_food"},
    "hisn_travel": {"title": "hisn_travel", "icon": "ic_travel"},
    "hisn_mosque": {"title": "hisn_mosque", "icon": "ic_mosque"},
    "hisn_tasbeehat": {"title": "hisn_tasbeehat", "icon": "ic_tasbeehat"},
}

def restructure_hisn():
    if not os.path.exists(HISN_JSON_PATH):
        print(f"Error: {HISN_JSON_PATH} not found.")
        return

    print(f"Reading {HISN_JSON_PATH}...")
    with open(HISN_JSON_PATH, 'r', encoding='utf-8') as f:
        items = json.load(f)

    if not isinstance(items, list):
        print("Error: JSON root is not a list.")
        return

    # Check if already structured (if the first item has "items" key)
    if len(items) > 0 and "items" in items[0]:
        print("JSON is already structured. Checking for field fixes...")
        # Iterate over existing categories and fix items
        print(f"Iterating over {len(items)} categories...")
        for category in items:
            if "items" not in category: 
                print(f"Skipping category {category.get('id')} - no items")
                continue
            
            print(f"Processing category {category.get('id')} with {len(category['items'])} items")
            new_items = []
            for item in category["items"]:
                new_item = item.copy()
                
                # 1. Fix Arabic Text
                if "arabicText" in new_item:
                    new_item["arabic"] = new_item.pop("arabicText")
                elif "arabic" not in new_item:
                    # If neither exists (rare), skip or keep as is
                    pass
                
                # 2. Fix Translation
                if "explanation" in new_item and isinstance(new_item["explanation"], dict):
                    explanation = new_item["explanation"]
                    if "en" in explanation:
                        new_item["translation"] = explanation["en"]
                    new_item.pop("explanation")
                
                # Ensure 'fadl'
                if "fadl" not in new_item:
                    new_item["fadl"] = {}
                    
                new_items.append(new_item)
            
            category["items"] = new_items
            
        # Write back directly
        with open(HISN_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
        print("Successfully updated existing hierarchical structure.")
        return

    print(f"Found {len(items)} flat items. Grouping by category...")

    grouped_data = {}

    for item in items:
        cat_id = item.get("categoryId")
        if not cat_id:
            print(f"Warning: Item {item.get('id')} has no categoryId. Skipping.")
            continue

        if cat_id not in grouped_data:
            metadata = CATEGORY_METADATA.get(cat_id, {"title": "app_name", "icon": "ic_launcher_foreground"})
            grouped_data[cat_id] = {
                "id": cat_id,
                "title_res": metadata["title"],
                "icon_res": metadata["icon"],
                "items": []
            }
        
        # Add item to the category's list
        # We need to transform fields to match JsonDataLoader expectations:
        # arabicText -> arabic
        # explanation.en -> translation
        
        new_item = item.copy()
        
        # 1. Fix Arabic Text
        if "arabicText" in new_item:
            new_item["arabic"] = new_item.pop("arabicText")
        
        # 2. Fix Translation
        # JsonDataLoader reads 'translation' string and puts it into explanation['en']
        # Current JSON has 'explanation': {'en': '...'}
        if "explanation" in new_item and isinstance(new_item["explanation"], dict):
            explanation = new_item["explanation"]
            if "en" in explanation:
                new_item["translation"] = explanation["en"]
            # We can keep 'explanation' or remove it, JsonDataLoader ignores it.
            # But let's keep it clean.
            new_item.pop("explanation")
            
        # Ensure 'fadl' is correctly formatted
        if "fadl" not in new_item:
            new_item["fadl"] = {}
        
        grouped_data[cat_id]["items"].append(new_item)

    # Convert dictionary values to list
    final_list = list(grouped_data.values())

    # Sort categories? Optional, but let's keep a consistent order
    # Order defined by keys in CATEGORY_METADATA
    ordered_list = []
    for key in CATEGORY_METADATA.keys():
        if key in grouped_data:
            # Sort items by orderIndex
            grouped_data[key]["items"].sort(key=lambda x: x.get("orderIndex", 0))
            ordered_list.append(grouped_data[key])
            del grouped_data[key]
    
    # Add any remaining categories (if any unknown ones existed)
    for cat in grouped_data.values():
         cat["items"].sort(key=lambda x: x.get("orderIndex", 0))
         ordered_list.append(cat)

    print(f"Created {len(ordered_list)} categories.")

    # Write back to file
    with open(HISN_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(ordered_list, f, indent=2, ensure_ascii=False)
    
    print("Successfully rewritten hisn.json with hierarchical structure.")

if __name__ == "__main__":
    restructure_hisn()
