import sqlite3
from typing import List, Optional, Tuple
from datetime import datetime
from models.livre import Livre
from models.emprunt import Emprunt

class Bibliotheque:
    """
    Classe gérant les opérations de la bibliothèque et la base de données SQLite.
    """
    
    def __init__(self, db_path: str = "database.db"):
        """
        Initialise la connexion à la base de données et crée la table si nécessaire.
        
        Args:
            db_path (str): Chemin vers le fichier de la base de données
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connecter()
        self.creer_tables()
    
    def connecter(self):
        """Établit la connexion à la base de données."""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    
    def deconnecter(self):
        """Ferme la connexion à la base de données."""
        if self.conn:
            self.conn.close()
    
    def creer_tables(self):
        """Crée les tables si elles n'existent pas."""
        # Table des livres
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS livres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                auteur TEXT NOT NULL,
                date_publication TEXT NOT NULL,
                UNIQUE(titre, auteur)
            )
        ''')
        
        # Table des emprunts
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS emprunts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                livre_id INTEGER NOT NULL,
                emprunteur TEXT NOT NULL,
                date_emprunt TEXT NOT NULL,
                date_retour_prevue TEXT NOT NULL,
                date_retour_reelle TEXT,
                FOREIGN KEY (livre_id) REFERENCES livres (id)
            )
        ''')
        
        self.conn.commit()
    
    def livre_est_disponible(self, livre_id: int) -> bool:
        """
        Vérifie si un livre est disponible pour l'emprunt.
        
        Args:
            livre_id (int): L'ID du livre à vérifier
            
        Returns:
            bool: True si le livre est disponible, False sinon
        """
        self.cursor.execute(
            """
            SELECT COUNT(*) FROM emprunts 
            WHERE livre_id = ? AND date_retour_reelle IS NULL
            """,
            (livre_id,)
        )
        return self.cursor.fetchone()[0] == 0
    
    def emprunter_livre(self, livre_id: int, emprunteur: str) -> Emprunt:
        """
        Enregistre l'emprunt d'un livre.
        
        Args:
            livre_id (int): L'ID du livre à emprunter
            emprunteur (str): Le nom de l'emprunteur
            
        Returns:
            Emprunt: L'emprunt créé
            
        Raises:
            ValueError: Si le livre n'existe pas ou n'est pas disponible
        """
        # Vérifier que le livre existe
        self.cursor.execute("SELECT id FROM livres WHERE id = ?", (livre_id,))
        if not self.cursor.fetchone():
            raise ValueError("Ce livre n'existe pas")
        
        # Vérifier que le livre est disponible
        if not self.livre_est_disponible(livre_id):
            raise ValueError("Ce livre n'est pas disponible")
        
        # Créer l'emprunt
        emprunt = Emprunt(livre_id, emprunteur)
        
        # Enregistrer l'emprunt
        self.cursor.execute(
            """
            INSERT INTO emprunts (livre_id, emprunteur, date_emprunt, date_retour_prevue)
            VALUES (?, ?, ?, ?)
            """,
            (emprunt.livre_id, emprunt.emprunteur, emprunt.date_emprunt, emprunt.date_retour_prevue)
        )
        self.conn.commit()
        
        emprunt.id = self.cursor.lastrowid
        return emprunt
    
    def retourner_livre(self, livre_id: int) -> bool:
        """
        Enregistre le retour d'un livre.
        
        Args:
            livre_id (int): L'ID du livre à retourner
            
        Returns:
            bool: True si le retour a été enregistré, False sinon
            
        Raises:
            ValueError: Si le livre n'est pas emprunté
        """
        # Vérifier que le livre est bien emprunté
        self.cursor.execute(
            """
            SELECT id FROM emprunts 
            WHERE livre_id = ? AND date_retour_reelle IS NULL
            """,
            (livre_id,)
        )
        emprunt = self.cursor.fetchone()
        if not emprunt:
            raise ValueError("Ce livre n'est pas emprunté")
        
        # Enregistrer la date de retour
        date_retour = datetime.now().strftime("%d/%m/%Y")
        self.cursor.execute(
            """
            UPDATE emprunts 
            SET date_retour_reelle = ? 
            WHERE livre_id = ? AND date_retour_reelle IS NULL
            """,
            (date_retour, livre_id)
        )
        self.conn.commit()
        return True
    
    def obtenir_emprunts_en_cours(self) -> List[Tuple[Emprunt, Livre]]:
        """
        Récupère la liste des emprunts en cours avec les informations des livres.
        
        Returns:
            List[Tuple[Emprunt, Livre]]: Liste des emprunts en cours avec leurs livres
        """
        self.cursor.execute(
            """
            SELECT e.id, e.livre_id, e.emprunteur, e.date_emprunt, e.date_retour_prevue,
                   e.date_retour_reelle, l.titre, l.auteur, l.date_publication
            FROM emprunts e
            JOIN livres l ON e.livre_id = l.id
            WHERE e.date_retour_reelle IS NULL
            """
        )
        resultats = []
        for row in self.cursor.fetchall():
            emprunt = Emprunt(
                livre_id=row[1],
                emprunteur=row[2],
                date_emprunt=row[3],
                date_retour_prevue=row[4],
                date_retour_reelle=row[5],
                id=row[0]
            )
            livre = Livre(
                titre=row[6],
                auteur=row[7],
                date_publication=row[8],
                id=row[1]
            )
            resultats.append((emprunt, livre))
        return resultats
    
    def obtenir_historique_emprunts(self, livre_id: Optional[int] = None) -> List[Tuple[Emprunt, Livre]]:
        """
        Récupère l'historique des emprunts.
        
        Args:
            livre_id (Optional[int]): Si spécifié, limite l'historique à un livre particulier
            
        Returns:
            List[Tuple[Emprunt, Livre]]: Liste des emprunts avec leurs livres
        """
        query = """
            SELECT e.id, e.livre_id, e.emprunteur, e.date_emprunt, e.date_retour_prevue,
                   e.date_retour_reelle, l.titre, l.auteur, l.date_publication
            FROM emprunts e
            JOIN livres l ON e.livre_id = l.id
        """
        params = []
        
        if livre_id is not None:
            query += " WHERE e.livre_id = ?"
            params.append(livre_id)
        
        query += " ORDER BY e.date_emprunt DESC"
        
        self.cursor.execute(query, params)
        resultats = []
        for row in self.cursor.fetchall():
            emprunt = Emprunt(
                livre_id=row[1],
                emprunteur=row[2],
                date_emprunt=row[3],
                date_retour_prevue=row[4],
                date_retour_reelle=row[5],
                id=row[0]
            )
            livre = Livre(
                titre=row[6],
                auteur=row[7],
                date_publication=row[8],
                id=row[1]
            )
            resultats.append((emprunt, livre))
        return resultats
    
    def livre_existe(self, titre: str, auteur: str) -> bool:
        """
        Vérifie si un livre existe déjà avec le même titre et auteur.
        
        Args:
            titre (str): Le titre du livre
            auteur (str): L'auteur du livre
            
        Returns:
            bool: True si le livre existe déjà, False sinon
        """
        self.cursor.execute(
            "SELECT COUNT(*) FROM livres WHERE titre = ? AND auteur = ?",
            (titre, auteur)
        )
        return self.cursor.fetchone()[0] > 0
    
    def ajouter_livre(self, livre: Livre) -> int:
        """
        Ajoute un nouveau livre à la base de données.
        
        Args:
            livre (Livre): Le livre à ajouter
            
        Returns:
            int: L'ID du livre ajouté
            
        Raises:
            ValueError: Si le livre existe déjà
        """
        # Valider le format de la date avant l'insertion
        livre.valider_date()
        
        # Vérifier si le livre existe déjà
        if self.livre_existe(livre.titre, livre.auteur):
            raise ValueError(f"Le livre '{livre.titre}' de {livre.auteur} existe déjà dans la bibliothèque")
        
        try:
            self.cursor.execute(
                "INSERT INTO livres (titre, auteur, date_publication) VALUES (?, ?, ?)",
                (livre.titre, livre.auteur, livre.date_publication)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError(f"Le livre '{livre.titre}' de {livre.auteur} existe déjà dans la bibliothèque")
    
    def obtenir_tous_les_livres(self) -> List[Livre]:
        """
        Récupère tous les livres de la base de données.
        
        Returns:
            List[Livre]: Liste de tous les livres
        """
        self.cursor.execute("SELECT id, titre, auteur, date_publication FROM livres")
        return [Livre(titre, auteur, date_publication, id) 
                for id, titre, auteur, date_publication in self.cursor.fetchall()]
    
    def rechercher_livre(self, terme: str) -> List[Livre]:
        """
        Recherche des livres par titre ou auteur.
        
        Args:
            terme (str): Terme de recherche
            
        Returns:
            List[Livre]: Liste des livres correspondants
        """
        terme = f"%{terme}%"
        self.cursor.execute(
            "SELECT id, titre, auteur, date_publication FROM livres WHERE titre LIKE ? OR auteur LIKE ?",
            (terme, terme)
        )
        return [Livre(titre, auteur, date_publication, id) 
                for id, titre, auteur, date_publication in self.cursor.fetchall()]
    
    def mettre_a_jour_livre(self, livre: Livre) -> bool:
        """
        Met à jour les informations d'un livre.
        
        Args:
            livre (Livre): Le livre avec les nouvelles informations
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
            
        Raises:
            ValueError: Si le nouveau titre/auteur existe déjà pour un autre livre
        """
        if not livre.id:
            return False
        
        # Valider le format de la date avant la mise à jour
        livre.valider_date()
        
        # Vérifier si un autre livre existe déjà avec le même titre et auteur
        self.cursor.execute(
            "SELECT id FROM livres WHERE titre = ? AND auteur = ? AND id != ?",
            (livre.titre, livre.auteur, livre.id)
        )
        if self.cursor.fetchone():
            raise ValueError(f"Un autre livre avec le titre '{livre.titre}' de {livre.auteur} existe déjà")
        
        try:
            self.cursor.execute(
                "UPDATE livres SET titre = ?, auteur = ?, date_publication = ? WHERE id = ?",
                (livre.titre, livre.auteur, livre.date_publication, livre.id)
            )
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.IntegrityError:
            raise ValueError(f"Un autre livre avec le titre '{livre.titre}' de {livre.auteur} existe déjà")
    
    def supprimer_livre(self, id: int) -> bool:
        """
        Supprime un livre de la base de données.
        
        Args:
            id (int): L'ID du livre à supprimer
            
        Returns:
            bool: True si la suppression a réussi, False sinon
        """
        self.cursor.execute("DELETE FROM livres WHERE id = ?", (id,))
        self.conn.commit()
        return self.cursor.rowcount > 0 