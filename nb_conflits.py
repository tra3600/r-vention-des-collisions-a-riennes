# Exemple de matrice de conflits
conflit = [
    [0, 0, 0, 100, 100, 0, 0, 150, 0],
    [0, 0, 0, 0, 0, 50, 0, 0, 0],
    [0, 0, 0, 0, 200, 0, 0, 300, 50],
    [100, 0, 0, 0, 0, 0, 400, 0, 0],
    [100, 0, 200, 0, 0, 0, 200, 0, 100],
    [0, 50, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 400, 200, 0, 0, 0, 0],
    [150, 0, 300, 0, 0, 0, 0, 0, 0],
    [0, 0, 50, 0, 100, 0, 0, 0, 0]
]

def nb_conflits():
    """
    Renvoie le nombre de conflits potentiels, c'est-à-dire le nombre d'arêtes de valuation non nulle du graphe.
    
    Retourne:
    int: Nombre de conflits potentiels.
    """
    n = len(conflit)
    nb_conflits = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            if conflit[i][j] != 0:
                nb_conflits += 1
                
    return nb_conflits

# Exemple d'utilisation
print(nb_conflits())  # Devrait afficher le nombre de conflits potentiels
