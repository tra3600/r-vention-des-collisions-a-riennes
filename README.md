# r-vention-des-collisions-a-riennes
déterminer le risque de collision entre deux avions  -couloirs aériens proches
Partie I: Enregistrement des plans de vol
Dans cette partie, nous allons aborder l'enregistrement des plans de vol des différentes compagnies aériennes. Nous allons définir des structures de données en Python pour stocker ces informations et écrire des fonctions pour effectuer des opérations sur ces données.

I.A - Structures de données pour les plans de vol
Supposons que chaque plan de vol contient les informations suivantes :

Numéro de vol
Compagnie aérienne
Heure de départ
Heure d'arrivée
Aéroport de départ
Aéroport d'arrivée
Altitude de croisière
Couloir aérien (à attribuer ultérieurement)

I.B - Fonction d'enregistrement des plans de vol
Nous allons écrire une fonction enregistrer_plan_de_vol qui prend en argument un plan de vol et l'ajoute à une liste de plans de vol existants.

Partie II: Attribution des couloirs aériens
Dans cette partie, nous allons écrire une fonction pour attribuer un couloir aérien à chaque vol en fonction de l'altitude de croisière souhaitée.

II.A - Attribution d'un couloir aérien
Supposons que nous avons une liste de couloirs aériens disponibles avec leurs altitudes minimales et maximales. Nous allons écrire une fonction attribuer_couloir_aerien qui prend en argument la liste des plans de vol et la liste des couloirs aériens disponibles, et attribue à chaque vol un couloir aérien répondant au mieux à ses souhaits.

Partie III: Détection de collision
Dans cette partie, nous allons écrire une fonction pour détecter un risque de collision entre deux avions se croisant à des altitudes proches.

III.A - Fonction de détection de collision
Nous allons écrire une fonction detecter_collision qui prend en argument la liste des plans de vol et détecte les risques de collision en fonction de l'altitude et des horaires.

Nous avons défini des structures de données en Python pour enregistrer les plans de vol, attribuer des couloirs aériens et détecter les risques de collision. Ces fonctions permettent de gérer les opérations de base nécessaires à la prévention des collisions aériennes.

Requêtes SQL pour la gestion des plans de vol
Pour gérer les plans de vol et les informations sur les aéroports, nous devons effectuer plusieurs requêtes SQL. Voici quelques exemples de requêtes pour répondre à différentes questions sur les tables vol et aeroport.

I.A - Requête SQL pour obtenir tous les vols d'un certain jour
Pour obtenir tous les vols qui décollent un jour spécifique, vous pouvez utiliser la requête suivante :

SQL
SELECT * 
FROM vol 
WHERE jour = '2016-05-02';
I.B - Requête SQL pour obtenir les vols entre deux aéroports spécifiques
Pour obtenir tous les vols entre deux aéroports spécifiques, vous pouvez utiliser la requête suivante :

SQL
SELECT * 
FROM vol 
WHERE depart = 'CDG' AND arrivee = 'FCO';
I.C - Requête SQL pour obtenir les aéroports d'un pays spécifique
Pour obtenir la liste des aéroports dans un pays spécifique, vous pouvez utiliser la requête suivante :

SQL
SELECT * 
FROM aeroport 
WHERE pays = 'France';
I.D - Requête SQL pour obtenir les vols d'une compagnie aérienne spécifique
Pour obtenir tous les vols d'une compagnie aérienne spécifique (en utilisant un préfixe dans le numéro de vol, par exemple "AF" pour Air France), vous pouvez utiliser la requête suivante :

SQL
SELECT * 
FROM vol 
WHERE id_vol LIKE 'AF%';

Prévention des collisions aériennes
Pour prévenir les collisions aériennes, nous devons nous assurer que les avions ne volent pas à des altitudes trop proches les unes des autres. Nous pouvons utiliser une fonction Python pour vérifier les plans de vol et détecter les risques de collision.

Fonction Python pour détecter les risques de collision
Voici une fonction Python pour détecter les risques de collision entre les vols en fonction de leurs niveaux de vol et de leurs horaires de décollage et d'atterrissage :

Explications des Requêtes SQL et Fonction Python
Requêtes SQL :
I.A : Obtenir tous les vols d'un certain jour permet de filtrer les vols pour une date spécifique, utile pour la gestion quotidienne des vols.
I.B : Obtenir les vols entre deux aéroports spécifiques permet de suivre les trajets spécifiques, utile pour les statistiques de trafic aérien.
I.C : Obtenir les aéroports d'un pays spécifique permet de lister les aéroports dans une région particulière, utile pour les opérations nationales.
I.D : Obtenir les vols d'une compagnie aérienne spécifique permet de filtrer les vols pour une compagnie, utile pour la gestion des compagnies.
Fonction Python :
detecter_collision_vols : Cette fonction vérifie les niveaux de vol et les horaires des vols pour détecter les risques de collision. Les vols avec des niveaux de vol proches et des horaires de décollage et d'atterrissage proches sont considérés comme présentant un risque de collision.
Cette approche permet de gérer efficacement les plans de vol et de prévenir les collisions aériennes, en utilisant des requêtes SQL pour extraire les informations nécessaires et des fonctions Python pour analyser ces informations.

I.A – Requête SQL pour le nombre de vols décollant avant midi le 2 mai 2016
Pour obtenir le nombre de vols qui doivent décoller dans la journée du 2 mai 2016 avant midi, vous pouvez utiliser la requête suivante :

SQL
SELECT COUNT(*) AS nombre_de_vols
FROM vol
WHERE jour = '2016-05-02' AND heure < '12:00';
I.B – Requête SQL pour la liste des numéros de vols au départ d’un aéroport desservant Paris le 2 mai 2016
Pour obtenir la liste des numéros de vols au départ d'un aéroport desservant Paris le 2 mai 2016, vous pouvez utiliser la requête suivante :

SQL
SELECT id_vol
FROM vol
JOIN aeroport ON vol.depart = aeroport.id_aero
WHERE aeroport.ville = 'Paris' AND jour = '2016-05-02';
I.C – Explication de la requête SQL
La requête suivante sélectionne les numéros de vol (id_vol) des vols qui décollent et atterrissent dans des aéroports situés en France, pour la journée du 2 mai 2016 :

SQL
SELECT id_vol
FROM vol
JOIN aeroport AS d ON d.id_aero = depart
JOIN aeroport AS a ON a.id_aero = arrivee
WHERE
    d.pays = 'France' AND
    a.pays = 'France' AND
    jour = '2016-05-02';
Explications :
JOIN aeroport AS d ON d.id_aero = depart : Cette jointure associe chaque vol à son aéroport de départ, en utilisant un alias d pour l'aéroport de départ.
JOIN aeroport AS a ON a.id_aero = arrivee : Cette jointure associe chaque vol à son aéroport d'arrivée, en utilisant un alias a pour l'aéroport d'arrivée.
WHERE d.pays = 'France' AND a.pays = 'France' : Cette condition filtre les vols pour lesquels l'aéroport de départ (d.pays) et l'aéroport d'arrivée (a.pays) sont tous deux situés en France.
AND jour = '2016-05-02' : Cette condition filtre les vols pour la journée du 2 mai 2016.
Ainsi, cette requête fournit les numéros de vols qui partent et arrivent en France le 2 mai 2016.

