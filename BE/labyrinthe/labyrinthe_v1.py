"""
Résoudre le problème du labyrinthe

Algorithme à Essais Successifs (AES), implementation naïve, avec backtracking simple
"""
from time import time
from remplisage import Labyrinthe

# — libre : -1
# — murs : on note ces cases ’1’
# — départ : 2
# — arrivée : 3
# — occupé / marqué : 4


TAB_DELTA_X_Y = [[0, 1], [0, -1], [1, 0], [-1, 0]]


def AES_le_premier_succes_suffit_adapte_au_labyrinthe(labyrinthe, noeud_courant):
    x_courant = noeud_courant[0]
    y_courant = noeud_courant[1]
    if labyrinthe[x_courant][y_courant] == 3:
        return True
    if labyrinthe[x_courant][y_courant] != 2:
        labyrinthe[x_courant][y_courant] = 4
    for offset in TAB_DELTA_X_Y:
        next_x = x_courant + offset[0]
        next_y = y_courant + offset[1]
        if prometteur(labyrinthe, (next_x, next_y)):
            res = AES_le_premier_succes_suffit_adapte_au_labyrinthe(labyrinthe, (next_x, next_y))
            if res:
                return True
            labyrinthe[next_x][next_y] = 0
    return False


def trouver_depart(matrice):
    for i, row in enumerate(matrice):
        for j, el in enumerate(row):
            if el == 2:
                return i, j
    return None


def prometteur(mat, noeud):
    x, y = noeud
    return 0 <= x < len(mat) and 0 <= y < len(mat[x]) and (mat[x][y] == 0 or mat[x][y] == 3)


def print_G(matrice):
    for row in matrice:
        for el in row:
            print(el, end=' ')
        print()
    print()


if __name__ == '__main__':
    lab = Labyrinthe(10)
    lab.remplir(10)
    G = lab.obtenir_matrice()
    depart = trouver_depart(G)
    print(depart)
    print_G(G)

    t_1 = time()
    final_res = AES_le_premier_succes_suffit_adapte_au_labyrinthe(G, depart)
    t_2 = time()

    if final_res:
        print_G(G)
    else:
        print('échec')

    print('Temps de calcul :', t_2 - t_1)
