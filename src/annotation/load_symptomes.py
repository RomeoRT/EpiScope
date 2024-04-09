"""
Functions for loading symptoms from text files
"""
from annotation.class_symptome import Symptome


def read_symptoms(filename):
    """
    Reads a text file containing symptoms and returns a list of Symptome objects.

    Args:
        filename (str): The path to the text file containing symptoms.

    Returns:
        list: A list of Symptome objects.
    """

    symptom_list = []
    with open(filename, 'r') as file:
        
        buffer = file.readlines() 

        buffer.pop(0)                      # first line = titles (useless)
        
        for elt in buffer :
          symp_init = elt.split("\t")

          sympt = Symptome(symp_init[0],symp_init[1],symp_init[2],symp_init[3],symp_init[4],symp_init[5],symp_init[6],symp_init[7],symp_init[8]) 
          symptom_list.append(sympt)

    return symptom_list

if __name__ == "__main__":

    myfile= "../../../../txt_episcope/save_sympt1.txt"
    list = read_symptoms(myfile)

    for Symp in list: 
        print(f"{Symp.get_ID()} \n")
        print(f"{Symp.get_Name()} \n")
        print(f"{Symp.get_Lateralization()} \n")
        print(f"{Symp.get_Topography()} \n")
        print(f"{Symp.get_Orientation()} \n")
        print(f"{Symp.get_AttributSuppl()} \n")
        print(f"{Symp.get_Tdeb()} \n")
        print(f"{Symp.get_Tfin()} \n")
        print(f"{Symp.get_Comment()} \n")

        print("---------------\n")
        

     

    
    


