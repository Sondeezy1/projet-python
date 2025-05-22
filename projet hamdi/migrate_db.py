#!/usr/bin/env python3
"""
Script de migration pour transférer les données de bibliotheque.db vers database.db
"""

import sqlite3
import os

def migrer_donnees():
    # Vérifier si l'ancienne base de données existe
    ancien_chemin = "data/bibliotheque.db"
    if not os.path.exists(ancien_chemin):
        print("Aucune ancienne base de données trouvée.")
        return

    # Connexion aux deux bases de données
    try:
        ancien_db = sqlite3.connect(ancien_chemin)
        nouveau_db = sqlite3.connect("database.db")
        
        # Copier les données
        ancien_cursor = ancien_db.cursor()
        nouveau_cursor = nouveau_db.cursor()
        
        # Créer la table dans la nouvelle base de données si elle n'existe pas
        nouveau_cursor.execute('''
            CREATE TABLE IF NOT EXISTS livres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                auteur TEXT NOT NULL,
                annee INTEGER NOT NULL
            )
        ''')
        
        # Récupérer les données de l'ancienne base
        ancien_cursor.execute("SELECT titre, auteur, annee FROM livres")
        livres = ancien_cursor.fetchall()
        
        if not livres:
            print("Aucune donnée trouvée dans l'ancienne base de données.")
            return
        
        # Insérer les données dans la nouvelle base
        for livre in livres:
            nouveau_cursor.execute(
                "INSERT INTO livres (titre, auteur, annee) VALUES (?, ?, ?)",
                livre
            )
        
        # Valider les changements
        nouveau_db.commit()
        
        print(f"{len(livres)} livre(s) transféré(s) avec succès!")
        
        # Fermer les connexions
        ancien_db.close()
        nouveau_db.close()
        
        # Sauvegarder l'ancienne base de données avec un nouveau nom
        backup_path = "data/bibliotheque.db.backup"
        os.rename(ancien_chemin, backup_path)
        print(f"L'ancienne base de données a été sauvegardée sous : {backup_path}")
        
    except sqlite3.Error as e:
        print(f"Erreur lors de la migration : {e}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")

if __name__ == "__main__":
    print("Début de la migration des données...")
    migrer_donnees()
    print("Migration terminée.") 