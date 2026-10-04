# État Claude AI (Master Verifier) — AeterniTrak V1.0

- **Rôle** : Architecte Suprême, rédaction des vecteurs formels, validation sur pièces, arbitrage et fusion sur `main`.
- **Dernière révision** : 2026-10-04 — cycle de revue 0007.
- **Branche active** : `agent-mailbox` (messages) ; `main` certifié à **`eeba7bd`**.
- **Fichier rédigé par Claude AI uniquement.**

## Cycle 0007 (2026-10-04)
| Message | Verdict | Réponse |
|---|---|---|
| 0038 décision DEC-AET-07, option B (`ee71ef2`) | actée, fusionnée | ordre 0041 |
| 0039 validateur du profil (`2fa7d95`) | validé, fusionné ; 60 010 profils fuzzés sans écart de verdict ni de code | ordre 0041 |
| 0040 moteur COSE_Sign1 (`eae1ffb`) | 84/84 reproduit ; **non fusionné** : clé d'en-tête texte `"4"` acceptée (36 enveloppes non conformes validées sur 9 000), import `node:crypto`, constante K1 non corrigée dans la spec | redirect 0042 |

- Livré sur `main` via `tests/0041-cose-rules-v11` : suite `crypto.cose.rules-v11` (20 cas : typage des clés d'en-tête, opération `cose-open`), `README.md` §4.9.
- **Banc sur `main@eeba7bd` : 528 vecteurs, 424 PASS, 104 RED, 0 INVALID.**
- Sur `main` : `core/cbor`, `core/jcs`, `core/profile`, `validators/antiprion`. Pas encore `core/cose`.

## Décisions de Kudoro actées (2026-10-04)
- **DEC-AET-04** : option C, COSE_Sign1 agile.
- **DEC-AET-05** : dérogation de mémoire forestière privée, animaux de compagnie catégorie 1 LFA négatifs ; humains exclus.
- **DEC-AET-06** : correction du vecteur `CBOR-REJ-006`.
- **DEC-AET-07** : option B, bandeau pour un émetteur inconnu, blocage pour une clé révoquée ou une signature fausse.
- **Prénom « Guy »** : maintenu, en hommage.

## Limites connues de ce qui est certifié
- Le vert prouve la conformité aux vecteurs et à mes références, pas au droit : les règles P5 et P6 de la Porte de Fer reposent sur la vérification EUR-Lex du Bushi 12, que je n'ai pas refaite.
- Environ 7 % des revendications bloquées le sont avec des listes de motifs différentes entre le code et ma référence. À fixer par vecteurs ; toujours pas fait.
- Les attentes du profil que j'ai ajoutées viennent de ma seule référence ; le code livré s'y accorde sur 60 010 profils, ce qui confirme la cohérence, pas la justesse du CDDL.
- Option B : une carte d'émetteur inconnu s'affiche sans que sa signature ait pu être contrôlée. Une carte forgée avec un `kid` inventé s'affiche donc aussi, sous bandeau.
- Non couvert par des vecteurs : validité temporelle des clés, signatures Ed25519 forgées avec des points d'ordre faible, composition profil + enveloppe et certificat de lot + enveloppe.

## Conventions arrêtées
- Fichiers de gouvernance : `main` fait foi ; `agent-mailbox` ne porte que `mailbox/`.
- Branches : `ag/bushi-NN-<slug>`, `ag/orchestrator-<slug>`, `fix/bushi-NN-<slug>`, `tests/*` ; toujours depuis `main`.
- Numérotation globale continue ; prochain numéro libre côté Antigravity : `0043`.
- Budget bloc 1 : enveloppe COSE_Sign1 ≤ 2 048 o, charge utile ≤ 1 900 o.
- Type d'enveloppe : paramètre `typ`, étiquette 16, en-tête protégé (`application/aeternitrak-profile+cbor`, `application/aeternitrak-batch-claim+cbor`).
- Porte de Fer : `evaluate(claim, policy)` ; aucune dérogation en dur.
- Une faute de décodage remonte toujours avec son code `ERR_CBOR_*` ; les registres `ERR_PROFILE_*` et `ERR_COSE_*` ne la doublent pas.
- Validité d'une clé : fenêtre comparée à la date d'émission de la charge utile vérifiée, jamais à la date de lecture ; statuts `ACTIVE`, `RETIRED`, `REVOKED`.
- Lecture d'une carte : `cose-open` (DEC-AET-07 option B) ; seul un émetteur inconnu rend le contenu sous réserve ; un contenu `UNVERIFIED` n'a aucune valeur de preuve.
- Une clé d'en-tête COSE est un entier ; aucune conversion depuis un texte.

## En attente chez Antigravity
1. `fix/bushi-02-crypto-v11` (0042) : D1 à D3, `coseOpen`, sept mutations ; attendu 104/104 crypto, 528 PASS au total.
2. Acquittement 0041.

## En attente de l'arbitrage de Kudoro
- `DEC-AET-01` (codec du bloc 3), `DEC-AET-02`, `DEC-AET-03`.
- Référence de l'autorisation administrative pour DEC-AET-05 avant toute politique réelle.

## Prochaines actions Claude AI
- Vecteurs de validité temporelle des clés (K2).
- Suite de composition : enveloppe + profil, enveloppe + certificat de lot.
- Vecteurs fixant les listes de motifs divergentes de la Porte de Fer.
