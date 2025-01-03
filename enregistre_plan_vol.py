def enregistrer_plan_de_vol(plans_de_vol, plan_de_vol):
    """
    Enregistre un plan de vol dans la liste des plans de vol existants.
    
    Paramètres:
    plans_de_vol (list): Liste des plans de vol existants.
    plan_de_vol (dict): Dictionnaire contenant les informations du plan de vol à enregistrer.
    
    Retourne:
    list: Liste mise à jour des plans de vol incluant le nouveau plan de vol.
    """
    plans_de_vol.append(plan_de_vol)
    return plans_de_vol

# Exemple de test
plans_de_vol = []
plan_de_vol_1 = {
    "numero_vol": "AF123",
    "compagnie": "Air France",
    "heure_depart": "10:00",
    "heure_arrivee": "14:00",
    "aeroport_depart": "CDG",
    "aeroport_arrivee": "JFK",
    "altitude_croisiere": 35000,
    "couloir_aerien": None
}
plans_de_vol = enregistrer_plan_de_vol(plans_de_vol, plan_de_vol_1)
print(plans_de_vol)