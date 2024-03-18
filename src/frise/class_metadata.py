class MetaData():
    def __init__(self, Nom="", prenom="", dateC="", doc="", dateA=""):
        self.nom = Nom
        self.prenom = prenom
        self.docteur = doc
        self.dateCrise = dateC
        self.dateAnnotation = dateA
    
    def get_nom(self):
        return self.nom
    
    def get_prenom(self):
        return self.prenom
    
    def get_docteur(self):
        return self.docteur
    
    def get_dateCrise(self):
        return self.dateCrise
    
    def get_dateAnnotation(self):
        return self.dateAnnotation

    def set_nom(self, value):
        self.nom = value

    def set_prenom(self, value):
        self.prenom = value

    def set_docteur(self, value):
        self.docteur = value
    
    def set_dateCrise(self, value):
        self.dateCrise = value

    def set_dateAnnotation(self, value):
        self.dateAnnotation = value              

