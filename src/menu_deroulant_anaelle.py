import tkinter as tk
import os


maFenêtre = tk.Tk() 
maFenêtre.title("Menu Déroulant annaelle")
maFenêtre.geometry('300x200')

labelChoix = tk.Label(maFenêtre, text = "Veuillez faire un choix !")
labelChoix.grid()

Liste = []
i=15  # pour un affichage jolibeau

# 1) Nom du fichier contenant la liste des fruits regroupés par catégorie
script_directory = os.path.dirname(os.path.abspath(__file__))
Monfichier = os.path.join(script_directory,"Liste_Fruits.txt")


# 2) Création des differents menus déroualant

with open(Monfichier, 'r') as file :       # Ouverture du fichier en lecture seule
    for line in file :
        line = line.strip()             # Supprime les espaces inutiles
        Liste = line.split(';')         # Indique que le point-virgule est l'outil de séparation des éléments dans chaque ligne du fichier

        var_selected = tk.StringVar()
        var_selected.set(Liste[0])      # Place le premier élément de la liste en option par défaut du menu (titre)

        Liste = Liste[1:]
        MenuDeroulant = tk.OptionMenu(maFenêtre, var_selected, *Liste)      # Création du menu déroulant
        MenuDeroulant.grid(row=i, sticky="nsew", padx=5, pady=5)        # Positionnement du menu déroulant dans la fénêtre
        i+=10


maFenêtre.mainloop()