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
from __future__ import annotations
from random import choice

import tkinter as tk
from typing import TYPE_CHECKING

from morpion_v1 import Morpion

if TYPE_CHECKING:
    from utils import Case


class Interface(tk.Tk):
    """Interface pour le jeu du morpion
    """

    def __init__(self, *morpion_args):
        super().__init__()

        self.morpion_args: tuple[int, str, str]
        self.morpion_args = morpion_args
        self.morpion = Morpion(*self.morpion_args)
        self.morpion.joueur_actuel = choice(self.morpion.JOUEURS)

        self.width_canvas = 600
        self.height_canvas = 600
        self.offset_x_drawing_from_border = self.width_canvas / self.morpion.dimension * 0.1
        self.offset_y_drawing_from_border = self.height_canvas / self.morpion.dimension * 0.1

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
        for i in range(1, self.morpion.dimension):
            self.canvas.create_line(i * self.width_canvas / self.morpion.dimension, 0,
                                    i * self.width_canvas / self.morpion.dimension,
                                    self.height_canvas, fill='black')
            self.canvas.create_line(0, i * self.height_canvas / self.morpion.dimension,
                                    self.width_canvas,
                                    i * self.height_canvas / self.morpion.dimension, fill='black')

        # <Button-1> : Bouton gauche de la souris
        self.canvas.bind("<Button-1>", self.on_click_souris)
        self.canvas.pack()

        self.humain = False
        self.liste_coords_cases = {}
        width_cell = self.width_canvas / self.morpion.dimension
        height_cell = self.height_canvas / self.morpion.dimension
        # Création de la liste des cases pour y tracer les formes
        for i in range(self.morpion.dimension):
            for j in range(self.morpion.dimension):
                self.liste_coords_cases[(i, j)] = (
                    i*width_cell + self.offset_x_drawing_from_border,
                    j*height_cell + self.offset_y_drawing_from_border,
                    (i + 1) * width_cell - self.offset_x_drawing_from_border,
                    (j + 1)*height_cell - self.offset_y_drawing_from_border
                )

    def action_reinitialiser(self):
        self.morpion = Morpion(*self.morpion_args)
        self.morpion.joueur_actuel = choice(self.morpion.JOUEURS)
        self.retracer()
        self.message.set('Morpion réinitialisé !')
        self.current_player.set(f'Joueur {self.morpion.joueur_actuel}')
        self.jouer_tour()

    def action_quitter(self):
        self.destroy()

    def retracer(self):
        for case in self.morpion.cases_vides:
            self.effacer(case)
        for forme in self.morpion.JOUEURS:
            for case in self.morpion.coords_joueur[forme]:
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
        if self.morpion.vainqueur:
            return
        _x = event.x
        _y = event.y

        case = (int(_x // (self.width_canvas / self.morpion.dimension)),
                int(_y // (self.height_canvas / self.morpion.dimension)))
        case = self.morpion.essai_marquer_case(case)
        if not isinstance(case, tuple):
            return
        self.retracer()

        if self.morpion.case_videe is not None:
            return

        if self.morpion.gagnant(case[0]):
            self.morpion.vainqueur = case[1]
            self.message.set(f'Joueur {case[1]} a gagné !')
            return

        self.morpion.basculer_joueur()
        self.current_player.set(f'Joueur {self.morpion.joueur_actuel}')
        self.jouer_tour()

    def jouer_tour(self):
        if self.morpion.joueurs[self.morpion.joueur_actuel] == 'humain':
            # espérer action de joueur
            return
        case_marquee = self.morpion.jouer_ia()
        self.morpion.essai_marquer_case(case_marquee)
        if self.morpion.case_videe:
            case_marquee = self.morpion.jouer_ia()
            self.morpion.essai_marquer_case(case_marquee)

        self.retracer()

        if self.morpion.gagnant(case_marquee):
            self.morpion.vainqueur = self.morpion.joueur_actuel
            self.message.set(f'Joueur {self.morpion.vainqueur} a gagné !')
            return
        # next turn
        self.morpion.basculer_joueur()
        self.current_player.set(f'Joueur {self.morpion.joueur_actuel}')
        self.jouer_tour()

    def commencer(self):
        self.jouer_tour()
        self.mainloop()


if __name__ == '__main__':
    dimension = 3
    # humain vs humain
    # interface = Interface(dimension)

    # humain vs ia
    interface = Interface(dimension, 'ia')

    # ia vs ia
    # interface = Interface(dimension, 'ia', 'ia')
    interface.commencer()
