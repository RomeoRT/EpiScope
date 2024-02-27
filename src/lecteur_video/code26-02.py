#pour lancer ce code il faut avoir le fichier "Objective_Sympotomes.txt" dans le meme dossier qu ce fichier.
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import datetime
import tkinter.font as tkFont
import os
import tkinter.font as tkFont

class Menu_symptomes(ctk.CTkFrame):
    def __init__(self, master, largeur_totale):
        super().__init__(master, width=largeur_totale)
        self.file_name = "Objective_Symptomes.txt"
        title, symptoms = self.read_symptoms_from_file(self.file_name)

        # Créer un CTkButton qui, lorsqu'il est cliqué, affiche les symptômes sous forme de menus déroulants
  
        self.symptom_button = ctk.CTkButton(self, text=title,command=self.create_dropdown_menus, width=largeur_totale,fg_color='navajo white',text_color='black')
        self.symptom_button.pack(pady=20,fill='x')
        

        self.symptoms = symptoms  # Stocker les symptômes pour les utiliser plus tard

    def create_dropdown_menus(self):
        # Cette fonction crée les menus déroulants en utilisant les symptômes stockés
        top_level = tk.Toplevel(self)  # Créer une nouvelle fenêtre pour les menus déroulants
        menu_bar = tk.Menu(top_level)  # Créer un menu bar dans la fenêtre top-level
        top_level.config(menu=menu_bar)
        my_font = tkFont.Font(size=12)  # Création d'une police de taille 10
        main_menu = tk.Menu(menu_bar, tearoff=0, bg="#444444", fg="white", font=my_font)  # Créer le menu principal
        menu_bar.add_cascade(label="Symptômes", menu=main_menu)

        for symptom, sub_symptoms in self.symptoms:
            self.create_submenu(main_menu, symptom, sub_symptoms)

        # Obtenir la position du cadre parent (supposant que c'est le master de self)
        parent_x = self.master.winfo_rootx()  # Position x du cadre parent par rapport à l'écran
        parent_y = self.symptom_button.winfo_rooty()  # Position y du bouton
        button_height = self.symptom_button.winfo_height()  # Hauteur du bouton
        frame_width = self.winfo_width()  # Largeur du cadre CTkFrame

        # Définir la géométrie de la fenêtre top-level pour qu'elle soit directement en dessous du bouton et alignée avec la limite gauche de l'interface, décalée de 5 pixels vers la gauche
        top_level.geometry(f"{frame_width}x200+{parent_x - 7}+{parent_y + button_height}")

    # Assurez-vous d'inclure les autres méthodes nécessaires comme read_symptoms_from_file et create_submenu


    def create_submenu(self,parent_menu, symptom, sub_symptoms):
        # Initialisation du menu pour ce symptôme
        my_font = tkFont.Font(size=12)
        symptom_menu = tk.Menu(parent_menu, tearoff=0, font=my_font)
        has_sub_items = False  # Indicateur pour vérifier si le symptôme a des sous-éléments

        for item in sub_symptoms:
            # Séparation des sous-symptômes et des sous-sous-symptômes
            parts = item.split('[')
            main_part = parts[0].strip()
            sub_sub_symptoms = parts[1].strip(']').split(',') if len(parts) > 1 else []

            if sub_sub_symptoms:  # Vérifie s'il y a des sous-sous-symptômes
                has_sub_items = True  # Il y a des sous-éléments
                sub_menu = tk.Menu(symptom_menu, tearoff=0, font=my_font)  # Création d'un sous-menu
                for sub_sub_symptom in sub_sub_symptoms:
                    sub_menu.add_command(label=sub_sub_symptom.strip())  # Ajout des sous-sous-symptômes
                symptom_menu.add_cascade(label=main_part, menu=sub_menu)
            else:
                symptom_menu.add_command(label=main_part)  # Ajout des sous-symptômes comme commandes simples

        # Ajout du menu en cascade seulement s'il y a des sous-éléments
        if has_sub_items:
            parent_menu.add_cascade(label=symptom, menu=symptom_menu)
        else:
            parent_menu.add_command(label=symptom)


    def read_symptoms_from_file(self,file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            title = file.readline().strip()
            symptoms = []
            for line in file:
                line = line.strip()
                if line:
                    symptom, *sub_symptoms = line.split('(')
                    symptom = symptom.strip()
                    sub_symptoms = sub_symptoms[0].replace(')', '').split(';') if sub_symptoms else []
                    symptoms.append((symptom, [sub.strip() for sub in sub_symptoms]))
        return title, symptoms



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
        self.frame_menu = ctk.CTkFrame(fenetre, fg_color='Medium orchid', height=40)
        self.frame_menu.pack(side=ctk.TOP, fill=ctk.X)
        police_label_m = tkFont.Font(size=12)
        # Menu déroulant
        options = ["Ouvrir","Ouvrir sans video","Save"]
        self.menu_deroulant = ctk.StringVar()
        self.menu_deroulant.set('Menu')
        self.menu = tk.OptionMenu(self.frame_menu, self.menu_deroulant, *options, command=self.menu_action)
        self.menu.config(bg='purple3',fg='white',font=police_label_m)
        self.menu["menu"].config(bg='black', fg='white',font=14)
        self.menu.pack(side=ctk.LEFT, padx=10, pady=10)

        # Variable pour stocker les coordonnées du clic
        self.clic_x = 0
        self.clic_y = 0
        

        # Cadres pour la partie de gauche, milieu et droite
        # Modify the frame initialization in the __init__ method of LecteurVideo class
        self.frame_left = ctk.CTkFrame(fenetre, fg_color='grey',border_width=5,width=fenetre.winfo_screenwidth() // 5)
        self.frame_middle = ctk.CTkFrame(fenetre, fg_color='grey',border_width=5 ,width=3 * (fenetre.winfo_screenwidth()) // 5, height=fenetre.winfo_screenheight()  )  # Ajustement ici
        self.frame_right = ctk.CTkFrame(fenetre, fg_color='grey',border_width=5 ,width=fenetre.winfo_screenwidth() // 5)


        # Placer les cadres dans la fenêtre
        self.frame_left.pack(side=ctk.LEFT, fill=ctk.Y)
        self.frame_middle.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        self.frame_right.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=False)


        # Frame pour les boutons
        self.frame_CTkButton = ctk.CTkFrame(self.frame_middle, fg_color='grey', height=50)
        self.frame_CTkButton.pack(side=ctk.BOTTOM, fill=ctk.BOTH)
            # Boutons
        self.bouton_reculer = ctk.CTkButton(self.frame_CTkButton, text="recule", command=self.lec_video.recule_progress,text_color='black',fg_color='navajo white')
        self.bouton_reculer.pack(side=ctk.LEFT, padx=60)

        self.bouton_pause_lecture = ctk.CTkButton(self.frame_CTkButton, text="Pause", command=self.lec_video.pause_lecture,text_color='black',fg_color='light salmon')
        self.bouton_pause_lecture.pack(side=ctk.LEFT, padx=100)

        self.bouton_avancer = ctk.CTkButton(self.frame_CTkButton, text="avace", command=self.lec_video.avance_progress,text_color='black',fg_color='navajo white')
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

# Dans InterfaceGenerale:
        self.menu_symptomes = Menu_symptomes(self.frame_left, fenetre.winfo_screenwidth() // 5)

 # root au lieu de self.frame_left

        self.menu_symptomes.pack(expand=True, fill=ctk.BOTH)




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
            self.interface_generale.cap = cv2.VideoCapture(file_path)

            largeur = int(self.interface_generale.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            hauteur = int(self.interface_generale.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Mettre à jour la taille du canevas pour correspondre à la partie du milieu
            largeur_partie_milieu = self.interface_generale.frame_middle.winfo_reqwidth()
            hauteur_partie_milieu = self.interface_generale.frame_middle.winfo_reqheight()
            hauteur_canevas = (largeur_partie_milieu / largeur) * hauteur

            self.interface_generale.canvas.configure(width=largeur_partie_milieu, height=hauteur_canevas)

            self.interface_generale.progress_slider.configure(to=self.interface_generale.cap.get(cv2.CAP_PROP_FRAME_COUNT))

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
        if self.interface_generale.cap.isOpened():
            ret, frame = self.interface_generale.cap.read()
            if ret:
                # Convertir BGR en RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Ajuster la taille du frame pour correspondre à la taille du canevas
                largeur_canevas = self.interface_generale.canvas.winfo_width()
                hauteur_canevas = self.interface_generale.canvas.winfo_height()
                frame = cv2.resize(frame, (largeur_canevas, hauteur_canevas))

                # Convertir l'image CV2 en image Tkinter
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame))

                # Afficher l'image dans le canevas
                self.interface_generale.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                self.interface_generale.canvas.image = photo  # Empêcher l'image d'être effacée par le ramasse-miettes.

                # Mise à jour du temps écoulé et du temps total
                frame_number = self.interface_generale.cap.get(cv2.CAP_PROP_POS_FRAMES)
                fps = self.interface_generale.cap.get(cv2.CAP_PROP_FPS)
                total_frames = self.interface_generale.cap.get(cv2.CAP_PROP_FRAME_COUNT)

                temps_ecoule = int(frame_number / fps)
                duree_totale = int(total_frames / fps)
                self.interface_generale.label_temps.config(text=f"Temps écoulé: {self.format_duree(temps_ecoule)} / Durée totale: {self.format_duree(duree_totale)}")

                # S'assurer que la vidéo continue de jouer si elle n'est pas en pause
                if not self.interface_generale.lec_video.video_paused:
                    self.interface_generale.canvas.after(int(1000/fps), self.afficher_video)

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

    def avance_progress(self):
        if self.interface_generale.cap.isOpened():
            current_frame = self.interface_generale.cap.get(cv2.CAP_PROP_POS_FRAMES)
            fps = self.interface_generale.cap.get(cv2.CAP_PROP_FPS)
            new_frame = current_frame + fps * 2  # Avance de 2 secondes
            self.interface_generale.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
            # Ne pas appeler afficher_video ici pour éviter le dédoublement

    def recule_progress(self):
        if self.interface_generale.cap.isOpened():
            current_frame = self.interface_generale.cap.get(cv2.CAP_PROP_POS_FRAMES)
            fps = self.interface_generale.cap.get(cv2.CAP_PROP_FPS)
            new_frame = max(0, current_frame - fps * 2)  # Recule de 2 secondes
            self.interface_generale.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
            # Ne pas appeler afficher_video ici pour éviter le dédoublement


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
