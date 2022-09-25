"""Outils"""

import numpy as np

Case = tuple[int, int]


def creer_matrice(dim: int) -> np.ndarray:
    """Créer une matrice carrée de taille dim remplie de -1

    Args:
        dim (int): dimension de la matrice à créer

    Returns:
        np.ndarray: matrice résultant
    """
    return -1 * np.ones((dim, dim))


def creer_matrice_avec_bandes(dim: int) -> np.ndarray:
    """Créer une matrice avec bandes carrée de taille dim remplie de -1

    Args:
        dim (int): dimension de la matrice à créer (sans compter les bandes)

    Returns:
        np.ndarray: matrice résultant
    """
    m_base = np.zeros((dim + 4, dim + 4))
    for i in range(2, dim + 2):
        for j in range(2, dim + 2):
            m_base[i][j] = -1
    return m_base
