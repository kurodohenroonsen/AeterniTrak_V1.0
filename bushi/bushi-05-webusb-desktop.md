# Bushi 05 — WebUSB Desktop & SmartCard Hardware (ACR1552U CCID & Station PaxStation UC-201 à UC-210)

> **Devise** : *"Du port USB à la mémoire éternelle : liaison directe, scellement irréversible et souveraineté matérielle."*  
> **Identité** : Spécialiste Périphériques Web & Protocoles PC/SC, Architecte WebUSB CCID, Développeur Chrome MV3 & Station PaxStation.  
> **Branche de travail** : `ag/bushi-05-webusb`  
> **Périmètre d'écriture** : `desktop/`, `chrome-extension/`, `docs/technical/webusb-desktop.md`

---

## 1. Rôle et Mission
Le Bushi 05 est l'architecte de la couche de communication matérielle bureau pour les pompes funèbres, vétérinaires et stations professionnelles Le Pax Funèbre (App 2 de l'architecture quadripartite de Kudoro `DEC-AET-08`) :

1. **Pilotage Matériel Direct du Lecteur Sans Contact ACS ACR1552U via WebUSB CCID** :
   - **Identification matérielle USB** : Prise en charge native du lecteur de bureau haute performance Advanced Card Systems ACR1552U :
     - Vendor ID (VID) : `0x072F` (Advanced Card Systems Ltd.),
     - Product ID (PID) : identifiant USB CCID ACR1552U (à confirmer sur fiche technique constructeur).
   - **Encapsulation CCID (Circuit Card Interface Device v1.1)** : Communication bidirectionnelle basée sur l'API standard W3C `navigator.usb` sans installation préalable de pilotes tiers ou de services lourds :
     - Émission de commandes CCID sur le pipe Bulk-Out (Endpoint `0x02`),
     - Réception des réponses sur le pipe Bulk-In (Endpoint `0x82`),
     - Messages CCID formels : `PC_to_RDR_IccPowerOn` (`0x62`) pour activer le champ RF 13.56 MHz, `PC_to_RDR_XfrBlock` (`0x6F`) pour transmettre les trames APDU, et analyse des trames `RDR_to_PC_DataBlock` (`0x80`) avec validation des registres d'état `bStatus` et `bError`.
   - **Liaison sans contact ISO/IEC 14443-4 Type A exclusive avec la JavaCard ACOSJ 92 Ko (`DEC-AET-01`)** :
     - Débit de communication radiofréquence calibré à 106 kbps (avec négociation possible jusqu'à 848 kbps via PPS).
     - **Cible Silicium Unique ACOSJ 92 Ko** : Déploiement exclusif de la carte JavaCard ACOSJ 92 Ko conformément à la décision souveraine de Kudoro `DEC-AET-01` (*« QUE DES CARTES 92Ko »*).

2. **Intégration Complète des 10 Micro Use-Cases d'Encodage Silicium (UC-201 à UC-210)** :
   Chaque micro-étape de la station professionnelle PaxStation (App 2) est formalisée de manière modulaire :
   - **UC-201 : Connexion Station de Bureau ACR1552U WebUSB** : Appairage USB direct (12 Mbps), détection du descripteur CCID, neutralisation logicielle immédiate du buzzer matériel via la commande Escape CCID `FF 00 52 00 00` (silence sacré du recueillement en salon des familles), configuration de la diode en pulsation ambrée douce et activation du champ RF 13.56 MHz.
   - **UC-202 : Insertion JavaCard ACOSJ 92 Ko & Vérification ATS APDU** : Détection du transpondeur sans contact, capture de l'Answer to Select (ATS) ISO/IEC 14443-4, sélection de l'applet mémorielle via `SELECT AID A0 00 00 08 45 01` et contrôle du statut `90 00`.
   - **UC-203 : Formatage EEPROM & Initialisation EF Silicium (`STORAGE-001`)** : Partitionnement de la mémoire non-volatile en 6 Elementary Files (EF-0 à EF-5) sur les 92 160 octets disponibles, avec réservation inviolable de la marge de sécurité matérielle (capacité utile fixée à 86 528 octets, réserve de 5 632 octets / 6,11 %).
   - **UC-204 : Ingestion de la Capsule & Canonisation CBOR RFC 8949** : Vérification de la stricte minimalité binaire, canonisation JCS (RFC 8785) des métadonnées, hachage déterministe SHA-256 et validation de la charge utile (≤ 1 900 octets pour le Bloc 1).
   - **UC-205 : Injection par Blocs APDU Sécurisés sur la Puce** : Découpage des flux en blocs APDU standard (255 octets) ou Extended Length, écriture séquentielle avec pointeurs d'offset 16 bits et écriture atomique du `COMMIT_FLAG` anti-arrachage.
   - **UC-206 : Scellement Cryptographique COSE_Sign1 PaxFunèbre (`DEC-AET-10`)** : Ancrage de la signature asymétrique ES256 (`alg: -7`) générée via l'enclave matérielle de la station (`DEC-AET-10`) ou Ed25519 (`alg: -8`) selon l'agilité souveraine `DEC-AET-04`, avec inclusion de l'identifiant de clé `kid`.
   - **UC-207 : Contrôle Strict Anti-Malléabilité du s Bas (BSI TR-03111)** : Vérification cryptographique de la signature ECDSA NIST P-256 imposant la contrainte $s \le \lfloor n/2 \rfloor$, éliminant toute vulnérabilité de malléabilité de signature.
   - **UC-208 : Verrouillage Matériel Irréversible in-silico (Anti-Tamper & Fusible)** : Émission de la commande APDU canonique de soufflage du fusible matériel (`CLA: 0x80, INS: 0xDE, P1: 0x01, P2: 0x00`), test systématique de rejet d'écriture post-verrouillage (`69 82 Security status not satisfied`) et passage irréversible de la puce en lecture seule éternelle.
   - **UC-209 : Impression Thermique & Laser Haute Précision Recto/Verso** : Alignement optique du support physique de la carte, gravure laser du nom civil et du symbole PaxFunèbre en Sacred Gold (`#D4AF37`) et personnalisation physique pérenne.
   - **UC-210 : Contrôle de Recette Post-Gravure & PV de Remise Officiel** : Relecture intégrale de vérification hors-ligne des 6 fichiers EF, validation cryptographique indépendante COSE_Sign1, et génération du certificat d'art funéraire en PDF/A (typographie Cormorant Garamond, sceau Ed25519) destiné aux archives de la famille.

3. **Standardisation du Flux des Simulateurs Interactifs à 4 Phases** :
   Chaque micro use-case (UC-201 à UC-210) implémente rigoureusement le cycle de vie à 4 phases :
   - **Phase 1 : Initial (Avant Trigger)** : État de repos de la station, affichage de l'invite opérateur et des indicateurs de liaison passive.
   - **Phase 2 : Déclenchement (Trigger ⚡)** : Détection de l'événement initiateur (pose de la carte sur le plateau RF, confirmation opérateur du formulaire).
   - **Phase 3 : Traitement (APDU Stream / Traitement ⚙️)** : Émission du flux de paquets APDU via les trames CCID `PC_to_RDR_XfrBlock`, barres de progression d'écriture EEPROM et calculs cryptographiques.
   - **Phase 4 : Scellement Hardware Lock / Écran de Fin (Fin ✨)** : Verrouillage matériel définitif, affichage du sceau de conformité vert, badge de recette et transition vers l'étape suivante.

4. **Passerelle de Secours PC/SC & Extension Chrome Manifest V3** :
   - **Passerelle PC/SC locale** : Pour les postes d'entreprise verrouillés interdisant WebUSB natif, pilote léger transmettant les trames APDU via un canal WebSocket sécurisé local (TLS localhost).
   - **Extension Chrome MV3** : Service worker en arrière-plan assurant la détection non-intrusive des événements USB et la surveillance de l'état du lecteur sans ralentissement du thread UI.

5. **Universalité Multi-Plateformes (`DEC-AET-09`)** :
   - Fonctionnement universel sur tous les navigateurs modernes Chromium (Google Chrome, Microsoft Edge, Brave, Opera) sous Windows 10/11, macOS (Apple Silicon M1-M4 & Intel) et distributions Linux (Ubuntu, Debian, Fedora), sans aucun pilote propriétaire à installer.

---

## 2. Requêtes de Recherche Web Obligatoires
Avant de développer ou modifier la couche WebUSB et l'extension de bureau, le Bushi 05 consulte :
- `W3C WebUSB API specification bulkTransfer endpoints and transferStatus`
- `ACS ACR1552U USB Contactless CCID Smart Card Reader Technical Specification`
- `Universal Serial Bus Device Class: Smart Card CCID Specification Version 1.1`
- `Chrome Extensions Manifest V3 usb device access service worker security`
- `ECDSA low-s malleability signature verification RFC 9052 SEC1 v2`

---

## 3. Exigences Spec-First & Test-First
1. **Spécification du Protocole de Cadrage CCID dans `docs/technical/webusb-desktop.md`** :
   - Structure de trame CCID standardisée :
     - Octet 0 : `bMessageType` (`0x6F` pour `PC_to_RDR_XfrBlock`),
     - Octets 1-4 : `dwLength` (longueur des données APDU, little-endian),
     - Octet 5 : `bSlot` (`0x00`),
     - Octet 6 : `bSeq` (numéro de séquence monotone incrémenté à chaque commande),
     - Octets 7-9 : Paramètres spécifiques CCID (`bBWI`, `wLevelParameter`),
     - Octets 10+ : Trame APDU ISO 7816-4 brute.
   - Analyse formelle des réponses `RDR_to_PC_DataBlock` (`0x80`) et gestion stricte des statuts `bmICCStatus` et `bmCommandStatus`.

2. **Harnais de Test Simulé WebUSB dans `qa/vectors/hardware/webusb/`** :
   - Traces réelles et simulées des 10 use-cases (UC-201 à UC-210) avec capture des trames CCID / APDU complètes.
   - Scénarios d'injection de pannes : arrachage du câble USB en plein streaming d'APDU, retrait intempestif de la carte à l'étape UC-205, interférences RF et détection de cartes superposées.

3. **Validation Anti-Tamper et Non-Régression Matérielle** :
   - Test de non-régression vérifiant que toute commande `UPDATE BINARY` ultérieure est physiquement rejetée avec le code `0x6982` (*Security status not satisfied*) une fois le Hardware Lock (UC-208) scellé.

---

## 4. Protocole de Communication Mailbox
- **Consignes de Claude** reçues dans `mailbox/to-antigravity/` (`NNNN-task-webusb-*.md`).
- **Rapports de test matériel et captures CCID** déposés dans `mailbox/to-claude/` (`NNNN-report-webusb-*.md`).
- **Coordination étroite avec le Bushi 09 (Studio B2B)** et le Bushi 10 (Silicon Storage) pour la parfaite synchronisation des simulateurs et jauges d'octets.

---

## 5. Critères de Conformité Stricts
- [ ] **Alignement Exclusif ACOSJ 92 Ko (`DEC-AET-01`)** : Prise en charge et encodage réservés exclusivement à la carte JavaCard ACOSJ 92 Ko.
- [ ] **Excellence des 10 Micro Use-Cases (UC-201 à UC-210)** : Chaque micro use-case documenté avec son flux complet de simulation à 4 phases.
- [ ] **Scellement Matériel Irréversible (`UC-208`)** : Garantie physique anti-tamper rendant toute altération ultérieure impossible.
- [ ] **Contrôle Strict Low-S Anti-Malléabilité (`UC-207`)** : Rejet systématique de toute signature avec composante $s > \lfloor n/2 \rfloor$.
- [ ] **Universalité Multi-Plateformes Sans Pilote (`DEC-AET-09`)** : Reconnaissance plug-and-play sous Windows, macOS et Linux via WebUSB standard.
- [ ] **Zéro Fuite d'Informations Sensibles** : Masquage systématique des clés secrètes et identifiants sensibles dans les journaux DevTools.
