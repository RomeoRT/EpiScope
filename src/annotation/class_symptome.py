"""
This module defines a Symptome class used for instantiating symptom objects.
"""

class Symptome:
    """
    A class used to instantiate a Symptome object with all its attributes.

    Attributes:
        ID (str): The ID of the symptom.
        Name (str): The name of the symptom.
        Lateralization (str): The lateralization of the symptom.
        Topography (str): The topography of the symptom.
        Orientation (str): The orientation of the symptom.
        AttributSuppl (str): Additional attributes of the symptom.
        Tdeb (str): The start time of the symptom.
        Tfin (str): The end time of the symptom.
        Comment (str): Any additional comments related to the symptom.
    """


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
        """Returns a list containing the values of the object's attributes.

        Returns:
            :obj:`list` of :obj:`str`: A list containing the values of all attributes.
                [ 
                ID,
                Name,
                Lateralization,
                Topography,
                Orientation,
                AttributSuppl,
                Tdeb,
                Tfin,
                Comment  
                ]
        """
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
        """Returns the ID of the symptom."""
        return self.ID

    def get_Name(self):
        """Returns the name of the symptom."""
        return self.Name

    def get_Lateralization(self):
        """Returns the lateralization of the symptom."""
        return self.Lateralization

    def get_Topography(self):
        """Returns the topography of the symptom."""
        return self.Topography

    def get_Orientation(self):
        """Returns the orientation of the symptom."""
        return self.Orientation

    def get_AttributSuppl(self):
        """Returns the additional attributes of the symptom."""
        return self.AttributSuppl

    def get_Tdeb(self):
        """Returns the start time of the symptom."""
        return self.Tdeb

    def get_Tfin(self):
        """Returns the end time of the symptom."""
        return self.Tfin

    def get_Comment(self):

        return self.Comment



    # fonctions qui permettent de donner une valeur(str) a chaque attribut

    def set_ID(self, new_ID):
        """Sets the ID of the symptom."""
        self.ID = new_ID

    def set_Name(self, new_Name):
        """Sets the name of the symptom."""
        self.Name = new_Name

    def set_Lateralization(self, new_Lateralization):
        """Sets the lateralization of the symptom."""
        self.Lateralization = new_Lateralization

    def set_Topography(self, new_Topography):
        """Sets the topography of the symptom."""
        self.Topography = new_Topography

    def set_Orientation(self, new_Orientation):
        """Sets the orientation of the symptom."""
        self.Orientation = new_Orientation

    def set_AttributSuppl(self, new_AttributSuppl):
        """Sets the additional attributes of the symptom."""
        self.AttributSuppl = new_AttributSuppl

    def set_Tdeb(self, new_Tdeb):
        """Sets the start time of the symptom."""
        self.Tdeb = new_Tdeb

    def set_Tfin(self, new_Tfin):
        """Sets the end time of the symptom."""
        self.Tfin = new_Tfin

    def set_Comment(self, new_Comment):
        """Sets any additional comments related to the symptom."""
        self.Comment = new_Comment