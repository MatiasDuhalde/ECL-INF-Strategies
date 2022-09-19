"""
Algorithme à Essais Successifs (AES)

Structure générale d'un algorithme AES
"""


def AES_basique(etat_courant, fonction_de_transition, actions_possibles, etat_final):
    if etat_courant == etat_final:
        return True
    for action_possible in actions_possibles:
        for etat_successeur in fonction_de_transition(etat_courant, action_possible):
            if AES_basique(etat_successeur, fonction_de_transition, actions_possibles, etat_final):
                return True
    return False
