import tkinter as tk
import customtkinter as ctk

class search_symptomes:
    """
    A class to create a symptom search bar in the EpiScope GUI.
    
    This class provides a search bar to look for symptoms in a hierarchical dictionary structure
    and display the matching results in a listbox. It also allows selecting an item from the listbox
    by clicking on it, triggering a specified function with the selected item as an argument.
    
    Attributes:
        symptoms_structure (dict): Hierarchical dictionary containing organized symptom data.
        search_entry (CTkEntry): Entry widget for user input.
        symptom_listbox (Listbox): Listbox widget to display search results.
    
    Methods:
        search_element(search_term): Searches for matching elements based on the search term.
        get_selected(event, func): Retrieves the selected item from the listbox.
        update_search(event): Updates the listbox based on the search input.
    """

    def __init__(self, root, symptoms_struct, myfunc, width) :
        """
        Initializes the search_symptomes object.
        
        Args:
            root (tk.Tk): The Tkinter root window.
            symptoms_struct (dict): Hierarchical dictionary containing organized symptom data.
            myfunc (function): Function to be called when an item is selected from the listbox.
        """
        self.symptoms_structure = symptoms_struct

        # Search entry
        self.search_entry = ctk.CTkEntry(root, placeholder_text="Symptom")
        self.search_entry.pack(side='top', padx=5, pady=10, expand=False)

        self.search_entry.bind('<KeyRelease>', self.update_search)


    # Listbox to display the search results
        self.frame = ctk.CTkFrame(root, fg_color='gray97',corner_radius=0,border_width=0 ,width=width, height=5)  # Ajustement ici
        self.frame.pack(padx=5, pady=1, expand=True, fill=tk.BOTH)

        self.symptom_listbox = tk.Listbox(self.frame, width=width, height=5, bd=0, bg='gray97')
        self.symptom_listbox.pack(padx=5, pady=1, expand=True, fill=tk.BOTH)
        self.symptom_listbox.bind('<ButtonRelease-1>', lambda event, func=myfunc: self.get_selected(event, func))  # Lier l'événement de clic de souris à la fonction truc_special_cool
       
        self.bouton_nul = ctk.CTkButton(self.frame, text="", width=100, fg_color='gray97', hover_color='gray97') # pour gerer le placement
        self.bouton_nul.pack(side=ctk.LEFT, padx=100, pady=200)
        self.bouton_nul.configure(state="disabled")    

    def search_element(self, search_term):
        """
        Searches for elements matching the search term in the 'Designation' and 'Description' columns.
        
        Args:
            symptoms_structure (dict): Hierarchical dictionary containing organized symptom data.
            search_term (str): Term to search for in 'Designation' and 'Description' columns.
        
        Returns:
            list: List of matching elements found for the search term.
        
        This function searches for the specified term in the 'Designation' and 'Description' columns 
        of the hierarchical structure and returns a list of matching elements.
        """
        
        matching_elements = []

        for typology, designations in self.symptoms_structure.items():
            for designation, descriptions in designations.items():
                if search_term.lower() in designation.lower():
                    matching_elements.append((typology, designation, ''))
                
                if descriptions is not None:
                    for description, details in descriptions.items():
                        # Check if the description is not empty or if there are other details
                        if description.strip() or details or descriptions[description]:
                            if search_term.lower() in description.lower():
                                matching_elements.append((typology, designation, description))
                            
        return matching_elements

    def get_selected(self, event, func):
        """
        Retrieves the selected item from the listbox and calls the specified function.
        
        Args:
            event: The event object (not used directly, but required by Tkinter).
            func (function): Function to be called with the selected item as an argument.
        """
        # Récupérer l'index de l'élément sélectionné
        selected_index = self.symptom_listbox.curselection()
        
        if selected_index:
            # Récupérer l'élément sélectionné à partir de l'index
            selected_item = self.symptom_listbox.get(selected_index)
            func(selected_item)
        

    def update_search(self, event):
        """
        Update the displayed symptoms based on the user input in the search bar.
        
        This function filters the symptoms based on the user input in the 
        search bar and updates the listbox to show only the matching symptoms.
        
        Args:
            event: The event object (not used in this function, but required by Tkinter)
        """
        query = self.search_entry.get().lower()  # Get the user input and convert it to lowercase
        
        # Clear the existing items in the listbox
        self.symptom_listbox.delete(0, tk.END)
        
        if query != "":
            results = self.search_element(query)
            
            # Add matching elements to the listbox
            for element in results:
                typology, designation, description = element
                self.symptom_listbox.insert(tk.END, f"{designation} ; {description}")
            
            num_items = self.symptom_listbox.size()
            if num_items < 10:
                self.symptom_listbox.config(height=num_items+1)
            else:
                self.symptom_listbox.config(height=10)  # Taille fixe si plus de 5 éléments


if __name__ == "__main__" :

    import exel_menus as excel
# Create the Tkinter window
    root = tk.Tk()
    root.title('Symptom Selection')

    # Load the Excel file and create the symptoms structure
    file_path = 'ictal_symptoms.xlsx'
    symptoms_structure = excel.Read_excel(file_path)

    def f(x):
        pass

    mybar = search_symptomes(root, symptoms_structure, f, 100)
        
    # Run the Tkinter event loop
    root.mainloop()
