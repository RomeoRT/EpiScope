import matplotlib.pyplot as plt
import numpy as np
import mplcursors



def chercherElt(list):
    """cherche s'il y a un élément manquant dans une liste de chiffre 0,1,2,3,4,5,...
    return: l'élément manquant ou l'élément suivant le dernier le cas échéant"""

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
    """ liste: liste des symptomes avec début et fin
        symp: symptome actuel
        current_index: indice du symp actuel dans la liste.
    Return: niveau y où afficher le rectangle """

    level = 0
    list = []
    for i in range(len(levels)):
        if (float(liste[i][2])+0.5 > float(symp[1])) : # and (float(liste[i][2]) > float(symp[1]))
            list.append(levels[i][1])
    level = chercherElt(list)
    levels.append([current_index, level])

    return level





def afficher_frise(liste):
    """ Affiche une frise chronologique avec gestion du chevauchement
        liste: liste des symptomes où chaque élément est une liste [nom, début, fin] """
    
    liste = sorted(liste, key=lambda x: float(x[1]))
    levels = []
    fig, ax = plt.subplots()

    annotations = []  # Liste pour stocker les annotations
   
    for i, symp in enumerate(liste):
        y = chevauchement(liste, symp, i, levels) / 1.5
        rect = plt.Rectangle((float(symp[1]), y), float(symp[2]) - float(symp[1]), 0.4, color=tuple((np.random.rand(3) * 0.7 + 0.3).tolist())) #couleurs[i % len(couleurs)]
        ax.add_patch(rect)

#        ax.text(float(symp[1]) + (float(symp[2]) - float(symp[1])) / 2, y + 0.15, symp[0], va='center', ha='center')
        
        text = ax.text(float(symp[1]) + (float(symp[2]) - float(symp[1])) / 2, y + 0.15, symp[0], va='center', ha='center')

        # Ajouter les informations du symptôme comme une annotation sur le texte
        annotation = ax.annotate(f"{symp[0]}\nDébut: {symp[1]}\nFin: {symp[2]}", 
                                xy=(float(symp[1]) + (float(symp[2]) - float(symp[1])) / 2, y + 0.15),
                                xytext=(0, 10), textcoords="offset points",
                                bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle="->"))
        annotation.set_visible(False)
        annotations.append(annotation)

    ax.set_xlim(0, max(float(symp[2]) for symp in liste) + 5)
    ax.set_ylim(0, len(liste))
#
#    annot = ax.annotate("", xy=(0, 0), xytext=(0, 0), textcoords="offset points", bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle="->"))
#    annot.set_visible(False)

    '''
    # Apparence de l'axe des x pour qu'il ressemble à une flèche
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_position('zero')  # Place l'axe des x à la position zéro
    ax.xaxis.set_ticks_position('bottom')
    '''

    plt.gca().get_yaxis().set_visible(False)
    plt.xlabel("Time (seconds)")
    plt.title("Patient 1")

    '''# Utilisation de mplcursors pour afficher les annotations au survol
    cursor = mplcursors.cursor(hover=True)

    @cursor.connect("add")
    def on_add(sel):
        # Fonction appelée lors de l'ajout d'un curseur
        symbole = sel.annotation.get_text()
        for annotation in annotations:
            annotation.set_visible(False)
            if symbole == annotation.get_text():
                annotation.set_visible(True)
                sel.annotation.set_text(annotation.get_text())
'''
    plt.show()