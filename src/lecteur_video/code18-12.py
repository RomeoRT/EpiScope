# -*- coding: utf-8 -*-
import tkinter as tk
import customtkinter as CTk
import os

class MenuSymptomesPrincipal(CTk.CTkFrame):
    """Classe pour avoir les menus déroulants et la recherche textuelle
       Les fichiers de symptômes doivent être de la forme : Categorie; Symptome1; Symptome2; Symptome3 \n 
    """

    def __init__(self, master):
        super().__init__(master)

        # Création des widgets
        self.options_symptomes = []  # Liste des options initiales
        self.sous_options_menus = {}  # Dictionnaire pour stocker les sous-options associées à chaque option
        self.menu_principal = None  # Menu principal
        self.sous_menus = {}  # Dictionnaire pour stocker les sous-menus des options
        self.nb_menus = 0  # Compteur de menus déroulants

        # Chargement des options initiales depuis le fichier
        script_directory = os.path.dirname(os.path.abspath(__file__))
        Monfichier = os.path.join(script_directory, "case1.txt")

        with open(Monfichier, 'r') as file:
            for line in file:
                line = line.strip()
                categorie, *sous_options = self.parse_line(line)
                self.options_symptomes.append(categorie)
                self.sous_options_menus[categorie] = sous_options

        # Création du menu principal (première ligne du fichier)
        self.menu_principal = CTk.CTkOptionMenu(self, values=self.options_symptomes, command=self.afficher_sous_options)
        self.menu_principal.grid(row=0, sticky="nsew", padx=5, pady=5)

        # Création de la barre de recherche
        self.entry = CTk.CTkEntry(self, placeholder_text="Symptomes")
        self.entry.grid(row=1)
        self.entry.bind("<KeyRelease>", self.filtrer_options)

        # Associer l'événement <Enter> pour afficher les sous-options lorsque le curseur est sur une option
        for value in self.options_symptomes:
            self.menu_principal.bind("<Enter>", lambda event, value=value: self.afficher_sous_options_enter(value))

    def parse_line(self, line):
        """Parse une ligne du fichier texte pour extraire la catégorie et les sous-options."""
        parts = line.split('"')
        categorie = parts[0].strip()
        sous_options = [opt.strip() for opt in parts[1].strip('()').split(';')] if len(parts) > 1 else []
        return categorie, sous_options

    def afficher_sous_options(self, selected_categorie):
        """
        Affiche les sous-options en fonction de la catégorie sélectionnée
        """
        if selected_categorie in self.sous_options_menus:
            # Afficher les sous-options si elles existent
            options = self.sous_options_menus[selected_categorie]

            # Détruire les sous-menus précédents
            for menu in self.sous_menus.values():
                menu.destroy()

            self.sous_menus = {}  # Réinitialiser le dictionnaire des sous-menus
            self.nb_menus = 0  # Réinitialiser le compteur de menus déroulants

            # Créer les sous-menus pour les sous-options
            for sous_option in options:
                sous_menu = tk.Menu(self.menu_principal, tearoff=0)
                for item in sous_option:
                    sous_menu.add_command(label=item, command=lambda i=item: self.on_sous_option_selected(i))
                self.sous_menus[sous_option[0]] = sous_menu  # Utiliser le premier élément comme identifiant
                self.menu_principal.entryconfigure(selected_categorie, menu=sous_menu)

    def afficher_sous_options_enter(self, event, selected_categorie):
        """
        Affiche les sous-options lorsque le curseur est placé sur une option
        """
        self.afficher_sous_options(selected_categorie)

    def on_sous_option_selected(self, selected_option):
        """Fonction appelée lorsque l'utilisateur sélectionne une sous-option."""
        print(f"Sous-option sélectionnée : {selected_option}")

    def filtrer_options(self, event):
        """
        Filtrer les options en fonction de la recherche textuelle
        """
        recherche = self.entry.get().lower()
        options_filtrees = [categorie for categorie in self.options_symptomes if recherche in categorie.lower()]
        self.menu_principal.configure(values=options_filtrees)

if __name__ == '__main__':
    maFenetre = tk.Tk()
    maFenetre.title("Classe Menu Déroulant")
    maFenetre.geometry('400x300')

    Menu = MenuSymptomesPrincipal(maFenetre)
    Menu.grid(row=0, column=0, sticky="nsew")

    maFenetre.mainloop()
