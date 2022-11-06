"""Travail à rendre 2
"""


from morpion_interface import Interface
from morpion_v4 import Morpion

if __name__ == '__main__':
    DIM = 3
    # humain vs humain
    # interface = Interface(Morpion, DIM)

    # humain vs ia
    interface = Interface(Morpion, DIM, 'ia')

    # ia vs ia
    # interface = Interface(Morpion, DIM, 'ia', 'ia')
    interface.commencer()
