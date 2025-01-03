def cout_du_sommet(s, etat_sommet):
    """
    Calcule le coût d'un sommet dans le graphe défini par la variable globale 'conflit' et 'etat_sommet'.
    
    Paramètres:
    s (int): Numéro du sommet.
    etat_sommet (list of int): Liste indiquant l'état de chaque sommet (0 pour supprimé, 1 pour choisi, 2 pour autres).
    
    Retourne:
    int: Coût du sommet.
    """
    n = len(etat_sommet)
    cout = 0
    
    for i in range(n):
        if etat_sommet[i] == 2:  # Seulement considérer les sommets qui n'ont pas été supprimés
            cout += conflit[s][i]
    
    return cout

# Exemple d'utilisation
etat_sommet = [2] * 9  # Initialement, tous les sommets sont "autres" (2)
print(cout_du_sommet(0, etat_sommet))  # Devrait afficher le coût du sommet 0