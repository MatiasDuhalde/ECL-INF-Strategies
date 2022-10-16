

from __future__ import annotations
import random

from typing import Union, TYPE_CHECKING


if TYPE_CHECKING:
    from utils import Case
    from morpion import Morpion


class MorpionAdversaire:

    def __init__(self, morpion: Morpion, forme: str) -> None:
        self.morpion = morpion
        self.forme = forme

    def choisir_case_vide(self, restriction: Union[None, list[Case]] = None) -> Case:
        cases = self.morpion.get_cases_vides()
        if restriction:
            cases = [case for case in cases if case not in restriction]
        return random.choice(cases)

    def choisir_case_propre(self, restriction: Union[None, list[Case]] = None) -> Case:
        cases = self.morpion.coords_joueur[self.forme]
        if restriction:
            cases = [case for case in cases if case not in restriction]
        return random.choice(cases)
