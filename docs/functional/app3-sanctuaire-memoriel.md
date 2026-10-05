# Application 3 — Sanctuaire Mémoriel Mobile & B2C (UC-301 à UC-316)

**Application Universelle de Recueillement, Hommage & Consultation des Directives**

> [!NOTE]
> **Périmètre Applicatif :**
> Le **Sanctuaire Mémoriel Mobile** est l'application grand public d'hommage et de recueillement destinée aux familles, amis et intervenants d'urgence. Déclenchée instantanément par un simple effleurement sans contact (**NFC Tap Zéro-Login, sans identifiant ni mot de passe**), elle valide l'intégrité cryptographique COSE_Sign1 en local, gère l'accueil des émetteurs selon la politique de confiance (Bandeau de réserve **Option B DEC-AET-07** pour clés inconnues), orchestre le sanctuaire acoustique avec **ducking vocal automatique (-14 dB)** et offre un tiroir d'accès solennel aux volontés civiles et médicales prioritaires (**alerte exérèse pacemaker, don d'organes, legs à la science — références à confirmer par un juriste**).

## 📌 Sommaire des Micro Use-Cases Spécifiés

| ID | Titre du Cas d'Usage | Catégorie Métier | Acteur | Plateformes | Référence Normative |
| :---: | :--- | :--- | :--- | :--- | :--- |
| [`UC-301`](#uc-301) | [Scan NFC Instantané Direct Sans Login (NFC Tap Android/iOS)](#uc-301) | **Accès & Identité** | Famille, Proches & Cérémonie | Natif (iOS & Android), Web NFC (Chrome Android), Web Standard (PWA Hors-Ligne) | Règlement général sur la protection des données (RGPD art. 5 - minimisation et souveraineté absolue des données). |
| [`UC-302`](#uc-302) | [Vérification Cryptographique Hybride Ed25519 / ES256 (DEC-AET-04)](#uc-302) | **Sécurité & Cryptographie** | Système Mobile & Sécurité | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Règlement eIDAS (UE 910/2014 - exigences pour les signatures électroniques avancées). |
| [`UC-303`](#uc-303) | [Affichage Sanctuaire, Recueillement & Livre d'Or Familial](#uc-303) | **Expérience Sanctuaire** | Famille & Proches | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Respect de la dignité des défunts et de la vie privée mémorielle (protection des données locales sans transfert distant). |
| [`UC-304`](#uc-304) | [Bandeau de Réserve DEC-AET-07 Option B pour Émetteur Inconnu](#uc-304) | **Résilience Mémorielle** | Famille & Régulateur | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Décision Kudoro DEC-AET-07 (Option B : Lisibilité mémorielle maintenue avec réserve réglementaire). |
| [`UC-305`](#uc-305) | [Blocage Hermétique sur Carte Falsifiée ou Clé Révoquée](#uc-305) | **Sécurité & Anti-Fraude** | Système Mobile & Auditeur | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Code pénal belge (art. 196 et suivants - faux en écriture et usage de faux). |
| [`UC-306`](#uc-306) | [Sanctuaire Acoustique & Ducking Vocal Vivant Automatique](#uc-306) | **Expérience Émotionnelle** | Famille & Proches | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Directives déontologiques funéraires relatives à la dignité et au respect des cérémonies. |
| [`UC-307`](#uc-307) | [Consultation des Volontés Civiles et Funéraires](#uc-307) | **Dernières Volontés** | Famille, Exécuteur Testamentaire & Pompes Funèbres | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Loi du 20 juillet 1971 sur les funérailles et sépultures (art. 2 - primauté absolue des volontés) (référence à confirmer par un juriste). |
| [`UC-308`](#uc-308) | [Fiche d'Urgence Médicale Interactive & Alerte Pacemaker (Art. L1232-24 CDLD & Modèle IIIC réglementaire)](#uc-308) | **Directives Médicales & Sécurité** | Secouristes, Urgentistes, Pompes Funèbres & Médecin Légiste | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Art. L1232-24 CDLD & Modèle IIIC réglementaire (exérèse obligatoire des stimulateurs cardiaques) et loi belge sur le don d'organes de 1986. |
| [`UC-309`](#uc-309) | [Consultation du Statut de Don d'Organes (Consentement Présumé Loi 1986)](#uc-309) | **Directives Médicales** | Coordinateur Hospitalier de Transplantation | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Loi du 13 juin 1986 sur le prélèvement et la transplantation d'organes (art. 10 - consentement présumé). |
| [`UC-310`](#uc-310) | [Directives Legs du Corps à la Science sous 48h](#uc-310) | **Directives Médicales** | Famille & Faculté de Médecine | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Décret wallon et arrêtés royaux régissant le don de corps à l'enseignement anatomique universitaire (référence à confirmer par un juriste). |
| [`UC-311`](#uc-311) | [Droit d'Accès Post-Mortem au Dossier Médical (Loi 2002 Art. 9 §4)](#uc-311) | **Droits du Patient** | Praticien Professionnel Désigné & Ayants Droit | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Loi du 22 août 2002 relative aux droits du patient (art. 9 §4 - accès post-mortem par praticien intermédiaire). |
| [`UC-312`](#uc-312) | [Politique Mémorielle PaxFunèbre & Pérennité Séculaire (DEC-AET-11)](#uc-312) | **Pérennité & Économie** | Famille & Réseau PaxFunèbre | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Directive européenne 2011/83/UE sur les droits des consommateurs (transparence et pérennité contractuelle) (référence à confirmer par un juriste). |
| [`UC-313`](#uc-313) | [Panne Audio / Perte de Périphérique & Mode Sanctuaire Silencieux Visuel](#uc-313) | **Expérience Émotionnelle & Résilience** | Famille & Proches en Recueillement | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Directives d'accessibilité numérique W3C WCAG 2.1 (critère 1.2 médias temporels) & Charte Sanctuaire Mémoriel. |
| [`UC-314`](#uc-314) | [Lecture de Secours par QR Code Micro-Gravé sur Carte Endommagée](#uc-314) | **Résilience Mémorielle & Secours** | Proches du Défunt & Conseiller Funéraire | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Norme ISO/IEC 18004 (code à barres matriciel QR Code haute densité) & Principe de résilience mémorielle séculaire. |
| [`UC-315`](#uc-315) | [Réclamations Contradictoires des Ayants Droit sur l'Arbre du Souvenir (Mise en Réserve Conservatoire)](#uc-315) | **Arbitrage & Volontés Funéraires** | Ayants Droit & Médiateur / Notaire | Web Standard (PWA Hors-Ligne), Natif (iOS & Android) | Loi du 20 juillet 1971 sur les funérailles et sépultures & Code civil (règles de dévolution des décisions funéraires). |
| [`UC-316`](#uc-316) | [Mode Hors-Ligne Extrême / Zone Blanche sans Réseau en Forêt Mémorielle (WebCrypto Local Ed25519)](#uc-316) | **Sécurité & Résilience Hors-Ligne** | Famille en Forêt Cinéraire & Garde-Forestier | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) | Décision Kudoro DEC-AET-09 (universalité d'accès sans contact hors-ligne) & Charte de résilience mémorielle séculaire. |

---

<a id="uc-301"></a>
## UC-301 : Scan NFC Instantané Direct Sans Login (NFC Tap Android/iOS)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-301` |
| **Catégorie Métier** | **Accès & Identité** |
| **Acteur Principal** | Famille, Proches & Cérémonie |
| **Plateformes Cibles** | Natif (iOS & Android), Web NFC (Chrome Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `NFC`, `ZeroLogin`, `IsoDep`, `CoreNFC`, `WebNFC` |
| **Base Légale & Normative** | Règlement général sur la protection des données (RGPD art. 5 - minimisation et souveraineté absolue des données). |
| **Terminal / Canvas Wireframe** | `Sanctuaire Mobile • iPhone 15 Pro (CoreNFC & Web NFC)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Application mobile Sanctuaire ouverte ou scan via Web NFC sur Chrome Android.

> [!TIP]
> **Postconditions Garanties :**
> Données de la carte chargées en mémoire vive locale, session de recueillement ouverte.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. L'utilisateur approche la Carte Sanctuaire ou le Médaillon du dos de son smartphone.
2. Détection du champ NFC en moins de 50 millisecondes (protocole IsoDep natif).
3. Lecture directe et intégrale des données mémorielles chiffrées sans AUCUNE invite de connexion, sans création de compte et sans mot de passe (zéro friction pour les personnes âgées).
4. Émission d'un retour haptique doux confirmant la bonne lecture du silicium.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `auth_mode` | **Mode d'Authentification** | `text` | `ZÉRO LOGIN (Local-First Universel)` | Auth | `Zéro Friction` | ⭕ Optionnel |
| `nfc_proto` | **Protocole Sans Contact** | `text` | `NFC IsoDep / ISO 14443-4 T=CL` | Protocole | `IsoDep` | ⭕ Optionnel |
| `scan_latency` | **Temps de Détection** | `text` | `38 millisecondes` | Latence | `Instantané` | ⭕ Optionnel |
| `loaded_bytes` | **Données Rapatriées** | `text` | `78 412 octets in-silico (Portraits + Audio + Volontés)` | Volume | `Mémoire Vive` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_tap_nfc` | **Approcher la Carte du Haut du Smartphone** | `primary` | `idle` | 📱 |
| `btn_nfc_help` | **Aide Emplacement Antenne NFC** | `secondary` | `idle` | ❓ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Carte Sanctuaire Reconnue Instantanément
>
> **Badge de Conformité :** `Lecture Silicium 38 ms`
>
> **Détail Opérationnel :** Accès direct sans mot de passe. Données de la défunte Claire Dubois chargées.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_NFC_READ_TIMEOUT` |
| **Intitulé de l'Incident** | **Rupture de Champ NFC Avant Fin de Lecture** |
| **Condition Déclenchante** | Retrait précipité de la carte avant le transfert complet des 78 Ko. |
| **Message d'Erreur UI** | *« Erreur de transmission : La carte a été retirée trop rapidement de l'antenne smartphone. »* |
| **Action Corrective Requise** | **Maintenir la carte immobile contre le dos de l'appareil pendant 1 seconde complète.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Sanctuaire Mobile • iPhone 15 Pro (CoreNFC & Web NFC)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Écran d'Accueil Épuré en Attente de Scan | *En attente utilisateur* | Smartphone en veille passive. Invite solennelle d'approche de la carte visible. |
| **2** | **Déclenchement ⚡** | Tap NFC Physique & Vibration Haptique | `Apposition de la carte contre le module NFC supérieur du smartphone` | Couplage inductif immédiat avec retour haptique doux et animation d'ondes concentriques. |
| **3** | **Traitement ⚙️** | Décompression Locale CBOR & Extraction des Médias | `Progression : 80%` | Décodage en local des portraits WebP et du fichier vocal Opus sans aucun appel serveur. |
| **4** | **Scellement & Fin ✨** | Sanctuaire Déverrouillé Immédiatement | `Statut : success` | Portrait mémoriel affiché, musique prête. Expérience de recueillement ouverte sans friction. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-301 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Écran d'Accueil Épuré en Attente de Scan
*Smartphone en veille passive. Invite solennelle d'approche de la carte visible.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Le Pax Funèbre • Sanctuaire Mémoriel</span>
                        <span class="wf-status-badge wf-badge-neutral">Antenne NFC Prête</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-nfc-icon">🎴</span>
                        <div><strong>Approchez votre Carte ou Médaillon du smartphone</strong></div>
                        <div class="wf-subtext">Aucun identifiant ni mot de passe requis • 100% Hors-Ligne</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">📱 Approcher la Carte du Haut du Smartphone</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Tap NFC Physique & Vibration Haptique
*Couplage inductif immédiat avec retour haptique doux et animation d'ondes concentriques.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire Mobile • Couplage NFC</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Tap NFC Détecté (38ms)</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Liaison sans fil IsoDep établie avec l'ACOSJ 92k</div>
                        <div class="wf-subtext">Transfert direct en mémoire vive des 78 412 octets mémoriels</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Lecture des données in-silico...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Décompression Locale CBOR & Extraction des Médias
*Décodage en local des portraits WebP et du fichier vocal Opus sans aucun appel serveur.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire Mobile • Décodage Local-First</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Décodage Mémoire (80%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 80%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [CORE-READ] Décodage partition EF-1 (Profile) et EF-2 (Portrait) : OK</code><br>
                        <code>> [WEBP-DEC] Décompression portrait 480x480 (DEC-AET-12) en mémoire graphique</code><br>
                        <code>> [OPUS-DEC] Chargement tampon audio vocal 30 secondes : Prêt</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Sanctuaire Déverrouillé Immédiatement
*Portrait mémoriel affiché, musique prête. Expérience de recueillement ouverte sans friction.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Recueillement Ouvert</span>
                        <span class="wf-status-badge wf-badge-success">✨ Données Chargées</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🕊️</span>
                        <div>
                          <strong>Bienvenue dans l'Espace de Mémoire d'Henri Dubois</strong>
                          <p class="wf-subtext">Lecture locale achevée en 120 ms • Zéro donnée transmise sur Internet</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Vérification Cryptographique →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-302"></a>
## UC-302 : Vérification Cryptographique Hybride Ed25519 / ES256 (DEC-AET-04)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-302` |
| **Catégorie Métier** | **Sécurité & Cryptographie** |
| **Acteur Principal** | Système Mobile & Sécurité |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `Crypto`, `Ed25519`, `ES256`, `TrustList`, `DEC-AET-04` |
| **Base Légale & Normative** | Règlement eIDAS (UE 910/2014 - exigences pour les signatures électroniques avancées). |
| **Terminal / Canvas Wireframe** | `Sanctuaire Mobile • Vérificateur Cryptographique Décentralisé` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Enveloppe COSE_Sign1 lue depuis la partition `EF.SIGN` de la carte.

> [!TIP]
> **Postconditions Garanties :**
> Authenticité et intégrité de la carte certifiées à 100% de manière déterministe.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Extraction du `kid` (Key ID) de 16 octets et de l'identifiant d'algorithme dans l'en-tête protégé.
2. Recherche de la clé publique correspondante dans la liste de confiance locale embarquée (Trust Store décentralisé).
3. Vérification de la validité temporelle de la clé de signature.
4. Reconstruction de la `Sig_structure` canonique et exécution de l'algorithme de vérification :
5. - Si Ed25519 (`alg: -8`) : vérification RFC 8032 ($8SB = 8R + 8kA$).
6. - Si ES256 (`alg: -7`) : vérification RFC 6979 / SEC 1 avec contrôle strict de non-malléabilité du s bas.
7. Affichage du badge solennel de certification officielle Le Pax Funèbre.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `detected_alg` | **Algorithme Utilisé** | `text` | `Ed25519 (EdDSA, alg: -8, RFC 8032)` | Algorithme | `Homologué` | ⭕ Optionnel |
| `key_kid` | **Identifiant Clé (kid)** | `text` | `3c81e592...71aa (Magasin de Confiance Local)` | kid | `De Confiance` | ⭕ Optionnel |
| `key_validity` | **Validité Clé de Signature** | `text` | `Certificat Valide (Émis par Le Pax Funèbre)` | Validité | `Active` | ⭕ Optionnel |
| `sig_result` | **Résultat Vérification** | `text` | `SIGNATURE AUTHENTIQUE (0 divergence binaire)` | Résultat | `Certifié` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_verify_crypto` | **Vérifier la Signature Cryptographique** | `primary` | `idle` | 🔐 |
| `btn_inspect_cert` | **Inspecter l'Autorité de Scellement** | `secondary` | `idle` | 📜 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Signature COSE_Sign1 100% Authentique
>
> **Badge de Conformité :** `Certifié Le Pax Funèbre`
>
> **Détail Opérationnel :** Signature Ed25519 vérifiée avec succès. Données inaltérées depuis la gravure en agence.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_COSE_INVALID_SIGNATURE` |
| **Intitulé de l'Incident** | **Signature Cryptographique Non Concordante** |
| **Condition Déclenchante** | Altération même d'un seul bit de la charge utile ou signature générée par une clé pirate. |
| **Message d'Erreur UI** | *« REJET CRYPTOGRAPHIQUE SÉVÈRE : La signature ne concorde pas avec les données de la carte. »* |
| **Action Corrective Requise** | **Carte compromise ou contrefaite. Refuser l'accès et signaler l'anomalie au réseau Le Pax Funèbre.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Sanctuaire Mobile • Vérificateur Cryptographique Décentralisé**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Enveloppe Signée en Attente de Contrôle | *En attente utilisateur* | Signature brute lue. L'oracle cryptographique local n'a pas encore validé les scalaires. |
| **2** | **Déclenchement ⚡** | Extraction de la Clé Publique & Calcul de Sig_structure | `Clic sur 'Vérifier la Signature' et consultation du magasin local` | Recherche instantanée de la clé publique de l'agence Namur dans la liste de confiance embarquée. |
| **3** | **Traitement ⚙️** | Résolution de l'Équation 8SB = 8R + 8kA (Ed25519) | `Progression : 95%` | Exécution de l'algorithme mathématique sans aucune dépendance serveur ni connexion Internet. |
| **4** | **Scellement & Fin ✨** | Sceau Doré d'Authenticité PaxFunèbre Déposé | `Statut : success` | Carte déclarée authentique. Le Sanctuaire passe en mode nominal certifié. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-302 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Enveloppe Signée en Attente de Contrôle
*Signature brute lue. L'oracle cryptographique local n'a pas encore validé les scalaires.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Oracle Cryptographique</span>
                        <span class="wf-status-badge wf-badge-neutral">En Attente de Vérification</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-crypto-icon">🔐</span>
                        <div><strong>Enveloppe COSE_Sign1 Tag 18 détectée sur EF.SIGN</strong></div>
                        <div class="wf-subtext">Algorithme déclaré : Ed25519 (alg: -8) • kid: 3c81e592...71aa</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔐 Vérifier la Signature Cryptographique</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Extraction de la Clé Publique & Calcul de Sig_structure
*Recherche instantanée de la clé publique de l'agence Namur dans la liste de confiance embarquée.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Consultation Trust Store</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Correspondance Clé Trouvée</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Clé de confiance reconnue : Le Pax Funèbre Agence Namur</div>
                        <div class="wf-subtext">Signature1 reconstruite avec external_aad vide et en-tête protégé typ</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Équation de vérification RFC 8032...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Résolution de l'Équation 8SB = 8R + 8kA (Ed25519)
*Exécution de l'algorithme mathématique sans aucune dépendance serveur ni connexion Internet.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Moteur Mathématique RFC 8032</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Vérification Équation (95%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 95%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [ED25519] Décodage de la signature 64 octets R || S : Conforme</code><br>
                        <code>> [ED25519] Vérification scalaire S < L (rejet scalaires non canoniques) : OK</code><br>
                        <code>> [ED25519] Équation 8SB == 8R + 8kA : ÉGALITÉ STRICTE (Signature valide)</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Sceau Doré d'Authenticité PaxFunèbre Déposé
*Carte déclarée authentique. Le Sanctuaire passe en mode nominal certifié.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Authenticité Certifiée</span>
                        <span class="wf-status-badge wf-badge-success">✨ Sceau Officiel Actif</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🏆</span>
                        <div>
                          <strong>Carte Mémorielle Authentifiée par Le Pax Funèbre</strong>
                          <p class="wf-subtext">Signature Ed25519 certifiée • Données inaltérées • Décision DEC-AET-04 OK</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Affichage Sanctuaire Nominal →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-303"></a>
## UC-303 : Affichage Sanctuaire, Recueillement & Livre d'Or Familial

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-303` |
| **Catégorie Métier** | **Expérience Sanctuaire** |
| **Acteur Principal** | Famille & Proches |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `Sanctuaire`, `Recueillement`, `Veilleuse`, `LivreDOr`, `Ducking14dB`, `WebAudio`, `Offline` |
| **Base Légale & Normative** | Respect de la dignité des défunts et de la vie privée mémorielle (protection des données locales sans transfert distant). |
| **Terminal / Canvas Wireframe** | `Sanctuaire Mobile • Espace de Recueillement & Livre d'Or Familial` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Carte Sanctuaire authentifiée par la vérification cryptographique (DEC-AET-04 / DEC-AET-10).

> [!TIP]
> **Postconditions Garanties :**
> Veilleuse mémorielle allumée, ambiance musicale active avec ducking vocal fluide (-14 dB), pensées de la famille scellées localement hors-ligne.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Ouverture solennelle de l'espace de recueillement avec portrait haute définition 480×480 (DEC-AET-12) et halo doré doux.
2. Formulaire interactif de recueillement : allumage d'une veilleuse mémorielle avec flamme vacillante persistante.
3. Sélection de l'ambiance musicale d'adieu (In Paradisum de Fauré, Pavane de Ravel, Silence Méditatif) en boucle harmonique.
4. Lecture du mémo vocal gravé in-silico avec ducking automatique calibré à -14 dB (baisse progressive de l'ambiance musicale au profit de la voix).
5. Saisie et recueil des pensées de la famille dans le Livre d'Or, chiffrées et stockées localement en mémoire sécurisée hors-ligne (zéro dépendance au cloud).

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `deceased_name` | **Défunt Honoré** | `text` | `Henri Dubois (1944 — 2026)` | Nom du défunt | `Certifié` | ⭕ Optionnel |
| `candle_state` | **Veilleuse Mémorielle** | `select` | `Flamme Dorée Active (Allumage Perpétuel)` | Veilleuse | `Flamme Active` | ✅ Requis |
| `music_selection` | **Ambiance Musicale d'Adieu** | `select` | `In Paradisum (G. Fauré) — Boucle Harmonique 432 Hz` | Choix musical | `Audio Actif` | ✅ Requis |
| `voice_playback` | **Mémo Vocal Silicium & Ducking** | `text` | `Témoignage Audio Opus SILK (Ducking Automatique -14 dB)` | Voix | `-14 dB Calibré` | ⭕ Optionnel |
| `guestbook_message` | **Livre d'Or Familial (Pensée)** | `textarea` | `« Ton souvenir reste une présence vivante dans la paix des bois et nos cœurs réunis. »` | Rédiger une pensée ou un hommage... | `Stockage Hors-Ligne` | ✅ Requis |
| `guestbook_author` | **Auteur du Témoignage** | `text` | `Claire & Antoine Dubois (Enfants)` | Votre nom | `Famille` | ✅ Requis |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_light_candle` | **Allumer la Veilleuse Mémorielle** | `primary` | `idle` | 🕯️ |
| `btn_listen_voice` | **Écouter le Mémo Vocal (Ducking -14 dB)** | `secondary` | `idle` | 🎙️ |
| `btn_sign_guestbook` | **Déposer une Pensée dans le Livre d'Or** | `secondary` | `idle` | ✍️ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Espace de Recueillement Éclairé & Pensée Scellée
>
> **Badge de Conformité :** `Veilleuse Active • Ducking -14 dB • Livre d'Or Hors-Ligne`
>
> **Détail Opérationnel :** Veilleuse mémorielle allumée. Ambiance musicale avec ducking vocal fluide. Hommage familial enregistré dans le coffre chiffré hors-ligne.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_GUESTBOOK_LOCAL_STORAGE_FULL` |
| **Intitulé de l'Incident** | **Mémoire Locale Sécurisée Saturée** |
| **Condition Déclenchante** | Espace de stockage local chiffré du terminal épuisé lors de l'enregistrement d'une pensée. |
| **Message d'Erreur UI** | *« Erreur de sauvegarde locale : Impossible d'ajouter le message au livre d'or hors-ligne faute d'espace disque suffisant. »* |
| **Action Corrective Requise** | **Libérer de l'espace sur l'appareil mobile ou exporter les messages précédents au format archive chiffrée.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Sanctuaire Mobile • Espace de Recueillement & Livre d'Or Familial**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Sanctuaire Mémoriel & Formulaire de Recueillement | *En attente utilisateur* | Espace de recueillement avec veilleuse éteinte, sélecteur musical et formulaire du livre d'or familial prêt à recevoir la pensée. |
| **2** | **Déclenchement ⚡** | Tap Allumage Veilleuse & Dépôt dans le Livre d'Or | `Tap sur 'Allumer la Veilleuse' et soumission de la pensée familiale` | Allumage immédiat de la flamme dorée et capture locale de la pensée de la famille. |
| **3** | **Traitement ⚙️** | Scintillement de la Flamme, Ducking Sonore -14 dB & Scellement Local | `Progression : 92%` | WebAudio applique le ducking à -14 dB sur la musique lors de la lecture vocale. Chiffrement local de la pensée. |
| **4** | **Scellement & Fin ✨** | Veilleuse Éclairée, Voix en Écoute & Livre d'Or Consigné | `Statut : success` | Sanctuaire solennel complet. La veilleuse brille, la voix résonne avec ducking, le livre d'or est scellé. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-303 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Sanctuaire Mémoriel & Formulaire de Recueillement
*Espace de recueillement avec veilleuse éteinte, sélecteur musical et formulaire du livre d'or familial prêt à recevoir la pensée.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Recueillement & Livre d'Or</span>
                        <span class="wf-status-badge wf-badge-neutral">Veilleuse en Attente</span>
                      </div>
                      <div class="wf-sanctuary-center">
                        <div class="wf-portrait-halo">👤 Portrait HD d'Henri Dubois (480x480 DEC-AET-12)</div>
                        <div class="wf-gold-title">Henri Dubois (1944 — 2026)</div>
                        <div class="wf-subtext">« Le souvenir est une présence invisible dans la paix des bois »</div>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-field-group">
                          <label class="wf-label">Veilleuse Mémorielle <span class="wf-req">*</span></label>
                          <div class="wf-select-placeholder">🕯️ Allumer la flamme perpétuelle</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Ambiance Musicale d'Adieu</label>
                          <div class="wf-select-placeholder">🎵 In Paradisum (G. Fauré) — Boucle 432 Hz</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Livre d'Or Familial (Pensée locale)</label>
                          <div class="wf-select-placeholder">« Ton souvenir reste une présence vivante... »</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🕯️ Allumer la Veilleuse Mémorielle</button>
                        <button class="wf-btn wf-btn-sub">🎙️ Mémo Vocal (Ducking -14 dB)</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Tap Allumage Veilleuse & Dépôt dans le Livre d'Or
*Allumage immédiat de la flamme dorée et capture locale de la pensée de la famille.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Allumage Mémoriel</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Flamme & Hommage Actifs</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">🕯️ Veilleuse Mémorielle Allumée • Pensée Déposée</div>
                        <div class="wf-subtext">Claire & Antoine Dubois : « Ton souvenir reste gravé dans nos cœurs »</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Allumage du sanctuaire et activation sonore...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Scintillement de la Flamme, Ducking Sonore -14 dB & Scellement Local
*WebAudio applique le ducking à -14 dB sur la musique lors de la lecture vocale. Chiffrement local de la pensée.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Moteur Audio & Livre d'Or</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Immersion Solennelle (92%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 92%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [CANDLE-SHADER] Allumage de la flamme mémorielle : Scintillement doux 120 Hz</code><br>
                        <code>> [AUDIO-DUCKING] Déclenchement voix Opus SILK : Atténuation musique à -14 dB</code><br>
                        <code>> [LOCAL-VAULT] Chiffrement de la pensée familiale en AES-GCM local hors-ligne</code><br>
                        <code>> [SYNC-ZERO] Zéro donnée transmise au réseau • Confidentialité absolue</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Veilleuse Éclairée, Voix en Écoute & Livre d'Or Consigné
*Sanctuaire solennel complet. La veilleuse brille, la voix résonne avec ducking, le livre d'or est scellé.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Espace de Recueillement Éclairé</span>
                        <span class="wf-status-badge wf-badge-success">✨ Veilleuse Allumée & Livre d'Or Scellé</span>
                      </div>
                      <div class="wf-sanctuary-full">
                        <div class="wf-portrait-circle">🕯️ 👤</div>
                        <div class="wf-gold-title">Veilleuse Perpétuelle d'Henri Dubois</div>
                        <div class="wf-epitaph-quote">« Ton souvenir reste une présence vivante dans la paix des bois »</div>
                        <div class="wf-music-indicator">🎙️ Voix d'Henri en cours d'écoute (Ducking musical -14 dB actif)</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">✍️ Ajouter une Autre Pensée au Livre d'Or</button>
                        <button class="wf-btn wf-btn-sub">📜 Directives & Volontés</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-304"></a>
## UC-304 : Bandeau de Réserve DEC-AET-07 Option B pour Émetteur Inconnu

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-304` |
| **Catégorie Métier** | **Résilience Mémorielle** |
| **Acteur Principal** | Famille & Régulateur |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `DEC-AET-07`, `ReserveBanner`, `EmetteurInconnu`, `Resilience` |
| **Base Légale & Normative** | Décision Kudoro DEC-AET-07 (Option B : Lisibilité mémorielle maintenue avec réserve réglementaire). |
| **Terminal / Canvas Wireframe** | `Sanctuaire Mobile • Bandeau de Réserve Ambré DEC-AET-07` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Carte scellée par une autorité tierce ou émetteur absent du Trust Store local.

> [!TIP]
> **Postconditions Garanties :**
> Sanctuaire affiché avec bandeau de réserve ambré explicite, conformité DEC-AET-07 respectée.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Le vérificateur cryptographique constate que la signature est mathématiquement valide mais que le `kid` ne figure pas dans la liste des autorités Le Pax Funèbre.
2. Application stricte de l'arbitrage souverain de Kudoro (Décision DEC-AET-07 Option B) :
3. - Zéro blocage aveugle : le sanctuaire mémoriel reste accessible à la famille pour préserver le souvenir.
4. - Affichage obligatoire d'un bandeau ambré solennel d'avertissement en haut d'écran : « Attention : Émetteur non référencé au réseau officiel. Données non garanties par Le Pax Funèbre ».
5. Possibilité pour l'utilisateur de consulter l'empreinte publique de l'autorité émettrice.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `sig_math_status` | **Statut de Signature** | `text` | `Mathématiquement Valide (Ed25519 OK)` | Signature | `Valide` | ⭕ Optionnel |
| `issuer_status` | **Statut Émetteur** | `text` | `ÉMETTEUR INCONNU du Magasin Local` | Émetteur | `Avertissement` | ⭕ Optionnel |
| `decision_code` | **Décision Appliquée** | `text` | `DEC-AET-07 Option B (Bandeau de Réserve Ambré)` | Décision | `Souverain` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_dismiss_banner` | **Poursuivre le Recueillement avec Avertissement** | `primary` | `idle` | ⚠️ |
| `btn_audit_unknown_key` | **Examiner la Clé Inconnue (kid)** | `secondary` | `idle` | 🔍 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Bandeau de Réserve DEC-AET-07 Option B Affiché
>
> **Badge de Conformité :** `Avertissement Réglementaire`
>
> **Détail Opérationnel :** Accès maintenu pour la famille mais non labellisé par Le Pax Funèbre.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `WARN_UNKNOWN_ISSUER_BANNER` |
| **Intitulé de l'Incident** | **Autorité de Scellement Non Certifiée** |
| **Condition Déclenchante** | Scan d'une carte valide issue d'un opérateur étranger non fédéré au réseau. |
| **Message d'Erreur UI** | *« Avertissement : La signature de cette carte n'émane pas d'une agence agréée Le Pax Funèbre. »* |
| **Action Corrective Requise** | **Contacter l'émetteur d'origine pour vérifier son affiliation ou mettre à jour la liste locale de confiance.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Sanctuaire Mobile • Bandeau de Réserve Ambré DEC-AET-07**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Détection d'une Clé Hors Liste de Confiance | *En attente utilisateur* | Signature valide mais kid non répertorié. L'arbitrage DEC-AET-07 va s'appliquer. |
| **2** | **Déclenchement ⚡** | Injection du Bandeau Ambré Réglementaire | `Application de la règle Option B avec bandeau ambré en tête` | Création du bandeau solennel en haut d'écran sans bloquer l'accès aux photos et volontés. |
| **3** | **Traitement ⚙️** | Déchiffrement Maintenu & Marquage de Réserve | `Progression : 85%` | Les volontés et photos restent lisibles pour la famille conformément au respect des proches. |
| **4** | **Scellement & Fin ✨** | Sanctuaire Affiché avec Bandeau Ambré Visible | `Statut : warning` | Équilibre parfait entre intégrité réglementaire et respect du recueillement familial. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-304 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Détection d'une Clé Hors Liste de Confiance
*Signature valide mais kid non répertorié. L'arbitrage DEC-AET-07 va s'appliquer.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Vérification de Confiance</span>
                        <span class="wf-status-badge wf-badge-alert">Clé Hors Magasin</span>
                      </div>
                      <div class="wf-device-status-box">
                        <div><strong>kid: f901b2a4...c018 absent du magasin d'agence</strong></div>
                        <div class="wf-subtext">Décision DEC-AET-07 Option B : Maintien de l'accès avec avertissement ambré</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">Appliquer DEC-AET-07 Option B</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Injection du Bandeau Ambré Réglementaire
*Création du bandeau solennel en haut d'écran sans bloquer l'accès aux photos et volontés.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Décision DEC-AET-07</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Déploiement Bandeau Ambré</span>
                      </div>
                      <div class="wf-alert-card wf-alert-amber wf-radar-pulse">
                        <div class="wf-trigger-indicator">⚠️ AVERTISSEMENT : Émetteur Non Référencé</div>
                        <div class="wf-subtext">Signature mathématique valide mais autorité inconnue de Le Pax Funèbre</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Poursuite avec réserve...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Déchiffrement Maintenu & Marquage de Réserve
*Les volontés et photos restent lisibles pour la famille conformément au respect des proches.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Traitement de Réserve</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Affichage Adapté (85%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 85%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [DEC-AET-07] Option B sélectionnée par Kudoro : Pas de blocage noir</code><br>
                        <code>> [UI-BANNER] Bandeau d'avertissement ambré fixé en position haute</code><br>
                        <code>> [MEDIA] Décodage des souvenirs maintenu pour les proches</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Sanctuaire Affiché avec Bandeau Ambré Visible
*Équilibre parfait entre intégrité réglementaire et respect du recueillement familial.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Accès Sous Réserve</span>
                        <span class="wf-status-badge wf-badge-alert">⚠️ Émetteur Tiers</span>
                      </div>
                      <div class="wf-banner-amber-top">
                        ⚠️ <strong>Émetteur Non Certifié PaxFunèbre :</strong> Données lisibles sous réserve légale.
                      </div>
                      <div class="wf-sanctuary-center">
                        <div class="wf-portrait-circle">👤</div>
                        <div class="wf-gold-title">Henri Dubois (1944 — 2026)</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-sub">Détails de l'Autorité Inconnue ↗</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-305"></a>
## UC-305 : Blocage Hermétique sur Carte Falsifiée ou Clé Révoquée

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-305` |
| **Catégorie Métier** | **Sécurité & Anti-Fraude** |
| **Acteur Principal** | Système Mobile & Auditeur |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `Blocage`, `Falsification`, `Revocation`, `AntiFraude`, `AlerteRouge` |
| **Base Légale & Normative** | Code pénal belge (art. 196 et suivants - faux en écriture et usage de faux). |
| **Terminal / Canvas Wireframe** | `Sanctuaire Mobile • Bouclier Hermétique Anti-Falsification` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Carte scannée portant des données altérées ou signée par une clé révoquée.

> [!TIP]
> **Postconditions Garanties :**
> Accès hermétiquement verrouillé, alerte rouge de falsification affichée sans fuite de données.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Le vérificateur cryptographique exécute l'algorithme de contrôle de signature.
2. Constat d'une anomalie critique :
3. - Soit la signature mathématique échoue (un octet au moins a été modifié après signature).
4. - Soit le `kid` correspond à une clé officielle compromise déclarée sur la liste noire de révocation.
5. Bascule immédiate et irréversible en écran de blocage hermétique rouge sombre.
6. Refus catégorique de délivrer les textes ou médias mémoriels pour empêcher toute usurpation.
7. Consignation d'un incident de sécurité chiffré dans le journal d'audit local.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `sig_status` | **Statut Cryptographique** | `text` | `ÉCHEC MAJEUR (Signature Invalide ou Clé Révoquée)` | Statut | `ALERTE ROUGE` | ⭕ Optionnel |
| `rejection_cause` | **Cause du Rejet** | `text` | `Altération binaire post-signature ou clé d'autorité compromise` | Cause | `Faux Détecté` | ⭕ Optionnel |
| `security_policy` | **Politique de Sécurité** | `text` | `BLOCAGE HERMÉTIQUE (Zéro affichage de données)` | Politique | `Zéro Fuite` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_close_session` | **Fermer la Session de Sécurité** | `danger` | `idle` | 🛑 |
| `btn_export_audit_log` | **Exporter Rapport d'Incident** | `secondary` | `idle` | 📄 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Bouclier Anti-Fraude Opérationnel
>
> **Badge de Conformité :** `Hermétique 100%`
>
> **Détail Opérationnel :** Aucune donnée compromise n'a été affichée. Incident consigné au journal d'audit.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_CARD_FALSIFIED_OR_REVOKED` |
| **Intitulé de l'Incident** | **Carte Falsifiée ou Clé d'Autorité Révoquée** |
| **Condition Déclenchante** | Non-concordance de l'équation mathématique ou clé révoquée pour compromission. |
| **Message d'Erreur UI** | *« BLOCAGE DE SÉCURITÉ INVIOLABLE : Cette carte présente une signature invalide ou une altération de données. Accès formellement refusé. »* |
| **Action Corrective Requise** | **Contacter immédiatement l'agence émettrice pour expertise physique de la carte silicium.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Sanctuaire Mobile • Bouclier Hermétique Anti-Falsification**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Données en Cours d'Analyse Cryptographique | *En attente utilisateur* | Signature en cours de décodage. L'anomalie de signature n'est pas encore révélée. |
| **2** | **Déclenchement ⚡** | Détection d'un Bit Corrompu & Claquage du Verrou Rouge | `Échec de l'équation RFC 8032 ou correspondance avec la liste de révocation` | Bascule instantanée en alerte critique rouge sombre avec arrêt de tout rendu. |
| **3** | **Traitement ⚙️** | Effacement Mémoire & Journalisation de l'Incident | `Progression : 100%` | Purge immédiate des tampons mémoire vive pour empêcher toute exfiltration de données. |
| **4** | **Scellement & Fin ✨** | Écran Rouge Hermétique : Accès Bloqué | `Statut : alert` | Refus absolu d'accès. La dignité et la sécurité de la mémoire sont protégées contre les faux. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-305 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Données en Cours d'Analyse Cryptographique
*Signature en cours de décodage. L'anomalie de signature n'est pas encore révélée.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Audit de Sécurité</span>
                        <span class="wf-status-badge wf-badge-neutral">Contrôle en Cours</span>
                      </div>
                      <div class="wf-device-status-box">
                        <div><strong>Analyse mathématique de la signature Ed25519...</strong></div>
                        <div class="wf-subtext">Comparaison du hash de charge utile avec la Sig_structure</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">Exécuter Contrôle d'Intégrité</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Détection d'un Bit Corrompu & Claquage du Verrou Rouge
*Bascule instantanée en alerte critique rouge sombre avec arrêt de tout rendu.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Alerte Falsification</span>
                        <span class="wf-status-badge wf-badge-alert">🛑 ÉCHEC DE SIGNATURE</span>
                      </div>
                      <div class="wf-alert-card wf-alert-red wf-radar-pulse">
                        <div class="wf-trigger-indicator">🛑 ALERTE ROUGE : Altération Binaire Détectée</div>
                        <div class="wf-subtext">La signature ne correspond pas à la clé d'autorité PaxFunèbre</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-danger wf-pulse-btn">Verrouillage de sécurité actif...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Effacement Mémoire & Journalisation de l'Incident
*Purge immédiate des tampons mémoire vive pour empêcher toute exfiltration de données.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Purge Mémoire Sécurisée</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Purge Hermétique (100%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 100%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [SECURITY-ALERT] Invalidation immédiate des données mémoires : PURGE OK</code><br>
                        <code>> [AUDIT-LOG] Incident INC-2026-FALSIF consigné dans le journal chiffré</code><br>
                        <code>> [UI-LOCKOUT] Verrouillage hermétique de l'interface en écran rouge</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Écran Rouge Hermétique : Accès Bloqué
*Refus absolu d'accès. La dignité et la sécurité de la mémoire sont protégées contre les faux.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Accès Interdit</span>
                        <span class="wf-status-badge wf-badge-alert">🛑 Carte Rejetée</span>
                      </div>
                      <div class="wf-alert-box-full">
                        <span class="wf-alert-icon">🚫</span>
                        <strong>CARTE NON AUTHENTIQUE OU FALSIFIÉE</strong>
                        <p class="wf-subtext">Les signatures cryptographiques sont invalides. Aucun média ne peut être restitué.</p>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-danger">Fermer la Session</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-306"></a>
## UC-306 : Sanctuaire Acoustique & Ducking Vocal Vivant Automatique

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-306` |
| **Catégorie Métier** | **Expérience Émotionnelle** |
| **Acteur Principal** | Famille & Proches |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `Ducking`, `WebAudio`, `AudioMixer`, `Voix`, `Emotion` |
| **Base Légale & Normative** | Directives déontologiques funéraires relatives à la dignité et au respect des cérémonies. |
| **Terminal / Canvas Wireframe** | `Sanctuaire Mobile • Processeur Acoustique & Ducking Vocal` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Musique d'ambiance en cours de lecture et message vocal disponible.

> [!TIP]
> **Postconditions Garanties :**
> Immersion sonore réussie, harmonie acoustique digne et respectueuse de l'émotion familiale.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. L'utilisateur clique sur le bouton de lecture du témoignage vocal « Écouter la Voix du Défunt ».
2. Le processeur WebAudio active instantanément le compresseur/ducking automatique :
3. - Atténuation fluide du volume musical de fond de 100% à -14 dB en 400 millisecondes.
4. - Lancement prioritaire de la voix au premier plan sonore à niveau solennel clair.
5. Affichage simultané d'un oscilloscope lumineux synchronisé avec la vibration vocale.
6. À la fin de la parole, rétablissement doux du volume musical d'ambiance en 1 200 millisecondes (fade-up).

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `bg_music` | **Piste Musique de Fond** | `text` | `Gabriel Fauré — In Paradisum (Volume actuel : -14 dB)` | Musique | `Atténuée` | ⭕ Optionnel |
| `voice_state` | **Témoignage Vocal** | `text` | `Lecture en cours : 00:14 / 00:30 (Premier Plan)` | Voix | `Prioritaire` | ⭕ Optionnel |
| `duck_attack` | **Attaque Ducking DSP** | `text` | `400 ms (Descente douce)` | Attaque | `DSP` | ⭕ Optionnel |
| `duck_release` | **Relâchement Ducking** | `text` | `1 200 ms (Remontée progressive en fin de voix)` | Relâchement | `DSP` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_pause_voice` | **⏸ Mettre la Voix en Pause** | `primary` | `active` | ⏸ |
| `btn_mute_all` | **Silence Solennel Immédiat** | `secondary` | `idle` | 🔇 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Ducking Vocal Actif & Parfaitement Calibré
>
> **Badge de Conformité :** `DSP WebAudio -14 dB`
>
> **Détail Opérationnel :** Musique atténuée avec élégance. Voix chaleureuse et solennelle au premier plan.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_WEBAUDIO_AUTOPLAY_BLOCKED` |
| **Intitulé de l'Incident** | **Politique de Lecture Automatique Bloquée** |
| **Condition Déclenchante** | Navigateur mobile bloquant l'audio sans interaction tactile préalable de l'utilisateur. |
| **Message d'Erreur UI** | *« Erreur audio : Le navigateur requiert un geste tactile pour autoriser la restitution sonore. »* |
| **Action Corrective Requise** | **Toucher l'écran pour débloquer le contexte WebAudio et lancer le sanctuaire sonore.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Sanctuaire Mobile • Processeur Acoustique & Ducking Vocal**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Musique de Fond Seule à 100% du Volume | *En attente utilisateur* | In Paradisum joue à volume normal. Le bouton du témoignage vocal attend d'être pressé. |
| **2** | **Déclenchement ⚡** | Clic sur 'Écouter la Voix' & Déclenchement de l'Atténuateur | `Clic tactile sur le lecteur de voix déclenchant la rampe de ducking` | Envoi du signal DSP au nœud de gain de la musique pour descente à -14 dB en 400 ms. |
| **3** | **Traitement ⚙️** | Oscilloscope Vocal Actif & Musique Douce en Fond | `Progression : 50%` | La forme d'onde vocale vibre en rythme au centre de l'écran, soutenue par le fond orchestral. |
| **4** | **Scellement & Fin ✨** | Fin de Parole & Rétablissement Musique (Fade-Up 1.2s) | `Statut : success` | Le message d'adieu s'achève avec émotion, la musique remonte doucement au premier plan. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-306 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Musique de Fond Seule à 100% du Volume
*In Paradisum joue à volume normal. Le bouton du témoignage vocal attend d'être pressé.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Ambiance Seule</span>
                        <span class="wf-status-badge wf-badge-neutral">Musique à 100%</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-music-icon">🎵</span>
                        <div><strong>Musique d'ambiance active (Fauré)</strong></div>
                        <div class="wf-subtext">Témoignage vocal de 30 secondes prêt pour écoute</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🎙️ Écouter le Témoignage Vocal (Ducking)</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Clic sur 'Écouter la Voix' & Déclenchement de l'Atténuateur
*Envoi du signal DSP au nœud de gain de la musique pour descente à -14 dB en 400 ms.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Enclenchement Ducking</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Atténuation Musique (-14 dB)</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">⚡ Descente du gain musical : 100% -> 20% (-14 dB)</div>
                        <div class="wf-subtext">Lancement immédiat du flux vocal au premier plan</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Écoute vocale en cours...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Oscilloscope Vocal Actif & Musique Douce en Fond
*La forme d'onde vocale vibre en rythme au centre de l'écran, soutenue par le fond orchestral.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Lecture Vocale</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Parole Active (15s / 30s)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 50%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [DSP-DUCK] Musique atténuée maintenue à -14.0 dBFS</code><br>
                        <code>> [VOICE-DSP] Niveau vocal RMS : -23 LUFS clair et solennel</code><br>
                        <code>> [OSCILLO] FFT 256 bandes animée en direct</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Fin de Parole & Rétablissement Musique (Fade-Up 1.2s)
*Le message d'adieu s'achève avec émotion, la musique remonte doucement au premier plan.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Message Conclu</span>
                        <span class="wf-status-badge wf-badge-success">✨ Rétablissement Musique</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🎙️</span>
                        <div>
                          <strong>Témoignage Vocal Écouté dans le Recueillement</strong>
                          <p class="wf-subtext">La musique d'ambiance reprend doucement son volume pour clore l'hommage</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Consultation des Volontés →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-307"></a>
## UC-307 : Consultation des Volontés Civiles et Funéraires

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-307` |
| **Catégorie Métier** | **Dernières Volontés** |
| **Acteur Principal** | Famille, Exécuteur Testamentaire & Pompes Funèbres |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `Volontes`, `Loi1971`, `Sepulture`, `ArbreCineraire`, `Preuve` |
| **Base Légale & Normative** | Loi du 20 juillet 1971 sur les funérailles et sépultures (art. 2 - primauté absolue des volontés) (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `Sanctuaire Mobile • Acte des Volontés Civiles Scellé` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Carte Directives (Carte 2) scannée par un membre de la famille ou le conseiller.

> [!TIP]
> **Postconditions Garanties :**
> Dernières volontés du défunt portées à la connaissance des héritiers avec valeur probante légale.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Sélection de l'onglet 'Volontés Civiles & Funéraires' dans l'application mobile.
2. Déchiffrement local de la structure CBOR des volontés enregistrées lors du Bon à Tirer.
3. Affichage solennel des choix formulés :
4. - Cérémonie laïque civile sans fleurs artificielles.
5. - Sépulture par sarcomusation avec restitution des amendements en forêt cinéraire (Démonstrateur de faisabilité prospectif — Option non autorisée par le droit positif actuel (référence à confirmer par un juriste)).
6. - Désignation de l'Arbre Mémoriel n° F-2408 dans le massif forestier ardennais agréé.
7. Génération d'une copie numérique certifiée infalsifiable opposable à toute contestation (sous réserve de conformité, référence à confirmer par un juriste).

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `wills_ceremony` | **Cérémonie Souhaitée** | `text` | `Cérémonie Civile Laïque sous les Arbres` | Cérémonie | `Loi 1971 (référence à confirmer par un juriste)` | ⭕ Optionnel |
| `wills_burial` | **Mode de Sépulture** | `text` | `Sarcomusation & Retour en Forêt Cinéraire (Démonstrateur de faisabilité prospectif — Option non autorisée par le droit positif actuel (référence à confirmer par un juriste))` | Sépulture | `Démonstrateur Prospectif` | ⭕ Optionnel |
| `wills_tree` | **Arbre Cinéraire Désigné** | `text` | `Chêne du Souvenir n° F-2408 (Forêt Saint-Hubert)` | Arbre | `Cadastré` | ⭕ Optionnel |
| `wills_timestamp` | **Horodatage Légal Scellé** | `text` | `2026-10-04T15:30:00Z (Double Émargement Certifié)` | Horodatage | `Inviolable` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_export_wills_pdf` | **Télécharger l'Acte des Volontés (PDF)** | `primary` | `idle` | 📄 |
| `btn_view_signatories` | **Vérifier Signatures Mandataire** | `secondary` | `idle` | ✍️ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Volontés Civiles Consultables en Lecture Seule
>
> **Badge de Conformité :** `Valeur Probante Légale`
>
> **Détail Opérationnel :** Texte intègre conforme à la loi du 20 juillet 1971 (référence à confirmer par un juriste). Inaltérable in-silico.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_POSTMORTEM_ACCESS_DENIED` |
| **Intitulé de l'Incident** | **Opposition Formelle à la Divulgation** |
| **Condition Déclenchante** | Clause de confidentialité post-mortem stipulée expressément par le défunt. |
| **Message d'Erreur UI** | *« Accès restreint : Le défunt a expressément stipulé que ces volontés ne soient communiquées qu'à l'exécuteur testamentaire désigné. »* |
| **Action Corrective Requise** | **Présenter le badge professionnel de l'exécuteur testamentaire ou la clé notariée habilitée.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Sanctuaire Mobile • Acte des Volontés Civiles Scellé**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Volet des Volontés Non Déployé | *En attente utilisateur* | Menu principal affiché. L'utilisateur clique sur 'Consulter les Dernières Volontés'. |
| **2** | **Déclenchement ⚡** | Ouverture du Compartiment Légal & Déchiffrement | `Clic sur 'Consulter les Dernières Volontés' et décompression CBOR` | Déchiffrement instantané des clauses funéraires avec contrôle de signature. |
| **3** | **Traitement ⚙️** | Mise en Page Solennelle & Contrôle de Primauté | `Progression : 95%` | Application de la typographie solennelle et vérification des références aux lois belges. |
| **4** | **Scellement & Fin ✨** | Acte des Volontés Affiché en Lecture Seule | `Statut : success` | Document probant consultable et téléchargeable pour exécution immédiate. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-307 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Volet des Volontés Non Déployé
*Menu principal affiché. L'utilisateur clique sur 'Consulter les Dernières Volontés'.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Carte Directives</span>
                        <span class="wf-status-badge wf-badge-neutral">Menu Principal</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-wills-icon">📜</span>
                        <div><strong>Dernières Volontés Civiles & Funéraires</strong></div>
                        <div class="wf-subtext">Scellées le 04/10/2026 par Claire Dubois et Le Pax Funèbre</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">📜 Consulter les Dernières Volontés</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Ouverture du Compartiment Légal & Déchiffrement
*Déchiffrement instantané des clauses funéraires avec contrôle de signature.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Déchiffrement Légal</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Décompression Acte</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Acte de dernières volontés authentifié</div>
                        <div class="wf-subtext">Affichage des dispositions relatives à la cérémonie et à la sépulture</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Affichage de l'acte formel...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Mise en Page Solennelle & Contrôle de Primauté
*Application de la typographie solennelle et vérification des références aux lois belges.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Mise en Page Juridique</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Rendu Légal (95%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 95%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [WILLS-RENDER] Clause 1 : Cérémonie civile laïque -> VALIDÉ</code><br>
                        <code>> [WILLS-RENDER] Clause 2 : Sarcomusation (Démonstrateur de faisabilité prospectif) & Forêt cinéraire -> VALIDÉ</code><br>
                        <code>> [LAW-1971] Primauté légale de la volonté du défunt confirmée (référence à confirmer par un juriste)</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Acte des Volontés Affiché en Lecture Seule
*Document probant consultable et téléchargeable pour exécution immédiate.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Acte des Volontés</span>
                        <span class="wf-status-badge wf-badge-success">✨ Conforme Loi 1971 (référence à confirmer par un juriste)</span>
                      </div>
                      <div class="wf-wills-card-view">
                        <div><strong>Cérémonie :</strong> Laïque solennelle sous les arbres</div>
                        <div><strong>Sépulture :</strong> Sarcomusation & Arbre F-2408 <span class="wf-badge-warning">[Démonstrateur de faisabilité prospectif — Option non autorisée par le droit positif actuel (référence à confirmer par un juriste)]</span></div>
                        <div><strong>Message :</strong> « Que la nature accueille ma mémoire en paix... »</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">📄 Télécharger l'Acte Certifié (PDF)</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-308"></a>
## UC-308 : Fiche d'Urgence Médicale Interactive & Alerte Pacemaker (Art. L1232-24 CDLD & Modèle IIIC réglementaire)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-308` |
| **Catégorie Métier** | **Directives Médicales & Sécurité** |
| **Acteur Principal** | Secouristes, Urgentistes, Pompes Funèbres & Médecin Légiste |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `UrgenceMedicale`, `Secouristes`, `Pacemaker`, `DonOrganes`, `DAE`, `CDLD`, `AppelUrgence` |
| **Base Légale & Normative** | Art. L1232-24 CDLD & Modèle IIIC réglementaire (exérèse obligatoire des stimulateurs cardiaques) et loi belge sur le don d'organes de 1986. |
| **Terminal / Canvas Wireframe** | `Sanctuaire Mobile • Fiche d'Urgence Médicale Secouristes (Scan Directives)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Scan NFC instantané de la Carte Directives par un secouriste, urgentiste ou agent funéraire habilité (Zéro Login requis).

> [!TIP]
> **Postconditions Garanties :**
> Fiche d'urgence médicale consultée, alerte d'exérèse pacemaker levée ou confirmée, protocole de don d'organes engagé et sécurité des intervenants garantie.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Scan NFC immédiat de la Carte Directives civile & médicale sans aucun identifiant ni mot de passe (zéro login d'urgence pour secouristes).
2. Ouverture instantanée de la Fiche d'Urgence Médicale Interactive sur le terminal mobile des secouristes ou urgentistes.
3. Alerte immédiate exérèse stimulateur cardiaque / pacemaker : affichage rouge vif du danger d'explosion thermique (> 250°C), attestation chirurgicale d'exérèse (Dr. Marc Vaneck) avec rappel de l'Art. L1232-24 CDLD & Modèle IIIC réglementaire.
4. Affichage direct du statut de consentement ou refus du don d'organes (cadre légal du consentement présumé de la loi de 1986).
5. Mise à disposition immédiate de boutons d'appel d'urgence (SAMU 112, médecin certificateur) et des consignes post-mortem d'urgence (maintien chambre froide 4°C, délai d'exérèse < 24h, interdiction formelle de crémation sans visa).

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `emergency_trigger` | **Déclencheur d'Urgence** | `text` | `Scan Immédiat Carte Directives (NFC Tap Zéro-Login Secouriste)` | Déclencheur | `Priorité Vitale` | ⭕ Optionnel |
| `pacemaker_alert` | **Alerte Stimulateur (Pacemaker / DAE)** | `text` | `PRÉSENCE CONFIRMÉE — Risque Explosion Thermique (> 250°C)` | Implant | `ALERTE ROUGE` | ✅ Requis |
| `removal_cert` | **Statut Exérèse Chirurgicale** | `text` | `CERTIFIÉ RETIRÉ (Dr. Marc Vaneck — INAMI 1-40912-88-004)` | Exérèse | `Exérèse Conforme` | ✅ Requis |
| `organ_donation` | **Directives Don d'Organes (Loi 1986)** | `select` | `Consentement Plein et Entier Confirmé` | Don organes | `Loi 1986` | ✅ Requis |
| `emergency_contacts` | **Appels d'Urgence Rapides** | `text` | `SAMU 112 • Dr. Marc Vaneck (+32 81 22 33 44)` | Contacts | `Liaison Directe` | ⭕ Optionnel |
| `post_mortem_instructions` | **Consignes Post-Mortem d'Urgence** | `text` | `Chambre froide 4°C • Délai légal exérèse < 24h • Interdiction crémation sans visa` | Consignes | `Consignes Pro` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_call_emergency_112` | **Appel d'Urgence Immédiat (112)** | `primary` | `idle` | 🚨 |
| `btn_call_doctor_vaneck` | **Appeler Dr. Vaneck (Médecin)** | `secondary` | `idle` | 📞 |
| `btn_view_full_medical_cert` | **Consulter Visa Exérèse Médical** | `secondary` | `idle` | 🩺 |
| `btn_view_organ_protocol` | **Protocole Don d'Organes** | `secondary` | `idle` | 🫀 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Fiche d'Urgence Médicale Secouriste Validée
>
> **Badge de Conformité :** `Alerte Pacemaker Levée • Don d'Organes Notifié`
>
> **Détail Opérationnel :** Scan Carte Directives réussi. Visa d'exérèse vérifié conforme. Statut don d'organes communiqué pour protocole d'urgence.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_PACEMAKER_NOT_REMOVED_CRITICAL` |
| **Intitulé de l'Incident** | **Alerte Rouge : Pacemaker Présent Non Retiré** |
| **Condition Déclenchante** | Défunt porteur d'un stimulateur sans certificat médical d'exérèse renseigné. |
| **Message d'Erreur UI** | *« DANGER DE MORT / EXPLOSION : Pacemaker actif non retiré. Manipulation, transport thermique et crémation formellement interdits (Art. L1232-24 CDLD & Modèle IIIC réglementaire). »* |
| **Action Corrective Requise** | **Interdire immédiatement toute opération thermique. Contacter le médecin requis pour exérèse chirurgicale d'urgence.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Sanctuaire Mobile • Fiche d'Urgence Médicale Secouristes (Scan Directives)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Terminal Secouriste / Urgentiste en Écoute NFC | *En attente utilisateur* | Fiche d'urgence en attente de présentation de la Carte Directives. Scan zéro-login prêt pour secouristes. |
| **2** | **Déclenchement ⚡** | Scan Immédiat de la Carte Directives & Alerte Prioritaire | `NFC Tap de la Carte Directives civile & médicale sans contact` | Détection instantanée de la partition d'urgence et affichage prioritaire de la bannière rouge vif. |
| **3** | **Traitement ⚙️** | Contrôle Visa Exérèse & Directives Don d'Organes (< 150 ms) | `Progression : 98%` | Vérification in-silico du certificat d'exérèse du Dr. Vaneck et du consentement don d'organes (Loi 1986). |
| **4** | **Scellement & Fin ✨** | Fiche d'Urgence Médicale Complète & Boutons d'Appel Actifs | `Statut : success` | Fiche d'urgence validée. Sécurité garantie contre l'explosion, protocole don d'organes prêt, boutons d'appel 112 opérationnels. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-308 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Terminal Secouriste / Urgentiste en Écoute NFC
*Fiche d'urgence en attente de présentation de la Carte Directives. Scan zéro-login prêt pour secouristes.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Fiche d'Urgence Secouriste</span>
                        <span class="wf-status-badge wf-badge-neutral">En Attente de Scan</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-alert-icon">🚨</span>
                        <div><strong>Scan Immédiat Carte Directives (Zéro-Login Secouriste)</strong></div>
                        <div class="wf-subtext">Approchez la Carte Directives pour affichage instantané de l'état vital et des volontés</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🚨 Scanner Carte Directives d'Urgence</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Scan Immédiat de la Carte Directives & Alerte Prioritaire
*Détection instantanée de la partition d'urgence et affichage prioritaire de la bannière rouge vif.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Alerte Vitale Prioritaire</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Carte Détectée en 42ms</span>
                      </div>
                      <div class="wf-alert-card wf-alert-red wf-radar-pulse">
                        <div class="wf-trigger-indicator">⚠️ FICHE D'URGENCE MÉDICALE : Stimulateur Cardiaque Détecté</div>
                        <div class="wf-subtext">Vérification prioritaire de l'exérèse chirurgicale et des volontés de don d'organes</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-danger wf-pulse-btn">Contrôle du visa d'exérèse & directives...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Contrôle Visa Exérèse & Directives Don d'Organes (< 150 ms)
*Vérification in-silico du certificat d'exérèse du Dr. Vaneck et du consentement don d'organes (Loi 1986).*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Moteur d'Urgence Médicale</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Contrôle In-Silico (98%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 98%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [NFC-FAST] Directive Card AID A00000084501 détectée en 42ms</code><br>
                        <code>> [PACEMAKER-ALERT] Stimulateur actif identifié • Recherche visa chirurgical...</code><br>
                        <code>> [VISA-CHECK] Attestation Dr. Marc Vaneck INAMI 1-40912-88-004 : EXÉRÈSE VALIDÉE</code><br>
                        <code>> [ORGAN-DONATION] Position lue : Consentement confirmé (Loi 1986)</code><br>
                        <code>> [SAFETY-CLEAR] Feu vert opérationnel accordé aux secouristes et opérateurs</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Fiche d'Urgence Médicale Complète & Boutons d'Appel Actifs
*Fiche d'urgence validée. Sécurité garantie contre l'explosion, protocole don d'organes prêt, boutons d'appel 112 opérationnels.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Fiche d'Urgence Médicale Validée</span>
                        <span class="wf-status-badge wf-badge-success">✨ Exérèse Conforme & Don Notifié</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🩺</span>
                        <div>
                          <strong>Exérèse Chirurgicale Conforme (Dr. Marc Vaneck)</strong>
                          <p class="wf-subtext">Art. L1232-24 CDLD & Modèle IIIC réglementaire • Don d'organes : Consentement validé (Loi 1986)</p>
                        </div>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-field-group">
                          <label class="wf-label">Appels d'Urgence Directs</label>
                          <div class="wf-select-placeholder">🚨 SAMU 112 • Dr. Vaneck (+32 81 22 33 44)</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Consigne Post-Mortem</label>
                          <div class="wf-select-placeholder">Conservation chambre froide 4°C (délai &lt; 24h)</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🚨 Appel SAMU 112</button>
                        <button class="wf-btn wf-btn-sub">📞 Dr. Vaneck</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-309"></a>
## UC-309 : Consultation du Statut de Don d'Organes (Consentement Présumé Loi 1986)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-309` |
| **Catégorie Métier** | **Directives Médicales** |
| **Acteur Principal** | Coordinateur Hospitalier de Transplantation |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `DonOrganes`, `Loi1986`, `Greffe`, `Transplantation`, `SPF` |
| **Base Légale & Normative** | Loi du 13 juin 1986 sur le prélèvement et la transplantation d'organes (art. 10 - consentement présumé). |
| **Terminal / Canvas Wireframe** | `Sanctuaire Mobile • Directives Hospitalières Don d'Organes` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Carte Directives présentée au coordinateur de prélèvement d'organes d'un CHU.

> [!TIP]
> **Postconditions Garanties :**
> Volonté du défunt respectée sans ambiguïté, facilitation du travail urgent des équipes de greffe.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Scan de la carte par le praticien de coordination des greffes hospitalières.
2. Accès immédiat et sans mot de passe au compartiment 'Don d'Organes et Tissus Humains'.
3. Affichage de la déclaration formelle de la personne :
4. - Soit confirmation expresse et volontaire de consentement (cornées, reins, foie, cœur).
5. - Soit enregistrement d'une opposition formelle de son vivant.
6. Rappel des dispositions de la loi belge du 13 juin 1986 (régime de l'opt-out / consentement présumé).
7. Édition d'un bordereau de traçabilité officiel annexé au dossier de prélèvement.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `organ_law` | **Régime Légal Belge** | `text` | `Loi du 13 juin 1986 (Consentement Présumé Opt-Out)` | Loi | `Loi 1986` | ⭕ Optionnel |
| `organ_status` | **Volonté Enregistrée** | `text` | `CONSENTEMENT EXPRÈS CONFIRMÉ in-silico` | Volonté | `Donneur Actif` | ⭕ Optionnel |
| `organ_types` | **Tissus & Organes Autorisés** | `text` | `Cornées, Reins, Foie, Poumons, Cœur` | Organes | `Multi-Dons` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_certify_organ_status` | **Délivrer le Visa de Consultation Médicale** | `primary` | `idle` | ❤️ |
| `btn_spf_verify` | **Vérifier Registre Central SPF Santé** | `secondary` | `idle` | 🏥 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Directives de Don d'Organes Validées
>
> **Badge de Conformité :** `Loi 13 juin 1986`
>
> **Détail Opérationnel :** Consentement exprès confirmé in-silico. Consultation consignée au dossier médical.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_DONATION_OPPOSITION_FOUND` |
| **Intitulé de l'Incident** | **Opposition Formelle au Don d'Organes** |
| **Condition Déclenchante** | La carte contient une mention d'opposition formelle expresse enregistrée par le défunt. |
| **Message d'Erreur UI** | *« OPPOSITION FORMELLE ENREGISTRÉE : Le défunt s'est expressément opposé au prélèvement de ses organes de son vivant. Tout prélèvement est pénalement interdit. »* |
| **Action Corrective Requise** | **Respecter impérativement la volonté d'opposition du défunt et clore la procédure de transplantation.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Sanctuaire Mobile • Directives Hospitalières Don d'Organes**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Coordinateur Médical Approchant la Carte Directives | *En attente utilisateur* | Urgence hospitalière. Le praticien vérifie si le défunt s'est opposé au don d'organes. |
| **2** | **Déclenchement ⚡** | Scan NFC & Lecture du Compartiment Don d'Organes | `Lecture NFC par le coordinateur hospitalier en salle de réanimation` | Décodage en 30 millisecondes de la volonté enregistrée sur la puce ACOSJ. |
| **3** | **Traitement ⚙️** | Confrontation au Cadre Légal du Consentement Présumé | `Progression : 95%` | Vérification de l'absence de clause d'opposition et validation pour l'équipe de transplantation. |
| **4** | **Scellement & Fin ✨** | Fiche Médicale de Don Validée | `Statut : success` | Attestation hospitalière générée pour l'équipe chirurgicale de prélèvement. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-309 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Coordinateur Médical Approchant la Carte Directives
*Urgence hospitalière. Le praticien vérifie si le défunt s'est opposé au don d'organes.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Coordination Greffes</span>
                        <span class="wf-status-badge wf-badge-neutral">Urgence Médicale</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-heart-icon">❤️</span>
                        <div><strong>Vérification Immédiate du Statut de Don d'Organes</strong></div>
                        <div class="wf-subtext">Loi belge du 13 juin 1986 • Accès instantané sans mot de passe</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">Consulter Directives Don d'Organes</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Scan NFC & Lecture du Compartiment Don d'Organes
*Décodage en 30 millisecondes de la volonté enregistrée sur la puce ACOSJ.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Lecture Directives</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Décodage Immédiat</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Déclaration expresse trouvée in-silico</div>
                        <div class="wf-subtext">Consentement plein et entier confirmé de son vivant par Henri Dubois</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Génération du visa médical...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Confrontation au Cadre Légal du Consentement Présumé
*Vérification de l'absence de clause d'opposition et validation pour l'équipe de transplantation.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Contrôle Légal Don</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Contrôle Loi 1986 (95%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 95%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [ORGAN-CHECK] Absence formelle d'opposition confirmée</code><br>
                        <code>> [ORGAN-CHECK] Volonté positive de don exprimée : Cornées, Reins</code><br>
                        <code>> [LAW-1986] Cadre légal respecté : Prélèvement thérapeutique autorisé</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Fiche Médicale de Don Validée
*Attestation hospitalière générée pour l'équipe chirurgicale de prélèvement.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Fiche de Don Émise</span>
                        <span class="wf-status-badge wf-badge-success">✨ Don d'Organes Confirmé</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">❤️</span>
                        <div>
                          <strong>Consentement Exprès Confirmé in-silico</strong>
                          <p class="wf-subtext">Volonté solennelle du défunt respectée • Visa de coordination émis</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Legs du Corps à la Science →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-310"></a>
## UC-310 : Directives Legs du Corps à la Science sous 48h

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-310` |
| **Catégorie Métier** | **Directives Médicales** |
| **Acteur Principal** | Famille & Faculté de Médecine |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `LegsCorps`, `Science`, `Universite`, `Delai48h`, `Anatomie` |
| **Base Légale & Normative** | Décret wallon et arrêtés royaux régissant le don de corps à l'enseignement anatomique universitaire (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `Sanctuaire Mobile • Protocole d'Urgence Legs à la Science (48h)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Convention de legs du corps conclue de son vivant avec une université belge.

> [!TIP]
> **Postconditions Garanties :**
> Procédure de legs notifiée, respect impératif du délai des 48h garanti par l'application.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Affichage des directives d'urgence en cas de legs du corps à la science.
2. Rappel impératif du délai légal absolu : le transport de corps vers le laboratoire d'anatomie doit intervenir dans les 48 heures ouvrées post-mortem.
3. Affichage des coordonnées directes d'astreinte 24h/24 de la faculté de médecine conventionnée (ULiège, UCLouvain, ULB).
4. Notification des pièces administratives requises (certificat de décès modèle IIIC et convention originale signée).
5. Bouton d'appel d'urgence du service de transport anatomique conventionné.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `med_university` | **Faculté Conventionnée** | `text` | `Université de Liège (ULiège) — Laboratoire d'Anatomie` | Université | `Conventionné` | ⭕ Optionnel |
| `legal_delay` | **Délai Légal Impératif** | `text` | `48 HEURES MAXIMALES ouvrées post-décès` | Délai | `Urgence 48h` | ⭕ Optionnel |
| `convention_num` | **Numéro de Convention** | `text` | `ULIEGE-LEG-2024-819 (Signée du vivant)` | Convention | `Enregistré` | ⭕ Optionnel |
| `morgue_contact` | **Astreinte 24h/24 Morgue** | `text` | `+32 4 366 21 11 (Permanence Corps Science)` | Téléphone | `Astreinte` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_call_transporter` | **📞 Alerter le Transporteur Anatomique** | `primary` | `idle` | 📞 |
| `btn_view_contract` | **Consulter la Convention ULiège** | `secondary` | `idle` | 📄 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Protocole de Legs sous 48h Notifié
>
> **Badge de Conformité :** `Urgence Déclenchée`
>
> **Détail Opérationnel :** Contacts d'astreinte et convention ULiège affichés. Délai des 48h rappelé aux proches.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_LEG_BODY_DELAY_EXPIRED` |
| **Intitulé de l'Incident** | **Délai Légal de 48 Heures Expiré** |
| **Condition Déclenchante** | Signalement du décès plus de 48 heures après la survenue de la mort. |
| **Message d'Erreur UI** | *« DÉLAI DÉPASSÉ : Le délai légal de 48 heures pour le transfert vers le laboratoire d'anatomie est expiré. La faculté de médecine ne peut plus accepter le corps. »* |
| **Action Corrective Requise** | **Basculer immédiatement vers le protocole de sépulture par sarcomusation mémorielle (Démonstrateur de faisabilité prospectif — Option non autorisée par le droit positif actuel (référence à confirmer par un juriste)) ou crémation civile.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Sanctuaire Mobile • Protocole d'Urgence Legs à la Science (48h)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Signalement d'un Décès avec Volonté de Legs | *En attente utilisateur* | La famille consulte les volontés médicales et découvre la convention de don à la science. |
| **2** | **Déclenchement ⚡** | Déclenchement de l'Alerte Chronométrée des 48 Heures | `Clic sur 'Consulter le Protocole 48h' et affichage des contacts d'astreinte` | Mise en avant du compte à rebours légal des 48 heures et du numéro vert d'astreinte. |
| **3** | **Traitement ⚙️** | Génération du Dossier Administratif d'Accompagnement | `Progression : 90%` | Préparation de la fiche de transfert avec numéro de convention et horodatage certifié. |
| **4** | **Scellement & Fin ✨** | Protocole Universitaire Notifié avec Succès | `Statut : success` | La permanence anatomique est prévenue. Le transport légal est sécurisé dans les délais. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-310 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Signalement d'un Décès avec Volonté de Legs
*La famille consulte les volontés médicales et découvre la convention de don à la science.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Protocole Legs Science</span>
                        <span class="wf-status-badge wf-badge-neutral">Urgence 48 Heures</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-uni-icon">🏛️</span>
                        <div><strong>Convention de Legs à la Science ULiège Détectée</strong></div>
                        <div class="wf-subtext">Le transfert doit être engagé sans délai vers la morgue anatomique</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">Consulter le Protocole 48h</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Déclenchement de l'Alerte Chronométrée des 48 Heures
*Mise en avant du compte à rebours légal des 48 heures et du numéro vert d'astreinte.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Astreinte ULiège</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Compte à Rebours Actif</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">📞 Astreinte Faculté : +32 4 366 21 11</div>
                        <div class="wf-subtext">Convention ULiège n° LEG-2024-819 prête pour présentation</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Appel de la permanence...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Génération du Dossier Administratif d'Accompagnement
*Préparation de la fiche de transfert avec numéro de convention et horodatage certifié.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Dossier de Transfert</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Préparation Bordereau (90%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 90%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [LEG-DOCS] Vérification validité convention ULiège : VALIDE</code><br>
                        <code>> [LEG-TIME] Constat horaire : Décès survenu il y a 6h (< 48h : Conforme)</code><br>
                        <code>> [TRANSPORT] Avis d'enlèvement transmis à l'opérateur conventionné</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Protocole Universitaire Notifié avec Succès
*La permanence anatomique est prévenue. Le transport légal est sécurisé dans les délais.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Legs Enregistré</span>
                        <span class="wf-status-badge wf-badge-success">✨ Transfert Notifié</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🏛️</span>
                        <div>
                          <strong>Transfert Anatomique Engagé dans les 48h</strong>
                          <p class="wf-subtext">Faculté ULiège alertée • Convention honorée avec respect et dignité</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Accès Dossier Patient →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-311"></a>
## UC-311 : Droit d'Accès Post-Mortem au Dossier Médical (Loi 2002 Art. 9 §4)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-311` |
| **Catégorie Métier** | **Droits du Patient** |
| **Acteur Principal** | Praticien Professionnel Désigné & Ayants Droit |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `Loi2002`, `DossierMedical`, `AyantsDroit`, `SecretMedical`, `Praticien` |
| **Base Légale & Normative** | Loi du 22 août 2002 relative aux droits du patient (art. 9 §4 - accès post-mortem par praticien intermédiaire). |
| **Terminal / Canvas Wireframe** | `Sanctuaire Mobile • Guichet d'Accès Médical Post-Mortem (Loi 2002)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Carte Directives présentée par un médecin désigné par les ayants droit.

> [!TIP]
> **Postconditions Garanties :**
> Accès strictement encadré accordé au médecin désigné, secret médical préservé face aux tiers non habilités.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Conformément à l'article 9 §4 de la loi du 22 août 2002 relative aux droits du patient, l'accès au dossier médical après décès est strictement réservé à un praticien professionnel de santé désigné par la famille.
2. Présentation conjointe de la Carte Directives et du jeton d'authentification professionnel du médecin (numéro INAMI).
3. Saisie obligatoire de la motivation de la demande (recherche d'antécédents génétiques, vérification d'une faute médicale).
4. Vérification de l'absence d'opposition expresse formulée de son vivant par le patient.
5. Déverrouillage cryptographique du compartiment médical et consignation inaltérable dans le registre d'audit.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `designated_doc` | **Praticien Professionnel Désigné** | `text` | `Dr. Sophie Laurent (Médecin désigné par Claire Dubois)` | Médecin | `Habilité` | ✅ Requis |
| `doc_inami` | **Numéro d'Ordre / INAMI** | `text` | `INAMI : 1-89412-22-109` | INAMI | `Vérifié` | ✅ Requis |
| `request_motive` | **Motivation de la Demande** | `textarea` | `Recherche d'antécédents cardiovasculaires héréditaires au bénéfice des descendants.` | Motivation | `Exigé par Loi` | ✅ Requis |
| `prior_opposition` | **Opposition Antérieure Patient** | `text` | `AUCUNE OPPOSITION enregistrée du vivant du patient` | Opposition | `Autorisé` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_unlock_medical_vault` | **Déverrouiller le Compartiment Médical (Clé Praticien)** | `primary` | `idle` | 🔓 |
| `btn_verify_family_mandate` | **Vérifier Mandat des Ayants Droit** | `secondary` | `idle` | ⚖️ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Accès Médical Post-Mortem Accordé
>
> **Badge de Conformité :** `Conforme Loi 22 août 2002`
>
> **Détail Opérationnel :** Dr. Sophie Laurent authentifiée. Synthèse médicale déverrouillée, journal d'audit émargé.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_PATIENT_RIGHTS_UNAUTHORIZED` |
| **Intitulé de l'Incident** | **Opposition du Défunt ou Praticien Non Habilité** |
| **Condition Déclenchante** | Tentative d'accès direct par un membre de la famille sans passer par un praticien, ou opposition du défunt. |
| **Message d'Erreur UI** | *« ACCÈS REFUSÉ (Loi 22 août 2002) : L'accès au dossier médical post-mortem requiert l'intermédiation obligatoire d'un médecin désigné et l'absence d'opposition expresse du défunt. »* |
| **Action Corrective Requise** | **Mandater un praticien professionnel de santé assermenté pour formuler la requête motivée.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Sanctuaire Mobile • Guichet d'Accès Médical Post-Mortem (Loi 2002)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Compartiment Médical Chiffré en Attente de Praticien | *En attente utilisateur* | Volet confidentiel verrouillé. Le médecin doit s'authentifier avec son numéro INAMI. |
| **2** | **Déclenchement ⚡** | Authentification du Praticien & Saisie de la Motivation | `Scan du jeton professionnel du Dr. Laurent et validation de la motivation` | Contrôle automatique de l'absence d'opposition du défunt dans le profil in-silico. |
| **3** | **Traitement ⚙️** | Vérification Art. 9 §4 & Dérivation de Clé Temporaire | `Progression : 95%` | Déverrouillage cryptographique éphémère en mémoire vive avec émargement du journal d'audit. |
| **4** | **Scellement & Fin ✨** | Synthèse Médicale Consultable par le Médecin | `Statut : success` | Accès conforme au droit belge. Secret médical préservé pour les tiers non autorisés. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-311 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Compartiment Médical Chiffré en Attente de Praticien
*Volet confidentiel verrouillé. Le médecin doit s'authentifier avec son numéro INAMI.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Espace Patient Protégé</span>
                        <span class="wf-status-badge wf-badge-alert">🔒 Chiffrement Médical Actif</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-lock-icon">🔒</span>
                        <div><strong>Dossier Médical Post-Mortem (Loi du 22 août 2002)</strong></div>
                        <div class="wf-subtext">Accès réservé au praticien professionnel désigné par les ayants droit</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔓 Déverrouiller le Compartiment Médical</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Authentification du Praticien & Saisie de la Motivation
*Contrôle automatique de l'absence d'opposition du défunt dans le profil in-silico.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Requête Dr. Laurent</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Clé Praticien Apposée</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Dr. Sophie Laurent (INAMI 1-89412-22-109)</div>
                        <div class="wf-subtext">Motivation : Recherche antécédents génétiques • Mandat Claire Dubois OK</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Vérification de non-opposition...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Vérification Art. 9 §4 & Dérivation de Clé Temporaire
*Déverrouillage cryptographique éphémère en mémoire vive avec émargement du journal d'audit.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Dérivation Cryptographique</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Contrôle Loi 2002 (95%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 95%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [LAW-2002] Contrôle opposition expresse défunt : Aucune opposition</code><br>
                        <code>> [AUDIT-TRAIL] Journalisation de l'accès par Dr. Laurent horodatée 2026-10-04</code><br>
                        <code>> [CRYPTO-VAULT] Dérivation clé de session médicale : Accès accordé</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Synthèse Médicale Consultable par le Médecin
*Accès conforme au droit belge. Secret médical préservé pour les tiers non autorisés.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Synthèse Médicale Ouverte</span>
                        <span class="wf-status-badge wf-badge-success">✨ Accès Habilité Loi 2002</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🩺</span>
                        <div>
                          <strong>Dossier Médical Consulté sous Secret Professionnel</strong>
                          <p class="wf-subtext">Dr. Laurent habilitée • Journal d'audit légal scellé in-silico</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Pérennité Séculaire →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-312"></a>
## UC-312 : Politique Mémorielle PaxFunèbre & Pérennité Séculaire (DEC-AET-11)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-312` |
| **Catégorie Métier** | **Pérennité & Économie** |
| **Acteur Principal** | Famille & Réseau PaxFunèbre |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `Perennite`, `Seculaire`, `DEC-AET-11`, `PolitiqueMemorielle`, `LocalFirst` |
| **Base Légale & Normative** | Directive européenne 2011/83/UE sur les droits des consommateurs (transparence et pérennité contractuelle) (référence à confirmer par un juriste). |
| **Terminal / Canvas Wireframe** | `Sanctuaire Mobile • Arche de Pérennité Séculaire (100 Ans)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Sanctuaire mémoriel actif, consultation de l'onglet 'Pérennité & Archivage'.

> [!TIP]
> **Postconditions Garanties :**
> Pérennité physique et numérique garantie sur un siècle, discrétion tarifaire absolue et indépendance totale vis-à-vis des serveurs cloud.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Affichage des garanties de conservation de la mémoire physique in-silico :
2. - Rétention des données EEPROM certifiée 100 ans à température ambiante sur JavaCard ACOSJ.
3. - Fonctionnement 100% autonome sans abonnement obligatoire : la carte reste lisible à perpétuité par simple contact NFC même sans connexion Internet.
4. - Présentation de l'accès mémoriel et de ses extensions selon la politique mémorielle Le Pax Funèbre (discrétion tarifaire absolue et dignité du deuil, DEC-AET-11).
5. - Dotation familiale séculaire pour rééditions physiques de cartes ou médaillons en cas de perte par un descendant.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `silicon_retention` | **Rétention Physique Silicium** | `text` | `100 ANS GARANTIS (Cellules EEPROM ACOSJ)` | Rétention | `100 Ans` | ⭕ Optionnel |
| `cloud_dependency` | **Dépendance Cloud Obligatoire** | `text` | `ZÉRO DÉPENDANCE (100% Autonome Local-First)` | Cloud | `Souverain` | ⭕ Optionnel |
| `pricing_policy` | **Politique Mémorielle PaxFunèbre** | `text` | `Régie par la politique PaxFunèbre (Discrétion tarifaire, DEC-AET-11)` | Politique | `DEC-AET-11` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_verify_vault_cert` | **Consulter le Certificat de Pérennité Séculaire** | `primary` | `idle` | 🏛️ |
| `btn_duplicate_request` | **Demander un Médaillon pour Descendant** | `secondary` | `idle` | 🎴 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Sanctuaire Mémoriel Séculaire Actif
>
> **Badge de Conformité :** `100 Ans in-silico`
>
> **Détail Opérationnel :** Autonomie totale sans abonnement obligatoire. Accès régi par la politique mémorielle PaxFunèbre (DEC-AET-11).

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_VAULT_DEPOSIT_EXHAUSTED` |
| **Intitulé de l'Incident** | **Dotation de Réédition Échue** |
| **Condition Déclenchante** | Demande de fabrication d'un duplicata physique sans fonds de dotation séculaire actif. |
| **Message d'Erreur UI** | *« Information contractuelle : Le quota de réédition physique est épuisé. La carte originale reste cependant lisible à 100% sans frais. »* |
| **Action Corrective Requise** | **Consulter les modalités d'accueil mémoriel auprès de l'agence Le Pax Funèbre selon la politique mémorielle en vigueur (DEC-AET-11).** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Sanctuaire Mobile • Arche de Pérennité Séculaire (100 Ans)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Statut de Conservation Séculaire en Consultation | *En attente utilisateur* | La famille consulte l'arche de mémoire et les garanties matérielles de la puce ACOSJ. |
| **2** | **Déclenchement ⚡** | Affichage des Côtés Techniques & Absence de Cloud | `Clic sur 'Consulter le Certificat de Pérennité Séculaire'` | Mise en avant des arguments souverains : Zéro abonnement obligatoire, politique mémorielle et discrétion tarifaire PaxFunèbre (DEC-AET-11). |
| **3** | **Traitement ⚙️** | Génération de l'Attestation Séculaire Infalsifiable | `Progression : 95%` | Scellement de l'acte de pérennité avec signature officielle de la dotation Le Pax Funèbre. |
| **4** | **Scellement & Fin ✨** | Certificat de Pérennité Séculaire Remis | `Statut : success` | Sérénité absolue pour la famille. La mémoire d'Henri Dubois traversera les générations. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-312 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Statut de Conservation Séculaire en Consultation
*La famille consulte l'arche de mémoire et les garanties matérielles de la puce ACOSJ.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Arche de Pérennité</span>
                        <span class="wf-status-badge wf-badge-neutral">Rétention 100 Ans</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-vault-icon">🏛️</span>
                        <div><strong>Garantie Séculaire in-silico (2026 — 2126)</strong></div>
                        <div class="wf-subtext">Zéro dépendance cloud • Vos souvenirs appartiennent physiquement à votre famille</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">Consulter le Certificat de Pérennité Séculaire</button>
                      </div>
                    </div>
```

#### Phase 2 - Déclenchement : Affichage des Côtés Techniques & Absence de Cloud
*Mise en avant des arguments souverains : Zéro abonnement obligatoire, politique mémorielle et discrétion tarifaire PaxFunèbre (DEC-AET-11).*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Certificat de Pérennité</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Garantie Matérielle 100 Ans</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Rétention EEPROM certifiée : 100 ans sans rafraîchissement</div>
                        <div class="wf-subtext">Accueil et extensions mémorielles régis par la politique PaxFunèbre (DEC-AET-11)</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Édition du certificat séculaire...</button>
                      </div>
                    </div>
```

#### Phase 3 - Traitement : Génération de l'Attestation Séculaire Infalsifiable
*Scellement de l'acte de pérennité avec signature officielle de la dotation Le Pax Funèbre.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Moteur d'Arche Mémorielle</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Scellement Séculaire (95%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 95%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [VAULT-ENG] Validation du statut local-first : ZÉRO serveur distant requis</code><br>
                        <code>> [DEC-AET-11] Politique mémorielle PaxFunèbre appliquée (discrétion tarifaire absolue)</code><br>
                        <code>> [CRYPTO-SEAL] Attestation de souveraineté 100 ans scellée</code>
                      </div>
                    </div>
```

#### Phase 4 - Fin de Cycle : Certificat de Pérennité Séculaire Remis
*Sérénité absolue pour la famille. La mémoire d'Henri Dubois traversera les générations.*

```html
<div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Sérénité Perpétuelle</span>
                        <span class="wf-status-badge wf-badge-success">✨ Pérennité 100 Ans Actif</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🏛️</span>
                        <div>
                          <strong>Mémoire Transmissible aux Générations Futures</strong>
                          <p class="wf-subtext">Puce physique ACOSJ inaltérable • Accès mémoriel régi par la politique PaxFunèbre (DEC-AET-11)</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Bascule vers App 4 : Filière & Traçabilité →</button>
                      </div>
                    </div>
```

</details>

---

<a id="uc-313"></a>
## UC-313 : Panne Audio / Perte de Périphérique & Mode Sanctuaire Silencieux Visuel

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-313` |
| **Catégorie Métier** | **Expérience Émotionnelle & Résilience** |
| **Acteur Principal** | Famille & Proches en Recueillement |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `SanctuaireSilencieux`, `WebAudio`, `Accessibilite`, `VisualWave`, `OpusSILK`, `EF-3` |
| **Base Légale & Normative** | Directives d'accessibilité numérique W3C WCAG 2.1 (critère 1.2 médias temporels) & Charte Sanctuaire Mémoriel. |
| **Terminal / Canvas Wireframe** | `Sanctuaire Mobile • Mode Recueillement Silencieux Visuel (Partition EF-3)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> La famille consulte la carte Sanctuaire sur un smartphone dont la sortie audio est muette, en panne ou en mode silencieux strict.

> [!TIP]
> **Postconditions Garanties :**
> L'hommage mémoriel se déroule dans la sérénité et le recueillement, même sans canal audio actif.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. L'utilisateur effleure la carte Sanctuaire pour lancer l'hommage sonore d'EF-3.
2. Le composant WebAudio tente d'ouvrir le flux de restitution : détection d'une suspension du sous-système audio ou absence de sortie.
3. Bascule instantanée, fluide et solennelle vers le 'Mode Sanctuaire Silencieux Visuel' sans message d'erreur alarmant.
4. Déploiement d'une animation d'ondes dorées synchronisées avec la modulation de la voix et affichage textuel de la transcription.
5. Maintien de l'émotion et du recueillement avec proposition discrète de réactiver le son dès reconnexion d'un périphérique.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `audio_device_status` | **Périphérique de Sortie Audio** | `text` | `Indisponible / Mode Silencieux Détecté` | - | `Silencieux` | ⭕ Optionnel |
| `visual_sanctuary_mode` | **Mode Visuel Actif** | `text` | `Ondes Harmoniques Dorées + Transcription Hommage` | - | `Sérénité` | ⭕ Optionnel |
| `voice_transcript` | **Transcription Textuelle EF-3** | `textarea` | `« Souvenez-vous des jours heureux passés ensemble sous le grand chêne... Mon amour veille sur vous. »` | - | `Transcription` | ⭕ Optionnel |
| `ambiance_status` | **Ducking & Ambiance** | `text` | `Transition douce vers silence apaisé (0 dB)` | - | `WebAudio` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_activate_visual_mode` | **Basculer en Mode Sanctuaire Silencieux Visuel** | `primary` | `idle` | 🕊️ |
| `btn_retry_audio` | **Réessayer la Sortie Audio** | `secondary` | `idle` | 🔊 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Mode Sanctuaire Silencieux Visuel Engagé avec Succès
>
> **Badge de Conformité :** `Sanctuaire Visuel Actif`
>
> **Détail Opérationnel :** Expérience mémorielle préservée. Transcription synchronisée et ondes de recueillement dorées actives.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_AUDIO_OUTPUT_UNAVAILABLE` |
| **Intitulé de l'Incident** | **Sortie Audio Inaccessible ou Système Muet** |
| **Condition Déclenchante** | Absence de périphérique audio disponible ou blocage de la lecture automatique par la politique du navigateur. |
| **Message d'Erreur UI** | *« Périphérique audio indisponible : bascule automatique vers le recueillement visuel respectueux. »* |
| **Action Corrective Requise** | **Vérifier le commutateur silencieux du smartphone ou brancher des écouteurs pour écouter la voix originale.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Sanctuaire Mobile • Mode Recueillement Silencieux Visuel (Partition EF-3)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Détection d'une Sortie Audio Muette | *En attente utilisateur* | Le smartphone est en mode silencieux lors de l'effleurement NFC de la carte Sanctuaire. |
| **2** | **Déclenchement ⚡** | Déploiement des Ondes Harmoniques Dorées | `Clic sur 'Basculer en Mode Sanctuaire Silencieux'` | Génération de l'animation d'ondes douces synchronisée sur le spectre de la voix mémorisée. |
| **3** | **Traitement ⚙️** | Diffusion du Message & Veilleuse Lumineuse | `Progression : 96%` | Le texte défile doucement accompagné d'une flamme mémorielle numérique. |
| **4** | **Scellement & Fin ✨** | Recueillement Achevé dans la Dignité | `Statut : success` | L'hommage s'est déroulé dans la sérénité. La famille a vécu un moment de communion intact. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-313 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Détection d'une Sortie Audio Muette
*Le smartphone est en mode silencieux lors de l'effleurement NFC de la carte Sanctuaire.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">Sanctuaire • Recueillement Mobile</span>
                                            <span class="wf-status-badge wf-badge-neutral">Audio Silencieux</span>
                                          </div>
                                          <div class="wf-device-status-box">
                                            <span class="wf-qa-icon">🕊️</span>
                                            <div><strong>Sortie Audio Système Non Détectée</strong></div>
                                            <div class="wf-subtext">Activation possible du mode sanctuaire silencieux pour un recueillement visuel</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary">🕊️ Basculer en Mode Sanctuaire Silencieux Visuel</button>
                                          </div>
                                        </div>
```

#### Phase 2 - Déclenchement : Déploiement des Ondes Harmoniques Dorées
*Génération de l'animation d'ondes douces synchronisée sur le spectre de la voix mémorisée.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">Sanctuaire • Méditation Visuelle</span>
                                            <span class="wf-status-badge wf-badge-trigger">⚡ Onde Visuelle Active</span>
                                          </div>
                                          <div class="wf-trigger-card wf-radar-pulse">
                                            <div class="wf-trigger-indicator">✓ Ondes dorées satinées calquées sur le signal vocal EF-3</div>
                                            <div class="wf-subtext">Affichage de la transcription textuelle avec typographie mémorielle solennelle</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary wf-pulse-btn">Recueillement en cours...</button>
                                          </div>
                                        </div>
```

#### Phase 3 - Traitement : Diffusion du Message & Veilleuse Lumineuse
*Le texte défile doucement accompagné d'une flamme mémorielle numérique.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">Sanctuaire • Lecture Silencieuse</span>
                                            <span class="wf-status-badge wf-badge-process">⚙️ Hommage Actif (96%)</span>
                                          </div>
                                          <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 96%;"></div></div>
                                          <div class="wf-console-log">
                                            <code>> [AUDIO-FALLBACK] Sortie sonore mutée -> Bascule sans accroc validée</code><br>
                                            <code>> [TRANSCRIPT] Ligne 1/3 : « Souvenez-vous des jours heureux... »</code><br>
                                            <code>> [VISUAL-FLAME] Veilleuse mémorielle allumée en mémoire d'Henri</code><br>
                                            <code>> [WCAG-2.1] Critère d'accessibilité universelle 100% respecté</code>
                                          </div>
                                        </div>
```

#### Phase 4 - Fin de Cycle : Recueillement Achevé dans la Dignité
*L'hommage s'est déroulé dans la sérénité. La famille a vécu un moment de communion intact.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">Sanctuaire • Sérénité Préservée</span>
                                            <span class="wf-status-badge wf-badge-success">✨ Hommage Transmis</span>
                                          </div>
                                          <div class="wf-success-banner">
                                            <span class="wf-seal-icon">🕯️</span>
                                            <div>
                                              <strong>Communion Mémorielle Respectée</strong>
                                              <p class="wf-subtext">La voix d'Henri a été transmise par les mots et la lumière • Dignité absolue</p>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-gold">Signer le Livre d'Or Virtuel →</button>
                                          </div>
                                        </div>
```

</details>

---

<a id="uc-314"></a>
## UC-314 : Lecture de Secours par QR Code Micro-Gravé sur Carte Endommagée

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-314` |
| **Catégorie Métier** | **Résilience Mémorielle & Secours** |
| **Acteur Principal** | Proches du Défunt & Conseiller Funéraire |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `QRCode`, `Secours`, `AntenneNFCBrisée`, `OfflineFallback`, `CBOR`, `EF-1` |
| **Base Légale & Normative** | Norme ISO/IEC 18004 (code à barres matriciel QR Code haute densité) & Principe de résilience mémorielle séculaire. |
| **Terminal / Canvas Wireframe** | `Sanctuaire Mobile • Scanner de Secours QR Code Haute Densité (EF-1)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> La carte physique a subi une violente torsion ou un choc mécanique ayant fracturé l'antenne NFC interne.

> [!TIP]
> **Postconditions Garanties :**
> La mémoire du défunt est restituée avec intégrité malgré la destruction matérielle de la liaison radio NFC.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. L'utilisateur pose son smartphone sur la carte : aucun contact RF n'est établi après plusieurs essais.
2. L'application Sanctuaire propose automatiquement l'option 'Relecture de Secours par Capteur Optique'.
3. La caméra du smartphone capture le micro QR Code haute densité gravé au laser au verso de la carte.
4. Décodage instantané du flux binaire compressé CBOR contenant l'identité civile, l'épitaphe et l'empreinte de signature.
5. Reconstitution intégrale du profil mémoriel et vérification de la signature cryptographique en mémoire locale.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `nfc_rf_status` | **Signal Radio NFC** | `text` | `ZÉRO SIGNAL DÉTECTÉ (Antenne fracturée)` | - | `Panne RF` | ⭕ Optionnel |
| `fallback_method` | **Méthode de Repli** | `select` | `Micro QR Code Laser Recto/Verso Haute Densité` | - | `Secours Optique` | ✅ Requis |
| `cbor_decoded_summary` | **Données Décodées CBOR** | `text` | `Henri Dubois • 1948-2026 • Épitaphe & Directives Intègres` | - | `Validé` | ⭕ Optionnel |
| `sha256_hash_status` | **Vérification Empreinte SHA-256** | `text` | `CONCORDANCE PARFAITE avec le sceau d'origine` | - | `Intégrité` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_scan_qr_fallback` | **Activer la Caméra & Scanner le QR Code de Secours** | `primary` | `idle` | 📷 |
| `btn_manual_aid_input` | **Saisir le Code d'Identité Imprimé** | `secondary` | `idle` | ⌨️ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Profil Mémoriel Restitué par Décodage Optique
>
> **Badge de Conformité :** `Secours QR Code Conforme`
>
> **Détail Opérationnel :** Flux binaire CBOR décodé avec succès. Intégrité et empreinte cryptographique validées à 100%.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_NFC_ANTENNA_DAMAGED_QR_FALLBACK` |
| **Intitulé de l'Incident** | **Antenne Sans Contact Défaillante & Recours au QR Code** |
| **Condition Déclenchante** | Absence de réponse APDU ISO 14443-4 sur une carte présentant des fissures physiques. |
| **Message d'Erreur UI** | *« Liaison NFC indisponible : L'antenne de la carte est endommagée. Déclenchement de la capture optique de secours. »* |
| **Action Corrective Requise** | **Présenter le verso de la carte devant l'objectif de la caméra pour lire le micro-code de secours matriciel.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Sanctuaire Mobile • Scanner de Secours QR Code Haute Densité (EF-1)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Échec de Détection Radio & Proposition de Secours | *En attente utilisateur* | Le scan NFC échoue en raison d'une avarie d'antenne. L'application invite à utiliser l'optique. |
| **2** | **Déclenchement ⚡** | Visée Optique & Capture Haute Vitesse | `Clic sur 'Scanner le QR Code de Secours'` | Reconnaissance du motif matriciel haute densité et extraction du payload binaire compressé. |
| **3** | **Traitement ⚙️** | Décompression CBOR & Contrôle d'Intégrité | `Progression : 94%` | Validation de l'authenticité des données d'état civil sans nécessiter aucun réseau externe. |
| **4** | **Scellement & Fin ✨** | Sanctuaire Ouvert & Mémoire Accessible | `Statut : success` | La mémoire triomphe de la panne matérielle. La famille accède au mémorial sans encombre. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-314 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Échec de Détection Radio & Proposition de Secours
*Le scan NFC échoue en raison d'une avarie d'antenne. L'application invite à utiliser l'optique.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">Sanctuaire • Diagnostic de Connexion</span>
                                            <span class="wf-status-badge wf-badge-neutral">Pas de Réponse NFC</span>
                                          </div>
                                          <div class="wf-device-status-box" style="border-color: #f59e0b;">
                                            <span class="wf-qa-icon">⚠️</span>
                                            <div><strong>Liaison Sans Contact Inopérante</strong></div>
                                            <div class="wf-subtext">L'antenne semble fracturée • Recours au micro QR Code gravé au verso</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary">📷 Scanner le QR Code de Secours</button>
                                          </div>
                                        </div>
```

#### Phase 2 - Déclenchement : Visée Optique & Capture Haute Vitesse
*Reconnaissance du motif matriciel haute densité et extraction du payload binaire compressé.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">Sanctuaire • Capture Optique</span>
                                            <span class="wf-status-badge wf-badge-trigger">⚡ Scan QR Code Actif</span>
                                          </div>
                                          <div class="wf-trigger-card wf-radar-pulse">
                                            <div class="wf-trigger-indicator">✓ Micro QR Code détecté au verso : format binaire compressé</div>
                                            <div class="wf-subtext">Lecture de 840 octets CBOR canonique et signature cryptographique associée</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary wf-pulse-btn">Décodage du profil en cours...</button>
                                          </div>
                                        </div>
```

#### Phase 3 - Traitement : Décompression CBOR & Contrôle d'Intégrité
*Validation de l'authenticité des données d'état civil sans nécessiter aucun réseau externe.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">Sanctuaire • Reconstitution CBOR</span>
                                            <span class="wf-status-badge wf-badge-process">⚙️ Décodage (94%)</span>
                                          </div>
                                          <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 94%;"></div></div>
                                          <div class="wf-console-log">
                                            <code>> [OPTICAL-DECODE] 840 octets extraits du micro QR Code</code><br>
                                            <code>> [CBOR-PARSER] Profil mémoriel d'Henri Dubois reconstitué</code><br>
                                            <code>> [SHA256-CHECK] Empreinte du profil validée : 100% conforme</code><br>
                                            <code>> [RESCUE-ENGINE] Accès complet au Sanctuaire rétabli avec succès</code>
                                          </div>
                                        </div>
```

#### Phase 4 - Fin de Cycle : Sanctuaire Ouvert & Mémoire Accessible
*La mémoire triomphe de la panne matérielle. La famille accède au mémorial sans encombre.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">Sanctuaire • Profil Reconstitué</span>
                                            <span class="wf-status-badge wf-badge-success">✨ Secours Réussi</span>
                                          </div>
                                          <div class="wf-success-banner">
                                            <span class="wf-seal-icon">🏛️</span>
                                            <div>
                                              <strong>Mémoire d'Henri Dubois Préservée</strong>
                                              <p class="wf-subtext">Lecture optique de secours validée • Les directives et hommages sont accessibles</p>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-gold">Entrer dans le Sanctuaire Mémoriel →</button>
                                          </div>
                                        </div>
```

</details>

---

<a id="uc-315"></a>
## UC-315 : Réclamations Contradictoires des Ayants Droit sur l'Arbre du Souvenir (Mise en Réserve Conservatoire)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-315` |
| **Catégorie Métier** | **Arbitrage & Volontés Funéraires** |
| **Acteur Principal** | Ayants Droit & Médiateur / Notaire |
| **Plateformes Cibles** | Web Standard (PWA Hors-Ligne), Natif (iOS & Android) |
| **Tags Clés** | `LitigeFamilial`, `ArbreDuSouvenir`, `ReserveConservatoire`, `Sequestre`, `EF-4`, `Loi1971` |
| **Base Légale & Normative** | Loi du 20 juillet 1971 sur les funérailles et sépultures & Code civil (règles de dévolution des décisions funéraires). |
| **Terminal / Canvas Wireframe** | `Sanctuaire Pro • Module d'Arbitrage & Séquestre Mémoriel (Partition EF-4)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> Deux branches d'une famille expriment des volontés divergentes concernant la destination cinéraire ou la gestion du livre d'or.

> [!TIP]
> **Postconditions Garanties :**
> Aucune modification unilatérale n'est enregistrée ; le respect de l'ordre public funéraire est garanti.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Notification formelle d'une contestation successorale ou funéraire transmise au service d'arbitrage mémoriel.
2. Activation sur l'application Sanctuaire de la procédure de 'Mise en Réserve Conservatoire'.
3. Verrouillage immédiat des modifications sur le registre de sépulture et l'amendement de l'Arbre du Souvenir dans EF-4.
4. Affichage d'un bandeau neutre et solennel appelant au respect de la mémoire et signalant la médiation notariale en cours.
5. Maintien exclusif des fonctions de recueillement contemplatif (photos, textes) sans modification possible des sépultures.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `case_reference` | **Dossier Mémoriel Concerné** | `text` | `Dossier #AET-2026-NAM-0491 (Henri Dubois)` | - | `Dossier` | ⭕ Optionnel |
| `legal_reserve_status` | **Statut Juridique d'Affectation** | `text` | `MISE EN RÉSERVE CONSERVATOIRE (Litige Ayants Droit)` | - | `Séquestre` | ⭕ Optionnel |
| `disputed_tree` | **Arbre du Souvenir Revendiqué** | `text` | `Chêne Séculaire Parcelle DNF #B-12 (Opposition déclarée)` | - | `Litige` | ⭕ Optionnel |
| `protective_measure` | **Mesure Conservatoire Prise** | `select` | `Gel des Inscriptions & Maintien Recueillement Neutre` | - | `Médiation` | ✅ Requis |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_apply_conservative_hold` | **Activer le Séquestre Conservatoire Mémoriel** | `primary` | `idle` | ⚖️ |
| `btn_view_notarial_notice` | **Consulter l'Avis de Médiation Notariale** | `secondary` | `idle` | 📜 |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Mise en Réserve Conservatoire Notifiée
>
> **Badge de Conformité :** `Séquestre Mémoriel Actif`
>
> **Détail Opérationnel :** Registre EF-4 verrouillé en modification. Accès maintenu en mode neutre solennel en attente d'arbitrage notarié.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_CONTRADICTORY_HEIRS_CLAIM` |
| **Intitulé de l'Incident** | **Conflit Juridique Entre Ayants Droit sur la Destination des Cendres** |
| **Condition Déclenchante** | Opposition formelle déposée par un héritier direct contestant l'affectation de l'Arbre du Souvenir. |
| **Message d'Erreur UI** | *« Blocage conservatoire : Des réclamations contradictoires sont enregistrées. Aucune modification du registre n'est autorisée. »* |
| **Action Corrective Requise** | **Transmettre l'acte de notoriété ou l'accord signé de tous les héritiers au notaire instrumentant pour lever la réserve.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Sanctuaire Pro • Module d'Arbitrage & Séquestre Mémoriel (Partition EF-4)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Signalement d'une Contestation Familiale | *En attente utilisateur* | Deux ayants droit revendiquent des décisions opposées concernant le devenir de l'amendement cinéraire. |
| **2** | **Déclenchement ⚡** | Application du Gel Conservatoire sur EF-4 | `Clic sur 'Activer le Séquestre Conservatoire'` | Verrouillage des transactions sur la partition de sépulture et génération du bandeau d'apaisement. |
| **3** | **Traitement ⚙️** | Configuration du Sanctuaire en Mode Neutre Solennel | `Progression : 100%` | L'interface masque les options contestées et préserve la dignité des hommages visuels. |
| **4** | **Scellement & Fin ✨** | Paix Mémorielle Préservée & Médiation en Cours | `Statut : success` | La mémoire du défunt est mise à l'abri des querelles. La décision finale interviendra sereinement. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-315 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Signalement d'une Contestation Familiale
*Deux ayants droit revendiquent des décisions opposées concernant le devenir de l'amendement cinéraire.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">Sanctuaire • Service de Régulation</span>
                                            <span class="wf-status-badge wf-badge-neutral">Contestation Reçue</span>
                                          </div>
                                          <div class="wf-content-grid">
                                            <div class="wf-field-group">
                                              <label class="wf-label">Objet du Litige</label>
                                              <div class="wf-input-placeholder">Destination des cendres sous l'Arbre du Souvenir DNF</div>
                                            </div>
                                            <div class="wf-field-group">
                                              <label class="wf-label">Parties en Présence</label>
                                              <div class="wf-input-placeholder">Branche A (Inhumation forêt) vs Branche B (Columbarium)</div>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary">⚖️ Activer le Séquestre Conservatoire Mémoriel</button>
                                          </div>
                                        </div>
```

#### Phase 2 - Déclenchement : Application du Gel Conservatoire sur EF-4
*Verrouillage des transactions sur la partition de sépulture et génération du bandeau d'apaisement.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">Sanctuaire • Gel Juridique</span>
                                            <span class="wf-status-badge wf-badge-trigger">⚡ Séquestre en Cours</span>
                                          </div>
                                          <div class="wf-trigger-card wf-radar-pulse">
                                            <div class="wf-trigger-indicator">✓ Partition EF-4 placée sous protection conservatoire</div>
                                            <div class="wf-subtext">Gel des écritures • Interdiction de transfert cinéraire sans ordonnance</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary wf-pulse-btn">Verrouillage conservatoire actif...</button>
                                          </div>
                                        </div>
```

#### Phase 3 - Traitement : Configuration du Sanctuaire en Mode Neutre Solennel
*L'interface masque les options contestées et préserve la dignité des hommages visuels.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">Sanctuaire • Mode Neutre Actif</span>
                                            <span class="wf-status-badge wf-badge-process">⚙️ Protection Active (100%)</span>
                                          </div>
                                          <div class="wf-console-log">
                                            <code>> [LEGAL-HOLD] Séquestre conservatoire appliqué à 14:15:30 UTC</code><br>
                                            <code>> [PARTITION-EF4] Modifications bloquées (lecture seule maintenue)</code><br>
                                            <code>> [NEUTRAL-BANNER] Bandeau d'apaisement affiché sur les terminaux des proches</code><br>
                                            <code>> [MEDIATION] Dossier référé à Me Vanhove, notaire instrumentant</code>
                                          </div>
                                        </div>
```

#### Phase 4 - Fin de Cycle : Paix Mémorielle Préservée & Médiation en Cours
*La mémoire du défunt est mise à l'abri des querelles. La décision finale interviendra sereinement.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">Sanctuaire • Sérénité Protégée</span>
                                            <span class="wf-status-badge wf-badge-success">✨ Réserve Établie</span>
                                          </div>
                                          <div class="wf-success-banner">
                                            <span class="wf-seal-icon">⚖️</span>
                                            <div>
                                              <strong>Sanctuaire Mémoriel sous Protection Conservatoire</strong>
                                              <p class="wf-subtext">Respect absolu de la mémoire • Résolution sereine confiée à la médiation notariale</p>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-sub">Accéder à l'Espace de Recueillement Neutre</button>
                                          </div>
                                        </div>
```

</details>

---

<a id="uc-316"></a>
## UC-316 : Mode Hors-Ligne Extrême / Zone Blanche sans Réseau en Forêt Mémorielle (WebCrypto Local Ed25519)

### 📋 Métadonnées Spécifiées

| Propriété | Valeur Spécifiée |
| :--- | :--- |
| **Identifiant Unique** | `UC-316` |
| **Catégorie Métier** | **Sécurité & Résilience Hors-Ligne** |
| **Acteur Principal** | Famille en Forêt Cinéraire & Garde-Forestier |
| **Plateformes Cibles** | Natif (iOS & Android), Web Standard (PWA Hors-Ligne) |
| **Tags Clés** | `ZoneBlanche`, `HorsLigneExtreme`, `WebCrypto`, `Ed25519`, `TrustList`, `LocalFirst`, `EF-5` |
| **Base Légale & Normative** | Décision Kudoro DEC-AET-09 (universalité d'accès sans contact hors-ligne) & Charte de résilience mémorielle séculaire. |
| **Terminal / Canvas Wireframe** | `Sanctuaire Mobile • Moteur Cryptographique WebCrypto Hors-Ligne (EF-5)` |

### 🎯 Préconditions & Postconditions

> [!NOTE]
> **Préconditions Requises :**
> La famille se recueille au pied de l'Arbre du Souvenir au fond d'un massif forestier DNF, en zone blanche totale (zéro barre 4G/5G).

> [!TIP]
> **Postconditions Garanties :**
> L'intégrité cryptographique et l'authenticité sont démontrées à 100% sans nécessiter un seul bit échangé sur Internet.

### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)

1. Effleurement NFC sans contact de la carte mémorielle par le smartphone en pleine forêt isolée.
2. Le service worker de la PWA prend le relais à 100% sans tenter aucune requête HTTP distante.
3. Exécution locale de la validation cryptographique COSE_Sign1 via la bibliothèque WebCrypto (SubtleCrypto Ed25519).
4. Vérification de l'empreinte de la clé émettrice par rapport à la TrustList souveraine pré-enregistrée en stockage persistant.
5. Ouverture instantanée du sanctuaire mémoriel : affichage des portraits, lecture du testament et recueillement en pleine nature.

### 📝 Spécification des Champs de Saisie & Données

| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `network_status` | **Couverture Réseau Mobile** | `text` | `ZONE BLANCHE TOTALE (0 barre • Aucun réseau)` | - | `100% Déconnecté` | ⭕ Optionnel |
| `crypto_engine` | **Moteur Cryptographique** | `text` | `WebCrypto API Locale (SubtleCrypto Ed25519 / ES256)` | - | `In-Device` | ⭕ Optionnel |
| `embedded_trustlist` | **TrustList Souveraine Embarquée** | `text` | `TrustList v2.4 (24 clés de confiance Le Pax Funèbre)` | - | `Vérifié` | ⭕ Optionnel |
| `local_verify_time` | **Temps de Vérification Locale** | `text` | `18 millisecondes (Calcul mathématique local)` | - | `Instantané` | ⭕ Optionnel |

### ⚡ Boutons d'Action & Déclencheurs Interactifs

| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |
| :--- | :--- | :--- | :--- | :---: |
| `btn_verify_offline_crypto` | **Vérifier la Signature Ed25519 en Local (WebCrypto)** | `primary` | `idle` | 🌲 |
| `btn_open_forest_sanctuary` | **Entrer dans le Sanctuaire Forestier** | `secondary` | `idle` | 🕊️ |

### ✅ Critères de Succès & Validation Normative

> [!IMPORTANT]

> **Titre :** Authenticité Cryptographique Vérifiée 100% Hors-Ligne
>
> **Badge de Conformité :** `WebCrypto Ed25519 Valide`
>
> **Détail Opérationnel :** Signature COSE_Sign1 vérifiée en 18 ms via SubtleCrypto local. Chaîne de confiance souveraine validée sans réseau.

### ⚠️ Cas d'Erreur & Procédure de Remédiation

| Propriété d'Anomalie | Description Technique |
| :--- | :--- |
| **Code d'Erreur Normatif** | `ERR_OFFLINE_CACHE_UNAVAILABLE` |
| **Intitulé de l'Incident** | **Cache PWA Absent ou TrustList Non Initialisée Hors-Ligne** |
| **Condition Déclenchante** | Premier lancement de l'application effectué en zone blanche sans avoir préalablement mis en cache les assets. |
| **Message d'Erreur UI** | *« Erreur d'initialisation : Le cache de l'application est incomplet. Impossible d'exécuter la vérification locale sans les artefacts de base. »* |
| **Action Corrective Requise** | **Effectuer une première ouverture de l'application en zone connectée pour mettre en cache la TrustList et les modules WebCrypto.** |

### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)

*Canvas & Résolution Cible :* **Sanctuaire Mobile • Moteur Cryptographique WebCrypto Hors-Ligne (EF-5)**

| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Initial / Avant Trigger** | Recueillement en Forêt DNF sans Réseau | *En attente utilisateur* | La famille est réunie au pied de l'Arbre du Souvenir en zone blanche complète. |
| **2** | **Déclenchement ⚡** | Calcul Mathématique Local de la Signature Ed25519 | `Clic sur 'Vérifier la Signature Ed25519 en Local'` | Exécution de la formule RFC 8032 sur les courbes elliptiques directement dans le processeur du smartphone. |
| **3** | **Traitement ⚙️** | Authenticité Prouvée & Zéro Dépendance Serveur | `Progression : 100%` | Preuve mathématique irréfutable de la validité de la carte en 18 millisecondes. |
| **4** | **Scellement & Fin ✨** | Sanctuaire Mémoriel Ouvert en Pleine Forêt | `Statut : success` | Le recueillement s'opère en parfaite harmonie avec la nature, sans fil et sans dépendance. |

<details>
<summary>🔍 Consulter les fragments HTML Wireframe de UC-316 (4 États Dépliables)</summary>

#### Phase 1 - Avant Trigger : Recueillement en Forêt DNF sans Réseau
*La famille est réunie au pied de l'Arbre du Souvenir en zone blanche complète.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">Sanctuaire • Forêt Cinéraire DNF</span>
                                            <span class="wf-status-badge wf-badge-neutral">Hors-Ligne (0 Barre)</span>
                                          </div>
                                          <div class="wf-device-status-box">
                                            <span class="wf-qa-icon">🌲</span>
                                            <div><strong>Zone Blanche Forestière Détectée</strong></div>
                                            <div class="wf-subtext">Activation automatique du moteur de vérification cryptographique 100% local WebCrypto</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary">🌲 Vérifier la Signature Ed25519 en Local (WebCrypto)</button>
                                          </div>
                                        </div>
```

#### Phase 2 - Déclenchement : Calcul Mathématique Local de la Signature Ed25519
*Exécution de la formule RFC 8032 sur les courbes elliptiques directement dans le processeur du smartphone.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">Sanctuaire • WebCrypto Local</span>
                                            <span class="wf-status-badge wf-badge-trigger">⚡ Calcul In-Device</span>
                                          </div>
                                          <div class="wf-trigger-card wf-radar-pulse">
                                            <div class="wf-trigger-indicator">✓ SubtleCrypto.verify('Ed25519', key, signature, tbs)</div>
                                            <div class="wf-subtext">Vérification de l'enveloppe EF-5 contre la TrustList stockée dans IndexedDB</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary wf-pulse-btn">Calcul mathématique en cours...</button>
                                          </div>
                                        </div>
```

#### Phase 3 - Traitement : Authenticité Prouvée & Zéro Dépendance Serveur
*Preuve mathématique irréfutable de la validité de la carte en 18 millisecondes.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">Sanctuaire • Sceau Cryptographique</span>
                                            <span class="wf-status-badge wf-badge-process">⚙️ Preuve Établie (100%)</span>
                                          </div>
                                          <div class="wf-console-log">
                                            <code>> [OFFLINE-ENGINE] Zéro requête réseau émise • Mode souverain actif</code><br>
                                            <code>> [CRYPTO-VERIFY] Ed25519 signature VALID : R, S points vérifiés sur Curve25519</code><br>
                                            <code>> [TRUST-LIST] kid 9a8b7c6d... reconnu (PaxStation Namur)</code><br>
                                            <code>> [SOUVERAINETÉ] 100% autonome • Consultation garantie pour les 100 prochaines années</code>
                                          </div>
                                        </div>
```

#### Phase 4 - Fin de Cycle : Sanctuaire Mémoriel Ouvert en Pleine Forêt
*Le recueillement s'opère en parfaite harmonie avec la nature, sans fil et sans dépendance.*

```html
<div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">Sanctuaire • Forêt Cinéraire</span>
                                            <span class="wf-status-badge wf-badge-success">✨ Recueillement Ouvert</span>
                                          </div>
                                          <div class="wf-success-banner">
                                            <span class="wf-seal-icon">🍃</span>
                                            <div>
                                              <strong>Sanctuaire Mémoriel Actif en Forêt du Souvenir</strong>
                                              <p class="wf-subtext">Souveraineté cryptographique prouvée hors-ligne • Paix et sérénité sous les arbres</p>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-gold">🕊️ Écouter le Mémo Vocal sous l'Arbre du Souvenir</button>
                                          </div>
                                        </div>
```

</details>

---
