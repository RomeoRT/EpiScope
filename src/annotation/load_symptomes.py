"""
fonctions pour charger des symptomes
"""
from class_symptome import Symptome

def read_symptoms(filename):
    """
    lit un fichier texte de symptomes symptome dans un fichier texte
    """
    symptom_list = []
    with open(filename, 'r') as file:
        buffer = file.readline() # la premiere ligne contient l'intitulé des colones
        
        for line in file:
            symp_buffer = file.readline()

            symp_init = symp_buffer.split("\t")
            print(f"liste : {symp_init}")
            print(f"len liste : {len(symp_init)}")
            print(f"symp_init[1] : {symp_init[1]}")
            print("---------------\n")
            # EOF problem

            #sympt = Symptome(symp_init[0],symp_init[1],symp_init[2],symp_init[3],symp_init[4],symp_init[5],symp_init[6],symp_init[7],symp_init[8]) 
            #symptom_list.append(sympt)

    return symptom_list

if __name__ == "__main__":
    
    myfile= "../../../../txt_episcope/save_sympt1.txt"
    list = read_symptoms(myfile)

   # for s in list: 
    #    print(f"{s.get_ID()} \n")
  #      print(f"{s.get_Nom()} \n")
#   print(f"{s.get_Lateralisation()} \n")
 #       print(f"{s.get_SegCorporel()} \n")
  #      print(f"{s.get_Orientation()} \n")
#
 #       print("---------------\n")
        

     

    
    


