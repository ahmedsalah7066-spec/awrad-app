#!/usr/bin/env python3
"""
Simple Python Data Exporter - Reads from Kotlin source files and exports to JSON
This replaces the need to run DataExporter.kt from Android Studio
"""

import json
import re
from pathlib import Path

def read_kotlin_file(file_path):
    """Read a Kotlin file and return its content"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_string_content(text, start_marker, end_marker='"""'):
    """Extract content between triple quotes"""
    pattern = rf'{re.escape(start_marker)}\s*=\s*"""(.*?)"""'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches[0].strip() if matches else None

def export_hisn_content(project_dir):
    """Export Hisn Al-Muslim content"""
    print("Exporting Hisn Al-Muslim content...")
    
    hisn_file = project_dir / "app/src/main/java/com/example/awrad/HisnContent.kt"
    content = read_kotlin_file(hisn_file)
    
    # Parse categories and items (simplified - we'll create basic structure)
    duas = []
    
    # Extract category IDs
    category_pattern = r'HisnCategory\(\s*id\s*=\s*"([^"]+)"'
    categories_found = re.findall(category_pattern, content)
    
    print(f"   Found {len(categories_found)} Hisn categories")
    
    # Extract DhikrItems
    dhikr_pattern = r'DhikrItem\(\s*arabic\s*=\s*"""(.*?)"""'
    dhikr_items = re.findall(dhikr_pattern, content, re.DOTALL)
    
    print(f"   Found {len(dhikr_items)} Dhikr items")
    
    # Create basic structure
    for idx, arabic_text in enumerate(dhikr_items):
        duas.append({
            "id": idx + 1,
            "categoryId": categories_found[min(idx // 10, len(categories_found) - 1)] if categories_found else "morning",
            "arabicText": arabic_text.strip(),
            "count": 1,
            "orderIndex": idx
        })
    
    return duas

def export_munajat(project_dir):
    """Export Munajat content"""
    print("Exporting Munajat content...")
    
    munajat_file = project_dir / "app/src/main/java/com/example/awrad/Munajat.kt"
    content = read_kotlin_file(munajat_file)
    
    # Extract Munajat content
    munajat_pattern = r'Munajat\(\s*titleResId\s*=\s*R\.string\.(\w+),\s*content\s*=\s*"""(.*?)"""'
    munajat_items = re.findall(munajat_pattern, content, re.DOTALL)
    
    duas = []
    for idx, (title_res, arabic_text) in enumerate(munajat_items):
        duas.append({
            "categoryId": "munajat",
            "titleResId": title_res,
            "arabicText": arabic_text.strip(),
            "count": 1,
            "orderIndex": idx
        })
    
    print(f"   Found {len(duas)} Munajat")
    return duas

def export_awrad(project_dir):
    """Export Awrad (Dalail) content"""
    print("Exporting Awrad (Dalail) content...")
    
    awrad_file = project_dir / "app/src/main/java/com/example/awrad/Awrad.kt"
    content = read_kotlin_file(awrad_file)
    
    # Extract Awrad content
    awrad_pattern = r'Awrad\(\s*dayResId\s*=\s*R\.string\.(\w+),\s*content\s*=\s*"""(.*?)"""'
    awrad_items = re.findall(awrad_pattern, content, re.DOTALL)
    
    duas = []
    for idx, (day_res, arabic_text) in enumerate(awrad_items):
        duas.append({
            "categoryId": "awrad",
            "dayResId": day_res,
            "arabicText": arabic_text.strip(),
            "count": 1,
            "orderIndex": idx
        })
    
    print(f"   Found {len(duas)} Awrad")
    return duas

def export_daily_essentials(project_dir):
    """Export Daily Essentials (Istiftah and Ibrahimi)"""
    print("Exporting Daily Essentials...")
    
    wird_file = project_dir / "app/src/main/java/com/example/awrad/WirdContent.kt"
    content = read_kotlin_file(wird_file)
    
    # Extract ISTIFTAH
    istiftah = extract_string_content(content, 'val ISTIFTAH')
    # Extract IBRAHIMI
    ibrahimi = extract_string_content(content, 'val IBRAHIMI')
    
    duas = []
    if istiftah:
        duas.append({
            "categoryId": "daily_essentials",
            "title": "دعاء الاستفتاح",
            "arabicText": istiftah,
            "count": 1,
            "orderIndex": 0
        })
    
    if ibrahimi:
        duas.append({
            "categoryId": "daily_essentials",
            "title": "الصلاة الإبراهيمية",
            "arabicText": ibrahimi,
            "count": 1,
            "orderIndex": 1
        })
    
    print(f"   Found {len(duas)} Daily Essentials")
    return duas

def export_categories():
    """Create categories structure"""
    categories = [
        # Hisn categories
        {"id": "morning", "titleResId": "hisn_morning", "iconResId": 0, "orderIndex": 0, "type": "hisn"},
        {"id": "evening", "titleResId": "hisn_evening", "iconResId": 0, "orderIndex": 1, "type": "hisn"},
        {"id": "sleep", "titleResId": "hisn_sleep", "iconResId": 0, "orderIndex": 2, "type": "hisn"},
        {"id": "prayer", "titleResId": "hisn_prayer", "iconResId": 0, "orderIndex": 3, "type": "hisn"},
        {"id": "wakeup", "titleResId": "hisn_wakeup", "iconResId": 0, "orderIndex": 4, "type": "hisn"},
        {"id": "quran", "titleResId": "hisn_quran", "iconResId": 0, "orderIndex": 5, "type": "hisn"},
        {"id": "home", "titleResId": "hisn_home", "iconResId": 0, "orderIndex": 6, "type": "hisn"},
        {"id": "mosque", "titleResId": "hisn_mosque", "iconResId": 0, "orderIndex": 7, "type": "hisn"},
        {"id": "travel", "titleResId": "hisn_travel", "iconResId": 0, "orderIndex": 8, "type": "hisn"},
        {"id": "various", "titleResId": "hisn_various", "iconResId": 0, "orderIndex": 9, "type": "hisn"},
        # Munajat
        {"id": "munajat", "titleResId": "munajat_title", "iconResId": 0, "orderIndex": 100, "type": "munajat"},
        # Awrad
        {"id": "awrad", "titleResId": "dalail_title", "iconResId": 0, "orderIndex": 101, "type": "awrad"},
        # Daily Essentials
        {"id": "daily_essentials", "titleResId": "daily_essentials_title", "iconResId": 0, "orderIndex": 102, "type": "essential"},
    ]
    return categories

def main():
    print("=" * 60)
    print("Simple Python Data Exporter")
    print("=" * 60)
    
    # Determine project directory
    project_dir = Path(__file__).parent.parent
    print(f"\nProject directory: {project_dir}")
    
    # Create output directory
    output_dir = project_dir / "firebase_data_export"
    output_dir.mkdir(exist_ok=True)
    print(f"Output directory: {output_dir}\n")
    
    try:
        # Export categories
        print("Exporting categories...")
        categories = export_categories()
        with open(output_dir / "categories.json", "w", encoding="utf-8") as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)
        print(f"[OK] Exported {len(categories)} categories\n")
        
        # Export Hisn content
        hisn_duas = export_hisn_content(project_dir)
        with open(output_dir / "hisn_duas.json", "w", encoding="utf-8") as f:
            json.dump(hisn_duas, f, ensure_ascii=False, indent=2)
        print(f"[OK] Exported Hisn content\n")
        
        # Export Munajat
        munajat_duas = export_munajat(project_dir)
        with open(output_dir / "munajat.json", "w", encoding="utf-8") as f:
            json.dump(munajat_duas, f, ensure_ascii=False, indent=2)
        print(f"[OK] Exported Munajat\n")
        
        # Export Awrad
        awrad_duas = export_awrad(project_dir)
        with open(output_dir / "awrad_dalail.json", "w", encoding="utf-8") as f:
            json.dump(awrad_duas, f, ensure_ascii=False, indent=2)
        print(f"[OK] Exported Awrad\n")
        
        # Export Daily Essentials
        daily_duas = export_daily_essentials(project_dir)
        with open(output_dir / "daily_essentials.json", "w", encoding="utf-8") as f:
            json.dump(daily_duas, f, ensure_ascii=False, indent=2)
        print(f"[OK] Exported Daily Essentials\n")
        
        print("=" * 60)
        print("Export Complete!")
        print("=" * 60)
        print(f"\nFiles saved in: {output_dir.absolute()}")
        print("\nNext: Run upload_to_firebase.py to upload to Firestore")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
