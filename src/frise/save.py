"""
Projet Episcope

Auteur : Roméo RAMOS--TANGHE

Ce fichier contient des fonctions pour créer et éditer les fichiers '.txt' de sortie
"""
from tkinter import filedialog

def save(Liste):
    """
    saves the contents of a list in a text file

    :param kind: Optional "kind" of ingredients.
    :type kind: list[str] or None
    :raise lumache.InvalidKindError: If the kind is invalid.
    :return: The ingredients list.
    :rtype: list[str]

    """
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])
    with open(filename, 'w') as file :
        for data in Liste :
            file.write(data)

def edit(Liste):
    """
    Cette fonction permet d'ecrire le contenu d'une liste dans un fichier '.txt'.
    Elle y accède par l'explorateur de fichier. 
    Si le fichier existe déja, on ecrit a la suite, sinon il est créé.
    
    Paramètres :
    - liste : une liste formatée de la forme ["element_x\n"] 
    """
    filename = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])
    with open(filename, 'a') as file :
        file.write("\n")
        for data in Liste :
            file.write(data)


############################################################################################################################################
if __name__=="__main__":
    liste = ["romeo\n", "yosra\n", "annaelle\n", "rachel\n", "chloe\n"]
    save(liste)
    edit(liste)
