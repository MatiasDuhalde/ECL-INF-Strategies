# -*- coding: utf-8 -*-
"""
Sept 2020 : code minimal Tkinter pour Morpion
Tiré de l aversion plus complète "Code-Eleve-OK-MorpionFinal.py" de AC-2019-20
"""

"""
Ce code affiche un ematrice pour le jeu Morpion puis en cas de clique dans une case, place aléatoirement
un 'rond' ou une 'croix' dans la case cliquée.
Si la case cliquée n'est aps vide, on la vide !
Deux boutons sont crées (bouton1, bouton2) pour la démo.
Ce code est une aide de base pour réaliser le BE 'Morpion' avec TkInter.
"""
import random
import tkinter as tk
import time
import copy

class Interface(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frameCan = tk.Frame(self)
        self.frameCan.pack(side='top')
        self.canvas = tk.Canvas(self.frameCan,width=600,height=480,bg='white')
        self.canvas.bind("<Button-1>",self.onClick_souris) # <Button-1> : Bouton gauche de la souris 
        self.canvas.pack()
        self.canvas.create_line(200,0,200,479)
        self.canvas.create_line(400,0,400,479)
        self.canvas.create_line(0,160,599,160)
        self.canvas.create_line(0,320,599,320)
        self.morpion = Morpion(self)
        self.frameButton = tk.Frame(self)
        self.frameButton.pack(side='bottom')
        self.listButton = []
        button1 = tk.Button(self.frameButton, text='Bouton 1', command = self.fonction1)
        button1.pack()
        self.listButton.append(button1)
        button2 = tk.Button(self.frameButton, text='Bouton 2', command = self.fonction2)
        button2.pack()
        self.listButton.append(button2)
        self.humain = False
        self.liste_cases = []
        self.liste_cases_opposee = []
        #Création de la liste des cases pour y tracer les formes
        for j in range(3):
            for i in range(3):
                self.liste_cases.append([i*201,j*161,i*201+198,j*161+158])
                #Permet de tracer les croix facilement
                self.liste_cases_opposee.append([i*201,j*161+159,i*201+199,j*161])

    def fonction1(self) :
        print("On est dans fonction1; décider quoi faire si on clique sur Bouton 1")
        
    def fonction2(self) :
        print("On est dans fonction2; décider quoi faire si on clique sur Bouton 2"    )
            
    def tracer(self,forme,case):
        #Trace la forme dans la case, rond ou croix
        if forme=='rond':
            self.canvas.create_oval(*(self.liste_cases[case]))
        else:
            self.canvas.create_line(*(self.liste_cases[case]))
            self.canvas.create_line(*(self.liste_cases_opposee[case]))
        self.update()
        
    def effacer(self,case):
        #vide la case
        self.canvas.create_rectangle(*(self.liste_cases[case]),fill='white',outline='white')
    
    def onClick_souris(self,event):
        x=event.x
        y=event.y
        print(f"On a cliqué dans la case {(x,y)}; on affiche un 'O' ou 'X' dans la case (si vide)")
        # Sur quelle case a-t-on cliqué ?
        for case in self.liste_cases:
            if x>case[0] and x<case[2] and y>case[1] and y<case[3]:
                self.morpion.dessiner_au_piff_c_est_un_test(self.liste_cases.index(case))
                          
    
                    
class Morpion():
    def __init__(self,interface):
        self.interface = interface
        self.matrice = [None for i in range(9)]
        self.joueurs = ['rond','croix']
        self.joueur_debut = random.randint(0,1)
        self.nombre_tour = 0
        self.case_a_vider = -1
        self.vainqueur = None
        self.IA = None
        
    def dessiner_au_piff_c_est_un_test(self, case) :        
        if self.matrice[case] == None:
            self.matrice[case] = random.choice(['rond','croix'])
            self.repaint()    
        else :
            print(f"La case {case} n'est pas vide !")
            self.case_a_vider = case
            self.matrice[self.case_a_vider] = None
            self.repaint()            
                    
    def repaint(self):
        for i in range(9):
            self.interface.effacer(i)
            if self.matrice[i] == 'croix':
                self.interface.tracer('croix', i)
            elif self.matrice[i] == 'rond' :
                self.interface.tracer('rond', i)

def printMatrice(M):
    for i in range(len(M)):
        print(M[i])
     
def adversaire(joueur):
    if joueur == 'croix':
        return 'rond'
    return 'croix'

def copyMatrice(M):
    L=copy.deepcopy(M)
    return L

if __name__ == "__main__" :
    jeu = Interface()
    jeu.mainloop()
