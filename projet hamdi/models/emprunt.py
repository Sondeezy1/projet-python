from datetime import datetime, timedelta

class Emprunt:
    """
    Classe représentant un emprunt de livre.
    
    Attributes:
        id (int): Identifiant unique de l'emprunt
        livre_id (int): Identifiant du livre emprunté
        emprunteur (str): Nom de l'emprunteur
        date_emprunt (str): Date de l'emprunt au format JJ/MM/AAAA
        date_retour_prevue (str): Date de retour prévue au format JJ/MM/AAAA
        date_retour_reelle (str): Date de retour réelle au format JJ/MM/AAAA (None si non retourné)
    """
    
    DUREE_PRET = 14  # Durée de prêt en jours
    
    def __init__(self, livre_id: int, emprunteur: str, date_emprunt: str = None,
                 date_retour_prevue: str = None, date_retour_reelle: str = None, id: int = None):
        """
        Initialise un nouvel emprunt.
        
        Args:
            livre_id (int): ID du livre emprunté
            emprunteur (str): Nom de l'emprunteur
            date_emprunt (str, optional): Date d'emprunt. Si None, utilise la date du jour.
            date_retour_prevue (str, optional): Date de retour prévue. Si None, calculée automatiquement.
            date_retour_reelle (str, optional): Date de retour réelle. Defaults to None.
            id (int, optional): ID de l'emprunt. Defaults to None.
        """
        self.id = id
        self.livre_id = livre_id
        self.emprunteur = emprunteur
        
        # Si pas de date d'emprunt fournie, utiliser la date du jour
        if date_emprunt is None:
            self.date_emprunt = datetime.now().strftime("%d/%m/%Y")
        else:
            self.date_emprunt = date_emprunt
        
        # Si pas de date de retour prévue fournie, calculer automatiquement
        if date_retour_prevue is None:
            date_emp = datetime.strptime(self.date_emprunt, "%d/%m/%Y")
            date_ret = date_emp + timedelta(days=self.DUREE_PRET)
            self.date_retour_prevue = date_ret.strftime("%d/%m/%Y")
        else:
            self.date_retour_prevue = date_retour_prevue
        
        self.date_retour_reelle = date_retour_reelle
    
    @property
    def est_en_retard(self) -> bool:
        """
        Vérifie si l'emprunt est en retard.
        
        Returns:
            bool: True si l'emprunt est en retard, False sinon
        """
        if self.date_retour_reelle is not None:
            return False
        
        date_retour = datetime.strptime(self.date_retour_prevue, "%d/%m/%Y")
        return datetime.now() > date_retour
    
    @property
    def est_en_cours(self) -> bool:
        """
        Vérifie si l'emprunt est en cours.
        
        Returns:
            bool: True si l'emprunt est en cours, False sinon
        """
        return self.date_retour_reelle is None
    
    def retourner(self) -> None:
        """Marque le livre comme retourné à la date du jour."""
        self.date_retour_reelle = datetime.now().strftime("%d/%m/%Y")
    
    def __str__(self) -> str:
        """
        Retourne une représentation textuelle de l'emprunt.
        
        Returns:
            str: Représentation de l'emprunt
        """
        status = "En cours" if self.est_en_cours else "Retourné"
        if self.est_en_retard:
            status = "En retard"
        
        return (f"Emprunt {self.id} - Livre {self.livre_id} - {self.emprunteur} - "
                f"Emprunté le {self.date_emprunt} - Retour prévu le {self.date_retour_prevue} - "
                f"Status: {status}") 