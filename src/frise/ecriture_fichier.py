"""
Projet Episcope

Auteur : Roméo RAMOS--TANGHE

Ce fichier contient des fonctions pour créer et éditer les fichiers '.txt' de sortie avec les symptomes
"""
#from class_symptome import *
import datetime
##########################################################################################################################
class Symptome:
    """Classe permettant d'instancier un objet Symptome

    attributs : ID, nom, lateralisation, segment corporel, Tps debut, Tps fin, Orientation, Attributs suppl, Commentaire
    """

    def __init__(self, ID, Nom, Lateralisation, SegCorporel, Orientation, AttributSuppl, Tdeb, Tfin, Commentaire):
        self.ID = ID
        self.Nom = Nom
        self.Lateralisation = Lateralisation
        self.SegCorporel = SegCorporel
        self.Orientation = Orientation
        self.AttributSuppl = AttributSuppl
        self.Tdeb = Tdeb
        self.Tfin = Tfin
        self.Commentaire = Commentaire



    def get_attributs(self):
        """Retourne une liste contenant les valeurs des attributs de l'objet"""
        attributs = [
            self.ID,
            self.Nom,
            self.Lateralisation,
            self.SegCorporel,
            self.Orientation,
            self.AttributSuppl,
            self.Tdeb,
            self.Tfin,
            self.Commentaire
        ]
        return attributs    



    # fonctions pour recuperer les attributs separements

    def get_ID(self):
        return self.ID

    def get_Nom(self):
        return self.Nom

    def get_Lateralisation(self):
        return self.Lateralisation

    def get_SegCorporel(self):
        return self.SegCorporel

    def get_Orientation(self):
        return self.Orientation

    def get_AttributSuppl(self):
        return self.AttributSuppl

    def get_Tdeb(self):
        return self.Tdeb

    def get_Tfin(self):
        return self.Tfin

    def get_Commentaire(self):
        return self.Commentaire

    # fonctions qui permettent de donner une valeur(str) a chaque attribut

    def set_ID(self, new_ID):
        self.ID = new_ID

    def set_Nom(self, new_Nom):
        self.Nom = new_Nom

    def set_Lateralisation(self, new_Lateralisation):
        self.Lateralisation = new_Lateralisation

    def set_SegCorporel(self, new_SegCorporel):
        self.SegCorporel = new_SegCorporel

    def set_Orientation(self, new_Orientation):
        self.Orientation = new_Orientation

    def set_AttributSuppl(self, new_AttributSuppl):
        self.AttributSuppl = new_AttributSuppl

    def set_Tdeb(self, new_Tdeb):
        self.Tdeb = new_Tdeb

    def set_Tfin(self, new_Tfin):
        self.Tfin = new_Tfin

    def set_Commentaire(self, new_Commentaire):
        self.Commentaire = new_Commentaire
#########################################################################################################
    

def EcrireSymptome(symptome, nomfichier) :
    """Ecrit un symptome dans un fichier texte dont on specifie le nom"""

    data = symptome.get_attributs()
    with open(nomfichier, 'a') as fichier :
        for attribut in data :
            fichier.write(attribut)
            fichier.write("\t")
        fichier.write("\n")


def EcrireListeSymptome(listeSymptome, nomfichier) :
    """Ecrit une liste de symptomes dans un fichier texte
    
    Chaque symptome est écrit sur une ligne
    Fait appel à la fonction EcrireSymptome
    """
    for symptome in listeSymptome :
        EcrireSymptome(symptome, nomfichier)

def EcrireMetaData(ListeMeta, nomfichier) :
    """Ecrit les metadata d'une annotation dans un fichier texte
    """
    mydate = datetime.date.today()
    with open(nomfichier, 'a') as fichier :
         fichier.write("Metadonnées :\n")
         fichier.write("heure réelle :\tpatient :\tpraticien :\tdate d'annotation : \n")
         fichier.write(f"{ListeMeta[0]}\t{ListeMeta[1]}\t{ListeMeta[2]}\t{mydate}\n\n")
        


##########################################################################################################
if __name__ == "__main__" :
    
    L = []
    for i in range(20) :
        S = Symptome(f"ID{i}", f"Nom{i}", f"Lateralisation{i}", f"SegCorporel{i}", f"Orientation{i}", f"AttributSuppl{i}", f"Tdeb{i}", f"Tfin{i}", f"Commentaire{i}")
        L.append(S)

    meta = ["15h12", "M. Smith", "toto" ]
    nomfichier = 'd:/Unfichiertest.txt'


    EcrireMetaData(meta, nomfichier)
    EcrireListeSymptome(L, nomfichier)