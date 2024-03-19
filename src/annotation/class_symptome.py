
'''Classe permettant d instancier un objet Symptome avec tous ses attributs
Par exemple ID, Name, Lateralization, segment corporel, Tps debut, Tps fin, Orientation, Attributs suppl, Comment'''

# voir comment utiliser les methodes


class Symptome:



    def __init__(self, ID=None, Name=None, Lateralization=None, Topography=None, Orientation=None, AttributSuppl=None, Tdeb=None, Tfin=None, Comment=None):
        self.ID = ID
        self.Name = Name
        self.Lateralization = Lateralization
        self.Topography = Topography
        self.Orientation = Orientation
        self.AttributSuppl = AttributSuppl
        self.Tdeb = Tdeb
        self.Tfin = Tfin
        self.Comment = Comment



    def get_attributs(self):
        ''' Retourne une liste contenant les valeurs des attributs de l'objet'''
        attributs = [
            self.ID,
            self.Name,
            self.Lateralization,
            self.Topography,
            self.Orientation,
            self.AttributSuppl,
            self.Tdeb,
            self.Tfin,
            self.Comment
        ]
        return attributs    



    # fonctions pour recuperer les attributs separements

    def get_ID(self):
        return self.ID

    def get_Name(self):
        return self.Name

    def get_Lateralization(self):
        return self.Lateralization

    def get_Topography(self):
        return self.Topography

    def get_Orientation(self):
        return self.Orientation

    def get_AttributSuppl(self):
        return self.AttributSuppl

    def get_Tdeb(self):
        return self.Tdeb

    def get_Tfin(self):
        return self.Tfin

    def get_Comment(self):
        return self.Comment



    # fonctions qui permettent de donner une valeur(str) a chaque attribut

    def set_ID(self, new_ID):
        self.ID = new_ID

    def set_Name(self, new_Name):
        self.Name = new_Name

    def set_Lateralization(self, new_Lateralization):
        self.Lateralization = new_Lateralization

    def set_Topography(self, new_Topography):
        self.Topography = new_Topography

    def set_Orientation(self, new_Orientation):
        self.Orientation = new_Orientation

    def set_AttributSuppl(self, new_AttributSuppl):
        self.AttributSuppl = new_AttributSuppl

    def set_Tdeb(self, new_Tdeb):
        self.Tdeb = new_Tdeb

    def set_Tfin(self, new_Tfin):
        self.Tfin = new_Tfin

    def set_Comment(self, new_Comment):
        self.Comment = new_Comment


    


