import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import keyboard

#### une modification de roméo

# Fonction pour mettre à jour la barre de progression automatiquement
def auto_update_progress():
    global progress_width, is_paused, cap
    if not is_paused:
        ret, frame = cap.read()
        if ret:
            progress_width += 1
            canvas.delete("progress")
            canvas.create_rectangle(0, 0, progress_width, 20, fill="purple", tags="progress")

            # Convertir l'image OpenCV en format PhotoImage
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(frame)

            # Afficher l'image dans le canevas
            canvas.create_image(0, 25, anchor=tk.NW, image=photo)
            canvas.image = photo

            progress_slider.set(progress_width)
        root.after(100, auto_update_progress)

# Fonction appelée lors du déplacement du curseur
def manual_update_progress(value):
    global progress_width
    progress_width = int(value)
    canvas.delete("progress")
    canvas.create_rectangle(0, 0, progress_width, 20, fill="purple", tags="progress")
    cap.set(cv2.CAP_PROP_POS_FRAMES, progress_width)

# Fonction pour mettre en pause la progression
def pause_progress():
    global is_paused
    is_paused = True

# Fonction pour mettre en pause grâce à la touche espace 
def toggle_pause():
    global is_paused
    is_paused = not is_paused
    if not is_paused:
        auto_update_progress()

# Fonction pour reprendre la progression
def play_progress():
    global is_paused
    is_paused = False
    auto_update_progress()

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

# Bouton pour mettre en pause la progression
pause_button = tk.Button(root, text="Pause", command=pause_progress)
pause_button.pack()
# Entrer clavier qui permet de mettre en pause
keyboard.add_hotkey('space', toggle_pause)

# Bouton pour reprendre la progression
play_button = tk.Button(root, text="Play", command=play_progress)
play_button.pack()

# Création d'un bouton à droite pour avancer de 2 secondes:
avance_button = tk.Button(root, text=">", command=avance_progress)
avance_button.pack()
# Associer la fonction avance_image à l'événement de la touche 'Right'
keyboard.add_hotkey('Right', avance_progress)

# Création d'un bouton à gauche pour reculer de 2 secondes:
recule_button = tk.Button(root, text="<", command=recule_progress)
recule_button.pack()
# Associer la fonction avance_image à l'événement de la touche 'Right'
keyboard.add_hotkey('Left', recule_progress)


# Variable pour suivre l'état de pause
is_paused = False

# Lancer la vidéo
file_path = filedialog.askopenfilename(filetypes=[("Fichiers vidéo", "*.mp4 *.avi")])
cap = cv2.VideoCapture(file_path)
auto_update_progress()

root.mainloop()
