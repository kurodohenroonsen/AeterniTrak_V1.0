#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeterniTrak V1.0 — Définition Complète des Micro Use-Cases pour App 2 : PaxStation Encodage Silicium (UC-201 à UC-210)
Avec Simulateur de Wireframes Interactifs à 4 États, Spécifications des Formulaires, Actions, Validations et Erreurs Normatives.
"""

APP2_USECASES = [
    {
        "id": "UC-201",
        "title": "Connexion Station de Bureau ACR1552U WebUSB",
        "cat": "Matériel & Poste Pro",
        "actor": "Opérateur d'Encodage",
        "platforms": ["WebUSB (Chromium Desktop)", "PC/SC (Desktop Natif)"],
        "tags": ["ACR1552U", "WebUSB", "PCSC", "Pilote"],
        "preconditions": "Poste de travail d'agence avec lecteur ACR1552U branché sur port USB 3.0.",
        "flow": [
            "Ouverture de PaxStation Encodage sur Chrome / Edge ou client lourd de bureau.",
            "Détection du descripteur USB Vendor ID 0x072F (Advanced Card Systems) et Product ID 0x2200 (ACR1552U USB CCID Reader).",
            "Demande d'autorisation d'accès matériel WebUSB et initialisation du canal de commande.",
            "Passage du voyant LED du lecteur au vert fixe (état prêt) et affichage du moniteur de liaison 106 kbps."
        ],
        "postconditions": "Canal de communication USB ouvert à 12 Mbps, prêt pour la détection de puces sans contact.",
        "legal": "Spécification USB CCID (Integrated Circuit(s) Cards Interface Device, USB-IF).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "desktop",
            "deviceLabel": "PaxStation Station Pro • ACR1552U USB CCID Monitor",
            "formFields": [
                {"label": "Pilote Matériel", "name": "usb_driver", "type": "select", "value": "WebUSB Chromium Direct (USB CCID v1.1)", "placeholder": "Pilote", "badge": "WebUSB", "required": True},
                {"label": "Périphérique Détecté", "name": "device_name", "type": "text", "value": "ACS ACR1552U USB Contactless Reader (VID:072F / PID:2200)", "placeholder": "Lecteur", "badge": "USB 3.0", "required": False},
                {"label": "Baudrate RF Contactless", "name": "baudrate", "type": "text", "value": "106 kbps ISO/IEC 14443 Type A", "placeholder": "Baudrate", "badge": "106k", "required": False},
                {"label": "Firmware Lecteur", "name": "firmware_version", "type": "text", "value": "v2.04 SAM Secure Ready", "placeholder": "Firmware", "badge": "À Jour", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_connect_acr", "label": "Autoriser l'Accès WebUSB AeterniTrak", "role": "primary", "state": "idle", "icon": "🔌"},
                {"id": "btn_ping_rf", "label": "Tester Boucle RF & Bip Sonore", "role": "secondary", "state": "idle", "icon": "📡"}
            ],
            "validationMsg": {
                "title": "Lecteur ACR1552U Connecté",
                "badge": "Canal USB CCID 12 Mbps Ouvert",
                "detail": "Lecteur opérationnel. Champ électromagnétique RF 13.56 MHz actif en veille."
            },
            "errorCase": {
                "code": "ERR_ACR1552U_DEVICE_DETACHED",
                "title": "Périphérique ACR1552U Non Détecté",
                "condition": "Câble USB déconnecté, hub USB sous-alimenté ou absence de permission WebUSB du navigateur.",
                "message": "Erreur matérielle : Impossible d'établir la liaison avec le lecteur de bureau ACR1552U.",
                "remediation": "Vérifier le branchement USB, autoriser l'accès périphérique dans la barre d'adresse et recharger la session."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Station en Attente de Connexion USB",
                    "caption": "Lecteur non appairé. L'interface affiche l'invite de connexion WebUSB.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Autorisation WebUSB Accordée par l'Opérateur",
                    "triggerName": "Clic sur 'Autoriser l'accès WebUSB' et sélection du périphérique 0x072F",
                    "caption": "Dialogue natif Chromium de sélection du périphérique USB avec confirmation opérateur.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Initialisation du Firmware & Test Boucle RF 13.56 MHz",
                    "progress": 80,
                    "caption": "Envoi de la commande de contrôle firmware et activation de l'antenne sans contact.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Station Prête pour l'Insertion de Silicium",
                    "status": "success",
                    "caption": "Lecteur prêt en écoute active. La station attend la pose de la JavaCard ACOSJ.",
                    "screenHtml": """
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
                    "caption": "Puce prête pour l'allocation des fichiers élémentaires EF01, EF02 et EF03.",
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
            "Création des trois Elementary Files (EF) prescrits par STORAGE-001 :",
            "- `EF01 (ID)` : 2 048 octets réservés pour métadonnées et identifiant unique de carte.",
            "- `EF02 (Profile)` : 16 384 octets réservés pour le profil CBOR complet (volontés, directives, textes).",
            "- `EF03 (Media)` : 73 728 octets réservés pour les portraits WebP et l'audio vocal.",
            "Vérification de l'absence de fragmentation mémoire."
        ],
        "postconditions": "Système de fichiers silicium initialisé selon la cartographie stricte du jalon STORAGE-001.",
        "legal": "Spécification technique AeterniTrak STORAGE-001 (allocation EEPROM JavaCard).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "desktop",
            "deviceLabel": "PaxStation Station Pro • Partitionneur EEPROM Silicium (STORAGE-001)",
            "formFields": [
                {"label": "Partition EF01 (Meta ID)", "name": "ef01_size", "type": "number", "value": "2048", "placeholder": "Taille", "badge": "2 Ko", "required": True},
                {"label": "Partition EF02 (Profile CBOR)", "name": "ef02_size", "type": "number", "value": "16384", "placeholder": "Taille", "badge": "16 Ko", "required": True},
                {"label": "Partition EF03 (Medias WebP/Opus)", "name": "ef03_size", "type": "number", "value": "73728", "placeholder": "Taille", "badge": "72 Ko", "required": True},
                {"label": "Total Alloué", "name": "total_allocated", "type": "text", "value": "92 160 octets (100% sans fragmentation)", "placeholder": "Total", "badge": "Optimum", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_format_eeprom", "label": "Initialiser la Structure EF Silicium (STORAGE-001)", "role": "primary", "state": "idle", "icon": "🗄️"},
                {"id": "btn_check_ef", "label": "Vérifier Table d'Allocation EF", "role": "secondary", "state": "idle", "icon": "🔍"}
            ],
            "validationMsg": {
                "title": "Système de Fichiers Silicium Initialisé",
                "badge": "Jalon STORAGE-001 Validé",
                "detail": "EF01 (2 Ko), EF02 (16 Ko), EF03 (72 Ko) alloués avec succès. Zéro fragment."
            },
            "errorCase": {
                "code": "ERR_EEPROM_QUOTA_EXCEEDED",
                "title": "Dépassement de la Capacité EEPROM",
                "condition": "Tentative d'allocation d'une partition dont la taille dépasse les 92 Ko de la puce physique.",
                "message": "Erreur d'allocation : La somme des partitions demandées dépasse la taille maximale de l'EEPROM ACOSJ.",
                "remediation": "Restaurer les tailles standard prescrites par STORAGE-001 (2 Ko, 16 Ko, 72 Ko)."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "EEPROM Vierge Non Partitionnée",
                    "caption": "Carte connectée. La table de fichiers élémentaires n'est pas encore créée.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Clic sur 'Initialiser la Structure EF Silicium'",
                    "triggerName": "Émission des commandes APDU de création des fichiers EF01, EF02 et EF03",
                    "caption": "Ordre d'écriture physique de la structure de répertoires in-silico.",
                    "screenHtml": """
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
                        <code>> [APDU-TX] 00 E0 00 00 07 62 05 01 08 00 (CREATE EF01 : 2048 o) -> 90 00</code><br>
                        <code>> [APDU-TX] 00 E0 00 00 07 62 05 02 40 00 (CREATE EF02 : 16384 o) -> 90 00</code><br>
                        <code>> [APDU-TX] 00 E0 00 00 07 62 05 03 20 00 (CREATE EF03 : 73728 o) -> 90 00</code>
                      </div>
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Structure EF01, EF02, EF03 Initialisée avec Succès",
                    "status": "success",
                    "caption": "Système de fichiers prêt pour recevoir les flux de données compressés.",
                    "screenHtml": """
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
                        <code>> [APDU-SEG] Découpage en 306 tranches de 255 octets (Payload EF02 + EF03)</code>
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
                          <p class="wf-subtext">306 blocs APDU prêts à être injectés sur les partitions EF02 et EF03</p>
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
            "Sélection successive du fichier `EF02` puis `EF03` via `SELECT FILE`.",
            "Envoi cadencé des commandes APDU `UPDATE BINARY` (commande `00 D6 P1 P2 Lc [Octets]`).",
            "Contrôle systématique du mot de statut `90 00` en réponse à chaque bloc.",
            "Gestion des reprises sur incident : si un bloc échoue, rejeu automatique (max 3 tentatives).",
            "Mise à jour en temps réel de la barre de progression pour l'opérateur."
        ],
        "postconditions": "78 412 octets gravés avec succès dans l'EEPROM de la JavaCard ACOSJ.",
        "legal": "Spécification technique ISO/IEC 7816-4 §7.2 (commandes d'écriture binaire).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "desktop",
            "deviceLabel": "PaxStation Station Pro • Graveur Silicium APDU IsoDep",
            "formFields": [
                {"label": "Nombre de Blocs", "name": "block_count", "type": "text", "value": "306 blocs de 255 octets", "placeholder": "Blocs", "badge": "306 Blocs", "required": False},
                {"label": "Vitesse de Transfert", "name": "transfer_rate", "type": "text", "value": "14.2 Ko/sec (106 kbps IsoDep)", "placeholder": "Débit", "badge": "106k", "required": False},
                {"label": "Taux d'Erreur APDU", "name": "error_rate", "type": "text", "value": "0 erreur (306/306 acquittements 90 00)", "placeholder": "Erreurs", "badge": "0 Défaut", "required": False},
                {"label": "Temps Écoulé", "name": "elapsed_time", "type": "text", "value": "05.8 secondes", "placeholder": "Temps", "badge": "Chrono", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_start_burning", "label": "Lancer la Gravure Silicium", "role": "primary", "state": "idle", "icon": "🔥"},
                {"id": "btn_pause_burning", "label": "Mettre en Pause", "role": "secondary", "state": "idle", "icon": "⏸"}
            ],
            "validationMsg": {
                "title": "Gravure Silicium Achevée avec Succès",
                "badge": "306/306 Blocs Écrits (90 00)",
                "detail": "78 412 octets injectés dans les partitions EF02 et EF03 sans aucune erreur."
            },
            "errorCase": {
                "code": "ERR_APDU_WRITE_FAILURE",
                "title": "Échec de Transmission d'un Bloc APDU",
                "condition": "Micro-déplacement de la carte sur l'antenne provoquant un code statut `6A 84` ou perte de liaison.",
                "message": "Erreur d'écriture : Rupture de liaison RF lors de l'injection du bloc n° 142/306.",
                "remediation": "Laisser la carte immobile au contact de l'antenne et relancer la procédure d'écriture automatique."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Graveur en Attente de Démarrage",
                    "caption": "Les 306 blocs sont prêts. La jauge d'écriture est à 0%.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Lancement de la Rafale de Commandes APDU",
                    "triggerName": "Clic sur 'Lancer la Gravure Silicium' et sélection du fichier EF02",
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
                    "phaseTitle": "Injection en Cours : Bloc 198 / 306 (65%)",
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
                        <code>> [APDU-TX] 00 D6 02 C4 FF [255 octets Opus]   -> < 90 00 (Bloc 198/306)</code>
                      </div>
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Gravure Silicium Accomplie à 100%",
                    "status": "success",
                    "caption": "Totalité des 78 412 octets gravés avec intégrité absolue.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-206",
        "title": "Scellement Cryptographique COSE_Sign1 PaxFunèbre (Secure Element)",
        "cat": "Cryptographie & Signature",
        "actor": "Opérateur d'Encodage",
        "platforms": ["WebUSB (Chromium Desktop)", "PC/SC (Desktop Natif)"],
        "tags": ["COSE_Sign1", "Ed25519", "ES256", "SecureElement", "RFC9052"],
        "preconditions": "Données gravées sur la puce mais non encore signées.",
        "flow": [
            "Appel au module matériel sécurisé (Secure Element / HSM d'agence PaxFunèbre).",
            "Construction de la structure canonique `Sig_structure` COSE_Sign1 (Tag 18) selon la RFC 9052 :",
            "- Contexte : `\"Signature1\"`",
            "- En-tête protégé : `{1: -8, 16: \"application/aeternitrak-profile+cbor\"}` (Ed25519) ou `{1: -7}` (ES256)",
            "- Données associées externes : `h''` (vide)",
            "- Charge utile : le condensat SHA-256 de la capsule",
            "Génération de la signature cryptographique par la clé d'autorité officielle.",
            "Écriture de l'enveloppe signée COSE_Sign1 dans le fichier dédié `EF.SIGN` de la carte."
        ],
        "postconditions": "Carte physique scellée avec signature COSE_Sign1 officielle infalsifiable.",
        "legal": "Spécification technique IETF RFC 9052 (COSE Structures and Process) et RFC 9596 (COSE typ Header).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "desktop",
            "deviceLabel": "PaxStation Station Pro • Module de Signature Matérielle COSE_Sign1",
            "formFields": [
                {"label": "Module HSM / Secure Element", "name": "hsm_module", "type": "text", "value": "PaxFunèbre Hardware Token v2.1", "placeholder": "HSM", "badge": "FIPS 140-3", "required": False},
                {"label": "Algorithme Utilisé", "name": "sig_alg", "type": "select", "value": "Ed25519 (EdDSA, alg: -8, RFC 8032)", "placeholder": "Algorithme", "badge": "Recommandé", "required": True},
                {"label": "Type MIME Protégé (typ)", "name": "mime_typ", "type": "text", "value": "application/aeternitrak-profile+cbor (RFC 9596)", "placeholder": "Type", "badge": "Protégé", "required": False},
                {"label": "Empreinte Clé Publique (kid)", "name": "key_kid", "type": "text", "value": "3c81e592...71aa (16 octets SHA-256)", "placeholder": "kid", "badge": "16 Octets", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_sign_cose", "label": "Générer le Sceau Matériel COSE_Sign1", "role": "primary", "state": "idle", "icon": "🔐"},
                {"id": "btn_inspect_sig_struct", "label": "Inspecter Sig_structure", "role": "secondary", "state": "idle", "icon": "🔍"}
            ],
            "validationMsg": {
                "title": "Sceau Cryptographique COSE_Sign1 Apposé",
                "badge": "Tag 18 • Ed25519 Certifié",
                "detail": "Enveloppe signée gravée sur EF.SIGN. Intégrité infalsifiable garantie sans contact."
            },
            "errorCase": {
                "code": "ERR_COSE_EXPIRED_KEY",
                "title": "Clé de Scellement Opérateur Expirée",
                "condition": "Tentative de signature avec un token HSM dont le certificat d'autorité est expiré.",
                "message": "Erreur de sécurité : La clé matérielle de scellement a dépassé sa date limite de validité.",
                "remediation": "Insérer le token HSM de secours ou procéder au renouvellement de clé auprès de l'autorité centrale AeterniTrak."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Données Gravées Non Signées",
                    "caption": "Puce écrite. La partition EF.SIGN est vide, le sceau officiel n'est pas encore apposé.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Appel au Secure Element & Construction de la Sig_structure",
                    "triggerName": "Clic sur 'Générer le Sceau Matériel COSE_Sign1'",
                    "caption": "Assemblage des en-têtes protégés déterministes et envoi du hash au coprocesseur de signature.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Signature Déterministe RFC 8032 & Injection sur EF.SIGN",
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
                        <code>> [ED25519] Signature émise (64 octets fixes R||S) : 5a2c91f0...77b1</code><br>
                        <code>> [APDU-SIGN] Écriture sur EF.SIGN (APDU UPDATE BINARY) : < 90 00</code>
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
                          <strong>Signature Cryptographique PaxFunèbre Apposée</strong>
                          <p class="wf-subtext">Ed25519 • kid: 3c81e592...71aa • Inaltérable sans contact</p>
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
        "title": "Contrôle de Recette Post-Gravure & PV de Remise Officiel",
        "cat": "Assurance Qualité & Conformité",
        "actor": "Opérateur d'Encodage & Conseiller",
        "platforms": ["PC/SC (Desktop Natif)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["QA", "Recette", "PVRemise", "Conformite", "Coffret"],
        "preconditions": "Carte physique imprimée et gravée reposée sur le lecteur de contrôle.",
        "flow": [
            "Relecture intégrale sans fil des 78 412 octets gravés via l'antenne NFC de recette.",
            "Vérification mathématique indépendante de la signature COSE_Sign1 par la clé publique officielle.",
            "Confrontation de l'empreinte de relecture avec l'empreinte d'origine du Bon à Tirer (zéro différence admise).",
            "Génération du Procès-Verbal (PV) de Remise Officiel infalsifiable avec QR code de contrôle.",
            "Insertion solennelle des deux cartes dans leur coffret mémoriel doublé de velours Le Pax Funèbre."
        ],
        "postconditions": "PV de remise officiel édité et signé, coffret scellé prêt pour la remise solennelle à la famille.",
        "legal": "Code de droit économique belge (garantie de conformité des biens et services funéraires).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "desktop",
            "deviceLabel": "PaxStation Station Pro • Banc de Recette Qualité & Édition PV",
            "formFields": [
                {"label": "Relecture Silicium Intégrale", "name": "recheck_bytes", "type": "text", "value": "78 412 octets relus à 106 kbps (0 divergence)", "placeholder": "Relecture", "badge": "100% Intègre", "required": False},
                {"label": "Signature COSE_Sign1", "name": "recheck_sig", "type": "text", "value": "VALIDE (Clé publique Ed25519 officielle vérifiée)", "placeholder": "Signature", "badge": "Authentique", "required": False},
                {"label": "Numéro de Série Lot", "name": "lot_serial", "type": "text", "value": "AET-2026-LOT-NAM-0491", "placeholder": "Numéro", "badge": "Traçable", "required": False},
                {"label": "Destinataire Officiel", "name": "recipient_family", "type": "text", "value": "Claire Dubois (Mandat n° 8841)", "placeholder": "Famille", "badge": "Mandataire", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_run_qa", "label": "Lancer le Contrôle de Recette Automatisé", "role": "primary", "state": "idle", "icon": "🔬"},
                {"id": "btn_print_pv", "label": "Éditer le PV de Remise Officiel (PDF Chiffré)", "role": "secondary", "state": "idle", "icon": "📄"}
            ],
            "validationMsg": {
                "title": "Contrôle de Recette Qualité 100% Conforme",
                "badge": "PV Officiel Validé",
                "detail": "Zéro anomalie détectée. Coffret mémoriel scellé prêt pour remise solennelle à la famille."
            },
            "errorCase": {
                "code": "ERR_QA_HASH_MISMATCH",
                "title": "Non-Concordance d'Empreinte de Recette",
                "condition": "Altération d'un octet lors de la relecture ou divergence avec le BAT d'origine.",
                "message": "REJET QUALITÉ CRITIQUE : L'empreinte SHA-256 relue sur la puce ne correspond pas au Bon à Tirer signé.",
                "remediation": "Mettre la carte immédiatement au rebut, procéder à l'analyse de défaillance matérielle et réencoder une nouvelle carte."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Carte Terminée Déposée sur le Banc de Recette",
                    "caption": "Carte posée sur le lecteur de contrôle qualité. L'audit automatisé est en attente.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Lancement de l'Audit Qualité Automatisé",
                    "triggerName": "Clic sur 'Lancer le Contrôle de Recette Automatisé'",
                    "caption": "Relecture complète des blocs APDU et vérification cryptographique hors-ligne.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Vérification Mathématique COSE_Sign1 & Hachage JCS",
                    "progress": 95,
                    "caption": "Confirmation de la validité de la signature Ed25519 et de la fidélité au BAT.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "PV de Remise Officiel Émis & Coffret Scellé",
                    "status": "success",
                    "caption": "Processus d'encodage terminé avec succès. Les 2 cartes sont prêtes pour la famille.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    }
]
