
from class_symptome import Symptome
import tkinter as tk

class SymptomeEditor:

    def __init__(self, master):
        self.master = master
        self.master.title("Éditeur de Symptômes")
        self.master.geometry("500x350")  # taille initiale de la fenêtre

        # champs de saisie pour chaque attribut
        self.id_entry = self.create_entry("ID :")
        self.nom_entry = self.create_entry("Nom :")
        self.lat_entry = self.create_entry("Latéralisation :")
        self.seg_entry = self.create_entry("Segment Corporel :")
        self.ori_entry = self.create_entry("Orientation :")
        self.attr_entry = self.create_entry("Attribut Supplémentaire :")
        self.tdeb_entry = self.create_entry("Temps début:")
        self.tfin_entry = self.create_entry("Temps fin :")
        self.comment_entry = self.create_entry("Commentaire :")

        # Bouton pour appliquer les modifications
        self.apply_button = tk.Button(master, text="Confirmer", command=self.apply_changes, bg="#D8BFD8", fg="black")
        self.apply_button.pack(pady=10)

    def create_entry(self, label_text):
        # label et un champ de saisie pour un attribut
        frame = tk.Frame(self.master, pady=5)
        frame.pack()

        label = tk.Label(frame, text=label_text, width=20, anchor='e')
        label.pack(side=tk.LEFT, padx=5)

        entry = tk.Entry(frame, width=30)
        entry.pack(side=tk.RIGHT)

        return entry

    def apply_changes(self):
        # Récupère les valeurs saisies et met à jour les attributs de la classe Symptome
        if self.id_entry.get():
            symptome.ID = self.id_entry.get()
        if self.nom_entry.get():
            symptome.Nom = self.nom_entry.get()
        if self.lat_entry.get():
            symptome.Lateralisation = self.lat_entry.get()
        if self.seg_entry.get():
            symptome.SegCorporel = self.seg_entry.get()
        if self.ori_entry.get():
            symptome.Orientation = self.ori_entry.get()
        if self.attr_entry.get():
            symptome.AttributSuppl = self.attr_entry.get()
        if self.tdeb_entry.get():
            symptome.Tdeb = self.tdeb_entry.get()
        if self.tfin_entry.get():
            symptome.Tfin = self.tfin_entry.get()
        if self.comment_entry.get():
            symptome.Commentaire = self.comment_entry.get()

        

        print("OK!")

# Création d'une instance de la classe Symptome pour tester l'éditeur
symptome = Symptome(ID="", Nom="", Lateralisation="", SegCorporel="", Orientation="", AttributSuppl="", Tdeb="", Tfin="", Commentaire="")

# Création de la fenêtre principale de l'éditeur
root = tk.Tk()
editor = SymptomeEditor(root)

root.mainloop()

print(symptome.Nom, symptome.Lateralisation)