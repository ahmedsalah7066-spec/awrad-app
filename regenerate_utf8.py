import json
import os

langs = ['ur', 'uz', 'id', 'tr']
files = ['awrad.json', 'dalail.json', 'munajat.json', 'hisn.json']

def rewrite():
    for lang in langs:
        for fname in files:
            path = f'app/src/main/assets/{lang}/{fname}'
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    rewrite()
    print("Files successfully rewritten with UTF-8.")
