"""
01 décembre 2020

Les Ronds = Blancs ('B'), Croix = Noirs
Echiquier = [LB, LN, LV]
Lancer ce code et voir les meilleures cases à jouer pour chhaque joueur

L'échiquier est déjà rempli par 2 ronds et 2 croix.
"""


def la_case_est_sur_la_diagonale(echiquier, case, No_diag):
    lig, col = case
    if No_diag == 1:
        if lig == col:  # 1e diagonale
            return True
    elif lig+col == 4:  # 2e diagonale diagonale
        return True
    else:
        return False

# Trouver le nbr de pion de couleur "couleur" sur une diagonale


# Diagonale 1 : gauche-droite , 2: droite-gauche
def combien_de_Coul_sur_une_diagonale(echiquier, case, No_diag=1, couleur='B'):
    # Echiquier = [LB, LN, LV] et LB=liste des cases (l,c) des blancs, LN : pou rles blancs, LV= cases vides
    if not la_case_est_sur_la_diagonale(echiquier, case, No_diag):
        return 0
    LB, LN, LV = echiquier
    Liste = LB if couleur == 'B' else LN
    temp_lst = [1 for (l, c) in Liste if l == c] if No_diag == 1 else [
        1 for (l, c) in Liste if l+c == 4]
    return sum(temp_lst)

# Trouver le nbr de pion de couleur "couleur" sur une ligne ou une colonne


def combien_de_Coul_sur_ligne(echiquier, lig=1, couleur='B'):
    # Echiquier = [LB, LN, LV] et LB=liste des cases (l,c) des blancs, LN : pou rles blancs, LV= cases vides
    LB, LN, LV = echiquier
    Liste = LB if couleur == 'B' else LN
    return sum([1 for (l, c) in Liste if lig == l])


def combien_de_Coul_sur_colonne(echiquier, col=1, couleur='B'):
    # Echiquier = [LB, LN, LV] et LB=liste des cases (l,c) des blancs, LN : pou rles blancs, LV= cases vides
    LB, LN, LV = echiquier
    Liste = LB if couleur == 'B' else LN
    return sum([1 for (l, c) in Liste if col == c])


def la_couleur_opposee_a(Couleur):
    return 'N' if Couleur == 'B' else 'N'


def valeur_d_une_case(echiquier, couleur, case):
    lig, col = case  # la case est de la forme "(ligne, colonne)"
    NL1 = combien_de_Coul_sur_ligne(echiquier, lig, couleur)
    Adversaire = la_couleur_opposee_a(couleur)  # la couleur de l'adversaire de "Couleur"
    NL2 = combien_de_Coul_sur_ligne(echiquier, lig, Adversaire)
    #print(f"Pour la case {case}, NL1, NL2 ", NL1, NL2)
    Val_ligne = NL1 - NL2

    NC1 = combien_de_Coul_sur_colonne(echiquier, col, couleur)
    NC2 = combien_de_Coul_sur_colonne(echiquier, col, Adversaire)
    #print(f"Pour la case {case}, NC1, NC2 ", NC1, NC2)
    Val_colonne = NC1 - NC2

    # 0 si on n'est pas sur la première diagonale
    ND1_1 = combien_de_Coul_sur_une_diagonale(echiquier, case, 1, couleur)
    # 0 si on n'est pas sur la première diagonale
    ND1_2 = combien_de_Coul_sur_une_diagonale(echiquier, case, 1, Adversaire)
    #print(f"Pour la case {case}, ND1_1, ND1_2 ", ND1_1, ND1_2)
    Val_diagonale_1 = ND1_1 - ND1_2

    # 0 si on n'est pas sur la première diagonale
    ND2_1 = combien_de_Coul_sur_une_diagonale(echiquier, case, 2, couleur)
    # 0 si on n'est pas sur la première diagonale
    ND2_2 = combien_de_Coul_sur_une_diagonale(echiquier, case, 2, Adversaire)
    #print(f"Pour la case {case}, ND2_1, ND2_2 ", ND2_1, ND2_2)
    Val_diagonale_2 = ND2_1 - ND2_2

    g = Val_ligne**2 + Val_colonne**2 + Val_diagonale_1**2 + Val_diagonale_2**2
    return g


if __name__ == "__main__":
    # On va dire : les ronds=Blancs (donc LB), les croix=Noirs (donc LN)

    # =========== EXEMPLE 1 ==================
    # LB=[(1,1),(3,2)];  LN=[(1,2),(2,2)] ; LV=[(1,3), (2,1), (2,3), (3,1), (3,3)]
    """
    Pour la couleur B, on a trouvé la liste des valeurs : 
    {(1, 3): -1, (2, 1): 0, (2, 3): -1, (3, 1): 1, (3, 3): 1}
    le meilleur coup à jouer pour la couleur B = (3, 1) dont la valeur =1
    ------------------------------------------------------------
    Pour la couleur N, on a trouvé la liste des valeurs : 
    {(1, 3): 0, (2, 1): 0, (2, 3): 0, (3, 1): 0, (3, 3): 0}
    le meilleur coup à jouer pour la couleur N = (1, 3) dont la valeur =0
    """

    # =========== EXEMPLE 2 ==================
    # LB=[(1,2),(2,1), (2,2)];  LN=[(1,1),(2,3), (3,2)] ; LV=[(1,3), (3,1), (3,3)]
    """
   Pour la couleur B, on a trouvé la liste des valeurs : 
   {(1, 3): 0, (3, 1): 0, (3, 3): -2}
   le meilleur coup à jouer pour la couleur B = (1, 3) dont la valeur =0
   ------------------------------------------------------------
   Pour la couleur N, on a trouvé la liste des valeurs : 
   {(1, 3): 0, (3, 1): 0, (3, 3): 0}
   le meilleur coup à jouer pour la couleur N = (1, 3) dont la valeur =0
   """

    # =========== EXEMPLE 3 ==================
    LB = [(1, 2), (2, 2)]
    LN = [(1, 1), (2, 1)]
    LV = [(1, 3), (2, 3), (3, 1), (3, 2), (3, 3)]
    echiquier = [LB, LN, LV]
    print("Les Blancs = ", LB, "Les Noirs = ", LB, "\nLes Vides = ", LV, "\n")

    """ 
   Pour la couleur B, on a trouvé la liste des valeurs : 
   (1, 3): 1, (2, 3): 0, (3, 1): -7, (3, 2): 8, (3, 3): 0}
   le meilleur coup à jouer pour la couleur B = (3, 2) dont la valeur =8
   ------------------------------------------------------------
   Pour la couleur N, on a trouvé la liste des valeurs : 
   {(1, 3): 0, (2, 3): 0, (3, 1): 0, (3, 2): 0, (3, 3): 0}
   le meilleur coup à jouer pour la couleur N = (1, 3) dont la valeur =0
   """

    # =========== EXEMPLE 3 ==================
    LB = [(1, 2), (2, 2), (3, 3)]
    LN = [(1, 1), (2, 1), (2, 3)]
    LV = [(1, 3),  (3, 1), (3, 2)]
    echiquier = [LB, LN, LV]
    print("Les Blancs = ", LB, "Les Noirs = ", LB, "\nLes Vides = ", LV, "\n")

    # Pour les 'B' (Ronds), on va calculer pour chacune des cases vides (de la liste LV : liste vide)
    #     la valeur de celle-ci à l'aide d'une fonction cubique Puis on affiche ces cases avec leur
    #     valeur + la meilleure case à jouer pour les 'B'
    # Ensuite, on fera la même chose pour les "Ns""
    #  La meilleure case est celle de valeur maximale mais il se peut que d'autres
    #  cases aient la même valeur. On prend la 1ere.

    couleur = 'B'
    dico_valeurs_pour_couleur = {case: valeur_d_une_case(echiquier, couleur, case) for case in LV}
    print(
        f"Pour la couleur {couleur}, on a trouvé la liste des valeurs : \n{dico_valeurs_pour_couleur}")

    liste_cles_du_dico_trie = sorted(dico_valeurs_pour_couleur,
                                     key=dico_valeurs_pour_couleur.get, reverse=True)
    print(
        f"le meilleur coup à jouer pour la couleur {couleur} = {liste_cles_du_dico_trie[0]} dont la valeur ={dico_valeurs_pour_couleur[liste_cles_du_dico_trie[0]]}")
    print('-'*60)
    couleur = 'N'
    dico_valeurs_pour_couleur = {case: valeur_d_une_case(echiquier, couleur, case) for case in LV}
    print(
        f"Pour la couleur {couleur}, on a trouvé la liste des valeurs : \n{dico_valeurs_pour_couleur}")
    liste_cles_du_dico_trie = sorted(dico_valeurs_pour_couleur,
                                     key=dico_valeurs_pour_couleur.get, reverse=True)
    print(
        f"le meilleur coup à jouer pour la couleur {couleur} = {liste_cles_du_dico_trie[0]} dont la valeur ={dico_valeurs_pour_couleur[liste_cles_du_dico_trie[0]]}")

    """
   Echiquier =  [[(1, 1), (3, 2)], [(1, 2), (2, 2)], [(1, 3), (2, 1), (2, 3), (3, 1), (3, 3)]]
   Pour la couleur B, on a trouvé la liste des valeurs : 
   {(1, 3): -1, (2, 1): 0, (2, 3): -1, (3, 1): 1, (3, 3): 1}
   le meilleur coup à jouer pour la couleur B = (3, 1) dont la valeur =1
   ------------------------------------------------------------
   Pour la couleur N, on a trouvé la liste des valeurs : 
   {(1, 3): 0, (2, 1): 0, (2, 3): 0, (3, 1): 0, (3, 3): 0}
   le meilleur coup à jouer pour la couleur N = (1, 3) dont la valeur =0

   """
