"""
This module defines the MetaData class for managing metadata information.

Classes:
    MetaData: Represents metadata for annotations.

"""
class MetaData():
    """
    Represents metadata for annotations.

    Attributes:
        nom (str): The last name of the patient.
        prenom (str): The first name of the patient.
        docteur (str): The name of the doctor who made the annotation.
        dateCrise (str): The date and time of the crisis.
        dateAnnotation (str): The date of the annotation.
    """
    def __init__(self, Nom="", prenom="", dateC="", doc="", dateA=""):
        """
        Initializes a MetaData object.

        Args:
            Nom (str): The last name of the patient. Defaults to an empty string.
            prenom (str): The first name of the patient. Defaults to an empty string.
            dateC (str): The date and time of the crisis. Defaults to an empty string.
            doc (str): The name of the doctor who made the annotation. Defaults to an empty string.
            dateA (str): The date of the annotation. Defaults to an empty string.
        """
        self.nom = Nom
        self.prenom = prenom
        self.docteur = doc
        self.dateCrise = dateC
        self.dateAnnotation = dateA
    
    def get_nom(self):
        """
        Get the last name of the patient.

        Returns:
            str: The last name of the patient.
        """
        return self.nom
    
    def get_prenom(self):
        """
        Get the first name of the patient.

        Returns:
            str: The first name of the patient.
        """
        return self.prenom
    
    def get_docteur(self):
        """
        Get the name of the doctor who made the annotation.

        Returns:
            str: The name of the doctor.
        """
        return self.docteur
    
    def get_dateCrise(self):
        """
        Get the date and time of the crisis.

        Returns:
            str: The date and time of the crisis.
        """
        return self.dateCrise
    
    def get_dateAnnotation(self):
        """
        Get the date of the annotation.

        Returns:
            str: The date of the annotation.
        """
        return self.dateAnnotation

    def set_nom(self, value):
        """
        Set the last name of the patient.

        Args:
            value (str): The last name of the patient.
        """
        self.nom = value

    def set_prenom(self, value):
        """
        Set the first name of the patient.

        Args:
            value (str): The first name of the patient.
        """
        self.prenom = value

    def set_docteur(self, value):
        """
        Set the name of the doctor who made the annotation.

        Args:
            value (str): The name of the doctor.
        """
        self.docteur = value
    
    def set_dateCrise(self, value):
        """
        Set the date and time of the crisis.

        Args:
            value (str): The date and time of the crisis.
        """
        self.dateCrise = value

    def set_dateAnnotation(self, value):
        """
        Set the date of the annotation.

        Args:
            value (str): The date of the annotation.
        """
        self.dateAnnotation = value              

