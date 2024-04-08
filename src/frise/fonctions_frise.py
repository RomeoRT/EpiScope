import matplotlib.pyplot as plt
import numpy as np

"""
# pas git 
from class_symptome import Symptome
"""
from annotation.class_symptome import Symptome

def chercherElt(list):
    """Cherche s'il y a un élément manquant dans une liste de chiffre 0,1,2,3,4,5,..."""
    if len(list) != 0 :
        list = sorted(list)
        last = list[-1]
        for i in range(last):
            if not(i in list):
                return i
        return last+1
    else :
        return 0

def chevauchement(liste, symp, current_index, levels):
    """ Gère le problème de superposition visuelle des symptômes.

    Args:
        liste (list): liste des symptomes avec début et fin
        symp (:obj:`Symptome`): symptome actuel.
        current_index (int): indice du symp actuel dans la liste.
    
    Return: 
        int: niveau y où afficher le rectangle. 
        """
    level = 0
    list = []
    for i in range(len(levels)):
        if (float(liste[i][2])+0.5 > float(symp[1])) : # and (float(liste[i][2]) > float(symp[1]))
            list.append(levels[i][1])
    level = chercherElt(list)
    levels.append([current_index, level])

    return level

def on_text_click(event):
    """Affiche l'annotation lorsque le texte est cliqué."""
    for annotation, rect in zip(annotations, rects):
        if rect.contains(event)[0]:
            annotation.set_visible(True)
        else:
            annotation.set_visible(False)
    plt.draw()

def afficher_frise(liste):
    """ Affiche la frise chronologique des symptômes.
    Args:
        liste (:obj:list of :obj:list): liste des symptomes où chaque élément est une liste [Name, début, fin, Lateralization, seg corporel, orientation, attribut suppl, Comment, tdeb_str, tfin_str]. 
    """
    liste = sorted(liste, key=lambda x: float(x[1]))
    levels = []
    fig, ax = plt.subplots()

    global annotations, rects  # Pour conserver les annotations et les rectangles en mémoire
    annotations = []  # Liste pour stocker les annotations
    rects = []  # Liste pour stocker les rectangles
   
    for i, symp in enumerate(liste):
        y = chevauchement(liste, symp, i, levels) / 1.5
        rect = plt.Rectangle((float(symp[1]), y), float(symp[2]) - float(symp[1]), 0.4, color=tuple((np.random.rand(3) * 0.7 + 0.3).tolist())) #couleurs[i % len(couleurs)]
        ax.add_patch(rect)
        rects.append(rect)
        
        text = plt.text(float(symp[1]) + (float(symp[2]) - float(symp[1])) / 2, y + 0.15, symp[0], va='center', ha='center', zorder=2)

        # Ajouter les informations du symptôme comme une annotation sur le texte
        if symp[3] != "":
            symp[3] = f"\nID: {symp[3]}"
        if symp[4] != "":
            symp[4] = f"\nLateralization: {symp[4]}"
        if symp[5] != "":
            symp[5] = f"\nTopography: {symp[5]}"
        if symp[6] != "":
            symp[6] = f"\nOrientation: {symp[6]}"        
        if symp[7] != "":
            symp[7] = f"\nAdditionnal Attribute: {symp[7]}"
        if symp[8] != "":
            symp[8] = f"\nComment: {symp[8]}"
        
        annotation = ax.annotate(f"{symp[0]}\nStart: {symp[9]}End: {symp[10]}{symp[3]}{symp[4]}{symp[5]}{symp[6]}{symp[7]}{symp[8]}", 
                                xy=(float(symp[1]) + (float(symp[2]) - float(symp[1])) / 2, y + 0.15),
                                bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle="->"), zorder=3)
        annotation.set_visible(False)  # Rendre l'annotation initialement invisible
        annotations.append(annotation)

    ax.set_xlim(0, max(float(symp[2]) for symp in liste) + 5)
    ax.set_ylim(0, len(liste))

    plt.gca().get_yaxis().set_visible(False)
    plt.xlabel("Time (seconds)")
    plt.title("Patient 1")

    fig.canvas.mpl_connect('button_press_event', on_text_click)

    plt.show()

if __name__=="__main__":
    # Création d'instances de la classe Symptome pour tester l'éditeur
    Symp1 = Symptome(ID="", Name="symp1", Lateralization="droite", Topography="", Orientation="", AttributSuppl="", Tdeb="00:00:01", Tfin="00:00:05", Comment="")
    Symp2 = Symptome(ID="", Name="symp2", Lateralization="", Topography="segment cor", Orientation="", AttributSuppl="", Tdeb="00:00:06", Tfin="00:00:08", Comment="")
    Symp3 = Symptome(ID="", Name="symp3", Lateralization="gauche", Topography="", Orientation="orietation", AttributSuppl="", Tdeb="00:00:03", Tfin="00:00:09", Comment="")
    Symp4 = Symptome(ID="", Name="symp4", Lateralization="", Topography="", Orientation="", AttributSuppl="", Tdeb="00:00:09", Tfin="00:00:12", Comment="")

    L = [Symp1, Symp2, Symp3, Symp4]
    newL=[]

    for symp in L:
        Name = symp.get_Name()
        # Transformer la chaine str du temps de début en float
        tdeb_str = symp.get_Tdeb()
        hd, md, sd = tdeb_str.split(":")
        hd = int(hd)
        md = int(md)
        sd = int(sd)
        debut = hd * 3600 + md * 60 + sd
        # Pareil pour le temps de fin
        tfin_str = symp.get_Tfin()
        hf, mf, sf = tfin_str.split(":")
        hf = int(hf)
        mf = int(mf)
        sf = int(sf)
        fin = hf * 3600 + mf * 60 + sf

        id = symp.get_ID()
        lat = symp.get_Lateralization()
        segcor = symp.get_Topography()
        orient = symp.get_Orientation()
        attsup = symp.get_AttributSuppl()
        comm = symp.get_Comment()


        newL.append([Name, debut, fin, id, lat, segcor, orient, attsup, comm, tdeb_str, tfin_str])

    newL = sorted(newL, key=lambda x: float(x[1]))
    afficher_frise(newL)


