def nb_vol_par_niveau_relatif(regulation):
    """
    Renvoie le nombre de vols à chaque niveau relatif.
    
    Paramètres:
    regulation (list of int): Liste des niveaux relatifs pour chaque vol.
    
    Retourne:
    list of int: Liste [a, b, c] où a est le nombre de vols à leurs niveaux RFL,
                 b est le nombre de vols au-dessus de leurs niveaux RFL,
                 et c est le nombre de vols au-dessous de leurs niveaux RFL.
    """
    a = regulation.count(0)
    b = regulation.count(1)
    c = regulation.count(2)
    return [a, b, c]

# Exemple d'utilisation
regulation = [0, 1, 0, 2, 1, 0, 2, 2, 1]
print(nb_vol_par_niveau_relatif(regulation))  # Devrait afficher [3, 3, 3]