def minimal():
    """
    Applique l'algorithme Minimal pour trouver la régulation minimale.
    
    Retourne:
    list of int: Régulation résultante.
    """
    n = len(conflit) // 3
    etat_sommet = [2] * (3 * n)  # Initialement, tous les sommets sont "autres" (2)
    regulation = [-1] * n  # Initialiser la régulation
    
    for _ in range(n):
        s = sommet_de_cout_min(etat_sommet)
        etat_sommet[s] = 1  # Marquer le sommet comme choisi
        regulation[s // 3] = s % 3  # Mettre à jour la régulation
        
        # Supprimer les deux autres niveaux possibles pour ce vol
        etat_sommet[3 * (s // 3) + (s % 3 + 1) % 3] = 0
        etat_sommet[3 * (s // 3) + (s % 3 + 2) % 3] = 0
    
    return regulation

# Exemple d'utilisation
print(minimal())  # Devrait afficher la régulation minimale