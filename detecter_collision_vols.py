def detecter_collision_vols(vols):
    """
    Détecte les risques de collision entre les vols en fonction de leur niveau de vol et de leurs horaires.
    
    Paramètres:
    vols (list of dict): Liste des vols avec leurs informations.
    
    Retourne:
    list of tuple: Liste des paires de vols présentant un risque de collision.
    """
    risques_collision = []
    
    for i in range(len(vols)):
        for j in range(i + 1, len(vols)):
            vol1 = vols[i]
            vol2 = vols[j]
            
            # Vérifier si les niveaux de vol sont proches (moins de 1000 pieds d'écart)
            if abs(vol1["niveau"] - vol2["niveau"]) <= 10:
                # Vérifier si les horaires de croisement sont proches
                if (vol1["jour"] == vol2["jour"] and
                    vol1["heure"] <= vol2["heure"] <= vol1["heure"] or
                    vol2["heure"] <= vol1["heure"] <= vol2["heure"]):
                    risques_collision.append((vol1["id_vol"], vol2["id_vol"]))
    
    return risques_collision

# Exemple d'utilisation
vols = [
    {"id_vol": "AF1204", "depart": "CDG", "arrivee": "FCO", "jour": "2016-05-02", "heure": "07:35", "niveau": 300},
    {"id_vol": "AF1205", "depart": "FCO", "arrivee": "CDG", "jour": "2016-05-02", "heure": "10:25", "niveau": 300},
    {"id_vol": "AF1504", "depart": "CDG", "arrivee": "FCO", "jour": "2016-05-02", "heure": "10:05", "niveau": 310},
    {"id_vol": "AF1505", "depart": "FCO", "arrivee": "CDG", "jour": "2016-05-02", "heure": "13:00", "niveau": 310}
]

risques_collision = detecter_collision_vols(vols)
print(risques_collision)