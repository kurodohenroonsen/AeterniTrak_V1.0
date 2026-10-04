# État Claude AI (Master Verifier) — AeterniTrak V1.0

- **Rôle** : Architecte Suprême, rédaction des vecteurs formels, validation sur pièces, arbitrage et fusion sur `main`.
- **Dernière révision** : 2026-10-04 — cycle de revue 0001.
- **Branche active** : `agent-mailbox` (messages) ; `main` certifié à **`7d16362`**.
- **Fichier rédigé par Claude AI uniquement** (ordre 0002, C8).

## Cycle 0001 (2026-10-04)
- Rapport 0001 (échafaudage, `edd5f66`) : **validé** avec neuf corrections de cohérence (ordre 0002).
- Livré sur `main` via `tests/0002-vector-contract` (fusion `7d16362`) : `qa/vectors/README.md` (contrat), schéma de suite, 246 vecteurs `approved` :
  - `core.cbor.deterministic` : 151 cas (RFC 8949 §4.2.1 + profil AeterniCore v1), encodeur de référence indépendant + contrôle croisé `cbor2`.
  - `core.jcs.rfc8785` : 28 cas (tri UTF-16, nombres ECMAScript, échappements).
  - `antiprion.feedban.matrix` : 67 cas (17 AUTHORISED / 36 BLOCKED / 14 DEFAULT_DENY) + `taxonomy-snapshot.json` (26 taxons NCBI vérifiés via UniProt le 2026-10-04).
- Ordres émis : `0002` (orchestrateur, corrections C1–C9), `0003` (Bushi 01, spec + CBOR/JCS), `0004` (Bushi 12, spec + Porte de Fer), `0005` (Bushi 16, harnais `QA-001`, **prérequis** de 0003/0004).

## Conventions arrêtées
- Fichiers de gouvernance font foi sur `main` seulement ; `agent-mailbox` ne porte que `mailbox/`.
- Branches : `ag/bushi-NN-<slug>`, `ag/orchestrator-<slug>`, `fix/bushi-NN-<slug>`, `tests/*` (Claude).
- Messages : `NNNN-<type>-<bushi>-<slug>.md`, numérotation globale continue (prochain numéro libre côté Antigravity : `0006`).
- Budget bloc 1 : enveloppe COSE_Sign1 ≤ 2 048 o, charge utile CBOR ≤ 1 900 o.
- Cycle en deux phases pour tout chantier : Phase A spec + vecteurs rouges → approbation Claude → Phase B implémentation.

## En attente chez Antigravity
- Rapport `scaffold-fixes` (0002), rapport `qa-harness` (0005) en premier, puis rapports de spec `core` (0003) et `antiprion` (0004).

## Questions soumises à l'arbitrage de Kudoro (à consigner dans `DECISIONS-KUDORO.md` §2)
- **DEC-AET-04 — Algorithme de signature** : Ed25519 (RFC 8032, COSE `-8`) ou ES256 (P-256, COSE `-7`) ? Contraintes matérielles : Secure Enclave iOS = P-256 uniquement ; Android KeyStore/StrongBox = P-256 garanti, Ed25519 selon KeyMint ; ACOSJ JavaCard = ECDSA P-256. Proposition Claude AI : enveloppe COSE_Sign1 avec `alg` explicite ; Ed25519 pour les signatures d'émission logicielles (Studio, filière, validateur anti-prion), ES256 pour les clés ancrées dans les enclaves mobiles et les puces ; vérification des deux partout.
- **DEC-AET-05 — Dérogations** : le validateur v1 refuse par défaut la mémoire forestière (animaux de compagnie LFA-négatifs, restes humains) avec `DEROGATION_REQUIRED`. Faut-il un objet de politique signé par Kudoro (base légale citée, périmètre, durée) débloquant ces routes, et sur quelle base (ordonnance bruxelloise art. 25, avant-projet de loi de juillet 2026) ?

## Prochaines actions Claude AI
- À réception des rapports : vérifier sur pièces (SHA, sorties brutes, `git diff --stat main -- qa/vectors` vide), approuver les specs ou rediriger, fusionner sur `main`.
- Préparer les vecteurs `crypto/` (RFC 8032, COSE_Sign1) dès l'arbitrage `DEC-AET-04`.
