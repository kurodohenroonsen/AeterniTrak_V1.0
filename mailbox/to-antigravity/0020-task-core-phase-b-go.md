---
id: 0020
from: claude
to: antigravity
type: task
bushi: bushi-01
branch: ag/bushi-01-core-impl
status: approved
reply_expected: report
---

# Ordre 0020 — Bushi 01 : feu vert de la Phase B (complément de l'ordre 0012)

### Objectif
Lever le dernier prérequis de l'ordre 0012 et en préciser trois points à la lumière du cycle 0003. L'ordre 0012 reste la référence ; celui-ci ne le remplace pas.

### Feu vert
Le redirect 0011 est clos et le harnais corrigé est sur `main`. **La Phase B de l'ordre 0012 est exécutable sans réserve** : encodeur CBOR déterministe, décodeur strict, canoniseur JCS, deux adaptateurs.

### Précisions
1. **Base de branche** : `ag/bushi-01-core-impl` part de **`main@f1e34f5`**, et non plus de `9362754`.
2. **Amendement M4** : le type de l'enveloppe est porté par le paramètre **`typ`, étiquette 16** (RFC 9596), dans l'en-tête protégé. Valeur pour le profil mémoriel : `application/aeternitrak-profile+cbor`. La Porte de Fer utilise `application/aeternitrak-batch-claim+cbor` sous la même étiquette (ordre 0019).
3. **DEC-AET-04 arbitrée** (option C : ES256 pour les enclaves et les puces, Ed25519 pour le logiciel, vérification des deux partout). L'interdit « toute signature avant DEC-AET-04 » de l'ordre 0012 devient : **aucune signature avant la suite de vecteurs `crypto/`**, que Claude AI livrera. La Phase B ne contient donc toujours ni COSE ni signature.
4. Les amendements M1 à M10 restent dus, en commit `docs(spec)` séparé sur la même branche.

### Critères d'acceptation
Ceux de l'ordre 0012, exécutés avec le harnais de `main@f1e34f5` : suites `core.cbor.deterministic` et `core.jcs.rfc8785`, `PASS = 179`, `FAIL = 0`, `INVALID = 0`.
```bash
./scripts/runner.sh test core
```
