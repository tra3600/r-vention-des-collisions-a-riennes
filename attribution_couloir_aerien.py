def attribuer_couloir_aerien(plans_de_vol, couloirs_aeriens):
    """
    Attribue un couloir aérien à chaque vol en fonction de l'altitude de croisière souhaitée.
    
    Paramètres:
    plans_de_vol (list): Liste des plans de vol.
    couloirs_aeriens (list): Liste des couloirs aériens disponibles. Chaque couloir est un dictionnaire contenant
                             les clés 'id', 'altitude_min' et 'altitude_max'.
    
    Retourne:
    list: Liste des plans de vol avec les couloirs aériens attribués.
    """
    for plan_de_vol in plans_de_vol:
        altitude_croisiere = plan_de_vol["altitude_croisiere"]
        for couloir in couloirs_aeriens:
            if couloir["altitude_min"] <= altitude_croisiere <= couloir["altitude_max"]:
                plan_de_vol["couloir_aerien"] = couloir["id"]
                break
    return plans_de_vol

# Exemple de test
couloirs_aeriens = [
    {"id": "A1", "altitude_min": 30000, "altitude_max": 35000},
    {"id": "A2", "altitude_min": 35001, "altitude_max": 40000}
]
plans_de_vol = attribuer_couloir_aerien(plans_de_vol, couloirs_aeriens)
print(plans_de_vol)