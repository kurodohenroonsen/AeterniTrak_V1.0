# État Claude AI (Master Verifier) — AeterniTrak V1.0

- **Rôle** : Architecte Suprême, rédaction des vecteurs formels, validation sur pièces, arbitrage et fusion sur `main`.
- **Dernière révision** : 2026-10-04 — cycle de revue 0010.
- **Branche active** : `agent-mailbox` (messages) ; `main` à **`98c3892`**.
- **Fichier rédigé par Claude AI uniquement.**

## Cycle 0010 (2026-10-04)
| Message | Verdict | Réponse |
|---|---|---|
| 0058 règle P18 (`7d804cb`) | validé, fusionné (`a9567f2`) ; 212/212, 8/8 mutations, 570 000 revendications sans écart | ordre 0064 |
| 0059 validité des clés K2 (`0fb4afa`) | validé, fusionné (`9421adb`) ; 144/144, 9/9 mutations ; écarts du fuzzing dus au décodeur, pas à la branche | ordres 0064, 0065 |
| 0060 spécification du certificat v1.1.0 (`effa3c0`) | validé, fusionné (`97dcfdf`) | ordre 0066 |
| 0061 portail (`213e066`) | non fusionné : autonome, mais tableau juridique non vérifiable et chiffres sans source | redirect 0067 |
| 0062 études de droit (`85a8dec`) | non fusionné : deux liens Wallex ouverts, deux erreurs 404 ; détails d'API non sourcés | redirect 0068 |
| 0063 acquittement du cycle 0009 (`1ee3daa`) | validé, fusionné (`a500ca2`) | ordre 0064 |
| 0052 décisions DEC-AET-08 et 09 (`ea52868`) | branche abandonnée ; décisions inscrites par moi | ordre 0064 |

- Après les fusions de code (`9421adb`) : 597 PASS, 0 FAIL.
- Livré sur `main` via `tests/0064-notation-and-batch-certificate` : `core.cbor.rules-v12` (16), `core.profile.rules-v11` (5), `crypto.cose.rules-v13` (5), `crypto.batch-certificate` (70) ; `README.md` §3 règle AVN-R, §4.13, §4.14 ; DEC-AET-08 et 09 ; `PROTOCOL.md` P7 et P8.
- **Banc sur `main@98c3892` : 18 suites, 693 vecteurs, 600 PASS, 13 FAIL, 70 RED, 10 INVALID (code de sortie 2).**
- **Défaut trouvé ce cycle, présent sur `main` depuis la fusion de `core/cbor`** : le décodeur rend de l'AVN, et une carte CBOR à clés texte `$tag`, `$map`, `$int`, `$bytes` passe pour un tag, une carte à clés entières, un entier, une chaîne d'octets. Le validateur du profil déclare valides cinq profils qui ne le sont pas. Le décodeur de contrôle du harnais a le même défaut (10 INVALID).
- Sur `main` : `core/cbor`, `core/jcs`, `core/profile`, `core/cose` (K2 compris), `validators/antiprion` (règles 1.5.0).

## Décisions de Kudoro actées (2026-10-04)
- **DEC-AET-01** : cartes ACOSJ 92 Ko uniquement ; le contenu de la carte reste à prouver par `STORAGE-001`.
- **DEC-AET-02** : connecteurs API vers les guichets officiels, CERISE en premier ; existence des API à établir.
- **DEC-AET-04** : option C, COSE_Sign1 agile.
- **DEC-AET-08** : quatre applications (conception des cartes, encodage par les membres, lecture par les participants, traçabilité).
- **DEC-AET-09** : toutes les plateformes ; faisabilité à prouver fonction par fonction (NFC web : Chrome Android seul ; WebUSB : Chromium seul).
- **DEC-AET-05** : dérogation de mémoire forestière privée, animaux de compagnie catégorie 1 LFA négatifs ; humains exclus.
- **DEC-AET-06** : correction du vecteur `CBOR-REJ-006`.
- **DEC-AET-07** : option B, bandeau pour un émetteur inconnu, blocage pour une clé révoquée ou une signature fausse.
- **Prénom « Guy »** : maintenu, en hommage.

## Limites connues de ce qui est certifié
- Le vert prouve la conformité aux vecteurs et à mes références, pas au droit.
- **Mes fuzzings ne trouvent que ce que leur générateur sait produire.** La confusion de notation a traversé 60 010 profils et 21 000 enveloppes sans apparaître, faute de clés `$…`. Zéro écart ne vaut que pour la famille d'entrées jouée.
- Les 70 attentes du certificat et les 45 de K2 viennent de ma seule référence. Le JCS des revendications a été recalculé par `core/jcs` (13 objets, 0 écart) ; rien d'autre n'a de seconde source.
- P18 et P4 sont plus stricts que le règlement 2017/893, qui admet certains substrats animaux de catégorie 3. Lecture faite sur une seule consultation en ligne.
- Je ne peux pas ouvrir `ejustice.just.fgov.be` : aucun lien fédéral du portail ou des études n'a été vérifié par moi.
- La date d'émission est déclarée par le signataire : la fenêtre de validité ne protège pas contre une clé volée qui antidate.
- Non couvert par des vecteurs : authentification du registre de politiques, émission ES256, plusieurs moteurs ou snapshots, signatures Ed25519 à points d'ordre faible, composition profil + enveloppe au-delà de `cose-open`.

## Conventions arrêtées
- Fichiers de gouvernance : `main` fait foi ; `agent-mailbox` ne porte que `mailbox/`.
- Branches : `ag/bushi-NN-<slug>`, `ag/orchestrator-<slug>`, `fix/bushi-NN-<slug>`, `tests/*` ; toujours depuis `main`.
- Numérotation globale continue ; prochain numéro libre, les deux boîtes confondues : `0069`.
- Budget bloc 1 : enveloppe COSE_Sign1 ≤ 2 048 o, charge utile ≤ 1 900 o.
- Type d'enveloppe : paramètre `typ`, étiquette 16, en-tête protégé (`application/aeternitrak-profile+cbor`, `application/aeternitrak-batch-claim+cbor`).
- Porte de Fer : `evaluate(claim, policy)` ; aucune dérogation en dur.
- Une faute de décodage remonte toujours avec son code `ERR_CBOR_*` ; les registres `ERR_PROFILE_*` et `ERR_COSE_*` ne la doublent pas.
- Validité d'une clé : fenêtre comparée à la date d'émission de la charge utile vérifiée, jamais à la date de lecture ; statuts `ACTIVE`, `RETIRED`, `REVOKED`.
- Lecture d'une carte : `cose-open` (DEC-AET-07 option B) ; seul un émetteur inconnu rend le contenu sous réserve ; un contenu `UNVERIFIED` n'a aucune valeur de preuve.
- Une clé d'en-tête COSE est un entier ; aucune conversion depuis un texte.
- Une entrée du registre des décisions cite Kudoro entre guillemets ; toute affirmation de droit ou de capacité matérielle y est sourcée ou absente.
- Un certificat de lot ne passe jamais par `cose-open` ; sa politique de dérogation vient du registre du vérificateur, jamais du présentateur.
- La liste de motifs n'entre pas dans le certificat (il n'existe que pour `AUTHORISED`) ; elle sert au journal des refus.
- Règle AVN-R : un objet JSON simple ne porte jamais de clé en `$` ; un validateur juge l'élément CBOR, pas sa notation.
- Certificat de lot, v1 : moteur unique (`RULES_VERSION`, empreinte de snapshot `55717d33…2c90`) ; refus d'émission `ERR_CERT_ISSUANCE_REFUSED` avec `refusal_reasons`.
- `PROTOCOL.md` P7 : j'inscris moi-même les décisions de Kudoro, avec ses mots. P8 : un lien cité a été ouvert.

## En attente chez Antigravity
1. `fix/bushi-01-decoder-notation` (0065) : harnais puis `core/cbor` ; attendu 0 FAIL, 0 INVALID. **Prioritaire.**
2. `ag/bushi-02-batch-certificate` (0066) : `core/cert`, adaptateur `crypto.cert` ; attendu 70 PASS (69 admis avant 0065).
3. Portail (0067) et études de droit (0068), citations de P18 (0068, L5).
4. Acquittement 0064.

## En attente de l'arbitrage de Kudoro
- `DEC-AET-03` : trois options posées par l'étude 0062 (ancrage communal, exécuteur testamentaire notarié, déclaration sans opposabilité). L'étude n'est pas fusionnée : ses liens ne s'ouvrent pas. À faire relire par un juriste avant de trancher.
- Référence de l'autorisation administrative pour DEC-AET-05 : toujours ouverte. Constat partagé : aucune voie automatique, une autorisation expresse par lot ou par site.
- P18 : arrêtée par moi, plus stricte que le texte ; Kudoro peut la renverser.

## Prochaines actions Claude AI
- Rejouer les fuzzings du profil, des enveloppes et du décodeur avec des clés `$…` à tous les niveaux sur `fix/bushi-01-decoder-notation`.
- Fuzzing différentiel émission puis vérification sur `ag/bushi-02-batch-certificate`.
- Vecteurs de composition profil + enveloppe (`open-profile`) : toujours dus.
