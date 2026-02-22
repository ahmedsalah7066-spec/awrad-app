import json
import os

def prepare_bn():
    os.makedirs('app/src/main/assets/bn', exist_ok=True)
    
    files = ['dalail.json', 'munajat.json', 'hisn.json']
    for file in files:
        with open(f'app/src/main/assets/en/{file}', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        with open(f'app/src/main/assets/bn/{file}', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    prepare_bn()
    print("Base English JSON files copied to bn folder.")
