"""Travail à rendre 4"""
from __future__ import annotations

import math
from copy import deepcopy
from random import choice
from typing import TYPE_CHECKING

from morpion_base import MorpionBase

if TYPE_CHECKING:
    from morpion_base import Case, Plateau


class Morpion(MorpionBase):
    """Classe morpion : Implementation IA avec stratégie min-max"""

    def __init__(self, dimension: int, player1='humain', player2='humain'):
        self.min_max_profondeur = 2
        super().__init__(dimension, player1, player2)

    # Fonctions IA

    def jouer_ia(self) -> Case:
        """IA: jouer une case

        Returns:
            Case: case choisie pour jouer
        """
        if len(self.res_stack) != 0:
            return self.res_stack.pop()
        self.res_stack.extend(self.min_max())
        return self.res_stack.pop()

    def min_max(self) -> tuple[Case, ...]:
        """Stratégie min

        Returns:
            tuple[Case, ...]: cases à jouer trouvées par l'IA (deux cases s'il faut enlever)
        """
        coords_joueur_copy = deepcopy(self.coords_joueur)
        cases_vides_copy = [*self.cases_vides]
        plateau, _ = self.min_max_rec(
            (self.coords_joueur, self.cases_vides, (0, 0), None),
            self.min_max_profondeur, self.joueur_actuel, 'max'
        )
        self.coords_joueur = coords_joueur_copy
        self.cases_vides = cases_vides_copy
        if isinstance(plateau[3], tuple):
            return (plateau[2], plateau[3])
        return (plateau[2],)

    def min_max_rec(self, plateau: Plateau, k: int, joueur_a_jouer: str, mode: str
                    ) -> tuple[Plateau, float]:
        autre = self.autre_joueur(joueur_a_jouer)
        # set vars pour pouvoir utiliser les méthodes de la classe
        self.coords_joueur = plateau[0]
        self.cases_vides = plateau[1]
        derniere_case_placee = plateau[2]

        # si on est à la profondeur max ou l'autre joueur gagne, on renvoie le plateau + son score
        if k != self.min_max_profondeur:
            est_gagnant = self.gagnant(derniere_case_placee, autre)
            if est_gagnant:
                score = math.inf if autre == self.joueur_actuel else -math.inf
                return plateau, score
            if k == 0:
                score = self.valeur_min_max(self.joueur_actuel)
                return plateau, score

        min_score = +math.inf
        max_score = -math.inf

        # trouver successeurs
        liste_plateaux_successeurs: list[Plateau] = []
        cases_vides_avant = [*self.cases_vides]
        if self.joueur_peut_ajouter_nouvelle_forme(joueur_a_jouer):
            for case_vide in cases_vides_avant:
                self.marquer_case(case_vide, joueur_a_jouer)
                new_coords_joueur = deepcopy(self.coords_joueur)
                new_cases_vides = [*self.cases_vides]
                liste_plateaux_successeurs.append(
                    (new_coords_joueur, new_cases_vides, case_vide, None))
                self.liberer_case(case_vide, joueur_a_jouer)
        else:
            for case_occupee in [*self.coords_joueur[joueur_a_jouer]]:
                self.liberer_case(case_occupee, joueur_a_jouer)
                for case_vide in cases_vides_avant:
                    self.marquer_case(case_vide, joueur_a_jouer)
                    new_coords_joueur = deepcopy(self.coords_joueur)
                    new_cases_vides = [*self.cases_vides]
                    liste_plateaux_successeurs.append(
                        (new_coords_joueur, new_cases_vides, case_vide, case_occupee))
                    self.liberer_case(case_vide, joueur_a_jouer)
                self.marquer_case(case_occupee, joueur_a_jouer)

        best_plateaux = []
        best_score = 0
        new_mode = 'min' if mode == 'max' else 'max'
        # tester tous les plateaux successeurs
        for plateau_successeur in liste_plateaux_successeurs:
            plateau_successeur_2, score = self.min_max_rec(
                plateau_successeur, k - 1, autre, new_mode)
            if mode == 'max':
                if score == max_score:
                    best_plateaux.append(plateau_successeur_2)
                elif score > max_score:
                    best_score = score
                    best_plateaux = [plateau_successeur_2]
                    max_score = best_score
            else:
                if score == max_score:
                    best_plateaux.append(plateau_successeur_2)
                if score < min_score:
                    best_score = score
                    best_plateaux = [plateau_successeur_2]
                    min_score = best_score
        if k == self.min_max_profondeur:
            cx = choice(best_plateaux)
            return cx, best_score
        return plateau, best_score

    def valeur_min_max(self, joueur) -> int:
        """Calculer la valeur min-max du plateau courant pour le joueur

        Args:
            joueur (_type_): joueur

        Returns:
            int: Valeur min-max (plus c'est grand, plus c'est bon pour le joueur)
        """
        autre = self.autre_joueur(joueur)
        return self.gagnants_possibles(joueur) - self.gagnants_possibles(autre)

    def gagnants_possibles(self, joueur: str) -> int:
        """Calculer le nombre de lignes, colonnes et diagonales possibles pour gagner (pour joueur)

        Args:
            joueur (str): joueur

        Returns:
            int: positions possibles pour gagner pour le joueur
        """
        compteur = 0
        autre = self.autre_joueur(joueur)
        for m in range(self.dimension):
            if self.nombre_pions_ligne((m, 0))[autre] == 0:
                compteur += 1
            if self.nombre_pions_colonne((0, m))[autre] == 0:
                compteur += 1
        if self.nombre_pions_diag_1((0, 0))[autre] == 0:
            compteur += 1
        if self.nombre_pions_diag_2((0, self.dimension - 1))[autre] == 0:
            compteur += 1
        return compteur


if __name__ == "__main__":
    DIM = 3
    # humain vs humain
    # morpion = Morpion(DIM)

    # humain vs ia
    morpion = Morpion(DIM, 'ia')

    # ia vs ia
    # morpion = Morpion(DIM, 'ia', 'ia')

    morpion.commencer()
