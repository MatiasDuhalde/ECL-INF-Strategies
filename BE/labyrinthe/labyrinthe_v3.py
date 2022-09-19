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


def initialiser_matrice_de_probabilites(mat):
    mat_res = []
    for i, row in enumerate(mat):
        mat_res.append([])
        for el in row:
            if el == 0:
                mat_res[i].append(0.25)
            elif el == 3:
                mat_res[i].append(1)
            else:
                mat_res[i].append(0)
    return mat_res


def parcours_probabiliste(mat_de_prob, labyrinthe, noeud_courant, ):
    x_courant, y_courant = noeud_courant
    if labyrinthe[x_courant][y_courant] == 3:
        mat_de_prob[x_courant][y_courant] = 1
        return True
    possibilites = []
    for step in TAB_DELTA_X_Y:
        n_x = x_courant + step[0]
        n_y = y_courant + step[1]
        if prometteur(labyrinthe, (n_x, n_y)) and mat_de_prob[n_x][n_y] >= 0:
            possibilites.append((n_x, n_y))
    for _ in range(len(possibilites)):
        possibilites.sort(key=lambda x: mat_de_prob[x[0]][x[1]])
        next_x, next_y = possibilites.pop()
        mat_de_prob[next_x][next_y] *= 0.9
        if parcours_probabiliste(mat_de_prob, labyrinthe, (next_x, next_y)):
            return True
        mat_de_prob[next_x][next_y] *= 0.5


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
            print(f'{el:.3f}'.ljust(5, ' '), end=' ')
        print()
    print()


if __name__ == '__main__':
    lab = Labyrinthe(5)
    lab.remplir(5)
    G = lab.obtenir_matrice()
    depart = trouver_depart(G)
    if depart is None:
        print("Pas de départ")
        exit(1)
    matrice_de_probabilites = initialiser_matrice_de_probabilites(G)

    print_G(G)

    t_1 = time()
    parcours_probabiliste(matrice_de_probabilites, G, depart)
    t_2 = time()

    print('Matrice de probabilités finale :')
    print_G(matrice_de_probabilites)

    print('Temps de calcul :', t_2 - t_1)
