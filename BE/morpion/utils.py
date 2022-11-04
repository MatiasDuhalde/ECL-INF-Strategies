from typing import Union

Case = tuple[int, int]

# (dict_cases_joueurs, liste_cases_vides, dernière_case_placée, dernière case enlevée)
Plateau = tuple[dict[str, list[Case]], list[Case], Case, Union[Case, None]]
