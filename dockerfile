# Użyj oficjalnego obrazu z Pythonem
FROM python

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj pliki wymagań
COPY requirements.txt .

# Zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj aplikację
COPY . .

# Wystaw port
EXPOSE 3000

# Uruchom aplikację
CMD ["python", "webapp.py"]