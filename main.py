from prevention_collisions import *

couloirs = [{"id": "A1", "niveau_min": 300, "niveau_max": 350},
            {"id": "A2", "niveau_min": 351, "niveau_max": 400}]
plans = []
for args in [("AF1204", "CDG", "FCO", "07:35", "09:50", 300),
             ("AF1205", "FCO", "CDG", "08:10", "10:25", 300),
             ("AF1504", "CDG", "FCO", "08:00", "10:15", 305),
             ("AF1505", "FCO", "CDG", "13:00", "15:10", 310)]:
    enregistrer_plan_de_vol(plans, PlanDeVol(*args[:5], niveau=args[5], jour="2016-05-02"))
attribuer_couloir_aerien(plans, couloirs)

print("Conflits au RFL :", detecter_collision(plans))
c = matrice_conflit(plans)
reg, cout = minimal(c), None
print("Heuristique :", reg, "coût", cout_regulation(c, reg), "(RFL :", cout_rfl(c), ")")
print("Optimum     :", *regulation_optimale(c))
appliquer_regulation(plans, regulation_optimale(c)[0])
print("Conflits après régulation :", detecter_collision(plans))
