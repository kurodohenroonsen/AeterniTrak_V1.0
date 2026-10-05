# Application 1 — PaxStudio Design (UC-101 à UC-110)

**Outil Créatif de Personnalisation Graphique & Mémorielle (Familles & Conseillers)**

> [!NOTE]
> **Périmètre Applicatif :**
> L'application **PaxStudio Design** est l'environnement interactif dédié à la famille et au conseiller funéraire en salon des familles ou en mobilité. Elle permet la co-conception visuelle et mémorielle du double support physique (Carte Sanctuaire mémorielle et Carte Directives civiles/médicales, ou Médaillons 35 mm), la prévisualisation 3D temps réel avec matériaux nobles (or satiné, résine obsidienne), l'intégration de portraits optimisés WebP (norme STORAGE-001), la captured d'oscillogrammes vocaux avec ducking sonore, et la compilation en **capsule de pré-encodage scellée** au format CBOR/JSON prête pour la gravure physique.

## 📌 Sommaire des Micro Use-Cases Spécifiés

| ID | Titre du Cas d'Usage | Catégorie Métier | Acteur | Plateformes | Référence Normative |
| :---: | :--- | :--- | :--- | :--- | :--- |
| [`UC-101`](#uc-101) | [Choix des Modèles de Carte & Médaillons (Sanctuaire & Directives)](#uc-101) | **Gabarits & Modèles** | Famille & Conseiller Funéraire | Web Standard (PWA Hors-Ligne), Natif (iOS & Android) | Norme ISO/IEC 7810 ID-1 (spécifications des cartes physiques d'identification). |
| [`UC-102`](#uc-102) | [Prévisualisation 3D Interactive Recto/Verso avec Rendu Or & Mat](#uc-102) | **Rendu 3D & Matériaux** | Famille | Web Standard (PWA Hors-Ligne), Natif (iOS & Android) | Code de droit économique belge (art. VI.45 - obligation d'information précontractuelle claire) (référence à confirmer par un juriste). |
| [`UC-103`](#uc-103) | [Colorimétrie, Dorures & Typographies Solennelles](#uc-103) | **Design & Esthétique** | Conseiller & Famille | Web Standard (PWA Hors-Ligne), Natif (iOS & Android) | Règlement général sur l'accessibilité des services (Directive européenne 2019/882) (référence à confirmer par un juriste). |
| [`UC-104`](#uc-104) | [Studio Photo & Carrousel Portraits WebP (Jalon STORAGE-001)](#uc-104) | **Médias Visuels** | Famille & Conseiller | Web Standard (PWA Hors-Ligne), Natif (iOS & Android) | Règlement général sur la protection des données (RGPD art. 5 - minimisation des données) (référence à confirmer par un juriste). |
| [`UC-105`](#uc-105) | [Studio Vocal & Oscilloscope Waveform Crop (Anti-Gestes Android)](#uc-105) | **Médias Sonores** | Famille & Conseiller | Web Standard (PWA Hors-Ligne), Natif (iOS & Android) | Code de la santé publique (protection de l'intégrité morale du recueillement) (référence à confirmer par un juriste). |
| [`UC-106`](#uc-106) | [Choix & Intégration des Musiques d'Adieu & Recueillement](#uc-106) | **Médias Sonores** | Famille & Conseiller | Web Standard (PWA Hors-Ligne), Natif (iOS & Android) | Code de la propriété intellectuelle (œuvres tombées dans le domaine public / licences acquises) (référence à confirmer par un juriste). |
| [`UC-107`](#uc-107) | [Saisie Guidée des Dernières Volontés Civiles & Funéraires](#uc-107) | **Dernières Volontés** | Famille & Conseiller | Web Standard (PWA Hors-Ligne), Natif (iOS & Android) | Loi du 20 juillet 1971 sur les funérailles et sépultures (primauté de la volonté du défunt) (référence à confirmer par un juriste). |
| [`UC-108`](#uc-108) | [Directives Médicales Post-Mortem (Pacemaker, Dons, Legs)](#uc-108) | **Directives Médicales** | Famille & Conseiller | Web Standard (PWA Hors-Ligne), Natif (iOS & Android) | Article L1232-17 §2 du CDLD (exérèse obligatoire des stimulateurs cardiaques) (référence à confirmer par un juriste). |
| [`UC-109`](#uc-109) | [Génération & Validation de la Capsule de Pré-Encodage CBOR](#uc-109) | **Compilation & Core** | Conseiller & Système Core | Web Standard (PWA Hors-Ligne), Node.js / Core Engine | Spécification technique IETF RFC 8949 (déterminisme binaire CBOR). |
| [`UC-110`](#uc-110) | [Bon à Tirer (BAT) Numérique & Validation Familiale](#uc-110) | **Validation Finale** | Famille & Conseiller Funéraire | Web Standard (PWA Hors-Ligne), Natif (iOS & Android) | Code civil belge (art. 1322 - valeur probante de la signature électronique) (référence à confirmer par un juriste). |

---

<a id="uc-101"></a>
## UC-101 : Choix des Modèles de Carte & Médaillons (Sanctuaire & Directives)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-101` |
| **Catégorie Métier** | **Gabarits & Modèles** |
| **Acteur Principal** | Famille & Conseiller Funéraire |
| **Plateformes Cibles** | Web Standard (PWA Hors-Ligne), Natif (iOS & Android) |
| **Tags Clés** | `Gabarits`, `CarteSanctuaire`, `CarteDirectives`, `Medaillon35mm` |
| **Base Légale & Normative** | Norme ISO/IEC 7810 ID-1 (spécifications des cartes physiques d'identification). |
| **Terminal / Canvas Wireframe** | `PaxStudio Pro • iPad Pro Canvas (2732×2048)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Ouverture de la session PaxStudio Design sur tablette ou PC en salon des familles.

> [!TIP]
> **Postconditions Garanties :**
> Le gabarit vectoriel est calibré au dixième de millimètre pour le double recto/verso.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Sélection du format physique : Carte CR-80 standard (85.6 x 53.98 mm) ou Médaillon circulaire (diamètre 35 mm).
2. Attribution du rôle de chaque carte : Carte 1 Sanctuaire (mémoriel affectif) et Carte 2 Directives (directives civiles, médicales et administratives).
3. Choix de la matière noble : Carte polycarbonate or satiné, résine composite noire obsidienne ou médaillon en titane anodisé.
4. Chargement immédiat des contraintes d'impression thermique/laser et de la zone d'exclusion de l'antenne NFC.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `card_format` | **Format Physique** | `select` | `Médaillon Circulaire ø35mm` | Sélectionner le format | `Requis` | ✅ Requis |
| `card_role` | **Double Support** | `select` | `Carte 1 Sanctuaire + Carte 2 Directives` | Rôle des cartes | `Dédié` | ✅ Requis |
| `material_finish` | **Matière Noble** | `select` | `Titane Anodisé Or & Obsidienne` | Sélectionner le matériau | `Finition` | ✅ Requis |
| `nfc_margin` | **Zone Exclusion Antenne** | `text` | `5.0 mm bords (ISO 7810 ID-1)` | Marge de sécurité | `Lecture Seule` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_validate_format` | **Valider le Gabarit Physique** | `primary` | `idle` | 📐 |
| `btn_reset_format` | **Réinitialiser** | `secondary` | `idle` | ↩ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Gabarit Physique Initialisé
>
> **Badge de Conformité :** `Conforme ISO/IEC 7810 ID-1`
>
> **Détail Opérationnel :** Cotes 85.6x53.98mm et ø35mm verrouillées. Marge d'antenne NFC réservée (5mm).

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_INVALID_CARD_FORMAT` |
| **Intitulé de l'Incident** | **Format Physique Non Conforme** |
| **Condition Déclenchante** | Sélection d'une épaisseur hors norme (> 0.84 mm) ou dimensions non normalisées. |
| **Message d'Erreur UI** | *« Erreur critique : Le gabarit sélectionné viole la norme ISO/IEC 7810 ID-1 pour les cartes sans contact. »* |
| **Action Corrective Requise** | **Restreindre le choix aux deux gabarits officiels : CR-80 standard ou Médaillon 35mm homologué ACOSJ.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStudio Pro • iPad Pro Canvas (2732×2048)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Sélection du Gabarit Vierge & Matériau | *En attente utilisateur* | Formulaire vierge en attente. Aucun format sélectionné, bouton de validation grisé. |
| **2** | **Déclenchement ⚡** | Tap Tactile de Sélection du Médaillon | `Tap sur le gabarit 'Médaillon ø35mm' et clic 'Valider'` | Action utilisateur en cours : mise en évidence avec onde radar dorée et activation du bouton. |
| **3** | **Traitement ⚙️** | Calibration Vectorielle Submillimétrique | `Progression : 72%` | Calcul en temps réel des zones d'exclusion antenne et des repères laser de gravure. |
| **4** | **Scellement & Fin ✨** | Gabarit Calibré & Zone d'Impression Scellée | `Statut : success` | Gabarit verrouillé avec succès. Cotes vectorielles conformes et bouton 'Design 3D' déverrouillé. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-101 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Sélection du Gabarit Vierge & Matériau
*Formulaire vierge en attente. Aucun format sélectionné, bouton de validation grisé.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Configuration du Support Physique</span>
                        <span class="wf-status-badge wf-badge-neutral">En Attente de Saisie</span>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-field-group">
                          <label class="wf-label">Format de Support <span class="wf-req">*</span></label>
                          <div class="wf-select-placeholder">-- Sélectionner : CR-80 ou Médaillon ø35mm --</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Rôle des Puces Silicium <span class="wf-req">*</span></label>
                          <div class="wf-select-placeholder">Carte 1 Sanctuaire + Carte 2 Directives</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Matière Noble & Teinte</label>
                          <div class="wf-select-placeholder">Titane Anodisé Or Satiné & Obsidienne</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-disabled" disabled>📐 Valider le Gabarit (Inactif)</button>
                        <button class="wf-btn wf-btn-sub">↩ Réinitialiser</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Tap Tactile de Sélection du Médaillon
*Action utilisateur en cours : mise en évidence avec onde radar dorée et activation du bouton.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Sélection Active</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Événement Tap Détecté</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">⚡ Action Déclenchante : Tap sur le Format Médaillon 35mm</div>
                        <div class="wf-selection-summary">
                          <strong>Sélectionné :</strong> Médaillon ø35mm • Titane Or & Obsidienne • Antenne Intégrée
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">📐 Valider le Gabarit Physique (Clic Actif)</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Calibration Vectorielle Submillimétrique
*Calcul en temps réel des zones d'exclusion antenne et des repères laser de gravure.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Moteur de Calibration Vectorielle</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Traitement Actif (72%)</span>
                      </div>
                      <div class="wf-progress-container">
                        <div class="wf-progress-bar" style="width: 72%;"></div>
                      </div>
                      <div class="wf-console-log">
                        <code>> [CAD-ENGINE] Initialisation du système de coordonnées polaires ø35.00mm...</code><br>
                        <code>> [CAD-ENGINE] Application marge de sécurité antenne RF (ISO 7810 ID-1 : 5.0mm) : OK</code><br>
                        <code>> [CAD-ENGINE] Alignement repères laser recto (portrait) & verso (épitaphe) : 100%</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Gabarit Calibré & Zone d'Impression Scellée
*Gabarit verrouillé avec succès. Cotes vectorielles conformes et bouton 'Design 3D' déverrouillé.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Gabarit Homologué</span>
                        <span class="wf-status-badge wf-badge-success">✨ Validé & Verrouillé</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🏆</span>
                        <div>
                          <strong>Gabarit Vectoriel Prêt pour Personnalisation 3D</strong>
                          <p class="wf-subtext">Médaillon Titane ø35mm • Double Face Recto/Verso • Conforme ISO/IEC 7810 ID-1</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Passer à l'Étape 2 : Prévisualisation 3D →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-102"></a>
## UC-102 : Prévisualisation 3D Interactive Recto/Verso avec Rendu Or & Mat

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-102` |
| **Catégorie Métier** | **Rendu 3D & Matériaux** |
| **Acteur Principal** | Famille |
| **Plateformes Cibles** | Web Standard (PWA Hors-Ligne), Natif (iOS & Android) |
| **Tags Clés** | `WebGL`, `ThreeJS`, `PBR`, `Rendu3D` |
| **Base Légale & Normative** | Code de droit économique belge (art. VI.45 - obligation d'information précontractuelle claire) (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `PaxStudio Pro • Visionneuse 3D PBR WebGL` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Modèle de carte sélectionné avec textures haute résolution chargées.

> [!TIP]
> **Postconditions Garanties :**
> Validation visuelle en temps réel sans nécessiter d'impression d'épreuve papier intermédiaire.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Génération du maillage 3D photoréaliste de la carte avec shader PBR (Physically Based Rendering).
2. La famille fait pivoter la carte d'un simple glissement de doigt pour inspecter le recto (portrait et nom) et le verso (épitaphe et puce).
3. Simulation réaliste de la lumière rasante révélant les dorures à chaud et le relief tactile du logo Le Pax Funèbre.
4. Bascule instantanée entre la Carte Sanctuaire et la Carte Directives.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `shader_type` | **Shader PBR Actif** | `select` | `Dorure Or 24k + Mat Velours` | Choix du shader | `Rendu PBR` | ✅ Requis |
| `light_angle` | **Angle de Lumière Rasante** | `range` | `45° Nord-Est` | Axe d'éclairage | `Dynamique` | ⭕ Optionnel |
| `view_face` | **Face Active** | `radio` | `Recto (Portrait Mémoriel)` | Face affichée | `360°` | ✅ Requis |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_rotate_3d` | **Pivoter Recto / Verso (360°)** | `primary` | `idle` | 🔄 |
| `btn_export_preview` | **Capturer Bon Visuel HD** | `secondary` | `idle` | 📸 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Rendu 3D PBR Conforme
>
> **Badge de Conformité :** `60 FPS Fluidité Native`
>
> **Détail Opérationnel :** Textures PBR validées. Reflets spéculaires et micro-reliefs tactilement conformes.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_WEBGL_CONTEXT_LOST` |
| **Intitulé de l'Incident** | **Perte du Contexte Graphique WebGL** |
| **Condition Déclenchante** | Saturation mémoire GPU ou mise en veille prolongée du terminal mobile. |
| **Message d'Erreur UI** | *« Erreur d'affichage : Le moteur 3D PBR a perdu le contexte matériel GPU. »* |
| **Action Corrective Requise** | **Réinitialisation automatique du contexte WebGL et bascule temporaire en rendu 2D haute définition.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStudio Pro • Visionneuse 3D PBR WebGL**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Canevas 3D Initial en Attente de Manipulation | *En attente utilisateur* | Maillage 3D neutre chargé. La carte est fixe, vue de face, prête à l'inspection tactile. |
| **2** | **Déclenchement ⚡** | Geste de Glissement Tactile 360° (Swipe) | `Glissement du doigt sur l'écran tactile pour faire pivoter la carte` | Mise en évidence du vecteur de rotation avec anneau de force dynamique. |
| **3** | **Traitement ⚙️** | Calcul du Shader PBR & Lumière Rasante 45° | `Progression : 85%` | Le moteur WebGL recalcule les ombrages, dorures à chaud et le relief de l'épitaphe. |
| **4** | **Scellement & Fin ✨** | Verso Inspecté & Épreuve Visuelle Validée | `Statut : success` | Carte pivotée à 180° révélant le verso solennel. Épreuve numérique sans papier acceptée. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-102 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Canevas 3D Initial en Attente de Manipulation
*Maillage 3D neutre chargé. La carte est fixe, vue de face, prête à l'inspection tactile.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Visionneuse 3D PBR Temps Réel</span>
                        <span class="wf-status-badge wf-badge-neutral">Face Recto • Éclairage Fixe</span>
                      </div>
                      <div class="wf-3d-viewport">
                        <div class="wf-card-mockup-3d">
                          <div class="wf-gold-border"></div>
                          <div class="wf-portrait-slot">👤 Portrait Mémoriel HD</div>
                          <div class="wf-name-slot">Henri Dubois (1944 - 2026)</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔄 Pivoter Recto / Verso (En attente de glissement)</button>
                        <button class="wf-btn wf-btn-sub">📸 Capturer Vue</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Geste de Glissement Tactile 360° (Swipe)
*Mise en évidence du vecteur de rotation avec anneau de force dynamique.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Interaction Tactile 3D</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Geste Swipe Détecté</span>
                      </div>
                      <div class="wf-3d-viewport wf-radar-pulse">
                        <div class="wf-card-mockup-3d wf-rotating">
                          <div class="wf-rotation-vector">↻ Rotation Angulaire : +145° (Bascule Verso)</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">🔄 Rotation 3D en Cours...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Calcul du Shader PBR & Lumière Rasante 45°
*Le moteur WebGL recalcule les ombrages, dorures à chaud et le relief de l'épitaphe.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Calcul Shaders PBR</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Rendu PBR Actif (85%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 85%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [PBR-SHADER] Éclairage spéculaire 45° sur la dorure à chaud : OK</code><br>
                        <code>> [PBR-SHADER] Rendu micro-relief logo Le Pax Funèbre : 60 FPS constant</code><br>
                        <code>> [PBR-SHADER] Texture verso ACOSJ 92k et antenne sans contact simulée</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Verso Inspecté & Épreuve Visuelle Validée
*Carte pivotée à 180° révélant le verso solennel. Épreuve numérique sans papier acceptée.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Épreuve 3D Validée</span>
                        <span class="wf-status-badge wf-badge-success">✨ Rendu Verso Validé</span>
                      </div>
                      <div class="wf-3d-viewport">
                        <div class="wf-card-mockup-verso">
                          <div class="wf-epitaph-slot">« Le souvenir est une présence invisible dans la paix des bois »</div>
                          <div class="wf-chip-slot">💾 Emplacement Silicium JavaCard ACOSJ 92 Ko</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Valider l'Épreuve & Passer aux Couleurs →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-103"></a>
## UC-103 : Colorimétrie, Dorures & Typographies Solennelles

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-103` |
| **Catégorie Métier** | **Design & Esthétique** |
| **Acteur Principal** | Conseiller & Famille |
| **Plateformes Cibles** | Web Standard (PWA Hors-Ligne), Natif (iOS & Android) |
| **Tags Clés** | `Palette`, `Dorures`, `Typographie`, `Harmonie` |
| **Base Légale & Normative** | Règlement général sur l'accessibilité des services (Directive européenne 2019/882) (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `PaxStudio Pro • Palette Chromatique & Typographies` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Photo principale importée dans le canevas de création.

> [!TIP]
> **Postconditions Garanties :**
> Charte graphique de la carte arrêtée et conforme à la dignité de la cérémonie.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Extraction algorithmique de la palette chromatique dominante de la photo (couleurs chaudes, froides, sépia).
2. Proposition automatique d'une harmonie chromatique : or impérial, argent lunaire ou noir onyx.
3. Sélection parmi 6 polices de caractères funéraires intemporelles (Outfit, Cormorant Garamond, Cinzel, JetBrains Mono pour les données).
4. Ajustement du contraste et contrôle de lisibilité selon les normes d'accessibilité visuelle pour personnes âgées.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `color_scheme` | **Harmonie Chromatique** | `select` | `Or Impérial & Noir Obsidienne` | Palette | `Harmonie` | ✅ Requis |
| `font_title` | **Police Solennelle (Titres)** | `select` | `Cormorant Garamond (Sérif Solennel)` | Typographie titres | `Typo` | ✅ Requis |
| `font_mono` | **Police Technique (Données)** | `text` | `JetBrains Mono (ISO 7816 & Hash)` | Typographie données | `Lecture Seule` | ⭕ Optionnel |
| `a11y_ratio` | **Ratio Contraste WCAG AAA** | `text` | `14.8:1 (Seuil mini: 7.0:1)` | Contraste | `Accessible` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_apply_palette` | **Appliquer la Charte Typographique** | `primary` | `idle` | 🎨 |
| `btn_a11y_check` | **Vérifier Lisibilité Seniors** | `secondary` | `idle` | 👁 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Charte Typographique Validée
>
> **Badge de Conformité :** `Conforme Directive 2019/882`
>
> **Détail Opérationnel :** Contraste 14.8:1 validé pour personnes âgées. Cormorant Garamond et dorures harmonisées.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_A11Y_CONTRAST_DEFICIT` |
| **Intitulé de l'Incident** | **Contraste Typographique Insuffisant** |
| **Condition Déclenchante** | Texte doré clair sur fond blanc ou gris perle résultant en un ratio inférieur à 4.5:1. |
| **Message d'Erreur UI** | *« Erreur d'accessibilité : Le contraste calculé viole la Directive européenne 2019/882 pour la lisibilité des seniors. »* |
| **Action Corrective Requise** | **Forcer le fond en noir obsidienne ou rehausser le liseré d'ombrage typographique.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStudio Pro • Palette Chromatique & Typographies**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Palette Par Défaut en Attente d'Harmonisation | *En attente utilisateur* | Formulaire avec palette standard. L'analyse chromatique de la photo n'est pas encore lancée. |
| **2** | **Déclenchement ⚡** | Clic sur 'Extraire Harmonie depuis la Photo' | `Clic déclencheur sur l'outil d'extraction automatique de palette` | Animation de scan spectral sur les pixels de la photo du défunt. |
| **3** | **Traitement ⚙️** | Vérification WCAG AAA & Ajustement Typographique | `Progression : 90%` | Calcul mathématique du contraste des textes dorés selon les algorithmes WCAG 2.2. |
| **4** | **Scellement & Fin ✨** | Harmonie Or Impérial & Obsidienne Appliquée | `Statut : success` | Typographie Cormorant Garamond dorée gravée avec succès sur le modèle de carte. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-103 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Palette Par Défaut en Attente d'Harmonisation
*Formulaire avec palette standard. L'analyse chromatique de la photo n'est pas encore lancée.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Nuancier & Typographies</span>
                        <span class="wf-status-badge wf-badge-neutral">Palette Standard Non Calibrée</span>
                      </div>
                      <div class="wf-field-group">
                        <label class="wf-label">Harmonie Proposée</label>
                        <div class="wf-select-placeholder">Palette Par Défaut (Gris neutre / Blanc)</div>
                      </div>
                      <div class="wf-field-group">
                        <label class="wf-label">Typographie Solennelle</label>
                        <div class="wf-select-placeholder">Sans-serif Standard</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🎨 Extraire Harmonie depuis la Photo</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Clic sur 'Extraire Harmonie depuis la Photo'
*Animation de scan spectral sur les pixels de la photo du défunt.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Scan Chromatique</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Scan Spectrophotométrique</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">⚡ Événement : Détection des pigments dominants de la photo</div>
                        <div class="wf-subtext">Couleurs détectées : Or sépia, ambre chaud, noir onyx profond</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Calcul de l'Harmonie Or Impérial...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Vérification WCAG AAA & Ajustement Typographique
*Calcul mathématique du contraste des textes dorés selon les algorithmes WCAG 2.2.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Moteur d'Accessibilité WCAG</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Contrôle Lisibilité (90%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 90%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [A11Y] Test contraste texte 'Or #d4af37' sur fond 'Obsidienne #06070b'...</code><br>
                        <code>> [A11Y] Ratio mesuré : 14.82:1 (Exigence AAA : >= 7.0:1) : SUCCÈS</code><br>
                        <code>> [FONT] Chargement glyphes solennels Cormorant Garamond avec ligatures funéraires</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Harmonie Or Impérial & Obsidienne Appliquée
*Typographie Cormorant Garamond dorée gravée avec succès sur le modèle de carte.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Charte Arrêtée</span>
                        <span class="wf-status-badge wf-badge-success">✨ Conforme Directive 2019/882</span>
                      </div>
                      <div class="wf-card-specimen">
                        <span class="wf-gold-title">Henri Dubois</span>
                        <span class="wf-gold-dates">1944 — 2026</span>
                        <span class="wf-a11y-badge">✓ Ratio 14.8:1 Certifié Senior</span>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Studio Photo WebP →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-104"></a>
## UC-104 : Studio Photo & Carrousel Portraits WebP (Jalon STORAGE-001)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-104` |
| **Catégorie Métier** | **Médias Visuels** |
| **Acteur Principal** | Famille & Conseiller |
| **Plateformes Cibles** | Web Standard (PWA Hors-Ligne), Natif (iOS & Android) |
| **Tags Clés** | `WebP`, `Portraits`, `Carrousel`, `STORAGE-001` |
| **Base Légale & Normative** | Règlement général sur la protection des données (RGPD art. 5 - minimisation des données) (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `PaxStudio Pro • Studio Photo & Compression WebP (STORAGE-001)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Photos de famille transmises sur clé USB ou via smartphone.

> [!TIP]
> **Postconditions Garanties :**
> Portraits compressés et dimensionnés à 480×480 pixels (WebP max 20 Ko / 20 480 octets, conforme DEC-AET-12), empreintes SHA-256 enregistrées.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Import des photographies mémorielles du défunt dont le volume et le format respectent les quotas alloués par le jalon technique STORAGE-001.
2. Outil de cadrage circulaire adapté au médaillon avec détection automatique du visage.
3. Compression algorithmique en WebP sans perte perceptible, calibrée sous le seuil maximal de 48 Ko de la partition EF-3.
4. Génération du carrousel de 3 portraits solennels prêts pour l'injection dans le silicium.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `source_photo` | **Fichier Source** | `file` | `portrait_famille_hd.jpg (4.2 Mo)` | Choisir une photo | `Source HD` | ✅ Requis |
| `crop_dim` | **Résolution Cible** | `text` | `480 × 480 pixels (WebP max 20 Ko / 20 480 octets, conforme DEC-AET-12)` | Dimensions | `DEC-AET-12` | ✅ Requis |
| `quota_ef3` | **Quota Partition EF-3** | `text` | `Budget Max : 48 Ko (STORAGE-001)` | Quota puce | `Silicium` | ⭕ Optionnel |
| `webp_size` | **Taille Compressée** | `text` | `12.4 Ko (Consommation : 25.8% du budget)` | Poids final | `Optimisé` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_crop_compress` | **Rogner 480×480 & Compresser WebP (DEC-AET-12)** | `primary` | `idle` | ✂️ |
| `btn_add_carousel` | **Ajouter au Carrousel (Max 3)** | `secondary` | `idle` | ➕ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Portraits WebP Validés
>
> **Badge de Conformité :** `Jalon STORAGE-001 Conforme`
>
> **Détail Opérationnel :** Poids total 37.2 Ko pour 3 portraits. Quota partition EF-3 (48 Ko) respecté.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_PROFILE_TOO_LARGE` |
| **Intitulé de l'Incident** | **Dépassement du Quota Silicium EF-3** |
| **Condition Déclenchante** | Import d'images dont le poids compressé cumulé excède 48 Ko (limite matérielle de l'ACOSJ 92k). |
| **Message d'Erreur UI** | *« Erreur critique : La taille cumulée des médias (52.4 Ko) dépasse le budget strict de 48 Ko alloué par STORAGE-001. »* |
| **Action Corrective Requise** | **Abaisser la résolution de quantification WebP ou limiter le carrousel à 2 portraits.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStudio Pro • Studio Photo & Compression WebP (STORAGE-001)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Zone de Glisser-Déposer de Photo Brute | *En attente utilisateur* | Photo HD de 4.2 Mo chargée. Outil de cadrage circulaire en attente, bouton de compression inactif. |
| **2** | **Déclenchement ⚡** | Clic sur 'Rogner 480×480 & Compresser WebP (DEC-AET-12)' | `Déclenchement du rognage facial automatique 480x480 pixels (DEC-AET-12)` | Détection automatique des contours du visage et application du masque médaillon. |
| **3** | **Traitement ⚙️** | Compression Algorithmique WebP & Vérification Quota | `Progression : 68%` | Compression sans perte perceptible et vérification stricte du budget STORAGE-001 (48 Ko max). |
| **4** | **Scellement & Fin ✨** | Portrait Mémoriel Scellé dans le Carrousel | `Statut : success` | Photo optimisée prête pour gravure silicium. Jauge mémoire verte affichée. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-104 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Zone de Glisser-Déposer de Photo Brute
*Photo HD de 4.2 Mo chargée. Outil de cadrage circulaire en attente, bouton de compression inactif.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Studio Photo</span>
                        <span class="wf-status-badge wf-badge-neutral">Photo Brute 4.2 Mo Chargée</span>
                      </div>
                      <div class="wf-dropzone-box">
                        <span class="wf-file-icon">🖼️</span>
                        <div><strong>portrait_famille_hd.jpg</strong> (4 210 Ko)</div>
                        <div class="wf-subtext">Cadrage circulaire 480×480 et compression WebP (max 20 Ko / 20 480 octets, conforme DEC-AET-12) requis</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">✂️ Rogner 480×480 & Compresser WebP (DEC-AET-12)</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Clic sur 'Rogner 480×480 & Compresser WebP (DEC-AET-12)'
*Détection automatique des contours du visage et application du masque médaillon.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Rognage Facial</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Détection Biométrique du Visage</span>
                      </div>
                      <div class="wf-crop-canvas wf-radar-pulse">
                        <div class="wf-circle-crop-guide">
                          <span class="wf-crop-label">Cible 480×480 px (DEC-AET-12) • Centrage automatique</span>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Encodage WebP en cours...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Compression Algorithmique WebP & Vérification Quota
*Compression sans perte perceptible et vérification stricte du budget STORAGE-001 (48 Ko max).*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Compresseur WebP Local</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Compression en Cours (68%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 68%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [WEBP-CORE] Rééchantillonnage 480x480 bicubique (DEC-AET-12) : OK</code><br>
                        <code>> [WEBP-CORE] Quantification colorimétrique sans perte perceptible : 12.4 Ko</code><br>
                        <code>> [STORAGE-001] Quota partition EF-3 vérifié : 12.4 Ko / 48.0 Ko (Conforme)</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Portrait Mémoriel Scellé dans le Carrousel
*Photo optimisée prête pour gravure silicium. Jauge mémoire verte affichée.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Photo Prête Silicium</span>
                        <span class="wf-status-badge wf-badge-success">✨ Validé (12.4 Ko)</span>
                      </div>
                      <div class="wf-carousel-preview">
                        <div class="wf-portrait-thumb">👤 Portrait 1 (12.4 Ko)</div>
                        <div class="wf-portrait-empty">+ Slot 2</div>
                        <div class="wf-portrait-empty">+ Slot 3</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Studio Vocal Waveform →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-105"></a>
## UC-105 : Studio Vocal & Oscilloscope Waveform Crop (Anti-Gestes Android)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-105` |
| **Catégorie Métier** | **Médias Sonores** |
| **Acteur Principal** | Famille & Conseiller |
| **Plateformes Cibles** | Web Standard (PWA Hors-Ligne), Natif (iOS & Android) |
| **Tags Clés** | `Waveform`, `AudioCrop`, `AntiGestesAndroid`, `WebAudio` |
| **Base Légale & Normative** | Code de la santé publique (protection de l'intégrité morale du recueillement) (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `PaxStudio Pro • Oscilloscope Vocal & Anti-Gestes Android` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Fichier audio vocal brut importé (message d'adieu, bénédiction, souvenir).

> [!TIP]
> **Postconditions Garanties :**
> Extrait audio vocal calibré à une durée maximale de 30 secondes, prêt pour l'intégration.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Affichage de la forme d'onde dynamique interactive (oscilloscope WebAudio) sur l'écran tactile.
2. Manipulation des curseurs temporels de début et fin pour rogner l'extrait solennel sans déclencher les gestes de retour système Android (zone d'exclusion gestuelle appliquée).
3. Filtre coupe-bas automatique éliminant les bruits de souffle et de manipulation du microphone.
4. Normalisation du niveau d'écoute à -23 LUFS (recommandation broadcast funéraire solennelle).

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `audio_raw` | **Fichier Brut** | `file` | `temoignage_vocal.m4a (1 min 30 s)` | Audio brut | `Source` | ✅ Requis |
| `crop_start` | **Curseur Début** | `text` | `00:05.200` | Début | `Découpe` | ✅ Requis |
| `crop_end` | **Curseur Fin** | `text` | `00:35.200 (Durée : 30.0 s)` | Fin | `Max 30s` | ✅ Requis |
| `ebu_lufs` | **Normalisation EBU R128** | `text` | `-23 LUFS (Filtre anti-souffle actif)` | Volume | `Audio Pro` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_crop_audio` | **Rogner & Normaliser EBU R128 (-23 LUFS)** | `primary` | `idle` | 🎙️ |
| `btn_play_preview` | **▶ Écouter Extrait 30s** | `secondary` | `idle` | 🔊 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Audio Vocal Mémoriel Validé
>
> **Badge de Conformité :** `Durée 30.0s • -23 LUFS`
>
> **Détail Opérationnel :** Filtre anti-souffle appliqué. Normalisation broadcast EBU R128 effectuée.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_AUDIO_DURATION_OVERFLOW` |
| **Intitulé de l'Incident** | **Dépassement de la Durée Vocale Maximale** |
| **Condition Déclenchante** | Sélection d'un extrait de plus de 45 secondes excédant le budget mémoire alloué. |
| **Message d'Erreur UI** | *« Erreur audio : La durée sélectionnée dépasse la limite stricte de 30 secondes pour le stockage silicium. »* |
| **Action Corrective Requise** | **Resserrer les curseurs temporels de début et de fin pour respecter la fenêtre de 30 secondes.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStudio Pro • Oscilloscope Vocal & Anti-Gestes Android**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Oscilloscope Brut Non Découpé | *En attente utilisateur* | Forme d'onde brute affichée sur toute la longueur (1m30s). Curseur en attente de déplacement. |
| **2** | **Déclenchement ⚡** | Déplacement des Curseurs Temporels avec Marge Anti-Retour | `Glissement tactile des balises de début (00:05) et fin (00:35)` | Zone tactile sécurisée isolée des bords d'écran pour bloquer le geste de retour Android. |
| **3** | **Traitement ⚙️** | Traitement WebAudio & Normalisation EBU R128 | `Progression : 78%` | Filtrage passe-haut anti-souffle et calcul du loudness intégré à -23 LUFS. |
| **4** | **Scellement & Fin ✨** | Extrait Vocal Mémoriel 30s Prêt | `Statut : success` | Forme d'onde finalisée avec bouton d'écoute instantanée sans latence. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-105 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Oscilloscope Brut Non Découpé
*Forme d'onde brute affichée sur toute la longueur (1m30s). Curseur en attente de déplacement.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Oscilloscope Audio Brut</span>
                        <span class="wf-status-badge wf-badge-neutral">Durée Brute : 01:30.000</span>
                      </div>
                      <div class="wf-waveform-canvas">
                        <div class="wf-wave-bars"> ▂▃▅▆▇▆▅▃▂ ▂▃▅▆▇▆▅▃▂ ▂▃▅▆▇▆▅▃▂ ▂▃▅▆▇▆▅▃▂ </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🎙️ Rogner & Normaliser EBU R128 (-23 LUFS)</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Déplacement des Curseurs Temporels avec Marge Anti-Retour
*Zone tactile sécurisée isolée des bords d'écran pour bloquer le geste de retour Android.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Recadrage Audio Tactile</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Glissement Curseur Temporel</span>
                      </div>
                      <div class="wf-waveform-canvas wf-radar-pulse">
                        <div class="wf-crop-marker wf-marker-start">Balise Début: 00:05.200</div>
                        <div class="wf-crop-window">Fenêtre Vocale 30.0 s (Isolée anti-gestes)</div>
                        <div class="wf-crop-marker wf-marker-end">Balise Fin: 00:35.200</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Traitement WebAudio en cours...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Traitement WebAudio & Normalisation EBU R128
*Filtrage passe-haut anti-souffle et calcul du loudness intégré à -23 LUFS.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Processeur WebAudio</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Normalisation (-23 LUFS)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 78%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [WEBAUDIO] Filtre passe-haut 120 Hz anti-pop : Actif</code><br>
                        <code>> [WEBAUDIO] Normalisation dynamique EBU R128 : -23.0 LUFS atteint</code><br>
                        <code>> [ENCODER] Encodage Ogg Opus mono 16 kbps : 58.2 Ko alloués</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Extrait Vocal Mémoriel 30s Prêt
*Forme d'onde finalisée avec bouton d'écoute instantanée sans latence.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Voix Mémorielle Scellée</span>
                        <span class="wf-status-badge wf-badge-success">✨ Extrait 30s Prêt (-23 LUFS)</span>
                      </div>
                      <div class="wf-player-card">
                        <button class="wf-play-circle">▶</button>
                        <div>
                          <strong>« Message d'Adieu pour mes Proches »</strong>
                          <p class="wf-subtext">00:30.000 • Ogg Opus 16 kbps • Prêt pour ducking vocal</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Musiques d'Adieu →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-106"></a>
## UC-106 : Choix & Intégration des Musiques d'Adieu & Recueillement

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-106` |
| **Catégorie Métier** | **Médias Sonores** |
| **Acteur Principal** | Famille & Conseiller |
| **Plateformes Cibles** | Web Standard (PWA Hors-Ligne), Natif (iOS & Android) |
| **Tags Clés** | `Musique`, `Recueillement`, `Ambiance`, `Fauré`, `Satie` |
| **Base Légale & Normative** | Code de la propriété intellectuelle (œuvres tombées dans le domaine public / licences acquises) (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `PaxStudio Pro • Ambiance Musicale & Recueillement` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Bibliothèque musicale funéraire hors-ligne chargée dans l'application.

> [!TIP]
> **Postconditions Garanties :**
> Piste musicale d'ambiance sélectionnée et configurée avec atténuation automatique (ducking).

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Consultation du répertoire musical solennel embarqué (In Paradisum de Gabriel Fauré, Gymnopédie de Satie, silence sacré).
2. Écoute d'un extrait de 15 secondes pour validation par la famille.
3. Paramétrage du point de bouclage harmonique et de la transition douce en fondu enchaîné (crossfade 3s).
4. Association de la musique à la Carte Sanctuaire pour déclenchement automatique lors du scan NFC.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `music_track` | **Piste Sélectionnée** | `select` | `Gabriel Fauré — In Paradisum (Requiem Op. 48)` | Choisir une musique | `Domaine Public` | ✅ Requis |
| `music_volume` | **Volume Nominal** | `range` | `80% (Volume solennel)` | Niveau sonore | `Ambiance` | ⭕ Optionnel |
| `ducking_level` | **Atténuation Ducking Vocal** | `text` | `-14 dB automatique lors de la voix` | Ducking | `Actif` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_select_music` | **Intégrer la Piste d'Ambiance** | `primary` | `idle` | 🎵 |
| `btn_test_fade` | **Tester Fondu Enchaîné (3s)** | `secondary` | `idle` | 🎧 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Piste Musicale Associée
>
> **Badge de Conformité :** `Ducking -14 dB Prêt`
>
> **Détail Opérationnel :** In Paradisum configuré avec fondu enchaîné de 3s et ducking vocal automatique.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_AUDIO_FORMAT_UNSUPPORTED` |
| **Intitulé de l'Incident** | **Format Audio Non Conforme** |
| **Condition Déclenchante** | Fichier musical corrompu ou codec propriétaire non supporté hors-ligne. |
| **Message d'Erreur UI** | *« Erreur sonore : Le fichier sélectionné ne respecte pas le format Ogg Opus ou WAV pur. »* |
| **Action Corrective Requise** | **Sélectionner une des pistes de la bibliothèque sacrée embarquée ou convertir le fichier en WAV 44.1 kHz.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStudio Pro • Ambiance Musicale & Recueillement**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Répertoire Musical Sacré en Attente | *En attente utilisateur* | Bibliothèque de morceaux funéraires hors-ligne affichée. Piste non encore confirmée. |
| **2** | **Déclenchement ⚡** | Sélection de 'In Paradisum' de Gabriel Fauré | `Clic sur la piste 'In Paradisum' et validation du volume` | Surbrillance dorée de la piste sélectionnée avec prévisualisation sonore instantanée. |
| **3** | **Traitement ⚙️** | Calibration du Profil de Ducking Vocal | `Progression : 82%` | Configuration du compresseur WebAudio pour atténuer la musique à -14 dB lors du témoignage vocal. |
| **4** | **Scellement & Fin ✨** | Ambiance Musicale Associée au Sanctuaire | `Statut : success` | Piste validée avec succès. Elle se lancera automatiquement lors de l'apposition de la carte. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-106 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Répertoire Musical Sacré en Attente
*Bibliothèque de morceaux funéraires hors-ligne affichée. Piste non encore confirmée.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Bibliothèque Musicale Sacrée</span>
                        <span class="wf-status-badge wf-badge-neutral">Sélection en Attente</span>
                      </div>
                      <div class="wf-track-list">
                        <div class="wf-track-item">🎵 Gabriel Fauré — In Paradisum (Requiem)</div>
                        <div class="wf-track-item">🎵 Erik Satie — Gymnopédie N°1</div>
                        <div class="wf-track-item">🎵 Silence Solennel & Sons de la Forêt</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">Intégrer la Piste d'Ambiance</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Sélection de 'In Paradisum' de Gabriel Fauré
*Surbrillance dorée de la piste sélectionnée avec prévisualisation sonore instantanée.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Piste Choise</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Sélection Active</span>
                      </div>
                      <div class="wf-track-selected wf-radar-pulse">
                        <strong>✓ Gabriel Fauré — In Paradisum (Requiem Op. 48)</strong>
                        <p class="wf-subtext">Bouclage harmonique calibré • Crossfade 3 secondes</p>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Enregistrement des Paramètres...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Calibration du Profil de Ducking Vocal
*Configuration du compresseur WebAudio pour atténuer la musique à -14 dB lors du témoignage vocal.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Moteur de Ducking WebAudio</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Calibration Audio (82%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 82%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [DUCKING-DSP] Analyse du niveau RMS de la piste d'ambiance : -18 dBFS</code><br>
                        <code>> [DUCKING-DSP] Enveloppe d'atténuation : Attaque 400ms, Relâchement 1200ms</code><br>
                        <code>> [DUCKING-DSP] Seuil de déclenchement vocal synchronisé : OK</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Ambiance Musicale Associée au Sanctuaire
*Piste validée avec succès. Elle se lancera automatiquement lors de l'apposition de la carte.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Audio Sanctuaire Prêt</span>
                        <span class="wf-status-badge wf-badge-success">✨ Profil Musical Scellé</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🎼</span>
                        <div>
                          <strong>In Paradisum (Fauré) Associé à la Carte Sanctuaire</strong>
                          <p class="wf-subtext">Ducking vocal actif (-14 dB) • Durée de recueillement infinie par bouclage</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Volontés Civiles →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-107"></a>
## UC-107 : Saisie Guidée des Dernières Volontés Civiles & Funéraires

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-107` |
| **Catégorie Métier** | **Dernières Volontés** |
| **Acteur Principal** | Famille & Conseiller |
| **Plateformes Cibles** | Web Standard (PWA Hors-Ligne), Natif (iOS & Android) |
| **Tags Clés** | `Volontes`, `Loi1971`, `Ceremonie`, `Sepulture` |
| **Base Légale & Normative** | Loi du 20 juillet 1971 sur les funérailles et sépultures (primauté de la volonté du défunt) (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `PaxStudio Pro • Fiche des Volontés Civiles & Funéraires` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Famille en salon de recueillement avec le conseiller funéraire agréé.

> [!TIP]
> **Postconditions Garanties :**
> Fiche de dernières volontés civiques encodée, horodatée et prête pour le scellement cryptographique.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Questionnaire structuré conforme à la loi belge du 20 juillet 1971 (cérémonie civile laïque ou culte religieux) (référence à confirmer par un juriste).
2. Choix du mode de sépulture : inhumation traditionnelle, crémation cinéraire ou sarcomusation avec retour en forêt (Démonstrateur de faisabilité prospectif — Option non autorisée par le droit positif actuel (référence à confirmer par un juriste)).
3. Désignation de la destination finale des cendres ou résidus mémoriels (arbre cinéraire privé agréé sous dérogation DEC-AET-05).
4. Rédaction des souhaits spécifiques (fleurs, dons à une association, dispersion solennelle).

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `ceremony_type` | **Nature de Cérémonie** | `select` | `Cérémonie Civile Laïque sous les Arbres` | Cérémonie | `Loi 1971 (référence à confirmer par un juriste)` | ✅ Requis |
| `burial_mode` | **Mode de Sépulture** | `select` | `Sarcomusation & Amendement Forestier (Démonstrateur de faisabilité prospectif — Option non autorisée par le droit positif actuel (référence à confirmer par un juriste))` | Sépulture | `Démonstrateur Prospectif` | ✅ Requis |
| `residue_dest` | **Destination des Résidus** | `select` | `Arbre Cinéraire Mémoriel (Forêt Saint-Hubert)` | Destination | `DEC-AET-05` | ✅ Requis |
| `public_message` | **Message d'Adieu Public** | `textarea` | `« Que la nature accueille ma mémoire en paix auprès des grands chênes. »` | Message | `Facultatif` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_seal_wills` | **Sceller les Volontés Civiles in-silico** | `primary` | `idle` | 📜 |
| `btn_preview_wills` | **Prévisualiser l'Acte Formel** | `secondary` | `idle` | 👁 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Volontés Civiles Encodées
>
> **Badge de Conformité :** `Conforme Loi 20 juillet 1971 (référence à confirmer par un juriste)`
>
> **Détail Opérationnel :** Primauté des volontés garantie. Sarcomusation (Démonstrateur de faisabilité prospectif — Option non autorisée par le droit positif actuel (référence à confirmer par un juriste)) et arbre cinéraire enregistrés.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_WILLS_SYNTAX_INVALID` |
| **Intitulé de l'Incident** | **Clauses Incompatibles avec la Législation** |
| **Condition Déclenchante** | Stipulation d'une clause contraire à l'ordre public ou refus de signature des ayants droit. |
| **Message d'Erreur UI** | *« Erreur de conformité : La disposition funéraire renseignée contrevient au cadre légal des sépultures. »* |
| **Action Corrective Requise** | **Reformuler les clauses pour s'aligner sur les options autorisées par la loi du 20 juillet 1971 (référence à confirmer par un juriste).** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStudio Pro • Fiche des Volontés Civiles & Funéraires**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Formulaire des Volontés Vierge | *En attente utilisateur* | Questionnaire funéraire en attente d'arbitrage par la famille. |
| **2** | **Déclenchement ⚡** | Validation des Choix Funéraires & Signature Famille | `Clic sur 'Sceller les Volontés Civiles in-silico'` | Champs renseignés avec arbitrage formel : Sarcomusation mémorielle et arbre du souvenir. |
| **3** | **Traitement ⚙️** | Sérialisation Canonique & Chiffrement Préparatoire | `Progression : 75%` | Encodage des volontés sous format CBOR canonique déterministe (RFC 8949). |
| **4** | **Scellement & Fin ✨** | Acte des Volontés Scellé pour la Carte Directives | `Statut : success` | Volontés immuables gravées dans la structure de données de la Carte 2 Directives. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-107 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Formulaire des Volontés Vierge
*Questionnaire funéraire en attente d'arbitrage par la famille.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Volontés Civiles</span>
                        <span class="wf-status-badge wf-badge-neutral">Formulaire en Attente</span>
                      </div>
                      <div class="wf-field-group">
                        <label class="wf-label">Cérémonie Souhaitée <span class="wf-req">*</span></label>
                        <div class="wf-select-placeholder">-- Sélectionner : Civile, Religieuse, Hommage intime --</div>
                      </div>
                      <div class="wf-field-group">
                        <label class="wf-label">Destination Mémorielle <span class="wf-req">*</span></label>
                        <div class="wf-select-placeholder">-- Sarcomusation & Forêt cinéraire (Démonstrateur de faisabilité prospectif — Option non autorisée par le droit positif actuel (référence à confirmer par un juriste)) --</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">📜 Sceller les Volontés Civiles in-silico</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Validation des Choix Funéraires & Signature Famille
*Champs renseignés avec arbitrage formel : Sarcomusation mémorielle et arbre du souvenir.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Volontés Arrêtées</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Scellement enclenché</span>
                      </div>
                      <div class="wf-wills-summary wf-radar-pulse">
                        <div><strong>Cérémonie :</strong> Laïque solennelle</div>
                        <div><strong>Sépulture :</strong> Sarcomusation & Retour forestier (DEC-AET-05) <span class="wf-badge-warning">[Démonstrateur de faisabilité prospectif — Option non autorisée par le droit positif actuel (référence à confirmer par un juriste)]</span></div>
                        <div><strong>Arbre du Souvenir :</strong> Chêne n° F-2408 (Saint-Hubert)</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Scellement CBOR en cours...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Sérialisation Canonique & Chiffrement Préparatoire
*Encodage des volontés sous format CBOR canonique déterministe (RFC 8949).*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Sérialisation CBOR</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Encodage Légal (75%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 75%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [CORE-CBOR] Sérialisation clé 1 (cérémonie) et clé 2 (destination) : OK</code><br>
                        <code>> [CORE-CBOR] Vérification conformité Loi 20 juillet 1971 (référence à confirmer par un juriste) : SUCCÈS</code><br>
                        <code>> [CORE-CBOR] Calcul du condensat SHA-256 des volontés : 8e4b...910a</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Acte des Volontés Scellé pour la Carte Directives
*Volontés immuables gravées dans la structure de données de la Carte 2 Directives.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Volontés Scellées</span>
                        <span class="wf-status-badge wf-badge-success">✨ Conforme Loi 1971 (référence à confirmer par un juriste)</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">⚖️</span>
                        <div>
                          <strong>Volontés Funéraires Gravées in-silico</strong>
                          <p class="wf-subtext">Inaltérables • Primauté légale garantie • Carte 2 Directives prête</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Directives Médicales →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-108"></a>
## UC-108 : Directives Médicales Post-Mortem (Pacemaker, Dons, Legs)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-108` |
| **Catégorie Métier** | **Directives Médicales** |
| **Acteur Principal** | Famille & Conseiller |
| **Plateformes Cibles** | Web Standard (PWA Hors-Ligne), Natif (iOS & Android) |
| **Tags Clés** | `Pacemaker`, `DonOrganes`, `LegsCorps`, `SecuriteOperateurs` |
| **Base Légale & Normative** | Article L1232-17 §2 du CDLD (exérèse obligatoire des stimulateurs cardiaques) (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `PaxStudio Pro • Volet Médical d'Urgence & Sécurité` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Accès au volet de sécurité médicale post-mortem dans PaxStudio.

> [!TIP]
> **Postconditions Garanties :**
> Volet médical post-mortem validé, alerte pacemaker levée uniquement sur certificat médical officiel.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Contrôle obligatoire d'alerte sur la présence d'un stimulateur cardiaque (pacemaker) ou défibrillateur implantable (Art. L1232-17 §2 CDLD — référence à confirmer par un juriste).
2. Si stimulateur présent : blocage strict imposant le renseignement de l'attestation chirurgicale d'exérèse avec numéro d'ordre du médecin.
3. Recueil de la position sur le don d'organes (rappel de la loi belge du consentement présumé de 1986 — référence à confirmer par un juriste).
4. Enregistrement éventuel d'un protocole de legs du corps à la science sous 48h auprès d'une université conventionnée.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `has_pacemaker` | **Porteur de Stimulateur Cardiaque (Pacemaker)** | `select` | `OUI (Présence confirmée)` | Sélectionner | `ALERTE VITALE` | ✅ Requis |
| `pacemaker_cert` | **Attestation d'Exérèse Chirurgicale** | `file` | `certificat_exerese_dr_vaneck.pdf` | Téléverser attestation | `Obligatoire si Oui` | ✅ Requis |
| `pacemaker_doc` | **Médecin Certificateur & N° Ordre** | `text` | `Dr. Marc Vaneck — INAMI 1-40912-88-004` | Nom et INAMI | `Vérifié` | ✅ Requis |
| `organ_donation` | **Don d'Organes (Loi 1986 — référence à confirmer par un juriste)** | `select` | `Consentement Plein et Entier Confirmé` | Statut don | `Loi 1986 (référence à confirmer par un juriste)` | ✅ Requis |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_validate_medical` | **Valider le Volet Médical d'Urgence** | `primary` | `idle` | 🩺 |
| `btn_verify_inami` | **Vérifier Validité Ordre Médecin** | `secondary` | `idle` | 🔍 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Volet Médical d'Urgence Certifié
>
> **Badge de Conformité :** `Conforme Art. L1232-17 CDLD (référence à confirmer par un juriste)`
>
> **Détail Opérationnel :** Exérèse chirurgicale du pacemaker certifiée par le Dr. Vaneck. Zéro risque d'explosion.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_PACEMAKER_UNVERIFIED` |
| **Intitulé de l'Incident** | **Alerte Vitale : Stimulateur Cardiaque Non Retiré** |
| **Condition Déclenchante** | Déclaration d'un pacemaker sans téléversement d'attestation médicale d'exérèse chirurgicale. |
| **Message d'Erreur UI** | *« BLOCAGE DE SÉCURITÉ INVIOLABLE : Présence d'un pacemaker non retiré. Risque d'explosion thermique mortelle en crémation ou bioconversion. »* |
| **Action Corrective Requise** | **Fournir immédiatement l'attestation officielle d'exérèse signée par un médecin avec son numéro INAMI pour déverrouiller l'encodage.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStudio Pro • Volet Médical d'Urgence & Sécurité**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Alerte Pacemaker en Attente de Certification | *En attente utilisateur* | Pacemaker déclaré présent. Le système bloque tout encodage tant que l'attestation n'est pas fournie. |
| **2** | **Déclenchement ⚡** | Import de l'Attestation Médicale d'Exérèse Chirurgicale | `Téléversement du certificat de retrait signé par le Dr. Marc Vaneck` | Saisie de l'identifiant INAMI du praticien et levée de l'alerte bloquante. |
| **3** | **Traitement ⚙️** | Vérification Algorithmique & Levée du Verrou Légal | `Progression : 95%` | Validation de la structure de l'INAMI et encodage du certificat de sécurité médicale. |
| **4** | **Scellement & Fin ✨** | Sceau de Sécurité Médicale Déposé | `Statut : success` | Alerte rouge effacée, remplacée par le sceau vert de conformité chirurgicale. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-108 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Alerte Pacemaker en Attente de Certification
*Pacemaker déclaré présent. Le système bloque tout encodage tant que l'attestation n'est pas fournie.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Alerte de Sécurité Médicale</span>
                        <span class="wf-status-badge wf-badge-alert">⚠️ Stimulateur Déclaré</span>
                      </div>
                      <div class="wf-alert-card wf-alert-red">
                        <strong>ATTENTION OBLIGATOIRE : Présence d'un Pacemaker</strong>
                        <p class="wf-subtext">L'article L1232-17 §2 CDLD (référence à confirmer par un juriste) impose l'exérèse chirurgicale avant toute opération.</p>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-disabled" disabled>🩺 Valider le Volet Médical (Bloqué)</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Import de l'Attestation Médicale d'Exérèse Chirurgicale
*Saisie de l'identifiant INAMI du praticien et levée de l'alerte bloquante.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Attestation Médicale Reçue</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Certificat Médical Déposé</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Attestation d'exérèse reçue : Dr. Marc Vaneck (INAMI: 1-40912-88-004)</div>
                        <div class="wf-subtext">Dispositif médical retiré avec succès le 04/10/2026 à 09h15</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Valider la Conformité Médicale...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Vérification Algorithmique & Levée du Verrou Légal
*Validation de la structure de l'INAMI et encodage du certificat de sécurité médicale.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Contrôle Sécurité Exérèse (référence à confirmer par un juriste)</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Vérification Légale (95%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 95%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [LEGAL-CHECK] Format numéro INAMI médecin : Valide</code><br>
                        <code>> [LEGAL-CHECK] Règle Art. L1232-17 §2 satisfaite (référence à confirmer par un juriste) : Exérèse certifiée</code><br>
                        <code>> [LEGAL-CHECK] Levée formelle du verrou de pré-encodage : AUTORISÉ</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Sceau de Sécurité Médicale Déposé
*Alerte rouge effacée, remplacée par le sceau vert de conformité chirurgicale.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Sécurité Médicale Validée</span>
                        <span class="wf-status-badge wf-badge-success">✨ Exérèse Certifiée Conforme</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🛡️</span>
                        <div>
                          <strong>Sécurité des Opérateurs Funéraires Garantie</strong>
                          <p class="wf-subtext">Visa médical Dr. Vaneck scellé in-silico • Prêt pour compilation CBOR</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Compilation CBOR Déterministe →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-109"></a>
## UC-109 : Génération & Validation de la Capsule de Pré-Encodage CBOR

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-109` |
| **Catégorie Métier** | **Compilation & Core** |
| **Acteur Principal** | Conseiller & Système Core |
| **Plateformes Cibles** | Web Standard (PWA Hors-Ligne), Node.js / Core Engine |
| **Tags Clés** | `AeterniCore`, `CBOR`, `RFC8949`, `Determinisme` |
| **Base Légale & Normative** | Spécification technique IETF RFC 8949 (déterminisme binaire CBOR). |
| **Terminal / Canvas Wireframe** | `PaxStudio Pro • Compilateur AeterniCore RFC 8949` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Médias, volontés, charte graphique et directives médicales entièrement complétés.

> [!TIP]
> **Postconditions Garanties :**
> Fichier binaire capsule `.cbor` généré, scellé et prêt pour l'envoi vers PaxStation.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Agrégation de l'ensemble des données des 2 cartes par le moteur AeterniCore.
2. Application des règles de déterminisme strictes de la RFC 8949 (tri lexicographique des clés entières, entiers canoniques les plus courts).
3. Calcul de l'empreinte cryptographique SHA-256 canonique JCS de la capsule globale.
4. Vérification que la taille totale compilée ne dépasse pas 80 Ko, laissant une marge de sécurité sur les 92 Ko de l'ACOSJ.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `cbor_engine` | **Moteur CBOR** | `text` | `AeterniCore Deterministic v1.4.2` | Moteur | `RFC 8949` | ⭕ Optionnel |
| `cbor_sorting` | **Tri Canonique des Clés** | `checkbox` | `Actif (Bytewise-lexicographique)` | Tri | `Obligatoire` | ✅ Requis |
| `cbor_size` | **Taille Finale Compilée** | `text` | `78 412 octets (< 80 Ko recommandés / 92 Ko EEPROM)` | Taille | `Conforme` | ⭕ Optionnel |
| `sha256_hash` | **Condensat SHA-256 Canonique** | `text` | `a4f81c90...b1297e41 (64 hex)` | Empreinte | `Scellé` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_compile_cbor` | **Générer la Capsule CBOR Déterministe** | `primary` | `idle` | ⚡ |
| `btn_audit_cbor` | **Auditer Syntaxe Binaire RFC 8949** | `secondary` | `idle` | 🔍 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Capsule CBOR Compilée avec Succès
>
> **Badge de Conformité :** `100% Déterministe RFC 8949`
>
> **Détail Opérationnel :** 78 412 octets sérialisés. Zéro octet superflu. Empreinte SHA-256 générée.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_CBOR_NON_DETERMINISTIC` |
| **Intitulé de l'Incident** | **Non-Déterminisme Binaire CBOR** |
| **Condition Déclenchante** | Clés de dictionnaires non ordonnées ou entiers encodés sur un format non minimal. |
| **Message d'Erreur UI** | *« Erreur critique de compilation : La capsule CBOR produite viole les règles canoniques de la RFC 8949 §4.2.1. »* |
| **Action Corrective Requise** | **Réexécuter la canonisation AeterniCore en forçant le tri lexicographique des clés entières.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStudio Pro • Compilateur AeterniCore RFC 8949**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Données Rassemblées en Attente de Compilation | *En attente utilisateur* | Toutes les sections sont prêtes. L'agrégat binaire n'est pas encore compilé. |
| **2** | **Déclenchement ⚡** | Clic sur 'Générer la Capsule CBOR Déterministe' | `Lancement du pipeline de sérialisation binaire déterministe` | Ordonnancement binaire des clés entières et calcul de l'arbre binaire. |
| **3** | **Traitement ⚙️** | Génération du Hash SHA-256 Canonique JCS | `Progression : 88%` | Calcul de l'empreinte cryptographique de la capsule (RFC 8785 / RFC 8949). |
| **4** | **Scellement & Fin ✨** | Capsule Binaire `.cbor` Scellée avec Succès | `Statut : success` | Fichier de pré-encodage scellé prêt pour transfert sécurisé vers PaxStation. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-109 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Données Rassemblées en Attente de Compilation
*Toutes les sections sont prêtes. L'agrégat binaire n'est pas encore compilé.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Agrégateur AeterniCore</span>
                        <span class="wf-status-badge wf-badge-neutral">Prêt pour Compilation</span>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-mini-stat">📸 Portraits : 37.2 Ko</div>
                        <div class="wf-mini-stat">🎙️ Audio Vocal : 58.2 Ko</div>
                        <div class="wf-mini-stat">📜 Volontés : 2.1 Ko</div>
                        <div class="wf-mini-stat">🩺 Médical : 1.4 Ko</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">⚡ Générer la Capsule CBOR Déterministe</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Clic sur 'Générer la Capsule CBOR Déterministe'
*Ordonnancement binaire des clés entières et calcul de l'arbre binaire.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Sérialisation en Cours</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Pipeline AeterniCore Actif</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">⚡ Tri Bytewise-Lexicographique des Cartes CBOR</div>
                        <div class="wf-subtext">Conversion des textes UTF-8 et injection des flux WebP/Opus</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Compilation Binaire en cours...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Génération du Hash SHA-256 Canonique JCS
*Calcul de l'empreinte cryptographique de la capsule (RFC 8785 / RFC 8949).*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Calculateur Cryptographique</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Hachage SHA-256 (88%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 88%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [CBOR-SERIAL] 78 412 octets générés au format compact déterministe</code><br>
                        <code>> [JCS-HASH] Calcul SHA-256 sur sig_structure préparatoire...</code><br>
                        <code>> [JCS-HASH] Digest : a4f81c9053d867c29019b7842ef84a12...b129 : OK</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Capsule Binaire `.cbor` Scellée avec Succès
*Fichier de pré-encodage scellé prêt pour transfert sécurisé vers PaxStation.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Capsule Prête</span>
                        <span class="wf-status-badge wf-badge-success">✨ Capsule 78 412 o Scellée</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">📦</span>
                        <div>
                          <strong>Capsule CBOR Déterministe Prête pour PaxStation</strong>
                          <p class="wf-subtext">SHA-256 : a4f8...b129 • Conforme RFC 8949 • 0 octet superflu</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Bon à Tirer (BAT) →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-110"></a>
## UC-110 : Bon à Tirer (BAT) Numérique & Validation Familiale

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-110` |
| **Catégorie Métier** | **Validation Finale** |
| **Acteur Principal** | Famille & Conseiller Funéraire |
| **Plateformes Cibles** | Web Standard (PWA Hors-Ligne), Natif (iOS & Android) |
| **Tags Clés** | `BAT`, `Emargement`, `Signature`, `Contrat` |
| **Base Légale & Normative** | Code civil belge (art. 1322 - valeur probante de la signature électronique) (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `PaxStudio Pro • Bon à Tirer (BAT) Numérique Officiel` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Capsule CBOR générée et visuels recto/verso des 2 cartes approuvés.

> [!TIP]
> **Postconditions Garanties :**
> Ordre d'encodage officiel émis, BAT PDF/CBOR archivé localement avec double émargement.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Affichage de la synthèse solennelle du Bon à Tirer (BAT) numérique récapitulant les médias, les textes, les directives médicales et l'empreinte de la capsule.
2. Signature manuscrite sur écran tactile par le mandataire de la famille et le conseiller funéraire.
3. Horodatage local certifié et scellement non répudiable du document contractuel BAT.
4. Transmission sécurisée de l'ordre d'encodage et de gravure à l'application PaxStation de l'atelier.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `family_signatory` | **Mandataire Familial** | `text` | `Claire Dubois (Épouse et Mandataire désignée)` | Nom mandataire | `Ayant Droit` | ✅ Requis |
| `pro_signatory` | **Conseiller Funéraire Agréé** | `text` | `Jean-Luc Lambert (Le Pax Funèbre Namur)` | Nom conseiller | `Opérateur` | ✅ Requis |
| `sig_status` | **Émargement Tactile Requis** | `checkbox` | `Double émargement numérique apposé` | Signature | `Légal` | ✅ Requis |
| `timestamp_utc` | **Horodatage Certifié** | `text` | `2026-10-04T15:30:00Z (Horodatage local non répudiable)` | Horodatage | `Certifié` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_sign_bat` | **Signer le BAT Numérique & Transmettre à PaxStation** | `primary` | `idle` | ✍️ |
| `btn_print_bat` | **Imprimer Copie Papier Famille** | `secondary` | `idle` | 🖨️ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Bon à Tirer Définitivement Validé
>
> **Badge de Conformité :** `Conforme Art. 1322 Code Civil (référence à confirmer par un juriste)`
>
> **Détail Opérationnel :** Double signature enregistrée. Ordre d'encodage transmis à PaxStation pour gravure physique.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_BAT_UNAUTHORIZED_SIGNATURE` |
| **Intitulé de l'Incident** | **Défaut d'Habilitation du Signataire** |
| **Condition Déclenchante** | Absence de lien d'ayant droit ou mandat post-mortem contesté. |
| **Message d'Erreur UI** | *« Erreur juridique : Le signataire n'a pas produit de mandat d'ayant droit valide pour engager la commande funéraire. »* |
| **Action Corrective Requise** | **Vérifier le mandat post-mortem ou solliciter la signature conjointe des héritiers réservataires.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStudio Pro • Bon à Tirer (BAT) Numérique Officiel**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Synthèse du Bon à Tirer en Attente de Signature | *En attente utilisateur* | Document officiel affiché. Les deux zones de signature manuscrite sont vides. |
| **2** | **Déclenchement ⚡** | Émargement Tactile Conjoint Famille & Conseiller | `Apposition des deux signatures manuscrites au stylet sur tablette` | Tracé vectoriel des deux signatures avec surbrillance dorée instantanée. |
| **3** | **Traitement ⚙️** | Scellement Légal & Transmission vers PaxStation | `Progression : 92%` | Horodatage cryptographique non répudiable et émission du bon de production. |
| **4** | **Scellement & Fin ✨** | BAT Verrouillé & Ordre d'Encodage Transmis | `Statut : success` | Validation finale de PaxStudio terminée avec succès. La session bascule vers PaxStation. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-110 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Synthèse du Bon à Tirer en Attente de Signature
*Document officiel affiché. Les deux zones de signature manuscrite sont vides.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Bon à Tirer (BAT) Numérique</span>
                        <span class="wf-status-badge wf-badge-neutral">En Attente des Signatures</span>
                      </div>
                      <div class="wf-bat-summary">
                        <div><strong>Commande :</strong> Lot Duo Le Pax Funèbre (Sanctuaire + Directives)</div>
                        <div><strong>Défunt :</strong> Henri Dubois • Empreinte CBOR : a4f8...b129</div>
                        <div><strong>Sécurité :</strong> Pacemaker retiré (Dr. Vaneck) • Sarcomusation (Démonstrateur de faisabilité prospectif — Option non autorisée par le droit positif actuel (référence à confirmer par un juriste)) validée</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">✍️ Signer le BAT Numérique & Transmettre</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Émargement Tactile Conjoint Famille & Conseiller
*Tracé vectoriel des deux signatures avec surbrillance dorée instantanée.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Émargement Électronique</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Double Signature Apposée</span>
                      </div>
                      <div class="wf-signature-boxes wf-radar-pulse">
                        <div class="wf-sig-box">✒️ Signature Famille (Claire Dubois) : Apposée ✓</div>
                        <div class="wf-sig-box">✒️ Signature Conseiller (J-L Lambert) : Apposée ✓</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Scellement Légal du Contrat...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Scellement Légal & Transmission vers PaxStation
*Horodatage cryptographique non répudiable et émission du bon de production.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Transmission Atelier PaxStation</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Envoi Sécurisé (92%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 92%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [BAT-LEGAL] Horodatage certifié : 2026-10-04T15:30:00Z</code><br>
                        <code>> [BAT-LEGAL] Verrouillage contractuel non répudiable (Art. 1322 C. civ. — référence à confirmer par un juriste) : OK</code><br>
                        <code>> [NETWORK-LOCAL] Ordre d'encodage n° ORD-2026-0491 transmis à PaxStation</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : BAT Verrouillé & Ordre d'Encodage Transmis
*Validation finale de PaxStudio terminée avec succès. La session bascule vers PaxStation.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Processus Terminé</span>
                        <span class="wf-status-badge wf-badge-success">✨ BAT Scellé & Transmis</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🤝</span>
                        <div>
                          <strong>Commande Validée par la Famille</strong>
                          <p class="wf-subtext">Ordre transmis à PaxStation pour gravure sur silicium ACOSJ 92k</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Bascule vers App 2 : PaxStation Encodage →</button>
                      </div>
                    </div>
```

</details>

---
