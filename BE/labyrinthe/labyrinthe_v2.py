"""
Résoudre le problème du labyrinthe

Algorithme à Essais Successifs (AES), implementation utilisant matrice de numéros et BFS
"""
from collections import deque
from time import time
from remplisage import Labyrinthe

# — libre : -1
# — murs : on note ces cases ’1’
# — départ : 2
# — arrivée : 3
# — occupé / marqué : 4


TAB_DELTA_X_Y = [[0, 1], [0, -1], [1, 0], [-1, 0]]


def initialiser_matrice_des_numeros(mat):
    mat_res = []
    for i, row in enumerate(mat):
        mat_res.append([])
        for el in row:
            if el == 0:
                mat_res[i].append(10000)
            else:
                mat_res[i].append(el)
    return mat_res


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


def un_des_PCC(labyrinthe, mdn, premier_noeud):
    queue = deque([premier_noeud])
    parents = {}
    while len(queue) > 0:
        noeud_courant = queue.popleft()
        x_courant, y_courant = noeud_courant
        if labyrinthe[x_courant][y_courant] == 3:
            path_node = noeud_courant
            path = [path_node]
            while path_node != premier_noeud:
                path_node = parents[path_node]
                path.append(path_node)
            return path[::-1]
        for step in TAB_DELTA_X_Y:
            next_x = x_courant + step[0]
            next_y = y_courant + step[1]
            if prometteur(labyrinthe, (next_x, next_y)):
                if mdn[next_x][next_y] == 3 or mdn[next_x][next_y] == mdn[x_courant][y_courant] + 1:
                    queue.append((next_x, next_y))
                    parents[(next_x, next_y)] = noeud_courant
    return []


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
            print(f'{el}'.ljust(5, ' '), end=' ')
        print()
    print()


if __name__ == '__main__':
    lab = Labyrinthe(10)
    lab.remplir(10)
    offset = 100
    G = lab.obtenir_matrice()
    depart = trouver_depart(G)
    if depart is None:
        print("Pas de départ")
        exit(1)
    matrice_des_numeros = initialiser_matrice_des_numeros(G)

    print_G(G)

    t_1 = time()
    numerotation_des_cases(matrice_des_numeros, G, depart, offset)
    matrice_des_numeros[depart[0]][depart[1]] = offset
    res_final = un_des_PCC(G, matrice_des_numeros, depart)
    t_2 = time()

    print('Matrice des numéros finale :')
    print_G(matrice_des_numeros)

    if res_final:
        print('PCC trouvé :', res_final)
    else:
        print('échec')

    print('Temps de calcul :', t_2 - t_1)
