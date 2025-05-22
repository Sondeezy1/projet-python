# Gestion de Bibliothèque

Une application de gestion de bibliothèque développée en Python avec interface graphique Tkinter et base de données SQLite.

## Fonctionnalités

- Ajouter des livres (titre, auteur, année)
- Rechercher des livres par titre ou auteur
- Mettre à jour les informations des livres
- Supprimer des livres
- Liste complète des livres avec scrollbar
- Validation des données saisies
- Base de données persistante

## Prérequis

- Python 3.x
- Tkinter (généralement inclus avec Python)
- SQLite3 (inclus avec Python)

## Installation

1. Clonez ce dépôt :
```bash
git clone [URL_DU_REPO]
cd gestion-bibliotheque
```

2. Aucune dépendance externe n'est nécessaire car le projet utilise uniquement des modules standards Python.

## Utilisation

1. Lancez l'application :
```bash
python main.py
```

2. Interface utilisateur :
   - Remplissez les champs (titre, auteur, année)
   - Utilisez les boutons pour effectuer les opérations
   - La liste des livres se met à jour automatiquement
   - Cliquez sur un livre dans la liste pour charger ses informations

## Structure du projet

```
bibliotheque/
    ├── models/
    │   ├── __init__.py
    │   ├── livre.py
    │   └── bibliotheque.py
    ├── views/
    │   ├── __init__.py
    │   └── interface_graphique.py
    ├── data/
    │   └── bibliotheque.db
    ├── main.py
    ├── requirements.txt
    └── README.md
```

## Idées d'améliorations futures

1. Export des données en CSV
2. Statistiques sur la bibliothèque
3. Tri des livres par différents critères
4. Interface modernisée avec CustomTkinter
5. Système de catégories/genres pour les livres
6. Recherche avancée avec filtres multiples
7. Import de données depuis un fichier

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

# Gestion de Bibliothèque - Processus de Retour d'un Livre

## Processus de Retour d'un Livre

Le retour d'un livre dans l'application se fait en suivant ces étapes :

1. **Accéder à l'interface des emprunts**
   - Ouvrir l'application
   - Cliquer sur l'onglet "Emprunts"

2. **Identifier le livre à retourner**
   - Dans le tableau "Emprunts en cours", repérer le livre à retourner
   - Noter l'ID du livre dans la première colonne
   - Vérifier le statut du livre (En cours ou En retard)

3. **Effectuer le retour**
   - Saisir l'ID du livre dans le champ "ID du livre"
   - Cliquer sur le bouton "Retourner"

4. **Confirmation du retour**
   - Un message de confirmation s'affiche si le retour est réussi
   - Le livre disparaît de la liste des emprunts en cours
   - Le statut du livre est automatiquement mis à jour dans la base de données

## Messages d'erreur possibles

- **"Veuillez saisir l'ID du livre"** : Le champ ID est vide
- **"L'ID du livre doit être un nombre"** : L'ID saisi n'est pas un nombre valide
- **"Ce livre n'est pas emprunté"** : Tentative de retour d'un livre qui n'est pas actuellement emprunté

## Notes importantes

- Un livre ne peut être retourné que s'il est actuellement emprunté
- La date de retour est automatiquement enregistrée à la date du jour
- Le système met à jour automatiquement le statut des emprunts (En cours, En retard, Retourné)
- La liste des emprunts en cours est automatiquement rafraîchie après chaque retour 