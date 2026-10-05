# Application 4 — Filière Sarcomusation & Traçabilité Post-Décès (UC-401 à UC-414)

**Système Expert de Contrôle Biologique, Régulation Sanitaire & The Iron Gate**

> [!NOTE]
> **Périmètre Applicatif :**
> L'application **Filière Sarcomusation & Traçabilité** régit l'intégralité de la chaîne biologique de biodégradation par les larves d'***Hermetia illucens*** (mouche soldat noire). Utilisée par les vétérinaires légistes, les gardes-forestiers DNF et les inspecteurs sanitaires AFSCA, elle assure la ségrégation stricte des 4 profils de dépouilles (Compagnie, Faune sauvage DNF, Élevage agricole Sanitel, Déchets d'abattoir MRS), le dépistage toxicologique qualitatif LFA du pentobarbital (absence de molécule détectée, lignes C et T visibles), la stérilisation thermique obligatoire (Méthode 1 : 133°C, 3 bars, 20 min ou pasteurisation 70°C/1h), et le filtrage déterministe infranchissable **The Iron Gate (portes G0 à G9)** garantissant le respect absolu de la **règle d'or anti-prion** (feed-ban européen interdisant tout recyclage intraspécifique).

## 📌 Sommaire des Micro Use-Cases Spécifiés

| ID | Titre du Cas d'Usage | Catégorie Métier | Acteur | Plateformes | Référence Normative |
| :---: | :--- | :--- | :--- | :--- | :--- |
| [`UC-401`](#uc-401) | [Constat Médical Initial & Aiguillage des 4 Filières Post-Décès](#uc-401) | **Constat Civil & Tri** | Vétérinaire Sanitaire & Conseiller | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Règlement (CE) n° 1069/2009 (règles sanitaires applicables aux sous-produits animaux) (référence à confirmer par un juriste). |
| [`UC-402`](#uc-402) | [Profil 1 — Filière Compagnie (Catégorie 1 Mémoriel) & Ségrégation](#uc-402) | **Profils Dépouilles** | Opérateur de Bioconversion | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Arrêté royal du 27 avril 2007 (règles sanitaires pour les cadavres d'animaux de compagnie) (référence à confirmer par un juriste). |
| [`UC-403`](#uc-403) | [Dépistage Toxicologique Qualitatif LFA du Pentobarbital](#uc-403) | **Contrôle Biologique** | Vétérinaire & Opérateur | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Directive The Iron Gate G4 et normes de sécurité toxicologique vétérinaire AFSCA (référence à confirmer par un juriste). |
| [`UC-404`](#uc-404) | [Pasteurisation Thermique Mémorielle (70°C, 1 heure continue)](#uc-404) | **Traitement Thermique** | Opérateur de Traitement Thermique | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Règlement (CE) n° 142/2011 (normes de transformation pour sous-produits animaux) (référence à confirmer par un juriste). |
| [`UC-405`](#uc-405) | [Valorisation Forestière Cinéraire sous Dérogation DEC-AET-05](#uc-405) | **Destination Finale** | Garde Forestier DNF & Famille | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Décret wallon du 15 juillet 2008 (Code forestier art. 41) et Dérogation souveraine DEC-AET-05 (référence à confirmer par un juriste). |
| [`UC-406`](#uc-406) | [Profil 2 — Filière Faune Sauvage (Cat 1/2 DNF) : Badge & GPS](#uc-406) | **Profils Dépouilles** | Garde Forestier DNF | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Décret wallon du 15 juillet 2008 relatif au Code forestier (missions de police sylvicole des agents DNF) (référence à confirmer par un juriste). |
| [`UC-407`](#uc-407) | [Dépistages PCR Épizooties en Laboratoire Agréé (PPA & CWD)](#uc-407) | **Contrôle Biologique** | Biologiste de Laboratoire Agréé (Sciensano) | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Règlement d'exécution (UE) 2021/605 (mesures spéciales de lutte contre la peste porcine africaine) (référence à confirmer par un juriste). |
| [`UC-408`](#uc-408) | [Stérilisation Européenne Méthode 1 (133°C, 3 bars, 20 minutes)](#uc-408) | **Traitement Thermique** | Opérateur d'Autoclave Haute Pression | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Règlement (CE) n° 142/2011 (annexe IV, chapitre III - Méthode 1 de transformation standard) (référence à confirmer par un juriste). |
| [`UC-409`](#uc-409) | [Profil 3 — Filière Élevage / Ferme (Catégorie 2) & Boucle Sanitel](#uc-409) | **Profils Dépouilles** | Éleveur & Vétérinaire Sanitaire | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Arrêté royal du 23 mars 2011 (identification et enregistrement des bovins dans le système Sanitel) (référence à confirmer par un juriste). |
| [`UC-410`](#uc-410) | [Ingestion Automatisée APIs Sanitel & CERISE (Traçabilité Élevage)](#uc-410) | **Interopérabilité APIs** | Système Core & Autorité AFSCA | Node.js / Core Engine, Web Standard (PWA Hors-Ligne) | Arrêté ministériel du 28 juin 2013 (modalités d'accès et d'échange de données avec le système Sanitel) (référence à confirmer par un juriste). |
| [`UC-411`](#uc-411) | [Profil 4 — Filière Déchets d'Abattoir (Cat 1 MRS) & Dénaturation Bleu](#uc-411) | **Profils Dépouilles** | Inspecteur AFSCA & Opérateur d'Abattoir | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Règlement (CE) n° 999/2001 (annexe V - spécifications des Matériels à Risque Spécifié MRS) (référence à confirmer par un juriste). |
| [`UC-412`](#uc-412) | [Évaluation Algorithmique Pure par The Iron Gate (G0 à G9, Anti-Prion)](#uc-412) | **Validation Algorithmique** | The Iron Gate (Moteur Déterministe) | Node.js / Core Engine, Web Standard (PWA Hors-Ligne) | Spécification AeterniTrak AET-SPEC-PRION-001 et Règlement (CE) n° 999/2001 (Feed-ban) (référence à confirmer par un juriste). |
| [`UC-413`](#uc-413) | [Émission du Certificat de Lot Signé Ed25519 (AET-SPEC-CERT-001)](#uc-413) | **Cryptographie Filière** | The Iron Gate & Autorité de Conformité | Node.js / Core Engine, Web Standard (PWA Hors-Ligne) | Spécification technique formelle AET-SPEC-CERT-001 et Règlement (UE) 2021/1372 (référence à confirmer par un juriste). |
| [`UC-414`](#uc-414) | [Double Audit Réglementaire AFSCA / DNF Hors-Ligne](#uc-414) | **Audit & Régulateurs** | Inspecteur AFSCA & Contrôleur DNF | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Règlement (UE) 2017/625 (contrôles officiels le long de la chaîne agroalimentaire) (référence à confirmer par un juriste). |

---

## ⛓️ Chaîne Événementielle Complète de Traçabilité Post-Mortem (Événements 1 à 6)

Cette chaîne événementielle régit l'intégralité du cycle post-mortem de la dépouille, garantissant une traçabilité sans faille, de l'instant du décès jusqu'au scellement cryptographique Ed25519 final et à la remise mémorielle, articulée rigoureusement **lieu par lieu** selon la réglementation funéraire et sanitaire belge et européenne.

### 🏛️ Matrice Événementielle Globale (Lieu par Lieu)

| Étape | Événement Clé | Lieu Réglementaire | Acteur Principal | Statut Scellé | Température / Thermique | Résumé & Enjeux Sanitaires | UCs Liés |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Constat de Décès & Déclaration Initiale** (`EVT-01`) | **Domicile du déclarant / Clinique (Liège)** | Officier de Santé / Autorité Agréée | `SCEL_INITIALISE_NON_ROMPU` | 12.4°C (Température ambiante initiale) | Constat médical de fin de vie, horodatage certifié RFC 3339, géolocalisation par balise RTK, vérification de l'identité du défunt ou de l'animal, et scellement physique et cryptographique immédiat par scellé inviolable NFC/QR à signature Ed25519. | [`UC-401`](#uc-401), [`UC-406`](#uc-406), [`UC-409`](#uc-409) |
| **2** | **Prise en Charge & Transport Sécurisé de la Dépouille** (`EVT-02`) | **Itinéraire Transit Agréé E25 (Rocade Sud)** | Conducteur Spécialisé Véhicule Agréé | `SCEL_INTACT_EN_TRANSIT` | +3.2°C (Chaîne du Froid Conforme [Consigne 2.0°C - 4.0°C]) | Prise en charge dans un véhicule funéraire/sanitaire agréé, monitoring télématique continu de la température de la chaîne du froid entre 2°C et 4°C, étapes de transit géolocalisées avec horodatage balises GPS et émargement numérique du chauffeur. | [`UC-401`](#uc-401), [`UC-406`](#uc-406), [`UC-409`](#uc-409) |
| **3** | **Admission & Réception à l'Unité / Salon Funéraire** (`EVT-03`) | **Unité Centrale AeterniTrak Liège (Cellule #B4)** | Gestionnaire d'Unité Funéraire & Sanitaire | `SCEL_VERIFIE_NON_ROMPU` | +2.8°C (Cellule Frigorifique #B4 Assignée) | Arrivée à l'unité de destination : scan sans contact du scellé inviolable, vérification de non-rupture de scellé, pesée métrologique certifiée sur balance étalonnée classe III, et assignation automatique d'une cellule réfrigérée de conservation. | [`UC-402`](#uc-402), [`UC-410`](#uc-410) |
| **4** | **Préparation Sanitaire & Contrôles Amonts** (`EVT-04`) | **Salle Technique Stérile & BioLab AeterniCore** | Praticien Spécialiste Santé & Sécurité | `SCEL_OUVERT_CONTROLE_STERILE` | +14.0°C (Ambiante salle technique stérile) | Préparation sanitaire amont obligatoire : exérèse validée du stimulateur cardiaque (pacemaker) avant toute incinération ou traitement thermique, dépistage toxicologique qualitatif LFA du pentobarbital (cassette C+T visibles = absence de produit létal, conforme), et prélèvements PCR épizooties selon le profil de dépouille. | [`UC-403`](#uc-403), [`UC-407`](#uc-407), [`UC-411`](#uc-411) |
| **5** | **Bioconversion / Sarcomusation & Traitement Thermique** (`EVT-05`) | **Sas Hermétique de Bioconversion & Autoclaves HP** | Responsable Unité Biologique & Thermique | `SAS_BIOCONVERSION_SCELLE` | 70.2°C (Pasteurisation continue 1h) / Méthode 1: 133°C, 3 bars | Introduction dans le sas hermétique de bioconversion dédié par les larves d'Hermetia illucens, ségrégation stricte des flux pour interdire tout mélange, et application du traitement thermique légal : pasteurisation continue à 70°C pendant 1h continue sous dérogation DEC-AET-05 mémorielle forestière exclusive, ou stérilisation Méthode 1 européenne (133°C, 3 bars, 20 min en cœur de matière) pour les autres filières. | [`UC-402`](#uc-402), [`UC-404`](#uc-404), [`UC-408`](#uc-408) |
| **6** | **Clôture de Traçabilité, The Iron Gate & Remise Mémorielle** (`EVT-06`) | **Salon Solennel d'Hommage & Forêt DNF** | Autorité Cryptographique & Conseiller Funéraire | `LOT_SIGNE_ET_REMIS` | Température ambiante salon d'hommage | Évaluation algorithmique pure et inviolable par l'oracle The Iron Gate (G0 à G9 : vérification stricte de la règle d'or anti-prion interdisant tout recyclage intra-espèce), scellement cryptographique Ed25519 du certificat de lot AET-SPEC-CERT-001 (COSE_Sign1), séparation méticuleuse des reliques et remise solennelle de l'urne cinéraire ou de l'amendement forestier à la famille. | [`UC-405`](#uc-405), [`UC-412`](#uc-412), [`UC-413`](#uc-413), [`UC-414`](#uc-414) |

### 👤 Profil Humain (`p0`) — Traçabilité Funéraire Légale & Démonstrateur Prospectif (DEC-AET-15)

Le Profil Humain (`p0`) modélise la prise en charge d'un sujet de droit (ex. *Guy Heyman, 1942 — 2026, Matricule État Civil #NAM-2026-0814*, dépouille `AET-HUM-2026-BE-0814`) selon le cadre légal belge (Loi du 20 juillet 1971, Décret wallon du 6 mars 2009 modifiant le CDLD, Art. L1232-17 §2 - références à confirmer par un juriste) :

1. **Événement 1 (Survenance)** : Domicile / Chambre d'hôpital (Namur) — Médecin traitant/légiste (Certificat Modèle III C/D), visa d'absence d'obstacle médico-légal, registre SPF Santé Publique (don d'organes, consentement présumé), bracelet inviolable poignet Ed25519 (`SCL-HUM-2026-INIT`).
2. **Événement 2 (Transport Primaire)** : Trajet Domicile ➔ Salon PaxFunèbre (N4 Namur) — Fourgon SPW #1-PFN-884, caisson isotherme (0°C..+4°C), autorisation communale de transport avant mise en bière (< 24h/48h sous froid).
3. **Événement 3 (Salon & Thanatopraxie)** : Funérarium PaxFunèbre (Cellule #C3, Namur) — **Exérèse chirurgicale OBLIGATOIRE du stimulateur cardiaque (Pacemaker / DAE) selon Art. L1232-17 §2 CDLD (danger d'explosion > 250°C et lithium)**, attestation médicale INAMI, mise en bière cercueil agréé.
4. **Événement 4 (Maison Communale)** : Hôtel de Ville de Namur — Acte de décès n° 0814/2026, contrôle des dernières volontés (Loi 1971 / Art. 15 CDLD), permis officiel de crémation/sépulture, scellement municipal du cercueil.
5. **Événement 5 (Transformation)** : Crématorium de Ciney (850°C) OU Bioréacteur démonstrateur prospectif Hermetia illucens (pasteurisation 70°C/1h, DEC-AET-05/15) — **Verrou absolu The Iron Gate Gate G2 (`HUMAN_REMAINS_DETECTED` ➔ interdiction mathématique de toute filière alimentaire/technique)**.
6. **Événement 6 (Sépulture & Clôture)** : Forêt Cinéraire Privée de la Basse-Sambre (Parcelle #FM-08) — Remise solennelle Médaillon ACOSJ 92 Ko (hommage et mémo vocal), amendement biologique au pied de l'arbre du souvenir familial (DEC-AET-05), scellement Ed25519 du certificat de sépulture final (`AET-SPEC-CERT-001`).


---

<a id="uc-401"></a>
## UC-401 : Constat Médical Initial & Aiguillage des 4 Filières Post-Décès

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-401` |
| **Catégorie Métier** | **Constat Civil & Tri** |
| **Acteur Principal** | Vétérinaire Sanitaire & Conseiller |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `Aiguillage`, `Triage`, `4Filieres`, `Constat`, `Biosecurite` |
| **Base Légale & Normative** | Règlement (CE) n° 1069/2009 (règles sanitaires applicables aux sous-produits animaux) (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `Terminal Terrain DNF / AFSCA • Triage Sanitaire Initial (IP68)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Arrivée d'une dépouille animale au centre de collecte ou constat en exploitation.

> [!TIP]
> **Postconditions Garanties :**
> Dépouille affectée de manière irrévocable à sa filière réglementaire, zéro risque de contamination croisée.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Ouverture du terminal industriel AeterniTrak par le vétérinaire sanitaire agréé.
2. Saisie des données biométriques et cliniques initiales : identification de l'espèce (TaxID NCBI), cause présumée de la mort, antécédents médicaux.
3. Aiguillage algorithmique strict vers l'une des 4 filières étanches :
4. - Profil 1 : Compagnie (Catégorie 1 mémorielle exclusive)
5. - Profil 2 : Faune Sauvage (Catégorie 1/2 DNF avec badge et GPS)
6. - Profil 3 : Élevage / Ferme (Catégorie 2 avec boucle Sanitel)
7. - Profil 4 : Déchets d'Abattoir (Catégorie 1 MRS avec dénaturation bleue)
8. Génération du dossier numérique de traçabilité scellé in-silico.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `depouille_id` | **Identifiant Unique Dépouille** | `text` | `DEP-2026-BEL-99201 (Génération Automatique)` | ID Dépouille | `RFID / QR` | ⭕ Optionnel |
| `species_taxid` | **Taxonomie Espèce (NCBI)** | `select` | `Canis familiaris (TaxID 9615 - Chien de Compagnie)` | Espèce | `TaxID 9615` | ✅ Requis |
| `cause_death` | **Cause du Décès** | `select` | `Fin de vie naturelle / Vieillesse (Absence d'épizootie)` | Cause | `Clinique` | ✅ Requis |
| `channel_assigned` | **Aiguillage Réglementaire** | `text` | `PROFIL 1 : Compagnie (Catégorie 1 Mémoriel Exclusif)` | Filière | `Profil 1 Mémoriel` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_confirm_triage` | **Valider l'Aiguillage Réglementaire AeterniTrak** | `primary` | `idle` | 🧭 |
| `btn_quarantine` | **Mise sous Séquestre Sanitaire Suspect** | `danger` | `idle` | ☣️ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Aiguillage Sanitaire Réussi
>
> **Badge de Conformité :** `Profil 1 Mémoriel Assigné`
>
> **Détail Opérationnel :** Espèce résolue (TaxID 9615). Ligne mémorielle hermétique réservée sans contamination.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_INITIAL_TRIAGE_INVALID` |
| **Intitulé de l'Incident** | **Suspicion d'Épizootie ou Espèce Non Répertoriée** |
| **Condition Déclenchante** | Cause de mortalité suspecte (fièvre charbonneuse, rage) ou espèce inconnue de l'arbre taxonomique. |
| **Message d'Erreur UI** | *« ALERTE SANITAIRE : Suspicion de maladie réputée contagieuse ou anomalie taxonomique. Aiguillage normal suspendu. »* |
| **Action Corrective Requise** | **Isoler immédiatement la carcasse en zone de confinement étanche et alerter les inspecteurs vétérinaires AFSCA.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Terminal Terrain DNF / AFSCA • Triage Sanitaire Initial (IP68)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Terminal Prêt au Poste de Réception des Dépouilles | *En attente utilisateur* | Formulaire de déclaration vierge. Le vétérinaire inspecte la dépouille. |
| **2** | **Déclenchement ⚡** | Saisie de l'Espèce & Résolution Taxonomique | `Sélection de Canis familiaris et constat de mort naturelle sans épizootie` | Recherche instantanée dans le snapshot taxonomique officiel NCBI embarqué. |
| **3** | **Traitement ⚙️** | Génération de l'Identifiant Unique & Verrouillage de Filière | `Progression : 88%` | Attribution irrévocable du Profil 1 Mémoriel et création du scellé numérique RFID. |
| **4** | **Scellement & Fin ✨** | Filière Mémorielle Assignée & Scellée | `Statut : success` | La carcasse est admise dans le sas de décontamination mémoriel dédié. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-401 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Terminal Prêt au Poste de Réception des Dépouilles
*Formulaire de déclaration vierge. Le vétérinaire inspecte la dépouille.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Poste de Triage Sanitaire</span>
                        <span class="wf-status-badge wf-badge-neutral">En Attente de Déclaration</span>
                      </div>
                      <div class="wf-field-group">
                        <label class="wf-label">Identification de l'Espèce <span class="wf-req">*</span></label>
                        <div class="wf-select-placeholder">-- Sélectionner : Canis familiaris, Sus scrofa, Bos taurus --</div>
                      </div>
                      <div class="wf-field-group">
                        <label class="wf-label">Contexte du Décès <span class="wf-req">*</span></label>
                        <div class="wf-select-placeholder">-- Mort naturelle, Euthanasie, Gibier forêt, Abattoir --</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🧭 Valider l'Aiguillage Réglementaire</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Saisie de l'Espèce & Résolution Taxonomique
*Recherche instantanée dans le snapshot taxonomique officiel NCBI embarqué.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Moteur de Triage</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Résolution TaxID</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Taxon résolu : Canis familiaris (TaxID NCBI: 9615)</div>
                        <div class="wf-subtext">Orientation déterministe vers la Ligne 1 Mémorielle Familiale</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Attribution de la filière...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Génération de l'Identifiant Unique & Verrouillage de Filière
*Attribution irrévocable du Profil 1 Mémoriel et création du scellé numérique RFID.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Scellement Sanitaire</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Scellement Triage (88%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 88%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [TRIAGE-CORE] Analyse profil : Animal de compagnie familial</code><br>
                        <code>> [BIO-GATE] Exclusion catégorique de tout aiguillage agricole ou humain</code><br>
                        <code>> [RFID-TAG] Association identifiant DEP-2026-BEL-99201 au scellé physique</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Filière Mémorielle Assignée & Scellée
*La carcasse est admise dans le sas de décontamination mémoriel dédié.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Triage Validé</span>
                        <span class="wf-status-badge wf-badge-success">✨ Profil 1 Mémoriel Scellé</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🐾</span>
                        <div>
                          <strong>Dépouille de Compagnie Admise en Ligne Mémorielle</strong>
                          <p class="wf-subtext">ID: DEP-2026-BEL-99201 • Destination exclusive : Sarcomusation forestière</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Dépistage LFA Pentobarbital →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-402"></a>
## UC-402 : Profil 1 — Filière Compagnie (Catégorie 1 Mémoriel) & Ségrégation

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-402` |
| **Catégorie Métier** | **Profils Dépouilles** |
| **Acteur Principal** | Opérateur de Bioconversion |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `Compagnie`, `Profil1`, `Cat1Memoriel`, `Segregation`, `SasIndividuel` |
| **Base Légale & Normative** | Arrêté royal du 27 avril 2007 (règles sanitaires pour les cadavres d'animaux de compagnie) (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `Terminal Terrain DNF / AFSCA • Sas Mémoriel Individuel (IP68)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Animal de compagnie orienté vers le Profil 1 mémoriel.

> [!TIP]
> **Postconditions Garanties :**
> Ségrégation physique absolue accomplie, traçabilité individuelle garantie pour la famille.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Réception de la dépouille dans le sas de décontamination individuel mémoriel.
2. Vérification de l'absence totale de contact physique ou aéraulique avec les filières d'élevage ou d'abattoir.
3. Attribution d'un bac de sarcomusation individuel avec larves d'Hermetia illucens dédiées.
4. Enregistrement de la traçabilité de la colonie de bioconversion (TaxID 343691).
5. Verrouillage hermétique interdisant tout mélange de résidus entre animaux.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `bioreactor_id` | **Bac de Sarcomusation** | `text` | `Caisson Mémoriel N° 04 (Ligne Hermétique)` | Bac | `Individuel` | ⭕ Optionnel |
| `colony_taxid` | **Colonie de Bioconversion** | `text` | `Hermetia illucens (TaxID 343691 — Mouche soldat noire)` | Colonie | `TaxID 343691` | ⭕ Optionnel |
| `airlock_status` | **Ségrégation Aéraulique** | `text` | `SAS INDIVIDUEL ÉTANCHE (Pression négative 25 Pa)` | Sas | `Confiné` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_seal_airlock` | **Sceller le Sas de Bioconversion Mémoriel** | `primary` | `idle` | 🔒 |
| `btn_check_sensors` | **Vérifier Détecteurs de Pression Sas** | `secondary` | `idle` | 📊 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Sas Individuel Scellé
>
> **Badge de Conformité :** `Ségrégation 100% Hermétique`
>
> **Détail Opérationnel :** Zéro contact avec les filières agricoles. Ligne mémorielle dédiée et isolée.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_PET_CROSS_CONTAMINATION` |
| **Intitulé de l'Incident** | **Rupture de Ségrégation ou Risque de Mélange** |
| **Condition Déclenchante** | Tentative d'introduction conjointe de deux dépouilles dans le même caisson ou défaillance du sas. |
| **Message d'Erreur UI** | *« ALERTE CRITIQUE : Rupture de confinement individuel. Risque de contamination croisée entre flux mémoriels. »* |
| **Action Corrective Requise** | **Stopper immédiatement l'introduction, désinfecter le sas et rétablir le caisson individuel exclusif.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Terminal Terrain DNF / AFSCA • Sas Mémoriel Individuel (IP68)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Caisson Individuel Ouvert en Attente de Dépouille | *En attente utilisateur* | Caisson n° 04 nettoyé et stérilisé. Les larves d'Hermetia illucens sont prêtes. |
| **2** | **Déclenchement ⚡** | Introduction de la Dépouille & Fermeture du Sas | `Dépôt de la dépouille identifiée DEP-2026-BEL-99201 et verrouillage` | Verrouillage électromagnétique du sas individuel avec retour visuel vert. |
| **3** | **Traitement ⚙️** | Surveillance Télémétrique de la Bioconversion | `Progression : 70%` | Suivi des capteurs de température, d'hygrométrie et d'activité des larves. |
| **4** | **Scellement & Fin ✨** | Cycle de Sarcomusation Mémorielle Scellé | `Statut : success` | Résidus cinéraires individuels prêts pour l'étape de pasteurisation thermique. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-402 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Caisson Individuel Ouvert en Attente de Dépouille
*Caisson n° 04 nettoyé et stérilisé. Les larves d'Hermetia illucens sont prêtes.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Sas Mémoriel N° 04</span>
                        <span class="wf-status-badge wf-badge-neutral">Caisson Vierge Prêt</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-pet-icon">🐾</span>
                        <div><strong>Caisson de sarcomusation individuelle n° 04</strong></div>
                        <div class="wf-subtext">Colonie Hermetia illucens calibrée • Pression négative active</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔒 Sceller le Sas de Bioconversion Mémoriel</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Introduction de la Dépouille & Fermeture du Sas
*Verrouillage électromagnétique du sas individuel avec retour visuel vert.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Fermeture Sas</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Verrouillage Sas Actif</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Dépouille installée dans le bioréacteur mémoriel n° 04</div>
                        <div class="wf-subtext">Association électronique irréversible du scellé RFID au caisson</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Scellement étanche en cours...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Surveillance Télémétrique de la Bioconversion
*Suivi des capteurs de température, d'hygrométrie et d'activité des larves.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Télémétrie Bioréacteur</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Bioconversion Active (70%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 70%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [BIOMONITOR] Température litière : 34.2°C (Activité larvaire optimale)</code><br>
                        <code>> [AIRFLOW] Confinement maintenu : Dépression -25 Pa constante</code><br>
                        <code>> [TRACE-CHAIN] Zéro contact avec les unités industrielles certifié</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Cycle de Sarcomusation Mémorielle Scellé
*Résidus cinéraires individuels prêts pour l'étape de pasteurisation thermique.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Sarcomusation Achevée</span>
                        <span class="wf-status-badge wf-badge-success">✨ Bioconversion Terminée</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🌱</span>
                        <div>
                          <strong>Bioconversion Mémorielle Accomplie avec Respect</strong>
                          <p class="wf-subtext">Résidus organiques et protéines d'insectes prêts pour pasteurisation</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Dépistage LFA Pentobarbital →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-403"></a>
## UC-403 : Dépistage Toxicologique Qualitatif LFA du Pentobarbital

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-403` |
| **Catégorie Métier** | **Contrôle Biologique** |
| **Acteur Principal** | Vétérinaire & Opérateur |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `Pentobarbital`, `LFA`, `DepistageQualitatif`, `Toxicologie`, `PorteG4` |
| **Base Légale & Normative** | Directive The Iron Gate G4 et normes de sécurité toxicologique vétérinaire AFSCA (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `Terminal Terrain DNF / AFSCA • Lecteur Optique LFA Pentobarbital` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Prélèvement d'échantillon tissulaire sur dépouille de compagnie avant ou après transformation.

> [!TIP]
> **Postconditions Garanties :**
> Statut toxicologique certifié, garantie absolue de l'absence de résidus d'euthanasique toxique.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Extraction liquide rapide sur bandelette de test immunochromatographique (LFA - Lateral Flow Assay) basée sur un principe compétitif.
2. Insertion de la bandelette dans le lecteur optique connecté au terminal.
3. Vérification de la présence des lignes de contrôle (C) et de test (T) :
4. - Lignes C et T visibles : RÉSULTAT NÉGATIF / CONFORME (absence de pentobarbital détecté), validation formelle 'PENTO_OK' pour la filière mémorielle.
5. - Ligne C seule visible (ligne T absente / inhibée) : RÉSULTAT POSITIF / CONTAMINÉ (présence de pentobarbital), REJET ABSOLU, blocage irréversible de la signature et réorientation obligatoire vers incinération Catégorie 1.
6. - Ligne C absente : test non valide, obligation de réitérer le dépistage.
7. Évaluation de la Porte de Fer G4 (Dépistage Pentobarbital) : verrouillage déterministe.
8. Scellement cryptographique du résultat qualitatif LFA dans la revendication de lot.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `target_toxin` | **Substance Recherchée** | `text` | `Pentobarbital Sodique (Agent Euthanasique Vétérinaire)` | Substance | `Toxique` | ⭕ Optionnel |
| `screening_type` | **Principe de Dépistage** | `text` | `Test immunochromatographique compétitif LFA` | Principe | `Compétitif` | ⭕ Optionnel |
| `measured_lines` | **Lecture Optique des Lignes** | `text` | `Lignes C et T visibles (NÉGATIF — Absence de molécule détectée)` | Résultat | `C+T Conforme` | ⭕ Optionnel |
| `gate_g4_status` | **Verdict Porte G4** | `text` | `VALIDÉ (Absence de pentobarbital, feu vert pour pasteurisation et forêt)` | Porte G4 | `Porte G4 OK` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_run_lfa_scan` | **Lancer la Lecture Optique LFA** | `primary` | `idle` | 🔬 |
| `btn_simulate_pento_fail` | **Simuler Rejet Pentobarbital (Ligne C seule)** | `secondary` | `idle` | ⚠️ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Test LFA Pentobarbital Conforme
>
> **Badge de Conformité :** `Porte G4 Franchie (Lignes C+T)`
>
> **Détail Opérationnel :** Lignes C et T visibles (principe compétitif). Absence de molécule de pentobarbital. Zéro risque toxicologique pour les écosystèmes forestiers.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_PENTO_DETECTED` |
| **Intitulé de l'Incident** | **Présence de Pentobarbital Détectée (Ligne C Seule)** |
| **Condition Déclenchante** | Bandelette LFA positive : ligne C seule visible, ligne test T inhibée par la molécule de pentobarbital. |
| **Message d'Erreur UI** | *« REJET TOXICOLOGIQUE MAJEUR (Porte G4) : Bandelette LFA positive (Ligne C seule visible, ligne T absente/inhibée). Présence de résidus d'euthanasique mortels pour la faune sylvicole. Valorisation forestière formellement interdite. »* |
| **Action Corrective Requise** | **Aiguiller immédiatement le lot vers l'incinération thermique industrielle de Catégorie 1.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Terminal Terrain DNF / AFSCA • Lecteur Optique LFA Pentobarbital**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Bandelette LFA Insérée dans le Lecteur Optique | *En attente utilisateur* | Bandelette de test insérée. Le lecteur attend l'ordre de numérisation optique. |
| **2** | **Déclenchement ⚡** | Acquisition Optique de la Bandelette LFA | `Clic sur 'Lancer la Lecture' et capture haute résolution de la bandelette` | Acquisition optique et détection de contraste des lignes Contrôle (C) et Test (T). |
| **3** | **Traitement ⚙️** | Vérification Porte G4 : Lignes C et T Validées (Négatif) | `Progression : 92%` | Validation du principe compétitif : présence de la ligne T confirmant l'absence de pentobarbital. |
| **4** | **Scellement & Fin ✨** | Visa Sanitaire Toxicologique Délivré | `Statut : success` | Feu vert accordé pour la pasteurisation thermique et le retour en forêt mémorielle. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-403 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Bandelette LFA Insérée dans le Lecteur Optique
*Bandelette de test insérée. Le lecteur attend l'ordre de numérisation optique.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Analyseur Toxicologique LFA</span>
                        <span class="wf-status-badge wf-badge-neutral">Bandelette Insérée</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-test-strip-icon">🧪</span>
                        <div><strong>Bandelette LFA Pentobarbital prête pour numérisation</strong></div>
                        <div class="wf-subtext">Principe compétitif : C+T visibles = Négatif / C seule = Positif • Prélèvement DEP-2026-BEL-99201</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔬 Lancer la Lecture Optique LFA</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Acquisition Optique de la Bandelette LFA
*Acquisition optique et détection de contraste des lignes Contrôle (C) et Test (T).*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Scan Optique LFA</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Numérisation Active</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Bandelette analysée par capteur optique haute résolution</div>
                        <div class="wf-subtext">Vérification de la présence simultanée des lignes C (contrôle) et T (test)</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Évaluation de la conformité LFA...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Vérification Porte G4 : Lignes C et T Validées (Négatif)
*Validation du principe compétitif : présence de la ligne T confirmant l'absence de pentobarbital.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Évaluation Porte G4</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Contrôle Barrière G4 (92%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 92%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [LFA-SCAN] Lignes détectées : Contrôle C (Visible) + Test T (Visible)</code><br>
                        <code>> [IRON-GATE-G4] Principe compétitif : Absence de molécule détectée -> PENTO_NEGATIVE_OK</code><br>
                        <code>> [GATE-VERDICT] Porte G4 franchie avec succès : PENTO_OK</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Visa Sanitaire Toxicologique Délivré
*Feu vert accordé pour la pasteurisation thermique et le retour en forêt mémorielle.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Visa Toxicologique</span>
                        <span class="wf-status-badge wf-badge-success">✨ Porte G4 Validée (Lignes C+T)</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🌿</span>
                        <div>
                          <strong>Absence de Résidus Euthanasiques Certifiée</strong>
                          <p class="wf-subtext">Pentobarbital absent (C+T visibles) • Autorisation de traitement thermique mémoriel</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Pasteurisation Thermique 70°C/1h →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-404"></a>
## UC-404 : Pasteurisation Thermique Mémorielle (70°C, 1 heure continue)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-404` |
| **Catégorie Métier** | **Traitement Thermique** |
| **Acteur Principal** | Opérateur de Traitement Thermique |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `Pasteurisation`, `70Degres`, `1Heure`, `Thermocouple`, `PorteG9` |
| **Base Légale & Normative** | Règlement (CE) n° 142/2011 (normes de transformation pour sous-produits animaux) (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `Terminal Terrain DNF / AFSCA • Moniteur Thermique de Pasteurisation (IP68)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Lot de résidus et protéines d'Hermetia illucens certifié négatif au pentobarbital.

> [!TIP]
> **Postconditions Garanties :**
> Éradication complète des bactéries pathogènes (Salmonella, Enterobacteriaceae), scellement thermique.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Chargement des matières dans la cuve de pasteurisation thermique mémorielle.
2. Immersion de trois thermocouples étalonnés au cœur de la matière.
3. Montée en température progressive jusqu'à atteindre au moins 70,0°C au point le plus froid.
4. Maintien continu et ininterrompu du palier thermique à 70,0°C pendant au moins 60 minutes.
5. Acquisition continue des courbes de température (1 mesure par seconde) par l'automate homologué.
6. Vérification de la Porte de Fer G9 (Traitement Sanitaire Requis & Preuve : pasteurisation mémorielle 70°C/1h sous dérogation DEC-AET-05).

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `temp_core` | **Température Cœur Actuelle** | `number` | `70.8°C (Seuil mini réglementaire : 70.0°C)` | Température | `70.8°C` | ⭕ Optionnel |
| `hold_duration` | **Durée Maintien Continu** | `text` | `60 min 00 s (Palier continu sans interruption)` | Durée | `1h Validée` | ⭕ Optionnel |
| `gauge_pressure` | **Pression Manométrique** | `text` | `Pression Atmosphérique Normale (Pasteurisation)` | Pression | `1.0 bar` | ⭕ Optionnel |
| `gate_g9_status` | **Verdict Porte G9** | `text` | `VALIDÉ (Pasteurisation conforme, éradication des pathogènes végétatifs)` | Porte G9 | `Porte G9 OK` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_certify_pasteurisation` | **Certifier le Cycle de Pasteurisation Thermique** | `primary` | `idle` | 🔥 |
| `btn_export_thermal_curve` | **Exporter Courbe Température-Temps** | `secondary` | `idle` | 📈 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Cycle de Pasteurisation Conforme
>
> **Badge de Conformité :** `70°C / 1h Continue`
>
> **Détail Opérationnel :** Salmonella et Enterobacteriaceae éradiquées. Courbe thermique validée par la Porte G9.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_PASTEURISATION_TEMP_DROP` |
| **Intitulé de l'Incident** | **Rupture Thermique : Baisse de Température** |
| **Condition Déclenchante** | Chute de la température au cœur sous 70.0°C à tout moment des 60 minutes de maintien. |
| **Message d'Erreur UI** | *« CYCLE THERMIQUE INVALIDÉ : La température est descendue à 68.9°C au cours du palier. Le compteur de temps continu est remis à zéro. »* |
| **Action Corrective Requise** | **Réchauffer la cuve au-dessus de 70.0°C et recommencer l'intégralité du cycle de 60 minutes continues.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Terminal Terrain DNF / AFSCA • Moniteur Thermique de Pasteurisation (IP68)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Cuve Chargée en Début de Montée Thermique | *En attente utilisateur* | Matières chargées. La température actuelle est de 42°C, en phase de préchauffage. |
| **2** | **Déclenchement ⚡** | Franchissement du Seuil des 70.0°C & Déclenchement Chrono | `La température au cœur atteint 70.0°C, démarrage du compteur 60 min` | Activation du compte à rebours de 60 minutes avec verrouillage de cuve. |
| **3** | **Traitement ⚙️** | Maintien Continu : 45 min / 60 min (T° = 70.8°C) | `Progression : 75%` | Surveillance seconde par seconde. La température oscille de manière stable entre 70.5°C et 71.2°C. |
| **4** | **Scellement & Fin ✨** | Cycle de Pasteurisation 70°C/1h Validé | `Statut : success` | Sécurité microbiologique absolue. Le lot pasteurisé peut être valorisé en forêt cinéraire. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-404 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Cuve Chargée en Début de Montée Thermique
*Matières chargées. La température actuelle est de 42°C, en phase de préchauffage.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Cuve Pasteurisation</span>
                        <span class="wf-status-badge wf-badge-neutral">Préchauffage (42°C)</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-fire-icon">🔥</span>
                        <div><strong>Montée en température vers le palier de 70.0°C</strong></div>
                        <div class="wf-subtext">3 sondes thermocouples étalonnées immergées au cœur du lot</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">Démarrer Surveillance Palier 70°C</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Franchissement du Seuil des 70.0°C & Déclenchement Chrono
*Activation du compte à rebours de 60 minutes avec verrouillage de cuve.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Palier Atteint</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Seuil 70.0°C Atteint</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Démarrage du chronomètre continu de 60 minutes</div>
                        <div class="wf-subtext">Toute baisse sous 70.0°C réinitialisera automatiquement le cycle</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Maintien du palier thermique...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Maintien Continu : 45 min / 60 min (T° = 70.8°C)
*Surveillance seconde par seconde. La température oscille de manière stable entre 70.5°C et 71.2°C.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Maintien Thermique</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Palier Actif (45/60 min)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 75%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [THERMO-1] Sonde cœur supérieure : 70.9°C (Stable)</code><br>
                        <code>> [THERMO-2] Sonde cœur centrale   : 70.8°C (Stable)</code><br>
                        <code>> [THERMO-3] Sonde cœur basse      : 70.5°C (Conforme >= 70.0°C)</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Cycle de Pasteurisation 70°C/1h Validé
*Sécurité microbiologique absolue. Le lot pasteurisé peut être valorisé en forêt cinéraire.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Pasteurisation Conforme</span>
                        <span class="wf-status-badge wf-badge-success">✨ 60 min Continues Validées</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🛡️</span>
                        <div>
                          <strong>Éradication des Pathogènes Végétatifs Certifiée</strong>
                          <p class="wf-subtext">Porte G9 franchie • Matière saine prête pour retour forestier DEC-AET-05</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Valorisation Forestière DEC-AET-05 →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-405"></a>
## UC-405 : Valorisation Forestière Cinéraire sous Dérogation DEC-AET-05

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-405` |
| **Catégorie Métier** | **Destination Finale** |
| **Acteur Principal** | Garde Forestier DNF & Famille |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `ForetCineraire`, `DEC-AET-05`, `ArbreDuSouvenir`, `Amendement`, `DNF` |
| **Base Légale & Normative** | Décret wallon du 15 juillet 2008 (Code forestier art. 41) et Dérogation souveraine DEC-AET-05 (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `Terminal Terrain DNF / AFSCA • Cadastre Forestier Cinéraire (IP68)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Lot de compagnie sain, pasteurisé à 70°C pendant 1h, politique dérogatoire signée.

> [!TIP]
> **Postconditions Garanties :**
> Boucle de retour à la nature accomplie dans le recueillement et le respect de la loi.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Vérification par The Iron Gate de l'application de la dérogation souveraine DEC-AET-05.
2. Conditionnement des protéines et résidus sous forme d'amendement fertilisant pour arbre cinéraire du souvenir.
3. Épandage au pied de l'arbre mémoriel désigné dans une forêt cinéraire privée agréée.
4. Inscription de l'arbre et du défunt dans le cadastre mémoriel forestier.
5. Verrouillage cryptographique absolu interdisant toute réintroduction dans la chaîne alimentaire agricole.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `derogation_policy` | **Cadre Dérogatoire Appliqué** | `text` | `DEC-AET-05 (Amendement Mémoriel Sylvicole)` | Dérogation | `DEC-AET-05` | ⭕ Optionnel |
| `tree_id` | **Arbre Cinéraire Cadastré** | `text` | `Chêne Mémoriel n° F-2408 (Massif de Saint-Hubert)` | Arbre | `Cadastré DNF` | ✅ Requis |
| `tree_gps` | **Coordonnées GPS Submétriques** | `text` | `50.02418° N, 5.37214° E (Précision ±0.3m)` | GPS | `RTK Fix` | ⭕ Optionnel |
| `feed_ban_lock` | **Interdiction Réinjection Agricole** | `text` | `VERROU ABSOLU (Exclusion chaîne alimentaire agricole)` | Feed-Ban | `Inviolable` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_issue_forestry_cert` | **Émettre l'Attestation d'Épandage Cinéraire** | `primary` | `idle` | 🌳 |
| `btn_check_cadastre` | **Vérifier Inscription Cadastrale DNF** | `secondary` | `idle` | 🗺️ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Attestation Forestière Cinéraire Émise
>
> **Badge de Conformité :** `Dérogation DEC-AET-05 Validée`
>
> **Détail Opérationnel :** Amendement apporté au Chêne F-2408. Cadastre forestier émargé et scellé.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_FOREST_DEROGATION_INVALID` |
| **Intitulé de l'Incident** | **Dérogation Non Signée ou Arbre Non Cadastré** |
| **Condition Déclenchante** | Tentative d'épandage sur parcelle publique non conventionnée ou absence d'accord DNF. |
| **Message d'Erreur UI** | *« INTERDICTION D'ÉPANDAGE : La parcelle visée ne bénéficie pas de l'agrément de forêt cinéraire ou la dérogation DEC-AET-05 n'est pas scellée. »* |
| **Action Corrective Requise** | **Sélectionner un arbre mémoriel agréé au cadastre DNF conventionné.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Terminal Terrain DNF / AFSCA • Cadastre Forestier Cinéraire (IP68)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Parcelle Forestière Identifiée sur le Cadastre | *En attente utilisateur* | Garde forestier sur site. L'arbre cinéraire est repéré par coordonnées GPS. |
| **2** | **Déclenchement ⚡** | Apport de l'Amendement Organique & Signature Badge DNF | `Scan du badge de l'agent DNF validant l'acte d'amendement du sol` | Épandage au pied du système racinaire et enregistrement géolocalisé immédiat. |
| **3** | **Traitement ⚙️** | Enregistrement dans le Cadastre Mémoriel & Verrou Feed-Ban | `Progression : 95%` | Verrouillage absolu interdisant tout réemploi des terres à des fins agricoles. |
| **4** | **Scellement & Fin ✨** | Retour à la Nature Accompli dans la Dignité | `Statut : success` | Certificat d'Arbre Mémoriel remis à la famille. Cycle de vie bouclé avec pureté. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-405 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Parcelle Forestière Identifiée sur le Cadastre
*Garde forestier sur site. L'arbre cinéraire est repéré par coordonnées GPS.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Cadastre Sylvicole</span>
                        <span class="wf-status-badge wf-badge-neutral">Arbre F-2408 Repéré</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-tree-icon">🌳</span>
                        <div><strong>Chêne Centenaire n° F-2408 (Forêt de Saint-Hubert)</strong></div>
                        <div class="wf-subtext">Parcelle cinéraire agréée sous dérogation souveraine DEC-AET-05</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🌳 Émettre l'Attestation d'Épandage</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Apport de l'Amendement Organique & Signature Badge DNF
*Épandage au pied du système racinaire et enregistrement géolocalisé immédiat.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Épandage Mémoriel</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Badge DNF Validé</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Amendement organique apporté au pied de l'arbre F-2408</div>
                        <div class="wf-subtext">Position RTK confirmée : 50.02418° N, 5.37214° E (±0.3m)</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Scellement cadastral en cours...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Enregistrement dans le Cadastre Mémoriel & Verrou Feed-Ban
*Verrouillage absolu interdisant tout réemploi des terres à des fins agricoles.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Registre Foncier DNF</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Scellement Foncier (95%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 95%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [DNF-CADASTRE] Enregistrement arbre F-2408 au registre des sépultures sylvestres</code><br>
                        <code>> [FEED-BAN] Verrou cryptographique : Interdiction recyclage agricole scellée</code><br>
                        <code>> [DEC-AET-05] Dérogation souveraine confirmée conforme</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Retour à la Nature Accompli dans la Dignité
*Certificat d'Arbre Mémoriel remis à la famille. Cycle de vie bouclé avec pureté.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Hommage Forestier</span>
                        <span class="wf-status-badge wf-badge-success">✨ Arbre Cinéraire Scellé</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🌳</span>
                        <div>
                          <strong>Mémoire Vivante Ancrée dans la Forêt Ardennaise</strong>
                          <p class="wf-subtext">Arbre n° F-2408 protégé à perpétuité • Certificat cadastral délivré à la famille</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Profil 2 Faune Sauvage DNF →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-406"></a>
## UC-406 : Profil 2 — Filière Faune Sauvage (Cat 1/2 DNF) : Badge & GPS

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-406` |
| **Catégorie Métier** | **Profils Dépouilles** |
| **Acteur Principal** | Garde Forestier DNF |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `FauneSauvage`, `DNF`, `BadgeAgent`, `GPS-RTK`, `Sanglier`, `Cerf`, `ControleAmont`, `DEC-AET-13` |
| **Base Légale & Normative** | Décret wallon du 15 juillet 2008 relatif au Code forestier (missions de police sylvicole des agents DNF) (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `Terminal Terrain DNF / AFSCA • Module Agent DNF Faune Sauvage (IP68)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Cadavre de grand gibier sauvage découvert en milieu naturel (sanglier, cerf, chevreuil).

> [!TIP]
> **Postconditions Garanties :**
> Carcasse prise en charge sous séquestre sanitaire officiel DNF.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Arrivée de l'agent DNF sur le lieu de signalement de la carcasse.
2. Authentification de l'agent par scan de son badge NFC professionnel sécurisé (contrôle amont déclaratif, DEC-AET-13).
3. Relevé automatique des coordonnées GPS satellitaires avec précision submétrique (< 1 mètre).
4. Identification de l'espèce sauvage et encodage du TaxID NCBI (ex: 9823 pour Sus scrofa).
5. Conditionnement en sac de confinement hermétique avec scellé numéroté DNF inviolable.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `dnf_badge_id` | **Badge Agent Assermenté** | `text` | `Agent Jean Dupont (Badge DNF-2026-771)` | Badge | `Assermenté` | ✅ Requis |
| `gps_coords` | **Position GPS RTK** | `text` | `50.41284° N, 5.82341° E (Précision: ±0.28m)` | GPS | `Submétrique` | ⭕ Optionnel |
| `wild_species` | **Grand Gibier Identifié** | `select` | `Sus scrofa (TaxID 9823 — Sanglier d'Europe)` | Espèce | `TaxID 9823` | ✅ Requis |
| `seal_number` | **Scellé de Confinement** | `text` | `Scellé DNF-BE-2026-8891 (Sac étanche C1)` | Scellé | `Séquestre` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_seal_wild_corpse` | **Signer le Prélèvement de Faune Sauvage (Badge DNF)** | `primary` | `idle` | 🐗 |
| `btn_rtk_recalibrate` | **Recalibrer Point GPS RTK** | `secondary` | `idle` | 🛰️ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Prélèvement Faune Sauvage Enregistré
>
> **Badge de Conformité :** `Sous Séquestre DNF`
>
> **Détail Opérationnel :** GPS ±0.28m et badge agent scellés. Sac étanche prêt pour transfert laboratoire.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_DNF_GPS_ACCURACY_LOW` |
| **Intitulé de l'Incident** | **Précision Satellitaire Insuffisante (> 1.0 m)** |
| **Condition Déclenchante** | Canopée dense bloquant le signal GPS RTK avec imprécision de localisation supérieure à 1 mètre. |
| **Message d'Erreur UI** | *« Erreur géodésique : La précision GPS actuelle (±3.4m) ne respecte pas le standard submétrique imposé par le DNF. »* |
| **Action Corrective Requise** | **Déplacer l'antenne RTK en clairière ou utiliser le point de repère topographique cadastré le plus proche.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Terminal Terrain DNF / AFSCA • Module Agent DNF Faune Sauvage (IP68)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Garde DNF Face à la Carcasse en Forêt | *En attente utilisateur* | Carcasse de sanglier localisée. Le terminal DNF attend le scan du badge agent. |
| **2** | **Déclenchement ⚡** | Scan du Badge Agent & Fix Satellitaire RTK | `Scan du badge NFC de l'agent Jean Dupont et verrouillage GPS submétrique` | Authentification de l'officier de police sylvicole et horodatage satellitaire atomique. |
| **3** | **Traitement ⚙️** | Génération de l'Identifiant de Séquestre Sanitaire | `Progression : 90%` | Création du dossier de surveillance épidémiologique et affectation du sac étanche. |
| **4** | **Scellement & Fin ✨** | Prélèvement Faune Sauvage Scellé pour Laboratoire | `Statut : success` | Carcasse confinée sous contrôle étatique. Prête pour expédition au laboratoire d'analyse. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-406 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Garde DNF Face à la Carcasse en Forêt
*Carcasse de sanglier localisée. Le terminal DNF attend le scan du badge agent.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">DNF • Constat Faune Sauvage</span>
                        <span class="wf-status-badge wf-badge-neutral">En Attente Badge Agent</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-boar-icon">🐗</span>
                        <div><strong>Carcasse de grand gibier repérée</strong></div>
                        <div class="wf-subtext">Approchez votre badge professionnel NFC d'agent assermenté DNF</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">Signer le Prélèvement (Badge DNF)</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Scan du Badge Agent & Fix Satellitaire RTK
*Authentification de l'officier de police sylvicole et horodatage satellitaire atomique.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">DNF • Authentification Agent</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Badge Valide (Agent Dupont)</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Agent assermenté identifié : DNF-2026-771</div>
                        <div class="wf-subtext">Fix GPS RTK verrouillé : 50.41284° N, 5.82341° E (Précision ±0.28m)</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Scellement du prélèvement...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Génération de l'Identifiant de Séquestre Sanitaire
*Création du dossier de surveillance épidémiologique et affectation du sac étanche.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">DNF • Séquestre Sanitaire</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Enregistrement (90%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 90%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [DNF-POLICE] Relevé d'identité : Sus scrofa (Sanglier adulte ~85 kg)</code><br>
                        <code>> [SEAL-NUM] Bague inviolable scellée : DNF-BE-2026-8891</code><br>
                        <code>> [EPIZOO-WARN] Prélèvement ganglions programmé pour analyse PCR PPA</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Prélèvement Faune Sauvage Scellé pour Laboratoire
*Carcasse confinée sous contrôle étatique. Prête pour expédition au laboratoire d'analyse.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">DNF • Prélèvement Validé</span>
                        <span class="wf-status-badge wf-badge-success">✨ Séquestre Actif</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🐗</span>
                        <div>
                          <strong>Gibier Pris en Charge sous Séquestre Officiel DNF</strong>
                          <p class="wf-subtext">Scellé n° 8891 • Épizootie en attente • Expédition laboratoire agréé</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Dépistages PCR Épizooties →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-407"></a>
## UC-407 : Dépistages PCR Épizooties en Laboratoire Agréé (PPA & CWD)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-407` |
| **Catégorie Métier** | **Contrôle Biologique** |
| **Acteur Principal** | Biologiste de Laboratoire Agréé (Sciensano) |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `PCR`, `PPA`, `CWD`, `Prions`, `Epizootie`, `ControleAmont`, `DEC-AET-13` |
| **Base Légale & Normative** | Règlement d'exécution (UE) 2021/605 (mesures spéciales de lutte contre la peste porcine africaine) (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `Terminal Terrain DNF / AFSCA • Console de Laboratoire PCR (Sciensano)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Prélèvement d'organes cibles effectué par le garde DNF sur le gibier.

> [!TIP]
> **Postconditions Garanties :**
> Statut sanitaire certifié par le laboratoire officiel avant toute bioconversion.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Analyse moléculaire par PCR en temps réel pour le virus de la Peste Porcine Africaine (PPA).
2. Test Western Blot / ELISA pour le dépistage de la Maladie du Dépérissement Chronique des Cervidés (CWD - prions).
3. Évaluation du contrôle sanitaire amont déclaratif (DEC-AET-13, Sciensano) :
4. - Si résultat positif à une épizootie majeure : alerte d'urgence AFSCA, confinement du massif forestier et incinération C1 immédiate.
5. - Si résultat strictement négatif : émission du visa sanitaire d'admission à la transformation.
6. Scellement cryptographique du rapport de laboratoire dans le dossier du lot.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `pcr_asf_result` | **Test PCR PPA (Peste Porcine)** | `text` | `NÉGATIF (Ct indéterminé > 40 cycles)` | PPA | `PPA Négatif` | ⭕ Optionnel |
| `cwd_prion_result` | **Test Prions CWD (Cervidés)** | `text` | `NÉGATIF (Western Blot sans bande PrPSc)` | CWD | `CWD Négatif` | ⭕ Optionnel |
| `lab_certifier` | **Laboratoire Certificateur** | `text` | `Sciensano Laboratoire de Référence Nationale` | Laboratoire | `Agrément AFSCA` | ⭕ Optionnel |
| `upstream_check_status` | **Contrôle Amont Sanitaire** | `text` | `VALIDÉ (Contrôle déclaratif DEC-AET-13 conforme)` | Contrôle Amont | `DEC-AET-13 OK` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_issue_sanitary_visa` | **Délivrer le Visa Sanitaire d'Admission** | `primary` | `idle` | 🧬 |
| `btn_simulate_asf_positive` | **Simuler Détection Positive PPA (Alerte Rouge)** | `danger` | `idle` | ☣️ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Visa Sanitaire Laboratoire Validé
>
> **Badge de Conformité :** `Contrôle Amont Validé (DEC-AET-13)`
>
> **Détail Opérationnel :** Aucun agent d'épizootie ni prion détecté. Admission pour stérilisation Méthode 1.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_EPIZOOTIC_PCR_POSITIVE` |
| **Intitulé de l'Incident** | **Alerte Épizootie Majeure : PCR PPA Positive** |
| **Condition Déclenchante** | Amplification virale PPA détectée avec Ct < 35 ou détection de prions CWD. |
| **Message d'Erreur UI** | *« ALERTE NATIONALE DE BIOSÉCURITÉ (Contrôle Amont DEC-AET-13) : Virus PPA ou prion CWD détecté dans la carcasse. Risque épidémique majeur. »* |
| **Action Corrective Requise** | **Déclencher le plan d'urgence sanitaire AFSCA, confiner le massif forestier et incinérer immédiatement la carcasse en Catégorie 1.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Terminal Terrain DNF / AFSCA • Console de Laboratoire PCR (Sciensano)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Échantillons d'Organes Prêts dans le Thermocycleur | *En attente utilisateur* | Échantillon de rate et ganglions prêt. Le cycle PCR attend d'être analysé. |
| **2** | **Déclenchement ⚡** | Fin de l'Amplification & Détection de Fluorescence | `Lecture des courbes d'amplification temps réel (40 cycles)` | Constat de l'absence totale de courbe de fluorescence pour le virus PPA. |
| **3** | **Traitement ⚙️** | Contrôle Amont Déclaratif (DEC-AET-13) & Scellement Cryptographique | `Progression : 95%` | Injection du certificat d'analyse officielle dans le dossier amont du lot. |
| **4** | **Scellement & Fin ✨** | Visa Sanitaire d'Admission Délivré | `Statut : success` | Le gibier sauvage peut être admis en filière de traitement thermique haute sécurité. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-407 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Échantillons d'Organes Prêts dans le Thermocycleur
*Échantillon de rate et ganglions prêt. Le cycle PCR attend d'être analysé.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sciensano • Laboratoire Épizooties</span>
                        <span class="wf-status-badge wf-badge-neutral">PCR Prête</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-dna-icon">🧬</span>
                        <div><strong>Recherche moléculaire PPA (Sanglier n° 8891)</strong></div>
                        <div class="wf-subtext">Amorces PCR spécifiques gène VP72 du virus de la peste porcine</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">Délivrer le Visa Sanitaire</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Fin de l'Amplification & Détection de Fluorescence
*Constat de l'absence totale de courbe de fluorescence pour le virus PPA.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sciensano • Analyse Fluorescence</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ 40 Cycles Achevés</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Absence d'amplification virale : Signal plat</div>
                        <div class="wf-subtext">Témoins positifs valides • Échantillon certifié indemne de PPA</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Édition du visa officiel...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Contrôle Amont Déclaratif (DEC-AET-13) & Scellement Cryptographique
*Injection du certificat d'analyse officielle dans le dossier amont du lot.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sciensano • Contrôle Amont DEC-AET-13</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Contrôle Amont (95%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 95%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [LAB-PCR] Virus PPA : NÉGATIF (Ct > 40)</code><br>
                        <code>> [LAB-PRION] Prions CWD : NÉGATIF (Western Blot 0 bande)</code><br>
                        <code>> [UPSTREAM-CHECK] Barrière d'épizootie amont (DEC-AET-13) : ADMISSIBLE</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Visa Sanitaire d'Admission Délivré
*Le gibier sauvage peut être admis en filière de traitement thermique haute sécurité.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sciensano • Certificat Émis</span>
                        <span class="wf-status-badge wf-badge-success">✨ Visa Sanitaire Accordé</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🔬</span>
                        <div>
                          <strong>Statut Sanitaire Faune Sauvage Conforme</strong>
                          <p class="wf-subtext">Exempt de PPA et prions • Autorisation de traitement Méthode 1</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Stérilisation Méthode 1 (133°C/3b) →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-408"></a>
## UC-408 : Stérilisation Européenne Méthode 1 (133°C, 3 bars, 20 minutes)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-408` |
| **Catégorie Métier** | **Traitement Thermique** |
| **Acteur Principal** | Opérateur d'Autoclave Haute Pression |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `Methode1`, `133Degres`, `3Bars`, `20Minutes`, `Prions`, `PorteG9` |
| **Base Légale & Normative** | Règlement (CE) n° 142/2011 (annexe IV, chapitre III - Méthode 1 de transformation standard) (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `Terminal Terrain DNF / AFSCA • Moniteur Autoclave Méthode 1 (IP68)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Matières de Catégorie 1 ou 2 nécessitant une neutralisation absolue des agents prions.

> [!TIP]
> **Postconditions Garanties :**
> Inactivation irréversible de l'infectiosité des agents transmissibles non conventionnels (prions).

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Broyage préalable obligatoire de la matière à une granulométrie inférieure ou égale à 50 mm.
2. Chargement en autoclave industriel à vapeur saturée.
3. Chauffe à une température minimale au cœur de la matière de 133,0°C sans interruption.
4. Maintien sous pression manométrique d'au moins 3,0 bars pendant au moins 20 minutes consécutives.
5. Acquisition horodatée et scellée des courbes Pression-Température-Temps par automate homologué.
6. Validation de la Porte de Fer G9 (Traitement Sanitaire Requis & Preuve : Méthode 1 standard européen 133°C, 3 bars, 20 min).

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `temp_meth1` | **Température au Cœur** | `number` | `133.5°C (Seuil réglementaire : >= 133.0°C)` | Température | `133.5°C` | ⭕ Optionnel |
| `pressure_meth1` | **Pression Vapeur Saturée** | `number` | `3.2 bars (Seuil réglementaire : >= 3.0 bars)` | Pression | `3.2 bars` | ⭕ Optionnel |
| `duration_meth1` | **Durée Maintien Continu** | `text` | `20 min 00 s (Palier continu sans chute)` | Durée | `20 min` | ⭕ Optionnel |
| `grain_size` | **Granulométrie Préalable** | `text` | `< 50 mm (Broyage industriel certifié)` | Broyat | `≤ 50 mm` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_certify_meth1` | **Valider la Conformité Méthode 1 (Règlement 1069/2009)** | `primary` | `idle` | ♨️ |
| `btn_export_pt_curve` | **Télécharger Courbe P-T-t Chiffrée** | `secondary` | `idle` | 📈 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Stérilisation Européenne Méthode 1 Validée
>
> **Badge de Conformité :** `133°C / 3 bars / 20 min OK`
>
> **Détail Opérationnel :** Prions et agents conventionnels irréversiblement inactivés. Porte G9 satisfaite.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_METHOD1_PRESSURE_LOSS` |
| **Intitulé de l'Incident** | **Chute de Pression ou de Température sous les Seuils Légaux** |
| **Condition Déclenchante** | Pression descendant sous 3.0 bars ou température sous 133.0°C au cours des 20 minutes. |
| **Message d'Erreur UI** | *« CYCLE MÉTHODE 1 INVALIDÉ : Pression manométrique descendue à 2.8 bars. Violation des exigences du Règlement (CE) 142/2011. »* |
| **Action Corrective Requise** | **Purger la vapeur résiduelle, rétablir la pression à 3.2 bars et relancer l'intégralité du palier de 20 minutes.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Terminal Terrain DNF / AFSCA • Moniteur Autoclave Méthode 1 (IP68)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Autoclave Chargé avec Broyat Calibré < 50mm | *En attente utilisateur* | Matières broyées scellées dans la cuve. La montée en pression est en cours. |
| **2** | **Déclenchement ⚡** | Atteinte du Palier 133°C & 3 bars : Déclenchement Chrono | `La pression atteint 3.2 bars à 133.5°C, lancement du compteur 20 min` | Verrouillage des vannes de sécurité et scellement du cycle haute pression. |
| **3** | **Traitement ⚙️** | Surveillance P-T-t : 15 min / 20 min (Pression Stable 3.2 b) | `Progression : 75%` | Enregistrement cryptographique continu des données de pression et température. |
| **4** | **Scellement & Fin ✨** | Cycle Méthode 1 Certifié Conforme | `Statut : success` | Matières stérilisées au niveau réglementaire européen maximal. Inactivation validée. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-408 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Autoclave Chargé avec Broyat Calibré < 50mm
*Matières broyées scellées dans la cuve. La montée en pression est en cours.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Autoclave Haute Pression</span>
                        <span class="wf-status-badge wf-badge-neutral">Montée en Pression (1.8 bar)</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-steamer-icon">♨️</span>
                        <div><strong>Broyat calibré < 50 mm sous vapeur saturée</strong></div>
                        <div class="wf-subtext">Cibles : 133.0°C minimum • 3.0 bars minimum • 20 minutes continues</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">Démarrer Palier Méthode 1</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Atteinte du Palier 133°C & 3 bars : Déclenchement Chrono
*Verrouillage des vannes de sécurité et scellement du cycle haute pression.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Palier Méthode 1</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ 133.5°C • 3.2 Bars Atteints</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Démarrage du chronomètre de stérilisation (20:00)</div>
                        <div class="wf-subtext">Inactivation physique des conformations anormales de la protéine prion</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Maintien 133°C / 3 bars...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Surveillance P-T-t : 15 min / 20 min (Pression Stable 3.2 b)
*Enregistrement cryptographique continu des données de pression et température.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Moniteur P-T-t</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Palier Actif (15/20 min)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 75%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [AUTOCLAVE] Température cœur : 133.5°C (Tolérance : +0.5°C)</code><br>
                        <code>> [AUTOCLAVE] Pression vapeur saturée : 3.22 bars manométriques</code><br>
                        <code>> [IRON-GATE-G9] Critères Méthode 1 européenne strictement respectés</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Cycle Méthode 1 Certifié Conforme
*Matières stérilisées au niveau réglementaire européen maximal. Inactivation validée.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Stérilisation Réussie</span>
                        <span class="wf-status-badge wf-badge-success">✨ Méthode 1 Certifiée</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">♨️</span>
                        <div>
                          <strong>Inactivation Irréversible des Prions Validée</strong>
                          <p class="wf-subtext">133°C / 3 bars / 20 min accomplis • Porte G9 validée avec succès</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Profil 3 Élevage & Sanitel →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-409"></a>
## UC-409 : Profil 3 — Filière Élevage / Ferme (Catégorie 2) & Boucle Sanitel

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-409` |
| **Catégorie Métier** | **Profils Dépouilles** |
| **Acteur Principal** | Éleveur & Vétérinaire Sanitaire |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `Elevage`, `Ferme`, `Sanitel`, `Boucle`, `Cat2`, `Bovine` |
| **Base Légale & Normative** | Arrêté royal du 23 mars 2011 (identification et enregistrement des bovins dans le système Sanitel) (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `Terminal Terrain DNF / AFSCA • Module Sanitel Élevage (IP68)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Mortalité survenue dans une exploitation agricole agréée (bovins, porcins, ovins).

> [!TIP]
> **Postconditions Garanties :**
> Carcasse agricole classée en Catégorie 2 prête pour la synchronisation officielle.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Déclaration obligatoire du décès dans les 24 heures via le terminal d'exploitation.
2. Lecture optique et NFC de la boucle auriculaire officielle d'identification Sanitel.
3. Vérification de l'absence de signes cliniques d'EST (ESB bovine, tremblante du mouton).
4. Attribution exclusive de la filière de valorisation technique Catégorie 2 (biodiesel, engrais minéraux).
5. Interdiction catégorique de tout aiguillage vers l'alimentation humaine ou animale mémorielle.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `sanitel_tag` | **Boucle Auriculaire Sanitel** | `text` | `BE 5 1284 9901 (Scan Optique & RFID)` | Boucle | `Sanitel National` | ✅ Requis |
| `farm_id` | **Exploitation Agricole** | `text` | `Ferme du Bocage (N° Troupeau: BE 0412.981.203)` | Exploitation | `Agréée` | ⭕ Optionnel |
| `livestock_species` | **Espèce Agricole** | `select` | `Bos taurus (TaxID 9913 — Ruminant Bovin Laitier)` | Espèce | `Ruminant` | ✅ Requis |
| `assigned_category` | **Filière Attribuée** | `text` | `CATÉGORIE 2 (Aiguillage Industriel Exclusif : Biodiesel)` | Filière | `Cat 2 Technique` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_validate_farm_admission` | **Valider l'Admission Catégorie 2 Agricole** | `primary` | `idle` | 🐄 |
| `btn_verify_sanitel_online` | **Vérifier Déclaration Sanitel** | `secondary` | `idle` | 📡 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Dépouille Agricole Admise en Catégorie 2
>
> **Badge de Conformité :** `Sanitel BE 5 1284 9901`
>
> **Détail Opérationnel :** Boucle nationale validée. Aiguillage exclusif vers valorisation technique (biodiesel).

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_FARM_FOOD_CHANNEL_LEAK` |
| **Intitulé de l'Incident** | **Tentative d'Aiguillage vers la Chaîne Alimentaire** |
| **Condition Déclenchante** | Erreur d'opérateur sélectionnant une destination d'alimentation animale pour un animal d'élevage mort. |
| **Message d'Erreur UI** | *« BLOCAGE STRICT (Feed-Ban) : Les animaux morts en élevage relèvent obligatoirement de la Catégorie 2. Toute utilisation pour l'alimentation est pénalement interdite. »* |
| **Action Corrective Requise** | **Forcer l'aiguillage exclusif vers la filière technique (combustion cimenterie ou biodiesel industriel).** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Terminal Terrain DNF / AFSCA • Module Sanitel Élevage (IP68)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Bovin Déclaré en Exploitation en Attente de Scan | *En attente utilisateur* | Éleveur devant la dépouille. La boucle Sanitel doit être scannée par RFID. |
| **2** | **Déclenchement ⚡** | Lecture RFID de la Boucle Auriculaire BE 5 1284 9901 | `Scan RFID de l'étiquette auriculaire officielle Sanitel` | Reconnaissance instantanée du numéro national d'identification bovine. |
| **3** | **Traitement ⚙️** | Classification Obligatoire en Sous-Produit Catégorie 2 | `Progression : 90%` | Verrouillage anti-alimentation animale et préparation de l'admission vers biodiesel. |
| **4** | **Scellement & Fin ✨** | Dépouille Classée Catégorie 2 & Tracée | `Statut : success` | Dossier sanitaire clos. La carcasse partira en filière technique certifiée. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-409 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Bovin Déclaré en Exploitation en Attente de Scan
*Éleveur devant la dépouille. La boucle Sanitel doit être scannée par RFID.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Déclaration Élevage</span>
                        <span class="wf-status-badge wf-badge-neutral">En Attente Boucle Sanitel</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-cow-icon">🐄</span>
                        <div><strong>Mortalité bovine déclarée en exploitation agricole</strong></div>
                        <div class="wf-subtext">Approchez le scanner optique ou RFID de la boucle auriculaire</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">Scanner la Boucle Sanitel</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Lecture RFID de la Boucle Auriculaire BE 5 1284 9901
*Reconnaissance instantanée du numéro national d'identification bovine.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Détection Boucle</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Boucle Détectée</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Numéro Sanitel : BE 5 1284 9901</div>
                        <div class="wf-subtext">Ruminant Bos taurus • Statut exploitation : Indemne d'EST</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Vérification de la filière...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Classification Obligatoire en Sous-Produit Catégorie 2
*Verrouillage anti-alimentation animale et préparation de l'admission vers biodiesel.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Classification Sanitaire</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Classification (90%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 90%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [SANITEL] Identification nationale confirmée : BE 5 1284 9901</code><br>
                        <code>> [REGL-1069] Matière classée obligatoirement en Catégorie 2</code><br>
                        <code>> [FOOD-BAN] Verrou anti-réinjection chaîne alimentaire enclenché</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Dépouille Classée Catégorie 2 & Tracée
*Dossier sanitaire clos. La carcasse partira en filière technique certifiée.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Admission Ferme Validée</span>
                        <span class="wf-status-badge wf-badge-success">✨ Catégorie 2 Scellée</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🐄</span>
                        <div>
                          <strong>Bovin Enregistré en Filière Catégorie 2 Technique</strong>
                          <p class="wf-subtext">Boucle BE 5 1284 9901 • Aiguillage exclusif : Réacteur biodiesel C2</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Ingestion APIs Sanitel/CERISE →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-410"></a>
## UC-410 : Ingestion Automatisée APIs Sanitel & CERISE (Traçabilité Élevage)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-410` |
| **Catégorie Métier** | **Interopérabilité APIs** |
| **Acteur Principal** | Système Core & Autorité AFSCA |
| **Plateformes Cibles** | Node.js / Core Engine, Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `APIs`, `Sanitel`, `CERISE`, `ARSIA`, `Tracabilite`, `ControleAmont`, `DEC-AET-13` |
| **Base Légale & Normative** | Arrêté ministériel du 28 juin 2013 (modalités d'accès et d'échange de données avec le système Sanitel) (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `Terminal Terrain DNF / AFSCA • Passerelle d'Interopérabilité Sanitel/CERISE` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Numéro de boucle nationale Sanitel scanné sur la dépouille agricole.

> [!TIP]
> **Postconditions Garanties :**
> Zéro risque d'erreur de saisie manuelle, intégrité administrative garantie.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Appel sécurisé en temps réel aux APIs du guichet agricole wallon CERISE et du registre fédéral Sanitel (AFSCA) pour vérification déclarative amont (DEC-AET-13).
2. Récupération de la fiche complète : race, date de naissance, historique des déplacements d'exploitation en exploitation.
3. Contrôle automatique du registre des traitements médicamenteux vétérinaires et respect des temps d'attente.
4. Interrogation des bases sanitaires régionales ARSIA (Wallonie) et DGZ (Flandre) pour confirmer l'absence de mise sous séquestre.
5. Agrégation des données certifiées au dossier numérique de revendication de lot.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `api_sanitel` | **API Fédérale Sanitel (AFSCA)** | `text` | `CONNECTÉ (OAuth2 Mutual TLS — Jeton Valide)` | API Sanitel | `Fédéral` | ⭕ Optionnel |
| `api_cerise` | **API Régionale CERISE (SPW)** | `text` | `CONNECTÉ (Guichet Agricole Wallon Synchronisé)` | API CERISE | `Régional` | ⭕ Optionnel |
| `withhold_period` | **Temps d'Attente Médicamenteux** | `text` | `RESPECTÉ (45 jours écoulés post-antibiotiques)` | Temps attente | `Conforme` | ⭕ Optionnel |
| `quarantine_status` | **Statut Séquestre Sanitaire** | `text` | `INDEMNE (Aucune restriction sur l'élevage BE 0412)` | Séquestre | `Indemne` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_sync_apis` | **Synchroniser avec Sanitel (AFSCA) & CERISE (SPW)** | `primary` | `idle` | 🔄 |
| `btn_refresh_tokens` | **Rafraîchir Jetons de Sécurité OAuth2** | `secondary` | `idle` | 🔑 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Données Fédérales & Régionales Ingestionnées
>
> **Badge de Conformité :** `Sanitel & CERISE 100% OK`
>
> **Détail Opérationnel :** Historique de vie complet et temps d'attente médicamenteux certifiés sans saisie manuelle.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_SANITEL_API_UNREACHABLE` |
| **Intitulé de l'Incident** | **API Sanitel Inaccessible ou Numéro Inexistant** |
| **Condition Déclenchante** | Panne de réseau ou numéro de boucle auriculaire non répertorié au registre national. |
| **Message d'Erreur UI** | *« Erreur d'interopérabilité : Impossible de synchroniser la fiche avec les registres Sanitel / CERISE. »* |
| **Action Corrective Requise** | **Basculer en mode cache local sécurisé et réexécuter la synchronisation dès retour du réseau.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Terminal Terrain DNF / AFSCA • Passerelle d'Interopérabilité Sanitel/CERISE**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Requête d'Interopérabilité Prête à l'Envoi | *En attente utilisateur* | Boucle BE 5 1284 9901 en attente d'interrogation sur les passerelles fédérales. |
| **2** | **Déclenchement ⚡** | Échange REST / OAuth2 Sécurisé avec les Registres | `Clic sur 'Synchroniser' et appel mTLS aux serveurs de l'AFSCA` | Requête chiffrée par certificat d'autorité avec rapatriement des tables généalogiques. |
| **3** | **Traitement ⚙️** | Contrôle Automatique des Délais d'Attente Médicamenteux | `Progression : 95%` | Vérification algorithmique du respect des 45 jours après administration d'antibiotiques. |
| **4** | **Scellement & Fin ✨** | Dossier Agricole Scellé Sans Erreur de Saisie | `Statut : success` | Données certifiées à 100% intégrées au lot pour l'évaluation de The Iron Gate. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-410 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Requête d'Interopérabilité Prête à l'Envoi
*Boucle BE 5 1284 9901 en attente d'interrogation sur les passerelles fédérales.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Passerelle Sanitel</span>
                        <span class="wf-status-badge wf-badge-neutral">Prêt à Synchroniser</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-cloud-icon">🔄</span>
                        <div><strong>Boucle BE 5 1284 9901 en attente d'ingestion API</strong></div>
                        <div class="wf-subtext">Interopérabilité Sanitel (AFSCA), CERISE (SPW) et ARSIA</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔄 Synchroniser avec Sanitel & CERISE</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Échange REST / OAuth2 Sécurisé avec les Registres
*Requête chiffrée par certificat d'autorité avec rapatriement des tables généalogiques.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Échange API Sécurisé</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Appel mTLS Sanitel</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Échange mTLS réussi avec sanitel.afsca.be</div>
                        <div class="wf-subtext">Récupération des déclarations de naissance et traitements vétérinaires</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Agrégation des flux...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Contrôle Automatique des Délais d'Attente Médicamenteux
*Vérification algorithmique du respect des 45 jours après administration d'antibiotiques.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Contrôle Résidus</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Analyse Délais (95%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 95%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [API-SANITEL] Animal : Blanc Bleu Belge (Né le 12/03/2021)</code><br>
                        <code>> [API-CERISE] Dernier traitement vétérinaire : Il y a 48 jours (> 45 jours requis)</code><br>
                        <code>> [HEALTH-CHECK] Temps d'attente médicamenteux respecté : CONFORME</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Dossier Agricole Scellé Sans Erreur de Saisie
*Données certifiées à 100% intégrées au lot pour l'évaluation de The Iron Gate.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Fiche Synchronisée</span>
                        <span class="wf-status-badge wf-badge-success">✨ Données Sanitel Validées</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🌐</span>
                        <div>
                          <strong>Fiche Sanitaire AFSCA Ingestionnée avec Succès</strong>
                          <p class="wf-subtext">Antécédents et délais certifiés conformes • Zéro saisie manuelle</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Profil 4 Déchets Abattoir →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-411"></a>
## UC-411 : Profil 4 — Filière Déchets d'Abattoir (Cat 1 MRS) & Dénaturation Bleu

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-411` |
| **Catégorie Métier** | **Profils Dépouilles** |
| **Acteur Principal** | Inspecteur AFSCA & Opérateur d'Abattoir |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `Abattoir`, `MRS`, `BleuDeMethylene`, `Cat1`, `Denaturation`, `ControleAmont`, `DEC-AET-13` |
| **Base Légale & Normative** | Règlement (CE) n° 999/2001 (annexe V - spécifications des Matériels à Risque Spécifié MRS) (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `Terminal Terrain DNF / AFSCA • Contrôleur MRS & Dénaturation Bleu (IP68)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Sous-produits animaux issus de la chaîne d'abattage industrielle agréée.

> [!TIP]
> **Postconditions Garanties :**
> Flux MRS marqué de manière indélébile et tracé sous contrôle étatique.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Ségrégation immédiate des Matériels à Risque Spécifié (MRS) : crâne, encéphale, yeux et moelle épinière des ruminants.
2. Classification obligatoire en Sous-Produits de Catégorie 1 (risque maximal de transmission d'EST).
3. Dénaturation chimique par pulvérisation d'une solution de bleu de méthylène à 0,5 % pour marquer visuellement la chair.
4. Émission du Document Commercial (Commercial Document) officiel AFSCA avec code QR sécurisé (contrôle amont déclaratif, DEC-AET-13).
5. Stérilisation Méthode 1 préalable obligatoire avant expédition en cimenterie ou réacteur biodiesel.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `mrs_nature` | **Nature des Matières** | `text` | `Matériels à Risque Spécifié (Crâne, encéphale, moelle)` | MRS | `Cat 1 MRS` | ⭕ Optionnel |
| `dye_agent` | **Agent de Dénaturation** | `text` | `Solution de Bleu de Méthylène à 0,5% pulvérisée` | Dénaturation | `Bleu 0.5%` | ✅ Requis |
| `com_doc_id` | **Document Commercial AFSCA** | `text` | `DOC-COMM-2026-MRS-49 (Code QR Sécurisé)` | Document | `AFSCA Officiel` | ⭕ Optionnel |
| `mrs_destination` | **Destination Exclusive** | `text` | `Combustion en Cimenterie / Biodiesel Industriel` | Destination | `Zéro Alimentation` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_validate_denaturation` | **Valider la Dénaturation & Émettre Document Commercial** | `primary` | `idle` | 🔵 |
| `btn_inspect_spray` | **Contrôler Pression Rampe de Pulvérisation** | `secondary` | `idle` | 🚿 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Lot MRS Dénaturé au Bleu de Méthylène 0,5%
>
> **Badge de Conformité :** `Document Commercial Scellé`
>
> **Détail Opérationnel :** Coloration indélébile validée. Stérilisation Méthode 1 imposée avant cimenterie.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_SRM_NOT_DENATURED` |
| **Intitulé de l'Incident** | **Dénaturation au Bleu Insuffisante ou Absente** |
| **Condition Déclenchante** | Concentration en bleu de méthylène inférieure à 0,5% ou pulvérisation incomplète des surfaces. |
| **Message d'Erreur UI** | *« REJET RÉGLEMENTAIRE SÉVÈRE : Les Matériels à Risque Spécifié n'ont pas été dénaturés au bleu de manière indélébile. Interdiction de transport. »* |
| **Action Corrective Requise** | **Réexécuter la pulvérisation de solution de bleu à 0,5% jusqu'à imprégnation visuelle complète avant émission du document.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Terminal Terrain DNF / AFSCA • Contrôleur MRS & Dénaturation Bleu (IP68)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Benne MRS Triée en Attente de Pulvérisation | *En attente utilisateur* | Matières à Risque Spécifié isolées. La rampe de bleu de méthylène est prête. |
| **2** | **Déclenchement ⚡** | Activation de la Rampe & Pulvérisation Indélébile | `Enclenchement de la pompe de bleu de méthylène 0,5% sous 4 bars` | Coloration intense et immédiate de l'ensemble des tissus cérébraux en bleu vif. |
| **3** | **Traitement ⚙️** | Génération du Document Commercial AFSCA Sécurisé | `Progression : 92%` | Encodage du QR code officiel de transport vers la cimenterie conventionnée. |
| **4** | **Scellement & Fin ✨** | Lot MRS Dénaturé & Prêt pour Stérilisation Méthode 1 | `Statut : success` | Traçabilité infaillible. Le lot marqué ne pourra jamais pénétrer la chaîne alimentaire. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-411 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Benne MRS Triée en Attente de Pulvérisation
*Matières à Risque Spécifié isolées. La rampe de bleu de méthylène est prête.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Benne MRS Abattoir</span>
                        <span class="wf-status-badge wf-badge-neutral">En Attente Dénaturation</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-skull-icon">☠️</span>
                        <div><strong>Matériels à Risque Spécifié isolés (Catégorie 1)</strong></div>
                        <div class="wf-subtext">Pulvérisation de solution de bleu de méthylène à 0,5% requise</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔵 Valider la Dénaturation & Émettre Doc</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Activation de la Rampe & Pulvérisation Indélébile
*Coloration intense et immédiate de l'ensemble des tissus cérébraux en bleu vif.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Pulvérisation Active</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Bleu de Méthylène Pulvérisé</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Coloration indélébile au bleu de méthylène 0,5% validée</div>
                        <div class="wf-subtext">Marquage visuel permanent empêchant tout détournement frauduleux</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Émission document commercial...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Génération du Document Commercial AFSCA Sécurisé
*Encodage du QR code officiel de transport vers la cimenterie conventionnée.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Document Commercial</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Scellement AFSCA (92%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 92%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [AFSCA-DOC] Génération Commercial Document n° DOC-COMM-2026-MRS-49</code><br>
                        <code>> [COLOR-CHECK] Taux d'imprégnation chromatique > 98% de la surface : OK</code><br>
                        <code>> [ROUTING] Destination cimenterie sous scellés étatiques : VERROUILLÉ</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Lot MRS Dénaturé & Prêt pour Stérilisation Méthode 1
*Traçabilité infaillible. Le lot marqué ne pourra jamais pénétrer la chaîne alimentaire.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Lot Dénaturé</span>
                        <span class="wf-status-badge wf-badge-success">✨ Marqué au Bleu & Scellé</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🔵</span>
                        <div>
                          <strong>Matériels à Risque Spécifié Dénaturés sous Contrôle AFSCA</strong>
                          <p class="wf-subtext">Document Commercial émis • Stérilisation Méthode 1 obligatoire avant cimenterie</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : The Iron Gate (G0 à G9) →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-412"></a>
## UC-412 : Évaluation Algorithmique Pure par The Iron Gate (G0 à G9, Anti-Prion)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-412` |
| **Catégorie Métier** | **Validation Algorithmique** |
| **Acteur Principal** | The Iron Gate (Moteur Déterministe) |
| **Plateformes Cibles** | Node.js / Core Engine, Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `IronGate`, `AntiPrion`, `G0-G9`, `FeedBan`, `Whitelist` |
| **Base Légale & Normative** | Spécification AeterniTrak AET-SPEC-PRION-001 et Règlement (CE) n° 999/2001 (Feed-ban) (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `Terminal Terrain DNF / AFSCA • Oracle Algorithmique The Iron Gate (G0-G9)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Revendication de lot complète soumise pour autorisation de signature.

> [!TIP]
> **Postconditions Garanties :**
> Verdict déterministe émis : AUTHORISED (signature_permitted = true) ou BLOCKED avec motifs normalisés.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. G0 : Destination & Spécification des cibles (whitelist d'usages autorisés, cibles obligatoires si alimentation).
2. G1 : Taxonomie & Lignage (résolution stricte TaxID NCBI dans le snapshot officiel, default-deny, interdiction rang > espèce).
3. G2 : Protection Restes Humains (rejet absolu en filière générale ; en mémoire forestière : démonstrateur de faisabilité prospectif — option non autorisée par le droit positif actuel sous DEC-AET-15).
4. G3 : Catégories & Substrats (Catégories 1, 2, 3, material classes, dérogation souveraine DEC-AET-05 pour animaux de compagnie).
5. G4 : Dépistage Pentobarbital (Animaux de compagnie : test immunochromatographique qualitatif LFA négatif obligatoire [lignes C et T visibles] ; rejet si positif ou non testé).
6. G5 : Feed-Ban Source Ruminant (interdiction stricte de protéines de ruminants en alimentation).
7. G6 : Feed-Ban Cible Ruminant (interdiction stricte de nourrir des ruminants avec des PAT).
8. G7 : LA RÈGLE D'OR ANTI-PRION / ANTI-CANNIBALISME : interdiction mathématique absolue de nourrir une espèce avec ses propres protéines (FEED_BAN_INTRA_SPECIES_VIOLATION).
9. G8 : Feed-Ban Groupes & Espèces (vérification des filières intra-groupe et destinations positives).
10. G9 : Traitement Sanitaire Requis & Preuve (Méthode 1 [133°C, 3 bar, 20 min] pour Cat 1/2 ou pasteurisation [70°C, 60 min] sous dérogation mémorielle DEC-AET-05, avec condensat SHA-256 de preuve).
11. Nota : Les contrôles amont (PCR Sciensano, boucles Sanitel, documents commerciaux MRS abattoir) sont vérifiés en amont dans la chaîne documentaire déclarative (DEC-AET-13).

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `gates_g0_g3` | **Portes G0-G3 (Destination, Taxon, Humain, Substrat)** | `text` | `100% VALIDE (Format CBOR, TaxID résolu, Zéro humain, Substrat conforme)` | G0-G3 | `G0-G3 OK` | ⭕ Optionnel |
| `gate_g4` | **Porte G4 (Dépistage Pentobarbital)** | `text` | `VALIDE (LFA négatif qualitatif, lignes C et T visibles)` | G4 | `G4 OK` | ⭕ Optionnel |
| `gates_g5_g6` | **Portes G5-G6 (Feed-Ban Ruminants Source & Cible)** | `text` | `VALIDE (Zéro ruminant en source ni en cible alimentaire)` | G5-G6 | `G5-G6 OK` | ⭕ Optionnel |
| `gate_g7` | **Porte G7 (RÈGLE D'OR ANTI-PRION)** | `text` | `ZÉRO RECYCLAGE INTRA-ESPÈCE (G7 Mathématiquement Satisfaite)` | G7 | `ANTI-PRION OK` | ⭕ Optionnel |
| `gate_g8` | **Porte G8 (Feed-Ban Groupes & Espèces)** | `text` | `VALIDE (Filières intra-groupe autorisées respectées)` | G8 | `G8 OK` | ⭕ Optionnel |
| `gate_g9` | **Porte G9 (Traitement Sanitaire & Preuve)** | `text` | `VALIDE (Méthode 1 ou Pasteurisation 70°C/1h, Preuve SHA-256)` | G9 | `G9 OK` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_evaluate_iron_gate` | **Évaluer The Iron Gate (G0 à G9)** | `primary` | `idle` | 🛡️ |
| `btn_simulate_intra_species` | **Simuler Violation Règle G7 Anti-Prion** | `danger` | `idle` | ☣️ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** VERDICT THE IRON GATE : AUTHORISED
>
> **Badge de Conformité :** `10/10 Portes Validées`
>
> **Détail Opérationnel :** signature_permitted = true. Zéro risque de prions ni de recyclage intra-espèce.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_PRION_INTRA_SPECIES` |
| **Intitulé de l'Incident** | **Violation de la Règle d'Or Anti-Prion (Porte G7)** |
| **Condition Déclenchante** | Revendication associant des protéines issues d'une espèce à la nourriture de cette même espèce (ex: Porc vers Porc). |
| **Message d'Erreur UI** | *« REJET INVIOLABLE THE IRON GATE (Porte G7) : Recyclage intra-espèce détecté. Violation absolue du feed-ban européen et du verrou anti-prion. Signature formellement refusée (signature_permitted = false). »* |
| **Action Corrective Requise** | **Aiguiller impérativement le lot vers une destination exempte de risque intra-espèce ou vers la valorisation énergétique.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Terminal Terrain DNF / AFSCA • Oracle Algorithmique The Iron Gate (G0-G9)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Revendication de Lot Soumise aux 10 Portes | *En attente utilisateur* | Revendication prête. Les 10 portes de sécurité G0 à G9 sont en attente d'évaluation. |
| **2** | **Déclenchement ⚡** | Lancement du Banc de Test des 10 Portes de Sécurité | `Clic sur 'Évaluer The Iron Gate' et exécution déterministe` | Évaluation instantanée séquentielle des règles positives G0, G1, G2, G3, G4, G5, G6, G7, G8, G9. |
| **3** | **Traitement ⚙️** | Analyse de Matrice : 10/10 Portes Franchies sans Déviation | `Progression : 98%` | Toutes les conditions de la liste blanche positive sont rigoureusement remplies. |
| **4** | **Scellement & Fin ✨** | Verdict Solennel : AUTHORISED (Signature Autorisée) | `Statut : success` | The Iron Gate délivre son blanc-seing. Le lot peut être cryptographiquement scellé. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-412 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Revendication de Lot Soumise aux 10 Portes
*Revendication prête. Les 10 portes de sécurité G0 à G9 sont en attente d'évaluation.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">The Iron Gate • Banc de Validation Anti-Prion</span>
                        <span class="wf-status-badge wf-badge-neutral">10 Portes en Attente</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-gate-icon">🛡️</span>
                        <div><strong>Revendication de lot n° LOT-2026-BEL-0491</strong></div>
                        <div class="wf-subtext">Principe inviolable : Whitelist stricte (Default-Deny) • Zéro complaisance</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🛡️ Évaluer The Iron Gate (G0 à G9)</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Lancement du Banc de Test des 10 Portes de Sécurité
*Évaluation instantanée séquentielle des règles positives G0, G1, G2, G3, G4, G5, G6, G7, G8, G9.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">The Iron Gate • Évaluation en Cours</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Pipeline Déterministe</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">⚡ Vérification de la Porte G7 (Règle d'or Anti-Prion)</div>
                        <div class="wf-subtext">Contrôle de non-recyclage intra-espèce et validation Hermetia illucens</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Évaluation des 10 portes...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Analyse de Matrice : 10/10 Portes Franchies sans Déviation
*Toutes les conditions de la liste blanche positive sont rigoureusement remplies.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">The Iron Gate • Matrice de Conformité</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Portes G0-G9 (98%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 98%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [G0-G3] Format CBOR déterministe, zéro humain, TaxID résolu : OK</code><br>
                        <code>> [G4-G6] LFA négatif qualitatif (C+T), Feed-Ban Ruminants respecté : OK</code><br>
                        <code>> [G7-G9] Pas de recyclage intra-espèce (G7), Groupes (G8), Traitement prouvé (G9) : OK</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Verdict Solennel : AUTHORISED (Signature Autorisée)
*The Iron Gate délivre son blanc-seing. Le lot peut être cryptographiquement scellé.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">The Iron Gate • Verdict Émis</span>
                        <span class="wf-status-badge wf-badge-success">✨ AUTHORISED (10/10 OK)</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🏆</span>
                        <div>
                          <strong>VERDICT FORMEL : AUTHORISED (signature_permitted = true)</strong>
                          <p class="wf-subtext">Règle anti-prion respectée • Autorisation formelle de signature délivrée</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Émission Certificat Ed25519 →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-413"></a>
## UC-413 : Émission du Certificat de Lot Signé Ed25519 (AET-SPEC-CERT-001)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-413` |
| **Catégorie Métier** | **Cryptographie Filière** |
| **Acteur Principal** | The Iron Gate & Autorité de Conformité |
| **Plateformes Cibles** | Node.js / Core Engine, Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `Certificat`, `Ed25519`, `COSE_Sign1`, `AET-SPEC-CERT-001`, `HSM` |
| **Base Légale & Normative** | Spécification technique formelle AET-SPEC-CERT-001 et Règlement (UE) 2021/1372 (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `Terminal Terrain DNF / AFSCA • Autorité de Certification de Lot Ed25519` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> The Iron Gate a délivré un verdict formellement AUTHORISED.

> [!TIP]
> **Postconditions Garanties :**
> Certificat de lot infalsifiable délivré aux acteurs de la filière et régulateurs.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Calcul du hachage SHA-256 canonique JCS de la revendication de lot (Clé 1).
2. Insertion du statut littéral 'AUTHORISED' (Clé 2) et de l'horodatage UNIX Tag 1 (Clé 3).
3. Insertion de l'empreinte du snapshot taxonomique (Clé 4) et de la version des règles v1.4 (Clé 5).
4. Intégration de l'empreinte de la dérogation forestière mémorielle DEC-AET-05 si applicable (Clé 6).
5. Encodage CBOR déterministe et signature cryptographique par la clé Ed25519 officielle de l'autorité de conformité.
6. Génération de l'enveloppe COSE_Sign1 (content type : application/aeternitrak-batch-claim+cbor).

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `cert_status` | **Statut de Conformité** | `text` | `AUTHORISED (Clé 2 du Certificat)` | Statut | `AUTHORISED` | ⭕ Optionnel |
| `cert_alg` | **Algorithme de Scellement** | `text` | `Ed25519 (alg: -8, RFC 8032)` | Algorithme | `Ed25519` | ⭕ Optionnel |
| `claim_jcs_hash` | **Empreinte Revendication JCS** | `text` | `7f3a9b1c...d84e (Clé 1 SHA-256)` | Hash JCS | `SHA-256` | ⭕ Optionnel |
| `cose_typ` | **Type MIME COSE Protégé** | `text` | `application/aeternitrak-batch-claim+cbor (RFC 9596)` | typ | `Protégé` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_issue_batch_cert` | **Signer & Émettre le Certificat de Conformité** | `primary` | `idle` | 🔏 |
| `btn_download_cbor_cert` | **Télécharger Certificat CBOR Déterministe** | `secondary` | `idle` | 💾 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Certificat de Lot Signé Ed25519 Émis
>
> **Badge de Conformité :** `AET-SPEC-CERT-001 Conforme`
>
> **Détail Opérationnel :** Enveloppe COSE_Sign1 générée avec sceau d'autorité infalsifiable. Prêt pour audit.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_BATCH_CERT_SIGN_FAILED` |
| **Intitulé de l'Incident** | **Refus de Signature : Revendication Non Autorisée** |
| **Condition Déclenchante** | Tentative d'émission d'un certificat sur un lot ayant échoué à une des portes de The Iron Gate. |
| **Message d'Erreur UI** | *« REFUS DE SIGNATURE ABSOLU : L'oracle cryptographique est matériellement incapable d'apposer son sceau sur une revendication non AUTHORISED. »* |
| **Action Corrective Requise** | **Corriger les non-conformités sanitaires identifiées par The Iron Gate avant toute nouvelle tentative.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Terminal Terrain DNF / AFSCA • Autorité de Certification de Lot Ed25519**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Verdict AUTHORISED Reçu, Prêt pour Signature | *En attente utilisateur* | The Iron Gate a validé le lot. Le module HSM prépare la structure COSE_Sign1. |
| **2** | **Déclenchement ⚡** | Calcul du Hash Canonique & Construction de l'Enveloppe | `Clic sur 'Signer & Émettre le Certificat de Conformité'` | Injection des 6 clés canoniques du certificat et signature matérielle Ed25519. |
| **3** | **Traitement ⚙️** | Encodage CBOR Déterministe & Signature COSE_Sign1 | `Progression : 98%` | Génération de l'enveloppe CBOR avec Tag 18 et type application/aeternitrak-batch-claim+cbor. |
| **4** | **Scellement & Fin ✨** | Certificat de Lot Infalsifiable Émis | `Statut : success` | Passeport sanitaire officiel délivré. Les transporteurs et régulateurs peuvent auditer le lot. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-413 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Verdict AUTHORISED Reçu, Prêt pour Signature
*The Iron Gate a validé le lot. Le module HSM prépare la structure COSE_Sign1.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Autorité de Certification</span>
                        <span class="wf-status-badge wf-badge-neutral">Prêt pour Scellement</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-key-icon">🔏</span>
                        <div><strong>Revendication approuvée par The Iron Gate</strong></div>
                        <div class="wf-subtext">Clé Ed25519 d'autorité de conformité en ligne • Spécification AET-SPEC-CERT-001</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔏 Signer & Émettre le Certificat</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Calcul du Hash Canonique & Construction de l'Enveloppe
*Injection des 6 clés canoniques du certificat et signature matérielle Ed25519.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Signature de Lot</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Signature Ed25519 Active</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Hachage canonique JCS : 7f3a9b1c...d84e</div>
                        <div class="wf-subtext">Signature1 [ "Signature1", protected, empty_aad, cert_payload ]</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Scellement cryptographique...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Encodage CBOR Déterministe & Signature COSE_Sign1
*Génération de l'enveloppe CBOR avec Tag 18 et type application/aeternitrak-batch-claim+cbor.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Enveloppe de Lot</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Scellement COSE (98%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 98%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [CERT-CORE] Insertion Clé 1 (claim_hash) et Clé 2 (AUTHORISED) : OK</code><br>
                        <code>> [ED25519] Signature apposée : e4a1...99bc (64 octets canoniques)</code><br>
                        <code>> [COSE-TAG] Tag CBOR 18 injecté avec en-tête protégé MIME RFC 9596</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Certificat de Lot Infalsifiable Émis
*Passeport sanitaire officiel délivré. Les transporteurs et régulateurs peuvent auditer le lot.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Certificat Officiel</span>
                        <span class="wf-status-badge wf-badge-success">✨ Certificat Scellé</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🏆</span>
                        <div>
                          <strong>Certificat de Lot Signé Ed25519 Prêt pour Audit</strong>
                          <p class="wf-subtext">AET-SPEC-CERT-001 • Inaltérable • Audit réglementaire hors-ligne possible</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Double Audit AFSCA / DNF →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-414"></a>
## UC-414 : Double Audit Réglementaire AFSCA / DNF Hors-Ligne

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-414` |
| **Catégorie Métier** | **Audit & Régulateurs** |
| **Acteur Principal** | Inspecteur AFSCA & Contrôleur DNF |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `Audit`, `AFSCA`, `DNF`, `HorsLigne`, `DoubleControle`, `Preuve` |
| **Base Légale & Normative** | Règlement (UE) 2017/625 (contrôles officiels le long de la chaîne agroalimentaire) (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `Terminal Terrain DNF / AFSCA • Console d'Audit Réglementaire Hors-Ligne` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Contrôle inopiné d'un chargement de protéines d'insectes transformées (PAT) ou d'amendements forestiers.

> [!TIP]
> **Postconditions Garanties :**
> Sécurité sanitaire et légale démontrée à 100% auprès des autorités publiques.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. L'inspecteur scanne le certificat cryptographique via son terminal mobile de contrôle.
2. Double vérification autonome et instantanée exécutée sans aucune connexion réseau :
3. 1. Vérification mathématique de la signature Ed25519 par rapport à la clé publique de l'autorité AeterniTrak.
4. 2. Réévaluation intégrale en local des règles The Iron Gate G0 à G9 sur la revendication originale.
5. Constat infaillible de l'absence totale de prions, de barbituriques et de recyclage illicite.
6. Délivrance de l'attestation de conformité réglementaire immédiate.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `inspector_name` | **Inspecteur Officiel** | `text` | `Inspecteur AFSCA & Garde DNF Assermenté` | Inspecteur | `Autorité Étatique` | ⭕ Optionnel |
| `audit_mode` | **Mode d'Exécution** | `text` | `100% HORS-LIGNE (Zéro connexion réseau requise)` | Mode | `Autonome` | ⭕ Optionnel |
| `audit_sig_status` | **Vérification 1 : Signature Ed25519** | `text` | `AUTHENTIQUE (Clé d'autorité AeterniTrak reconnue)` | Signature | `Vérifié` | ⭕ Optionnel |
| `audit_gate_status` | **Vérification 2 : The Iron Gate G0-G9** | `text` | `10/10 PORTES VALIDÉES EN LOCAL (Zéro déviation)` | The Iron Gate | `Conforme` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_run_offline_audit` | **Lancer le Double Audit Réglementaire Hors-Ligne** | `primary` | `idle` | ⚖️ |
| `btn_export_audit_pv` | **Éditer l'Attestation de Contrôle AFSCA (PDF)** | `secondary` | `idle` | 📄 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Double Audit Réglementaire Réussi à 100%
>
> **Badge de Conformité :** `Conforme AFSCA / DNF`
>
> **Détail Opérationnel :** Absence totale de prions, de barbituriques et de recyclage intra-espèce démontrée.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_AUDIT_REGULATORY_NON_COMPLIANT` |
| **Intitulé de l'Incident** | **Échec de Conformité Réglementaire Lors de l'Audit** |
| **Condition Déclenchante** | Signature de lot non reconnue ou réévaluation locale de The Iron Gate rejetant une porte. |
| **Message d'Erreur UI** | *« SAISIE SANITAIRE IMMÉDIATE : Le certificat présenté est invalide ou les règles sanitaires The Iron Gate sont violées. Blocage du chargement. »* |
| **Action Corrective Requise** | **Mettre le chargement immédiatement sous séquestre judiciaire et ordonner l'enquête sanitaire approfondie.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Terminal Terrain DNF / AFSCA • Console d'Audit Réglementaire Hors-Ligne**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Inspecteur Face au Chargement avec Terminal Hors-Ligne | *En attente utilisateur* | Contrôle inopiné sur route ou en usine. Le certificat CBOR est scanné. |
| **2** | **Déclenchement ⚡** | Lancement Instantané de la Double Vérification Locale | `Clic sur 'Lancer le Double Audit' sans aucune connexion Internet` | Exécution conjointe de la vérification cryptographique et de l'oracle sanitaire. |
| **3** | **Traitement ⚙️** | Réévaluation Complète des Règles G0-G9 en 80 ms | `Progression : 98%` | Preuve mathématique absolue de l'absence de prions, barbituriques et recyclage illicite. |
| **4** | **Scellement & Fin ✨** | Attestation de Conformité Réglementaire Délivrée | `Statut : success` | Contrôle réussi avec félicitations. Le chargement circule en toute légalité. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-414 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Inspecteur Face au Chargement avec Terminal Hors-Ligne
*Contrôle inopiné sur route ou en usine. Le certificat CBOR est scanné.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AFSCA / DNF • Audit Réglementaire</span>
                        <span class="wf-status-badge wf-badge-neutral">Prêt pour Double Audit</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-badge-icon">⚖️</span>
                        <div><strong>Certificat de lot AET-SPEC-CERT-001 scanné</strong></div>
                        <div class="wf-subtext">Double vérification : 1. Signature Ed25519 • 2. Moteur The Iron Gate G0-G9</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">⚖️ Lancer le Double Audit Hors-Ligne</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Lancement Instantané de la Double Vérification Locale
*Exécution conjointe de la vérification cryptographique et de l'oracle sanitaire.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AFSCA / DNF • Audit en Cours</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Double Audit Actif</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Contrôle 1 : Mathématique Ed25519 sur clé d'autorité</div>
                        <div class="wf-subtext">Contrôle 2 : Réexécution intégrale The Iron Gate sur la revendication</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Évaluation déterministe locale...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Réévaluation Complète des Règles G0-G9 en 80 ms
*Preuve mathématique absolue de l'absence de prions, barbituriques et recyclage illicite.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AFSCA / DNF • Preuve Déterministe</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Traitement Local (98%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 98%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [AUDIT-CRYPTO] Signature Ed25519 vérifiée avec succès : 100% Intègre</code><br>
                        <code>> [AUDIT-GATE] Réévaluation The Iron Gate : 10/10 Portes VALIDÉES</code><br>
                        <code>> [ZERO-PRION] Règle G7 Anti-Prion respectée : ZÉRO recyclage intra-espèce</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Attestation de Conformité Réglementaire Délivrée
*Contrôle réussi avec félicitations. Le chargement circule en toute légalité.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AFSCA / DNF • Contrôle Conforme</span>
                        <span class="wf-status-badge wf-badge-success">✨ 100% Conforme & Libéré</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🏆</span>
                        <div>
                          <strong>Conformité Sanitaire et Réglementaire Absolue Démontrée</strong>
                          <p class="wf-subtext">Zéro prion • Zéro barbiturique • Autorisation officielle de circulation accordée</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Audit Terminé avec Succès (Filière AeterniTrak)</button>
                      </div>
                    </div>
```

</details>

---
