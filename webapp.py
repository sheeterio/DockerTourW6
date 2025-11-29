# Importy
from flask import Flask, jsonify, request, send_from_directory, abort
from flask_cors import CORS
from pymongo import MongoClient
import os, json, hashlib, time

# Aplikacja TourW6
app = Flask(__name__, static_folder='static', static_url_path='/')
CORS(app)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.static_folder),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

# Baza danych Mongo
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["GeocentrumDB"]
features_col = db["features"]
static_col = db["static"]

# Pierwszy setup Mongo z plików JSONL
def load_jsonl_to_mongo(filepath, collection):
    if collection.count_documents({}) == 0 and os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            docs = [json.loads(line) for line in f]
        if docs:
            collection.insert_many(docs)
            print(f"Inserted {len(docs)} docs into {collection.name}")

load_jsonl_to_mongo('./baza_danych/features.jsonl', features_col)
load_jsonl_to_mongo('./baza_danych/static.jsonl', static_col)

# Fetchingi z aplikacji
@app.route('/features') # Warstwy mapowe - dynamiczne
def get_features():
    data = list(features_col.find({}, {'_id': False}))
    return jsonify(data)
@app.route('/static') # Warstwy mapowe - statyczne
def get_static():
    data = list(static_col.find({}, {'_id': False}))
    return jsonify(data)
    
# Klucz haszowania zdjęć
kluczyk = "hugisko"

# Funkcja tworząca klucz dostępu dla panoramy na 5 minut
def klucz_dostepu(zdj, trwa=300):
    wygas = int(time.time()) + trwa
    znaki = f"{zdj}:{wygas}:{kluczyk}"
    token = hashlib.sha256(znaki.encode()).hexdigest()
    return token, wygas

# Funkcja weryfikująca klucz dostępu
def weryfikuj_klucz(zdj, klucz, wygas):
    if not (zdj and klucz and wygas):
        return False  # Brak parametru
    try:
        if int(wygas) < time.time():
            return False  # Klucz wygasł
    except (TypeError, ValueError):
        return False  # Niewłaściwy czas
    znaki = f"{zdj}:{wygas}:{kluczyk}"
    porownanie = hashlib.sha256(znaki.encode()).hexdigest()
    return porownanie == klucz

# Fetch panoramy
@app.route('/get-pano')
def get_pano():
    container = request.args.get('container')
    zdj = request.args.get('name')

    if container not in ['panos']:
        abort(400, "Zły kontener")
    if not zdj or not zdj.endswith('.avif'):
        abort(400, "Zły plik")

    pano_path = os.path.join(app.static_folder, container)
    file_path = os.path.join(pano_path, zdj)
    if not os.path.exists(file_path):
        abort(404, "Nie znaleziono pliku")

    token, wygas = klucz_dostepu(zdj)
    access_url = f"/serve-pano?container={container}&name={zdj}&key={token}&exp={wygas}"
    return jsonify({"url": access_url})

# Wyświetlenie zdjęcia
@app.route('/serve-pano')
def serve_pano():
    container = request.args.get('container')
    zdj = request.args.get('name')
    klucz = request.args.get('key')
    wygas = request.args.get('exp')
    if not all([container, zdj]):
        abort(400, "Brak parametrów zapytania")
    folder = os.path.join(app.static_folder, container)
    file_path = os.path.join(folder, zdj)
    if not os.path.exists(file_path):
        abort(404, description="Plik nie istnieje")
    if not klucz or not wygas or not weryfikuj_klucz(zdj, klucz, wygas):
        abort(403, description="Brak dostępu: nieprawidłowy lub brakujący klucz")
    return send_from_directory(folder, zdj)

# Ładowanie aplikacji
@app.route('/')
def root():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000) #debug=True