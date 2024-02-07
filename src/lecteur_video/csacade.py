import tkinter as tk
import os

def remplir_menu_deroulant_i(Monfichier):
    try:
        lignes = lire_fichier(Monfichier)
       # Création du menu déroulant 
        menu_deroulant = tk.Menu(maFenêtre, tearoff=0)

        if lignes:
            
            # menu_deroulant = tk.Menu(maFenêtre, tearoff=0)
            # Dictionnaires pour stocker les sous-options associées à chaque option
            sous_options = {}
            sous2_options = {}

            # Remplissage du menu déroulant avec les options du fichier
            for option in lignes:
                # Vérifier si l'option a une sous-option (entre parenthèses)
                if '(' in option and ')' in option:
                    nom_option, sous_option_str = option.split('(')
                    sous_option_str = sous_option_str.split(')')[0]
                    sous_options_list = [sous.strip() for sous in sous_option_str.split(';')]
                    sous_options.setdefault(nom_option.strip(), []).extend(sous_options_list)
                else:
                    # Ajouter l'option au menu principal
                    menu_deroulant.add_command(label=option.strip())

            # Créer des sous-menus pour les options avec des sous-options
            for nom_option, sous_options_list in sous_options.items():
                sous_menu = tk.Menu(menu_deroulant, tearoff=0)
                for sous_option in sous_options_list:
                    # Vérifier si l'option a une sous2-option (entre crochets)
                    if '[' in sous_option and ']' in sous_option:
                        nom_sous_option, sous2_option_str = sous_option.split('[')
                        sous2_option_str = sous2_option_str.split(']')[0]
                        sous2_options_list = [sous2.strip() for sous2 in sous2_option_str.split('*')]
                        sous2_options.setdefault(nom_sous_option.strip(), []).extend(sous2_options_list)
                    else:
                        # Ajouter l'option au menu principal
                        #menu_deroulant.add_command(label=sous_option.strip())
                        sous_menu.add_command(label=sous_option.strip())

                menu_deroulant.add_cascade(label=nom_option.strip(), menu=sous_menu)

            # Poste le menu contextuel avec les coordonnées de la fenêtre principale
            menu_deroulant.post(100, 100)

    except FileNotFoundError:
        print(f"Le fichier {Monfichier} n'a pas été trouvé.")

def lire_fichier(nom_fichier):
    """Lecture d'un fichier texte ligne par ligne"""
    try:
        # Ouvre le fichier en mode lecture
        with open(nom_fichier, 'r') as fichier:
            # Lit toutes les lignes du fichier et les stocke dans une liste
            lignes = fichier.read().splitlines()
            return lignes
    except FileNotFoundError:
        print(f"Le fichier {nom_fichier} n'a pas été trouvé.")
        return []

if __name__ == "__main__":
    maFenêtre = tk.Tk()
    maFenêtre.title("Menu Déroulant")
    maFenêtre.geometry('300x200')
    labelChoix = tk.Label(maFenêtre, text="Veuillez faire un choix !")
    labelChoix.grid()

    # 1) Nom du fichier contenant la liste des fruits regroupés par catégorie
    script_directory = os.path.dirname(os.path.abspath(__file__))
    Monfichier = os.path.join(script_directory, "Zeft_symptoms.txt")
    remplir_menu_deroulant_i(Monfichier)

    maFenêtre.mainloop()
