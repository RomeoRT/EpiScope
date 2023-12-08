"""
Projet Episcope

Auteur : Roméo RAMOS--TANGHE

Ce fichier édite des fichiers grâce à une interface graphique.
"""
import customtkinter
import save

app = customtkinter.CTk()


liste = ["bonjour\n"]

app = customtkinter.CTk()
app.geometry("400x150")
app.mainloop()

bouton = customtkinter.CTkButton(app, text="save")#, command = lambda : save.save(liste))
bouton.pack(padx=20, pady=10)

bouton = customtkinter.CTkButton(app, text="edit")#, command = lambda : save.edit(liste))
bouton.pack(padx=20, pady=30)

app.mainloop()