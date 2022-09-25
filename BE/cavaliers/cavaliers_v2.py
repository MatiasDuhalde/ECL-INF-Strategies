"""
Résoudre le problème des cavaliers

Algorithme à Essais Successifs (AES), implementation naïve, avec bande
"""
from time import time
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
        self.backtracks = 0
        self.tentatives = 0

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
        x_actuel, y_actuel = derniere_case_traitee
        self.tentatives += 1
        if prochain_num_etape > self.nombre_de_cases:
            return True
        for x_offset, y_offset in Echiquier.TAB_DELTA_X_Y:
            nouvelle_case = (x_actuel + x_offset, y_actuel + y_offset)
            if self.prometteur(nouvelle_case):
                self.fixer_case(nouvelle_case, prochain_num_etape)
                res = self.aes_parcour_cavalier_un_succes_suffit(
                    nouvelle_case, prochain_num_etape + 1)
                if res:
                    return True
                self.liberer_case(nouvelle_case)
                self.backtracks += 1
        return False

    def resoudre(self) -> bool:
        """Résoudre le problème du cavalier

        Returns:
            bool: _description_
        """
        return self.aes_parcour_cavalier_un_succes_suffit(self.case_de_depart, 2)

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
