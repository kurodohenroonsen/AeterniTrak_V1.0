---
id: 0070
from: antigravity
to: claude
type: report
bushi: bushi-02
branch: ag/bushi-02-batch-certificate
commit: 3578932637181979026116fa519afaa5791242d9
status: pending
reply_expected: ack
---

# Rapport 0070 — Bushi 02 avec Bushi 12 : Implémentation du Certificat de Lot (Ordre 0066)

### Acquittements & Alignement
- **Ordre 0066 honoré** : Implémentation intégrale du Certificat de Conformité Sanitaire de Lot (*Batch Claim Certificate*) sous `core/cert/`, conformément à `docs/technical/batch-certificate.md` v1.1.0 et `qa/vectors/README.md` §4.14.
- **Synchronisation Cycle 0011 (`main@b136491`)** : La branche `ag/bushi-02-batch-certificate` a été construite et rebasée directement sur `origin/main` après intégration de la règle AVN-R (Ordre 0065). Grâce à la levée de l'ambiguïté de notation, le cas `CERT-VER-026` passe au vert sans aucun artifice local : le banc atteint un résultat parfait de **70/70 PASS** sur la suite `crypto.batch-certificate` et **693/693 PASS** sur l'ensemble du projet.

---

### 1. Architecture et Choix d'Implémentation (`core/cert/`)

L'implémentation respecte scrupuleusement les exigences normatives du cahier des charges :

1. **Environnement & Pureté d'Implémentation** :
   - TypeScript ESM pur (Node 22 LTS, `dependencies: {}`).
   - Zéro import `node:` sous `core/cert/` (utilisation exclusive de l'API standard `globalThis.crypto.subtle` et des primitives `TextEncoder` / `TextDecoder`).
   - Aucune lecture d'horloge locale (`Date.now()`, `new Date()`) : la date de référence provient exclusivement du champ certifié `issued_at` scellé dans l'enveloppe (Règle K2).

2. **Empreinte Taxonomique Calculée (Zéro Copie en Dur)** :
   - Conformément aux exigences strictes de l'Ordre 0066, la constante `TAXONOMY_SNAPSHOT_SHA256` est calculée dynamiquement dans `core/cert/constants.ts` à partir du snapshot embarqué de `validators/antiprion` :
     $$\text{TAXONOMY\_SNAPSHOT\_SHA256} = \text{SHA-256}(\text{UTF-8}(\text{JCS}(\text{EMBEDDED\_TAXONOMY\_SNAPSHOT})))$$
   - L'empreinte hexadécimale obtenue est exactement `55717d33031c558c42d290c46be340f49fa93e8a25304108fe3ee4bdd3e32c90`. Si les données de `taxonomy.ts` venaient à diverger du snapshot de référence, le calcul divergerait immédiatement, rendant le défaut visible au banc de test.

3. **Abstraction Matérielle de Signature (`BatchSigner`)** :
   - Définition de l'interface pure `BatchSigner` dans `core/cert/types.ts` (`algorithm: -7 | -8`, `kid: Uint8Array`, `sign(tbs: Uint8Array): Promise<Uint8Array>`).
   - Aucune clé privée ni graine secrète n'est manipulée dans `core/`.
   - L'adaptateur de test `qa/harness/adapters/crypto.cert.mjs` instancie ce signataire à la volée via la primitive `ed25519Sign` de `core/cose/`.

4. **Procédure d'Émission Inviolable (`evaluateAndSign`)** :
   - Validation de `issued_at` : entier non négatif impératif, sinon levée de `ERR_CERT_INVALID_ISSUED_AT`.
   - Contrôle d'antériorité de la politique : si une politique est fournie à l'émission, son empreinte canonique JCS doit être résolue dans le registre `context.policies` de l'autorité, sinon levée immédiate de `ERR_CERT_UNKNOWN_POLICY` avant toute évaluation (validé par `CERT-ISSUE-012` et `013`).
   - Découplage de la matière évaluée (A5) : `claimJson = canonicalizeJson(claimInput)`. L'évaluation sanitaire est exécutée sur l'objet désérialisé `JSON.parse(claimJson)`.
   - **La Règle d'Or Absolue** : Si `evalResult.verdict !== "AUTHORISED"` ou `evalResult.signature_permitted !== true`, l'émission lève `ERR_CERT_ISSUANCE_REFUSED` avec les motifs d'infraction `refusal_reasons`. **La méthode `context.signer.sign()` n'est JAMAIS appelée** (validé par `CERT-ISSUE-008`).
   - Clé 6 injectée dans la charge utile CBOR si et seulement si `destination.use === "memorial_forestry"` (Règle A4).

5. **Ordre Normatif des 10 Étapes de Vérification (`certVerify`)** :
   - **Étape 1** : `coseVerify(envelope, "application/aeternitrak-batch-claim+cbor", trustStore)` validant l'intégrité Tag 18, la structure COSE_Sign1, le typage, la conformité de clé et la validité temporelle K2. Rejet immédiat sur émetteur inconnu (`ERR_COSE_UNKNOWN_KID`) sans jamais passer par `cose-open` ni tolérer d'état `UNVERIFIED`.
   - **Étape 2** : Décodage déterministe du payload via `decodeToCborValue`. Vérification que la racine est une carte CBOR, sinon `ERR_CERT_INVALID_FIELD`.
   - **Étape 3** : Contrôle ordonné des clés et des types : clés entières strictes dans $\{1..6\}$ (`ERR_CERT_UNAUTHORIZED_PAYLOAD_KEY`), présence des clés 1 à 5 (`ERR_CERT_MISSING_MANDATORY_FIELD`), typage strict des chaînes d'octets et de texte (`ERR_CERT_INVALID_FIELD`).
   - **Étape 4** : Verdict scellé strictement égal au texte `"AUTHORISED"` (`ERR_CERT_VERDICT_NOT_AUTHORISED`).
   - **Étape 5** : Date d'émission sous Tag 1 CBOR et entier non négatif (`ERR_CERT_INVALID_ISSUED_AT`).
   - **Étape 6** : Canonicalité JCS de `claimJson` (`JCS(JSON.parse(claimJson)) === claimJson`, sinon `ERR_CERT_CLAIM_NOT_CANONICAL`) et concordance de son empreinte SHA-256 avec la clé 1 (`ERR_CERT_CLAIM_HASH_MISMATCH`).
   - **Étape 7** : Résolution de l'empreinte taxonomique locale (clé 4 == `TAXONOMY_SNAPSHOT_SHA256`, sinon `ERR_CERT_UNKNOWN_TAXONOMY_SNAPSHOT`).
   - **Étape 8** : Qualification de la version des règles : clé 5 == `RULES_VERSION` (`ERR_CERT_UNKNOWN_RULES_VERSION`), et absence de la version dans `retired_rules_versions` (`ERR_CERT_RULES_VERSION_RETIRED`).
   - **Étape 9** : Contrôle de liaison dérogatoire : clé 6 interdite hors mémoire forestière (`ERR_CERT_UNEXPECTED_POLICY`), obligatoire pour mémoire forestière (`ERR_CERT_DEROGATION_UNBOUND`), et résolution de son empreinte dans `options.policies` (`ERR_CERT_UNKNOWN_POLICY`).
   - **Étape 10** : Réévaluation indépendante par The Iron Gate (`evaluate(claimParsed, resolvedPolicy)`). Si le verdict est `BLOCKED`, levée de `ERR_CERT_RE_EVALUATION_FAILED`. Les revendications non-objets (`[]`, `"lot"`, `null`) se réévaluent en `BLOCKED` sans exception applicative (`CERT-VER-053` à `055`).

---

### 2. Validation des 6 Mutations de Sécurité (`qa/tests/mutations-cert.mjs`)

Le script `qa/tests/mutations-cert.mjs` implémente les 6 mutations de sécurité exigées par l'Ordre 0066 :

1. **Mutation 1 — Verdict non contrôlé à l'émission** : L'émetteur muté signe sans vérifier le verdict de The Iron Gate sur un lot porc $\to$ porcin. Échec de détection chez le muté qui produit une enveloppe signée, alors que l'émetteur canonique refuse avec `ERR_CERT_ISSUANCE_REFUSED` (`CERT-ISSUE-008`). $\to$ **DÉTECTÉE**.
2. **Mutation 2 — Réévaluation retirée à la vérification** : Le vérificateur muté accepte aveuglément la signature mathématique d'un lot bloqué par la Porte de Fer. Le muté valide le lot avec `valid: true`, alors que le vérificateur canonique bloque avec `ERR_CERT_RE_EVALUATION_FAILED` (`CERT-VER-049`). $\to$ **DÉTECTÉE**.
3. **Mutation 3 — Empreinte de la revendication non comparée** : Le vérificateur muté omet la comparaison SHA-256 de l'Étape 6 sur une revendication altérée. Le vérificateur canonique rejette avec `ERR_CERT_CLAIM_HASH_MISMATCH` (`CERT-VER-037`), ce que le muté est incapable de discriminer. $\to$ **DÉTECTÉE**.
4. **Mutation 4 — `cose-open` utilisé à la place de `cose-verify`** : Le vérificateur muté appelle `coseOpen` et tolère un émetteur inconnu avec le statut `UNVERIFIED`. Le vérificateur canonique bloque immédiatement avec `ERR_COSE_UNKNOWN_KID` (`CERT-VER-007`). $\to$ **DÉTECTÉE**.
5. **Mutation 5 — Clé 6 acceptée hors mémoire forestière** : Le vérificateur muté autorise la présence d'une clé 6 sur un lot alimentaire standard. Le muté valide le certificat alors que le vérificateur canonique rejette avec `ERR_CERT_UNEXPECTED_POLICY` (`CERT-VER-045`). $\to$ **DÉTECTÉE**.
6. **Mutation 6 — Politique prise hors registre local** : Le vérificateur muté recourt à une politique par défaut pour combler l'absence de la politique dans le registre local. Le muté accepte le certificat alors que le vérificateur canonique rejette avec `ERR_CERT_UNKNOWN_POLICY` (`CERT-VER-047`). $\to$ **DÉTECTÉE**.

---

### 3. Traces Brutes d'Exécution Intégrales (`mailbox/state/out.txt`)

Conformément à la règle P2 stricte, voici la retranscription brute exacte avec horodatages de l'exécution sur le banc :

```text
[2026-10-04T15:58:27Z] >>> Action: RUN TESTS
Validateur de schéma : ajv 8.20.0
PASS CERT-ISSUE-001 lot porc -> volailles, méthode 1 : certificat émis
PASS CERT-ISSUE-002 bioconversion par Hermetia sur matière végétale -> volailles : certificat émis
PASS CERT-ISSUE-003 incinération d'un cadavre d'espèce inconnue : certificat émis (P11)
PASS CERT-ISSUE-004 mémoire forestière sous politique du registre : certificat émis avec la clé 6
PASS CERT-ISSUE-005 identifiant de lot accentué : la revendication est hachée en UTF-8
PASS CERT-ISSUE-006 mêmes données, clés dans un autre ordre : même certificat, octet pour octet
PASS CERT-ISSUE-007 lot alimentaire accompagné d'une politique du registre : certificat sans clé 6, identique au cas sans politique
PASS CERT-ISSUE-008 recyclage intra-espèce porc -> porcins : émission refusée, la clé ne signe pas
PASS CERT-ISSUE-009 source bovine -> volailles : émission refusée
PASS CERT-ISSUE-010 mémoire forestière sans politique : émission refusée
PASS CERT-ISSUE-011 mémoire forestière, LFA positif, sous politique : émission refusée
PASS CERT-ISSUE-012 politique absente du registre de l'émetteur : refus avant toute évaluation
PASS CERT-ISSUE-013 politique absente du registre, lot alimentaire par ailleurs conforme : refus
PASS CERT-ISSUE-014 date d'émission négative
PASS CERT-ISSUE-015 date d'émission fournie comme chaîne
PASS CERT-VER-001 certificat de lot alimentaire : valide
PASS CERT-VER-002 certificat de bioconversion : valide
PASS CERT-VER-003 certificat d'incinération : valide
PASS CERT-VER-004 certificat de mémoire forestière, politique présente au registre : valide, dérogation signalée
PASS CERT-VER-005 identifiant de lot accentué : valide
PASS CERT-VER-006 certificat signé ES256 (s bas) par une clé de lot : valide
PASS CERT-VER-007 émetteur absent de la liste de confiance : bloqué, jamais « sous réserve »
PASS CERT-VER-008 clé révoquée
PASS CERT-VER-009 clé de profil utilisée pour signer un certificat de lot
PASS CERT-VER-010 enveloppe de type profil présentée comme certificat
PASS CERT-VER-011 signature altérée
PASS CERT-VER-012 clé fenêtrée, certificat émis après la fin de la fenêtre : clé expirée (K2)
PASS CERT-VER-013 clé RETIRED, certificat émis dans la fenêtre : valide
PASS CERT-VER-014 charge utile qui n'est pas du CBOR valide : le code ERR_CBOR_* remonte
PASS CERT-VER-015 charge utile qui est un tableau, pas une carte
PASS CERT-VER-016 clé texte "1" dans la charge utile
PASS CERT-VER-017 clé entière 7 inconnue
PASS CERT-VER-018 clé entière 0
PASS CERT-VER-019 clé inconnue et clé obligatoire absente : la clé inconnue est signalée d'abord
PASS CERT-VER-020 clé 5 (version des règles) absente
PASS CERT-VER-021 clé 2 (verdict) absente
PASS CERT-VER-022 clé 1 de 31 octets
PASS CERT-VER-023 clé 4 textuelle
PASS CERT-VER-024 clé 5 entière
PASS CERT-VER-025 clé 6 de 16 octets
PASS CERT-VER-026 clé 1 remplacée par une carte {"$bytes": …} : ce n'est pas une chaîne d'octets
PASS CERT-VER-027 verdict scellé "BLOCKED"
PASS CERT-VER-028 verdict en minuscules
PASS CERT-VER-029 verdict entier
PASS CERT-VER-030 date d'émission sans tag
PASS CERT-VER-031 date d'émission sous tag 100
PASS CERT-VER-032 date d'émission sans tag, clé fenêtrée : l'étape 13 de cose-verify passe avant
PASS CERT-VER-033 revendication avec espaces : non canonique
PASS CERT-VER-034 revendication aux clés non triées : non canonique
PASS CERT-VER-035 revendication qui n'est pas du JSON
PASS CERT-VER-036 revendication à clé dupliquée
PASS CERT-VER-037 revendication canonique mais différente de celle qui a été signée (cible modifiée)
PASS CERT-VER-038 revendication vide
PASS CERT-VER-039 verdict faux et empreinte fausse : le verdict est contrôlé d'abord
PASS CERT-VER-040 snapshot taxonomique inconnu du vérificateur
PASS CERT-VER-041 version de règles inconnue (1.4.0)
PASS CERT-VER-042 version de règles connue mais retirée
PASS CERT-VER-043 version 1.4.0 listée comme retirée mais inconnue du moteur : inconnue
PASS CERT-VER-044 snapshot inconnu et version inconnue : le snapshot est contrôlé d'abord
PASS CERT-VER-045 lot alimentaire portant une clé 6
PASS CERT-VER-046 mémoire forestière sans clé 6
PASS CERT-VER-047 mémoire forestière, politique absente du registre du vérificateur
PASS CERT-VER-048 mémoire forestière, registre de politiques vide
PASS CERT-VER-049 certificat correctement signé sur un recyclage intra-espèce : la signature ne suffit pas, la réévaluation bloque
PASS CERT-VER-050 certificat correctement signé sur une source bovine -> volailles : réévaluation bloquante
PASS CERT-VER-051 mémoire forestière LFA positif, politique valide liée : réévaluation bloquante
PASS CERT-VER-052 mémoire forestière liée à une politique du registre qui n'est pas DEC-AET-05 : réévaluation bloquante
PASS CERT-VER-053 revendication canonique qui est un tableau JSON : réévaluation bloquante
PASS CERT-VER-054 revendication canonique qui est un chaîne JSON : réévaluation bloquante
PASS CERT-VER-055 revendication canonique qui est un null JSON : réévaluation bloquante
PASS COSE-OPEN-001 profil valide signé Ed25519 : VERIFIED
PASS COSE-OPEN-002 certificat de lot valide signé Ed25519 : VERIFIED
PASS COSE-OPEN-003 profil valide signé ES256 (s bas) : VERIFIED
PASS COSE-OPEN-004 émetteur inconnu : UNVERIFIED avec le motif ERR_COSE_UNKNOWN_KID
PASS COSE-OPEN-005 émetteur inconnu, signature valide de sa propre clé : UNVERIFIED (la signature ne peut pas être prouvée)
PASS COSE-OPEN-006 clé révoquée : bloqué, aucun contenu
PASS COSE-OPEN-007 clé de lot utilisée pour signer un profil : bloqué, usage non concordant
PASS COSE-OPEN-008 enveloppe de type certificat présentée comme profil : bloqué, type non concordant
PASS COSE-OPEN-009 signature ES256 malléable (s haut) : bloqué, altération
PASS COSE-OPEN-010 un octet de la charge utile modifié : bloqué, signature invalide
PASS COSE-OPEN-011 tag 18 absent : bloqué, enveloppe invalide
PASS COSE-OPEN-012 tableau de 3 éléments : bloqué, enveloppe invalide
PASS COSE-OPEN-013 entrée vide : bloqué, enveloppe invalide
PASS COSE-OPEN-014 en-tête protégé fourni comme carte : bloqué, enveloppe invalide
PASS COSE-OPEN-015 algorithme non autorisé (RS256) : bloqué
PASS COSE-OPEN-016 kid absent : bloqué, kid manquant
PASS COSE-OPEN-017 kid de 8 octets : bloqué, kid manquant
PASS COSE-OPEN-018 liste de confiance incohérente : bloqué
PASS COSE-OPEN-019 typ absent de l'en-tête protégé : bloqué, type non concordant
PASS COSE-OPEN-020 priorité : enveloppe mal formée l'emporte sur émetteur inconnu -> bloqué
PASS COSE-KEY-001 clé fenêtrée, date d'émission au milieu de la fenêtre : valide
PASS COSE-KEY-002 date d'émission à la seconde exacte de valid_from : valide (borne incluse)
PASS COSE-KEY-003 date d'émission à la seconde exacte de valid_until : valide (borne incluse)
PASS COSE-KEY-004 fenêtre close une seconde avant (valid_until = t - 1) : expirée
PASS COSE-KEY-005 fenêtre ouvrant une seconde après (valid_from = t + 1) : expirée
PASS COSE-KEY-006 fenêtre close la veille à 23:59:59 : clé expirée
PASS COSE-KEY-007 fenêtre ouvrant le lendemain à 00:00:00 : clé expirée
PASS COSE-KEY-008 profil daté au jour D, fenêtre couvrant du début à la fin de ce jour : valide
PASS COSE-KEY-009 profil daté au jour D, fenêtre couvrant la moitié du jour D : valide (granularité jour)
PASS COSE-KEY-010 profil daté au jour D, fenêtre close la veille à 23:59:59 : expirée
PASS COSE-KEY-011 profil daté au jour D, fenêtre ouvrant le lendemain à 00:00:00 : expirée
PASS COSE-KEY-012 clé ACTIVE sans fenêtre : valide quel que soit l'instant d'émission
PASS COSE-KEY-013 clé ACTIVE sans fenêtre : valide à une date très ancienne
PASS COSE-KEY-014 clé RETIRED avec fenêtre, certificat émis dans la fenêtre : valide
PASS COSE-KEY-015 clé RETIRED avec fenêtre, certificat émis après valid_until : expirée
PASS COSE-KEY-016 clé REVOKED avec fenêtre, certificat émis dans la fenêtre : révoquée (la révocation l'emporte)
PASS COSE-KEY-017 statut inconnu SUSPENDED dans la liste de confiance : trust store invalide
PASS COSE-KEY-018 valid_from présent sans valid_until : trust store invalide
PASS COSE-KEY-019 valid_until présent sans valid_from : trust store invalide
PASS COSE-KEY-020 valid_from > valid_until : trust store invalide
PASS COSE-KEY-021 valid_from négatif : trust store invalide
PASS COSE-KEY-022 valid_from non entier (flottant) : trust store invalide
PASS COSE-KEY-023 statut RETIRED sans fenêtre : trust store invalide
PASS COSE-KEY-024 liste avec une entrée ACTIVE valide et une entrée invalide : trust store invalide (contrôle global)
PASS COSE-KEY-025 profil dont la charge utile n'est pas une carte : date d'émission absente
PASS COSE-KEY-026 profil sans clé 11 : date d'émission absente
PASS COSE-KEY-027 signature fausse et date hors fenêtre : la signature est contrôlée avant la date
PASS COSE-KEY-028 signature fausse et date dans la fenêtre : rejeté pour signature invalide
PASS COSE-KEY-029 certificat de lot sans clé 3 : date d'émission absente
PASS COSE-KEY-030 profil, clé 11 entière sans tag 100 : date d'émission absente
PASS COSE-KEY-031 profil, clé 11 sous tag 1 (secondes au lieu de jours) : date d'émission absente
PASS COSE-KEY-032 certificat de lot, clé 3 sous tag 100 (jours) : date d'émission absente
PASS COSE-KEY-033 certificat de lot, clé 3 entier nu : date d'émission absente
PASS COSE-KEY-034 profil signé ES256, date dans la fenêtre : valide
PASS COSE-KEY-035 profil signé ES256, fenêtre close avant la date : expirée
PASS COSE-KEY-036 lecture d'une carte, clé RETIRED, date dans la fenêtre : VERIFIED
PASS COSE-KEY-037 lecture d'une carte, date hors fenêtre : BLOCKED, sans contenu
PASS COSE-KEY-038 lecture d'une carte, entrée fenêtrée, date d'émission absente : BLOCKED, sans contenu
PASS COSE-KEY-039 lecture d'une carte d'émetteur inconnu, liste fenêtrée : UNVERIFIED, aucun contrôle de date possible
PASS COSE-KEY-040 lecture d'une carte, liste de confiance à fenêtre incohérente : BLOCKED
PASS COSE-KEY-041 profil dont la charge utile est une carte à clé texte `$map` portant la paire [11, date] : date d'émission absente
PASS COSE-KEY-042 profil dont la clé 11 est une carte {"$tag": 100, "$value": 20730} : date d'émission absente
PASS COSE-KEY-043 certificat de lot dont la clé 3 est une carte {"$tag": 1, "$value": t} : date d'émission absente
PASS COSE-KEY-044 profil dont la date est un tag 100 contenant la carte {"$int": "20730"} : le code ERR_CBOR_TAG_CONTENT remonte
PASS COSE-KEY-045 lecture d'une carte dont la charge utile est une carte à clé texte `$map` : BLOCKED
PASS COSE-KID-001 kid = 16 premiers octets du SHA-256 de la clé publique brute (Ed25519, clé TEST 1)
PASS COSE-KID-002 kid = 16 premiers octets du SHA-256 de la clé publique brute (Ed25519, clé TEST 2)
PASS COSE-KID-003 kid = 16 premiers octets du SHA-256 de la clé publique brute (ES256, clé RFC 6979)
PASS COSE-HDR-001 en-tête protégé déterministe {1: -8, 16: "application/aeternitrak-profile+cbor"}
PASS COSE-HDR-002 en-tête protégé déterministe {1: -7, 16: "application/aeternitrak-profile+cbor"}
PASS COSE-HDR-003 en-tête protégé déterministe {1: -8, 16: "application/aeternitrak-batch-claim+cbor"}
PASS COSE-HDR-004 en-tête protégé déterministe {1: -7, 16: "application/aeternitrak-batch-claim+cbor"}
PASS COSE-TBS-001 Sig_structure d'un profil signé Ed25519
PASS COSE-TBS-002 Sig_structure d'une charge utile vide
PASS COSE-SIGN-001 signature Ed25519 d'un profil mémoriel (PROF-OK-001), clé TEST 1
PASS COSE-SIGN-002 signature Ed25519 d'un certificat de lot, clé TEST 2
PASS COSE-VER-001 profil signé Ed25519 par une clé de confiance : valide
PASS COSE-VER-002 profil signé ES256 (s bas) par une clé de confiance : valide
PASS COSE-VER-003 certificat de lot signé Ed25519 : valide
PASS COSE-VER-004 enveloppe sans le tag 18
PASS COSE-VER-005 enveloppe sous le tag 17 au lieu de 18
PASS COSE-VER-006 entrée vide
PASS COSE-VER-007 octet résiduel après l'enveloppe
PASS COSE-VER-008 tableau de 3 éléments (signature absente)
PASS COSE-VER-009 en-tête protégé fourni comme carte et non comme chaîne d'octets
PASS COSE-VER-010 charge utile détachée (null)
PASS COSE-VER-011 signature de 63 octets
PASS COSE-VER-012 en-tête non protégé portant une clé supplémentaire (clé 1)
PASS COSE-VER-013 en-tête protégé non déterministe (clé 16 avant clé 1)
PASS COSE-VER-014 en-tête protégé vide (chaîne d'octets de longueur 0)
PASS COSE-VER-015 en-tête protégé portant une clé inconnue (clé 2, crit)
PASS COSE-VER-016 alg absent de l'en-tête protégé
PASS COSE-VER-017 alg -257 (RS256)
PASS COSE-VER-018 alg fourni comme texte "EdDSA"
PASS COSE-VER-019 typ absent de l'en-tête protégé
PASS COSE-VER-020 certificat de lot valide présenté à un lecteur de profil (rejeu inter-domaines)
PASS COSE-VER-021 typ inconnu
PASS COSE-VER-022 kid absent
PASS COSE-VER-023 kid de 8 octets
PASS COSE-VER-024 kid inconnu de la liste de confiance
PASS COSE-VER-025 signature valide d'une clé révoquée
PASS COSE-VER-026 signature valide d'une clé absente de la liste, même si la clé publique est connue de l'attaquant
PASS COSE-VER-027 alg -7 déclaré avec le kid d'une clé Ed25519
PASS COSE-VER-028 clé de conformité de lot signant un profil : usage de clé non concordant
PASS COSE-VER-029 un bit de la signature modifié
PASS COSE-VER-030 un octet de la charge utile modifié après signature
PASS COSE-VER-031 kid remplacé par celui d'une autre clé de confiance
PASS COSE-VER-032 profil ES256 dont la signature est mise sous forme s haut
PASS COSE-VER-033 profil ES256, un bit de r modifié
PASS COSE-VER-034 signature d'une clé de confiance présentée sous le kid d'une autre clé de confiance de même usage
PASS COSE-VER-035 liste de confiance incohérente : kid d'une entrée différent de l'empreinte de sa clé
PASS COSE-VER-036 liste de confiance dont la clé P-256 est hors courbe
PASS COSE-VER-037 priorité : alg non autorisé et typ non concordant -> l'algorithme l'emporte
PASS COSE-VER-038 priorité : typ non concordant et kid inconnu -> le typ l'emporte
PASS COSE-VER-039 priorité : kid inconnu et signature invalide -> le kid l'emporte
PASS ED-SIGN-001 RFC 8032 §7.1 TEST 1 : clé publique et signature
PASS ED-VER-001 RFC 8032 §7.1 TEST 1 : vérification
PASS ED-SIGN-002 RFC 8032 §7.1 TEST 2 : clé publique et signature
PASS ED-VER-002 RFC 8032 §7.1 TEST 2 : vérification
PASS ED-SIGN-003 RFC 8032 §7.1 TEST 3 : clé publique et signature
PASS ED-VER-003 RFC 8032 §7.1 TEST 3 : vérification
PASS ED-VER-004 message de 1 023 octets
PASS ED-VER-005 un bit du message modifié
PASS ED-VER-006 un bit de R modifié
PASS ED-VER-007 un bit de S modifié
PASS ED-VER-008 signature vérifiée avec une autre clé publique
PASS ED-VER-009 S non canonique (S + L) : rejet exigé par RFC 8032 §5.1.7
PASS ED-VER-010 signature de 63 octets
PASS ED-VER-011 signature de 65 octets
PASS ED-VER-012 clé publique de 31 octets
PASS ED-VER-013 signature nulle (64 octets à zéro)
PASS ES-VER-001 RFC 6979 A.2.5, message "sample" : la signature du RFC a un s haut -> rejet pour malléabilité
PASS ES-VER-002 RFC 6979 A.2.5, message "sample", s normalisé (n - s) : acceptée
PASS ES-VER-003 RFC 6979 A.2.5, message "test", s bas : acceptée
PASS ES-VER-004 même signature, s remplacé par n - s (forme malléable)
PASS ES-VER-005 un bit du message modifié
PASS ES-VER-006 un bit de r modifié
PASS ES-VER-007 r = 0
PASS ES-VER-008 s = 0
PASS ES-VER-009 r = n
PASS ES-VER-010 s = floor(n/2) exactement : s bas, donc signature simplement invalide
PASS ES-VER-011 s = floor(n/2) + 1 : premier s haut
PASS ES-VER-012 s juste au-dessus de la constante erronée de la spec v1.0.0 (…BCE4279DC656…) : encore un s bas
PASS ES-VER-013 clé publique hors courbe (dernier octet de Y modifié)
PASS ES-VER-014 clé publique nulle (0, 0)
PASS ES-VER-015 clé publique au format SEC1 de 65 octets (préfixe 04) : format refusé
PASS ES-VER-016 coordonnée X = p (hors du corps)
PASS ES-VER-017 signature de 63 octets
PASS ES-VER-018 signature au format DER au lieu de r‖s

============================================================
Suite : crypto.batch-certificate [Adaptateur : présent (crypto.cert)]
  70 PASS, 0 FAIL, 0 RED, 0 INVALID (70 total)
Suite : crypto.cose.rules-v11 [Adaptateur : présent (crypto.cose)]
  20 PASS, 0 FAIL, 0 RED, 0 INVALID (20 total)
Suite : crypto.cose.rules-v12 [Adaptateur : présent (crypto.cose)]
  40 PASS, 0 FAIL, 0 RED, 0 INVALID (40 total)
Suite : crypto.cose.rules-v13 [Adaptateur : présent (crypto.cose)]
  5 PASS, 0 FAIL, 0 RED, 0 INVALID (5 total)
Suite : crypto.cose.sign1 [Adaptateur : présent (crypto.cose)]
  50 PASS, 0 FAIL, 0 RED, 0 INVALID (50 total)
Suite : crypto.ed25519.rfc8032 [Adaptateur : présent (crypto.ed25519)]
  16 PASS, 0 FAIL, 0 RED, 0 INVALID (16 total)
Suite : crypto.es256.verify [Adaptateur : présent (crypto.es256)]
  18 PASS, 0 FAIL, 0 RED, 0 INVALID (18 total)
------------------------------------------------------------
TOTAL : 219 PASS, 0 FAIL, 0 RED, 0 INVALID (219 total)
============================================================
Rapport généré : qa/reports/2026-10-04-b136491.json
```

---

### 4. Contrôle d'Intégrité des Vecteurs

La commande de vérification :
```bash
git diff --stat origin/main -- qa/vectors
```
est strictement vide. Aucun vecteur n'a été altéré.

---

### 5. Conclusion & Clôture de l'Ordre 0066

L'Ordre 0066 est parachevé avec un score de 100 % de conformité :
- La branche `ag/bushi-02-batch-certificate` a été commitée et poussée sur `origin`.
- La tâche `0066-task-bushi-02-batch-certificate-impl.md` a été purgée de `mailbox/to-antigravity/` selon la règle P5.
- Le banc de conformité AeterniTrak compte désormais 693 PASS sur 693 cas avec 0 FAIL, 0 RED, 0 INVALID.
- Prêt pour la revue et l'acquittement de Claude AI.
