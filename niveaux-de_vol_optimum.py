import itertools

# Représentation des coûts des conflits dans un dictionnaire
conflits = {
    ('A_0', 'B_0'): 100,
    ('B_0', 'C_0'): 400,
    ('A_+', 'B_0'): 50,
    ('A_0', 'C_+'): 150,
    ('B_+', 'C_0'): 300,
    ('A_0', 'C_-'): 200,
    # Ajouter les autres conflits ici
}

# Fonction pour calculer le coût total d'une combinaison donnée
def calculer_cout(combinaison, conflits):
    cout_total = 0
    for (vol1, niveau1), (vol2, niveau2) in itertools.combinations(combinaison.items(), 2):
        sommet1 = f"{vol1}_{niveau1}"
        sommet2 = f"{vol2}_{niveau2}"
        cout_total += conflits.get((sommet1, sommet2), 0) + conflits.get((sommet2, sommet1), 0)
    return cout_total

# Fonction pour trouver la combinaison optimale
def trouver_combinaison_optimal(vols, niveaux, conflits):
    min_cout = float('inf')
    meilleure_combinaison = None
    for combinaison in itertools.product(niveaux, repeat=len(vols)):
        combinaison_dict = dict(zip(vols, combinaison))
        cout_total = calculer_cout(combinaison_dict, conflits)
        if cout_total < min_cout:
            min_cout = cout_total
            meilleure_combinaison = combinaison_dict
    return meilleure_combinaison, min_cout

# Exemple d'utilisation
vols = ['A', 'B', 'C']
niveaux = ['0', '+', '-']
meilleure_combinaison, min_cout = trouver_combinaison_optimal(vols, niveaux, conflits)

print(f"Meilleure combinaison: {meilleure_combinaison}")
print(f"Coût total des conflits: {min_cout}")