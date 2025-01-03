# Exemple de plan de vol
plan_de_vol = {
    "numero_vol": "AF123",
    "compagnie": "Air France",
    "heure_depart": "10:00",
    "heure_arrivee": "14:00",
    "aeroport_depart": "CDG",
    "aeroport_arrivee": "JFK",
    "altitude_croisiere": 35000,  # en pieds
    "couloir_aerien": None  # à attribuer ultérieurement
}

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


def detecter_collision(plans_de_vol):
    """
    Détecte les risques de collision entre les vols en fonction de l'altitude et des horaires.
    
    Paramètres:
    plans_de_vol (list): Liste des plans de vol.
    
    Retourne:
    list: Liste des paires de vols présentant un risque de collision.
    """
    risques_collision = []
    for i in range(len(plans_de_vol)):
        for j in range(i + 1, len(plans_de_vol)):
            vol1 = plans_de_vol[i]
            vol2 = plans_de_vol[j]
            # Vérification des altitudes proches (moins de 1000 pieds d'écart)
            if abs(vol1["altitude_croisiere"] - vol2["altitude_croisiere"]) <= 1000:
                # Vérification des horaires de croisement
                if (vol1["heure_depart"] <= vol2["heure_arrivee"] and vol1["heure_arrivee"] >= vol2["heure_depart"]):
                    risques_collision.append((vol1["numero_vol"], vol2["numero_vol"]))
    return risques_collision

# Exemple de test
plan_de_vol_2 = {
    "numero_vol": "DL456",
    "compagnie": "Delta",
    "heure_depart": "11:00",
    "heure_arrivee": "15:00",
    "aeroport_depart": "JFK",
    "aeroport_arrivee": "LAX",
    "altitude_croisiere": 36000,
    "couloir_aerien": None
}
plans_de_vol = enregistrer_plan_de_vol(plans_de_vol, plan_de_vol_2)
risques_collision = detecter_collision(plans_de_vol)
print(risques_collision)