from class_symptome import Symptome
import tkinter as tk

class SymptomeEditor:

    def __init__(self, master, Symp):
        self.master = master
        self.Symp = Symp
        self.master.title("Éditeur de Symptômes")
        self.master.geometry("500x350")  # taille initiale de la fenêtre

        # champs de saisie pour chaque attribut
        self.id_entry = self.create_entry("ID :", self.Symp.ID)
        self.nom_entry = self.create_entry("Nom :", self.Symp.Nom)
        self.lat_entry = self.create_entry("Latéralisation :", self.Symp.Lateralisation)
        self.seg_entry = self.create_entry("Segment Corporel :", self.Symp.SegCorporel)
        self.ori_entry = self.create_entry("Orientation :", self.Symp.Orientation)
        self.attr_entry = self.create_entry("Attribut Supplémentaire :", self.Symp.AttributSuppl)
        self.tdeb_entry = self.create_entry("Temps début:", self.Symp.Tdeb)
        self.tfin_entry = self.create_entry("Temps fin :", self.Symp.Tfin)
        self.comment_entry = self.create_entry("Commentaire :", self.Symp.Commentaire)

        # Bouton pour appliquer les modifications
        self.apply_button = tk.Button(master, text="Confirmer", command= lambda: self.apply_changes(Symp), bg="#FFFFFF", fg="black")
        self.apply_button.pack(pady=10)

        # Lier l'événement <Return> à la fonction apply_changes
        master.bind('<Return>', lambda event: self.apply_changes(Symp))

    def create_entry(self, label_text, initial_value):
        # label et un champ de saisie pour un attribut
        frame = tk.Frame(self.master, pady=5)
        frame.pack()

        label = tk.Label(frame, text=label_text, width=20, anchor='e')
        label.pack(side=tk.LEFT, padx=5)

        entry = tk.Entry(frame, width=30)
        entry.insert(tk.END, initial_value)
        entry.pack(side=tk.RIGHT)

        return entry

    def apply_changes(self,Symp):
        # Récupère les valeurs saisies et met à jour les attributs de la classe Symp
        if self.id_entry.get():
            self.Symp.ID = self.id_entry.get()
        if self.nom_entry.get():
            self.Symp.Nom = self.nom_entry.get()
        if self.lat_entry.get():
            self.Symp.Lateralisation = self.lat_entry.get()
        if self.seg_entry.get():
            self.Symp.SegCorporel = self.seg_entry.get()
        if self.ori_entry.get():
            self.Symp.Orientation = self.ori_entry.get()
        if self.attr_entry.get():
            self.Symp.AttributSuppl = self.attr_entry.get()
        if self.tdeb_entry.get():
            self.Symp.Tdeb = self.tdeb_entry.get()
        if self.tfin_entry.get():
            self.Symp.Tfin = self.tfin_entry.get()
        if self.comment_entry.get():
            self.Symp.Commentaire = self.comment_entry.get()

        self.master.destroy()
