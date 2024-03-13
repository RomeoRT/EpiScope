"""
Projet Episcope

Auteur : Roméo RAMOS--TANGHE

Ce fichier contient des fonctions de base pour sauvegarder les fichiers '.txt' et frise de sortie
"""
from tkinter import filedialog
from tkinter import messagebox
import customtkinter as CTK
import frise.ecriture_fichier as EF

class save :
    """
    classe dédiée à la sauvegarde des fichiers 
    """
    def __init__(self, Liste_symptomes = []):
        self.symptomes = Liste_symptomes
        

    def save(self):
        """
        Enregistre les symptomes dans un fichier et produit la frise chronologique
        """
        # récuperer le nom et emplacement des fichiers
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])
        try :
            if self.symptomes == [] :
                messagebox.showinfo('Episcope Error', 'Empty symptom list\nCannot save properly')
            else :
                # ecrire les métadatas
                Meta_wd = metadata(filename)
                Meta_wd.after(100, Meta_wd.lift)

                EF.EcrireListeSymptome(self.symptomes, filename)
                #print("ecriture")

        except FileNotFoundError:
            Meta_wd.destroy()
            Meta_wd.update()
            messagebox.showinfo('Episcope Error', 'No file selected\nCannot save properly')
    
    def set_symptomes(self, Liste_symptomes):
        """Actualise les symptomes"""
        self.symptomes = Liste_symptomes



        
        
class metadata(CTK.CTkToplevel) :
    """
    fenetre toplevel pour saisir les metadonnées
    """
    def __init__(self,filename) :
        super().__init__()

        self.liste = []
        self.filename = filename


        self.title("Metadata")
        self.geometry("400x200")
        self.grid_columnconfigure(3, weight=1)

        self.meta_label = CTK.CTkLabel(self, text="enter MetaData")
        self.meta_label.grid(row=0, column=1, padx=5, pady=5)

        # metadatas
        self.patient_entry = CTK.CTkEntry(self, placeholder_text="Patient name")
        self.patient_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.patient_label = CTK.CTkLabel(self, text="Patient's name : ")
        self.patient_label.grid(row=1, column=0, padx=5, pady=5)

        self.doctor_entry = CTK.CTkEntry(self, placeholder_text="Doctor name")
        self.doctor_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.doctor_label = CTK.CTkLabel(self, text="Doctor's name : ")
        self.doctor_label.grid(row=2, column=0, padx=5, pady=5)

        self.hour_entry = CTK.CTkEntry(self, placeholder_text="Time of seizure")
        self.hour_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.hour_label = CTK.CTkLabel(self, text="Time of seizure : ")
        self.hour_label.grid(row=3, column=0, padx=5, pady=5)

        # Bouton
        self.boutonOK = CTK.CTkButton(self, text="OK",fg_color='green', hover_color= ('darkgreen'))
        self.boutonOK.bind("<Button-1>", self.get_metadata)
        self.boutonOK.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
    

    def get_metadata(self, event):
        """
        ecrire une liste des metadonnées sous la forme [heure réelle, patient, praticien]
        """
        
        self.liste.append(self.hour_entry.get())
        self.liste.append(self.doctor_entry.get())
        self.liste.append(self.patient_entry.get())
        
        EF.EcrireMetaData(self.liste, self.filename)

        self.destroy()
        self.update()
        


############################################################################################################################################
if __name__=="__main__":
# test des fonctions
    
    root = CTK.CTk()

    L = []
    for i in range(20) :
        S = EF.Symptome(f"ID{i}", f"Nom{i}", f"Lateralisation{i}", f"SegCorporel{i}", f"Orientation{i}", f"AttributSuppl{i}", f"Tdeb{i}", f"Tfin{i}", f"Commentaire{i}")
        L.append(S)   

    sauvegarde = save(L)
    Bouton_save = CTK.CTkButton(root, text = "save", command = sauvegarde.save)
    Bouton_save.grid(row=0, column=0, padx=20, pady=20)

    root.mainloop()