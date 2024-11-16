import os
import datetime
import psycopg2
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Connexion à la base de données
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, client_encoding='utf8')
    return conn

# Initialisation de la base de données
def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    # Création des tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS livres (
            id SERIAL PRIMARY KEY,
            Titre TEXT NOT NULL UNIQUE,
            auteur TEXT NOT NULL,
            annee INTEGER NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS lecteurs (
            id SERIAL PRIMARY KEY,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            UNIQUE (nom, prenom)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS emprunts (
            id SERIAL PRIMARY KEY,
            id_livre INTEGER REFERENCES livres(id),
            id_lecteur INTEGER REFERENCES lecteurs(id),
            date_emprunt DATE,
            date_retour DATE
        )
    ''')

    # Vérifier si les tables contiennent déjà des données
    c.execute('SELECT COUNT(*) FROM livres')
    if c.fetchone()[0] == 0:  # Si aucun livre n'est présent
        livres = [
            ('Une si longue lettre', 'Mariama Ba', 1979),
            ('Les bouts de bois de Dieu', 'Ousmane Sembene', 1960),
            ('Le Baobab fou', 'Ken Bugul', 1982),
            ('Le soleil des indépendances', 'Ahmadou Kourouma', 1968)
        ]
        c.executemany('INSERT INTO livres (Titre, auteur, annee) VALUES (%s, %s, %s)', livres)

    c.execute('SELECT COUNT(*) FROM lecteurs')
    if c.fetchone()[0] == 0:  # Si aucun lecteur n'est présent
        lecteurs = [
            ('Isabelle Olive', 'Kantoussan'),
            ('Gomis', 'Pierre'),
            ('Faye', 'Lorie'),
            ('Diatta', 'Marie-Louise')
        ]
        c.executemany('INSERT INTO lecteurs (nom, prenom) VALUES (%s, %s)', lecteurs)

    conn.commit()
    conn.close()


init_db()

# Routes
@app.route('/')
def index():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM livres')
    livres = c.fetchall()
    c.execute('SELECT * FROM lecteurs')
    lecteurs = c.fetchall()
    conn.close()
    return render_template('index.html', livres=livres, lecteurs=lecteurs)

@app.route('/emprunter', methods=['POST'])
def emprunter_livre():
    data = request.get_json()
    id_livre = data['id_livre']
    id_lecteur = data['id_lecteur']

    conn = get_db_connection()
    c = conn.cursor()

    # Vérifie si le livre est déjà emprunté
    c.execute('SELECT * FROM emprunts WHERE id_livre = %s AND date_retour IS NULL', (id_livre,))
    emprunt = c.fetchone()

    if emprunt:
        return jsonify({'message': 'Ce livre est déjà emprunté'})

    date_emprunt = datetime.datetime.now().strftime('%Y-%m-%d')
    c.execute('''
        INSERT INTO emprunts (id_livre, id_lecteur, date_emprunt)
        VALUES (%s, %s, %s)
    ''', (id_livre, id_lecteur, date_emprunt))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Livre emprunté avec succès'})

@app.route('/retourner/<int:livre_id>', methods=['PUT'])
def retourner_livre(livre_id):
    conn = get_db_connection()
    c = conn.cursor()

    date_retour = datetime.datetime.now().strftime('%Y-%m-%d')
    c.execute('''
        UPDATE emprunts
        SET date_retour = %s
        WHERE id_livre = %s AND date_retour IS NULL
    ''', (date_retour, livre_id))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Livre retourné avec succès'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
