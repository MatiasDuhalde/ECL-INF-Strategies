# -*- coding: utf-8 -*-
"""
Sept 2020 : code minimal Tkinter pour Morpion
Tiré de l aversion plus complète "Code-Eleve-OK-MorpionFinal.py" de AC-2019-20

Ce code affiche un matrice pour le jeu Morpion puis en cas de clique dans une case, place
aléatoirement un 'rond' ou une 'croix' dans la case cliquée. Si la case cliquée n'est pas vide,
on la vide !

Deux boutons sont crées (bouton1, bouton2) pour la démo.
Ce code est une aide de base pour réaliser le BE 'Morpion' avec TKinter.
"""


import random
import tkinter as tk
import copy
from typing import Union


Case = tuple[int, int]


class Interface(tk.Tk):
    """Interface pour le jeu du morpion
    """

    def __init__(self):
        super().__init__()

        self.dimension = 3
        self.morpion = Morpion(self.dimension, interface=self)

        self.width_canvas = 600
        self.height_canvas = 600
        self.offset_x_drawing_from_border = self.width_canvas / self.dimension * 0.1
        self.offset_y_drawing_from_border = self.height_canvas / self.dimension * 0.1

        # Frame principale
        self.frame_can = tk.Frame(self)
        self.frame_can.pack(side='top')

        self.message = tk.StringVar()
        self.message.set('Morpion !')
        self.message_label = tk.Label(self, textvariable=self.message)
        self.message_label.pack(side='bottom', pady=10)

        # Boutons
        self.action_frame = tk.Frame(self)
        self.action_frame.pack(side='bottom')

        self.current_player = tk.StringVar()
        self.current_player.set(f'Joueur {self.morpion.joueur_actuel}')

        self.info_frame = tk.Frame(self.action_frame)
        self.info_frame.pack(side='left')
        self.current_player_label = tk.Label(self.info_frame, textvariable=self.current_player)
        self.current_player_label.pack(side='left', padx=20)

        self.button_frame = tk.Frame(self.action_frame)
        self.button_frame.pack(side='right')

        self.list_button = []
        button1 = tk.Button(self.button_frame, text='Réinitialiser',
                            command=self.action_reinitialiser)
        button1.pack(side='left')
        self.list_button.append(button1)
        button2 = tk.Button(self.button_frame, text='Quitter', command=self.action_quitter)
        button2.pack(side='left')
        self.list_button.append(button2)

        # Canvas
        self.canvas = tk.Canvas(self.frame_can, width=self.width_canvas,
                                height=self.height_canvas, bg='white')
        # Creer lignes verticales et horizontales
        for i in range(1, self.dimension):
            self.canvas.create_line(i * self.width_canvas / self.dimension, 0,
                                    i * self.width_canvas / self.dimension,
                                    self.height_canvas, fill='black')
            self.canvas.create_line(0, i * self.height_canvas / self.dimension,
                                    self.width_canvas,
                                    i * self.height_canvas / self.dimension, fill='black')

        # <Button-1> : Bouton gauche de la souris
        self.canvas.bind("<Button-1>", self.on_click_souris)
        self.canvas.pack()

        self.humain = False
        self.liste_coords_cases = {}
        width_cell = self.width_canvas / self.dimension
        height_cell = self.height_canvas / self.dimension
        # Création de la liste des cases pour y tracer les formes
        for i in range(self.dimension):
            for j in range(self.dimension):
                self.liste_coords_cases[(i, j)] = (
                    i*width_cell + self.offset_x_drawing_from_border,
                    j*height_cell + self.offset_y_drawing_from_border,
                    (i + 1) * width_cell - self.offset_x_drawing_from_border,
                    (j + 1)*height_cell - self.offset_y_drawing_from_border
                )

    def action_reinitialiser(self):
        print('Réinitialisation...')
        self.morpion = Morpion(self.dimension, interface=self)
        self.retracer()
        self.message.set('Morpion !')
        self.current_player.set(f'Joueur {self.morpion.joueur_actuel}')

    def action_quitter(self):
        self.destroy()

    def retracer(self):
        for i in range(self.dimension):
            for j in range(self.dimension):
                case = (i, j)
                self.effacer(case)
                forme = self.morpion.get_case_value(case)
                if forme is not None:
                    self.tracer(forme, case)

    def tracer(self, forme: str, case: Case):
        # Trace la forme dans la case, rond ou croix
        case_coords = self.liste_coords_cases[case]
        if forme == 'rond':
            self.canvas.create_oval(*(case_coords))
        else:
            self.canvas.create_line(*(case_coords))
            _a, _b, _c, _d = case_coords
            self.canvas.create_line(_a, _d, _c, _b)
        self.update()

    def effacer(self, case):
        # vide la case
        self.canvas.create_rectangle(
            *(self.liste_coords_cases[case]), fill='white', outline='white')

    def on_click_souris(self, event):
        _x = event.x
        _y = event.y

        case = (int(_x // (self.width_canvas / self.dimension)),
                int(_y // (self.height_canvas / self.dimension)))
        self.morpion.essai_marquer_case(case)


class Morpion():

    JOEURS = ['rond', 'croix']

    def __init__(self, dimension: int, interface=None):
        self.dimension = dimension
        self.interface: Union[None, Interface] = interface
        self.cases_per_joueur = self.dimension
        self.matrice: list[list[Union[str, None]]] = [
            [None for j in range(self.dimension)] for i in range(self.dimension)
        ]
        self.joueur_actuel = random.choice(self.JOEURS)
        self.nombre_tour = 0
        self.coords_joueur = {joueur: [] for joueur in self.JOEURS}
        self.case_a_vider: Union[None, tuple[int, int]] = None
        self.vainqueur: Union[None, str] = None
        self.ia = None

    def essai_marquer_case(self, case: Case) -> Union[bool, tuple[Case, Union[str, None]]]:
        if not self.interface:
            print(f'Joeur {self.joueur_actuel} joue en {case}')
        res = self.essai_marquer_case_internal(case)
        if self.interface:
            interface_message = ''
            if res == False:
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
        else:
            # Console
            print(f'Choix {case} invalide')
        return res

    def essai_marquer_case_internal(self, case: Case) -> Union[bool, tuple[Case, Union[str, None]]]:
        if (self.case_est_libre(case) and
                self.joueur_peut_ajouter_nouvelle_forme(self.joueur_actuel) and
                self.case_a_vider != case):
            self.set_case_value(case, self.joueur_actuel)
            self.case_a_vider = None
            self.basculer_joeur()
            return case, self.joueur_actuel
        if (self.case_a_vider is None and
            not self.joueur_peut_ajouter_nouvelle_forme(self.joueur_actuel) and
                self.case_est_de_joeueur(case, self.joueur_actuel)):
            self.set_case_value(case, None)
            if self.interface:
                self.interface.effacer(case)
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

    def basculer_joeur(self):
        self.joueur_actuel = 'rond' if self.joueur_actuel == 'croix' else 'croix'


def print_matrice(M: list):
    """Affiche la matrice M

    Args:
        M (list): Matrice à afficher
    """
    for i in range(len(M)):
        print(M[i])


def adversaire(joueur):
    if joueur == 'croix':
        return 'rond'
    return 'croix'


def copier_matrice(M: list) -> list:
    """Faire une copie de la matrice M

    Args:
        M (list): Matrice à copier

    Returns:
        list: Copie de la matrice M
    """
    L = copy.deepcopy(M)
    return L


if __name__ == "__main__":
    jeu = Interface()
    jeu.mainloop()
