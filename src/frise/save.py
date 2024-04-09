"""

This file contains basic classes and functions for saving '.txt' files and outputting timelines.

Classes:
    save: Class dedicated to saving files.
    MetaData_WD: Toplevel window for entering metadata.

Functions:
    None

"""
from tkinter import filedialog
from tkinter import messagebox
from typing import Any
import customtkinter as CTK
import datetime

import frise.ecriture_fichier as EF
from frise.class_metadata import MetaData

class save :
    """
    Class dedicated to saving files.

    Attributes:
       symptomes (list): List of symptoms to be saved
    """
    def __init__(self, Liste_symptomes = []):
        self.symptomes = Liste_symptomes
        
    def save(self):
        """
        Saves the symptoms to a file for reloading.

        Raises:
            FileNotFoundError: Error message if failed to retrieve file path.
        """
        # récuperer le nom et emplacement des fichiers
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])
        try :
            if self.symptomes == [] :
                messagebox.showinfo('Episcope Error', 'Empty symptom list\nCannot save properly')
            else :
                # ecrire les métadatas

                EF.EcrireListeSymptome(self.symptomes, filename)

        except FileNotFoundError:
            messagebox.showinfo('Episcope Error', 'No file selected\nCannot save properly')


    def write_report(self):
        """
        Writes a human-readable file.

        Raises:
            FileNotFoundError: Error message if failed to retrieve file path.
        """
        # récuperer le nom et emplacement des fichiers
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])
        try :
            if self.symptomes == [] :
                messagebox.showinfo('Episcope Error', 'Empty symptom list\nCannot save properly')
            else :
                # ecrire les métadatas
                Meta_wd = MetaData_WD(filename)
                Meta_wd.after(100, Meta_wd.lift)

                # Ecrire le rapport
                EF.ecrire_rapport(self.symptomes, filename)

        except FileNotFoundError:
            Meta_wd.destroy()
            Meta_wd.update()
            messagebox.showinfo('Episcope Error', 'No file selected\nCannot save properly')
    
    def set_symptomes(self, Liste_symptomes):
        """
        Updates the symptoms.

        Args:
            Liste_symptomes (list): List of symptoms
        """
        self.symptomes = Liste_symptomes



        
        
class MetaData_WD(CTK.CTkToplevel) :
    """
    Toplevel window for entering metadata.

    Attributes:
        liste (list): List of symptoms to be saved.
        filename (string): Path of the file to write to.
    """
    def __init__(self,filename) :
        """
        Constructor for metadata.

        Args:
            filename (string): Path of the file to write to.
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
        self.boutonOK.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        # Lier l'événement <Return> à la fonction get_metadata
        self.bind('<Return>', lambda event: self.get_metadata(event))
    

    def get_metadata(self, event):
        """
        Write a list of metadata in the form [real time, patient, practitioner].

        Args:
            event (any): Corresponds to writing in the text boxes.
        """
        
        self.data.set_dateCrise(self.hour_entry.get())
        self.data.set_docteur(self.doctor_entry.get())
        self.data.set_nom(self.patientName_entry.get())
        self.data.set_prenom(self.patientSurname_entry.get())
        self.data.set_dateAnnotation(datetime.date.today())
        
        EF.EcrireMetaData(self.data, self.filename)

        self.destroy()
        self.update()

        return 1


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