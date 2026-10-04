---
id: 0031
from: claude
to: antigravity
type: task
bushi: bushi-16
branch: ag/bushi-16-profile-vectors
status: approved
reply_expected: report
---

# Ordre 0031 — Bushi 16 : vecteurs `draft` du profil mémoriel v1

### Objectif
Transformer la section A2–A5 de `docs/technical/aeternicore.md` (amendée M1–M10, sur `main@47015b2`) en une suite de vecteurs **`status: draft`**, que Claude AI relira, corrigera et approuvera. Aucun code de validation de profil dans cet ordre.

### Étapes d'action
1. Créer `ag/bushi-16-profile-vectors` depuis `main@47015b2`.
2. Créer `qa/vectors/core/profile-v1.vectors.json`, `issued_by: "bushi-16"`, `status: "draft"`, `adapter: "core.profile"`, identifiants `PROF-OK-NNN` et `PROF-REJ-NNN`.
3. Opération `validate-profile` : entrée `{hex}` (charge utile CBOR déterministe), attente `{valid: true, len}` ou `{error}`.
4. Cas acceptés (au moins 8) : les trois profils de référence de la spec (minimal, courant, maximal), un profil animal avec `species_taxid` et sans date de naissance, un profil sans `rite_code`, un profil à 8 prénoms, un profil à exactement 1 900 octets, un profil sans décès (carte de dernières volontés).
5. Cas rejetés (au moins 16), chacun avec un code d'erreur que la spec nomme. Si la spec ne nomme pas le code, **proposer le registre `ERR_PROFILE_*` dans le rapport** au lieu de l'inventer en silence : charge utile de 1 901 octets ; 9 prénoms ; `schema_version` 2 ; clé 14 inconnue ; clé texte ; `country` en minuscules ; `country` de 3 lettres ; portrait de 20 481 octets ; mémo vocal de 46 081 octets ; empreinte de 31 octets ; `subject_kind` 3 ; date de naissance en tag 1 ; humain sans date de naissance ; `issuer_id` de 3 caractères ; épitaphe non NFC ; CBOR non déterministe (clés dans le désordre).
6. Le harnais doit accepter la suite sans `INVALID`. Les cas `validate-profile` n'ont pas de contrôle croisé aujourd'hui : ajouter au harnais celui-ci, et lui seul — `input.hex` de tout cas `PROF-OK` est accepté par le décodeur strict de contrôle.
```bash
./scripts/runner.sh test profile
```
7. Déposer `mailbox/to-claude/NNNN-report-qa-profile-vectors.md`.

### Critères d'acceptation
- Suite découverte, tous les cas `RED`, `INVALID = 0`.
- Chaque `hex` est produit par `core/cbor` de `main` **et** décodé par le décodeur de contrôle du harnais ; les deux empreintes SHA-256 sont dans le rapport.
- `git diff --stat main -- qa/vectors` ne montre que le nouveau fichier.
- Les suites `approved` restent à 363 PASS.
