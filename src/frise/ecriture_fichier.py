"""
Projet Episcope

Auteur : Roméo RAMOS--TANGHE

Ce fichier contient des fonctions pour créer et éditer les fichiers '.txt' de sortie avec les symptomes
"""
from annotation import class_symptome

def EcrireSymptome(symptome, nomfichier) :
    data = symptome.get_attributs()
    with open(nomfichier, 'a') as fichier :
        for attribut in data :
            fichier.write(attribut)


def EcrireListeSymptome(listeSymptome, nomfichier) :
    for symptome in listeSymptome :
        EcrireSymptome(symptome, nomfichier)

##########################################################################################################
if __name__ == "__main__" :
     S1 = Symptome("ID", "Nom", "Lateralisation", "SegCorporel", "Orientation", "AttributSuppl", "Tdeb", "Tfin", "Commentaire")

     nomfichier = '../../../unficierdetest.txt'

     EcrireSymptome(S1, nomfichier)