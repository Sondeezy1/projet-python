import customtkinter as ctk
from tkinter import messagebox
from typing import Callable, List, Optional, Tuple
from datetime import datetime
from models.livre import Livre
from models.emprunt import Emprunt
from models.bibliotheque import Bibliotheque

class InterfaceEmprunts(ctk.CTkFrame):
    """Interface de gestion des emprunts."""
    
    def __init__(self, parent, bibliotheque: Bibliotheque):
        """
        Initialise l'interface des emprunts.
        
        Args:
            parent: Widget parent
            bibliotheque (Bibliotheque): Instance de la bibliothèque
        """
        super().__init__(parent)
        self.bibliotheque = bibliotheque
        
        self._creer_widgets()
        self._placer_widgets()
        self.rafraichir_liste()
    
    def _creer_widgets(self):
        """Crée les widgets de l'interface des emprunts."""
        # Frame pour l'emprunt
        self.frame_emprunt = ctk.CTkFrame(self)
        self.label_emprunt = ctk.CTkLabel(
            self.frame_emprunt,
            text="Nouvel emprunt",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        
        # Champs de saisie
        self.entry_livre_id = ctk.CTkEntry(
            self.frame_emprunt,
            placeholder_text="ID du livre",
            width=100
        )
        
        self.entry_emprunteur = ctk.CTkEntry(
            self.frame_emprunt,
            placeholder_text="Nom de l'emprunteur",
            width=200
        )
        
        # Boutons d'action
        self.btn_emprunter = ctk.CTkButton(
            self.frame_emprunt,
            text="Emprunter",
            command=self._emprunter_livre,
            width=150
        )
        
        self.btn_retourner = ctk.CTkButton(
            self.frame_emprunt,
            text="Retourner",
            command=self._retourner_livre,
            width=150
        )
        
        # Frame pour la liste des emprunts
        self.frame_liste = ctk.CTkFrame(self)
        self.label_liste = ctk.CTkLabel(
            self.frame_liste,
            text="Emprunts en cours",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        
        # Tableau des emprunts avec scrollbar
        self.frame_tableau = ctk.CTkScrollableFrame(
            self.frame_liste,
            width=800,
            height=400
        )
        
        # En-têtes du tableau
        self.frame_entetes = ctk.CTkFrame(self.frame_tableau)
        self.label_id = ctk.CTkLabel(
            self.frame_entetes,
            text="ID",
            width=50,
            font=ctk.CTkFont(weight="bold")
        )
        self.label_livre = ctk.CTkLabel(
            self.frame_entetes,
            text="Livre",
            width=250,
            font=ctk.CTkFont(weight="bold")
        )
        self.label_emprunteur_col = ctk.CTkLabel(
            self.frame_entetes,
            text="Emprunteur",
            width=150,
            font=ctk.CTkFont(weight="bold")
        )
        self.label_date_emprunt = ctk.CTkLabel(
            self.frame_entetes,
            text="Emprunté le",
            width=100,
            font=ctk.CTkFont(weight="bold")
        )
        self.label_date_retour = ctk.CTkLabel(
            self.frame_entetes,
            text="Retour prévu",
            width=100,
            font=ctk.CTkFont(weight="bold")
        )
        self.label_statut = ctk.CTkLabel(
            self.frame_entetes,
            text="Statut",
            width=100,
            font=ctk.CTkFont(weight="bold")
        )
    
    def _placer_widgets(self):
        """Place les widgets dans l'interface."""
        # Frame d'emprunt
        self.frame_emprunt.pack(pady=10, padx=10, fill="x")
        self.label_emprunt.pack(pady=5)
        
        # Frame pour les champs de saisie
        frame_saisie = ctk.CTkFrame(self.frame_emprunt)
        frame_saisie.pack(pady=5, fill="x", padx=10)
        
        self.entry_livre_id.pack(side="left", padx=5)
        self.entry_emprunteur.pack(side="left", padx=5)
        
        # Frame pour les boutons
        frame_boutons = ctk.CTkFrame(self.frame_emprunt)
        frame_boutons.pack(pady=5, fill="x", padx=10)
        
        self.btn_emprunter.pack(side="left", padx=5)
        self.btn_retourner.pack(side="left", padx=5)
        
        # Frame de la liste
        self.frame_liste.pack(pady=10, padx=10, fill="both", expand=True)
        self.label_liste.pack(pady=5)
        self.frame_tableau.pack(expand=True, fill="both", padx=10, pady=10)
        
        # En-têtes du tableau
        self.frame_entetes.pack(fill="x", padx=5, pady=5)
        self.label_id.pack(side="left", padx=5)
        self.label_livre.pack(side="left", padx=5)
        self.label_emprunteur_col.pack(side="left", padx=5)
        self.label_date_emprunt.pack(side="left", padx=5)
        self.label_date_retour.pack(side="left", padx=5)
        self.label_statut.pack(side="left", padx=5)
    
    def _emprunter_livre(self):
        """Gère l'emprunt d'un livre."""
        try:
            livre_id = int(self.entry_livre_id.get().strip())
            emprunteur = self.entry_emprunteur.get().strip()
            
            if not emprunteur:
                messagebox.showerror("Erreur", "Veuillez saisir le nom de l'emprunteur")
                return
            
            emprunt = self.bibliotheque.emprunter_livre(livre_id, emprunteur)
            messagebox.showinfo("Succès", "Livre emprunté avec succès")
            self._vider_champs()
            self.rafraichir_liste()
            
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")
    
    def _retourner_livre(self):
        """Gère le retour d'un livre."""
        try:
            livre_id_str = self.entry_livre_id.get().strip()
            
            if not livre_id_str:
                messagebox.showerror("Erreur", "Veuillez saisir l'ID du livre")
                return
                
            try:
                livre_id = int(livre_id_str)
            except ValueError:
                messagebox.showerror("Erreur", "L'ID du livre doit être un nombre")
                return
            
            if self.bibliotheque.retourner_livre(livre_id):
                messagebox.showinfo("Succès", "Livre retourné avec succès")
                self._vider_champs()
                self.rafraichir_liste()
            
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")
    
    def _vider_champs(self):
        """Vide les champs de saisie."""
        self.entry_livre_id.delete(0, "end")
        self.entry_emprunteur.delete(0, "end")
    
    def _creer_ligne_emprunt(self, emprunt: Emprunt, livre: Livre) -> ctk.CTkFrame:
        """
        Crée une ligne dans le tableau pour un emprunt.
        
        Args:
            emprunt (Emprunt): L'emprunt à afficher
            livre (Livre): Le livre emprunté
            
        Returns:
            ctk.CTkFrame: La frame contenant la ligne
        """
        frame = ctk.CTkFrame(self.frame_tableau)
        
        # Déterminer le statut et la couleur
        if emprunt.est_en_retard:
            status = "En retard"
            color = "red"
        elif emprunt.est_en_cours:
            status = "En cours"
            color = "green"
        else:
            status = "Retourné"
            color = "gray"
        
        ctk.CTkLabel(frame, text=str(emprunt.id), width=50).pack(side="left", padx=5)
        ctk.CTkLabel(frame, text=f"{livre.titre} ({livre.auteur})", width=250).pack(side="left", padx=5)
        ctk.CTkLabel(frame, text=emprunt.emprunteur, width=150).pack(side="left", padx=5)
        ctk.CTkLabel(frame, text=emprunt.date_emprunt, width=100).pack(side="left", padx=5)
        ctk.CTkLabel(frame, text=emprunt.date_retour_prevue, width=100).pack(side="left", padx=5)
        ctk.CTkLabel(frame, text=status, width=100, text_color=color).pack(side="left", padx=5)
        
        return frame
    
    def rafraichir_liste(self):
        """Rafraîchit la liste des emprunts."""
        # Supprimer toutes les lignes existantes sauf les en-têtes
        for widget in self.frame_tableau.winfo_children():
            if widget != self.frame_entetes:
                widget.destroy()
        
        # Récupérer et afficher les emprunts en cours
        emprunts = self.bibliotheque.obtenir_emprunts_en_cours()
        for emprunt, livre in emprunts:
            ligne = self._creer_ligne_emprunt(emprunt, livre)
            ligne.pack(fill="x", padx=5, pady=2) 