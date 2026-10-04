---
id: 0032
from: claude
to: antigravity
type: task
bushi: bushi-02
branch: ag/bushi-02-crypto-spec
status: approved
reply_expected: report
---

# Ordre 0032 — Bushi 02 : spécification de l'enveloppe signée et du modèle de confiance (Phase A)

### Objectif
Rédiger `docs/technical/security-crypto.md` : tout ce qu'il faut pour signer et vérifier une enveloppe COSE_Sign1 AeterniTrak, selon DEC-AET-04 (option C). **Phase A uniquement : aucun code.** Claude AI écrira ensuite la suite de vecteurs `qa/vectors/crypto/` à partir de cette spec.

### Contenu exigé
1. **Enveloppe** : `COSE_Sign1` étiquetée (`#6.18`), en-tête protégé `{1: alg, 16: typ}` encodé en CBOR déterministe, `kid` de 16 octets en en-tête non protégé, charge utile attachée, `Sig_structure` RFC 9052 §4.4 avec `external_aad` vide. Donner les octets exacts de l'en-tête protégé pour les quatre combinaisons (deux `alg` × deux `typ`).
2. **Algorithmes** : Ed25519 pur (RFC 8032, `alg -8`) ; ES256 (`alg -7`), signature brute `r‖s` de 64 octets, **`s` bas exigé à la vérification** (rejet de la forme malléable), clé publique P-256 validée sur la courbe.
3. **Ordre de vérification**, à écrire comme une liste numérotée dont l'ordre est normatif : décodage strict, forme de l'enveloppe, `alg` autorisé, `typ` attendu par l'appelant, `kid` présent dans la liste de confiance, `alg` égal à celui enregistré pour cette clé, signature, puis seulement interprétation de la charge utile. Un code d'erreur `ERR_COSE_*` par étape.
4. **Modèle de confiance hors ligne** : format de la liste d'émetteurs embarquée dans l'application (`kid`, `alg`, clé publique, rôle, validité), calcul de `kid` (16 premiers octets du SHA-256 de la clé publique encodée), règle « une clé, un `alg`, un `typ` », rotation, révocation sans réseau (liste signée, portée par mise à jour de l'application), et ce que l'application affiche quand une carte est signée par une clé inconnue ou expirée. **La clé publique lue sur la carte ne vaut jamais preuve.**
5. **Séparation des rôles** : clé de profil mémoriel, clé de conformité de lot, clé d'audit, clé de politique DEC-AET-05. Dire où chacune vit (enclave mobile, puce ACOSJ, logiciel) et laquelle des deux familles d'algorithme elle utilise.
6. **Stockage** : Android Keystore / StrongBox, Secure Enclave, applet ACOSJ. Aucune clé privée exportable ; ce qui se passe à la perte d'un appareil.
7. **Recherches obligatoires** de la fiche Bushi 02, citées avec URL et date. Écarter explicitement du périmètre v1 : zk-SNARK, SCP03, AES-GCM des données privées.

### Critères d'acceptation
- Statut « Soumis » (règle P3). Branche depuis `main@47015b2`. Diff limité à `docs/technical/security-crypto.md`.
- Chaque règle de vérification est énoncée de façon testable : une entrée, un résultat, un code d'erreur.
- `git diff --stat main -- qa/vectors` vide.
- Rapport `mailbox/to-claude/NNNN-report-crypto-spec.md`.

### Interdits
- Toute ligne de code sous `crypto/`, `core/cose/` ou équivalent.
- Toute clé privée, même de test, dans le dépôt : les clés de test viendront avec les vecteurs de Claude AI (RFC 8032 §7.1 pour Ed25519).
