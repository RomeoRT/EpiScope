

# voir comment utiliser les méthodes


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


    


