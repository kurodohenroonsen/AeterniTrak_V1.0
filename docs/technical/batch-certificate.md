# Spécification Technique & Formelle — Certificat de Conformité Sanitaire de Lot (Batch Claim Certificate)

> **Document ID** : `AET-SPEC-CERT-001`  
> **Version** : 1.0.0  
> **Statut** : Soumis pour révision  
> **Date de référence** : 2026-10-04  
> **Branche Git** : `ag/bushi-02-batch-certificate-spec`  
> **Auteur** : Bushi 02 (Security & Cryptography Lead, en concertation avec Bushi 12)  
> **Revue & Arbitrage** : Claude AI (Master Verifier)  
> **Autorité Souveraine** : Kudoro (`DECISIONS-KUDORO.md`, décisions `DEC-AET-04`, `DEC-AET-05`, `DEC-AET-07`)  
> **Contrats Partagés** : Bushi 12 (Anti-Prion & The Iron Gate), Bushi 01 (AeterniCore Déterminisme CBOR & Canonisation JCS), Bushi 16 (QA Testvectors & Harnais)  
> **Phase du Chantier** : Phase A — Spécification Formelle Pure (Zéro code d'implémentation dans `core/`, zéro vecteur de test approuvé)

---

## 1. Cadre Architectural & Objet de la Spécification

Le présent document formalise l'architecture, la structure binaire, les règles d'évaluation, le protocole d'émission et l'ordre normatif de vérification du **Certificat de Conformité Sanitaire de Lot** (*Batch Claim Certificate*).

Ce certificat constitue la clé de voûte de la filière de traçabilité AeterniTrak. Il réalise la composition sécurisée entre deux sous-systèmes préalablement validés et scellés :
1. **The Iron Gate (Bushi 12 / `AET-SPEC-PRION-001`)** : Le moteur algorithmique déterministe appliquant le principe du *Default-Deny* et les 10 portes de contrôle sanitaire G0 à G9 relatives aux encéphalopathies spongiformes transmissibles (EST / prions), au feed-ban européen (Règlements CE 999/2001, UE 2021/1372, CE 1069/2009, UE 142/2011) et à l'interdiction absolue de recyclage intra-espèce.
2. **Le Moteur Cryptographique COSE_Sign1 (Bushi 02 / `AET-SPEC-CRYPTO-001`)** : L'infrastructure de signature numérique universelle, agnostique et portable, assurant l'agilité cryptographique (Ed25519 `alg: -8` et NIST P-256 ES256 `alg: -7`), le déterminisme d'encodage CBOR (RFC 8949 §4.2.1), la séparation stricte de domaine (`typ`) et le modèle de confiance hors-ligne (*Offline-First Trust Store*).

### 1.1 Principes Fondamentaux Arrêtés

Conformément à l'Ordre 0047 de Claude AI et aux arbitrages de Kudoro :

1. **Aucun Certificat pour une Revendication Rejetée** : L'oracle d'émission évalue la revendication via The Iron Gate. Si le verdict n'est pas strictement `AUTHORISED` ou si la condition `signature_permitted` est fausse, l'émission est formellement bloquée. Aucun certificat de rejet ou certificat conditionnel n'est jamais signé.
2. **Double Validation Indépendante (Zéro Confiance Aveugle en la Signature)** : Le vérificateur ne se contente pas de valider la signature mathématique de l'enveloppe : il reconstruit et réévalue obligatoirement la revendication sanitaire originale à l'aide du snapshot taxonomique officiel et de la version des règles formellement scellés dans le certificat.
3. **Architecture Anti-Flottants (A3)** : Pour préserver le déterminisme absolu du décodage CBOR (qui proscrit les flottants de type major 7), la revendication originale complète voyage sous forme de chaîne JSON canonique JCS (RFC 8785). La charge utile CBOR signée ne contient que l'empreinte SHA-256 de cette chaîne canonique.
4. **Imperméabilité Temporelle Post-Signature (Règle K2)** : La validité d'une clé de signature est comparée à la date d'émission portée par la charge utile certifiée (clé `3`), jamais à la date locale de lecture sur le terminal de contrôle.
5. **Séparation de Domaine Hermétique** : L'enveloppe porte impérativement le paramètre d'en-tête protégé `typ = "application/aeternitrak-batch-claim+cbor"`. Une clé de conformité de lot ne peut en aucun cas signer un profil mémoriel, et un profil mémoriel ne peut en aucun cas être substitué à un certificat de lot (`ERR_COSE_KEY_USAGE_MISMATCH`, `ERR_COSE_TYPE_MISMATCH`).

---

## 2. Spécification Binaire de la Charge Utile (Payload CBOR Déterministe)

La charge utile du certificat de lot est une carte CBOR déterministe (RFC 8949 §4.2.1) encodée selon les règles strictes d'AeterniCore. Toutes les clés sont **strictement des entiers non signés (Major Type 0)**, triées par ordre lexicographique bytewise croissant.

### 2.1 Structure des Clés Entières de la Charge Utile

| Clé (Int) | Nom Sémantique | Type CBOR | Taille / Format | Statut | Description Normative |
|:---:|---|---|---|:---:|---|
| **`1`** | `claim_sha256` | Byte String (`bstr`, Major 2) | Exactement 32 octets | **Obligatoire** | Empreinte SHA-256 de la représentation JSON canonique de la revendication : $\text{SHA-256}(\text{JCS}(\text{claim}))$. |
| **`2`** | `verdict` | Text String (`tstr`, Major 3) | Chaîne UTF-8 | **Obligatoire** | Chaîne littérale `"AUTHORISED"` exclusivement. Toute autre valeur rend le certificat invalide. |
| **`3`** | `issued_at` | Semantic Tag 1 (`#6.1`, Major 6) | Entier non négatif (Major 0) | **Obligatoire** | Date et heure de scellage du certificat, en secondes écoulées depuis l'epoch UNIX (1970-01-01T00:00:00Z UTC). |
| **`4`** | `snapshot_sha256` | Byte String (`bstr`, Major 2) | Exactement 32 octets | **Obligatoire** | Empreinte SHA-256 du snapshot taxonomique officiel (RFC 8785 JCS) employé lors de l'évaluation sanitaire : $\text{SHA-256}(\text{JCS}(\text{taxonomy-snapshot}))$. |
| **`5`** | `rules_version` | Text String (`tstr`, Major 3) | Chaîne UTF-8 SemVer | **Obligatoire** | Version de la spécification normative des règles sanitaires de la Porte de Fer (ex. `"1.4.0"`). |
| **`6`** | `policy_sha256` | Byte String (`bstr`, Major 2) | Exactement 32 octets | **Conditionnel** | Empreinte SHA-256 du document de politique dérogatoire canonisé JCS : $\text{SHA-256}(\text{JCS}(\text{policy}))$. Présent **uniquement** si le lot est validé sous dérogation DEC-AET-05. |

### 2.2 Règle de Présence / Absence Absolue de la Clé `6` (Dérogation)

1. **Lot Standard (Sans Dérogation)** :
   - Pour toute destination standard (`feed`, `aquaculture_feed`, `technical`, `fertiliser`, `incineration`), la clé `6` **DOIT ÊTRE STRICTEMENT ABSENTE** de la carte CBOR.
   - La présence d'une clé `6` sur un lot standard constitue une violation de déterminisme structurel et déclenche le rejet immédiat avec `ERR_CERT_UNEXPECTED_POLICY`.
2. **Lot sous Dérogation (DEC-AET-05)** :
   - Pour la destination `memorial_forestry` autorisée sous l'arbitrage Kudoro DEC-AET-05, la clé `6` **DOIT ÊTRE STRICTEMENT PRÉSENTE** et contenir exactement les 32 octets du hachage de la politique homologuée.
   - L'absence de la clé `6` pour un lot requérant une dérogation déclenche le rejet immédiat avec `ERR_CERT_DEROGATION_UNBOUND`.

### 2.3 Définition Formelle CDDL (RFC 8610)

```cddl
batch_claim_certificate = #6.18(COSE_Sign1_Batch)

COSE_Sign1_Batch = [
  protected: bstr .cbor protected_header_map,
  unprotected: unprotected_header_map,
  payload: bstr .cbor batch_certificate_payload,
  signature: bstr .size 64
]

protected_header_map = {
  1: -7 / -8, ; alg: ES256 (-7) ou Ed25519 (-8)
  16: "application/aeternitrak-batch-claim+cbor" ; typ spécifique (RFC 9596)
}

unprotected_header_map = {
  4: bstr .size 16 ; kid: 16 octets = SHA-256(raw_public_key)[0..15]
}

batch_certificate_payload = {
  1: bstr .size 32, ; claim_sha256 = SHA-256(JCS(claim))
  2: "AUTHORISED",  ; verdict textuel scellé
  3: #6.1(uint),    ; issued_at: epoch secondes UTC
  4: bstr .size 32, ; snapshot_sha256 = SHA-256(JCS(taxonomy_snapshot))
  5: tstr,          ; rules_version (ex: "1.4.0")
  ? 6: bstr .size 32 ; policy_sha256 = SHA-256(JCS(policy)), conditionnel DEC-AET-05
}
```

---

## 3. Spécification de l'Enveloppe COSE_Sign1 & Budget de Taille

### 3.1 Structure de l'Enveloppe Scellée

1. **Tag CBOR 18 Obligatoire (`0xd2`)** :
   - Conformément au RFC 9052 §4.2 et à `AET-SPEC-CRYPTO-001` (Règle K4), le premier octet de l'enveloppe sérialisée est obligatoirement `0xd2`. Toute omission ou utilisation d'un autre tag est rejetée avec `ERR_COSE_INVALID_ENVELOPE`.
2. **En-tête Protégé (`protected`)** :
   - Encodé de manière canonique sous la forme d'une carte CBOR sérialisée en chaîne d'octets (`bstr`).
   - Clés entières strictes triées par ordre lexicographique :
     - `1` (`alg`) : `-8` (Ed25519) ou `-7` (ES256).
     - `16` (`typ`) : `"application/aeternitrak-batch-claim+cbor"`.
   - Octets canoniques exacts :
     - Pour Ed25519 (`alg: -8`) : `a201271078286170706c69636174696f6e2f61657465726e697472616b2d62617463682d636c61696d2b63626f72` (46 octets)
     - Pour ES256 (`alg: -7`) : `a201261078286170706c69636174696f6e2f61657465726e697472616b2d62617463682d636c61696d2b63626f72` (46 octets)
3. **En-tête Non Protégé (`unprotected`)** :
   - Carte CBOR ne portant aucune autre clé que la clé entière `4` (`kid`).
   - La clé texte `"4"` est formellement interdite (`COSE-VER-041`, `ERR_COSE_INVALID_ENVELOPE`).
   - La valeur associée à `4` est obligatoirement un `bstr` de 16 octets exacts, calculé selon :
     $$\text{kid} = \text{SHA-256}(\text{raw\_public\_key})[0..15]$$
4. **Structure TBS (`Sig_structure`)** :
   - Conforme au RFC 9052 §4.4 :
     $$\text{Sig\_structure} = \big[ \text{"Signature1"}, \text{protected\_bytes}, \text{h''}, \text{payload\_bytes} \big]$$
5. **Signature Cryptographique** :
   - Chaîne d'octets (`bstr`) de 64 octets exactement.
   - Pour ES256 : Format IEEE P1363 ($r \parallel s$) avec respect absolu de la règle du $s$ bas ($s \le \lfloor n/2 \rfloor$, `ERR_COSE_MALLEABLE_SIGNATURE`).
   - Pour Ed25519 : Format RFC 8032 ($R \parallel S$) avec vérification du scalaire canonique ($S < L$).

### 3.2 Budget de Taille (Contrainte Bloc 1 NFC & QR Code)

Le certificat de lot scellé a été expressément dimensionné pour tenir dans le budget strict d'un tag NFC Type 4 ou d'un QR code haute densité :
- En-tête Tag 18 : 1 octet (`0xd2`)
- Tableau de 4 éléments : 1 à 2 octets (`0x84` ou `0x84 58...`)
- En-tête protégé : 48 octets (`0x58 0x2e` + 46 octets)
- En-tête non protégé : 19 octets (`0xa1 0x04 0x50` + 16 octets de kid)
- Charge utile CBOR :
  - Sans dérogation (clés 1 à 5) : environ 95 à 105 octets.
  - Avec dérogation (clés 1 à 6) : environ 130 à 140 octets.
- Signature : 66 octets (`0x58 0x40` + 64 octets).
- **Taille totale de l'enveloppe COSE_Sign1** : **~235 à 275 octets**.

Cette compacité garantit que l'enveloppe peut être gravée dans le Bloc 1 d'une puce ou transportée via un canal radio bas-débit sans fragmentation.

---

## 4. Les 5 Points d'Arbitrage Normatifs

### 4.1 Point 1 : Architecture de `evaluateAndSign` et Séparation de l'Oracle

#### 4.1.1 Localisation et Confinement de la Clé Privée
Pour respecter le principe de sécurité de moindre privilège et neutraliser toute compromission de la clé de filière :
1. **Interdiction de Stockage en Espace Mémoire Applicatif** : La clé privée ne réside jamais sous forme en clair dans le tas JavaScript/TypeScript de l'application ou du serveur de traitement.
2. **Ancrage Matériel Obligatoire** :
   - **En environnement serveur / cloud de filière** : Module de sécurité matériel (HSM) certifié FIPS 140-3 Niveau 3, accessible exclusivement via interface scellée (PKCS#11 ou Cloud KMS dédié).
   - **Sur terminal mobile de contrôle d'abattoir / équarrissage** :
     - iOS : Apple Secure Enclave Processor (SEP) avec génération *in-silico* et contrôle d'accès biométrique.
     - Android : Android StrongBox KeyMint avec puce matérielle isolée (Titan M) et flag `isStrongBoxBacked(true)`.
   - **Sur automate de pesée / poste d'inspection fixe** : Carte à puce JavaCard ACOSJ 92k certifiée CC EAL5+ connectée via lecteur NFC sécurisé (ACR1552U) avec contrôle par code PIN opérateur.
3. **Clé Non-Exportable** : L'attribut de non-exportabilité (`extractable: false`) est formellement exigé lors de l'initialisation matérielle.

#### 4.1.2 Interface Formelle de Signature (`BatchSigner`)
Le moteur d'évaluation n'accède jamais directement à la cryptographie. Il dialogue avec le sous-système de signature via une abstraction unifiée :

```typescript
export interface BatchSigner {
  /** Algorithme cryptographique matériel : -7 (ES256) ou -8 (Ed25519) */
  readonly algorithm: -7 | -8;
  /** Identifiant SHA-256 tronqué à 16 octets de la clé publique de l'autorité */
  readonly kid: Uint8Array;
  /**
   * Appose la signature cryptographique sur la structure canonique Sig_structure (TBS).
   * La clé privée ne quitte jamais l'enclave sécurisée.
   *
   * @param tbs - Octets CBOR stricts de Sig_structure.
   * @returns Signature brute de 64 octets (IEEE P1363 pour ES256, RFC 8032 pour Ed25519).
   */
  sign(tbs: Uint8Array): Promise<Uint8Array>;
}
```

#### 4.1.3 Fonction d'Émission `evaluateAndSign`
La fonction d'émission constitue le goulet d'étranglement de sécurité :

```typescript
export async function evaluateAndSign(
  claimInput: BatchClaimInput,
  policyInput: PolicyInput | null,
  context: BatchIssuanceContext
): Promise<{ envelope: Uint8Array; claimJson: string }>
```

**Algorithme de Sécurité d'Émission** :
1. **Clonage et Gel Immuable** : La revendication d'entrée `claimInput` et la politique éventuelle `policyInput` sont clonées en profondeur via `structuredClone()` et récursivement gelées via `Object.freeze()` pour interdire toute modification concurrente en mémoire (anti-race condition).
2. **Canonisation JCS de la Revendication** : La revendication est sérialisée au format JSON canonique RFC 8785 :
   $$\text{claimJson} = \text{JCS}(\text{claimInput})$$
   $$\text{claimSha256} = \text{SHA-256}(\text{claimJson})$$
3. **Évaluation Sanitaire The Iron Gate** :
   $$\text{result} = \text{evaluate}(\text{claimInput}, \text{policyInput}, \text{context.taxonomyMap})$$
4. **Vérification Inviolable du Verdict** :
   - Si `result.verdict !== "AUTHORISED"` ou `result.signature_permitted !== true` :
     - La tentative d'émission est consignée de manière irréversible dans le journal d'audit append-only.
     - La fonction lève immédiatement une exception de sécurité `IronGateSecurityViolation` portant l'ensemble des motifs d'infraction `result.reasons`.
     - **La méthode `context.signer.sign()` n'est JAMAIS appelée.**
5. **Construction de la Charge Utile CBOR Déterministe** :
   - Assemblage des clés `1` à `5` (et de la clé `6` si et seulement si `policyInput` est non nul).
   - Sérialisation déterministe via `encode({ $map: entries })`.
6. **Scellage Cryptographique COSE_Sign1** :
   - Construction de l'en-tête protégé `{ 1: context.signer.algorithm, 16: "application/aeternitrak-batch-claim+cbor" }`.
   - Construction de `Sig_structure`.
   - Appel de `context.signer.sign(tbs)`.
   - Préfixage obligatoire par le Tag 18 `0xd2`.
7. **Restitution** : La fonction retourne l'enveloppe binaire signée scellée et la chaîne `claimJson` canonique associée.

---

### 4.2 Point 2 : Liaison de la Dérogation Souveraine DEC-AET-05 au Certificat

#### 4.2.1 Problématique Juridique et Sanitaire
La décision souveraine de Kudoro `DEC-AET-05` autorise, à titre exceptionnel et strictement encadré, la valorisation des animaux de compagnie (Catégorie 1, dépistage LFA Pentobarbital négatif, pasteurisation validée 70 °C / 1 h) pour l'amendement d'arbres du souvenir en forêts cinéraires privées (`memorial_forestry`).

Pour garantir qu'un certificat émis sous dérogation ne puisse jamais être détourné ou présenté comme un certificat standard de filière générale, la politique administrative accordant la dérogation doit être **intrinsèquement et indissociablement liée au certificat binaire**.

#### 4.2.2 Mécanisme de Liaison Cryptographique via la Clé `6`
1. **Canonisation de la Politique** :
   Le document de politique administrative `policy` (contenant `policy_id: "DEC-AET-05"`, `legal_basis`, et la référence de l'autorisation `authority_reference`) est canonisé selon la RFC 8785 :
   $$\text{policyJson} = \text{JCS}(\text{policy})$$
2. **Calcul de l'Empreinte** :
   $$\text{policySha256} = \text{SHA-256}(\text{policyJson})$$
3. **Injection dans la Clé `6`** :
   L'empreinte de 32 octets est injectée sous la clé entière `6` de la charge utile CBOR.
4. **Vérification de la Liaison** :
   Le vérificateur exige la fourniture du document de politique en regard du certificat. Il recalcule $\text{SHA-256}(\text{JCS}(\text{policy}))$ et vérifie la stricte identité octet par octet avec la clé `6`.
   Toute altération du texte de la dérogation ou substitution d'une autorisation invalide déclenche l'erreur `ERR_CERT_POLICY_HASH_MISMATCH`.

---

### 4.3 Point 3 : Registre des Erreurs `ERR_CERT_*` & Ordre de Contrôle Normatif

#### 4.3.1 Registre Normatif des Codes d'Erreur Typés

| Code d'Erreur | Étape de Rejet | Signification Formelle & Justification |
|---|:---:|---|
| `ERR_CERT_INVALID_ENVELOPE` | 1 | L'enveloppe COSE_Sign1 est invalide (tag 18 manquant, signature corrompue, format CBOR invalide, etc. - propage l'erreur sous-jacente `ERR_COSE_*`). |
| `ERR_CERT_INVALID_PAYLOAD` | 2 | La charge utile déballée n'est pas une carte CBOR déterministe valide, contient des données tronquées ou des octets résiduels. |
| `ERR_CERT_UNAUTHORIZED_PAYLOAD_KEY` | 3 | La carte de charge utile contient une clé non entière, inconnue ou interdite (ex. clés autres que 1 à 6). |
| `ERR_CERT_MISSING_MANDATORY_FIELD` | 3 | Un des champs obligatoires (clés 1, 2, 3, 4 ou 5) est absent de la charge utile. |
| `ERR_CERT_VERDICT_NOT_AUTHORISED` | 4 | La valeur de la clé `2` n'est pas la chaîne textuelle stricte `"AUTHORISED"`. |
| `ERR_CERT_INVALID_ISSUED_AT` | 5 | Le champ d'horodatage `issued_at` (clé `3`) n'est pas étiqueté avec le Tag 1 ou sa valeur est invalide/négative. |
| `ERR_CERT_CLAIM_HASH_MISMATCH` | 6 | L'empreinte SHA-256 de la revendication canonisée JCS ne correspond pas à la clé `1` scellée dans le certificat. |
| `ERR_CERT_UNKNOWN_TAXONOMY_SNAPSHOT` | 7 | L'empreinte taxonomique (clé `4`) ne correspond à aucun snapshot homologué dans le registre local du vérificateur. |
| `ERR_CERT_UNKNOWN_RULES_VERSION` | 8 | La version des règles (clé `5`) n'est pas reconnue ou supportée par le vérificateur. |
| `ERR_CERT_UNKNOWN_POLICY` | 9 | La politique requise (clé `6`) est introuvable dans le registre local des politiques homologuées. |
| `ERR_CERT_POLICY_HASH_MISMATCH` | 9 | L'empreinte SHA-256 de la politique fournie ne correspond pas à la valeur de la clé `6` scellée. |
| `ERR_CERT_DEROGATION_UNBOUND` | 9 | La revendication concerne une destination dérogatoire (ex. `memorial_forestry`) mais le certificat ne porte pas la clé `6`. |
| `ERR_CERT_UNEXPECTED_POLICY` | 9 | Le certificat porte une clé `6` alors que la revendication ne relève d'aucune dérogation reconnue. |
| `ERR_CERT_RE_EVALUATION_FAILED` | 10 | La ré-évaluation complète par The Iron Gate conclut à `BLOCKED` (infraction sanitaire détectée). |
| `ERR_CERT_KEY_USAGE_MISMATCH` | 11 | La clé publique de l'émetteur n'est pas autorisée pour les certificats de lot (`typ` mismatch dans le TrustStore). |
| `ERR_CERT_EXPIRED_KEY` | 12 | La clé de signature était expirée lors de l'émission du certificat (`issued_at` hors de `[valid_from, valid_until]`). |
| `ERR_CERT_REVOKED_KEY` | 12 | La clé de signature a été révoquée par l'autorité de sécurité sanitaire. |

#### 4.3.2 Ordre de Contrôle Normatif Séquentiel (12 Étapes)

Le vérificateur exécute obligatoirement les 12 étapes dans l'ordre séquentiel immuable ci-dessous, avec **arrêt immédiat dès la première défaillance détectée** (*Fail-Fast*) :

```
[Entrée : Enveloppe binaire COSE_Sign1, claimJson, options de vérification]
   │
   ▼
[Étape 1] Vérification de l'Enveloppe COSE_Sign1 ────────────────► Échec : ERR_CERT_INVALID_ENVELOPE (ou ERR_COSE_*)
   │      - Vérification du Tag 18 (0xd2), décodage strict, intégrité cryptographique
   │      - Typage d'en-tête (typ = "application/aeternitrak-batch-claim+cbor")
   │      - Signature mathématique Ed25519 ou ES256 (low-s)
   ▼
[Étape 2] Décodage Déterministe de la Charge Utile ──────────────► Échec : ERR_CERT_INVALID_PAYLOAD
   │      - Décodage strict du payload extrait (carte CBOR)
   ▼
[Étape 3] Typage Strict des Clés de Charge Utile ────────────────► Échec : ERR_CERT_UNAUTHORIZED_PAYLOAD_KEY /
   │      - Clés autorisées : {1..5} (standard) ou {1..6} (dérogatoire)      ERR_CERT_MISSING_MANDATORY_FIELD
   │      - Clés 1 à 5 présentes et strictement entières
   ▼
[Étape 4] Contrôle du Verdict Scellé (Clé 2) ────────────────────► Échec : ERR_CERT_VERDICT_NOT_AUTHORISED
   │      - payload[2] === "AUTHORISED"
   ▼
[Étape 5] Contrôle de la Date d'Émission (Clé 3) ────────────────► Échec : ERR_CERT_INVALID_ISSUED_AT
   │      - payload[3] porte le Tag CBOR 1 (#6.1) et un entier non négatif
   ▼
[Étape 6] Concordance Cryptographique de la Revendication (Clé 1)► Échec : ERR_CERT_CLAIM_HASH_MISMATCH
   │      - payload[1] === SHA-256(JCS(claimJson))
   ▼
[Étape 7] Résolution du Snapshot Taxonomique (Clé 4) ────────────► Échec : ERR_CERT_UNKNOWN_TAXONOMY_SNAPSHOT
   │      - payload[4] existe dans options.taxonomyRegistry
   ▼
[Étape 8] Résolution du Moteur de Règles Sanitaires (Clé 5) ─────► Échec : ERR_CERT_UNKNOWN_RULES_VERSION
   │      - payload[5] existe dans options.rulesEngines
   ▼
[Étape 9] Contrôle de Liaison Dérogatoire (Clé 6) ───────────────► Échec : ERR_CERT_DEROGATION_UNBOUND /
   │      - Si dérogation requise : clé 6 présente, politique résolue        ERR_CERT_UNEXPECTED_POLICY /
   │        et payload[6] === SHA-256(JCS(policy))                           ERR_CERT_POLICY_HASH_MISMATCH /
   │      - Si dérogation non requise : clé 6 absente                        ERR_CERT_UNKNOWN_POLICY
   ▼
[Étape 10] Ré-Évaluation Complète par The Iron Gate ─────────────► Échec : ERR_CERT_RE_EVALUATION_FAILED
   │       - evaluate(claim, policy, resolvedTaxonomy) === AUTHORISED
   ▼
[Étape 11] Autorisation d'Usage de la Clé Émettrice ─────────────► Échec : ERR_CERT_KEY_USAGE_MISMATCH
   │       - Entrée du TrustStore autorisée pour le typ certificat de lot
   ▼
[Étape 12] Contrôle Temporel de Validité Post-Signature (K2) ────► Échec : ERR_CERT_REVOKED_KEY /
   │       - Clé non révoquée dans le TrustStore                             ERR_CERT_EXPIRED_KEY
   │       - payload[3] (issued_at) ∈ [valid_from, valid_until]
   ▼
[SUCCÈS : Certificat Validé Plein Droit]
```

---

### 4.4 Point 4 : Gestion des Références Inconnues (Taxonomie & Versions de Règles)

#### 4.4.1 Principe de Fermeture Cognitive (Cognitive Closure)
La vérification d'un certificat sanitaire n'admet aucune heuristique d'approximation, aucune extrapolation taxonomique et aucune rétrogradation de version (*no fallback, no downgrade*) :

1. **Snapshot Taxonomique Inconnu (`ERR_CERT_UNKNOWN_TAXONOMY_SNAPSHOT`)** :
   - Si la clé `4` porte une empreinte $\text{SHA-256}$ qui ne figure pas dans le magasin local de snapshots certifiés du vérificateur, l'opération est **immédiatement rejetée**.
   - Le vérificateur n'a pas le droit d'utiliser un snapshot plus récent ou plus ancien en remplacement : l'évaluation doit reproduire fidèlement l'état exact de l'arbre phylogénétique au moment où le lot a été certifié.
2. **Version de Règles Inconnue (`ERR_CERT_UNKNOWN_RULES_VERSION`)** :
   - Si la clé `5` désigne une version de règles (ex. `"1.5.0"`) pour laquelle le vérificateur ne possède pas le moteur d'évaluation correspondant dans sa table `rulesEngines`, l'opération est **immédiatement rejetée**.
   - Toute exécution avec un moteur de règles d'une version différente est formellement interdite : cela constituerait une faille critique de substitution de logique réglementaire.

#### 4.4.2 Protection Contre les Attaques par Rétrogradation (Anti-Downgrade)
Un attaquant ne peut pas forger un certificat en déclarant une version ancienne des règles qui comporterait une vulnérabilité corrigée ultérieurement :
- Le vérificateur maintient une liste de versions de règles acceptables (`minimum_rules_version`).
- Toute version révoquée ou dépréciée par l'autorité sanitaire déclenche `ERR_CERT_UNKNOWN_RULES_VERSION`.

---

### 4.5 Point 5 : Limites Probatoires du Certificat (Périmètre de Garantie)

Pour prévenir tout risque juridique de mauvaise interprétation de la garantie apportée par la technologie AeterniTrak, la présente spécification définit avec une rigueur absolue la frontière entre la preuve mathématique et la réalité physique du monde réel.

#### 4.5.1 Ce que le Certificat PROUVE Formellement
Le Certificat de Conformité Sanitaire apporte la **preuve cryptographique irréfutable, vérifiable hors-ligne et opposable en justice** des faits suivants :
1. **Intégrité Logique & Sanitaire Absolue** : L'ensemble des données déclarées dans la revendication $\text{claim}$ satisfait sans exception la totalité des listes blanches positives des portes G0 à G9 de The Iron Gate, selon les règles de la version déclarée et la taxonomie certifiée.
2. **Non-Répudiation de l'Autorité d'Émission** : Le certificat a été scellé par une entité légitime, identifiée par son `kid`, détentrice d'une clé privée active répertoriée dans le Trust Store officiel au moment de l'émission.
3. **Immutabilité de la Déclaration** : Pas un seul bit de la revendication $\text{claim}$ n'a été altéré ou falsifié depuis l'instant de scellage ($\text{issued\_at}$).
4. **Validité Temporelle Historique** : Le certificat a été émis pendant la période de qualification opérationnelle certifiée de la clé émettrice.

#### 4.5.2 Ce que le Certificat NE PROUVE PAS (Non-Garanti)
Le certificat **NE PEUT EN AUCUN CAS PROUVER NI GARANTIR** :
1. **La Véracité Physique des Déclarations à la Source (Fraude Matérielle)** :
   - Si un opérateur malveillant introduit clandestinement des carcasses bovines (Cat. 1 MRS) dans un broyeur tout en déclarant informatiquement des co-produits de volailles saines (Cat. 3) avec des numéros de boucle falsifiés, le certificat sera mathématiquement valide sur la base des déclarations transmises.
   - **La cryptographie valide la cohérence des faits déclarés, elle ne valide pas la matière physique non instrumentée.**
2. **L'Absence de Contamination Croisée en Ligne de Production** :
   - Le certificat scelle un lot théorique. Il ne garantit pas qu'une ligne de convoyage industrielle n'a pas été souillée par des résidus d'un lot précédent si les protocoles de nettoyage d'usine n'ont pas été physiquement respectés.
3. **L'Authenticité Métrologique des Sondes Physiques** :
   - Le certificat enregistre l'empreinte `evidence_sha256` du journal de sonde de température/pression (Méthode 1 ou pasteurisation). Il garantit que le journal n'a pas été altéré après coup, mais ne garantit pas que les capteurs thermiques étaient correctement étalonnés ou qu'ils n'ont pas été trompés par une source de chaleur artificielle externe.
4. **La Conservation et l'Intégrité Post-Scellage** :
   - Le certificat ne garantit pas les conditions de transport ultérieures (rupture de la chaîne du froid, moisissures, contamination biologique après ouverture du conditionnement scellé).

> [!CAUTION]
> **Avertissement Juridique Institutionnel** :  
> Le certificat AeterniTrak constitue un instrument de preuve de conformité algorithmique. Il vient en appui des contrôles officiels de l'AFSCA, du DNF et des services vétérinaires d'État, mais **ne se substitue en aucun cas aux inspections physiques sur site, aux prélèvements histologiques et aux audits réguliers de biosécurité des installations**.

---

## 5. Matrice de Conformité & Critères d'Acceptation (Phase A)

Conformément à l'Ordre 0047 de Claude AI :

- **Phase A Exclusive** : Le présent document constitue une spécification formelle pure. Aucun code source d'implémentation n'a été ajouté dans `core/` et aucun vecteur approuvé n'a été inséré dans `qa/vectors/`.
- **Alignement Inter-Bushi Parfait** : Harmonisation intégrale avec `AET-SPEC-CRYPTO-001` v1.1.1 (Bushi 02), `AET-SPEC-PRION-001` v1.4.0 (Bushi 12) et `AET-SPEC-CORE-001` (Bushi 01).
- **Prochaine Étape (Phase B)** : Dépôt par Claude AI de la suite de vecteurs normatifs de certificat de lot (`qa/vectors/crypto/batch-certificate.vectors.json`), puis implémentation conjointe Bushi 02 / Bushi 12.
