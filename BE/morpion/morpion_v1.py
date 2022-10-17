

from __future__ import annotations

from random import choice
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from morpion import Morpion
    from utils import Case


class MorpionAdversaire:

    def __init__(self, morpion: Morpion, forme: str) -> None:
        self.morpion = morpion
        self.forme = forme

    def choisir_case_vide(self, restriction: Union[None, list[Case]] = None) -> Case:
        cases = self.morpion.get_cases_vides()
        if restriction:
            cases = [case for case in cases if case not in restriction]
        return choice(cases)

    def choisir_case_propre(self, restriction: Union[None, list[Case]] = None) -> Case:
        cases = self.morpion.coords_joueur[self.forme]
        if restriction:
            cases = [case for case in cases if case not in restriction]
        return choice(cases)


if __name__ == "__main__":
    pass
    # human vs ai

    # ai vs ai
