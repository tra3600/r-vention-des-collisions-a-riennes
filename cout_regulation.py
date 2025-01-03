def cout_regulation(regulation):
    """
    Renvoie le coût d'une régulation.
    
    Paramètres:
    regulation (list of int): Liste des niveaux relatifs pour chaque vol.
    
    Retourne:
    int: Coût total des conflits potentiels pour cette régulation.
    """
    n = len(regulation)
    total_cost = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            sommet_i = 3 * i + regulation[i]
            sommet_j = 3 * j + regulation[j]
            total_cost += conflit[sommet_i][sommet_j]
    
    return total_cost

# Exemple d'utilisation
regulation = [0, 1, 0, 2, 1, 0, 2, 2, 1]
print(cout_regulation(regulation))  # Devrait afficher le coût total pour cette régulation