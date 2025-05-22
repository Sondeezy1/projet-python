#!/usr/bin/env python3
"""
Script d'initialisation de la base de données
"""

import sqlite3
import os
from datetime import datetime
import time

def initialiser_base_donnees():
    # Essayer de supprimer l'ancienne base de données
    if os.path.exists("database.db"):
        try:
            os.remove("database.db")
            print("Ancienne base de données supprimée.")
        except PermissionError:
            print("La base de données est verrouillée. Tentative de connexion directe...")
            time.sleep(1)  # Attendre un peu
    
    try:
        # Créer une nouvelle base de données ou se connecter à l'existante
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        # Supprimer les tables si elles existent
        cursor.execute("DROP TABLE IF EXISTS emprunts")
        cursor.execute("DROP TABLE IF EXISTS livres")
        
        # Créer la table des livres avec contrainte d'unicité
        cursor.execute('''
            CREATE TABLE livres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                auteur TEXT NOT NULL,
                date_publication TEXT NOT NULL,
                UNIQUE(titre, auteur)
            )
        ''')
        
        # Créer la table des emprunts
        cursor.execute('''
            CREATE TABLE emprunts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                livre_id INTEGER NOT NULL,
                emprunteur TEXT NOT NULL,
                date_emprunt TEXT NOT NULL,
                date_retour_prevue TEXT NOT NULL,
                date_retour_reelle TEXT,
                FOREIGN KEY (livre_id) REFERENCES livres (id)
            )
        ''')
        
        # Ajouter quelques livres de test
        livres_test = [
            ("Le Petit Prince", "Antoine de Saint-Exupéry", "06/04/1943"),
            ("1984", "George Orwell", "08/06/1949"),
            ("Notre-Dame de Paris", "Victor Hugo", "16/03/1831")
        ]
        
        # Insérer les livres de test
        for titre, auteur, date in livres_test:
            try:
                cursor.execute(
                    "INSERT INTO livres (titre, auteur, date_publication) VALUES (?, ?, ?)",
                    (titre, auteur, date)
                )
            except sqlite3.IntegrityError:
                print(f"Le livre '{titre}' de {auteur} existe déjà.")
        
        # Valider les changements
        conn.commit()
        print("Base de données initialisée avec succès!")
        print(f"Nombre de livres ajoutés : {len(livres_test)}")
        
    except sqlite3.Error as e:
        print(f"Erreur lors de l'initialisation de la base de données : {e}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("Initialisation de la base de données...")
    initialiser_base_donnees()
    print("Initialisation terminée.") 