"""Travail à rendre 3"""
from __future__ import annotations

from collections import defaultdict
from random import choice
from typing import TYPE_CHECKING

from morpion_base import MorpionBase

if TYPE_CHECKING:
    from morpion_base import Case


class Morpion(MorpionBase):
    """Classe morpion : Implementation IA avec fonction de coût"""
    # Fonctions IA

    def jouer_ia(self) -> Case:
        """IA: jouer une case

        Returns:
            Case: case choisie pour jouer
        """
        if len(self.res_stack) != 0:
            return self.res_stack.pop()
        self.res_stack.extend(self.best_first())
        return self.res_stack.pop()

    def best_first(self) -> tuple[Case, ...]:
        """IA: calculer pion a placer (ou enlever) par best-first

        Returns:
            tuple[Case, ...]: cases a placer/enlever
        """
        valeurs = defaultdict(list)
        if self.joueur_peut_ajouter_nouvelle_forme(self.joueur_actuel):
            for case in self.cases_vides:
                valeurs[self.obtenir_valeur_case(case)].append((case,))
        else:
            for case_a_enlever in [*self.coords_joueur[self.joueur_actuel]]:
                cases_vides_avant = [*self.cases_vides]
                self.liberer_case(case_a_enlever, self.joueur_actuel)
                for case_a_placer in cases_vides_avant:
                    valeurs[self.obtenir_valeur_case(case_a_placer)].append(
                        (case_a_placer, case_a_enlever))
                self.marquer_case(case_a_enlever, self.joueur_actuel)
        best = valeurs[max(valeurs)]
        # privilégier diag
        best_diags = list(filter(lambda x: x[0][0] == x[0][1]
                          or x[0][0] + x[0][1] == self.dimension - 1, best))
        if best_diags:
            return choice(best_diags)
        return choice(best)

    def obtenir_valeur_case(self, case: Case) -> int:
        """Calculer la valeur de la case

        Args:
            case (Case): case à calculer

        Returns:
            int: valeur de la case
        """
        autre = 'croix' if self.joueur_actuel == 'rond' else 'rond'
        nl = self.nombre_pions_ligne(case)
        nc = self.nombre_pions_colonne(case)
        nl_1 = nl[self.joueur_actuel]
        nc_1 = nc[self.joueur_actuel]
        nl_2 = nl[autre]
        nc_2 = nc[autre]
        facteur_nl = -1 if nl_2 > nl_1 else 1
        facteur_nc = -1 if nc_2 > nc_1 else 1
        g_partial = facteur_nl * (nl_1 - nl_2)**2 + facteur_nc * (nc_1 - nc_2)**2

        facteur_nd1 = 1
        facteur_nd2 = 1
        if case[0] == case[1]:
            nd1 = self.nombre_pions_diag_1(case)
            nd1_1 = nd1[self.joueur_actuel]
            nd1_2 = nd1[autre]
            facteur_nd1 = -1 if nd1_2 > nd1_1 else 1
            g_partial = g_partial + facteur_nd1 * (nd1_1 - nd1_2)**2
            facteur_nd1 = 2 if nd1_2 > 1 else 1

        if case[0] + case[1] == self.dimension - 1:
            nd2 = self.nombre_pions_diag_2(case)
            nd2_1 = nd2[self.joueur_actuel]
            nd2_2 = nd2[autre]
            facteur_nd2 = -1 if nd2_2 > nd2_1 else 1
            g_partial = g_partial + facteur_nd2 * (nd2_1 - nd2_2)**2
            facteur_nd2 = 2 if nd2_2 > 1 else 1

        facteur_nl = 2 if nl_2 > 1 else 1
        facteur_nc = 2 if nc_2 > 1 else 1
        g = g_partial * facteur_nc * facteur_nl * facteur_nd1 * facteur_nd2
        return abs(g)


if __name__ == "__main__":
    DIM = 3
    # humain vs humain
    # morpion = Morpion(DIM)

    # humain vs ia
    # morpion = Morpion(DIM, 'ia')

    # ia vs ia
    morpion = Morpion(DIM, 'ia', 'ia')

    morpion.commencer()
