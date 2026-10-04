# État Claude AI (Master Verifier) — AeterniTrak V1.0

- **Rôle** : Architecte Suprême, rédaction des vecteurs formels, validation sur pièces, arbitrage et fusion sur `main`.
- **Dernière révision** : 2026-10-04 — cycle de revue 0009.
- **Branche active** : `agent-mailbox` (messages) ; `main` à **`18f33c9`**.
- **Fichier rédigé par Claude AI uniquement.**

## Cycle 0009 (2026-10-04)
| Message | Verdict | Réponse |
|---|---|---|
| 0048 acquittement du cycle 0008 (`f257f14`) | validé, fusionné (`d450058`) | ordre 0052 |
| 0049 listes de motifs v1.4 (`8e30ea5`) | validé, fusionné (`7817e1a`) ; 547 PASS reproduit, 7/7 mutations, 220 000 revendications sans écart | ordres 0052, 0056 |
| 0050 spécification du certificat de lot (`4048e61`) | non fusionné, dix amendements (codes en doublon, politique fournie par le présentateur, clé 6, évaluer ce qui est haché) | redirect 0053 |
| 0051 décisions 01, 02, 03, 05 (`9cdfae9`) | rejeté : références de droit fausses, DEC-AET-03 n'est pas un arbitrage ; DEC-AET-01 et 02 inscrites par moi | redirect 0054 |
| portail des cas d'usage (`6716f0e`, sans rapport) | rejeté : Google Fonts et script distant, références fausses, 14 textes et non 24 | redirect 0055 |

- Livré sur `main` via `tests/0052-key-validity-and-insect-nature` : suite `crypto.cose.rules-v12` (40 cas, K2, `README.md` §4.11), suite `antiprion.feedban.rules-v15` (10 cas, P18, §4.12), entrées DEC-AET-01 et DEC-AET-02.
- **Banc sur `main@18f33c9` : 14 suites, 597 vecteurs, 563 PASS, 34 FAIL, 0 RED, 0 INVALID.** 28 FAIL K2 (fonction non écrite), 6 FAIL P18.
- **Trois FAIL sont des verdicts** (`PRION-HARD-092`, `093`, `096`) : `main` autorise un insecte déclaré comme source en équarrissage direct, sans contrôle de son substrat. Ma référence l'autorisait aussi jusqu'à ce cycle.
- Sur `main` : `core/cbor`, `core/jcs`, `core/profile`, `core/cose`, `validators/antiprion`.

## Décisions de Kudoro actées (2026-10-04)
- **DEC-AET-01** : cartes ACOSJ 92 Ko uniquement ; le contenu de la carte reste à prouver par `STORAGE-001`.
- **DEC-AET-02** : connecteurs API vers les guichets officiels, CERISE en premier ; existence des API à établir.
- **DEC-AET-04** : option C, COSE_Sign1 agile.
- **DEC-AET-05** : dérogation de mémoire forestière privée, animaux de compagnie catégorie 1 LFA négatifs ; humains exclus.
- **DEC-AET-06** : correction du vecteur `CBOR-REJ-006`.
- **DEC-AET-07** : option B, bandeau pour un émetteur inconnu, blocage pour une clé révoquée ou une signature fausse.
- **Prénom « Guy »** : maintenu, en hommage.

## Limites connues de ce qui est certifié
- Le vert prouve la conformité aux vecteurs et à mes références, pas au droit. Les règles P5, P6 et P18 reposent sur des textes que je n'ai pas relus sur EUR-Lex (P18 : vérification demandée au Bushi 12).
- Ma référence de la Porte de Fer s'est trompée deux fois de suite sur un point que le fuzzing du même corpus ne montrait pas. Un corpus neuf par cycle est nécessaire ; zéro écart sur un corpus déjà joué ne prouve rien de plus.
- Les 40 attentes K2 viennent de ma seule référence ; aucune seconde implémentation ne les a recalculées.
- La date d'émission est déclarée par le signataire : la fenêtre de validité ne protège pas contre une clé volée qui antidate.
- Mes contrôles de droit du cycle 0009 (loi du 30 juillet 2018, article 19 du règlement 1069/2009, article 2003 de l'ancien Code civil) reposent sur une lecture rapide de sources en ligne. Ils suffisent à refuser une entrée, pas à en écrire une.
- Option B : une carte d'émetteur inconnu s'affiche sans que sa signature ait pu être contrôlée.
- Non couvert par des vecteurs : signatures Ed25519 forgées avec des points d'ordre faible, composition profil + enveloppe et certificat de lot + enveloppe.

## Conventions arrêtées
- Fichiers de gouvernance : `main` fait foi ; `agent-mailbox` ne porte que `mailbox/`.
- Branches : `ag/bushi-NN-<slug>`, `ag/orchestrator-<slug>`, `fix/bushi-NN-<slug>`, `tests/*` ; toujours depuis `main`.
- Numérotation globale continue ; prochain numéro libre côté Antigravity : `0058`.
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

## En attente chez Antigravity
1. `fix/bushi-12-insect-source-p18` (0056) : P18, `RULES_VERSION` ; attendu 212/212 anti-prion. **Prioritaire : verdict en jeu.**
2. `ag/bushi-02-key-validity` (0057) : K2 ; attendu 144/144 crypto.
3. `ag/bushi-02-batch-certificate-spec` (0053) : document v1.1.0, dix amendements.
4. Études de droit et inventaire des API (0054) ; portail autonome (0055).
5. Acquittement 0052.

## En attente de l'arbitrage de Kudoro
- `DEC-AET-03` : après l'étude du Bushi 13.
- Référence de l'autorisation administrative pour DEC-AET-05 : toujours ouverte ; l'article 19 du règlement 1069/2009 ne couvre que l'enfouissement.
- P18 : je l'ai arrêtée seul parce qu'elle ferme une route ; Kudoro peut la renverser.

## Prochaines actions Claude AI
- Rejouer les deux corpus (370 000) plus un corpus neuf sur `fix/bushi-12-insect-source-p18`.
- Fuzzing différentiel de K2 sur `ag/bushi-02-key-validity`.
- Suite `crypto/batch-certificate.vectors.json` sur la spécification amendée.
- Ajouter à `PROTOCOL.md` la règle sur le registre des décisions.
