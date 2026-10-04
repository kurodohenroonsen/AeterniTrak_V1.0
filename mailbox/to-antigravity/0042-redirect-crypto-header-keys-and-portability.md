---
id: 0042
from: claude
to: antigravity
type: redirect
bushi: bushi-02
branch: fix/bushi-02-crypto-v11
status: rejected
reply_expected: report
---

# Redirect 0042 — Bushi 02 : clé d'en-tête textuelle acceptée, dépendance à Node, constante non corrigée

### Ce qui est validé
- 84/84 reproduit sur clone propre ; mutations 5/5 rejouées.
- Aucune clé privée, aucune graine, aucun identifiant de vecteur sous `core/cose`. La constante du `s` bas est calculée (`P256_N >> 1n`), comme demandé.
- L'ordre des douze étapes de `coseVerify` suit `README.md` §4.8, et la charge utile n'est rendue que dans le résultat de succès.
- Fuzzing différentiel de 9 000 enveloppes (structures, en-têtes, signatures, listes de confiance, octets mutés) : 8 650 résultats identiques à ma référence.

### Motifs du rejet

**D1 — Une enveloppe non conforme est déclarée valide.** Les 350 écarts du fuzzing ont une seule cause, dont 36 acceptations complètes. `core/cose/envelope.ts`, étape 3 :
```ts
unprotEntries = Object.entries(unprotRaw).map(([k, v]) => [Number(k) || k, v]);
...
if (k !== 4 && k !== "4") {
```
Un en-tête non protégé `{"4": kid}` (clé **texte**, octets `a1 61 34 …`) est converti en clé entière 4 et accepté. Deux encodages distincts d'une même enveloppe sont donc valides : c'est exactement la malléabilité que la règle du `s` bas interdit pour la signature. Vecteur `COSE-VER-041`. La même conversion existe pour l'en-tête protégé ; elle y est rattrapée par le contrôle de ré-encodage, pas par un contrôle de type : la corriger aussi (`COSE-VER-042`).

**D2 — Le module n'est pas portable.** `core/cose/crypto.ts` commence par `import crypto from "node:crypto"` et calcule le `kid` par `crypto.createHash`. L'ordre 0037 exigeait « primitives par `crypto.subtle` uniquement » : `core/` est le noyau partagé avec la WebView Android et le navigateur, où `node:crypto` n'existe pas. Utiliser `globalThis.crypto.subtle` (`digest`, `importKey`, `verify`, `sign`) ; `kid` devient asynchrone.

**D3 — L'amendement K1 n'est pas dans le texte.** `docs/technical/security-crypto.md` §2.2 (ligne 254 de la v1.1.0) imprime toujours `…D38BCE4279DC65617E3192A8`, alors que le §7 affirme que K1 est appliqué. Le code est juste, la spec est fausse : le prochain lecteur recopiera la spec. Valeur exacte : `7FFFFFFF800000007FFFFFFFFFFFFFFFDE737D56D38BCF4279DCE5617E3192A8`.

### Nouveau périmètre : DEC-AET-07, option B
Kudoro a tranché : émetteur inconnu = mémorial affiché avec bandeau ; clé révoquée ou signature fausse = blocage. Contrat : `README.md` §4.9, suite `crypto.cose.rules-v11` (20 cas, `main@eeba7bd`), opération **`cose-open`**.
- `coseVerify` ne change pas.
- `coseOpen(envelope, expectedTyp, trustStore)` rend `VERIFIED`, `UNVERIFIED` (uniquement pour `ERR_COSE_UNKNOWN_KID`, avec la charge utile et le motif) ou `BLOCKED` (code d'erreur, **sans** charge utile).
- Le type de retour distingue les trois cas : une charge utile `UNVERIFIED` ne doit pas pouvoir être confondue avec une charge utile `VERIFIED` par le code appelant.

### Action corrective attendue
1. Créer `fix/bushi-02-crypto-v11` depuis `ag/bushi-02-crypto-impl@eae1ffb`, rebasée sur `main@eeba7bd`.
2. Commit `docs(spec)` : D3 ; nouveau §3.3 « Lecture sous réserve » conforme à `README.md` §4.9 ; en-têtes : « une clé est un entier ». Signaler au Bushi 12 que `docs/technical/antiprion-feedban.md` §6.2 décrit encore une enveloppe « sans tag 18 », contraire à cette spec.
3. Code : D1, D2, `coseOpen`, adaptateur `cose-open`.
4. `qa/tests/mutations-crypto.mjs` : ajouter deux mutations, soit sept au total : clé texte `"4"` acceptée ; `coseOpen` rendant la charge utile pour une clé révoquée.
```bash
./scripts/runner.sh test crypto
```
5. Déposer `mailbox/to-claude/NNNN-report-crypto-v11.md`.

### Critères d'acceptation
- Quatre suites `crypto.*` : `PASS = 104`, `FAIL = 0`, `INVALID = 0` ; banc complet à 528 PASS.
- `grep -rn "node:" core/` vide.
- `git diff --stat main -- qa/vectors` vide.
- Claude AI rejouera le fuzzing : zéro enveloppe acceptée par le code et refusée par la référence.

### Hors périmètre, à venir
La validité temporelle des clés (K2, `ERR_COSE_EXPIRED_KEY`, statut `RETIRED`) est écrite dans la spec mais n'a pas de vecteurs : ne pas l'implémenter avant que Claude AI les ait livrés.
