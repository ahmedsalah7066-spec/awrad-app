# -*- coding: utf-8 -*-
"""Add Titles with Numbers to Munajat"""
import json

# Define titles with numbers
TITLES = {
    "munajat_taibin": {
        "title": "1. مُنَاجَاةُ التَّائِبِينَ",
        "title_en": "1. The Whispered Prayer of the Repenters"
    },
    "munajat_shakin": {
        "title": "2. مُنَاجَاةُ الشَّاكِينَ",
        "title_en": "2. The Whispered Prayer of the Complainers"
    },
    "munajat_khaifin": {
        "title": "3. مُنَاجَاةُ الْخَائِفِينَ",
        "title_en": "3. The Whispered Prayer of the Fearful"
    },
    "munajat_rajin": {
        "title": "4. مُنَاجَاةُ الرَّاجِينَ",
        "title_en": "4. The Whispered Prayer of the Hopeful"
    },
    "munajat_raghibin_2": {
        "title": "5. مُنَاجَاةُ الرَّاغِبِينَ",
        "title_en": "5. The Whispered Prayer of the Desirers"
    },
    "munajat_shakirin": {
        "title": "6. مُنَاجَاةُ الشَّاكِرِينَ",
        "title_en": "6. The Whispered Prayer of the Thankful"
    },
    "munajat_mutiin": {
        "title": "7. مُنَاجَاةُ الْمُطِيعِينَ",
        "title_en": "7. The Whispered Prayer of the Obedient Ones"
    },
    "munajat_muridin": {
        "title": "8. مُنَاجَاةُ الْمُرِيدِينَ",
        "title_en": "8. The Whispered Prayer of the Devotees"
    },
    "munajat_muhibbin": {
        "title": "9. مُنَاجَاةُ الْمُحِبِّينَ",
        "title_en": "9. The Whispered Prayer of the Lovers"
    },
    "munajat_raghibin_1": { # Matches 'munajat_10_mutawassilin' or similar in mapping check
        "title": "10. مُنَاجَاةُ الْمُتَوَسِّلِينَ",
        "title_en": "10. The Whispered Prayer of the Seekers of Mediation"
    },
    "munajat_muftaqirin": {
        "title": "11. مُنَاجَاةُ الْمُفْتَقِرِينَ",
        "title_en": "11. The Whispered Prayer of the Utterly Poor"
    },
    "munajat_arifin": {
        "title": "12. مُنَاجَاةُ الْعَارِفِينَ",
        "title_en": "12. The Whispered Prayer of the Knowers"
    },
    "munajat_dhakirin": {
        "title": "13. مُنَاجَاةُ الذَّاكِرِينَ",
        "title_en": "13. The Whispered Prayer of the Rememberers"
    },
    "munajat_mutawassilin": { # Matches 'munajat_14_mutasimin'
        "title": "14. مُنَاجَاةُ الْمُعْتَصِمِينَ",
        "title_en": "14. The Whispered Prayer of the Seekers of Protection"
    },
    "munajat_zahidin": {
        "title": "15. مُنَاجَاةُ الزَّاهِدِينَ",
        "title_en": "15. The Whispered Prayer of the Ascetics"
    }
}

# The ID mapping used previously was:
# munajat_taibin -> munajat_01_taibin (in structure? No, existing IDs were kept)
# Wait, let's check existing IDs in the file first to match correctly.
with open('app/src/main/assets/data/munajat.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update titles
count = 0
for item in data:
    if item['id'] in TITLES:
        key = item['id']
        item['title'] = TITLES[key]['title']
        # Adding a new field for English Title or appending to translation?
        # Usually apps expect specific fields. If 'title_en' is not supported, 
        # let's put it as 'title_en' for now, or check if we should combine.
        # User asked "did you keep numbering", implying visual numbering.
        item['title_en'] = TITLES[key]['title_en']
        count += 1
        print(f"Updated titles for {key}")

# Save
with open('app/src/main/assets/data/munajat.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nAdded numbered titles to {count} munajat entries.")
