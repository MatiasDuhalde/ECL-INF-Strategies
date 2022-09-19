# Mars 2019
# Code parcours en profondeur récursif (sans trajet) donné aux élèves

class Labyrinthe:
    voisins = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # variable de classe

    def __init__(self, taille, debut=None, fin=None):
        # initialisation de la matrice.

        """
        self.__matrice = [
            [0, 2, 0, 0, 0],
            [0, 1, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1],
            [0, 3, 1, 1, 0]]

        self.__taille=len(self.__matrice[0])
        self.__case_debut = (0,1);
        self.__case_fin = (4, 1);
        self.afficher()
        """
        self.__matrice = [
                [2, 1, 0, 0],
                [0, 1, 0, 3],
                [0, 0, 0, 0],
                [0, 1, 0, 1]
            ]

        trajet = []
        self.__taille=len(self.__matrice[0])
        self.__case_debut = (0, 0);
        self.__case_fin = (1, 3);

    def remplir(self, nb_murs):
        # Avec Tirage aléatoire de des '1' (mur). Il y en aura nb_murs
        pass

    def afficher(self):
        for l in range(self.__taille):
            print(self.__matrice[l])

    # étant donné une case, est-ce que cette case est dans la matrice et est-elle libre ?
    def prometteur(self, case_a_tester):
        L, C = case_a_tester
        return 0 <= L < self.__taille and 0 <= C < self.__taille and (
        self.__matrice[L][C] == 0 or self.__matrice[L][C] == 3)

    # La fonction de parcours récursif en profondeur
    def AES(self, case_actuelle):
        (L, C) = case_actuelle
        if self.__matrice[L][C] == 3:  # On est arrivé
            # return True

            print("Une solution :"); self.afficher()
            input("Une autre sol ?????")
            return False


        for i in range(4):  # 4  voisins possibles
            (next_x, next_y) = (L + Labyrinthe.voisins[i][0], C + Labyrinthe.voisins[i][1])
            if self.prometteur((next_x, next_y)):
                if self.__matrice[next_x][next_y] != 3: self.__matrice[next_x][next_y] = 4

                if self.AES((next_x, next_y)): return True
                # On n'a pas réussi à utiliser cette case. Remettre sa valeur initiale (sauf pour 3)
                # Needed ?
                # Si si car on aura besoin de reconstituer le trajet (avec les '4')
                # if self.__matrice[next_x][next_y] != 3: self.__matrice[next_x][next_y] = 0
        return False

    def traverser(self):
        if self.AES(self.__case_debut):
            print('Il y a une route : suivez les 4 depuis le début à la fin !')
            print('**** Ou écrire la fonction qui reconstitue le trajet ! ****')
        else:
            print('Pas de route')


if __name__ == "__main__":
    # Ex avec debut et fin fournis lab = Labyrinthe(5, 0, 3)
    lab = Labyrinthe(7)  # Taille=7. Sans donner debut/fin. seront générés aléatoirement

    lab.traverser()
    lab.afficher()

"""
TRACE

[0, 2, 0, 0, 0]
[0, 1, 0, 0, 1]
[0, 0, 0, 0, 0]
[0, 1, 1, 1, 1]
[0, 3, 1, 1, 0]
Il y a une route : suivez les 4 depuis le début à la fin !
**** Ou écrire la fonction qui reconstitue le trajet ! ****
[0, 2, 4, 4, 0]
[0, 1, 0, 4, 1]
[4, 4, 4, 4, 0]
[4, 1, 1, 1, 1]
[4, 3, 1, 1, 0]
"""

"""
D'autres matrices


"""