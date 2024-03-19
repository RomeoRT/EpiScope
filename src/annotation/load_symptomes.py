"""
fonctions pour charger des symptomes
"""
from annotation.class_symptome import Symptome
from frise.ecriture_fichier import format

def read_symptoms(filename):
    """
    lit un fichier texte de symptomes symptome dans un fichier texte
    """
    symptom_list = []
    with open(filename, 'r') as file:
        
        buffer = file.readlines() 

        buffer.pop(0)                      # first line = titles (useless)
        #buffer = format(buffer, ["\n",""]) # remove '\n' at the end of line

        for elt in buffer :
          symp_init = elt.split("\t")

          sympt = Symptome(symp_init[0],symp_init[1],symp_init[2],symp_init[3],symp_init[4],symp_init[5],symp_init[6],symp_init[7],symp_init[8]) 
          symptom_list.append(sympt)

    return symptom_list

if __name__ == "__main__":

    myfile= "../../../../txt_episcope/save_sympt1.txt"
    list = read_symptoms(myfile)

    for s in list: 
        print(f"{s.get_ID()} \n")
        print(f"{s.get_Nom()} \n")
        print(f"{s.get_Lateralisation()} \n")
        print(f"{s.get_SegCorporel()} \n")
        print(f"{s.get_Orientation()} \n")
        print(f"{s.get_AttributSuppl()} \n")
        print(f"{s.get_Tdeb()} \n")
        print(f"{s.get_Tfin()} \n")
        print(f"{s.get_Commentaire()} \n")

        print("---------------\n")
        

     

    
    


