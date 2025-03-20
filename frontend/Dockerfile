FROM python:alpine3.20

# Mettre à jour les packets
RUN apk -U upgrade

# Définition du répertoire de travail
WORKDIR /app

# Copier et installer les dépendances python
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier tous les fichiers
COPY ./app.py /app/app.py
COPY ./templates /app/templates

# Exposer le port sur lequel l'application Flask écoute
EXPOSE 5000

CMD ["python3", "app.py"]
