import tkinter as tk
from tkinter import Menu
import pandas as pd
from collections import defaultdict

# Chemin vers le nouveau fichier Excel
file_path = 'ictal_symptoms_zeft.xlsx'  # Assurez-vous que ce chemin est correct
# Charger les données depuis le fichier Excel
data = pd.read_excel(file_path)

# Structure pour organiser les données pour l'interface graphique
symptoms_structure = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

# Organiser les données
for _, row in data.iterrows():
    typology = row['Typologie'] if pd.notnull(row['Typologie']) else ''
    designation = row['Designation'] if pd.notnull(row['Designation']) else ''
    description = row['Description'] if pd.notnull(row['Description']) else ''
    topographies = str(row['Topography']).split(';') if pd.notnull(row['Topography']) else []
    lateralizations = str(row['Lateralized']).split(',') if pd.notnull(row['Lateralized']) else []

    if not description and not topographies and lateralizations:
        # If there's no description and no topographies, but there are lateralizations
        symptoms_structure[typology][designation][''] = [('', lateralizations)]
    elif not description and not topographies and not lateralizations:
        # If there's no additional information, store a flag to indicate this
        symptoms_structure[typology][designation] = None
    elif not description and topographies and lateralizations:
        # Handle the case where there is topography and lateralization but no description
        for topo in topographies:
            symptoms_structure[typology][designation][topo].append(('', lateralizations))

    else:
        # Otherwise, store the detailed information
        for topo in topographies or ['']:  # Ensure at least an empty string if no topology
            symptoms_structure[typology][designation][description].append((topo, lateralizations))

# Initialize the GUI
root = tk.Tk()
root.title('Symptom Selection')

main_menu = Menu(root)
root.config(menu=main_menu)

# Function to add elements to the menu
def add_submenus(menu, data):
    for desc, topo_lats in data.items():
        if topo_lats is not None:  # Check if there is additional information
            if desc == '':  # Si la description est vide, attacher directement les sous-éléments
                for topo, lats in topo_lats:
                    if topo:  # S'il y a une topographie, l'ajouter comme un menu en cascade
                        topo_menu = Menu(menu, tearoff=0)
                        for lat in lats:
                            topo_menu.add_command(label=lat)
                        menu.add_cascade(label=topo, menu=topo_menu)
                    else:  # S'il n'y a pas de topographie, attacher directement les latéralisations
                        for lat in lats:
                            menu.add_command(label=lat)
            else:  # Si la description n'est pas vide, suivre la procédure normale
                desc_menu = Menu(menu, tearoff=0)
                for topo, lats in topo_lats:
                    topo_menu = Menu(desc_menu, tearoff=0)
                    for lat in lats:
                        topo_menu.add_command(label=lat)
                    if topo:
                        desc_menu.add_cascade(label=topo, menu=topo_menu)
                    else:
                        for lat in lats:
                            desc_menu.add_command(label=lat)
                if desc_menu.index('end') is not None:
                    menu.add_cascade(label=desc if desc else 'General', menu=desc_menu)
                elif desc:
                    menu.add_command(label=desc)
        else:
            # Add the designation as a command if there are no additional details
            menu.add_command(label=desc)

# Build the cascading menu
for typology, designations in symptoms_structure.items():
    typology_menu = Menu(main_menu, tearoff=0)
    for designation, descriptions in designations.items():
        if descriptions is not None:  # Check if there are descriptions or it's a flag indicating no additional info
            designation_menu = Menu(typology_menu, tearoff=0)
            add_submenus(designation_menu, descriptions)
            if designation_menu.index('end') is not None:
                typology_menu.add_cascade(label=designation, menu=designation_menu)
            else:
                typology_menu.add_command(label=designation)
        else:
            # Directly add the designation as a command if no additional info
            typology_menu.add_command(label=designation)
    if typology_menu.index('end') is not None:
        main_menu.add_cascade(label=typology, menu=typology_menu)

root.mainloop()
