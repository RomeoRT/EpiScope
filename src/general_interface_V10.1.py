"""
Episcope general interface containing 

* video player :
    * video playback
    * play/pause, skip>>, skip<<, review buttons
    * advance and rewind by 1s and pause 
    * synchronised sound
    * good speed
    * progression bar sychronised

* annotations :
    * menus based on exel file (xls)
    * pre-load symptoms
    * cascading menus on left
    * correct initialization of symptoms
    * retrieve symptoms from a list
    * retrieve start and end times
    * display symptoms on the right
    * scrollable symptoms
    * pop-up to modify symptoms 

* files :
    * generate frieze
    * generate a report
    * generate a symptom file

modification of the general design and buttons of the drop-down menus and the video progress management buttons 
everything is in english
configuration of the progress bar(state of the cursor:pressed, not pressed)
version : 0.10.1
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from tkinter import messagebox as error
import cv2
from PIL import Image, ImageTk
import datetime
import tkinter.font as tkFont
import os

import moviepy.editor as mp
from moviepy.editor import VideoFileClip
import pygame
from pygame.time import Clock
from tkinter import Menu
import functools #pour update right panel


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
import annotation.exel_menus as exel
import annotation.search_bar as search


class Menu_symptomes(ctk.CTkFrame):
    """
    Class used to instantiate drop-down menus displaying symptoms in a frame on the left of the interface.

    """        
    def __init__(self, master, interface_generale, couleur, bordure, largeur):
        """
        The constructor of the :obj:'Menu_symptomes' class.

        The files containing the symptoms must be in the same folder as the source file

        Attributes: 
            master (any): the master widget in which to display the menus
            interface generale (InterfaceGenerale): the general interface in which to display the menus
            couleur (str): background color of the frame
            bordure (int): border width of the frame
            largeur (int): width of the frame
        """
        super().__init__(master, fg_color=couleur, corner_radius=0, border_width=bordure, width=largeur)

        self.interface_generale = interface_generale
        self.file_path = 'ictal_symptoms.xlsx'  # Assurez-vous que ce chemin est correct
        self.symptoms_structure = exel.Read_excel(self.file_path)

        

        self.create_dropdown_menus(largeur)  # Crée et affiche les menus déroulants
        self.bar = search.search_symptomes(self, self.symptoms_structure, self.on_select_bar, largeur//10) 

    def create_dropdown_menus(self,largeur):
        """
        Creates a drop-down menu containing the various symptoms classified according to whether they are objective or subjective.

        Args:
            largeur (int): width of the frame of the menus
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

            # build sub-structures for objective and subjectives symptoms
        symptoms_objective = self.symptoms_structure['Objective']
        symptoms_subjective = self.symptoms_structure['Subjective']

        exel.build_menu(symptoms_objective, menu_objective, self.on_select)
        exel.build_menu(symptoms_subjective, menu_subjective, self.on_select)

    def on_select(self, selection):
        """
        Symptoms selector

        Sets the right attributes depending on the menu selection to update the symptom list 
        Recovers data linked to the video to obtain the current time
        the selection is expected to be on the form 
            designation > description > sub descrition> topography > lateralization

        Args:
            selection (path): selected symptom
        """
        current_video_time = self.interface_generale.get_current_video_time() 
        
        #print(selection)

        buffer_attributs = selection.split(">")

        attributs = ["","","","","","","","",""]

        attributs[1] = f"{buffer_attributs[1]} {buffer_attributs[0]}"
        attributs[2] = buffer_attributs[4]
        attributs[3] = buffer_attributs[3]
        attributs[5] = buffer_attributs[2]

        attributs[6] = current_video_time

        self.interface_generale.update_right_panel(attributs)

    def on_select_bar(self, selection):
        current_video_time = self.interface_generale.get_current_video_time()
        
        buffer_attributs = selection.split(";")
        attributs = ["","","","","","","","",""]

        if len(buffer_attributs)<2 or buffer_attributs[1] in ["Foot/Inferior limb","Hand/Superior limb",
                                                              "Body","Eyes","Head","Eyelids","Mouth","Face",
                                                              "Foot","Hand","Superior limb","Throat"]:
            attributs[1] = f"{buffer_attributs[0]}"
        else :
            attributs[1] = f"{buffer_attributs[1]} {buffer_attributs[0]}"

        attributs[6] = current_video_time

        self.interface_generale.update_right_panel(attributs)


class FriseSymptomes:
    """
    Class used to generate a timeline summarising all the symptoms present during an epileptic seizure.

    Attributes: 
        interfaceGenerale (:obj:`InterfaceGenerale`): the general interface with the symptoms list
        MenuDeroulant (:obj:`Menu_symptomes`): dropdown menus
    """
    def __init__(self,InterfaceGenerale,MenuDeroulant):
        self.menu_deroulant=MenuDeroulant
        self.interface_generale=InterfaceGenerale
        

    def afficher(self):
        """
        Retrieves the list of symptoms instantiated in the InterfaceGenerale class's update_right_panel function.

        This method retrieves the list of symptoms stored in the InterfaceGenerale class instance's ListeSymptomes attribute.
        It then processes each symptom in the list, extracting relevant information such as name, start time, end time,
        ID, lateralization, topography, orientation, additional attributes, and comments. This information is then formatted
        and sorted based on the start time of each symptom.

        Returns:
            None

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
    General interface class, which provides the overall look and feel of the graphical interface. 
    
    It is represented in the form of a window and allows the other classes to be integrated into it.
    It calls the LecteurVideo, FriseSymptomes and Menu_symptoms classes. 

    Attributes:
        fenetre: Represents the main window of the graphical interface.
        cap: Represents the video capture object.
        lec_video: An instance of the LecteurVideo class.
        frise: An instance of the FriseSymptomes class.
        set_end_time_mode: A boolean variable indicating whether the end time mode is set.
        current_symptom: Represents the current symptom being processed.
        ListeSymptomes: A list containing symptom objects, initially empty.
        theme: A list containing color theme values.
        menu_bar: A menu bar for the interface.
        menu_open: A menu for opening different options like video and symptoms.
        menu_save: A menu for saving options like symptoms, report, and timeline.
        clic_x: The x-coordinate of the click event.
        clic_y: The y-coordinate of the click event.
        frame_left: Represents the left frame of the interface.
        frame_middle: Represents the middle frame of the interface.
        frame_right: Represents the right frame of the interface.
        scrollable1: A scrollable frame for the right panel.
        text_output: A scrollable frame for displaying text output.
        frame_CTkButton: A frame for buttons in the middle frame.
        bouton_revoir: Button for rewinding the video.
        bouton_reculer: Button for moving the video backward.
        bouton_play_pause: Button for playing or pausing the video.
        bouton_avancer: Button for moving the video forward.
        bouton_nul: A dummy button.
        frame_frise: A frame for displaying the symptom timeline.
        bouton_frise: Button for displaying the timeline.
        bouton_save: Button for saving the report.
        label_temps: Label for displaying elapsed time and total time.
        progress_slider: A slider for manual video progress.
        canvas: Canvas for displaying the video.
        zone_text: A text area for comments.

    """
    def __init__(self, fenetre):
        """
        the constructor of the InterfaceGenerale class

        Set the overall look and places all the frames, butons and canvases.

        Arguments:
            fenetre(any): the widget in witch to create the general interface (a window normally)
        """
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
        
        manage the display of symptom start/end times on the right-hand side and pop-up management to modify a symptom.
 

        Args:
            attributs (list): symptom initialisation list | default = [] 
        """
        def set_end_time(event, Symp):
            """
            Adds the end time to an existing symptom
            
            Args:
                event (None): corresponds to pressing on the area where the symptom is displayed
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
            Opens the symptom editing window

            Args:
                event (None): corresponds to pressing on the window to modify the symptom
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
        """
        Remove a symptom from the list of symptoms and destroy its display container.

        Args:
            selection: The symptom object to be removed.
            container: The container containing the display elements of the symptom.

        Returns:
            None
        """
        for symp in self.ListeSymptomes:
            if symp.get_Name() == selection.get_Name():
                self.ListeSymptomes.remove(symp)
                container.destroy()  # Supprime le conteneur entier, y compris le label et le bouton
                break       


    def get_current_video_time(self):
        """
        Get the current time of the video.

        Returns:
            str: A string representing the current time of the video in the format "HH:MM:SS".
                Returns "00:00:00" if the video is not opened.
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
        Get the total duration of the video.

        Returns:
            int: The total duration of the video in seconds.
                Returns 0 if the video is not opened.
        """
        if self.cap is not None and self.cap.isOpened():
            total_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            return int(total_frames / fps)


    def ouvrir_video(self):
        """
        Opens the video by calling the Lecteur_video class
        """
        self.lec_video.ouvrir_video()
    

    def ouvrir_video_noire(self):
        """
        Opens the black_video by calling the Lecteur_video class
        """
        self.lec_video.ouvrir_video_noire()

    
    def lire_fichier(self,nom_fichier):
        """
        Opens a text file, reads it, and saves the information in a list.

        Args:
            nom_fichier (str): The path to the text file to be read.

        Returns:
            list: A list containing all the lines read from the file.

        Raises:
            FileNotFoundError: If the specified file is not found.
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
        Saves the list of symptoms to a text file.
        It calls the save class for this purpose. 
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
        Creates the text to display in the right panel.

        Args:
            sympt (Symptome): The symptom for which to create the text.

        Returns:
            str: The text to display containing the relevant information.
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
        Loads a list of symptoms from a text file.

        This function prompts the user to select a text file containing symptom data. It then reads the symptom data from the file 
        using the read_symptoms function from the load_symptomes module. For each symptom read from the file, it updates the right panel of 
        the interface with the symptom attributes.

        Raises:
            FileNotFoundError: If the selected file is not found.
            Exception: If an unexpected error occurs during the file reading process.

        """
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Fichiers textes", "*.txt")])
            if file_path:  # Check if a file was selected
                list_S = load.read_symptoms(file_path)
                if list_S:
                    for s in list_S:
                        text = self.text_sympt(s)
                        attr = s.get_attributs()
                        self.update_right_panel(attr)
                else:
                    print("The file is empty or does not contain valid symptoms.")
                    error.showerror("Episcope error", "The file is empty or does not contain valid symptoms.")
            else:
                print("No file selected.")
                error.showerror("Episcope error","No file selected.")

        except FileNotFoundError:
            print("File not found.")
            error.showerror("Episcope error", "File not found")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            error.showerror("Episcope error", f"An error occured: {str(e)}\n\nPlease check the file you tried to open ")


class LecteurVideo():

    """
    Video player class that manages the different functionalities of the video.

    Functionalities supported :
        * opening a video using the file explorer
        * opening a dark video - in case there is no video to actually open 
        * sychronizing sound and video
        * buttons gestion

    This class calls the InterfaceGenerale class

    Attributes:
        interface_generale (InterfaceGenerale): The main interface in which to open the video player.
        video_paused (bool): Indicates whether the video is currently paused.
        current_frame_time (int): Current time of the video frame being displayed.
        clock (Clock): Pygame clock to manage time-related operations.
        vitesse_lecture (int): Speed factor for video playback.
        valeur (int): A value indicating something, not clearly specified in the docstring.
        temps_ecoule (int): Elapsed time of the video playback.
        duree_totale (int): Total duration of the loaded video.
    """
    def __init__(self, InterfaceGenerale):
        """
        Constructor of the LecteurVideo class

        Arguements: 
            InterfaceGenerale(:obj: 'InterfaceGenerale') : the main interface in which to open the video player
        """

        self.interface_generale = InterfaceGenerale
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1026)
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
        Opens a video with the file explorer.
        Once chosen, it plays the video in the middle_frame
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
        Opens the black video.
        The black video must be in the same folder as the code : "video_noire.mp4"
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
            error.showerror('Episcope Error', "'Black Video' not found in the current folder.")
            print("'Black Video' not found in the current folder.")


    def preparer_mixer(self, file_path):
        # Utiliser moviepy pour extraire les propriétés audio
        clip = mp.VideoFileClip(file_path)
        audio = clip.audio
        if audio:
            # Extrait les propriétés audio
            fps_audio = audio.fps  # fréquence d'échantillonnage
            n_channels = audio.nchannels  # nombre de canaux

            # Fermer le clip pour libérer des ressources
            clip.close()

            # Réinitialise pygame.mixer avec les propriétés audio de la vidéo
            pygame.mixer.quit()
            pygame.mixer.init(frequency=fps_audio, size=-16, channels=n_channels, buffer=4096)  # buffer ajustable
            print(f"Mixer initialisé avec {fps_audio} Hz et {n_channels} canaux")
        else:
            print("Aucune piste audio détectée.")

    def preparer_son_video(self, file_path):
        # Préparer le mixer pour chaque vidéo
        self.preparer_mixer(file_path)

        # Charger et jouer l'audio comme précédemment
        clip = VideoFileClip(file_path)
        audio_path = "temp_audio.wav"
        clip.audio.write_audiofile(audio_path)
        clip.close()

        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play(-1)  # Jouer en boucle

    def afficher_video(self):
        """
        Allows to display and play the video.

        Resizes the frames of the video to match thoses  of the middle frame
        computes and displays the total and elapsed time of the video 
        """
        
        if self.interface_generale.cap.isOpened():# Vérifie si la vidéo est ouverte
            ret, frame = self.interface_generale.cap.read()  # Lit la prochaine frame de la vidéo
            if not ret:
                # Gérer l'erreur, éventuellement réinitialiser la capture ou passer à la frame suivante
                print("Erreur lors de la lecture de la frame.")
                return
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
        Checks if each frame of the video is correctly processed, resized and displayed in the GUI
        """
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.interface_generale.canvas.create_image(0, 0, image=frame, anchor=tk.NW)
        self.interface_generale.canvas.image = frame


    def mettre_a_jour_temps_video(self):
        """
        Ensures that the displayed time of the video is regularly updated and that the video plays smoothly. 
        It also ensures the sinchronization between the video advancement and the real time
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
        Manage the play/pause state of the video 
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
        """
        Methode qui met à jour la position du curseur dans la barre e proggression
        """
        self.interface_generale.progress_slider.set(self.temps_ecoule)
        self.interface_generale.fenetre.after(1, self.avancer)


    def configurer_barre_progression(self):
        """
        Methode qui contole l'eta de la barre de progression qu'elle soit relache ou appuiyé
        """
        total_duration = self.interface_generale.get_video_duration()
        self.interface_generale.progress_slider.config(to=total_duration, from_=0)
        self.interface_generale.progress_slider.bind("<ButtonPress>", self.on_drag_start)
        self.interface_generale.progress_slider.bind("<ButtonRelease>", self.on_drag_end)
    def on_drag_start(self, event):
        """Méthode appelée lorsque le curseur de la barre de progression est saisi."""
        self.pause_lecture()

    def on_drag_end(self, event):
        """Méthode appelée lorsque le curseur de la barre de progression est relâché."""
        # Mettre à jour la position de la vidéo en fonction de la position du curseur
        position = self.interface_generale.progress_slider.get()
        self.manual_update_progress(position)
        # Reprendre la lecture
        self.resume_lecture()

    def resume_lecture(self):
        """Reprend la lecture vidéo et audio."""
        if self.video_paused:
            self.video_paused = False
            self.interface_generale.bouton_play_pause.configure(text="Pause")
            pygame.mixer.music.unpause()
            self.afficher_video()
            self.mettre_a_jour_temps_video()

                
    def manual_update_progress(self, value):
        """Mise à jour manuelle de la position de la vidéo sans démarrer le son."""
        self.temps_ecoule = float(value)
        fps = self.interface_generale.cap.get(cv2.CAP_PROP_FPS)
        frame_number = self.temps_ecoule * fps
        self.interface_generale.cap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_number))
        if not self.video_paused:
            pygame.mixer.music.play(-1, start=self.temps_ecoule)
    def avance_progress(self):
        """Avance la vidéo et gère correctement la pause de la vidéo et de l'audio."""
        if self.interface_generale.cap.isOpened():
            if not self.video_paused:
                self.pause_lecture()  # Mettre en pause avant de modifier la position

            fps = self.interface_generale.cap.get(cv2.CAP_PROP_FPS)
            frames_to_skip = int(fps * 0.25)  # Avancer de 0.25 secondes
            current_frame = self.interface_generale.cap.get(cv2.CAP_PROP_POS_FRAMES)
            new_frame = current_frame + frames_to_skip
            self.interface_generale.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
            
            # Afficher immédiatement la frame mise à jour
            self.afficher_video_frame()

            # Si la vidéo était en pause avant l'opération, la laisser en pause
            if self.video_paused:
                pygame.mixer.music.pause()  # Assurez-vous que l'audio est aussi en pause

    def recule_progress(self):
        """Recule la vidéo et gère correctement la pause de la vidéo et de l'audio."""
        if self.interface_generale.cap.isOpened():
            if not self.video_paused:
                self.pause_lecture()

            fps = self.interface_generale.cap.get(cv2.CAP_PROP_FPS)
            frames_to_skip = int(fps * 0.25)  # Reculer de 0.25 secondes
            current_frame = self.interface_generale.cap.get(cv2.CAP_PROP_POS_FRAMES)
            new_frame = max(0, current_frame - frames_to_skip)
            self.interface_generale.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)

            # Afficher immédiatement la frame mise à jour
            self.afficher_video_frame()

            # Si la vidéo était en pause avant l'opération, la laisser en pause
            if self.video_paused:
                pygame.mixer.music.pause()


    def afficher_video_frame(self):
        """Affiche la frame actuelle de la vidéo sans continuer la lecture."""
        if self.interface_generale.cap.isOpened():
            ret, frame = self.interface_generale.cap.read()
            if ret:
                self.interface_generale.cap.set(cv2.CAP_PROP_POS_FRAMES, self.interface_generale.cap.get(cv2.CAP_PROP_POS_FRAMES) - 1)  # Revenir d'une frame car read avance
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.interface_generale.canvas.winfo_width(), self.interface_generale.canvas.winfo_height()))
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.interface_generale.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                self.interface_generale.canvas.image = photo
            else:
                print("Erreur lors de la lecture de la frame.")


    def revoir_video(self):
        """
        Allows to play the video again 
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
        Converts the time in seconds in a more readable format : minutes and secondes
        """
        return str(datetime.timedelta(seconds=seconds))


    def charger_son_video(self, file_path):
        """
        Stops the previous audio, and extracts and loads the new audio track associated with the selected video. 
        It also cleans up the resources used during the process. 
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
        Retrieve the coordinates by clicking on the video. 
        
        It currently displays a red cross.
        But you can use this red cross to display the symtoms by hovering over it with the cursor.
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
        Displays the red cross for 1 second where one clicks on the video

        Arguments:
            canvas (tk.Canvas): the canvas of the video
            x (int): x-coordinate of the cross
            y (int): y-coordinate of the cross
            taille (int): size of the cross

        """
        # Coordonnées pour créer un '+'
        ligne_horizontale = self.interface_generale.canvas.create_line(x-taille*20, y, x+taille*20, y, fill="red", width=3)
        ligne_verticale = self.interface_generale.canvas.create_line(x, y-taille*20, x, y+taille*20, fill="red", width=3)
                
        self.interface_generale.canvas.after(1000, lambda: self.interface_generale.canvas.delete(ligne_horizontale, ligne_verticale))



if __name__ == "__main__":
    root = ctk.CTk()

    root.after(0, lambda:root.state('zoomed'))
    
    # photo ?
    #iconpath = ImageTk.PhotoImage(file="..\docs\source\images\Logo_cerveau.png")
    #root.wm_iconbitmap()
    #root.iconphoto(False, iconpath)

    lecteur = InterfaceGenerale(root)
    root.mainloop()
