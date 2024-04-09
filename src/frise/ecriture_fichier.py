"""
This module provides functions for writing symptom data, symptom lists, and metadata to text files.

Functions:
    EcrireSymptome: Writes a single symptom to a file.
    EcrireListeSymptome: Writes a list of symptoms to a file.
    EcrireMetaData: Writes metadata to a file.
    format: Formats text data by replacing specified characters.
    ecrire_rapport: Writes a report with symptom details.

"""
from annotation.class_symptome import *
from frise.class_metadata import MetaData

    

def EcrireSymptome(symptome, nomfichier) :
    """
    Writes a single symptom to a file.

    Args:
        symptome (:obj:`Symptome`): The symptom object to be written to the file.
        nomfichier (str): The path of the file to write to.

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
    Writes a list of symptoms to a file.

    Args:
        listeSymptome (list): List of symptom objects to be written to the file.
        nomfichier (str): The path of the file to write to.
    
    Returns:
        None 
    """
    with open(nomfichier, 'a') as fichier :
        fichier.write("ID \tName \tLateralization \tTopography \tOrientation \tAttributs supplémentaires \tStart \tEnd   \tcomment \n")

    for symptome in listeSymptome :
        EcrireSymptome(symptome, nomfichier)
    
    with open(nomfichier, 'a') as fichier :
        fichier.write("\n\n")
    


def EcrireMetaData(Meta, nomfichier) :
    """
    Writes metadata to a file.

    Args:
        Meta (:obj:`Matadata`): metadata information.
        nomfichier (str): The path of the file to write to.

    Returns:
        None

    """
    with open(nomfichier, 'a') as fichier :
         fichier.write("patient :\n")
         fichier.write(f"Nom : {Meta.get_nom()}\n")
         fichier.write(f"Prenom : {Meta.get_prenom()}\n")
         fichier.write(f"Date et heure de la crise : {Meta.get_dateCrise()}\n")
         fichier.write(f"Annotation réalisée par : {Meta.get_docteur()}\n")
         fichier.write(f"Annotation réalisée le : {Meta.get_dateAnnotation()}\n")
         fichier.write("\n")

        
def format(data, caracteres):
    """
    Formats text data by replacing specified characters.
    
    Args:
        data (:obj:`list` of :obj:`str`) : List of text data to be formatted.
        caracteres (List): List containing character replacement pairs.

    Returns:
        :obj:`list` of :obj:`str` : Formatted text data.

    """
    for element in caracteres :
        new_data = [txt.replace(element[0],element[1]) for txt in data]
        data = new_data

    return new_data

def ecrire_rapport(Symptom_list, filename):
    """
    Writes a report with symptom details to a file.

    Args:
        Symptom_list (:obj:`list` of :obj:`Symptome`): List of symptom objects.
        filename (str): The path of the file to write to.
    """
    k = 1
    with open(filename, 'a') as fichier :
         for symptom in Symptom_list:
            tdeb = symptom.get_Tdeb()
            tfin = symptom.get_Tfin()
            duree = compute_duration(tdeb, tfin)
        
            fichier.write(f"{k} - {symptom.get_Name()}, {symptom.get_Topography()}, {symptom.get_Lateralization()} : debut a {symptom.get_Tdeb()}, duree : {duree} sec (fin : {symptom.get_Tfin()})\n")
            
            k+=1

def compute_duration(deb, fin):
    """
    Compute the duration between two time strings in seconds.

    Args:
        deb (str): Start time string in the format "hh:mm:ss".
        fin (str): End time string in the format "hh:mm:ss".

    Returns:
        int: Total duration between the start and end time in seconds.
    """
    deb_hours, deb_minutes, deb_seconds = map(int, deb.split(':'))
    fin_hours, fin_minutes, fin_seconds = map(int, fin.split(':'))

    total_deb_seconds = deb_hours * 3600 + deb_minutes * 60 + deb_seconds
    total_fin_seconds = fin_hours * 3600 + fin_minutes * 60 + fin_seconds

    duration_seconds = total_fin_seconds - total_deb_seconds

    return duration_seconds            

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