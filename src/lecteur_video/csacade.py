import tkinter as tk

def create_submenu(parent_menu, symptom, sub_symptoms):
    symptom_menu = tk.Menu(parent_menu, tearoff=0)
    if sub_symptoms:  # Vérifier si des sous-symptômes existent
        parent_menu.add_cascade(label=symptom, menu=symptom_menu)
        for sub_symptom in sub_symptoms:
            # Vérifier si le sous-symptôme a des sous-sous-symptômes
            if '[' in sub_symptom:
                sub_symptom_name, sub_sub_symptoms_str = sub_symptom.split('[')
                sub_symptom_name = sub_symptom_name.strip()
                sub_sub_symptoms_str = sub_sub_symptoms_str.replace(']', '')
                sub_sub_symptoms = sub_sub_symptoms_str.split(',')
                sub_sub_menu = tk.Menu(symptom_menu, tearoff=0)
                symptom_menu.add_cascade(label=sub_symptom_name, menu=sub_sub_menu)
                for sub_sub_symptom in sub_sub_symptoms:
                    sub_sub_menu.add_command(label=sub_sub_symptom.strip())
            else:
                symptom_menu.add_command(label=sub_symptom)
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
                if sub_symptoms:
                    sub_symptoms = sub_symptoms[0].replace(')', '').split(';')
                    sub_symptoms = [sub_symptom.strip() for sub_symptom in sub_symptoms]
                else:
                    sub_symptoms = []
                symptoms.append((symptom, sub_symptoms))
    return title, symptoms

def display_symptoms(title, symptoms):
    root = tk.Tk()
    root.title("Symptoms Menu")

    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    main_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label=title, menu=main_menu)

    for symptom, sub_symptoms in symptoms:
        create_submenu(main_menu, symptom, sub_symptoms)

    root.mainloop()

file_name = "Objective_Symptomes.txt"
title, symptoms = read_symptoms_from_file(file_name)
display_symptoms(title, symptoms)
