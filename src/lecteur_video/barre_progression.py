import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import keyboard
import pygame
from moviepy.editor import VideoFileClip 

# Initialisation de pygame
pygame.mixer.init()

# Fonction pour mettre à jour la barre de progression automatiquement
def auto_update_progress():
    global progress_width, is_paused, cap
    if not is_paused:
        ret, frame = cap.read()
        if ret:
            progress_width += 1
            canvas.delete("progress")
            
            # Convertir l'image OpenCV en format PhotoImage
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(frame)

            # Afficher l'image dans le canevas
            canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            canvas.image = photo
            
            canvas.create_rectangle(0, 290, progress_width, 300, fill="purple", tags="progress")

            progress_slider.set(progress_width)

            #Jouer le son:
            sound.play()

            #on calcule le delai en fonction du frame rate
            delay=int(1000/video_framerate)
            root.after(delay, auto_update_progress)


# Fonction appelée lors du déplacement du curseur
def manual_update_progress(value):
    global progress_width
    progress_width = int(value)
    canvas.delete("progress")
    canvas.create_rectangle(0, 290,  progress_width, 300, fill="purple", tags="progress")
    cap.set(cv2.CAP_PROP_POS_FRAMES, progress_width)

def pause_lecture():
    global is_paused
    if is_paused:
        pause_button.configure(text="Pause")
        is_paused= False
        auto_update_progress()
    else:
        pause_button.configure(text="Reprendre")
        is_paused = True
        
# Fonction qui permet d'avancer de 2 secondes la vidéo:
def avance_progress():
    global progress_width
    progress_width += 1
    manual_update_progress(progress_width)

# Fonction qui permet de reculer de 2 secondes la vidéo:
def recule_progress():
    global progress_width
    progress_width -= 1
    manual_update_progress(progress_width)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Barre de progression avec vidéo")

# Création d'un canevas
canvas_width = 400  # Ajustez la largeur du canevas en fonction de la taille de votre vidéo
canvas_height = 300  # Ajustez la hauteur du canevas en fonction de la taille de votre vidéo
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Initialisation de la largeur de la barre de progression
progress_width = 0

# Création d'un curseur (Scale) pour la barre de progression
progress_slider = tk.Scale(root, from_=0, to=canvas_width, orient="horizontal", command=manual_update_progress)
progress_slider.set(progress_width)
progress_slider.pack()


# Création d'un bouton à gauche pour reculer de 2 secondes:
recule_button = tk.Button(root, text="-2", command=recule_progress)
recule_button.pack(side="left",padx=50)
# Associer la fonction avance_image à l'événement de la touche 'Right'
keyboard.add_hotkey('Left', recule_progress)

# Bouton pour mettre en pause la progression
pause_button = tk.Button(root, text="Pause", command=pause_lecture)
pause_button.pack(side="left",padx=60)
# Entrer clavier qui permet de mettre en pause
keyboard.add_hotkey('space', pause_lecture)

# Création d'un bouton à droite pour avancer de 2 secondes:
avance_button = tk.Button(root, text="+2", command=avance_progress)
avance_button.pack(side="left",padx=70)
# Associer la fonction avance_image à l'événement de la touche 'Right'
keyboard.add_hotkey('Right', avance_progress)

# Variable pour suivre l'état de pause
is_paused = False


file_path = filedialog.askopenfilename(filetypes=[("Fichiers vidéo", "*.mp4 *.avi")])

# Extraire l'audio du fichier vidéo
video_clip = VideoFileClip(file_path)
video_framerate=video_clip.fps
audio_clip = video_clip.audio
audio_clip.write_audiofile("audio.wav")

# Ajouter une instance pygame.mixer.Sound pour gérer le son de la vidéo
sound = pygame.mixer.Sound(file="audio.wav")

# Lancer la vidéo
cap = cv2.VideoCapture(file_path)
auto_update_progress()

root.mainloop()
