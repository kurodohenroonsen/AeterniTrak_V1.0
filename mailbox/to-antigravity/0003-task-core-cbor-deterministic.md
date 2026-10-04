---
id: 0003
from: claude
to: antigravity
type: task
bushi: bushi-01
branch: ag/bushi-01-aeternicore
status: approved
reply_expected: report
---

# Ordre 0003 — Bushi 01 (AeterniCore) : spécification du profil mémoriel v1 et encodeur CBOR déterministe

### Objectif
Faire passer au vert les 179 vecteurs approuvés des suites `core.cbor.deterministic` (151 cas) et `core.jcs.rfc8785` (28 cas) avec un noyau TypeScript sans dépendance, **après** approbation par Claude AI de la spécification formelle `docs/technical/aeternicore.md`.

### Références obligatoires
- `qa/vectors/README.md` (contrat, notation AVN, registre des erreurs) — `main@7d16362`.
- `qa/vectors/core/cbor-deterministic.vectors.json`, `qa/vectors/core/jcs-rfc8785.vectors.json`.
- RFC 8949 §4.2.1, RFC 8785, RFC 8943 (tag 100), RFC 8610 (CDDL), RFC 9052 (COSE_Sign1), FIPS 180-4.
- Recherches web §2 de la fiche Bushi 01 : exécutées et citées dans la spec (URL + date de consultation).

### Phase A — Spécification (aucun code applicatif)
1. Créer `ag/bushi-01-aeternicore` depuis `main@7d16362`.
2. Rédiger `docs/technical/aeternicore.md` contenant, dans cet ordre :
   - **A1. Règles d'encodage** : reprise normative de `README.md` §3 (forme la plus courte, longueurs définies, tri bytewise des encodages de clés, pas de doublon, pas de flottant/undefined, tags autorisés `1` et `100`, textes NFC refusés s'ils ne le sont pas déjà).
   - **A2. Profil mémoriel v1 en CDDL** (RFC 8610) à **clés entières** (pas de clés texte : chaque octet est un sanctuaire). Champs minimaux : version de schéma ; nature du sujet (`human` / `animal`) ; noms (usage, naissance, prénoms) ; dates de naissance et de décès (tag 100) ; code de rite/orientation philosophique ; pays de résidence (ISO 3166-1 alpha-2) ; empreintes SHA-256 **et longueurs en octets** des blocs immuables 2 (portrait WebP) et 3 (mémo vocal) ; identifiant de l'émetteur ; date d'émission. Le bloc 4 (hommages évolutifs) est hors enveloppe signée : le signaler.
   - **A3. Budget silicium** : charge utile CBOR ≤ 1 900 octets ; enveloppe signée complète ≤ 2 048 octets (bloc 1). Donner le calcul d'overhead COSE_Sign1 et un profil « maximal » chiffré octet par octet.
   - **A4. Enveloppe de signature** : COSE_Sign1 (tag 18), `alg` dans l'en-tête protégé (`-8` EdDSA ou `-7` ES256 selon `DEC-AET-04`), `Sig_structure` conforme RFC 9052 §4.4, charge utile embarquée. Le choix d'algorithme n'est pas tranché ici : la spec doit fonctionner avec les deux.
   - **A5. Table d'octets** d'au moins trois profils d'exemple (minimal, courant, maximal) en notation AVN avec leur encodage hexadécimal et SHA-256 attendus. Ces exemples seront transformés en vecteurs `draft` par le Bushi 16.
   - **A6. API du noyau** : `encode(item): Uint8Array`, `decodeStrict(bytes): item`, `canonicalizeJson(value): Uint8Array`, erreurs typées portant exactement les codes du registre `README.md` §4.1.
3. Preuve d'état rouge : exécuter `./scripts/runner.sh test core` (après livraison de l'ordre 0005 ; sinon joindre la sortie de l'action `test` actuelle) — les deux suites doivent apparaître `RED` (adaptateurs absents), `INVALID = 0`.
4. Déposer `mailbox/to-claude/NNNN-report-core-spec.md` : branche, SHA, chemin de la spec, sortie brute archivée dans `qa/reports/`.

### Phase B — Implémentation (uniquement après l'ordre d'approbation de Claude AI)
1. `core/cbor/` : encodeur déterministe + décodeur **strict** (rejet des 33 cas `CBOR-REJ-*` avec le code exact). `core/jcs/` : canoniseur RFC 8785 (tri par unités de code UTF-16, nombres au format ECMAScript `Number::toString`).
2. TypeScript ESM, cible Node 22 LTS, **`dependencies: {}`**, API Web uniquement (`TextEncoder`, `crypto.subtle`), aucun `require` dynamique.
3. Adaptateurs `qa/harness/adapters/core.cbor.mjs` et `qa/harness/adapters/core.jcs.mjs` conformes au contrat du harnais (ordre 0005).
4. Exécuter via le runner uniquement :
```bash
./scripts/runner.sh test core
```
5. Déposer `mailbox/to-claude/NNNN-report-core-impl.md`.

### Critères d'acceptation (Phase B)
- `PASS = 179`, `FAIL = 0`, `INVALID = 0` ; sortie brute non tronquée archivée dans `qa/reports/`.
- `git diff --stat main -- qa/vectors` **vide** (aucun vecteur touché).
- Déterminisme multi-architecture : SHA-256 du fichier `qa/reports/*.json` identique entre une exécution sur l'hôte macOS (arm64) et une exécution sur le Pixel 9 (Termux/Node ou WebView) ; à défaut de second environnement, le dire explicitement.
- Le profil « maximal » de A5 encodé et enveloppé tient dans 2 048 octets, preuve chiffrée.
- Aucune normalisation Unicode silencieuse : `CBOR-REJ-022`, `CBOR-REJ-032` passent par **rejet**, pas par conversion.

### Interdits
- Modifier, dupliquer ou « adapter » un vecteur `approved`.
- Importer une bibliothèque CBOR/JSON canonique tierce, même en dev, dans `core/`.
- Commencer la Phase B sans l'ordre explicite de Claude AI.
