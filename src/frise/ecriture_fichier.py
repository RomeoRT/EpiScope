"""
Ce module contient des fonctions pour créer et éditer les fichiers '.txt' de sortie avec les symptomes
"""
from annotation.class_symptome import *
import datetime
    

def EcrireSymptome(symptome, nomfichier) :
    """
    Ecrit un symptome dans un fichier texte dont on specifie le nom
    
    Args:
        symptome (Symptome): symptome à écrire
        nomfichier (string): chemin du fichier

    Returns:
        None 
    
    """
    
    data = symptome.get_attributs()
    
    # formattage : caracteres a supprimer
    caract = [["\n",""],["\t"," "]]
    
    data = format(data, caract)
    with open(nomfichier, 'a') as fichier :
        for attribut in data :
            fichier.write(attribut)
            fichier.write(" \t")
        fichier.write("\n")

def EcrireListeSymptome(listeSymptome, nomfichier) :
    """
    Ecrit une liste de symptomes dans un fichier texte
    
    Chaque symptome est écrit sur une ligne
    Fait appel à la fonction EcrireSymptome

    Args:
        symptome (list): liste des symptomes
        nomfichier (string): chemin du fichier
    
    Returns:
        None 
    """
    with open(nomfichier, 'a') as fichier :
        fichier.write("ID \tNom \tLateralisation \tSegment corporel \tDebut \tFin \tOrientation \tAttributs supplémentaires \tcommentaires \n")

    for symptome in listeSymptome :
        EcrireSymptome(symptome, nomfichier)
    
    with open(nomfichier, 'a') as fichier :  
        fichier.write("\n\n")  

def EcrireMetaData(ListeMeta, nomfichier) :
    """
    Ecrit les metadata d'une annotation dans un fichier texte sous la forme : heure réelle :\tpatient :\tpraticien :\tdate d'annotation : \n

    Args:
        ListeMeta (List): liste des métadatas
        nomfichier (string): chemin du fichier

    Returns:
        None

    """
    mydate = datetime.date.today()
    with open(nomfichier, 'a') as fichier :
         fichier.write("Metadonnées :\n")
         fichier.write("heure réelle :\tpraticien :\tpatient :\tdate d'annotation : \n")
         fichier.write(f"{ListeMeta[0]}\t{ListeMeta[1]}\t{ListeMeta[2]}\t{mydate}\n\n")
        
def format(data, caracteres):
    """
    supprime les caracteres speciaux d'une liste de string
    
    Args:
        data (List) : liste de strings a traiter
        caracteres (List): liste des caracteres et de leur remplacement, de la forme [("C1", "C2")]

    Returns:
        new_data (list) : liste de strings traitée
    """
    for element in caracteres :
        new_data = [txt.replace(element[0],element[1]) for txt in data]
        data = new_data

    return new_data

##########################################################################################################
if __name__ == "__main__" :
    # test des fonctions 
    L = []
    for i in range(20) :
        S = Symptome(f"ID{i}", f"Nom{i}", f"Lateralisation{i}", f"SegCorporel{i}", f"Orientation{i}", f"AttributSuppl{i}", f"Tdeb{i}", f"Tfin{i}", f"Commentaire{i}")
        L.append(S)

    meta = ["15h12", "M. Smith", "toto" ]
    nomfichier = 'd:/Unfichiertest.txt'


    EcrireMetaData(meta, nomfichier)
    EcrireListeSymptome(L, nomfichier)

    #test format
    unicode = [("\n",""),("é","e"),("a","o")]
    liste_nulle = ["coucou \n lés amis", "coucou més amis"]
    list_cool = format(liste_nulle, unicode)

    print(list_cool)