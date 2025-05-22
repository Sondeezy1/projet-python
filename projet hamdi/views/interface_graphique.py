import customtkinter as ctk
from tkinter import messagebox
from typing import Callable, List, Optional
from datetime import datetime
from models.livre import Livre
from models.bibliotheque import Bibliotheque
from views.interface_emprunts import InterfaceEmprunts

class InterfaceGraphique:
    """
    Classe gérant l'interface graphique moderne de l'application avec CustomTkinter.
    """
    
    def __init__(self, bibliotheque: Bibliotheque):
        """
        Initialise l'interface graphique moderne.
        
        Args:
            bibliotheque (Bibliotheque): Instance de la classe Bibliotheque
        """
        # Configuration de CustomTkinter
        ctk.set_appearance_mode("system")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        
        # Configuration de la fenêtre principale
        self.bibliotheque = bibliotheque
        self.fenetre = ctk.CTk()
        self.fenetre.title("Gestion de Bibliothèque")
        self.fenetre.geometry("1200x800")
        self.fenetre.minsize(1000, 600)
        
        # Création du notebook pour les onglets
        self.notebook = ctk.CTkTabview(self.fenetre)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Onglet Livres
        self.tab_livres = self.notebook.add("Livres")
        self.tab_livres.grid_rowconfigure(0, weight=1)
        self.tab_livres.grid_columnconfigure(1, weight=1)
        
        # Onglet Emprunts
        self.tab_emprunts = self.notebook.add("Emprunts")
        
        self._creer_widgets()
        self._placer_widgets()
        self.rafraichir_liste()
    
    def _creer_widgets(self):
        """Crée tous les widgets modernes de l'interface."""
        # Frame gauche pour les contrôles (dans l'onglet Livres)
        self.frame_controles = ctk.CTkFrame(self.tab_livres)
        
        # Frame pour l'ajout de livre
        self.frame_ajout = ctk.CTkFrame(self.frame_controles)
        self.label_ajout = ctk.CTkLabel(
            self.frame_ajout,
            text="Ajouter un livre",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        
        # Champs de saisie
        self.entry_titre = ctk.CTkEntry(
            self.frame_ajout,
            placeholder_text="Titre du livre",
            width=250
        )
        
        self.entry_auteur = ctk.CTkEntry(
            self.frame_ajout,
            placeholder_text="Nom de l'auteur",
            width=250
        )
        
        # Frame pour la date avec 3 champs
        self.frame_date = ctk.CTkFrame(self.frame_ajout)
        
        self.entry_jour = ctk.CTkEntry(
            self.frame_date,
            placeholder_text="JJ",
            width=50
        )
        
        self.label_sep1 = ctk.CTkLabel(self.frame_date, text="/")
        
        self.entry_mois = ctk.CTkEntry(
            self.frame_date,
            placeholder_text="MM",
            width=50
        )
        
        self.label_sep2 = ctk.CTkLabel(self.frame_date, text="/")
        
        self.entry_annee = ctk.CTkEntry(
            self.frame_date,
            placeholder_text="AAAA",
            width=70
        )
        
        # Boutons d'action
        self.btn_ajouter = ctk.CTkButton(
            self.frame_ajout,
            text="Ajouter",
            command=self._ajouter_livre,
            width=250
        )
        
        # Frame pour la recherche
        self.frame_recherche = ctk.CTkFrame(self.frame_controles)
        self.label_recherche = ctk.CTkLabel(
            self.frame_recherche,
            text="Rechercher",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        
        self.entry_recherche = ctk.CTkEntry(
            self.frame_recherche,
            placeholder_text="Rechercher un livre...",
            width=250
        )
        self.entry_recherche.bind("<KeyRelease>", self._recherche_dynamique)
        
        # Frame droite pour la liste des livres
        self.frame_liste = ctk.CTkFrame(self.tab_livres)
        self.label_liste = ctk.CTkLabel(
            self.frame_liste,
            text="Bibliothèque",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        
        # Tableau des livres avec scrollbar
        self.frame_tableau = ctk.CTkScrollableFrame(
            self.frame_liste,
            width=700,
            height=600
        )
        
        # En-têtes du tableau
        self.frame_entetes = ctk.CTkFrame(self.frame_tableau)
        self.label_id = ctk.CTkLabel(
            self.frame_entetes,
            text="ID",
            width=50,
            font=ctk.CTkFont(weight="bold")
        )
        self.label_titre_col = ctk.CTkLabel(
            self.frame_entetes,
            text="Titre",
            width=300,
            font=ctk.CTkFont(weight="bold")
        )
        self.label_auteur_col = ctk.CTkLabel(
            self.frame_entetes,
            text="Auteur",
            width=200,
            font=ctk.CTkFont(weight="bold")
        )
        self.label_date_col = ctk.CTkLabel(
            self.frame_entetes,
            text="Date",
            width=100,
            font=ctk.CTkFont(weight="bold")
        )
        
        # Switch pour le thème
        self.switch_theme = ctk.CTkSwitch(
            self.frame_controles,
            text="Mode sombre",
            command=self._changer_theme,
            onvalue="dark",
            offvalue="light"
        )
        
        # Boutons de contrôle pour le livre sélectionné
        self.frame_actions = ctk.CTkFrame(self.frame_controles)
        self.btn_modifier = ctk.CTkButton(
            self.frame_actions,
            text="Modifier",
            command=self._mettre_a_jour_livre,
            width=120,
            state="disabled"
        )
        self.btn_supprimer = ctk.CTkButton(
            self.frame_actions,
            text="Supprimer",
            command=self._supprimer_livre,
            width=120,
            fg_color="red",
            hover_color="darkred",
            state="disabled"
        )
        
        # Interface des emprunts
        self.interface_emprunts = InterfaceEmprunts(self.tab_emprunts, self.bibliotheque)
    
    def _placer_widgets(self):
        """Place tous les widgets dans la fenêtre avec un layout moderne."""
        # Frame des contrôles (gauche) dans l'onglet Livres
        self.frame_controles.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Frame d'ajout
        self.frame_ajout.pack(pady=(0, 20), padx=10, fill="x")
        self.label_ajout.pack(pady=(10, 20))
        self.entry_titre.pack(pady=5)
        self.entry_auteur.pack(pady=5)
        
        # Frame de la date
        self.frame_date.pack(pady=5)
        self.entry_jour.pack(side="left", padx=2)
        self.label_sep1.pack(side="left", padx=2)
        self.entry_mois.pack(side="left", padx=2)
        self.label_sep2.pack(side="left", padx=2)
        self.entry_annee.pack(side="left", padx=2)
        
        self.btn_ajouter.pack(pady=10)
        
        # Frame de recherche
        self.frame_recherche.pack(pady=(0, 20), padx=10, fill="x")
        self.label_recherche.pack(pady=(10, 10))
        self.entry_recherche.pack(pady=(0, 10))
        
        # Frame des actions
        self.frame_actions.pack(pady=(0, 20), padx=10, fill="x")
        self.btn_modifier.pack(side="left", padx=5)
        self.btn_supprimer.pack(side="left", padx=5)
        
        # Switch thème
        self.switch_theme.pack(pady=20)
        
        # Frame de la liste (droite)
        self.frame_liste.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.label_liste.pack(pady=10)
        self.frame_tableau.pack(expand=True, fill="both", padx=10, pady=10)
        
        # En-têtes du tableau
        self.frame_entetes.pack(fill="x", padx=5, pady=5)
        self.label_id.pack(side="left", padx=5)
        self.label_titre_col.pack(side="left", padx=5)
        self.label_auteur_col.pack(side="left", padx=5)
        self.label_date_col.pack(side="left", padx=5)
        
        # Interface des emprunts
        self.interface_emprunts.pack(expand=True, fill="both")
    
    def _changer_theme(self):
        """Change le thème de l'application."""
        if self.switch_theme.get() == "dark":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
    
    def _obtenir_date_complete(self) -> str:
        """
        Récupère la date complète à partir des champs de saisie.
        
        Returns:
            str: Date au format JJ/MM/AAAA
        """
        jour = self.entry_jour.get().zfill(2)
        mois = self.entry_mois.get().zfill(2)
        annee = self.entry_annee.get()
        return f"{jour}/{mois}/{annee}"
    
    def _decomposer_date(self, date: str):
        """
        Décompose une date au format JJ/MM/AAAA dans les champs de saisie.
        
        Args:
            date (str): Date au format JJ/MM/AAAA
        """
        try:
            jour, mois, annee = date.split('/')
            self.entry_jour.delete(0, "end")
            self.entry_jour.insert(0, jour)
            self.entry_mois.delete(0, "end")
            self.entry_mois.insert(0, mois)
            self.entry_annee.delete(0, "end")
            self.entry_annee.insert(0, annee)
        except ValueError:
            self._vider_champs_date()
    
    def _vider_champs_date(self):
        """Vide les champs de saisie de la date."""
        self.entry_jour.delete(0, "end")
        self.entry_mois.delete(0, "end")
        self.entry_annee.delete(0, "end")
    
    def _valider_champs(self) -> bool:
        """
        Valide les champs de saisie.
        
        Returns:
            bool: True si les champs sont valides, False sinon
        """
        if not self.entry_titre.get().strip():
            messagebox.showerror("Erreur", "Le titre est obligatoire")
            return False
        
        if not self.entry_auteur.get().strip():
            messagebox.showerror("Erreur", "L'auteur est obligatoire")
            return False
        
        try:
            date = self._obtenir_date_complete()
            datetime.strptime(date, "%d/%m/%Y")
            return True
        except ValueError:
            messagebox.showerror("Erreur", "La date doit être au format JJ/MM/AAAA valide")
            return False
    
    def _ajouter_livre(self):
        """Ajoute un nouveau livre à la bibliothèque."""
        if not self._valider_champs():
            return
        
        livre = Livre(
            titre=self.entry_titre.get().strip(),
            auteur=self.entry_auteur.get().strip(),
            date_publication=self._obtenir_date_complete()
        )
        
        try:
            self.bibliotheque.ajouter_livre(livre)
            messagebox.showinfo("Succès", "Le livre a été ajouté avec succès")
            self._vider_champs()
            self.rafraichir_liste()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
    
    def _recherche_dynamique(self, event):
        """
        Effectue une recherche dynamique lors de la saisie.
        
        Args:
            event: L'événement de saisie
        """
        terme = self.entry_recherche.get().strip()
        if not terme:
            self.rafraichir_liste()
            return
        
        livres = self.bibliotheque.rechercher_livre(terme)
        self._afficher_livres(livres)
    
    def _mettre_a_jour_livre(self):
        """Met à jour le livre sélectionné."""
        if not hasattr(self, 'livre_selectionne'):
            messagebox.showwarning("Attention", "Veuillez sélectionner un livre à mettre à jour")
            return
        
        if not self._valider_champs():
            return
        
        livre = Livre(
            titre=self.entry_titre.get().strip(),
            auteur=self.entry_auteur.get().strip(),
            date_publication=self._obtenir_date_complete(),
            id=self.livre_selectionne.id
        )
        
        try:
            if self.bibliotheque.mettre_a_jour_livre(livre):
                messagebox.showinfo("Succès", "Le livre a été mis à jour avec succès")
                self._vider_champs()
                self.rafraichir_liste()
                self.btn_modifier.configure(state="disabled")
                self.btn_supprimer.configure(state="disabled")
            else:
                messagebox.showerror("Erreur", "Impossible de mettre à jour le livre")
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
    
    def _selection_livre(self, livre: Livre):
        """
        Gère la sélection d'un livre dans le tableau.
        
        Args:
            livre (Livre): Le livre sélectionné
        """
        self.livre_selectionne = livre
        self.entry_titre.delete(0, "end")
        self.entry_titre.insert(0, livre.titre)
        self.entry_auteur.delete(0, "end")
        self.entry_auteur.insert(0, livre.auteur)
        self._decomposer_date(livre.date_publication)
        
        self.btn_modifier.configure(state="normal")
        self.btn_supprimer.configure(state="normal")
    
    def _vider_champs(self):
        """Vide tous les champs de saisie."""
        self.entry_titre.delete(0, "end")
        self.entry_auteur.delete(0, "end")
        self._vider_champs_date()
        if hasattr(self, 'livre_selectionne'):
            delattr(self, 'livre_selectionne')
    
    def _creer_ligne_livre(self, livre: Livre) -> ctk.CTkFrame:
        """
        Crée une ligne dans le tableau pour un livre.
        
        Args:
            livre (Livre): Le livre à afficher
            
        Returns:
            ctk.CTkFrame: La frame contenant la ligne du livre
        """
        frame = ctk.CTkFrame(self.frame_tableau)
        
        ctk.CTkLabel(frame, text=str(livre.id), width=50).pack(side="left", padx=5)
        ctk.CTkLabel(frame, text=livre.titre, width=300).pack(side="left", padx=5)
        ctk.CTkLabel(frame, text=livre.auteur, width=200).pack(side="left", padx=5)
        ctk.CTkLabel(frame, text=livre.date_publication, width=100).pack(side="left", padx=5)
        
        frame.bind("<Button-1>", lambda e, l=livre: self._selection_livre(l))
        return frame
    
    def _afficher_livres(self, livres: List[Livre]):
        """
        Affiche la liste des livres dans le tableau.
        
        Args:
            livres (List[Livre]): La liste des livres à afficher
        """
        # Supprime toutes les lignes existantes sauf les en-têtes
        for widget in self.frame_tableau.winfo_children():
            if widget != self.frame_entetes:
                widget.destroy()
        
        # Ajoute les nouvelles lignes
        for livre in livres:
            ligne = self._creer_ligne_livre(livre)
            ligne.pack(fill="x", padx=5, pady=2)
    
    def rafraichir_liste(self):
        """Rafraîchit la liste des livres."""
        self._afficher_livres(self.bibliotheque.obtenir_tous_les_livres())
    
    def _supprimer_livre(self):
        """Supprime le livre sélectionné."""
        if not hasattr(self, 'livre_selectionne'):
            messagebox.showwarning("Attention", "Veuillez sélectionner un livre à supprimer")
            return
        
        if not messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce livre ?"):
            return
        
        if self.bibliotheque.supprimer_livre(self.livre_selectionne.id):
            messagebox.showinfo("Succès", "Le livre a été supprimé avec succès")
            self._vider_champs()
            self.rafraichir_liste()
            self.btn_modifier.configure(state="disabled")
            self.btn_supprimer.configure(state="disabled")
        else:
            messagebox.showerror("Erreur", "Impossible de supprimer le livre")
    
    def demarrer(self):
        """Démarre l'application."""
        self.fenetre.mainloop() 