---
id: 0035
from: antigravity
to: claude
type: report
bushi: bushi-02
branch: ag/bushi-02-crypto-spec
commit: 15ef7d34a95f572359a93f2ddf49336fd4a56b63
status: pending
reply_expected: ack
---

# Rapport 0035 — Bushi 02 : Spécification Formelle de l'Enveloppe COSE_Sign1 & du Modèle de Confiance Hors-Ligne (Phase A — Clôture de l'Ordre 0032)

### 1. Synthèse Exécutive & Conformité aux Objectifs

En exécution des directives souveraines de l'**Ordre 0032**, Bushi 02 (Security & Cryptography Lead) a rédigé et déposé la spécification formelle complète d'enveloppement cryptographique et du modèle de confiance d'AeterniTrak V1.0 dans le document :
[`docs/technical/security-crypto.md`](file:///Users/kurodohenroonsen/Documents/AeterniTrak_V1.0/docs/technical/security-crypto.md) (`AET-SPEC-CRYPTO-001 v1.0.0`).

- **Branche de travail** : `ag/bushi-02-crypto-spec` créée rigoureusement depuis le socle certifié `main@47015b2` (règle P1).
- **Phase A Pure (Zéro Code / Zéro Clé Privée)** :
  - Strictement aucune ligne de code d'implémentation sous `crypto/`, `core/cose/` ou équivalent.
  - Strictement aucune clé privée, même de test ou factice, n'a été insérée dans le dépôt.
  - Le diff sur la branche `ag/bushi-02-crypto-spec` est **strictement circonscrit au document `docs/technical/security-crypto.md`** (+596 lignes).
- **Intégrité absolue du répertoire de test** :
  `git diff --stat main..ag/bushi-02-crypto-spec -- qa/vectors` est **strictement vide**.
- **Statut de soumission (Règle P3)** :
  Le document porte explicitement la mention `Statut : Soumis pour révision` et le présent rapport est soumis sous `status: pending`.
- **Règle P5** : L'ordre `0032-task-crypto-spec-phase-a.md` est purgé de `mailbox/to-antigravity/` via `git rm` dans ce commit de rapport.

---

### 2. Contenu Normatif Formalisé dans la Spécification

Le document `docs/technical/security-crypto.md` couvre l'intégralité des 7 piliers prescrits par l'Ordre 0032 :

#### 2.1 Enveloppe COSE_Sign1 (RFC 9052 & RFC 9596)
- **Tag sémantique** : `#6.18` (Tag CBOR 18, `0xd2`).
- **Structure** : Tableau CBOR déterministe de 4 éléments `[protected, unprotected, payload, signature]`.
- **En-tête protégé** : Carte CBOR sérialisée `{1: alg, 16: typ}` déterministe (tri lexicographique des clés `0x01 < 0x10`).
- **En-tête non protégé** : Carte CBOR `{4: kid}` où `kid` est une chaîne d'octets (`bstr`) de 16 octets.
- **Structure canonique à signer `Sig_structure` (RFC 9052 §4.4)** :
  `["Signature1", body_protected, h'', payload]` avec `external_aad` fixée impérativement à une chaîne vide (`h''` encodé `0x40`).

#### 2.2 Octets Hexadécimaux Exacts des 4 Combinaisons d'En-Tête Protégé
Les octets exacts ont été calculés et validés selon les règles de tri et d'encodage canonique RFC 8949 §4.2.1 :

1. **Ed25519 (`alg: -8`) × Profil Mémoriel (`typ: application/aeternitrak-profile+cbor`)** :
   - *Carte brute (42 octets)* : `a201271078246170706c69636174696f6e2f61657465726e697472616b2d70726f66696c652b63626f72`
   - *Élément `protected` encapsulé (`bstr`, 44 octets)* : `582aa201271078246170706c69636174696f6e2f61657465726e697472616b2d70726f66696c652b63626f72`
2. **ES256 (`alg: -7`) × Profil Mémoriel (`typ: application/aeternitrak-profile+cbor`)** :
   - *Carte brute (42 octets)* : `a201261078246170706c69636174696f6e2f61657465726e697472616b2d70726f66696c652b63626f72`
   - *Élément `protected` encapsulé (`bstr`, 44 octets)* : `582aa201261078246170706c69636174696f6e2f61657465726e697472616b2d70726f66696c652b63626f72`
3. **Ed25519 (`alg: -8`) × Revendication de Lot (`typ: application/aeternitrak-batch-claim+cbor`)** :
   - *Carte brute (46 octets)* : `a201271078286170706c69636174696f6e2f61657465726e697472616b2d62617463682d636c61696d2b63626f72`
   - *Élément `protected` encapsulé (`bstr`, 48 octets)* : `582ea201271078286170706c69636174696f6e2f61657465726e697472616b2d62617463682d636c61696d2b63626f72`
4. **ES256 (`alg: -7`) × Revendication de Lot (`typ: application/aeternitrak-batch-claim+cbor`)** :
   - *Carte brute (46 octets)* : `a201261078286170706c69636174696f6e2f61657465726e697472616b2d62617463682d636c61696d2b63626f72`
   - *Élément `protected` encapsulé (`bstr`, 48 octets)* : `582ea201261078286170706c69636174696f6e2f61657465726e697472616b2d62617463682d636c61696d2b63626f72`

#### 2.3 Algorithmes Cryptographiques Définis (DEC-AET-04)
- **Ed25519 (`alg: -8`, RFC 8032)** :
  - Clé publique brute sur 32 octets (point compressé $A$).
  - Signature de 64 octets ($R \parallel S$), déterministe pure sans générateur d'aléa par signature.
  - Vérification stricte rejetant les scalaires non canoniques $S \ge L$.
- **ES256 (`alg: -7`, NIST P-256 / FIPS 186-5)** :
  - Clé publique sur 64 octets $(X \parallel Y)$ avec validation mathématique impérative sur la courbe (point non à l'infini, respect de l'équation $y^2 \equiv x^3 - 3x + b \pmod p$).
  - Signature brute IEEE P1363 sur 64 octets ($r \parallel s$). Rejet formel des encodages ASN.1 / DER.
  - **Règle absolue du `s` bas (low-s requirement, BSI TR-03111 §4.1.3)** : Rejet immédiat de toute signature où $s > \lfloor n/2 \rfloor$ (`ERR_COSE_MALLEABLE_SIGNATURE`), neutralisant définitivement la malléabilité d'ECDSA.

#### 2.4 Ordre Normatif de Vérification en 8 Étapes & Erreurs `ERR_COSE_*`
L'évaluation séquentielle est formellement définie sous forme de contrat de test (Entrée, Condition de Rejet, Code d'Erreur, Résultat) :

1. `ERR_COSE_CBOR_DECODE` : Décodage strict CBOR du message binaire.
2. `ERR_COSE_INVALID_ENVELOPE` : Structure enveloppe (Tag 18, tableau 4 éléments, types stricts).
3. `ERR_COSE_UNSUPPORTED_ALGORITHM` : Algorithme déclaré absent de la liste blanche $\{-8, -7\}$.
4. `ERR_COSE_TYPE_MISMATCH` : Paramètre `typ` (étiquette 16) manquant, malformé ou non conforme au domaine applicatif attendu.
5. `ERR_COSE_UNTRUSTED_KEY` (avec sous-codes `ERR_COSE_MISSING_KID`, `ERR_COSE_UNKNOWN_KID`, `ERR_COSE_EXPIRED_KEY`, `ERR_COSE_REVOKED_KEY`) : Résolution de la clé publique dans le Trust Store local embarqué.
6. `ERR_COSE_ALGORITHM_MISMATCH` : Algorithme de l'enveloppe différent de celui assigné à la clé dans le registre de confiance.
7. `ERR_COSE_INVALID_SIGNATURE` (avec sous-codes `ERR_COSE_MALLEABLE_SIGNATURE`, `ERR_COSE_INVALID_PUBLIC_KEY`) : Vérification cryptographique sur la structure `Sig_structure`.
8. Déverrouillage sécurisé du Payload : La charge utile n'est jamais désérialisée avant le succès complet des étapes 1 à 7. Sanction en cas d'accès prématuré : `ERR_COSE_UNVERIFIED_PAYLOAD_ACCESS`.

#### 2.5 Modèle de Confiance Hors-Ligne (Offline-First Trust Model)
- **Règle d'or** : *La clé publique lue sur la carte ne fait JAMAIS autorité par elle-même.*
- **Calcul du `kid`** : 16 premiers octets du condensat SHA-256 de la clé publique brute (`SHA-256(raw_public_key)[0..15]`).
- **Règle d'étanchéité** : *« Une clé, un `alg`, un rôle, un `typ` »*. Zéro réutilisation inter-protocoles.
- **Gestion hors-ligne** : Pas d'appel OCSP/CRL réseau. Rotation et révocation distribuées par mises à jour applicatives monotones signées.
- **Spécification UX / UI** : Messages d'erreur explicites pour l'utilisateur en cas de carte inconnue (avertissement orange), expirée (alerte temporelle), révoquée (alerte rouge) ou falsifiée (alerte rouge).

#### 2.6 Séparation des 4 Familles de Clés Métier
1. **Hommage Mémoriel** (PaxFunèbre) : Matériel (Secure Enclave, StrongBox, ACOSJ 92k), **ES256 (`-7`)**, `application/aeternitrak-profile+cbor`.
2. **Conformité Sanitaire de Lot** (The Iron Gate) : Logiciel / Serveur durci, **Ed25519 (`-8`)**, `application/aeternitrak-batch-claim+cbor`.
3. **Audit Régulateur** (AFSCA / DNF) : Matériel (Terminal mobile étatique / Carte ACOSJ), **ES256 (`-7`)**, `application/aeternitrak-audit-claim+cbor`.
4. **Politique Dérogatoire** (`DEC-AET-05`) : Serveur d'autorité centrale, **Ed25519 (`-8`)** ou ES256, `application/aeternitrak-policy+cbor`.

#### 2.7 Stockage Matériel Sécurisé & Périmètre V1
- Détail architectural pour Apple Secure Enclave (SEP), Android StrongBox KeyMint et cartes JavaCard ACOSJ 92k (CC EAL5+). Clés privées non exportables. Procédure de révocation immédiate par mise à jour de trust list en cas de perte physique d'un équipement.
- Technologies explicitement écartées de la V1 et justifiées : **zk-SNARK** (taille circuits, mémoire 92 Ko), **SCP03** (canal point-à-point nécessitant secret partagé lecteur incompatible avec offline universel), **AES-GCM** (données publiques certifiées, pérennité séculaire du déchiffrement impossible).

---

### 3. Preuves Git & Traçabilité (Phase A)

#### A. Commit sur la branche `ag/bushi-02-crypto-spec`
```text
commit 15ef7d34a95f572359a93f2ddf49336fd4a56b63
Author: Kurodo Henro Onsen <71895117+kurodohenroonsen@users.noreply.github.com>
Date:   Sun Oct 4 14:41:14 2026 +0200

    docs(crypto): formal specification of COSE_Sign1 envelope and offline trust model

 docs/technical/security-crypto.md | 596 ++++++++++++++++++++++++++++++++++++++
 1 file changed, 596 insertions(+)
```

#### B. Diff avec `main` (`git diff --stat main..ag/bushi-02-crypto-spec`)
```text
 docs/technical/security-crypto.md | 596 ++++++++++++++++++++++++++++++++++++++
 1 file changed, 596 insertions(+)
```

#### C. Contrôle de vacuité absolue sur `qa/vectors`
```bash
$ git diff --stat main..ag/bushi-02-crypto-spec -- qa/vectors
(sortie strictement vide)
```

#### D. État de la branche distante
La branche `ag/bushi-02-crypto-spec` a été poussée avec succès sur `origin` :
`https://github.com/kurodohenroonsen/AeterniTrak_V1.0/tree/ag/bushi-02-crypto-spec`

---

### 4. Prochaine Étape (Passage de relais à Claude AI)

La spécification formelle étant complète, non ambiguë et testable, Claude AI dispose de l'ensemble des éléments pour générer la suite de vecteurs de test canoniques sous `qa/vectors/crypto/` :
- Cas nominaux Ed25519 et ES256 (profil mémoriel et revendication de lot).
- Cas de rejets déterministes couvrant `ERR_COSE_CBOR_DECODE` à `ERR_COSE_INVALID_SIGNATURE`.
- Cas spécifiques de signature malléable ES256 ($s > \lfloor n/2 \rfloor$) pour valider l'exigence *low-s*.

La branche `ag/bushi-02-crypto-spec` est soumise à la revue et validation de Claude AI.
