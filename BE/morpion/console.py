
from __future__ import annotations

import sys
from typing import Union, TYPE_CHECKING

from morpion import Morpion

if TYPE_CHECKING:
    from utils import Case


class Console:
    SYMBOLS = {
        'rond':  'O',
        'croix':  'X',
        None: ' '
    }

    def __init__(self) -> None:

        self.dimension = 3
        self.morpion = Morpion(self.dimension, interface=self)

        self.message = ConsoleMessage('Morpion !')
        self.current_player = ConsoleMessage(f'Joueur {self.morpion.joueur_actuel}')

    def get_input(self) -> Union[str, Case]:
        input_valide = False
        res = ''
        while not input_valide:
            prompt = 'Veuillez introduire une case (format i j, r -> réinitialiser, q -> quitter): '
            value = input(prompt).strip()
            if value == 'q':
                self.quitter()
            if value == 'r':
                self.reinitialiser()
                return 'r'
            case = value.split()
            if len(case) == 2 and all(k.isnumeric() for k in case):
                tentative = tuple(int(x) for x in case)
                if all(0 <= k < self.dimension for k in tentative):
                    input_valide = True
                    res = tentative
            if not input_valide:
                print('Input invalide')
        return res

    def effacer(self, case):
        pass

    def tracer(self, forme, case):
        pass

    def reinitialiser(self):
        self.morpion = Morpion(self.dimension, interface=self)
        self.message = ConsoleMessage('Morpion !')
        self.current_player = ConsoleMessage(f'Joueur {self.morpion.joueur_actuel}')

    def quitter(self):
        sys.exit(0)

    def main_loop(self) -> str:
        while True:
            print('Joueur actuel :', self.current_player.value)
            self.print_matrice()
            case = self.get_input()
            if isinstance(case, str):
                return 'r'
            self.morpion.essai_marquer_case(case)
            print(self.message)

    def commencer(self):
        print('Morpion !')
        continuer = True
        while continuer:
            res = self.main_loop()
            if res == 'i':
                continue
            if res == 'fin':
                cont = self.demander_y_n('Voulez vous réinitialiser ? (y/n) : ')
                if cont == 'n':
                    continuer = False
                else:
                    self.reinitialiser()

    def demander_y_n(self, prompt: str) -> str:
        input_valide = False
        res = ''
        while not input_valide:
            value = input(prompt).strip().lower()
            if value in ('y', 'n'):
                input_valide = True
                res = value
            if not input_valide:
                print('Input invalide')
        return res

    def print_matrice(self):
        """Affiche la matrice M

        Args:
            M (list): Matrice à afficher
        """
        print('╔' + '═'*(2*self.dimension - 1) + '╗')
        for line in self.morpion.matrice:
            print('║', end='')
            print(*(self.SYMBOLS[el] for el in line), sep=' ', end='')
            print('║')
        print('╚' + '═'*(2*self.dimension - 1) + '╝')


class ConsoleMessage:

    def __init__(self, value='') -> None:
        self.value = value

    def set(self, value):
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value


if __name__ == '__main__':
    console = Console()
    console.commencer()
