import customtkinter as CTK
import frise.ecriture_fichier as EF
import annotation.class_symptome as SY

############################################################################################################################################
if __name__=="__main__":
# test des fonctions
    
    root = CTK.CTk()

   # test des fonctions 
    L = []
    for i in range(20) :
        S = SY.Symptome(f"ID{i}", f"Nom{i}", f"Lateralisation{i}", f"SegCorporel{i}", f"Orientation{i}", f"AttributSuppl{i}", f"Tdeb{i}", f"Tfin{i}", f"Commentaire{i}")
        L.append(S)

    meta = ["15h12", "M. Smith", "toto" ]
    nomfichier = 'd:/Unfichiertest.txt'


    EF.EcrireMetaData(meta, nomfichier)
    EF.EcrireListeSymptome(L, nomfichier)

    root.mainloop()