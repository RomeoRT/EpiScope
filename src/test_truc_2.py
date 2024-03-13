# pour lancer ce code il faut avoir le fichier "Objective_Sympotomes.txt" dans le meme dossier qu ce fichier.
# ce code genere les menus derouants indenté dans la partie gauche et affiche dan sla partie droite le schema complet.
# le pb est que les menus indentés s'affichent dans une feetre à part

"""
code de l'interface générale avec save 

auteur : romeo
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import datetime
import tkinter.font as tkFont
import os
import tkinter.font as tkFont
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# utile pour la génération de la frise chronologique:
from frise.fonctions_frise import afficher_frise
import frise.save  as save
# from class_symptome import Symptome

class Menu_symptomes(ctk.CTkFrame):
    def __init__(self, master, interface_generale, largeur_totale):
        """
        constructeur créant un menu déroulant
        arguments :
            master : fenetre principale 
            interface_generale : 
            largeur_totale : largeur des menus 

        """
        super().__init__(master, width=largeur_totale)
        self.interface_generale = interface_generale
        self.file_name = "Objective_Symptomes.txt"
        title, symptoms = self.read_symptoms_from_file(self.file_name)
        self.symptom_button = ctk.CTkButton(self, text=title, command=self.create_dropdown_menus, width=largeur_totale, fg_color='navajo white', text_color='black')
        self.symptom_button.pack(pady=20, fill='x')
        self.symptoms = symptoms
        self.top_level = None  



    def create_dropdown_menus(self):
        if self.top_level is None or not self.top_level.winfo_exists():  # Vérifiez si la fenêtre n'existe pas déjà
            self.top_level = tk.Toplevel(self)
            self.top_level.wm_title("Symptômes")  # Optionnel: donnez un titre à la fenêtre

            # Positionner la fenêtre juste en dessous du bouton
            x = self.symptom_button.winfo_rootx()
            y = self.symptom_button.winfo_rooty() + self.symptom_button.winfo_height()
            self.top_level.geometry(f"+{x}+{y}")  # Positionne la fenêtre

            # Définir la largeur de la fenêtre égale à celle du bouton
            self.top_level.geometry(f"{self.symptom_button.winfo_width()}x400")  # La hauteur peut être ajustée selon le besoin

            menu_bar = tk.Menu(self.top_level)
            self.top_level.config(menu=menu_bar)
            my_font = tkFont.Font(size=12)
            main_menu = tk.Menu(menu_bar, tearoff=0, bg="#444444", fg="white", font=my_font)
            menu_bar.add_cascade(label="Symptômes", menu=main_menu)
            for symptom, sub_symptoms in self.symptoms:
                self.create_submenu(main_menu, symptom, sub_symptoms)
        else:
            self.top_level.lift()  # Ramenez la fenêtre existante au premier plan
            self.top_level.focus()  # Donnez le focus à la fenêtre

    def create_submenu(self, parent_menu, symptom, sub_symptoms):
        my_font = tkFont.Font(size=12)
        symptom_menu = tk.Menu(parent_menu, tearoff=0, font=my_font)
        has_sub_items = False

        for item in sub_symptoms:
            parts = item.split('[')
            main_part = parts[0].strip()
            sub_sub_symptoms = parts[1].strip(']').split(',') if len(parts) > 1 else []

            if sub_sub_symptoms:
                has_sub_items = True
                sub_menu = tk.Menu(symptom_menu, tearoff=0, font=my_font)
                for sub_sub_symptom in sub_sub_symptoms:
                    full_path = f"{symptom} > {main_part} > {sub_sub_symptom.strip()}"
                    sub_menu.add_command(label=sub_sub_symptom.strip(), command=lambda path=full_path: self.on_select(path))
                symptom_menu.add_cascade(label=main_part, menu=sub_menu)
            else:
                full_path = f"{symptom} > {main_part}"
                symptom_menu.add_command(label=main_part, command=lambda path=full_path: self.on_select(path))

        if has_sub_items:
            parent_menu.add_cascade(label=symptom, menu=symptom_menu)
        else:
            full_path = symptom
            parent_menu.add_command(label=symptom, command=lambda path=full_path: self.on_select(path))

    def on_select(self, selection):
        # Appel à une nouvelle fonction dans InterfaceGenerale pour obtenir le temps actuel de la vidéo
        current_video_time = self.interface_generale.get_current_video_time() 
        display_text = f"{selection} - TD: {current_video_time}\n" # Ajoutez le temps actuel ici
        self.interface_generale.update_right_panel(display_text)


    def read_symptoms_from_file(self, file_name):
        """Lecture des fichiers pour créer les menus"""

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
        #for i in range(self.nb_menus) :
        options_filtrees = [option for option in self.symptoms if recherche in option.lower()]
        self.liste_MenuDeroulant.configure(values=options_filtrees) 

# Classe frise de Chloé:
class FriseSymptomes:
    def __init__(self,InterfaceGenerale,MenuDeroulant):
        self.menu_deroulant=MenuDeroulant
        self.interface_generale=InterfaceGenerale

    def afficher(self):
        # Récupérer le texte de la zone de texte des symptômes
        texte_symptomes = self.interface_generale.text_output.get("1.0", tk.END)

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


class InterfaceGenerale :
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Lecteur Vidéo")
        self.cap = None
        self.lec_video = LecteurVideo(self)
        self.frise = FriseSymptomes(self,self)
        self.lec_video.video_paused = False

        self.set_end_time_mode = False
        self.current_symptom = ""
       
        ### barre de menu 

        menu_bar = tk.Menu(fenetre, background= '#000000')
        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="video", command=self.ouvrir_video)
        menu_file.add_command(label = "black video", command=self.ouvrir_video_noire)
        menu_bar.add_cascade(label="open", menu=menu_file)

        menu_save = tk.Menu(menu_bar, tearoff=0)
        menu_save.add_command(label="compte rendu texte", command=save.save)
        menu_save.add_command(label="frise", command=None)
        menu_bar.add_cascade(label="save", menu=menu_save)

        self.fenetre.config(menu=menu_bar)

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

        self.text_output = tk.Text(self.frame_right, height=40, width=fenetre.winfo_screenwidth() // 5, relief=tk.GROOVE, wrap=tk.WORD, state=tk.DISABLED)  # Déplacé pour être un attribut de l'instance
        self.text_output.pack(side=ctk.TOP,padx=20,pady=20)

        # self.frame_right.grid_rowconfigure(0, weight=1)  # Donne un poids à la ligne où se trouve la zone de texte
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_rowconfigure(1, weight=1)  # Donne un poids à la ligne où se trouve le bouton
        self.frame_right.grid_columnconfigure(0, weight=1)  # Assure que la colonne s'étend correctement
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

        self.frame_frise = ctk.CTkFrame(self.fenetre, fg_color='light grey', border_width=5)  # Vous pouvez ajuster la couleur et les autres paramètres selon vos préférences
        self.frame_frise.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)  # Changez `side=ctk.LEFT` en fonction de l'endroit où vous souhaitez placer le cadre

        # Bouton pour activer la frise chronologique des symptomes:
        self.bouton_frise = ctk.CTkButton(self.frame_right, text="frise", command=self.frise.afficher, text_color='black', fg_color='Plum3')
        self.bouton_frise.pack(side=ctk.BOTTOM,padx=20,pady=20)

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

        self.menu_symptomes = Menu_symptomes(self.frame_left, self, fenetre.winfo_screenwidth() // 5)
        self.menu_symptomes.pack(expand=True, fill=ctk.BOTH)

        self.fenetre.bind('<space>', lambda event: self.lec_video.pause_lecture())
        self.fenetre.bind('<Right>', lambda event: self.lec_video.avance_progress())
        self.fenetre.bind('<Left>', lambda event: self.lec_video.recule_progress())

        # Créer une zone de texte pour les commentaires:
        self.zone_text = tk.Text(self.frame_right, height=20, width=fenetre.winfo_screenwidth() // 5, relief=tk.GROOVE, wrap=tk.WORD)
        self.zone_text.pack(side=tk.BOTTOM, pady=20,padx=20)

    def update_right_panel(self, text, is_start_time=False):
        

        def set_end_time(event, Symp):
            # Ajoute uniquement le temps de fin à un symptôme existant
            current_text = event.widget.cget("text")

            if Symp.Tfin=="":
                Symp.set_Tfin(f"{self.get_current_video_time()}")
                print(Symp.Tfin)
                print(Symp.Tdeb)
            # On vérifie si le temps de fin est déjà présent pour ne pas l'ajouter plusieurs fois
                # On découpe le texte actuel pour insérer le temps de fin juste après le temps de début
                parts = current_text.split(" - ")
                if len(parts) >= 2:  # Assurez-vous qu'il y a bien un temps de début pour insérer le temps de fin
                    new_text = f"{Symp.Nom} - TD: {Symp.Tdeb} - TF: {Symp.get_Tfin()}"
                    event.widget.config(text=new_text)  # Met à jour le texte du label avec le temps de fin
                    print(new_text)

        self.text_output.config(state=tk.NORMAL)  # Activez l'état normal pour permettre la mise à jour

        Symp = Symptome(ID="", Nom="", Lateralisation="", SegCorporel="", Orientation="", AttributSuppl="", Tdeb="", Tfin="", Commentaire="")
        splited = text.split(" - ")
        Symp.set_Nom(splited[0])
        Symp.set_Tdeb(splited[1][4:])
        print(Symp.get_Tdeb)
        
        symptom_with_time = f"{Symp.get_Nom()} - TD: {Symp.get_Tdeb()}"

        '''if is_start_time:
            # Pour un nouveau symptôme, ajoutez-le avec le temps de début
            Symp.set_Tdeb(f"{self.get_current_video_time()}")
            symptom_with_time = f"{Symp.get_Nom()} - TD: {Symp.get_Tdeb()}"
        else:
            # Sinon, affichez seulement le nom du symptôme
            symptom_with_time = Symp.get_Nom()'''

        symptom_label = tk.Label(self.text_output, text=symptom_with_time, bg="light grey", fg="black")

        '''symptom_label.bind('<Button-1>', lambda event: set_end_time(event, Symp)) ''' 

        # Associe l'événement de clic pour ajouter le temps de fin
        set_end_time_partial = functools.partial(set_end_time, Symp=Symp)
        symptom_label.bind('<Button-1>', set_end_time_partial)

        self.text_output.window_create(tk.END, window=symptom_label)  # Ajoute le symptôme à la zone de texte
        self.text_output.insert(tk.END, '\n')  # Nouvelle ligne après chaque symptôme

        self.text_output.config(state=tk.DISABLED)  # Désactive l'édition de la zone de texte après la mise à jour

        self.ListeSymptomes.append(Symp)
        print("liste :")
        print(self.ListeSymptomes)
        print(self.ListeSymptomes[0].get_Nom())
        print(self.ListeSymptomes[0].get_Tdeb())
        print("fin liste ...")

    def get_current_video_time(self):
        if self.cap is not None and self.cap.isOpened():
            current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            current_time_seconds = int(current_frame / fps)
            current_time_formatted = self.lec_video.format_duree(current_time_seconds)
            return current_time_formatted
        return "00:00"  # Retournez une valeur par défaut si la vidéo n'est pas ouverte

    def get_video_duration(self):
        if self.cap is not None and self.cap.isOpened():
            total_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            return int(total_frames / fps)
        return 0

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

    # ecriture de la selection dans un box à  part


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
        if self.interface_generale.set_end_time_mode and self.interface_generale.current_symptom:
            # Mettre à jour le panel de droite avec le temps de fin sans réécrire le symptôme
            self.interface_generale.update_right_panel(self.interface_generale.current_symptom, is_start_time=False)
            self.interface_generale.set_end_time_mode = False
            self.interface_generale.current_symptom = ""

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
        if self.interface_generale.set_end_time_mode:
            # Le mode de définition du temps de fin est activé
            self.afficher_video()  # Ceci va capturer le temps de fin
        else:
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
