import tkinter as tk
import customtkinter as ctk

def create_submenu(parent_menu, symptom, sub_symptoms):
    # Initialisation du menu pour ce symptôme
    symptom_menu = tk.Menu(parent_menu, tearoff=0)
    has_sub_items = False  # Indicateur pour vérifier si le symptôme a des sous-éléments

    for item in sub_symptoms:
        # Séparation des sous-symptômes et des sous-sous-symptômes
        parts = item.split('[')
        main_part = parts[0].strip()
        sub_sub_symptoms = parts[1].strip(']').split(',') if len(parts) > 1 else []

        if sub_sub_symptoms:  # Vérifie s'il y a des sous-sous-symptômes
            has_sub_items = True  # Il y a des sous-éléments
            sub_menu = tk.Menu(symptom_menu, tearoff=0)  # Création d'un sous-menu
            for sub_sub_symptom in sub_sub_symptoms:
                sub_menu.add_command(label=sub_sub_symptom.strip())  # Ajout des sous-sous-symptômes
            symptom_menu.add_cascade(label=main_part, menu=sub_menu)
        else:
            symptom_menu.add_command(label=main_part)  # Ajout des sous-symptômes comme commandes simples

    # Ajout du menu en cascade seulement s'il y a des sous-éléments
    if has_sub_items:
        parent_menu.add_cascade(label=symptom, menu=symptom_menu)
    else:
        parent_menu.add_command(label=symptom)


def read_symptoms_from_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        title = file.readline().strip()
        symptoms = []
        for line in file:
            line = line.strip()
            if line:
                symptom, *sub_symptoms = line.split('(')
                symptom = symptom.strip()
                sub_symptoms = sub_symptoms[0].replace(')', '').split(';') if sub_symptoms else []
                symptoms.append((symptom, [sub.strip() for sub in sub_symptoms]))
    return title, symptoms

def display_symptoms(title, symptoms):
    root = ctk.CTk()  # Changed to CustomTkinter window
    root.title("Symptoms Menu")

    # Tkinter Menu for compatibility
    menu_bar = tk.Menu(root, bg="#333333", fg="white")  # Added bg and fg for styling
    root.config(menu=menu_bar)
    main_menu = tk.Menu(menu_bar, tearoff=0, bg="#444444", fg="white")  # Styled Menu
    menu_bar.add_cascade(label=title, menu=main_menu)

    for symptom, sub_symptoms in symptoms:
        create_submenu(main_menu, symptom, sub_symptoms)
    
    # Here you can add more CustomTkinter widgets as needed
    # e.g., ctk.CTkButton(root, text="Check Symptoms").pack()

    root.mainloop()

file_name = "Objective_Symptomes.txt"
title, symptoms = read_symptoms_from_file(file_name)
display_symptoms(title, symptoms)

