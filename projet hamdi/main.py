#!/usr/bin/env python3
"""
Point d'entrée principal de l'application de gestion de bibliothèque.
"""

from models.bibliotheque import Bibliotheque
from views.interface_graphique import InterfaceGraphique

def main():
    """Fonction principale de l'application."""
    # Création de l'instance de la bibliothèque
    bibliotheque = Bibliotheque()
    
    # Création et démarrage de l'interface graphique
    interface = InterfaceGraphique(bibliotheque)
    interface.demarrer()

if __name__ == "__main__":
    main() 