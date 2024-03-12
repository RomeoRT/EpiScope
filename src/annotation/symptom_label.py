###### Brouillon
# pour afficher et gerer les symptomes de la partie droite de l'interface

import customtkinter as CTK
import class_symptome as symptome
import pop_up as popup

class SymptomLabel(label) :
    """classe pour gérer l'affichage et la manipulation d'un unique symptome"""
    def __init__(self, sympt) :
         """constructeur"""
         self.sympt = sympt 



################################################################################################################################
if __name__=="__main__":
    root = CTK.CTk()

    root.mainloop()