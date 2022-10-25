
from __future__ import annotations

import sys
from collections import deque
from random import choice
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from utils import Case


class Morpion():

    JOUEURS = ['croix', 'rond']

    def __init__(self, dimension: int, player1='humain', player2='humain'):
        self.dimension = dimension
        self.cases_per_joueur = self.dimension
        self.joueurs = {
            'croix': player1,
            'rond': player2,
        }
        self.silent = False

        self.cases_vides: list[Case]
        self.joueur_actuel: str
        self.nombre_tour: int
        self.coords_joueur: dict[str, list[Case]]
        self.case_videe: Union[None, Case]
        self.vainqueur: Union[None, str]
        self.etats_precedents: deque[tuple[tuple[Case], ...]]

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
        self.etats_precedents = deque((tuple(), tuple(), tuple()))

    def quitter(self):
        sys.exit(0)

    def commencer(self):
        self.log('Morpion !')
        self.log(f'Dimension = {self.dimension}')
        self.jouer()

    # Fonctions principales

    def jouer(self):
        # Choisir une joueur
        self.joueur_actuel = choice(self.JOUEURS)
        fini = False
        while not fini:
            self.log(f'Joueur actuel: {self.joueur_actuel} ({self.joueurs[self.joueur_actuel]})')
            self.print_matrice()
            place = self.placer_un_pion()
            fini = self.gagnant()
            if not fini and place:
                self.basculer_joueur()
        self.vainqueur = self.joueur_actuel
        self.print_matrice()
        self.log(f'Joueur {self.vainqueur} a gagné !')

    def placer_un_pion(self):
        joueur_est_humain = self.joueurs[self.joueur_actuel] == 'humain'
        if not self.joueur_peut_ajouter_nouvelle_forme(self.joueur_actuel):
            # retirer pion
            if joueur_est_humain:
                case_choisi = self.get_input()
                if not self.essai_marquer_case(case_choisi):
                    return False
            else:
                if not self.essai_marquer_case(self.jouer_ia()):
                    return False
            self.print_matrice()
        # ajouter pion
        if joueur_est_humain:
            case_choisi = self.get_input()
            if self.essai_marquer_case(case_choisi):
                return True
        elif self.essai_marquer_case(self.jouer_ia()):
            return True
        return False

    def gagnant(self) -> bool:
        cases_joueur = sorted(self.coords_joueur[self.joueur_actuel])
        if self.get_nombre_cases_occupees_du_joueur(self.joueur_actuel) < self.dimension:
            return False
        # check file
        fil, col = cases_joueur[0]
        for fil_c, col_c in cases_joueur:
            if fil != fil_c or col_c != col:
                break
            col += 1
        else:
            return True
        # check colonne
        fil, col = cases_joueur[0]
        for fil_c, col_c in cases_joueur:
            if fil != fil_c or col_c != col:
                break
            fil += 1
        else:
            return True
        # check diag 1
        fil, col = cases_joueur[0]
        for fil_c, col_c in cases_joueur:
            if fil != fil_c or col_c != col:
                break
            fil += 1
            col += 1
        else:
            return True
        # check diag 2
        fil, col = cases_joueur[0]
        for fil_c, col_c in cases_joueur:
            if fil != fil_c or col_c != col:
                break
            fil += 1
            col -= 1
        else:
            return True
        return False

    # Fonctions morpion

    def enregistrer_etat(self):
        entity = [tuple(self.coords_joueur[k]) for k in self.coords_joueur]
        entity.append(tuple(self.cases_vides))
        self.etats_precedents.append(tuple(entity))
        if len(self.etats_precedents) > 3:
            self.etats_precedents.popleft()

    def essai_marquer_case(self, case: Case) -> Union[bool, tuple[Case, Union[str, None]]]:
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
            self.log(f'Choix {case} valide ! ')
            case, forme = res
            if forme is None:
                self.log(f'Case {case} effacée')
            else:
                self.log(f'Case {case} marquée avec {forme}')
        return res

    def _essai_marquer_case(self, case: Case) -> Union[bool, tuple[Case, Union[str, None]]]:
        if (self.case_est_libre(case) and
                self.joueur_peut_ajouter_nouvelle_forme(self.joueur_actuel) and
                self.case_videe != case):
            self.marquer_case(case, self.joueur_actuel)
            self.case_videe = None
            self.enregistrer_etat()
            return case, self.joueur_actuel
        if (self.case_videe is None and
            not self.joueur_peut_ajouter_nouvelle_forme(self.joueur_actuel) and
                self.case_est_de_joueur(case, self.joueur_actuel)):
            self.liberer_case(case, self.joueur_actuel)
            self.case_videe = case
            return case, None
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
            case (Case): Case à vérifier

        Returns:
            bool: True si la case est vide, sinon False
        """
        return case in self.cases_vides

    def case_est_de_joueur(self, case: Case, joueur: str) -> bool:
        """Vérifier si la case appartient au joueur

        Args:
            case (Case): Case à vérifier
            joueur (str): Joueur

        Returns:
            bool: True si la case appartient au joueur, sinon False
        """
        return case in self.coords_joueur[joueur]

    def marquer_case(self, case: Case, joueur: str):
        """Marquer une case

        Args:
            case (Case): Case à marquer
            joueur (str): Joueur
        """
        self.cases_vides.remove(case)
        self.coords_joueur[joueur].append(case)

    def liberer_case(self, case: Case, joueur: str):
        """Libérer une case

        Args:
            case (Case): Case à marquer
            joueur (str): Joueur
        """
        self.coords_joueur[joueur].remove(case)
        self.cases_vides.append(case)

    def basculer_joueur(self):
        """Changer le joueur actuel
        """
        self.joueur_actuel = 'rond' if self.joueur_actuel == 'croix' else 'croix'

    # Fonctions IA

    def jouer_ia(self):
        print('///')
        if self.joueur_peut_ajouter_nouvelle_forme(self.joueur_actuel):
            rest = []
            if self.case_videe:
                rest.append(self.case_videe)
            return self.choisir_case_vide(rest)
        return self.choisir_case_propre()

    def choisir_case_vide(self, restriction: Union[None, list[Case]] = None) -> Case:
        cases = self.cases_vides
        if restriction:
            cases = [case for case in cases if case not in restriction]
        return choice(cases)

    def choisir_case_propre(self, restriction: Union[None, list[Case]] = None) -> Case:
        cases = self.coords_joueur[self.joueur_actuel]
        if restriction:
            cases = [case for case in cases if case not in restriction]
        return choice(cases)

    # Fonctions interface

    def log(self, *args, **kwargs):
        """Afficher un message avec print()
        """
        if not self.silent:
            print(*args, **kwargs)

    def get_input(self) -> Case:
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
            M (list): Matrice à afficher
        """
        self.log('╔' + '═'*(2*self.dimension - 1) + '╗')
        for i in range(self.dimension):
            self.log('║', end='')
            symboles = []
            for j in range(self.dimension):
                symbole = ' '
                if (i, j) in self.coords_joueur['croix']:
                    symbole = 'X'
                elif (i, j) in self.coords_joueur['rond']:
                    symbole = 'O'
                symboles.append(symbole)
            self.log(*symboles, sep=' ', end='')
            self.log('║')
        self.log('╚' + '═'*(2*self.dimension - 1) + '╝')


if __name__ == "__main__":
    dim = 4
    # humain vs humain
    # morpion = Morpion(dim)

    # humain vs ia
    # morpion = Morpion(dim, 'ia')

    # ia vs ia
    morpion = Morpion(dim, 'ia', 'ia')

    morpion.commencer()
