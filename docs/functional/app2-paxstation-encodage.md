# Application 2 — PaxStation Encodage Silicium (UC-201 à UC-210)

**Station Technique Professionnelle de Gravure Matérielle & Scellement Cryptographique**

> [!NOTE]
> **Périmètre Applicatif :**
> L'application **PaxStation Encodage Silicium** est l'outil technique réservé aux professionnels habilités du réseau *Le Pax Funèbre*. Connectée au lecteur de bureau **ACR1552U via WebUSB ou PC/SC CCID**, elle assure le dialogue APDU IsoDep de bas niveau avec la puce **JavaCard ACOSJ 92 Ko EEPROM**, l'initialisation du système de fichiers sécurisé, le scellement cryptographique déterministe **COSE_Sign1 (Ed25519 / ES256 avec s normalisé bas)**, l'activation du fusible matériel in-silico (protection anti-tamper en lecture seule) et le pilotage de l'impression thermique haute définition 600 DPI.

## 📌 Sommaire des Micro Use-Cases Spécifiés

| ID | Titre du Cas d'Usage | Catégorie Métier | Acteur | Plateformes | Référence Normative |
| :---: | :--- | :--- | :--- | :--- | :--- |
| [`UC-201`](#uc-201) | [Connexion Station de Bureau ACR1552U WebUSB](#uc-201) | **Matériel & Poste Pro** | Opérateur d'Encodage | WebUSB (Chromium Desktop), PC/SC (Desktop Natif) | Spécification USB CCID (Integrated Circuit(s) Cards Interface Device, USB-IF). |
| [`UC-202`](#uc-202) | [Insertion JavaCard ACOSJ 92 Ko & Vérification ATS APDU](#uc-202) | **Silicium & Détection** | Opérateur d'Encodage | WebUSB (Chromium Desktop), PC/SC (Desktop Natif) | Norme ISO/IEC 7816-4 (organisation, sécurité et commandes pour les échanges d'informations). |
| [`UC-203`](#uc-203) | [Formatage EEPROM & Initialisation EF Silicium (STORAGE-001)](#uc-203) | **Système de Fichiers Puce** | Opérateur d'Encodage | WebUSB (Chromium Desktop), PC/SC (Desktop Natif) | Spécification technique AeterniTrak STORAGE-001 (allocation EEPROM JavaCard). |
| [`UC-204`](#uc-204) | [Ingestion de la Capsule & Canonisation CBOR RFC 8949](#uc-204) | **Compilation & Core** | Opérateur d'Encodage | WebUSB (Chromium Desktop), Node.js / Core Engine | Spécification technique IETF RFC 8949 (CBOR Deterministic Encoding Rules §4.2.1). |
| [`UC-205`](#uc-205) | [Injection par Blocs APDU Sécurisés sur la Puce](#uc-205) | **Gravure Silicium** | Opérateur d'Encodage | WebUSB (Chromium Desktop), PC/SC (Desktop Natif) | Spécification technique ISO/IEC 7816-4 §7.2 (commandes d'écriture binaire). |
| [`UC-206`](#uc-206) | [Scellement Cryptographique COSE_Sign1 PaxFunèbre (Secure Element)](#uc-206) | **Cryptographie & Signature** | Opérateur d'Encodage | WebUSB (Chromium Desktop), PC/SC (Desktop Natif) | Spécification technique IETF RFC 9052 (COSE Structures and Process) et RFC 9596 (COSE typ Header). |
| [`UC-207`](#uc-207) | [Contrôle Strict Anti-Malléabilité du s Bas (RFC 9052)](#uc-207) | **Sécurité Mathématique** | Opérateur & Moteur de Sécurité | WebUSB (Chromium Desktop), Node.js / Core Engine | Guide BSI TR-03111 (Technical Guideline: Elliptic Curve Cryptography §4.1.3). |
| [`UC-208`](#uc-208) | [Verrouillage Matériel Irréversible in-silico (Anti-Tamper)](#uc-208) | **Sécurité Silicium** | Opérateur d'Encodage | WebUSB (Chromium Desktop), PC/SC (Desktop Natif) | Spécification JavaCard 3.0 Classic (Security and Applet Lifecycle Management). |
| [`UC-209`](#uc-209) | [Impression Thermique & Laser Haute Précision Recto/Verso](#uc-209) | **Impression Physique** | Opérateur d'Encodage | PC/SC (Desktop Natif), Web Standard (PWA Hors-Ligne) | Norme ISO/IEC 7810 ID-1 (durabilité physique et résistance aux torsions des cartes d'identité). |
| [`UC-210`](#uc-210) | [Contrôle de Recette Post-Gravure & PV de Remise Officiel](#uc-210) | **Assurance Qualité & Conformité** | Opérateur d'Encodage & Conseiller | PC/SC (Desktop Natif), Web Standard (PWA Hors-Ligne) | Code de droit économique belge (garantie de conformité des biens et services funéraires). |

---

<a id="uc-201"></a>
## UC-201 : Connexion Station de Bureau ACR1552U WebUSB

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-201` |
| **Catégorie Métier** | **Matériel & Poste Pro** |
| **Acteur Principal** | Opérateur d'Encodage |
| **Plateformes Cibles** | WebUSB (Chromium Desktop), PC/SC (Desktop Natif) |
| **Tags Clés** | `ACR1552U`, `WebUSB`, `PCSC`, `Pilote` |
| **Base Légale & Normative** | Spécification USB CCID (Integrated Circuit(s) Cards Interface Device, USB-IF). |
| **Terminal / Canvas Wireframe** | `PaxStation Station Pro • ACR1552U USB CCID Monitor` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Poste de travail d'agence avec lecteur ACR1552U branché sur port USB 3.0.

> [!TIP]
> **Postconditions Garanties :**
> Canal de communication USB ouvert à 12 Mbps, prêt pour la détection de puces sans contact.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Ouverture de PaxStation Encodage sur Chrome / Edge ou client lourd de bureau.
2. Détection du descripteur USB Vendor ID 0x072F (Advanced Card Systems) et Product ID 0x2200 (ACR1552U USB CCID Reader).
3. Demande d'autorisation d'accès matériel WebUSB et initialisation du canal de commande.
4. Passage du voyant LED du lecteur au vert fixe (état prêt) et affichage du moniteur de liaison 106 kbps.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `usb_driver` | **Pilote Matériel** | `select` | `WebUSB Chromium Direct (USB CCID v1.1)` | Pilote | `WebUSB` | ✅ Requis |
| `device_name` | **Périphérique Détecté** | `text` | `ACS ACR1552U USB Contactless Reader (VID:072F / PID:2200)` | Lecteur | `USB 3.0` | ⭕ Optionnel |
| `baudrate` | **Baudrate RF Contactless** | `text` | `106 kbps ISO/IEC 14443 Type A` | Baudrate | `106k` | ⭕ Optionnel |
| `firmware_version` | **Firmware Lecteur** | `text` | `v2.04 SAM Secure Ready` | Firmware | `À Jour` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_connect_acr` | **Autoriser l'Accès WebUSB AeterniTrak** | `primary` | `idle` | 🔌 |
| `btn_ping_rf` | **Tester Boucle RF & Bip Sonore** | `secondary` | `idle` | 📡 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Lecteur ACR1552U Connecté
>
> **Badge de Conformité :** `Canal USB CCID 12 Mbps Ouvert`
>
> **Détail Opérationnel :** Lecteur opérationnel. Champ électromagnétique RF 13.56 MHz actif en veille.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_ACR1552U_DEVICE_DETACHED` |
| **Intitulé de l'Incident** | **Périphérique ACR1552U Non Détecté** |
| **Condition Déclenchante** | Câble USB déconnecté, hub USB sous-alimenté ou absence de permission WebUSB du navigateur. |
| **Message d'Erreur UI** | *« Erreur matérielle : Impossible d'établir la liaison avec le lecteur de bureau ACR1552U. »* |
| **Action Corrective Requise** | **Vérifier le branchement USB, autoriser l'accès périphérique dans la barre d'adresse et recharger la session.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Station Pro • ACR1552U USB CCID Monitor**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Station en Attente de Connexion USB | *En attente utilisateur* | Lecteur non appairé. L'interface affiche l'invite de connexion WebUSB. |
| **2** | **Déclenchement ⚡** | Autorisation WebUSB Accordée par l'Opérateur | `Clic sur 'Autoriser l'accès WebUSB' et sélection du périphérique 0x072F` | Dialogue natif Chromium de sélection du périphérique USB avec confirmation opérateur. |
| **3** | **Traitement ⚙️** | Initialisation du Firmware & Test Boucle RF 13.56 MHz | `Progression : 80%` | Envoi de la commande de contrôle firmware et activation de l'antenne sans contact. |
| **4** | **Scellement & Fin ✨** | Station Prête pour l'Insertion de Silicium | `Statut : success` | Lecteur prêt en écoute active. La station attend la pose de la JavaCard ACOSJ. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-201 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Station en Attente de Connexion USB
*Lecteur non appairé. L'interface affiche l'invite de connexion WebUSB.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Gestionnaire Périphériques</span>
                        <span class="wf-status-badge wf-badge-alert">USB Déconnecté</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-usb-icon">🔌</span>
                        <div><strong>Aucun lecteur ACR1552U actif</strong></div>
                        <div class="wf-subtext">Branchez le câble USB et accordez l'autorisation WebUSB au navigateur</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔌 Autoriser l'Accès WebUSB AeterniTrak</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Autorisation WebUSB Accordée par l'Opérateur
*Dialogue natif Chromium de sélection du périphérique USB avec confirmation opérateur.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Négociation USB</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Poignée de Main USB</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Périphérique Détecté : ACS ACR1552U (VID:072F PID:2200)</div>
                        <div class="wf-subtext">Ouverture du descripteur de communication CCID sans pilote tiers</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Établissement du canal sécurisé...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Initialisation du Firmware & Test Boucle RF 13.56 MHz
*Envoi de la commande de contrôle firmware et activation de l'antenne sans contact.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Console Matérielle</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Initialisation USB (80%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 80%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [USB-CCID] Contrôle descripteur : Firmware v2.04 SAM Secure Ready</code><br>
                        <code>> [RF-RADIO] Allumage porteuse 13.56 MHz ISO 14443-A : Prêt</code><br>
                        <code>> [HARDWARE] LED verte fixe allumée • Bip sonore de confirmation émis</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Station Prête pour l'Insertion de Silicium
*Lecteur prêt en écoute active. La station attend la pose de la JavaCard ACOSJ.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Poste Prêt</span>
                        <span class="wf-status-badge wf-badge-success">✨ ACR1552U En Ligne (12 Mbps)</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🟢</span>
                        <div>
                          <strong>Poste d'Encodage Professionnel Opérationnel</strong>
                          <p class="wf-subtext">Antenne NFC active (106 kbps) • Prêt à recevoir la JavaCard ACOSJ 92k</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Insertion de la Carte ACOSJ →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-202"></a>
## UC-202 : Insertion JavaCard ACOSJ 92 Ko & Vérification ATS APDU

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-202` |
| **Catégorie Métier** | **Silicium & Détection** |
| **Acteur Principal** | Opérateur d'Encodage |
| **Plateformes Cibles** | WebUSB (Chromium Desktop), PC/SC (Desktop Natif) |
| **Tags Clés** | `ACOSJ`, `JavaCard`, `ATS`, `APDU`, `ISO14443-4` |
| **Base Légale & Normative** | Norme ISO/IEC 7816-4 (organisation, sécurité et commandes pour les échanges d'informations). |
| **Terminal / Canvas Wireframe** | `PaxStation Station Pro • Moniteur APDU Silicium ISO 7816` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Lecteur ACR1552U connecté et en écoute RF.

> [!TIP]
> **Postconditions Garanties :**
> Puce identifiée de manière unique, applet AeterniTrak active et prête pour l'initialisation.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. L'opérateur dépose la carte vierge ou le médaillon sur la zone sans contact du lecteur.
2. Détection du champ de proximité et émission de l'Answer to Select (ATS) conforme ISO/IEC 14443-4.
3. Négociation du Protocole Parameter Selection (PPS) pour confirmation de la vitesse de 106 kbps.
4. Sélection de l'Applet AeterniTrak via commande APDU `SELECT AID A0 00 00 08 45 01` et vérification du code de statut `90 00`.
5. Lecture de l'historique EEPROM pour confirmer la mémoire disponible de 92 Ko (ACOSJ).

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `chip_model` | **Modèle Silicium** | `text` | `ACOSJ JavaCard 3.0.4 Classic (92 Ko EEPROM)` | Puce | `Certifié` | ⭕ Optionnel |
| `ats_bytes` | **Réponse ATS Puce** | `text` | `3B 80 80 01 01 (ISO 14443-4 T=CL)` | ATS | `IsoDep` | ⭕ Optionnel |
| `applet_aid` | **AID AeterniTrak** | `text` | `A0 00 00 08 45 01 (Applet Active)` | AID | `Sélectionné` | ⭕ Optionnel |
| `status_word` | **Statut SW APDU** | `text` | `90 00 (Opération avec succès)` | SW | `Succès` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_select_aid` | **Interroger le Silicium (ATS & SELECT AID)** | `primary` | `idle` | 💳 |
| `btn_eject_card` | **Éjecter / Réinitialiser RF** | `secondary` | `idle` | ⏏️ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** JavaCard ACOSJ 92k Détectée
>
> **Badge de Conformité :** `Code APDU 90 00`
>
> **Détail Opérationnel :** Puce authentique homologuée. 92 160 octets d'EEPROM libre identifiés.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_ATS_COMMUNICATION_TIMEOUT` |
| **Intitulé de l'Incident** | **Délai de Réponse ATS Expiré** |
| **Condition Déclenchante** | Mauvais alignement de la carte sur l'antenne ou puce incompatible (non-JavaCard ou Mifare Classic). |
| **Message d'Erreur UI** | *« Erreur silicium : La puce présentée ne répond pas aux commandes APDU IsoDep ISO 14443-4. »* |
| **Action Corrective Requise** | **Repositionner la carte au centre du lecteur ACR1552U ou remplacer la carte par une JavaCard ACOSJ 92 Ko homologuée.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Station Pro • Moniteur APDU Silicium ISO 7816**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Champ RF en Écoute, Aucune Carte Présente | *En attente utilisateur* | Lecteur prêt. L'antenne cherche une carte à portée de couplage électromagnétique. |
| **2** | **Déclenchement ⚡** | Apposition Physique de la Carte sur le Lecteur | `Pose de la JavaCard ACOSJ sur le lecteur et émission de l'ATS` | Couplage inductif établi, bip de détection sonore et voyant bleu clignotant. |
| **3** | **Traitement ⚙️** | Échange APDU `SELECT AID` & Lecture Registres | `Progression : 70%` | Envoi de la commande `00 A4 04 00 07 A0 00 00 08 45 01` et vérification du code 90 00. |
| **4** | **Scellement & Fin ✨** | Carte ACOSJ Validée pour Gravure | `Statut : success` | Puce prête pour l'allocation des fichiers élémentaires EF01, EF02 et EF03. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-202 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Champ RF en Écoute, Aucune Carte Présente
*Lecteur prêt. L'antenne cherche une carte à portée de couplage électromagnétique.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Détecteur Silicium</span>
                        <span class="wf-status-badge wf-badge-neutral">En Attente de Carte</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-nfc-icon">📡</span>
                        <div><strong>Approchez ou insérez la carte JavaCard ACOSJ</strong></div>
                        <div class="wf-subtext">Portée sans contact : < 40 mm au-dessus du logo ACR1552U</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">💳 Interroger le Silicium (ATS & SELECT AID)</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Apposition Physique de la Carte sur le Lecteur
*Couplage inductif établi, bip de détection sonore et voyant bleu clignotant.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Couplage RF Établi</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Carte Détectée dans le Champ</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Signal RF détecté : Couplage inductif 13.56 MHz OK</div>
                        <div class="wf-subtext">Réception immédiate de l'Answer To Select (ATS) : 3B 80 80 01 01</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Émission APDU SELECT AID...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Échange APDU `SELECT AID` & Lecture Registres
*Envoi de la commande `00 A4 04 00 07 A0 00 00 08 45 01` et vérification du code 90 00.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Échange APDU Bas Niveau</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Négociation Silicium (70%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 70%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [APDU-TX] 00 A4 04 00 07 A0 00 00 08 45 01 (SELECT AID AeterniTrak)</code><br>
                        <code>< [APDU-RX] 90 00 (Statut : Succès d'activation de l'applet)</code><br>
                        <code>> [SYS-EEPROM] Lecture capacité : 92 160 octets (EEPROM vierge disponible)</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Carte ACOSJ Validée pour Gravure
*Puce prête pour l'allocation des fichiers élémentaires EF01, EF02 et EF03.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Silicium Prêt</span>
                        <span class="wf-status-badge wf-badge-success">✨ ACOSJ 92k Identifiée (90 00)</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">💾</span>
                        <div>
                          <strong>Puce JavaCard ACOSJ 92 Ko Prête pour Gravure</strong>
                          <p class="wf-subtext">UID matériel certifié • 92 160 octets libres • Applet AeterniTrak en ligne</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Formatage EEPROM & EF →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-203"></a>
## UC-203 : Formatage EEPROM & Initialisation EF Silicium (STORAGE-001)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-203` |
| **Catégorie Métier** | **Système de Fichiers Puce** |
| **Acteur Principal** | Opérateur d'Encodage |
| **Plateformes Cibles** | WebUSB (Chromium Desktop), PC/SC (Desktop Natif) |
| **Tags Clés** | `EEPROM`, `EF`, `STORAGE-001`, `Allocation` |
| **Base Légale & Normative** | Spécification technique AeterniTrak STORAGE-001 (allocation EEPROM JavaCard). |
| **Terminal / Canvas Wireframe** | `PaxStation Station Pro • Partitionneur EEPROM Silicium (STORAGE-001)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> JavaCard sélectionnée avec succès et authentifiée en mode administration.

> [!TIP]
> **Postconditions Garanties :**
> Système de fichiers silicium initialisé selon la cartographie stricte du jalon STORAGE-001.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Envoi de la commande APDU de formatage sécurisé pour effacement des anciennes structures ou résidus d'usine.
2. Création du Master File (MF) et du Dedicated File (DF AeterniTrak).
3. Création des trois Elementary Files (EF) prescrits par STORAGE-001 :
4. - `EF01 (ID)` : 2 048 octets réservés pour métadonnées et identifiant unique de carte.
5. - `EF02 (Profile)` : 16 384 octets réservés pour le profil CBOR complet (volontés, directives, textes).
6. - `EF03 (Media)` : 73 728 octets réservés pour les portraits WebP et l'audio vocal.
7. Vérification de l'absence de fragmentation mémoire.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `ef01_size` | **Partition EF01 (Meta ID)** | `number` | `2048` | Taille | `2 Ko` | ✅ Requis |
| `ef02_size` | **Partition EF02 (Profile CBOR)** | `number` | `16384` | Taille | `16 Ko` | ✅ Requis |
| `ef03_size` | **Partition EF03 (Medias WebP/Opus)** | `number` | `73728` | Taille | `72 Ko` | ✅ Requis |
| `total_allocated` | **Total Alloué** | `text` | `92 160 octets (100% sans fragmentation)` | Total | `Optimum` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_format_eeprom` | **Initialiser la Structure EF Silicium (STORAGE-001)** | `primary` | `idle` | 🗄️ |
| `btn_check_ef` | **Vérifier Table d'Allocation EF** | `secondary` | `idle` | 🔍 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Système de Fichiers Silicium Initialisé
>
> **Badge de Conformité :** `Jalon STORAGE-001 Validé`
>
> **Détail Opérationnel :** EF01 (2 Ko), EF02 (16 Ko), EF03 (72 Ko) alloués avec succès. Zéro fragment.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_EEPROM_QUOTA_EXCEEDED` |
| **Intitulé de l'Incident** | **Dépassement de la Capacité EEPROM** |
| **Condition Déclenchante** | Tentative d'allocation d'une partition dont la taille dépasse les 92 Ko de la puce physique. |
| **Message d'Erreur UI** | *« Erreur d'allocation : La somme des partitions demandées dépasse la taille maximale de l'EEPROM ACOSJ. »* |
| **Action Corrective Requise** | **Restaurer les tailles standard prescrites par STORAGE-001 (2 Ko, 16 Ko, 72 Ko).** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Station Pro • Partitionneur EEPROM Silicium (STORAGE-001)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | EEPROM Vierge Non Partitionnée | *En attente utilisateur* | Carte connectée. La table de fichiers élémentaires n'est pas encore créée. |
| **2** | **Déclenchement ⚡** | Clic sur 'Initialiser la Structure EF Silicium' | `Émission des commandes APDU de création des fichiers EF01, EF02 et EF03` | Ordre d'écriture physique de la structure de répertoires in-silico. |
| **3** | **Traitement ⚙️** | Écriture APDU des Descripteurs EF & Vérification Codes 90 00 | `Progression : 85%` | La puce confirme la création de chaque bloc de mémoire flash. |
| **4** | **Scellement & Fin ✨** | Structure EF01, EF02, EF03 Initialisée avec Succès | `Statut : success` | Système de fichiers prêt pour recevoir les flux de données compressés. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-203 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : EEPROM Vierge Non Partitionnée
*Carte connectée. La table de fichiers élémentaires n'est pas encore créée.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Partitionneur EEPROM</span>
                        <span class="wf-status-badge wf-badge-neutral">EEPROM Vierge (0/3 EF créés)</span>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-mini-stat">EF01 (ID) : En attente</div>
                        <div class="wf-mini-stat">EF02 (Profile) : En attente</div>
                        <div class="wf-mini-stat">EF03 (Media) : En attente</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🗄️ Initialiser la Structure EF Silicium</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Clic sur 'Initialiser la Structure EF Silicium'
*Ordre d'écriture physique de la structure de répertoires in-silico.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Allocation Silicium</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Création des Fichiers EF</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Envoi APDU `CREATE FILE` pour EF01, EF02 et EF03</div>
                        <div class="wf-subtext">Partitionnement strict : 2 Ko (ID), 16 Ko (Profil), 72 Ko (Médias)</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Écriture des tables d'allocation...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Écriture APDU des Descripteurs EF & Vérification Codes 90 00
*La puce confirme la création de chaque bloc de mémoire flash.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Journal d'Allocation Silicium</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Création EF (85%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 85%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [APDU-TX] 00 E0 00 00 07 62 05 01 08 00 (CREATE EF01 : 2048 o) -> 90 00</code><br>
                        <code>> [APDU-TX] 00 E0 00 00 07 62 05 02 40 00 (CREATE EF02 : 16384 o) -> 90 00</code><br>
                        <code>> [APDU-TX] 00 E0 00 00 07 62 05 03 20 00 (CREATE EF03 : 73728 o) -> 90 00</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Structure EF01, EF02, EF03 Initialisée avec Succès
*Système de fichiers prêt pour recevoir les flux de données compressés.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Silicium Partitionné</span>
                        <span class="wf-status-badge wf-badge-success">✨ Jalon STORAGE-001 OK</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🗄️</span>
                        <div>
                          <strong>Partitions EF Silicium Créées sans Fragmentation</strong>
                          <p class="wf-subtext">EF01 (2 Ko) • EF02 (16 Ko) • EF03 (72 Ko) • Prêt pour injection capsule</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Ingestion de la Capsule CBOR →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-204"></a>
## UC-204 : Ingestion de la Capsule & Canonisation CBOR RFC 8949

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-204` |
| **Catégorie Métier** | **Compilation & Core** |
| **Acteur Principal** | Opérateur d'Encodage |
| **Plateformes Cibles** | WebUSB (Chromium Desktop), Node.js / Core Engine |
| **Tags Clés** | `Capsule`, `Ingestion`, `CBOR`, `RFC8949`, `JCS` |
| **Base Légale & Normative** | Spécification technique IETF RFC 8949 (CBOR Deterministic Encoding Rules §4.2.1). |
| **Terminal / Canvas Wireframe** | `PaxStation Station Pro • Validateur Canonique CBOR RFC 8949` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Fichier capsule `.cbor` reçu depuis PaxStudio via réseau local ou clé de transfert.

> [!TIP]
> **Postconditions Garanties :**
> Capsule 100% validée, conforme à l'ordre BAT, prête pour le découpage en blocs APDU.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Chargement du binaire de la capsule et contrôle de syntaxe CBOR stricte.
2. Vérification de l'absence d'octets résiduels après le payload (règle anti-injection REJ006).
3. Recalcul indépendant de l'empreinte SHA-256 canonique JCS de la charge utile.
4. Confrontation de l'empreinte avec l'ordre de fabrication BAT signé par la famille.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `capsule_file` | **Fichier Source** | `file` | `capsule_paxstudio_78k.cbor (78 412 octets)` | Capsule | `Source` | ✅ Requis |
| `trailing_bytes` | **Contrôle Octets Résiduels** | `text` | `0 octet superflu (Règle REJ006 respectée)` | Résidus | `REJ006 OK` | ⭕ Optionnel |
| `hash_jcs` | **Hash Recalculé JCS** | `text` | `a4f81c90...b1297e41` | SHA-256 | `Calculé` | ⭕ Optionnel |
| `bat_match` | **Concordance Ordre BAT** | `text` | `100% IDENTIQUE à l'ordre n° ORD-2026-0491` | BAT | `Conforme` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_validate_capsule` | **Vérifier & Découper en Blocs APDU** | `primary` | `idle` | 📦 |
| `btn_view_cbor_tree` | **Inspecter Arbre Détaillé CBOR** | `secondary` | `idle` | 🌳 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Capsule CBOR Parfaitement Conforme
>
> **Badge de Conformité :** `Empreinte BAT Validée`
>
> **Détail Opérationnel :** Zéro octet superflu. Hachage SHA-256 concordant avec le Bon à Tirer signé.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_CBOR_REJ006_TRAILING_BYTES` |
| **Intitulé de l'Incident** | **Présence d'Octets Résiduels Post-Enveloppe** |
| **Condition Déclenchante** | Fichier corrompu ou injection de données après la fin de la carte CBOR. |
| **Message d'Erreur UI** | *« Erreur d'intégrité : Présence d'octets résiduels après la fermeture de l'enveloppe CBOR (violation règle REJ006). »* |
| **Action Corrective Requise** | **Rejeter la capsule et redemander une génération propre depuis PaxStudio.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Station Pro • Validateur Canonique CBOR RFC 8949**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Capsule Reçue en Attente d'Audit d'Intégrité | *En attente utilisateur* | Fichier de 78 Ko chargé. La vérification d'empreinte contre le BAT n'est pas encore faite. |
| **2** | **Déclenchement ⚡** | Lancement du Contrôle d'Intégrité & Canonisation | `Clic sur 'Vérifier & Découper en Blocs APDU'` | Décodage déterministe binaire et calcul du SHA-256 en mémoire vive. |
| **3** | **Traitement ⚙️** | Découpage en 306 Blocs APDU de 255 Octets | `Progression : 88%` | Segmentation des 78 Ko pour injection séquentielle via la commande IsoDep `UPDATE BINARY`. |
| **4** | **Scellement & Fin ✨** | Capsule Prête pour Gravure Silicium | `Statut : success` | Les 306 blocs sont mis en file d'attente d'écriture sur la puce ACOSJ. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-204 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Capsule Reçue en Attente d'Audit d'Intégrité
*Fichier de 78 Ko chargé. La vérification d'empreinte contre le BAT n'est pas encore faite.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Ingestion de Capsule</span>
                        <span class="wf-status-badge wf-badge-neutral">En Attente de Contrôle</span>
                      </div>
                      <div class="wf-capsule-file-box">
                        <strong>capsule_paxstudio_78k.cbor</strong> (78 412 octets)
                        <div class="wf-subtext">Ordre associé : ORD-2026-0491 (Famille Dubois)</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">📦 Vérifier & Découper en Blocs APDU</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Lancement du Contrôle d'Intégrité & Canonisation
*Décodage déterministe binaire et calcul du SHA-256 en mémoire vive.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Analyse Binaire</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Décodage RFC 8949</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Contrôle d'absence d'octets résiduels (REJ006) : Conforme</div>
                        <div class="wf-subtext">Comparaison de l'empreinte avec le Bon à Tirer signé</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Calcul du condensat cryptographique...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Découpage en 306 Blocs APDU de 255 Octets
*Segmentation des 78 Ko pour injection séquentielle via la commande IsoDep `UPDATE BINARY`.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Moteur de Segmentation APDU</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Segmentation (88%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 88%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [JCS-CORE] Recalcul SHA-256 : a4f81c9053d867c29019b7842ef84a12...b129</code><br>
                        <code>> [BAT-CHECK] Confrontation BAT : Égalité parfaite (100% concordant)</code><br>
                        <code>> [APDU-SEG] Découpage en 306 tranches de 255 octets (Payload EF02 + EF03)</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Capsule Prête pour Gravure Silicium
*Les 306 blocs sont mis en file d'attente d'écriture sur la puce ACOSJ.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Prêt pour Gravure</span>
                        <span class="wf-status-badge wf-badge-success">✨ 306 Blocs Prêts</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">⚡</span>
                        <div>
                          <strong>Capsule Validée contre l'Ordre BAT</strong>
                          <p class="wf-subtext">306 blocs APDU prêts à être injectés sur les partitions EF02 et EF03</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Injection Silicium APDU →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-205"></a>
## UC-205 : Injection par Blocs APDU Sécurisés sur la Puce

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-205` |
| **Catégorie Métier** | **Gravure Silicium** |
| **Acteur Principal** | Opérateur d'Encodage |
| **Plateformes Cibles** | WebUSB (Chromium Desktop), PC/SC (Desktop Natif) |
| **Tags Clés** | `APDU`, `UpdateBinary`, `IsoDep`, `Gravure` |
| **Base Légale & Normative** | Spécification technique ISO/IEC 7816-4 §7.2 (commandes d'écriture binaire). |
| **Terminal / Canvas Wireframe** | `PaxStation Station Pro • Graveur Silicium APDU IsoDep` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Structure EF créée et capsule découpée en 306 blocs.

> [!TIP]
> **Postconditions Garanties :**
> 78 412 octets gravés avec succès dans l'EEPROM de la JavaCard ACOSJ.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Sélection successive du fichier `EF02` puis `EF03` via `SELECT FILE`.
2. Envoi cadencé des commandes APDU `UPDATE BINARY` (commande `00 D6 P1 P2 Lc [Octets]`).
3. Contrôle systématique du mot de statut `90 00` en réponse à chaque bloc.
4. Gestion des reprises sur incident : si un bloc échoue, rejeu automatique (max 3 tentatives).
5. Mise à jour en temps réel de la barre de progression pour l'opérateur.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `block_count` | **Nombre de Blocs** | `text` | `306 blocs de 255 octets` | Blocs | `306 Blocs` | ⭕ Optionnel |
| `transfer_rate` | **Vitesse de Transfert** | `text` | `14.2 Ko/sec (106 kbps IsoDep)` | Débit | `106k` | ⭕ Optionnel |
| `error_rate` | **Taux d'Erreur APDU** | `text` | `0 erreur (306/306 acquittements 90 00)` | Erreurs | `0 Défaut` | ⭕ Optionnel |
| `elapsed_time` | **Temps Écoulé** | `text` | `05.8 secondes` | Temps | `Chrono` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_start_burning` | **Lancer la Gravure Silicium** | `primary` | `idle` | 🔥 |
| `btn_pause_burning` | **Mettre en Pause** | `secondary` | `idle` | ⏸ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Gravure Silicium Achevée avec Succès
>
> **Badge de Conformité :** `306/306 Blocs Écrits (90 00)`
>
> **Détail Opérationnel :** 78 412 octets injectés dans les partitions EF02 et EF03 sans aucune erreur.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_APDU_WRITE_FAILURE` |
| **Intitulé de l'Incident** | **Échec de Transmission d'un Bloc APDU** |
| **Condition Déclenchante** | Micro-déplacement de la carte sur l'antenne provoquant un code statut `6A 84` ou perte de liaison. |
| **Message d'Erreur UI** | *« Erreur d'écriture : Rupture de liaison RF lors de l'injection du bloc n° 142/306. »* |
| **Action Corrective Requise** | **Laisser la carte immobile au contact de l'antenne et relancer la procédure d'écriture automatique.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Station Pro • Graveur Silicium APDU IsoDep**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Graveur en Attente de Démarrage | *En attente utilisateur* | Les 306 blocs sont prêts. La jauge d'écriture est à 0%. |
| **2** | **Déclenchement ⚡** | Lancement de la Rafale de Commandes APDU | `Clic sur 'Lancer la Gravure Silicium' et sélection du fichier EF02` | Lancement de la boucle cadencée d'envoi des commandes UPDATE BINARY. |
| **3** | **Traitement ⚙️** | Injection en Cours : Bloc 198 / 306 (65%) | `Progression : 65%` | Écriture active dans les cellules EEPROM avec acquittement 90 00 systématique. |
| **4** | **Scellement & Fin ✨** | Gravure Silicium Accomplie à 100% | `Statut : success` | Totalité des 78 412 octets gravés avec intégrité absolue. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-205 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Graveur en Attente de Démarrage
*Les 306 blocs sont prêts. La jauge d'écriture est à 0%.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Graveur Silicium</span>
                        <span class="wf-status-badge wf-badge-neutral">Prêt à Graver (0 / 306 Blocs)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 0%;"></div></div>
                      <div class="wf-device-status-box">
                        <div><strong>78 412 octets prêts à être écrits sur l'ACOSJ 92k</strong></div>
                        <div class="wf-subtext">Durée estimée : ~6 secondes à 106 kbps IsoDep</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔥 Lancer la Gravure Silicium</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Lancement de la Rafale de Commandes APDU
*Lancement de la boucle cadencée d'envoi des commandes UPDATE BINARY.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Injection Silicium</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Écriture en Cours</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">⚡ Envoi des blocs APDU IsoDep T=CL</div>
                        <div class="wf-subtext">Cadence : 52 blocs / seconde avec vérification 90 00</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Écriture physique in-silico...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Injection en Cours : Bloc 198 / 306 (65%)
*Écriture active dans les cellules EEPROM avec acquittement 90 00 systématique.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Moniteur de Flux APDU</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Gravure Actif (65%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 65%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [APDU-TX] 00 D6 00 C6 FF [255 octets profil] -> < 90 00</code><br>
                        <code>> [APDU-TX] 00 D6 01 C5 FF [255 octets WebP]   -> < 90 00</code><br>
                        <code>> [APDU-TX] 00 D6 02 C4 FF [255 octets Opus]   -> < 90 00 (Bloc 198/306)</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Gravure Silicium Accomplie à 100%
*Totalité des 78 412 octets gravés avec intégrité absolue.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Gravure Accomplie</span>
                        <span class="wf-status-badge wf-badge-success">✨ 306/306 Blocs Scellés (100%)</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">💾</span>
                        <div>
                          <strong>Données Mémorielles Gravées in-silico</strong>
                          <p class="wf-subtext">78 412 octets stockés • Prêt pour scellement cryptographique COSE_Sign1</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Scellement COSE_Sign1 →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-206"></a>
## UC-206 : Scellement Cryptographique COSE_Sign1 PaxFunèbre (Secure Element)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-206` |
| **Catégorie Métier** | **Cryptographie & Signature** |
| **Acteur Principal** | Opérateur d'Encodage |
| **Plateformes Cibles** | WebUSB (Chromium Desktop), PC/SC (Desktop Natif) |
| **Tags Clés** | `COSE_Sign1`, `Ed25519`, `ES256`, `SecureElement`, `RFC9052` |
| **Base Légale & Normative** | Spécification technique IETF RFC 9052 (COSE Structures and Process) et RFC 9596 (COSE typ Header). |
| **Terminal / Canvas Wireframe** | `PaxStation Station Pro • Module de Signature Matérielle COSE_Sign1` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Données gravées sur la puce mais non encore signées.

> [!TIP]
> **Postconditions Garanties :**
> Carte physique scellée avec signature COSE_Sign1 officielle infalsifiable.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Appel au module matériel sécurisé (Secure Element / HSM d'agence PaxFunèbre).
2. Construction de la structure canonique `Sig_structure` COSE_Sign1 (Tag 18) selon la RFC 9052 :
3. - Contexte : `"Signature1"`
4. - En-tête protégé : `{1: -8, 16: "application/aeternitrak-profile+cbor"}` (Ed25519) ou `{1: -7}` (ES256)
5. - Données associées externes : `h''` (vide)
6. - Charge utile : le condensat SHA-256 de la capsule
7. Génération de la signature cryptographique par la clé d'autorité officielle.
8. Écriture de l'enveloppe signée COSE_Sign1 dans le fichier dédié `EF.SIGN` de la carte.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `hsm_module` | **Module HSM / Secure Element** | `text` | `PaxFunèbre Hardware Token v2.1` | HSM | `FIPS 140-3` | ⭕ Optionnel |
| `sig_alg` | **Algorithme Utilisé** | `select` | `Ed25519 (EdDSA, alg: -8, RFC 8032)` | Algorithme | `Recommandé` | ✅ Requis |
| `mime_typ` | **Type MIME Protégé (typ)** | `text` | `application/aeternitrak-profile+cbor (RFC 9596)` | Type | `Protégé` | ⭕ Optionnel |
| `key_kid` | **Empreinte Clé Publique (kid)** | `text` | `3c81e592...71aa (16 octets SHA-256)` | kid | `16 Octets` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_sign_cose` | **Générer le Sceau Matériel COSE_Sign1** | `primary` | `idle` | 🔐 |
| `btn_inspect_sig_struct` | **Inspecter Sig_structure** | `secondary` | `idle` | 🔍 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Sceau Cryptographique COSE_Sign1 Apposé
>
> **Badge de Conformité :** `Tag 18 • Ed25519 Certifié`
>
> **Détail Opérationnel :** Enveloppe signée gravée sur EF.SIGN. Intégrité infalsifiable garantie sans contact.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_COSE_EXPIRED_KEY` |
| **Intitulé de l'Incident** | **Clé de Scellement Opérateur Expirée** |
| **Condition Déclenchante** | Tentative de signature avec un token HSM dont le certificat d'autorité est expiré. |
| **Message d'Erreur UI** | *« Erreur de sécurité : La clé matérielle de scellement a dépassé sa date limite de validité. »* |
| **Action Corrective Requise** | **Insérer le token HSM de secours ou procéder au renouvellement de clé auprès de l'autorité centrale AeterniTrak.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Station Pro • Module de Signature Matérielle COSE_Sign1**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Données Gravées Non Signées | *En attente utilisateur* | Puce écrite. La partition EF.SIGN est vide, le sceau officiel n'est pas encore apposé. |
| **2** | **Déclenchement ⚡** | Appel au Secure Element & Construction de la Sig_structure | `Clic sur 'Générer le Sceau Matériel COSE_Sign1'` | Assemblage des en-têtes protégés déterministes et envoi du hash au coprocesseur de signature. |
| **3** | **Traitement ⚙️** | Signature Déterministe RFC 8032 & Injection sur EF.SIGN | `Progression : 92%` | Double hachage SHA-512 sans aléa et écriture de l'enveloppe de 64 octets sur la puce. |
| **4** | **Scellement & Fin ✨** | Sceau COSE_Sign1 Scellé sur le Silicium | `Statut : success` | La carte est cryptographiquement protégée. Toute tentative d'altération sera détectée. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-206 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Données Gravées Non Signées
*Puce écrite. La partition EF.SIGN est vide, le sceau officiel n'est pas encore apposé.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Scellement Cryptographique</span>
                        <span class="wf-status-badge wf-badge-neutral">Puce Non Signée</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-key-icon">🔑</span>
                        <div><strong>Token HSM PaxFunèbre en ligne (Clé d'agence prête)</strong></div>
                        <div class="wf-subtext">Algorithme cible : Ed25519 (alg: -8) • Enveloppe COSE_Sign1 Tag 18</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔐 Générer le Sceau Matériel COSE_Sign1</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Appel au Secure Element & Construction de la Sig_structure
*Assemblage des en-têtes protégés déterministes et envoi du hash au coprocesseur de signature.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Moteur de Signature</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Appel Secure Element</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">⚡ Sig_structure [ "Signature1", protected, external_aad, payload ]</div>
                        <div class="wf-subtext">Signature Ed25519 en cours par la clé privée d'autorité Le Pax Funèbre</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Calcul cryptographique matériel...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Signature Déterministe RFC 8032 & Injection sur EF.SIGN
*Double hachage SHA-512 sans aléa et écriture de l'enveloppe de 64 octets sur la puce.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Scellement Silicium</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Scellement Actif (92%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 92%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [COSE-HDR] En-tête protégé déterministe {1: -8, 16: "application/aeternitrak-profile+cbor"}</code><br>
                        <code>> [ED25519] Signature émise (64 octets fixes R||S) : 5a2c91f0...77b1</code><br>
                        <code>> [APDU-SIGN] Écriture sur EF.SIGN (APDU UPDATE BINARY) : < 90 00</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Sceau COSE_Sign1 Scellé sur le Silicium
*La carte est cryptographiquement protégée. Toute tentative d'altération sera détectée.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Carte Scellée</span>
                        <span class="wf-status-badge wf-badge-success">✨ Sceau COSE_Sign1 Actif</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🏆</span>
                        <div>
                          <strong>Signature Cryptographique PaxFunèbre Apposée</strong>
                          <p class="wf-subtext">Ed25519 • kid: 3c81e592...71aa • Inaltérable sans contact</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Contrôle Anti-Malléabilité →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-207"></a>
## UC-207 : Contrôle Strict Anti-Malléabilité du s Bas (RFC 9052)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-207` |
| **Catégorie Métier** | **Sécurité Mathématique** |
| **Acteur Principal** | Opérateur & Moteur de Sécurité |
| **Plateformes Cibles** | WebUSB (Chromium Desktop), Node.js / Core Engine |
| **Tags Clés** | `Malleabilite`, `s-bas`, `RFC9052`, `BSI-TR03111`, `ES256` |
| **Base Légale & Normative** | Guide BSI TR-03111 (Technical Guideline: Elliptic Curve Cryptography §4.1.3). |
| **Terminal / Canvas Wireframe** | `PaxStation Station Pro • Oracle Anti-Malléabilité Cryptographique` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Signature générée (particulièrement en cas d'utilisation d'ECDSA P-256).

> [!TIP]
> **Postconditions Garanties :**
> Signature mathématiquement canonique avec s bas garanti, conforme aux plus hauts standards.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Extraction des scalaires mathématiques `r` et `s` de la signature de 64 octets.
2. Si algorithme ES256 (P-256) : évaluation de la condition de non-malléabilité du BSI TR-03111 §4.1.3 :
3. - Ordre du sous-groupe $n = \text{0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551}$
4. - Contrôle formel : $s \le \lfloor n/2 \rfloor$.
5. Si $s > \lfloor n/2 \rfloor$, normalisation obligatoire immédiate : $s' = n - s$.
6. Vérification que la signature ne peut faire l'objet d'aucune malléabilité par un tiers.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `sig_r` | **Composante Scalaire r** | `text` | `0x4a18c092...38ab (32 octets)` | Scalaire r | `r ∈ [1, n-1]` | ⭕ Optionnel |
| `sig_s` | **Composante Scalaire s** | `text` | `0x391fe018...91ca (32 octets)` | Scalaire s | `s Bas` | ⭕ Optionnel |
| `half_n` | **Seuil floor(n/2)** | `text` | `0x7fffffff...7e28` | n/2 | `Seuil BSI` | ⭕ Optionnel |
| `malleability_status` | **Statut Anti-Malléabilité** | `text` | `CONFORME (s < floor(n/2) vérifié)` | Statut | `Sécurisé` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_verify_s_low` | **Vérifier la Condition Mathématique s Bas** | `primary` | `idle` | 📐 |
| `btn_simulate_s_high` | **Simuler Rejet s Haut Malléable** | `secondary` | `idle` | 🧪 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Signature Anti-Malléable Conforme
>
> **Badge de Conformité :** `BSI TR-03111 §4.1.3 OK`
>
> **Détail Opérationnel :** s bas garanti (s <= floor(n/2)). Zéro risque de signature alternative malléable.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_COSE_MALLEABLE_S` |
| **Intitulé de l'Incident** | **Signature Malléable Détectée (s Haut)** |
| **Condition Déclenchante** | Génération d'une signature ECDSA P-256 dont la valeur s excède floor(n/2). |
| **Message d'Erreur UI** | *« Rejet cryptographique : Composante s haute détectée. La signature viole la RFC 9052 et le BSI TR-03111. »* |
| **Action Corrective Requise** | **Normaliser impérativement la signature en remplaçant s par (n - s) avant gravure sur le silicium.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Station Pro • Oracle Anti-Malléabilité Cryptographique**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Signature Brute en Attente de Contrôle Scalaire | *En attente utilisateur* | Signature extraite. Le calcul de la position par rapport au pivot n/2 est en attente. |
| **2** | **Déclenchement ⚡** | Clic sur 'Vérifier la Condition Mathématique s Bas' | `Évaluation arithmétique multiprécision de l'inégalité s <= floor(n/2)` | Comparaison grand entier sur les 256 bits du scalaire de la courbe. |
| **3** | **Traitement ⚙️** | Comparaison BigInt & Normalisation In-Silico | `Progression : 96%` | La comparaison arithmétique confirme que le scalaire est dans la moitié basse. |
| **4** | **Scellement & Fin ✨** | Non-Malléabilité Mathématique Démontrée | `Statut : success` | Signature inaltérable et non rejouable validée pour le verrouillage définitif. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-207 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Signature Brute en Attente de Contrôle Scalaire
*Signature extraite. Le calcul de la position par rapport au pivot n/2 est en attente.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Contrôle Scalaire Anti-Malléabilité</span>
                        <span class="wf-status-badge wf-badge-neutral">Scalaires Prêts</span>
                      </div>
                      <div class="wf-device-status-box">
                        <div><strong>Signature brute de 64 octets reçue du coprocesseur</strong></div>
                        <div class="wf-subtext">Contrôle requis : BSI TR-03111 §4.1.3 et FIPS 186-5</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">📐 Vérifier la Condition Mathématique s Bas</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Clic sur 'Vérifier la Condition Mathématique s Bas'
*Comparaison grand entier sur les 256 bits du scalaire de la courbe.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Évaluation BSI</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Comparaison Arithmétique</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">⚡ Calcul : s < floor(n/2) pour la courbe P-256 / Ed25519</div>
                        <div class="wf-subtext">Vérification de l'absence de malléabilité de signature</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Vérification scalaire...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Comparaison BigInt & Normalisation In-Silico
*La comparaison arithmétique confirme que le scalaire est dans la moitié basse.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Moteur Arithmétique ECC</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Contrôle BSI (96%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 96%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [ECC-CHECK] r = 0x4a18...38ab ∈ [1, n-1] : VALIDE</code><br>
                        <code>> [ECC-CHECK] s = 0x391f...91ca < floor(n/2) : S BAS CONFIRMÉ</code><br>
                        <code>> [BSI-TR03111] Condition §4.1.3 satisfaite : Signature strictement non-malléable</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Non-Malléabilité Mathématique Démontrée
*Signature inaltérable et non rejouable validée pour le verrouillage définitif.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Sécurité Prouvée</span>
                        <span class="wf-status-badge wf-badge-success">✨ s Bas Garanti</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🛡️</span>
                        <div>
                          <strong>Signature Non-Malléable Conforme RFC 9052</strong>
                          <p class="wf-subtext">Zéro risque d'attaque par signature malléable • Prêt pour verrouillage in-silico</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Verrouillage Matériel in-silico →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-208"></a>
## UC-208 : Verrouillage Matériel Irréversible in-silico (Anti-Tamper)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-208` |
| **Catégorie Métier** | **Sécurité Silicium** |
| **Acteur Principal** | Opérateur d'Encodage |
| **Plateformes Cibles** | WebUSB (Chromium Desktop), PC/SC (Desktop Natif) |
| **Tags Clés** | `Lock`, `Fusible`, `ReadOnly`, `AntiTamper`, `Securite` |
| **Base Légale & Normative** | Spécification JavaCard 3.0 Classic (Security and Applet Lifecycle Management). |
| **Terminal / Canvas Wireframe** | `PaxStation Station Pro • Console de Verrouillage Matériel in-silico` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Données gravées, enveloppe COSE_Sign1 scellée et validée.

> [!TIP]
> **Postconditions Garanties :**
> Carte physique verrouillée définitivement en lecture seule, protégée contre toute altération matérielle.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Affichage d'un avertissement solennel : l'opération est irréversible et passera la puce en lecture seule définitive.
2. Saisie du code de confirmation sécurisé de l'opérateur habilité.
3. Envoi de la commande APDU propriétaire `LOCK APPLICATION` (fusible logiciel et matériel).
4. Destruction des clés d'administration EEPROM dans la puce ACOSJ et claquage du bit fusible in-silico.
5. Tentative de réécriture de test : la puce doit impérativement retourner le code d'erreur `69 82` (Security status not satisfied).

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `fuse_state` | **État du Fusible Silicium** | `text` | `Mode R/W Déverrouillé (Opérateur)` | Fusible | `Ouvert` | ⭕ Optionnel |
| `confirm_lock_code` | **Code de Confirmation** | `text` | `LOCK-PERMANENT-ACOSJ` | Saisir code | `IRRÉVERSIBLE` | ✅ Requis |
| `target_mode` | **Mode Cible Puce** | `text` | `Lecture Seule Définitive (Read-Only RO)` | Cible | `RO Scellé` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_lock_fuse` | **Verrouiller Définitivement la Carte (Fusible in-silico)** | `danger` | `idle` | 🔒 |
| `btn_cancel_lock` | **Annuler l'Opération** | `secondary` | `idle` | ✕ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Carte Verrouillée Définitivement in-silico
>
> **Badge de Conformité :** `Fusible Claqué • Mode Read-Only`
>
> **Détail Opérationnel :** Clés d'écriture détruites. Toute tentative de réécriture rejetée (code 69 82).

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_SILICON_FUSE_BLOWN` |
| **Intitulé de l'Incident** | **Carte Déjà Verrouillée Matériellement** |
| **Condition Déclenchante** | Tentative de verrouillage d'une puce dont le fusible est déjà claqué ou commande avortée. |
| **Message d'Erreur UI** | *« Erreur silicium : La carte est déjà scellée en lecture seule ou le verrou matériel a échoué. »* |
| **Action Corrective Requise** | **Contrôler le statut de lecture de la carte ; si elle est déjà verrouillée, aucune action requise.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Station Pro • Console de Verrouillage Matériel in-silico**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Avertissement Solennel d'Irréversibilité | *En attente utilisateur* | Fusible encore ouvert. L'opérateur doit saisir le code de verrouillage permanent. |
| **2** | **Déclenchement ⚡** | Saisie du Code & Clic sur 'Verrouiller Définitivement' | `Validation de la commande irréversible de claquage de fusible in-silico` | Confirmation opérateur et injection de la commande APDU propriétaire `LOCK APPLICATION`. |
| **3** | **Traitement ⚙️** | Claquage Matériel & Test d'Inviolabilité Réflexe | `Progression : 98%` | Test immédiat d'écriture pirate pour confirmer le rejet avec code d'erreur `69 82`. |
| **4** | **Scellement & Fin ✨** | Carte Scellée à Perpétuité in-silico | `Statut : success` | La puce est désormais infalsifiable et prête pour l'impression physique thermique. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-208 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Avertissement Solennel d'Irréversibilité
*Fusible encore ouvert. L'opérateur doit saisir le code de verrouillage permanent.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Verrouillage Matériel in-silico</span>
                        <span class="wf-status-badge wf-badge-alert">⚠️ Action Irréversible</span>
                      </div>
                      <div class="wf-alert-card wf-alert-amber">
                        <strong>AVERTISSEMENT : Verrouillage Définitif en Lecture Seule</strong>
                        <p class="wf-subtext">Cette opération détruira les clés d'écriture EEPROM. La carte ne pourra plus JAMAIS être modifiée.</p>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-danger">🔒 Verrouiller Définitivement la Carte</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Saisie du Code & Clic sur 'Verrouiller Définitivement'
*Confirmation opérateur et injection de la commande APDU propriétaire `LOCK APPLICATION`.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Destruction des Clés d'Écriture</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Claquage Fusible</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">⚡ Commande APDU : LOCK APPLICATION ACOSJ</div>
                        <div class="wf-subtext">Écrasement irréversible du bit fusible EEPROM in-silico</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-danger wf-pulse-btn">Claquage matériel en cours...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Claquage Matériel & Test d'Inviolabilité Réflexe
*Test immédiat d'écriture pirate pour confirmer le rejet avec code d'erreur `69 82`.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Test d'Inviolabilité Matérielle</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Test d'Écriture Rejeté (98%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 98%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [APDU-TX] 80 0E 00 00 (LOCK APPLICATION) -> < 90 00 (Fusible claqué)</code><br>
                        <code>> [TEST-PIRATE] Tentative UPDATE BINARY d'écrasement -> < 69 82 (Security error)</code><br>
                        <code>> [CONFIRM] Verrouillage matériel validé : Carte devenue physiquement Read-Only</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Carte Scellée à Perpétuité in-silico
*La puce est désormais infalsifiable et prête pour l'impression physique thermique.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Silicium Inviolable</span>
                        <span class="wf-status-badge wf-badge-success">✨ Verrou RO Actif</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🔒</span>
                        <div>
                          <strong>Carte JavaCard ACOSJ Verrouillée à Perpétuité</strong>
                          <p class="wf-subtext">Lecture sans contact autorisée • Écriture physiquement impossible (Code 69 82)</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Impression Thermique & Laser →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-209"></a>
## UC-209 : Impression Thermique & Laser Haute Précision Recto/Verso

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-209` |
| **Catégorie Métier** | **Impression Physique** |
| **Acteur Principal** | Opérateur d'Encodage |
| **Plateformes Cibles** | PC/SC (Desktop Natif), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `Impression`, `Thermique`, `Fargo`, `Laser`, `Hologramme` |
| **Base Légale & Normative** | Norme ISO/IEC 7810 ID-1 (durabilité physique et résistance aux torsions des cartes d'identité). |
| **Terminal / Canvas Wireframe** | `PaxStation Station Pro • Contrôleur d'Impression Thermique 600 DPI` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Silicium gravé et scellé, imprimante Fargo HDP5000 en ligne.

> [!TIP]
> **Postconditions Garanties :**
> Carte physique terminée, surface résistante aux rayures et aux intempéries (norme ISO 7810).

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Centrage optique haute précision de la carte dans le chargeur de l'imprimante thermique par sublimation Fargo HDP5000.
2. Impression haute définition 600 DPI du recto (portrait mémoriel et dorures à chaud en résine or).
3. Retournement automatique de la carte par le module flipper interne de l'imprimante.
4. Impression du verso (épitaphe funéraire, micro-caractères de sécurité et repère optique de la puce).
5. Application du vernis de protection anti-UV et de la couche holographique inviolable.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `printer_model` | **Imprimante Professionnelle** | `select` | `Fargo HDP5000 Haute Définition (600 DPI)` | Imprimante | `Prête` | ✅ Requis |
| `ribbon_type` | **Ruban de Sécurité** | `select` | `Quadrichromie YMCK + Ruban Dorure Or & Hologramme` | Ruban | `Or 24k` | ✅ Requis |
| `lamination` | **Vernis de Protection** | `text` | `Overlay Polycarbonate Anti-UV 1.0 mil` | Vernis | `Anti-UV` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_start_print` | **Lancer l'Impression Thermique Recto/Verso** | `primary` | `idle` | 🖨️ |
| `btn_calibrate_head` | **Calibrer Centrage Micrométrique** | `secondary` | `idle` | 🎯 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Impression Physique 600 DPI Terminée
>
> **Badge de Conformité :** `Conforme ISO/IEC 7810`
>
> **Détail Opérationnel :** Dorure à chaud et vernis anti-UV appliqués. Éjection bac de sortie sans défaut.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_THERMAL_HEAD_OVERHEAT` |
| **Intitulé de l'Incident** | **Surchauffe de la Tête Thermique** |
| **Condition Déclenchante** | Température de la tête de sublimation dépassant le seuil de 85°C lors des séries d'encodage. |
| **Message d'Erreur UI** | *« Erreur d'impression : Surchauffe thermique détectée sur la tête d'impression Fargo. »* |
| **Action Corrective Requise** | **Mettre l'imprimante en pause de refroidissement 90 secondes avant de reprendre le cycle de pelliculage.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Station Pro • Contrôleur d'Impression Thermique 600 DPI**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Imprimante Fargo HDP5000 Prête dans le Bac d'Alimentation | *En attente utilisateur* | Carte positionnée dans le chargeur optique. Prête pour l'impression thermique. |
| **2** | **Déclenchement ⚡** | Prise en Charge de la Carte & Chauffage Tête Thermique | `Clic sur 'Lancer l'Impression Thermique Recto/Verso'` | Centrage micrométrique optique et montée en température de la tête thermique. |
| **3** | **Traitement ⚙️** | Impression Sublimation 600 DPI & Pelliculage Anti-UV | `Progression : 75%` | Dépôt des pigments couleur, application de la dorure à chaud et retournement flipper. |
| **4** | **Scellement & Fin ✨** | Carte Physique Éjectée & Vernis Séché | `Statut : success` | La carte imprimée repose dans le bac de sortie. Rendu or et mat conforme à l'épreuve. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-209 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Imprimante Fargo HDP5000 Prête dans le Bac d'Alimentation
*Carte positionnée dans le chargeur optique. Prête pour l'impression thermique.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Contrôle Imprimante</span>
                        <span class="wf-status-badge wf-badge-neutral">Fargo HDP5000 En Ligne</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-printer-icon">🖨️</span>
                        <div><strong>Bac d'entrée : Carte ACOSJ prête pour l'impression</strong></div>
                        <div class="wf-subtext">Ruban quadrichromie + film holographique or opérationnels</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🖨️ Lancer l'Impression Thermique Recto/Verso</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Prise en Charge de la Carte & Chauffage Tête Thermique
*Centrage micrométrique optique et montée en température de la tête thermique.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Démarrage Impression</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Cycle Thermique Démarré</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Aspiration de la carte et centrage optique de la puce</div>
                        <div class="wf-subtext">Transfert thermique réversible HDP à 175°C sur film transparent</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Impression du Recto en cours...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Impression Sublimation 600 DPI & Pelliculage Anti-UV
*Dépôt des pigments couleur, application de la dorure à chaud et retournement flipper.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Cycle Impression en Cours</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Impression Recto/Verso (75%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 75%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [PRINT-HDP] Impression Recto 600 DPI (Portrait Henri Dubois) : OK</code><br>
                        <code>> [PRINT-FLIP] Actionnement module de retournement 180° : OK</code><br>
                        <code>> [PRINT-VERSO] Impression Verso et laminage overlay polycarbonate 1 mil</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Carte Physique Éjectée & Vernis Séché
*La carte imprimée repose dans le bac de sortie. Rendu or et mat conforme à l'épreuve.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Carte Imprimée</span>
                        <span class="wf-status-badge wf-badge-success">✨ Éjectée Bac de Sortie</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🎴</span>
                        <div>
                          <strong>Carte Physique Haute Définition Achevée</strong>
                          <p class="wf-subtext">Dorures 24k en relief • Vernis anti-UV durci • Prête pour le contrôle de recette</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Contrôle de Recette & PV →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-210"></a>
## UC-210 : Contrôle de Recette Post-Gravure & PV de Remise Officiel

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-210` |
| **Catégorie Métier** | **Assurance Qualité & Conformité** |
| **Acteur Principal** | Opérateur d'Encodage & Conseiller |
| **Plateformes Cibles** | PC/SC (Desktop Natif), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `QA`, `Recette`, `PVRemise`, `Conformite`, `Coffret` |
| **Base Légale & Normative** | Code de droit économique belge (garantie de conformité des biens et services funéraires). |
| **Terminal / Canvas Wireframe** | `PaxStation Station Pro • Banc de Recette Qualité & Édition PV` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Carte physique imprimée et gravée reposée sur le lecteur de contrôle.

> [!TIP]
> **Postconditions Garanties :**
> PV de remise officiel édité et signé, coffret scellé prêt pour la remise solennelle à la famille.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Relecture intégrale sans fil des 78 412 octets gravés via l'antenne NFC de recette.
2. Vérification mathématique indépendante de la signature COSE_Sign1 par la clé publique officielle.
3. Confrontation de l'empreinte de relecture avec l'empreinte d'origine du Bon à Tirer (zéro différence admise).
4. Génération du Procès-Verbal (PV) de Remise Officiel infalsifiable avec QR code de contrôle.
5. Insertion solennelle des deux cartes dans leur coffret mémoriel doublé de velours Le Pax Funèbre.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `recheck_bytes` | **Relecture Silicium Intégrale** | `text` | `78 412 octets relus à 106 kbps (0 divergence)` | Relecture | `100% Intègre` | ⭕ Optionnel |
| `recheck_sig` | **Signature COSE_Sign1** | `text` | `VALIDE (Clé publique Ed25519 officielle vérifiée)` | Signature | `Authentique` | ⭕ Optionnel |
| `lot_serial` | **Numéro de Série Lot** | `text` | `AET-2026-LOT-NAM-0491` | Numéro | `Traçable` | ⭕ Optionnel |
| `recipient_family` | **Destinataire Officiel** | `text` | `Claire Dubois (Mandat n° 8841)` | Famille | `Mandataire` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_run_qa` | **Lancer le Contrôle de Recette Automatisé** | `primary` | `idle` | 🔬 |
| `btn_print_pv` | **Éditer le PV de Remise Officiel (PDF Chiffré)** | `secondary` | `idle` | 📄 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Contrôle de Recette Qualité 100% Conforme
>
> **Badge de Conformité :** `PV Officiel Validé`
>
> **Détail Opérationnel :** Zéro anomalie détectée. Coffret mémoriel scellé prêt pour remise solennelle à la famille.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_QA_HASH_MISMATCH` |
| **Intitulé de l'Incident** | **Non-Concordance d'Empreinte de Recette** |
| **Condition Déclenchante** | Altération d'un octet lors de la relecture ou divergence avec le BAT d'origine. |
| **Message d'Erreur UI** | *« REJET QUALITÉ CRITIQUE : L'empreinte SHA-256 relue sur la puce ne correspond pas au Bon à Tirer signé. »* |
| **Action Corrective Requise** | **Mettre la carte immédiatement au rebut, procéder à l'analyse de défaillance matérielle et réencoder une nouvelle carte.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Station Pro • Banc de Recette Qualité & Édition PV**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Carte Terminée Déposée sur le Banc de Recette | *En attente utilisateur* | Carte posée sur le lecteur de contrôle qualité. L'audit automatisé est en attente. |
| **2** | **Déclenchement ⚡** | Lancement de l'Audit Qualité Automatisé | `Clic sur 'Lancer le Contrôle de Recette Automatisé'` | Relecture complète des blocs APDU et vérification cryptographique hors-ligne. |
| **3** | **Traitement ⚙️** | Vérification Mathématique COSE_Sign1 & Hachage JCS | `Progression : 95%` | Confirmation de la validité de la signature Ed25519 et de la fidélité au BAT. |
| **4** | **Scellement & Fin ✨** | PV de Remise Officiel Émis & Coffret Scellé | `Statut : success` | Processus d'encodage terminé avec succès. Les 2 cartes sont prêtes pour la famille. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-210 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Carte Terminée Déposée sur le Banc de Recette
*Carte posée sur le lecteur de contrôle qualité. L'audit automatisé est en attente.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Banc de Recette Qualité</span>
                        <span class="wf-status-badge wf-badge-neutral">En Attente d'Audit</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-qa-icon">🔬</span>
                        <div><strong>Carte n° AET-2026-NAM-0491 en position de contrôle</strong></div>
                        <div class="wf-subtext">Audit automatique : Relecture mémoire + Vérification signature + Concordance BAT</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔬 Lancer le Contrôle de Recette Automatisé</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Lancement de l'Audit Qualité Automatisé
*Relecture complète des blocs APDU et vérification cryptographique hors-ligne.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Relecture Qualité</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Audit 100% Automatisé</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Relecture NFC des 78 412 octets en cours</div>
                        <div class="wf-subtext">Confrontation binaire bit-à-bit avec la capsule source</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Audit de conformité en cours...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Vérification Mathématique COSE_Sign1 & Hachage JCS
*Confirmation de la validité de la signature Ed25519 et de la fidélité au BAT.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Moteur de Recette Qualité</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Contrôle Final (95%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 95%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [QA-READ] 78 412 octets relus : 0 divergence binaire (100% intègre)</code><br>
                        <code>> [QA-COSE] Vérification signature Ed25519 par clé publique PaxFunèbre : VALIDE</code><br>
                        <code>> [QA-BAT] Concordance SHA-256 avec BAT signé : PARFAITE</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : PV de Remise Officiel Émis & Coffret Scellé
*Processus d'encodage terminé avec succès. Les 2 cartes sont prêtes pour la famille.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Commande Terminée</span>
                        <span class="wf-status-badge wf-badge-success">✨ 100% Conforme & Remis</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🏆</span>
                        <div>
                          <strong>Procès-Verbal de Remise Officiel n° PV-2026-0491 Validé</strong>
                          <p class="wf-subtext">Carte 1 Sanctuaire & Carte 2 Directives prêtes pour remise solennelle</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Bascule vers App 3 : Sanctuaire Mémoriel Mobile →</button>
                      </div>
                    </div>
```

</details>

---
