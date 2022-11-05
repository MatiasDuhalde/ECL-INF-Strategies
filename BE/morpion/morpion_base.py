"""Travaux à rendre 1"""
from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from random import choice
from typing import Union

Case = tuple[int, int]

# (dict_cases_joueurs, liste_cases_vides, dernière_case_placée, dernière case enlevée)
Plateau = tuple[dict[str, list[Case]], list[Case], Case, Union[Case, None]]


class MorpionBase(ABC):
    """Classe de base pour le morpion"""

    JOUEURS = ['croix', 'rond']

    def __init__(self, dimension: int, player1='humain', player2='humain'):
        self.dimension = dimension
        self.cases_per_joueur = self.dimension
        self.cases_a_la_suite_gagnants = self.dimension
        self.joueurs = {
            'croix': player1,
            'rond': player2,
        }
        self.silent = False
        self.jeu_nul = False

        self.cases_vides: list[Case]
        self.joueur_actuel: str
        self.nombre_tour: int
        self.coords_joueur: dict[str, list[Case]]
        self.case_videe: Union[None, Case]
        self.vainqueur: Union[None, str]
        self.etats_precedents: dict[tuple[frozenset[Case], frozenset[Case]], bool]
        self.res_stack: list[Case]

        self.reinitialiser()

    def reinitialiser(self):
        """Réinitialiser le morpion
        """
        self.cases_vides = [(i, j) for i in range(self.dimension) for j in range(self.dimension)]
        self.joueur_actuel = choice(self.JOUEURS)
        self.nombre_tour = 0
        self.coords_joueur = {joueur: [] for joueur in self.JOUEURS}
        self.case_videe = None
        self.vainqueur = None
        self.etats_precedents = {}
        self.jeu_nul = False
        self.res_stack = []

    def quitter(self):
        """Quitter le jeu
        """
        sys.exit(0)

    def commencer(self):
        """Commencer le jeu
        """
        self.log('Morpion !')
        self.log(f'Dimension = {self.dimension}')
        self.jouer()

    # Fonctions cycle de jeu

    def jouer(self):
        """Main loop du jeu
        """
        # Choisir une joueur
        self.joueur_actuel = choice(self.JOUEURS)
        fini = False
        while not fini and not self.jeu_nul:
            self.log(f'Joueur actuel: {self.joueur_actuel} ({self.joueurs[self.joueur_actuel]})')
            self.print_matrice()
            case_placee = self.placer_un_pion()
            if case_placee:
                fini = self.gagnant(case_placee)
                if not fini:
                    self.basculer_joueur()
        self.print_matrice()
        if self.jeu_nul:
            self.log('Jeu nul (répétition)')
        else:
            self.vainqueur = self.joueur_actuel
            self.log(f'Joueur {self.vainqueur} a gagné !')

    def placer_un_pion(self):
        """Fonction pour placer un pion (humain ou IA)

        Returns:
            Case: Case à placer ou None si la choix à été invalide
        """
        joueur_est_humain = self.joueurs[self.joueur_actuel] == 'humain'
        if not self.joueur_peut_ajouter_nouvelle_forme(self.joueur_actuel):
            # retirer pion
            if joueur_est_humain:
                case_choisi = self.get_input()
                if not self.essai_marquer_case(case_choisi):
                    return None
            else:
                if not self.essai_marquer_case(self.jouer_ia()):
                    return None
            self.print_matrice()
        # ajouter pion
        if joueur_est_humain:
            case_choisi = self.get_input()
            if self.essai_marquer_case(case_choisi):
                return case_choisi
        else:
            case_choisi = self.jouer_ia()
            if self.essai_marquer_case(case_choisi):
                return case_choisi
        return None

    def gagnant(self, case_placee: Case, joueur: Union[str, None] = None) -> bool:
        """Calculer si la position actuelle est gagnante

        Args:
            case_placee (Case): dernière case placée pour optimiser l'algorithme
            joueur (Union[str, None], optional): Joueur. Defaults to self.joueur_actuel.

        Returns:
            bool: True si gagnant, sinon False
        """
        joueur = joueur or self.joueur_actuel
        fil, col = case_placee
        cases_joueur = self.coords_joueur[joueur]
        if self.get_nombre_cases_occupees_du_joueur(joueur) < self.dimension:
            return False
        # check file
        cases_a_la_suite = 1
        # check left
        for j in range(col - 1, -1, -1):
            if (fil, j) in cases_joueur:
                cases_a_la_suite += 1
            else:
                break
        # check right
        for j in range(col + 1, self.dimension):
            if (fil, j) in cases_joueur:
                cases_a_la_suite += 1
            else:
                break
        if cases_a_la_suite == self.cases_a_la_suite_gagnants:
            return True
        # check colonne
        cases_a_la_suite = 1
        # check up
        for i in range(fil - 1, -1, -1):
            if (i, col) in cases_joueur:
                cases_a_la_suite += 1
            else:
                break
        # check down
        for i in range(fil + 1, self.dimension):
            if (i, col) in cases_joueur:
                cases_a_la_suite += 1
            else:
                break
        if cases_a_la_suite == self.cases_a_la_suite_gagnants:
            return True
        # check diag 1
        cases_a_la_suite = 1
        # check up-left
        for k in range(1, min(fil, col) + 1):
            if (fil - k, col - k) in cases_joueur:
                cases_a_la_suite += 1
            else:
                break
        # check down-right
        for k in range(1, self.dimension - max(fil, col)):
            if (fil + k, col + k) in cases_joueur:
                cases_a_la_suite += 1
            else:
                break
        if cases_a_la_suite == self.cases_a_la_suite_gagnants:
            return True
        # check diag 2
        cases_a_la_suite = 1
        # check up-right
        for k in range(1, min(fil, self.dimension - col) + 1):
            if (fil - k, col + k) in cases_joueur:
                cases_a_la_suite += 1
            else:
                break
        # check down-left
        for k in range(1, min(self.dimension - fil, col) + 1):
            if (fil + k, col - k) in cases_joueur:
                cases_a_la_suite += 1
            else:
                break
        if cases_a_la_suite == self.cases_a_la_suite_gagnants:
            return True
        return False

    # Fonctions morpion

    def enregistrer_etat(self):
        """Garder l'état dans la liste d'états precedentes
        """
        nouvel_etat = tuple(frozenset(self.coords_joueur[k]) for k in self.coords_joueur)
        if len(self.etats_precedents) > 2 * self.dimension:
            if nouvel_etat in self.etats_precedents:
                self.jeu_nul = True
        if len(self.cases_vides) <= self.dimension**2 - 2 * self.dimension:
            self.etats_precedents[nouvel_etat] = True

    def essai_marquer_case(self, case: Case) -> Union[bool, Case]:
        """Essayer de marquer une case

        Args:
            case (Case): case à marquer

        Returns:
            Union[bool, Case]: False si case est invalide, sinon la case
                marquée
        """
        res = self._essai_marquer_case(case)
        if res is False:
            self.log(f'Choix {case} invalide ! ', end='')
            if self.joueur_peut_ajouter_nouvelle_forme(self.joueur_actuel):
                if self.case_videe == case:
                    self.log('Veuillez choisir une case différente !')
                else:
                    self.log('Veuillez choisir une case vide !')
            else:
                self.log('Veuillez choisir une de vos cases !')
        elif isinstance(res, tuple):
            self.log(f'Choix {res} valide ! ')
            if self.case_videe:
                self.log(f'Case {res} effacée')
            else:
                self.log(f'Case {res} marquée')
        return res

    def _essai_marquer_case(self, case: Case) -> Union[bool, Case]:
        if (self.case_est_libre(case) and
                self.joueur_peut_ajouter_nouvelle_forme(self.joueur_actuel) and
                self.case_videe != case):
            self.marquer_case(case, self.joueur_actuel)
            self.case_videe = None
            self.enregistrer_etat()
            return case
        if (self.case_videe is None and
            not self.joueur_peut_ajouter_nouvelle_forme(self.joueur_actuel) and
                self.case_est_de_joueur(case, self.joueur_actuel)):
            self.liberer_case(case, self.joueur_actuel)
            self.case_videe = case
            return case
        return False

    def joueur_peut_ajouter_nouvelle_forme(self, joueur: str) -> bool:
        """Vérifier si le joueur peut ajouter une nouvelle forme (remplir une nouvelle case)

        Args:
            joueur (str): Joueur

        Returns:
            bool: True si le joueur peut ajouter une nouvelle forme, sinon False
        """
        return self.get_nombre_cases_occupees_du_joueur(joueur) < self.cases_per_joueur

    def get_nombre_cases_occupees_du_joueur(self, joueur: str) -> int:
        """Obtenir le nombre de cases occupées par le joueur

        Args:
            joueur (str): Joueur

        Returns:
            int: Nombre de cases occupées par le joueur
        """
        return len(self.coords_joueur[joueur])

    def case_est_libre(self, case: Case) -> bool:
        """Vérifier si la case est vide

        Args:
            case (Case): Case à vérifier

        Returns:
            bool: True si la case est vide, sinon False
        """
        return case in self.cases_vides

    def case_est_de_joueur(self, case: Case, joueur: str) -> bool:
        """Vérifier si la case appartient au joueur

        Args:
            case (Case): Case à vérifier
            joueur (str): Joueur

        Returns:
            bool: True si la case appartient au joueur, sinon False
        """
        return case in self.coords_joueur[joueur]

    def marquer_case(self, case: Case, joueur: str):
        """Marquer une case

        Args:
            case (Case): Case à marquer
            joueur (str): Joueur
        """
        self.cases_vides.remove(case)
        self.coords_joueur[joueur].append(case)

    def liberer_case(self, case: Case, joueur: str):
        """Libérer une case

        Args:
            case (Case): Case à marquer
            joueur (str): Joueur
        """
        self.coords_joueur[joueur].remove(case)
        self.cases_vides.append(case)

    def autre_joueur(self, joueur: str):
        """Obtenir l'autre joueur

        Args:
            joueur (str): Joueur

        Returns:
            str: Autre joueur
        """
        return 'croix' if joueur == 'rond' else 'rond'

    def basculer_joueur(self):
        """Changer le joueur actuel
        """
        self.joueur_actuel = self.autre_joueur(self.joueur_actuel)

    def nombre_pions_ligne(self, case: Case) -> dict[str, int]:
        """Trouver le nombre de pions dans la ligne

        Args:
            case (Case): coordonnées

        Returns:
            dict[str, int]: nombre de cases par joueur
        """
        compteur = {'croix': 0, 'rond': 0}
        i = case[0]
        for j in range(self.dimension):
            if self.case_est_de_joueur((i, j), 'croix'):
                compteur['croix'] += 1
            elif self.case_est_de_joueur((i, j), 'rond'):
                compteur['rond'] += 1
        return compteur

    def nombre_pions_colonne(self, case: Case) -> dict[str, int]:
        """Trouver le nombre de pions dans la colonne

        Args:
            case (Case): coordonnées

        Returns:
            dict[str, int]: nombre de cases par joueur
        """
        compteur = {'croix': 0, 'rond': 0}
        j = case[1]
        for i in range(self.dimension):
            if self.case_est_de_joueur((i, j), 'croix'):
                compteur['croix'] += 1
            elif self.case_est_de_joueur((i, j), 'rond'):
                compteur['rond'] += 1
        return compteur

    def nombre_pions_diag_1(self, case: Case) -> dict[str, int]:
        """Trouver le nombre de pions dans la diagonale 1 (du haut à gauche vers le bas à droite)

        Args:
            case (Case): coordonnées

        Returns:
            dict[str, int]: nombre de cases par joueur
        """
        compteur = {'croix': 0, 'rond': 0}
        i, j = case
        min_coord = min(i, j)
        fil, col = i - min_coord, j - min_coord
        for _ in range(self.dimension - fil - col):
            if self.case_est_de_joueur((fil, col), 'croix'):
                compteur['croix'] += 1
            elif self.case_est_de_joueur((fil, col), 'rond'):
                compteur['rond'] += 1
            fil += 1
            col += 1
        return compteur

    def nombre_pions_diag_2(self, case: Case) -> dict[str, int]:
        """Trouver le nombre de pions dans la diagonale 2 (du haut à droite vers le bas à gauche)

        Args:
            case (Case): coordonnées

        Returns:
            dict[str, int]: nombre de cases par joueur
        """
        compteur = {'croix': 0, 'rond': 0}
        i, j = case
        min_desp = min(self.dimension - j - 1, i)
        fil, col = i - min_desp, j + min_desp
        for _ in range(min(self.dimension - fil, col + 1)):
            if self.case_est_de_joueur((fil, col), 'croix'):
                compteur['croix'] += 1
            elif self.case_est_de_joueur((fil, col), 'rond'):
                compteur['rond'] += 1
            fil += 1
            col -= 1
        return compteur

    # Fonctions IA

    @abstractmethod
    def jouer_ia(self) -> Case:
        """IA: jouer une case

        Returns:
            Case: case choisie pour jouer
        """
        return None

    # Fonctions interface

    def log(self, *args, **kwargs):
        """Afficher un message avec print()
        """
        if not self.silent:
            print(*args, **kwargs)

    def get_input(self) -> Case:
        """Demander une case à l'humain

        Returns:
            Case: case choisi
        """
        input_valide = False
        while not input_valide:
            prompt = 'Veuillez introduire une case (format i j, q -> quitter): '
            value = input(prompt).strip()
            if value == 'q':
                self.quitter()
            case = value.split()
            if len(case) == 2 and all(k.isnumeric() for k in case):
                tentative = tuple(int(x) for x in case)
                if all(0 <= k < self.dimension for k in tentative):
                    input_valide = True
                    return tentative
            if not input_valide:
                self.log('Input invalide')
        return (0, 0)

    def demander_y_n(self, prompt: str) -> str:
        """Demander une input yes or no à l'humain

        Args:
            prompt (str): prompt a montrer

        Returns:
            str: string reçu
        """
        input_valide = False
        res = ''
        while not input_valide:
            value = input(prompt).strip().lower()
            if value in ('y', 'n'):
                input_valide = True
                res = value
            if not input_valide:
                self.log('Input invalide')
        return res

    def print_matrice(self):
        """Affiche la matrice M

        Args:
            M (list): Matrice à afficher
        """
        self.log('╔' + '═'*(2*self.dimension - 1) + '╗')
        for i in range(self.dimension):
            self.log('║', end='')
            symboles = []
            for j in range(self.dimension):
                symbole = ' '
                if self.case_est_de_joueur((i, j), 'croix'):
                    symbole = 'X'
                elif self.case_est_de_joueur((i, j), 'rond'):
                    symbole = 'O'
                symboles.append(symbole)
            self.log(*symboles, sep=' ', end='')
            self.log('║')
        self.log('╚' + '═'*(2*self.dimension - 1) + '╝')
