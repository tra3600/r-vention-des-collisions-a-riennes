def sommet_de_cout_min(etat_sommet):
    """
    Trouve le sommet de coût minimal parmi ceux qui n'ont pas encore été choisis ou supprimés.
    
    Paramètres:
    etat_sommet (list of int): Liste indiquant l'état de chaque sommet (0 pour supprimé, 1 pour choisi, 2 pour autres).
    
    Retourne:
    int: Numéro du sommet de coût minimal.
    """
    min_cout = float('inf')
    min_sommet = -1
    
    for s in range(len(etat_sommet)):
        if etat_sommet[s] == 2:  # Seulement considérer les sommets qui n'ont pas été supprimés ou choisis
            cout = cout_du_sommet(s, etat_sommet)
            if cout < min_cout:
                min_cout = cout
                min_sommet = s
    
    return min_sommet

# Exemple d'utilisation
etat_sommet = [2] * 9  # Initialement, tous les sommets sont "autres" (2)
print(sommet_de_cout_min(etat_sommet))  # Devrait afficher le numéro du sommet de coût minimal