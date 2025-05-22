#!/usr/bin/env python3
"""
Script pour vérifier et nettoyer la base de données
"""

import sqlite3
from datetime import datetime

def nettoyer_base_donnees():
    try:
        # Connexion à la base de données
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        # Créer une nouvelle base de données propre
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS livres_clean (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                auteur TEXT NOT NULL,
                date_publication TEXT NOT NULL
            )
        ''')
        
        # Lire les données existantes
        cursor.execute("SELECT * FROM livres")
        livres = cursor.fetchall()
        
        print(f"Nombre total de livres : {len(livres)}")
        
        # Vérifier et corriger chaque entrée
        for livre in livres:
            id, titre, auteur, date = livre
            print(f"\nTraitement du livre {id}:")
            print(f"Titre: {titre}")
            print(f"Auteur: {auteur}")
            print(f"Date actuelle: {date}")
            
            try:
                # Essayer de parser la date
                datetime.strptime(date, "%d/%m/%Y")
                date_valide = date
            except ValueError:
                # Si la date est invalide, créer une date par défaut
                print(f"Date invalide détectée : {date}")
                date_valide = "01/01/2000"
                print(f"Utilisation de la date par défaut : {date_valide}")
            
            # Insérer les données corrigées
            cursor.execute(
                "INSERT INTO livres_clean (id, titre, auteur, date_publication) VALUES (?, ?, ?, ?)",
                (id, titre, auteur, date_valide)
            )
        
        # Sauvegarder l'ancienne table
        cursor.execute("ALTER TABLE livres RENAME TO livres_backup")
        
        # Mettre en place la nouvelle table
        cursor.execute("ALTER TABLE livres_clean RENAME TO livres")
        
        # Valider les changements
        conn.commit()
        print("\nNettoyage de la base de données terminé avec succès!")
        
    except sqlite3.Error as e:
        print(f"Erreur SQLite : {e}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("Début du nettoyage de la base de données...")
    nettoyer_base_donnees()
    print("Nettoyage terminé.") 