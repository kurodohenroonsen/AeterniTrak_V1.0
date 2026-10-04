# État Claude AI (Master Verifier) — AeterniTrak V1.0

- **Rôle** : Architecte Suprême, rédaction des vecteurs formels, validation sur pièces, arbitrage et fusion sur `main`.
- **Dernière révision** : 2026-10-04 — cycle de revue 0008.
- **Branche active** : `agent-mailbox` (messages) ; `main` à **`4a87163`**.
- **Fichier rédigé par Claude AI uniquement.**

## Cycle 0008 (2026-10-04)
| Message | Verdict | Réponse |
|---|---|---|
| 0043 moteur COSE_Sign1 v1.1 (`32f7adc`) | validé, fusionné (`253267a`) ; 528 PASS reproduit, 7/7 mutations, 12 000 enveloppes fuzzées sans écart sur `cose-verify` et `cose-open` | ordre 0045 |
| 0044 acquittement du cycle 0007 (`1210a7e`) | validé, fusionné (`240b2d6`) | ordre 0045 |

- Livré sur `main` via `tests/0045-antiprion-rules-v14` : suite `antiprion.feedban.rules-v14` (19 cas, `PRION-HARD-073` à `091`), `README.md` §4.10 (P15 à P17).
- **Banc sur `main@4a87163` : 12 suites, 547 vecteurs, 532 PASS, 15 FAIL, 0 RED, 0 INVALID.** Les 15 FAIL sont les listes de motifs de la Porte de Fer que la suite v1.4 fixe ; aucun verdict n'est en cause (220 000 revendications, 0 écart de verdict).
- Sur `main` : `core/cbor`, `core/jcs`, `core/profile`, `core/cose`, `validators/antiprion`.

## Décisions de Kudoro actées (2026-10-04)
- **DEC-AET-04** : option C, COSE_Sign1 agile.
- **DEC-AET-05** : dérogation de mémoire forestière privée, animaux de compagnie catégorie 1 LFA négatifs ; humains exclus.
- **DEC-AET-06** : correction du vecteur `CBOR-REJ-006`.
- **DEC-AET-07** : option B, bandeau pour un émetteur inconnu, blocage pour une clé révoquée ou une signature fausse.
- **Prénom « Guy »** : maintenu, en hommage.

## Limites connues de ce qui est certifié
- Le vert prouve la conformité aux vecteurs et à mes références, pas au droit : les règles P5 et P6 de la Porte de Fer reposent sur la vérification EUR-Lex du Bushi 12, que je n'ai pas refaite.
- `main` porte 15 FAIL connus (listes de motifs, suite v1.4) jusqu'à la fusion de `fix/bushi-12-reasons-v14`. Les 19 cas couvrent les trois causes trouvées, pas forcément toutes celles qui existent : le rejeu des 220 000 revendications après correction le dira.
- Les attentes du profil que j'ai ajoutées viennent de ma seule référence ; le code livré s'y accorde sur 60 010 profils, ce qui confirme la cohérence, pas la justesse du CDDL.
- Option B : une carte d'émetteur inconnu s'affiche sans que sa signature ait pu être contrôlée. Une carte forgée avec un `kid` inventé s'affiche donc aussi, sous bandeau.
- Non couvert par des vecteurs : validité temporelle des clés, signatures Ed25519 forgées avec des points d'ordre faible, composition profil + enveloppe et certificat de lot + enveloppe.

## Conventions arrêtées
- Fichiers de gouvernance : `main` fait foi ; `agent-mailbox` ne porte que `mailbox/`.
- Branches : `ag/bushi-NN-<slug>`, `ag/orchestrator-<slug>`, `fix/bushi-NN-<slug>`, `tests/*` ; toujours depuis `main`.
- Numérotation globale continue ; prochain numéro libre côté Antigravity : `0048`.
- Budget bloc 1 : enveloppe COSE_Sign1 ≤ 2 048 o, charge utile ≤ 1 900 o.
- Type d'enveloppe : paramètre `typ`, étiquette 16, en-tête protégé (`application/aeternitrak-profile+cbor`, `application/aeternitrak-batch-claim+cbor`).
- Porte de Fer : `evaluate(claim, policy)` ; aucune dérogation en dur.
- Une faute de décodage remonte toujours avec son code `ERR_CBOR_*` ; les registres `ERR_PROFILE_*` et `ERR_COSE_*` ne la doublent pas.
- Validité d'une clé : fenêtre comparée à la date d'émission de la charge utile vérifiée, jamais à la date de lecture ; statuts `ACTIVE`, `RETIRED`, `REVOKED`.
- Lecture d'une carte : `cose-open` (DEC-AET-07 option B) ; seul un émetteur inconnu rend le contenu sous réserve ; un contenu `UNVERIFIED` n'a aucune valeur de preuve.
- Une clé d'en-tête COSE est un entier ; aucune conversion depuis un texte.

## En attente chez Antigravity
1. `fix/bushi-12-reasons-v14` (0046) : P15 à P17 ; attendu 202/202 anti-prion, 547 PASS au total.
2. `ag/bushi-02-batch-certificate-spec` (0047) : spécification du certificat de lot, sans code.
3. Acquittement 0045.

## En attente de l'arbitrage de Kudoro
- `DEC-AET-01` (codec du bloc 3), `DEC-AET-02`, `DEC-AET-03`.
- Référence de l'autorisation administrative pour DEC-AET-05 avant toute politique réelle.

## Prochaines actions Claude AI
- Vecteurs de validité temporelle des clés (K2) : promis depuis le cycle 0007, pas encore livrés.
- Rejouer les 220 000 revendications sur `fix/bushi-12-reasons-v14`.
- Auditer la spécification du certificat de lot, puis écrire la suite de composition (enveloppe + profil, enveloppe + certificat).
