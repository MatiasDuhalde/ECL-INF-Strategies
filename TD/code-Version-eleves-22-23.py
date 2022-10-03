# Septembre 2022

import random
import math

# Mettre ce booléen à True pour avoir plein de message de trace
TRACE = False


class Noeud:
    def __init__(self, coordonnees, degre=0):
        x, y = coordonnees
        self.__x = x
        self.__y = y
        self.__degre = degre

    # Créer un noeud avec le couple (x,y)
    @classmethod
    def noeud_from_x_y(cls, x_y):
        return cls(x_y)

    @property
    def coordonnees(self):
        return (self.__x, self.__y, self.__degre)

    @coordonnees.setter
    def coordonnees(self, x, y, degre=0):
        self.__x = x
        self.__y = y
        self.__degre = degre

    @property
    def degre(self):
        return self.__degre

    @degre.setter
    def degre(self, degre=0):
        self.__degre = degre

    def distance_euclidienne(self, noeud):
        autre_x, autre_y = noeud.get_coordonnees()
        return math.sqrt((self.__x - autre_x)**2 + (self.__y - autre_y)**2)

    def __str__(self):
        return str((self.__x, self.__y)) + " de degré " + str(self.__degre)

    # Égalité de 2 noeuds (en coordonnées). Vrai si égalité
    def __eq__(self, noeud):
        autre_x, autre_y = noeud.get_coordonnees()
        return self.__x == autre_x and self.__y == autre_y

    # En premier : get, puis set puis deleter
    coordonnees = property(get_coordonnees, set_coordonnees)
    degre = property(get_degre, set_degre)

# ------------------------------------------------------------------------------------------


class Graphe:
    def __init__(self, is_DAG=False):  # pard défaut "non orienté".
        self.vertices_dico = {}
        # entre V1 et V2 (si ar^ête, les couples sont répétés, sinon, dans un seul sens)
        self.edges_dico = {}
        self.is_DAG = is_DAG
        self.racine = None
        self.taille = 0

    def set_racine(self, Node):
        self.racine = Node

    def add_node(self, noeud: Noeud):  # Le noeud : (x,y) +autres infos
        # tester si le noeud n'est aps déjà présent
        x, y, _d = noeud.coordonnees
        if (x, y) not in self.vertices_dico:
            self.vertices_dico[(x, y)] = noeud  # .getInfos_sans_coordonnees()
            self.taille += 1
            self.edges_dico[(x, y)] = []  # pas de edge pour l'instant pour ce noeud

    def get_nodes(self):
        return self.vertices_dico

    def afficher_graphe(self):
        print("\nLes noeuds (vertices) :")
        for k, v in self.vertices_dico.items():
            print(v)
        print("\nLes arêtes (ou les arcs si DAG) :")
        for k, v in self.edges_dico.items():
            print(k, '->', v)

    def get_node_from_son_tuple_de_coordonnees(self, coord_noeud):
        # x,y=coord_noeud # inutile
        return self.vertices_dico[coord_noeud]  # le champe 0 répète les coordonnées

    def add_edge(self, from_coords_v1, to_coords_v2):
        # assert from_coords_v1 in self.vertices_dico and to_coords_v2 in self.vertices_dico
        # Si les noeuds ne sont pas encore dans le graphe, on les ajoute
        if from_coords_v1 not in self.vertices_dico:
            noeud1 = Noeud.noeud_from_x_y(from_coords_v1)
            self.add_node(noeud1)
        else:
            noeud1 = self.get_node_from_son_tuple_de_coordonnees(from_coords_v1)

        if to_coords_v2 not in self.vertices_dico:
            noeud2 = Noeud.noeud_from_x_y(to_coords_v2)
            self.add_node(noeud2)
        else:
            noeud2 = self.get_node_from_son_tuple_de_coordonnees(to_coords_v2)

        if to_coords_v2 not in self.edges_dico[from_coords_v1]:
            self.edges_dico[from_coords_v1].append(to_coords_v2)
            noeud1.degre += 1
            # self.vertices_dico[from_coords_v1].__degre +=1  # Le degré du noeud augmente

        if self.is_DAG:  # et le cas symétrique
            return
        # On met l'arc inverse
        if from_coords_v1 not in self.edges_dico[to_coords_v2]:
            self.edges_dico[to_coords_v2].append(from_coords_v1)
            noeud2.degre += 1
            # self.vertices_dico[to_coords_v2].__degre+=1  # Le degré du noeud augmente

    def get_degre_d_un_noeud(self, coords_noeud):
        infos_du_noeud = self.vertices_dico[coords_noeud]
        return infos_du_noeud[-1]  # le degré = dernier élé de la liste des infos d'un noeud

# -------------------------------
# Ajout d'aretes à la main


def ajouter_aretes(graphe):
    coords_v1 = (13, 14)
    coords_v2 = (10, 10)
    graphe.add_edge(coords_v1, coords_v2)
    coords_v2 = (27, 5)
    graphe.add_edge(coords_v1, coords_v2)
    coords_v1 = (2, 9)
    coords_v2 = (13, 10)
    graphe.add_edge(coords_v1, coords_v2)
    coords_v2 = (4, 20)
    graphe.add_edge(coords_v1, coords_v2)
    coords_v1 = (17, 16)
    coords_v2 = (9, 18)
    graphe.add_edge(coords_v1, coords_v2)
    coords_v2 = (17, 5)
    graphe.add_edge(coords_v1, coords_v2)
    coords_v1 = (13, 10)
    coords_v2 = (13, 14)
    graphe.add_edge(coords_v1, coords_v2)
    coords_v2 = (2, 9)
    graphe.add_edge(coords_v1, coords_v2)
    coords_v1 = (16, 12)
    coords_v2 = (14, 20)
    graphe.add_edge(coords_v1, coords_v2)
    coords_v2 = (19, 7)
    graphe.add_edge(coords_v1, coords_v2)
    coords_v1 = (29, 7)
    coords_v2 = (16, 12)
    graphe.add_edge(coords_v1, coords_v2)
    coords_v2 = (10, 5)
    graphe.add_edge(coords_v1, coords_v2)
    coords_v1 = (17, 5)
    coords_v2 = (13, 14)
    graphe.add_edge(coords_v1, coords_v2)
    coords_v2 = (17, 16)
    graphe.add_edge(coords_v1, coords_v2)
    coords_v1 = (10, 15)
    coords_v2 = (19, 7)
    graphe.add_edge(coords_v1, coords_v2)
    coords_v2 = (9, 18)
    graphe.add_edge(coords_v1, coords_v2)
    coords_v1 = (4, 20)
    coords_v2 = (2, 9)
    graphe.add_edge(coords_v1, coords_v2)
    coords_v2 = (16, 12)
    graphe.add_edge(coords_v1, coords_v2)
    coords_v1 = (9, 18)
    coords_v2 = (17, 16)
    graphe.add_edge(coords_v1, coords_v2)
    coords_v2 = (10, 5)
    graphe.add_edge(coords_v1, coords_v2)
# -------------------------------------------------------


if __name__ == "__main__":

    # =========== Test de la class Noeud ======================
    print("\nDebut test de la classe Noeud".upper())
    print("-"*70)
    n1 = Noeud((random.randint(1, 10), random.randint(1, 10)))
    n2 = Noeud((random.randint(1, 10), random.randint(1, 10)))
    print("n1 = ", n1)
    print("n2 = ", n2)

    if n1 == n2:
        print("n1 = n2")
    else:
        print("n1 != n2")

    print("coordonnées de n1 ", n1.coordonnees)
# =========== Test de la class Graphe ======================
    print("\nDebut test d'un  graphe".upper())
    print("-"*70)
    G_test = Graphe()
    # Initialisation de la matrice
    NB_NOEUDS = 10
    TAILLE_PLAN = 50  # un espace 50 x 50
    for i in range(NB_NOEUDS):
        coords = (random.randint(1, TAILLE_PLAN), random.randint(1, TAILLE_PLAN))
        G_test.add_node((Noeud(coords)))

    liste_des_noeuds = list(G_test.get_nodes().keys())
    print("Les noeuds de ce graphe : ")
    print(liste_des_noeuds)

    # ============================================
    # Création d'un autre graphe
    print("\nDebut test un 2e graphe".upper())
    print("-"*70)
    G = Graphe()

    ajouter_aretes(G)

    print("Affichage de tout le graphe :")
    print("Les noeuds puis les arêtes")
    G.afficher_graphe()
    print("La taille du graphe : ", G.taille)
