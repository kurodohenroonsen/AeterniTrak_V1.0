> « Avertissement de gouvernance : Ces études sont rédigées par des agents techniques. Elles préparent une question à poser à un juriste ou à l'autorité compétente ; elles ne la remplacent pas. »

# Spécification Prospective d'Architecture V2 — Intégration des Contrôles Amonts et Étanchéité Profil ↔ Catégorie (PROPOSAL)

> **Référence normative** : `AET-SPEC-UPSTREAM-V2-PROP-001`  
> **Auteurs** : Bushi 11 (Bio-Traçabilité & Filière Vétérinaire), Bushi 12 (Sécurité Sanitaire Anti-Prion / The Iron Gate), Orchestrateur Antigravity  
> **Date de publication** : 5 octobre 2026  
> **Statut du document** : **Proposition d'Architecture Technique Prospective (PROPOSAL)**  
> **Décision Souveraine rattachée** : `DEC-AET-13` (Spec-First & Test-First pour les contrôles amonts)  
> **Garantie d'intégrité** : **Zéro modification de code et zéro altération des vecteurs normatifs V1 existants** (693/693 tests PASS préservés).

---

## 1. Contexte, Motivation Métier & Arbitrage Souverain DEC-AET-13

### 1.1 Contexte et Objet de la Proposition
L'écosystème **AeterniTrak V1.0** intègre un moteur déterministe d'évaluation cryptographique des risques sanitaires et prions dénommé **The Iron Gate** (spécifié dans [`docs/technical/antiprion-feedban.md`](antiprion-feedban.md)). Ce moteur évalue formellement 10 portes de fer séquentielles ordonnées (**G0 à G9**) sur une charge utile structurée (`BatchClaimInput`), garantissant l'application stricte de la Règle d'Or Anti-Prion (Règlement CE n° 999/2001 et Règlement CE n° 1069/2009).

Dans la version V1.0 actuelle, plusieurs contrôles de terrain et exigences administratives indispensables à la filière globale sont traités de façon **déclarative et amont** au niveau logistique :
1. Les dépistages par PCR des épizooties de la faune sauvage (Peste Porcine Africaine - PPA sur sangliers, Maladie du Dépérissement Chronique - CWD sur cervidés) ;
2. Le contrôle des temps d'attente médicamenteux et de l'identification Sanitel / CERISE pour les animaux de ferme ;
3. Le Document Commercial AFSCA et la dénaturation chimique au bleu de méthylène 0,5% pour les Déchets d'Abattoir (Catégorie 1 / MRS) ;
4. La validation formelle de l'étanchéité stricte entre le profil d'origine de la dépouille (`origin_profile`) et la catégorie européenne de sous-produits animaux (`substrate.category`).

### 1.2 Arbitrage Souverain DEC-AET-13
Face à la tentation d'injecter prématurément ces contrôles dans le validateur figé sans couverture de test préalable, Kudoro a prononcé l'arbitrage souverain `DEC-AET-13` le 5 octobre 2026 :
> **Kudoro** : *« Oui : spec d'abord, puis vecteurs approuvés par Claude, puis code. »*
> **Portée** : Les contrôles amont restent déclaratifs dans les documentations actuelles tant qu'une spécification formelle (`docs/technical/antiprion-upstream-controls-PROPOSAL.md`) et une suite de vecteurs normatifs n'auront pas été approuvées par Claude AI (Master Verifier). Aucun code direct non couvert par vecteurs approuvés n'est introduit dans `evaluator.ts`.

Le présent document constitue formellement cette spécification d'architecture préalable.

### 1.3 Pourquoi ces Contrôles sont Traités en Amont en V1.0
La décision de maintenir ces contrôles au niveau logistique et administratif en V1.0 repose sur trois fondements d'ingénierie logicielle et réglementaire :
1. **Nature physique et temporelle des opérations de terrain** :  
   Un prélèvement PCR de faune sauvage par un agent du DNF en forêt ardennaise, la vérification physique d'une boucle auriculaire Sanitel en bétaillère ou la vérification visuelle d'un badigeon au bleu de méthylène en abattoir sont des actes physiques amonts. Ils se déroulent plusieurs heures voire plusieurs jours avant la préparation du lot de bioconversion ou de traitement thermique.
2. **Absence d'APIs publiques ouvertes pour les guichets officiels (DEC-AET-02)** :  
   Comme l'a formellement établi l'étude technique [`docs/technical/registry-apis.md`](registry-apis.md), aucun des quatre registres publics cibles (CERISE, Sanitel/ARSIA, DogID/CatID, SPW DNF) ne dispose d'une API publique ouverte sans convention bilatérale d'homologation préalable. Le validateur cryptographique V1.0 devant opérer de manière 100 % déterministe et autonome (y compris en environnement hors-ligne ou sur terminal durci), il ne peut dépendre d'appels réseau synchrones vers des services tiers indisponibles.
3. **Immuabilité et reproductibilité du cœur cryptographique V1.0** :  
   Le moteur `The Iron Gate` V1.0 est validé par 693 tests unitaires et d'intégration à l'état de l'art (100% PASS). Modifier sa logique interne ou son schéma de signature romprait la reproductibilité historique des certificats de lot déjà scellés.

---

## 2. Spécification des 4 Profils de Dépouilles et des Contrôles Amonts

AeterniTrak structure la filière de collecte et de traitement autour de 4 profils de dépouilles distincts, conformément à [`bushi/bushi-11-bio-traceability.md`](../../bushi/bushi-11-bio-traceability.md) et [`docs/functional/app4-filiere-sarcomusation.md`](../functional/app4-filiere-sarcomusation.md).

```
                      +---------------------------------------+
                      | Dépouille / Matière Première Entrante |
                      +---------------------------------------+
                                          |
        +------------------+--------------+-------------+--------------------+
        |                  |                            |                    |
        v                  v                            v                    v
+---------------+  +-------------------+        +---------------+    +-------------------+
|   Profil 1    |  |     Profil 2      |        |   Profil 3    |    |     Profil 4      |
|  Compagnie    |  |   Faune Sauvage   |        | Ferme/Élevage |    | Déchets Abattoir  |
| (Cat 1 Mém.)  |  | (Cat 1/2 Biocont) |        | (Catégorie 2) |    |  (Cat 1 / MRS)    |
+---------------+  +-------------------+        +---------------+    +-------------------+
        |                  |                            |                    |
        v                  v                            v                    v
  [Test LFA Pento]   [Badge DNF + GPS]           [Boucle Sanitel]     [Doc Comm AFSCA]
  (Binaire Neg)      [PCR PPA / CWD]             [Temps d'attente]    [Bleu Méthylène]
        |                  |                            |                    |
        v                  v                            v                    v
  Pasteurisation     Stérilisation Méthode 1     Stérilisation M1     Stérilisation M1
   (70°C, 1h)         (133°C, 3b, 20min)        (133°C, 3b, 20min)   (133°C, 3b, 20min)
        |                  |                            |                    |
        v                  v                            v                    v
Arbre Souvenir       Aiguillage Technique         Aiguillage B2B       Combustion Ind.
(DEC-AET-05)         / Cimenterie / Biofuel       Biodiesel C2         Cimenterie Excl.
```

### 2.1 Profil 1 : Animaux de Compagnie (Catégorie 1 Mémoriel)
- **Base légale** : Règlement (CE) n° 1069/2009 article 8 (sous-produits animaux de Catégorie 1) et Arrêté royal du 27 avril 2007 (référence à confirmer par un juriste).
- **Contrôle amont obligatoire** :
  - **Dépistage LFA du Pentobarbital (`UC-403`)** : Test qualitatif à flux latéral réalisé sur carcasse à l'arrivée au centre de réception.
  - Résultat binaire : si `POSITIVE`, réorientation immédiate vers l'incinération haute température exclusive sans bioconversion (`PRION-AUTH-015`). Si `NEGATIVE`, admission en sarcomusation dédiée.
- **Traitement thermique imposé** : Pasteurisation thermique validée à **70 °C pendant 60 minutes continues** en cœur de matière (`UC-404`, Règlement CE n° 142/2011).
- **Destination autorisée** : Amendement d'arbres du souvenir en forêts cinéraires privées (`UC-405`), sous dérogation administrative expresse (`DEC-AET-05`). Interdiction absolue et algorithmique de réintroduction dans la chaîne alimentaire ou agricole.

### 2.2 Profil 2 : Faune Sauvage (Catégorie 1/2 Biocontrôle DNF)
- **Base légale** : Règlement (CE) n° 1069/2009 articles 8 et 9, protocole sanitaire SPW ARNE — Département de la Nature et des Forêts (DNF).
- **Contrôles amonts obligatoires** :
  - **Badgeage et traçabilité de collecte (`UC-406`)** : Enregistrement de l'identifiant de badge de l'agent forestier assermenté DNF, bracelet physique inviolable sur la carcasse, horodatage UTC et géolocalisation GPS WGS84 du point de collecte.
  - **Dépistages PCR Épizooties en laboratoire agréé (`UC-407`)** :
    * Suidés sauvages (*Sus scrofa*, TaxID 9823) : PCR Peste Porcine Africaine (PPA / African Swine Fever). Tout résultat positif entraîne le confinement immédiat et l'incinération sous scellés sanitaires de l'autorité compétente.
    * Cervidés (*Cervidae*, TaxID 9850, incluant chevreuils TaxID 9886 et cerfs TaxID 9874) : PCR Maladie du Dépérissement Chronique (CWD / Chronic Wasting Disease). Tout résultat positif entraîne le blocage total pour suspicion d'encéphalopathie spongiforme transmissible.
- **Traitement thermique imposé** : Stérilisation européenne **Méthode 1** (**133 °C, 3 bars, 20 minutes** en continu sans interruption sous vapeur saturée, `UC-408`, Règlement CE n° 142/2011 annexe IV chapitre III).
- **Destination autorisée** : Débouchés techniques hors chaîne alimentaire humaine et animale (combustion industrielle, cimenterie, biodiesel technique).

### 2.3 Profil 3 : Animaux de Ferme & Élevage (Catégorie 2)
- **Base légale** : Règlement (CE) n° 1069/2009 article 9 (Catégorie 2 — animaux morts d'élevage ne relevant pas de la Catégorie 1).
- **Contrôles amonts obligatoires** :
  - **Identification auriculaire Sanitel & CERISE (`UC-409`, `UC-410`)** : Vérification de la boucle auriculaire officielle, conciliation avec l'identifiant d'exploitation Sanitel (ARSIA / DGZ) et la fiche sanitaire d'exploitation.
  - **Contrôle des temps d'attente médicamenteux** : Vérification de l'absence de résidus thérapeutiques vétérinaires (antibiotiques, antiparasitaires, anesthésiques) non purgés au moment de la mort, ou qualification expresse en risque chimique imposant le confinement.
- **Traitement thermique imposé** : Stérilisation européenne **Méthode 1** obligatoire (`UC-408`).
- **Destination autorisée** : Aiguillage B2B technique exclusif : biodiesel de Catégorie 2, cimenteries, combustion thermique industrielle. Débouché fertilisant sous réserve d'évaluation spécifique. Interdiction absolue en alimentation animale (feed ban).

### 2.4 Profil 4 : Déchets d'Abattoir (Catégorie 1 / Matériaux à Risques Spécifiés MRS)
- **Base légale** : Règlement (CE) n° 999/2001 annexe V et Règlement (CE) n° 1069/2009 article 8 (MRS : crânes, moelle épinière, amygdales, rate, etc. de ruminants).
- **Contrôles amonts obligatoires** :
  - **Document Commercial AFSCA (`UC-411`)** : Accompagnement obligatoire d'un Document Commercial officiel normalisé pour le transport des sous-produits animaux de Catégorie 1, précisant l'abattoir d'origine, le numéro d'agrément vétérinaire, la quantité et la date d'enlèvement.
  - **Dénaturation chimique au bleu de méthylène 0,5% m/v** : Vérification physique du marquage indélébile par coloration au bleu de méthylène de l'ensemble des matières MRS, empêchant toute tentative de détournement ou de réintroduction frauduleuse.
- **Traitement thermique imposé** : Stérilisation européenne **Méthode 1** obligatoire (`UC-408`).
- **Destination autorisée** : Incinération ou co-incinération directe en cimenterie agréée, ou transformation en biodiesel industriel Catégorie 1. **Bioconversion par larves d'Hermetia illucens formellement interdite sur ce profil**.

---

## 3. Formalisation de la Règle G3 Profil ↔ Catégorie (Étanchéité Réglementaire)

La porte de fer **G3** (`docs/technical/antiprion-feedban.md` §4) est actuellement dédiée au contrôle de la catégorie du substrat larvaire et de la dérogation forestière :
- `SUBSTRATE_CATEGORY_VIOLATION`
- `CATEGORY_DESTINATION_PROHIBITED`
- `DEROGATION_REQUIRED`

Dans l'architecture V2 proposée, la porte G3 est enrichie de la règle formelle d'étanchéité **Profil ↔ Catégorie** afin d'interdire toute incohérence taxonomique ou fraude d'aiguillage entre le profil opérationnel déclaré et la catégorie de sous-produits animaux.

### 3.1 Matrice d'Étanchéité Profil ↔ Catégorie

| Profil Opérationnel (`origin_profile`) | Catégories SPA Admissibles (`substrate.category`) | Bioconversion Larvaire Autorisée ? | Traitement Thermique Minimal Exigé | Motif d'Infraction en cas de Violation |
| :--- | :---: | :---: | :--- | :--- |
| `pet` *(Compagnie mémoriel)* | `cat1` exclusivement | OUI (Dédiée) | Pasteurisation 70°C, 1h | `PROFILE_CATEGORY_MISMATCH` |
| `wildlife` *(Faune sauvage DNF)* | `cat1`, `cat2` | OUI (Sous condition) | Méthode 1 (133°C, 3b, 20min) | `PROFILE_CATEGORY_MISMATCH` |
| `farm` *(Ferme / Élevage)* | `cat2` exclusivement | OUI (Technique) | Méthode 1 (133°C, 3b, 20min) | `PROFILE_CATEGORY_MISMATCH` |
| `slaughterhouse_waste` *(MRS)* | `cat1` exclusivement | **NON** (Interdiction absolue) | Méthode 1 (133°C, 3b, 20min) | `PROFILE_CATEGORY_MISMATCH` ou `SUBSTRATE_CATEGORY_VIOLATION` |
| `human_remains` *(Démonstrateur)* | *Non catégorisé SPA* | Prospective recherche | Incinération / Crémation | `HUMAN_REMAINS_ROUTE_PROHIBITED` (G2) |

### 3.2 Règles d'Incompatibilité Absolue
1. **Règle P-G3-A (Compagnie non-déclassable)** : Un profil `pet` ne peut en aucun cas être déclaré en `cat2` ou `cat3`. Tout animal de compagnie relève par principe de la Catégorie 1 mémorielle.
2. **Règle P-G3-B (Élevage non-reclassable)** : Une carcasse d'élevage `farm` morte sur l'exploitation ne peut être étiquetée `cat3` (réservée aux matières saines d'abattoir déclarées propres à la consommation mais écartées pour des motifs commerciaux).
3. **Règle P-G3-C (Étanchéité MRS)** : Les déchets d'abattoir `slaughterhouse_waste` contenant des MRS sont obligatoirement `cat1` et ne peuvent recevoir aucune destination biologique larvaire.

---

## 4. Modèle de Données V2 (`BatchClaimInputV2`) & Préservation de la Rétrocompatibilité V1

Pour respecter scrupuleusement la règle de non-régression et préserver l'exécution des 693 tests normatifs existants, le modèle V2 adopte une approche par **extension non intrusive**.

### 4.1 Extension Optionnelle du Schéma de Revendication (`upstream_controls`)

La structure `BatchClaimInput` V1 est étendue par un champ optionnel `upstream_controls`.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://aeternitrak.org/schemas/batch-claim-v2-proposal.json",
  "title": "BatchClaimInputV2",
  "description": "Revendication d'intégrité de lot avec contrôles amonts (Proposition V2)",
  "type": "object",
  "properties": {
    "claim_version": { "type": "string", "enum": ["1.0", "2.0"] },
    "batch_id": { "type": "string" },
    "origin_profile": {
      "type": "string",
      "enum": ["pet", "wildlife", "farm", "slaughterhouse_waste", "human"]
    },
    "substrate": {
      "type": "object",
      "properties": {
        "category": { "type": "string", "enum": ["cat1", "cat2", "cat3", "feed_grade_plant"] },
        "material_class": { "type": "string" },
        "sources": { "type": "array" }
      },
      "required": ["category"]
    },
    "upstream_controls": {
      "type": "object",
      "description": "Données certifiées des contrôles amonts (Requis en version 2.0)",
      "properties": {
        "pet_lfa": {
          "type": "object",
          "properties": {
            "test_kit_lot": { "type": "string" },
            "tested_at": { "type": "string", "format": "date-time" },
            "result": { "type": "string", "enum": ["negative", "positive"] },
            "operator_id": { "type": "string" }
          },
          "required": ["result", "test_kit_lot"]
        },
        "dnf_biocontrol": {
          "type": "object",
          "properties": {
            "ranger_badge_id": { "type": "string" },
            "collection_gps": {
              "type": "object",
              "properties": {
                "latitude": { "type": "number", "minimum": -90, "maximum": 90 },
                "longitude": { "type": "number", "minimum": -180, "maximum": 180 }
              },
              "required": ["latitude", "longitude"]
            },
            "pcr_screenings": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "target_disease": { "type": "string", "enum": ["PPA", "CWD"] },
                  "lab_accreditation": { "type": "string" },
                  "analysis_date": { "type": "string", "format": "date-time" },
                  "result": { "type": "string", "enum": ["negative", "positive"] }
                },
                "required": ["target_disease", "result"]
              }
            }
          },
          "required": ["ranger_badge_id", "collection_gps"]
        },
        "farm_sanitel": {
          "type": "object",
          "properties": {
            "ear_tag_id": { "type": "string" },
            "sanitel_holding_id": { "type": "string" },
            "drug_withdrawal_cleared": { "type": "boolean" },
            "veterinary_attestation_ref": { "type": "string" }
          },
          "required": ["ear_tag_id", "sanitel_holding_id", "drug_withdrawal_cleared"]
        },
        "slaughterhouse_mrs": {
          "type": "object",
          "properties": {
            "afsca_commercial_doc_id": { "type": "string" },
            "methylene_blue_denaturation_verified": { "type": "boolean" },
            "slaughterhouse_approval_number": { "type": "string" }
          },
          "required": ["afsca_commercial_doc_id", "methylene_blue_denaturation_verified"]
        }
      }
    }
  },
  "required": ["batch_id", "origin_profile", "substrate"]
}
```

### 4.2 Principe d'Exécution Tolérante et Rétrocompatibilité
1. **Mode V1 par défaut (Compatibilité stricte)** :  
   Lorsque `claim_version` est égal à `"1.0"` ou non spécifié, le validateur ignore l'absence du bloc `upstream_controls`. Les vérifications des portes G0 à G9 s'exécutent selon la logique V1 figée sans lever de nouveau code d'erreur. Les 693 tests normatifs du harnais s'exécutent sans aucune régression.
2. **Mode V2 explicite (Contrôles amonts activés)** :  
   Lorsque `claim_version === "2.0"`, le validateur active la sous-routine `evaluateUpstreamControls()` avant la signature cryptographique du certificat de lot. Tout manquement ou résultat positif non conforme lève le code d'infraction V2 correspondant.

---

## 5. Spécification Préparatoire des Vecteurs de Test V2 (Spec-First)

Conformément à la consigne `DEC-AET-13`, la présente spécification liste les motifs d'infraction prévus pour la suite de vecteurs V2 à soumettre au Master Verifier Claude AI :

| Code Motif d'Infraction V2 Anticipé | Description Métier | Condition de Déclenchement |
| :--- | :--- | :--- |
| `PROFILE_CATEGORY_MISMATCH` | Incompatibilité formelle entre le profil d'origine et la catégorie SPA | Profil `pet` déclaré en `cat2`/`cat3` ou profil `farm` déclaré en `cat1`/`cat3`. |
| `UPSTREAM_PPA_POSITIVE` | Détection d'épizootie PPA sur faune sauvage | Sanglier sauvage dont la PCR PPA en laboratoire agréé est positive. |
| `UPSTREAM_CWD_POSITIVE` | Détection de prion CWD sur faune sauvage | Cervidé sauvage dont la PCR CWD en laboratoire agréé est positive. |
| `UPSTREAM_DNF_TRACE_MISSING` | Absence de traçabilité d'agent ou GPS | Dépouille de faune sauvage sans badge DNF ou sans géolocalisation de collecte. |
| `UPSTREAM_SANITEL_CLEARANCE_MISSING` | Délai médicamenteux non purgé en élevage | Animal de ferme dont `drug_withdrawal_cleared` est faux ou non attesté. |
| `UPSTREAM_AFSCA_DOC_MISSING` | Absence de Document Commercial officiel | Lot de déchets d'abattoir Cat 1 sans identifiant de document commercial AFSCA. |
| `UPSTREAM_METHYLENE_BLUE_ABSENT` | Absence de dénaturation chimique certifiée | Lot de MRS d'abattoir sans validation du marquage au bleu de méthylène 0,5%. |

---

## 6. Conclusion et Feuille de Route d'Intégration (Spec-First & Test-First)

Cette proposition architecturale pose les fondations rigoureuses de la version 2.0 d'AeterniTrak sans enfreindre la stabilité du socle V1.0 :
1. **Étape 1 (Réalisée)** : Rédaction et publication de la spécification prospective `docs/technical/antiprion-upstream-controls-PROPOSAL.md` (le présent document).
2. **Étape 2 (Prochaine étape)** : Rédaction du jeu d'essais normatif `qa/vectors/filiere/v2-upstream-controls.vectors.json` modélisant les 7 cas de rejet et les 4 cas nominaux.
3. **Étape 3** : Soumission de la spécification et des vecteurs pour revue formelle par **Claude AI (Master Verifier)** via la boîte aux lettres Git (`agent-mailbox`).
4. **Étape 4** : Implémentation du moteur de validation amont dans un sous-module isolé (`core/filiere/upstream-v2.ts`) avec adaptateur de harnais dédié, sans toucher au fichier figé `core/antiprion/evaluator.ts`.
