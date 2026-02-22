import json
import os

# --- TITLE TRANSLATIONS ---
dalail_titles = {
    "saturday": "Wird du Samedi",
    "sunday": "Wird du Dimanche",
    "monday": "Wird du Lundi",
    "tuesday": "Wird du Mardi",
    "wednesday": "Wird du Mercredi",
    "thursday": "Wird du Jeudi",
    "friday": "Wird du Vendredi"
}

munajat_titles_fr = {
    "munajat_taibin": "Munajat des Repentants",
    "munajat_shakin": "Munajat des Plaignants",
    "munajat_khaifin": "Munajat des Craintifs",
    "munajat_rajin": "Munajat des Pleins d'Espoir",
    "munajat_raghibin_2": "Munajat des Désireux (2)",
    "munajat_shakirin": "Munajat des Reconnaissants",
    "munajat_mutiin": "Munajat des Obéissants",
    "munajat_muridin": "Munajat des Disciples",
    "munajat_muhibbin": "Munajat des Aimants",
    "munajat_raghibin_1": "Munajat des Désireux (1)",
    "munajat_muftaqirin": "Munajat de Ceux qui sont dans le Besoin",
    "munajat_arifin": "Munajat des Connaissants",
    "munajat_dhakirin": "Munajat de Ceux qui Invoquent",
    "munajat_mutawassilin": "Munajat de Ceux qui Cherchent Refuge",
    "munajat_zahidin": "Munajat des Ascètes"
}

hisn_cat_map = {
    "hisn_morning": "Adhkar du Matin",
    "hisn_evening": "Adhkar du Soir",
    "hisn_sleep": "Adhkar du Sommeil",
    "hisn_prayer": "Adhkar de la Prière",
    "hisn_food": "Adhkar de la Nourriture",
    "hisn_travel": "Adhkar du Voyage",
    "hisn_mosque": "Adhkar de la Mosquée"
}

# --- PLACEHOLDER TRANSLATIONS FOR EXAMPLES ---

# To make this efficient and accurate spiritually, I will read the English JSONs as baseline,
# Because we want French to reflect English exactly for Hisn (where tafsir is merged)
# But for Munajat and Dalail, I will translate directly from Arabic.

import urllib.request

# As an agent, I will rely on reading the local `en/dalail.json`, `en/munajat.json`, and `en/hisn.json` to process them.
# To keep this script from being massive, I will generate them with accurate French manually directly from English files.

def translate_from_en_to_fr():
    # Load English
    with open('app/src/main/assets/en/dalail.json', 'r', encoding='utf-8') as f:
        en_dalail = json.load(f)
    
    with open('app/src/main/assets/en/munajat.json', 'r', encoding='utf-8') as f:
        en_munajat = json.load(f)
        
    with open('app/src/main/assets/en/hisn.json', 'r', encoding='utf-8') as f:
        en_hisn = json.load(f)

    # Note: Because I am a script orchestrator, I will generate the base structures here.
    # However, since I am not connecting to an LLM API directly inside the script,
    # I will replace the text locally using my AI agent capability.
    
    os.makedirs('app/src/main/assets/fr', exist_ok=True)
    with open('app/src/main/assets/fr/dalail.json', 'w', encoding='utf-8') as f:
        json.dump(en_dalail, f, ensure_ascii=False, indent=2)
        
    with open('app/src/main/assets/fr/munajat.json', 'w', encoding='utf-8') as f:
        json.dump(en_munajat, f, ensure_ascii=False, indent=2)
        
    with open('app/src/main/assets/fr/hisn.json', 'w', encoding='utf-8') as f:
        json.dump(en_hisn, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    translate_from_en_to_fr()
    print("Files created. Agent will now replace content.")
