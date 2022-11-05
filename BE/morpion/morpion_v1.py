"""Travail à rendre 1"""
from __future__ import annotations

from random import choice
from typing import TYPE_CHECKING, Union

from morpion_base import MorpionBase

if TYPE_CHECKING:
    from morpion_base import Case


class Morpion(MorpionBase):
    """Classe morpion : Implementation IA avec choix aléatoire"""

    # Fonctions IA

    def jouer_ia(self) -> Case:
        """IA: jouer une case

        Returns:
            Case: case choisie pour jouer
        """
        if self.joueur_peut_ajouter_nouvelle_forme(self.joueur_actuel):
            rest = []
            if self.case_videe:
                rest.append(self.case_videe)
            return self.choisir_case_vide(rest)
        return self.choisir_case_propre()

    def choisir_case_vide(self, restriction: Union[None, list[Case]] = None) -> Case:
        """IA: choisir aléatoirement une case vide

        Args:
            restriction (Union[None, list[Case]], optional): Cases interdites. Defaults to None.

        Returns:
            Case: Case choisie
        """
        cases = self.cases_vides
        if restriction:
            cases = [case for case in cases if case not in restriction]
        return choice(cases)

    def choisir_case_propre(self, restriction: Union[None, list[Case]] = None) -> Case:
        """IA: choisir aléatoirement une case propre

        Args:
            restriction (Union[None, list[Case]], optional): Cases. Defaults to None.

        Returns:
            Case: Case choisie
        """
        cases = self.coords_joueur[self.joueur_actuel]
        if restriction:
            cases = [case for case in cases if case not in restriction]
        return choice(cases)


if __name__ == "__main__":
    DIM = 3
    # humain vs humain
    # morpion = Morpion(DIM)

    # humain vs ia
    # morpion = Morpion(DIM, 'ia')

    # ia vs ia
    morpion = Morpion(DIM, 'ia', 'ia')

    morpion.commencer()
