import customtkinter as CTk
import tkinter as tk

# Je n'ai pas réussi à faire en sorte que le menu se déroule tout seul quand on fait la recherche (pour montrer les résultats)

def filtrer_options(event):
    """
    filtre les options d'un menu déroulant en fonction d'une recherche textuelle
    """
    recherche = entry.get().lower()
    options_filtrées = [option for option in options if recherche in option.lower()]
    menu.configure(values=options_filtrées)


app = CTk.CTk()
app.title("Barre de recherche")
app.geometry("1000x500")

options = ["toto", "tata", "toti", "tota", "tato", "TiTi"]

entry = CTk.CTkEntry(app, placeholder_text="Symptomes")

entry.grid(row = 0)
entry.bind("<KeyRelease>", filtrer_options)

menu = CTk.CTkOptionMenu(app, values=options )
menu.grid(row=1)
menu.set("Symptomes")


app.mainloop()

