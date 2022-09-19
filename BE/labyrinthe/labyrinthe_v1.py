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


def AES_le_premier_succes_suffit_adapte_au_labyrinthe(G, noeud_courant):
    x_courant = noeud_courant[0]
    y_courant = noeud_courant[1]
    if G[x_courant][y_courant] == 3:
        return True
    if G[x_courant][y_courant] != 2:
        G[x_courant][y_courant] = 4
    for offset in TAB_DELTA_X_Y:
        next_x = x_courant + offset[0]
        next_y = y_courant + offset[1]
        if prometteur(G, (next_x, next_y)):
            res = AES_le_premier_succes_suffit_adapte_au_labyrinthe(G, (next_x, next_y))
            if res:
                return True
            G[next_x][next_y] = 0
    return False


def trouver_depart(G):
    for i in range(len(G)):
        for j in range(len(G[i])):
            if G[i][j] == 2:
                return i, j
    return None


def prometteur(G, noeud):
    x = noeud[0]
    y = noeud[1]
    return 0 <= x < len(G) and 0 <= y < len(G[x]) and (G[x][y] == 0 or G[x][y] == 3)


def print_G(G):
    for i in range(len(G)):
        for j in range(len(G[i])):
            print(G[i][j], end=' ')
        print()
    print()


if __name__ == '__main__':
    lab = Labyrinthe(10)
    lab.remplir(10)
    G = lab.obtenir_matrice()
    depart = trouver_depart(G)
    print(depart)
    print_G(G)
    final_res = AES_le_premier_succes_suffit_adapte_au_labyrinthe(G, depart)
    if final_res:
        print_G(G)
    else:
        print('échec')
