import unittest
from prevention_collisions import *


def vol(num, dep, arr, h1, h2, fl, jour="d1"):
    return PlanDeVol(num, dep, arr, h1, h2, fl, jour=jour)


class Tests(unittest.TestCase):
    def test_sens_inverse_meme_niveau(self):
        v = [vol("A", "CDG", "FCO", "08:00", "10:00", 300), vol("B", "FCO", "CDG", "08:30", "10:30", 300)]
        self.assertEqual(len(detecter_collision(v)), 1)

    def test_sens_inverse_horaires_disjoints(self):
        v = [vol("A", "CDG", "FCO", "07:00", "09:00", 300), vol("B", "FCO", "CDG", "10:00", "12:00", 300)]
        self.assertEqual(detecter_collision(v), [])

    def test_separation_verticale(self):
        v = [vol("A", "CDG", "FCO", "08:00", "10:00", 300), vol("B", "FCO", "CDG", "08:00", "10:00", 310)]
        self.assertEqual(detecter_collision(v), [])

    def test_autre_jour(self):
        v = [vol("A", "CDG", "FCO", "08:00", "10:00", 300), vol("B", "FCO", "CDG", "08:00", "10:00", 300, "d2")]
        self.assertEqual(detecter_collision(v), [])

    def test_arrivee_lendemain(self):
        self.assertEqual(vol("A", "CDG", "JFK", "22:00", "06:00", 350).fin, 6 * 60 + 1440)

    def test_doublon_et_erreurs(self):
        plans = []
        enregistrer_plan_de_vol(plans, vol("A", "CDG", "FCO", "08:00", "10:00", 300))
        with self.assertRaises(ValueError):
            enregistrer_plan_de_vol(plans, vol("A", "CDG", "FCO", "08:00", "10:00", 300))
        with self.assertRaises(ValueError):
            vol("X", "CDG", "ZZZ", "08:00", "10:00", 300)
        with self.assertRaises(ValueError):
            en_minutes("25:00")

    def test_couloirs(self):
        c = [{"id": "A1", "niveau_min": 300, "niveau_max": 350}]
        p = attribuer_couloir_aerien([vol("A", "CDG", "FCO", "8:00", "10:00", 300),
                                      vol("B", "CDG", "FCO", "8:00", "10:00", 390)], c)
        self.assertEqual([x.couloir_aerien for x in p], ["A1", None])

    def test_regulation_resout_conflit(self):
        v = [vol("A", "CDG", "FCO", "08:00", "10:00", 300), vol("B", "FCO", "CDG", "08:30", "10:30", 300)]
        c = matrice_conflit(v)
        self.assertEqual(nb_conflits(c), 3)  # (0,0),(1,2)? seuls niveaux égaux : (0,0),(1,1),(2,2)
        self.assertGreater(cout_rfl(c), 0)
        for reg in (minimal(c), regulation_optimale(c)[0]):
            self.assertEqual(cout_regulation(c, reg), 0)
            appliquer_regulation(v, reg)
            self.assertEqual(detecter_collision(v), [])
            appliquer_regulation(v, [0, 0])

    def test_minimal_pas_pire_que_rfl_et_valide(self):
        v = [vol("A", "CDG", "FCO", "08:00", "10:00", 300), vol("B", "FCO", "CDG", "08:30", "10:30", 300),
             vol("C", "CDG", "FCO", "08:10", "10:10", 300), vol("D", "ORY", "MAD", "08:00", "10:00", 300)]
        c = matrice_conflit(v)
        reg = minimal(c)
        self.assertEqual(len(reg), 4)
        self.assertLessEqual(cout_regulation(c, reg), cout_rfl(c))
        self.assertLessEqual(regulation_optimale(c)[1], cout_regulation(c, reg))
        self.assertEqual(sum(nb_vol_par_niveau_relatif(reg)), 4)


if __name__ == "__main__":
    unittest.main()
