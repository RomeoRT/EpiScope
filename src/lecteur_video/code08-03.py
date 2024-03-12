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

#utile pour la génération de la frise chronologique:
from annotation.fonctions_frise import afficher_frise
from class_symptome import Symptome

class Menu_symptomes(ctk.CTkFrame):
    def __init__(self, master, interface_generale, largeur_totale):
        super().__init__(master, width=largeur_totale)
        self.interface_generale = interface_generale
        self.file_name = "Objective_Symptomes.txt"
        title, symptoms = self.read_symptoms_from_file(self.file_name)
        self.symptom_button = ctk.CTkButton(self, text=title, command=self.create_dropdown_menus, width=largeur_totale, fg_color='Plum3', text_color='black')
        self.symptom_button.pack(pady=20, fill='x')
        self.symptoms = symptoms 
        self.top_level = None  
        


    def create_dropdown_menus(self):
        if self.top_level is None or not self.top_level.winfo_exists():  # Vérifiez si la fenêtre n'existe pas déjà
            self.top_level = tk.Toplevel(self)
            self.top_level.wm_title("Symptômes")  # Optionnel: donnez un titre à la fenêtre où il y a les symptomes

            # Positionner la fenêtre juste en dessous du bouton
            x = self.symptom_button.winfo_rootx()
            y = self.symptom_button.winfo_rooty() + self.symptom_button.winfo_height()
            self.top_level.geometry("100x100")  # Positionne la fenêtre

            # Définir la largeur de la fenêtre égale à celle du bouton
            self.top_level.geometry(f"{self.symptom_button.winfo_width()}x400")  # La hauteur peut être ajustée selon le besoin

            menu_bar = tk.Menu(self.top_level)
            self.top_level.config(menu=menu_bar)
            my_font = tkFont.Font(size=12)
            main_menu = tk.Menu(menu_bar, tearoff=0, bg="grey", fg="white", font=my_font)
            menu_bar.add_cascade(label="Objective Symptômes ", menu=main_menu)
            
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
        self.interface_generale.update_right_panel(selection)

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


    def filtrer_options(self, event): 
        """
        filtre les options d'un menu déroulant en fonction d'une recherche textuelle
        """
        recherche = self.entry.get().lower()
        for i in range(self.nb_menus) :
            options_filtrees = [option for option in self.options_symptomes[i] if recherche in option.lower()]
            self.liste_MenuDeroulant[i].configure(values=options_filtrees) 

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

class InterfaceGenerale():
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Lecteur Vidéo")
        self.cap = None
        self.lec_video=LecteurVideo(self)
        self.frise=FriseSymptomes(self,self)
        self.lec_video.video_paused = False
 
        # Cadre pour le menu déroulant en haut
        self.frame_menu = ctk.CTkFrame(fenetre, fg_color='Plum2', height=40)
        self.frame_menu.pack(side=ctk.TOP, fill=ctk.X)
        police_label_m = tkFont.Font(size=12)
        # Menu déroulant
        options = ["Ouvrir","Ouvrir sans video","Save"]
        self.menu_deroulant = ctk.StringVar()
        self.menu_deroulant.set('Menu')
        self.menu = tk.OptionMenu(self.frame_menu, self.menu_deroulant, *options, command=self.menu_action)
        self.menu.config(bg='Plum3',fg='white',font=police_label_m)
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

        #Affichage des symptomes dans la partie de droite de l'interface:
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

        self.bouton_avancer = ctk.CTkButton(self.frame_CTkButton, text="avance", command=self.lec_video.avance_progress,text_color='black',fg_color='Plum4')
        self.bouton_avancer.pack(side=ctk.LEFT, padx=50)

        # Bouton pour activer la frise chronologique des symptomes:
        self.bouton_frise = ctk.CTkButton(self.frame_right, text="frise", command=self.frise.afficher, text_color='black', fg_color='Plum3')
        self.bouton_frise.pack(side=ctk.BOTTOM,padx=20,pady=20)
    
        # Étiquettes pour afficher le temps écoulé et la durée totale
        self.label_temps = tk.Label(self.frame_middle, text="Temps écoulé: 0:00 / Durée totale: 0:00", bg='grey', fg='white')
        self.label_temps.pack(side=tk.BOTTOM, padx=20)

        # Barre de progression manuelle
        self.progress_slider =tk.Scale(self.frame_middle, from_=0, to=100, orient="horizontal", command=self.lec_video.manual_update_progress)
        self.progress_slider.pack(side=tk.BOTTOM, fill=tk.X)

        # Créer une zone de texte pour les commentaires:
        self.zone_text = tk.Text(self.frame_right, height=40, width=fenetre.winfo_screenwidth() // 5, relief=tk.GROOVE, wrap=tk.WORD)
        self.zone_text.pack(side=tk.BOTTOM, pady=20,padx=20)

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


    def update_right_panel(self, text):
        self.text_output.config(state=tk.NORMAL)
        self.text_output.insert(tk.END, text + '\n')  # Ajoute le texte sélectionné à la zone de texte
        self.text_output.config(state=tk.DISABLED)
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
