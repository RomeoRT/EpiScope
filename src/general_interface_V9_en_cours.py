"""
interface générale Episcope contenant :
    lecteur vidéo :
    - lecture video
    - boutons play/pause, skip>>, skip<<, revoir
    - avance et recule de 1s et mets en pause 
    - son synchronisé
    - bonne vitesse

    annotations :
    - pré-charger des symptomes
    - les menus en cascade a gauche
    - initialisation correcte des symptomes
    - recuperer les symptomes dans une liste
    - recuperer les temps de debut et de fin
    - afficher les symptomes a droite
    - symptomes scrollables
    - pop-up pour modifier les symptomes 

    fichiers :
    - générer la frise
    - generer un rapport
    - générer un fichiers de s ymptomes

modification design general et boutons de menus deroulants et de gestion avancement video gestion 
tout est en anglais
La document des fonctions est faite
version : 0.9
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

from moviepy.editor import VideoFileClip
import pygame
from pygame.time import Clock
from tkinter import Menu
import functools #pour update right panel
import pandas as pd
from collections import defaultdict


"""
# import pas git
from fonctions_frise import afficher_frise
import save as sauvg
from class_symptome import Symptome
from pop_up import SymptomeEditor
"""
# import git
from frise.fonctions_frise import afficher_frise
import frise.save as sauvg

from annotation.class_symptome import Symptome
from annotation.pop_up import SymptomeEditor
import annotation.load_symptomes as load


class Menu_symptomes(ctk.CTkFrame):
    """
        Classe permettant d'instancier les menus déroulants rassemblant les symptomes dans une frame qui se situe sur la gauche de l'interface

        Attributes: 
            master (any):  
            interface generale (InterfaceGenerale): 
            couleur (str): couleur du fond
            bordure (int):
            largeur (int):
    """        
    def __init__(self, master, interface_generale, couleur, bordure, largeur):
        super().__init__(master, fg_color=couleur, corner_radius=0, border_width=bordure, width=largeur)
        
        
        
        self.interface_generale = interface_generale
        # Chemin vers le nouveau fichier Excel
        self.file_path = 'ictal_symptoms_zeft.xlsx'  # Assurez-vous que ce chemin est correct
        # Charger les données depuis le fichier Excel
        self.data = pd.read_excel(self.file_path)

        # Structure pour organiser les données pour l'interface graphique
        self.symptoms_structure = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    def organiser_fichier_excel(self):
                # Organiser les données
        for _, row in self.data.iterrows():
            typology = row['Typologie'] if pd.notnull(row['Typologie']) else ''
            designation = row['Designation'] if pd.notnull(row['Designation']) else ''
            description = row['Description'] if pd.notnull(row['Description']) else ''
            topographies = str(row['Topography']).split(';') if pd.notnull(row['Topography']) else []
            lateralizations = str(row['Lateralized']).split(',') if pd.notnull(row['Lateralized']) else []

            if not description and not topographies and lateralizations:
                # If there's no description and no topographies, but there are lateralizations
                self.symptoms_structure[typology][designation][''] = [('', lateralizations)]
            elif not description and not topographies and not lateralizations:
                # If there's no additional information, store a flag to indicate this
                self.symptoms_structure[typology][designation] = None
            elif not description and topographies and lateralizations:
                # Handle the case where there is topography and lateralization but no description
                for topo in topographies:
                    self.symptoms_structure[typology][designation][topo].append(('', lateralizations))

            else:
                # Otherwise, store the detailed information
                for topo in topographies or ['']:  # Ensure at least an empty string if no topology
                    self.symptoms_structure[typology][designation][description].append((topo, lateralizations))

        # Function to add elements to the menu
    def add_submenus(menu, data):
        for desc, topo_lats in data.items():
            if topo_lats is not None:  # Check if there is additional information
                if desc == '':  # Si la description est vide, attacher directement les sous-éléments
                    for topo, lats in topo_lats:
                        if topo:  # S'il y a une topographie, l'ajouter comme un menu en cascade
                            topo_menu = Menu(menu, tearoff=0)
                            for lat in lats:
                                topo_menu.add_command(label=lat)
                            menu.add_cascade(label=topo, menu=topo_menu)
                        else:  # S'il n'y a pas de topographie, attacher directement les latéralisations
                            for lat in lats:
                                menu.add_command(label=lat)
                else:  # Si la description n'est pas vide, suivre la procédure normale
                    desc_menu = Menu(menu, tearoff=0)
                    for topo, lats in topo_lats:
                        topo_menu = Menu(desc_menu, tearoff=0)
                        for lat in lats:
                            topo_menu.add_command(label=lat)
                        if topo:
                            desc_menu.add_cascade(label=topo, menu=topo_menu)
                        else:
                            for lat in lats:
                                desc_menu.add_command(label=lat)
                    if desc_menu.index('end') is not None:
                        menu.add_cascade(label=desc if desc else 'General', menu=desc_menu)
                    elif desc:
                        menu.add_command(label=desc)
            else:
                # Add the designation as a command if there are no additional details
                menu.add_command(label=desc)
    def build_menu_cascade(self):
                # Build the cascading menu
        for typology, designations in self.symptoms_structure.items():
            typology_menu = Menu(self.main_menu, tearoff=0)
            for designation, descriptions in designations.items():
                if descriptions is not None:  # Check if there are descriptions or it's a flag indicating no additional info
                    designation_menu = Menu(typology_menu, tearoff=0)
                    self.add_submenus(designation_menu, descriptions)
                    if designation_menu.index('end') is not None:
                        typology_menu.add_cascade(label=designation, menu=designation_menu)
                    else:
                        typology_menu.add_command(label=designation)
                else:
                    # Directly add the designation as a command if no additional info
                    typology_menu.add_command(label=designation)
            if typology_menu.index('end') is not None:
                self.main_menu.add_cascade(label=typology, menu=typology_menu)

    def create_dropdown_menus(self,master,largeur):
        """
        Crée un menu déroulants contenant les différents symptomes classés selon s'ils sont objectifs ou subjectifs.

        Args:
            master(fenetre): fenetre dans laquelle on veut afficher le sous menu déroulant
        """
        my_font = tkFont.Font(size=12)    
        # Création du Menubutton
        menubutton_objective = tk.Menubutton(self, text="Objective/Motor Symptoms", width=largeur//9, direction='flush', relief="flat", font=my_font)
        menubutton_objective.pack(side='top', padx=5, pady=20, expand=False)
        # Création du Menubutton
        menubutton_subjective = tk.Menubutton(self, text="Subjective Symptoms", width=largeur//9, relief="flat", font=my_font)
        menubutton_subjective.pack(side='top', padx=5, pady=10, expand=False)
        

        # Création du menu principal
        menu_objective = tk.Menu(menubutton_objective, tearoff=0, font=my_font)
        menubutton_objective.config(menu=menu_objective)

        menu_subjective = tk.Menu(menubutton_subjective, tearoff=0, font=my_font)
        menubutton_subjective.config(menu=menu_subjective)

        # Ajoute les sous-menus avec les symptômes et sous-symptômes
                # Ajoute les sous-menus avec les symptômes et sous-symptômes
        for symptom, sub_symptoms in self.symptoms:
            self.create_submenu(menu_objective, symptom, sub_symptoms, my_font, self.on_select_obj)

        for symptom2, sub_symptoms2 in self.symptoms2:
            self.create_submenu(menu_subjective, symptom2, sub_symptoms2, my_font, self.on_select_subj)

    def create_submenu(self, parent_menu, symptom, sub_symptoms, my_font, on_select):
        """
        Crée les sous menus déroulants après avoir sélectionné un symptome.
        Les éléments de ce menu precisent la localisation du symptome sur le corps et la latéralité.

        Args:
            parent_menu (Menu): Menu déroulant lié au symptome sélectionné
            symptom (symptome): Symptome sélectionné
            sub_symptoms (list): liste complémantaire au symptôme sélectionné (indique la position/latéralisation)
            my_font (Font): indique la taille de la police d'écriture
            on_select (function): commande de selection des symptomes
        """
        #my_font = tkFont.Font(size=15)
        symptom_menu = tk.Menu(parent_menu, tearoff=0, font=my_font)
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
                    sub_menu.add_command(label=sub_sub_symptom.strip(), command=lambda path=full_path: on_select(path))
                symptom_menu.add_cascade(label=main_part, menu=sub_menu)
            else:
                full_path = f"{symptom} > {main_part}"
                symptom_menu.add_command(label=main_part, command=lambda path=full_path: on_select(path))

        if has_sub_items:
            parent_menu.add_cascade(label=symptom, menu=symptom_menu)
        else:
            full_path = symptom
            parent_menu.add_command(label=symptom, command=lambda path=full_path: on_select(path))

    def read_symptoms_from_file(self, file_name):
        """
        Lit les fichiers textes contenant la liste des symptomes pour remplir les menus

        Les symptomes doivent etre ecrits avec des séparateurs spécifiques 
        *example :  Negative myoclonus[Oriented(Left;Right;Bilateral);Hand/Superior limb;Foot/Inferior limb]* 

        Args:
            file_name (string): chemin du fichier

        Returns:
            title (string): titre du menu
            symptoms (list): liste contenant les symptomes pour remplir les menus 
        """
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
    
    def on_select_obj(self, selection):
        """
        Récupère des données lié à la video pour obtenir le temps actuel

        Args:
            selection (path): Symptome sélectionné 
        """
        current_video_time = self.interface_generale.get_current_video_time() 
        #display_text = f"{selection} - TD: {current_video_time}\n" # Ajoutez le temps actuel ici

        buffer_attributs = selection.split(">")

        attributs = ["","","","","","","","",""]
        match len(buffer_attributs):
            case 0:
                pass
            case 1:
                attributs[1]=buffer_attributs[0]

            case 2:
                attributs[1], attributs[3] = buffer_attributs[0],buffer_attributs[-1]
            
            case 3:
                attributs[1], attributs[3], attributs[2] = buffer_attributs[0], buffer_attributs[1], buffer_attributs[2]
            
            case _ :
                attributs[1], attributs[3], attributs[2] = buffer_attributs[0], buffer_attributs[1], buffer_attributs[-1]
                attributs[5] = f"{buffer_attributs[2:-2]}"

        attributs[6] = current_video_time
        self.interface_generale.update_right_panel(attributs)

    def on_select_subj(self, selection):
        """
        Récupère des données lié à la video pour obtenir le temps actuel

        Args:
            selection (path): Symptome sélectionné 
        """
        # Appel à une nouvelle fonction dans InterfaceGenerale pour obtenir le temps actuel de la vidéo
        current_video_time = self.interface_generale.get_current_video_time() 
        #display_text = f"{selection} - TD: {current_video_time}\n" # Ajoutez le temps actuel ici

        attributs = ["","","","","","","","",""]
        attributs[1]  = selection
        attributs[6] = current_video_time
        self.interface_generale.update_right_panel(attributs)


class FriseSymptomes:
    """
    Classe permettant de généré une frise chronologique récapitulant l'ensemble des symptomes présent lors de la crise épileptique

    Attributes: 
        interfaceGenerale (InterfaceGenerale): 
        MenuDeroulant (Menu_symptomes):
    """
    def __init__(self,InterfaceGenerale,MenuDeroulant):
        self.menu_deroulant=MenuDeroulant
        self.interface_generale=InterfaceGenerale
        

    def afficher(self):
        """
        Récuperation de la liste de symptomes instanciée dans class interface generale fonction update right panel
        """
        Lsymp = self.interface_generale.ListeSymptomes
        newL=[]

        for symp in Lsymp:
            nom = symp.get_Name()
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

            id = symp.get_ID()
            lat = symp.get_Lateralization()
            segcor = symp.get_Topography()
            orient = symp.get_Orientation()
            attsup = symp.get_AttributSuppl()
            comm = symp.get_Comment()
            newL.append([nom, debut, fin, id, lat, segcor, orient, attsup, comm, tdeb_str, tfin_str])

        newL = sorted(newL, key=lambda x: float(x[1]))
        afficher_frise(newL)


class InterfaceGenerale():
    """
    Classe interface Générale qui donne le visuel global de l'interface graphique. 
    
    Elle est représenter sous forme de fenetre et permet aux autres classes de s'intégrer dedans.
    Elle appel la classe Lecteur_video, FriseSymptomes et Menu_symptomes 

    Atributes:
        ListeSymptomes (list): liste des symptomes s'actualisant au fur et a mesure

        **A completer !!!**

    """
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Episcope")
        self.cap = None
        self.lec_video=LecteurVideo(self)
        self.frise=FriseSymptomes(self,self)
        self.lec_video.video_paused = False


        self.set_end_time_mode = False
        self.current_symptom = ""

        # Liste symptomes vide
        self.ListeSymptomes = []

        # self.theme couleurs
        # L= = [text, frames, frame menu, menu, bouton revoir, bouton pause, boutons <<>>, boutons frise/texte  ]
        self.theme = ['black', 'gray97', 'whitesmoke', 'lightsteelblue1', 'navajo white', 'gray60', 'gray80', 'cornflowerblue']

        #####################################
        ###     barre de menus
        #####################################

        police_label_m = tkFont.Font(size=12)

        # Menu 
        menu_bar = Menu(self.fenetre)
        menu_open = Menu(menu_bar, tearoff=0)
        menu_open.add_command(label="Open Video", command=self.ouvrir_video)
        menu_open.add_command(label="Launch Without Video", command=self.ouvrir_video_noire)
        menu_open.add_separator()
        menu_open.add_command(label ="Open Symptoms", command=self.load_symptoms)
        menu_bar.add_cascade(label="Open", menu=menu_open)

        menu_save = Menu(menu_bar, tearoff=0)
        menu_save.add_command(label="Save Symptoms", command=self.sauvegarde)
        menu_save.add_command(label="Save Report", command=self.rapport)
        menu_save.add_command(label="Save Timeline", command=self.frise.afficher)
        menu_bar.add_cascade(label="Save", menu=menu_save)

        menu_bar.config(bg=self.theme[3],fg=self.theme[3], font=police_label_m)
        menu_save.config(font=police_label_m)
        menu_open.config(font=police_label_m)
    
        root.config(menu=menu_bar)

        # Variable pour stocker les coordonnées du clic
        self.clic_x = 0
        self.clic_y = 0
        

        # Cadres pour la partie de gauche, milieu et droite
        # Modify the frame initialization in the __init__ method of LecteurVideo class
        self.frame_left = Menu_symptomes(fenetre, self, self.theme[1], 0, ((fenetre.winfo_screenwidth()) // 5))
        self.frame_middle = ctk.CTkFrame(fenetre, fg_color=self.theme[1],corner_radius=0,border_width=0 ,width=3 * (fenetre.winfo_screenwidth()) // 5, height=fenetre.winfo_screenheight()  )  # Ajustement ici
        self.frame_right = ctk.CTkFrame(fenetre, fg_color=self.theme[1],corner_radius=0,border_width=0 ,width=fenetre.winfo_screenwidth() // 5)


        # Placer les cadres dans la fenêtre
        self.frame_left.pack(side=ctk.LEFT, fill=ctk.Y)
        self.frame_middle.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        self.frame_right.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)

        self.scrollable1 = ctk.CTkScrollableFrame(self.frame_right, border_width=0, height=400, fg_color=self.theme[1], width=(fenetre.winfo_screenwidth() // 5), orientation='vertical')
        self.text_output = ctk.CTkScrollableFrame(self.scrollable1, border_width=0, height=400, fg_color=self.theme[1], width=(fenetre.winfo_screenwidth() // 5), orientation='horizontal')
        self.scrollable1.pack(side=ctk.TOP,padx=20,pady=20)
        self.text_output.pack()

        #self.frame_right.grid_rowconfigure(0, weight=1)  # Donne un poids à la ligne où se trouve la zone de texte
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_rowconfigure(1, weight=1)  # Donne un poids à la ligne où se trouve le bouton
        self.frame_right.grid_columnconfigure(0, weight=1)  # Assure que la colonne s'étend correctement
        # Frame pour les boutons
        self.frame_CTkButton = ctk.CTkFrame(self.frame_middle, fg_color=self.theme[1], height=50)
        self.frame_CTkButton.pack(side=ctk.BOTTOM, fill=ctk.BOTH)
        
        #####################################################
        ####################### Boutons
        #####################################################

        self.bouton_revoir = ctk.CTkButton(self.frame_CTkButton, text="Rewatch", command=self.lec_video.revoir_video, width=100, text_color=self.theme[0], fg_color=self.theme[4])
        self.bouton_revoir.pack(side=ctk.LEFT, padx=100, pady=10)

        self.bouton_reculer = ctk.CTkButton(self.frame_CTkButton, text="<<", command=self.lec_video.recule_progress, width=50, text_color=self.theme[0],fg_color=self.theme[6])
        self.bouton_reculer.pack(side=ctk.LEFT, padx=5, pady=10)

        self.bouton_play_pause = ctk.CTkButton(self.frame_CTkButton, text="Pause", command=self.lec_video.pause_lecture,text_color=self.theme[0],fg_color=self.theme[5])
        self.bouton_play_pause.pack(side=ctk.LEFT, padx=5, pady=10)

        self.bouton_avancer = ctk.CTkButton(self.frame_CTkButton, text=">>", command=self.lec_video.avance_progress, width=50, text_color=self.theme[0],fg_color=self.theme[6])
        self.bouton_avancer.pack(side=ctk.LEFT, padx=5, pady=10)

        self.bouton_nul = ctk.CTkButton(self.frame_CTkButton, text="", width=100, fg_color=self.theme[1], hover_color=self.theme[1])
        self.bouton_nul.pack(side=ctk.LEFT, padx=100, pady=10)
        self.bouton_nul.configure(state="disabled")       

        self.frame_frise = ctk.CTkFrame(self.fenetre, fg_color=self.theme[1], border_width=5)  # Vous pouvez ajuster la couleur et les autres paramètres selon vos préférences
        self.frame_frise.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)  # Changez `side=ctk.LEFT` en fonction de l'endroit où vous souhaitez placer le cadre


        # Bouton pour activer la frise chronologique des symptomes:
        self.bouton_frise = ctk.CTkButton(self.frame_right, text="Timeline", command=self.frise.afficher, text_color=self.theme[0], fg_color=self.theme[7])
        self.bouton_frise.pack(side=ctk.BOTTOM,padx=20,pady=20)
        
        # gros bouton save (primitif)
        self.bouton_save = ctk.CTkButton(self.frame_right, text="Report", command=self.rapport, text_color=self.theme[0], fg_color=self.theme[7])
        self.bouton_save.pack(side=ctk.BOTTOM,padx=20,pady=20)
    
        # Étiquettes pour afficher le temps écoulé et la durée totale
        self.label_temps = tk.Label(self.frame_middle, text="Elapsed Time: 0:00 / Total Time: 0:00", bg=self.theme[1], fg=self.theme[0])
        self.label_temps.pack(side=tk.BOTTOM, padx=20)

        total_duration = self.get_video_duration()
        # Barre de progression manuelle
        self.progress_slider =tk.Scale(self.frame_middle, from_=0, to=total_duration, command=self.lec_video.manual_update_progress, orient="horizontal", bg=self.theme[1])
        self.progress_slider.pack(side=tk.BOTTOM, fill=tk.X)

        # Lire la vidéo avec OpenCV
        self.cap = None

        # Créer un Canvas pour afficher la vidéo
        self.canvas = ctk.CTkCanvas(self.frame_middle, bg='black')
        self.canvas.pack(expand=True, fill=ctk.BOTH)

        # Binding du clic gauche à l'affichage du menu
        self.canvas.bind("<Button-1>", self.lec_video.afficher_menu_annotations)

        self.fenetre.bind('<space>', lambda event: self.lec_video.pause_lecture())
        self.fenetre.bind('<Right>', lambda event: self.lec_video.avance_progress())
        self.fenetre.bind('<Left>', lambda event: self.lec_video.recule_progress())
        self.canvas.bind("<Button-1>", self.lec_video.afficher_menu_annotations)

        # Créer une zone de texte pour les commentaires:
        self.zone_text = tk.Text(self.frame_right, height=20, width=fenetre.winfo_screenwidth() // 5, relief=tk.GROOVE, wrap=tk.WORD)
        self.zone_text.pack(side=tk.BOTTOM, pady=20,padx=20)

    def update_right_panel(self, attributs=[], is_start_time=False):
        """
        Permet de gerer l'affichage dans la partie de droite du temps de début/fin des symptomes et gestion du pop-up pour modifier un symptome.

        Args:
            attributs (list): liste d'initialisation du symptome | defaut = [] 
        """
        def set_end_time(event, Symp):
            """
            Ajoute le temps de fin à un symptôme existant
            
            Args:
                event (None): correspond à l'appuie sur la zone ou s'affiche le symptome
            """
            #current_text = event.widget.cget("text")
            if Symp.Tfin=="": # On vérifie si le temps de fin est déjà présent pour ne pas l'ajouter plusieurs fois
                Symp.set_Tfin(f"{self.get_current_video_time()}")
                
                if Symp.Tdeb != "":  # Assurez-vous qu'il y a bien un temps de début pour insérer le temps de fin
                    new_text = self.text_sympt(Symp)
                    event.widget.config(text=new_text)  # Met à jour le texte du label avec le temps de fin
                    open_editor_partial = functools.partial(open_editor_on_click, Symp=Symp)
                    symptom_label.bind('<Button-1>', open_editor_partial) # Lier le button1 au popup après Tfin
                else:
                    open_editor_partial = functools.partial(open_editor_on_click, Symp=Symp)
                    symptom_label.bind('<Button-1>', open_editor_partial) # Lier le button1 au popup après Tfin
                    open_editor_on_click(event, Symp)
            else :
                open_editor_partial = functools.partial(open_editor_on_click, Symp=Symp)
                symptom_label.bind('<Button-1>', open_editor_partial) # Lier le button1 au popup après Tfin
                open_editor_on_click(event, Symp)
        
        def open_editor_on_click(event, Symp):
            """
            Ouvre la fenêtre de modification d'un symptôme

            Args:
                event (None): correspond à l'appuie sur la fenetre pour modifier le symptome
            """
            if event.widget.cget("text"):
                # Instancier la fenêtre de modification TopLevel
                editor_window = SymptomeEditor(Symp)
                # Afficher la fenêtre de modification
                editor_window.transient(event.widget.master)  # Définissez la fenêtre de modification comme une fenêtre enfant de l'interface principale
                editor_window.grab_set()  # Empêche l'interaction avec l'interface principale jusqu'à ce que la fenêtre de modification soit fermée
                editor_window.focus_set()  # Définissez le focus sur la fenêtre de modification
                editor_window.wait_window()  # Attendre jusqu'à ce que la fenêtre de modification soit fermée avant de reprendre l'exécution

                #deb=Symp.get_Tdeb()
                #splitdeb=deb.rstrip("\n")
                new_text = self.text_sympt(Symp)
                event.widget.config(text=new_text)  # Met à jour le texte du label avec le temps de fin

        #self.text_output.config(state=tk.NORMAL)  # Activez l'état normal pour permettre la mise à jour

        ## initialisation du symptome
        if attributs == []:
            Symp = Symptome(ID="", Name="", Lateralization="", Topography="", Orientation="", AttributSuppl="", Tdeb="", Tfin="", Comment="")
        else:
            Symp = Symptome(attributs[0], attributs[1], attributs[2], attributs[3], attributs[4], attributs[5], attributs[6], attributs[7], attributs[8])
            
        #splited = text.split(" - ")
        #Symp.set_Name(splited[0])
        #Symp.set_Tdeb(splited[1][4:])
        #symptom_with_time = f"{Symp.get_Name()} - Starting Time: {Symp.get_Tdeb()}        SET END TIME"
        symptom_with_time = self.text_sympt(Symp)

        container = tk.Frame(self.text_output)  # Créer un conteneur pour le label et le bouton
        container.pack(side=tk.TOP, fill=tk.X)

        symptom_label = tk.Label(container, text=symptom_with_time, bg="gray89", fg=self.theme[0])
        # Changement de la taille de la police
        symptom_label.config(font=("Arial",12))
        symptom_label.pack(side=tk.LEFT)

        delete_button = ctk.CTkButton(container, text="X", command=lambda symp=Symp, cont=container: self.supprimer(symp, cont), text_color='white', fg_color='FireBrick', width=len('X')*15)
        delete_button.pack(side=ctk.LEFT,padx=10,pady=10)

        # Associe l'événement de clic pour ajouter le temps de fin
        set_end_time_partial = functools.partial(set_end_time, Symp=Symp)
        symptom_label.bind('<Button-1>', set_end_time_partial)

        #self.text_output.insert(tk.END, '\n')  # Nouvelle ligne après chaque symptôme
        #self.text_output.config(state=tk.DISABLED)  # Désactive l'édition de la zone de texte après la mise à jour

        self.ListeSymptomes.append(Symp)

    def supprimer(self, selection, container):
        for symp in self.ListeSymptomes:
            if symp.get_Name() == selection.get_Name():
                self.ListeSymptomes.remove(symp)
                container.destroy()  # Supprime le conteneur entier, y compris le label et le bouton
                break       


    def get_current_video_time(self):
        """
        Permet d'avoir le temps actuel de la vidéo
        """
        if self.cap is not None and self.cap.isOpened():
            current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            current_time_seconds = int(current_frame / fps)
            current_time_formatted = self.lec_video.format_duree(current_time_seconds)
            return current_time_formatted
        return "00:00:00"  # Retournez une valeur par défaut si la vidéo n'est pas ouverte


    def get_video_duration(self):
        """
        Permet d'avoir le temps total de la vidéo
        """
        if self.cap is not None and self.cap.isOpened():
            total_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            return int(total_frames / fps)


    def ouvrir_video(self):
        """
        Ouvre la vidéo en appelant la class Lecteur_video
        """
        self.lec_video.ouvrir_video()
    

    def ouvrir_video_noire(self):
        """
        Ouvre la vidéo noire en appelant la class Lecteur_video
        """
        self.lec_video.ouvrir_video_noire()

    
    def lire_fichier(self,nom_fichier):
        """
        Ouvre un fichier texte le lit et sauvegarde les informations dans une liste
        """
        try:
            # Ouvre le fichier en mode lecture
            with open(nom_fichier, 'r') as fichier:
                # Lit toutes les lignes du fichier et les stocke dans une liste
                lignes = fichier.read().splitlines()
                return lignes
        except FileNotFoundError:
            print(f"File not found : {nom_fichier}")
            return 


    def sauvegarde(self):
        """
        sauvegarde de la liste de symtptomes dans un fichier texte
        fait appel a la classe save 
        """
        save = sauvg.save(self.ListeSymptomes)
        save.save()
    

    def rapport(self):
        """
        ecrit le rapport de la crise
        """
        save = sauvg.save(self.ListeSymptomes)
        save.write_report()


    def text_sympt(self, sympt):
        """
        crée le texta a afficher dans le right_pannel

        Args:
            sympt (Symptome): symptome dont on crée le texte

        Returns:
            text (string): texte a afficher contenant les bonnes infos
        """
        time = ""

        if sympt.get_Tfin()!="":
            time = f" - Start : {sympt.get_Tdeb()}  -  End :  {sympt.get_Tfin()}"
        else :
            time = f" - Start : {sympt.get_Tdeb()} \n SET END TIME"

        if sympt.get_Lateralization() != "" and sympt.get_Topography()!="":
            return f"{sympt.get_Name()} > {sympt.get_Lateralization()} > {sympt.get_Topography()} " + time
        
        elif sympt.get_Lateralization() != "" and sympt.get_Topography()=="":
            return f"{sympt.get_Name()} > {sympt.get_Lateralization()} " + time
        
        elif ((sympt.get_Lateralization() == "") and (sympt.get_Topography()!="")):
            return f"{sympt.get_Name()} > {sympt.get_Topography()}" + time
        
        else :
            return f"{sympt.get_Name()}" + time
  
    
    def load_symptoms(self):
      """
      charge une liste de symptomes a partir d'un fichier
      """  
      file_path = filedialog.askopenfilename(filetypes=[("Fichiers textes", "*.txt")])
      list_S = load.read_symptoms(file_path)
      for s in list_S:
          text = self.text_sympt(s)
          attr = s.get_attributs()
          self.update_right_panel(attr)
     


class LecteurVideo():

    """
    Classe du lecteur video qui gére les differentes fonctionnalités de la video.

    fonctionnalités : ouverture de la vidéo, de la vidéo noire,l'affichage de la vidéo,la synchroisation du son et la gestion des boutons
    Elle appelle la classe InterfaceGenerale 

    Attributes:
        **A completer**
    """
    def __init__(self, InterfaceGenerale):
        """
        Constructeur de la class Lecteur_video
        """

        self.interface_generale = InterfaceGenerale
        pygame.mixer.init()
        self.video_paused = False
        self.current_frame_time = 0
        self.clock = Clock()  # Initialisez l'horloge pygame
        self.vitesse_lecture = 2
        self.valeur=-1
        self.temps_ecoule=0
        self.duree_totale=0


    def ouvrir_video(self):
        """
        Ouvre une vidéo depuis l'explorateur du fichier
        une fois choisie, elle se met en lecture dans middle_frame
        """
        # Sélection du fichier vidéo et préparation de la vidéo et du son
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers vidéo", "*.mp4 *.avi *mpg")])
        if file_path:
            self.interface_generale.cap = cv2.VideoCapture(file_path)
            if not self.interface_generale.cap.isOpened():
                print("Error: Impossible to open.")
                return
            self.preparer_son_video(file_path)
            self.avancer()
            self.configurer_barre_progression()
            self.afficher_video()
            self.mettre_a_jour_temps_video()  # Démarre la mise à jour de la progression et du temps.


    def ouvrir_video_noire(self):
        """
        Ouvre la vidéo noire directement qui doit étre dans le meme dossier que le code
        """
        # Chemin du fichier vidéo "ma vidéo noire" dans le dossier courant
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "video_noire.mp4")
        print("Video file path:", file_path)

        if os.path.exists(file_path):
            self.interface_generale.cap = cv2.VideoCapture(file_path)

            largeur = int(self.interface_generale.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            hauteur = int(self.interface_generale.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Mettre à jour la taille du canevas pour correspondre à la partie du milieu
            largeur_partie_milieu = self.interface_generale.frame_middle.winfo_reqwidth()
            hauteur_partie_milieu = self.interface_generale.frame_middle.winfo_reqheight()
            hauteur_canevas = (largeur_partie_milieu / largeur) * hauteur

            self.interface_generale.canvas.configure(width=largeur_partie_milieu, height=hauteur_canevas)

            #self.interface_generale.progress_slider.configure(to=self.interface_generale.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.configurer_barre_progression()
            self.afficher_video()
            self.mettre_a_jour_temps_video()
            self.interface_generale.bouton_play_pause.configure(state=ctk.NORMAL)
        else:
            print("'Black Video' not found in the current folder.")


    def preparer_son_video(self, file_path):
        """
        Prépare le son de la vidéo à partir de la vidéo originale.
        """
        
        clip = VideoFileClip(file_path)# Convertir la piste audio de la vidéo en fichier WAV
        audio_path = "temp_audio.wav"  # Définissez le chemin de fichier pour l'audio temporaire
        clip.audio.write_audiofile(audio_path)
        clip.close()  # Fermez le clip pour libérer les ressources

        # Utilisez pygame.mixer.music pour charger et jouer la piste audio
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play(-1)  # Jouez en boucle


    def afficher_video(self):
        """
        permet l'affichage et la lecture de la video:
        redimensionnement des frames de la video pour correspondre les dimensions de middle frame
        Calcule et affiche le temps totale et le temps écoulé
        """
        
        if self.interface_generale.cap.isOpened():# Vérifie si la vidéo est ouverte
            ret, frame = self.interface_generale.cap.read()  # Lit la prochaine frame de la vidéo
            if ret:
                # Convertir BGR en RGB puisque OpenCV utilise BGR par défaut
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Ajuster la taille de la frame pour qu'elle corresponde à la taille du canevas
                largeur_canevas = self.interface_generale.canvas.winfo_width()
                hauteur_canevas = self.interface_generale.canvas.winfo_height()
                frame = cv2.resize(frame, (largeur_canevas, hauteur_canevas))

                # Convertir l'image CV2 en image Tkinter pour l'affichage
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame))

                # Afficher l'image dans le canevas
                self.interface_generale.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                # Garde une référence de l'image pour éviter le ramasse-miettes
                self.interface_generale.canvas.image = photo

                # Mise à jour du temps écoulé et du temps total de la vidéo
                frame_number = self.interface_generale.cap.get(cv2.CAP_PROP_POS_FRAMES)
                fps = self.interface_generale.cap.get(cv2.CAP_PROP_FPS)
                total_frames = self.interface_generale.cap.get(cv2.CAP_PROP_FRAME_COUNT)

                self.temps_ecoule = int(frame_number / fps)
                self.duree_totale = int(total_frames / fps)
                self.interface_generale.label_temps.config(text=f"Elapsed Time: {self.format_duree(self.temps_ecoule)} / Total Time: {self.format_duree(self.duree_totale)}")

                # Continuez la lecture si la vidéo n'est pas en pause
                if not self.video_paused:
                    # Ajustez le délai pour la vitesse de lecture (vitesse normale = 1.0)
                    self.interface_generale.canvas.after(int(1000 / fps / self.vitesse_lecture), self.afficher_video)
                

    def mettre_a_jour_frame_video(self, frame):
        """
        permet de s'assurer que chaque frame de la vidéo est correctement traitée,
        redimensionnée et affichée dans l'interface utilisateur
        """
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.interface_generale.canvas.create_image(0, 0, image=frame, anchor=tk.NW)
        self.interface_generale.canvas.image = frame


    def mettre_a_jour_temps_video(self):
        """
            Assure que le temps de la vidéo affichée est régulièrement mis à jour et que la lecture de la vidéo continue 
            de manière fluide. Elle assure la sychronisation de  l'avancement de la vidéo avec le temps réel
        """
        if self.interface_generale.cap.isOpened() and not self.video_paused:
            temps_actuel_ms = self.interface_generale.cap.get(cv2.CAP_PROP_POS_MSEC)
            temps_actuel = int(temps_actuel_ms / 1000)  # Convertis en secondes
            self.interface_generale.progress_slider.set(temps_actuel)  # Mise à jour de la position du curseur de la barre de progression
            
            # Mise à jour de l'affichage du temps écoulé (facultatif, si tu veux aussi mettre à jour le label du temps)
            duree_totale = self.interface_generale.get_video_duration()  # Assure-toi que cette méthode retourne la durée totale en secondes
            self.interface_generale.label_temps.config(text=f"Elapsed Time: {self.format_duree(temps_actuel)} / Total Time: {self.format_duree(duree_totale)}")
            
            # Planifiez la prochaine mise à jour
            self.interface_generale.fenetre.after(500, self.mettre_a_jour_temps_video)


    def pause_lecture(self):
        """
        Cette fonction gère l'état de pause et reprise de la vidéo 
        """
        self.video_paused = not self.video_paused
        if self.video_paused:
            pygame.mixer.music.pause()  # Pause le son
            # Mettre à jour le texte du bouton ici, exemple :
            self.interface_generale.bouton_play_pause.configure(text="Play")
        else:
            pygame.mixer.music.unpause()  # Reprend le son
            self.interface_generale.fenetre.after(0, self.afficher_video)  # Reprend la lecture vidéo immédiatement
            # Mettre à jour le texte du bouton ici, exemple :
            self.interface_generale.bouton_play_pause.configure(text="Pause")
            self.mettre_a_jour_temps_video()  # Démarre la mise à jour de la progression et du temps.


    def avancer(self):
        self.interface_generale.progress_slider.set(self.temps_ecoule)
        self.interface_generale.fenetre.after(1, self.avancer)


    def configurer_barre_progression(self):
        total_duration = self.interface_generale.get_video_duration()
        self.interface_generale.progress_slider.config(to=total_duration)
            
            
    def manual_update_progress(self,value):
        self.temps_ecoule=float(value)
        fps = self.interface_generale.cap.get(cv2.CAP_PROP_FPS)
        frame_number=self.temps_ecoule*fps
        self.interface_generale.cap.set(cv2.CAP_PROP_POS_FRAMES,int(frame_number))
        pygame.mixer.music.play(start=self.temps_ecoule)


    def avance_progress(self):
        """
        permet d'avancer la video d'une seonde et assure l'avancement du son aussi
        """
        if self.interface_generale.cap.isOpened():
            self.video_paused = True  # Assumer que la vidéo est en pause
            self.pause_lecture()  # Pause la vidéo et l'audio

            current_frame = self.interface_generale.cap.get(cv2.CAP_PROP_POS_FRAMES)
            fps = self.interface_generale.cap.get(cv2.CAP_PROP_FPS)
            new_frame = current_frame + fps * 1  # Avance de 1 seconde
            self.interface_generale.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
           
            # Calculez la nouvelle position de la piste audio en secondes
            new_time = new_frame / fps
            # Ajustez la position de la piste audio
            pygame.mixer.music.play(0, new_time)
            self.pause_lecture()  # Reprendre la lecture de la vidéo et l'audio


    def recule_progress(self):
        """
        Permet de reculer de 1 seconde dans la video en assurant la synchronisation du son avec la video
        """
        if self.interface_generale.cap.isOpened():
            self.video_paused = True  # Assumer que la vidéo est en pause
            self.pause_lecture()  # Pause la vidéo et l'audio

            current_frame = self.interface_generale.cap.get(cv2.CAP_PROP_POS_FRAMES)
            fps = self.interface_generale.cap.get(cv2.CAP_PROP_FPS)
            new_frame = max(0, current_frame - fps * 1)  # Recule de 1 seconde
            self.interface_generale.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
            # Calculez la nouvelle position de la piste audio en secondes
            new_time = new_frame / fps
            # Ajustez la position de la piste audio
            pygame.mixer.music.play(0, new_time)
            self.pause_lecture()


    def revoir_video(self):
        """
        Permet de revoir la video depuis le début
        """
        if self.interface_generale.cap.isOpened():
        # Réinitialiser la vidéo au début
            self.interface_generale.cap.set(cv2.CAP_PROP_POS_FRAMES,0)
            # Réinitialiser l'audio au début
            pygame.mixer.music.play(0, 0.0)
            # Reprendre la lecture vidéo s'il était en pause
            if self.video_paused==False:
                self.play_pause
            if self.video_paused==True:
                self.video_paused = False
                self.interface_generale.bouton_play_pause.configure(text="Pause")
            self.afficher_video()            


    def format_duree(self, seconds):
        """
        convertir une durée en secondes en un format de temps plus lisible, 
        sous la forme de minutes et secondes.
        """
        return str(datetime.timedelta(seconds=seconds))


    def charger_son_video(self, file_path):
        """
         Arrête le son précédent, et fait l'extraction et le chargement 
         de la nouvelle piste audio associée à la vidéo sélectionnée
         Elle fait aussi le nettoyage des ressources utilisées pendant le processus. 
        """
        # Assurez-vous que le son précédent est arrêté et supprimé
        if self.sound:
            self.sound.stop()

        # Extraction et chargement du son de la vidéo
        clip = VideoFileClip(file_path)
        clip.audio.write_audiofile("temp_audio.wav")
        self.sound = pygame.mixer.Sound("temp_audio.wav")
        clip.close()  # Libérer les ressources


    def afficher_menu_annotations(self, event):
        """
        Récupére les coordonnées d'un clic sur la vidéo. Pour l'intant elle affiche une croix rouge
        Mais il ya possibilté d'utiliser cette croix roug pour afficher le symtoms en la survolant 
        par le curseur
        """
        # Coordonnées du clic
        x = event.x
        y = event.y
        # Toggle the video playback state
        self.video_paused = not self.video_paused
        if self.video_paused:
            # Pause the video and the sound
            pygame.mixer.music.pause()  # Pause the sound
            # Update the play/pause button text, if you have one
            self.interface_generale.bouton_play_pause.configure(text="Play")
        else:
            # Resume video and sound playback
            pygame.mixer.music.unpause()  # Resume the sound
            self.interface_generale.fenetre.after(0, self.afficher_video)  # Resume video playback immediately
            # Update the play/pause button text
            self.interface_generale.bouton_play_pause.configure(text="Pause")
        
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
        """
        Ajoute la croix rouge durat 1 seconde là où on appuie
        """
        # Coordonnées pour créer un '+'
        ligne_horizontale = self.interface_generale.canvas.create_line(x-taille*20, y, x+taille*20, y, fill="red", width=3)
        ligne_verticale = self.interface_generale.canvas.create_line(x, y-taille*20, x, y+taille*20, fill="red", width=3)
                
        self.interface_generale.canvas.after(1000, lambda: self.interface_generale.canvas.delete(ligne_horizontale, ligne_verticale))


if __name__ == "__main__":
    root = ctk.CTk()
    #root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))  # Plein écran
    root.after(0, lambda:root.state('zoomed'))
    lecteur = InterfaceGenerale(root)
    root.mainloop()
