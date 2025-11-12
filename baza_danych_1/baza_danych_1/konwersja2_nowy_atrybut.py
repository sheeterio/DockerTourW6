import json

# Parametry
floorval = 3
typ = "L1_Bud"

wejscie = 'Out1/L1_Bud_0.json'
wyjscie = 'Out2/L1_Bud_0.json'

with open(wejscie, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Dodaje atrybut do pliku .json
for feature in data.get('features', []):
    #feature['Floor'] = floorval
    feature['Typ'] = typ

with open(wyjscie, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Dodano atrybut do pliku {wyjscie}")
