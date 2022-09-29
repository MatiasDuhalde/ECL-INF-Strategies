"""
Résoudre le problème des cavaliers

Algorithme à Essais Successifs (AES) utilisant matrice de voisins
Code basé sur des slides du cours et annexes
"""
from time import time

import numpy as np
from utils import Case, creer_matrice_avec_bandes


class Echiquier:
    """Échiquier Classe pour résoudre le problème du cavalier
    """

    TAB_DELTA_X_Y = [[1, 2], [1, -2], [-1, 2], [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1]]

    def __init__(self, dimension: int, case_de_depart: Case):
        self.dimension = dimension
        self.nombre_de_cases = dimension * dimension
        self.case_de_depart = (case_de_depart[0] + 2, case_de_depart[1] + 2)
        self.reset()

    def reset(self) -> None:
        """Remettre l'échiquier dans son état initial
        """
        self.__matrice = creer_matrice_avec_bandes(self.dimension)
        self.fixer_case(self.case_de_depart, 1)
        self.__voisins = self.obtenir_matrice_de_voisins()
        self.backtracks = 0
        self.tentatives = 0

    def obtenir_matrice_de_voisins(self) -> np.ndarray:
        """Obtenir la matrice de voisins de l'échiquier

        Returns:
            np.ndarray: Matrice de voisins calculée
        """
        voisins = np.zeros((self.dimension, self.dimension))
        for i in range(self.dimension):
            for j in range(self.dimension):
                for x_offset, y_offset in Echiquier.TAB_DELTA_X_Y:
                    # echiquer a une bande donc il faut ajouter 2
                    x_suivant = i + x_offset + 2
                    y_suivant = j + y_offset + 2
                    if self.prometteur((x_suivant, y_suivant)):
                        voisins[i, j] += 1
        return voisins

    def mise_a_jour_voisins(self, position_actuel: Case, inverse=False) -> None:
        """Mise à jour la matrice de voisins quand la position du cavalier change

        Args:
            position_actuel (Case): position du cavalier
            inverse (bool, optional): Si c'est False, la fonction réduira la quantité de voisins.
                Si c'est True, la fonction augmentera la quantité de voisins. Defaults to False.
        """
        _x, _y = position_actuel
        ajout = 1 if inverse else -1
        for x_offset, y_offset in Echiquier.TAB_DELTA_X_Y:
            x_suivant, y_suivant = _x + x_offset, _y + y_offset
            if self.prometteur((x_suivant, y_suivant)):
                # matrice de voisins n'a pas de bande donc il faut soustraire 2
                self.__voisins[x_suivant - 2][y_suivant - 2] += ajout

    def trouver_meilleurs_voisins_libres(self, position_actuel: Case) -> list[Case]:
        """Trouver la liste de meilleurs voisins libres d'une case

        Args:
            position_actuel (Case): case d'où on retrouve les voisins

        Returns:
            list[Case]: liste de meilleurs voisins trouvée
        """
        k_min = self.trouver_le_premier_voisin_de_degre_minimal_libre(position_actuel)
        if k_min >= 0:
            return self.trouver_tous_les_meilleurs_voisins(position_actuel, k_min)
        # Il n'y a pas de voisins
        return []

    def trouver_le_premier_voisin_de_degre_minimal_libre(self, position_actuel: Case) -> int:
        """Trouver le degré minimal libre (la valeur de la case avec le moins de voisins)

        Args:
            position_actuel (Case): case d'où on retrouve les voisins

        Returns:
            int: valeur de la case avec le moins de voisins
        """
        _x, _y = position_actuel
        # on commence par le maximum (9)
        k_min = 9
        for x_offset, y_offset in Echiquier.TAB_DELTA_X_Y:
            x_suivant, y_suivant = _x + x_offset, _y + y_offset
            if self.prometteur((x_suivant, y_suivant)):
                # matrice de voisins n'a pas de bande donc il faut soustraire 2
                if k_min > self.__voisins[x_suivant - 2][y_suivant - 2]:
                    k_min = self.__voisins[x_suivant - 2][y_suivant - 2]
        return k_min

    def trouver_tous_les_meilleurs_voisins(self, position_actuel: Case, k_min: int) -> list[Case]:
        """Trouver la liste de voisins de la position actuelle où le nombre de voisins est égal à
            k_min

        Args:
            position_actuel (Case): case d'où on retrouve les voisins
            k_min (int): valeur désirée

        Returns:
            list[Case]: liste de voisins trouvée
        """
        meilleurs_voisins = []
        _x, _y = position_actuel
        for x_offset, y_offset in Echiquier.TAB_DELTA_X_Y:
            x_suivant, y_suivant = _x + x_offset, _y + y_offset
            if self.prometteur((x_suivant, y_suivant)):
                # matrice de voisins n'a pas de bande donc il faut soustraire 2
                if k_min == self.__voisins[x_suivant - 2][y_suivant - 2]:
                    meilleurs_voisins.append((x_suivant, y_suivant))
        return meilleurs_voisins

    def prometteur(self, case: Case) -> bool:
        """Vérifier si case est valide pour le cavalier

        Args:
            case (Case): case tentative pour y aller

        Returns:
            bool: True si la case est valide, sinon False
        """
        return not self.is_taken(case)

    def is_taken(self, case: Case) -> bool:
        """Vérifier si la case est déjà occupée

        Args:
            case (Case): case tentative à vérifier

        Returns:
            bool: True si la case est déjà occupée, sinon False
        """
        _x, _y = case
        return self.__matrice[_x, _y] != -1

    def liberer_case(self, case: Case) -> None:
        """Libérer la case désirée (la remettre dans son état initial, sauf case de depart)

        Args:
            case (Case): case à libérer
        """
        self.fixer_case(case, -1)

    def fixer_case(self, case: Case, valeur: int) -> None:
        """Fixer la valeur de la case désirée

        Args:
            case (Case): case désirée
            valeur (int): valeur à fixer
        """
        _x, _y = case
        self.__matrice[_x, _y] = valeur

    def aes_parcour_cavalier_un_succes_suffit(self, derniere_case_traitee: Case,
                                              prochain_num_etape: int) -> bool:
        """Partie récursive (AES) du problème du cavalier

        Args:
            derniere_case_traitee (Case): Case où le cavalier se trouve maintenant
            prochain_num_etape (int): étape actuelle du parcours

        Returns:
            bool: False si l'algorithme ne trouve pas une solution pour l'état actuel, sinon True
        """
        if prochain_num_etape > self.nombre_de_cases:
            return True
        meilleurs_voisins = self.trouver_meilleurs_voisins_libres(derniere_case_traitee)
        for nouvelle_case in meilleurs_voisins:
            self.mise_a_jour_voisins(nouvelle_case)
            self.tentatives += 1
            if self.prometteur(nouvelle_case):
                self.fixer_case(nouvelle_case, prochain_num_etape)
                res = self.aes_parcour_cavalier_un_succes_suffit(
                    nouvelle_case, prochain_num_etape + 1)
                if res:
                    return True
                self.liberer_case(nouvelle_case)
                self.mise_a_jour_voisins(nouvelle_case, True)
                self.backtracks += 1
        return False

    def resoudre(self) -> bool:
        """Résoudre le problème du cavalier

        Returns:
            bool: True s'il est possible pour le chevalier de parcourir tout l'échiquier.
                Sinon, False.
        """
        return self.aes_parcour_cavalier_un_succes_suffit(self.case_de_depart, 2)

    def obtenir_echiquier(self):
        return self.__matrice[2:2+self.dimension, 2:2+self.dimension]

    def __repr__(self) -> str:
        return str(self.__matrice[2:2+self.dimension, 2:2+self.dimension])


if __name__ == '__main__':
    N = int(input("Taille de la matrice ? (>4; défaut 5) ") or 5)
    depart = tuple(
        map(int, (input(f"Départ du cavalier ? (0<=x,y<={N-1}; défaut 0 0) ") or "0 0").split()))

    echiquier = Echiquier(N, depart)

    t_1 = time()
    resultat_final = echiquier.resoudre()
    t_2 = time()

    if resultat_final:
        print('Solution trouvée:')
        print(echiquier)
    else:
        print('Échec')

    print('Nombre de tentatives :', echiquier.tentatives)
    print('Nombre de backtracks :', echiquier.backtracks)
    print(f'Temps de calcul : {t_2 - t_1}s')
