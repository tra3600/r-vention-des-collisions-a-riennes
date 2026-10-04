"""Prévention des collisions aériennes.

Pipeline complet :
  1. enregistrement des plans de vol,
  2. attribution des couloirs aériens (par niveau de vol),
  3. détection des conflits (séparation verticale ET horizontale),
  4. construction du graphe de conflits (3 niveaux relatifs par vol),
  5. régulation : heuristique « minimale » ou optimum exact.

Niveaux de vol (FL) en centaines de pieds. Niveau relatif d'un vol :
0 = son RFL (niveau demandé), 1 = RFL + 10 (1000 ft au-dessus), 2 = RFL - 10.
"""
from dataclasses import dataclass, field
from itertools import product
from math import cos, radians, sqrt, ceil
from typing import Dict, List, Optional, Tuple

SEPARATION_VERTICALE = 10      # FL (= 1000 ft)
SEPARATION_HORIZONTALE = 5.0   # milles nautiques
DECALAGES = (0, 10, -10)       # niveau relatif -> décalage de FL

# (latitude, longitude) en degrés
AEROPORTS: Dict[str, Tuple[float, float]] = {
    "CDG": (49.0097, 2.5479), "ORY": (48.7233, 2.3794), "FCO": (41.8003, 12.2389),
    "JFK": (40.6413, -73.7781), "LAX": (33.9416, -118.4085), "LHR": (51.4700, -0.4543),
    "MAD": (40.4983, -3.5676), "FRA": (50.0379, 8.5622), "AMS": (52.3105, 4.7683),
    "NCE": (43.6584, 7.2159), "LYS": (45.7256, 5.0811), "BCN": (41.2974, 2.0833),
}


def en_minutes(heure: str) -> int:
    """'HH:MM' -> minutes depuis minuit (ValueError si le format est invalide)."""
    h, m = heure.split(":")
    h, m = int(h), int(m)
    if not (0 <= h < 24 and 0 <= m < 60):
        raise ValueError(f"heure invalide : {heure!r}")
    return h * 60 + m


@dataclass
class PlanDeVol:
    numero_vol: str
    aeroport_depart: str
    aeroport_arrivee: str
    heure_depart: str
    heure_arrivee: str
    niveau: int                      # RFL en FL (ex. 350)
    compagnie: str = ""
    jour: str = ""
    couloir_aerien: Optional[str] = None
    niveau_effectif: Optional[int] = field(default=None, repr=False)

    def __post_init__(self):
        for a in (self.aeroport_depart, self.aeroport_arrivee):
            if a not in AEROPORTS:
                raise ValueError(f"aéroport inconnu : {a}")
        if self.aeroport_depart == self.aeroport_arrivee:
            raise ValueError("départ et arrivée identiques")
        if self.niveau <= 0:
            raise ValueError("niveau de vol invalide")
        if self.niveau_effectif is None:
            self.niveau_effectif = self.niveau

    @property
    def debut(self) -> int:
        return en_minutes(self.heure_depart)

    @property
    def fin(self) -> int:
        fin = en_minutes(self.heure_arrivee)
        # arrivée le lendemain
        return fin + 1440 if fin <= self.debut else fin


def enregistrer_plan_de_vol(plans: List[PlanDeVol], plan: PlanDeVol) -> List[PlanDeVol]:
    """Ajoute un plan de vol ; refuse les doublons (même numéro de vol et même jour)."""
    if any(p.numero_vol == plan.numero_vol and p.jour == plan.jour for p in plans):
        raise ValueError(f"plan de vol déjà enregistré : {plan.numero_vol}")
    plan.debut, plan.fin  # valide les horaires
    plans.append(plan)
    return plans


def attribuer_couloir_aerien(plans: List[PlanDeVol], couloirs: List[dict]) -> List[PlanDeVol]:
    """Affecte à chaque vol le premier couloir dont [niveau_min, niveau_max] contient son niveau.

    Les vols sans couloir compatible gardent ``couloir_aerien = None``.
    """
    for p in plans:
        p.couloir_aerien = next(
            (c["id"] for c in couloirs if c["niveau_min"] <= p.niveau <= c["niveau_max"]), None)
    return plans


# ---------------------------------------------------------------- géométrie

def _xy(code: str, lat0: float) -> Tuple[float, float]:
    """Projection plane (NM) autour de la latitude lat0."""
    lat, lon = AEROPORTS[code]
    return lon * 60 * cos(radians(lat0)), lat * 60


def _trajectoire(p: PlanDeVol, lat0: float):
    """Position linéaire en fonction du temps : pos(t) = a + v*t."""
    (x0, y0), (x1, y1) = _xy(p.aeroport_depart, lat0), _xy(p.aeroport_arrivee, lat0)
    d = p.fin - p.debut
    vx, vy = (x1 - x0) / d, (y1 - y0) / d
    return x0 - vx * p.debut, y0 - vy * p.debut, vx, vy


def duree_perte_separation(p1: PlanDeVol, p2: PlanDeVol,
                           rayon: float = SEPARATION_HORIZONTALE) -> float:
    """Durée (minutes) pendant laquelle les deux avions sont à moins de ``rayon`` NM l'un de l'autre,
    en vol simultané, sur des trajectoires rectilignes à vitesse constante (indépendamment du niveau)."""
    t0, t1 = max(p1.debut, p2.debut), min(p1.fin, p2.fin)
    if t0 >= t1:
        return 0.0
    lat0 = sum(AEROPORTS[c][0] for c in (p1.aeroport_depart, p1.aeroport_arrivee,
                                         p2.aeroport_depart, p2.aeroport_arrivee)) / 4
    ax, ay, vx1, vy1 = _trajectoire(p1, lat0)
    bx, by, vx2, vy2 = _trajectoire(p2, lat0)
    # position relative r(t) = r0 + w*t ; on cherche |r|^2 <= rayon^2
    rx, ry, wx, wy = ax - bx, ay - by, vx1 - vx2, vy1 - vy2
    a = wx * wx + wy * wy
    b = 2 * (rx * wx + ry * wy)
    c = rx * rx + ry * ry - rayon * rayon
    if a < 1e-12:                       # même vecteur vitesse : distance constante
        return float(t1 - t0) if c <= 0 else 0.0
    disc = b * b - 4 * a * c
    if disc < 0:
        return 0.0
    s = sqrt(disc)
    lo, hi = (-b - s) / (2 * a), (-b + s) / (2 * a)
    return max(0.0, min(hi, t1) - max(lo, t0))


def en_conflit(p1: PlanDeVol, p2: PlanDeVol) -> float:
    """Durée de conflit (min) : séparation verticale < 1000 ft ET horizontale < 5 NM."""
    if p1.jour != p2.jour:
        return 0.0
    if abs(p1.niveau_effectif - p2.niveau_effectif) >= SEPARATION_VERTICALE:
        return 0.0
    return duree_perte_separation(p1, p2)


def detecter_collision(plans: List[PlanDeVol]) -> List[Tuple[str, str, float]]:
    """Liste des (vol1, vol2, durée du conflit en min) aux niveaux effectifs actuels."""
    res = []
    for i in range(len(plans)):
        for j in range(i + 1, len(plans)):
            d = en_conflit(plans[i], plans[j])
            if d > 0:
                res.append((plans[i].numero_vol, plans[j].numero_vol, round(d, 1)))
    return res


# ------------------------------------------------- graphe de conflits / régulation

def matrice_conflit(plans: List[PlanDeVol]) -> List[List[int]]:
    """Matrice 3n x 3n ; sommet 3*i+k = vol i au niveau relatif k. Coût = minutes de conflit (>= 1)."""
    n = len(plans)
    m = [[0] * (3 * n) for _ in range(3 * n)]
    sauv = [p.niveau_effectif for p in plans]
    for i in range(n):
        for j in range(i + 1, n):
            for ki, kj in product(range(3), repeat=2):
                plans[i].niveau_effectif = plans[i].niveau + DECALAGES[ki]
                plans[j].niveau_effectif = plans[j].niveau + DECALAGES[kj]
                d = en_conflit(plans[i], plans[j])
                if d > 0:
                    m[3 * i + ki][3 * j + kj] = m[3 * j + kj][3 * i + ki] = max(1, ceil(d))
    for p, s in zip(plans, sauv):
        p.niveau_effectif = s
    return m


def nb_conflits(conflit: List[List[int]]) -> int:
    """Nombre d'arêtes de valuation non nulle."""
    n = len(conflit)
    return sum(1 for i in range(n) for j in range(i + 1, n) if conflit[i][j])


def cout_regulation(conflit: List[List[int]], regulation: List[int]) -> int:
    """Coût total d'une régulation (liste de niveaux relatifs, un par vol)."""
    n = len(regulation)
    return sum(conflit[3 * i + regulation[i]][3 * j + regulation[j]]
               for i in range(n) for j in range(i + 1, n))


def cout_rfl(conflit: List[List[int]]) -> int:
    """Coût quand chaque avion vole à son RFL."""
    return cout_regulation(conflit, [0] * (len(conflit) // 3))


def nb_vol_par_niveau_relatif(regulation: List[int]) -> List[int]:
    """[à RFL, au-dessus, au-dessous]."""
    return [regulation.count(k) for k in range(3)]


def cout_du_sommet(conflit, s: int, etat: List[int]) -> int:
    """Somme des conflits de s avec les sommets choisis (état 1, conflits certains) et ceux
    encore en jeu (état 2, conflits potentiels) ; les sommets supprimés (0) sont ignorés."""
    return sum(conflit[s][i] for i in range(len(etat)) if etat[i] != 0)


def sommet_de_cout_min(conflit, etat: List[int]) -> int:
    candidats = [s for s in range(len(etat)) if etat[s] == 2]
    return min(candidats, key=lambda s: cout_du_sommet(conflit, s, etat))


def minimal(conflit: List[List[int]]) -> List[int]:
    """Heuristique gloutonne : choisit à chaque étape le sommet de coût minimal, élimine les 2 autres
    niveaux du même vol."""
    n = len(conflit) // 3
    etat = [2] * (3 * n)
    regulation = [0] * n
    for _ in range(n):
        s = sommet_de_cout_min(conflit, etat)
        regulation[s // 3] = s % 3
        for k in range(3):
            etat[3 * (s // 3) + k] = 0
        etat[s] = 1
    return regulation


def regulation_optimale(conflit: List[List[int]]) -> Tuple[List[int], int]:
    """Optimum exact par énumération (3^n, à réserver à de petites instances)."""
    n = len(conflit) // 3
    if n > 12:
        raise ValueError("trop de vols pour l'énumération exhaustive")
    meilleur = min(product(range(3), repeat=n), key=lambda r: cout_regulation(conflit, list(r)))
    return list(meilleur), cout_regulation(conflit, list(meilleur))


def appliquer_regulation(plans: List[PlanDeVol], regulation: List[int]) -> List[PlanDeVol]:
    for p, k in zip(plans, regulation):
        p.niveau_effectif = p.niveau + DECALAGES[k]
    return plans
