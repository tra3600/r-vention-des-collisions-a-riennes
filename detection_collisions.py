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