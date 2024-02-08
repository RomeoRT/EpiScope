#pour lancer ce code il faut avoir le fichier "Objective_Sympotomes.txt" dans le meme dossier qu ce fichier.
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import datetime
import tkinter.font as tkFont
import os

class Menu_symptomes(ctk.CTkFrame):
    def __init__(self, master, largeur_totale):
        super().__init__(master)
        Liste_cat = []
        self.options_symptomes = []
        self.liste_MenuDeroulant = []
        self.nb_menus = 0

        script_directory = os.path.dirname(os.path.abspath(__file__))
        Monfichier = os.path.join(script_directory, "Objective_symptomes.txt")

        with open(Monfichier, 'r') as file:
            for line in file:
                line = line.strip()
                Liste = line.split(';')

                Liste_cat.append(Liste[0])

                Liste = Liste[1:]
                self.options_symptomes.append(Liste)
                self.nb_menus += 1

                MenuDeroulant = ctk.CTkOptionMenu(self, values=Liste)
                self.liste_MenuDeroulant.append(MenuDeroulant)
                self.liste_MenuDeroulant[-1].grid(row=self.nb_menus, sticky="nsew", padx=5, pady=5)
                self.liste_MenuDeroulant[-1].set(Liste_cat[-1])

                # Ajuster la largeur des menus déroulants à 1/5 de la largeur totale
                menu_width = largeur_totale-91
                self.liste_MenuDeroulant[-1].configure(width=menu_width, fg_color='Plum3')

        self.entry = ctk.CTkEntry(self, placeholder_text="Symptomes")
        self.entry.grid(row=0)
        self.entry.bind("<KeyRelease>", self.filtrer_options)

        # definition des méthodes
    def filtrer_options(self, event): 
        """
        filtre les options d'un menu déroulant en fonction d'une recherche textuelle
        """
        recherche = self.entry.get().lower()
        for i in range(self.nb_menus) :
            options_filtrees = [option for option in self.options_symptomes[i] if recherche in option.lower()]
            self.liste_MenuDeroulant[i].configure(values=options_filtrees) 

class InterfaceGenerale():
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Lecteur Vidéo")
        self.cap = None
        self.lec_video=LecteurVideo(self)

        self.lec_video.video_paused = False
 
        # Cadre pour le menu déroulant en haut
        self.frame_menu = ctk.CTkFrame(fenetre, fg_color='Plum3', height=40)
        self.frame_menu.pack(side=ctk.TOP, fill=ctk.X)
        police_label_m = tkFont.Font(size=12)
        # Menu déroulant
        options = ["Ouvrir","Ouvrir sans video","Save"]
        self.menu_deroulant = ctk.StringVar()
        self.menu_deroulant.set('Menu')
        self.menu = tk.OptionMenu(self.frame_menu, self.menu_deroulant, *options, command=self.menu_action)
        self.menu.config(bg='Plum3',fg='white',font=police_label_m)
        self.menu["menu"].config(bg='black', fg='white',font=police_label_m)
        self.menu.pack(side=ctk.LEFT, padx=10, pady=10)

        # Variable pour stocker les coordonnées du clic
        self.clic_x = 0
        self.clic_y = 0
        

        # Cadres pour la partie de gauche, milieu et droite
        # Modify the frame initialization in the __init__ method of LecteurVideo class
        self.frame_left = ctk.CTkFrame(fenetre, fg_color='grey',border_width=5,border_color='Plum3' ,width=fenetre.winfo_screenwidth() // 5)
        self.frame_middle = ctk.CTkFrame(fenetre, fg_color='grey',border_width=5,border_color='Plum3' ,width=3 * (fenetre.winfo_screenwidth()) // 5, height=fenetre.winfo_screenheight() - 200 )  # Ajustement ici
        self.frame_right = ctk.CTkFrame(fenetre, fg_color='grey',border_width=5,border_color='Plum3' ,width=fenetre.winfo_screenwidth() // 5)


        # Placer les cadres dans la fenêtre
        self.frame_left.pack(side=ctk.LEFT, fill=ctk.Y)
        self.frame_middle.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        self.frame_right.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=False)


        # Frame pour les boutons
        self.frame_CTkButton = ctk.CTkFrame(self.frame_middle, fg_color='grey', height=50)
        self.frame_CTkButton.pack(side=ctk.BOTTOM, fill=ctk.BOTH)
            # Boutons
        self.bouton_reculer = ctk.CTkButton(self.frame_CTkButton, text="-2s", command=self.lec_video.recule_progress,text_color='black',fg_color='Plum3')
        self.bouton_reculer.pack(side=ctk.LEFT, padx=50)

        self.bouton_pause_lecture = ctk.CTkButton(self.frame_CTkButton, text="Pause", command=self.lec_video.pause_lecture,text_color='black',fg_color='Plum3')
        self.bouton_pause_lecture.pack(side=ctk.LEFT, padx=100)

        self.bouton_avancer = ctk.CTkButton(self.frame_CTkButton, text="+2s", command=self.lec_video.avance_progress,text_color='black',fg_color='Plum3')
        self.bouton_avancer.pack(side=ctk.LEFT, padx=50)

        
        # Étiquettes pour afficher le temps écoulé et la durée totale
        self.label_temps = tk.Label(self.frame_middle, text="Temps écoulé: 0:00 / Durée totale: 0:00", bg='grey', fg='white')
        self.label_temps.pack(side=tk.BOTTOM, padx=20)

        # Barre de progression manuelle
        self.progress_slider =tk.Scale(self.frame_middle, from_=0, to=100, orient="horizontal", command=self.lec_video.manual_update_progress)
        self.progress_slider.pack(side=tk.BOTTOM, fill=tk.X)


        # Lire la vidéo avec OpenCV
        self.cap = None

        # Créer un Canvas pour afficher la vidéo
        self.canvas = ctk.CTkCanvas(self.frame_middle, bg='grey')
        self.canvas.pack(expand=True, fill=ctk.BOTH)

        # Binding du clic gauche à l'affichage du menu
        self.canvas.bind("<Button-1>", self.lec_video.afficher_menu_annotations)

        # Ajout de la partie gauche avec les menus déroulants
        self.menu_symptomes = Menu_symptomes(self.frame_left, self.frame_left.winfo_reqwidth())
        self.menu_symptomes.pack(side=ctk.LEFT, fill=ctk.Y)


        # Ajuster la taille des cadres après ajout de la partie gauche
        #self.frame_left.configure(width=fenetre.winfo_screenwidth() // 5)
        #self.frame_middle.configure(width=3 * (fenetre.winfo_screenwidth()) // 5)
        #self.frame_right.configure(width=fenetre.winfo_screenwidth() // 5)


        self.fenetre.bind('<space>', lambda event: self.lec_video.pause_lecture())
        self.fenetre.bind('<Right>', lambda event: self.lec_video.avance_progress())
        self.fenetre.bind('<Left>', lambda event: self.lec_video.recule_progress())
 
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
