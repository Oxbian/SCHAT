from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
import os
import pymysql

app = Flask(__name__)

# Récupération des variables d'environnement pour la base de données
DB_USER = os.getenv('DB_USER', 'chat')  # Utilisateur MySQL (par défaut 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'PWD')  # Mot de passe MySQL (par défaut 'password')
DB_HOST = os.getenv('DB_HOST', '192.168.122.232')  # Hôte de la base de données (par défaut 'localhost')
DB_NAME = os.getenv('DB_NAME', 'chat_db')  # Nom de la base de données (par défaut 'chat_db')

# Configuration de la base de données MySQL avec les variables d'environnement
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle de la table Message
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.String(200), nullable=False)

# Fonction pour créer la base de données et les tables si elles n'existent pas
def create_database():
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        connection.commit()
        cursor.close()
        connection.close()
    except OperationalError as e:
        print(f"Erreur lors de la création de la base de données : {e}")
        exit()

# Créer la base de données et les tables si elles n'existent pas
create_database()
with app.app_context():
    db.create_all()


# Route principale qui sert la page d'accueil (Frontend)
@app.route('/')
def index():
    return render_template('index.html')

# Route pour récupérer tous les messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([{'id': msg.id, 'contenu': msg.contenu} for msg in messages])

# Route pour envoyer un message
@app.route('/messages', methods=['POST'])
def post_message():
    contenu = request.json.get('contenu')
    if contenu:
        message = Message(contenu=contenu)
        db.session.add(message)
        db.session.commit()
        return jsonify({'message': 'Message ajouté avec succès'}), 201
    return jsonify({'error': 'Contenu du message manquant'}), 400

# Route pour modifier un message
@app.route('/messages/<int:id>', methods=['PUT'])
def edit_message(id):
    message = Message.query.get(id)
    if message:
        contenu = request.json.get('contenu')
        if contenu:
            message.contenu = contenu
            db.session.commit()
            return jsonify({'message': 'Message modifié avec succès'})
        return jsonify({'error': 'Contenu manquant'}), 400
    return jsonify({'error': 'Message non trouvé'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
