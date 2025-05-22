from datetime import datetime

class Livre:
    """
    Classe représentant un livre dans la bibliothèque.
    
    Attributes:
        id (int): Identifiant unique du livre
        titre (str): Titre du livre
        auteur (str): Nom de l'auteur du livre
        date_publication (str): Date de publication au format JJ/MM/AAAA
    """
    
    def __init__(self, titre: str, auteur: str, date_publication: str, id: int = None):
        """
        Initialise un nouveau livre.
        
        Args:
            titre (str): Titre du livre
            auteur (str): Nom de l'auteur
            date_publication (str): Date de publication au format JJ/MM/AAAA
            id (int, optional): Identifiant unique du livre. Defaults to None.
        """
        self.id = id
        self.titre = titre
        self.auteur = auteur
        self.date_publication = date_publication
        
        # Valider le format de la date
        self.valider_date()
    
    def valider_date(self) -> bool:
        """
        Valide le format de la date (JJ/MM/AAAA).
        
        Returns:
            bool: True si la date est valide
            
        Raises:
            ValueError: Si le format de la date est invalide
        """
        try:
            datetime.strptime(self.date_publication, "%d/%m/%Y")
            return True
        except ValueError:
            raise ValueError("La date doit être au format JJ/MM/AAAA")
    
    def __str__(self) -> str:
        """
        Retourne une représentation textuelle du livre.
        
        Returns:
            str: Format: ID - Titre - Auteur (Date)
        """
        return f"{self.id} - {self.titre} - {self.auteur} ({self.date_publication})" 