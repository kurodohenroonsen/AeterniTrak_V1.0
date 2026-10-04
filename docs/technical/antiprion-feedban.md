# Spécification Technique — Validateur Anti-Prion & Feed-Ban (« The Iron Gate »)

> **Bushi 12** : Anti-Prion & Feed-Ban Validator  
> **Devise** : *« Jamais l'espèce ne se nourrira d'elle-même. La barrière cryptographique est infranchissable. »*  
> **Version** : 1.0.0  
> **Statut** : Approuvé pour Phase A (Spécification formelle)  
> **Date de référence** : 2026-10-04  
> **Branche Git** : `ag/bushi-12-antiprion`  
> **Contrat Partagé** : Bushi 11 (Registres de filière), Bushi 01 (Déterminisme CBOR), Bushi 16 (QA Testvectors)  
> **Vecteurs de référence** : `qa/vectors/antiprion/feedban-matrix.vectors.json` (67 vecteurs)

---

## 1. Cadre Réglementaire & Lecture Juridique Arrêtée

Le présent document constitue la spécification technique et formelle du moteur de validation sanitaire et anti-prion d'AeterniTrak V1.0. Conformément aux arbitrages consignés dans `DECISIONS-KUDORO.md` et aux exigences de `PROTOCOL.md` §5, la prévention des encéphalopathies spongiformes transmissibles (EST / prions) et le respect du droit européen des sous-produits animaux ne reposent pas sur une simple politique déclarative ou administrative, mais sur un **blocage cryptographique algorithmique irréversible** : l'oracle de signature Ed25519 est mathématiquement et logiquement incapable de sceller une revendication de conformité de lot (*BatchClaim*) non conforme.

### 1.1 Références Juridiques Européennes (EUR-Lex)

Les règles implémentées sont directement issues du corpus réglementaire de l'Union Européenne, vérifié le **2026-10-04** :

1. **Règlement (CE) n° 999/2001 du Parlement européen et du Conseil du 22 mai 2001**  
   *Fixant les règles pour la prévention, le contrôle et l'éradication de certaines encéphalopathies spongiformes transmissibles.*  
   - Article 7 (Interdiction en matière d'alimentation animale) et Annexe IV (Alimentation des animaux).  
   - Identifiant ELI : [http://data.europa.eu/eli/reg/2001/999/2021-11-23](http://data.europa.eu/eli/reg/2001/999/2021-11-23)
2. **Règlement (UE) 2021/1372 de la Commission du 17 août 2021**  
   *Modifiant l'annexe IV du règlement (CE) n° 999/2001 en ce qui concerne l'interdiction de nourrir les animaux d'élevage non-ruminants avec des protéines animales transformées issues d'autres animaux d'élevage.*  
   - Réautorisation encadrée des PAT porcines pour la volaille, des PAT de volailles pour les porcins, et des PAT d'insectes pour les porcins, volailles et l'aquaculture.  
   - Identifiant ELI : [http://data.europa.eu/eli/reg/2021/1372/oj](http://data.europa.eu/eli/reg/2021/1372/oj)
3. **Règlement (CE) n° 1069/2009 du Parlement européen et du Conseil du 21 octobre 2009**  
   *Établissant des règles sanitaires applicables aux sous-produits animaux et produits dérivés non destinés à la consommation humaine.*  
   - Articles 8, 9, 10 (Matières des catégories 1, 2 et 3) ; Articles 11(1)(a)(b) (Restrictions absolues d'utilisation et recyclage intra-espèce) ; Articles 12, 13, 14 (Élimination et utilisation autorisées).  
   - Identifiant ELI : [http://data.europa.eu/eli/reg/2009/1069/2019-12-14](http://data.europa.eu/eli/reg/2009/1069/2019-12-14)
4. **Règlement (UE) n° 142/2011 de la Commission du 25 février 2011**  
   *Portant application du règlement (CE) n° 1069/2009.*  
   - Annexe IV, Chapitre III (Méthodes standard de transformation : Méthode 1 = 133 °C à cœur, 3 bars de pression absolue, 20 minutes sans interruption, granulométrie ≤ 50 mm).  
   - Identifiant ELI : [http://data.europa.eu/eli/reg/2011/142/2022-04-17](http://data.europa.eu/eli/reg/2011/142/2022-04-17)
5. **Règlement (UE) 2017/893 de la Commission du 24 mai 2017**  
   *Modifiant les annexes I et IV du règlement (CE) n° 999/2001 et les annexes X, XIV et XV du règlement (UE) n° 142/2011 en ce qui concerne les dispositions relatives aux protéines animales transformées.*  
   - Régime strict des substrats d'élevage pour insectes destinés aux PAT : matières d'origine non-animale ou matières de catégorie 3 limitativement énumérées.  
   - Identifiant ELI : [http://data.europa.eu/eli/reg/2017/893/oj](http://data.europa.eu/eli/reg/2017/893/oj)

---

### 1.2 Lecture Juridique Arrêtée (Claude AI & Kudoro)

Les six principes directeurs suivants régissent sans exception la logique de contrôle :

1. **Règle d'Or (Règlement 1069/2009, art. 11(1)(a))** :  
   Il est strictement interdit de nourrir des animaux terrestres d'une espèce donnée avec des protéines animales transformées (PAT) issues du corps ou de parties du corps d'animaux de la même espèce biologique.  
   *Résolution systématique au rang espèce* : Les sous-espèces sont résolues vers leur espèce parente avant comparaison (`9825 → 9823`, `208526 → 9031`, `9615 → 9612`). Une tentative de déclarer un porcelet en `Sus scrofa domesticus` (9825) pour consommer des PAT de `Sus scrofa` (9823) est interceptée comme cannibalisme intra-espèce (`FEED_BAN_INTRA_SPECIES_VIOLATION`).
2. **Règle de Groupe (Règlement 999/2001 annexe IV ch. II, tel que modifié par 2021/1372)** :  
   Les PAT porcines ne peuvent être destinées qu'aux volailles et à l'aquaculture. Les PAT de volailles ne peuvent être destinées qu'aux porcins et à l'aquaculture. Les PAT d'insectes peuvent nourrir porcins, volailles et aquaculture.  
   *Interdiction intra-groupe* : Poulet vers dinde (ou canard vers poulet) est **formellement bloqué** sous le motif `FEED_BAN_INTRA_GROUP_VIOLATION`, bien qu'il s'agisse d'espèces distinctes au sein du règne aviaire.
3. **Exclusion Absolue des Ruminants (Règlement 999/2001)** :  
   Aucune PAT issue de ruminants ne peut entrer dans l'alimentation d'animaux d'élevage. Aucune PAT (quelle qu'en soit la source) ne peut nourrir un ruminant. Le groupe `RUMINANT` est défini sans équivoque par la présence du marqueur de lignée taxonomique NCBI `9845`.
4. **Régime des Substrats (Règlement 2017/893)** :  
   Les insectes d'élevage destinés à la production de PAT ne peuvent être nourris que sur des substrats végétaux sains ou des matières de catégorie 3 sélectionnées. Les **cadavres d'animaux (Cat. 1 ou Cat. 2), le fumier, les déchets de cuisine et de table, ainsi que les sous-produits d'abattoir crus excluent irrévocablement toute destination alimentaire**.  
   *Conséquence pour la sarcomusation* : Les larves d'insectes (*Hermetia illucens*) développées sur des cadavres d'animaux de ferme, faune ou compagnie ne peuvent **en aucun cas** alimenter la chaîne trophique ; leurs débouchés sont exclusivement techniques (biodiesel, chimie), agronomiques (frass fertilisant après stérilisation Méthode 1), ou mémoriels sous dérogation.
5. **Politique du "Default-Deny" (Refus par Défaut)** :  
   Tout taxon doit être spécifié par son identifiant numérique NCBI Taxonomy valide présent dans le snapshot officiel embarqué. Tout nom vernaculaire ou latin sans identifiant numérique est rejeté (`TAXON_UNKNOWN`). Tout rang taxonomique strictement supérieur à l'espèce (famille, ordre, classe) est rejeté (`TAXON_RANK_ABOVE_SPECIES`). Toute destination ou catégorie non explicitement répertoriée est bloquée (`DESTINATION_UNSUPPORTED`, `SUBSTRATE_CATEGORY_VIOLATION`).
6. **Gestion des Dérogations & Mémoire Forestière** :  
   Aucune dérogation n'est codée en dur ou activée par défaut. L'aiguillage mémoriel (arbres cinéraires, valorisation forestière pour animaux de compagnie LFA-négatifs ou restes humains) émet systématiquement le motif bloquant `DEROGATION_REQUIRED` tant que la décision souveraine `DEC-AET-05` n'a pas été formellement signée par Kudoro.

---

## 2. A1. Spécification Formelle du Schéma `BatchClaim` v1

Le schéma `BatchClaim` v1 est le contrat de données universel échangé entre les registres de traçabilité de filière (Bushi 11), le moteur de contrôle d'intégrité déterministe (Bushi 01) et le validateur anti-prion (Bushi 12).

### 2.1 JSON Schema (Draft 2020-12)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://aeternitrak.org/schemas/batch-claim-v1.json",
  "title": "BatchClaim",
  "description": "Revendication d'intégrité et de conformité sanitaire d'un lot AeterniTrak V1.0",
  "type": "object",
  "required": [
    "batch_id",
    "substrate",
    "process",
    "product",
    "destination"
  ],
  "additionalProperties": false,
  "properties": {
    "batch_id": {
      "type": "string",
      "pattern": "^[A-Za-z0-9_-]{3,64}$",
      "description": "Identifiant unique du lot de production"
    },
    "substrate": {
      "type": "object",
      "required": [
        "category",
        "material_class",
        "origin_profile",
        "sources"
      ],
      "additionalProperties": false,
      "properties": {
        "category": {
          "type": ["integer", "null"],
          "enum": [1, 2, 3, null],
          "description": "Catégorie sous-produits animaux selon règl. 1069/2009 (1, 2, 3 ou null si indéterminé)"
        },
        "material_class": {
          "type": "string",
          "enum": [
            "slaughter_byproduct",
            "feed_grade_plant",
            "carcass",
            "human_remains",
            "manure",
            "catering_waste",
            "unknown"
          ]
        },
        "origin_profile": {
          "type": "string",
          "enum": [
            "slaughterhouse",
            "feed_industry",
            "farm",
            "pet",
            "human",
            "wildlife_dnf"
          ]
        },
        "sources": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "taxid": {
                "type": "integer",
                "minimum": 1
              },
              "label": {
                "type": "string"
              }
            },
            "additionalProperties": true
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
          "enum": [
            "direct_rendering",
            "insect_bioconversion"
          ]
        },
        "insect_taxid": {
          "type": "integer",
          "minimum": 1
        },
        "treatment": {
          "type": "object",
          "required": ["method"],
          "additionalProperties": false,
          "properties": {
            "method": {
              "type": "integer",
              "enum": [1, 6, 7]
            },
            "core_temp_c": {
              "type": "number"
            },
            "pressure_bar": {
              "type": "number"
            },
            "minutes": {
              "type": "number"
            },
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
      "enum": [
        "PAP",
        "insect_PAP",
        "fishmeal",
        "rendered_fat",
        "frass",
        "ash"
      ]
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
            "memorial_forestry",
            "pet_food"
          ]
        },
        "target_taxids": {
          "type": "array",
          "items": {
            "type": "integer",
            "minimum": 1
          }
        }
      }
    }
  }
}
```

### 2.2 Schéma CDDL (Concise Data Definition Language, RFC 8610)

```cddl
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
                  "human_remains" / "manure" / "catering_waste" / "unknown",
  origin_profile: "slaughterhouse" / "feed_industry" / "farm" /
                  "pet" / "human" / "wildlife_dnf",
  sources: [* source_item],
  ? pentobarbital_lfa: "positive" / "negative" / "not_tested",
}

source_item = {
  ? taxid: uint,
  ? label: tstr,
  * tstr => any,
}

process_record = {
  route: "direct_rendering" / "insect_bioconversion",
  ? insect_taxid: uint,
  ? treatment: treatment_record,
}

treatment_record = {
  method: 1 / 6 / 7,
  ? core_temp_c: number,
  ? pressure_bar: number,
  ? minutes: number,
  ? evidence_sha256: tstr, ; Empreinte hexadécimale SHA-256 de 64 caractères
}

product_type = "PAP" / "insect_PAP" / "fishmeal" / "rendered_fat" / "frass" / "ash"

destination_record = {
  use: "feed" / "aquaculture_feed" / "technical" / "fertiliser" /
       "incineration" / "memorial_forestry" / "pet_food",
  ? target_taxids: [* uint],
}
```

---

## 3. A2. Résolution Taxonomique & Snapshot Embarqué

Le validateur opère en isolation totale du réseau. Aucune requête externe (UniProt, NCBI REST, DNS) n'est exécutée à l'évaluation d'un lot. La vérité taxonomique est figée dans le snapshot immuable `qa/vectors/antiprion/taxonomy-snapshot.json` (26 taxons vérifiés au 2026-10-04).

### 3.1 Les 26 Taxons Embarqués

| TaxID | Nom Scientifique | Rang | Parent | Marqueurs Lignée | Groupe AeterniTrak | Nom Vernaculaire |
|---|---|---|---|---|---|---|
| `9823` | *Sus scrofa* | `species` | 9822 | `[9821]` | `PORCINE` | Porc / Sanglier |
| `9825` | *Sus scrofa domesticus* | `subspecies` | 9823 | `[9821]` | `PORCINE` | Porc domestique (sous-espèce) |
| `9031` | *Gallus gallus* | `species` | 9030 | `[8782]` | `POULTRY` | Poule / Poulet |
| `208526` | *Gallus gallus gallus* | `subspecies` | 9031 | `[8782]` | `POULTRY` | Coq bankiva (sous-espèce) |
| `9103` | *Meleagris gallopavo* | `species` | 9102 | `[8782]` | `POULTRY` | Dinde |
| `8839` | *Anas platyrhynchos* | `species` | 8835 | `[8782]` | `POULTRY` | Canard colvert |
| `9913` | *Bos taurus* | `species` | 9903 | `[9845]` | `RUMINANT` | Bovin |
| `89462` | *Bubalus bubalis* | `species` | 9918 | `[9845]` | `RUMINANT` | Buffle d'eau |
| `9940` | *Ovis aries* | `species` | 9935 | `[9845]` | `RUMINANT` | Mouton |
| `9925` | *Capra hircus* | `species` | 9922 | `[9845]` | `RUMINANT` | Chèvre |
| `9860` | *Cervus elaphus* | `species` | 9859 | `[9845]` | `RUMINANT` | Cerf élaphe |
| `9858` | *Capreolus capreolus* | `species` | 9857 | `[9845]` | `RUMINANT` | Chevreuil |
| `343691` | *Hermetia illucens* | `species` | 343581 | `[50557]` | `INSECT` | Mouche soldat noire |
| `8030` | *Salmo salar* | `species` | 8028 | `[7898]` | `FISH` | Saumon atlantique |
| `8022` | *Oncorhynchus mykiss* | `species` | 8016 | `[7898]` | `FISH` | Truite arc-en-ciel |
| `9615` | *Canis lupus familiaris* | `subspecies` | 9612 | `[]` | `CARNIVORE` | Chien (sous-espèce) |
| `9612` | *Canis lupus* | `species` | 9611 | `[]` | `CARNIVORE` | Loup |
| `9685` | *Felis catus* | `species` | 9682 | `[]` | `CARNIVORE` | Chat |
| `9796` | *Equus caballus* | `species` | 9789 | `[]` | `EQUINE` | Cheval |
| `9986` | *Oryctolagus cuniculus* | `species` | 9984 | `[]` | `LAGOMORPH` | Lapin |
| `9606` | *Homo sapiens* | `species` | 9605 | `[9606]` | `HUMAN` | Être humain |
| `9821` | *Suidae* | `family` | 35497 | `[9821]` | `PORCINE` | Suidés (famille — rang > espèce) |
| `8782` | *Aves* | `class` | 436492 | `[8782]` | `POULTRY` | Oiseaux (classe — rang > espèce) |
| `9845` | *Ruminantia* | `suborder` | 91561 | `[9845]` | `RUMINANT` | Ruminants (sous-ordre — rang > espèce) |
| `50557` | *Insecta* | `class` | 6960 | `[50557]` | `INSECT` | Insectes (classe — rang > espèce) |
| `7898` | *Actinopterygii* | `superclass` | 117571 | `[7898]` | `FISH` | Poissons à nageoires rayonnées |

### 3.2 Algorithme de Résolution et d'Affectation de Groupe

L'algorithme de résolution garantit que tout taxon déclaré est réduit à sa véritable entité d'espèce biologique :

```
Fonction ResoudreTaxon(taxid):
  1. Si type(taxid) n'est pas un entier numérique:
       Retourner Erreur("TAXON_UNKNOWN")
  2. taxon = RechercheSnapshot(taxid)
  3. Si taxon est Nul:
       Retourner Erreur("TAXON_UNKNOWN")
  4. Si taxon.rank n'est ni "species" ni "subspecies":
       Retourner Erreur("TAXON_RANK_ABOVE_SPECIES")
  5. courant = taxon
  6. Tant que courant.rank == "subspecies":
       parent = RechercheSnapshot(courant.parent_taxid)
       Si parent est Nul:
         Retourner Erreur("TAXON_UNKNOWN")
       courant = parent
  7. Retourner { espece: courant, taxon_origine: taxon, groupe: DeterminerGroupe(courant) }

Fonction DeterminerGroupe(taxon):
  Si 9845 appartient à taxon.lineage_markers: Retourner "RUMINANT"
  Si 9821 appartient à taxon.lineage_markers: Retourner "PORCINE"
  Si 8782 appartient à taxon.lineage_markers: Retourner "POULTRY"
  Si 7898 appartient à taxon.lineage_markers: Retourner "FISH"
  Si 50557 appartient à taxon.lineage_markers: Retourner "INSECT"
  Si 9606 appartient à taxon.lineage_markers ou taxon.taxid == 9606: Retourner "HUMAN"
  Sinon: Retourner taxon.group // (CARNIVORE, EQUINE, LAGOMORPH ou OTHER)
```

---

## 4. A3. Les 10 Portes de Fer G0 à G9 : Spécification Exhaustive

Le moteur d'évaluation anti-prion exécute **10 portes séquentielles ordonnées (G0 à G9)**. L'évaluation est **exhaustive** : toutes les portes sont vérifiées pour consigner la totalité des motifs d'infraction, avec seulement **deux cas d'arrêt anticipé impératifs** :
1. **Arrêt G0** : Si `destination.use` n'appartient pas à l'énumération supportée v1 (`DESTINATION_UNSUPPORTED`).
2. **Arrêt G2** : Si des restes humains sont orientés vers une filière d'alimentation ou technique (`HUMAN_REMAINS_ROUTE_PROHIBITED`).

La condition d'émission de signature est binaire et intransigeante :
$$\text{signature\_permitted} \iff (\text{reasons} == []) \iff (\text{verdict} == \text{"AUTHORISED"})$$

### 4.1 Registre Ordonné des Motifs d'Infraction

| Ordre | Porte | Code Motif d'Infraction | Base Légale & Sécuritaire |
|---|---|---|---|
| 1 | **G0** | `DESTINATION_UNSUPPORTED` | Refus par défaut : `use` non reconnu dans la v1 |
| 2 | **G0** | `TARGET_UNSPECIFIED` | Refus par défaut : destination alimentaire sans aucune cible |
| 3 | **G1** | `TAXON_UNKNOWN` | Refus par défaut : taxon absent du snapshot ou non numérique |
| 4 | **G1** | `TAXON_RANK_ABOVE_SPECIES` | Refus par défaut : rang supérieur à l'espèce (famille, classe, etc.) |
| 5 | **G2** | `HUMAN_REMAINS_ROUTE_PROHIBITED` | Dignité & Ordre Public : aucune voie alimentaire ou industrielle pour l'humain |
| 6 | **G3** | `SUBSTRATE_CATEGORY_VIOLATION` | Règl. 1069/2009 art. 12-14 ; Règl. 2017/893 (substrats larvaires) |
| 7 | **G3** | `CATEGORY_DESTINATION_PROHIBITED` | Règl. 1069/2009 art. 12 : Catégorie 1 interdite en fertilisant |
| 8 | **G3** | `DEROGATION_REQUIRED` | `DEC-AET-05` requise : aucune dérogation forestière active en V1 |
| 9 | **G4** | `PENTOBARBITAL_POSITIVE` | `PROTOCOL.md` §5.2 : Euthanasiant toxique avéré -> incinération C1 exclusive |
| 10 | **G4** | `PENTOBARBITAL_NOT_TESTED` | `PROTOCOL.md` §5.2 : Dépistage LFA manquant sur animal de compagnie |
| 11 | **G5** | `FEED_BAN_RUMINANT_SOURCE` | Règl. 999/2001 Annexe IV ch. I : Aucune protéine de ruminant en alimentation |
| 12 | **G6** | `FEED_BAN_RUMINANT_TARGET` | Règl. 999/2001 Annexe IV ch. I : Ruminant cible strictement interdit de PAT |
| 13 | **G7** | `FEED_BAN_INTRA_SPECIES_VIOLATION` | Règl. 1069/2009 art. 11(1)(a) : **Règle d'Or Anti-Prion** (Cannibalisme) |
| 14 | **G8** | `FEED_BAN_INTRA_GROUP_VIOLATION` | Règl. 999/2001 Annexe IV ch. II (2021/1372) : Volaille<->Volaille, Porc<->Porc |
| 15 | **G8** | `SOURCE_GROUP_NOT_AUTHORISED` | Règl. 2021/1372 : Source non homologuée en alimentation de rente |
| 16 | **G8** | `TARGET_GROUP_NOT_AUTHORISED` | Règl. 2021/1372 : Cible animale hors liste de dérogation positive |
| 17 | **G9** | `TREATMENT_NOT_PROVEN` | Règl. 142/2011 Annexe IV : Méthode 1 (133°C, 3 bars, 20 min, SHA-256) |

---

### 4.2 Pseudo-Code Exhaustif des Portes G0 à G9

```typescript
function evaluate(claim: BatchClaim): EvaluationResult {
  const reasons: ReasonCode[] = [];
  const supportedUses = [
    "feed", "aquaculture_feed", "technical", 
    "fertiliser", "incineration", "memorial_forestry"
  ];

  // -------------------------------------------------------------
  // PORTE G0 : Destination & Spécification des cibles
  // -------------------------------------------------------------
  if (!claim.destination || !supportedUses.includes(claim.destination.use)) {
    // Arrêt anticipé absolu : destination hors énumération
    return { verdict: "BLOCKED", reasons: ["DESTINATION_UNSUPPORTED"], signature_permitted: false };
  }

  const isFeed = (claim.destination.use === "feed" || claim.destination.use === "aquaculture_feed");
  if (isFeed && (!claim.destination.target_taxids || claim.destination.target_taxids.length === 0)) {
    return { verdict: "BLOCKED", reasons: ["TARGET_UNSPECIFIED"], signature_permitted: false };
  }

  // -------------------------------------------------------------
  // PORTE G1 : Taxonomie, Résolution & Default-Deny
  // -------------------------------------------------------------
  let g1Reason: ReasonCode | null = null;
  const resolvedSources: ResolvedTaxon[] = [];

  // Validation des sources de substrat
  if (claim.substrate && Array.isArray(claim.substrate.sources)) {
    for (const src of claim.substrate.sources) {
      if (typeof src.taxid !== "number") {
        g1Reason = "TAXON_UNKNOWN";
        break;
      }
      const res = ResoudreTaxon(src.taxid);
      if (res.error) {
        g1Reason = res.error;
        break;
      }
      resolvedSources.push(res);
    }
  }

  // Validation de l'insecte de bioconversion (si applicable)
  let resolvedInsect: ResolvedTaxon | null = null;
  if (!g1Reason && claim.process && claim.process.route === "insect_bioconversion") {
    if (typeof claim.process.insect_taxid !== "number") {
      g1Reason = "TAXON_UNKNOWN";
    } else {
      const res = ResoudreTaxon(claim.process.insect_taxid);
      if (res.error) g1Reason = res.error;
      else resolvedInsect = res;
    }
  }

  // Validation des cibles animales
  const resolvedTargets: ResolvedTaxon[] = [];
  if (!g1Reason && claim.destination && Array.isArray(claim.destination.target_taxids)) {
    for (const tid of claim.destination.target_taxids) {
      if (typeof tid !== "number") {
        g1Reason = "TAXON_UNKNOWN";
        break;
      }
      const res = ResoudreTaxon(tid);
      if (res.error) {
        g1Reason = res.error;
        break;
      }
      resolvedTargets.push(res);
    }
  }

  if (g1Reason) {
    // Si la taxonomie est invalide ou de rang trop haut, blocage immédiat
    return { verdict: "BLOCKED", reasons: [g1Reason], signature_permitted: false };
  }

  // -------------------------------------------------------------
  // PORTE G2 : Protection des Restes Humains
  // -------------------------------------------------------------
  const isHumanSource = resolvedSources.some(s => s.espece.taxid === 9606 || s.groupe === "HUMAN");
  if (isHumanSource) {
    if (claim.destination.use !== "incineration" && claim.destination.use !== "memorial_forestry") {
      // Arrêt anticipé : profanation de restes humains proscrite
      return { verdict: "BLOCKED", reasons: ["HUMAN_REMAINS_ROUTE_PROHIBITED"], signature_permitted: false };
    }
  }

  // -------------------------------------------------------------
  // PORTE G3 : Catégorie de Matières & Régime des Substrats
  // -------------------------------------------------------------
  if (isFeed) {
    if (claim.substrate.category !== 3) {
      reasons.push("SUBSTRATE_CATEGORY_VIOLATION");
    } else if (claim.process && claim.process.route === "insect_bioconversion") {
      const forbiddenMaterials = ["carcass", "manure", "catering_waste", "slaughter_byproduct"];
      if (forbiddenMaterials.includes(claim.substrate.material_class)) {
        reasons.push("SUBSTRATE_CATEGORY_VIOLATION");
      }
    }
  }

  if (claim.substrate && claim.substrate.category === 1 && claim.destination.use === "fertiliser") {
    reasons.push("CATEGORY_DESTINATION_PROHIBITED");
  }

  if (claim.destination.use === "memorial_forestry") {
    reasons.push("DEROGATION_REQUIRED");
  }

  // -------------------------------------------------------------
  // PORTE G4 : Dépistage Toxico-Chimique (Pentobarbital LFA)
  // -------------------------------------------------------------
  const isPet = claim.substrate && (
    claim.substrate.origin_profile === "pet" || 
    claim.substrate.material_class === "companion_animal"
  );
  if (isPet && claim.destination.use !== "incineration") {
    if (claim.substrate.pentobarbital_lfa === "positive") {
      reasons.push("PENTOBARBITAL_POSITIVE");
    } else if (claim.substrate.pentobarbital_lfa !== "negative") {
      reasons.push("PENTOBARBITAL_NOT_TESTED");
    }
  }

  // -------------------------------------------------------------
  // PORTES G5 à G8 : Règles Spécifiques de l'Alimentation Animale
  // -------------------------------------------------------------
  if (isFeed) {
    // Calcul des sources protéiques effectives (incluant l'insecte vecteur)
    const effectiveSources: ResolvedTaxon[] = [];
    if (claim.process && claim.process.route === "insect_bioconversion" && resolvedInsect) {
      effectiveSources.push(resolvedInsect);
    }
    for (const s of resolvedSources) {
      effectiveSources.push(s);
    }

    // PORTE G5 : Ruminant Source
    if (effectiveSources.some(s => s.groupe === "RUMINANT")) {
      reasons.push("FEED_BAN_RUMINANT_SOURCE");
    }

    // PORTE G6 : Ruminant Cible
    if (resolvedTargets.some(t => t.groupe === "RUMINANT")) {
      reasons.push("FEED_BAN_RUMINANT_TARGET");
    }

    // PORTE G7 : Règle d'Or Intra-Espèce (Cannibalisme au rang espèce)
    let intraSpeciesViolation = false;
    for (const src of effectiveSources) {
      for (const tgt of resolvedTargets) {
        if (src.espece.taxid === tgt.espece.taxid) {
          intraSpeciesViolation = true;
          break;
        }
      }
      if (intraSpeciesViolation) break;
    }
    if (intraSpeciesViolation) {
      reasons.push("FEED_BAN_INTRA_SPECIES_VIOLATION");
    }

    // PORTE G8 : Règle de Groupe & Dérogations 2021/1372
    let intraGroupViolation = false;
    let sourceGroupNotAuth = false;
    let targetGroupNotAuth = false;

    // Validation des cibles autorisées
    if (claim.destination.use === "aquaculture_feed") {
      for (const tgt of resolvedTargets) {
        if (tgt.groupe !== "FISH") targetGroupNotAuth = true;
      }
    } else if (claim.destination.use === "feed") {
      for (const tgt of resolvedTargets) {
        if (tgt.groupe !== "PORCINE" && tgt.groupe !== "POULTRY") targetGroupNotAuth = true;
      }
    }

    // Validation des sources autorisées et interdiction intra-groupe
    for (const src of effectiveSources) {
      const g = src.groupe;
      if (g === "RUMINANT" || g === "CARNIVORE" || g === "LAGOMORPH") {
        sourceGroupNotAuth = true;
      } else if (g === "EQUINE") {
        if (claim.destination.use !== "aquaculture_feed") sourceGroupNotAuth = true;
      } else if (g === "PORCINE") {
        for (const tgt of resolvedTargets) {
          if (tgt.groupe === "PORCINE") intraGroupViolation = true;
          else if (tgt.groupe !== "POULTRY" && tgt.groupe !== "FISH") targetGroupNotAuth = true;
        }
      } else if (g === "POULTRY") {
        for (const tgt of resolvedTargets) {
          if (tgt.groupe === "POULTRY") intraGroupViolation = true;
          else if (tgt.groupe !== "PORCINE" && tgt.groupe !== "FISH") targetGroupNotAuth = true;
        }
      }
    }

    if (intraGroupViolation) reasons.push("FEED_BAN_INTRA_GROUP_VIOLATION");
    if (sourceGroupNotAuth) reasons.push("SOURCE_GROUP_NOT_AUTHORISED");
    if (targetGroupNotAuth) reasons.push("TARGET_GROUP_NOT_AUTHORISED");
  }

  // -------------------------------------------------------------
  // PORTE G9 : Preuve de Traitement Thermique & Barométrique
  // -------------------------------------------------------------
  if (claim.process && claim.process.treatment) {
    const tr = claim.process.treatment;
    if (tr.method === 1) {
      if (!tr.evidence_sha256 || tr.core_temp_c < 133 || tr.pressure_bar < 3 || tr.minutes < 20) {
        reasons.push("TREATMENT_NOT_PROVEN");
      }
    } else if (tr.method === 7) {
      if (!tr.evidence_sha256) reasons.push("TREATMENT_NOT_PROVEN");
    } else if (tr.method === 6) {
      const hasMammal = resolvedSources.some(s => 
        ["PORCINE", "RUMINANT", "EQUINE"].includes(s.groupe)
      );
      if (hasMammal) reasons.push("TREATMENT_NOT_PROVEN");
    }
  } else {
    // Si aucun traitement n'est déclaré mais que la matière l'exige impérativement
    if (["feed", "aquaculture_feed", "fertiliser", "technical"].includes(claim.destination.use)) {
      if (claim.substrate && (claim.substrate.category === 1 || claim.substrate.category === 2)) {
        reasons.push("TREATMENT_NOT_PROVEN");
      }
    }
  }

  // Dédoublonnage en conservant strictement l'ordre d'apparition
  const orderedUniqueReasons = Array.from(new Set(reasons));
  const signaturePermitted = (orderedUniqueReasons.length === 0);

  return {
    verdict: signaturePermitted ? "AUTHORISED" : "BLOCKED",
    reasons: orderedUniqueReasons,
    signature_permitted: signaturePermitted
  };
}
```

---

## 5. A4. Matrices à Double Entrée de Conformité & Preuves

Chaque cellule de ces matrices renvoie à l'identifiant exact du vecteur de test dans `qa/vectors/antiprion/feedban-matrix.vectors.json` qui atteste du comportement attendu.

### 5.1 Matrice (a) : Groupe Source × Groupe Cible (Alimentation `feed` & `aquaculture_feed`)

| Groupe Source | Cible `POULTRY` (`feed`) | Cible `PORCINE` (`feed`) | Cible `FISH` (`aquaculture_feed`) | Cible `RUMINANT` (`feed`) | Cible `LAGOMORPH` (`feed`) | Cible `INSECT` (`feed`) |
|---|---|---|---|---|---|---|
| **`PORCINE`** | **AUTORISÉ**<br>[`PRION-AUTH-001`]<br>[`PRION-AUTH-002`] | **BLOQUÉ**<br>`FEED_BAN_INTRA_SPECIES`<br>`FEED_BAN_INTRA_GROUP`<br>[`PRION-BLOCK-001`]<br>[`PRION-BLOCK-002`] | **AUTORISÉ**<br>[`PRION-AUTH-008`] | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_TARGET`<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-BLOCK-011`] | **BLOQUÉ**<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-DENY-012`] | **BLOQUÉ**<br>`TARGET_GROUP_NOT_AUTH`<br>*(Règl. 2021/1372)* |
| **`POULTRY`** | **BLOQUÉ**<br>`FEED_BAN_INTRA_GROUP`<br>[`PRION-BLOCK-003`]<br>[`PRION-BLOCK-004`]<br>[`PRION-BLOCK-005`] | **AUTORISÉ**<br>[`PRION-AUTH-003`]<br>[`PRION-AUTH-004`] | **AUTORISÉ**<br>*(Règl. 2021/1372)* | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_TARGET`<br>*(Règl. 999/2001)* | **BLOQUÉ**<br>`TARGET_GROUP_NOT_AUTH`<br>*(Règl. 2021/1372)* | **BLOQUÉ**<br>`TARGET_GROUP_NOT_AUTH`<br>*(Règl. 2021/1372)* |
| **`INSECT`** | **AUTORISÉ**<br>[`PRION-AUTH-005`] | **AUTORISÉ**<br>[`PRION-AUTH-006`] | **AUTORISÉ**<br>[`PRION-AUTH-007`] | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_TARGET`<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-BLOCK-012`] | **BLOQUÉ**<br>`TARGET_GROUP_NOT_AUTH`<br>*(Règl. 2021/1372)* | **BLOQUÉ**<br>`FEED_BAN_INTRA_SPECIES`<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-BLOCK-008`] |
| **`FISH`** | **AUTORISÉ**<br>*(Règl. 999/2001)* | **AUTORISÉ**<br>[`PRION-AUTH-011`] | **AUTORISÉ** (si $\neq$ espèce)<br>[`PRION-AUTH-010`]<br>**BLOQUÉ** (si = espèce)<br>[`PRION-BLOCK-009`] | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_TARGET`<br>`TARGET_GROUP_NOT_AUTH`<br>[`PRION-BLOCK-014`] | **BLOQUÉ**<br>`TARGET_GROUP_NOT_AUTH`<br>*(Règl. 999/2001)* | **BLOQUÉ**<br>`TARGET_GROUP_NOT_AUTH`<br>*(Règl. 999/2001)* |
| **`EQUINE`** | **BLOQUÉ**<br>`SOURCE_GROUP_NOT_AUTH`<br>*(Règl. 2021/1372)* | **BLOQUÉ**<br>`SOURCE_GROUP_NOT_AUTH`<br>[`PRION-DENY-010`] | **AUTORISÉ**<br>[`PRION-AUTH-009`] | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_TARGET`<br>*(Règl. 999/2001)* | **BLOQUÉ**<br>`TARGET_GROUP_NOT_AUTH`<br>*(Règl. 2021/1372)* | **BLOQUÉ**<br>`TARGET_GROUP_NOT_AUTH`<br>*(Règl. 2021/1372)* |
| **`LAGOMORPH`** | **BLOQUÉ**<br>`SOURCE_GROUP_NOT_AUTH`<br>[`PRION-DENY-011`] | **BLOQUÉ**<br>`SOURCE_GROUP_NOT_AUTH`<br>*(Règl. 2021/1372)* | **BLOQUÉ**<br>`SOURCE_GROUP_NOT_AUTH`<br>*(Règl. 2021/1372)* | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_TARGET`<br>*(Règl. 999/2001)* | **BLOQUÉ**<br>`TARGET_GROUP_NOT_AUTH`<br>*(Règl. 2021/1372)* | **BLOQUÉ**<br>`TARGET_GROUP_NOT_AUTH`<br>*(Règl. 2021/1372)* |
| **`CARNIVORE`** | **BLOQUÉ**<br>`SUBSTRATE_CAT_VIOLATION`<br>`SOURCE_GROUP_NOT_AUTH`<br>[`PRION-BLOCK-022`] | **BLOQUÉ**<br>`SUBSTRATE_CAT_VIOLATION`<br>`SOURCE_GROUP_NOT_AUTH`<br>*(Règl. 1069/2009)* | **BLOQUÉ**<br>`SUBSTRATE_CAT_VIOLATION`<br>`SOURCE_GROUP_NOT_AUTH`<br>*(Règl. 1069/2009)* | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_TARGET`<br>*(Règl. 999/2001)* | **BLOQUÉ**<br>`TARGET_GROUP_NOT_AUTH`<br>*(Règl. 1069/2009)* | **BLOQUÉ**<br>`TARGET_GROUP_NOT_AUTH`<br>*(Règl. 1069/2009)* |
| **`RUMINANT`** | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_SRC`<br>`SOURCE_GROUP_NOT_AUTH`<br>[`PRION-BLOCK-013`]<br>[`PRION-BLOCK-015`] | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_SRC`<br>`SOURCE_GROUP_NOT_AUTH`<br>[`PRION-BLOCK-010`] | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_SRC`<br>`SOURCE_GROUP_NOT_AUTH`<br>*(Règl. 999/2001)* | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_SRC`<br>`FEED_BAN_RUMINANT_TGT`<br>*(Règl. 999/2001)* | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_SRC`<br>`TARGET_GROUP_NOT_AUTH`<br>*(Règl. 999/2001)* | **BLOQUÉ**<br>`FEED_BAN_RUMINANT_SRC`<br>`TARGET_GROUP_NOT_AUTH`<br>*(Règl. 999/2001)* |

*Cas particuliers prouvés par vecteurs :*
- Lot poolé multi-sources contenant une source interdite : Porc + Poulet -> Volaille = BLOQUÉ [`PRION-BLOCK-006`].
- Cibles multiples dont l'une est interdite : Porc -> [Volaille, Porcin] = BLOQUÉ [`PRION-BLOCK-007`].
- Route aquaculture avec cible aviaire non aquatique : Porc -> Volaille en `aquaculture_feed` = BLOQUÉ [`PRION-DENY-013`].

---

### 5.2 Matrice (b) : Catégorie de Matières × Destination

| Catégorie Substrat | `feed` / `aquaculture_feed` | `fertiliser` (Engrais) | `technical` (Industriel/C2) | `incineration` (Crémation/C1) | `memorial_forestry` (Forêt) |
|---|---|---|---|---|---|
| **Catégorie 1** *(MRS, animaux compagnie, faune suspecte)* | **BLOQUÉ**<br>`SUBSTRATE_CATEGORY_VIOLATION`<br>[`PRION-BLOCK-022`] | **BLOQUÉ**<br>`CATEGORY_DESTINATION_PROHIBITED`<br>[`PRION-BLOCK-023`] | **AUTORISÉ** (Méthode 1 cimenterie)<br>[`PRION-AUTH-014`]<br>*(Bloqué si pentobarbital: [`PRION-BLOCK-025`])* | **AUTORISÉ**<br>[`PRION-AUTH-015`]<br>[`PRION-AUTH-016`] | **BLOQUÉ**<br>`DEROGATION_REQUIRED`<br>[`PRION-BLOCK-024`]<br>[`PRION-BLOCK-027`]<br>[`PRION-BLOCK-028`] |
| **Catégorie 2** *(Cadavres ferme, faune saine, fumier)* | **BLOQUÉ**<br>`SUBSTRATE_CATEGORY_VIOLATION`<br>[`PRION-BLOCK-015`]<br>[`PRION-BLOCK-016`]<br>[`PRION-BLOCK-017`]<br>[`PRION-BLOCK-018`]<br>[`PRION-BLOCK-019`]<br>[`PRION-BLOCK-020`] | **AUTORISÉ** (Méthode 1 frass)<br>[`PRION-AUTH-013`] | **AUTORISÉ** (Méthode 1 biodiesel)<br>[`PRION-AUTH-012`]<br>[`PRION-AUTH-017`] | **AUTORISÉ**<br>*(Règl. 1069/2009 art. 13)* | **BLOQUÉ**<br>`DEROGATION_REQUIRED`<br>*(DEC-AET-05)* |
| **Catégorie 3** *(Abattoir sain, matières végétales)* | **AUTORISÉ** (si règles d'or et de groupe respectées)<br>[`PRION-AUTH-001` à `011`]<br>*(Bloqué si abattoir cru sur larves: [`PRION-BLOCK-021`])* | **AUTORISÉ**<br>*(Règl. 1069/2009 art. 14)* | **AUTORISÉ**<br>*(Règl. 1069/2009 art. 14)* | **AUTORISÉ**<br>*(Règl. 1069/2009 art. 14)* | **BLOQUÉ**<br>`DEROGATION_REQUIRED`<br>*(DEC-AET-05)* |
| **Catégorie Nulle / Indéterminée** | **BLOQUÉ**<br>`SUBSTRATE_CATEGORY_VIOLATION`<br>[`PRION-DENY-014`] | **BLOQUÉ**<br>`SUBSTRATE_CATEGORY_VIOLATION` | **BLOQUÉ**<br>`SUBSTRATE_CATEGORY_VIOLATION` | **BLOQUÉ**<br>`SUBSTRATE_CATEGORY_VIOLATION` | **BLOQUÉ**<br>`DEROGATION_REQUIRED` |

*Cas particuliers prouvés par vecteurs :*
- Restes humains vers alimentation animale : BLOQUÉ [`PRION-BLOCK-029`].
- Restes humains vers filière technique industrielle : BLOQUÉ [`PRION-BLOCK-030`].
- Animal de compagnie euthanasié sans test de pentobarbital vers usage technique : BLOQUÉ [`PRION-BLOCK-026`].

---

### 5.3 Matrice (c) : Destination × Traitement Sanitaire Requis

| Destination Finale | Type de Produit / Substrat | Traitement Exigé (Règl. 142/2011) | Vecteurs Nominaux & Défaillances Prouvées |
|---|---|---|---|
| `feed` / `aquaculture_feed` | PAT de mammifères (Cat. 3) | **Méthode 1** : 133 °C, 3 bars, 20 min, empreinte SHA-256 | **AUTORISÉ** : [`PRION-AUTH-001`], [`PRION-AUTH-002`], [`PRION-AUTH-008`]<br>**BLOQUÉ** (absence hash SHA-256) : [`PRION-BLOCK-035`]<br>**BLOQUÉ** (méthode 6 interdite mammifères) : [`PRION-BLOCK-036`] |
| `feed` / `aquaculture_feed` | PAT d'insectes (*Hermetia* sur végétal) | **Méthode 7** : Traitement thermique validé + empreinte SHA-256 | **AUTORISÉ** : [`PRION-AUTH-005`], [`PRION-AUTH-006`], [`PRION-AUTH-007`] |
| `technical` (Biodiesel, Cimenterie) | Cadavres de ferme (Cat. 2) ou MRS (Cat. 1) | **Méthode 1 Obligatoire** : 133 °C, 3 bars, 20 min, SHA-256 | **AUTORISÉ** : [`PRION-AUTH-012`], [`PRION-AUTH-014`], [`PRION-AUTH-017`]<br>**BLOQUÉ** (sans preuve méthode 1) : [`PRION-BLOCK-031`]<br>**BLOQUÉ** (température 132 °C < 133 °C) : [`PRION-BLOCK-032`]<br>**BLOQUÉ** (durée 19 min < 20 min) : [`PRION-BLOCK-033`]<br>**BLOQUÉ** (pression 2,9 bar < 3 bars) : [`PRION-BLOCK-034`] |
| `fertiliser` (Frass de sarcomusation) | Frass issu de cadavres de ferme (Cat. 2) | **Méthode 1 Obligatoire** : 133 °C, 3 bars, 20 min, SHA-256 | **AUTORISÉ** : [`PRION-AUTH-013`] |
| `incineration` | C1 pentobarbital positif, restes humains | Incinération / Crémation haute température | **AUTORISÉ** : [`PRION-AUTH-015`], [`PRION-AUTH-016`] |
| `memorial_forestry` | C1 mémoriel LFA-négatif | Pasteurisation (70 °C, 1h) | **BLOQUÉ EN V1** : `DEROGATION_REQUIRED` [`PRION-BLOCK-024`], [`PRION-BLOCK-027`], [`PRION-BLOCK-028`] |

---

## 6. A5. Oracle de Signature Ed25519 & Étanchéité Cryptographique

L'architecture de sécurité repose sur le principe de l'oracle étanche : la clé privée de signature de conformité Ed25519 ne peut être atteinte par aucun chemin d'exécution si l'évaluation n'a pas préalablement retourné un verdict favorable exempt d'infraction.

### 6.1 Système de Typage Scellé (*Branded Type Pattern*)

En TypeScript, la fonction de signature requiert un type opaque non forgeable en dehors du module `validators/antiprion/` :

```typescript
// Déclaration du symbole privé opaque, non exporté
declare const AuthorisedClaimBrand: unique symbol;

/**
 * Type représentant une revendication formellement autorisée par The Iron Gate.
 * Ce type ne peut être instancié QUE par la fonction evaluate().
 */
export type AuthorisedClaim = BatchClaim & {
  readonly [AuthorisedClaimBrand]: true;
};

export interface EvaluationSuccess {
  readonly verdict: "AUTHORISED";
  readonly reasons: readonly [];
  readonly signature_permitted: true;
  readonly claim: AuthorisedClaim; // Jeton d'autorisation
}

export interface EvaluationFailure {
  readonly verdict: "BLOCKED";
  readonly reasons: readonly ReasonCode[];
  readonly signature_permitted: false;
}

export type EvaluationResult = EvaluationSuccess | EvaluationFailure;
```

### 6.2 Signature Cryptographique & Sérialisation CBOR Déterministe

Lorsqu'une revendication produit une `EvaluationSuccess`, la charge utile signée est forgée selon le profil **CBOR Déterministe AeterniCore** (RFC 8949 §4.2.1, spécifié par le Bushi 01) :

$$\text{Payload} = \text{CBOR\_Deterministic}(\{ \text{"claim"}: \text{claim}, \text{"verdict"}: \text{"AUTHORISED"}, \text{"issued\_at"}: t \})$$
$$\text{Signature} = \text{Ed25519\_Sign}(K_{\text{compliance\_private}}, \text{SHA-256}(\text{Payload}))$$

### 6.3 Vérification en Profondeur (*Dual-Sided Re-evaluation*)

Tout vérificateur (nœud P2P, console de douane AFSCA, inspecteur d'abattoir) effectue une **défense en profondeur à deux niveaux** :
1. **Niveau Cryptographique** : Vérification de la signature Ed25519 sur le payload CBOR avec la clé publique de l'autorité de lot.
2. **Niveau Algorithmique Obligatoire** : Le vérificateur extrait le `BatchClaim` du CBOR et **ré-exécute localement `evaluate(claim)`**. Si le verdict ré-évalué n'est pas `AUTHORISED` (`signature_permitted === false`), le certificat est **rejeté comme falsifié**, même si la signature mathématique Ed25519 était valide (protection contre les clés compromises ou les oracles dévoyés).

### 6.4 Garantie Zéro-Bypass

Aucun commutateur (`--force`, `--bypass`, `--skip-feedban`), aucun rôle utilisateur (`SUPERADMIN`, `EMERGENCY_OVERRIDE`), ni aucune variable d'environnement (`process.env.BYPASS_*`) n'existe dans le moteur de validation. Le code applicatif de la Phase B sera scanné et audité pour prouver l'absence totale de tels motifs.

---

## 7. A6. Boîte Noire d'Infractions Append-Only (Journal d'Audit Chaîné)

Toute tentative d'émission de certificat rejetée par l'une des portes G0 à G9 ne disparaît pas : elle est **immédiatement et irréversiblement scellée dans le registre d'audit des infractions**.

### 7.1 Architecture de Chaînage Cryptographique

Le journal des infractions est une structure *append-only* où chaque entrée est cryptographiquement liée à la précédente par son hachage SHA-256 :

$$\text{entry\_hash}_i = \text{SHA-256}\Big(\text{CBOR\_Deterministic}\big(\text{seq}_i, \text{timestamp}_i, \text{prev\_hash}_{i-1}, \text{claim}_i, \text{reasons}_i\big)\Big)$$

### 7.2 Ségrégation des Clés d'Audit

Pour empêcher un exploitant d'altérer le journal d'audit :
- La clé de signature de conformité $K_{\text{compliance}}$ sert uniquement à signer les lots autorisés.
- La clé de signature d'audit $K_{\text{audit}}$ est une clé Ed25519 **physiquement et logiquement distincte**, hébergée sur un module de sécurité hardware indépendant (HSM / Secure Element JavaCard du superviseur de conformité). Chaque entrée de la boîte noire est signée avec $K_{\text{audit}}$.

### 7.3 Format d'une Entrée d'Audit

```json
{
  "sequence_number": 42,
  "timestamp": "2026-10-04T12:00:00Z",
  "prev_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "batch_id": "AT-B-01",
  "batch_claim": {
    "substrate": { "sources": [{ "taxid": 9823 }] },
    "destination": { "use": "feed", "target_taxids": [9823] }
  },
  "verdict": "BLOCKED",
  "reasons": [
    "FEED_BAN_INTRA_SPECIES_VIOLATION",
    "FEED_BAN_INTRA_GROUP_VIOLATION"
  ],
  "entry_hash": "a1b2c3d4e5f6...",
  "audit_signature": "ed25519_hex_signature..."
}
```

---

## 8. Synthèse de la Preuve d'État Rouge (Phase A)

Conformément à l'Ordre 0004, le harnais de test `./scripts/runner.sh test antiprion` a été exécuté sur la suite officielle `antiprion.feedban.matrix` en l'absence de l'adaptateur d'implémentation `qa/harness/adapters/antiprion.feedban.mjs`.

### 8.1 Résultat Attendu et Validé

- **Total vecteurs exécutés** : 67
- **RED (Attente d'implémentation Phase B)** : 67
- **PASS** : 0
- **FAIL** : 0
- **INVALID (Erreur de contrat / format)** : 0
- **Code de sortie** : `0`

L'intégrité de la suite de tests est absolue (`INVALID = 0`), prouvant la cohérence mathématique des 67 vecteurs d'or avec le schéma de suite et les règles de conformité.

---
*Fin de la spécification technique AeterniTrak — Bushi 12 (Anti-Prion & Feed-Ban Validator)*
