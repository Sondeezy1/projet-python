#!/usr/bin/env python3
"""
Script de migration pour convertir les années en dates complètes (JJ/MM/AAAA)
"""

import sqlite3
from datetime import datetime

def migrer_format_date():
    try:
        # Connexion à la base de données
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        # Créer une table temporaire avec la nouvelle structure
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS livres_temp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                auteur TEXT NOT NULL,
                date_publication TEXT NOT NULL
            )
        ''')
        
        # Récupérer les données existantes
        cursor.execute("SELECT id, titre, auteur, annee FROM livres")
        livres = cursor.fetchall()
        
        # Convertir et insérer les données dans la nouvelle table
        for id, titre, auteur, annee in livres:
            # S'assurer que l'année est sur 4 chiffres
            annee_str = str(annee).zfill(4)
            # Utiliser le 1er janvier de l'année comme date par défaut
            date_publication = f"01/01/{annee_str}"
            
            # Vérifier que la date est valide
            try:
                datetime.strptime(date_publication, "%d/%m/%Y")
                cursor.execute(
                    "INSERT INTO livres_temp (id, titre, auteur, date_publication) VALUES (?, ?, ?, ?)",
                    (id, titre, auteur, date_publication)
                )
            except ValueError as e:
                print(f"Erreur avec le livre {id} - {titre}: {e}")
                continue
        
        # Supprimer l'ancienne table
        cursor.execute("DROP TABLE livres")
        
        # Renommer la table temporaire
        cursor.execute("ALTER TABLE livres_temp RENAME TO livres")
        
        # Valider les changements
        conn.commit()
        print("Migration du format de date terminée avec succès!")
        
    except sqlite3.Error as e:
        print(f"Erreur lors de la migration : {e}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("Début de la migration du format de date...")
    migrer_format_date()
    print("Migration terminée.") 