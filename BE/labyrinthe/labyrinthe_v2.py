"""
Résoudre le problème du labyrinthe
"""
from time import time
from remplisage import Labyrinthe

# — libre : -1
# — murs : on note ces cases ’1’
# — départ : 2
# — arrivée : 3
# — occupé / marqué : 4


TAB_DELTA_X_Y = [[0, 1], [0, -1], [1, 0], [-1, 0]]


def initialiser_matrice_des_numeros(mat):
    mat = []
    for i, row in enumerate(mat):
        mat.append([])
        for el in row:
            if el == 0:
                mat[i].append(10000000000)
            else:
                mat[i].append(el)
    return mat


def numerotation_des_cases(mat_des_numeros, labyrinthe, noeud_courant, numero_de_cette_case):
    x_courant, y_courant = noeud_courant
    if labyrinthe[x_courant][y_courant] == 3:
        return True
    for step in TAB_DELTA_X_Y:
        next_x = x_courant + step[0]
        next_y = y_courant + step[1]
        if prometteur(labyrinthe, (next_x, next_y)):
            if labyrinthe[next_x][next_y] == 2 or labyrinthe[next_x][next_y] == 3:
                continue
            if mat_des_numeros[next_x][next_y] < numero_de_cette_case:
                continue
            mat_des_numeros[next_x][next_y] = min(
                mat_des_numeros[next_x][next_y], numero_de_cette_case + 1)
            numerotation_des_cases(mat_des_numeros, labyrinthe, (next_x, next_y),
                                   mat_des_numeros[next_x][next_y])


def trouver_depart(matrice):
    for i, row in enumerate(matrice):
        for j, el in enumerate(row):
            if el == 2:
                return i, j
    return None


def prometteur(mat, noeud):
    x, y = noeud
    return 0 <= x < len(mat) and 0 <= y < len(mat[x]) and mat[x][y] != 1


def print_G(matrice):
    for row in matrice:
        for el in row:
            print(el, end=' ')
        print()
    print()


if __name__ == '__main__':
    lab = Labyrinthe(10)
    lab.remplir(10)
    offset = 100
    G = lab.obtenir_matrice()
    depart = trouver_depart(G)
    matrice_des_numeros = initialiser_matrice_des_numeros(G)
    print(matrice_des_numeros)
    print(depart)
    print_G(G)

    t_1 = time()
    numerotation_des_cases(matrice_des_numeros, G, depart, offset)
    t_2 = time()

    print_G(matrice_des_numeros)

    print('Temps de calcul :', t_2 - t_1)
