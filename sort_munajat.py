# -*- coding: utf-8 -*-
"""Sort munajat entries 1-15"""
import json

with open('app/src/main/assets/data/munajat.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Define correct order of IDs
ORDER = [
    "munajat_taibin",        # 1
    "munajat_shakin",        # 2
    "munajat_khaifin",       # 3
    "munajat_rajin",         # 4
    "munajat_raghibin_2",    # 5
    "munajat_shakirin",      # 6
    "munajat_mutiin",        # 7
    "munajat_muridin",       # 8
    "munajat_muhibbin",      # 9
    "munajat_raghibin_1",    # 10 (mutawassilin/raghibin mismatch resolved by key)
    "munajat_muftaqirin",    # 11
    "munajat_arifin",        # 12
    "munajat_dhakirin",      # 13
    "munajat_mutawassilin",  # 14
    "munajat_zahidin"        # 15
]

# Create a map for quick lookup
data_map = {item['id']: item for item in data}

# Create sorted list
sorted_data = []
for munajat_id in ORDER:
    if munajat_id in data_map:
        sorted_data.append(data_map[munajat_id])
    else:
        print(f"Warning: ID {munajat_id} not found in data!")

# Save sorted list
with open('app/src/main/assets/data/munajat.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_data, f, ensure_ascii=False, indent=2)

print(f"Sorted {len(sorted_data)} munajat entries in correct sequence (1-15).")
