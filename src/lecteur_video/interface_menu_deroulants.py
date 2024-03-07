import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import datetime
import tkinter.font as tkFont
import os
import random

#utile pour la génération de la frise chronologique:
from fonctions_frise import afficher_frise
from class_symptome import Symptome


#Classe menu déroulant d'Annaelle:
class MenuDeroulant(tk.Frame):
    def __init__(self, master, largeur,InterfaceGenerale):
        super().__init__(master)
        self.interface_generale = InterfaceGenerale
        self.master = master
        self.largeur = largeur
        
        # Créer le cadre pour le menu déroulant
        self.frame_menu = tk.Frame(master, bg='grey')
        self.frame_menu.pack(side=tk.LEFT, fill=tk.Y)

        # Créer le menu déroulant
        self.create_dropdown_menus()
        
        # Zone de texte pour la partie de droite
        self.symptomes_text = tk.Text(self.interface_generale.frame_right, height=40, width=40, relief=tk.GROOVE, wrap=tk.WORD, state=tk.DISABLED)
        self.symptomes_text.pack(side=tk.TOP, padx=20,pady=15)
    
    def create_dropdown_menus(self):
        # Charger les options du fichier
        script_directory = os.path.dirname(os.path.abspath(__file__))
        mon_fichier = os.path.join(script_directory, "Liste_Fruits.txt")

        with open(mon_fichier, 'r') as file:
            for line in file:
                line = line.strip()
                liste = line.split(';')

                var_selected = tk.StringVar()
                var_selected.set(liste[0])

                # Créer le menu déroulant
                menu_deroulant = tk.OptionMenu(self.frame_menu, var_selected, *liste)
                menu_deroulant.pack(side=tk.TOP, padx=5, pady=5)

                # Configuration de la fonction appelée lorsqu'une option est sélectionnée
                var_selected.trace_add('write', lambda *args, var=var_selected: self.on_select(var))

    def on_select(self, var_selected):
        symptome = var_selected.get()

        # Mettre à jour le contenu de la zone de texte des symptômes dans la partie droite
        
        self.symptomes_text.config(state=tk.NORMAL)
        self.symptomes_text.insert(tk.END, symptome + "\n")
        self.symptomes_text.config(state=tk.DISABLED)


class InterfaceGenerale():
    def __init__(self, fenetre,):
        self.fenetre = fenetre
        self.fenetre.title("Lecteur Vidéo")
        self.cap = None
        self.lec_video = LecteurVideo(self)
        self.frise=FriseSymptomes(self,self)

        self.lec_video.video_paused = False

        # Cadre pour le menu déroulant en haut
        self.frame_menu = ctk.CTkFrame(fenetre, fg_color='Plum3', height=40)
        self.frame_menu.pack(side=ctk.TOP, fill=ctk.X)
        police_label_m = tkFont.Font(size=12)

        # Menu déroulant
        options = ["Ouvrir", "Ouvrir sans video", "Save"]
        self.menu_deroulant = ctk.StringVar()
        self.menu_deroulant.set('Menu')
        self.menu = tk.OptionMenu(self.frame_menu, self.menu_deroulant, *options, command=self.menu_action)
        self.menu.config(bg='Plum3', fg='white', font=police_label_m)
        self.menu["menu"].config(bg='black', fg='white', font=police_label_m)
        self.menu.pack(side=ctk.LEFT, padx=10, pady=10)

        # Variable pour stocker les coordonnées du clic
        self.clic_x = 0
        self.clic_y = 0

        # Cadres pour la partie de gauche, milieu et droite
        self.frame_left = ctk.CTkFrame(fenetre, fg_color='grey', border_width=5, border_color='Plum3',width=fenetre.winfo_screenwidth() // 5) 
        self.frame_middle = ctk.CTkFrame(fenetre, fg_color='grey', border_width=5, border_color='Plum3', width=3 * (fenetre.winfo_screenwidth()) // 5, height=fenetre.winfo_screenheight() - 200)  
        self.frame_right = ctk.CTkFrame(fenetre, fg_color='grey', border_width=5, border_color='Plum3', width=fenetre.winfo_screenwidth() // 5)

        # Placer les cadres dans la fenêtre
        self.frame_left.pack(side=ctk.LEFT, fill=ctk.Y)
        self.frame_middle.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        self.frame_right.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=False)

        # Frame pour les boutons
        self.frame_CTkButton = ctk.CTkFrame(self.frame_middle, fg_color='grey', height=50)
        self.frame_CTkButton.pack(side=ctk.BOTTOM, fill=ctk.BOTH)

        # Boutons
        self.bouton_reculer = ctk.CTkButton(self.frame_CTkButton, text="-2s", command=self.lec_video.recule_progress,text_color='black', fg_color='Plum3') 
        self.bouton_reculer.pack(side=ctk.LEFT, padx=50)

        self.bouton_pause_lecture = ctk.CTkButton(self.frame_CTkButton, text="Pause", command=self.lec_video.pause_lecture, text_color='black',fg_color='Plum3')
        self.bouton_pause_lecture.pack(side=ctk.LEFT, padx=100)

        self.bouton_avancer = ctk.CTkButton(self.frame_CTkButton, text="+2s", command=self.lec_video.avance_progress, text_color='black', fg_color='Plum3')
        self.bouton_avancer.pack(side=ctk.LEFT, padx=50)

        # Bouton pour activer la frise chronologique des symptomes:
        self.bouton_frise = ctk.CTkButton(self.frame_right, text="frise", command=self.frise.afficher, text_color='black', fg_color='Plum3')
        self.bouton_frise.pack(side=ctk.BOTTOM, padx=20, pady=20)

        # Étiquettes pour afficher le temps écoulé et la durée totale
        self.label_temps = tk.Label(self.frame_middle, text="Temps écoulé: 0:00 / Durée totale: 0:00", bg='grey', fg='white')
        self.label_temps.pack(side=tk.BOTTOM, padx=20)

        # Barre de progression manuelle
        self.progress_slider = tk.Scale(self.frame_middle, from_=0, to=100, orient="horizontal",  command=self.lec_video.manual_update_progress)
        self.progress_slider.pack(side=tk.BOTTOM, fill=tk.X)

        # Créer un Canvas pour afficher la vidéo
        self.canvas = ctk.CTkCanvas(self.frame_middle, bg='grey')  
        self.canvas.pack(expand=True, fill=ctk.BOTH)

        # Binding du clic gauche à l'affichage du menu
        self.canvas.bind("<Button-1>", self.lec_video.afficher_menu_annotations)

        # Ajout de la partie gauche avec les menus déroulants
        self.menu_symptomes = MenuDeroulant(self.frame_left,self.frame_left,self)
        self.menu_symptomes.pack(side=ctk.LEFT, fill=ctk.Y)

        self.fenetre.bind('<space>', lambda event: self.lec_video.pause_lecture())
        self.fenetre.bind('<Right>', lambda event: self.lec_video.avance_progress())
        self.fenetre.bind('<Left>', lambda event: self.lec_video.recule_progress())

        # Créer une zone de texte pour afficher les symptômes dans la partie droite
        self.zone_text = tk.Text(self.frame_right, height=40, width=40, relief=tk.GROOVE, wrap=tk.WORD)
        self.zone_text.pack(side=tk.BOTTOM, pady=20)


    def ouvrir_video(self):
        self.lec_video.ouvrir_video()
    
    def ouvrir_video_noire(self):
        self.lec_video.ouvrir_video_noire()


    def menu_action( self,selection):
        if selection == "Ouvrir":
            self.ouvrir_video()
        else:
            if (selection == "Ouvrir sans video"):
                
                self.ouvrir_video_noire()
    

    def lire_fichier(self,nom_fichier):
        try:
            # Ouvre le fichier en mode lecture
            with open(nom_fichier, 'r') as fichier:
                # Lit toutes les lignes du fichier et les stocke dans une liste
                lignes = fichier.read().splitlines()
                return lignes
        except FileNotFoundError:
            print(f"Le fichier {nom_fichier} n'a pas été trouvé.")
            return 


# Classe frise de Chloé:
class FriseSymptomes:
    def __init__(self,InterfaceGenerale,MenuDeroulant):
        self.menu_deroulant=MenuDeroulant
        self.interface_generale=InterfaceGenerale

    def afficher(self):
        # Récupérer le texte de la zone de texte des symptômes
        texte_symptomes = self.interface_generale.menu_symptomes.symptomes_text.get("1.0", tk.END)

        # Diviser le texte en une liste de lignes
        lignes_symptomes = texte_symptomes.splitlines()

        # Créer une liste pour stocker les informations des symptômes
        symptomes_formattes = []

        # Parcourir chaque ligne de symptômes
        for ligne in lignes_symptomes:
            nom=ligne
            # Extraire les informations sur le symptôme (nom, temps de début, temps de fin)
            tdeb = random.randint(0,3)
            tfin = random.randint(4,10)
            # Ajouter les informations formatées à la liste des symptômes
            symptomes_formattes.append([nom, tdeb, tfin])

        # Triez les symptômes par temps de début
        symptomes_formattes.pop()
        symptomes_formattes.sort(key=lambda x: x[1])

        # Appelez la fonction afficher_frise avec la liste de symptômes formatés
        afficher_frise(symptomes_formattes)


class LecteurVideo():
    
    def __init__(self, InterfaceGenerale):

        self.interface_generale = InterfaceGenerale
        self.canvas = None  # Initialisation de la variable canvas

    def ouvrir_video_noire(self):
        # Chemin du fichier vidéo "ma vidéo noire" dans le dossier courant
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "video_noire.mp4")
        print("Chemin du fichier vidéo:", file_path)

        if os.path.exists(file_path):
            self.cap = cv2.VideoCapture(file_path)

            largeur = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            hauteur = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Mettre à jour la taille du canevas pour correspondre à la partie du milieu
            largeur_partie_milieu = self.interface_generale.frame_middle.winfo_reqwidth()
            hauteur_partie_milieu = self.interface_generale.frame_middle.winfo_reqheight() - 50
            hauteur_canevas = (largeur_partie_milieu / largeur) * hauteur

            self.interface_generale.canvas.configure(width=largeur_partie_milieu, height=hauteur_canevas)

            self.interface_generale.progress_slider.configure(to=self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

            self.afficher_video()
            self.interface_generale.bouton_pause_lecture.configure(state=ctk.NORMAL)
        else:
            print("La vidéo 'vidéo noire' n'a pas été trouvée dans le dossier courant.")



    def ouvrir_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers vidéo", "*.mp4 *.avi")])
        if file_path:
            self.interface_generale.cap = cv2.VideoCapture(file_path)

            largeur = int(self.interface_generale.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            hauteur = int(self.interface_generale.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Mettre à jour la taille du canevas pour correspondre à la partie du milieu
            largeur_partie_milieu = self.interface_generale.frame_middle.winfo_reqwidth()
            hauteur_partie_milieu = self.interface_generale.frame_middle.winfo_reqheight() - 50
            hauteur_canevas = (largeur_partie_milieu / largeur) * hauteur

            self.interface_generale.canvas.configure(width=largeur_partie_milieu, height=hauteur_canevas)



            # Ajuster la taille du canevas pour occuper toute la partie du milieu
            self.interface_generale.canvas.config(width=largeur_partie_milieu, height=hauteur_canevas)

            self.interface_generale.progress_slider.configure(to=self.interface_generale.cap.get(cv2.CAP_PROP_FRAME_COUNT))

            self.afficher_video()
            self.interface_generale.bouton_pause_lecture.configure(state=ctk.NORMAL)

    def afficher_video(self):
        ret, frame = self.interface_generale.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Redimensionner l'image pour qu'elle corresponde à la taille du canevas
            largeur_canevas = self.interface_generale.canvas.winfo_width()
            hauteur_canevas = self.interface_generale.canvas.winfo_height()
            frame = cv2.resize(frame, (largeur_canevas, hauteur_canevas))

            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.interface_generale.canvas.create_image(0, 0, anchor=ctk.NW, image=photo)
            self.interface_generale.canvas.image = photo

            if not self.video_paused:
                # Ajuster le délai ici pour refléter le temps réel entre les images
                delay = int(1000 / self.interface_generale.cap.get(cv2.CAP_PROP_FPS))
                self.interface_generale.canvas.after(delay, self.afficher_video)

            # Mettre à jour l'étiquette du temps écoulé et de la durée totale
            temps_ecoule = int(self.interface_generale.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)
            duree_totale = int(self.interface_generale.cap.get(cv2.CAP_PROP_FRAME_COUNT) / self.interface_generale.cap.get(cv2.CAP_PROP_FPS))
            self.interface_generale.label_temps.config(text=f"Temps écoulé: {self.format_duree(temps_ecoule)} / Durée totale: {self.format_duree(duree_totale)}")

    def pause_lecture(self):
        if self.video_paused:
            self.interface_generale.bouton_pause_lecture.configure(text="Pause")
            self.video_paused = False
            self.afficher_video()
        else:
            self.interface_generale.bouton_pause_lecture.configure(text="Reprendre")
            self.video_paused = True

    def manual_update_progress(self, value):
        frame_number = int(value)
        self.interface_generale.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        self.afficher_video()

    def avance_progress(self, event=None):
        current_time = self.interface_generale.cap.get(cv2.CAP_PROP_POS_MSEC)
        self.interface_generale.cap.set(cv2.CAP_PROP_POS_MSEC, current_time + 2000)  # Avancer de 2000 millisecondes (2 secondes)
        self.afficher_video()

    def recule_progress(self, event=None):
        current_time = self.interface_generale.cap.get(cv2.CAP_PROP_POS_MSEC)
        new_time = max(0, current_time - 2000)  # Reculer de 2000 millisecondes (2 secondes)
        self.interface_generale.cap.set(cv2.CAP_PROP_POS_MSEC, new_time)
        self.afficher_video()

    def format_duree(self, seconds):
        return str(datetime.timedelta(seconds=seconds))

    def afficher_menu_annotations(self, event):
        # Coordonnées du clic
        x = event.x
        y = event.y
        largeur_canevas = self.interface_generale.canvas.winfo_width()
        hauteur_canevas = self.interface_generale.canvas.winfo_height()
        # Calcul des dimensions d'une case
        largeur_case = largeur_canevas // 2
        hauteur_case = hauteur_canevas // 2
        # Déterminer dans quelle case se trouve le clic
        colonne = x // largeur_case
        ligne = y // hauteur_case
        taille_plus = 1/3  

        self.ajouter_plus_rouge(self.canvas, x, y, taille_plus)
        if colonne == 0 and ligne == 0:
            print("la case 1 a été selectionnée")
        elif colonne == 1 and ligne == 0:
            print ("la case 2 a été sélectionnée")
        elif colonne == 0 and ligne == 1:
            print ("la case 3 a été sélectionnée")
        elif colonne == 1 and ligne == 1:
            print ("la case 4 a été sélectionnée")
        
    def ajouter_plus_rouge(self,canvas, x, y, taille):
        # Coordonnées pour créer un '+'
        ligne_horizontale = self.interface_generale.canvas.create_line(x-taille*20, y, x+taille*20, y, fill="red", width=3)
        ligne_verticale = self.interface_generale.canvas.create_line(x, y-taille*20, x, y+taille*20, fill="red", width=3)
                
        self.interface_generale.canvas.after(1000, lambda: self.interface_generale.canvas.delete(ligne_horizontale, ligne_verticale))

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))  # Plein écran
    lecteur = InterfaceGenerale(root)
    root.mainloop()