import os
import re

wejscie = "./FunkcjeJS"
wyjscie = "./Out1"

os.makedirs(wyjscie, exist_ok=True)

for plik in os.listdir(wejscie):
    if plik.endswith(".js"):
        pliku = os.path.join(wejscie, plik)
        zapis = os.path.join(wyjscie, os.path.splitext(plik)[0] + ".json")
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        # Usuń wrapper funkcji .js
        nowy = re.sub(r'^\s*var\s+\w+\s*=\s*', '', content)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(nowy)

print("Konwersja zakończona.")
