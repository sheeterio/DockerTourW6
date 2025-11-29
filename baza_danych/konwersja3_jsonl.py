import os
import json

wejscie = './Out2/Features'
wyjscie = 'features.jsonl'

with open(wyjscie, 'w', encoding='utf-8') as zapis:
    for plik in os.listdir(wejscie):
        if not plik.endswith('.json'):
            continue
        file_path = os.path.join(wejscie, plik)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Błąd JSON w {plik}: {e}")
                continue

            features = data.get('features', [])
            for i, feature in enumerate(features):
                feature_doc = feature.copy()
                feature_doc['id'] = f"{os.path.splitext(plik)[0]}-{feature.get('id', i)}"
                json.dump(feature_doc, zapis, ensure_ascii=False)
                zapis.write('\n')

print(f"Zapisano plik {wyjscie}")
