"""
This module defines a SymptomeEditor class for editing symptom attributes via a graphical user interface.
"""
import tkinter as tk
import customtkinter as CTK


from annotation.class_symptome import Symptome

class SymptomeEditor(CTK.CTkToplevel):
    """
    SymptomeEditor class for editing symptom attributes via a graphical user interface.
    Allows editing of symptoms through a window.

    Attributes:
        Symp (:obj:`Symptome`): An instance of the Symptome class representing the symptom to be edited.
    """
    def __init__(self, Symp):
        """
        Initializes the SymptomeEditor object.

        Args:
            Symp (:obj:`Symptome`): The Symptome object to be edited.
        """
        super().__init__()
        self.Symp = Symp
        self.title("Symptom Editor")
        self.geometry("400x400")  # taille initiale de la fenêtre

        # champs de saisie pour chaque attribut
        self.id_entry = self.create_entry("ID:", self.Symp.ID, 1)
        self.Name_entry = self.create_entry("Name:", self.Symp.Name, 2)
        self.lat_entry = self.create_entry("Lateralization:", self.Symp.Lateralization, 3)
        self.seg_entry = self.create_entry("Topography:", self.Symp.Topography, 4)
        self.ori_entry = self.create_entry("Orientation:", self.Symp.Orientation, 5)
        self.attr_entry = self.create_entry("Additionnal Attribute:", self.Symp.AttributSuppl, 6)
        self.tdeb_entry = self.create_entry("Start Time:", self.Symp.Tdeb, 7)
        self.tfin_entry = self.create_entry("End Time:", self.Symp.Tfin, 8)
        self.comment_entry = self.create_entry("Comment:", self.Symp.Comment, 9)

        # Bouton pour appliquer les modifications
        self.boutonOK = CTK.CTkButton(self, text="OK",fg_color='green', hover_color= ('darkgreen'))
        self.boutonOK.bind("<Button-1>", lambda event: self.apply_changes(Symp))
        self.boutonOK.grid(row=10, column=1, padx=5, pady=5, sticky="ew")

        # Lier l'événement <Return> à la fonction apply_changes
        self.bind('<Return>', lambda event: self.apply_changes(Symp))

    def create_entry(self, label_text, initial_value, i):
        """
        Creates and places text entry fields (entries) on the window.

        Args:
            label_text (str): The label for the entry.
            initial_value (str): The current value of the entry.
            i (int): The index of the entry row.
        """
        # label et un champ de saisie pour un attribut
        #frame = tk.Frame(self.master, pady=5)
        #frame.pack()

        label = CTK.CTkLabel(self, text=label_text)
        label.grid(row=i, column=0, padx=5, pady=5)

        entry = CTK.CTkEntry(self,placeholder_text=initial_value)
        #entry.insert(tk.END, initial_value)
        entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")

        return entry

    def apply_changes(self,Symp):
        """
        Retrieves the entered values and updates the attributes of the Symp class.

        Args:
            Symp (:obj:`Symptome`): The Symptome object to be updated.
        """
        if self.id_entry.get():
            self.Symp.ID = self.id_entry.get()
        if self.Name_entry.get():
            self.Symp.Name = self.Name_entry.get()
        if self.lat_entry.get():
            self.Symp.Lateralization = self.lat_entry.get()
        if self.seg_entry.get():
            self.Symp.Topography = self.seg_entry.get()
        if self.ori_entry.get():
            self.Symp.Orientation = self.ori_entry.get()
        if self.attr_entry.get():
            self.Symp.AttributSuppl = self.attr_entry.get()
        if self.tdeb_entry.get():
            self.Symp.Tdeb = self.tdeb_entry.get()
        if self.tfin_entry.get():
            self.Symp.Tfin = self.tfin_entry.get()
        if self.comment_entry.get():
            self.Symp.Comment = self.comment_entry.get()

        self.destroy()

        
if __name__=="__main__":
    # Création d'une instance de la classe Symptome pour tester l'éditeur
    Symp = Symptome(ID="", Name="cuhecbe s", Lateralization="", Topography="", Orientation="", AttributSuppl="", Tdeb="", Tfin="", Comment="")

    # Création de la fenêtre principale de l'éditeur
    root = CTK.CTk()
    root.title("coucou")
    editor= SymptomeEditor(Symp)
    root.mainloop()


    print(Symp.Name, Symp.Lateralization)