"""
Résoudre le problème des cavaliers

Code basé sur des slides du cours
"""
import numpy as np

TAB_DELTA_X_Y = [[1, 2], [1, -2], [-1, 2], [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1]]


def creer_matrice(dim):
    """Créer une matrice carrée de taille n (avec des bandes)"""
    m_base = np.zeros((dim + 4, dim + 4))
    for i in range(2, dim + 2):
        for j in range(2, dim + 2):
            m_base[i][j] = -1
    return m_base


def calculer_voisins(matrice, dim):
    voisins = np.zeros((dim, dim))
    for i in range(dim):
        for j in range(dim):
            for k in range(8):
                next_x = i + TAB_DELTA_X_Y[k][0] + 2
                next_y = j + TAB_DELTA_X_Y[k][1] + 2
                if prometteur(matrice, next_x, next_y):
                    voisins[i][j] += 1
    return voisins


def mise_a_jour_voisins(matrice, voisins, pos):
    x, y = pos
    for k in range(8):
        next_x, next_y = x + TAB_DELTA_X_Y[k][0], y + TAB_DELTA_X_Y[k][1]
        if not prometteur(matrice, next_x, next_y):
            continue
        voisins[next_x - 2][next_y - 2] -= 1


def remise_a_jour_voisins(matrice, voisins, pos):
    x, y = pos
    for k in range(8):
        next_x, next_y = x + TAB_DELTA_X_Y[k][0], y + TAB_DELTA_X_Y[k][1]
        if not prometteur(matrice, next_x, next_y):
            continue
        voisins[next_x - 2][next_y - 2] += 1


def trouver_meilleurs_voisins_libres(matrice, matrice_voisins, pos_cavalier):
    min_k = trouver_le_premier_voisin_de_degre_minimal_libre(matrice, matrice_voisins, pos_cavalier)
    if min_k >= 0:
        return trouver_tous_les_best_voisins(matrice, matrice_voisins, pos_cavalier, min_k)
    return []


def trouver_le_premier_voisin_de_degre_minimal_libre(matrice, matrice_voisins, pos_cavalier):
    x, y = pos_cavalier
    min_k = 9
    nx_k, ny_k = -1, -1
    for k in range(8):
        nx, ny = x + TAB_DELTA_X_Y[k][0], y + TAB_DELTA_X_Y[k][1]
        if not prometteur(matrice, nx, ny):
            continue
        if min_k > matrice_voisins[nx - 2][ny - 2]:
            min_k = matrice_voisins[nx - 2][ny - 2]
            nx_k, ny_k = nx, ny
    return min_k


def trouver_tous_les_best_voisins(matrice, matrice_voisins, pos_cavalier, min_k):
    best_voisins = []
    x, y = pos_cavalier
    for z in range(8):
        nx, ny = x + TAB_DELTA_X_Y[z][0], y + TAB_DELTA_X_Y[z][1]
        if not prometteur(matrice, nx, ny):
            continue
        if min_k == matrice_voisins[nx - 2][ny - 2]:
            best_voisins.append((nx, ny))
    return best_voisins


def AES_parcours_cavalier_un_succes_suffit(echiquier, taille, voisins, derniere_case_traitee,
                                           prochain_num_etape, compteurs):
    compteurs[0] += 1
    if prochain_num_etape > taille * taille:
        return True
    best_voisins = trouver_meilleurs_voisins_libres(echiquier, voisins, derniere_case_traitee)
    for best_voisin in best_voisins:
        next_x, next_y = best_voisin[0], best_voisin[1]
        mise_a_jour_voisins(echiquier, voisins, best_voisin)
        if prometteur(echiquier, next_x, next_y):
            echiquier[next_x][next_y] = prochain_num_etape
            res = AES_parcours_cavalier_un_succes_suffit(
                echiquier, taille, voisins, (next_x, next_y), prochain_num_etape + 1, compteurs)
            if res:
                return True
            echiquier[next_x][next_y] = -1
            remise_a_jour_voisins(echiquier, voisins, best_voisin)
            compteurs[1] += 1
    return False


def prometteur(echiquier, next_x, next_y):
    return echiquier[next_x][next_y] == -1


if __name__ == '__main__':
    N = int(input("Taille de la matrice ? "))
    depart = tuple(map(int, input("Départ du cavalier ? ").split()))
    real_depart = (depart[0] + 2, depart[1] + 2)

    print("Taille : ", N)
    print("Départ : ", depart)

    G = creer_matrice(N)
    V = calculer_voisins(G, N)
    G[real_depart[0], real_depart[1]] = 1

    prochaine_numero = 2

    stats = [0, 0]

    final_res = AES_parcours_cavalier_un_succes_suffit(
        G, N, V, real_depart, prochaine_numero, stats)
    if final_res:
        for row in range(2, N + 2):
            print(G[2:N + 2, row])
    else:
        print('échec')
    print('Nombre de tentatives :', stats[0])
    print('Nombre de backtracks :', stats[1])
