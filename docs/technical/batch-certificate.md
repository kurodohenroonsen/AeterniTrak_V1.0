# Spécification Technique & Formelle — Certificat de Conformité Sanitaire de Lot (Batch Claim Certificate)

> **Document ID** : `AET-SPEC-CERT-001`  
> **Version** : 1.1.0  
> **Statut** : Soumis pour révision (v1.1.0 intégrant les amendements A1 à A10 du Redirect 0053)  
> **Date de référence** : 2026-10-04  
> **Branche Git** : `ag/bushi-02-batch-certificate-spec`  
> **Auteur** : Bushi 02 (Security & Cryptography Lead, en concertation avec Bushi 12)  
> **Revue & Arbitrage** : Claude AI (Master Verifier) — Redirect 0053  
> **Autorité Souveraine** : Kudoro (`DECISIONS-KUDORO.md`, décisions `DEC-AET-04`, `DEC-AET-05`, `DEC-AET-07`, `DEC-AET-08`, `DEC-AET-09`)  
> **Contrats Partagés** : Bushi 12 (Anti-Prion & The Iron Gate), Bushi 01 (AeterniCore Déterminisme CBOR & Canonisation JCS), Bushi 16 (QA Testvectors & Harnais)  
> **Phase du Chantier** : Phase A — Spécification Formelle Pure (Zéro code d'implémentation dans `core/`, zéro vecteur de test approuvé)

---

## 1. Cadre Architectural & Objet de la Spécification

Le présent document formalise l'architecture, la structure binaire, les règles d'évaluation, le protocole d'émission et l'ordre normatif de vérification du **Certificat de Conformité Sanitaire de Lot** (*Batch Claim Certificate*).

Ce certificat constitue la clé de voûte de la filière de traçabilité AeterniTrak. Il réalise la composition sécurisée entre deux sous-systèmes préalablement validés et scellés :
1. **The Iron Gate (Bushi 12 / `AET-SPEC-PRION-001`)** : Le moteur algorithmique déterministe appliquant le principe du *Default-Deny* et les 10 portes de contrôle sanitaire G0 à G9 relatives aux encéphalopathies spongiformes transmissibles (EST / prions), au feed-ban européen (Règlements CE 999/2001, UE 2021/1372, CE 1069/2009, UE 142/2011) et à l'interdiction absolue de recyclage intra-espèce.
2. **Le Moteur Cryptographique COSE_Sign1 (Bushi 02 / `AET-SPEC-CRYPTO-001`)** : L'infrastructure de signature numérique universelle, agnostique et portable, assurant l'agilité cryptographique (Ed25519 `alg: -8` et NIST P-256 ES256 `alg: -7`), le déterminisme d'encodage CBOR (RFC 8949 §4.2.1), la séparation stricte de domaine (`typ`) et le modèle de confiance hors-ligne (*Offline-First Trust Store*).

### 1.1 Principes Fondamentaux Arrêtés

Conformément à l'Ordre 0047, aux arbitrages de Kudoro et aux directives du Redirect 0053 :

1. **Aucun Certificat pour une Revendication Rejetée** : L'oracle d'émission évalue la revendication via The Iron Gate. Si le verdict n'est pas strictement `AUTHORISED` ou si la condition `signature_permitted` est fausse, l'émission est formellement bloquée. Aucun certificat de rejet ou certificat conditionnel n'est jamais signé. Les motifs de refus `reasons` sont réservés au journal d'audit append-only et à l'accord d'investigation entre implémentations : ils ne figurent jamais dans le certificat signé.
2. **Double Validation Indépendante (Zéro Confiance Aveugle en la Signature)** : Le vérificateur ne se contente pas de valider la signature mathématique de l'enveloppe : il reconstruit et réévalue obligatoirement la revendication sanitaire originale à l'aide du snapshot taxonomique officiel et de la version des règles formellement scellés dans le certificat.
3. **Architecture Anti-Flottants (A3)** : Pour préserver le déterminisme absolu du décodage CBOR (qui proscrit les flottants de type major 7), la revendication originale complète voyage sous forme de chaîne JSON canonique JCS (RFC 8785). La charge utile CBOR signée ne contient que l'empreinte SHA-256 de cette chaîne canonique.
4. **Imperméabilité Temporelle Post-Signature (Règle K2)** : La validité d'une clé de signature est comparée à la date d'émission portée par la charge utile certifiée (clé `3`), jamais à la date locale de lecture sur le terminal de contrôle.
5. **Séparation de Domaine Hermétique** : L'enveloppe porte impérativement le paramètre d'en-tête protégé `typ = "application/aeternitrak-batch-claim+cbor"`. Une clé de conformité de lot ne peut en aucun cas signer un profil mémoriel, et un profil mémoriel ne peut en aucun cas être substitué à un certificat de lot (`ERR_COSE_KEY_USAGE_MISMATCH`, `ERR_COSE_TYPE_MISMATCH`).
6. **Exclusion Formelle de `cose-open` (A2)** : Un certificat sanitaire de lot ne passe **JAMAIS** par la procédure `cose-open` ni par le concept d'état « sous réserve » (`UNVERIFIED`). Un émetteur inconnu (`kid` absent du Trust Store du vérificateur) bloque irrémédiablement avec l'erreur `ERR_COSE_UNKNOWN_KID`. L'intégrité de la filière sanitaire exclut toute tolérance à l'affichage ou au traitement de données non authentifiées.

---

## 2. Spécification Binaire de la Charge Utile (Payload CBOR Déterministe)

La charge utile du certificat de lot est une carte CBOR déterministe (RFC 8949 §4.2.1) encodée selon les règles strictes d'AeterniCore. Toutes les clés sont **strictement des entiers non signés (Major Type 0)**, triées par ordre lexicographique bytewise croissant.

### 2.1 Structure des Clés Entières de la Charge Utile

| Clé (Int) | Nom Sémantique | Type CBOR | Taille / Format | Statut | Description Normative |
|:---:|---|---|---|:---:|---|
| **`1`** | `claim_sha256` | Byte String (`bstr`, Major 2) | Exactement 32 octets | **Obligatoire** | Empreinte SHA-256 des octets UTF-8 de la chaîne JSON canonique JCS de la revendication : $\text{SHA-256}(\text{UTF-8}(\text{JCS}(\text{claim})))$. |
| **`2`** | `verdict` | Text String (`tstr`, Major 3) | Chaîne UTF-8 | **Obligatoire** | Chaîne littérale `"AUTHORISED"` exclusivement. Toute autre valeur rend le certificat invalide. |
| **`3`** | `issued_at` | Semantic Tag 1 (`#6.1`, Major 6) | Entier non négatif (Major 0) | **Obligatoire** | Date et heure de scellage du certificat, en secondes écoulées depuis l'epoch UNIX (1970-01-01T00:00:00Z UTC). |
| **`4`** | `snapshot_sha256` | Byte String (`bstr`, Major 2) | Exactement 32 octets | **Obligatoire** | Empreinte SHA-256 du snapshot taxonomique officiel (RFC 8785 JCS) employé lors de l'évaluation sanitaire : $\text{SHA-256}(\text{UTF-8}(\text{JCS}(\text{taxonomy-snapshot})))$. |
| **`5`** | `rules_version` | Text String (`tstr`, Major 3) | Chaîne UTF-8 SemVer | **Obligatoire** | Version de la spécification normative des règles sanitaires de la Porte de Fer (ex. `"1.5.0"`). |
| **`6`** | `policy_sha256` | Byte String (`bstr`, Major 2) | Exactement 32 octets | **Conditionnel** | Empreinte SHA-256 de la politique dérogatoire officielle résolue dans le registre : $\text{SHA-256}(\text{UTF-8}(\text{JCS}(\text{policy})))$. Présente **si et seulement si** `destination.use = "memorial_forestry"`. |

### 2.2 Règle d'Unicité Absolue de la Clé `6` (A4)

La règle de présence ou d'absence de la clé `6` est **strictement symétrique et identique à l'émission et à la vérification** :

1. **Règle Unique** :
   - La clé `6` est **STRICTEMENT PRÉSENTE** si et seulement si `destination.use = "memorial_forestry"`.
2. **Lot Standard (Sans Dérogation)** :
   - Pour toute destination standard (`feed`, `aquaculture_feed`, `technical`, `fertiliser`, `incineration`), la clé `6` **DOIT ÊTRE STRICTEMENT ABSENTE** de la carte CBOR.
   - La présence d'une clé `6` sur un lot standard constitue une violation de structure et déclenche le rejet immédiat avec `ERR_CERT_UNEXPECTED_POLICY`.
3. **Lot sous Dérogation Mémorielle (DEC-AET-05)** :
   - Pour la destination `memorial_forestry`, la clé `6` **DOIT ÊTRE STRICTEMENT PRÉSENTE** et contenir exactement les 32 octets de l'empreinte de la politique officielle homologuée.
   - L'absence de la clé `6` pour un lot dont la destination est `memorial_forestry` déclenche le rejet immédiat avec `ERR_CERT_DEROGATION_UNBOUND`.

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
  1: bstr .size 32, ; claim_sha256 = SHA-256(UTF-8(JCS(claim)))
  2: "AUTHORISED",  ; verdict textuel scellé
  3: #6.1(uint),    ; issued_at: epoch secondes UTC
  4: bstr .size 32, ; snapshot_sha256 = SHA-256(UTF-8(JCS(taxonomy_snapshot)))
  5: tstr,          ; rules_version (ex: "1.5.0")
  ? 6: bstr .size 32 ; policy_sha256: présent ssi destination.use == "memorial_forestry"
}
```

---

## 3. Spécification de l'Enveloppe COSE_Sign1 & Budget de Taille

### 3.1 Structure de l'Enveloppe Scellée

1. **Tag CBOR 18 Obligatoire (`0xd2`)** :
   - Conformément au RFC 9052 §4.2 et à `AET-SPEC-CRYPTO-001` (Règle K4), le premier octet de l'enveloppe sérialisée est obligatoirement `0xd2`. Toute omission ou utilisation d'un autre tag est rejetée par `cose-verify` avec `ERR_COSE_INVALID_ENVELOPE`.
2. **En-tête Protégé (`protected`)** :
   - Encodé de manière canonique sous la forme d'une carte CBOR sérialisée en chaîne d'octets (`bstr`).
   - Clés entières strictes triées par ordre lexicographique :
     - `1` (`alg`) : `-8` (Ed25519) ou `-7` (ES256).
     - `16` (`typ`) : `"application/aeternitrak-batch-claim+cbor"`.
   - Octets canoniques exacts (46 octets de carte sérialisée) :
     - Pour Ed25519 (`alg: -8`) : `a201271078286170706c69636174696f6e2f61657465726e697472616b2d62617463682d636c61696d2b63626f72`
     - Pour ES256 (`alg: -7`) : `a201261078286170706c69636174696f6e2f61657465726e697472616b2d62617463682d636c61696d2b63626f72`
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
   - Pour ES256 : Format IEEE P1363 ($r \parallel s$) avec respect absolu de la règle du $s$ bas ($s \le \lfloor n/2 \rfloor$, rejet `ERR_COSE_MALLEABLE_SIGNATURE`).
   - Pour Ed25519 : Format RFC 8032 ($R \parallel S$) avec vérification du scalaire canonique ($S < L$).

### 3.2 Budget de Taille Recalculé (Contrainte Bloc 1 NFC & QR Code)

Le certificat de lot scellé a été dimensionné avec précision pour tenir dans le budget matériel strict d'un tag NFC Type 4 ou d'un QR code haute densité :
- **En-tête Tag 18** : 1 octet (`0xd2`)
- **Tableau de 4 éléments** : 1 octet (`0x84`)
- **En-tête protégé** : 48 octets (`0x58 0x2e` + 46 octets d'en-tête canonique)
- **En-tête non protégé** : 19 octets (`0xa1 0x04 0x50` + 16 octets de `kid`)
- **Charge utile CBOR** :
  - *Sans dérogation* (clés 1 à 5) : 99 octets de payload brut + 2 octets d'encapsulation `bstr` (`0x58 0x63`) = **101 octets**.
  - *Avec dérogation* (clés 1 à 6) : 134 octets de payload brut + 2 octets d'encapsulation `bstr` (`0x58 0x86`) = **136 octets**.
- **Signature cryptographique** : 66 octets (`0x58 0x40` + 64 octets de signature).

**Budget Total Recalculé de l'Enveloppe COSE_Sign1 Scellée** :
- **234 octets sans dérogation**
- **269 octets avec dérogation**

Cette compacité garantit que l'enveloppe complète peut être gravée directement dans le Bloc 1 d'une puce NFC ou transmise via un protocole radio bas-débit sans aucune fragmentation réseau.

---

## 4. Les Points d'Arbitrage Normatifs

### 4.1 Point 1 : Architecture de `evaluateAndSign` et Séparation de l'Oracle

#### 4.1.1 Confinement et Ancrage Matériel de la Clé Privée (A10)
Pour respecter le principe de sécurité de moindre privilège et neutraliser le risque d'exfiltration de la clé de filière :
1. **Interdiction de Stockage en Espace Mémoire Applicatif** : La clé privée ne réside jamais sous forme en clair dans le tas mémoire JavaScript/TypeScript de l'application ou du serveur de traitement.
2. **Ancrage Matériel Obligatoire** :
   - **En environnement serveur / cloud de filière** : Utilisation d'un module de sécurité matériel (HSM) ou d'un service de gestion de clés (KMS) dédié avec protection matérielle des clés privées, accessible exclusivement par interface d'API cryptographique scellée.
   - **Sur terminal mobile de contrôle d'abattoir / équarrissage** : Utilisation de l'enclave sécurisée matérielle du terminal (Secure Enclave sous iOS, Hardware Keymaster / StrongBox sous Android) avec génération *in-silico* et contrôle d'accès sécurisé.
   - **Sur automate de pesée / poste d'inspection fixe** : Utilisation d'un élément sécurisé physique (Secure Element / carte à puce) connecté via lecteur sécurisé avec contrôle d'accès opérateur (code PIN ou défi d'authentification mutuelle).
3. **Clé Non-Exportable** : L'attribut de non-exportabilité (`extractable: false`) est formellement exigé lors de la génération de la paire de clés.
4. **Neutralité Normative** : La présente spécification technique s'abstient de certifier des composants commerciaux spécifiques (les qualifications matérielles de type CC EAL ou FIPS relèvent des dossiers de conformité industrielle et du profil de déploiement des intégrateurs, non de cette spécification de protocole).

#### 4.1.2 Interface Formelle de Signature (`BatchSigner`)
Le moteur d'évaluation n'accède jamais directement au matériel cryptographique. Il dialogue avec le sous-système de signature via une abstraction unifiée :

```typescript
export interface BatchSigner {
  /** Algorithme cryptographique matériel : -7 (ES256) ou -8 (Ed25519) */
  readonly algorithm: -7 | -8;
  /** Identifiant SHA-256 tronqué à 16 octets de la clé publique de l'autorité */
  readonly kid: Uint8Array;
  /**
   * Appose la signature cryptographique sur la structure canonique Sig_structure (TBS).
   * La clé privée ne quitte jamais l'enclave matérielle sécurisée.
   *
   * @param tbs - Octets CBOR stricts de Sig_structure.
   * @returns Signature brute de 64 octets (IEEE P1363 pour ES256, RFC 8032 pour Ed25519).
   */
  sign(tbs: Uint8Array): Promise<Uint8Array>;
}
```

#### 4.1.3 Fonction d'Émission `evaluateAndSign` (A3, A4, A5)
La fonction d'émission constitue le point d'étranglement de sécurité de l'autorité sanitaire :

```typescript
export async function evaluateAndSign(
  claimInput: unknown,
  policyInput: unknown | null,
  context: BatchIssuanceContext
): Promise<{ envelope: Uint8Array; claimJson: string }>
```

**Algorithme de Sécurité d'Émission** :
1. **Canonisation et Découplage de la Revendication (A5)** :
   Pour fermer tout risque d'écart d'interprétation entre la matière évaluée et la matière hachée (neutralisation des accesseurs dynamiques, accesseurs `toJSON`, valeurs `undefined` ignorées par JCS, mutations concurrentes en mémoire) :
   $$\text{claimJson} = \text{JCS}(\text{claimInput})$$
   $$\text{claimSha256} = \text{SHA-256}(\text{UTF-8}(\text{claimJson}))$$
   $$\text{claimEvaluated} = \text{JSON.parse}(\text{claimJson})$$
   L'évaluation sanitaire porte obligatoirement sur l'objet obtenu par `JSON.parse(claimJson)`, garantissant une identité sémantique et syntaxique absolue avec le flux scellé.
2. **Authentification de la Politique Dérogatoire (A3, A4)** :
   - Règle A4 : La dérogation s'applique **si et seulement si** `claimEvaluated.destination?.use === "memorial_forestry"`.
   - Si `destination.use === "memorial_forestry"` :
     - `policyInput` est obligatoire.
     - L'autorité d'émission valide impérativement que `policyInput` provient du **registre signé de politiques officielles** de l'autorité (authentifié selon le même modèle cryptographique que le Trust Store des clés).
     - $\text{policyJson} = \text{JCS}(\text{policyInput})$
     - $\text{policySha256} = \text{SHA-256}(\text{UTF-8}(\text{policyJson}))$
     - $\text{policyEvaluated} = \text{JSON.parse}(\text{policyJson})$
   - Si `destination.use !== "memorial_forestry"` :
     - `policyInput` doit être nul. Si une politique est fournie alors que la destination est standard, l'émission est refusée. Aucune clé `6` ne sera injectée.
     - $\text{policyEvaluated} = \text{null}$
3. **Évaluation Sanitaire par The Iron Gate** :
   $$\text{result} = \text{evaluate}(\text{claimEvaluated}, \text{policyEvaluated})$$
4. **Vérification Inviolable du Verdict** :
   - Si `result.verdict !== "AUTHORISED"` ou `result.signature_permitted !== true` :
     - La tentative d'émission est consignée de manière irréversible dans le journal d'audit append-only des refus (avec l'ensemble des motifs d'infraction `result.reasons`).
     - La fonction lève immédiatement une exception de sécurité `IronGateSecurityViolation`.
     - **La méthode `context.signer.sign()` n'est JAMAIS appelée.**
     - Aucun certificat n'est généré (les motifs `reasons` n'entrent jamais dans un certificat de lot).
5. **Construction de la Charge Utile CBOR Déterministe (A4)** :
   - Assemblage des clés `1` à `5` selon le tableau §2.1.
   - Si et seulement si `claimEvaluated.destination.use === "memorial_forestry"` : ajout de la clé `6` contenant `policySha256` (32 octets).
   - Sérialisation déterministe canonique CBOR via `encode({ $map: entries })`.
6. **Scellage Cryptographique COSE_Sign1** :
   - Construction de l'en-tête protégé : `{ 1: context.signer.algorithm, 16: "application/aeternitrak-batch-claim+cbor" }`.
   - Construction de `Sig_structure` conforme au RFC 9052 §4.4.
   - Appel à l'enclave sécurisée : `signature = await context.signer.sign(tbs)`.
   - Assemblage du tableau COSE_Sign1 à 4 éléments préfixé obligatoirement par le Tag 18 (`0xd2`).
7. **Restitution** : La fonction retourne le certificat binaire scellé `envelope` et la chaîne JSON canonique `claimJson`.

---

### 4.2 Point 2 : Modèle de Dérogation DEC-AET-05 et Registre Authentifié de Politiques (A3, A4)

#### 4.2.1 Problématique Sanitaire et Décision Souveraine DEC-AET-05
La décision souveraine de Kudoro `DEC-AET-05` autorise, à titre exceptionnel et strictement encadré, la valorisation des animaux de compagnie (Catégorie 1, dépistage LFA Pentobarbital négatif, pasteurisation validée 70 °C / 1 h) pour l'amendement d'arbres du souvenir en forêts cinéraires privées (`memorial_forestry`).

Pour garantir qu'un certificat émis sous dérogation ne puisse jamais être détourné ou présenté comme un certificat standard de filière générale, la politique administrative accordant la dérogation est **intrinsèquement liée au certificat binaire**.

#### 4.2.2 Origine et Authentification de la Politique (A3)
1. **Interdiction de Politique Fournie par le Présentateur** :
   Le porteur ou présentateur d'un certificat ne fournit **jamais** le document de politique au vérificateur. Comme The Iron Gate ne contrôle d'une politique que trois champs non vides (`policy_id`, `legal_basis`, `authority_reference`), accepter un document transmis par le présentateur permettrait à un fraudeur de forger une fausse politique auto-validante.
2. **Résolution dans le Registre Local du Vérificateur** :
   La clé `6` porte l'empreinte de 32 octets $\text{policy\_sha256}$. Le vérificateur résout cette empreinte exclusivement dans son propre **registre local authentifié de politiques**, pré-chargé et signé par l'autorité sanitaire de tutelle.
   - Si l'empreinte de la clé `6` est absente du registre local du vérificateur : échec immédiat avec `ERR_CERT_UNKNOWN_POLICY`.
   - L'ancien code `ERR_CERT_POLICY_HASH_MISMATCH` devient sans objet et est supprimé de la nomenclature.
3. **Symétrie Côté Émission** :
   L'oracle d'émission valide de la même manière que toute politique passée en entrée provient de son registre officiel signé avant de procéder au calcul de l'empreinte et à l'évaluation.

---

### 4.3 Point 3 : Registre des Erreurs & Ordre de Contrôle Normatif Séquentiel

#### 4.3.1 Élimination des Doublons de Codes (A1)
La convention d'architecture d'AeterniTrak stipule qu'une anomalie remonte obligatoirement avec son **code d'origine**. En conséquence, les anciens codes `ERR_CERT_INVALID_ENVELOPE`, `ERR_CERT_INVALID_PAYLOAD`, `ERR_CERT_KEY_USAGE_MISMATCH`, `ERR_CERT_EXPIRED_KEY` et `ERR_CERT_REVOKED_KEY` sont **définitivement supprimés** de la spécification :
- Toute anomalie de structure COSE, de signature, d'algorithme, de type MIME ou de validité de clé remonte avec son code `ERR_COSE_*` (ex: `ERR_COSE_INVALID_ENVELOPE`, `ERR_COSE_INVALID_SIGNATURE`, `ERR_COSE_UNKNOWN_KID`, `ERR_COSE_REVOKED_KEY`, `ERR_COSE_KEY_USAGE_MISMATCH`, `ERR_COSE_EXPIRED_KEY`).
- Toute anomalie de décodage CBOR de la charge utile remonte avec son code `ERR_CBOR_*`.

#### 4.3.2 Registre Normatif des Codes d'Erreur `ERR_CERT_*`

| Code d'Erreur | Étape | Signification Formelle & Justification |
|---|:---:|---|
| `ERR_CERT_UNAUTHORIZED_PAYLOAD_KEY` | 3 | La carte de charge utile contient une clé non entière (ex. texte) ou un entier hors de l'ensemble autorisé $\{1..6\}$. |
| `ERR_CERT_MISSING_MANDATORY_FIELD` | 3 | Un des champs obligatoires (clés 1, 2, 3, 4 ou 5) est absent de la charge utile. |
| `ERR_CERT_INVALID_FIELD` | 3 | Typage incorrect d'un champ : clé 1, 4 ou 6 qui n'est pas un `bstr` de 32 octets, ou clé 5 qui n'est pas un `tstr`. |
| `ERR_CERT_VERDICT_NOT_AUTHORISED` | 4 | La valeur de la clé `2` n'est pas la chaîne textuelle stricte `"AUTHORISED"`. |
| `ERR_CERT_INVALID_ISSUED_AT` | 5 | Le champ `issued_at` (clé `3`) ne porte pas le Tag 1 (`#6.1`) ou sa valeur n'est pas un entier non négatif. |
| `ERR_CERT_CLAIM_NOT_CANONICAL` | 6 | La chaîne `claimJson` reçue n'est pas strictement canonique JCS : $\text{JCS}(\text{JSON.parse}(\text{claimJson})) \neq \text{claimJson}$. |
| `ERR_CERT_CLAIM_HASH_MISMATCH` | 6 | L'empreinte $\text{SHA-256}(\text{UTF-8}(\text{claimJson}))$ ne correspond pas à la valeur de la clé `1` scellée. |
| `ERR_CERT_UNKNOWN_TAXONOMY_SNAPSHOT` | 7 | L'empreinte taxonomique (clé `4`) ne correspond à aucun snapshot dans le registre local du vérificateur. |
| `ERR_CERT_UNKNOWN_RULES_VERSION` | 8 | La version des règles (clé `5`) n'existe pas dans le registre de moteurs de règles du vérificateur. |
| `ERR_CERT_RULES_VERSION_RETIRED` | 8 | La version des règles (clé `5`) est répertoriée comme dépréciée ou révoquée par l'autorité sanitaire. |
| `ERR_CERT_UNEXPECTED_POLICY` | 9 | Le certificat porte une clé `6` alors que la revendication n'a pas pour destination `memorial_forestry`. |
| `ERR_CERT_DEROGATION_UNBOUND` | 9 | La revendication concerne `memorial_forestry` mais le certificat ne porte pas la clé `6`. |
| `ERR_CERT_UNKNOWN_POLICY` | 9 | L'empreinte de politique (clé `6`) est introuvable dans le registre local authentifié de politiques. |
| `ERR_CERT_RE_EVALUATION_FAILED` | 10 | La ré-évaluation complète par The Iron Gate conclut à `BLOCKED` (infraction sanitaire détectée). |

#### 4.3.3 Ordre de Contrôle Normatif Séquentiel (10 Étapes Inviolables)

Le vérificateur exécute obligatoirement les 10 étapes ci-dessous dans l'ordre séquentiel immuable, avec **arrêt immédiat dès la première défaillance détectée** (*Fail-Fast*) :

```
[Entrée : Enveloppe binaire COSE_Sign1, claimJson (chaîne brute), options de vérification]
   │
   ▼
[Étape 1] Validation Intégrale de l'Enveloppe COSE_Sign1 ────────► Échec : ERR_COSE_* (13 étapes K1-K2)
   │      - Appel strict à coseVerify(envelope, trustStore, { expectedType: "application/aeternitrak-batch-claim+cbor" })
   │      - Décodage Tag 18 (0xd2), 4 éléments, en-têtes canoniques, kid 16 octets
   │      - Émetteur inconnu : BLOQUE avec ERR_COSE_UNKNOWN_KID (JAMAIS de cose-open)
   │      - Clé révoquée : ERR_COSE_REVOKED_KEY
   │      - Usage de clé : ERR_COSE_KEY_USAGE_MISMATCH
   │      - Signature mathématique Ed25519 ou ES256 (low-s) : ERR_COSE_INVALID_SIGNATURE / MALLEABLE
   │      - Fenêtre temporelle K2 : issued_at ∈ [valid_from, valid_until] : ERR_COSE_EXPIRED_KEY
   │      - Restitue les octets déballés de la charge utile (payloadBytes)
   ▼
[Étape 2] Décodage Déterministe de la Charge Utile CBOR ──────────► Échec : ERR_CBOR_*
   │      - Décodage strict du payloadBytes en carte CBOR
   ▼
[Étape 3] Contrôle Ordonné de Structure et de Typage (Clés & Valeurs)
   │      1. Type des clés : chaque clé est obligatoirement un uint (Major 0) ──► ERR_CERT_UNAUTHORIZED_PAYLOAD_KEY
   │      2. Clés autorisées : aucune clé hors de {1, 2, 3, 4, 5, 6} ──────────► ERR_CERT_UNAUTHORIZED_PAYLOAD_KEY
   │      3. Clés obligatoires : présence impérative de 1, 2, 3, 4 et 5 ────────► ERR_CERT_MISSING_MANDATORY_FIELD
   │      4. Typage des valeurs :
   │         - payload[1] est bstr de 32 octets ───────────────────────────────► ERR_CERT_INVALID_FIELD
   │         - payload[4] est bstr de 32 octets ───────────────────────────────► ERR_CERT_INVALID_FIELD
   │         - payload[5] est une chaîne de texte (tstr) ──────────────────────► ERR_CERT_INVALID_FIELD
   │         - payload[6] (si présente) est bstr de 32 octets ────────────────► ERR_CERT_INVALID_FIELD
   ▼
[Étape 4] Contrôle du Verdict Scellé (Clé 2) ────────────────────► Échec : ERR_CERT_VERDICT_NOT_AUTHORISED
   │      - payload[2] === "AUTHORISED"
   ▼
[Étape 5] Contrôle de la Date d'Émission (Clé 3) ────────────────► Échec : ERR_CERT_INVALID_ISSUED_AT
   │      - payload[3] porte le Tag CBOR 1 (#6.1) et est un entier non négatif
   ▼
[Étape 6] Contrôle de Canonicalité & Concordance de la Revendication (Clé 1)
   │      1. Vérification de canonicalité JCS :
   │         JCS(JSON.parse(claimJson)) === claimJson ────────────────────────► Échec : ERR_CERT_CLAIM_NOT_CANONICAL
   │      2. Concordance cryptographique du hachage :
   │         SHA-256(UTF-8(claimJson)) === payload[1] ────────────────────────► Échec : ERR_CERT_CLAIM_HASH_MISMATCH
   ▼
[Étape 7] Résolution du Snapshot Taxonomique (Clé 4) ────────────► Échec : ERR_CERT_UNKNOWN_TAXONOMY_SNAPSHOT
   │      - payload[4] est résolu dans options.taxonomyRegistry
   ▼
[Étape 8] Résolution et Qualification du Moteur de Règles (Clé 5)
   │      1. payload[5] existe dans options.rulesEngines ──────────────────────► Échec : ERR_CERT_UNKNOWN_RULES_VERSION
   │      2. payload[5] n'est pas dans options.retiredRulesVersions ───────────► Échec : ERR_CERT_RULES_VERSION_RETIRED
   ▼
[Étape 9] Contrôle Ordonné de Liaison Dérogatoire (Clé 6)
   │      1. Si destination.use !== "memorial_forestry" et clé 6 présente ─────► Échec : ERR_CERT_UNEXPECTED_POLICY
   │      2. Si destination.use === "memorial_forestry" et clé 6 absente ──────► Échec : ERR_CERT_DEROGATION_UNBOUND
   │      3. Si destination.use === "memorial_forestry" et clé 6 présente :
   │         payload[6] résolu dans options.policyRegistry ────────────────────► Échec : ERR_CERT_UNKNOWN_POLICY
   ▼
[Étape 10] Ré-Évaluation Complète Indépendante par The Iron Gate ─► Échec : ERR_CERT_RE_EVALUATION_FAILED
   │       - evaluate(claimParsed, resolvedPolicy) === AUTHORISED
   ▼
[SUCCÈS : Certificat Validé Plein Droit]
```

---

### 4.4 Point 4 : Gestion des Références Inconnues (Taxonomie & Versions de Règles)

#### 4.4.1 Définition des Changements de `rules_version` (A8)
Un changement de valeur de `rules_version` (clé `5`) intervient **si et seulement si** une modification de la logique de The Iron Gate est susceptible de modifier un verdict sanitaire (`AUTHORISED` $\leftrightarrow$ `BLOCKED`) pour au moins une revendication possible.
- **Exemple de rupture de verdict** : L'intégration de la règle P18 au cycle 0009 a fait basculer trois vecteurs de test (`PRION-HARD-092`, `093`, `096`) d'autorisé à bloqué. Cette modification a entraîné le passage de la version normative de `1.4.0` à `1.5.0`.
- **Modifications sans changement de version majeure/mineure de verdict** : Les clarifications d'ordonnancement de motifs de refus (ex: P15 à P17) sans modification de verdicts n'affectent pas la logique de décision du certificat (puisqu'un certificat n'est émis que pour `AUTHORISED`).

#### 4.4.2 Protection Anti-Rétrogradation : Version Inconnue vs Version Retirée (A8)
La spécification distingue rigoureusement l'absence de support d'une version de sa dépréciation sanitaire :
1. **Version Inconnue (`ERR_CERT_UNKNOWN_RULES_VERSION`)** :
   - Le vérificateur ne dispose pas du moteur de règles correspondant dans sa table `rulesEngines`.
   - Tout repli (*fallback*) vers une version antérieure ou postérieure est formellement interdit.
2. **Version Retirée (`ERR_CERT_RULES_VERSION_RETIRED`)** :
   - La version est connue du vérificateur mais a été révoquée par l'autorité sanitaire (ex: découverte d'une faille dans une ancienne réglementation ou transition de période de grâce).
   - Cette distinction permet aux outils de diagnostic et d'audit d'indiquer précisément à l'opérateur que le certificat s'appuie sur une version réglementaire abrogée.

#### 4.4.3 Analyse de l'État Actuel de l'Implémentation & Chiffrage d'Évolution (A8)
Le Bushi 02 et le Bushi 12 actent en toute transparence technique l'état actuel du moteur :
- **État Actuel du Code** : La signature théorique `evaluate(claim, policy, taxonomyMap)` n'existe pas encore sous cette forme paramétrée dynamique dans `core/`. Le moteur The Iron Gate actuel porte son snapshot taxonomique directement compilé en dur (*hardcoded snapshot*), et la version des règles n'est pas encore instanciable dynamiquement par registre de versions.
- **Chiffrage de l'Évolution Paramétrée avec le Bushi 12** :
  - *Chantier 1 : Découplage Taxonomique* : Extraction de l'arbre phylogénétique sous forme de structure de données immutable injectée en paramètre (`TaxonomySnapshot`). Effort : **1 cycle**.
  - *Chantier 2 : Registre Multi-Moteurs* : Table de dispatch dynamique `Map<RulesVersion, RuleEngineInstance>`. Effort : **1 cycle**.
  - *Total estimé* : **2 cycles d'ingénierie conjointe** (Bushi 12 pour les règles pures, Bushi 01 pour le schéma CBOR/JCS du snapshot, Bushi 16 pour les vecteurs de test multi-versions).

---

### 4.5 Point 5 : Périmètre Probatoire et Limites du Certificat

Pour prévenir toute interprétation abusive de la portée juridique de la technologie AeterniTrak, la présente spécification circonscrit précisément la frontière entre la vérification algorithmique et la réalité physique du monde matériel.

#### 4.5.1 Ce que le Certificat Prouve Formellement (A9)
Le Certificat de Conformité Sanitaire apporte la **preuve cryptographique vérifiable hors-ligne** des assertions suivantes :
1. **Conformité Algorithmique Déclarative** : L'ensemble des données déclarées dans la revendication `claim` satisfait sans exception la totalité des listes blanches positives des portes G0 à G9 de The Iron Gate, selon les règles de la version déclarée et la taxonomie officielle scellée.
2. **Authenticité et Non-Répudiation de la Signature** : Le certificat a été scellé par une entité identifiée par son `kid`, détentrice d'une clé privée active répertoriée dans la liste de confiance officielle du vérificateur, dont l'usage autorise les certificats de lot et dont le statut n'est pas `REVOKED`.
3. **Intégrité Binaire de la Déclaration** : Pas un seul octet de la chaîne `claimJson` canonique n'a été altéré depuis l'instant de signature.

#### 4.5.2 Ce que le Certificat NE PROUVE PAS (Limites Physiques & Non-Garanti) (A9)
Le certificat **NE PEUT EN AUCUN CAS PROUVER NI GARANTIR** :
1. **La Véracité Physique des Déclarations à la Source (Fraude Matérielle)** :
   - Si un opérateur malveillant introduit clandestinement des carcasses bovines (Cat. 1 MRS) dans un broyeur tout en déclarant informatiquement des co-produits de volailles saines (Cat. 3) avec des numéros de boucle falsifiés, le certificat sera mathématiquement valide sur la base des déclarations transmises.
   - **La cryptographie garantit la cohérence logique des faits déclarés, elle ne valide pas la matière physique non instrumentée.**
2. **L'Absence de Contamination Croisée en Ligne de Production** :
   - Le certificat scelle un lot théorique. Il ne garantit pas qu'une ligne de convoyage industrielle n'a pas été souillée par des résidus d'un lot précédent si les protocoles de nettoyage d'usine n'ont pas été physiquement respectés.
3. **L'Authenticité Métrologique des Sondes Physiques** :
   - Le certificat enregistre l'empreinte `evidence_sha256` du journal de sonde de température/pression (Méthode 1 ou pasteurisation). Il garantit que le journal n'a pas été altéré après coup, mais ne garantit pas que les capteurs thermiques étaient correctement étalonnés ou qu'ils n'ont pas été trompés par une source de chaleur artificielle externe.
4. **La Conservation et l'Intégrité Post-Scellage** :
   - Le certificat ne garantit pas les conditions de transport ultérieures (rupture de la chaîne du froid, moisissures, contamination biologique après ouverture du conditionnement scellé).
5. **La Date Réelle d'Émission Physique (Vulnérabilité à l'Antidatage unilatéral)** :
   - La date d'émission `issued_at` (clé `3`) est déclarée unilatéralement par le signataire dans la charge utile.
   - En cas de compromission d'une clé privée, un attaquant détenant cette clé peut forger un certificat en antidatant la valeur de `issued_at` pour la situer artificiellement à l'intérieur de la fenêtre `[valid_from, valid_until]` de la clé (`qa/vectors/README.md` §4.11).
   - Le contrôle temporel K2 garantit la cohérence d'archive pour des signataires réguliers mais **ne protège pas contre l'antidatage frauduleux par une clé volée** : seule la révocation explicite de la clé dans le Trust Store protège contre ce risque.

> [!CAUTION]
> **Avertissement Réglementaire** :  
> Le certificat AeterniTrak constitue un instrument de preuve de conformité algorithmique. Il vient en appui des contrôles officiels de l'AFSCA, du DNF et des services vétérinaires d'État, mais **ne se substitue en aucun cas aux inspections physiques sur site, aux prélèvements histologiques et aux audits réguliers de biosécurité des installations**.

---

## 5. Matrice de Conformité & Critères d'Acceptation (Phase A)

Conformément aux instructions souveraines et à l'Ordre 0047 de Claude AI :

- **Phase A Exclusive** : Le présent document constitue une spécification formelle pure. Aucun code source d'implémentation n'a été ajouté dans `core/` et aucun vecteur approuvé n'a été inséré dans `qa/vectors/`.
- **Alignement Inter-Bushi Parfait** : Harmonisation intégrale avec `AET-SPEC-CRYPTO-001` v1.1.1 (Bushi 02), `AET-SPEC-PRION-001` v1.5.0 (Bushi 12) et `AET-SPEC-CORE-001` (Bushi 01).
- **Prochaine Étape (Phase B)** : Dépôt par Claude AI de la suite de vecteurs normatifs de certificat de lot (`qa/vectors/crypto/batch-certificate.vectors.json`), suivie de l'implémentation conjointe Bushi 02 / Bushi 12.
