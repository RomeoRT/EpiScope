"""
Ce fichier contient des classes et fonctions de base pour sauvegarder les fichiers '.txt' et frise de sortie
"""
from tkinter import filedialog
from tkinter import messagebox
from typing import Any
import customtkinter as CTK
import datetime

import frise.ecriture_fichier as EF

class save :
    """
    classe dédiée à la sauvegarde des fichiers 

    Attributes:
       symptomes (Liste): liste des symptomes a sauvegarder 
    """
    def __init__(self, Liste_symptomes = []):
        self.symptomes = Liste_symptomes
        

    def save(self):
        """
        Enregistre les symptomes dans un fichier et produit la frise chronologique

        Raises:
            FileNotFoundError: message d'erreur si echec de recuperation du chemin du fichier.
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
        """
        Actualise les symptomes

        Args:
            Liste_symptomes (list): Liste de symptomes
        """
        self.symptomes = Liste_symptomes



        
        
class metadata_WD(CTK.CTkToplevel) :
    """
    fenetre toplevel pour saisir les metadonnées

    Attributes:
        liste (list): liste de symptomes a sauvegarder
        filename (string): chemin du fichier dans lequel ecrire
    """
    def __init__(self,filename) :
        """
        constructeur de metadata

        Args:
            filename (string) : chemin du ficher dans lequel ecrire
        """
        super().__init__()

        self.data = MetaData()
        self.filename = filename


        self.title("Metadata")
        self.geometry("400x200")
        self.grid_columnconfigure(3, weight=1)

        self.meta_label = CTK.CTkLabel(self, text="enter MetaData")
        self.meta_label.grid(row=0, column=1, padx=5, pady=5)

        # metadata_entries 
        #patient
        self.patientName_entry = CTK.CTkEntry(self, placeholder_text="Patient Name")
        self.patientName_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.patientName_label = CTK.CTkLabel(self, text="Patient's Name : ")
        self.patientName_label.grid(row=1, column=0, padx=5, pady=5)

        self.patientSurname_entry = CTK.CTkEntry(self, placeholder_text="Patient surname")
        self.patientSurname_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.patient_label = CTK.CTkLabel(self, text="Patient's surname : ")
        self.patient_label.grid(row=2, column=0, padx=5, pady=5)

        #doctor
        self.doctor_entry = CTK.CTkEntry(self, placeholder_text="Doctor")
        self.doctor_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.doctor_label = CTK.CTkLabel(self, text="Doctor : ")
        self.doctor_label.grid(row=3, column=0, padx=5, pady=5)

        #date crise
        self.hour_entry = CTK.CTkEntry(self, placeholder_text="Time of seizure")
        self.hour_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.hour_label = CTK.CTkLabel(self, text="Time of seizure : ")
        self.hour_label.grid(row=4, column=0, padx=5, pady=5)

        # Bouton
        self.boutonOK = CTK.CTkButton(self, text="OK",fg_color='green', hover_color= ('darkgreen'))
        self.boutonOK.bind("<Button-1>", self.get_metadata)
        self.boutonOK.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Lier l'événement <Return> à la fonction get_metadata
        self.bind('<Return>', lambda event: self.get_metadata(event))
    

    def get_metadata(self, event):
        """
        ecrire une liste des metadonnées sous la forme [heure réelle, patient, praticien]

        Args:
            event (any): correspont a l'ecriture dans les box de texte
        """
        
        self.data.set_dateCrise(self.hour_entry.get())
        self.data.set_docteur(self.doctor_entry.get())
        self.data.set_nom(self.patientName_entry.get())
        self.data.set_prenom(self.patientSurname_entry.get())
        self.data.set_dateAnnotation(datetime.date.today())
        
        EF.EcrireMetaData(self.data, self.filename)

        self.destroy()
        self.update()

class MetaData():
    def __init__(Nom="", prenom="", dateC="", doc="", dateA=""):
        self.nom = Nom
        self.prenom = prenom
        self.docteur = doc
        self.dateCrise = dateC
        self.dateAnnotation = dateA
    
    def get_nom():
        return self.nom
    
    def get_prenom():
        return self.prenom
    
    def get_docteur():
        return self.docteur
    
    def get_dateCrise():
        return self.dateCrise
    
    def get_dateAnnotation():
        return self.dateAnnotation

    def set_nom(value):
        self.nom = value

    def set_prenom(value):
        self.prenom = value

    def set_docteur(value):
        self.docteur = value
    
    def set_dateCrise(value):
        self.dateCrise = value

    def set_dateAnnotation(value):
        self.dateAnnotation = value              


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