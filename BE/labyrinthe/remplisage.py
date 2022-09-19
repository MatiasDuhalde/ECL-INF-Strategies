import math
import random


class Labyrinthe:
    voisins = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def __init__(self, taille, debut=None, fin=None):
        self.__taille = taille
        if debut != None:
            L, C = debut
            assert (0 <= L < self.__taille and 0 <= C < self.__taille)
            # assert (debut >= 0 and debut < taille * taille)
        if fin != None:
            L, C = debut
            assert (0 <= L < self.__taille and 0 <= C < self.__taille)
        self.__debut = debut  # peut être None. De la forme (L,C)
        self.__fin = fin
        self.__matrice = []

        # On décide que la case debut et fin doivent avoir une distance de (taille/2) en ligne et en col
        self.__distnce_entre_debut_et_fin_not_used = math.ceil(
            taille/2)  # arrondi par exèse de taille/2
        print('labyrinth créé')

    def remplir(self, nb_murs):
        # Fonction utilitaire pour définir debu / fin (ce sont des couples (L,C)
        def fixer_case_debut_fin():  # On vient ici car debut et fin = None. Il faut les fixer
            # On décide que la case debut et fin doivent avoir une distance de DIST (eg. 3) en ligne et en col
            # Fixer les cases début et fin (peuvent être données)

            N = self.__taille  # Pour simplifier les écritures
            num_case_debut = -1
            num_case_fin = -1

            # Pour les tirages random j’ai besoin des ces num case plutot que des tuples (pour debut et fin)
            if num_case_debut not in range(N * N) and num_case_fin not in range(N * N):
                # Si non définis, mettre début (2) et cible (3) sur le contour extérieur
                Top_bande = list(range(N))  # [0.. taille]
                Bottom_bande = list(range(N * N - N, N * N))
                Left_bande = list(range(0, N * N, N))
                Right_bande = list(range(N - 1, N * N, N))
                Les_4_listes = [Top_bande, Bottom_bande, Left_bande, Right_bande]
                # Tirage du début : on choisit l’un de ces 4 liste de contours pour y mettre le début
                quelle_liste_debut = random.randint(0, 3)  # On a 4 listes de contours 0..3
                # On sait que chaucun des 4 listes est de taille N : len(Les_4_listes[quelle_liste])=N
                num_case_debut = Les_4_listes[quelle_liste_debut][random.randint(0, N - 1)]
                # Tirage de fin != debut
                quelle_liste_fin = random.randint(0, 3)
                # Debut est fixé. On ne le touch eplus
                self.__debut = num_case_debut // N, num_case_debut % N

                while True:
                    while quelle_liste_debut == quelle_liste_fin:
                        quelle_liste_fin = random.randint(0, 3)
                    num_case_fin = Les_4_listes[quelle_liste_fin][random.randint(0, N - 1)]
                    if num_case_fin != num_case_debut:
                        break

                self.__fin = num_case_fin // N, num_case_fin % N

        # On met des -1 partout d’abord
        for i in range(0, self.__taille):
            lig = [0 for i in range(self.__taille)]
            self.__matrice.append(lig)

        if self.__debut == None and self.__fin == None:
            fixer_case_debut_fin()
            print("debut / fin = ", self.__debut, self.__fin)
            self.__matrice[self.__debut[0]][self.__debut[1]] = 2
            self.__matrice[self.__fin[0]][self.__fin[1]] = 3
        # Else : l’utilisateur les a déjà fourni
        # Tirage aléatoire de k ’1’ (mur)
        assert (nb_murs > 0 and nb_murs < self.__taille * self.__taille)
        # on a traité d’abord case debut et fin (que l’on cenvertit en un num_case

        num_case_debut = self.__debut[0] * self.__taille + self.__debut[1]
        num_case_fin = self.__fin[0] * self.__taille + self.__fin[1]

        # On met les murs après avoir traité case debut et fin
        for i in range(nb_murs):
            case_mur = random.randint(0, self.__taille * self.__taille - 1)
            if case_mur == num_case_debut or case_mur == num_case_fin:  # recommencer
                continue
            ligne = case_mur // self.__taille
            col = case_mur % self.__taille
            self.__matrice[ligne][col] = 1

    def obtenir_matrice(self):
        return self.__matrice

    def __repr__(self) -> str:
        res = ""
        for i in range(self.__taille):
            res += str(self.__matrice[i]) + "\n"
        return res


if __name__ == "__main__":
    taille = 7
    lab = Labyrinthe(taille)  # sans donner debut/fin. seront générés aléatoirement
    lab.remplir(taille * taille//3)
    print(lab)
    asd = lab.obtenir_matrice()
