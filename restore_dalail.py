# -*- coding: utf-8 -*-
"""Restore full awrad.json with 7 days and dual language content"""
import sys
import json
import os

# Add current directory to path
sys.path.append(os.getcwd())

from update_dalail_full import DALAIL_DATA
from update_dalail_english import DALAIL_ENGLISH

ORDER = ["saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday"]

final_data = []

print("Constructing full awrad.json data...")

for day_id in ORDER:
    # Get Arabic data
    arabic_entry = DALAIL_DATA.get(day_id)
    if not arabic_entry:
        print(f"Error: Missing Arabic data for {day_id}")
        continue
        
    # Get English data
    english_entry = DALAIL_ENGLISH.get(day_id)
    if not english_entry:
        print(f"Error: Missing English data for {day_id}")
        continue

    # Create new object
    new_obj = {
        "id": day_id,
        "day": day_id,
        "type": "dua",
        "title": arabic_entry["title"],
        "title_en": english_entry["title_en"],
        "content": arabic_entry["content"],
        "translation": english_entry["translation"]
    }
    final_data.append(new_obj)
    print(f"Processed {day_id}")

# Write to file
output_path = 'app/src/main/assets/data/awrad.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully restored {output_path} with {len(final_data)} entries.")
