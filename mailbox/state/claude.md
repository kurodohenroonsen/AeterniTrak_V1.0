# État Claude AI (Master Verifier) — AeterniTrak V1.0

- **Rôle** : Architecte Suprême, rédaction des vecteurs formels, validation sur pièces, arbitrage et fusion sur `main`.
- **Dernière révision** : 2026-10-04 — cycle de revue 0006.
- **Branche active** : `agent-mailbox` (messages) ; `main` certifié à **`d6e5f4d`**.
- **Fichier rédigé par Claude AI uniquement.**

## Cycle 0006 (2026-10-04)
| Rapport | Verdict | Réponse |
|---|---|---|
| 0033 nettoyage (`5f56788`) | validé, fusionné ; ordre 0030 clos | ordre 0036 |
| 0034 vecteurs `draft` du profil (`abd8b52`) | validé, fusionné ; 22 cas sur 24 confirmés à l'identique par ma référence ; suite approuvée en 1.1.0 (61 cas) | ordre 0036 |
| 0035 spec crypto (`15ef7d3`) | approuvée avec sept amendements (K1–K7), fusionnée | ordre 0037 |

- Livré sur `main` via `tests/0036-profile-approval-and-crypto-vectors` : suite `core.profile` approuvée, trois suites `crypto.*` (84 cas), `README.md` §4.7 et §4.8, `DEC-AET-07` soumise.
- **Banc sur `main@d6e5f4d` : 508 vecteurs, 363 PASS, 145 RED, 0 INVALID.**
- Vecteurs crypto : clés publiées des RFC 8032 §7.1 et RFC 6979 A.2.5 ; valeurs produites par `cryptography` et `ecdsa`, recontrôlées par WebCrypto de Node (35 contrôles, aucun écart).

## Décisions de Kudoro actées (2026-10-04)
- **DEC-AET-04** : option C, COSE_Sign1 agile.
- **DEC-AET-05** : dérogation de mémoire forestière privée, animaux de compagnie catégorie 1 LFA négatifs ; humains exclus.
- **DEC-AET-06** : correction du vecteur `CBOR-REJ-006`.
- **Prénom « Guy »** : maintenu, en hommage.

## Limites connues de ce qui est certifié
- Le vert prouve la conformité aux vecteurs et à mes références, pas au droit : les règles P5 et P6 de la Porte de Fer reposent sur la vérification EUR-Lex du Bushi 12, que je n'ai pas refaite.
- Environ 7 % des revendications bloquées le sont avec des listes de motifs différentes entre le code et ma référence. À fixer par vecteurs ; pas encore fait.
- Les 39 attentes du profil que j'ai ajoutées ou corrigées viennent de ma seule référence, sans second avis.
- Les vecteurs crypto ne couvrent ni la validité temporelle des clés, ni les signatures Ed25519 forgées avec des points d'ordre faible.
- Rien n'est encore signé de bout en bout : profil, enveloppe et Porte de Fer ne sont pas composés.

## Conventions arrêtées
- Fichiers de gouvernance : `main` fait foi ; `agent-mailbox` ne porte que `mailbox/`.
- Branches : `ag/bushi-NN-<slug>`, `ag/orchestrator-<slug>`, `fix/bushi-NN-<slug>`, `tests/*` ; toujours depuis `main`.
- Numérotation globale continue ; prochain numéro libre côté Antigravity : `0038`.
- Budget bloc 1 : enveloppe COSE_Sign1 ≤ 2 048 o, charge utile ≤ 1 900 o.
- Type d'enveloppe : paramètre `typ`, étiquette 16, en-tête protégé (`application/aeternitrak-profile+cbor`, `application/aeternitrak-batch-claim+cbor`).
- Porte de Fer : `evaluate(claim, policy)` ; aucune dérogation en dur.
- Une faute de décodage remonte toujours avec son code `ERR_CBOR_*` ; les registres `ERR_PROFILE_*` et `ERR_COSE_*` ne la doublent pas.
- Validité d'une clé : fenêtre comparée à la date d'émission de la charge utile vérifiée, jamais à la date de lecture ; statuts `ACTIVE`, `RETIRED`, `REVOKED`.

## En attente chez Antigravity
1. `ag/bushi-01-profile-validator` (0036) : validateur du profil, 61 vecteurs, script de mutations.
2. `ag/bushi-02-crypto-impl` (0037) : amendements K1–K7 puis `core/cose`, 84 vecteurs, script de mutations.

## En attente de l'arbitrage de Kudoro
- **`DEC-AET-07`** : que voit une famille quand la carte ne peut pas être vérifiée (blocage, bandeau, ou affichage dans tous les cas).
- `DEC-AET-01` (codec du bloc 3), `DEC-AET-02`, `DEC-AET-03`.
- Référence de l'autorisation administrative pour DEC-AET-05 avant toute politique réelle.

## Prochaines actions Claude AI
- Vecteurs de validité temporelle des clés (après l'amendement K2).
- Vecteurs fixant les listes de motifs divergentes de la Porte de Fer.
- Suite de composition : enveloppe signée + profil, enveloppe signée + certificat de lot.
