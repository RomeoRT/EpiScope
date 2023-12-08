import customtkinter

app = customtkinter.CTk()
def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)

optionmenu = customtkinter.CTkOptionMenu(app, values=["option 1", "option 2"],
                                         command=optionmenu_callback)

optionmenu.set("option 2")
progressbar = customtkinter.CTkProgressBar(app, orientation="horizontal")

progressbar.pack()
optionmenu.pack()

app.mainloop()