"""
menus and submenus based on exel file
"""

import tkinter as tk
import tkinter.font as tkFont
from tkinter import Menu
import pandas as pd
from collections import defaultdict

def Read_excel(file_path):
    """
    Reads an Excel file and organizes the data into a hierarchical structure for a graphical interface.
    
    Args:
    - file_path (str): Path to the Excel file containing the data.
    
    Returns:
    - dict: A hierarchical dictionary containing organized symptom data.
    
    The function reads an Excel file specified by 'file_path', 
    processes the data, and organizes it into a hierarchical structure. 
    This structure is designed to facilitate the creation of a graphical 
    interface for displaying and interacting with the symptom data.
    
    The Excel file is expected to have columns named 'Typologie', 'Designation', 
    'Description', 'Sub_description','Topography', and 'Lateralized'.
    
    The data is organized based on the following criteria:
    - There can not be sub sescription without description.
    - If there is no description, no sub_description no topography, but there are lateralizations, 
      they are stored under an empty string.
    - If there is no additional information, a 'None' flag is stored.
    - If there is topography and lateralizations but no description, 
      the data is stored based on topography.
    - Otherwise, the detailed information is stored including description, 
      topography, and lateralizations.
    
    Example:
    >>> Read_excel('ictal_symptoms.xlsx')
    
    Note:
    - The function uses Pandas to read the Excel file and defaultdict 
      to create the hierarchical structure.
    """
    
    # Load data from the Excel file
    data = pd.read_excel(file_path)
    
    # Initialize a hierarchical structure to organize the data
    symptoms_structure = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    
    # Process the data read from Excel
    for _, row in data.iterrows():
        typology = row['Typologie'] if pd.notnull(row['Typologie']) else ''
        designation = row['Designation'] if pd.notnull(row['Designation']) else ''
        description = row['Description'] if pd.notnull(row['Description']) else ''
        sub_descriptions = str(row['Sub_description']).split(',') if pd.notnull(row['Sub_description']) else []
        topographies = str(row['Topography']).split(';') if pd.notnull(row['Topography']) else []
        lateralizations = str(row['Lateralized']).split(',') if pd.notnull(row['Lateralized']) else []

        if not description and not topographies and lateralizations:
            # If there's no description, no topographies, but there are lateralizations
            symptoms_structure[typology][designation][''] = [('','', lateralizations)]
        elif not description and not topographies and not lateralizations:
            # If there's no additional information, store a flag to indicate this
            symptoms_structure[typology][designation] = None
        elif not description and topographies and lateralizations:
            # Handle the case where there is topography and lateralization but no description
            for topo in topographies:
                symptoms_structure[typology][designation][topo].append(('','',lateralizations))
        elif sub_descriptions:
        #Handle the case where there are sub_descriptions
            symptoms_structure[typology][designation][description].append((sub_descriptions,'', ''))
        else:
            # Otherwise, store the detailed information
            for topo in topographies or ['']:  # Ensure at least an empty string if no topology
                symptoms_structure[typology][designation][description].append(('', topo, lateralizations))

    return symptoms_structure

def add_submenus(menu, data, full_path, on_select):
    """
    Add submenus to the main menu based on the provided data.
    
    This function iterates through the data dictionary to add submenus 
    and menu items to the provided Tkinter menu. It checks for different 
    scenarios in the data structure to determine the appropriate way to 
    add submenus and menu items.
    
    Args:
        menu (tk.Menu): The menu to which the submenus will be added.
        data (dict): The hierarchical data containing submenu information.
        full_path (str): The full path to the current menu item.
        on_select (function) : The function to select the symptom
    """

    for desc, topo_lats in data.items():
        if topo_lats is not None:  # Check if there is additional information
            if desc == '':  # Si la description est vide, attacher directement les sous-éléments
                for ss_desc, topo, lats in topo_lats:
                    if topo:  # S'il y a une topographie, l'ajouter comme un menu en cascade
                        topo_menu = Menu(menu, tearoff=0)
                        for lat in lats:
                            new_path = full_path + f"{desc} > {topo} > {lat} >"
                            topo_menu.add_command(label=lat, command=lambda path=new_path: on_select(path))
                        menu.add_cascade(label=topo, menu=topo_menu)
                    
                    else:  # S'il n'y a pas de topo, attacher directement les latéralisations
                        for lat in lats:
                            new_path = full_path + f"{desc} > > {lat} >"
                            menu.add_command(label=lat, command=lambda path=new_path: on_select(path))
        
            
            else:  # Si la description n'est pas vide, suivre la procédure normale
                desc_menu = Menu(menu, tearoff=0)
                for ss_desc, topo, lats in topo_lats:
                    if ss_desc =='':
                        topo_menu = Menu(desc_menu, tearoff=0)
                        for lat in lats:
                            new_path = full_path + f"{desc} > > {topo} > {lat} >"
                            topo_menu.add_command(label=lat, command=lambda path=new_path: on_select(path))
                        if topo:
                            desc_menu.add_cascade(label=topo, menu=topo_menu)
                        else:
                            for lat in lats:
                                new_path = full_path + f"{desc} >  >  > {lat} >"
                                desc_menu.add_command(label=lat, command=lambda path=new_path: on_select(path))
                    else :
                        ss_desc_menu = Menu(desc_menu, tearoff=0)
                        new_path = full_path + f"{desc} > {ss_desc[0]} >  >"
                        desc_menu.add_command(label=ss_desc, command=lambda path=new_path: on_select(path))

                if desc_menu.index('end') is not None:
                    menu.add_cascade(label=desc if desc else 'General', menu=desc_menu)
                elif desc:
                    new_path = full_path + f"{desc} > {topo} >  >"
                    menu.add_command(label=desc, command=lambda path=new_path: on_select(path))
        else:
            # Add the designation as a command if there are no additional details
            new_path = full_path + f"{desc} >  >  >"
            menu.add_command(label=desc, command=lambda path=new_path: on_select(path))

def build_menu(structure, main_menu, on_select):
    """
    Build a cascading menu based on the provided structure.
    
    This function builds a cascading menu using Tkinter based on the 
    hierarchical structure provided. It iterates through the structure 
    to add main menu items, submenus, and menu items. Depending on the 
    data in the structure, it calls the add_submenus function to add 
    appropriate submenus and menu items to the main menu.
    
    Args:
        structure (dict): The hierarchical structure of the menu.
        main_menu (tk.Menu): The main menu to which the cascading menu will be added.
        on_select (function) : The function to select the symptom
    """

    full_path = f""
    for designation, descriptions in structure.items():
        full_path = f"{designation} > "
        if descriptions is not None:  # Check if there are descriptions or it's a flag indicating no additional info
            designation_menu = Menu(main_menu, tearoff=0)
            add_submenus(designation_menu, descriptions, full_path, on_select)
            if designation_menu.index('end') is not None:
                main_menu.add_cascade(label=designation, menu=designation_menu)
            else:
                main_menu.add_command(label=designation)
        else:
            full_path = f"{designation} > > > > "
            # Directly add the designation as a command if no additional info
            main_menu.add_command(label=designation, command=lambda path=full_path: on_select(path))

if __name__ == "__main__":
    # -----------------------------------------
    #            Initialize the GUI
    # -----------------------------------------
    root = tk.Tk()
    root.title('Symptom Selection')
    
    def on_select(path):
            print(f"Selected Path: {path}")
    
    # Chemin vers le nouveau fichier Excel
    file_path = 'ictal_symptoms_zeft_copie.xlsx'  # Assurez-vous que ce chemin est correct
    symptoms_structure = Read_excel(file_path)

    # _________________________________________
    #       initialize the buttons
    largeur = 900

    my_font = tkFont.Font(size=12)    
    # Création du Menubutton
    menubutton_objective = tk.Menubutton(text="Objective/Motor Symptoms", width=largeur//9, direction='flush', relief="flat", font=my_font)
    menubutton_objective.pack(side='top', padx=5, pady=20, expand=False)
    # Création du Menubutton
    menubutton_subjective = tk.Menubutton(text="Subjective Symptoms", width=largeur//9, relief="flat", font=my_font)
    menubutton_subjective.pack(side='top', padx=5, pady=10, expand=False)


    # Création du menu principal
    menu_objective = tk.Menu(menubutton_objective, tearoff=0, font=my_font)
    menubutton_objective.config(menu=menu_objective)

    menu_subjective = tk.Menu(menubutton_subjective, tearoff=0, font=my_font)
    menubutton_subjective.config(menu=menu_subjective)

    #____________________________________________________________________________
    # Build the cascading menu

    # build sub-structures for objective and subjectives symptoms
    symptoms_objective = symptoms_structure['Objective']
    symptoms_subjective = symptoms_structure['Subjective']

    build_menu(symptoms_objective, menu_objective, on_select)
    build_menu(symptoms_subjective, menu_subjective, on_select)

    root.mainloop()
