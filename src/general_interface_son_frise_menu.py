#pour lancer ce code il faut avoir le fichier "Objective_Sympotomes.txt" dans le meme dossier qu ce fichier.
#ce code genere les menus derouants indenté dans la partie gauche et affiche dan sla partie droite le schema complet.
#le pb est que les menus indenté s'affiche dans une feetre à part
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
from tkinter import Menu
from moviepy.editor import VideoFileClip
import pygame
from pygame.time import Clock


import functools #pour update right panel

#utile pour la génération de la frise chronologique:
from fonctions_frise import chevauchement
from fonctions_frise import afficher_frise
from fonctions_frise import chercherElt
from class_symptome import Symptome


class Menu_symptomes(ctk.CTkFrame):
    def __init__(self, master, interface_generale, largeur_totale):
        super().__init__(master, width=largeur_totale)
        self.interface_generale = interface_generale
        self.file_name = "Objective_Symptomes.txt"
        title, symptoms = self.read_symptoms_from_file(self.file_name)
        self.symptoms = symptoms
        self.file_name2 = "Subjective_Symptomes.txt"
        title2, symptoms2 = self.read_symptoms_from_file(self.file_name2)
        self.symptoms2 = symptoms2

        self.create_dropdown_menus(master,largeur_totale)  # Crée et affiche les menus déroulants

    def create_dropdown_menus(self,master,largeur_totale):
        # Crée une nouvelle fenêtre
        fenetre = tk.Toplevel(master,width=largeur_totale+40,height=30,bg="grey")
        fenetre.title("")
        fenetre.protocol("WM_DELETE_WINDOW", lambda: None)

        fenetre.transient(master) 
        # Positionne le Toplevel
        fenetre.geometry(f"+{0}+{100}")       
            
        # Crée une barre de menus pour la fenêtre
        menu_bar = Menu(fenetre)
        fenetre.config(menu=menu_bar)

        # Crée un menu principal dans la barre de menus
        my_font = tkFont.Font(size=12)
        main_menu = Menu(menu_bar, tearoff=0, bg="grey", fg="white", font=my_font)
        menu_bar.add_cascade(label="        Symptômes objectifs        ", menu=main_menu)
        main_menu.add_separator()
        main_menu2 = Menu(menu_bar, tearoff=0, bg="grey", fg="white", font=my_font)
        menu_bar.add_cascade(label="        Symptômes subjectifs       ", menu=main_menu2)
        
        # Ajoute les sous-menus avec les symptômes et sous-symptômes
        for symptom, sub_symptoms in self.symptoms:
            self.create_submenu(main_menu, symptom, sub_symptoms)

        for symptom2, sub_symptoms2 in self.symptoms2:
            self.create_submenu(main_menu2, symptom2, sub_symptoms2)

    def create_submenu(self, parent_menu, symptom, sub_symptoms):
        my_font = tkFont.Font(size=12)
        symptom_menu = Menu(parent_menu, tearoff=0, font=my_font)
        has_sub_items = False

        # Parcourt chaque sous-symptôme pour créer des sous-menus si nécessaire
        for item in sub_symptoms:
            parts = item.split('[')
            main_part = parts[0].strip()
            sub_sub_symptoms = parts[1].strip(']').split(',') if len(parts) > 1 else []

            if sub_sub_symptoms:
                has_sub_items = True
                sub_menu = Menu(symptom_menu, tearoff=0, font=my_font)
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


# Classe frise de Chloé:
class FriseSymptomes:
    def __init__(self,InterfaceGenerale,MenuDeroulant):
        self.menu_deroulant=MenuDeroulant
        self.interface_generale=InterfaceGenerale
        

    def afficher(self):
        # Recuperation de la liste de symptomes instanciée dans class interface generale fonction update right panel
        Lsymp = self.interface_generale.ListeSymptomes
        newL=[]

        for symp in Lsymp:
            nom = symp.get_Nom()
            # Transformer la chaine str du temps de début en float
            tdeb_str = symp.get_Tdeb()
            hd, md, sd = tdeb_str.split(":")
            hd = int(hd)
            md = int(md)
            sd = int(sd)
            debut = hd * 3600 + md * 60 + sd
            # Pareil pour le temps de fin
            tfin_str = symp.get_Tfin()
            hf, mf, sf = tfin_str.split(":")
            hf = int(hf)
            mf = int(mf)
            sf = int(sf)
            fin = hf * 3600 + mf * 60 + sf
            newL.append([nom, debut, fin])

        newL = sorted(newL, key=lambda x: float(x[1]))
        afficher_frise(newL)



class InterfaceGenerale():
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Lecteur Vidéo")
        self.cap = None
        self.lec_video=LecteurVideo(self)
        self.frise=FriseSymptomes(self,self)
        self.lec_video.video_paused = False


        self.set_end_time_mode = False
        self.current_symptom = ""

        # Liste symptome vide
        self.ListeSymptomes = []

        # Cadre pour le menu déroulant en haut
        self.frame_menu = ctk.CTkFrame(fenetre, fg_color='Plum3', height=40)
        self.frame_menu.pack(side=ctk.TOP, fill=ctk.X)
        police_label_m = tkFont.Font(size=12)
        # Menu déroulant
        options = ["Ouvrir","Ouvrir sans video","Save"]
        self.menu_deroulant = ctk.StringVar()
        self.menu_deroulant.set('Menu')
        self.menu = tk.OptionMenu(self.frame_menu, self.menu_deroulant, *options, command=self.menu_action)
        self.menu.config(bg='Plum4',fg='white',font=police_label_m)
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

        self.text_output = tk.Text(self.frame_right, height=40, width=fenetre.winfo_screenwidth() // 5, relief=tk.GROOVE, wrap=tk.WORD, state=tk.DISABLED)  # Déplacé pour être un attribut de l'instance
        self.text_output.pack(side=ctk.TOP,padx=20,pady=20)

        #self.frame_right.grid_rowconfigure(0, weight=1)  # Donne un poids à la ligne où se trouve la zone de texte
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_rowconfigure(1, weight=1)  # Donne un poids à la ligne où se trouve le bouton
        self.frame_right.grid_columnconfigure(0, weight=1)  # Assure que la colonne s'étend correctement
        # Frame pour les boutons
        self.frame_CTkButton = ctk.CTkFrame(self.frame_middle, fg_color='grey', height=50)
        self.frame_CTkButton.pack(side=ctk.BOTTOM, fill=ctk.BOTH)
            # Boutons
        self.bouton_reculer = ctk.CTkButton(self.frame_CTkButton, text="recule", command=self.lec_video.recule_progress,text_color='black',fg_color='Plum4')
        self.bouton_reculer.pack(side=ctk.LEFT, padx=60)

        self.bouton_pause_lecture = ctk.CTkButton(self.frame_CTkButton, text="Pause", command=self.lec_video.pause_lecture,text_color='black',fg_color='Plum4')
        self.bouton_pause_lecture.pack(side=ctk.LEFT, padx=100)

        self.bouton_avancer = ctk.CTkButton(self.frame_CTkButton, text="avace", command=self.lec_video.avance_progress,text_color='black',fg_color='Plum4')
        self.bouton_avancer.pack(side=ctk.LEFT, padx=50)

        self.frame_frise = ctk.CTkFrame(self.fenetre, fg_color='Plum4', border_width=5)  # Vous pouvez ajuster la couleur et les autres paramètres selon vos préférences
        self.frame_frise.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)  # Changez `side=ctk.LEFT` en fonction de l'endroit où vous souhaitez placer le cadre


        # Bouton pour activer la frise chronologique des symptomes:
        self.bouton_frise = ctk.CTkButton(self.frame_right, text="frise", command=self.frise.afficher, text_color='black', fg_color='Plum4')
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

            if Symp.Tfin=="": # On vérifie si le temps de fin est déjà présent pour ne pas l'ajouter plusieurs fois
                Symp.set_Tfin(f"{self.get_current_video_time()}")
                # On découpe le texte actuel pour insérer le temps de fin juste après le temps de début
                parts = current_text.split(" - ")
                if len(parts) >= 2:  # Assurez-vous qu'il y a bien un temps de début pour insérer le temps de fin
                    new_text = f"{Symp.Nom} - TD: {Symp.Tdeb} - TF: {Symp.get_Tfin()}"
                    event.widget.config(text=new_text)  # Met à jour le texte du label avec le temps de fin

        self.text_output.config(state=tk.NORMAL)  # Activez l'état normal pour permettre la mise à jour

        Symp = Symptome(ID="", Nom="", Lateralisation="", SegCorporel="", Orientation="", AttributSuppl="", Tdeb="", Tfin="", Commentaire="")
        splited = text.split(" - ")
        Symp.set_Nom(splited[0])
        Symp.set_Tdeb(splited[1][4:])
        
        symptom_with_time = f"{Symp.get_Nom()} - TD: {Symp.get_Tdeb()}"

        symptom_label = tk.Label(self.text_output, text=symptom_with_time, bg="light grey", fg="black")

        # Associe l'événement de clic pour ajouter le temps de fin
        set_end_time_partial = functools.partial(set_end_time, Symp=Symp)
        symptom_label.bind('<Button-1>', set_end_time_partial)

        self.text_output.window_create(tk.END, window=symptom_label)  # Ajoute le symptôme à la zone de texte
        self.text_output.insert(tk.END, '\n')  # Nouvelle ligne après chaque symptôme

        self.text_output.config(state=tk.DISABLED)  # Désactive l'édition de la zone de texte après la mise à jour

        self.ListeSymptomes.append(Symp)
        

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


    #ecriture de la selection dans un box à  part



class LecteurVideo():

    def __init__(self, InterfaceGenerale):
        self.interface_generale = InterfaceGenerale
        pygame.mixer.init()
        self.video_paused = False
        self.current_frame_time = 0
        self.clock = Clock()  # Initialisez l'horloge pygame

    def ouvrir_video(self):
        # Sélection du fichier vidéo et préparation de la vidéo et du son
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers vidéo", "*.mp4 *.avi")])
        if file_path:
            self.interface_generale.cap = cv2.VideoCapture(file_path)
            if not self.interface_generale.cap.isOpened():
                print("Erreur: Impossible d'ouvrir la vidéo.")
                return
            self.preparer_son_video(file_path)
            self.afficher_video()

    def preparer_son_video(self, file_path):
        # Convertir la piste audio de la vidéo en fichier WAV
        clip = VideoFileClip(file_path)
        audio_path = "temp_audio.wav"  # Définissez le chemin de fichier pour l'audio temporaire
        clip.audio.write_audiofile(audio_path)
        clip.close()  # Fermez le clip pour libérer les ressources

        # Utilisez pygame.mixer.music pour charger et jouer la piste audio
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play(-1)  # Jouez en boucle



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

    def mettre_a_jour_frame_video(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.interface_generale.canvas.create_image(0, 0, image=frame, anchor=tk.NW)
        self.interface_generale.canvas.image = frame

    def mettre_a_jour_temps_video(self):
        self.current_frame_time = self.interface_generale.cap.get(cv2.CAP_PROP_POS_MSEC)
        if not self.video_paused:
            self.interface_generale.fenetre.after(33, self.afficher_video)  # Continuez la lecture environ toutes les 33 ms

    def pause_lecture(self):
        self.video_paused = not self.video_paused
        if self.video_paused:
            pygame.mixer.music.pause()  # Pause le son
            # Mettre à jour le texte du bouton ici, exemple :
            self.interface_generale.bouton_pause_lecture.configure(text="Reprendre")
        else:
            pygame.mixer.music.unpause()  # Reprend le son
            self.interface_generale.fenetre.after(0, self.afficher_video)  # Reprend la lecture vidéo immédiatement
            # Mettre à jour le texte du bouton ici, exemple :
            self.interface_generale.bouton_pause_lecture.configure(text="Pause")



    def mettre_a_jour_progression_son(self):
        if self.interface_generale.cap.isOpened():
            # Synchroniser la position de lecture du son avec celle de la vidéo
            position_video = self.current_frame_time / 1000.0  # Convertir en secondes
            pygame.mixer.music.set_pos(position_video)
    def manual_update_progress(self, value):
        frame_number = int(value)
        123
        self.interface_generale.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        self.sound.set_pos(self.interface_generale.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)
        self.afficher_video()

    def avance_progress(self):
        if self.interface_generale.cap.isOpened():
            fps = self.interface_generale.cap.get(cv2.CAP_PROP_FPS)  # Obtenez les FPS de la vidéo
            current_frame = self.interface_generale.cap.get(cv2.CAP_PROP_POS_FRAMES)  # Obtenez le numéro de frame actuel
            # Calculez le nouveau numéro de frame en avançant de 2 secondes
            new_frame = current_frame + fps * 2  
            # Mettez à jour la position de la vidéo
            self.interface_generale.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
            
            # Calculez la nouvelle position de la piste audio en secondes
            new_time = new_frame / fps
            # Ajustez la position de la piste audio
            pygame.mixer.music.play(0, new_time)
            self.afficher_video()  # Mettez à jour l'affichage vidéo

    def recule_progress(self):
        if self.interface_generale.cap.isOpened():
            fps = self.interface_generale.cap.get(cv2.CAP_PROP_FPS)  # Obtenez les FPS de la vidéo
            current_frame = self.interface_generale.cap.get(cv2.CAP_PROP_POS_FRAMES)  # Obtenez le numéro de frame actuel
            # Calculez le nouveau numéro de frame en reculant de 2 secondes
            new_frame = max(0, current_frame - fps * 2)  # S'assure que le nouveau frame n'est pas négatif
            # Mettez à jour la position de la vidéo
            self.interface_generale.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
            
            # Calculez la nouvelle position de la piste audio en secondes
            new_time = new_frame / fps
            # Ajustez la position de la piste audio
            pygame.mixer.music.play(0, new_time)
            self.afficher_video()  # Mettez à jour l'affichage vidéo


    def format_duree(self, seconds):
        return str(datetime.timedelta(seconds=seconds))

    def charger_son_video(self, file_path):
        # Assurez-vous que le son précédent est arrêté et supprimé
        if self.sound:
            self.sound.stop()

        # Extraction et chargement du son de la vidéo
        clip = VideoFileClip(file_path)
        clip.audio.write_audiofile("temp_audio.wav")
        self.sound = pygame.mixer.Sound("temp_audio.wav")
        clip.close()  # Libérer les ressources


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

        self.ajouter_plus_rouge(self.interface_generale.canvas, x, y, taille_plus)
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
