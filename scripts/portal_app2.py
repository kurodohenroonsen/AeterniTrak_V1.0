#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeterniTrak V1.0 — Définition Complète des Micro Use-Cases pour App 2 : PaxStation Encodage Silicium (UC-201 à UC-210)
Avec Simulateur de Wireframes Interactifs à 4 États, Spécifications des Formulaires, Actions, Validations et Erreurs Normatives.
"""

APP2_USECASES = [
    {
        "id": "UC-201",
        "title": "Connexion Station de Bureau ACR1552U WebUSB & Session Opérateur Funéraire",
        "cat": "Matériel & Poste Pro",
        "actor": "Opérateur d'Encodage & Conseiller Funéraire",
        "platforms": ["WebUSB (Chromium Desktop)", "PC/SC (Desktop Natif)"],
        "tags": ["ACR1552U", "WebUSB", "PCSC", "SessionOperateur", "StrongBox", "DEC-AET-10", "ACOSJ92k"],
        "preconditions": "Poste de travail d'agence avec lecteur ACR1552U branché sur port USB 3.0 et enclave cryptographique active de la station (DEC-AET-10).",
        "flow": [
            "Ouverture de PaxStation Encodage sur Chromium Desktop avec détection USB CCID du lecteur ACR1552U (VID 0x072F / PID 0x2200).",
            "Saisie et contrôle du formulaire d'ouverture de session : ID Conseiller/Opérateur et présentation du Badge Agence PaxFunèbre.",
            "Authentification et initialisation de l'Enclave Cryptographique active de la station (StrongBox / Secure Enclave ES256 DEC-AET-10).",
            "Sélection et allocation du lot de puces JavaCard ACOSJ 92 Ko homologuées pour la série d'encodage.",
            "Passage du voyant LED du lecteur au vert fixe (état prêt) et ouverture du canal sans contact 106 kbps ISO/IEC 14443-4."
        ],
        "postconditions": "Session opérateur funéraire ouverte, enclave ES256 prête (DEC-AET-10), lot ACOSJ 92 Ko assigné et canal USB CCID 12 Mbps opérationnel.",
        "legal": "Spécification USB CCID (Integrated Circuit(s) Cards Interface Device, USB-IF) et politique de sécurité opérationnelle PaxFunèbre (décision souveraine DEC-AET-10).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "desktop",
            "deviceLabel": "PaxStation Station Pro • Session Opérateur & Console ACR1552U (DEC-AET-10)",
            "formFields": [
                {"label": "ID Conseiller / Opérateur", "name": "operator_id", "type": "text", "value": "OP-NAM-8842 (Marc Lambert)", "placeholder": "Identifiant opérateur", "badge": "Authentifié", "required": True},
                {"label": "Badge Agence PaxFunèbre", "name": "agency_badge", "type": "text", "value": "PaxFunèbre Namur Centre #AG-04 (Habilitation H3)", "placeholder": "Badge agence", "badge": "Habilité H3", "required": True},
                {"label": "Enclave Cryptographique Station", "name": "crypto_enclave", "type": "select", "value": "Station Secure Enclave / StrongBox (ES256 DEC-AET-10)", "placeholder": "Enclave matérielle", "badge": "DEC-AET-10", "required": True},
                {"label": "Sélection du Lot de Cartes ACOSJ 92 Ko", "name": "card_lot", "type": "select", "value": "Lot ACOSJ-92K-2026-N1 (JavaCard 92 160 octets)", "placeholder": "Lot silicium", "badge": "92 Ko EEPROM", "required": True},
                {"label": "Pilote & Matériel Détecté", "name": "usb_driver", "type": "text", "value": "ACS ACR1552U USB CCID v1.1 (VID:072F / PID:2200 - 12 Mbps)", "placeholder": "Pilote", "badge": "WebUSB Direct", "required": False},
                {"label": "Liaison RF & Baudrate", "name": "rf_link", "type": "text", "value": "13.56 MHz • 106 kbps ISO/IEC 14443 Type A", "placeholder": "Baudrate RF", "badge": "106 kbps", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_open_session", "label": "Authentifier l'Opérateur & Ouvrir Session", "role": "primary", "state": "idle", "icon": "🔐"},
                {"id": "btn_test_enclave", "label": "Tester Enclave ES256 & Bip Sonore", "role": "secondary", "state": "idle", "icon": "🛡️"},
                {"id": "btn_connect_acr", "label": "Autoriser l'Accès WebUSB ACR1552U", "role": "secondary", "state": "idle", "icon": "🔌"}
            ],
            "validationMsg": {
                "title": "Session Opérateur Funéraire Ouverte & Station Prête",
                "badge": "Enclave ES256 Active (DEC-AET-10)",
                "detail": "Opérateur OP-NAM-8842 identifié. Enclave matérielle de station armée. Lot ACOSJ 92 Ko verrouillé. Lecteur ACR1552U en veille RF 106 kbps."
            },
            "errorCase": {
                "code": "ERR_OPERATOR_AUTH_OR_ENCLAVE_FAILED",
                "title": "Échec d'Authentification Opérateur ou Enclave Indisponible",
                "condition": "Badge opérateur non reconnu, identifiant conseiller invalide ou échec de poignée de main avec l'enclave sécurisée de la station.",
                "message": "Accès refusé : La station d'encodage ne peut s'authentifier auprès de l'enclave cryptographique (DEC-AET-10) ou le badge opérateur est invalide.",
                "remediation": "Vérifier le badge d'agence PaxFunèbre, s'assurer que le module StrongBox / Secure Enclave est disponible et relancer l'identification."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Formulaire d'Ouverture de Session & Authentification Station",
                    "caption": "Formulaire opérateur en attente. ID Conseiller, badge agence et sélection du lot ACOSJ 92 Ko prêts à être validés.",
                    "screenHtml": """
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
                        <div><strong>Lecteur ACS ACR1552U détecté (VID:072F / PID:2200)</strong></div>
                        <div class="wf-subtext">Liaison WebUSB 12 Mbps • En attente de déverrouillage de la session opérateur</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔐 Authentifier l'Opérateur & Ouvrir Session</button>
                        <button class="wf-btn wf-btn-sub">🛡️ Tester Enclave ES256</button>
                      </div>
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Validation des Accréditations Opérateur & Déverrouillage Enclave",
                    "triggerName": "Tap du badge agence et clic sur 'Authentifier l'Opérateur & Ouvrir Session'",
                    "caption": "Validation biométrique/badge opérateur et appel sécurisé du module Enclave Cryptographique (DEC-AET-10).",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Initialisation de l'Enclave Matérielle & Armement RF 13.56 MHz",
                    "progress": 85,
                    "caption": "Armement de l'enclave station pour signatures ES256 (DEC-AET-10) et mise en veille active du lecteur.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Session Opérateur Ouverte & Station Prête pour Gravure",
                    "status": "success",
                    "caption": "Station authentifiée et prête. L'opérateur peut déposer la première JavaCard ACOSJ 92 Ko.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-202",
        "title": "Insertion JavaCard ACOSJ 92 Ko & Vérification ATS APDU",
        "cat": "Silicium & Détection",
        "actor": "Opérateur d'Encodage",
        "platforms": ["WebUSB (Chromium Desktop)", "PC/SC (Desktop Natif)"],
        "tags": ["ACOSJ", "JavaCard", "ATS", "APDU", "ISO14443-4"],
        "preconditions": "Lecteur ACR1552U connecté et en écoute RF.",
        "flow": [
            "L'opérateur dépose la carte vierge ou le médaillon sur la zone sans contact du lecteur.",
            "Détection du champ de proximité et émission de l'Answer to Select (ATS) conforme ISO/IEC 14443-4.",
            "Négociation du Protocole Parameter Selection (PPS) pour confirmation de la vitesse de 106 kbps.",
            "Sélection de l'Applet AeterniTrak via commande APDU `SELECT AID A0 00 00 08 45 01` et vérification du code de statut `90 00`.",
            "Lecture de l'historique EEPROM pour confirmer la mémoire disponible de 92 Ko (ACOSJ)."
        ],
        "postconditions": "Puce identifiée de manière unique, applet AeterniTrak active et prête pour l'initialisation.",
        "legal": "Norme ISO/IEC 7816-4 (organisation, sécurité et commandes pour les échanges d'informations).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "desktop",
            "deviceLabel": "PaxStation Station Pro • Moniteur APDU Silicium ISO 7816",
            "formFields": [
                {"label": "Modèle Silicium", "name": "chip_model", "type": "text", "value": "ACOSJ JavaCard 3.0.4 Classic (92 Ko EEPROM)", "placeholder": "Puce", "badge": "Certifié", "required": False},
                {"label": "Réponse ATS Puce", "name": "ats_bytes", "type": "text", "value": "3B 80 80 01 01 (ISO 14443-4 T=CL)", "placeholder": "ATS", "badge": "IsoDep", "required": False},
                {"label": "AID AeterniTrak", "name": "applet_aid", "type": "text", "value": "A0 00 00 08 45 01 (Applet Active)", "placeholder": "AID", "badge": "Sélectionné", "required": False},
                {"label": "Statut SW APDU", "name": "status_word", "type": "text", "value": "90 00 (Opération avec succès)", "placeholder": "SW", "badge": "Succès", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_select_aid", "label": "Interroger le Silicium (ATS & SELECT AID)", "role": "primary", "state": "idle", "icon": "💳"},
                {"id": "btn_eject_card", "label": "Éjecter / Réinitialiser RF", "role": "secondary", "state": "idle", "icon": "⏏️"}
            ],
            "validationMsg": {
                "title": "JavaCard ACOSJ 92k Détectée",
                "badge": "Code APDU 90 00",
                "detail": "Puce authentique homologuée. 92 160 octets d'EEPROM libre identifiés."
            },
            "errorCase": {
                "code": "ERR_ATS_COMMUNICATION_TIMEOUT",
                "title": "Délai de Réponse ATS Expiré",
                "condition": "Mauvais alignement de la carte sur l'antenne ou puce incompatible (non-JavaCard ou Mifare Classic).",
                "message": "Erreur silicium : La puce présentée ne répond pas aux commandes APDU IsoDep ISO 14443-4.",
                "remediation": "Repositionner la carte au centre du lecteur ACR1552U ou remplacer la carte par une JavaCard ACOSJ 92 Ko homologuée."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Champ RF en Écoute, Aucune Carte Présente",
                    "caption": "Lecteur prêt. L'antenne cherche une carte à portée de couplage électromagnétique.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Apposition Physique de la Carte sur le Lecteur",
                    "triggerName": "Pose de la JavaCard ACOSJ sur le lecteur et émission de l'ATS",
                    "caption": "Couplage inductif établi, bip de détection sonore et voyant bleu clignotant.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Échange APDU `SELECT AID` & Lecture Registres",
                    "progress": 70,
                    "caption": "Envoi de la commande `00 A4 04 00 07 A0 00 00 08 45 01` et vérification du code 90 00.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Carte ACOSJ Validée pour Gravure",
                    "status": "success",
                    "caption": "Puce prête pour l'allocation des fichiers élémentaires EF-1, EF-2 et EF-3.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-203",
        "title": "Formatage EEPROM & Initialisation EF Silicium (STORAGE-001)",
        "cat": "Système de Fichiers Puce",
        "actor": "Opérateur d'Encodage",
        "platforms": ["WebUSB (Chromium Desktop)", "PC/SC (Desktop Natif)"],
        "tags": ["EEPROM", "EF", "STORAGE-001", "Allocation"],
        "preconditions": "JavaCard sélectionnée avec succès et authentifiée en mode administration.",
        "flow": [
            "Envoi de la commande APDU de formatage sécurisé pour effacement des anciennes structures ou résidus d'usine.",
            "Création du Master File (MF) et du Dedicated File (DF AeterniTrak).",
            "Création des six Fichiers Élémentaires (EF-0 à EF-5) prescrits par STORAGE-001 (table canonique 86 528 octets utiles / 92 160 octets total) :",
            "- `EF-0 (Header/UID)` : 512 octets réservés pour passeport matériel TLV, UID, flags.",
            "- `EF-1 (Profile)` : 2 048 octets réservés pour profil CBOR civil mémoriel canonique.",
            "- `EF-2 (Portrait)` : 20 480 octets réservés pour portrait WebP 480×480 px (DEC-AET-12).",
            "- `EF-3 (Voice)` : 46 080 octets réservés pour mémo vocal Opus SILK 16 kHz.",
            "- `EF-4 (Registry)` : 15 360 octets réservés pour registre sépulture & hommages.",
            "- `EF-5 (Signature)` : 2 048 octets réservés pour enveloppe COSE_Sign1 scellée.",
            "- `Réserve d'usure matérielle` : 5 632 octets (6,11 % > plancher de 5 % garanti pour wear-leveling).",
            "Vérification de l'absence de fragmentation mémoire."
        ],
        "postconditions": "Système de fichiers silicium initialisé selon la table canonique stricte du jalon STORAGE-001 (86 528 octets utiles / 92 160 octets total).",
        "legal": "Spécification technique AeterniTrak STORAGE-001 (allocation EEPROM JavaCard).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "desktop",
            "deviceLabel": "PaxStation Station Pro • Partitionneur EEPROM Silicium (STORAGE-001)",
            "formFields": [
                {"label": "Partitions Utiles (EF-0 à EF-5)", "name": "useful_size", "type": "text", "value": "86 528 octets utiles (6 EF alloués)", "placeholder": "Taille utile", "badge": "86 528 o", "required": True},
                {"label": "Réserve d'Usure / Wear-Leveling", "name": "wear_reserve", "type": "text", "value": "5 632 octets (6,11 % > 5 %)", "placeholder": "Réserve", "badge": "5 632 o", "required": True},
                {"label": "Total Silicium EEPROM", "name": "total_allocated", "type": "text", "value": "92 160 octets (100% sans fragmentation)", "placeholder": "Total", "badge": "92 160 o", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_format_eeprom", "label": "Initialiser la Structure EF Silicium (STORAGE-001)", "role": "primary", "state": "idle", "icon": "🗄️"},
                {"id": "btn_check_ef", "label": "Vérifier Table d'Allocation EF", "role": "secondary", "state": "idle", "icon": "🔍"}
            ],
            "validationMsg": {
                "title": "Système de Fichiers Silicium Initialisé",
                "badge": "Table Canonique STORAGE-001",
                "detail": "Table canonique allouée : 86 528 octets utiles (EF-0 à EF-5), 5 632 octets réserve (6,11 %), total 92 160 octets."
            },
            "errorCase": {
                "code": "ERR_EEPROM_QUOTA_EXCEEDED",
                "title": "Dépassement de la Capacité EEPROM",
                "condition": "Tentative d'allocation d'une partition dont la taille dépasse les 86 528 octets utiles de la puce physique.",
                "message": "Erreur d'allocation : La somme des partitions demandées dépasse le budget utile canonique de 86 528 octets.",
                "remediation": "Restaurer les tailles standard prescrites par la table canonique (86 528 octets utiles, 5 632 octets réserve, 92 160 octets total)."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "EEPROM Vierge Non Partitionnée",
                    "caption": "Carte connectée. La table canonique des fichiers EF-0 à EF-5 n'est pas encore créée.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Clic sur 'Initialiser la Structure EF Silicium'",
                    "triggerName": "Émission des commandes APDU de création des fichiers EF-0 à EF-5",
                    "caption": "Ordre d'écriture physique de la structure de répertoires in-silico.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Écriture APDU des Descripteurs EF & Vérification Codes 90 00",
                    "progress": 85,
                    "caption": "La puce confirme la création de chaque bloc de mémoire flash.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Structure Canonique EF-0 à EF-5 Initialisée avec Succès",
                    "status": "success",
                    "caption": "Système de fichiers prêt pour recevoir les flux de données compressés.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-204",
        "title": "Ingestion de la Capsule & Canonisation CBOR RFC 8949",
        "cat": "Compilation & Core",
        "actor": "Opérateur d'Encodage",
        "platforms": ["WebUSB (Chromium Desktop)", "Node.js / Core Engine"],
        "tags": ["Capsule", "Ingestion", "CBOR", "RFC8949", "JCS"],
        "preconditions": "Fichier capsule `.cbor` reçu depuis PaxStudio via réseau local ou clé de transfert.",
        "flow": [
            "Chargement du binaire de la capsule et contrôle de syntaxe CBOR stricte.",
            "Vérification de l'absence d'octets résiduels après le payload (règle anti-injection REJ006).",
            "Recalcul indépendant de l'empreinte SHA-256 canonique JCS de la charge utile.",
            "Confrontation de l'empreinte avec l'ordre de fabrication BAT signé par la famille."
        ],
        "postconditions": "Capsule 100% validée, conforme à l'ordre BAT, prête pour le découpage en blocs APDU.",
        "legal": "Spécification technique IETF RFC 8949 (CBOR Deterministic Encoding Rules §4.2.1).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "desktop",
            "deviceLabel": "PaxStation Station Pro • Validateur Canonique CBOR RFC 8949",
            "formFields": [
                {"label": "Fichier Source", "name": "capsule_file", "type": "file", "value": "capsule_paxstudio_78k.cbor (78 412 octets)", "placeholder": "Capsule", "badge": "Source", "required": True},
                {"label": "Contrôle Octets Résiduels", "name": "trailing_bytes", "type": "text", "value": "0 octet superflu (Règle REJ006 respectée)", "placeholder": "Résidus", "badge": "REJ006 OK", "required": False},
                {"label": "Hash Recalculé JCS", "name": "hash_jcs", "type": "text", "value": "a4f81c90...b1297e41", "placeholder": "SHA-256", "badge": "Calculé", "required": False},
                {"label": "Concordance Ordre BAT", "name": "bat_match", "type": "text", "value": "100% IDENTIQUE à l'ordre n° ORD-2026-0491", "placeholder": "BAT", "badge": "Conforme", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_validate_capsule", "label": "Vérifier & Découper en Blocs APDU", "role": "primary", "state": "idle", "icon": "📦"},
                {"id": "btn_view_cbor_tree", "label": "Inspecter Arbre Détaillé CBOR", "role": "secondary", "state": "idle", "icon": "🌳"}
            ],
            "validationMsg": {
                "title": "Capsule CBOR Parfaitement Conforme",
                "badge": "Empreinte BAT Validée",
                "detail": "Zéro octet superflu. Hachage SHA-256 concordant avec le Bon à Tirer signé."
            },
            "errorCase": {
                "code": "ERR_CBOR_REJ006_TRAILING_BYTES",
                "title": "Présence d'Octets Résiduels Post-Enveloppe",
                "condition": "Fichier corrompu ou injection de données après la fin de la carte CBOR.",
                "message": "Erreur d'intégrité : Présence d'octets résiduels après la fermeture de l'enveloppe CBOR (violation règle REJ006).",
                "remediation": "Rejeter la capsule et redemander une génération propre depuis PaxStudio."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Capsule Reçue en Attente d'Audit d'Intégrité",
                    "caption": "Fichier de 78 Ko chargé. La vérification d'empreinte contre le BAT n'est pas encore faite.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Lancement du Contrôle d'Intégrité & Canonisation",
                    "triggerName": "Clic sur 'Vérifier & Découper en Blocs APDU'",
                    "caption": "Décodage déterministe binaire et calcul du SHA-256 en mémoire vive.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Découpage en 306 Blocs APDU de 255 Octets",
                    "progress": 88,
                    "caption": "Segmentation des 78 Ko pour injection séquentielle via la commande IsoDep `UPDATE BINARY`.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Capsule Prête pour Gravure Silicium",
                    "status": "success",
                    "caption": "Les 306 blocs sont mis en file d'attente d'écriture sur la puce ACOSJ.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-205",
        "title": "Injection par Blocs APDU Sécurisés sur la Puce",
        "cat": "Gravure Silicium",
        "actor": "Opérateur d'Encodage",
        "platforms": ["WebUSB (Chromium Desktop)", "PC/SC (Desktop Natif)"],
        "tags": ["APDU", "UpdateBinary", "IsoDep", "Gravure"],
        "preconditions": "Structure EF créée et capsule découpée en 306 blocs.",
        "flow": [
            "Sélection successive des fichiers `EF-0` à `EF-5` via `SELECT FILE`.",
            "Envoi cadencé des commandes APDU `UPDATE BINARY` (commande `00 D6 P1 P2 Lc [Octets]`).",
            "Contrôle systématique du mot de statut `90 00` en réponse à chaque bloc.",
            "Gestion des reprises sur incident : si un bloc échoue, rejeu automatique (max 3 tentatives).",
            "Mise à jour en temps réel de la barre de progression pour l'opérateur."
        ],
        "postconditions": "86 528 octets gravés avec succès dans l'EEPROM de la JavaCard ACOSJ (table canonique).",
        "legal": "Spécification technique ISO/IEC 7816-4 §7.2 (commandes d'écriture binaire).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "desktop",
            "deviceLabel": "PaxStation Station Pro • Graveur Silicium APDU IsoDep",
            "formFields": [
                {"label": "Nombre de Blocs", "name": "block_count", "type": "text", "value": "340 blocs de 255 octets", "placeholder": "Blocs", "badge": "Table Canonique", "required": False},
                {"label": "Vitesse de Transfert", "name": "transfer_rate", "type": "text", "value": "14.2 Ko/sec (106 kbps IsoDep)", "placeholder": "Débit", "badge": "106k", "required": False},
                {"label": "Taux d'Erreur APDU", "name": "error_rate", "type": "text", "value": "0 erreur (acquittements 90 00)", "placeholder": "Erreurs", "badge": "0 Défaut", "required": False},
                {"label": "Temps Écoulé", "name": "elapsed_time", "type": "text", "value": "06.1 secondes", "placeholder": "Temps", "badge": "Chrono", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_start_burning", "label": "Lancer la Gravure Silicium", "role": "primary", "state": "idle", "icon": "🔥"},
                {"id": "btn_pause_burning", "label": "Mettre en Pause", "role": "secondary", "state": "idle", "icon": "⏸"}
            ],
            "validationMsg": {
                "title": "Gravure Silicium Achevée avec Succès",
                "badge": "Table Canonique Écrite (90 00)",
                "detail": "86 528 octets injectés dans les partitions EF-0 à EF-5 sans aucune erreur."
            },
            "errorCase": {
                "code": "ERR_APDU_WRITE_FAILURE",
                "title": "Échec de Transmission d'un Bloc APDU",
                "condition": "Micro-déplacement de la carte sur l'antenne provoquant un code statut `6A 84` ou perte de liaison.",
                "message": "Erreur d'écriture : Rupture de liaison RF lors de l'injection d'un bloc.",
                "remediation": "Laisser la carte immobile au contact de l'antenne et relancer la procédure d'écriture automatique."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Graveur en Attente de Démarrage",
                    "caption": "Les blocs sont prêts. La jauge d'écriture est à 0%.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Lancement de la Rafale de Commandes APDU",
                    "triggerName": "Clic sur 'Lancer la Gravure Silicium' et sélection des fichiers EF-0 à EF-5",
                    "caption": "Lancement de la boucle cadencée d'envoi des commandes UPDATE BINARY.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Injection en Cours : Blocs Silicium (65%)",
                    "progress": 65,
                    "caption": "Écriture active dans les cellules EEPROM avec acquittement 90 00 systématique.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Gravure Silicium Accomplie à 100%",
                    "status": "success",
                    "caption": "Totalité des 86 528 octets utiles gravés avec intégrité absolue.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-206",
        "title": "Scellement Cryptographique COSE_Sign1 PaxFunèbre (Enclave Station DEC-AET-10)",
        "cat": "Cryptographie & Signature",
        "actor": "Opérateur d'Encodage",
        "platforms": ["WebUSB (Chromium Desktop)", "PC/SC (Desktop Natif)"],
        "tags": ["COSE_Sign1", "Ed25519", "ES256", "EnclaveStation", "DEC-AET-10", "RFC9052"],
        "preconditions": "Données gravées sur la puce mais non encore signées.",
        "flow": [
            "Appel à l'enclave sécurisée de la station (PaxStation Enclave sous DEC-AET-10).",
            "Construction de la structure canonique `Sig_structure` COSE_Sign1 (Tag 18, DEC-AET-10) selon la RFC 9052 :",
            "- Contexte : `\"Signature1\"`",
            "- En-tête protégé : `{1: -8, 16: \"application/aeternitrak-profile+cbor\"}` (Ed25519) ou `{1: -7}` (ES256)",
            "- Données associées externes : `h''` (vide)",
            "- Charge utile : le condensat SHA-256 de la capsule",
            "Génération de la signature cryptographique par la clé d'autorité officielle de l'enclave station.",
            "Écriture de l'enveloppe signée COSE_Sign1 dans le fichier dédié `EF-5` (0x0005) de la carte."
        ],
        "postconditions": "Carte physique scellée par l'enclave station (DEC-AET-10) avec signature COSE_Sign1 officielle infalsifiable.",
        "legal": "Spécification technique IETF RFC 9052 (COSE Structures and Process) et RFC 9596 (COSE typ Header).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "desktop",
            "deviceLabel": "PaxStation Station Pro • Module de Signature Matérielle Enclave (DEC-AET-10)",
            "formFields": [
                {"label": "Module Enclave Station", "name": "hsm_module", "type": "text", "value": "PaxStation Enclave Sécurisée (DEC-AET-10)", "placeholder": "Enclave", "badge": "DEC-AET-10", "required": False},
                {"label": "Algorithme Utilisé", "name": "sig_alg", "type": "select", "value": "Ed25519 (EdDSA, alg: -8, RFC 8032)", "placeholder": "Algorithme", "badge": "Recommandé", "required": True},
                {"label": "Type MIME Protégé (typ)", "name": "mime_typ", "type": "text", "value": "application/aeternitrak-profile+cbor (RFC 9596)", "placeholder": "Type", "badge": "Protégé", "required": False},
                {"label": "Empreinte Clé Publique (kid)", "name": "key_kid", "type": "text", "value": "3c81e592...71aa (16 octets SHA-256)", "placeholder": "kid", "badge": "16 Octets", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_sign_cose", "label": "Générer le Sceau Matériel COSE_Sign1 (DEC-AET-10)", "role": "primary", "state": "idle", "icon": "🔐"},
                {"id": "btn_inspect_sig_struct", "label": "Inspecter Sig_structure", "role": "secondary", "state": "idle", "icon": "🔍"}
            ],
            "validationMsg": {
                "title": "Sceau Cryptographique COSE_Sign1 Apposé",
                "badge": "Tag 18 • Enclave DEC-AET-10",
                "detail": "Enveloppe signée par l'enclave station (DEC-AET-10) et gravée sur EF-5. Intégrité infalsifiable garantie sans contact."
            },
            "errorCase": {
                "code": "ERR_COSE_EXPIRED_KEY",
                "title": "Clé de Scellement Enclave Expirée",
                "condition": "Tentative de signature avec une enclave dont le certificat d'autorité est expiré.",
                "message": "Erreur de sécurité : La clé matérielle de scellement a dépassé sa date limite de validité.",
                "remediation": "Procéder au renouvellement de clé auprès de l'autorité centrale AeterniTrak."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Données Gravées Non Signées",
                    "caption": "Puce écrite. La partition EF-5 est vide, le sceau officiel n'est pas encore apposé.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Appel à l'Enclave Station (DEC-AET-10) & Construction de la Sig_structure",
                    "triggerName": "Clic sur 'Générer le Sceau Matériel COSE_Sign1 (DEC-AET-10)'",
                    "caption": "Assemblage des en-têtes protégés déterministes et scellement par l'enclave station (DEC-AET-10).",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Signature Déterministe RFC 8032 & Injection sur EF-5",
                    "progress": 92,
                    "caption": "Double hachage SHA-512 sans aléa et écriture de l'enveloppe de 64 octets sur la puce.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Sceau COSE_Sign1 Scellé sur le Silicium",
                    "status": "success",
                    "caption": "La carte est cryptographiquement protégée. Toute tentative d'altération sera détectée.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-207",
        "title": "Contrôle Strict Anti-Malléabilité du s Bas (RFC 9052)",
        "cat": "Sécurité Mathématique",
        "actor": "Opérateur & Moteur de Sécurité",
        "platforms": ["WebUSB (Chromium Desktop)", "Node.js / Core Engine"],
        "tags": ["Malleabilite", "s-bas", "RFC9052", "BSI-TR03111", "ES256"],
        "preconditions": "Signature générée (particulièrement en cas d'utilisation d'ECDSA P-256).",
        "flow": [
            "Extraction des scalaires mathématiques `r` et `s` de la signature de 64 octets.",
            "Si algorithme ES256 (P-256) : évaluation de la condition de non-malléabilité du BSI TR-03111 §4.1.3 :",
            "- Ordre du sous-groupe $n = \\text{0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551}$",
            "- Contrôle formel : $s \\le \\lfloor n/2 \\rfloor$.",
            "Si $s > \\lfloor n/2 \\rfloor$, normalisation obligatoire immédiate : $s' = n - s$.",
            "Vérification que la signature ne peut faire l'objet d'aucune malléabilité par un tiers."
        ],
        "postconditions": "Signature mathématiquement canonique avec s bas garanti, conforme aux plus hauts standards.",
        "legal": "Guide BSI TR-03111 (Technical Guideline: Elliptic Curve Cryptography §4.1.3).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "desktop",
            "deviceLabel": "PaxStation Station Pro • Oracle Anti-Malléabilité Cryptographique",
            "formFields": [
                {"label": "Composante Scalaire r", "name": "sig_r", "type": "text", "value": "0x4a18c092...38ab (32 octets)", "placeholder": "Scalaire r", "badge": "r ∈ [1, n-1]", "required": False},
                {"label": "Composante Scalaire s", "name": "sig_s", "type": "text", "value": "0x391fe018...91ca (32 octets)", "placeholder": "Scalaire s", "badge": "s Bas", "required": False},
                {"label": "Seuil floor(n/2)", "name": "half_n", "type": "text", "value": "0x7fffffff...7e28", "placeholder": "n/2", "badge": "Seuil BSI", "required": False},
                {"label": "Statut Anti-Malléabilité", "name": "malleability_status", "type": "text", "value": "CONFORME (s < floor(n/2) vérifié)", "placeholder": "Statut", "badge": "Sécurisé", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_verify_s_low", "label": "Vérifier la Condition Mathématique s Bas", "role": "primary", "state": "idle", "icon": "📐"},
                {"id": "btn_simulate_s_high", "label": "Simuler Rejet s Haut Malléable", "role": "secondary", "state": "idle", "icon": "🧪"}
            ],
            "validationMsg": {
                "title": "Signature Anti-Malléable Conforme",
                "badge": "BSI TR-03111 §4.1.3 OK",
                "detail": "s bas garanti (s <= floor(n/2)). Zéro risque de signature alternative malléable."
            },
            "errorCase": {
                "code": "ERR_COSE_MALLEABLE_S",
                "title": "Signature Malléable Détectée (s Haut)",
                "condition": "Génération d'une signature ECDSA P-256 dont la valeur s excède floor(n/2).",
                "message": "Rejet cryptographique : Composante s haute détectée. La signature viole la RFC 9052 et le BSI TR-03111.",
                "remediation": "Normaliser impérativement la signature en remplaçant s par (n - s) avant gravure sur le silicium."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Signature Brute en Attente de Contrôle Scalaire",
                    "caption": "Signature extraite. Le calcul de la position par rapport au pivot n/2 est en attente.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Clic sur 'Vérifier la Condition Mathématique s Bas'",
                    "triggerName": "Évaluation arithmétique multiprécision de l'inégalité s <= floor(n/2)",
                    "caption": "Comparaison grand entier sur les 256 bits du scalaire de la courbe.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Comparaison BigInt & Normalisation In-Silico",
                    "progress": 96,
                    "caption": "La comparaison arithmétique confirme que le scalaire est dans la moitié basse.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Non-Malléabilité Mathématique Démontrée",
                    "status": "success",
                    "caption": "Signature inaltérable et non rejouable validée pour le verrouillage définitif.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-208",
        "title": "Verrouillage Matériel Irréversible in-silico (Anti-Tamper)",
        "cat": "Sécurité Silicium",
        "actor": "Opérateur d'Encodage",
        "platforms": ["WebUSB (Chromium Desktop)", "PC/SC (Desktop Natif)"],
        "tags": ["Lock", "Fusible", "ReadOnly", "AntiTamper", "Securite"],
        "preconditions": "Données gravées, enveloppe COSE_Sign1 scellée et validée.",
        "flow": [
            "Affichage d'un avertissement solennel : l'opération est irréversible et passera la puce en lecture seule définitive.",
            "Saisie du code de confirmation sécurisé de l'opérateur habilité.",
            "Envoi de la commande APDU propriétaire `LOCK APPLICATION` (fusible logiciel et matériel).",
            "Destruction des clés d'administration EEPROM dans la puce ACOSJ et claquage du bit fusible in-silico.",
            "Tentative de réécriture de test : la puce doit impérativement retourner le code d'erreur `69 82` (Security status not satisfied)."
        ],
        "postconditions": "Carte physique verrouillée définitivement en lecture seule, protégée contre toute altération matérielle.",
        "legal": "Spécification JavaCard 3.0 Classic (Security and Applet Lifecycle Management).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "desktop",
            "deviceLabel": "PaxStation Station Pro • Console de Verrouillage Matériel in-silico",
            "formFields": [
                {"label": "État du Fusible Silicium", "name": "fuse_state", "type": "text", "value": "Mode R/W Déverrouillé (Opérateur)", "placeholder": "Fusible", "badge": "Ouvert", "required": False},
                {"label": "Code de Confirmation", "name": "confirm_lock_code", "type": "text", "value": "LOCK-PERMANENT-ACOSJ", "placeholder": "Saisir code", "badge": "IRRÉVERSIBLE", "required": True},
                {"label": "Mode Cible Puce", "name": "target_mode", "type": "text", "value": "Lecture Seule Définitive (Read-Only RO)", "placeholder": "Cible", "badge": "RO Scellé", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_lock_fuse", "label": "Verrouiller Définitivement la Carte (Fusible in-silico)", "role": "danger", "state": "idle", "icon": "🔒"},
                {"id": "btn_cancel_lock", "label": "Annuler l'Opération", "role": "secondary", "state": "idle", "icon": "✕"}
            ],
            "validationMsg": {
                "title": "Carte Verrouillée Définitivement in-silico",
                "badge": "Fusible Claqué • Mode Read-Only",
                "detail": "Clés d'écriture détruites. Toute tentative de réécriture rejetée (code 69 82)."
            },
            "errorCase": {
                "code": "ERR_SILICON_FUSE_BLOWN",
                "title": "Carte Déjà Verrouillée Matériellement",
                "condition": "Tentative de verrouillage d'une puce dont le fusible est déjà claqué ou commande avortée.",
                "message": "Erreur silicium : La carte est déjà scellée en lecture seule ou le verrou matériel a échoué.",
                "remediation": "Contrôler le statut de lecture de la carte ; si elle est déjà verrouillée, aucune action requise."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Avertissement Solennel d'Irréversibilité",
                    "caption": "Fusible encore ouvert. L'opérateur doit saisir le code de verrouillage permanent.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Saisie du Code & Clic sur 'Verrouiller Définitivement'",
                    "triggerName": "Validation de la commande irréversible de claquage de fusible in-silico",
                    "caption": "Confirmation opérateur et injection de la commande APDU propriétaire `LOCK APPLICATION`.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Claquage Matériel & Test d'Inviolabilité Réflexe",
                    "progress": 98,
                    "caption": "Test immédiat d'écriture pirate pour confirmer le rejet avec code d'erreur `69 82`.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Carte Scellée à Perpétuité in-silico",
                    "status": "success",
                    "caption": "La puce est désormais infalsifiable et prête pour l'impression physique thermique.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-209",
        "title": "Impression Thermique & Laser Haute Précision Recto/Verso",
        "cat": "Impression Physique",
        "actor": "Opérateur d'Encodage",
        "platforms": ["PC/SC (Desktop Natif)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["Impression", "Thermique", "Fargo", "Laser", "Hologramme"],
        "preconditions": "Silicium gravé et scellé, imprimante Fargo HDP5000 en ligne.",
        "flow": [
            "Centrage optique haute précision de la carte dans le chargeur de l'imprimante thermique par sublimation Fargo HDP5000.",
            "Impression haute définition 600 DPI du recto (portrait mémoriel et dorures à chaud en résine or).",
            "Retournement automatique de la carte par le module flipper interne de l'imprimante.",
            "Impression du verso (épitaphe funéraire, micro-caractères de sécurité et repère optique de la puce).",
            "Application du vernis de protection anti-UV et de la couche holographique inviolable."
        ],
        "postconditions": "Carte physique terminée, surface résistante aux rayures et aux intempéries (norme ISO 7810).",
        "legal": "Norme ISO/IEC 7810 ID-1 (durabilité physique et résistance aux torsions des cartes d'identité).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "desktop",
            "deviceLabel": "PaxStation Station Pro • Contrôleur d'Impression Thermique 600 DPI",
            "formFields": [
                {"label": "Imprimante Professionnelle", "name": "printer_model", "type": "select", "value": "Fargo HDP5000 Haute Définition (600 DPI)", "placeholder": "Imprimante", "badge": "Prête", "required": True},
                {"label": "Ruban de Sécurité", "name": "ribbon_type", "type": "select", "value": "Quadrichromie YMCK + Ruban Dorure Or & Hologramme", "placeholder": "Ruban", "badge": "Or 24k", "required": True},
                {"label": "Vernis de Protection", "name": "lamination", "type": "text", "value": "Overlay Polycarbonate Anti-UV 1.0 mil", "placeholder": "Vernis", "badge": "Anti-UV", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_start_print", "label": "Lancer l'Impression Thermique Recto/Verso", "role": "primary", "state": "idle", "icon": "🖨️"},
                {"id": "btn_calibrate_head", "label": "Calibrer Centrage Micrométrique", "role": "secondary", "state": "idle", "icon": "🎯"}
            ],
            "validationMsg": {
                "title": "Impression Physique 600 DPI Terminée",
                "badge": "Conforme ISO/IEC 7810",
                "detail": "Dorure à chaud et vernis anti-UV appliqués. Éjection bac de sortie sans défaut."
            },
            "errorCase": {
                "code": "ERR_THERMAL_HEAD_OVERHEAT",
                "title": "Surchauffe de la Tête Thermique",
                "condition": "Température de la tête de sublimation dépassant le seuil de 85°C lors des séries d'encodage.",
                "message": "Erreur d'impression : Surchauffe thermique détectée sur la tête d'impression Fargo.",
                "remediation": "Mettre l'imprimante en pause de refroidissement 90 secondes avant de reprendre le cycle de pelliculage."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Imprimante Fargo HDP5000 Prête dans le Bac d'Alimentation",
                    "caption": "Carte positionnée dans le chargeur optique. Prête pour l'impression thermique.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Prise en Charge de la Carte & Chauffage Tête Thermique",
                    "triggerName": "Clic sur 'Lancer l'Impression Thermique Recto/Verso'",
                    "caption": "Centrage micrométrique optique et montée en température de la tête thermique.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Impression Sublimation 600 DPI & Pelliculage Anti-UV",
                    "progress": 75,
                    "caption": "Dépôt des pigments couleur, application de la dorure à chaud et retournement flipper.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Carte Physique Éjectée & Vernis Séché",
                    "status": "success",
                    "caption": "La carte imprimée repose dans le bac de sortie. Rendu or et mat conforme à l'épreuve.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-210",
        "title": "Diagnostic Silicium, Relecture des 6 EF & PV de Gravure Officiel",
        "cat": "Assurance Qualité & Conformité",
        "actor": "Opérateur d'Encodage & Conseiller Funéraire",
        "platforms": ["PC/SC (Desktop Natif)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["QA", "Diagnostic", "Relecture6EF", "FusibleAntiTamper", "PVRemise", "COSE_Sign1", "DEC-AET-10"],
        "preconditions": "Carte physique gravée et imprimée reposée sur le lecteur de contrôle qualité ACR1552U.",
        "flow": [
            "Relecture sans contact séquentielle des 6 Elementary Files (EF-0 à EF-5) via l'antenne NFC de recette à 106 kbps.",
            "Audit binaire de conformité de chaque compartiment : EF-0 (Manifeste), EF-1 (Identité), EF-2 (Portrait WebP 480×480 DEC-AET-12), EF-3 (Mémo Vocal Opus), EF-4 (Volontés Civiles), EF-5 (Signature).",
            "Vérification mathématique indépendante de la signature COSE_Sign1 apposée par l'enclave de la station (DEC-AET-10) avec contrôle anti-malléabilité du s bas (RFC 9052).",
            "Interrogation matérielle de l'état du fusible in-silico (commande APDU 80 DE 00 00 confirmant le verrouillage irréversible anti-tamper en lecture seule).",
            "Génération du Procès-Verbal (PV) de Remise Officiel infalsifiable avec QR code de contrôle d'intégrité et empreinte SHA-256 scellée.",
            "Insertion solennelle des deux cartes mémorielles dans leur coffret doublé de velours Le Pax Funèbre pour remise à la famille."
        ],
        "postconditions": "Diagnostic 100% conforme des 6 EF (EF-0 à EF-5), intégrité signature certifiée, fusible matériel in-silico verrouillé, PV de remise officiel édité et coffret prêt pour la famille.",
        "legal": "Code de droit économique belge (garantie de conformité des biens et services funéraires — référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "desktop",
            "deviceLabel": "PaxStation Station Pro • Banc de Diagnostic Silicium & Édition PV",
            "formFields": [
                {"label": "Relecture sans Contact des 6 EF", "name": "recheck_6ef", "type": "text", "value": "EF-0 à EF-5 relus (78 412 octets sur 86 528 utiles — 0 divergence)", "placeholder": "Audit 6 EF", "badge": "6 EF Intègres", "required": False},
                {"label": "Intégrité Signature COSE_Sign1", "name": "recheck_sig", "type": "text", "value": "VALIDE (Enclave Station DEC-AET-10 • ES256 / s bas normalisé RFC 9052)", "placeholder": "Signature", "badge": "Authentique", "required": False},
                {"label": "État Fusible Matériel in-silico", "name": "fuse_status", "type": "text", "value": "VERROUILLÉ DÉFINITIF (APDU 80 DE 01 00 — Lecture Seule Anti-Tamper)", "placeholder": "Fusible", "badge": "Anti-Tamper Scellé", "required": False},
                {"label": "Procès-Verbal de Remise Famille", "name": "pv_reference", "type": "text", "value": "PV-2026-NAM-0491 (Horodatage certifié & QR Code d'Intégrité)", "placeholder": "Numéro PV", "badge": "PDF Scellé", "required": False},
                {"label": "Destinataire Mandataire", "name": "recipient_family", "type": "text", "value": "Claire Dubois (Mandat familial n° 8841)", "placeholder": "Famille", "badge": "Mandataire", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_run_full_diag", "label": "Lancer le Diagnostic Intégral & Relecture 6 EF", "role": "primary", "state": "idle", "icon": "🔬"},
                {"id": "btn_print_pv", "label": "Générer le PV de Remise Officiel (PDF Scellé)", "role": "secondary", "state": "idle", "icon": "📄"},
                {"id": "btn_seal_box", "label": "Valider la Mise en Coffret Mémoriel", "role": "secondary", "state": "idle", "icon": "🎁"}
            ],
            "validationMsg": {
                "title": "Diagnostic Silicium Conforme & PV Officiel Validé",
                "badge": "6 EF Conformes • Fusible Scellé • PV Émis",
                "detail": "Audit sans contact des 6 EF (EF-0 à EF-5) 100% conforme. Signature enclave station vérifiée. Fusible matériel actif. Coffret prêt pour remise à la famille."
            },
            "errorCase": {
                "code": "ERR_DIAGNOSTIC_EF_INTEGRITY_FAIL",
                "title": "Divergence sur Relecture des 6 EF ou Fusible Ouvert",
                "condition": "Altération binaire sur l'un des EF (EF-0 à EF-5), fusible matériel non verrouillé ou signature COSE_Sign1 corrompue.",
                "message": "REJET QUALITÉ CRITIQUE : L'empreinte binaire relue sur la puce ne concorde pas avec la capsule d'origine ou le fusible est resté ouvert.",
                "remediation": "Mettre immédiatement la carte au rebut, détruire le support non conforme et consigner l'incident pour réencodage d'une nouvelle carte ACOSJ 92 Ko."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Carte Terminée Déposée sur le Banc de Diagnostic",
                    "caption": "Carte posée sur le lecteur sans contact. Le formulaire de diagnostic des 6 EF et génération du PV est en attente d'exécution.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Lancement du Diagnostic & Relecture sans Contact des 6 EF",
                    "triggerName": "Clic sur 'Lancer le Diagnostic Intégral & Relecture 6 EF'",
                    "caption": "Interrogation séquentielle sans fil des compartiments EF-0 à EF-5 à 106 kbps et contrôle cryptographique.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Audit Binaire des 6 EF & Contrôle Fusible in-silico",
                    "progress": 96,
                    "caption": "Validation des 6 EF (EF-0 à EF-5), vérification de la signature enclave station et confirmation du fusible verrouillé.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Procès-Verbal de Remise Émis & Coffret Mémoriel Scellé",
                    "status": "success",
                    "caption": "Diagnostic 100% conforme. Le PV officiel de remise est édité et le coffret velours est scellé pour la famille.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    }
]
