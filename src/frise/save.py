"""
Projet Episcope

Auteur : Roméo RAMOS--TANGHE

Ce fichier contient des fonctions de base pour sauvegarder les fichiers '.txt' et frise de sortie
"""
from tkinter import filedialog
import customtkinter as CTK
import ecriture_fichier as EF
import annotation.class_symptome as CS

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
        
        # recuperer les métadatas
        Meta_wd = metadata()
        ListeMeta = Meta_wd.get_metadata()
        EF.EcrireMetaData(ListeMeta, filename)
        EF.EcrireListeSymptome(self.symptomes, filename)




class metadata(CTK.CTkToplevel) :
    """
    fenetre toplevel pour saisir les metadonnées
    """
    def __init__(self) :
        super().__init__()

        self.title("Metadata")
        self.geometry("400x150")
        self.grid_columnconfigure(0, weight=1)

        self.meta_label = CTK.CTkLabel(self, text="enter MetaData")
        self.meta_label.grid(row=0, column=0, padx=5, pady=5)

        # metadatas
        self.patient_entry = CTK.CTkEntry(self, placeholder_text="Patient name")
        self.patient_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.doctor_entry = CTK.CTkEntry(self, placeholder_text="Doctor name")
        self.doctor_entry.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        self.hour_entry = CTK.CTkEntry(self, placeholder_text="Time of seizure")
        self.hour_entry.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        # Bouton
        self.boutonOK = CTK.CTkButton(self, text="OK", command=self.okidoki)
    
    def get_metadata(self):
        """
        recuperer une liste des metadonnées sous la forme [heure réelle, patient, praticien]
        """
        liste =[]

        liste.append(self.hour_entry.get())
        liste.append(self.doctor_entry.get())
        liste.append(self.patient_entry.get())

        return(liste)
    
    def okidoki(self):
        """Ferme la fenetre et recupere les données"""
        self.destroy
        return self.get_metadata()




############################################################################################################################################
if __name__=="__main__":
    root = CTK.CTk()

    L = []
    for i in range(20) :
        S = CS.Symptome(f"ID{i}", f"Nom{i}", f"Lateralisation{i}", f"SegCorporel{i}", f"Orientation{i}", f"AttributSuppl{i}", f"Tdeb{i}", f"Tfin{i}", f"Commentaire{i}")
        L.append(S)   

    sauvegarde = save(L)
    Bouton_save = CTK.CTkButton(root, text = "save", command = sauvegarde.save)
    Bouton_save.grid(row=0, column=0, padx=20, pady=20)
    root.mainloop()