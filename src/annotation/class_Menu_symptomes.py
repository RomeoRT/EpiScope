# -*- coding: utf-8 -*-
import tkinter as tk
import customtkinter as CTk
import os

# - - - - - - - - - - - -
# DECLARATION DES CLASSES
# - - - - - - - - - - - -


class MenuSymptomes(CTk.CTkFrame):
    """
    Classe pour avoir les menus déroulants et la recherche textuelle
    Les fichiers de symptomes doivent etre de la forme : Categorie; Symptome1; Symptome2; Symptome3 \n 
    """

    # Methode constructeur
    def __init__(self, master):
        super().__init__(master)
        Liste_cat = []
        # création des menus déroulants 
        self.options_symptomes = []
        self.liste_MenuDeroulant = []  # une liste de boutons
        self.nb_menus = 0  # pour un affichage jolibeau

        # 1) Nom du fichier contenant la liste des fruits regroupés par catégorie
        script_directory = os.path.dirname(os.path.abspath(__file__))
        Monfichier = os.path.join(script_directory,"Liste_Fruits.txt")


        # 2) Création des differents menus déroualant

        with open(Monfichier, 'r') as file :    # Ouverture du fichier en lecture seule
            for line in file :
                line = line.strip()             # Supprime les espaces inutiles
                Liste = line.split(';')         # Indique que le point-virgule est l'outil de séparation des éléments dans chaque ligne du fichier
                
                Liste_cat.append(Liste[0])

                Liste = Liste[1:]
                self.options_symptomes.append(Liste)
                self.nb_menus += 1

                MenuDeroulant = CTk.CTkOptionMenu(self, values=Liste )   # Création du menu déroulant
                self.liste_MenuDeroulant.append(MenuDeroulant)
                self.liste_MenuDeroulant[-1].grid(row = self.nb_menus, sticky="nsew", padx=5, pady=5)   
                self.liste_MenuDeroulant[-1].set(Liste_cat[-1])
        # création de la barre de recherche 

        self.entry = CTk.CTkEntry(self, placeholder_text="Symptomes") 
        self.entry.grid(row = 0)
        self.entry.bind("<KeyRelease>", self.filtrer_options)

    # definition des méthodes
    def filtrer_options(self, event): 
        """
        filtre les options d'un menu déroulant en fonction d'une recherche textuelle
        affiche dans le menu déroulant la premiere option correspondante
        """
        recherche = self.entry.get().lower()
        for i in range(self.nb_menus) :
            options_filtrees = [option for option in self.options_symptomes[i] if recherche in option.lower()]
            self.liste_MenuDeroulant[i].configure(values=options_filtrees)  
            if len(options_filtrees)> 0 : 
                self.liste_MenuDeroulant[i].set(options_filtrees[0])
            else :
                self.liste_MenuDeroulant[i].set("") 
        
            

if __name__=='__main__':
    maFenetre = tk.Tk() 
    maFenetre.title("Classe Menu Déroulant")
    maFenetre.geometry('300x200')

    Menu = MenuSymptomes(maFenetre)
    Menu.grid()

    maFenetre.mainloop()
