#!/usr/bin/env python3
"""
Utilitaire en ligne de commande pour gérer la base de données de la bibliothèque.
Usage:
    python db_tools.py list                    # Liste tous les livres
    python db_tools.py add titre auteur année  # Ajoute un livre
    python db_tools.py delete id               # Supprime un livre par son ID
    python db_tools.py search terme            # Recherche des livres
    python db_tools.py clear                   # Vide la base de données
"""

import sys
from models.bibliotheque import Bibliotheque
from models.livre import Livre

def afficher_aide():
    print(__doc__)

def lister_livres(bibliotheque):
    """Affiche tous les livres de la base de données."""
    livres = bibliotheque.obtenir_tous_les_livres()
    if not livres:
        print("Aucun livre dans la base de données.")
        return
    
    print("\nListe des livres :")
    print("-" * 60)
    print(f"{'ID':4} | {'Titre':25} | {'Auteur':20} | {'Année':6}")
    print("-" * 60)
    for livre in livres:
        print(f"{livre.id:4} | {livre.titre[:25]:25} | {livre.auteur[:20]:20} | {livre.annee:6}")
    print("-" * 60)

def ajouter_livre(bibliotheque, titre, auteur, annee):
    """Ajoute un nouveau livre."""
    try:
        annee = int(annee)
        livre = Livre(titre=titre, auteur=auteur, annee=annee)
        id = bibliotheque.ajouter_livre(livre)
        print(f"Livre ajouté avec succès ! ID: {id}")
    except ValueError:
        print("Erreur : L'année doit être un nombre entier.")
    except Exception as e:
        print(f"Erreur lors de l'ajout du livre : {e}")

def supprimer_livre(bibliotheque, id):
    """Supprime un livre par son ID."""
    try:
        id = int(id)
        if bibliotheque.supprimer_livre(id):
            print(f"Livre avec ID {id} supprimé avec succès !")
        else:
            print(f"Aucun livre trouvé avec l'ID {id}")
    except ValueError:
        print("Erreur : L'ID doit être un nombre entier.")

def rechercher_livres(bibliotheque, terme):
    """Recherche des livres par titre ou auteur."""
    livres = bibliotheque.rechercher_livre(terme)
    if not livres:
        print(f"Aucun livre trouvé pour le terme '{terme}'")
        return
    
    print(f"\nRésultats de recherche pour '{terme}' :")
    print("-" * 60)
    print(f"{'ID':4} | {'Titre':25} | {'Auteur':20} | {'Année':6}")
    print("-" * 60)
    for livre in livres:
        print(f"{livre.id:4} | {livre.titre[:25]:25} | {livre.auteur[:20]:20} | {livre.annee:6}")
    print("-" * 60)

def vider_base_donnees(bibliotheque):
    """Vide complètement la base de données."""
    try:
        bibliotheque.cursor.execute("DELETE FROM livres")
        bibliotheque.conn.commit()
        print("Base de données vidée avec succès !")
    except Exception as e:
        print(f"Erreur lors de la suppression des données : {e}")

def main():
    bibliotheque = Bibliotheque()
    
    if len(sys.argv) < 2:
        afficher_aide()
        return
    
    commande = sys.argv[1].lower()
    
    try:
        if commande == "list":
            lister_livres(bibliotheque)
        
        elif commande == "add" and len(sys.argv) >= 5:
            ajouter_livre(bibliotheque, sys.argv[2], sys.argv[3], sys.argv[4])
        
        elif commande == "delete" and len(sys.argv) == 3:
            supprimer_livre(bibliotheque, sys.argv[2])
        
        elif commande == "search" and len(sys.argv) == 3:
            rechercher_livres(bibliotheque, sys.argv[2])
        
        elif commande == "clear":
            confirmation = input("Êtes-vous sûr de vouloir vider la base de données ? (oui/non) : ")
            if confirmation.lower() == "oui":
                vider_base_donnees(bibliotheque)
            else:
                print("Opération annulée.")
        
        else:
            afficher_aide()
    
    finally:
        bibliotheque.deconnecter()

if __name__ == "__main__":
    main() 