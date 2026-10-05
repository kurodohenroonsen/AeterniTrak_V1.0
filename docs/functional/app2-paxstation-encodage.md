# Application 2 — PaxStation Encodage Silicium (UC-201 à UC-225)

**Station Technique Professionnelle de Gravure Matérielle & Scellement Cryptographique**

> [!NOTE]
> **Périmètre Applicatif :**
> L'application **PaxStation Encodage Silicium** est l'outil technique réservé aux professionnels habilités du réseau *Le Pax Funèbre*. Connectée au lecteur de bureau **ACR1552U via WebUSB ou PC/SC CCID**, elle assure le dialogue APDU IsoDep de bas niveau avec la puce **JavaCard ACOSJ 92 Ko EEPROM**, l'initialisation du système de fichiers sécurisé, le scellement cryptographique déterministe **COSE_Sign1 (Ed25519 / ES256 avec s normalisé bas)**, l'activation du fusible matériel in-silico (protection anti-tamper en lecture seule) et le pilotage de l'impression thermique haute définition 600 DPI.

## 📌 Sommaire des Micro Use-Cases Spécifiés

| ID | Titre du Cas d'Usage | Catégorie Métier | Acteur | Plateformes | Référence Normative |
| :---: | :--- | :--- | :--- | :--- | :--- |
| [`UC-201`](#uc-201) | [Connexion Station de Bureau ACR1552U WebUSB & Session Opérateur Funéraire](#uc-201) | **Matériel & Poste Pro** | Opérateur d'Encodage & Conseiller Funéraire | WebUSB (Chromium Desktop), PC/SC (Desktop Natif) | Spécification USB CCID (Integrated Circuit(s) Cards Interface Device, USB-IF, classe 0x0B), architecture nominale PC/SC locale (contournement UsbBlocklist Chromium) et politique de sécurité opérationnelle PaxFunèbre (décision souveraine DEC-AET-10). |
| [`UC-202`](#uc-202) | [Insertion JavaCard ACOSJ 92 Ko & Vérification ATS APDU](#uc-202) | **Silicium & Détection** | Opérateur d'Encodage | WebUSB (Chromium Desktop), PC/SC (Desktop Natif) | Norme ISO/IEC 7816-4 (organisation, sécurité et commandes pour les échanges d'informations). |
| [`UC-203`](#uc-203) | [Formatage EEPROM & Initialisation EF Silicium (STORAGE-001)](#uc-203) | **Système de Fichiers Puce** | Opérateur d'Encodage | WebUSB (Chromium Desktop), PC/SC (Desktop Natif) | Spécification technique AeterniTrak STORAGE-001 (allocation EEPROM JavaCard). |
| [`UC-204`](#uc-204) | [Ingestion de la Capsule & Canonisation CBOR RFC 8949](#uc-204) | **Compilation & Core** | Opérateur d'Encodage | WebUSB (Chromium Desktop), Node.js / Core Engine | Spécification technique IETF RFC 8949 (CBOR Deterministic Encoding Rules §4.2.1). |
| [`UC-205`](#uc-205) | [Injection par Blocs APDU Sécurisés sur la Puce](#uc-205) | **Gravure Silicium** | Opérateur d'Encodage | WebUSB (Chromium Desktop), PC/SC (Desktop Natif) | Spécification technique ISO/IEC 7816-4 §7.2 (commandes d'écriture binaire). |
| [`UC-206`](#uc-206) | [Scellement Cryptographique COSE_Sign1 PaxFunèbre (Enclave Station DEC-AET-10)](#uc-206) | **Cryptographie & Signature** | Opérateur d'Encodage | WebUSB (Chromium Desktop), PC/SC (Desktop Natif) | Spécification technique IETF RFC 9052 (COSE Structures and Process) et RFC 9596 (COSE typ Header). |
| [`UC-207`](#uc-207) | [Contrôle Strict Anti-Malléabilité du s Bas (RFC 9052)](#uc-207) | **Sécurité Mathématique** | Opérateur & Moteur de Sécurité | WebUSB (Chromium Desktop), Node.js / Core Engine | Guide BSI TR-03111 (Technical Guideline: Elliptic Curve Cryptography §4.1.3). |
| [`UC-208`](#uc-208) | [Verrouillage Matériel Irréversible in-silico (Anti-Tamper)](#uc-208) | **Sécurité Silicium** | Opérateur d'Encodage | WebUSB (Chromium Desktop), PC/SC (Desktop Natif) | Spécification JavaCard 3.0 Classic (Security and Applet Lifecycle Management). |
| [`UC-209`](#uc-209) | [Impression Thermique & Laser Haute Précision Recto/Verso](#uc-209) | **Impression Physique** | Opérateur d'Encodage | PC/SC (Desktop Natif), Web Standard (PWA Hors-Ligne) | Norme ISO/IEC 7810 ID-1 (durabilité physique et résistance aux torsions des cartes d'identité). |
| [`UC-210`](#uc-210) | [Diagnostic Silicium, Relecture des 6 EF & PV de Gravure Officiel](#uc-210) | **Assurance Qualité & Conformité** | Opérateur d'Encodage & Conseiller Funéraire | PC/SC (Desktop Natif), Web Standard (PWA Hors-Ligne) | Code de droit économique belge (garantie de conformité des biens et services funéraires — référence à confirmer par un juriste). |
| [`UC-211`](#uc-211) | [Déconnexion Brutale & Perte de Champ RF pendant l'Écriture (Anti-Tearing & Tag 0x07 COMMIT_FLAG)](#uc-211) | **Résilience Matérielle & Silicium** | Opérateur d'Atelier Funéraire | Poste Pro Dédié (macOS, Windows, Linux) | Spécification technique AET-SPEC-STORAGE-001 §2.1 (Gestion transactionnelle TLV Tag 0x07) & Norme ISO/IEC 14443-4. |
| [`UC-212`](#uc-212) | [Tentative de Réécriture sur Puce Déjà Verrouillée / Fusible Grillé (Tag 0x06 LOCK_FUSE = 0x01, SW 0x6985)](#uc-212) | **Sécurité Silicium & Anti-Tamper** | Opérateur d'Atelier Funéraire | Poste Pro Dédié (macOS, Windows, Linux) | Spécification technique AET-SPEC-STORAGE-001 §2.1 (Tag 0x06 FUSE_STATUS) & Décision Kudoro DEC-AET-01. |
| [`UC-213`](#uc-213) | [Révocation de Clé Privée d'Enclave ou Certificat d'Opérateur Expiré](#uc-213) | **Cryptographie & Contrôle d'Accès** | Administrateur Système & Opérateur Funéraire | Poste Pro Dédié (macOS, Windows, Linux) | Norme IETF RFC 9052 §3 (gestion des identifiants kid et clés COSE) & Décision Kudoro DEC-AET-10. |
| [`UC-214`](#uc-214) | [Échec d'Impression Thermique/Laser & Procédure de Rebut Silicium (SCRAPPED)](#uc-214) | **Production Physique & Assurance Qualité** | Opérateur d'Atelier & Contrôleur Qualité | Poste Pro Dédié (macOS, Windows, Linux) | Norme ISO/IEC 7810 (critères d'aspect et d'intégrité des cartes d'identification) & Protocole Qualité PaxFunèbre QA-PRO-04. |
| [`UC-215`](#uc-215) | [Polling Détection Lecteur USB CCID & Événements PnP Carte Présente](#uc-215) | **Silicium & Détection** | Opérateur d'Atelier | Poste Pro Dédié (macOS, Windows, Linux) | Spécification USB CCID (Integrated Circuit Card Interface Devices) & Spécifications PC/SC Workgroup Part 2 & 3. |
| [`UC-216`](#uc-216) | [Analyse Trame Réponse ATR / ATS & Identification ISO 14443-4 Type A](#uc-216) | **Silicium & Détection** | Opérateur d'Atelier & Système Automatisé | Poste Pro Dédié (macOS, Windows, Linux) | Norme internationale ISO/IEC 14443-4 (Cartes d'identification sans contact - Protocole de transmission T=CL). |
| [`UC-217`](#uc-217) | [Sélection de l'Applet par Commande APDU SELECT AID & Validation SW 0x9000](#uc-217) | **Système de Fichiers Puce** | Système Automatisé PaxStation | Poste Pro Dédié (macOS, Windows, Linux) | Norme ISO/IEC 7816-4 (Organisation, sécurité et commandes pour les échanges) & Spécifications Java Card 3.0.5. |
| [`UC-218`](#uc-218) | [Lecture En-tête EF-0 Silicium & Inspection des Compteurs Monotones](#uc-218) | **Système de Fichiers Puce** | Système Automatisé & Opérateur d'Atelier | Poste Pro Dédié (macOS, Windows, Linux) | Spécification technique AeterniTrak EF-0 (Conteneur racine d'amorçage) & ISO/IEC 7816-4. |
| [`UC-219`](#uc-219) | [Diagnostic d'Usure EEPROM & Cartographie des Blocs d'Écriture](#uc-219) | **Résilience Matérielle & Silicium** | Contrôleur Qualité Silicium | Poste Pro Dédié (macOS, Windows, Linux) | Norme JEDEC JESD22-A117 (Endurance et rétention de données pour mémoires non volatiles EEPROM). |
| [`UC-220`](#uc-220) | [Négociation de Vitesse PPS (Baudrate 106 ➔ 212 ➔ 424 ➔ 848 kbps)](#uc-220) | **Silicium & Détection** | Système Automatisé PaxStation | Poste Pro Dédié (macOS, Windows, Linux) | Norme internationale ISO/IEC 14443-4 Section 5.3 (Procédure de sélection de protocole et paramètres PPS). |
| [`UC-221`](#uc-221) | [Authentification Forte Opérateur par Clé FIDO2 / YubiKey & Enrôlement](#uc-221) | **Sécurité Silicium & Anti-Tamper** | Opérateur d'Atelier Habilité | Poste Pro Dédié (macOS, Windows, Linux) | Standard FIDO Alliance CTAP2.1 & Recommandation W3C Web Authentication (WebAuthn Level 2). |
| [`UC-222`](#uc-222) | [Découpage APDU Extended Length (Trames 255 octets vs Extended APDU 64 Ko)](#uc-222) | **Gravure Silicium** | Système Automatisé PaxStation | Poste Pro Dédié (macOS, Windows, Linux) | Norme ISO/IEC 7816-4 Section 5.1 (Structure des commandes APDU et mécanismes Extended Length). |
| [`UC-223`](#uc-223) | [Test à Blanc du Verrouillage Matériel (Simulation Fusible Virtuel in-silico)](#uc-223) | **Sécurité Silicium & Anti-Tamper** | Opérateur d'Atelier & Contrôleur Qualité | Poste Pro Dédié (macOS, Windows, Linux) | Politique de sécurité AeterniTrak Iron Gate & Recommandations Common Criteria EAL5+. |
| [`UC-224`](#uc-224) | [Relecture Intégrale de Contrôle & Concordance d'Empreinte SHA-256 post-gravure](#uc-224) | **Assurance Qualité & Conformité** | Contrôleur Qualité & Système Automatisé | Poste Pro Dédié (macOS, Windows, Linux) | Norme FIPS PUB 180-4 (Secure Hash Standard - SHA-256) & Procédure Qualité Funéraire QA-PRO-02. |
| [`UC-225`](#uc-225) | [Calibrage Alignement Imprimante Sublimation Thermique & Jauge Ruban](#uc-225) | **Production Physique & Assurance Qualité** | Opérateur d'Atelier & Technicien Maintenance | Poste Pro Dédié (macOS, Windows, Linux) | Spécifications industrielles HID Global Fargo HDP & Norme ISO/IEC 7810 ID-1 relative à la résistance mécanique des cartes. |

---

<a id="uc-201"></a>
## UC-201 : Connexion Station de Bureau ACR1552U WebUSB & Session Opérateur Funéraire

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-201` |
| **Catégorie Métier** | **Matériel & Poste Pro** |
| **Acteur Principal** | Opérateur d'Encodage & Conseiller Funéraire |
| **Plateformes Cibles** | WebUSB (Chromium Desktop), PC/SC (Desktop Natif) |
| **Tags Clés** | `ACR1552U`, `WebUSB`, `PCSC`, `SessionOperateur`, `StrongBox`, `DEC-AET-10`, `ACOSJ92k` |
| **Base Légale & Normative** | Spécification USB CCID (Integrated Circuit(s) Cards Interface Device, USB-IF, classe 0x0B), architecture nominale PC/SC locale (contournement UsbBlocklist Chromium) et politique de sécurité opérationnelle PaxFunèbre (décision souveraine DEC-AET-10). |
| **Terminal / Canvas Wireframe** | `PaxStation Station Pro • Session Opérateur & Console ACR1552U (DEC-AET-10)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Poste de travail d'agence avec lecteur ACR1552U branché sur port USB 3.0 et enclave cryptographique active de la station (DEC-AET-10).

> [!TIP]
> **Postconditions Garanties :**
> Session opérateur funéraire ouverte, enclave ES256 prête (DEC-AET-10), lot ACOSJ 92 Ko assigné et canal USB CCID 12 Mbps opérationnel.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Ouverture de PaxStation Encodage sur Chromium Desktop avec détection CCID universelle du lecteur ACS ACR1552U 1S CL Reader (VID 0x072F / classe USB 0x0B) via passerelle PC/SC locale nominale.
2. Saisie et contrôle du formulaire d'ouverture de session : ID Conseiller/Opérateur et présentation du Badge Agence PaxFunèbre.
3. Authentification et initialisation de l'Enclave Cryptographique active de la station (StrongBox / Secure Enclave ES256 DEC-AET-10).
4. Sélection et allocation du lot de puces JavaCard ACOSJ 92 Ko homologuées pour la série d'encodage.
5. Passage du voyant LED du lecteur au vert fixe (état prêt) et ouverture du canal sans contact 106 kbps ISO/IEC 14443-4.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `operator_id` | **ID Conseiller / Opérateur** | `text` | `OP-NAM-8842 (Marc Lambert)` | Identifiant opérateur | `Authentifié` | ✅ Requis |
| `agency_badge` | **Badge Agence PaxFunèbre** | `text` | `PaxFunèbre Namur Centre #AG-04 (Habilitation H3)` | Badge agence | `Habilité H3` | ✅ Requis |
| `crypto_enclave` | **Enclave Cryptographique Station** | `select` | `Station Secure Enclave / StrongBox (ES256 DEC-AET-10)` | Enclave matérielle | `DEC-AET-10` | ✅ Requis |
| `card_lot` | **Sélection du Lot de Cartes ACOSJ 92 Ko** | `select` | `Lot ACOSJ-92K-2026-N1 (JavaCard 92 160 octets)` | Lot silicium | `92 Ko EEPROM` | ✅ Requis |
| `usb_driver` | **Pilote & Matériel Détecté** | `text` | `ACS ACR1552U 1S CL Reader (VID:072F / Classe 0x0B CCID - 12 Mbps)` | Pilote | `PC/SC Nominal` | ⭕ Optionnel |
| `rf_link` | **Liaison RF & Baudrate** | `text` | `13.56 MHz • 106 kbps ISO/IEC 14443 Type A` | Baudrate RF | `106 kbps` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_open_session` | **Authentifier l'Opérateur & Ouvrir Session** | `primary` | `idle` | 🔐 |
| `btn_test_enclave` | **Tester Enclave ES256 & Bip Sonore** | `secondary` | `idle` | 🛡️ |
| `btn_connect_acr` | **Connecter Lecteur ACR1552U (PC/SC / USB)** | `secondary` | `idle` | 🔌 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Session Opérateur Funéraire Ouverte & Station Prête
>
> **Badge de Conformité :** `Enclave ES256 Active (DEC-AET-10)`
>
> **Détail Opérationnel :** Opérateur OP-NAM-8842 identifié. Enclave matérielle de station armée. Lot ACOSJ 92 Ko verrouillé. Lecteur ACR1552U en veille RF 106 kbps.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_OPERATOR_AUTH_OR_ENCLAVE_FAILED` |
| **Intitulé de l'Incident** | **Échec d'Authentification Opérateur ou Enclave Indisponible** |
| **Condition Déclenchante** | Badge opérateur non reconnu, identifiant conseiller invalide ou échec de poignée de main avec l'enclave sécurisée de la station. |
| **Message d'Erreur UI** | *« Accès refusé : La station d'encodage ne peut s'authentifier auprès de l'enclave cryptographique (DEC-AET-10) ou le badge opérateur est invalide. »* |
| **Action Corrective Requise** | **Vérifier le badge d'agence PaxFunèbre, s'assurer que le module StrongBox / Secure Enclave est disponible et relancer l'identification.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Station Pro • Session Opérateur & Console ACR1552U (DEC-AET-10)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Formulaire d'Ouverture de Session & Authentification Station | *En attente utilisateur* | Formulaire opérateur en attente. ID Conseiller, badge agence et sélection du lot ACOSJ 92 Ko prêts à être validés. |
| **2** | **Déclenchement ⚡** | Validation des Accréditations Opérateur & Déverrouillage Enclave | `Tap du badge agence et clic sur 'Authentifier l'Opérateur & Ouvrir Session'` | Validation biométrique/badge opérateur et appel sécurisé du module Enclave Cryptographique (DEC-AET-10). |
| **3** | **Traitement ⚙️** | Initialisation de l'Enclave Matérielle & Armement RF 13.56 MHz | `Progression : 85%` | Armement de l'enclave station pour signatures ES256 (DEC-AET-10) et mise en veille active du lecteur. |
| **4** | **Scellement & Fin ✨** | Session Opérateur Ouverte & Station Prête pour Gravure | `Statut : success` | Station authentifiée et prête. L'opérateur peut déposer la première JavaCard ACOSJ 92 Ko. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-201 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Formulaire d'Ouverture de Session & Authentification Station
*Formulaire opérateur en attente. ID Conseiller, badge agence et sélection du lot ACOSJ 92 Ko prêts à être validés.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Ouverture de Session & Authentification Station</span>
                        <span class="wf-status-badge wf-badge-neutral">Session Fermée</span>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-field-group">
                          <label class="wf-label">ID Conseiller / Opérateur <span class="wf-req">*</span></label>
                          <div class="wf-select-placeholder">OP-NAM-8842 (Marc Lambert)</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Badge Agence PaxFunèbre <span class="wf-req">*</span></label>
                          <div class="wf-select-placeholder">Badge Agence Namur Centre #AG-04 [H3]</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Enclave Cryptographique Station <span class="wf-req">*</span></label>
                          <div class="wf-select-placeholder">Station Secure Enclave / StrongBox (ES256 DEC-AET-10)</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Sélection du Lot de Cartes ACOSJ 92 Ko <span class="wf-req">*</span></label>
                          <div class="wf-select-placeholder">Lot ACOSJ-92K-2026-N1 (92 160 octets)</div>
                        </div>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-usb-icon">🔌</span>
                        <div><strong>Lecteur ACS ACR1552U 1S CL Reader détecté (VID:072F / Classe 0x0B CCID)</strong></div>
                        <div class="wf-subtext">Liaison Passerelle PC/SC Nominale 12 Mbps • En attente de déverrouillage de la session opérateur</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔐 Authentifier l'Opérateur & Ouvrir Session</button>
                        <button class="wf-btn wf-btn-sub">🛡️ Tester Enclave ES256</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Validation des Accréditations Opérateur & Déverrouillage Enclave
*Validation biométrique/badge opérateur et appel sécurisé du module Enclave Cryptographique (DEC-AET-10).*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Négociation des Droits & Sécurité</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Authentification en Cours</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Badge Détecté : Marc Lambert (Habilitation H3 • Agence Namur Centre)</div>
                        <div class="wf-subtext">Vérification de la clé d'habilitation agence et amorçage du sous-système cryptographique</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Initialisation de l'enclave cryptographique station...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Initialisation de l'Enclave Matérielle & Armement RF 13.56 MHz
*Armement de l'enclave station pour signatures ES256 (DEC-AET-10) et mise en veille active du lecteur.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Console de Sécurité Matérielle</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Armement Station (85%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 85%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [AUTH-OP] Opérateur OP-NAM-8842 vérifié : Habilitation H3 valide</code><br>
                        <code>> [CRYPTO-ENCLAVE] Liaison Secure Enclave / StrongBox (ES256 DEC-AET-10) : Établie</code><br>
                        <code>> [LOT-MGMT] Lot ACOSJ-92K-2026-N1 verrouillé pour 50 cartes</code><br>
                        <code>> [RF-RADIO] ACR1552U porteuse 13.56 MHz allumée • Vitesse 106 kbps ISO 14443-4</code><br>
                        <code>> [HARDWARE] LED verte fixe allumée • Silence sonore de recueillement activé</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Session Opérateur Ouverte & Station Prête pour Gravure
*Station authentifiée et prête. L'opérateur peut déposer la première JavaCard ACOSJ 92 Ko.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Poste d'Encodage Opérationnel</span>
                        <span class="wf-status-badge wf-badge-success">✨ Session Active (OP-NAM-8842)</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🛡️</span>
                        <div>
                          <strong>Station Authentifiée • Enclave Cryptographique Active (DEC-AET-10)</strong>
                          <p class="wf-subtext">Opérateur : Marc Lambert (Agence Namur) • Lot ACOSJ 92 Ko prêt • Lecteur ACR1552U en écoute</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Insertion de la JavaCard ACOSJ 92 Ko →</button>
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
| **4** | **Scellement & Fin ✨** | Carte ACOSJ Validée pour Gravure | `Statut : success` | Puce prête pour l'allocation des fichiers élémentaires EF-1, EF-2 et EF-3. |

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
*Puce prête pour l'allocation des fichiers élémentaires EF-1, EF-2 et EF-3.*

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
> Système de fichiers silicium initialisé selon la table canonique stricte du jalon STORAGE-001 (86 528 octets utiles / 92 160 octets total).

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Envoi de la commande APDU de formatage sécurisé pour effacement des anciennes structures ou résidus d'usine.
2. Création du Master File (MF) et du Dedicated File (DF AeterniTrak).
3. Création des six Fichiers Élémentaires (EF-0 à EF-5) prescrits par STORAGE-001 (table canonique 86 528 octets utiles / 92 160 octets total) :
4. - `EF-0 (Header/UID)` : 512 octets réservés pour passeport matériel TLV, UID, flags.
5. - `EF-1 (Profile)` : 2 048 octets réservés pour profil CBOR civil mémoriel canonique.
6. - `EF-2 (Portrait)` : 20 480 octets réservés pour portrait WebP 480×480 px (DEC-AET-12).
7. - `EF-3 (Voice)` : 46 080 octets réservés pour mémo vocal Opus SILK 16 kHz.
8. - `EF-4 (Registry)` : 15 360 octets réservés pour registre sépulture & hommages.
9. - `EF-5 (Signature)` : 2 048 octets réservés pour enveloppe COSE_Sign1 scellée.
10. - `Réserve d'usure matérielle` : 5 632 octets (6,11 % > plancher de 5 % garanti pour wear-leveling).
11. Vérification de l'absence de fragmentation mémoire.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `useful_size` | **Partitions Utiles (EF-0 à EF-5)** | `text` | `86 528 octets utiles (6 EF alloués)` | Taille utile | `86 528 o` | ✅ Requis |
| `wear_reserve` | **Réserve d'Usure / Wear-Leveling** | `text` | `5 632 octets (6,11 % > 5 %)` | Réserve | `5 632 o` | ✅ Requis |
| `total_allocated` | **Total Silicium EEPROM** | `text` | `92 160 octets (100% sans fragmentation)` | Total | `92 160 o` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_format_eeprom` | **Initialiser la Structure EF Silicium (STORAGE-001)** | `primary` | `idle` | 🗄️ |
| `btn_check_ef` | **Vérifier Table d'Allocation EF** | `secondary` | `idle` | 🔍 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Système de Fichiers Silicium Initialisé
>
> **Badge de Conformité :** `Table Canonique STORAGE-001`
>
> **Détail Opérationnel :** Table canonique allouée : 86 528 octets utiles (EF-0 à EF-5), 5 632 octets réserve (6,11 %), total 92 160 octets.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_EEPROM_QUOTA_EXCEEDED` |
| **Intitulé de l'Incident** | **Dépassement de la Capacité EEPROM** |
| **Condition Déclenchante** | Tentative d'allocation d'une partition dont la taille dépasse les 86 528 octets utiles de la puce physique. |
| **Message d'Erreur UI** | *« Erreur d'allocation : La somme des partitions demandées dépasse le budget utile canonique de 86 528 octets. »* |
| **Action Corrective Requise** | **Restaurer les tailles standard prescrites par la table canonique (86 528 octets utiles, 5 632 octets réserve, 92 160 octets total).** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Station Pro • Partitionneur EEPROM Silicium (STORAGE-001)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | EEPROM Vierge Non Partitionnée | *En attente utilisateur* | Carte connectée. La table canonique des fichiers EF-0 à EF-5 n'est pas encore créée. |
| **2** | **Déclenchement ⚡** | Clic sur 'Initialiser la Structure EF Silicium' | `Émission des commandes APDU de création des fichiers EF-0 à EF-5` | Ordre d'écriture physique de la structure de répertoires in-silico. |
| **3** | **Traitement ⚙️** | Écriture APDU des Descripteurs EF & Vérification Codes 90 00 | `Progression : 85%` | La puce confirme la création de chaque bloc de mémoire flash. |
| **4** | **Scellement & Fin ✨** | Structure Canonique EF-0 à EF-5 Initialisée avec Succès | `Statut : success` | Système de fichiers prêt pour recevoir les flux de données compressés. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-203 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : EEPROM Vierge Non Partitionnée
*Carte connectée. La table canonique des fichiers EF-0 à EF-5 n'est pas encore créée.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Partitionneur EEPROM</span>
                        <span class="wf-status-badge wf-badge-neutral">EEPROM Vierge (0/6 EF créés)</span>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-mini-stat">EF-0 (512 o) : En attente</div>
                        <div class="wf-mini-stat">EF-1 (2 Ko) : En attente</div>
                        <div class="wf-mini-stat">EF-2 (20 Ko) : En attente</div>
                        <div class="wf-mini-stat">EF-3 (45 Ko) : En attente</div>
                        <div class="wf-mini-stat">EF-4 (15 Ko) : En attente</div>
                        <div class="wf-mini-stat">EF-5 (2 Ko) : En attente</div>
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
                        <div class="wf-trigger-indicator">✓ Envoi APDU `CREATE FILE` pour EF-0 à EF-5</div>
                        <div class="wf-subtext">Table canonique : 86 528 octets utiles / 92 160 octets total (réserve 5 632 octets / 6,11 %)</div>
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
                        <code>> [APDU-TX] CREATE EF-0 (512 o) à EF-5 (2 048 o) -> 90 00</code><br>
                        <code>> [SYS-EEPROM] Quota utile 86 528 o / Réserve 5 632 o (6,11 %) : Conforme</code><br>
                        <code>> [APDU-TX] Vérification structure sans fragmentation : SUCCÈS</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Structure Canonique EF-0 à EF-5 Initialisée avec Succès
*Système de fichiers prêt pour recevoir les flux de données compressés.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Silicium Partitionné</span>
                        <span class="wf-status-badge wf-badge-success">✨ Table Canonique OK</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🗄️</span>
                        <div>
                          <strong>Partitions EF Silicium Créées sans Fragmentation</strong>
                          <p class="wf-subtext">86 528 octets utiles (EF-0 à EF-5) • Réserve 5 632 octets (6,11 %) • Total 92 160 octets</p>
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
                        <code>> [APDU-SEG] Découpage en 306 tranches de 255 octets (Payload EF-2 + EF-3)</code>
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
                          <p class="wf-subtext">306 blocs APDU prêts à être injectés sur les partitions EF-2 et EF-3</p>
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
> 86 528 octets gravés avec succès dans l'EEPROM de la JavaCard ACOSJ (table canonique).

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Sélection successive des fichiers `EF-0` à `EF-5` via `SELECT FILE`.
2. Envoi cadencé des commandes APDU `UPDATE BINARY` (commande `00 D6 P1 P2 Lc [Octets]`).
3. Contrôle systématique du mot de statut `90 00` en réponse à chaque bloc.
4. Gestion des reprises sur incident : si un bloc échoue, rejeu automatique (max 3 tentatives).
5. Mise à jour en temps réel de la barre de progression pour l'opérateur.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `block_count` | **Nombre de Blocs** | `text` | `340 blocs de 255 octets` | Blocs | `Table Canonique` | ⭕ Optionnel |
| `transfer_rate` | **Vitesse de Transfert** | `text` | `14.2 Ko/sec (106 kbps IsoDep)` | Débit | `106k` | ⭕ Optionnel |
| `error_rate` | **Taux d'Erreur APDU** | `text` | `0 erreur (acquittements 90 00)` | Erreurs | `0 Défaut` | ⭕ Optionnel |
| `elapsed_time` | **Temps Écoulé** | `text` | `06.1 secondes` | Temps | `Chrono` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_start_burning` | **Lancer la Gravure Silicium** | `primary` | `idle` | 🔥 |
| `btn_pause_burning` | **Mettre en Pause** | `secondary` | `idle` | ⏸ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Gravure Silicium Achevée avec Succès
>
> **Badge de Conformité :** `Table Canonique Écrite (90 00)`
>
> **Détail Opérationnel :** 86 528 octets injectés dans les partitions EF-0 à EF-5 sans aucune erreur.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_APDU_WRITE_FAILURE` |
| **Intitulé de l'Incident** | **Échec de Transmission d'un Bloc APDU** |
| **Condition Déclenchante** | Micro-déplacement de la carte sur l'antenne provoquant un code statut `6A 84` ou perte de liaison. |
| **Message d'Erreur UI** | *« Erreur d'écriture : Rupture de liaison RF lors de l'injection d'un bloc. »* |
| **Action Corrective Requise** | **Laisser la carte immobile au contact de l'antenne et relancer la procédure d'écriture automatique.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Station Pro • Graveur Silicium APDU IsoDep**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Graveur en Attente de Démarrage | *En attente utilisateur* | Les blocs sont prêts. La jauge d'écriture est à 0%. |
| **2** | **Déclenchement ⚡** | Lancement de la Rafale de Commandes APDU | `Clic sur 'Lancer la Gravure Silicium' et sélection des fichiers EF-0 à EF-5` | Lancement de la boucle cadencée d'envoi des commandes UPDATE BINARY. |
| **3** | **Traitement ⚙️** | Injection en Cours : Blocs Silicium (65%) | `Progression : 65%` | Écriture active dans les cellules EEPROM avec acquittement 90 00 systématique. |
| **4** | **Scellement & Fin ✨** | Gravure Silicium Accomplie à 100% | `Statut : success` | Totalité des 86 528 octets utiles gravés avec intégrité absolue. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-205 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Graveur en Attente de Démarrage
*Les blocs sont prêts. La jauge d'écriture est à 0%.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Graveur Silicium</span>
                        <span class="wf-status-badge wf-badge-neutral">Prêt à Graver (86 528 octets)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 0%;"></div></div>
                      <div class="wf-device-status-box">
                        <div><strong>86 528 octets utiles prêts à être écrits sur l'ACOSJ 92k (table canonique)</strong></div>
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

#### Phase 3 - Traitement : Injection en Cours : Blocs Silicium (65%)
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
                        <code>> [APDU-TX] 00 D6 02 C4 FF [255 octets Opus]   -> < 90 00</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Gravure Silicium Accomplie à 100%
*Totalité des 86 528 octets utiles gravés avec intégrité absolue.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Gravure Accomplie</span>
                        <span class="wf-status-badge wf-badge-success">✨ Table Canonique Scellée (100%)</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">💾</span>
                        <div>
                          <strong>Données Mémorielles Gravées in-silico</strong>
                          <p class="wf-subtext">86 528 octets utiles stockés (EF-0 à EF-5) • Prêt pour scellement cryptographique par l'enclave station (DEC-AET-10)</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Signature COSE_Sign1 →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-206"></a>
## UC-206 : Scellement Cryptographique COSE_Sign1 PaxFunèbre (Enclave Station DEC-AET-10)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-206` |
| **Catégorie Métier** | **Cryptographie & Signature** |
| **Acteur Principal** | Opérateur d'Encodage |
| **Plateformes Cibles** | WebUSB (Chromium Desktop), PC/SC (Desktop Natif) |
| **Tags Clés** | `COSE_Sign1`, `Ed25519`, `ES256`, `EnclaveStation`, `DEC-AET-10`, `RFC9052` |
| **Base Légale & Normative** | Spécification technique IETF RFC 9052 (COSE Structures and Process) et RFC 9596 (COSE typ Header). |
| **Terminal / Canvas Wireframe** | `PaxStation Station Pro • Module de Signature Matérielle Enclave (DEC-AET-10)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Données gravées sur la puce mais non encore signées.

> [!TIP]
> **Postconditions Garanties :**
> Carte physique scellée par l'enclave station (DEC-AET-10) avec signature COSE_Sign1 officielle infalsifiable.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Appel à l'enclave sécurisée de la station (PaxStation Enclave sous DEC-AET-10).
2. Construction de la structure canonique `Sig_structure` COSE_Sign1 (Tag 18, DEC-AET-10) selon la RFC 9052 :
3. - Contexte : `"Signature1"`
4. - En-tête protégé : `{1: -8, 16: "application/aeternitrak-profile+cbor"}` (Ed25519) ou `{1: -7}` (ES256)
5. - Données associées externes : `h''` (vide)
6. - Charge utile : le condensat SHA-256 de la capsule
7. Génération de la signature cryptographique par la clé d'autorité officielle de l'enclave station.
8. Écriture de l'enveloppe signée COSE_Sign1 dans le fichier dédié `EF-5` (0x0005) de la carte.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `hsm_module` | **Module Enclave Station** | `text` | `PaxStation Enclave Sécurisée (DEC-AET-10)` | Enclave | `DEC-AET-10` | ⭕ Optionnel |
| `sig_alg` | **Algorithme Utilisé** | `select` | `Ed25519 (EdDSA, alg: -8, RFC 8032)` | Algorithme | `Recommandé` | ✅ Requis |
| `mime_typ` | **Type MIME Protégé (typ)** | `text` | `application/aeternitrak-profile+cbor (RFC 9596)` | Type | `Protégé` | ⭕ Optionnel |
| `key_kid` | **Empreinte Clé Publique (kid)** | `text` | `3c81e592...71aa (16 octets SHA-256)` | kid | `16 Octets` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_sign_cose` | **Générer le Sceau Matériel COSE_Sign1 (DEC-AET-10)** | `primary` | `idle` | 🔐 |
| `btn_inspect_sig_struct` | **Inspecter Sig_structure** | `secondary` | `idle` | 🔍 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Sceau Cryptographique COSE_Sign1 Apposé
>
> **Badge de Conformité :** `Tag 18 • Enclave DEC-AET-10`
>
> **Détail Opérationnel :** Enveloppe signée par l'enclave station (DEC-AET-10) et gravée sur EF-5. Intégrité infalsifiable garantie sans contact.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_COSE_EXPIRED_KEY` |
| **Intitulé de l'Incident** | **Clé de Scellement Enclave Expirée** |
| **Condition Déclenchante** | Tentative de signature avec une enclave dont le certificat d'autorité est expiré. |
| **Message d'Erreur UI** | *« Erreur de sécurité : La clé matérielle de scellement a dépassé sa date limite de validité. »* |
| **Action Corrective Requise** | **Procéder au renouvellement de clé auprès de l'autorité centrale AeterniTrak.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Station Pro • Module de Signature Matérielle Enclave (DEC-AET-10)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Données Gravées Non Signées | *En attente utilisateur* | Puce écrite. La partition EF-5 est vide, le sceau officiel n'est pas encore apposé. |
| **2** | **Déclenchement ⚡** | Appel à l'Enclave Station (DEC-AET-10) & Construction de la Sig_structure | `Clic sur 'Générer le Sceau Matériel COSE_Sign1 (DEC-AET-10)'` | Assemblage des en-têtes protégés déterministes et scellement par l'enclave station (DEC-AET-10). |
| **3** | **Traitement ⚙️** | Signature Déterministe RFC 8032 & Injection sur EF-5 | `Progression : 92%` | Double hachage SHA-512 sans aléa et écriture de l'enveloppe de 64 octets sur la puce. |
| **4** | **Scellement & Fin ✨** | Sceau COSE_Sign1 Scellé sur le Silicium | `Statut : success` | La carte est cryptographiquement protégée. Toute tentative d'altération sera détectée. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-206 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Données Gravées Non Signées
*Puce écrite. La partition EF-5 est vide, le sceau officiel n'est pas encore apposé.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Scellement Cryptographique</span>
                        <span class="wf-status-badge wf-badge-neutral">Puce Non Signée</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-key-icon">🔑</span>
                        <div><strong>Enclave matérielle PaxStation en ligne (DEC-AET-10)</strong></div>
                        <div class="wf-subtext">Algorithme cible : Ed25519 (alg: -8) • Enveloppe COSE_Sign1 Tag 18</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔐 Générer le Sceau Matériel COSE_Sign1</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Appel à l'Enclave Station (DEC-AET-10) & Construction de la Sig_structure
*Assemblage des en-têtes protégés déterministes et scellement par l'enclave station (DEC-AET-10).*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Moteur de Signature</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Appel Enclave Station</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">⚡ Sig_structure [ "Signature1", protected, external_aad, payload ]</div>
                        <div class="wf-subtext">Signature Ed25519 en cours par l'enclave station Le Pax Funèbre (DEC-AET-10)</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Calcul cryptographique matériel...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Signature Déterministe RFC 8032 & Injection sur EF-5
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
                        <code>> [DEC-AET-10] Scellement par enclave station validé (Tag 18)</code><br>
                        <code>> [APDU-SIGN] Écriture sur EF-5 (APDU UPDATE BINARY) : < 90 00</code>
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
                          <strong>Signature Cryptographique PaxStation Apposée (DEC-AET-10)</strong>
                          <p class="wf-subtext">Ed25519 • Enclave station • kid: 3c81e592...71aa • Inaltérable sans contact</p>
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
| **Code d'Erreur Normatif** | `ERR_COSE_MALLEABLE_SIGNATURE` |
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
## UC-210 : Diagnostic Silicium, Relecture des 6 EF & PV de Gravure Officiel

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-210` |
| **Catégorie Métier** | **Assurance Qualité & Conformité** |
| **Acteur Principal** | Opérateur d'Encodage & Conseiller Funéraire |
| **Plateformes Cibles** | PC/SC (Desktop Natif), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `QA`, `Diagnostic`, `Relecture6EF`, `FusibleAntiTamper`, `PVRemise`, `COSE_Sign1`, `DEC-AET-10` |
| **Base Légale & Normative** | Code de droit économique belge (garantie de conformité des biens et services funéraires — référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `PaxStation Station Pro • Banc de Diagnostic Silicium & Édition PV` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Carte physique gravée et imprimée reposée sur le lecteur de contrôle qualité ACR1552U.

> [!TIP]
> **Postconditions Garanties :**
> Diagnostic 100% conforme des 6 EF (EF-0 à EF-5), intégrité signature certifiée, fusible matériel in-silico verrouillé, PV de remise officiel édité et coffret prêt pour la famille.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Relecture sans contact séquentielle des 6 Elementary Files (EF-0 à EF-5) via l'antenne NFC de recette à 106 kbps.
2. Audit binaire de conformité de chaque compartiment : EF-0 (Manifeste), EF-1 (Identité), EF-2 (Portrait WebP 480×480 DEC-AET-12), EF-3 (Mémo Vocal Opus), EF-4 (Volontés Civiles), EF-5 (Signature).
3. Vérification mathématique indépendante de la signature COSE_Sign1 apposée par l'enclave de la station (DEC-AET-10) avec contrôle anti-malléabilité du s bas (RFC 9052).
4. Interrogation matérielle de l'état du fusible in-silico (commande APDU 80 DE 00 00 confirmant le verrouillage irréversible anti-tamper en lecture seule).
5. Génération du Procès-Verbal (PV) de Remise Officiel infalsifiable avec QR code de contrôle d'intégrité et empreinte SHA-256 scellée.
6. Insertion solennelle des deux cartes mémorielles dans leur coffret doublé de velours Le Pax Funèbre pour remise à la famille.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `recheck_6ef` | **Relecture sans Contact des 6 EF** | `text` | `EF-0 à EF-5 relus (78 412 octets sur 86 528 utiles — 0 divergence)` | Audit 6 EF | `6 EF Intègres` | ⭕ Optionnel |
| `recheck_sig` | **Intégrité Signature COSE_Sign1** | `text` | `VALIDE (Enclave Station DEC-AET-10 • ES256 / s bas normalisé RFC 9052)` | Signature | `Authentique` | ⭕ Optionnel |
| `fuse_status` | **État Fusible Matériel in-silico** | `text` | `VERROUILLÉ DÉFINITIF (APDU 80 DE 01 00 — Lecture Seule Anti-Tamper)` | Fusible | `Anti-Tamper Scellé` | ⭕ Optionnel |
| `pv_reference` | **Procès-Verbal de Remise Famille** | `text` | `PV-2026-NAM-0491 (Horodatage certifié & QR Code d'Intégrité)` | Numéro PV | `PDF Scellé` | ⭕ Optionnel |
| `recipient_family` | **Destinataire Mandataire** | `text` | `Claire Dubois (Mandat familial n° 8841)` | Famille | `Mandataire` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_run_full_diag` | **Lancer le Diagnostic Intégral & Relecture 6 EF** | `primary` | `idle` | 🔬 |
| `btn_print_pv` | **Générer le PV de Remise Officiel (PDF Scellé)** | `secondary` | `idle` | 📄 |
| `btn_seal_box` | **Valider la Mise en Coffret Mémoriel** | `secondary` | `idle` | 🎁 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Diagnostic Silicium Conforme & PV Officiel Validé
>
> **Badge de Conformité :** `6 EF Conformes • Fusible Scellé • PV Émis`
>
> **Détail Opérationnel :** Audit sans contact des 6 EF (EF-0 à EF-5) 100% conforme. Signature enclave station vérifiée. Fusible matériel actif. Coffret prêt pour remise à la famille.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_DIAGNOSTIC_EF_INTEGRITY_FAIL` |
| **Intitulé de l'Incident** | **Divergence sur Relecture des 6 EF ou Fusible Ouvert** |
| **Condition Déclenchante** | Altération binaire sur l'un des EF (EF-0 à EF-5), fusible matériel non verrouillé ou signature COSE_Sign1 corrompue. |
| **Message d'Erreur UI** | *« REJET QUALITÉ CRITIQUE : L'empreinte binaire relue sur la puce ne concorde pas avec la capsule d'origine ou le fusible est resté ouvert. »* |
| **Action Corrective Requise** | **Mettre immédiatement la carte au rebut, détruire le support non conforme et consigner l'incident pour réencodage d'une nouvelle carte ACOSJ 92 Ko.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Station Pro • Banc de Diagnostic Silicium & Édition PV**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Carte Terminée Déposée sur le Banc de Diagnostic | *En attente utilisateur* | Carte posée sur le lecteur sans contact. Le formulaire de diagnostic des 6 EF et génération du PV est en attente d'exécution. |
| **2** | **Déclenchement ⚡** | Lancement du Diagnostic & Relecture sans Contact des 6 EF | `Clic sur 'Lancer le Diagnostic Intégral & Relecture 6 EF'` | Interrogation séquentielle sans fil des compartiments EF-0 à EF-5 à 106 kbps et contrôle cryptographique. |
| **3** | **Traitement ⚙️** | Audit Binaire des 6 EF & Contrôle Fusible in-silico | `Progression : 96%` | Validation des 6 EF (EF-0 à EF-5), vérification de la signature enclave station et confirmation du fusible verrouillé. |
| **4** | **Scellement & Fin ✨** | Procès-Verbal de Remise Émis & Coffret Mémoriel Scellé | `Statut : success` | Diagnostic 100% conforme. Le PV officiel de remise est édité et le coffret velours est scellé pour la famille. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-210 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Carte Terminée Déposée sur le Banc de Diagnostic
*Carte posée sur le lecteur sans contact. Le formulaire de diagnostic des 6 EF et génération du PV est en attente d'exécution.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Banc de Diagnostic & Recette Qualité</span>
                        <span class="wf-status-badge wf-badge-neutral">En Attente de Diagnostic</span>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-field-group">
                          <label class="wf-label">Carte en Position de Contrôle</label>
                          <div class="wf-select-placeholder">ACOSJ-92K #NAM-2026-0491 (Henri Dubois)</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Procédure de Recette</label>
                          <div class="wf-select-placeholder">Lecture sans contact 6 EF (EF-0 à EF-5) + Signature + Fusible</div>
                        </div>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-qa-icon">🔬</span>
                        <div><strong>Banc de Diagnostic Prêt pour Relecture Intégrale</strong></div>
                        <div class="wf-subtext">Audit automatique : Vérification binaire 6 EF + Validité COSE_Sign1 + Statut fusible in-silico</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔬 Lancer le Diagnostic Intégral & Relecture 6 EF</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Lancement du Diagnostic & Relecture sans Contact des 6 EF
*Interrogation séquentielle sans fil des compartiments EF-0 à EF-5 à 106 kbps et contrôle cryptographique.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Audit Silicium en Cours</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Relecture 6 EF Active</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Relecture NFC des 6 EF (78 412 octets relus à 106 kbps)</div>
                        <div class="wf-subtext">Contrôle de concordance binaire bit-à-bit et interrogation du registre fusible APDU</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Relecture des 6 EF & contrôle fusible...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Audit Binaire des 6 EF & Contrôle Fusible in-silico
*Validation des 6 EF (EF-0 à EF-5), vérification de la signature enclave station et confirmation du fusible verrouillé.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Moteur de Diagnostic Silicium</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Contrôle Final (96%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 96%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [DIAG-EF] EF-0 Manifeste (512 o) : Intègre (SHA-256 conforme)</code><br>
                        <code>> [DIAG-EF] EF-1 Identité Civile (2 048 o) : Intègre (Henri Dubois)</code><br>
                        <code>> [DIAG-EF] EF-2 Portrait WebP 480x480 (18 432 o, DEC-AET-12) : Intègre</code><br>
                        <code>> [DIAG-EF] EF-3 Mémo Vocal Opus (49 152 o) : Intègre</code><br>
                        <code>> [DIAG-EF] EF-4 Volontés Civiles (8 192 o) : Intègre</code><br>
                        <code>> [DIAG-EF] EF-5 Signature COSE_Sign1 Enclave Station (DEC-AET-10) : VALIDE (s bas)</code><br>
                        <code>> [FUSE-CHECK] Commande 80 DE 00 00 : Fusible in-silico VERROUILLÉ DÉFINITIF</code><br>
                        <code>> [PV-ENGINE] Génération du PV officiel PV-2026-NAM-0491 scellé...</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Procès-Verbal de Remise Émis & Coffret Mémoriel Scellé
*Diagnostic 100% conforme. Le PV officiel de remise est édité et le coffret velours est scellé pour la famille.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Diagnostic Validé & PV Émis</span>
                        <span class="wf-status-badge wf-badge-success">✨ 100% Conforme • Scellé</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🏆</span>
                        <div>
                          <strong>Procès-Verbal de Remise Officiel n° PV-2026-NAM-0491 Validé</strong>
                          <p class="wf-subtext">6 EF intègres (EF-0 à EF-5) • Fusible in-silico verrouillé • Coffret velours scellé pour Claire Dubois</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Bascule vers App 3 : Sanctuaire Mémoriel Mobile →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-211"></a>
## UC-211 : Déconnexion Brutale & Perte de Champ RF pendant l'Écriture (Anti-Tearing & Tag 0x07 COMMIT_FLAG)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-211` |
| **Catégorie Métier** | **Résilience Matérielle & Silicium** |
| **Acteur Principal** | Opérateur d'Atelier Funéraire |
| **Plateformes Cibles** | Poste Pro Dédié (macOS, Windows, Linux) |
| **Tags Clés** | `AntiTearing`, `RFFieldLoss`, `COMMIT_FLAG`, `Tag0x07`, `EF-0`, `ACR1552U`, `ACOSJ92k` |
| **Base Légale & Normative** | Spécification technique AET-SPEC-STORAGE-001 §2.1 (Gestion transactionnelle TLV Tag 0x07) & Norme ISO/IEC 14443-4. |
| **Terminal / Canvas Wireframe** | `PaxStation Station Pro • Moniteur Transactionnel Anti-Tearing (Tag 0x07 EF-0)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> La PaxStation exécute une séquence de commandes APDU UPDATE BINARY sur la puce sans contact ACOSJ 92 Ko.

> [!TIP]
> **Postconditions Garanties :**
> Aucune écriture partielle n'est validée en EEPROM ; l'inviolabilité transactionnelle est garantie par le Tag 0x07.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. L'opérateur retire inopinément la carte sans contact de l'antenne ACR1552U ou une perturbation RF intervient en pleine écriture APDU.
2. Le lecteur ACR1552U intercepte la perte brutale de porteuse (Field Loss Event) et remonte l'anomalie au pilote PC/SC.
3. Au ré-enfichage de la carte sur le plateau, la PaxStation lit immédiatement le bloc de contrôle matériel EF-0.
4. Contrôle du Tag 0x07 (COMMIT_FLAG) : valeur lue 0x55 (In-Flight) au lieu de 0xAA (Committed) démontrant une écriture tronquée (tearing).
5. La station bloque toute utilisation du support corrompu, journalise l'incident et déclenche la purge de réinitialisation sécurisée de la puce.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `nfc_reader` | **Lecteur Sans Contact** | `text` | `ACS ACR1552U USB-C (Firmware v2.04)` | - | `Matériel` | ⭕ Optionnel |
| `commit_flag_status` | **État Transaction Silicium** | `text` | `Tag 0x07 COMMIT_FLAG = 0x55 (IN-FLIGHT DÉTECTÉ)` | - | `Tearing Alerte` | ⭕ Optionnel |
| `interrupted_ef` | **Partition Altérée** | `text` | `EF-3 Mémo Vocal (Interruption à l'offset 0x5A00)` | - | `Tronqué` | ⭕ Optionnel |
| `recovery_action` | **Action de Sécurité** | `select` | `Rejet du Lot & Réinitialisation Complète EEPROM` | - | `Souverain` | ✅ Requis |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_diagnose_tearing` | **Diagnostiquer l'État Anti-Tearing (Tag 0x07)** | `primary` | `idle` | ⚡ |
| `btn_reset_card_eeprom` | **Réinitialiser la Carte Silicium** | `secondary` | `idle` | 🔄 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Incident de Déconnexion Neutralisé par Anti-Tearing
>
> **Badge de Conformité :** `Anti-Tearing Conforme`
>
> **Détail Opérationnel :** Arrachement RF détecté et intercepté. Le COMMIT_FLAG 0x55 a protégé la carte contre toute corruption silencieuse.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_RF_FIELD_LOSS_TEARING` |
| **Intitulé de l'Incident** | **Perte de Champ RF & Arrachement Pendant Gravure (Tearing)** |
| **Condition Déclenchante** | Rupture de communication sans contact durant un cycle d'écriture APDU (Tag 0x07 = 0x55). |
| **Message d'Erreur UI** | *« Erreur matérielle critique : Perte de champ RF während der APDU-Transaktion. La puce est dans un état instable non scellé. »* |
| **Action Corrective Requise** | **Laisser la carte immobile sur l'antenne ACR1552U et lancer une séquence complète d'effacement et de réécriture.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Station Pro • Moniteur Transactionnel Anti-Tearing (Tag 0x07 EF-0)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Perte de Liaison Sans Contact Signalée | *En attente utilisateur* | La carte a été retirée du champ RF pendant l'injection des blocs audio dans EF-3. |
| **2** | **Déclenchement ⚡** | Interrogation du Tag 0x07 COMMIT_FLAG dans EF-0 | `Clic sur 'Diagnostiquer l'État Anti-Tearing'` | Émission de la commande APDU READ BINARY sur EF-0 pour inspecter l'octet de transaction matériel. |
| **3** | **Traitement ⚙️** | Purge des Blocs Partiels & Journalisation d'Atelier | `Progression : 98%` | Rejet des données corrompues et mise en sécurité du contrôleur de l'ACOSJ 92 Ko. |
| **4** | **Scellement & Fin ✨** | Sécurité Transactionnelle Rétablie | `Statut : success` | La puce n'a subi aucune dégradation définitive. La procédure garantit l'absence de données hybrides. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-211 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Perte de Liaison Sans Contact Signalée
*La carte a été retirée du champ RF pendant l'injection des blocs audio dans EF-3.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStation • Contrôle Transactionnel APDU</span>
                                            <span class="wf-status-badge wf-badge-neutral">Liaison RF Perdue</span>
                                          </div>
                                          <div class="wf-device-status-box" style="border-color: #ef4444;">
                                            <span class="wf-qa-icon">⚡</span>
                                            <div><strong>Arrachement RF Détecté en Cours d'Écriture</strong></div>
                                            <div class="wf-subtext">Session interrompue • Risque de corruption partielle (Tearing)</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary">⚡ Diagnostiquer l'État Anti-Tearing (Tag 0x07)</button>
                                          </div>
                                        </div>
```

#### Phase 2 - Déclenchement : Interrogation du Tag 0x07 COMMIT_FLAG dans EF-0
*Émission de la commande APDU READ BINARY sur EF-0 pour inspecter l'octet de transaction matériel.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStation • Diagnostic Silicium EF-0</span>
                                            <span class="wf-status-badge wf-badge-trigger">⚡ Lecture Tag 0x07</span>
                                          </div>
                                          <div class="wf-trigger-card wf-radar-pulse">
                                            <div class="wf-trigger-indicator">✓ APDU: 00 B0 00 3D 01 -> Réponse: 55 90 00</div>
                                            <div class="wf-subtext">Valeur 0x55 confirmée : transaction interrompue avant scellement (Commit absent)</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary wf-pulse-btn">Traitement de l'incident...</button>
                                          </div>
                                        </div>
```

#### Phase 3 - Traitement : Purge des Blocs Partiels & Journalisation d'Atelier
*Rejet des données corrompues et mise en sécurité du contrôleur de l'ACOSJ 92 Ko.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStation • Moteur de Résilience</span>
                                            <span class="wf-status-badge wf-badge-process">⚙️ Restauration (98%)</span>
                                          </div>
                                          <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 98%;"></div></div>
                                          <div class="wf-console-log">
                                            <code>> [ANTI-TEARING] Tag 0x07 = 0x55 : écriture incomplète interceptée</code><br>
                                            <code>> [SECURITY-LOCK] Invalidation automatique du profil corrompu</code><br>
                                            <code>> [WEAR-LEVELING] Secteurs EEPROM non endommagés (réserve 5 632 o intacte)</code><br>
                                            <code>> [RECOVERY] Puce prête pour réinitialisation complète ou rebut sécurisé</code>
                                          </div>
                                        </div>
```

#### Phase 4 - Fin de Cycle : Sécurité Transactionnelle Rétablie
*La puce n'a subi aucune dégradation définitive. La procédure garantit l'absence de données hybrides.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStation • Statut Sécurisé</span>
                                            <span class="wf-status-badge wf-badge-success">✨ Incident Maîtrisé</span>
                                          </div>
                                          <div class="wf-success-banner">
                                            <span class="wf-seal-icon">🛡️</span>
                                            <div>
                                              <strong>Mécanisme Anti-Tearing Opérationnel à 100%</strong>
                                              <p class="wf-subtext">Puce protégée par Tag 0x07 • Aucune donnée tronquée n'a été validée en mémoire</p>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-gold">Lancer la Réécriture Complète →</button>
                                          </div>
                                        </div>
```

</details>

---

<a id="uc-212"></a>
## UC-212 : Tentative de Réécriture sur Puce Déjà Verrouillée / Fusible Grillé (Tag 0x06 LOCK_FUSE = 0x01, SW 0x6985)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-212` |
| **Catégorie Métier** | **Sécurité Silicium & Anti-Tamper** |
| **Acteur Principal** | Opérateur d'Atelier Funéraire |
| **Plateformes Cibles** | Poste Pro Dédié (macOS, Windows, Linux) |
| **Tags Clés** | `LOCK_FUSE`, `Fusible`, `SW6985`, `AntiTamper`, `ReadOnly`, `ACOSJ92k`, `EF-0` |
| **Base Légale & Normative** | Spécification technique AET-SPEC-STORAGE-001 §2.1 (Tag 0x06 FUSE_STATUS) & Décision Kudoro DEC-AET-01. |
| **Terminal / Canvas Wireframe** | `PaxStation Station Pro • Détecteur Fusible Matériel LOCK_FUSE (EF-0)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Pose sur le lecteur ACR1552U d'une carte préalablement encodée dont le fusible matériel anti-tamper in-silico a déjà été grillé.

> [!TIP]
> **Postconditions Garanties :**
> La carte reste protégée en lecture seule perpétuelle ; aucune tentative de falsification ou réécriture n'aboutit.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. L'opérateur dépose par mégarde une carte déjà gravée et scellée sur le lecteur de bureau.
2. La PaxStation tente d'exécuter une commande d'authentification ou d'initialisation en écriture APDU.
3. L'applet ACOSJ interroge le Tag 0x06 (LOCK_FUSE) de son registre physique : état = 0x01 (Fusible claqué).
4. Le microcontrôleur bloque immédiatement l'opération et retourne le status word normatif ISO 7816-4 : SW = 0x6985 (Conditions of use not satisfied).
5. La station passe en alerte rouge solennelle : interdiction absolue de toute écriture, confirmation de la lecture seule perpétuelle.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `card_uid_detected` | **Carte Détectée sur ACR1552U** | `text` | `ACOSJ-92K #04:5A:32:8F:1C:7B:80` | - | `UID Matériel` | ⭕ Optionnel |
| `fuse_status` | **État du Fusible Matériel** | `text` | `Tag 0x06 LOCK_FUSE = 0x01 (FUSIBLE DÉFINITIVEMENT GRILLÉ)` | - | `Inviolable` | ⭕ Optionnel |
| `apdu_sw_response` | **Réponse Commande Écriture APDU** | `text` | `Code Statut : SW 0x6985 (Conditions of use not satisfied)` | - | `Rejet Matériel` | ⭕ Optionnel |
| `station_verdict` | **Verdict de la Station** | `text` | `ACCÈS ÉCRITURE REFUSÉ • SUPPORT SCELLÉ PERPÉTUEL` | - | `Lecture Seule` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_verify_fuse_lock` | **Vérifier le Statut du Fusible Silicium** | `primary` | `idle` | 🔒 |
| `btn_eject_locked_card` | **Éjecter la Carte Scellée** | `secondary` | `idle` | ⏏️ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Verrouillage Matériel Anti-Tamper Confirmé Inviolable
>
> **Badge de Conformité :** `Conforme SW 0x6985 / LOCK_FUSE`
>
> **Détail Opérationnel :** Fusible matériel 0x01 vérifié. L'ACOSJ 92 Ko refuse toute commande d'écriture avec SW 0x6985. Protection perpétuelle certifiée.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_SILICON_PERMANENTLY_LOCKED` |
| **Intitulé de l'Incident** | **Rejet Matériel : Puce Déjà Verrouillée en Lecture Seule** |
| **Condition Déclenchante** | Tentative d'écriture APDU sur une carte dont le fusible matériel Tag 0x06 est à 0x01 (retour SW 0x6985). |
| **Message d'Erreur UI** | *« Opération interdite : La puce ACOSJ est définitivement scellée par son fusible matériel. Aucune modification n'est physiquement possible. »* |
| **Action Corrective Requise** | **Retirer immédiatement la carte du lecteur ; utiliser une carte ACOSJ 92 Ko vierge d'atelier pour une nouvelle gravure.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Station Pro • Détecteur Fusible Matériel LOCK_FUSE (EF-0)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Carte Déposée avec Fusible Déjà Verrouillé | *En attente utilisateur* | La carte posée sur le lecteur a déjà achevé son cycle de vie d'atelier et son fusible est grillé. |
| **2** | **Déclenchement ⚡** | Envoi de la Commande APDU & Réception du SW 0x6985 | `Clic sur 'Vérifier le Statut du Fusible Silicium'` | Tentative d'écriture rejetée par le microcontrôleur JavaCard avec le code de statut d'interdiction matérielle. |
| **3** | **Traitement ⚙️** | Certification du Statut de Lecture Seule Perpétuelle | `Progression : 100%` | Validation que les 6 Fichiers Élémentaires (EF-0 à EF-5) restent intègres et accessibles en lecture sans contact. |
| **4** | **Scellement & Fin ✨** | Alerte de Protection Validée & Invitation au Retrait | `Statut : success` | Sécurité absolue démontrée. La carte est protégée contre toute réécriture malveillante ou involontaire. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-212 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Carte Déposée avec Fusible Déjà Verrouillé
*La carte posée sur le lecteur a déjà achevé son cycle de vie d'atelier et son fusible est grillé.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStation • Contrôle Anti-Tamper Silicium</span>
                                            <span class="wf-status-badge wf-badge-neutral">Puce Insérée</span>
                                          </div>
                                          <div class="wf-content-grid">
                                            <div class="wf-field-group">
                                              <label class="wf-label">Carte Présente</label>
                                              <div class="wf-input-placeholder">ACOSJ-92K (Scellée antérieurement)</div>
                                            </div>
                                            <div class="wf-field-group">
                                              <label class="wf-label">Opération Tentée</label>
                                              <div class="wf-input-placeholder">Initialisation / Écriture APDU</div>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary">🔒 Vérifier le Statut du Fusible Silicium</button>
                                          </div>
                                        </div>
```

#### Phase 2 - Déclenchement : Envoi de la Commande APDU & Réception du SW 0x6985
*Tentative d'écriture rejetée par le microcontrôleur JavaCard avec le code de statut d'interdiction matérielle.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStation • Dialogue APDU ISO 7816-4</span>
                                            <span class="wf-status-badge wf-badge-trigger">⚡ Commande Rejetée</span>
                                          </div>
                                          <div class="wf-trigger-card wf-radar-pulse" style="border-color: #ef4444;">
                                            <div class="wf-trigger-indicator" style="color: #fda4af;">🔒 Commande 80 DE 01 00 rejetée : SW = 0x6985</div>
                                            <div class="wf-subtext">Conditions of use not satisfied : le fusible matériel Tag 0x06 = 0x01 interdit toute modification</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary wf-pulse-btn">Interprétation du verrouillage...</button>
                                          </div>
                                        </div>
```

#### Phase 3 - Traitement : Certification du Statut de Lecture Seule Perpétuelle
*Validation que les 6 Fichiers Élémentaires (EF-0 à EF-5) restent intègres et accessibles en lecture sans contact.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStation • Diagnostic de Verrouillage</span>
                                            <span class="wf-status-badge wf-badge-process">⚙️ Vérification Lecture Seule</span>
                                          </div>
                                          <div class="wf-console-log">
                                            <code>> [APDU-STATUS] SW 0x6985 intercepté : fusible in-silico irréversiblement actif</code><br>
                                            <code>> [TAG-0x06] FUSE_STATUS = 0x01 (Permanent Lock)</code><br>
                                            <code>> [TAMPER-PROOF] Zéro écriture autorisée • Protection cryptographique absolue</code><br>
                                            <code>> [READ-ACCESS] EF-0 à EF-5 consultables en lecture sans contact à 106 kbps</code>
                                          </div>
                                        </div>
```

#### Phase 4 - Fin de Cycle : Alerte de Protection Validée & Invitation au Retrait
*Sécurité absolue démontrée. La carte est protégée contre toute réécriture malveillante ou involontaire.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStation • Support Verrouillé</span>
                                            <span class="wf-status-badge wf-badge-success">✨ Protection Inviolable</span>
                                          </div>
                                          <div class="wf-success-banner">
                                            <span class="wf-seal-icon">🔒</span>
                                            <div>
                                              <strong>Carte ACOSJ 92 Ko Scellée Définitivement (SW 0x6985)</strong>
                                              <p class="wf-subtext">Fusible matériel actif • Données perpétuelles protégées contre toute altération</p>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-sub">⏏️ Éjecter la Carte et Insérer un Support Vierge</button>
                                          </div>
                                        </div>
```

</details>

---

<a id="uc-213"></a>
## UC-213 : Révocation de Clé Privée d'Enclave ou Certificat d'Opérateur Expiré

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-213` |
| **Catégorie Métier** | **Cryptographie & Contrôle d'Accès** |
| **Acteur Principal** | Administrateur Système & Opérateur Funéraire |
| **Plateformes Cibles** | Poste Pro Dédié (macOS, Windows, Linux) |
| **Tags Clés** | `TrustList`, `Revocation`, `CertificatExpire`, `COSE_Sign1`, `EnclaveStation`, `DEC-AET-10`, `EF-5` |
| **Base Légale & Normative** | Norme IETF RFC 9052 §3 (gestion des identifiants kid et clés COSE) & Décision Kudoro DEC-AET-10. |
| **Terminal / Canvas Wireframe** | `PaxStation Station Pro • Gestionnaire d'Enclave & Chaîne de Confiance (EF-5)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> La clé de signature de la PaxStation est inscrite dans la liste de révocation ou le certificat X.509 de l'opérateur a expiré.

> [!TIP]
> **Postconditions Garanties :**
> Aucune signature non autorisée n'est générée dans EF-5 ; la chaîne de confiance cryptographique reste souveraine.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. L'opérateur funéraire prépare la phase de scellement COSE_Sign1 pour finaliser la personnalisation d'un lot de cartes.
2. Le moteur cryptographique de la station interroge la TrustList certifiée locale et l'enclave sécurisée HSM / StrongBox.
3. Découverte que l'empreinte kid de la clé est révoquée ou que le certificat opérateur a dépassé sa date de validité UTC.
4. Verrouillage immédiat du module de signature COSE_Sign1 : interdiction formelle d'émettre l'enveloppe signée EF-5.
5. Émission d'un rapport de blocage d'autorité et notification à l'administrateur réseau Le Pax Funèbre pour réapprovisionnement de clé.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `hsm_module` | **Enclave Cryptographique** | `text` | `StrongBox Hardware Enclave #STN-NAMUR-01` | - | `HSM Local` | ⭕ Optionnel |
| `kid_fingerprint` | **Empreinte kid de Clé** | `text` | `kid: 7f8a9b0c1d2e3f4a (SHA-256 16 premiers octets)` | - | `Identifiant Clé` | ⭕ Optionnel |
| `trustlist_status` | **Statut TrustList Souveraine** | `text` | `RÉVOQUÉE (Inscription sur la liste de révocation CRL-2026-09)` | - | `Révocation Alerte` | ⭕ Optionnel |
| `signing_lock_action` | **Action de Sécurité Enclave** | `select` | `Refus de Signature COSE_Sign1 & Blocage Session` | - | `Sécurité EF-5` | ✅ Requis |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_verify_trust_chain` | **Auditer la Chaîne de Confiance & Certificats** | `primary` | `idle` | 🔑 |
| `btn_request_key_renewal` | **Demander le Renouvellement de Clé d'Enclave** | `secondary` | `idle` | 🔄 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Verrouillage de Sécurité Cryptographique Actif
>
> **Badge de Conformité :** `TrustList Souveraine Conforme`
>
> **Détail Opérationnel :** La tentative de signature a été interceptée avec succès. Aucune clé obsolète ou révoquée ne peut sceller de carte.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_OPERATOR_KEY_REVOKED_OR_EXPIRED` |
| **Intitulé de l'Incident** | **Clé d'Enclave Révoquée ou Certificat d'Opérateur Expiré** |
| **Condition Déclenchante** | Correspondance de l'empreinte kid dans la liste des clés compromises ou date UTC postérieure à la fin de validité. |
| **Message d'Erreur UI** | *« Alerte de sécurité majeure : La clé de signature de cette PaxStation a été révoquée par l'autorité Le Pax Funèbre. Scellement interdit. »* |
| **Action Corrective Requise** | **Contacter immédiatement l'administrateur souverain pour révoquer l'ancienne clé et approvisionner une nouvelle clé dans l'enclave.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Station Pro • Gestionnaire d'Enclave & Chaîne de Confiance (EF-5)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Session d'Encodage Face à une Clé Invalidée | *En attente utilisateur* | L'enclave tente de charger la clé de scellement alors que celle-ci figure sur la liste de révocation. |
| **2** | **Déclenchement ⚡** | Détection de la Révocation & Interdiction de Scellement | `Clic sur 'Auditer la Chaîne de Confiance'` | Confrontation du kid avec la base souveraine et blocage matériel du sous-système de signature. |
| **3** | **Traitement ⚙️** | Verrouillage de la Station & Notification d'Alerte | `Progression : 100%` | Enregistrement de l'alerte d'intégrité et gel des opérations de gravure jusqu'à intervention administrateur. |
| **4** | **Scellement & Fin ✨** | Chaîne de Confiance Intègre & Procédure de Renouvellement | `Statut : success` | La sécurité cryptographique a joué son rôle de garde inviolable. Zéro carte frauduleuse émise. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-213 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Session d'Encodage Face à une Clé Invalidée
*L'enclave tente de charger la clé de scellement alors que celle-ci figure sur la liste de révocation.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStation • Moteur Cryptographique Enclave</span>
                                            <span class="wf-status-badge wf-badge-neutral">Clé à Contrôler</span>
                                          </div>
                                          <div class="wf-content-grid">
                                            <div class="wf-field-group">
                                              <label class="wf-label">Module de Scellement</label>
                                              <div class="wf-input-placeholder">StrongBox Enclave #STN-NAMUR-01 (kid: 7f8a9b0c...)</div>
                                            </div>
                                            <div class="wf-field-group">
                                              <label class="wf-label">Contrôle de Révocation</label>
                                              <div class="wf-input-placeholder">Vérification TrustList AeterniTrak en cours</div>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary">🔑 Auditer la Chaîne de Confiance & Certificats</button>
                                          </div>
                                        </div>
```

#### Phase 2 - Déclenchement : Détection de la Révocation & Interdiction de Scellement
*Confrontation du kid avec la base souveraine et blocage matériel du sous-système de signature.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStation • Audit TrustList</span>
                                            <span class="wf-status-badge wf-badge-trigger" style="background: rgba(239, 68, 68, 0.2); color: #fca5a5;">⚡ Clé Révoquée Détectée</span>
                                          </div>
                                          <div class="wf-trigger-card wf-radar-pulse" style="border-color: #ef4444;">
                                            <div class="wf-trigger-indicator" style="color: #fca5a5;">🚫 Clé kid 7f8a9b0c1d2e3f4a marquée RÉVOQUÉE dans CRL-2026-09</div>
                                            <div class="wf-subtext">Signature COSE_Sign1 bloquée • Partition EF-5 non altérée</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary wf-pulse-btn">Verrouillage de la session...</button>
                                          </div>
                                        </div>
```

#### Phase 3 - Traitement : Verrouillage de la Station & Notification d'Alerte
*Enregistrement de l'alerte d'intégrité et gel des opérations de gravure jusqu'à intervention administrateur.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStation • Sécurité Opérationnelle</span>
                                            <span class="wf-status-badge wf-badge-process">⚙️ Alerte Sécurité (100%)</span>
                                          </div>
                                          <div class="wf-console-log">
                                            <code>> [TRUST-LIST] Vérification de l'ancre racine Le Pax Funèbre : CONFORME</code><br>
                                            <code>> [REVOCATION-CHECK] kid 7f8a9b0c... MATCH sur liste des clés révoquées</code><br>
                                            <code>> [CRYPTO-BLOCK] Enclave StrongBox verrouillée en écriture de signature</code><br>
                                            <code>> [AUDIT-TRAIL] Rapport d'incident #SEC-REVOC-2026-04 émis vers le serveur d'audit</code>
                                          </div>
                                        </div>
```

#### Phase 4 - Fin de Cycle : Chaîne de Confiance Intègre & Procédure de Renouvellement
*La sécurité cryptographique a joué son rôle de garde inviolable. Zéro carte frauduleuse émise.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStation • Station Bloquée</span>
                                            <span class="wf-status-badge wf-badge-success" style="background: rgba(239, 68, 68, 0.2); color: #fca5a5;">🚫 Signature Désactivée</span>
                                          </div>
                                          <div class="wf-success-banner" style="border-color: rgba(239, 68, 68, 0.4);">
                                            <span class="wf-seal-icon">🛡️</span>
                                            <div>
                                              <strong>Intégrité de la Chaîne de Confiance Préservée</strong>
                                              <p class="wf-subtext">Signature refusée • Demande de réapprovisionnement de clé d'enclave transmise</p>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-sub">🔄 Contacter l'Administrateur pour Renouvellement</button>
                                          </div>
                                        </div>
```

</details>

---

<a id="uc-214"></a>
## UC-214 : Échec d'Impression Thermique/Laser & Procédure de Rebut Silicium (SCRAPPED)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-214` |
| **Catégorie Métier** | **Production Physique & Assurance Qualité** |
| **Acteur Principal** | Opérateur d'Atelier & Contrôleur Qualité |
| **Plateformes Cibles** | Poste Pro Dédié (macOS, Windows, Linux) |
| **Tags Clés** | `Impression`, `Rebut`, `SCRAPPED`, `Fargo`, `Laser`, `AuditTrail`, `EF-0` |
| **Base Légale & Normative** | Norme ISO/IEC 7810 (critères d'aspect et d'intégrité des cartes d'identification) & Protocole Qualité PaxFunèbre QA-PRO-04. |
| **Terminal / Canvas Wireframe** | `PaxStation Station Pro • Banc d'Assurance Qualité & Rebut Silicium (EF-0)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Incident survenu durant la phase de finition physique CR-80 (bourrage imprimante Fargo, surchauffe ruban or ou rayure laser).

> [!TIP]
> **Postconditions Garanties :**
> L'identifiant silicium de la carte détruite est blacklisté dans le registre de production ; zéro support non conforme ne sort d'atelier.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. L'imprimante thermique professionnelle Fargo signale une interruption de personnalisation physique de la carte.
2. L'opérateur examine le support : constat d'un défaut visuel rédhibitoire (bavure thermique, vernis or dégradé, micro-fissure).
3. La PaxStation engage la procédure d'assurance qualité formelle : mise au rebut immédiate du support.
4. Enregistrement de l'UID silicium (Tag 0x02 d'EF-0) dans le registre d'audit sous le statut définitif SCRAPPED.
5. Perforation physique de la puce à l'emporte-pièce sécurisé et allocation d'un nouveau support vierge d'atelier.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `scrapped_card_uid` | **Carte Silicium Concernée** | `text` | `ACOSJ-92K #04:88:99:AA:BB:CC:DD` | - | `UID Matériel` | ⭕ Optionnel |
| `fault_type` | **Type d'Incident Physique** | `select` | `Bourrage Imprimante Fargo • Surchauffe Ruban Or Satiné` | - | `Défaut d'Aspect` | ✅ Requis |
| `scrapped_audit_status` | **Statut dans l'Audit Trail** | `text` | `SCRAPPED (Mis au rebut • UID révoqué définitivement)` | - | `Blacklist` | ⭕ Optionnel |
| `destruction_protocol` | **Protocole de Destruction** | `text` | `Perforation physique de l'antenne & puce neutralisée` | - | `Obligatoire` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_declare_scrapped` | **Déclarer Carte au Rebut (SCRAPPED) & Neutraliser** | `primary` | `idle` | 🗑️ |
| `btn_allocate_new_card` | **Allouer une Nouvelle Carte Vierge** | `secondary` | `idle` | ✨ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Mise au Rebut Validée & Traçabilité Silicium Conforme
>
> **Badge de Conformité :** `Audit SCRAPPED Validé`
>
> **Détail Opérationnel :** UID blacklisté dans l'audit trail de production. Procédure de destruction physique consignée selon QA-PRO-04.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_THERMAL_PRINTING_HARDWARE_FAULT` |
| **Intitulé de l'Incident** | **Incident Matériel d'Impression ou Défaut d'Aspect Physique** |
| **Condition Déclenchante** | Bourrage de carte, rupture du ruban thermique ou dégradation mécanique du support durant la personnalisation. |
| **Message d'Erreur UI** | *« Défaut qualité bloquant : La carte présente des altérations physiques incompatibles avec la dignité mémorielle Le Pax Funèbre. »* |
| **Action Corrective Requise** | **Déclarer le support sous le statut SCRAPPED, perforer la carte et recommencer sur un support neuf.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Station Pro • Banc d'Assurance Qualité & Rebut Silicium (EF-0)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Signalement d'Anomalie Matérielle sur l'Imprimante | *En attente utilisateur* | L'imprimante signale une erreur matérielle durant le dépôt du ruban thermique or satiné. |
| **2** | **Déclenchement ⚡** | Déclenchement de la Procédure de Rebut Officielle | `Clic sur 'Déclarer Carte au Rebut'` | Enregistrement de l'incident et marquage de l'UID matériel dans le registre d'atelier. |
| **3** | **Traitement ⚙️** | Perforation Silicium & Archivage de Sécurité | `Progression : 100%` | Neutralisation physique de la puce et décrémentation des stocks d'atelier avec justification. |
| **4** | **Scellement & Fin ✨** | Support Rebuté & Allocation d'un Nouveau Support | `Statut : success` | Exigence qualité respectée. Le client final ne recevra qu'un objet physique irréprochable. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-214 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Signalement d'Anomalie Matérielle sur l'Imprimante
*L'imprimante signale une erreur matérielle durant le dépôt du ruban thermique or satiné.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStation • Contrôle Qualité Impression</span>
                                            <span class="wf-status-badge wf-badge-neutral">Défaut Détecté</span>
                                          </div>
                                          <div class="wf-device-status-box" style="border-color: #f59e0b;">
                                            <span class="wf-qa-icon">⚠️</span>
                                            <div><strong>Incident d'Impression Thermique Signalé</strong></div>
                                            <div class="wf-subtext">Ruban or surchauffé • Support physique altéré non livrable</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary">🗑️ Déclarer Carte au Rebut (SCRAPPED) & Neutraliser</button>
                                          </div>
                                        </div>
```

#### Phase 2 - Déclenchement : Déclenchement de la Procédure de Rebut Officielle
*Enregistrement de l'incident et marquage de l'UID matériel dans le registre d'atelier.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStation • Journalisation Rebut</span>
                                            <span class="wf-status-badge wf-badge-trigger">⚡ Traitement SCRAPPED</span>
                                          </div>
                                          <div class="wf-trigger-card wf-radar-pulse">
                                            <div class="wf-trigger-indicator">✓ UID #04:88:99:AA:BB:CC:DD classé SCRAPPED</div>
                                            <div class="wf-subtext">Blacklistage dans le registre d'atelier et génération du bon de destruction</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary wf-pulse-btn">Consignation au registre d'audit...</button>
                                          </div>
                                        </div>
```

#### Phase 3 - Traitement : Perforation Silicium & Archivage de Sécurité
*Neutralisation physique de la puce et décrémentation des stocks d'atelier avec justification.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStation • Registre Qualité</span>
                                            <span class="wf-status-badge wf-badge-process">⚙️ Rebut Scellé (100%)</span>
                                          </div>
                                          <div class="wf-console-log">
                                            <code>> [QA-LOG] Rapport de rebut #REB-2026-019 archivé</code><br>
                                            <code>> [UID-REVOC] Identifiant matériel révoqué pour toute gravure ultérieure</code><br>
                                            <code>> [PHYSICAL-DESTRUCT] Confirmation de perforation par l'opérateur</code><br>
                                            <code>> [STOCK-CONTROL] Demande d'un nouveau support vierge ACOSJ 92 Ko validée</code>
                                          </div>
                                        </div>
```

#### Phase 4 - Fin de Cycle : Support Rebuté & Allocation d'un Nouveau Support
*Exigence qualité respectée. Le client final ne recevra qu'un objet physique irréprochable.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStation • Nouveau Cycle Prêt</span>
                                            <span class="wf-status-badge wf-badge-success">✨ Qualité Garantie</span>
                                          </div>
                                          <div class="wf-success-banner">
                                            <span class="wf-seal-icon">🏆</span>
                                            <div>
                                              <strong>Procédure de Rebut Exécutée avec Rigueur</strong>
                                              <p class="wf-subtext">Carte défectueuse détruite • Nouveau support vierge prêt pour la réimpression</p>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-gold">✨ Allouer une Nouvelle Carte Vierge et Relancer</button>
                                          </div>
                                        </div>
```

</details>

---

<a id="uc-215"></a>
## UC-215 : Polling Détection Lecteur USB CCID & Événements PnP Carte Présente

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-215` |
| **Catégorie Métier** | **Silicium & Détection** |
| **Acteur Principal** | Opérateur d'Atelier |
| **Plateformes Cibles** | Poste Pro Dédié (macOS, Windows, Linux) |
| **Tags Clés** | `CCID`, `PnP`, `USB`, `PCSC`, `Detection`, `Polling`, `LecteurNFC` |
| **Base Légale & Normative** | Spécification USB CCID (Integrated Circuit Card Interface Devices) & Spécifications PC/SC Workgroup Part 2 & 3. |
| **Terminal / Canvas Wireframe** | `PaxStation Pro • Détection Matérielle CCID & Événements PC/SC PnP` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> La PaxStation est active sur le poste pro ; le lecteur sans contact USB CCID est branché.

> [!TIP]
> **Postconditions Garanties :**
> Le lecteur CCID est synchronisé et la présence physique de la carte sans contact est certifiée.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Initialisation du contexte de ressources PC/SC par le démon matériel (SCardEstablishContext).
2. Boucle de polling asynchrone écoutant les changements d'état du lecteur (SCardGetStatusChange).
3. Détection physique de l'approche d'un support sans contact dans le champ électromagnétique 13.56 MHz.
4. Notification d'événement matériel Plug & Play : passage à l'état SCARD_STATE_PRESENT.
5. Verrouillage du canal d'interrogation pour empêcher tout décrochage radiofréquence durant l'amorçage.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `ccid_reader_model` | **Lecteur USB Détecté** | `text` | `Identiv uTrust 3700 F CL Reader [PCSC] (Bus 001 Dev 004)` | - | `CCID USB 2.0` | ⭕ Optionnel |
| `rf_field_state` | **État du Champ Radiofréquence** | `text` | `Actif • 13.56 MHz • Modulation ISO 14443 Type A activée` | - | `RF Émise` | ⭕ Optionnel |
| `pcsc_event_status` | **Événement Matériel PnP** | `select` | `SCARD_STATE_PRESENT (Support Détecté dans le Champ)` | - | `PC/SC Événement` | ✅ Requis |
| `usb_power_rail` | **Alimentation Bus USB** | `text` | `5.02 V • 120 mA (Tension Stable & Bruit < 15 mV)` | - | `Alimentation OK` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_poll_pcsc` | **Interroger l'État PC/SC Immédiat** | `primary` | `idle` | 🔌 |
| `btn_reset_ccid_bus` | **Réinitialiser Bus CCID** | `secondary` | `idle` | 🔄 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Lecteur USB CCID Synchronisé & Carte Détectée
>
> **Badge de Conformité :** `SCARD_STATE_PRESENT`
>
> **Détail Opérationnel :** Support sans contact positionné dans le champ RF. Prêt pour la séquence d'Answer to Select (ATS).

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_CCID_READER_NOT_FOUND` |
| **Intitulé de l'Incident** | **Aucun Lecteur de Carte Détecté sur le Bus USB** |
| **Condition Déclenchante** | Périphérique CCID déconnecté ou gestionnaire pcscd indisponible. |
| **Message d'Erreur UI** | *« Échec matériel : Aucun lecteur de carte sans contact compatible PC/SC n'est actif sur le système. »* |
| **Action Corrective Requise** | **Brancher le lecteur sur un port USB direct et relancer le démon PC/SC.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Pro • Détection Matérielle CCID & Événements PC/SC PnP**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Démon PC/SC en Écoute & Slot Lecteur Vide | *En attente utilisateur* | Le lecteur sans contact est prêt et alimenté, en attente de la présentation d'une carte. |
| **2** | **Déclenchement ⚡** | Détection Approche Carte dans le Champ 13.56 MHz | `Approche physique d'une carte ACOSJ sur l'antenne du lecteur` | Couplage inductif RF détecté et transition d'état PC/SC instantanée. |
| **3** | **Traitement ⚙️** | Stabilisation Alimentation RF & Verrouillage Canal | `Progression : 90%` | Mesure de la stabilité du signal et attribution du handle matériel PC/SC sécurisé. |
| **4** | **Scellement & Fin ✨** | Carte Détectée & Canal PC/SC Initialisé | `Statut : success` | Le support physique est solidement connecté et prêt pour la négociation de protocole. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-215 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Démon PC/SC en Écoute & Slot Lecteur Vide
*Le lecteur sans contact est prêt et alimenté, en attente de la présentation d'une carte.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Gestionnaire PC/SC USB CCID</span>
                        <span class="wf-status-badge wf-badge-neutral">En Attente de Carte (Champ 13.56 MHz Prêt)</span>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-field-group">
                          <label class="wf-label">Lecteur Assigné</label>
                          <div class="wf-input-placeholder">Identiv uTrust 3700 F CL Reader [PCSC]</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Statut PnP</label>
                          <div class="wf-input-placeholder">SCARD_STATE_EMPTY</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔌 Interroger l'État PC/SC Immédiat</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Détection Approche Carte dans le Champ 13.56 MHz
*Couplage inductif RF détecté et transition d'état PC/SC instantanée.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Détecteur Matériel</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Carte Détectée dans le Champ</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Événement SCARD_STATE_PRESENT déclenché sur le lecteur #0</div>
                        <div class="wf-subtext">Couplage RF stabilisé • Porteuse 13.56 MHz modulée</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Initialisation du lien sans contact...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Stabilisation Alimentation RF & Verrouillage Canal
*Mesure de la stabilité du signal et attribution du handle matériel PC/SC sécurisé.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Contrôleur Bus CCID</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Connexion PC/SC (90%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 90%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [PCSC-DAEMON] SCardConnect(SCARD_SHARE_SHARED, SCARD_PROTOCOL_T1) : OK</code><br>
                        <code>> [USB-CCID] Tension bus 5.02V stable, consommation 120 mA</code><br>
                        <code>> [RF-FIELD] Porteuse ISO 14443 Type A synchronisée</code><br>
                        <code>> [CHANNEL-LOCK] Canal exclusif réservé pour la session de gravure</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Carte Détectée & Canal PC/SC Initialisé
*Le support physique est solidement connecté et prêt pour la négociation de protocole.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Prêt pour Transaction</span>
                        <span class="wf-status-badge wf-badge-success">✨ Carte Connectée</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🎴</span>
                        <div>
                          <strong>Support Sans Contact Détecté & Stabilisé (SCARD_STATE_PRESENT)</strong>
                          <p class="wf-subtext">Lecteur Identiv uTrust 3700 F • Prêt pour la lecture ATS / ATR</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Lancer l'Identification Matérielle ATS →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-216"></a>
## UC-216 : Analyse Trame Réponse ATR / ATS & Identification ISO 14443-4 Type A

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-216` |
| **Catégorie Métier** | **Silicium & Détection** |
| **Acteur Principal** | Opérateur d'Atelier & Système Automatisé |
| **Plateformes Cibles** | Poste Pro Dédié (macOS, Windows, Linux) |
| **Tags Clés** | `ATS`, `ATR`, `ISO14443`, `TypeA`, `T=CL`, `ACOSJ`, `Identification` |
| **Base Légale & Normative** | Norme internationale ISO/IEC 14443-4 (Cartes d'identification sans contact - Protocole de transmission T=CL). |
| **Terminal / Canvas Wireframe** | `PaxStation Pro • Décodage ATS / ATR & Identification Matérielle ISO 14443-4` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Une carte sans contact a été positionnée sur le lecteur (UC-215).

> [!TIP]
> **Postconditions Garanties :**
> La puce est formellement identifiée comme un composant ACOSJ 92 Ko conforme aux spécifications d'encodage.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Envoi de la commande d'activation RATS (Request for Answer to Select) à la puce sans contact.
2. Capture de la trame de réponse ATS brute retournée par le composant silicium.
3. Décodage normalisé des octets d'en-tête : longueur TL, octet de format T0, octets d'interface TA/TB/TC et octets historiques.
4. Validation du protocole ISO 14443-4 Type A (T=CL) et vérification de la signature du contrôleur ACOSJ 92 Ko.
5. Contrôle de l'UID matériel (7 octets) contre le registre de sécurité d'atelier.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `ats_hex_payload` | **Trame ATS Brute (Hexadécimal)** | `text` | `0F 78 80 82 02 41 43 4F 53 4A 39 32 4B 90 00` | - | `ATS Réponse` | ⭕ Optionnel |
| `decoded_protocol` | **Protocole de Transmission Décodé** | `text` | `ISO/IEC 14443-4 Type A (T=CL Compliant)` | - | `Protocole` | ⭕ Optionnel |
| `silicon_chipset_id` | **Composant Silicium Identifié** | `select` | `ACS ACOSJ 92 Ko EEPROM • Microcontrôleur Sécurisé 32-bit` | - | `Homologué ACOSJ` | ✅ Requis |
| `rfid_hardware_uid` | **UID Matériel Unique (7 octets)** | `text` | `04:88:99:AA:BB:CC:DD (NXP/ACS Genuine)` | - | `UID Unique` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_decode_ats_frame` | **Analyser la Trame ATS / ATR** | `primary` | `idle` | 🔬 |
| `btn_verify_uid_whitelist` | **Vérifier UID sur Liste Blanche** | `secondary` | `idle` | 🛡️ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Trame ATS Conforme & Puce ACOSJ 92 Ko Identifiée
>
> **Badge de Conformité :** `ISO 14443-4 T=CL`
>
> **Détail Opérationnel :** Le composant est un support officiel ACOSJ 92 Ko certifié. Protocole de haut niveau initialisé.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_INVALID_ATS_SIGNATURE` |
| **Intitulé de l'Incident** | **Trame ATS Invalide ou Support Non Homologué** |
| **Condition Déclenchante** | La trame reçue ne correspond pas à la signature matérielle de l'ACOSJ ou présente une altération RF. |
| **Message d'Erreur UI** | *« Rejet de composant : Support incompatible détecté (Mifare non sécurisé ou tag non homologué). »* |
| **Action Corrective Requise** | **Remplacer la carte par un support sécurisé ACOSJ 92 Ko issu du stock officiel d'atelier.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Pro • Décodage ATS / ATR & Identification Matérielle ISO 14443-4**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Carte Alimentée en Attente de Commande RATS | *En attente utilisateur* | La carte est sous tension radiofréquence, prête pour la négociation de protocole ATS. |
| **2** | **Déclenchement ⚡** | Réception & Capture de la Trame Réponse ATS | `Émission commande RATS (Request for Answer to Select)` | La puce renvoie ses 15 octets ATS détaillant ses capacités mémoires et débits. |
| **3** | **Traitement ⚙️** | Décodage des Octets T0/TA/TB/TC & Identification Puce | `Progression : 95%` | Validation du protocole ISO 14443-4 Type A et contrôle de conformité silicium. |
| **4** | **Scellement & Fin ✨** | Protocole ISO 14443-4 Type A Certifié & UID Validé | `Statut : success` | Le composant est un support officiel authentique, prêt pour l'ouverture de l'applet. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-216 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Carte Alimentée en Attente de Commande RATS
*La carte est sous tension radiofréquence, prête pour la négociation de protocole ATS.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Analyseur Protocolaire ISO 14443</span>
                        <span class="wf-status-badge wf-badge-neutral">Prêt pour RATS</span>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-field-group">
                          <label class="wf-label">UID Matériel Détecté</label>
                          <div class="wf-input-placeholder">04:88:99:AA:BB:CC:DD (7 octets)</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Trame ATS</label>
                          <div class="wf-input-placeholder">Non interrogée</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔬 Analyser la Trame ATS / ATR</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Réception & Capture de la Trame Réponse ATS
*La puce renvoie ses 15 octets ATS détaillant ses capacités mémoires et débits.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Réception ATS</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Réponse ATS 15 Octets Reçue</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Trame ATS : 0F 78 80 82 02 41 43 4F 53 4A 39 32 4B 90 00</div>
                        <div class="wf-subtext">Signature ASCII détectée dans les octets historiques : 'ACOSJ92K'</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Décodage des paramètres T=CL...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Décodage des Octets T0/TA/TB/TC & Identification Puce
*Validation du protocole ISO 14443-4 Type A et contrôle de conformité silicium.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Moteur d'Identification Silicium</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Analyse Signature (95%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 95%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [ATS-DECODER] TL = 0x0F (15 octets) • T0 = 0x78 (TA, TB, TC présents)</code><br>
                        <code>> [SPEED-CAPABILITY] TA(1) = 0x80 : Support des vitesses jusqu'à 848 kbps</code><br>
                        <code>> [CHIPSET-MATCH] Puce homologuée ACOSJ 92 Ko EEPROM (ACS Smart Cards)</code><br>
                        <code>> [SECURITY-CHECK] UID matériel validé dans l'inventaire d'atelier</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Protocole ISO 14443-4 Type A Certifié & UID Validé
*Le composant est un support officiel authentique, prêt pour l'ouverture de l'applet.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Silicium Certifié</span>
                        <span class="wf-status-badge wf-badge-success">✨ ACOSJ 92 Ko Homologué</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🏆</span>
                        <div>
                          <strong>Puce ACOSJ 92 Ko Officielle Reconnue (T=CL Type A)</strong>
                          <p class="wf-subtext">UID #04:88:99:AA:BB:CC:DD • Composant certifié pour gravure funéraire</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Sélectionner l'Applet AeterniCore (SELECT AID) →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-217"></a>
## UC-217 : Sélection de l'Applet par Commande APDU SELECT AID & Validation SW 0x9000

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-217` |
| **Catégorie Métier** | **Système de Fichiers Puce** |
| **Acteur Principal** | Système Automatisé PaxStation |
| **Plateformes Cibles** | Poste Pro Dédié (macOS, Windows, Linux) |
| **Tags Clés** | `APDU`, `SELECT`, `AID`, `SW9000`, `AppletJavaCard`, `AeterniCore` |
| **Base Légale & Normative** | Norme ISO/IEC 7816-4 (Organisation, sécurité et commandes pour les échanges) & Spécifications Java Card 3.0.5. |
| **Terminal / Canvas Wireframe** | `PaxStation Pro • Sélection d'Applet JavaCard AeterniCore (ISO 7816-4 SELECT AID)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Le protocole de transmission T=CL est actif sur la puce (UC-216).

> [!TIP]
> **Postconditions Garanties :**
> L'applet AeterniCore est active en mémoire vive de la puce, prête pour les opérations sur les partitions EF.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Forge de la commande APDU de sélection applicative selon ISO/IEC 7816-4 : CLA 0x00, INS 0xA4, P1 0x04, P2 0x00.
2. Injection de l'AID souverain de l'applet AeterniCore : `A0 00 00 08 47 01 02` (7 octets).
3. Transmission de la trame via le canal logique 0 du protocole T=CL.
4. Réception et vérification du Status Word (mot d'état de retour SW1-SW2).
5. Confirmation de l'état `0x9000` (Succès normal) et activation de la session de commande sécurisée.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `apdu_select_payload` | **Commande APDU SELECT AID** | `text` | `00 A4 04 00 07 A0 00 00 08 47 01 02 00` | - | `APDU ISO 7816` | ⭕ Optionnel |
| `target_aid_string` | **Identifiant d'Application (AID)** | `text` | `A0000008470102 (AeterniCore Applet V1.0)` | - | `AID Souverain` | ⭕ Optionnel |
| `status_word_received` | **Mot d'État Retourné (SW)** | `select` | `0x9000 (Succès Normal • Applet Sélectionnée)` | - | `SW 0x9000` | ✅ Requis |
| `jc_vm_status` | **État Machine Virtuelle Silicium** | `text` | `Java Card VM Prête • Contexte d'exécution isolé` | - | `Sécurité Silicium` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_send_select_aid` | **Transmettre APDU SELECT AID** | `primary` | `idle` | 🎯 |
| `btn_read_applet_lifecycle` | **Vérifier Cycle de Vie Applet** | `secondary` | `idle` | 📋 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Applet AeterniCore Sélectionnée avec Succès (SW 0x9000)
>
> **Badge de Conformité :** `SW 0x9000 Validé`
>
> **Détail Opérationnel :** L'applet est active et réceptive. Les fichiers élémentaires EF-0 à EF-5 sont accessibles pour transaction.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_APDU_APPLET_NOT_FOUND` |
| **Intitulé de l'Incident** | **Échec Sélection AID (SW 0x6A82 - File / Application Not Found)** |
| **Condition Déclenchante** | L'AID demandé n'est pas instancié sur le support ou a été corrompu lors de la phase usine. |
| **Message d'Erreur UI** | *« Erreur logicielle silicium : L'applet A0000008470102 est introuvable sur cette carte. »* |
| **Action Corrective Requise** | **Charger le paquet CAP AeterniCore via le script d'initialisation GlobalPlatform d'atelier.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Pro • Sélection d'Applet JavaCard AeterniCore (ISO 7816-4 SELECT AID)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Puce Reconnue, Applet Non Encore Sélectionnée | *En attente utilisateur* | Le canal T=CL est ouvert. L'APDU SELECT AID attend d'être transmise pour activer l'applet. |
| **2** | **Déclenchement ⚡** | Émission de l'APDU SELECT AID (A0 00 00 08 47 01 02) | `Envoi APDU 00 A4 04 00 07 A0000008470102 00` | Bascule du contexte d'exécution de la machine virtuelle JavaCard vers l'instance AeterniCore. |
| **3** | **Traitement ⚙️** | Activation Contexte JavaCard & Analyse Code SW 0x9000 | `Progression : 96%` | Validation du code de succès 0x9000 et vérification des permissions de session. |
| **4** | **Scellement & Fin ✨** | Applet AeterniCore Active sur Canal 0 | `Statut : success` | La communication applicative est ouverte. Les commandes de lecture/écriture de fichiers sont prêtes. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-217 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Puce Reconnue, Applet Non Encore Sélectionnée
*Le canal T=CL est ouvert. L'APDU SELECT AID attend d'être transmise pour activer l'applet.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Gestionnaire d'Applets Silicium</span>
                        <span class="wf-status-badge wf-badge-neutral">Prêt pour SELECT AID</span>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-field-group">
                          <label class="wf-label">AID Cible</label>
                          <div class="wf-input-placeholder">A0000008470102 (AeterniCore)</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Canal Logique</label>
                          <div class="wf-input-placeholder">Canal de Base #0 (T=CL)</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🎯 Transmettre APDU SELECT AID</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Émission de l'APDU SELECT AID (A0 00 00 08 47 01 02)
*Bascule du contexte d'exécution de la machine virtuelle JavaCard vers l'instance AeterniCore.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Dialogue APDU ISO 7816-4</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ APDU SELECT Transmise</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Envoi : 00 A4 04 00 07 A0 00 00 08 47 01 02 00</div>
                        <div class="wf-subtext">Activation de l'applet sur le microcontrôleur ACOSJ</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Réception du Status Word...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Activation Contexte JavaCard & Analyse Code SW 0x9000
*Validation du code de succès 0x9000 et vérification des permissions de session.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Décodeur Status Word</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Analyse SW (96%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 96%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [APDU-RX] Status Word retourné : 0x9000 (Command successfully executed)</code><br>
                        <code>> [JC-APPLET] Instance AeterniCore v1.0 initialisée en RAM</code><br>
                        <code>> [SECURITY-DOMAIN] Droits de lecture/écriture débloqués pour session atelier</code><br>
                        <code>> [EF-MAPPING] 6 partitions élémentaires EF-0 à EF-5 prêtes pour transaction</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Applet AeterniCore Active sur Canal 0
*La communication applicative est ouverte. Les commandes de lecture/écriture de fichiers sont prêtes.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Applet Active</span>
                        <span class="wf-status-badge wf-badge-success">✨ SW 0x9000 Normal Execution</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🎯</span>
                        <div>
                          <strong>Applet AeterniCore Sélectionnée avec Succès</strong>
                          <p class="wf-subtext">Canal logique #0 prêt • Prêt pour l'inspection de l'en-tête EF-0</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Inspecter l'En-tête Matériel EF-0 →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-218"></a>
## UC-218 : Lecture En-tête EF-0 Silicium & Inspection des Compteurs Monotones

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-218` |
| **Catégorie Métier** | **Système de Fichiers Puce** |
| **Acteur Principal** | Système Automatisé & Opérateur d'Atelier |
| **Plateformes Cibles** | Poste Pro Dédié (macOS, Windows, Linux) |
| **Tags Clés** | `EF-0`, `CompteurMonotone`, `AntiRejeu`, `EnTete`, `UID`, `Silicium` |
| **Base Légale & Normative** | Spécification technique AeterniTrak EF-0 (Conteneur racine d'amorçage) & ISO/IEC 7816-4. |
| **Terminal / Canvas Wireframe** | `PaxStation Pro • Inspection En-tête Matériel EF-0 & Compteurs Monotones` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> L'applet AeterniCore a été sélectionnée avec succès (UC-217).

> [!TIP]
> **Postconditions Garanties :**
> L'en-tête matériel et le compteur monotone sont validés ; la carte est déclarée intègre et non altérée.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Envoi de la commande APDU de lecture transparente du fichier EF-0 (`00 B0 00 00 40`).
2. Décodage de la structure TLV de l'en-tête matériel : Tag 0x01 (version schéma), Tag 0x02 (UID matériel), Tag 0x03 (verrous d'accès).
3. Extraction de la valeur du compteur monotone non-réversible géré par le silicium.
4. Vérification que la valeur du compteur d'écritures correspond à un support vierge d'usine (0 ou 1 cycle de test).
5. Enregistrement de l'état initial dans le journal d'audit trail d'atelier pour la traçabilité de production.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `target_ef_file` | **Fichier Élémentaire Ciblé** | `text` | `EF-0 (Fichier Racine d'Amorçage & Sécurité)` | - | `EF-0 Silicium` | ⭕ Optionnel |
| `monotone_counter_value` | **Compteur Monotone d'Écriture** | `text` | `0x00000001 (1 cycle usine • Vierge pour gravure)` | - | `Anti-Rejeu` | ⭕ Optionnel |
| `write_lock_status` | **État du Verrou d'Écriture Silicium** | `select` | `UNLOCKED (Prêt pour Gravure Définitive)` | - | `Verrou Ouvert` | ✅ Requis |
| `metadata_schema_rev` | **Version du Schéma Métadonnées** | `text` | `AeterniCore v1.0 • Rétrocompatibilité garantie` | - | `Schéma 1.0` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_read_ef0_header` | **Lire En-tête EF-0** | `primary` | `idle` | 📖 |
| `btn_audit_anti_replay` | **Auditer Compteur Anti-Rejeu** | `secondary` | `idle` | 🛡️ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** En-tête EF-0 Valide & Compteur Monotone Conforme
>
> **Badge de Conformité :** `EF-0 Intègre`
>
> **Détail Opérationnel :** Support vierge de tout enregistrement pirate. Compteur matériel cohérent, prêt pour l'injection des données.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_MONOTONE_COUNTER_ABNORMAL` |
| **Intitulé de l'Incident** | **Valeur Anormale du Compteur Monotone Silicium** |
| **Condition Déclenchante** | Le compteur présente une valeur anormalement élevée ou incohérente, trahissant une réutilisation ou tentative de clonage. |
| **Message d'Erreur UI** | *« Alerte sécurité anti-tamper : Le compteur monotone matériel indique que cette carte a déjà été modifiée. »* |
| **Action Corrective Requise** | **Mettre la carte en quarantaine immédiate et la soumettre au contrôle qualité niveau 3.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Pro • Inspection En-tête Matériel EF-0 & Compteurs Monotones**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Applet Sélectionnée, En-tête EF-0 Non Audité | *En attente utilisateur* | La carte est prête pour la lecture de son fichier racine de configuration et de sécurité. |
| **2** | **Déclenchement ⚡** | Envoi de la Commande READ BINARY sur EF-0 | `Émission APDU 00 B0 00 00 40` | Extraction des 64 premiers octets structurés de la partition racine. |
| **3** | **Traitement ⚙️** | Contrôle Compteur Monotone (Anti-Rejeu) & Droits d'Accès | `Progression : 97%` | Vérification mathématique de non-altération du composant et de la virginité du support. |
| **4** | **Scellement & Fin ✨** | En-tête EF-0 Homologué & Silicium Vierge Confirmé | `Statut : success` | La puce est formellement déclarée vierge, intègre et prête pour recevoir la gravure. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-218 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Applet Sélectionnée, En-tête EF-0 Non Audité
*La carte est prête pour la lecture de son fichier racine de configuration et de sécurité.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Explorateur Silicium EF-0</span>
                        <span class="wf-status-badge wf-badge-neutral">Prêt pour Lecture EF-0</span>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-field-group">
                          <label class="wf-label">Cible Silicium</label>
                          <div class="wf-input-placeholder">EF-0 (Racine & Monotones)</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Commande</label>
                          <div class="wf-input-placeholder">READ BINARY 00 B0 00 00 40</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">📖 Lire En-tête EF-0</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Envoi de la Commande READ BINARY sur EF-0
*Extraction des 64 premiers octets structurés de la partition racine.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Transaction Silicium EF-0</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ 64 Octets Extraits</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ En-tête TLV extrait : Tag 0x01 Schema 1.0 • Tag 0x02 UID • Tag 0x03 LockFlag 0x00</div>
                        <div class="wf-subtext">Compteur monotone d'écritures : 0x00000001 (1 cycle usine)</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Contrôle anti-tamper en cours...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Contrôle Compteur Monotone (Anti-Rejeu) & Droits d'Accès
*Vérification mathématique de non-altération du composant et de la virginité du support.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Auditeur de Sécurité Silicium</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Contrôle Anti-Rejeu (97%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 97%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [MONOTONE-CHECK] Compteur matériel = 1 (Conforme carte neuve sortie usine)</code><br>
                        <code>> [LOCK-FLAG] État courant : UNLOCKED (Écriture autorisée)</code><br>
                        <code>> [ANTI-CLONING] Signature interne EEPROM conforme</code><br>
                        <code>> [AUDIT-TRAIL] Enregistrement du hash EF-0 dans le registre atelier</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : En-tête EF-0 Homologué & Silicium Vierge Confirmé
*La puce est formellement déclarée vierge, intègre et prête pour recevoir la gravure.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • EF-0 Validé</span>
                        <span class="wf-status-badge wf-badge-success">✨ Support Vierge Certifié</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🛡️</span>
                        <div>
                          <strong>En-tête Matériel EF-0 Validé & Compteur Monotone Conforme</strong>
                          <p class="wf-subtext">Carte neuve certifiée • Zéro tentative de rejeu • Prêt pour le diagnostic d'usure</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Lancer le Diagnostic d'Usure EEPROM →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-219"></a>
## UC-219 : Diagnostic d'Usure EEPROM & Cartographie des Blocs d'Écriture

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-219` |
| **Catégorie Métier** | **Résilience Matérielle & Silicium** |
| **Acteur Principal** | Contrôleur Qualité Silicium |
| **Plateformes Cibles** | Poste Pro Dédié (macOS, Windows, Linux) |
| **Tags Clés** | `EEPROM`, `Endurance`, `Diagnostic`, `SanteSilicium`, `WearLeveling`, `JEDEC` |
| **Base Légale & Normative** | Norme JEDEC JESD22-A117 (Endurance et rétention de données pour mémoires non volatiles EEPROM). |
| **Terminal / Canvas Wireframe** | `PaxStation Pro • Diagnostic d'Usure EEPROM & Cartographie Silicium (JEDEC JESD22)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> La carte est alimentée et les canaux de diagnostic usine sont ouverts.

> [!TIP]
> **Postconditions Garanties :**
> La matrice EEPROM est certifiée à 100% de santé, garantissant une pérennité intergénérationnelle.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Exécution d'une routine de diagnostic matériel non destructive sur l'ensemble de la matrice mémoire non-volatile.
2. Lecture des registres internes d'endurance EEPROM et mesure des temps de charge de programmation de grille.
3. Analyse de la table d'allocation de wear-leveling : détection d'éventuels blocs dégradés ou réalloués.
4. Calcul de l'indice de santé matériel global (Health Index) selon la norme d'endurance JEDEC JESD22.
5. Délivrance de la certification de longévité garantissant une conservation des données sur plus de 25 ans à 55°C.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `eeprom_cycles_count` | **Cycles d'Écriture Consommés** | `text` | `3 cycles / 500 000 garantis (0.0006% d'usure)` | - | `Endurance` | ⭕ Optionnel |
| `bad_blocks_map` | **Cartographie des Blocs Défectueux** | `text` | `0 bloc défectueux • 100% cellules fonctionnelles` | - | `Intégrité Blocs` | ⭕ Optionnel |
| `data_retention_estimate` | **Estimation Rétention de Données** | `text` | `> 25 ans garanti à 55°C (Spécification ACOSJ)` | - | `Pérennité` | ⭕ Optionnel |
| `silicon_health_score` | **Indice Global de Santé Silicium** | `select` | `INDICE DE SANTÉ 100.0% (ÉTAT PARFAIT ATELIER)` | - | `JEDEC 100%` | ✅ Requis |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_run_eeprom_diagnostic` | **Lancer le Diagnostic d'Usure EEPROM** | `primary` | `idle` | 🩺 |
| `btn_export_longevity_cert` | **Générer Certificat de Longévité** | `secondary` | `idle` | 📜 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Diagnostic EEPROM Réussi : Santé Matérielle Certifiée 100%
>
> **Badge de Conformité :** `JEDEC JESD22 Validé`
>
> **Détail Opérationnel :** Zéro bloc défaillant. La rétention des données mémorielles et directives est garantie pour le siècle à venir.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_EEPROM_WEAR_LIMIT_REACHED` |
| **Intitulé de l'Incident** | **Usure Prématurée ou Cellules EEPROM Altérées** |
| **Condition Déclenchante** | La tension de claquage ou le temps de programmation d'un secteur dépasse les tolérances usine. |
| **Message d'Erreur UI** | *« Défaut silicium critique : La matrice EEPROM présente une anomalie de rétention. »* |
| **Action Corrective Requise** | **Mettre le support au rebut (statut SCRAPPED) et prélever un nouveau support neuf.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Pro • Diagnostic d'Usure EEPROM & Cartographie Silicium (JEDEC JESD22)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Silicium Connecté Prêt pour Diagnostic d'Endurance | *En attente utilisateur* | Le banc d'essai matériel est armé pour ausculter l'état de santé de la matrice EEPROM 92 Ko. |
| **2** | **Déclenchement ⚡** | Lancement du Banc de Test Matériel EEPROM | `Clic sur 'Lancer le Diagnostic d'Usure EEPROM'` | Sondage des cellules et vérification des registres de charge de la pompe à haute tension. |
| **3** | **Traitement ⚙️** | Audit Blocs Défectueux & Calcul Health Index (JESD22) | `Progression : 98%` | Analyse statistique de l'endurance et vérification de la garantie constructeur de rétention. |
| **4** | **Scellement & Fin ✨** | Matrice EEPROM 100% Saine & Rétention 25 Ans Certifiée | `Statut : success` | La puce offre toutes les garanties physiques pour conserver les mémoires de manière pérenne. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-219 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Silicium Connecté Prêt pour Diagnostic d'Endurance
*Le banc d'essai matériel est armé pour ausculter l'état de santé de la matrice EEPROM 92 Ko.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Banc d'Endurance Matériel</span>
                        <span class="wf-status-badge wf-badge-neutral">Prêt pour Diagnostic EEPROM</span>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-field-group">
                          <label class="wf-label">Matrice Mémoire</label>
                          <div class="wf-input-placeholder">EEPROM 92 Ko (ACS ACOSJ)</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Norme de Référence</label>
                          <div class="wf-input-placeholder">JEDEC JESD22-A117</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🩺 Lancer le Diagnostic d'Usure EEPROM</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Lancement du Banc de Test Matériel EEPROM
*Sondage des cellules et vérification des registres de charge de la pompe à haute tension.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Sonde Silicium JEDEC</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Diagnostic Matriciel Actif</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Cartographie des 92 160 octets en cours • Mesure des temps d'accès</div>
                        <div class="wf-subtext">Vérification de l'absence de charges parasites piégées dans l'oxyde de grille</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Calcul de l'indice de santé...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Audit Blocs Défectueux & Calcul Health Index (JESD22)
*Analyse statistique de l'endurance et vérification de la garantie constructeur de rétention.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Contrôleur d'Endurance</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Analyse Santé (98%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 98%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [JESD22-CHECK] Évaluation de rétention thermique équivalente 25 ans à 55°C : OK</code><br>
                        <code>> [WEAR-LEVELING] Table d'usure uniforme, 0 bloc défectueux recensé</code><br>
                        <code>> [CHARGE-PUMP] Tension de programmation 14.8V stabilisée</code><br>
                        <code>> [HEALTH-INDEX] Score parfait 100.0% attribué au composant</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Matrice EEPROM 100% Saine & Rétention 25 Ans Certifiée
*La puce offre toutes les garanties physiques pour conserver les mémoires de manière pérenne.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Silicium Certifié JEDEC</span>
                        <span class="wf-status-badge wf-badge-success">✨ Santé Silicium 100%</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🏆</span>
                        <div>
                          <strong>Matrice EEPROM en Parfait État (Indice de Santé 100%)</strong>
                          <p class="wf-subtext">Rétention garantie > 25 ans selon JEDEC JESD22 • Prêt pour négociation de vitesse PPS</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Négocier Vitesse PPS Maximale (848 kbps) →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-220"></a>
## UC-220 : Négociation de Vitesse PPS (Baudrate 106 ➔ 212 ➔ 424 ➔ 848 kbps)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-220` |
| **Catégorie Métier** | **Silicium & Détection** |
| **Acteur Principal** | Système Automatisé PaxStation |
| **Plateformes Cibles** | Poste Pro Dédié (macOS, Windows, Linux) |
| **Tags Clés** | `PPS`, `Baudrate`, `Vitesse`, `ISO14443`, `848kbps`, `Optimisation`, `RF` |
| **Base Légale & Normative** | Norme internationale ISO/IEC 14443-4 Section 5.3 (Procédure de sélection de protocole et paramètres PPS). |
| **Terminal / Canvas Wireframe** | `PaxStation Pro • Négociation de Vitesse RF PPS (Baudrate 848 kbps ISO 14443-4)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> La carte a transmis son ATS indiquant la prise en charge des débits rapides (octets TA1).

> [!TIP]
> **Postconditions Garanties :**
> Le canal de communication fonctionne à 848 kbps avec un taux d'erreur nul, réduisant le temps de gravure à moins de 6 secondes.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Inspection des capacités de débit de la carte dans les paramètres de l'ATS (TA(1) codant les facteurs DSI/DRI).
2. Émission de la trame de négociation PPS (Protocol and Parameter Selection) demandant le palier maximal 848 kbps.
3. Attente de la trame d'acquittement PPS de la puce sous 10 millisecondes.
4. Bascule synchrone du modulateur du lecteur sans contact et de l'étage RF de la puce à 848 kbps.
5. Mesure du taux d'erreur de trame (Bit Error Rate) et accélération par un facteur 8 de la gravure des 92 Ko.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `initial_rf_speed` | **Débit de Base Initial** | `text` | `106 kbps (Débit par défaut ISO 14443)` | - | `106 kbps` | ⭕ Optionnel |
| `pps_exchange_frame` | **Trame de Négociation PPS** | `text` | `PPSS: 0xFF • PPS0: 0x11 • PPS1: 0x33 (DSI=3, DRI=3)` | - | `Trame PPS` | ⭕ Optionnel |
| `negotiated_baudrate` | **Vitesse Finale Négociée** | `select` | `848 KBPS (DÉBIT ULTRA-RAPIDE QUADRUPLÉ)` | - | `848 kbps Actif` | ✅ Requis |
| `estimated_write_duration` | **Temps Estimé de Gravure 92 Ko** | `text` | `5.4 secondes (au lieu de 44 secondes à 106 kbps)` | - | `Gain x8` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_negotiate_pps` | **Négocier Vitesse PPS Maximale** | `primary` | `idle` | ⚡ |
| `btn_test_rf_ber` | **Tester la Stabilité Radio (BER)** | `secondary` | `idle` | 📶 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Négociation PPS Réussie : Débit Établi à 848 kbps
>
> **Badge de Conformité :** `848 kbps Validé`
>
> **Détail Opérationnel :** Le canal sans contact est cadencé à 848 kbps sans aucune perte de paquet. Temps de cycle optimisé au maximum.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `WARN_PPS_FALLBACK_BASE_SPEED` |
| **Intitulé de l'Incident** | **Échec Négociation PPS (Repli Automatique à 106 kbps)** |
| **Condition Déclenchante** | La puce n'acquitte pas la trame PPS dans le délai imparti en raison d'interférences RF. |
| **Message d'Erreur UI** | *« Avertissement débit : Repli sécuritaire sur le débit standard 106 kbps. »* |
| **Action Corrective Requise** | **Recentrer la carte sur l'antenne pour minimiser les pertes de couplage magnétique.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Pro • Négociation de Vitesse RF PPS (Baudrate 848 kbps ISO 14443-4)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Débit Standard 106 kbps Actif | *En attente utilisateur* | Le canal RF fonctionne à la vitesse par défaut. La négociation PPS haute vitesse est disponible. |
| **2** | **Déclenchement ⚡** | Envoi Trame de Négociation PPS pour 848 kbps | `Émission trame PPS FF 11 33` | Demande de bascule de cadence adressée au contrôleur sans contact de la puce. |
| **3** | **Traitement ⚙️** | Bascule Modulateur RF & Contrôle Taux d'Erreurs BER | `Progression : 96%` | Vérification de la clarté du signal 13.56 MHz à 848 kbps et absence de paquets corrompus. |
| **4** | **Scellement & Fin ✨** | Lien Radiofréquence Établi à 848 kbps (Gain Vitesse x8) | `Statut : success` | Le débit maximal est actif. Les opérations d'écriture de masse s'exécuteront à cadence ultra-rapide. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-220 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Débit Standard 106 kbps Actif
*Le canal RF fonctionne à la vitesse par défaut. La négociation PPS haute vitesse est disponible.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Contrôleur de Débit RF</span>
                        <span class="wf-status-badge wf-badge-neutral">Vitesse de Base (106 kbps)</span>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-field-group">
                          <label class="wf-label">Vitesse Courante</label>
                          <div class="wf-input-placeholder">106 kbps (Durée estimée 92 Ko : 44s)</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Cible Négociation</label>
                          <div class="wf-input-placeholder">848 kbps (Quadri-vitesse DSI=3/DRI=3)</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">⚡ Négocier Vitesse PPS Maximale</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Envoi Trame de Négociation PPS pour 848 kbps
*Demande de bascule de cadence adressée au contrôleur sans contact de la puce.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Protocole PPS ISO 14443-4</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Trame PPS Émise</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Trame PPS transmise : FF 11 33 (DSI=3, DRI=3 ➔ 848 kbps)</div>
                        <div class="wf-subtext">Attente de l'acquittement de la puce sous 5 ms</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Bascule de modulation RF...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Bascule Modulateur RF & Contrôle Taux d'Erreurs BER
*Vérification de la clarté du signal 13.56 MHz à 848 kbps et absence de paquets corrompus.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Contrôle Radiofréquence</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Bascule Fréquence (96%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 96%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [PPS-ACK] Acquittement reçu de la puce : FF 00 (Accordé à 848 kbps)</code><br>
                        <code>> [RF-MODULATOR] Fréquence sous-porteuse calée à 848 kHz (fc/16)</code><br>
                        <code>> [BER-TEST] Taux d'erreurs binaire BER mesuré : 0.000% sur 10 000 trames</code><br>
                        <code>> [THROUGHPUT] Débit effectif : 91.2 Ko/s (Transfert total prévu en 5.4s)</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Lien Radiofréquence Établi à 848 kbps (Gain Vitesse x8)
*Le débit maximal est actif. Les opérations d'écriture de masse s'exécuteront à cadence ultra-rapide.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Débit Optimisé</span>
                        <span class="wf-status-badge wf-badge-success">✨ 848 kbps Négocié</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">⚡</span>
                        <div>
                          <strong>Communication Cadencée à 848 kbps (Gain Facteur 8)</strong>
                          <p class="wf-subtext">Transfert des 92 Ko en 5.4s • Prêt pour l'authentification forte opérateur</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Passer à l'Authentification Forte FIDO2 →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-221"></a>
## UC-221 : Authentification Forte Opérateur par Clé FIDO2 / YubiKey & Enrôlement

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-221` |
| **Catégorie Métier** | **Sécurité Silicium & Anti-Tamper** |
| **Acteur Principal** | Opérateur d'Atelier Habilité |
| **Plateformes Cibles** | Poste Pro Dédié (macOS, Windows, Linux) |
| **Tags Clés** | `FIDO2`, `YubiKey`, `CTAP2`, `WebAuthn`, `Authentification`, `Operateur`, `Audit` |
| **Base Légale & Normative** | Standard FIDO Alliance CTAP2.1 & Recommandation W3C Web Authentication (WebAuthn Level 2). |
| **Terminal / Canvas Wireframe** | `PaxStation Pro • Authentification Forte Opérateur FIDO2 / YubiKey (CTAP2)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> L'opérateur s'apprête à déverrouiller les fonctionnalités critiques d'écriture et de scellement matériel.

> [!TIP]
> **Postconditions Garanties :**
> L'identité de l'opérateur est formellement authentifiée au plus haut niveau de confiance matériel.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. La PaxStation génère un challenge cryptographique pseudo-aléatoire de 32 octets (norme FIDO2 / WebAuthn).
2. L'opérateur connecte sa clé matérielle FIDO2 (YubiKey Série 5) et applique son empreinte ou contact physique tactile.
3. La puce cryptographique de la clé FIDO2 valide le code PIN utilisateur et signe le challenge avec sa clé privée secp256r1.
4. Le module d'atelier vérifie la signature contre la clé publique enrôlée au registre des opérateurs habilités.
5. Délivrance d'un jeton d'habilitation de gravure nominatif (durée 15 minutes), journalisé dans la chaîne d'audit.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `operator_fullname` | **Opérateur Titulaire Habilité** | `text` | `Jean-Marc Vandamme (Matricule ATELIER-OP-08)` | - | `Graveur Agréé` | ✅ Requis |
| `fido2_device_sn` | **Clé Matérielle Détectée** | `text` | `Yubico YubiKey 5 NFC (ID 16294801 • Firmware 5.4.3)` | - | `FIDO2 / CTAP2` | ⭕ Optionnel |
| `user_presence_verification` | **Preuve de Présence Physique** | `select` | `PRÉSENCE TACTILE (UP) & PIN CONFIRMÉS` | - | `Touch Sensor OK` | ✅ Requis |
| `session_token_scope` | **Jeton de Session Gravure** | `text` | `ROLE_GRAVURE_SOUVERAINE (Expiration : 14 min 52 s)` | - | `Jeton 15 min` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_fido2_authenticate` | **Authentifier par Clé FIDO2 / YubiKey** | `primary` | `idle` | 🔑 |
| `btn_lock_session_now` | **Verrouiller le Poste Immédiatement** | `secondary` | `idle` | 🔒 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Authentification Forte Opérateur Réussie (FIDO2 CTAP2)
>
> **Badge de Conformité :** `FIDO2 Authentifié`
>
> **Détail Opérationnel :** Signature matérielle vérifiée avec succès. Autorisation accordée pour l'écriture et le scellement définitif.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_OPERATOR_AUTH_REJECTED` |
| **Intitulé de l'Incident** | **Échec d'Authentification FIDO2 ou Clé Non Enrôlée** |
| **Condition Déclenchante** | Signature CTAP2 invalide, clé matérielle révoquée ou contact physique non établi dans les 15 secondes. |
| **Message d'Erreur UI** | *« Accès refusé : Impossible de certifier l'habilitation de l'opérateur sur la PaxStation. »* |
| **Action Corrective Requise** | **Insérer la clé YubiKey officielle enregistrée au registre d'atelier et valider le contact tactile.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Pro • Authentification Forte Opérateur FIDO2 / YubiKey (CTAP2)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Demande d'Élévation de Privilèges pour Gravure Souveraine | *En attente utilisateur* | L'écriture définitive requiert la preuve de présence physique de l'opérateur habilité via sa clé matérielle. |
| **2** | **Déclenchement ⚡** | Présentation de la YubiKey & Contact Tactile Confirmé | `Touch sur le capteur doré de la YubiKey 5 NFC` | Signature du challenge cryptographique de 32 octets par la puce sécurisée de la clé. |
| **3** | **Traitement ⚙️** | Vérification Cryptographique ECDSA & Habilitation | `Progression : 98%` | Validation de la chaîne de confiance et émission du jeton d'autorisation de gravure. |
| **4** | **Scellement & Fin ✨** | Opérateur Authentifié & Droits de Gravure Accordés | `Statut : success` | L'opération de gravure est formellement imputable et tracée sous l'autorité de l'opérateur. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-221 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Demande d'Élévation de Privilèges pour Gravure Souveraine
*L'écriture définitive requiert la preuve de présence physique de l'opérateur habilité via sa clé matérielle.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Contrôle d'Accès Matériel</span>
                        <span class="wf-status-badge wf-badge-neutral">Clé FIDO2 Requise</span>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-field-group">
                          <label class="wf-label">Opérateur Attendu</label>
                          <div class="wf-input-placeholder">Jean-Marc Vandamme (OP-08)</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Authentification</label>
                          <div class="wf-input-placeholder">FIDO2 CTAP2 (Touch Sensor)</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔑 Authentifier par Clé FIDO2 / YubiKey</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Présentation de la YubiKey & Contact Tactile Confirmé
*Signature du challenge cryptographique de 32 octets par la puce sécurisée de la clé.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Challenge CTAP2</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Présence Tactile Détectée</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Contact physique validé • Clé secp256r1 activée dans l'élément sécurisé</div>
                        <div class="wf-subtext">Signature ECDSA renvoyée au démon d'authentification d'atelier</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Vérification de l'enrôlement...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Vérification Cryptographique ECDSA & Habilitation
*Validation de la chaîne de confiance et émission du jeton d'autorisation de gravure.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Vérificateur d'Identité</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Contrôle Signature (98%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 98%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [FIDO2-CTAP2] Signature ECDSA secp256r1 vérifiée contre le registre d'atelier</code><br>
                        <code>> [OPERATOR-ROLE] Habilitation 'GRAVEUR_SOUVERAIN' confirmée pour J.-M. Vandamme</code><br>
                        <code>> [TOKEN-ISSUANCE] Jeton de session #TOK-OP08-8842 émis (validité 15 min)</code><br>
                        <code>> [AUDIT-LOG] Entrée consignée : Autorisation d'écriture sur ACOSJ débloquée</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Opérateur Authentifié & Droits de Gravure Accordés
*L'opération de gravure est formellement imputable et tracée sous l'autorité de l'opérateur.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Session Déverrouillée</span>
                        <span class="wf-status-badge wf-badge-success">✨ Habilitation FIDO2 Accordée</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🔑</span>
                        <div>
                          <strong>Opérateur Officiellement Authentifié (YubiKey 5 CTAP2)</strong>
                          <p class="wf-subtext">Jean-Marc Vandamme • Droits d'écriture et de scellement accordés pour 15 min</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Lancer l'Injection APDU des Partitions →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-222"></a>
## UC-222 : Découpage APDU Extended Length (Trames 255 octets vs Extended APDU 64 Ko)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-222` |
| **Catégorie Métier** | **Gravure Silicium** |
| **Acteur Principal** | Système Automatisé PaxStation |
| **Plateformes Cibles** | Poste Pro Dédié (macOS, Windows, Linux) |
| **Tags Clés** | `ExtendedAPDU`, `Trames255`, `Chunking`, `ISO7816`, `Payload`, `Optimisation` |
| **Base Légale & Normative** | Norme ISO/IEC 7816-4 Section 5.1 (Structure des commandes APDU et mécanismes Extended Length). |
| **Terminal / Canvas Wireframe** | `PaxStation Pro • Gestionnaire de Segmentation APDU (Extended APDU vs Blocs 255o)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Une partition volumineuse (ex: Portrait WebP de 18 Ko dans EF-2 ou Audio de 42 Ko dans EF-3) doit être injectée.

> [!TIP]
> **Postconditions Garanties :**
> Les données volumineuses sont injectées sans incident, avec ou sans support Extended Length.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Interrogation de la carte et du lecteur pour déterminer la compatibilité Extended Length APDU (jusqu'à 65 535 octets par commande).
2. Sélection automatique de la stratégie de transfert : trames Extended directes ou segmentation en blocs ISO classiques (255 octets max).
3. Calcul des offsets mémoire P1-P2 pour chaque sous-trame UPDATE BINARY en cas de découpage dynamique.
4. Émission séquencée avec contrôle synchrone du code retour SW 0x9000 sur chaque tranche écrite.
5. Vérification de la continuité binaire de la partition réassemblée in-silico.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `payload_bytes_total` | **Volume de Données à Injecter** | `text` | `42 100 octets (Mémo Audio EF-3)` | - | `Volume Brut` | ⭕ Optionnel |
| `apdu_segmentation_mode` | **Mode de Transmission Retenu** | `select` | `EXTENDED LENGTH SUPPORTÉ (Trames de 4 096 octets)` | - | `Extended APDU` | ✅ Requis |
| `chunks_count_calculated` | **Nombre de Trames / Chunks** | `text` | `11 trames Extended (vs 166 trames courtes 255 o)` | - | `Optimisation x15` | ⭕ Optionnel |
| `average_write_throughput` | **Vitesse d'Injection Moyenne** | `text` | `68.2 Ko/s (Transfert total en 617 ms)` | - | `Performance` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_send_chunked_apdu` | **Transmettre en Extended APDU** | `primary` | `idle` | 📦 |
| `btn_fallback_short_apdu` | **Forcer Segmentation 255 Octets** | `secondary` | `idle` | ⚙️ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Segmentation APDU Validée : Écriture Silicium Intègre
>
> **Badge de Conformité :** `Extended APDU OK`
>
> **Détail Opérationnel :** 11 trames transmises sans aucune altération de buffer. Les 42 100 octets sont gravés dans la partition EF-3.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_APDU_BUFFER_OVERFLOW` |
| **Intitulé de l'Incident** | **Dépassement de Capacité de Tampon APDU sur le Lecteur** |
| **Condition Déclenchante** | Le micro-lecteur sans contact sature sa mémoire tampon face à une trame Extended trop large. |
| **Message d'Erreur UI** | *« Erreur matérielle : Tampon lecteur saturé (SW 0x6700 - Wrong Length). »* |
| **Action Corrective Requise** | **Basculer immédiatement en mode de découpage strict en blocs courts de 255 octets.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Pro • Gestionnaire de Segmentation APDU (Extended APDU vs Blocs 255o)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Partition Volumineuse (42 Ko) en Attente d'Injection | *En attente utilisateur* | Le mémo audio volumineux doit être segmenté de façon optimale pour respecter les tampons matériels. |
| **2** | **Déclenchement ⚡** | Calcul du Découpage en 11 Blocs Extended de 4 Ko | `Clic sur 'Transmettre en Extended APDU'` | Organisation des commandes UPDATE BINARY avec gestion fine des offsets d'adresses P1-P2. |
| **3** | **Traitement ⚙️** | Injection Séquencée par Chunks & Validation SW 0x9000 | `Progression : 96%` | Transfert haute vitesse et vérification du statut 0x9000 à l'issue de chaque bloc écrit. |
| **4** | **Scellement & Fin ✨** | Partition Gravée Sans Débordement de Mémoire Tampon | `Statut : success` | Le flux volumineux a été gravé en un temps record grâce au protocole Extended Length. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-222 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Partition Volumineuse (42 Ko) en Attente d'Injection
*Le mémo audio volumineux doit être segmenté de façon optimale pour respecter les tampons matériels.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Moteur de Segmentation APDU</span>
                        <span class="wf-status-badge wf-badge-neutral">Prêt pour Injection Silicium</span>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-field-group">
                          <label class="wf-label">Données Source</label>
                          <div class="wf-input-placeholder">Mémo Audio EF-3 (42 100 octets)</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Capacité APDU Lecteur</label>
                          <div class="wf-input-placeholder">Extended Length (Trames jusqu'à 64 Ko)</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">📦 Transmettre en Extended APDU</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Calcul du Découpage en 11 Blocs Extended de 4 Ko
*Organisation des commandes UPDATE BINARY avec gestion fine des offsets d'adresses P1-P2.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Chaînage APDU ISO 7816-4</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Découpage Extended Actif</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ 11 trames Extended APDU générées (10 x 4 096 octets + 1 x 1 140 octets)</div>
                        <div class="wf-subtext">Optimisation x15 par rapport au découpage traditionnel en blocs de 255 octets</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Écriture séquencée en cours...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Injection Séquencée par Chunks & Validation SW 0x9000
*Transfert haute vitesse et vérification du statut 0x9000 à l'issue de chaque bloc écrit.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Graveur Silicium</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Écriture Chunks (96%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 96%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [APDU-CHUNK-1] Offset 0x0000 : 4096 octets écrits ➔ SW 0x9000</code><br>
                        <code>> [APDU-CHUNK-5] Offset 0x4000 : 4096 octets écrits ➔ SW 0x9000</code><br>
                        <code>> [APDU-CHUNK-11] Offset 0xA000 : 1140 octets écrits ➔ SW 0x9000</code><br>
                        <code>> [VERIFY] 42 100 octets logés dans EF-3 sans aucune saturation de tampon</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Partition Gravée Sans Débordement de Mémoire Tampon
*Le flux volumineux a été gravé en un temps record grâce au protocole Extended Length.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Partition Flashee</span>
                        <span class="wf-status-badge wf-badge-success">✨ Extended APDU Conforme</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">📦</span>
                        <div>
                          <strong>Partition Audio EF-3 Gravée avec Succès (42 100 octets)</strong>
                          <p class="wf-subtext">11 trames Extended APDU sans erreur • Prêt pour le test à blanc du verrouillage</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Lancer le Test à Blanc du Verrouillage Matériel →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-223"></a>
## UC-223 : Test à Blanc du Verrouillage Matériel (Simulation Fusible Virtuel in-silico)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-223` |
| **Catégorie Métier** | **Sécurité Silicium & Anti-Tamper** |
| **Acteur Principal** | Opérateur d'Atelier & Contrôleur Qualité |
| **Plateformes Cibles** | Poste Pro Dédié (macOS, Windows, Linux) |
| **Tags Clés** | `DryRun`, `FusibleVirtuel`, `TestABlanc`, `SimulationLock`, `IronGate`, `InSilico` |
| **Base Légale & Normative** | Politique de sécurité AeterniTrak Iron Gate & Recommandations Common Criteria EAL5+. |
| **Terminal / Canvas Wireframe** | `PaxStation Pro • Simulation In-Silico de Verrouillage Matériel (Dry-Run Iron Gate)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Les partitions EF-1 à EF-5 sont écrites ; l'opérateur s'apprête à déclencher le scellement définitif irréversible.

> [!TIP]
> **Postconditions Garanties :**
> Le comportement post-verrouillage est certifié conforme in-silico, éliminant tout risque de blocage involontaire.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Activation de la commande de simulation de verrouillage (Dry-Run virtuel) supportée par l'applet AeterniCore.
2. Bascule temporaire en mémoire vive de l'état des droits d'accès au niveau 'READ ONLY SCENARIO'.
3. Émission d'une commande de test d'écriture interdite (UPDATE BINARY sur EF-1) : validation du rejet strict avec mot d'état SW 0x6982.
4. Vérification de la lisibilité sans entrave en lecture publique sans contact (READ BINARY) sur les fichiers mémoriels.
5. Restauration de l'état nominal avec délivrance du feu vert sécuritaire pour le claquage réel du fusible physique.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `dry_run_state` | **Mode de Test Exécuté** | `text` | `SIMULATION IN-SILICO (Zéro altération physique irréversible)` | - | `Dry-Run Actif` | ⭕ Optionnel |
| `simulated_probe_write` | **Sonde de Rejet d'Écriture Simulée** | `text` | `UPDATE BINARY testé -> Rejet SW 0x6982 confirmé` | - | `SW 0x6982 Rejet` | ⭕ Optionnel |
| `simulated_probe_read` | **Sonde de Lecture Libre Simulée** | `text` | `READ BINARY testé -> Succès SW 0x9000 confirmé` | - | `SW 0x9000 Lecture` | ⭕ Optionnel |
| `burn_fuse_authorization` | **Verdict d'Autorisation de Scellement** | `select` | `FEU VERT ACCORDÉ POUR FUSIBLE PHYSIQUE DÉFINITIF` | - | `Feu Vert Scellement` | ✅ Requis |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_run_dry_run_simulation` | **Lancer le Test à Blanc In-Silico** | `primary` | `idle` | 🛡️ |
| `btn_abort_dry_run` | **Annuler & Inspecter Données** | `secondary` | `idle` | ↩ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Test à Blanc Réussi : Comportement de Verrouillage Certifié
>
> **Badge de Conformité :** `In-Silico 100% Validé`
>
> **Détail Opérationnel :** La simulation confirme le verrouillage parfait en lecture seule et le blocage absolu de toute tentative d'écriture.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_DRY_RUN_VALIDATION_FAILED` |
| **Intitulé de l'Incident** | **Échec du Test à Blanc : Anomalie Détectée avant Scellement** |
| **Condition Déclenchante** | La commande de lecture échoue sous le profil verrouillé simulé ou l'écriture n'est pas convenablement rejetée. |
| **Message d'Erreur UI** | *« Blocage de sécurité préventif : Les tables de droits d'accès présentent une incohérence. »* |
| **Action Corrective Requise** | **Ne surtout pas claquer le fusible réel, ré-initialiser les descripteurs de sécurité d'EF-0.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Pro • Simulation In-Silico de Verrouillage Matériel (Dry-Run Iron Gate)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Données Gravées, Fusible Non Encore Claqué | *En attente utilisateur* | Toutes les partitions sont renseignées. Avant de percuter le fusible destructif, le test à blanc est requis. |
| **2** | **Déclenchement ⚡** | Activation du Profil Simulatif 'Read-Only' In-Silico | `Clic sur 'Lancer le Test à Blanc In-Silico'` | Bascule temporaire des masques de sécurité sans claquage électrique de la diode zener. |
| **3** | **Traitement ⚙️** | Test Sondes : Rejet Écriture (0x6982) & Succès Lecture | `Progression : 98%` | Contrôle que l'accès libre aux volontés est fluide et que toute écriture future est bannie. |
| **4** | **Scellement & Fin ✨** | Feu Vert Accordé pour Claquage Réel du Fusible Physique | `Statut : success` | La certitude absolue est acquise que la carte sera parfaite une fois scellée définitivement. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-223 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Données Gravées, Fusible Non Encore Claqué
*Toutes les partitions sont renseignées. Avant de percuter le fusible destructif, le test à blanc est requis.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Banc de Test Iron Gate</span>
                        <span class="wf-status-badge wf-badge-neutral">Prêt pour Dry-Run In-Silico</span>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-field-group">
                          <label class="wf-label">État Silicium</label>
                          <div class="wf-input-placeholder">Partitions Écrites • Fusible Intact (UNLOCKED)</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Test Préventif</label>
                          <div class="wf-input-placeholder">Simulation Droits READ-ONLY virtuels</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🛡️ Lancer le Test à Blanc In-Silico</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Activation du Profil Simulatif 'Read-Only' In-Silico
*Bascule temporaire des masques de sécurité sans claquage électrique de la diode zener.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Moteur Virtuel Anti-Tamper</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Dry-Run Actif (Simulation)</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Simulation verrouillage enclenchée • Envoi de sondes d'intrusion</div>
                        <div class="wf-subtext">Test de conformité des réponses APDU en mode lecture seule strict</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Évaluation des sondes de sécurité...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Test Sondes : Rejet Écriture (0x6982) & Succès Lecture
*Contrôle que l'accès libre aux volontés est fluide et que toute écriture future est bannie.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Sondeur de Sécurité</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Audit Dry-Run (98%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 98%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [PROBE-WRITE] Tentative UPDATE BINARY sur EF-1 ➔ Rejeté : SW 0x6982 (Security status not satisfied) : OK</code><br>
                        <code>> [PROBE-READ] Lecture publique READ BINARY sur EF-1 & EF-2 ➔ Succès SW 0x9000 : OK</code><br>
                        <code>> [ED25519-CHECK] Signature d'intégrité vérifiée en mode anonyme sans contact : OK</code><br>
                        <code>> [VERDICT] Comportement in-silico 100% conforme aux spécifications Common Criteria EAL5+</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Feu Vert Accordé pour Claquage Réel du Fusible Physique
*La certitude absolue est acquise que la carte sera parfaite une fois scellée définitivement.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Autorisation Validée</span>
                        <span class="wf-status-badge wf-badge-success">✨ Feu Vert Scellement Définitif</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🛡️</span>
                        <div>
                          <strong>Test à Blanc In-Silico Validé sans Aucune Discordance</strong>
                          <p class="wf-subtext">Rejet d'écriture 0x6982 certifié • Lecture publique garantie • Feu vert pour le verrou matériel</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Passer à la Relecture Intégrale de Contrôle SHA-256 →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-224"></a>
## UC-224 : Relecture Intégrale de Contrôle & Concordance d'Empreinte SHA-256 post-gravure

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-224` |
| **Catégorie Métier** | **Assurance Qualité & Conformité** |
| **Acteur Principal** | Contrôleur Qualité & Système Automatisé |
| **Plateformes Cibles** | Poste Pro Dédié (macOS, Windows, Linux) |
| **Tags Clés** | `Relecture`, `SHA256`, `Concordance`, `IntegriteBitABit`, `PostGravure`, `QA` |
| **Base Légale & Normative** | Norme FIPS PUB 180-4 (Secure Hash Standard - SHA-256) & Procédure Qualité Funéraire QA-PRO-02. |
| **Terminal / Canvas Wireframe** | `PaxStation Pro • Relecture Intégrale Post-Gravure & Concordance SHA-256` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> L'ensemble des données a été écrit sur la carte par la PaxStation.

> [!TIP]
> **Postconditions Garanties :**
> La concordance exacte entre la volonté du client et le silicium gravé est mathématiquement prouvée.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Lancement de la procédure de contrôle qualité : relecture séquentielle bit-à-bit des partitions gravées (EF-0 à EF-5).
2. Extraction intégrale des flux binaires sans décompression ni réinterprétation.
3. Calcul de l'empreinte cryptographique SHA-256 du flux mémoire complet lu in-situ sur la puce.
4. Comparaison avec l'empreinte SHA-256 de référence transmise dans le BAT initialement approuvé par le client.
5. Délivrance de l'attestation de concordance binaire absolue à 100.00% et scellement du rapport dans l'audit trail.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `reference_hash_sha256` | **Hash de Référence (BAT Signé)** | `text` | `3f79e2a8c149d56b009e8d4a51e68b3c9420bf824f912e61a84f3c05e1a7b942` | - | `Hash Consigne` | ⭕ Optionnel |
| `readback_hash_sha256` | **Hash Relecture Mémoire Silicium** | `text` | `3f79e2a8c149d56b009e8d4a51e68b3c9420bf824f912e61a84f3c05e1a7b942` | - | `Hash Silicium` | ⭕ Optionnel |
| `hash_comparison_result` | **Résultat Concordance Binaire** | `select` | `CONCORDANCE 100.00% STRICTE (ZÉRO BIT DE DIFFÉRENCE)` | - | `Match SHA-256` | ✅ Requis |
| `total_bytes_audited` | **Octets Lus et Vérifiés** | `text` | `91 420 octets vérifiés sur 92 Ko (Toutes partitions intègres)` | - | `Audit Bit-à-Bit` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_execute_readback_audit` | **Lancer la Relecture Intégrale Silicium** | `primary` | `idle` | 🔍 |
| `btn_issue_qa_certificate` | **Émettre Certificat d'Intégrité SHA-256** | `secondary` | `idle` | 🏆 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Concordance SHA-256 Bit-à-Bit Certifiée Conforme (100.00%)
>
> **Badge de Conformité :** `SHA-256 100% Match`
>
> **Détail Opérationnel :** Les données logées sur la puce correspondent rigoureusement et fidèlement au BAT signé par la famille.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_SHA256_MISMATCH_POST_WRITE` |
| **Intitulé de l'Incident** | **Divergence d'Empreinte Binaire Détectée Post-Gravure** |
| **Condition Déclenchante** | L'empreinte calculée sur la carte ne correspond pas au hash de référence (altération durant l'écriture). |
| **Message d'Erreur UI** | *« Incident qualité majeur : Les données gravées sur le silicium diffèrent du document de référence. »* |
| **Action Corrective Requise** | **Mettre la carte au rebut (SCRAPPED), inspecter l'alimentation RF du lecteur et relancer le processus.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Pro • Relecture Intégrale Post-Gravure & Concordance SHA-256**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Carte Gravée Prête pour Relecture Intégrale Bit-à-Bit | *En attente utilisateur* | Toutes les écritures sont achevées. L'audit d'intégrité bit-à-bit va comparer le silicium avec le BAT source. |
| **2** | **Déclenchement ⚡** | Extraction des 91 420 Octets Gravés sur le Silicium | `Clic sur 'Lancer la Relecture Intégrale Silicium'` | Relecture en rafale à 848 kbps de l'intégralité des partitions mémoire de la puce ACOSJ. |
| **3** | **Traitement ⚙️** | Calcul SHA-256 du Contenu Réel & Comparaison Hash BAT | `Progression : 99%` | Comparaison binaire stricte 256 bits et scellement du résultat dans le dossier de conformité. |
| **4** | **Scellement & Fin ✨** | Concordance Binaire Certifiée à 100.00% (Zéro Erreur) | `Statut : success` | Le contenu matériel est la copie conforme et inviolable du bon à tirer validé. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-224 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Carte Gravée Prête pour Relecture Intégrale Bit-à-Bit
*Toutes les écritures sont achevées. L'audit d'intégrité bit-à-bit va comparer le silicium avec le BAT source.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Contrôle Qualité Bit-à-Bit</span>
                        <span class="wf-status-badge wf-badge-neutral">Prêt pour Relecture SHA-256</span>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-field-group">
                          <label class="wf-label">Hash Référence BAT</label>
                          <div class="wf-input-placeholder">3f79e2a8c149d56b009e8d4a51e68b3c...</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Partitions à relire</label>
                          <div class="wf-input-placeholder">EF-0, EF-1, EF-2, EF-3, EF-4, EF-5</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔍 Lancer la Relecture Intégrale Silicium</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Extraction des 91 420 Octets Gravés sur le Silicium
*Relecture en rafale à 848 kbps de l'intégralité des partitions mémoire de la puce ACOSJ.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Lecteur Haute Vitesse</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Relecture en Rafale 848 kbps</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ 91 420 octets extraits sans erreur de parité en 1.1 seconde</div>
                        <div class="wf-subtext">Calcul du condensat SHA-256 sur le flux binaire extrait in-situ</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Comparaison avec l'empreinte de consigne...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Calcul SHA-256 du Contenu Réel & Comparaison Hash BAT
*Comparaison binaire stricte 256 bits et scellement du résultat dans le dossier de conformité.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Comparateur Cryptographique</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Vérification Hash (99%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 99%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [EXTRACT-STREAM] Reconstitution du flux ordonné EF-0 à EF-5 : 91 420 octets</code><br>
                        <code>> [SHA256-CALC] Hash extrait : 3f79e2a8c149d56b009e8d4a51e68b3c9420bf824f912e61a84f3c05e1a7b942</code><br>
                        <code>> [SHA256-BASE] Hash consigne : 3f79e2a8c149d56b009e8d4a51e68b3c9420bf824f912e61a84f3c05e1a7b942</code><br>
                        <code>> [MATCH-VERDICT] 100.00% IDENTIQUE • ZÉRO BIT DIVERGENT SUR TOUTE LA PUCE</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Concordance Binaire Certifiée à 100.00% (Zéro Erreur)
*Le contenu matériel est la copie conforme et inviolable du bon à tirer validé.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Intégrité Prouvée</span>
                        <span class="wf-status-badge wf-badge-success">✨ Concordance SHA-256 100%</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🏆</span>
                        <div>
                          <strong>Concordance Bit-à-Bit Certifiée Conforme (100.00%)</strong>
                          <p class="wf-subtext">Certificat d'intégrité SHA-256 émis • Prêt pour le calibrage de l'imprimante thermique</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Passer au Calibrage de l'Impression Physique →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-225"></a>
## UC-225 : Calibrage Alignement Imprimante Sublimation Thermique & Jauge Ruban

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-225` |
| **Catégorie Métier** | **Production Physique & Assurance Qualité** |
| **Acteur Principal** | Opérateur d'Atelier & Technicien Maintenance |
| **Plateformes Cibles** | Poste Pro Dédié (macOS, Windows, Linux) |
| **Tags Clés** | `Imprimante`, `SublimationThermique`, `Fargo`, `Calibrage`, `JaugeRuban`, `AlignementLaser` |
| **Base Légale & Normative** | Spécifications industrielles HID Global Fargo HDP & Norme ISO/IEC 7810 ID-1 relative à la résistance mécanique des cartes. |
| **Terminal / Canvas Wireframe** | `PaxStation Pro • Calibrage Imprimante Sublimation Retransfert & Jauge Consommables` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Avant de lancer le cycle de personnalisation graphique et dorure thermique sur la carte physique.

> [!TIP]
> **Postconditions Garanties :**
> L'imprimante est étalonnée et alimentée en consommables suffisants pour exécuter le tirage noble sans bavure ni rebut.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Interrogation télémétrique des capteurs de l'imprimante professionnelle de retransfert (ex: Fargo HDP5000).
2. Mesure des niveaux restants sur les consommables : ruban couleur YMCK, film de retransfert haute durabilité et ruban or satiné.
3. Lancement de la mire d'alignement micrométrique des têtes d'impression thermique (tolérance requise < 0.05 mm).
4. Régulation et stabilisation de la température du rouleau chauffant à 175.0°C ± 0.5°C.
5. Autorisation de l'impression physique avec assurance de ne subir aucune interruption en cours de cycle.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `printer_target_model` | **Imprimante Professionnelle Ciblée** | `text` | `HID Fargo HDP5000 Retransfert HD (Connectée USB / LAN)` | - | `Fargo HDP5000` | ⭕ Optionnel |
| `ribbon_consumables_gauge` | **Jauge Ruban Dorure & Couleurs** | `text` | `78% restant (Capacité estimée : 142 cartes complètes)` | - | `Consommables OK` | ⭕ Optionnel |
| `head_alignment_metric` | **Alignement Tête Micrométrique** | `text` | `Décalage X: +0.02 mm • Y: -0.01 mm (Tolérance < 0.05 mm)` | - | `Aligné 0.02mm` | ⭕ Optionnel |
| `heating_roller_temp` | **Température Rouleau Retransfert** | `select` | `175.4 °C (TEMPÉRATURE NOMINALE STABILISÉE)` | - | `175°C Conforme` | ✅ Requis |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_calibrate_printer_heads` | **Lancer Calibration & Nettoyage Rouleaux** | `primary` | `idle` | 🖨️ |
| `btn_print_alignment_pattern` | **Imprimer Mire de Contrôle Qualité** | `secondary` | `idle` | 🎯 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Imprimante Sublimation Calibrée & Consommables Prêts
>
> **Badge de Conformité :** `Prêt pour Tirage Pro`
>
> **Détail Opérationnel :** Têtes alignées à 0.02 mm, température à 175.4°C, réserve de ruban pour 142 cartes. Personnalisation physique autorisée.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `WARN_RIBBON_LEVEL_CRITICAL` |
| **Intitulé de l'Incident** | **Niveau Critique de Ruban d'Impression (< 5% Restant)** |
| **Condition Déclenchante** | La longueur restante de ruban or ou de film de retransfert est insuffisante pour achever la carte. |
| **Message d'Erreur UI** | *« Avertissement consommable : Risque de rupture de ruban en cours de personnalisation physique. »* |
| **Action Corrective Requise** | **Remplacer la cassette de ruban Fargo avant de lancer l'impression pour éviter une mise au rebut.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **PaxStation Pro • Calibrage Imprimante Sublimation Retransfert & Jauge Consommables**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Imprimante Fargo Connectée en Attente d'Étalonnage | *En attente utilisateur* | L'imprimante professionnelle de retransfert thermique est sous tension, prête pour le cycle d'alignement. |
| **2** | **Déclenchement ⚡** | Interrogation des Capteurs de Tête & Niveaux de Ruban | `Clic sur 'Lancer Calibration & Nettoyage Rouleaux'` | Mesure des jauges optiques de ruban et activation du cycle thermique de mise à température. |
| **3** | **Traitement ⚙️** | Calibration Optique (0.02 mm) & Chauffage Rouleau à 175°C | `Progression : 97%` | Ajustement micrométrique de l'axe d'impression pour garantir l'alignement sur la carte CR-80. |
| **4** | **Scellement & Fin ✨** | Imprimante Calibrée & Consommables Prêts pour Impression | `Statut : success` | Le poste physique est parfaitement étalonné. La personnalisation esthétique peut débuter. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-225 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Imprimante Fargo Connectée en Attente d'Étalonnage
*L'imprimante professionnelle de retransfert thermique est sous tension, prête pour le cycle d'alignement.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Contrôle Imprimante Fargo HDP5000</span>
                        <span class="wf-status-badge wf-badge-neutral">Prêt pour Calibration</span>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-field-group">
                          <label class="wf-label">Matériel Détecté</label>
                          <div class="wf-input-placeholder">HID Fargo HDP5000 (Retransfert HD)</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Jauges Consommables</label>
                          <div class="wf-input-placeholder">Ruban YMCK 78% • Film Retransfert 82%</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🖨️ Lancer Calibration & Nettoyage Rouleaux</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Interrogation des Capteurs de Tête & Niveaux de Ruban
*Mesure des jauges optiques de ruban et activation du cycle thermique de mise à température.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Télémétrie Impression</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Étalonnage Optique Actif</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Capteurs optiques interrogés • Décalage initial mesuré : X +0.02 mm, Y -0.01 mm</div>
                        <div class="wf-subtext">Montée en température du rouleau thermique vers la consigne 175.0°C</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Stabilisation thermique...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Calibration Optique (0.02 mm) & Chauffage Rouleau à 175°C
*Ajustement micrométrique de l'axe d'impression pour garantir l'alignement sur la carte CR-80.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Régulateur Fargo</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Alignement Tête (97%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 97%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [OPTIC-ALIGN] Tête d'impression recalée au 1/100e mm : Tolérance 0.02mm respectée</code><br>
                        <code>> [HEAT-ROLLER] Température mesurée : 175.4°C (Consigne 175.0°C ±0.5°C validée)</code><br>
                        <code>> [CONSUMABLES] Réserve de ruban or satiné vérifiée pour 142 impressions</code><br>
                        <code>> [PRINTER-STATUS] Prêt pour impression haute définition sans bavure</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Imprimante Calibrée & Consommables Prêts pour Impression
*Le poste physique est parfaitement étalonné. La personnalisation esthétique peut débuter.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStation • Imprimante Homologuée</span>
                        <span class="wf-status-badge wf-badge-success">✨ Fargo HDP5000 Prête</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🖨️</span>
                        <div>
                          <strong>Imprimante à Sublimation Thermique Calibrée au 1/100e mm</strong>
                          <p class="wf-subtext">Rubans suffisants pour 142 cartes • Température stabilisée à 175.4°C • Zéro risque de bavure</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Lancer l'Impression Noble de la Carte Physique →</button>
                      </div>
                    </div>
```

</details>

---
