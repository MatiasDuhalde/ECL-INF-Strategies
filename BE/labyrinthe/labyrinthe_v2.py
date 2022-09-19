"""
Résoudre le problème du labyrinthe
"""
from remplisage import Labyrinthe

# — libre : -1
# — murs : on note ces cases ’1’
# — départ : 2
# — arrivée : 3
# — occupé / marqué : 4


TAB_DELTA_X_Y = [[0, 1], [0, -1], [1, 0], [-1, 0]]


def numerotation_des_cases(mat_des_numeros, G, noeud_courant, numero_de_cette_case):
    x_courant = noeud_courant[0]
    y_courant = noeud_courant[1]
    if G[x_courant][y_courant] == 3:
        return True
    for offset in TAB_DELTA_X_Y:
        next_x = x_courant + offset[0]
        next_y = y_courant + offset[1]
        if prometteur(G, (next_x, next_y)):
            if G[next_x][next_y] == 2 or G[next_x][next_y] == 3:
                continue
            if mat_des_numeros[next_x][next_y] < numero_de_cette_case:
                continue
            mat_des_numeros[next_x][next_y] = min(
                mat_des_numeros[next_x][next_y], numero_de_cette_case + 1)
            numerotation_des_cases(mat_des_numeros, G, (next_x, next_y),
                                   mat_des_numeros[next_x][next_y])


def trouver_depart(G):
    for i in range(len(G)):
        for j in range(len(G[i])):
            if G[i][j] == 2:
                return i, j
    return None


def prometteur(G, noeud):
    x = noeud[0]
    y = noeud[1]
    return 0 <= x < len(G) and 0 <= y < len(G[x]) and G[x][y] != 1


def print_G(G):
    for i in range(len(G)):
        for j in range(len(G[i])):
            print(G[i][j], end=' ')
        print()
    print()


def initialiser_matrice_des_numeros(G):
    mat = []
    for i in range(len(G)):
        mat.append([])
        for j in range(len(G[i])):
            if G[i][j] == 0:
                mat[i].append(10000000000)
            else:
                mat[i].append(G[i][j])
    return mat


if __name__ == '__main__':
    lab = Labyrinthe(10)
    lab.remplir(10)
    offset = 100
    G = lab.obtenir_matrice()
    depart = trouver_depart(G)
    mat_des_numeros = initialiser_matrice_des_numeros(G)
    print(mat_des_numeros)
    print(depart)
    print_G(G)
    numerotation_des_cases(mat_des_numeros, G, depart, offset)
    print_G(mat_des_numeros)
