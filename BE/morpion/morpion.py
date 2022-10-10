
from __future__ import annotations

import random
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from utils import Case
    from console import Console
    from interface import Interface


class Morpion():

    JOUEURS = ['rond', 'croix']

    def __init__(self, dimension: int, interface=None, player1='humain', player2='humain'):
        self.dimension = dimension
        self.interface: Union[None, Interface, Console] = interface
        self.cases_per_joueur = self.dimension
        self.matrice: list[list[Union[str, None]]] = [
            [None for j in range(self.dimension)] for i in range(self.dimension)
        ]
        self.joueur_actuel = random.choice(self.JOUEURS)
        self.nombre_tour = 0
        self.coords_joueur = {joueur: [] for joueur in self.JOUEURS}
        self.case_a_vider: Union[None, tuple[int, int]] = None
        self.vainqueur: Union[None, str] = None
        self.joueurs = {
            'croix': player1,
            'rond': player2,
        }

    def essai_marquer_case(self, case: Case) -> Union[bool, tuple[Case, Union[str, None]]]:
        res = self.essai_marquer_case_internal(case)
        if self.interface:
            interface_message = ''
            if res is False:
                interface_message = f'Choix {case} invalide ! '
                if self.joueur_peut_ajouter_nouvelle_forme(self.joueur_actuel):
                    if self.case_a_vider == case:
                        interface_message += 'Veuillez choisir une case différente !'
                    else:
                        interface_message += 'Veuillez choisir une case vide !'
                else:
                    interface_message += 'Veuillez choisir une de vos cases !'
            elif isinstance(res, tuple):
                interface_message = f'Choix {case} valide ! '
                case, forme = res
                if forme is None:
                    self.interface.effacer(case)
                    interface_message += f'Case {case} effacée '
                else:
                    self.interface.tracer(forme, case)
                    interface_message += f'Case {case} marquée avec {forme} '
                self.interface.current_player.set(f'Joueur {self.joueur_actuel}')
            self.interface.message.set(interface_message)
        return res

    def essai_marquer_case_internal(self, case: Case) -> Union[bool, tuple[Case, Union[str, None]]]:
        if (self.case_est_libre(case) and
                self.joueur_peut_ajouter_nouvelle_forme(self.joueur_actuel) and
                self.case_a_vider != case):
            self.set_case_value(case, self.joueur_actuel)
            self.case_a_vider = None
            self.basculer_joueur()
            return case, self.joueur_actuel
        if (self.case_a_vider is None and
            not self.joueur_peut_ajouter_nouvelle_forme(self.joueur_actuel) and
                self.case_est_de_joeueur(case, self.joueur_actuel)):
            self.set_case_value(case, None)
            self.case_a_vider = case
            return case, None
        return False

    def joueur_peut_ajouter_nouvelle_forme(self, joueur: str) -> bool:
        return self.get_nombre_cases_occupees_du_joueur(joueur) < self.cases_per_joueur

    def get_nombre_cases_occupees_du_joueur(self, joueur: str) -> int:
        return len(self.coords_joueur[joueur])

    def case_est_libre(self, case: Case) -> bool:
        return self.get_case_value(case) is None

    def case_est_de_joeueur(self, case: Case, joueur: str) -> bool:
        return self.get_case_value(case) == joueur

    def get_case_value(self, case: Case) -> Union[str, None]:
        _x, _y = case
        return self.matrice[_x][_y]

    def set_case_value(self, case: Case, value: Union[str, None]) -> Union[str, None]:
        _x, _y = case
        self.matrice[_x][_y] = value
        if value is not None:
            self.coords_joueur[value].append(case)
        else:
            self.coords_joueur[self.joueur_actuel].remove(case)

    def basculer_joueur(self):
        self.joueur_actuel = 'rond' if self.joueur_actuel == 'croix' else 'croix'
