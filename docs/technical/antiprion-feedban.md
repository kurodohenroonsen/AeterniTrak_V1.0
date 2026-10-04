# Spécification Technique & Formelle — The Iron Gate (Validateur Anti-Prion & Feed-Ban)

> **Document ID** : `AET-SPEC-PRION-001`  
> **Version** : 1.4.0  
> **Statut** : Soumis pour révision  
> **Date de référence** : 2026-10-04  
> **Branche Git** : `fix/bushi-12-reasons-v14`  
> **Auteur** : Bushi 12 (Anti-Prion & Biosecurity Lead)  
> **Revue & Arbitrage** : Claude AI (Master Verifier)  
> **Contrats Partagés** : Bushi 11 (Registres de filière), Bushi 01 (Déterminisme CBOR & Profil AeterniCore), Bushi 16 (QA Testvectors & Harnais)  
> **Suites de Vecteurs de Référence** :  
> - `qa/vectors/antiprion/feedban-matrix.vectors.json` (67 cas de base)  
> - `qa/vectors/antiprion/feedban-hardening.vectors.json` (42 cas de durcissement)  
> - `qa/vectors/antiprion/feedban-rules-v12.vectors.json` (64 cas règles v1.2, matrice 5.1 et DEC-AET-05)  
> - `qa/vectors/antiprion/feedban-rules-v13.vectors.json` (10 cas règle P14)  
> - `qa/vectors/antiprion/feedban-rules-v14.vectors.json` (19 cas règles v1.4, motifs d'infraction P15 à P17)  
> **Total Vecteurs Validés** : 202 cas conformes

---

## 1. Cadre Réglementaire, Décisions Souveraines & Lecture Juridique Arrêtée

Le présent document constitue la spécification formelle, mathématique et algorithmique du moteur de validation sanitaire et anti-prion d'AeterniTrak V1.0, baptisé **The Iron Gate** (La Porte de Fer).

Conformément à `CLAUDE.md`, à `PROTOCOL.md` §5 et aux directives souveraines de Kudoro dans `DECISIONS-KUDORO.md`, la prévention des encéphalopathies spongiformes transmissibles (EST / prions) et l'étanchéité du feed-ban européen ne reposent pas sur une déclaration administrative ou une promesse documentaire : elles sont garanties par un **verrou cryptographique et algorithmique inviolable**. L'oracle de signature est physiquement et logiquement incapable d'apposer un sceau de conformité de lot sur une revendication qui ne satisfait pas l'intégralité des listes blanches positives des portes G0 à G9.

### 1.1 Principe Fondamental Inviolable : Whitelist Stricte (Default-Deny)

> [!IMPORTANT]
> **Le Principe Unique de la Porte de Fer** :  
> **Toute porte est une liste d'autorisation positive stricte (whitelist). Toute valeur absente, inconnue, nulle, non typée ou hors de la liste blanche BLOQUE immédiatement.**  
> Aucune liste d'interdiction (blacklist) n'est admise dans la logique de décision : une liste d'interdiction autorise par omission, ce qui est incompatible avec la sécurité biologique absolue requise face aux prions.

---

### 1.2 Références Juridiques Européennes Consolidées (EUR-Lex)

Les règles implémentées sont directement adossées aux textes officiels de l'Union Européenne, vérifiés sur EUR-Lex le **2026-10-04** :

1. **Règlement (CE) n° 999/2001 du Parlement européen et du Conseil du 22 mai 2001**  
   *Fixant les règles pour la prévention, le contrôle et l'éradication de certaines encéphalopathies spongiformes transmissibles.*  
   - **Article 7** (Interdiction en matière d'alimentation animale) : Interdiction absolue de nourrir les ruminants avec des protéines animales, et interdiction de nourrir les animaux d'élevage avec des protéines dérivées de mammifères.  
   - **Annexe IV, Chapitre I** : Interdictions générales.  
   - **Annexe IV, Chapitre II** (Dérogations et réautorisations encadrées) :  
     - *Section A* : L'alimentation des animaux d'aquaculture avec des PAT de non-ruminants d'élevage (porcins, volailles, insectes, équidés, lagomorphes) et des farines de poisson est expressément autorisée.  
     - *Section B* : L'alimentation des porcins avec des PAT de volailles, des PAT d'insectes et des farines de poisson est autorisée.  
     - *Section C* : L'alimentation des volailles avec des PAT porcines, des PAT d'insectes et des farines de poisson est autorisée.  
   - Identifiant ELI : [http://data.europa.eu/eli/reg/2001/999/2021-11-23](http://data.europa.eu/eli/reg/2001/999/2021-11-23)

2. **Règlement (UE) 2021/1372 de la Commission du 17 août 2021**  
   *Modifiant l'annexe IV du règlement (CE) n° 999/2001 en ce qui concerne l'interdiction de nourrir les animaux d'élevage non-ruminants avec des protéines animales transformées issues d'autres animaux d'élevage.*  
   - Fixe le régime strict de non-contamination croisée : interdiction intra-espèce absolue et interdiction intra-groupe (porcins vers porcins interdit, volailles vers volailles interdit).  
   - Identifiant ELI : [http://data.europa.eu/eli/reg/2021/1372/oj](http://data.europa.eu/eli/reg/2021/1372/oj)

3. **Règlement (CE) n° 1069/2009 du Parlement européen et du Conseil du 21 octobre 2009**  
   *Établissant des règles sanitaires applicables aux sous-produits animaux et produits dérivés non destinés à la consommation humaine.*  
   - **Articles 8, 9 et 10** : Définition stricte et classification des matières des Catégories 1, 2 et 3.  
   - **Article 11(1)(a)** : **La Règle d'Or Anti-Prion** — interdiction absolue de nourrir des animaux terrestres d'une espèce donnée avec des PAT issues du corps ou de parties du corps d'animaux de la même espèce (interdiction du cannibalisme intra-espèce).  
   - **Articles 12, 13 et 14** : Voies d'utilisation et d'élimination autorisées pour chaque catégorie de sous-produits. Les matières de Catégorie 1 sont formellement exclues des fertilisants/engrais (art. 12).  
   - Identifiant ELI : [http://data.europa.eu/eli/reg/2009/1069/2019-12-14](http://data.europa.eu/eli/reg/2009/1069/2019-12-14)

4. **Règlement (UE) n° 142/2011 de la Commission du 25 février 2011**  
   *Portant application du règlement (CE) n° 1069/2009.*  
   - **Annexe IV, Chapitre III** (Méthodes standard de transformation) :  
     - **Méthode 1 (Stérilisation sous pression)** : Température à cœur $\ge 133\text{ }^\circ\text{C}$, pression absolue $\ge 3{,}0\text{ bars}$, durée sans interruption $\ge 20\text{ minutes}$, granulométrie $\le 50\text{ mm}$. Obligatoire pour toutes les matières de Catégories 1 et 2 vers usage technique ou engrais.  
     - Méthodes 2 à 7 : Méthodes thermiques et mécaniques alternatives sous conditions d'agrément.  
   - **Annexe X, Chapitre II, Section 1** (Protéines animales transformées — Exigences relatives à la transformation selon la nature de la protéine) :  
     - *Point B.1 (PAT de mammifères)* : Les PAT issues de mammifères doivent obligatoirement être soumises à la **Méthode 1 exclusivement** (133 °C / 3 bars / 20 min).  
     - *Point B.2 (PAT de non-mammifères)* : Les PAT issues de volailles ou d'insectes peuvent être soumises aux **Méthodes 1 à 5 ou 7** (la Méthode 6 leur est formellement interdite).  
     - *Point B.3 (Farine de poisson)* : Les matières issues de poissons peuvent être traitées par les **Méthodes 1 à 7** (la Méthode 6 étant spécifiquement réservée aux produits de la pêche).  
   - Identifiant ELI : [http://data.europa.eu/eli/reg/2011/142/2022-04-17](http://data.europa.eu/eli/reg/2011/142/2022-04-17)

5. **Règlement (UE) 2017/893 de la Commission du 24 mai 2017**  
   *Modifiant les annexes I et IV du règlement (CE) n° 999/2001 et les annexes X, XIV et XV du règlement (UE) n° 142/2011.*  
   - Régime limitatif des substrats d'élevage pour les insectes producteurs de PAT : matières d'origine végétale saine ou matières sélectionnées de catégorie 3 (abattoir sain transformé).  
   - **Exclusion absolue** : Les cadavres d'animaux (Cat. 1 ou Cat. 2), le fumier, les déchets de cuisine et de table, ainsi que les sous-produits d'abattoir crus excluent définitivement toute destination alimentaire humaine ou animale.  
   - Identifiant ELI : [http://data.europa.eu/eli/reg/2017/893/oj](http://data.europa.eu/eli/reg/2017/893/oj)

---

### 1.3 Décisions Souveraines Applicables (`DECISIONS-KUDORO.md`)

- **DEC-AET-04 (Agilité Cryptographique & Enveloppe COSE_Sign1)** :  
  Validation de l'enveloppe hybride COSE_Sign1 supportant nativement l'algorithme ES256 (`alg: -7`, NIST P-256) pour les signatures ancrées dans les enclaves matérielles sécurisées (Apple Secure Enclave iOS, Android StrongBox KeyMint, puces JavaCard ACOSJ 92 Ko) et l'algorithme Ed25519 (`alg: -8`, PureEd25519 RFC 8032) pour les serveurs et validateurs logiciels de filière. Les vérificateurs vérifient les deux algorithmes de façon universelle.
- **DEC-AET-05 (Dérogations Mémorielles Forestières & Pentobarbital)** :  
  Pour les dépouilles d'animaux de compagnie (Catégorie 1 mémorielle, dépistage LFA Pentobarbital négatif), la filière de sarcomusation avec pasteurisation thermique validée (70 °C, 1 h) est admise sous dérogation expresse aux seules fins d'arbres du souvenir en forêts cinéraires privées.  
  *Garde-fou v1 de la Porte de Fer* : En l'absence d'une politique de dérogation signée chargée dynamiquement dans le validateur v1, la destination `memorial_forestry` produit systématiquement le motif bloquant `DEROGATION_REQUIRED`. Les dépouilles positives au pentobarbital sont limitées à l'incinération haute température exclusive (`PRION-AUTH-015`).

---

### 1.4 Lecture Juridique Arrêtée

1. **La Règle d'Or Anti-Prion (Règl. 1069/2009 art. 11(1)(a))** :  
   Résolution systématique au rang espèce biologique avant toute comparaison : les sous-espèces sont obligatoirement résolues vers leur espèce parente (`9825 -> 9823`, `208526 -> 9031`, `9615 -> 9612`). Une tentative d'obscurcissement par déclaration d'une sous-espèce est interceptée (`FEED_BAN_INTRA_SPECIES_VIOLATION`). Dans la filière de sarcomusation (bioconversion par insectes), la règle s'applique à la fois à l'insecte et aux matières du substrat larvaire (une larve nourrie sur carcasse porcine transmise à des porcins est bloquée).
2. **La Règle Intra-Groupe (Règl. 999/2001 annexe IV modifiée par 2021/1372)** :  
   Bien qu'appartenant à des espèces distinctes, les croisements volaille vers volaille (ex. poulet vers dinde ou canard vers poulet) et porcin vers porcin sont formellement bloqués (`FEED_BAN_INTRA_GROUP_VIOLATION`).
3. **Exclusion Absolue des Ruminants (Règl. 999/2001)** :  
   Aucune PAT issue de ruminants (marqueur taxonomique 9845) ne peut entrer dans l'alimentation animale. Aucun ruminant ne peut être déclaré comme cible d'une destination alimentaire.
4. **Groupes Sources Autorisés en Alimentation Animale (Liste Positive Whitelist)** :  
   - Alimentation terrestre (`feed`) : `PORCINE`, `POULTRY`, `INSECT`, `FISH`.  
   - Alimentation aquacole (`aquaculture_feed`) : `PORCINE`, `POULTRY`, `INSECT`, `FISH`, plus `EQUINE` et `LAGOMORPH` (non-ruminants d'élevage autorisés par le règlement 999/2001 annexe IV chap. II section A).  
   Tout autre groupe source produit `SOURCE_GROUP_NOT_AUTHORISED`.
5. **Cibles Autorisées (Liste Positive Whitelist)** :  
   - `feed` : `PORCINE`, `POULTRY` exclusivement.  
   - `aquaculture_feed` : `FISH` exclusivement.  
   Toute autre cible produit `TARGET_GROUP_NOT_AUTHORISED`.
6. **Protection Absolue des Restes Humains** :  
   Toute détection d'origine humaine (taxon 9606, `material_class === "human_remains"` ou `origin_profile === "human"`) bloque instantanément et définitivement toute route alimentaire ou industrielle technique (`HUMAN_REMAINS_ROUTE_PROHIBITED`). Seule la crémation / incinération est autorisée sans dérogation (`PRION-AUTH-016`, `PRION-HARD-011`).

---

## 2. Spécification des Modèles de Données & Schémas

Pour résoudre le défaut architectural A1 identifié lors de l'audit de sécurité, la spécification sépare formellement deux structures de données :
1. **`BatchClaimInput`** : Structure d'entrée acceptée par la fonction d'évaluation `evaluate()`. Ses champs sont optionnels et tolérants afin de permettre l'audit exhaustif et la détection cumulée de tous les motifs d'infraction.
2. **`BatchClaim`** : Structure fermée, stricte et non ambiguë, représentant une revendication valide et scellable.

### 2.1 Schéma JSON — `BatchClaim` (Forme Fermée, Draft 2020-12)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://aeternitrak.org/schemas/batch-claim-v1.json",
  "title": "BatchClaim",
  "description": "Revendication d'intégrité sanitaire d'un lot conforme (forme fermée signable)",
  "type": "object",
  "required": ["batch_id", "substrate", "process", "product", "destination"],
  "additionalProperties": false,
  "properties": {
    "batch_id": {
      "type": "string",
      "pattern": "^[A-Za-z0-9_-]{3,64}$"
    },
    "substrate": {
      "type": "object",
      "required": ["category", "material_class", "origin_profile", "sources"],
      "additionalProperties": false,
      "properties": {
        "category": {
          "type": ["integer", "null"],
          "enum": [1, 2, 3, null]
        },
        "material_class": {
          "type": "string",
          "enum": [
            "slaughter_byproduct",
            "feed_grade_plant",
            "carcass",
            "human_remains",
            "manure",
            "catering_waste"
          ]
        },
        "origin_profile": {
          "type": "string",
          "enum": ["slaughterhouse", "feed_industry", "farm", "pet", "human", "wildlife_dnf"]
        },
        "sources": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["taxid"],
            "additionalProperties": false,
            "properties": {
              "taxid": { "type": "integer", "minimum": 1 },
              "label": { "type": "string" }
            }
          }
        },
        "pentobarbital_lfa": {
          "type": "string",
          "enum": ["positive", "negative", "not_tested"]
        }
      }
    },
    "process": {
      "type": "object",
      "required": ["route"],
      "additionalProperties": false,
      "properties": {
        "route": {
          "type": "string",
          "enum": ["direct_rendering", "insect_bioconversion"]
        },
        "insect_taxid": {
          "type": "integer",
          "minimum": 1
        },
        "treatment": {
          "type": "object",
          "required": ["method", "evidence_sha256"],
          "additionalProperties": false,
          "properties": {
            "method": { "type": "integer", "enum": [1, 2, 3, 4, 5, 6, 7] },
            "core_temp_c": { "type": "number" },
            "pressure_bar": { "type": "number" },
            "minutes": { "type": "number" },
            "evidence_sha256": {
              "type": "string",
              "pattern": "^[0-9a-f]{64}$"
            }
          }
        },
        "pasteurisation": {
          "type": "object",
          "required": ["core_temp_c", "minutes", "evidence_sha256"],
          "additionalProperties": false,
          "properties": {
            "core_temp_c": { "type": "number" },
            "minutes": { "type": "number" },
            "evidence_sha256": {
              "type": "string",
              "pattern": "^[0-9a-f]{64}$"
            }
          }
        }
      }
    },
    "product": {
      "type": "string",
      "enum": ["PAP", "insect_PAP", "fishmeal", "rendered_fat", "frass", "ash"]
    },
    "destination": {
      "type": "object",
      "required": ["use"],
      "additionalProperties": false,
      "properties": {
        "use": {
          "type": "string",
          "enum": [
            "feed",
            "aquaculture_feed",
            "technical",
            "fertiliser",
            "incineration",
            "memorial_forestry"
          ]
        },
        "target_taxids": {
          "type": "array",
          "items": { "type": "integer", "minimum": 1 }
        }
      }
    }
  }
}
```

### 2.2 Schéma CDDL (`BatchClaim` et `BatchClaimInput`, RFC 8610)

```cddl
; Forme stricte et scellable (BatchClaim)
batch_claim = {
  batch_id: tstr,
  substrate: substrate_record,
  process: process_record,
  product: product_type,
  destination: destination_record,
}

substrate_record = {
  category: 1 / 2 / 3 / null,
  material_class: "slaughter_byproduct" / "feed_grade_plant" / "carcass" /
                  "human_remains" / "manure" / "catering_waste",
  origin_profile: "slaughterhouse" / "feed_industry" / "farm" /
                  "pet" / "human" / "wildlife_dnf",
  sources: [* source_item],
  ? pentobarbital_lfa: "positive" / "negative" / "not_tested",
}

source_item = {
  taxid: uint,
  ? label: tstr,
}

process_record = {
  route: "direct_rendering" / "insect_bioconversion",
  ? insect_taxid: uint,
  ? treatment: treatment_record,
  ? pasteurisation: pasteurisation_record,
}

treatment_record = {
  method: 1..7,
  ? core_temp_c: number,
  ? pressure_bar: number,
  ? minutes: number,
  evidence_sha256: tstr, ; 64 caractères hexadécimaux minuscules
}

pasteurisation_record = {
  core_temp_c: number,
  minutes: number,
  evidence_sha256: tstr, ; 64 caractères hexadécimaux minuscules
}

product_type = "PAP" / "insect_PAP" / "fishmeal" / "rendered_fat" / "frass" / "ash"

destination_record = {
  use: "feed" / "aquaculture_feed" / "technical" / "fertiliser" /
       "incineration" / "memorial_forestry",
  ? target_taxids: [* uint],
}

; Forme d'entrée d'évaluation tolérante (BatchClaimInput)
batch_claim_input = {
  ? batch_id: any,
  ? substrate: {
    ? category: any,
    ? material_class: any,
    ? origin_profile: any,
    ? sources: [* any],
    ? pentobarbital_lfa: any,
    * any => any,
  },
  ? process: {
    ? route: any,
    ? insect_taxid: any,
    ? treatment: {
      ? method: any,
      ? core_temp_c: any,
      ? pressure_bar: any,
      ? minutes: any,
      ? evidence_sha256: any,
      * any => any,
    } / any,
    ? pasteurisation: {
      ? core_temp_c: any,
      ? minutes: any,
      ? evidence_sha256: any,
      * any => any,
    } / any,
    * any => any,
  },
  ? product: any,
  ? destination: {
    ? use: any,
    ? target_taxids: any,
    * any => any,
  },
  * any => any,
}
```

---

## 3. Résolution Taxonomique & Snapshot Embarqué

Le validateur opère en isolement complet du réseau. Aucune requête externe (DNS, REST) n'est autorisée. La référence taxonomique est figée dans le snapshot officiel `qa/vectors/antiprion/taxonomy-snapshot.json` (26 taxons vérifiés).

### 3.1 Règles de Résolution Taxonomique (DEFAULT_DENY & P8)

1. **Typage strict (P8)** : Tout taxid doit être un entier JSON valide (`typeof taxid === "number" && Number.isInteger(taxid)`). Une chaîne de caractères (ex. `"9823"` dans `PRION-HARD-005`), un flottant (ex. `9823.5` dans `PRION-HARD-006`) ou une valeur booléenne/nulle est immédiatement traitée comme inconnue (`TAXON_UNKNOWN`).
2. **Identification par TaxID exclusivement** : Les noms latins ou vernaculaires sans taxid numérique (`PRION-DENY-001`, `PRION-DENY-002`) produisent `TAXON_UNKNOWN`.
3. **Résolution des Sous-Espèces** : Une sous-espèce (`rank === "subspecies"`) est obligatoirement résolue vers son espèce parente de rang `species`.
4. **Rejet des Rangs Supérieurs à l'Espèce** : Tout identifiant de rang supérieur à l'espèce (`family`, `order`, `suborder`, `class`, `superclass`) est formellement bloqué (`TAXON_RANK_ABOVE_SPECIES`).

### 3.2 Algorithme de Résolution Taxonomique

```typescript
interface TaxonEntry {
  taxid: number;
  scientific_name: string;
  rank: string;
  parent_taxid?: number;
  lineage_markers: number[];
  group: string;
}

interface ResolvedTaxon {
  taxid: number;
  species_taxid: number;
  rank: string;
  group: string;
  lineage_markers: number[];
}

type TaxonResolutionResult = 
  | { success: true; taxon: ResolvedTaxon }
  | { success: false; error: "TAXON_UNKNOWN" | "TAXON_RANK_ABOVE_SPECIES" };

function resolveTaxon(taxid: unknown, taxonomyMap: Map<number, TaxonEntry>): TaxonResolutionResult {
  // Règle P8 : Typage strict, aucun cast implicite
  if (typeof taxid !== "number" || !Number.isInteger(taxid)) {
    return { success: false, error: "TAXON_UNKNOWN" };
  }

  const entry = taxonomyMap.get(taxid);
  if (!entry) {
    return { success: false, error: "TAXON_UNKNOWN" };
  }

  if (entry.rank !== "species" && entry.rank !== "subspecies") {
    return { success: false, error: "TAXON_RANK_ABOVE_SPECIES" };
  }

  let current = entry;
  const markers = [...entry.lineage_markers];

  // Résolution récursive des sous-espèces vers l'espèce parente
  while (current.rank === "subspecies") {
    if (!current.parent_taxid) {
      return { success: false, error: "TAXON_UNKNOWN" };
    }
    const parent = taxonomyMap.get(current.parent_taxid);
    if (!parent) {
      return { success: false, error: "TAXON_UNKNOWN" };
    }
    current = parent;
    if (current.lineage_markers) {
      markers.push(...current.lineage_markers);
    }
  }

  return {
    success: true,
    taxon: {
      taxid: entry.taxid,
      species_taxid: current.taxid,
      rank: entry.rank,
      group: current.group || entry.group,
      lineage_markers: markers
    }
  };
}
```

---

## 4. Spécification Formelle Exhaustive des 10 Portes de Fer G0 à G9

Le validateur exécute **10 portes séquentielles ordonnées (G0 à G9)**. L'évaluation est **exhaustive** : toutes les portes sont vérifiées pour consigner l'intégralité des motifs d'infraction, avec seulement **deux cas d'arrêt anticipé impératifs** :
1. **Arrêt G0** : Si `destination.use` n'appartient pas à la liste blanche des usages supportés (`DESTINATION_UNSUPPORTED`).
2. **Arrêt G2** : Si des restes humains sont orientés vers une filière d'alimentation ou technique (`HUMAN_REMAINS_ROUTE_PROHIBITED`).

> [!IMPORTANT]
> **Règle d'exhaustivité P1** :  
> Le motif `TARGET_UNSPECIFIED` (G0) et les erreurs taxonomiques G1 (`TAXON_UNKNOWN`, `TAXON_RANK_ABOVE_SPECIES`) **n'arrêtent pas** l'évaluation : les portes suivantes s'évaluent sur l'ensemble des taxons ayant pu être résolus.

### 4.1 Registre Ordonné des 17 Motifs d'Infraction

| Ordre | Porte | Code Motif d'Infraction | Base Légale & Sécuritaire |
|:---:|:---:|---|---|
| 0 | **G0** | `DESTINATION_UNSUPPORTED` | Whitelist v1 : `use` non reconnu dans la liste blanche |
| 0 | **G0** | `TARGET_UNSPECIFIED` | Whitelist v1 : destination alimentaire sans cible spécifiée |
| 1 | **G1** | `TAXON_UNKNOWN` | Whitelist snapshot : taxid absent, non entier ou invalide |
| 1 | **G1** | `TAXON_RANK_ABOVE_SPECIES` | Règle espèce : rang supérieur à l'espèce (famille, classe, etc.) |
| 2 | **G2** | `HUMAN_REMAINS_ROUTE_PROHIBITED` | Ordre public : aucune valorisation alimentaire ou technique de l'humain |
| 3 | **G3** | `SUBSTRATE_CATEGORY_VIOLATION` | Règl. 1069/2009 art. 12-14 ; Règl. 2017/893 (substrats d'insectes) |
| 3 | **G3** | `CATEGORY_DESTINATION_PROHIBITED` | Règl. 1069/2009 art. 12 : Catégorie 1 interdite en fertilisant |
| 3 | **G3** | `DEROGATION_REQUIRED` | DEC-AET-05 requise : dérogation forestière obligatoire pour Cat. 1 |
| 4 | **G4** | `PENTOBARBITAL_POSITIVE` | PROTOCOL.md §5 : Euthanasiant toxique avéré -> incinération exclusive |
| 4 | **G4** | `PENTOBARBITAL_NOT_TESTED` | PROTOCOL.md §5 : Absence de test LFA sur animal de compagnie |
| 5 | **G5** | `FEED_BAN_RUMINANT_SOURCE` | Règl. 999/2001 Annexe IV ch. I : Protéine de ruminant interdite |
| 6 | **G6** | `FEED_BAN_RUMINANT_TARGET` | Règl. 999/2001 Annexe IV ch. I : Ruminant interdit de toute PAT |
| 7 | **G7** | `FEED_BAN_INTRA_SPECIES_VIOLATION` | Règl. 1069/2009 art. 11(1)(a) : **Règle d'Or Anti-Prion** (Cannibalisme) |
| 8 | **G8** | `FEED_BAN_INTRA_GROUP_VIOLATION` | Règl. 999/2001 Annexe IV (2021/1372) : Porc<->Porc, Volaille<->Volaille |
| 8 | **G8** | `SOURCE_GROUP_NOT_AUTHORISED` | Règl. 2021/1372 : Source animale non autorisée en alimentation |
| 8 | **G8** | `TARGET_GROUP_NOT_AUTHORISED` | Règl. 2021/1372 : Cible animale non homologuée pour la destination |
| 9 | **G9** | `TREATMENT_NOT_PROVEN` | Règl. 142/2011 Annexe X ch. II sect. 1 & Annexe IV ch. III |

---

### 4.2 Pseudo-Code Exhaustif du Validateur de la Porte de Fer (Règles v1.4 P9 à P17)

```typescript
export interface PolicyInput {
  policy_id: string;
  version?: number;
  legal_basis: string;
  authority_reference: string;
}

export interface EvaluationResult {
  verdict: "AUTHORISED" | "BLOCKED";
  reasons: string[];
  signature_permitted: boolean;
}

export function evaluate(
  claim: BatchClaimInput,
  policy: PolicyInput | null = null,
  taxonomyMap: Map<number, TaxonEntry>
): EvaluationResult {
  const reasons: string[] = [];

  const SUPPORTED_USES = new Set([
    "feed",
    "aquaculture_feed",
    "technical",
    "fertiliser",
    "incineration",
    "memorial_forestry"
  ]);

  const KNOWN_MATERIAL_CLASSES = new Set([
    "slaughter_byproduct",
    "feed_grade_plant",
    "carcass",
    "human_remains",
    "manure",
    "catering_waste"
  ]);

  const MAMMAL_GROUPS = new Set([
    "PORCINE",
    "EQUINE",
    "LAGOMORPH",
    "CARNIVORE",
    "RUMINANT",
    "HUMAN"
  ]);

  // =========================================================================
  // PORTE G0 : Destination & Spécification des cibles
  // =========================================================================
  const dest = claim.destination;
  const use = dest?.use;

  // Whitelist d'usage : arrêt anticipé absolu si usage non supporté
  if (!use || typeof use !== "string" || !SUPPORTED_USES.has(use)) {
    return {
      verdict: "BLOCKED",
      reasons: ["DESTINATION_UNSUPPORTED"],
      signature_permitted: false
    };
  }

  // Règle P11 : L'incinération est toujours autorisée de plein droit.
  // Après G0, aucune porte ne produit de motif pour l'incinération.
  if (use === "incineration") {
    return {
      verdict: "AUTHORISED",
      reasons: [],
      signature_permitted: true
    };
  }

  const isFeed = (use === "feed" || use === "aquaculture_feed");
  let targetTaxids: unknown[] = [];

  if (isFeed) {
    if (!Array.isArray(dest?.target_taxids) || dest.target_taxids.length === 0) {
      reasons.push("TARGET_UNSPECIFIED");
    } else {
      targetTaxids = dest.target_taxids;
    }
  } else if (Array.isArray(dest?.target_taxids)) {
    targetTaxids = dest.target_taxids;
  }

  // =========================================================================
  // PORTE G1 : Taxonomie, Résolution & Default-Deny (Règles P2, P8, P9, P14, P15)
  // =========================================================================
  let hasTaxonUnknown = false;
  let hasTaxonRankAbove = false;

  const resolvedSources: ResolvedTaxon[] = [];
  const substrate = claim.substrate;
  const sources = substrate?.sources;
  const proc = claim.process;
  const route = proc?.route;

  // Règle P9 & P15 : substrate.sources doit être un tableau.
  // Absent ou d'un autre type => TAXON_UNKNOWN (hors incinération).
  // En alimentation (feed ou aquaculture_feed), un tableau sources vide vaut TAXON_UNKNOWN
  // pour toute route autre que insect_bioconversion (inconnue, absente, mal typée comprise) (P15).
  if (!Array.isArray(sources)) {
    hasTaxonUnknown = true;
  } else {
    if (isFeed && route !== "insect_bioconversion" && sources.length === 0) {
      hasTaxonUnknown = true;
    }
    for (const s of sources) {
      if (!s || typeof s !== "object" || !("taxid" in s)) {
        hasTaxonUnknown = true;
        continue;
      }
      const res = resolveTaxon(s.taxid, taxonomyMap);
      if (!res.success) {
        if (res.error === "TAXON_UNKNOWN") hasTaxonUnknown = true;
        else if (res.error === "TAXON_RANK_ABOVE_SPECIES") hasTaxonRankAbove = true;
      } else {
        resolvedSources.push(res.taxon);
      }
    }
  }

  let resolvedInsect: ResolvedTaxon | null = null;
  if (route === "insect_bioconversion") {
    const insectTaxid = proc?.insect_taxid;
    if (insectTaxid === undefined || insectTaxid === null) {
      hasTaxonUnknown = true;
    } else {
      const res = resolveTaxon(insectTaxid, taxonomyMap);
      if (!res.success) {
        if (res.error === "TAXON_UNKNOWN") hasTaxonUnknown = true;
        else if (res.error === "TAXON_RANK_ABOVE_SPECIES") hasTaxonRankAbove = true;
      } else if (res.taxon.group !== "INSECT") {
        // Règle P14 : L'organisme de bioconversion doit être un insecte résolu
        hasTaxonUnknown = true;
      } else {
        resolvedInsect = res.taxon;
      }
    }
  }

  const resolvedTargets: ResolvedTaxon[] = [];
  for (const tid of targetTaxids) {
    const res = resolveTaxon(tid, taxonomyMap);
    if (!res.success) {
      if (res.error === "TAXON_UNKNOWN") hasTaxonUnknown = true;
      else if (res.error === "TAXON_RANK_ABOVE_SPECIES") hasTaxonRankAbove = true;
    } else {
      resolvedTargets.push(res.taxon);
    }
  }

  if (hasTaxonUnknown) reasons.push("TAXON_UNKNOWN");
  if (hasTaxonRankAbove) reasons.push("TAXON_RANK_ABOVE_SPECIES");

  // =========================================================================
  // PORTE G2 : Protection des Restes Humains (Règles P3, P11, P12, P15)
  // =========================================================================
  // Règle P15 : G1 s'évalue en entier avant G2. Sur des restes humains, les motifs
  // G1 (TAXON_UNKNOWN, TAXON_RANK_ABOVE_SPECIES) précèdent HUMAN_REMAINS_ROUTE_PROHIBITED.
  const isHuman = (
    resolvedSources.some(s => s.species_taxid === 9606 || s.group === "HUMAN") ||
    substrate?.material_class === "human_remains" ||
    substrate?.origin_profile === "human"
  );

  if (isHuman) {
    // Règle P12 : G2 arrête l'évaluation pour toute destination (hors incinération).
    // La mémoire forestière humaine renvoie DEROGATION_REQUIRED et s'arrête.
    if (use === "memorial_forestry") {
      reasons.push("DEROGATION_REQUIRED");
      return {
        verdict: "BLOCKED",
        reasons,
        signature_permitted: false
      };
    } else {
      reasons.push("HUMAN_REMAINS_ROUTE_PROHIBITED");
      return {
        verdict: "BLOCKED",
        reasons,
        signature_permitted: false
      };
    }
  }

  // =========================================================================
  // PORTE G3 : Catégorie de Matières & Substrats (Règles P4, P10, P12, P16, P17, DEC-AET-05)
  // =========================================================================
  const category = substrate?.category;
  const materialClass = substrate?.material_class;

  // Règle P16 : « Source déclarée » au sens de P10 : tout élément du tableau sources compte,
  // qu'il se résolve ou non (null, taxid mal typé, taxid hors snapshot, rang > espèce, nom sans taxid).
  const hasDeclaredSource = Array.isArray(sources) && sources.length > 0;
  const isPlantCategoryViolation = (materialClass === "feed_grade_plant" && hasDeclaredSource);

  let inDerogationScope = false;

  if (isFeed) {
    let feedViolation = false;
    if (category !== 3) {
      feedViolation = true;
    } else if (route === "direct_rendering") {
      if (materialClass !== "slaughter_byproduct" && materialClass !== "feed_grade_plant") {
        feedViolation = true;
      }
    } else if (route === "insect_bioconversion") {
      if (materialClass !== "feed_grade_plant") {
        feedViolation = true;
      }
    } else {
      feedViolation = true;
    }
    if (feedViolation || isPlantCategoryViolation) {
      reasons.push("SUBSTRATE_CATEGORY_VIOLATION");
    }
  } else if (use === "technical" || use === "fertiliser") {
    // Règle P12 : Portes indépendantes sans chaîne « sinon »
    const isInvalidCategory = (category !== 1 && category !== 2 && category !== 3);
    const isInvalidMaterial = (typeof materialClass !== "string" || !KNOWN_MATERIAL_CLASSES.has(materialClass));

    if (isInvalidCategory || isInvalidMaterial || isPlantCategoryViolation) {
      reasons.push("SUBSTRATE_CATEGORY_VIOLATION");
    }
    if (category === 1 && use === "fertiliser") {
      reasons.push("CATEGORY_DESTINATION_PROHIBITED");
    }
  } else if (use === "memorial_forestry") {
    // Règle P17 : Les contrôles de substrat (P4 et P10) s'appliquent à memorial_forestry.
    // SUBSTRATE_CATEGORY_VIOLATION précède DEROGATION_REQUIRED, avec ou sans politique.
    const isInvalidCategory = (category !== 1 && category !== 2 && category !== 3);
    const isInvalidMaterial = (typeof materialClass !== "string" || !KNOWN_MATERIAL_CLASSES.has(materialClass));

    if (isInvalidCategory || isInvalidMaterial || isPlantCategoryViolation) {
      reasons.push("SUBSTRATE_CATEGORY_VIOLATION");
    }

    // Dérogation souveraine DEC-AET-05 (§4.3)
    const isPolicyValid = (
      policy !== null &&
      typeof policy === "object" &&
      policy.policy_id === "DEC-AET-05" &&
      typeof policy.legal_basis === "string" &&
      policy.legal_basis.trim() !== "" &&
      typeof policy.authority_reference === "string" &&
      policy.authority_reference.trim() !== ""
    );

    const hasRuminantSource = resolvedSources.some(
      s => s.group === "RUMINANT" || s.lineage_markers.includes(9845)
    );

    // Règle P14 : insect_taxid doit impérativement avoir pour groupe résolu "INSECT"
    inDerogationScope = (
      isPolicyValid &&
      substrate?.origin_profile === "pet" &&
      category === 1 &&
      materialClass === "carcass" &&
      route === "insect_bioconversion" &&
      resolvedInsect !== null &&
      resolvedInsect.group === "INSECT" &&
      Array.isArray(sources) && sources.length > 0 &&
      !hasTaxonUnknown && !hasTaxonRankAbove &&
      !hasRuminantSource
    );

    if (!inDerogationScope) {
      reasons.push("DEROGATION_REQUIRED");
    }
  }

  // =========================================================================
  // PORTE G4 : Contrôle Pentobarbital (Animaux de Compagnie)
  // =========================================================================
  if (substrate?.origin_profile === "pet") {
    const lfa = substrate.pentobarbital_lfa;
    if (lfa === "positive") {
      reasons.push("PENTOBARBITAL_POSITIVE");
    } else if (lfa !== "negative") {
      reasons.push("PENTOBARBITAL_NOT_TESTED");
    }
  }

  // =========================================================================
  // PORTES G5 à G8 : Feed-Ban Européen (Alimentation Terrestre & Aquacole)
  // =========================================================================
  if (isFeed) {
    // G5 : Interdiction des Ruminants en Source (Règl. 999/2001)
    const hasRuminantSource = resolvedSources.some(
      s => s.group === "RUMINANT" || s.lineage_markers.includes(9845)
    );
    if (hasRuminantSource) {
      reasons.push("FEED_BAN_RUMINANT_SOURCE");
    }

    // G6 : Interdiction des Ruminants en Cible (Règl. 999/2001)
    const hasRuminantTarget = resolvedTargets.some(
      t => t.group === "RUMINANT" || t.lineage_markers.includes(9845)
    );
    if (hasRuminantTarget) {
      reasons.push("FEED_BAN_RUMINANT_TARGET");
    }

    // G7 : Règle d'Or Anti-Cannibalisme Intra-Espèce (Règl. 1069/2009 art. 11(1)(a))
    const allSourceSpecies = new Set(resolvedSources.map(s => s.species_taxid));
    if (route === "insect_bioconversion" && resolvedInsect) {
      allSourceSpecies.add(resolvedInsect.species_taxid);
    }
    const hasIntraSpecies = resolvedTargets.some(t => allSourceSpecies.has(t.species_taxid));
    if (hasIntraSpecies) {
      reasons.push("FEED_BAN_INTRA_SPECIES_VIOLATION");
    }

    // G8 : Interdictions de Groupe & Groupes Positifs (Règl. 2021/1372 & 999/2001)
    const effectiveSourceGroups = new Set(resolvedSources.map(s => s.group));
    if (route === "insect_bioconversion" && resolvedInsect) {
      // Le groupe de l'organisme provient toujours de la résolution du snapshot (Règle P14)
      effectiveSourceGroups.add(resolvedInsect.group);
    }
    const targetGroups = new Set(resolvedTargets.map(t => t.group));

    if (
      (effectiveSourceGroups.has("PORCINE") && targetGroups.has("PORCINE")) ||
      (effectiveSourceGroups.has("POULTRY") && targetGroups.has("POULTRY"))
    ) {
      reasons.push("FEED_BAN_INTRA_GROUP_VIOLATION");
    }

    if (effectiveSourceGroups.size > 0) {
      const allowedSources = (use === "feed")
        ? new Set(["PORCINE", "POULTRY", "INSECT", "FISH"])
        : new Set(["PORCINE", "POULTRY", "INSECT", "FISH", "EQUINE", "LAGOMORPH"]);

      let sourceGroupAuthorized = true;
      for (const g of effectiveSourceGroups) {
        if (!allowedSources.has(g)) {
          sourceGroupAuthorized = false;
          break;
        }
      }
      if (!sourceGroupAuthorized) {
        reasons.push("SOURCE_GROUP_NOT_AUTHORISED");
      }
    }

    if (targetGroups.size > 0) {
      if (use === "aquaculture_feed") {
        const allFish = Array.from(targetGroups).every(g => g === "FISH");
        if (!allFish) reasons.push("TARGET_GROUP_NOT_AUTHORISED");
      } else {
        const allowedTargets = new Set(["PORCINE", "POULTRY"]);
        const allAllowed = Array.from(targetGroups).every(g => allowedTargets.has(g));
        if (!allAllowed) reasons.push("TARGET_GROUP_NOT_AUTHORISED");
      }
    }
  }

  // =========================================================================
  // PORTE G9 : Traitement Sanitaire Requis & Preuve (Règles P6, P7, P8, P12, P13, DEC-AET-05)
  // =========================================================================
  // P12 : Une catégorie invalide vers technique ou engrais exige aussi la méthode 1
  if (isFeed || ((use === "technical" || use === "fertiliser") && category !== 3)) {
    const treatment = proc?.treatment;
    if (!treatment || typeof treatment !== "object") {
      reasons.push("TREATMENT_NOT_PROVEN");
    } else {
      const method = treatment.method;
      const evidence = treatment.evidence_sha256;
      const hasValidEvidence = typeof evidence === "string" && /^[0-9a-f]{64}$/.test(evidence);

      let methodAuthorized = false;
      if (use === "technical" || use === "fertiliser") {
        methodAuthorized = (method === 1);
      } else { // isFeed
        if (route === "insect_bioconversion") {
          methodAuthorized = (typeof method === "number" && [1, 2, 3, 4, 5, 7].includes(method));
        } else {
          // direct_rendering
          const isMammal = resolvedSources.some(s => MAMMAL_GROUPS.has(s.group)) || resolvedSources.length === 0;
          const isAllFish = resolvedSources.length > 0 && resolvedSources.every(s => s.group === "FISH");
          const isAllPoultry = resolvedSources.length > 0 && resolvedSources.every(s => s.group === "POULTRY");

          if (isMammal) {
            methodAuthorized = (method === 1);
          } else if (isAllFish) {
            methodAuthorized = (typeof method === "number" && [1, 2, 3, 4, 5, 6, 7].includes(method));
          } else if (isAllPoultry) {
            methodAuthorized = (typeof method === "number" && [1, 2, 3, 4, 5, 7].includes(method));
          } else {
            // Règle P13 : Natures mêlées => Méthode 1 exclusivement
            methodAuthorized = (method === 1);
          }
        }
      }

      if (!methodAuthorized || !hasValidEvidence) {
        reasons.push("TREATMENT_NOT_PROVEN");
      } else if (method === 1) {
        const temp = treatment.core_temp_c;
        const press = treatment.pressure_bar;
        const mins = treatment.minutes;

        const paramsValid = (
          typeof temp === "number" && !Number.isNaN(temp) && temp >= 133 &&
          typeof press === "number" && !Number.isNaN(press) && press >= 3.0 &&
          typeof mins === "number" && !Number.isNaN(mins) && mins >= 20
        );

        if (!paramsValid) {
          reasons.push("TREATMENT_NOT_PROVEN");
        }
      }
    }
  } else if (use === "memorial_forestry" && inDerogationScope) {
    // Dérogation DEC-AET-05 : pasteurisation thermique obligatoire (70 °C, 60 min)
    const pasteurisation = proc?.pasteurisation;
    if (!pasteurisation || typeof pasteurisation !== "object") {
      reasons.push("TREATMENT_NOT_PROVEN");
    } else {
      const temp = pasteurisation.core_temp_c;
      const mins = pasteurisation.minutes;
      const evidence = pasteurisation.evidence_sha256;
      const hasValidEvidence = typeof evidence === "string" && /^[0-9a-f]{64}$/.test(evidence);

      const paramsValid = (
        typeof temp === "number" && !Number.isNaN(temp) && temp >= 70 &&
        typeof mins === "number" && !Number.isNaN(mins) && mins >= 60 &&
        hasValidEvidence
      );

      if (!paramsValid) {
        reasons.push("TREATMENT_NOT_PROVEN");
      }
    }
  }

  // =========================================================================
  // Décision Finale & Invariance Mathématique
  // =========================================================================
  const isAuthorised = (reasons.length === 0);
  return {
    verdict: isAuthorised ? "AUTHORISED" : "BLOCKED",
    reasons,
    signature_permitted: isAuthorised
  };
}
```

---

### 4.3 Dérogation Souveraine DEC-AET-05 (Mémoire Forestière des Animaux de Compagnie)

Conformément à l'arbitrage souverain de Kudoro du **2026-10-04** (`DECISIONS-KUDORO.md`) et aux exigences du `README.md` §4.5, la Porte de Fer ne code aucune dérogation en dur : elle reçoit une politique explicite en second argument via la signature unifiée :

$$\text{evaluate}(\text{claim}, \text{policy})$$

Sans politique valide fournie (`policy === null` ou politique non conforme), le comportement de sécurité par défaut reste inchangé : la destination `memorial_forestry` produit le motif bloquant `DEROGATION_REQUIRED`.

#### 4.3.1 Validité Formelle de la Politique
Une politique est reconnue valide si et seulement si :
1. C'est un objet non nul ;
2. `policy_id === "DEC-AET-05"` ;
3. `legal_basis` est une chaîne non vide ;
4. `authority_reference` est une chaîne non vide.

La vérification cryptographique de la signature de la politique relève de l'hôte d'orchestration (Bushi 02). La Porte de Fer n'évalue qu'une politique déjà formellement authentifiée.

#### 4.3.2 Périmètre Strict d'Application (Conjonction Obligatoire)
La dérogation DEC-AET-05 ne s'applique que si **l'ensemble** des conditions suivantes est satisfait :
1. `destination.use === "memorial_forestry"` ;
2. `substrate.origin_profile === "pet"` ;
3. `substrate.category === 1` ;
4. `substrate.material_class === "carcass"` ;
5. `process.route === "insect_bioconversion"` ;
6. `process.insect_taxid` résolu dont le groupe taxonomique est `"INSECT"` (règle P14) ; s'il résout vers `BOVINE`, `HUMAN`, `FELINE`, etc., il produit `TAXON_UNKNOWN` et ne peut en aucun cas être injecté comme source d'insecte ni bénéficier de la dérogation ;
7. Au moins une source déclarée dans `substrate.sources` (`Array.isArray(sources) && sources.length > 0`) ;
8. Aucune erreur taxonomique en porte G1 (`!hasTaxonUnknown && !hasTaxonRankAbove`) ;
9. Aucun taxon ruminant parmi les sources résolues (`!hasRuminantSource`).

Toute revendication orientée vers la mémoire forestière ne satisfaisant pas l'intégralité de ce périmètre produit le motif bloquant `DEROGATION_REQUIRED`.

#### 4.3.3 Exigences Sanitaires dans le Périmètre
Dans le périmètre de la dérogation :
- **Porte G4** : Le dépistage du pentobarbital est obligatoire. `pentobarbital_lfa === "negative"` est exigé ; une valeur `"positive"` émet `PENTOBARBITAL_POSITIVE` et une valeur non testée émet `PENTOBARBITAL_NOT_TESTED`.
- **Porte G9** : Un traitement de pasteurisation validé est obligatoire dans `process.pasteurisation`. Il exige :
  - `core_temp_c` $\ge 70\text{ }^\circ\text{C}$ (numérique) ;
  - `minutes` $\ge 60\text{ min}$ (numérique) ;
  - `evidence_sha256` : empreinte cryptographique valide de 64 caractères hexadécimaux minuscules.
  L'absence ou la non-conformité de ces paramètres produit le motif `TREATMENT_NOT_PROVEN`.

#### 4.3.4 Exclusions Absolues & Portée Restreinte
- **Restes humains** : Jamais couverts par la dérogation DEC-AET-05. La porte G2 intercepte toute détection humaine et émet `DEROGATION_REQUIRED` avec arrêt anticipé immédiat.
- **Autres destinations** : La dérogation ne couvre ni l'alimentation humaine ou animale (`feed`, `aquaculture_feed`), ni les fertilisants (`fertiliser`), ni l'usage technique. Pour ces destinations, les portes G3 à G9 s'appliquent dans toute leur rigueur.

#### 4.3.5 Réserve Juridique & Administrative
La décision souveraine DEC-AET-05 engage le projet AeterniTrak, mais ne se substitue pas à l'autorisation administrative de l'autorité compétente (AFSCA / DNF en Région wallonne) requise par le règlement (CE) n° 1069/2009. C'est pourquoi le champ `authority_reference` est obligatoire et auditable, et pourquoi les vecteurs de test portent la référence fictive `TEST-ONLY-AUTHORITY-REF-0001`. **Aucune politique réelle en production ne doit être émise avant que le Bushi 13 n'ait formalisé la référence de l'arrêté d'autorisation dans `docs/functional/`.**
```

---

## 5. Matrices de Conformité & Références des Vecteurs

### 5.1 Matrice (a) : Groupe Source × Destination Animale (`feed` / `aquaculture_feed`)

La matrice ci-dessous spécifie le comportement de la Porte de Fer pour chaque combinaison source/cible en alimentation animale. Toutes les cellules citent désormais leur vecteur de test officiel (`PRION-AUTH-*`, `PRION-BLOCK-*`, `PRION-DENY-*`, `PRION-HARD-*`, `PRION-CELL-001` à `022`).

| Groupe Source | Cible `PORCINE` | Cible `POULTRY` | Cible `FISH` (Aquaculture) | Cible `RUMINANT` | Cible `LAGOMORPH` | Cible `INSECT` |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **`PORCINE`** | **BLOQUÉ**<br>`FEED_BAN_INTRA_SPECIES`<br>`FEED_BAN_INTRA_GROUP`<br>[`PRION-BLOCK-001`]<br>[`PRION-BLOCK-002`] | **AUTORISÉ**<br>[`PRION-AUTH-001`]<br>[`PRION-AUTH-002`] | **AUTORISÉ**<br>[`PRION-AUTH-008`] | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_TGT`<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-BLOCK-011`] | **BLOQUÉ**<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-DENY-012`] | **BLOQUÉ**<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-CELL-001`] |
| **`POULTRY`** | **AUTORISÉ**<br>[`PRION-AUTH-003`]<br>[`PRION-AUTH-004`] | **BLOQUÉ**<br>`FEED_BAN_INTRA_SPECIES`<br>`FEED_BAN_INTRA_GROUP`<br>[`PRION-BLOCK-003`]<br>[`PRION-BLOCK-004`]<br>[`PRION-BLOCK-005`] | **AUTORISÉ**<br>[`PRION-HARD-024`] | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_TGT`<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-CELL-002`] | **BLOQUÉ**<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-CELL-003`] | **BLOQUÉ**<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-CELL-004`] |
| **`INSECT`** | **AUTORISÉ**<br>[`PRION-AUTH-006`] | **AUTORISÉ**<br>[`PRION-AUTH-005`] | **AUTORISÉ**<br>[`PRION-AUTH-007`] | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_TGT`<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-BLOCK-012`] | **BLOQUÉ**<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-CELL-005`] | **BLOQUÉ**<br>`FEED_BAN_INTRA_SPECIES`<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-BLOCK-008`] |
| **`FISH`** | **AUTORISÉ**<br>[`PRION-AUTH-011`] | **AUTORISÉ**<br>[`PRION-HARD-025`] | **AUTORISÉ** (si $\neq$ espèce)<br>[`PRION-AUTH-010`]<br>**BLOQUÉ** (si = espèce)<br>[`PRION-BLOCK-009`] | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_TGT`<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-BLOCK-014`] | **BLOQUÉ**<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-CELL-006`] | **BLOQUÉ**<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-CELL-007`] |
| **`EQUINE`** | **BLOQUÉ**<br>`SOURCE_GROUP_NOT_AUTH`<br>[`PRION-DENY-010`] | **BLOQUÉ**<br>`SOURCE_GROUP_NOT_AUTH`<br>[`PRION-CELL-008`] | **AUTORISÉ**<br>[`PRION-AUTH-009`] | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_TGT`<br>`SOURCE_GROUP_NOT_AUTH`<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-CELL-009`] | **BLOQUÉ**<br>`SOURCE_GROUP_NOT_AUTH`<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-CELL-010`] | **BLOQUÉ**<br>`SOURCE_GROUP_NOT_AUTH`<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-CELL-011`] |
| **`LAGOMORPH`** | **BLOQUÉ**<br>`SOURCE_GROUP_NOT_AUTH`<br>[`PRION-CELL-012`] | **BLOQUÉ**<br>`SOURCE_GROUP_NOT_AUTH`<br>[`PRION-DENY-011`] | **AUTORISÉ**<br>[`PRION-HARD-021`] | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_TGT`<br>`SOURCE_GROUP_NOT_AUTH`<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-CELL-013`] | **BLOQUÉ**<br>`FEED_BAN_INTRA_SPECIES`<br>`SOURCE_GROUP_NOT_AUTH`<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-CELL-014`] | **BLOQUÉ**<br>`SOURCE_GROUP_NOT_AUTH`<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-CELL-015`] |
| **`CARNIVORE`** | **BLOQUÉ**<br>`SUBSTRATE_CAT_VIOLATION`<br>`SOURCE_GROUP_NOT_AUTH`<br>[`PRION-CELL-016`] | **BLOQUÉ**<br>`SUBSTRATE_CAT_VIOLATION`<br>`SOURCE_GROUP_NOT_AUTH`<br>[`PRION-BLOCK-022`] | **BLOQUÉ**<br>`SOURCE_GROUP_NOT_AUTH`<br>[`PRION-HARD-022`] | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_TGT`<br>`SOURCE_GROUP_NOT_AUTH`<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-CELL-017`] | **BLOQUÉ**<br>`SOURCE_GROUP_NOT_AUTH`<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-CELL-018`] | **BLOQUÉ**<br>`SOURCE_GROUP_NOT_AUTH`<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-CELL-019`] |
| **`RUMINANT`** | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_SRC`<br>`SOURCE_GROUP_NOT_AUTH`<br>[`PRION-BLOCK-010`] | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_SRC`<br>`SOURCE_GROUP_NOT_AUTH`<br>[`PRION-BLOCK-013`]<br>[`PRION-BLOCK-015`] | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_SRC`<br>`SOURCE_GROUP_NOT_AUTH`<br>[`PRION-HARD-023`] | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_SRC`<br>`FEED_BAN_RUMINANT_TGT`<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-HARD-042`]<br>[`PRION-CELL-022`] | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_SRC`<br>`SOURCE_GROUP_NOT_AUTH`<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-CELL-020`] | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_SRC`<br>`SOURCE_GROUP_NOT_AUTH`<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-CELL-021`] |

*Cas particuliers d'assemblage et cumul prouvés par vecteurs :*
- Lot poolé multi-sources contenant une source interdite : Porc + Poulet -> Volaille = BLOQUÉ [`PRION-BLOCK-006`].
- Cibles multiples dont l'une est interdite : Porc -> [Volaille, Porcin] = BLOQUÉ [`PRION-BLOCK-007`].
- Route aquaculture avec cible aviaire non piscicole : Porc -> Volaille en `aquaculture_feed` = BLOQUÉ [`PRION-DENY-013`].
- Cumul total d'infractions : Cadavre bovin Cat. 2 d'origine compagnie non testé sans traitement vers bovins = BLOQUÉ avec 8 motifs ordonnés [`PRION-HARD-042`].

---

### 5.2 Matrice (b) : Catégorie de Matières × Destination

| Catégorie Substrat | `feed` / `aquaculture_feed` | `fertiliser` (Engrais) | `technical` (Industriel) | `incineration` (Crémation/C1) | `memorial_forestry` (Forêt) |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **Catégorie 1** *(MRS, compagnie, faune suspecte)* | **BLOQUÉ**<br>`SUBSTRATE_CATEGORY_VIOLATION`<br>[`PRION-BLOCK-022`] | **BLOQUÉ**<br>`CATEGORY_DESTINATION_PROHIBITED`<br>[`PRION-BLOCK-023`] | **AUTORISÉ** (Méthode 1 cimenterie)<br>[`PRION-AUTH-014`]<br>*(Bloqué si pentobarbital: [`PRION-BLOCK-025`])* | **AUTORISÉ**<br>[`PRION-AUTH-015`]<br>[`PRION-AUTH-016`] | **BLOQUÉ**<br>`DEROGATION_REQUIRED`<br>[`PRION-BLOCK-024`]<br>[`PRION-BLOCK-027`] |
| **Catégorie 2** *(Cadavres ferme, faune saine, fumier)* | **BLOQUÉ**<br>`SUBSTRATE_CATEGORY_VIOLATION`<br>[`PRION-BLOCK-015` à `020`]<br>[`PRION-BLOCK-016` à `018`] | **AUTORISÉ** (Méthode 1 frass)<br>[`PRION-AUTH-013`]<br>*(Bloqué si méthode 3: [`PRION-HARD-040`])* | **AUTORISÉ** (Méthode 1 biodiesel)<br>[`PRION-AUTH-012`]<br>[`PRION-AUTH-017`]<br>*(Bloqué si méthode 7: [`PRION-HARD-039`])* | **AUTORISÉ**<br>[`PRION-HARD-041`] | **BLOQUÉ**<br>`DEROGATION_REQUIRED`<br>*(DEC-AET-05)* |
| **Catégorie 3** *(Abattoir sain, matières végétales)* | **AUTORISÉ** (si règles d'or et de groupe respectées)<br>[`PRION-AUTH-001` à `011`]<br>*(Bloqué si abattoir cru sur larves: [`PRION-BLOCK-021`])* | **AUTORISÉ**<br>*(Règl. 1069/2009 art. 14)* | **AUTORISÉ**<br>*(Règl. 1069/2009 art. 14)* | **AUTORISÉ**<br>*(Règl. 1069/2009 art. 14)* | **BLOQUÉ**<br>`DEROGATION_REQUIRED`<br>*(DEC-AET-05)* |
| **Catégorie Nulle / Non Déclarée** | **BLOQUÉ**<br>`SUBSTRATE_CATEGORY_VIOLATION`<br>[`PRION-DENY-014`] | **BLOQUÉ**<br>`SUBSTRATE_CATEGORY_VIOLATION`<br>[`PRION-HARD-017`] | **BLOQUÉ**<br>`SUBSTRATE_CATEGORY_VIOLATION`<br>[`PRION-HARD-016`] | **AUTORISÉ**<br>[`PRION-AUTH-016`]<br>[`PRION-HARD-011`]<br>[`PRION-HARD-019`] | **BLOQUÉ**<br>`DEROGATION_REQUIRED`<br>[`PRION-BLOCK-028`] |

---

### 5.3 Matrice (c) : Destination × Traitement Sanitaire Requis (Règl. 142/2011)

| Destination | Type de Matière / Substrat | Traitement Exigé | Vecteurs Nominaux & Défaillances |
|---|---|---|---|
| `feed` / `aquaculture_feed` | PAT de mammifères (Cat. 3) | **Méthode 1 obligatoire** : $\ge 133\text{ }^\circ\text{C}$, $\ge 3{,}0\text{ bar}$, $\ge 20\text{ min}$, hash SHA-256 (64 hex minuscules) | **AUTORISÉ** : [`PRION-AUTH-001`], [`PRION-AUTH-002`], [`PRION-AUTH-008`]<br>**BLOQUÉ** (sans traitement) : [`PRION-HARD-026`]<br>**BLOQUÉ** (méthode 1 incomplète) : [`PRION-HARD-027`], [`PRION-HARD-028`]<br>**BLOQUÉ** (méthodes 3, 6, 7 interdites pour mammifères) : [`PRION-BLOCK-036`], [`PRION-HARD-031`], [`PRION-HARD-032`] |
| `feed` / `aquaculture_feed` | PAT de volailles (Cat. 3) | **Méthodes 1, 2, 3, 4, 5, 7** + preuve SHA-256 | **AUTORISÉ** : [`PRION-AUTH-003`], [`PRION-AUTH-004`], [`PRION-HARD-033`]<br>**BLOQUÉ** (sans preuve) : [`PRION-HARD-034`]<br>**BLOQUÉ** (méthode 6 interdite volailles) : [`PRION-HARD-035`] |
| `feed` / `aquaculture_feed` | PAT d'insectes (*Hermetia*) | **Méthodes 1, 2, 3, 4, 5, 7** + preuve SHA-256 | **AUTORISÉ** : [`PRION-AUTH-005`], [`PRION-AUTH-006`], [`PRION-AUTH-007`]<br>**BLOQUÉ** (méthode 6 interdite) : [`PRION-HARD-037`]<br>**BLOQUÉ** (méthode 8 inexistante) : [`PRION-HARD-038`] |
| `feed` / `aquaculture_feed` | Farine de poisson (Cat. 3) | **Méthodes 1 à 7** + preuve SHA-256 | **AUTORISÉ** : [`PRION-AUTH-010`], [`PRION-AUTH-011`], [`PRION-HARD-036`] |
| `technical` (Biodiesel, cimenterie) | Cadavres Cat. 2 ou MRS Cat. 1 | **Méthode 1 Obligatoire** : 133 °C / 3 bars / 20 min + preuve SHA-256 | **AUTORISÉ** : [`PRION-AUTH-012`], [`PRION-AUTH-014`], [`PRION-AUTH-017`]<br>**BLOQUÉ** (sans preuve) : [`PRION-BLOCK-031`]<br>**BLOQUÉ** (132 °C < 133 °C) : [`PRION-BLOCK-032`]<br>**BLOQUÉ** (19 min < 20 min) : [`PRION-BLOCK-033`]<br>**BLOQUÉ** (2,9 bar < 3,0 bar) : [`PRION-BLOCK-034`]<br>**BLOQUÉ** (méthode 7 interdite) : [`PRION-HARD-039`] |
| `fertiliser` (Frass) | Frass issu de cadavres de ferme (Cat. 2) | **Méthode 1 Obligatoire** : 133 °C / 3 bars / 20 min + preuve SHA-256 | **AUTORISÉ** : [`PRION-AUTH-013`]<br>**BLOQUÉ** (méthode 3 interdite) : [`PRION-HARD-040`] |
| `incineration` | C1 pentobarbital positif, restes humains | Incinération / Crémation haute température | **AUTORISÉ** (G9 ne s'applique pas) : [`PRION-AUTH-015`], [`PRION-AUTH-016`], [`PRION-HARD-011`], [`PRION-HARD-019`], [`PRION-HARD-041`] |
| `memorial_forestry` | C1 mémoriel LFA-négatif | Pasteurisation (70 °C, 1h) | **BLOQUÉ EN V1** : `DEROGATION_REQUIRED` [`PRION-BLOCK-024`], [`PRION-BLOCK-027`], [`PRION-BLOCK-028`] |

---

## 6. Oracle de Signature Cryptographique & Enveloppe COSE_Sign1

L'oracle de signature de conformité est conçu pour empêcher toute fuite de privilège ou signature illicite par dérivation d'objet.

### 6.1 Architecture Anti-Flottants CBOR & Empreinte Canonique JCS (A3)

Le profil CBOR déterministe d'AeterniCore v1 (`qa/vectors/README.md` §3) **interdit formellement les flottants** (major type 7 flottants IEEE 754 non autorisés dans la charge utile signée). Or une revendication de lot peut contenir des flottants (ex. `pressure_bar: 2.9` dans `PRION-BLOCK-034`).

Conformément à l'arbitrage A3 de Claude AI et aux amendements M4 de l'ordre 0012 :
1. **La charge utile signée COSE_Sign1 ne contient pas la revendication directement**, mais son empreinte cryptographique SHA-256 calculée sur sa représentation JSON canonique selon la RFC 8785 (JCS).
2. **Structure de la charge utile CBOR signée** : Clés entières déterministes, typage compact :
   - `1` : `claim_sha256` : `bstr` de 32 octets = $\text{SHA-256}(\text{JCS}(\text{claim}))$.
   - `2` : `verdict` : `tstr` = `"AUTHORISED"`.
   - `3` : `issued_at` : tag 1 (epoch secondes en entier).
   - `4` : `snapshot_sha256` : `bstr` de 32 octets = $\text{SHA-256}(\text{snapshot\_bytes})$ du snapshot taxonomique embarqué (liaison des règles A4).
   - `5` : `rules_version` : `tstr` = `"1.2.0"` (liaison de la version des règles A4).
3. La revendication complète voyage à côté du certificat signé, sous forme JSON canonique RFC 8785 (`JCS(claim)`).

### 6.2 Enveloppe COSE_Sign1 & Agilité DEC-AET-04 (A2)

La signature est encapsulée dans une structure `COSE_Sign1` (RFC 9052 §4.2) conforme aux spécifications d'AeterniCore v1 (sans tag 18 `#6.18`, convention amendement M4 de l'ordre 0012) :

```cddl
COSE_Sign1_BatchClaim = [
  protected_header: bstr .cbor protected_header_map,
  unprotected_header: {},
  payload: bstr .cbor batch_claim_signed_payload,
  signature: bstr
]

protected_header_map = {
  1: -7 / -8, ; alg: ES256 (-7) ou Ed25519 (-8) selon DEC-AET-04
  16: "application/aeternitrak-batch-claim+cbor" ; typ spécifique (étiquette 16, RFC 9596)
}

batch_claim_signed_payload = {
  1: bstr .size 32, ; SHA-256 du JSON canonique (JCS RFC 8785) de la revendication
  2: "AUTHORISED",  ; Verdict obligatoire
  3: #6.1(uint),    ; Tag 1: Horodatage UTC (secondes depuis epoch)
  4: bstr .size 32, ; SHA-256 du snapshot taxonomique officiel
  5: tstr,          ; Version de spécification des règles ("1.2.0")
}
```

Calcul de la signature :
$$\text{Sig\_structure} = \big[ \text{"Signature1"}, \text{protected\_header}, \text{h''}, \text{payload} \big]$$
$$\text{Signature} = \text{Sign}(K_{\text{private}}, \text{CBOR\_Deterministic}(\text{Sig\_structure}))$$

---

### 6.3 Étanchéité à l'Exécution : `evaluateAndSign` & Registre Opaque (A5)

Pour garantir l'étanchéité absolue en JavaScript/TypeScript à l'exécution et empêcher toute altération concurrente ou post-évaluation de la revendication :
1. **Aucune fonction `sign()` n'est exportée du module**.
2. **Point d'entrée unique `evaluateAndSign(input, signer)`** :
   - L'entrée `input` est clonée en profondeur (`structuredClone`) pour isoler l'objet de tout accès mémoire concurrent.
   - La copie clonée est gelée récursivement (`Object.freeze`).
   - L'évaluation est exécutée sur la copie gelée.
   - En cas d'infraction (`verdict !== "AUTHORISED"`), la tentative est scellée dans le journal d'audit append-only et une exception `IronGateSecurityViolation` est levée.
   - Si et seulement si `reasons.length === 0`, un jeton scellé interne est consigné dans un registre `WeakSet` privé au module, le payload COSE_Sign1 est assemblé avec le hash JCS de la copie gelée, et la signature est apposée.

```typescript
// Registre privé au module (non exporté)
const authorisedTokens = new WeakSet<object>();

export interface BatchSigner {
  algorithm: "ES256" | "Ed25519";
  sign(data: Uint8Array): Promise<Uint8Array>;
}

export async function evaluateAndSign(
  input: BatchClaimInput,
  signer: BatchSigner,
  taxonomyMap: Map<number, TaxonEntry>,
  snapshotSha256: Uint8Array,
  auditLogger: AuditLogger
): Promise<Uint8Array> {
  // 1. Clonage en profondeur & gel récursif (anti-modification A5)
  const frozenClaim = deepFreeze(structuredClone(input));

  // 2. Évaluation des 10 portes de fer
  const evalResult = evaluate(frozenClaim, null, taxonomyMap);

  if (evalResult.verdict !== "AUTHORISED" || !evalResult.signature_permitted) {
    // 3. Enregistrement irrévocable dans le journal d'audit (boîte noire)
    await auditLogger.logInfraction(frozenClaim, evalResult.reasons);
    throw new IronGateSecurityViolation(
      `Lot rejeté par la Porte de Fer (${evalResult.reasons.join(", ")})`
    );
  }

  // 4. Scellage dans le WeakSet privé
  const token = {};
  authorisedTokens.add(token);

  // 5. Canonisation JCS RFC 8785 de la revendication
  const jcsClaimUtf8 = canonicalizeJCS(frozenClaim);
  const claimSha256 = crypto.createHash("sha256").update(jcsClaimUtf8).digest();

  // 6. Construction de la charge utile CBOR déterministe (clés entières sans flottant)
  const payloadMap = new Map<number, unknown>([
    [1, claimSha256],
    [2, "AUTHORISED"],
    [3, { $tag: 1, $value: Math.floor(Date.now() / 1000) }],
    [4, snapshotSha256],
    [5, "1.2.0"]
  ]);
  const payloadBytes = encodeDeterministicCBOR(payloadMap);

  // 7. Enveloppe COSE_Sign1 (agilité DEC-AET-04, étiquette typ 16 RFC 9596)
  const algId = signer.algorithm === "ES256" ? -7 : -8;
  const protectedHeaderMap = new Map<number, unknown>([
    [1, algId],
    [16, "application/aeternitrak-batch-claim+cbor"]
  ]);
  const protectedBytes = encodeDeterministicCBOR(protectedHeaderMap);

  const sigStructure = [
    "Signature1",
    protectedBytes,
    new Uint8Array(0),
    payloadBytes
  ];
  const toBeSigned = encodeDeterministicCBOR(sigStructure);
  const signatureBytes = await signer.sign(toBeSigned);

  const coseSign1 = [
    protectedBytes,
    new Map(), // headers non protégés
    payloadBytes,
    signatureBytes
  ];

  return encodeDeterministicCBOR(coseSign1);
}
```

---

### 6.4 Vérification en Profondeur (*Dual-Sided Re-evaluation*)

Tout contrôleur de lot (nœud décentralisé P2P, autorité sanitaire AFSCA, inspecteur d'abattoir) effectue une **vérification à deux niveaux** :
1. **Niveau Cryptographique** : Vérification de la signature COSE_Sign1 (ES256 ou Ed25519) sur la charge utile CBOR avec la clé publique de l'autorité de lot.
2. **Niveau Algorithmique Obligatoire** : Le vérificateur extrait le hash de revendication (clé 1), vérifie que $\text{SHA-256}(\text{JCS}(\text{revendication})) == \text{clé 1}$, vérifie l'empreinte du snapshot taxonomique (clé 4), puis **ré-exécute localement `evaluate(revendication)`**. Si le verdict ré-évalué n'est pas `AUTHORISED`, le certificat est **rejeté comme falsifié**, même si la signature mathématique était valide (défense absolue contre les clés compromises).

### 6.5 Garantie Zéro-Bypass

Aucun commutateur (`--force`, `--bypass`, `--skip-feedban`), aucun rôle applicatif (`SUPERADMIN`, `EMERGENCY_OVERRIDE`), ni aucune variable d'environnement (`process.env.BYPASS_*`) n'existe dans le moteur de validation. Tout certificat émis sans respecter les 10 portes de fer est rejeté dès la vérification algorithmique locale.

---

## 7. Boîte Noire d'Infractions Append-Only (Journal d'Audit Chaîné)

Toute tentative d'évaluation conclue par un verdict `BLOCKED` est immédiatement et irréversiblement scellée dans le registre d'audit des infractions.

### 7.1 Architecture de Chaînage Cryptographique

Le journal des infractions est une structure append-only où chaque entrée est cryptographiquement liée à la précédente par son hachage SHA-256 :

$$\text{entry\_hash}_i = \text{SHA-256}\Big(\text{JCS}\big(\{\text{"seq"}: i, \text{"timestamp"}: t_i, \text{"prev\_hash"}: h_{i-1}, \text{"batch\_id"}: b_i, \text{"claim"}: c_i, \text{"reasons"}: r_i\}\big)\Big)$$

### 7.2 Intégrité & Absence de Troncature (A6)

Conformément à l'exigence A6, **la revendication d'entrée complète (`claim`) est conservée sans aucune troncature** dans l'entrée d'audit afin de permettre l'instruction judiciaire complète par les services vétérinaires compétents.

### 7.3 Format d'une Entrée d'Audit

```json
{
  "sequence_number": 42,
  "timestamp": "2026-10-04T12:00:00Z",
  "prev_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "batch_id": "AT-H-42",
  "batch_claim": {
    "batch_id": "AT-H-42",
    "substrate": {
      "category": 2,
      "material_class": "carcass",
      "origin_profile": "pet",
      "sources": [{ "taxid": 9913 }],
      "pentobarbital_lfa": "not_tested"
    },
    "process": {
      "route": "direct_rendering",
      "treatment": null
    },
    "product": "PAP",
    "destination": {
      "use": "feed",
      "target_taxids": [9913]
    }
  },
  "verdict": "BLOCKED",
  "reasons": [
    "SUBSTRATE_CATEGORY_VIOLATION",
    "PENTOBARBITAL_NOT_TESTED",
    "FEED_BAN_RUMINANT_SOURCE",
    "FEED_BAN_RUMINANT_TARGET",
    "FEED_BAN_INTRA_SPECIES_VIOLATION",
    "SOURCE_GROUP_NOT_AUTHORISED",
    "TARGET_GROUP_NOT_AUTHORISED",
    "TREATMENT_NOT_PROVEN"
  ],
  "entry_hash": "b2f6c91a8e3d0475...",
  "audit_signature": "cose_sign1_hex_bytes..."
}
```

---

## 8. Bilan de Validation et Couverture des 202 Vecteurs

### 8.1 Couverture Intégrale des Suites de Vecteurs

L'algorithme formel spécifié dans le présent document résout l'intégralité des **202 vecteurs de tests** répartis sur les cinq suites officielles :
1. `qa/vectors/antiprion/feedban-matrix.vectors.json` (67 cas de base) :
   - 17 cas autorisés nominaux (`PRION-AUTH-001` à `017`)
   - 36 cas d'interdiction sanitaire (`PRION-BLOCK-001` à `036`)
   - 14 cas de rejet par défaut (`PRION-DENY-001` à `014`)
2. `qa/vectors/antiprion/feedban-hardening.vectors.json` (42 cas de durcissement) :
   - 42 cas d'épreuve éliminant les 8 failles de sécurité S1 à S8, les 6 défauts de contrat C1 à C6 et les 7 défauts d'architecture A1 à A7 (`PRION-HARD-001` à `042`).
3. `qa/vectors/antiprion/feedban-rules-v12.vectors.json` (64 cas règles v1.2) :
   - 20 cas de clarification des règles P9 à P13 (`PRION-HARD-043` à `062`)
   - 22 cas de couverture intégrale de la matrice 5.1 (`PRION-CELL-001` à `022`)
   - 22 cas d'encadrement strict de la dérogation mémorielle DEC-AET-05 (`PRION-DEROG-001` à `022`).
4. `qa/vectors/antiprion/feedban-rules-v13.vectors.json` (10 cas règle P14) :
   - 10 cas de validation stricte de l'organisme de bioconversion (`PRION-HARD-063` à `072`).
5. `qa/vectors/antiprion/feedban-rules-v14.vectors.json` (19 cas règles v1.4) :
   - 19 cas de fixation rigoureuse des listes de motifs d'infraction ordonnées selon les règles P15, P16 et P17 (`PRION-HARD-073` à `091`).

### 8.2 État de Conformité

Le validateur pur `evaluate(claim, policy)` implémente l'exact ensemble de règles spécifié ci-dessus, garantissant une conformité binaire stricte aux 202 vecteurs de tests approuvés.

---
*Fin de la spécification formelle The Iron Gate v1.4 — Bushi 12 (Anti-Prion & Biosecurity Lead)*
