#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeterniTrak V1.0 — Définition Complète des Micro Use-Cases pour App 3 : Sanctuaire Mémoriel Mobile (UC-301 à UC-325)
Avec Simulateur de Wireframes Interactifs à 4 États, Spécifications des Formulaires, Actions, Validations et Erreurs Normatives.
"""

APP3_USECASES = [
    {
        "id": "UC-301",
        "title": "Scan NFC Instantané Direct Sans Login (NFC Tap Android/iOS)",
        "cat": "Accès & Identité",
        "actor": "Famille, Proches & Cérémonie",
        "platforms": ["Natif (iOS & Android)", "Web NFC (Chrome Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["NFC", "ZeroLogin", "IsoDep", "CoreNFC", "WebNFC"],
        "preconditions": "Application mobile Sanctuaire ouverte ou scan via Web NFC sur Chrome Android.",
        "flow": [
            "L'utilisateur approche la Carte Sanctuaire ou le Médaillon du dos de son smartphone.",
            "Détection du champ NFC en moins de 50 millisecondes (protocole IsoDep natif).",
            "Lecture directe et intégrale des données mémorielles chiffrées sans AUCUNE invite de connexion, sans création de compte et sans mot de passe (zéro friction pour les personnes âgées).",
            "Émission d'un retour haptique doux confirmant la bonne lecture du silicium."
        ],
        "postconditions": "Données de la carte chargées en mémoire vive locale, session de recueillement ouverte.",
        "legal": "Règlement général sur la protection des données (RGPD art. 5 - minimisation et souveraineté absolue des données).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "mobile",
            "deviceLabel": "Sanctuaire Mobile • iPhone 15 Pro (CoreNFC & Web NFC)",
            "formFields": [
                {"label": "Mode d'Authentification", "name": "auth_mode", "type": "text", "value": "ZÉRO LOGIN (Local-First Universel)", "placeholder": "Auth", "badge": "Zéro Friction", "required": False},
                {"label": "Protocole Sans Contact", "name": "nfc_proto", "type": "text", "value": "NFC IsoDep / ISO 14443-4 T=CL", "placeholder": "Protocole", "badge": "IsoDep", "required": False},
                {"label": "Temps de Détection", "name": "scan_latency", "type": "text", "value": "38 millisecondes", "placeholder": "Latence", "badge": "Instantané", "required": False},
                {"label": "Données Rapatriées", "name": "loaded_bytes", "type": "text", "value": "78 412 octets in-silico (Portraits + Audio + Volontés)", "placeholder": "Volume", "badge": "Mémoire Vive", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_tap_nfc", "label": "Approcher la Carte du Haut du Smartphone", "role": "primary", "state": "idle", "icon": "📱"},
                {"id": "btn_nfc_help", "label": "Aide Emplacement Antenne NFC", "role": "secondary", "state": "idle", "icon": "❓"}
            ],
            "validationMsg": {
                "title": "Carte Sanctuaire Reconnue Instantanément",
                "badge": "Lecture Silicium 38 ms",
                "detail": "Accès direct sans mot de passe. Données de la défunte Claire Dubois chargées."
            },
            "errorCase": {
                "code": "ERR_NFC_READ_TIMEOUT",
                "title": "Rupture de Champ NFC Avant Fin de Lecture",
                "condition": "Retrait précipité de la carte avant le transfert complet des 78 Ko.",
                "message": "Erreur de transmission : La carte a été retirée trop rapidement de l'antenne smartphone.",
                "remediation": "Maintenir la carte immobile contre le dos de l'appareil pendant 1 seconde complète."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Écran d'Accueil Épuré en Attente de Scan",
                    "caption": "Smartphone en veille passive. Invite solennelle d'approche de la carte visible.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Tap NFC Physique & Vibration Haptique",
                    "triggerName": "Apposition de la carte contre le module NFC supérieur du smartphone",
                    "caption": "Couplage inductif immédiat avec retour haptique doux et animation d'ondes concentriques.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Décompression Locale CBOR & Extraction des Médias",
                    "progress": 80,
                    "caption": "Décodage en local des portraits WebP et du fichier vocal Opus sans aucun appel serveur.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Sanctuaire Déverrouillé Immédiatement",
                    "status": "success",
                    "caption": "Portrait mémoriel affiché, musique prête. Expérience de recueillement ouverte sans friction.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-302",
        "title": "Vérification Cryptographique Hybride Ed25519 / ES256 (DEC-AET-04)",
        "cat": "Sécurité & Cryptographie",
        "actor": "Système Mobile & Sécurité",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["Crypto", "Ed25519", "ES256", "TrustList", "DEC-AET-04"],
        "preconditions": "Enveloppe COSE_Sign1 lue depuis la partition `EF.SIGN` de la carte.",
        "flow": [
            "Extraction du `kid` (Key ID) de 16 octets et de l'identifiant d'algorithme dans l'en-tête protégé.",
            "Recherche de la clé publique correspondante dans la liste de confiance locale embarquée (Trust Store décentralisé).",
            "Vérification de la validité temporelle de la clé de signature.",
            "Reconstruction de la `Sig_structure` canonique et exécution de l'algorithme de vérification :",
            "- Si Ed25519 (`alg: -8`) : vérification RFC 8032 ($8SB = 8R + 8kA$).",
            "- Si ES256 (`alg: -7`) : vérification RFC 6979 / SEC 1 avec contrôle strict de non-malléabilité du s bas.",
            "Affichage du badge solennel de certification officielle Le Pax Funèbre."
        ],
        "postconditions": "Authenticité et intégrité de la carte certifiées à 100% de manière déterministe.",
        "legal": "Règlement eIDAS (UE 910/2014 - exigences pour les signatures électroniques avancées).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "mobile",
            "deviceLabel": "Sanctuaire Mobile • Vérificateur Cryptographique Décentralisé",
            "formFields": [
                {"label": "Algorithme Utilisé", "name": "detected_alg", "type": "text", "value": "Ed25519 (EdDSA, alg: -8, RFC 8032)", "placeholder": "Algorithme", "badge": "Homologué", "required": False},
                {"label": "Identifiant Clé (kid)", "name": "key_kid", "type": "text", "value": "3c81e592...71aa (Magasin de Confiance Local)", "placeholder": "kid", "badge": "De Confiance", "required": False},
                {"label": "Validité Clé de Signature", "name": "key_validity", "type": "text", "value": "Certificat Valide (Émis par Le Pax Funèbre)", "placeholder": "Validité", "badge": "Active", "required": False},
                {"label": "Résultat Vérification", "name": "sig_result", "type": "text", "value": "SIGNATURE AUTHENTIQUE (0 divergence binaire)", "placeholder": "Résultat", "badge": "Certifié", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_verify_crypto", "label": "Vérifier la Signature Cryptographique", "role": "primary", "state": "idle", "icon": "🔐"},
                {"id": "btn_inspect_cert", "label": "Inspecter l'Autorité de Scellement", "role": "secondary", "state": "idle", "icon": "📜"}
            ],
            "validationMsg": {
                "title": "Signature COSE_Sign1 100% Authentique",
                "badge": "Certifié Le Pax Funèbre",
                "detail": "Signature Ed25519 vérifiée avec succès. Données inaltérées depuis la gravure en agence."
            },
            "errorCase": {
                "code": "ERR_COSE_INVALID_SIGNATURE",
                "title": "Signature Cryptographique Non Concordante",
                "condition": "Altération même d'un seul bit de la charge utile ou signature générée par une clé pirate.",
                "message": "REJET CRYPTOGRAPHIQUE SÉVÈRE : La signature ne concorde pas avec les données de la carte.",
                "remediation": "Carte compromise ou contrefaite. Refuser l'accès et signaler l'anomalie au réseau Le Pax Funèbre."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Enveloppe Signée en Attente de Contrôle",
                    "caption": "Signature brute lue. L'oracle cryptographique local n'a pas encore validé les scalaires.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Extraction de la Clé Publique & Calcul de Sig_structure",
                    "triggerName": "Clic sur 'Vérifier la Signature' et consultation du magasin local",
                    "caption": "Recherche instantanée de la clé publique de l'agence Namur dans la liste de confiance embarquée.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Résolution de l'Équation 8SB = 8R + 8kA (Ed25519)",
                    "progress": 95,
                    "caption": "Exécution de l'algorithme mathématique sans aucune dépendance serveur ni connexion Internet.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Sceau Doré d'Authenticité PaxFunèbre Déposé",
                    "status": "success",
                    "caption": "Carte déclarée authentique. Le Sanctuaire passe en mode nominal certifié.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-303",
        "title": "Affichage Sanctuaire, Recueillement & Livre d'Or Familial",
        "cat": "Expérience Sanctuaire",
        "actor": "Famille & Proches",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["Sanctuaire", "Recueillement", "Veilleuse", "LivreDOr", "Ducking14dB", "WebAudio", "Offline"],
        "preconditions": "Carte Sanctuaire authentifiée par la vérification cryptographique (DEC-AET-04 / DEC-AET-10).",
        "flow": [
            "Ouverture solennelle de l'espace de recueillement avec portrait haute définition 480×480 (DEC-AET-12) et halo doré doux.",
            "Formulaire interactif de recueillement : allumage d'une veilleuse mémorielle avec flamme vacillante persistante.",
            "Sélection de l'ambiance musicale d'adieu (In Paradisum de Fauré, Pavane de Ravel, Silence Méditatif) en boucle harmonique.",
            "Lecture du mémo vocal gravé in-silico avec ducking automatique calibré à -14 dB (baisse progressive de l'ambiance musicale au profit de la voix).",
            "Saisie et recueil des pensées de la famille dans le Livre d'Or, chiffrées et stockées localement en mémoire sécurisée hors-ligne (zéro dépendance au cloud)."
        ],
        "postconditions": "Veilleuse mémorielle allumée, ambiance musicale active avec ducking vocal fluide (-14 dB), pensées de la famille scellées localement hors-ligne.",
        "legal": "Respect de la dignité des défunts et de la vie privée mémorielle (protection des données locales sans transfert distant).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "mobile",
            "deviceLabel": "Sanctuaire Mobile • Espace de Recueillement & Livre d'Or Familial",
            "formFields": [
                {"label": "Défunt Honoré", "name": "deceased_name", "type": "text", "value": "Henri Dubois (1944 — 2026)", "placeholder": "Nom du défunt", "badge": "Certifié", "required": False},
                {"label": "Veilleuse Mémorielle", "name": "candle_state", "type": "select", "value": "Flamme Dorée Active (Allumage Perpétuel)", "placeholder": "Veilleuse", "badge": "Flamme Active", "required": True},
                {"label": "Ambiance Musicale d'Adieu", "name": "music_selection", "type": "select", "value": "In Paradisum (G. Fauré) — Boucle Harmonique 432 Hz", "placeholder": "Choix musical", "badge": "Audio Actif", "required": True},
                {"label": "Mémo Vocal Silicium & Ducking", "name": "voice_playback", "type": "text", "value": "Témoignage Audio Opus SILK (Ducking Automatique -14 dB)", "placeholder": "Voix", "badge": "-14 dB Calibré", "required": False},
                {"label": "Livre d'Or Familial (Pensée)", "name": "guestbook_message", "type": "textarea", "value": "« Ton souvenir reste une présence vivante dans la paix des bois et nos cœurs réunis. »", "placeholder": "Rédiger une pensée ou un hommage...", "badge": "Stockage Hors-Ligne", "required": True},
                {"label": "Auteur du Témoignage", "name": "guestbook_author", "type": "text", "value": "Claire & Antoine Dubois (Enfants)", "placeholder": "Votre nom", "badge": "Famille", "required": True}
            ],
            "actionButtons": [
                {"id": "btn_light_candle", "label": "Allumer la Veilleuse Mémorielle", "role": "primary", "state": "idle", "icon": "🕯️"},
                {"id": "btn_listen_voice", "label": "Écouter le Mémo Vocal (Ducking -14 dB)", "role": "secondary", "state": "idle", "icon": "🎙️"},
                {"id": "btn_sign_guestbook", "label": "Déposer une Pensée dans le Livre d'Or", "role": "secondary", "state": "idle", "icon": "✍️"}
            ],
            "validationMsg": {
                "title": "Espace de Recueillement Éclairé & Pensée Scellée",
                "badge": "Veilleuse Active • Ducking -14 dB • Livre d'Or Hors-Ligne",
                "detail": "Veilleuse mémorielle allumée. Ambiance musicale avec ducking vocal fluide. Hommage familial enregistré dans le coffre chiffré hors-ligne."
            },
            "errorCase": {
                "code": "ERR_GUESTBOOK_LOCAL_STORAGE_FULL",
                "title": "Mémoire Locale Sécurisée Saturée",
                "condition": "Espace de stockage local chiffré du terminal épuisé lors de l'enregistrement d'une pensée.",
                "message": "Erreur de sauvegarde locale : Impossible d'ajouter le message au livre d'or hors-ligne faute d'espace disque suffisant.",
                "remediation": "Libérer de l'espace sur l'appareil mobile ou exporter les messages précédents au format archive chiffrée."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Sanctuaire Mémoriel & Formulaire de Recueillement",
                    "caption": "Espace de recueillement avec veilleuse éteinte, sélecteur musical et formulaire du livre d'or familial prêt à recevoir la pensée.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Tap Allumage Veilleuse & Dépôt dans le Livre d'Or",
                    "triggerName": "Tap sur 'Allumer la Veilleuse' et soumission de la pensée familiale",
                    "caption": "Allumage immédiat de la flamme dorée et capture locale de la pensée de la famille.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Scintillement de la Flamme, Ducking Sonore -14 dB & Scellement Local",
                    "progress": 92,
                    "caption": "WebAudio applique le ducking à -14 dB sur la musique lors de la lecture vocale. Chiffrement local de la pensée.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Veilleuse Éclairée, Voix en Écoute & Livre d'Or Consigné",
                    "status": "success",
                    "caption": "Sanctuaire solennel complet. La veilleuse brille, la voix résonne avec ducking, le livre d'or est scellé.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-304",
        "title": "Bandeau de Réserve DEC-AET-07 Option B pour Émetteur Inconnu",
        "cat": "Résilience Mémorielle",
        "actor": "Famille & Régulateur",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["DEC-AET-07", "ReserveBanner", "EmetteurInconnu", "Resilience"],
        "preconditions": "Carte scellée par une autorité tierce ou émetteur absent du Trust Store local.",
        "flow": [
            "Le vérificateur cryptographique constate que la signature est mathématiquement valide mais que le `kid` ne figure pas dans la liste des autorités Le Pax Funèbre.",
            "Application stricte de l'arbitrage souverain de Kudoro (Décision DEC-AET-07 Option B) :",
            "- Zéro blocage aveugle : le sanctuaire mémoriel reste accessible à la famille pour préserver le souvenir.",
            "- Affichage obligatoire d'un bandeau ambré solennel d'avertissement en haut d'écran : « Attention : Émetteur non référencé au réseau officiel. Données non garanties par Le Pax Funèbre ».",
            "Possibilité pour l'utilisateur de consulter l'empreinte publique de l'autorité émettrice."
        ],
        "postconditions": "Sanctuaire affiché avec bandeau de réserve ambré explicite, conformité DEC-AET-07 respectée.",
        "legal": "Décision Kudoro DEC-AET-07 (Option B : Lisibilité mémorielle maintenue avec réserve réglementaire).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "mobile",
            "deviceLabel": "Sanctuaire Mobile • Bandeau de Réserve Ambré DEC-AET-07",
            "formFields": [
                {"label": "Statut de Signature", "name": "sig_math_status", "type": "text", "value": "Mathématiquement Valide (Ed25519 OK)", "placeholder": "Signature", "badge": "Valide", "required": False},
                {"label": "Statut Émetteur", "name": "issuer_status", "type": "text", "value": "ÉMETTEUR INCONNU du Magasin Local", "placeholder": "Émetteur", "badge": "Avertissement", "required": False},
                {"label": "Décision Appliquée", "name": "decision_code", "type": "text", "value": "DEC-AET-07 Option B (Bandeau de Réserve Ambré)", "placeholder": "Décision", "badge": "Souverain", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_dismiss_banner", "label": "Poursuivre le Recueillement avec Avertissement", "role": "primary", "state": "idle", "icon": "⚠️"},
                {"id": "btn_audit_unknown_key", "label": "Examiner la Clé Inconnue (kid)", "role": "secondary", "state": "idle", "icon": "🔍"}
            ],
            "validationMsg": {
                "title": "Bandeau de Réserve DEC-AET-07 Option B Affiché",
                "badge": "Avertissement Réglementaire",
                "detail": "Accès maintenu pour la famille mais non labellisé par Le Pax Funèbre."
            },
            "errorCase": {
                "code": "WARN_UNKNOWN_ISSUER_BANNER",
                "title": "Autorité de Scellement Non Certifiée",
                "condition": "Scan d'une carte valide issue d'un opérateur étranger non fédéré au réseau.",
                "message": "Avertissement : La signature de cette carte n'émane pas d'une agence agréée Le Pax Funèbre.",
                "remediation": "Contacter l'émetteur d'origine pour vérifier son affiliation ou mettre à jour la liste locale de confiance."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Détection d'une Clé Hors Liste de Confiance",
                    "caption": "Signature valide mais kid non répertorié. L'arbitrage DEC-AET-07 va s'appliquer.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Injection du Bandeau Ambré Réglementaire",
                    "triggerName": "Application de la règle Option B avec bandeau ambré en tête",
                    "caption": "Création du bandeau solennel en haut d'écran sans bloquer l'accès aux photos et volontés.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Déchiffrement Maintenu & Marquage de Réserve",
                    "progress": 85,
                    "caption": "Les volontés et photos restent lisibles pour la famille conformément au respect des proches.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Sanctuaire Affiché avec Bandeau Ambré Visible",
                    "status": "warning",
                    "caption": "Équilibre parfait entre intégrité réglementaire et respect du recueillement familial.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-305",
        "title": "Blocage Hermétique sur Carte Falsifiée ou Clé Révoquée",
        "cat": "Sécurité & Anti-Fraude",
        "actor": "Système Mobile & Auditeur",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["Blocage", "Falsification", "Revocation", "AntiFraude", "AlerteRouge"],
        "preconditions": "Carte scannée portant des données altérées ou signée par une clé révoquée.",
        "flow": [
            "Le vérificateur cryptographique exécute l'algorithme de contrôle de signature.",
            "Constat d'une anomalie critique :",
            "- Soit la signature mathématique échoue (un octet au moins a été modifié après signature).",
            "- Soit le `kid` correspond à une clé officielle compromise déclarée sur la liste noire de révocation.",
            "Bascule immédiate et irréversible en écran de blocage hermétique rouge sombre.",
            "Refus catégorique de délivrer les textes ou médias mémoriels pour empêcher toute usurpation.",
            "Consignation d'un incident de sécurité chiffré dans le journal d'audit local."
        ],
        "postconditions": "Accès hermétiquement verrouillé, alerte rouge de falsification affichée sans fuite de données.",
        "legal": "Code pénal belge (art. 196 et suivants - faux en écriture et usage de faux).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "mobile",
            "deviceLabel": "Sanctuaire Mobile • Bouclier Hermétique Anti-Falsification",
            "formFields": [
                {"label": "Statut Cryptographique", "name": "sig_status", "type": "text", "value": "ÉCHEC MAJEUR (Signature Invalide ou Clé Révoquée)", "placeholder": "Statut", "badge": "ALERTE ROUGE", "required": False},
                {"label": "Cause du Rejet", "name": "rejection_cause", "type": "text", "value": "Altération binaire post-signature ou clé d'autorité compromise", "placeholder": "Cause", "badge": "Faux Détecté", "required": False},
                {"label": "Politique de Sécurité", "name": "security_policy", "type": "text", "value": "BLOCAGE HERMÉTIQUE (Zéro affichage de données)", "placeholder": "Politique", "badge": "Zéro Fuite", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_close_session", "label": "Fermer la Session de Sécurité", "role": "danger", "state": "idle", "icon": "🛑"},
                {"id": "btn_export_audit_log", "label": "Exporter Rapport d'Incident", "role": "secondary", "state": "idle", "icon": "📄"}
            ],
            "validationMsg": {
                "title": "Bouclier Anti-Fraude Opérationnel",
                "badge": "Hermétique 100%",
                "detail": "Aucune donnée compromise n'a été affichée. Incident consigné au journal d'audit."
            },
            "errorCase": {
                "code": "ERR_CARD_FALSIFIED_OR_REVOKED",
                "title": "Carte Falsifiée ou Clé d'Autorité Révoquée",
                "condition": "Non-concordance de l'équation mathématique ou clé révoquée pour compromission.",
                "message": "BLOCAGE DE SÉCURITÉ INVIOLABLE : Cette carte présente une signature invalide ou une altération de données. Accès formellement refusé.",
                "remediation": "Contacter immédiatement l'agence émettrice pour expertise physique de la carte silicium."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Données en Cours d'Analyse Cryptographique",
                    "caption": "Signature en cours de décodage. L'anomalie de signature n'est pas encore révélée.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Détection d'un Bit Corrompu & Claquage du Verrou Rouge",
                    "triggerName": "Échec de l'équation RFC 8032 ou correspondance avec la liste de révocation",
                    "caption": "Bascule instantanée en alerte critique rouge sombre avec arrêt de tout rendu.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Effacement Mémoire & Journalisation de l'Incident",
                    "progress": 100,
                    "caption": "Purge immédiate des tampons mémoire vive pour empêcher toute exfiltration de données.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Écran Rouge Hermétique : Accès Bloqué",
                    "status": "alert",
                    "caption": "Refus absolu d'accès. La dignité et la sécurité de la mémoire sont protégées contre les faux.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-306",
        "title": "Sanctuaire Acoustique & Ducking Vocal Vivant Automatique",
        "cat": "Expérience Émotionnelle",
        "actor": "Famille & Proches",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["Ducking", "WebAudio", "AudioMixer", "Voix", "Emotion"],
        "preconditions": "Musique d'ambiance en cours de lecture et message vocal disponible.",
        "flow": [
            "L'utilisateur clique sur le bouton de lecture du témoignage vocal « Écouter la Voix du Défunt ».",
            "Le processeur WebAudio active instantanément le compresseur/ducking automatique :",
            "- Atténuation fluide du volume musical de fond de 100% à -14 dB en 400 millisecondes.",
            "- Lancement prioritaire de la voix au premier plan sonore à niveau solennel clair.",
            "Affichage simultané d'un oscilloscope lumineux synchronisé avec la vibration vocale.",
            "À la fin de la parole, rétablissement doux du volume musical d'ambiance en 1 200 millisecondes (fade-up)."
        ],
        "postconditions": "Immersion sonore réussie, harmonie acoustique digne et respectueuse de l'émotion familiale.",
        "legal": "Directives déontologiques funéraires relatives à la dignité et au respect des cérémonies.",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "mobile",
            "deviceLabel": "Sanctuaire Mobile • Processeur Acoustique & Ducking Vocal",
            "formFields": [
                {"label": "Piste Musique de Fond", "name": "bg_music", "type": "text", "value": "Gabriel Fauré — In Paradisum (Volume actuel : -14 dB)", "placeholder": "Musique", "badge": "Atténuée", "required": False},
                {"label": "Témoignage Vocal", "name": "voice_state", "type": "text", "value": "Lecture en cours : 00:14 / 00:30 (Premier Plan)", "placeholder": "Voix", "badge": "Prioritaire", "required": False},
                {"label": "Attaque Ducking DSP", "name": "duck_attack", "type": "text", "value": "400 ms (Descente douce)", "placeholder": "Attaque", "badge": "DSP", "required": False},
                {"label": "Relâchement Ducking", "name": "duck_release", "type": "text", "value": "1 200 ms (Remontée progressive en fin de voix)", "placeholder": "Relâchement", "badge": "DSP", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_pause_voice", "label": "⏸ Mettre la Voix en Pause", "role": "primary", "state": "active", "icon": "⏸"},
                {"id": "btn_mute_all", "label": "Silence Solennel Immédiat", "role": "secondary", "state": "idle", "icon": "🔇"}
            ],
            "validationMsg": {
                "title": "Ducking Vocal Actif & Parfaitement Calibré",
                "badge": "DSP WebAudio -14 dB",
                "detail": "Musique atténuée avec élégance. Voix chaleureuse et solennelle au premier plan."
            },
            "errorCase": {
                "code": "ERR_WEBAUDIO_AUTOPLAY_BLOCKED",
                "title": "Politique de Lecture Automatique Bloquée",
                "condition": "Navigateur mobile bloquant l'audio sans interaction tactile préalable de l'utilisateur.",
                "message": "Erreur audio : Le navigateur requiert un geste tactile pour autoriser la restitution sonore.",
                "remediation": "Toucher l'écran pour débloquer le contexte WebAudio et lancer le sanctuaire sonore."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Musique de Fond Seule à 100% du Volume",
                    "caption": "In Paradisum joue à volume normal. Le bouton du témoignage vocal attend d'être pressé.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Clic sur 'Écouter la Voix' & Déclenchement de l'Atténuateur",
                    "triggerName": "Clic tactile sur le lecteur de voix déclenchant la rampe de ducking",
                    "caption": "Envoi du signal DSP au nœud de gain de la musique pour descente à -14 dB en 400 ms.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Oscilloscope Vocal Actif & Musique Douce en Fond",
                    "progress": 50,
                    "caption": "La forme d'onde vocale vibre en rythme au centre de l'écran, soutenue par le fond orchestral.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Fin de Parole & Rétablissement Musique (Fade-Up 1.2s)",
                    "status": "success",
                    "caption": "Le message d'adieu s'achève avec émotion, la musique remonte doucement au premier plan.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-307",
        "title": "Consultation des Volontés Civiles et Funéraires",
        "cat": "Dernières Volontés",
        "actor": "Famille, Exécuteur Testamentaire & Pompes Funèbres",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["Volontes", "Loi1971", "Sepulture", "ArbreCineraire", "Preuve"],
        "preconditions": "Carte Directives (Carte 2) scannée par un membre de la famille ou le conseiller.",
        "flow": [
            "Sélection de l'onglet 'Volontés Civiles & Funéraires' dans l'application mobile.",
            "Déchiffrement local de la structure CBOR des volontés enregistrées lors du Bon à Tirer.",
            "Affichage solennel des choix formulés :",
            "- Cérémonie laïque civile sans fleurs artificielles.",
            "- Sépulture par sarcomusation avec restitution des amendements en forêt cinéraire (Démonstrateur de faisabilité prospectif — Option non autorisée par le droit positif actuel (référence à confirmer par un juriste)).",
            "- Désignation de l'Arbre Mémoriel n° F-2408 dans le massif forestier ardennais agréé.",
            "Génération d'une copie numérique certifiée infalsifiable opposable à toute contestation (sous réserve de conformité, référence à confirmer par un juriste)."
        ],
        "postconditions": "Dernières volontés du défunt portées à la connaissance des héritiers avec valeur probante légale.",
        "legal": "Loi du 20 juillet 1971 sur les funérailles et sépultures (art. 2 - primauté absolue des volontés) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "mobile",
            "deviceLabel": "Sanctuaire Mobile • Acte des Volontés Civiles Scellé",
            "formFields": [
                {"label": "Cérémonie Souhaitée", "name": "wills_ceremony", "type": "text", "value": "Cérémonie Civile Laïque sous les Arbres", "placeholder": "Cérémonie", "badge": "Loi 1971 (référence à confirmer par un juriste)", "required": False},
                {"label": "Mode de Sépulture", "name": "wills_burial", "type": "text", "value": "Sarcomusation & Retour en Forêt Cinéraire (Démonstrateur de faisabilité prospectif — Option non autorisée par le droit positif actuel (référence à confirmer par un juriste))", "placeholder": "Sépulture", "badge": "Démonstrateur Prospectif", "required": False},
                {"label": "Arbre Cinéraire Désigné", "name": "wills_tree", "type": "text", "value": "Chêne du Souvenir n° F-2408 (Forêt Saint-Hubert)", "placeholder": "Arbre", "badge": "Cadastré", "required": False},
                {"label": "Horodatage Légal Scellé", "name": "wills_timestamp", "type": "text", "value": "2026-10-04T15:30:00Z (Double Émargement Certifié)", "placeholder": "Horodatage", "badge": "Inviolable", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_export_wills_pdf", "label": "Télécharger l'Acte des Volontés (PDF)", "role": "primary", "state": "idle", "icon": "📄"},
                {"id": "btn_view_signatories", "label": "Vérifier Signatures Mandataire", "role": "secondary", "state": "idle", "icon": "✍️"}
            ],
            "validationMsg": {
                "title": "Volontés Civiles Consultables en Lecture Seule",
                "badge": "Valeur Probante Légale",
                "detail": "Texte intègre conforme à la loi du 20 juillet 1971 (référence à confirmer par un juriste). Inaltérable in-silico."
            },
            "errorCase": {
                "code": "ERR_POSTMORTEM_ACCESS_DENIED",
                "title": "Opposition Formelle à la Divulgation",
                "condition": "Clause de confidentialité post-mortem stipulée expressément par le défunt.",
                "message": "Accès restreint : Le défunt a expressément stipulé que ces volontés ne soient communiquées qu'à l'exécuteur testamentaire désigné.",
                "remediation": "Présenter le badge professionnel de l'exécuteur testamentaire ou la clé notariée habilitée."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Volet des Volontés Non Déployé",
                    "caption": "Menu principal affiché. L'utilisateur clique sur 'Consulter les Dernières Volontés'.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Ouverture du Compartiment Légal & Déchiffrement",
                    "triggerName": "Clic sur 'Consulter les Dernières Volontés' et décompression CBOR",
                    "caption": "Déchiffrement instantané des clauses funéraires avec contrôle de signature.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Mise en Page Solennelle & Contrôle de Primauté",
                    "progress": 95,
                    "caption": "Application de la typographie solennelle et vérification des références aux lois belges.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Acte des Volontés Affiché en Lecture Seule",
                    "status": "success",
                    "caption": "Document probant consultable et téléchargeable pour exécution immédiate.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-308",
        "title": "Fiche d'Urgence Médicale Interactive & Alerte Pacemaker (Art. L1232-24 CDLD & Modèle IIIC réglementaire)",
        "cat": "Directives Médicales & Sécurité",
        "actor": "Secouristes, Urgentistes, Pompes Funèbres & Médecin Légiste",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["UrgenceMedicale", "Secouristes", "Pacemaker", "DonOrganes", "DAE", "CDLD", "AppelUrgence"],
        "preconditions": "Scan NFC instantané de la Carte Directives par un secouriste, urgentiste ou agent funéraire habilité (Zéro Login requis).",
        "flow": [
            "Scan NFC immédiat de la Carte Directives civile & médicale sans aucun identifiant ni mot de passe (zéro login d'urgence pour secouristes).",
            "Ouverture instantanée de la Fiche d'Urgence Médicale Interactive sur le terminal mobile des secouristes ou urgentistes.",
            "Alerte immédiate exérèse stimulateur cardiaque / pacemaker : affichage rouge vif du danger d'explosion thermique (> 250°C), attestation chirurgicale d'exérèse (Dr. Marc Vaneck) avec rappel de l'Art. L1232-24 CDLD & Modèle IIIC réglementaire.",
            "Affichage direct du statut de consentement ou refus du don d'organes (cadre légal du consentement présumé de la loi de 1986).",
            "Mise à disposition immédiate de boutons d'appel d'urgence (SAMU 112, médecin certificateur) et des consignes post-mortem d'urgence (maintien chambre froide 4°C, délai d'exérèse < 24h, interdiction formelle de crémation sans visa)."
        ],
        "postconditions": "Fiche d'urgence médicale consultée, alerte d'exérèse pacemaker levée ou confirmée, protocole de don d'organes engagé et sécurité des intervenants garantie.",
        "legal": "Art. L1232-24 CDLD & Modèle IIIC réglementaire (exérèse obligatoire des stimulateurs cardiaques) et loi belge sur le don d'organes de 1986.",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "mobile",
            "deviceLabel": "Sanctuaire Mobile • Fiche d'Urgence Médicale Secouristes (Scan Directives)",
            "formFields": [
                {"label": "Déclencheur d'Urgence", "name": "emergency_trigger", "type": "text", "value": "Scan Immédiat Carte Directives (NFC Tap Zéro-Login Secouriste)", "placeholder": "Déclencheur", "badge": "Priorité Vitale", "required": False},
                {"label": "Alerte Stimulateur (Pacemaker / DAE)", "name": "pacemaker_alert", "type": "text", "value": "PRÉSENCE CONFIRMÉE — Risque Explosion Thermique (> 250°C)", "placeholder": "Implant", "badge": "ALERTE ROUGE", "required": True},
                {"label": "Statut Exérèse Chirurgicale", "name": "removal_cert", "type": "text", "value": "CERTIFIÉ RETIRÉ (Dr. Marc Vaneck — INAMI 1-40912-88-004)", "placeholder": "Exérèse", "badge": "Exérèse Conforme", "required": True},
                {"label": "Directives Don d'Organes (Loi 1986)", "name": "organ_donation", "type": "select", "value": "Consentement Plein et Entier Confirmé", "placeholder": "Don organes", "badge": "Loi 1986", "required": True},
                {"label": "Appels d'Urgence Rapides", "name": "emergency_contacts", "type": "text", "value": "SAMU 112 • Dr. Marc Vaneck (+32 81 22 33 44)", "placeholder": "Contacts", "badge": "Liaison Directe", "required": False},
                {"label": "Consignes Post-Mortem d'Urgence", "name": "post_mortem_instructions", "type": "text", "value": "Chambre froide 4°C • Délai légal exérèse < 24h • Interdiction crémation sans visa", "placeholder": "Consignes", "badge": "Consignes Pro", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_call_emergency_112", "label": "Appel d'Urgence Immédiat (112)", "role": "primary", "state": "idle", "icon": "🚨"},
                {"id": "btn_call_doctor_vaneck", "label": "Appeler Dr. Vaneck (Médecin)", "role": "secondary", "state": "idle", "icon": "📞"},
                {"id": "btn_view_full_medical_cert", "label": "Consulter Visa Exérèse Médical", "role": "secondary", "state": "idle", "icon": "🩺"},
                {"id": "btn_view_organ_protocol", "label": "Protocole Don d'Organes", "role": "secondary", "state": "idle", "icon": "🫀"}
            ],
            "validationMsg": {
                "title": "Fiche d'Urgence Médicale Secouriste Validée",
                "badge": "Alerte Pacemaker Levée • Don d'Organes Notifié",
                "detail": "Scan Carte Directives réussi. Visa d'exérèse vérifié conforme. Statut don d'organes communiqué pour protocole d'urgence."
            },
            "errorCase": {
                "code": "ERR_PACEMAKER_NOT_REMOVED_CRITICAL",
                "title": "Alerte Rouge : Pacemaker Présent Non Retiré",
                "condition": "Défunt porteur d'un stimulateur sans certificat médical d'exérèse renseigné.",
                "message": "DANGER DE MORT / EXPLOSION : Pacemaker actif non retiré. Manipulation, transport thermique et crémation formellement interdits (Art. L1232-24 CDLD & Modèle IIIC réglementaire).",
                "remediation": "Interdire immédiatement toute opération thermique. Contacter le médecin requis pour exérèse chirurgicale d'urgence."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Terminal Secouriste / Urgentiste en Écoute NFC",
                    "caption": "Fiche d'urgence en attente de présentation de la Carte Directives. Scan zéro-login prêt pour secouristes.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Scan Immédiat de la Carte Directives & Alerte Prioritaire",
                    "triggerName": "NFC Tap de la Carte Directives civile & médicale sans contact",
                    "caption": "Détection instantanée de la partition d'urgence et affichage prioritaire de la bannière rouge vif.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Contrôle Visa Exérèse & Directives Don d'Organes (< 150 ms)",
                    "progress": 98,
                    "caption": "Vérification in-silico du certificat d'exérèse du Dr. Vaneck et du consentement don d'organes (Loi 1986).",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Fiche d'Urgence Médicale Complète & Boutons d'Appel Actifs",
                    "status": "success",
                    "caption": "Fiche d'urgence validée. Sécurité garantie contre l'explosion, protocole don d'organes prêt, boutons d'appel 112 opérationnels.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-309",
        "title": "Consultation du Statut de Don d'Organes (Consentement Présumé Loi 1986)",
        "cat": "Directives Médicales",
        "actor": "Coordinateur Hospitalier de Transplantation",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["DonOrganes", "Loi1986", "Greffe", "Transplantation", "SPF"],
        "preconditions": "Carte Directives présentée au coordinateur de prélèvement d'organes d'un CHU.",
        "flow": [
            "Scan de la carte par le praticien de coordination des greffes hospitalières.",
            "Accès immédiat et sans mot de passe au compartiment 'Don d'Organes et Tissus Humains'.",
            "Affichage de la déclaration formelle de la personne :",
            "- Soit confirmation expresse et volontaire de consentement (cornées, reins, foie, cœur).",
            "- Soit enregistrement d'une opposition formelle de son vivant.",
            "Rappel des dispositions de la loi belge du 13 juin 1986 (régime de l'opt-out / consentement présumé).",
            "Édition d'un bordereau de traçabilité officiel annexé au dossier de prélèvement."
        ],
        "postconditions": "Volonté du défunt respectée sans ambiguïté, facilitation du travail urgent des équipes de greffe.",
        "legal": "Loi du 13 juin 1986 sur le prélèvement et la transplantation d'organes (art. 10 - consentement présumé).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "mobile",
            "deviceLabel": "Sanctuaire Mobile • Directives Hospitalières Don d'Organes",
            "formFields": [
                {"label": "Régime Légal Belge", "name": "organ_law", "type": "text", "value": "Loi du 13 juin 1986 (Consentement Présumé Opt-Out)", "placeholder": "Loi", "badge": "Loi 1986", "required": False},
                {"label": "Volonté Enregistrée", "name": "organ_status", "type": "text", "value": "CONSENTEMENT EXPRÈS CONFIRMÉ in-silico", "placeholder": "Volonté", "badge": "Donneur Actif", "required": False},
                {"label": "Tissus & Organes Autorisés", "name": "organ_types", "type": "text", "value": "Cornées, Reins, Foie, Poumons, Cœur", "placeholder": "Organes", "badge": "Multi-Dons", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_certify_organ_status", "label": "Délivrer le Visa de Consultation Médicale", "role": "primary", "state": "idle", "icon": "❤️"},
                {"id": "btn_spf_verify", "label": "Vérifier Registre Central SPF Santé", "role": "secondary", "state": "idle", "icon": "🏥"}
            ],
            "validationMsg": {
                "title": "Directives de Don d'Organes Validées",
                "badge": "Loi 13 juin 1986",
                "detail": "Consentement exprès confirmé in-silico. Consultation consignée au dossier médical."
            },
            "errorCase": {
                "code": "ERR_DONATION_OPPOSITION_FOUND",
                "title": "Opposition Formelle au Don d'Organes",
                "condition": "La carte contient une mention d'opposition formelle expresse enregistrée par le défunt.",
                "message": "OPPOSITION FORMELLE ENREGISTRÉE : Le défunt s'est expressément opposé au prélèvement de ses organes de son vivant. Tout prélèvement est pénalement interdit.",
                "remediation": "Respecter impérativement la volonté d'opposition du défunt et clore la procédure de transplantation."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Coordinateur Médical Approchant la Carte Directives",
                    "caption": "Urgence hospitalière. Le praticien vérifie si le défunt s'est opposé au don d'organes.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Scan NFC & Lecture du Compartiment Don d'Organes",
                    "triggerName": "Lecture NFC par le coordinateur hospitalier en salle de réanimation",
                    "caption": "Décodage en 30 millisecondes de la volonté enregistrée sur la puce ACOSJ.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Confrontation au Cadre Légal du Consentement Présumé",
                    "progress": 95,
                    "caption": "Vérification de l'absence de clause d'opposition et validation pour l'équipe de transplantation.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Fiche Médicale de Don Validée",
                    "status": "success",
                    "caption": "Attestation hospitalière générée pour l'équipe chirurgicale de prélèvement.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-310",
        "title": "Directives Legs du Corps à la Science sous 48h",
        "cat": "Directives Médicales",
        "actor": "Famille & Faculté de Médecine",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["LegsCorps", "Science", "Universite", "Delai48h", "Anatomie"],
        "preconditions": "Convention de legs du corps conclue de son vivant avec une université belge.",
        "flow": [
            "Affichage des directives d'urgence en cas de legs du corps à la science.",
            "Rappel impératif du délai légal absolu : le transport de corps vers le laboratoire d'anatomie doit intervenir dans les 48 heures ouvrées post-mortem.",
            "Affichage des coordonnées directes d'astreinte 24h/24 de la faculté de médecine conventionnée (ULiège, UCLouvain, ULB).",
            "Notification des pièces administratives requises (certificat de décès modèle IIIC et convention originale signée).",
            "Bouton d'appel d'urgence du service de transport anatomique conventionné."
        ],
        "postconditions": "Procédure de legs notifiée, respect impératif du délai des 48h garanti par l'application.",
        "legal": "Décret wallon et arrêtés royaux régissant le don de corps à l'enseignement anatomique universitaire (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "mobile",
            "deviceLabel": "Sanctuaire Mobile • Protocole d'Urgence Legs à la Science (48h)",
            "formFields": [
                {"label": "Faculté Conventionnée", "name": "med_university", "type": "text", "value": "Université de Liège (ULiège) — Laboratoire d'Anatomie", "placeholder": "Université", "badge": "Conventionné", "required": False},
                {"label": "Délai Légal Impératif", "name": "legal_delay", "type": "text", "value": "48 HEURES MAXIMALES ouvrées post-décès", "placeholder": "Délai", "badge": "Urgence 48h", "required": False},
                {"label": "Numéro de Convention", "name": "convention_num", "type": "text", "value": "ULIEGE-LEG-2024-819 (Signée du vivant)", "placeholder": "Convention", "badge": "Enregistré", "required": False},
                {"label": "Astreinte 24h/24 Morgue", "name": "morgue_contact", "type": "text", "value": "+32 4 366 21 11 (Permanence Corps Science)", "placeholder": "Téléphone", "badge": "Astreinte", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_call_transporter", "label": "📞 Alerter le Transporteur Anatomique", "role": "primary", "state": "idle", "icon": "📞"},
                {"id": "btn_view_contract", "label": "Consulter la Convention ULiège", "role": "secondary", "state": "idle", "icon": "📄"}
            ],
            "validationMsg": {
                "title": "Protocole de Legs sous 48h Notifié",
                "badge": "Urgence Déclenchée",
                "detail": "Contacts d'astreinte et convention ULiège affichés. Délai des 48h rappelé aux proches."
            },
            "errorCase": {
                "code": "ERR_LEG_BODY_DELAY_EXPIRED",
                "title": "Délai Légal de 48 Heures Expiré",
                "condition": "Signalement du décès plus de 48 heures après la survenue de la mort.",
                "message": "DÉLAI DÉPASSÉ : Le délai légal de 48 heures pour le transfert vers le laboratoire d'anatomie est expiré. La faculté de médecine ne peut plus accepter le corps.",
                "remediation": "Basculer immédiatement vers le protocole de sépulture par sarcomusation mémorielle (Démonstrateur de faisabilité prospectif — Option non autorisée par le droit positif actuel (référence à confirmer par un juriste)) ou crémation civile."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Signalement d'un Décès avec Volonté de Legs",
                    "caption": "La famille consulte les volontés médicales et découvre la convention de don à la science.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Déclenchement de l'Alerte Chronométrée des 48 Heures",
                    "triggerName": "Clic sur 'Consulter le Protocole 48h' et affichage des contacts d'astreinte",
                    "caption": "Mise en avant du compte à rebours légal des 48 heures et du numéro vert d'astreinte.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Génération du Dossier Administratif d'Accompagnement",
                    "progress": 90,
                    "caption": "Préparation de la fiche de transfert avec numéro de convention et horodatage certifié.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Protocole Universitaire Notifié avec Succès",
                    "status": "success",
                    "caption": "La permanence anatomique est prévenue. Le transport légal est sécurisé dans les délais.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-311",
        "title": "Droit d'Accès Post-Mortem au Dossier Médical (Loi 2002 Art. 9 §4)",
        "cat": "Droits du Patient",
        "actor": "Praticien Professionnel Désigné & Ayants Droit",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["Loi2002", "DossierMedical", "AyantsDroit", "SecretMedical", "Praticien"],
        "preconditions": "Carte Directives présentée par un médecin désigné par les ayants droit.",
        "flow": [
            "Conformément à l'article 9 §4 de la loi du 22 août 2002 relative aux droits du patient, l'accès au dossier médical après décès est strictement réservé à un praticien professionnel de santé désigné par la famille.",
            "Présentation conjointe de la Carte Directives et du jeton d'authentification professionnel du médecin (numéro INAMI).",
            "Saisie obligatoire de la motivation de la demande (recherche d'antécédents génétiques, vérification d'une faute médicale).",
            "Vérification de l'absence d'opposition expresse formulée de son vivant par le patient.",
            "Déverrouillage cryptographique du compartiment médical et consignation inaltérable dans le registre d'audit."
        ],
        "postconditions": "Accès strictement encadré accordé au médecin désigné, secret médical préservé face aux tiers non habilités.",
        "legal": "Loi du 22 août 2002 relative aux droits du patient (art. 9 §4 - accès post-mortem par praticien intermédiaire).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "mobile",
            "deviceLabel": "Sanctuaire Mobile • Guichet d'Accès Médical Post-Mortem (Loi 2002)",
            "formFields": [
                {"label": "Praticien Professionnel Désigné", "name": "designated_doc", "type": "text", "value": "Dr. Sophie Laurent (Médecin désigné par Claire Dubois)", "placeholder": "Médecin", "badge": "Habilité", "required": True},
                {"label": "Numéro d'Ordre / INAMI", "name": "doc_inami", "type": "text", "value": "INAMI : 1-89412-22-109", "placeholder": "INAMI", "badge": "Vérifié", "required": True},
                {"label": "Motivation de la Demande", "name": "request_motive", "type": "textarea", "value": "Recherche d'antécédents cardiovasculaires héréditaires au bénéfice des descendants.", "placeholder": "Motivation", "badge": "Exigé par Loi", "required": True},
                {"label": "Opposition Antérieure Patient", "name": "prior_opposition", "type": "text", "value": "AUCUNE OPPOSITION enregistrée du vivant du patient", "placeholder": "Opposition", "badge": "Autorisé", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_unlock_medical_vault", "label": "Déverrouiller le Compartiment Médical (Clé Praticien)", "role": "primary", "state": "idle", "icon": "🔓"},
                {"id": "btn_verify_family_mandate", "label": "Vérifier Mandat des Ayants Droit", "role": "secondary", "state": "idle", "icon": "⚖️"}
            ],
            "validationMsg": {
                "title": "Accès Médical Post-Mortem Accordé",
                "badge": "Conforme Loi 22 août 2002",
                "detail": "Dr. Sophie Laurent authentifiée. Synthèse médicale déverrouillée, journal d'audit émargé."
            },
            "errorCase": {
                "code": "ERR_PATIENT_RIGHTS_UNAUTHORIZED",
                "title": "Opposition du Défunt ou Praticien Non Habilité",
                "condition": "Tentative d'accès direct par un membre de la famille sans passer par un praticien, ou opposition du défunt.",
                "message": "ACCÈS REFUSÉ (Loi 22 août 2002) : L'accès au dossier médical post-mortem requiert l'intermédiation obligatoire d'un médecin désigné et l'absence d'opposition expresse du défunt.",
                "remediation": "Mandater un praticien professionnel de santé assermenté pour formuler la requête motivée."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Compartiment Médical Chiffré en Attente de Praticien",
                    "caption": "Volet confidentiel verrouillé. Le médecin doit s'authentifier avec son numéro INAMI.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Authentification du Praticien & Saisie de la Motivation",
                    "triggerName": "Scan du jeton professionnel du Dr. Laurent et validation de la motivation",
                    "caption": "Contrôle automatique de l'absence d'opposition du défunt dans le profil in-silico.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Vérification Art. 9 §4 & Dérivation de Clé Temporaire",
                    "progress": 95,
                    "caption": "Déverrouillage cryptographique éphémère en mémoire vive avec émargement du journal d'audit.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Synthèse Médicale Consultable par le Médecin",
                    "status": "success",
                    "caption": "Accès conforme au droit belge. Secret médical préservé pour les tiers non autorisés.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-312",
        "title": "Politique Mémorielle PaxFunèbre & Pérennité Séculaire (DEC-AET-11)",
        "cat": "Pérennité & Économie",
        "actor": "Famille & Réseau PaxFunèbre",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["Perennite", "Seculaire", "DEC-AET-11", "PolitiqueMemorielle", "LocalFirst"],
        "preconditions": "Sanctuaire mémoriel actif, consultation de l'onglet 'Pérennité & Archivage'.",
        "flow": [
            "Affichage des garanties de conservation de la mémoire physique in-silico :",
            "- Rétention des données EEPROM certifiée 100 ans à température ambiante sur JavaCard ACOSJ.",
            "- Fonctionnement 100% autonome sans abonnement obligatoire : la carte reste lisible à perpétuité par simple contact NFC même sans connexion Internet.",
            "- Présentation de l'accès mémoriel et de ses extensions selon la politique mémorielle Le Pax Funèbre (discrétion tarifaire absolue et dignité du deuil, DEC-AET-11).",
            "- Dotation familiale séculaire pour rééditions physiques de cartes ou médaillons en cas de perte par un descendant."
        ],
        "postconditions": "Pérennité physique et numérique garantie sur un siècle, discrétion tarifaire absolue et indépendance totale vis-à-vis des serveurs cloud.",
        "legal": "Directive européenne 2011/83/UE sur les droits des consommateurs (transparence et pérennité contractuelle) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "mobile",
            "deviceLabel": "Sanctuaire Mobile • Arche de Pérennité Séculaire (100 Ans)",
            "formFields": [
                {"label": "Rétention Physique Silicium", "name": "silicon_retention", "type": "text", "value": "100 ANS GARANTIS (Cellules EEPROM ACOSJ)", "placeholder": "Rétention", "badge": "100 Ans", "required": False},
                {"label": "Dépendance Cloud Obligatoire", "name": "cloud_dependency", "type": "text", "value": "ZÉRO DÉPENDANCE (100% Autonome Local-First)", "placeholder": "Cloud", "badge": "Souverain", "required": False},
                {"label": "Politique Mémorielle PaxFunèbre", "name": "pricing_policy", "type": "text", "value": "Régie par la politique PaxFunèbre (Discrétion tarifaire, DEC-AET-11)", "placeholder": "Politique", "badge": "DEC-AET-11", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_verify_vault_cert", "label": "Consulter le Certificat de Pérennité Séculaire", "role": "primary", "state": "idle", "icon": "🏛️"},
                {"id": "btn_duplicate_request", "label": "Demander un Médaillon pour Descendant", "role": "secondary", "state": "idle", "icon": "🎴"}
            ],
            "validationMsg": {
                "title": "Sanctuaire Mémoriel Séculaire Actif",
                "badge": "100 Ans in-silico",
                "detail": "Autonomie totale sans abonnement obligatoire. Accès régi par la politique mémorielle PaxFunèbre (DEC-AET-11)."
            },
            "errorCase": {
                "code": "ERR_VAULT_DEPOSIT_EXHAUSTED",
                "title": "Dotation de Réédition Échue",
                "condition": "Demande de fabrication d'un duplicata physique sans fonds de dotation séculaire actif.",
                "message": "Information contractuelle : Le quota de réédition physique est épuisé. La carte originale reste cependant lisible à 100% sans frais.",
                "remediation": "Consulter les modalités d'accueil mémoriel auprès de l'agence Le Pax Funèbre selon la politique mémorielle en vigueur (DEC-AET-11)."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Statut de Conservation Séculaire en Consultation",
                    "caption": "La famille consulte l'arche de mémoire et les garanties matérielles de la puce ACOSJ.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Affichage des Côtés Techniques & Absence de Cloud",
                    "triggerName": "Clic sur 'Consulter le Certificat de Pérennité Séculaire'",
                    "caption": "Mise en avant des arguments souverains : Zéro abonnement obligatoire, politique mémorielle et discrétion tarifaire PaxFunèbre (DEC-AET-11).",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Génération de l'Attestation Séculaire Infalsifiable",
                    "progress": 95,
                    "caption": "Scellement de l'acte de pérennité avec signature officielle de la dotation Le Pax Funèbre.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Certificat de Pérennité Séculaire Remis",
                    "status": "success",
                    "caption": "Sérénité absolue pour la famille. La mémoire d'Henri Dubois traversera les générations.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-313",
        "title": "Panne Audio / Perte de Périphérique & Mode Sanctuaire Silencieux Visuel",
        "cat": "Expérience Émotionnelle & Résilience",
        "actor": "Famille & Proches en Recueillement",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": [
    "SanctuaireSilencieux",
    "WebAudio",
    "Accessibilite",
    "VisualWave",
    "OpusSILK",
    "EF-3"
],
        "preconditions": "La famille consulte la carte Sanctuaire sur un smartphone dont la sortie audio est muette, en panne ou en mode silencieux strict.",
        "flow": [
            "L'utilisateur effleure la carte Sanctuaire pour lancer l'hommage sonore d'EF-3.",
            "Le composant WebAudio tente d'ouvrir le flux de restitution : détection d'une suspension du sous-système audio ou absence de sortie.",
            "Bascule instantanée, fluide et solennelle vers le 'Mode Sanctuaire Silencieux Visuel' sans message d'erreur alarmant.",
            "Déploiement d'une animation d'ondes dorées synchronisées avec la modulation de la voix et affichage textuel de la transcription.",
            "Maintien de l'émotion et du recueillement avec proposition discrète de réactiver le son dès reconnexion d'un périphérique."
        ],
        "postconditions": "L'hommage mémoriel se déroule dans la sérénité et le recueillement, même sans canal audio actif.",
        "legal": "Directives d'accessibilité numérique W3C WCAG 2.1 (critère 1.2 médias temporels) & Charte Sanctuaire Mémoriel.",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "mobile",
            "deviceLabel": "Sanctuaire Mobile • Mode Recueillement Silencieux Visuel (Partition EF-3)",
            "formFields": [
                {
                    "label": "Périphérique de Sortie Audio",
                    "name": "audio_device_status",
                    "type": "text",
                    "value": "Indisponible / Mode Silencieux Détecté",
                    "badge": "Silencieux",
                    "required": False
                },
                {
                    "label": "Mode Visuel Actif",
                    "name": "visual_sanctuary_mode",
                    "type": "text",
                    "value": "Ondes Harmoniques Dorées + Transcription Hommage",
                    "badge": "Sérénité",
                    "required": False
                },
                {
                    "label": "Transcription Textuelle EF-3",
                    "name": "voice_transcript",
                    "type": "textarea",
                    "value": "« Souvenez-vous des jours heureux passés ensemble sous le grand chêne... Mon amour veille sur vous. »",
                    "badge": "Transcription",
                    "required": False
                },
                {
                    "label": "Ducking & Ambiance",
                    "name": "ambiance_status",
                    "type": "text",
                    "value": "Transition douce vers silence apaisé (0 dB)",
                    "badge": "WebAudio",
                    "required": False
                }
            ],
            "actionButtons": [
                {
                    "id": "btn_activate_visual_mode",
                    "label": "Basculer en Mode Sanctuaire Silencieux Visuel",
                    "role": "primary",
                    "state": "idle",
                    "icon": "🕊️"
                },
                {
                    "id": "btn_retry_audio",
                    "label": "Réessayer la Sortie Audio",
                    "role": "secondary",
                    "state": "idle",
                    "icon": "🔊"
                }
            ],
            "validationMsg": {
                "title": "Mode Sanctuaire Silencieux Visuel Engagé avec Succès",
                "badge": "Sanctuaire Visuel Actif",
                "detail": "Expérience mémorielle préservée. Transcription synchronisée et ondes de recueillement dorées actives."
            },
            "errorCase": {
                "code": "ERR_AUDIO_OUTPUT_UNAVAILABLE",
                "title": "Sortie Audio Inaccessible ou Système Muet",
                "condition": "Absence de périphérique audio disponible ou blocage de la lecture automatique par la politique du navigateur.",
                "message": "Périphérique audio indisponible : bascule automatique vers le recueillement visuel respectueux.",
                "remediation": "Vérifier le commutateur silencieux du smartphone ou brancher des écouteurs pour écouter la voix originale."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Détection d'une Sortie Audio Muette",
                    "caption": "Le smartphone est en mode silencieux lors de l'effleurement NFC de la carte Sanctuaire.",
                    "screenHtml": """
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
"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Déploiement des Ondes Harmoniques Dorées",
                    "triggerName": "Clic sur 'Basculer en Mode Sanctuaire Silencieux'",
                    "caption": "Génération de l'animation d'ondes douces synchronisée sur le spectre de la voix mémorisée.",
                    "screenHtml": """
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
"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Diffusion du Message & Veilleuse Lumineuse",
                    "progress": 96,
                    "caption": "Le texte défile doucement accompagné d'une flamme mémorielle numérique.",
                    "screenHtml": """
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
"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Recueillement Achevé dans la Dignité",
                    "status": "success",
                    "caption": "L'hommage s'est déroulé dans la sérénité. La famille a vécu un moment de communion intact.",
                    "screenHtml": """
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
"""
                }
            }
        }
    },
    {
        "id": "UC-314",
        "title": "Lecture de Secours par QR Code Micro-Gravé sur Carte Endommagée",
        "cat": "Résilience Mémorielle & Secours",
        "actor": "Proches du Défunt & Conseiller Funéraire",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": [
    "QRCode",
    "Secours",
    "AntenneNFCBrisée",
    "OfflineFallback",
    "CBOR",
    "EF-1"
],
        "preconditions": "La carte physique a subi une violente torsion ou un choc mécanique ayant fracturé l'antenne NFC interne.",
        "flow": [
            "L'utilisateur pose son smartphone sur la carte : aucun contact RF n'est établi après plusieurs essais.",
            "L'application Sanctuaire propose automatiquement l'option 'Relecture de Secours par Capteur Optique'.",
            "La caméra du smartphone capture le micro QR Code haute densité gravé au laser au verso de la carte.",
            "Décodage instantané du flux binaire compressé CBOR contenant l'identité civile, l'épitaphe et l'empreinte de signature.",
            "Reconstitution intégrale du profil mémoriel et vérification de la signature cryptographique en mémoire locale."
        ],
        "postconditions": "La mémoire du défunt est restituée avec intégrité malgré la destruction matérielle de la liaison radio NFC.",
        "legal": "Norme ISO/IEC 18004 (code à barres matriciel QR Code haute densité) & Principe de résilience mémorielle séculaire.",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "mobile",
            "deviceLabel": "Sanctuaire Mobile • Scanner de Secours QR Code Haute Densité (EF-1)",
            "formFields": [
                {
                    "label": "Signal Radio NFC",
                    "name": "nfc_rf_status",
                    "type": "text",
                    "value": "ZÉRO SIGNAL DÉTECTÉ (Antenne fracturée)",
                    "badge": "Panne RF",
                    "required": False
                },
                {
                    "label": "Méthode de Repli",
                    "name": "fallback_method",
                    "type": "select",
                    "value": "Micro QR Code Laser Recto/Verso Haute Densité",
                    "badge": "Secours Optique",
                    "required": True
                },
                {
                    "label": "Données Décodées CBOR",
                    "name": "cbor_decoded_summary",
                    "type": "text",
                    "value": "Henri Dubois • 1948-2026 • Épitaphe & Directives Intègres",
                    "badge": "Validé",
                    "required": False
                },
                {
                    "label": "Vérification Empreinte SHA-256",
                    "name": "sha256_hash_status",
                    "type": "text",
                    "value": "CONCORDANCE PARFAITE avec le sceau d'origine",
                    "badge": "Intégrité",
                    "required": False
                }
            ],
            "actionButtons": [
                {
                    "id": "btn_scan_qr_fallback",
                    "label": "Activer la Caméra & Scanner le QR Code de Secours",
                    "role": "primary",
                    "state": "idle",
                    "icon": "📷"
                },
                {
                    "id": "btn_manual_aid_input",
                    "label": "Saisir le Code d'Identité Imprimé",
                    "role": "secondary",
                    "state": "idle",
                    "icon": "⌨️"
                }
            ],
            "validationMsg": {
                "title": "Profil Mémoriel Restitué par Décodage Optique",
                "badge": "Secours QR Code Conforme",
                "detail": "Flux binaire CBOR décodé avec succès. Intégrité et empreinte cryptographique validées à 100%."
            },
            "errorCase": {
                "code": "ERR_NFC_ANTENNA_DAMAGED_QR_FALLBACK",
                "title": "Antenne Sans Contact Défaillante & Recours au QR Code",
                "condition": "Absence de réponse APDU ISO 14443-4 sur une carte présentant des fissures physiques.",
                "message": "Liaison NFC indisponible : L'antenne de la carte est endommagée. Déclenchement de la capture optique de secours.",
                "remediation": "Présenter le verso de la carte devant l'objectif de la caméra pour lire le micro-code de secours matriciel."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Échec de Détection Radio & Proposition de Secours",
                    "caption": "Le scan NFC échoue en raison d'une avarie d'antenne. L'application invite à utiliser l'optique.",
                    "screenHtml": """
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
"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Visée Optique & Capture Haute Vitesse",
                    "triggerName": "Clic sur 'Scanner le QR Code de Secours'",
                    "caption": "Reconnaissance du motif matriciel haute densité et extraction du payload binaire compressé.",
                    "screenHtml": """
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
"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Décompression CBOR & Contrôle d'Intégrité",
                    "progress": 94,
                    "caption": "Validation de l'authenticité des données d'état civil sans nécessiter aucun réseau externe.",
                    "screenHtml": """
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
"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Sanctuaire Ouvert & Mémoire Accessible",
                    "status": "success",
                    "caption": "La mémoire triomphe de la panne matérielle. La famille accède au mémorial sans encombre.",
                    "screenHtml": """
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
"""
                }
            }
        }
    },
    {
        "id": "UC-315",
        "title": "Réclamations Contradictoires des Ayants Droit sur l'Arbre du Souvenir (Mise en Réserve Conservatoire)",
        "cat": "Arbitrage & Volontés Funéraires",
        "actor": "Ayants Droit & Médiateur / Notaire",
        "platforms": ["Web Standard (PWA Hors-Ligne)", "Natif (iOS & Android)"],
        "tags": [
    "LitigeFamilial",
    "ArbreDuSouvenir",
    "ReserveConservatoire",
    "Sequestre",
    "EF-4",
    "Loi1971"
],
        "preconditions": "Deux branches d'une famille expriment des volontés divergentes concernant la destination cinéraire ou la gestion du livre d'or.",
        "flow": [
            "Notification formelle d'une contestation successorale ou funéraire transmise au service d'arbitrage mémoriel.",
            "Activation sur l'application Sanctuaire de la procédure de 'Mise en Réserve Conservatoire'.",
            "Verrouillage immédiat des modifications sur le registre de sépulture et l'amendement de l'Arbre du Souvenir dans EF-4.",
            "Affichage d'un bandeau neutre et solennel appelant au respect de la mémoire et signalant la médiation notariale en cours.",
            "Maintien exclusif des fonctions de recueillement contemplatif (photos, textes) sans modification possible des sépultures."
        ],
        "postconditions": "Aucune modification unilatérale n'est enregistrée ; le respect de l'ordre public funéraire est garanti.",
        "legal": "Loi du 20 juillet 1971 sur les funérailles et sépultures & Code civil (règles de dévolution des décisions funéraires).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "tablet",
            "deviceLabel": "Sanctuaire Pro • Module d'Arbitrage & Séquestre Mémoriel (Partition EF-4)",
            "formFields": [
                {
                    "label": "Dossier Mémoriel Concerné",
                    "name": "case_reference",
                    "type": "text",
                    "value": "Dossier #AET-2026-NAM-0491 (Henri Dubois)",
                    "badge": "Dossier",
                    "required": False
                },
                {
                    "label": "Statut Juridique d'Affectation",
                    "name": "legal_reserve_status",
                    "type": "text",
                    "value": "MISE EN RÉSERVE CONSERVATOIRE (Litige Ayants Droit)",
                    "badge": "Séquestre",
                    "required": False
                },
                {
                    "label": "Arbre du Souvenir Revendiqué",
                    "name": "disputed_tree",
                    "type": "text",
                    "value": "Chêne Séculaire Parcelle DNF #B-12 (Opposition déclarée)",
                    "badge": "Litige",
                    "required": False
                },
                {
                    "label": "Mesure Conservatoire Prise",
                    "name": "protective_measure",
                    "type": "select",
                    "value": "Gel des Inscriptions & Maintien Recueillement Neutre",
                    "badge": "Médiation",
                    "required": True
                }
            ],
            "actionButtons": [
                {
                    "id": "btn_apply_conservative_hold",
                    "label": "Activer le Séquestre Conservatoire Mémoriel",
                    "role": "primary",
                    "state": "idle",
                    "icon": "⚖️"
                },
                {
                    "id": "btn_view_notarial_notice",
                    "label": "Consulter l'Avis de Médiation Notariale",
                    "role": "secondary",
                    "state": "idle",
                    "icon": "📜"
                }
            ],
            "validationMsg": {
                "title": "Mise en Réserve Conservatoire Notifiée",
                "badge": "Séquestre Mémoriel Actif",
                "detail": "Registre EF-4 verrouillé en modification. Accès maintenu en mode neutre solennel en attente d'arbitrage notarié."
            },
            "errorCase": {
                "code": "ERR_CONTRADICTORY_HEIRS_CLAIM",
                "title": "Conflit Juridique Entre Ayants Droit sur la Destination des Cendres",
                "condition": "Opposition formelle déposée par un héritier direct contestant l'affectation de l'Arbre du Souvenir.",
                "message": "Blocage conservatoire : Des réclamations contradictoires sont enregistrées. Aucune modification du registre n'est autorisée.",
                "remediation": "Transmettre l'acte de notoriété ou l'accord signé de tous les héritiers au notaire instrumentant pour lever la réserve."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Signalement d'une Contestation Familiale",
                    "caption": "Deux ayants droit revendiquent des décisions opposées concernant le devenir de l'amendement cinéraire.",
                    "screenHtml": """
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
"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Application du Gel Conservatoire sur EF-4",
                    "triggerName": "Clic sur 'Activer le Séquestre Conservatoire'",
                    "caption": "Verrouillage des transactions sur la partition de sépulture et génération du bandeau d'apaisement.",
                    "screenHtml": """
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
"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Configuration du Sanctuaire en Mode Neutre Solennel",
                    "progress": 100,
                    "caption": "L'interface masque les options contestées et préserve la dignité des hommages visuels.",
                    "screenHtml": """
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
"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Paix Mémorielle Préservée & Médiation en Cours",
                    "status": "success",
                    "caption": "La mémoire du défunt est mise à l'abri des querelles. La décision finale interviendra sereinement.",
                    "screenHtml": """
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
"""
                }
            }
        }
    },
    {
        "id": "UC-316",
        "title": "Mode Hors-Ligne Extrême / Zone Blanche sans Réseau en Forêt Mémorielle (WebCrypto Local Ed25519)",
        "cat": "Sécurité & Résilience Hors-Ligne",
        "actor": "Famille en Forêt Cinéraire & Garde-Forestier",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": [
    "ZoneBlanche",
    "HorsLigneExtreme",
    "WebCrypto",
    "Ed25519",
    "TrustList",
    "LocalFirst",
    "EF-5"
],
        "preconditions": "La famille se recueille au pied de l'Arbre du Souvenir au fond d'un massif forestier DNF, en zone blanche totale (zéro barre 4G/5G).",
        "flow": [
            "Effleurement NFC sans contact de la carte mémorielle par le smartphone en pleine forêt isolée.",
            "Le service worker de la PWA prend le relais à 100% sans tenter aucune requête HTTP distante.",
            "Exécution locale de la validation cryptographique COSE_Sign1 via la bibliothèque WebCrypto (SubtleCrypto Ed25519).",
            "Vérification de l'empreinte de la clé émettrice par rapport à la TrustList souveraine pré-enregistrée en stockage persistant.",
            "Ouverture instantanée du sanctuaire mémoriel : affichage des portraits, lecture du testament et recueillement en pleine nature."
        ],
        "postconditions": "L'intégrité cryptographique et l'authenticité sont démontrées à 100% sans nécessiter un seul bit échangé sur Internet.",
        "legal": "Décision Kudoro DEC-AET-09 (universalité d'accès sans contact hors-ligne) & Charte de résilience mémorielle séculaire.",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "mobile",
            "deviceLabel": "Sanctuaire Mobile • Moteur Cryptographique WebCrypto Hors-Ligne (EF-5)",
            "formFields": [
                {
                    "label": "Couverture Réseau Mobile",
                    "name": "network_status",
                    "type": "text",
                    "value": "ZONE BLANCHE TOTALE (0 barre • Aucun réseau)",
                    "badge": "100% Déconnecté",
                    "required": False
                },
                {
                    "label": "Moteur Cryptographique",
                    "name": "crypto_engine",
                    "type": "text",
                    "value": "WebCrypto API Locale (SubtleCrypto Ed25519 / ES256)",
                    "badge": "In-Device",
                    "required": False
                },
                {
                    "label": "TrustList Souveraine Embarquée",
                    "name": "embedded_trustlist",
                    "type": "text",
                    "value": "TrustList v2.4 (24 clés de confiance Le Pax Funèbre)",
                    "badge": "Vérifié",
                    "required": False
                },
                {
                    "label": "Temps de Vérification Locale",
                    "name": "local_verify_time",
                    "type": "text",
                    "value": "18 millisecondes (Calcul mathématique local)",
                    "badge": "Instantané",
                    "required": False
                }
            ],
            "actionButtons": [
                {
                    "id": "btn_verify_offline_crypto",
                    "label": "Vérifier la Signature Ed25519 en Local (WebCrypto)",
                    "role": "primary",
                    "state": "idle",
                    "icon": "🌲"
                },
                {
                    "id": "btn_open_forest_sanctuary",
                    "label": "Entrer dans le Sanctuaire Forestier",
                    "role": "secondary",
                    "state": "idle",
                    "icon": "🕊️"
                }
            ],
            "validationMsg": {
                "title": "Authenticité Cryptographique Vérifiée 100% Hors-Ligne",
                "badge": "WebCrypto Ed25519 Valide",
                "detail": "Signature COSE_Sign1 vérifiée en 18 ms via SubtleCrypto local. Chaîne de confiance souveraine validée sans réseau."
            },
            "errorCase": {
                "code": "ERR_OFFLINE_CACHE_UNAVAILABLE",
                "title": "Cache PWA Absent ou TrustList Non Initialisée Hors-Ligne",
                "condition": "Premier lancement de l'application effectué en zone blanche sans avoir préalablement mis en cache les assets.",
                "message": "Erreur d'initialisation : Le cache de l'application est incomplet. Impossible d'exécuter la vérification locale sans les artefacts de base.",
                "remediation": "Effectuer une première ouverture de l'application en zone connectée pour mettre en cache la TrustList et les modules WebCrypto."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Recueillement en Forêt DNF sans Réseau",
                    "caption": "La famille est réunie au pied de l'Arbre du Souvenir en zone blanche complète.",
                    "screenHtml": """
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
"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Calcul Mathématique Local de la Signature Ed25519",
                    "triggerName": "Clic sur 'Vérifier la Signature Ed25519 en Local'",
                    "caption": "Exécution de la formule RFC 8032 sur les courbes elliptiques directement dans le processeur du smartphone.",
                    "screenHtml": """
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
"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Authenticité Prouvée & Zéro Dépendance Serveur",
                    "progress": 100,
                    "caption": "Preuve mathématique irréfutable de la validité de la carte en 18 millisecondes.",
                    "screenHtml": """
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
"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Sanctuaire Mémoriel Ouvert en Pleine Forêt",
                    "status": "success",
                    "caption": "Le recueillement s'opère en parfaite harmonie avec la nature, sans fil et sans dépendance.",
                    "screenHtml": """
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
"""
                }
            }
        }
    }
,
    {'id': 'UC-317', 'title': 'Décodage Enregistrements NDEF Mixtes (MIME Type vs URI Record Dispatcher)', 'cat': 'Accès & Identité', 'actor': 'PWA Sanctuaire / Parser NDEF Bas Niveau', 'platforms': ['Web NFC (Chrome Android)', 'Natif (iOS CoreNFC & Android IsoDep)', 'Lecteur USB-C NFC'], 'tags': ['NDEF', 'MIMEType', 'UriRecord', 'NfcDispatcher', 'IsoDep', 'Type4Tag'], 'summary': "Analyse et séparation séquentielle des enregistrements NDEF composites sur puce NFC Type 4 : aiguillage prioritaire vers le payload binaire MIME application/vnd.aeternitrak.sanctuary+cbor plutôt que vers l'URI de redirection web.", 'badge': 'NDEF Dispatcher Actif', 'legalRef': 'Spécification NFC Forum NDEF Type 4 Tag v2.0 & RFC 8152 (CBOR Object Signing and Encryption).', 'legal': 'Spécification NFC Forum NDEF Type 4 Tag v2.0 & RFC 8152 (CBOR Object Signing and Encryption).', 'legal_url': '#section-legal', 'preconditions': "Effleurement NFC d'une carte mémorielle ou médaillon contenant une structure NDEF composite (Well-Known URI + MIME media type).", 'flow': ["Capture de l'événement de détection NDEF par l'antenne NFC du smartphone en moins de 40 ms.", "Parsing séquentiel des octets d'en-tête (TNF Type Name Format et Chunk Flags).", "Identification de l'enregistrement 1 : URI Well-Known (fallback d'accès universel).", "Identification de l'enregistrement 2 : MIME application/vnd.aeternitrak.sanctuary+cbor (charge utile chiffrée et scellée de 42 812 octets).", 'Aiguillage du flux binaire brut vers le décodeur CBOR in-memory sans redirection de page web inutile.'], 'postconditions': 'Payload binaire CBOR extrait et injecté dans le moteur cryptographique COSE_Sign1 in-device.', 'incident': {'code': 'ERR_NDEF_MALFORMED_HEADER', 'title': 'En-Tête NDEF Corrompu ou Inconnu', 'message': 'Structure NDEF invalide (TNF non pris en charge ou taille de charge utile négative).', 'remediation': 'Réapprocher la carte ou utiliser le lecteur de secours optique QR micro-gravé.'}, 'wireframe': {'device': 'mobile', 'deviceLabel': 'Sanctuaire Mobile • Routeur NDEF Bas Niveau', 'formFields': [{'label': 'Type Name Format (TNF)', 'name': 'ndef_tnf', 'type': 'text', 'value': '0x02 (MIME_MEDIA) & 0x01 (WELL_KNOWN URI)', 'badge': 'Composite', 'required': False}, {'label': 'Record 1 (Fallback URI)', 'name': 'rec_uri', 'type': 'text', 'value': 'https://sanctuary.aeternitrak.eu/u/AET-BEL-84920', 'badge': 'URI Record', 'required': False}, {'label': 'Record 2 (MIME CBOR)', 'name': 'rec_mime', 'type': 'text', 'value': 'application/vnd.aeternitrak.sanctuary+cbor (42 812 octets)', 'badge': 'MIME Payload', 'required': False}, {'label': 'Stratégie Dispatcher', 'name': 'dispatch_policy', 'type': 'text', 'value': 'PRIORITÉ BINAIRE IN-SILICO (Zéro Redirection Web)', 'badge': 'Local First', 'required': False}], 'actionButtons': [{'id': 'btn_dispatch_ndef', 'label': 'Dégrouper & Router les Enregistrements NDEF', 'role': 'primary', 'state': 'idle', 'icon': '🔀'}, {'id': 'btn_raw_hex_ndef', 'label': 'Inspecter Trame Hexadécimale NDEF', 'role': 'secondary', 'state': 'idle', 'icon': '🔍'}], 'validationMsg': {'title': 'Enregistrements NDEF Mixtes Décodés avec Succès', 'badge': 'NDEF Parsing 100% OK', 'detail': 'Ségrégation validée : Payload binaire CBOR (42.8 Ko) routé vers le moteur cryptographique local sans requête HTTP.'}, 'errorCase': {'code': 'ERR_NDEF_MALFORMED_HEADER', 'title': 'En-Tête NDEF Corrompu ou TNF Réservé', 'condition': 'Corruption de mémoire EEPROM ou écriture interrompue générant un TNF non standard (0x07).', 'message': "Erreur de parsing NDEF : Le format des enregistrements est corrompu. Impossible d'extraire la charge utile binaire.", 'remediation': 'Approcher à nouveau la carte du terminal ou recourir à la lecture de secours par QR code micro-gravé.'}, 'phases': {'p1': {'tabTitle': '1. Avant Trigger', 'phaseTitle': "Trame NDEF Brute Détectée sur l'Antenne", 'caption': 'Le contrôleur NFC a capté une charge utile composite sur la puce Type 4.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Décodeur NDEF Bas Niveau</span>\n                        <span class="wf-status-badge wf-badge-neutral">Trame Reçue (43.2 Ko)</span>\n                      </div>\n                      <div class="wf-device-status-box">\n                        <span class="wf-qa-icon">📡</span>\n                        <div><strong>Enregistrements NDEF Multiples Présents</strong></div>\n                        <div class="wf-subtext">TNF 0x01 (URI universelle) + TNF 0x02 (MIME binaire in-silico)</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary">🔀 Dégrouper & Router les Enregistrements NDEF</button>\n                      </div>\n                    </div>\n'}, 'p2': {'tabTitle': '2. Déclenchement ⚡', 'phaseTitle': 'Séparation des Enregistrements dans le Buffer', 'triggerName': "Clic sur 'Dégrouper & Router'", 'caption': "Le moteur d'inspection analyse les offsets et isole le bloc applicatif CBOR.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Dispatcher NDEF</span>\n                        <span class="wf-status-badge wf-badge-trigger">⚡ Découpage Binaire</span>\n                      </div>\n                      <div class="wf-trigger-card wf-radar-pulse">\n                        <div class="wf-trigger-indicator">Parsing des offsets : Rec#1 @0x0003 (URI) | Rec#2 @0x004A (CBOR)</div>\n                        <div class="wf-subtext">Isolation du bloc MIME sans altération des signatures cryptographiques</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Routage in-memory en cours...</button>\n                      </div>\n                    </div>\n'}, 'p3': {'tabTitle': '3. Traitement ⚙️', 'phaseTitle': 'Aiguillage Local-First Vers Décodeur CBOR', 'progress': 96, 'caption': 'Redirection web contournée avec succès pour privilégier le déchiffrement direct.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Routeur Local-First</span>\n                        <span class="wf-status-badge wf-badge-process">⚙️ Payload Isolé (96%)</span>\n                      </div>\n                      <div class="wf-console-log">\n                        <code>> [NDEF] TNF=0x01 Type="U" -> Ignoré (zéro redirection réseau demandée)</code><br>\n                        <code>> [NDEF] TNF=0x02 Type="application/vnd.aeternitrak.sanctuary+cbor"</code><br>\n                        <code>> [DISPATCH] 42 812 octets dirigés vers le pipeline WebCrypto</code><br>\n                        <code>> [LOCAL-FIRST] Traitement in-silico 100% autonome validé</code>\n                      </div>\n                    </div>\n'}, 'p4': {'tabTitle': '4. Écran de Fin ✨', 'phaseTitle': 'Payload Prêt pour Vérification Cryptographique', 'status': 'success', 'caption': 'Le flux binaire est mis à disposition du moteur sans transition web superflue.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Parsing Achevée</span>\n                        <span class="wf-status-badge wf-badge-success">✨ Données Prêtes</span>\n                      </div>\n                      <div class="wf-success-banner">\n                        <span class="wf-seal-icon">📦</span>\n                        <div>\n                          <strong>Charge Utile Mémorielle Extraite sans Réseau</strong>\n                          <p class="wf-subtext">42 812 octets CBOR prêts pour vérification COSE_Sign1</p>\n                        </div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-gold">Passer au Contrôle Cryptographique Ed25519 →</button>\n                      </div>\n                    </div>\n'}}}},
    {'id': 'UC-318', 'title': 'Recherche Clé Publique dans le TrustStore Local par Key ID (kid 16 octets)', 'cat': 'Sécurité & Cryptographie', 'actor': 'Gestionnaire de Clés Souverain / Moteur Cryptographique', 'platforms': ['Natif (iOS & Android)', 'Web Standard (PWA Hors-Ligne IndexedDB)'], 'tags': ['TrustStore', 'KeyID', 'kid', 'Ed25519', 'IndexedDB', 'LocalFirst'], 'summary': "Extraction du Key ID (kid de 16 octets) de l'enveloppe COSE_Sign1 et résolution instantanée de la clé publique Ed25519 correspondante dans le TrustStore local sans requête réseau.", 'badge': 'Résolution TrustStore 12ms', 'legalRef': 'Norme RFC 9052 (COSE Structure) & Décision Kudoro DEC-AET-04 (validation cryptographique locale souveraine).', 'legal': 'Norme RFC 9052 (COSE Structure) & Décision Kudoro DEC-AET-04 (validation cryptographique locale souveraine).', 'legal_url': '#section-legal', 'preconditions': "Charge utile COSE_Sign1 extraite contenant l'en-tête non protégé kid = 0x9a8b7c6d5e4f3210.", 'flow': ["Extraction de l'en-tête COSE_Sign1 non protégé portant le kid (16 octets / 128 bits).", 'Interrogation indexée du TrustStore local persistant (IndexedDB / SQLite chiffré).', "Recherche par clé primaire sur le hash de clé d'autorité funéraire certifiée.", "Association confirmée avec l'Autorité Funéraire Émettrice (ex: Le Pax Funèbre Liège #01).", 'Fourniture de la clé publique Ed25519 non altérée au vérificateur mathématique.'], 'postconditions': 'Clé publique Ed25519 identifiée et chargée en mémoire vive pour validation mathématique.', 'incident': {'code': 'ERR_TRUSTSTORE_KID_NOT_FOUND', 'title': 'Key ID Inconnu dans le TrustStore Local', 'message': 'Le kid ne correspond à aucune clé publique répertoriée dans la TrustList locale.', 'remediation': 'Basculer sur le bandeau de réserve DEC-AET-07 Option B (consultation avec réserve).'}, 'wireframe': {'device': 'mobile', 'deviceLabel': 'Sanctuaire Mobile • Annuaire Cryptographique Local', 'formFields': [{'label': 'Key Identifier Extrait (kid)', 'name': 'cose_kid', 'type': 'text', 'value': '9a8b7c6d5e4f3210 (16 octets hexadécimaux)', 'badge': '128 bits', 'required': False}, {'label': 'Emplacement TrustStore', 'name': 'truststore_storage', 'type': 'text', 'value': 'IndexedDB Chiffré Local (TrustStore v2.4 • 24 clés)', 'badge': 'Hors-Ligne', 'required': False}, {'label': 'Entité Associée', 'name': 'issuer_name', 'type': 'text', 'value': 'Le Pax Funèbre • Unité Centrale Liège (#PAX-LIEGE-01)', 'badge': 'Autorité Funéraire', 'required': False}, {'label': 'Clé Publique Ed25519 Résolue', 'name': 'pubkey_hex', 'type': 'text', 'value': 'ed25519:pub:7e8d9c0b1a2f445566778899aabbccddeeff0011', 'badge': 'Curve25519', 'required': False}], 'actionButtons': [{'id': 'btn_lookup_kid', 'label': 'Rechercher la Clé Publique dans le TrustStore Local', 'role': 'primary', 'state': 'idle', 'icon': '🔑'}, {'id': 'btn_verify_truststore_seal', 'label': "Vérifier l'Empreinte de la TrustList", 'role': 'secondary', 'state': 'idle', 'icon': '🛡️'}], 'validationMsg': {'title': 'Clé Publique Ed25519 Résolue dans le TrustStore Local', 'badge': 'Confiance Souveraine Établie', 'detail': "Identifiant 9a8b... certifié. Clé publique de l'autorité 'Le Pax Funèbre Liège' prête pour le calcul de signature."}, 'errorCase': {'code': 'ERR_TRUSTSTORE_KID_NOT_FOUND', 'title': 'Key ID Absent de la Base Locale', 'condition': 'Carte émise par un réseau tiers non synchronisé ou clé forgée.', 'message': "Le Key ID extrait ne figure pas dans le magasin de clés locales de l'application.", 'remediation': "Appliquer le bandeau d'avertissement de réserve DEC-AET-07 Option B sans bloquer l'hommage familial."}, 'phases': {'p1': {'tabTitle': '1. Avant Trigger', 'phaseTitle': 'Demande de Résolution du Key Identifier (kid)', 'caption': "L'enveloppe COSE a fourni un identifiant de 16 octets à vérifier.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • TrustStore Local</span>\n                        <span class="wf-status-badge wf-badge-neutral">kid: 9a8b7c6d...</span>\n                      </div>\n                      <div class="wf-device-status-box">\n                        <span class="wf-qa-icon">🔑</span>\n                        <div><strong>Recherche d\'Autorité Requise</strong></div>\n                        <div class="wf-subtext">Correspondance demandée dans le magasin local IndexedDB souverain</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary">🔑 Rechercher la Clé Publique dans le TrustStore Local</button>\n                      </div>\n                    </div>\n'}, 'p2': {'tabTitle': '2. Déclenchement ⚡', 'phaseTitle': 'Requête Indexée dans le Magasin In-Device', 'triggerName': "Clic sur 'Rechercher la Clé Publique'", 'caption': "Scan instantané de l'index B-Tree chiffré dans le stockage du navigateur.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Interrogation Clé</span>\n                        <span class="wf-status-badge wf-badge-trigger">⚡ Scan Index B-Tree</span>\n                      </div>\n                      <div class="wf-trigger-card wf-radar-pulse">\n                        <div class="wf-trigger-indicator">SELECT pubkey FROM truststore WHERE kid = \'9a8b7c6d5e4f3210\'</div>\n                        <div class="wf-subtext">Interrogation locale sans transmission de métadonnées vers Internet</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Recherche locale en cours...</button>\n                      </div>\n                    </div>\n'}, 'p3': {'tabTitle': '3. Traitement ⚙️', 'phaseTitle': 'Clé Publique Trouvée & Ancrée Localement', 'progress': 100, 'caption': "La clé de l'autorité 'Le Pax Funèbre Liège #01' a été identifiée en 12 ms.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Clé Confirmée</span>\n                        <span class="wf-status-badge wf-badge-process">⚙️ Correspondance (100%)</span>\n                      </div>\n                      <div class="wf-console-log">\n                        <code>> [TRUSTSTORE] kid 9a8b7c6d... -> Trouvé dans partition IndexedDB</code><br>\n                        <code>> [ISSUER] Autorité : Le Pax Funèbre - Région Wallonne (#PAX-LIEGE-01)</code><br>\n                        <code>> [ED25519] Clé publique 32 octets chargée dans SubtleCrypto</code><br>\n                        <code>> [LATENCE] Résolution achevée en 12 millisecondes</code>\n                      </div>\n                    </div>\n'}, 'p4': {'tabTitle': '4. Écran de Fin ✨', 'phaseTitle': 'Autorité Certifiée & Clé Disponible', 'status': 'success', 'caption': 'La clé publique est mise à disposition pour le calcul cryptographique final.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Confiance Établie</span>\n                        <span class="wf-status-badge wf-badge-success">✨ Émetteur Certifié</span>\n                      </div>\n                      <div class="wf-success-banner">\n                        <span class="wf-seal-icon">🏛️</span>\n                        <div>\n                          <strong>Autorité Funéraire Officielle Identifiée</strong>\n                          <p class="wf-subtext">Le Pax Funèbre Liège #01 • Clé publique Ed25519 validée</p>\n                        </div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-gold">Lancer la Vérification Mathématique de Signature →</button>\n                      </div>\n                    </div>\n'}}}},
    {'id': 'UC-319', 'title': 'Vérification Liste de Révocation Locale (CRL / Statut de Clé hors-ligne)', 'cat': 'Sécurité & Anti-Fraude', 'actor': 'Contrôleur de Révocation Cryptographique', 'platforms': ['Natif (iOS & Android)', 'Web Standard (PWA Hors-Ligne)'], 'tags': ['CRL', 'Revocation', 'KeyStatus', 'AntiFraude', 'Ed25519', 'DeltaCRL'], 'summary': "Contrôle d'absence de révocation de la clé émettrice et du numéro de série de la carte mémorielle par consultation d'un filtre Bloom de révocation scellé et mis en cache.", 'badge': 'Contrôle CRL Négatif', 'legalRef': 'RFC 5280 (X.509 CRL Profile) adapté aux environnements contraints IoT & Règlement eIDAS.', 'legal': 'RFC 5280 (X.509 CRL Profile) adapté aux environnements contraints IoT & Règlement eIDAS.', 'legal_url': '#section-legal', 'preconditions': 'Clé publique résolue et identifiant de puce extrait.', 'flow': ['Chargement du filtre Bloom de révocation optimisé (256 Ko) depuis le cache persistant.', 'Hachage SHA-256 du couple {UID_Silicium, kid_Clé}.', 'Interrogation du filtre de révocation sans fuite de métadonnées.', "Confirmation d'absence d'inscription dans la liste des cartes perdues, volées ou révoquées.", "Attribution de l'attribut d'intégrité 'Active & Non Révoquée' au contexte d'exécution."], 'postconditions': "Statut sain (Good Status) certifié ; continuation du flux d'accès au sanctuaire.", 'incident': {'code': 'ERR_KEY_REVOKED_FRAUD_DETECTED', 'title': 'Clé ou Carte Déclarée Révoquée', 'message': "L'identifiant figure sur la liste de révocation officielle (déclaration de vol ou compromission).", 'remediation': "Bloquer l'accès aux données privées et afficher l'écran d'alerte sécurité."}, 'wireframe': {'device': 'mobile', 'deviceLabel': 'Sanctuaire Mobile • Filtre Anti-Révocation In-Device', 'formFields': [{'label': 'Version CRL Locale', 'name': 'crl_version', 'type': 'text', 'value': 'CRL Delta v148 (Scellée Ed25519 au 2026-10-04)', 'badge': 'Scellée', 'required': False}, {'label': 'UID Silicium Contrôlé', 'name': 'checked_uid', 'type': 'text', 'value': '04:A2:8B:11:9C:5F:80 (JavaCard ACOSJ)', 'badge': 'UID Hardware', 'required': False}, {'label': 'Filtre Bloom de Révocation', 'name': 'bloom_status', 'type': 'text', 'value': '262 144 bits (0 match • Zéro collision détectée)', 'badge': 'Statut Sain', 'required': False}, {'label': 'Verdict de Validité', 'name': 'revocation_verdict', 'type': 'text', 'value': 'GOOD STATUS (Carte et Clé Absolument Valides)', 'badge': 'Non Révoqué', 'required': False}], 'actionButtons': [{'id': 'btn_check_revocation', 'label': "Exécuter le Contrôle d'Intégrité & Révocation Locale", 'role': 'primary', 'state': 'idle', 'icon': '🛡️'}, {'id': 'btn_crl_manifest', 'label': 'Consulter le Manifeste de Sécurité', 'role': 'secondary', 'state': 'idle', 'icon': '📜'}], 'validationMsg': {'title': 'Statut Cryptographique Vérifié : Carte Active & Non Révoquée', 'badge': 'Statut Sain / Good Status', 'detail': 'Zéro correspondance dans la table des révocations. Clé autorisée pour les 100 prochaines années.'}, 'errorCase': {'code': 'ERR_KEY_REVOKED_FRAUD_DETECTED', 'title': 'Carte Répudiée ou Clé Révoquée', 'condition': 'La carte a été déclarée volée ou annulée suite à une réémission administrative.', 'message': "ALERTE SÉCURITÉ : Ce support mémoriel a été révoqué par l'autorité émettrice.", 'remediation': 'Contacter immédiatement Le Pax Funèbre pour renouvellement de la carte physique.'}, 'phases': {'p1': {'tabTitle': '1. Avant Trigger', 'phaseTitle': 'Contrôle Préalable Anti-Répudiation', 'caption': "Vérification systématique avant d'accorder l'accès aux volontés du défunt.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Contrôle de Validité</span>\n                        <span class="wf-status-badge wf-badge-neutral">CRL Delta Prête</span>\n                      </div>\n                      <div class="wf-device-status-box">\n                        <span class="wf-qa-icon">🛡️</span>\n                        <div><strong>Vérification Anti-Révocation Requise</strong></div>\n                        <div class="wf-subtext">Filtre Bloom de 256 Ko scellé cryptographiquement en cache</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary">🛡️ Exécuter le Contrôle d\'Intégrité & Révocation Locale</button>\n                      </div>\n                    </div>\n'}, 'p2': {'tabTitle': '2. Déclenchement ⚡', 'phaseTitle': 'Hachage Double & Test des 12 Fonctions de Hachage', 'triggerName': "Clic sur 'Contrôle d'Intégrité'", 'caption': 'Calcul matriciel instantané sur le filtre Bloom sans déchiffrement lourd.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Filtre Bloom</span>\n                        <span class="wf-status-badge wf-badge-trigger">⚡ Évaluation Mathématique</span>\n                      </div>\n                      <div class="wf-trigger-card wf-radar-pulse">\n                        <div class="wf-trigger-indicator">Test k=12 fonctions de hash sur UID 04:A2:8B...</div>\n                        <div class="wf-subtext">Zéro bit positif : absence mathématiquement certaine dans la liste noire</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Évaluation instantanée...</button>\n                      </div>\n                    </div>\n'}, 'p3': {'tabTitle': '3. Traitement ⚙️', 'phaseTitle': 'Absence de Révocation Démontrée', 'progress': 100, 'caption': 'La carte et la clé sont actives et saines.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Statut Sain</span>\n                        <span class="wf-status-badge wf-badge-process">⚙️ Vérifié (100%)</span>\n                      </div>\n                      <div class="wf-console-log">\n                        <code>> [CRL-CHECK] Filtre Bloom testé : Zéro collision constatée</code><br>\n                        <code>> [STATUS] UID 04:A2:8B:11:9C:5F:80 -> Statut \'ACTIF\'</code><br>\n                        <code>> [KEY-INTEGRITY] Clé Le Pax Funèbre non compromise</code><br>\n                        <code>> [VERDICT] Autorisation d\'ouverture accordée sans restriction</code>\n                      </div>\n                    </div>\n'}, 'p4': {'tabTitle': '4. Écran de Fin ✨', 'phaseTitle': 'Passeport Mémoriel Intègre & Confirmé', 'status': 'success', 'caption': "Sécurité confirmée : aucune déclaration de vol ou d'annulation n'existe.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Intégrité Totale</span>\n                        <span class="wf-status-badge wf-badge-success">✨ Statut Garanti</span>\n                      </div>\n                      <div class="wf-success-banner">\n                        <span class="wf-seal-icon">✅</span>\n                        <div>\n                          <strong>Support Mémoriel Actif & Non Répudié</strong>\n                          <p class="wf-subtext">Vérification de révocation locale réussie • Authenticité préservée</p>\n                        </div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-gold">Accéder au Sanctuaire Mémoriel →</button>\n                      </div>\n                    </div>\n'}}}},
    {'id': 'UC-320', 'title': 'Déverrouillage AudioContext par Geste Utilisateur Conforme Politiques Navigateurs', 'cat': 'Expérience Émotionnelle & WebAudio', 'actor': 'Visiteur / Famille en Recueillement', 'platforms': ['Web Standard (PWA Safari iOS / Chrome / Firefox)', 'Natif Hybride (Capacitor/WebView)'], 'tags': ['WebAudio', 'AudioContext', 'AutoplayPolicy', 'UserGesture', 'ResumeState'], 'summary': "Gestion bienveillante et solennelle du déverrouillage de l'AudioContext WebAudio via une interaction tactile consentie, conformément aux politiques strictes de sécurité anti-autoplay des navigateurs.", 'badge': 'AudioContext Running', 'legalRef': 'W3C Web Audio API Recommendation & Apple WebKit Autoplay Policy Guidelines.', 'legal': 'W3C Web Audio API Recommendation & Apple WebKit Autoplay Policy Guidelines.', 'legal_url': '#section-legal', 'preconditions': "Page du sanctuaire ouverte dans un navigateur mobile avec AudioContext à l'état initial suspended.", 'flow': ["Présentation d'une invite visuelle solennelle et tactile (« Éveiller le Sanctuaire Sonore »).", "Capture de l'événement pointerdown/touchend direct de l'utilisateur.", 'Exécution synchrone de audioContext.resume() dans la boucle événementielle du navigateur.', "Vérification de la transition d'état vers audioContext.state === 'running'.", 'Préchauffage transparent du Master GainNode et des bus de spatialisation stéréo.'], 'postconditions': 'Moteur WebAudio opérationnel sans distorsion ni blocage audio.', 'incident': {'code': 'ERR_AUDIOCONTEXT_BLOCKED_NO_GESTURE', 'title': 'Autoplay Audio Bloqué par la Politique Navigateur', 'message': "Le moteur sonore n'a pas pu démarrer car aucun geste utilisateur explicite n'a été capturé.", 'remediation': "Toucher l'écran sur le bouton d'accueil sonore pour réveiller le moteur audio."}, 'wireframe': {'device': 'mobile', 'deviceLabel': 'Sanctuaire Mobile • Passerelle Sonore WebAudio', 'formFields': [{'label': 'État Initial WebAudio', 'name': 'audio_initial_state', 'type': 'text', 'value': 'suspended (Politique Navigateur Safari/Chrome Active)', 'badge': 'Suspendu', 'required': False}, {'label': 'Geste Utilisateur Requis', 'name': 'user_gesture_type', 'type': 'text', 'value': 'PointerEvent (touchend / click explicite sur bouton)', 'badge': 'Geste Humain', 'required': False}, {'label': "Fréquence d'Échantillonnage", 'name': 'sample_rate', 'type': 'text', 'value': '48 000 Hz (Stéréo Flottante 32 bits)', 'badge': 'Haute Définition', 'required': False}, {'label': 'Latence Audio Estimée', 'name': 'audio_latency', 'type': 'text', 'value': '12 ms (Tampon interactif ultra-court)', 'badge': 'Temps Réel', 'required': False}], 'actionButtons': [{'id': 'btn_unlock_audiocontext', 'label': '🕊️ Toucher pour Éveiller le Sanctuaire Sonore', 'role': 'primary', 'state': 'idle', 'icon': '🎵'}, {'id': 'btn_silent_sanctuary', 'label': 'Poursuivre en Silence Visuel', 'role': 'secondary', 'state': 'idle', 'icon': '🤫'}], 'validationMsg': {'title': 'AudioContext Déverrouillé avec Succès', 'badge': 'WebAudio Running (48 kHz)', 'detail': 'Conformité W3C Autoplay atteinte. Moteur acoustique et filtres de réverbération mémoriels activés.'}, 'errorCase': {'code': 'ERR_AUDIOCONTEXT_BLOCKED_NO_GESTURE', 'title': 'Verrouillage Autoplay Non Franchi', 'condition': "Tentative d'émission sonore par script sans interaction utilisateur préalable.", 'message': 'Le navigateur a bloqué la lecture sonore pour respecter la vie privée acoustique.', 'remediation': "Inviter l'utilisateur à toucher délicatement l'écran pour autoriser l'ambiance sonore."}, 'phases': {'p1': {'tabTitle': '1. Avant Trigger', 'phaseTitle': "Sanctuaire Silencieux en Attente d'Interaction", 'caption': "L'AudioContext est suspendu pour respecter les politiques Safari et Chrome.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Ambiance Sonore</span>\n                        <span class="wf-status-badge wf-badge-neutral">AudioContext Suspendu</span>\n                      </div>\n                      <div class="wf-device-status-box">\n                        <span class="wf-qa-icon">🕊️</span>\n                        <div><strong>Entrer dans l\'Espace d\'Écoute Solennel</strong></div>\n                        <div class="wf-subtext">Un simple geste réveille la nappe musicale et la voix de l\'être cher</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary">🕊️ Toucher pour Éveiller le Sanctuaire Sonore</button>\n                      </div>\n                    </div>\n'}, 'p2': {'tabTitle': '2. Déclenchement ⚡', 'phaseTitle': 'Appel Synchrone audioContext.resume()', 'triggerName': 'Geste Tactile / Clic Détecté', 'caption': "Le thread audio s'éveille immédiatement sur l'événement PointerDown.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Éveil Sonore</span>\n                        <span class="wf-status-badge wf-badge-trigger">⚡ Déverrouillage API</span>\n                      </div>\n                      <div class="wf-trigger-card wf-radar-pulse">\n                        <div class="wf-trigger-indicator">audioCtx.resume() exécuté dans le gestionnaire de clic</div>\n                        <div class="wf-subtext">Transition d\'état : suspended -> running (latence 12 ms)</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Initialisation du graphe audio...</button>\n                      </div>\n                    </div>\n'}, 'p3': {'tabTitle': '3. Traitement ⚙️', 'phaseTitle': 'Préchauffage du Graphe Audio & Master Gain', 'progress': 100, 'caption': 'Mise en place de la rampe de volume douce pour éviter tout bruit parasite.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Graphe WebAudio</span>\n                        <span class="wf-status-badge wf-badge-process">⚙️ Moteur Actif (100%)</span>\n                      </div>\n                      <div class="wf-console-log">\n                        <code>> [AUDIO-CTX] State = \'running\' (SampleRate: 48000 Hz)</code><br>\n                        <code>> [MASTER-GAIN] Gain initialisé à 0.0 -> rampe vers 1.0 en 300 ms</code><br>\n                        <code>> [SPATIAL-BUS] Réverbération à convolution mémorielle enclenchée</code><br>\n                        <code>> [AUTOPLAY-POLICY] Conforme aux normes W3C & WebKit</code>\n                      </div>\n                    </div>\n'}, 'p4': {'tabTitle': '4. Écran de Fin ✨', 'phaseTitle': 'Sanctuaire Sonore Ouvert et Apaisant', 'status': 'success', 'caption': "L'ambiance musicale résonne délicatement dans les écouteurs ou le haut-parleur.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Harmonie Sonore</span>\n                        <span class="wf-status-badge wf-badge-success">✨ Son Prêt & Fluide</span>\n                      </div>\n                      <div class="wf-success-banner">\n                        <span class="wf-seal-icon">🎵</span>\n                        <div>\n                          <strong>Espace Acoustique Ouvert</strong>\n                          <p class="wf-subtext">Ambiance musicale active • Prêt pour le mémo vocal et l\'épitaphe</p>\n                        </div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-gold">Écouter l\'Épitaphe Mémorielle →</button>\n                      </div>\n                    </div>\n'}}}},
    {'id': 'UC-321', 'title': 'Réglage Dynamique des Seuils de Ducking WebAudio (-14 dB, Attaque/Relâche)', 'cat': 'Expérience Émotionnelle', 'actor': "Proches / Famille Ajustant le Confort d'Écoute", 'platforms': ['Natif (iOS & Android)', 'Web Standard (PWA WebAudio)'], 'tags': ['Ducking', 'WebAudio', 'GainNode', 'DynamicsCompressor', 'Parametric'], 'summary': "Calibration en direct des paramètres de ducking acoustique (atténuation à -14 dB, attaque douce de 80 ms, relâche progressive de 1200 ms) pour une clarté vocale maximale de l'être cher.", 'badge': 'Ducking -14 dB Calibré', 'legalRef': 'Spécification technique AET-SPEC-AUDIO-002 & Recommandation UIT-R BS.1770-4 (mesure de sonie audio).', 'legal': 'Spécification technique AET-SPEC-AUDIO-002 & Recommandation UIT-R BS.1770-4 (mesure de sonie audio).', 'legal_url': '#section-legal', 'preconditions': 'Sanctuaire sonore actif avec piste musicale atmosphérique et mémo vocal en mémoire.', 'flow': ["Sélection du profil d'écoute (intimiste, cérémonie de groupe, personne malentendante).", "Ajustement du gain d'atténuation du bus musical (-14 dB par défaut, paramétrable de -6 à -24 dB).", "Définition de la rampe d'attaque (exponentialRampToValueAtTime à 80 ms pour éliminer tout décrochage sec).", 'Définition de la rampe de relâchement (retour progressif en 1200 ms après fin de la voix).', 'Écoute de test interactive validant la parfaite intelligibilité des fréquences vocales (1 kHz - 4 kHz).'], 'postconditions': 'Paramètres DSP injectés dans le graphe WebAudio avec transition soyeuse.', 'incident': {'code': 'ERR_AUDIO_DSP_CLIPPING', 'title': 'Saturation DSP ou Écrêtage Numérique', 'message': 'Le gain cumulé de la voix et de la musique dépasse 0 dBFS.', 'remediation': 'Activer le limiteur de crête préventif (DynamicsCompressorNode) sur le bus master.'}, 'wireframe': {'device': 'mobile', 'deviceLabel': 'Sanctuaire Mobile • Console de Sonie Mémorielle', 'formFields': [{'label': 'Niveau de Ducking Musical', 'name': 'ducking_level', 'type': 'text', 'value': '-14.0 dB (Atténuation douce de la nappe musicale)', 'badge': '-14 dB', 'required': False}, {'label': "Constante de Temps d'Attaque", 'name': 'attack_time', 'type': 'text', 'value': '80 millisecondes (Courbe exponentielle sans clic)', 'badge': '80 ms', 'required': False}, {'label': 'Constante de Temps de Relâche', 'name': 'release_time', 'type': 'text', 'value': '1 200 millisecondes (Retour solennel progressif)', 'badge': '1.2 s', 'required': False}, {'label': "Détecteur d'Activité Vocale (VAD)", 'name': 'vad_threshold', 'type': 'text', 'value': '-28 dBFS (Détection immédiate des syllabes douces)', 'badge': 'VAD Actif', 'required': False}], 'actionButtons': [{'id': 'btn_apply_ducking_params', 'label': 'Appliquer les Paramètres de Ducking Acoustique', 'role': 'primary', 'state': 'idle', 'icon': '🎚️'}, {'id': 'btn_test_audio_ducking', 'label': "Tester l'Atténuation avec Simulation Vocale", 'role': 'secondary', 'state': 'idle', 'icon': '🎧'}], 'validationMsg': {'title': 'Paramètres de Ducking Acoustique Appliqués', 'badge': 'Intelligibilité Vocale Maximale', 'detail': "Courbe d'atténuation programmée sur le GainNode. Rapport voix/musique optimisé (+14 dB pour la parole)."}, 'errorCase': {'code': 'ERR_AUDIO_DSP_CLIPPING', 'title': "Risque d'Écrêtage DSP", 'condition': 'Volume de voix brut trop élevé causant une distorsion numérique sur le bus master.', 'message': "Le signal combiné atteint le seuil d'écrêtage (+0.8 dBFS).", 'remediation': 'Engager automatiquement le limiteur brickwall et abaisser le pré-gain vocal de -3 dB.'}, 'phases': {'p1': {'tabTitle': '1. Avant Trigger', 'phaseTitle': 'Console de Réglage des Niveaux Sonores', 'caption': 'Paramètres standard appliqués : -14 dB pour la nappe sous la voix.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Confort Acoustique</span>\n                        <span class="wf-status-badge wf-badge-neutral">Profil Standard (-14 dB)</span>\n                      </div>\n                      <div class="wf-device-status-box">\n                        <span class="wf-qa-icon">🎚️</span>\n                        <div><strong>Équilibrage Voix / Nappe Atmosphérique</strong></div>\n                        <div class="wf-subtext">Adapté aux oreilles sensibles et aux environnements calmes</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary">🎚️ Appliquer les Paramètres de Ducking Acoustique</button>\n                      </div>\n                    </div>\n'}, 'p2': {'tabTitle': '2. Déclenchement ⚡', 'phaseTitle': 'Programmation des Rampes Audio Paramétriques', 'triggerName': 'Validation des Nouveaux Seuils', 'caption': "Les valeurs de transition sont envoyées à l'AudioParam de l'API WebAudio.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Injection DSP</span>\n                        <span class="wf-status-badge wf-badge-trigger">⚡ Courbes Exponentielles</span>\n                      </div>\n                      <div class="wf-trigger-card wf-radar-pulse">\n                        <div class="wf-trigger-indicator">gainNode.gain.exponentialRampToValueAtTime(0.2, now + 0.08)</div>\n                        <div class="wf-subtext">Descente de 0 dB à -14 dB en 80 ms, relâchement en 1 200 ms</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Application aux filtres...</button>\n                      </div>\n                    </div>\n'}, 'p3': {'tabTitle': '3. Traitement ⚙️', 'phaseTitle': 'Simulation Vocale & Contrôle de Clarté', 'progress': 100, 'caption': "Vérification en temps réel de l'absence de claquement ou de coupure brusque.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Écoute Contrôlée</span>\n                        <span class="wf-status-badge wf-badge-process">⚙️ DSP Stabilisé (100%)</span>\n                      </div>\n                      <div class="wf-console-log">\n                        <code>> [DUCKING-DSP] Atténuation -14 dB validée sur canal musical</code><br>\n                        <code>> [INTELLIGIBILITÉ] Indice STI estimé : 0.88 (Excellent)</code><br>\n                        <code>> [RAMPE-ATTAQUE] 80 ms sans discontinuité de phase</code><br>\n                        <code>> [DYNAMICS] Compresseur limiteur calé à -0.3 dBFS de sécurité</code>\n                      </div>\n                    </div>\n'}, 'p4': {'tabTitle': '4. Écran de Fin ✨', 'phaseTitle': "Confort d'Écoute Parfait pour les Proches", 'status': 'success', 'caption': "La voix de l'être cher se détache avec une clarté émouvante et respectueuse.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Acoustique Maîtrisée</span>\n                        <span class="wf-status-badge wf-badge-success">✨ Sonie Optimale</span>\n                      </div>\n                      <div class="wf-success-banner">\n                        <span class="wf-seal-icon">🎧</span>\n                        <div>\n                          <strong>Ducking Vocal Calibré</strong>\n                          <p class="wf-subtext">Écoute cristalline • Harmonie parfaite entre souvenirs et musique</p>\n                        </div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-gold">Écouter le Message Vocal d\'Origine →</button>\n                      </div>\n                    </div>\n'}}}},
    {'id': 'UC-322', 'title': "Synthèse Vocale Text-To-Speech Multilingue de l'Épitaphe Mémorielle", 'cat': 'Accessibilité & Expérience Mémorielle', 'actor': 'Famille, Malvoyants, Personnes Âgées', 'platforms': ['Web Speech API (SpeechSynthesis)', 'Natif (AVSpeechSynthesizer / Android TTS)'], 'tags': ['TTS', 'SyntheseVocale', 'Accessibilite', 'WebSpeech', 'Multilingue'], 'summary': "Vocalisation haute fidélité solennelle de l'épitaphe et du testament moral par synthèse vocale in-device multilingue, offrant un accès universel sans écran aux aînés et malvoyants.", 'badge': 'TTS Mémoriel 0.85x', 'legalRef': "Directive européenne sur l'accessibilité (Directive UE 2019/882) & WCAG 2.2 Niveau AAA.", 'legal': "Directive européenne sur l'accessibilité (Directive UE 2019/882) & WCAG 2.2 Niveau AAA.", 'legal_url': '#section-legal', 'preconditions': 'Épitaphe textuelle chargée depuis la puce ou la capsule mémorielle.', 'flow': ["Sélection automatique de la voix locale haute définition correspondant à la langue de l'épitaphe (fr-BE, nl-BE, de-DE, en-GB).", 'Calibrage solennel du débit (rate: 0.85x) et de la hauteur tonale (pitch: 0.95) pour une élocution digne et chaleureuse.', "Envoi du texte balisé au moteur SpeechSynthesis du système d'exploitation.", "Atténuation synchrone de la musique d'ambiance en arrière-plan via le bus de ducking.", 'Notification visuelle avec mise en surbrillance karaoké bienveillante mot à mot pour les personnes âgées.'], 'postconditions': 'Message moral entendu dans un silence respectueux, transcription accessible validée.', 'incident': {'code': 'ERR_TTS_SYNTHESIS_VOICE_UNAVAILABLE', 'title': 'Voix Synthétique Hors-Ligne Absente', 'message': "Aucune voix haute fidélité n'est installée localement pour la langue requise.", 'remediation': 'Basculer sur la synthèse par défaut du système ou inviter à la lecture visuelle agrandie.'}, 'wireframe': {'device': 'mobile', 'deviceLabel': 'Sanctuaire Mobile • Voix Mémorielle Universelle', 'formFields': [{'label': 'Moteur TTS Système', 'name': 'tts_engine', 'type': 'text', 'value': 'SpeechSynthesis API Native (In-Device / Hors-Ligne)', 'badge': 'Local & Privé', 'required': False}, {'label': 'Langue & Voix Solennelle', 'name': 'tts_voice', 'type': 'text', 'value': 'fr-BE (Français Belgique • Voix Chaleureuse & Posée)', 'badge': 'fr-BE', 'required': False}, {'label': "Cadence d'Élocution", 'name': 'speech_rate', 'type': 'text', 'value': '0.85x (Tempo ralenti propice au recueillement)', 'badge': 'Solennel', 'required': False}, {'label': "Extrait d'Épitaphe Mémorielle", 'name': 'epitaph_preview', 'type': 'text', 'value': '« Ne pleurez pas mon départ, contemplez les arbres où je vis désormais. »', 'badge': 'Testament Moral', 'required': False}], 'actionButtons': [{'id': 'btn_play_tts_epitaph', 'label': "🕊️ Faire Résonner l'Épitaphe à Voix Haute", 'role': 'primary', 'state': 'idle', 'icon': '🔊'}, {'id': 'btn_stop_tts', 'label': 'Mettre en Pause la Lecture Solennelle', 'role': 'secondary', 'state': 'idle', 'icon': '⏸️'}], 'validationMsg': {'title': 'Lecture Vocale Solennelle Engagée', 'badge': 'Synthèse Phonétique Active', 'detail': 'Élocution posée à 0.85x en cours. Ducking automatique appliqué à la nappe sonore.'}, 'errorCase': {'code': 'ERR_TTS_SYNTHESIS_VOICE_UNAVAILABLE', 'title': 'Pack de Langue Synthétique Introuvable', 'condition': "Système d'exploitation sans pack de synthèse vocale pour la langue cible.", 'message': "Impossible d'initialiser la voix haute fidélité demandée.", 'remediation': "Utiliser la voix générique intégrée ou activer le mode d'affichage gros caractères pour malvoyants."}, 'phases': {'p1': {'tabTitle': '1. Avant Trigger', 'phaseTitle': "Texte de l'Épitaphe Prêt pour la Voix", 'caption': "Les derniers mots du défunt sont affichés avec l'option de lecture vocale.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Testament Moral</span>\n                        <span class="wf-status-badge wf-badge-neutral">Accessibilité Active</span>\n                      </div>\n                      <div class="wf-device-status-box">\n                        <span class="wf-qa-icon">🔊</span>\n                        <div><strong>Vocalisation de l\'Épitaphe Mémorielle</strong></div>\n                        <div class="wf-subtext">Synthèse vocale douce à 0.85x pour aînés et recueillement les yeux clos</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary">🕊️ Faire Résonner l\'Épitaphe à Voix Haute</button>\n                      </div>\n                    </div>\n'}, 'p2': {'tabTitle': '2. Déclenchement ⚡', 'phaseTitle': 'Instanciation SpeechSynthesisUtterance', 'triggerName': "Clic sur 'Faire Résonner l'Épitaphe'", 'caption': "Le moteur vocal s'apprête à prononcer la phrase avec le débit solennel.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Synthèse Vocale</span>\n                        <span class="wf-status-badge wf-badge-trigger">⚡ Émission Phonétique</span>\n                      </div>\n                      <div class="wf-trigger-card wf-radar-pulse">\n                        <div class="wf-trigger-indicator">window.speechSynthesis.speak(utterance) • Voix fr-BE</div>\n                        <div class="wf-subtext">Activation synchrone de l\'atténuation musicale (-14 dB)</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Élocution en cours...</button>\n                      </div>\n                    </div>\n'}, 'p3': {'tabTitle': '3. Traitement ⚙️', 'phaseTitle': 'Lecture en Cours & Défilement Bienveillant', 'progress': 65, 'caption': 'Les mots résonnent dans le silence avec accompagnement visuel adapté.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Parole Active</span>\n                        <span class="wf-status-badge wf-badge-process">⚙️ Vocalisation (65%)</span>\n                      </div>\n                      <div class="wf-console-log">\n                        <code>> [TTS-ENGINE] Voix locale haute fidélité active (fr-BE)</code><br>\n                        <code>> [SPEECH] « ...contemplez les arbres où je vis désormais. »</code><br>\n                        <code>> [DUCKING] Musique d\'ambiance maintenue à -14 dB</code><br>\n                        <code>> [ACCESSIBILITÉ] Conformité WCAG 2.2 AAA respectée</code>\n                      </div>\n                    </div>\n'}, 'p4': {'tabTitle': '4. Écran de Fin ✨', 'phaseTitle': 'Parole Conclue dans la Sérénité', 'status': 'success', 'caption': 'La nappe musicale retrouve doucement son volume initial.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Paix Retrouvée</span>\n                        <span class="wf-status-badge wf-badge-success">✨ Message Entendu</span>\n                      </div>\n                      <div class="wf-success-banner">\n                        <span class="wf-seal-icon">🕊️</span>\n                        <div>\n                          <strong>Dernières Paroles Résonnées avec Dignité</strong>\n                          <p class="wf-subtext">Recueillement achevé • Retour feutré de la nappe musicale</p>\n                        </div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-gold">Signer le Livre d\'Or Mémoriel →</button>\n                      </div>\n                    </div>\n'}}}},
    {'id': 'UC-323', 'title': "Signature Cryptographique Décentralisée d'un Message du Livre d'Or", 'cat': 'Expérience Sanctuaire & Cryptographie', 'actor': 'Proche ou Membre de la Famille Laissant un Témoignage', 'platforms': ['Natif (iOS & Android)', 'Web Standard (PWA WebCrypto)'], 'tags': ['LivreDor', 'SignatureCryptographique', 'Ed25519', 'WebCrypto', 'P2P', 'Pollen'], 'summary': "Création d'un témoignage mémoriel inaltérable scellé par une clé de signature Ed25519 locale (Pollen P2P), assurant l'authenticité et l'horodatage décentralisé du message sans serveur central.", 'badge': 'Pollen P2P Scellé Ed25519', 'legalRef': 'Règlement eIDAS (signatures électroniques avancées) & Spécification P2P Pollen AeterniTrak.', 'legal': 'Règlement eIDAS (signatures électroniques avancées) & Spécification P2P Pollen AeterniTrak.', 'legal_url': '#section-legal', 'preconditions': "Proche connecté au sanctuaire local via NFC ou PWA et rédigeant un mot d'adieu.", 'flow': ["Saisie de l'hommage et du nom du proche dans le formulaire du Livre d'Or.", "Génération ou récupération de la paire de clés Ed25519 in-device de l'auteur.", 'Canonisation JSON du message (RFC 8785 JCS - JSON Canonicalization Scheme).', "Signature cryptographique Ed25519 de l'empreinte SHA-256 via SubtleCrypto (14 ms).", 'Encapsulation dans un Pollen P2P réplicable en Bluetooth LE ou synchronisable lors du retour en réseau.'], 'postconditions': 'Message scellé et certifié inaltérable pour les siècles à venir dans la mémoire distribuée.', 'incident': {'code': 'ERR_GUESTBOOK_PAYLOAD_TOO_LARGE', 'title': 'Volume du Témoignage Excédentaire', 'message': 'Le texte ou les pièces jointes dépassent la capacité allouée pour la réplication P2P contrainte.', 'remediation': 'Réduire la longueur du message à moins de 2 000 caractères ou compresser les photos jointes.'}, 'wireframe': {'device': 'mobile', 'deviceLabel': "Sanctuaire Mobile • Sceau Décentralisé du Livre d'Or", 'formFields': [{'label': 'Auteur du Témoignage', 'name': 'author_identity', 'type': 'text', 'value': 'Camille de Valcourt (Filleule & Famille)', 'badge': 'Identité Vérifiée', 'required': True}, {'label': 'Hommage Mémoriel', 'name': 'testimony_body', 'type': 'text', 'value': '« Merci pour ta bonté infinie et pour tout ce que tu nous as transmis sous ces grands chênes. »', 'badge': 'Texte Scellé', 'required': True}, {'label': 'Moteur Cryptographique', 'name': 'guestbook_crypto', 'type': 'text', 'value': 'SubtleCrypto Ed25519 (Courbe Curve25519 • JCS Canonisation)', 'badge': 'Ed25519', 'required': False}, {'label': 'Empreinte SHA-256 du Témoignage', 'name': 'payload_hash', 'type': 'text', 'value': 'SHA-256: d4f3a18e9c0b2f5a6b7c8d9e0f1a2b3c...', 'badge': 'Inaltérable', 'required': False}], 'actionButtons': [{'id': 'btn_sign_guestbook_entry', 'label': "Sceller & Signer l'Hommage Cryptographique", 'role': 'primary', 'state': 'idle', 'icon': '✍️'}, {'id': 'btn_preview_guestbook_pollen', 'label': 'Prévisualiser le Paquet Pollen P2P', 'role': 'secondary', 'state': 'idle', 'icon': '📦'}], 'validationMsg': {'title': 'Hommage Mémoriel Cryptographiquement Scellé', 'badge': 'Signature Ed25519 Valide', 'detail': 'Pollen P2P généré en 14 ms. Intégrité et provenance inaltérables garanties sans autorité centrale.'}, 'errorCase': {'code': 'ERR_GUESTBOOK_PAYLOAD_TOO_LARGE', 'title': 'Message Trop Volumineux pour Silicium/P2P', 'condition': "Dépassement du quota de 2 Ko par entrée de livre d'or hors-ligne.", 'message': 'La charge utile dépasse la limite permise pour la réplication sans contact.', 'remediation': "Condenser le texte de l'hommage à l'essentiel pour préserver le stockage solennel."}, 'phases': {'p1': {'tabTitle': '1. Avant Trigger', 'phaseTitle': "Rédaction de l'Hommage Familial", 'caption': "Le témoignage d'affection est rédigé avec émotion par le proche.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Livre d\'Or</span>\n                        <span class="wf-status-badge wf-badge-neutral">Témoignage Rédigé</span>\n                      </div>\n                      <div class="wf-device-status-box">\n                        <span class="wf-qa-icon">✍️</span>\n                        <div><strong>Scellement Inaltérable Souhaité</strong></div>\n                        <div class="wf-subtext">Signature mathématique Ed25519 garantissant l\'intégrité séculaire</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary">✍️ Sceller & Signer l\'Hommage Cryptographique</button>\n                      </div>\n                    </div>\n'}, 'p2': {'tabTitle': '2. Déclenchement ⚡', 'phaseTitle': 'Canonisation JSON & Signature RFC 8032', 'triggerName': "Clic sur 'Sceller & Signer'", 'caption': 'Calcul local de la signature sans envoyer le moindre mot sur Internet.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Signature P2P</span>\n                        <span class="wf-status-badge wf-badge-trigger">⚡ SubtleCrypto.sign()</span>\n                      </div>\n                      <div class="wf-trigger-card wf-radar-pulse">\n                        <div class="wf-trigger-indicator">JCS RFC 8785 -> SHA-256 -> Signature Ed25519 (64 octets)</div>\n                        <div class="wf-subtext">Clé d\'auteur locale in-device • Horodatage cryptographique certifié</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Scellement en cours...</button>\n                      </div>\n                    </div>\n'}, 'p3': {'tabTitle': '3. Traitement ⚙️', 'phaseTitle': 'Génération du Paquet Pollen Distribué', 'progress': 100, 'caption': 'Le message devient une assertion cryptographique autonome.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Pollen Mémoriel</span>\n                        <span class="wf-status-badge wf-badge-process">⚙️ Paquet Prêt (100%)</span>\n                      </div>\n                      <div class="wf-console-log">\n                        <code>> [CRYPTO-SIGN] Ed25519 signature calculée en 14 ms</code><br>\n                        <code>> [POLLEN-CID] CID IPFS/P2P : bafybeigdyrzt5sfp7udm...</code><br>\n                        <code>> [REPLICATION] Prêt pour diffusion mesh BLE / Carte mémorielle</code><br>\n                        <code>> [CONFIDENTIALITÉ] Respect strict de la vie privée familiale</code>\n                      </div>\n                    </div>\n'}, 'p4': {'tabTitle': '4. Écran de Fin ✨', 'phaseTitle': 'Témoignage Gravé dans la Mémoire Éternelle', 'status': 'success', 'caption': 'Le souvenir est protégé contre toute altération ou suppression future.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Hommage Préservé</span>\n                        <span class="wf-status-badge wf-badge-success">✨ Scellé pour l\'Éternité</span>\n                      </div>\n                      <div class="wf-success-banner">\n                        <span class="wf-seal-icon">📜</span>\n                        <div>\n                          <strong>Hommage Enregistré avec Succès</strong>\n                          <p class="wf-subtext">Signature Ed25519 vérifiée • Témoignage associé au sanctuaire</p>\n                        </div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-gold">Voir le Livre d\'Or Complété →</button>\n                      </div>\n                    </div>\n'}}}},
    {'id': 'UC-324', 'title': "Export Fiche d'Urgence Médicale Pacemaker au Format PDF/A Conforme", 'cat': 'Directives Médicales & Sécurité', 'actor': 'Médecin Urgentiste, Thanatopracteur, Conseiller Funéraire', 'platforms': ['Natif (iOS & Android)', 'Web Standard (PWA Générateur PDF/A)'], 'tags': ['Pacemaker', 'PDF-A', 'UrgenceMedicale', 'SecuriteIncendie', 'ArtL1232-24'], 'summary': "Génération instantanée et conforme de la fiche d'urgence réglementaire Modèle IIIC selon l'Art. L1232-24 CDLD certifiant la présence/exérèse d'un stimulateur cardiaque pour la sécurité du crématorium ou bioréacteur.", 'badge': 'Modèle IIIC CDLD Conforme', 'legalRef': 'Art. L1232-24 CDLD & Modèle IIIC réglementaire & Norme ISO 19005-1 (PDF/A).', 'legal': 'Art. L1232-24 CDLD & Modèle IIIC réglementaire & Norme ISO 19005-1 (PDF/A).', 'legal_url': '#section-legal', 'preconditions': "Données médicales d'urgence lues depuis la partition EF4 de la carte mémorielle.", 'flow': ["Détection in-silico de l'alerte vitale : Présence d'un stimulateur cardiaque actif.", 'Extraction des références techniques du dispositif (Medtronic Viva XT S/N 84920).', 'Compilation selon le modèle officiel wallon Annexe IIIC (Art. L1232-24 CDLD).', 'Génération in-browser du document au format PDF/A-1b (archivage pérenne ISO 19005-1 avec métadonnées XMP).', "Mise à disposition pour signature de l'exérèse chirurgicale par le praticien habilité."], 'postconditions': "Fiche PDF/A générée, prête pour certification de l'exérèse et archivage légal.", 'incident': {'code': 'ERR_PDF_GENERATION_FAILED', 'title': "Erreur d'Assemblage du Document PDF/A", 'message': 'Échec de génération du binaire PDF/A ou non-conformité des profils colorimétriques sRGB.', 'remediation': "Réessayer l'export ou utiliser l'impression système standardisée."}, 'wireframe': {'device': 'mobile', 'deviceLabel': 'Sanctuaire Mobile • Export Réglementaire Modèle IIIC', 'formFields': [{'label': 'Dispositif Médical Implanté', 'name': 'implant_type', 'type': 'text', 'value': 'Stimulateur Cardiaque Actif (Medtronic Viva XT S/N 84920)', 'badge': 'ALERTE VITALE', 'required': False}, {'label': 'Cadre Juridique Wallon', 'name': 'legal_framework', 'type': 'text', 'value': 'Art. L1232-24 CDLD & Modèle IIIC réglementaire', 'badge': 'Obligatoire', 'required': False}, {'label': 'Risque Sanitaire / Explosion', 'name': 'hazard_level', 'type': 'text', 'value': 'Risque Majeur Déflagration en Incinérateur / Traitement Thermique', 'badge': 'Danger Incendie', 'required': False}, {'label': "Norme d'Archivage Documentaire", 'name': 'pdf_standard', 'type': 'text', 'value': 'PDF/A-1b Conforme ISO 19005-1 (Profil Colorimétrique sRGB & XMP)', 'badge': 'Pérenne ISO', 'required': False}], 'actionButtons': [{'id': 'btn_export_pacemaker_pdfa', 'label': 'Générer le Document Officiel PDF/A Conforme', 'role': 'primary', 'state': 'idle', 'icon': '📄'}, {'id': 'btn_print_emergency_sheet', 'label': 'Impression Directe Fiche IIIC', 'role': 'secondary', 'state': 'idle', 'icon': '🖨️'}], 'validationMsg': {'title': 'Document Réglementaire PDF/A Modèle IIIC Généré', 'badge': 'Art. L1232-24 CDLD Certifié', 'detail': 'Fiche officielle prête pour transmission immédiate au médecin légiste ou thanatopracteur pour exérèse.'}, 'errorCase': {'code': 'ERR_PDF_GENERATION_FAILED', 'title': 'Échec de Compilation PDF/A', 'condition': 'Ressource de police ou profil ICC manquant dans le générateur in-browser.', 'message': 'Impossible de certifier le document selon le standard ISO PDF/A.', 'remediation': 'Basculer en mode affichage direct HTML pour impression papier immédiate.'}, 'phases': {'p1': {'tabTitle': '1. Avant Trigger', 'phaseTitle': 'Alerte Dispositif Implantable Détectée', 'caption': "Présence confirmée d'un stimulateur cardiaque nécessitant attestation d'exérèse.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Sécurité Médicale</span>\n                        <span class="wf-status-badge wf-badge-neutral">Alerte Pacemaker Active</span>\n                      </div>\n                      <div class="wf-device-status-box">\n                        <span class="wf-qa-icon">⚠️</span>\n                        <div><strong>Attestation d\'Exérèse Réglementaire Obligatoire</strong></div>\n                        <div class="wf-subtext">Art. L1232-24 CDLD & Modèle IIIC réglementaire avant crémation / bioconversion</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary">📄 Générer le Document Officiel PDF/A Conforme</button>\n                      </div>\n                    </div>\n'}, 'p2': {'tabTitle': '2. Déclenchement ⚡', 'phaseTitle': 'Compilation des Métadonnées Conformes ISO 19005-1', 'triggerName': "Clic sur 'Générer Document Officiel'", 'caption': 'Création du fichier PDF/A-1b pérenne avec inclusion des polices vectorielles.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Compilateur PDF/A</span>\n                        <span class="wf-status-badge wf-badge-trigger">⚡ Binaire ISO 19005-1</span>\n                      </div>\n                      <div class="wf-trigger-card wf-radar-pulse">\n                        <div class="wf-trigger-indicator">pdfmake / jsPDF : Injection schéma XMP pdfaExtension</div>\n                        <div class="wf-subtext">Intégration du numéro de série Medtronic S/N 84920 et visa civil</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Compilation PDF/A en cours...</button>\n                      </div>\n                    </div>\n'}, 'p3': {'tabTitle': '3. Traitement ⚙️', 'phaseTitle': 'Vérification de Conformité Normative', 'progress': 100, 'caption': "Validation de l'absence de balises dynamiques interdites par la norme PDF/A.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Contrôle Qualité PDF</span>\n                        <span class="wf-status-badge wf-badge-process">⚙️ PDF/A Certifié (100%)</span>\n                      </div>\n                      <div class="wf-console-log">\n                        <code>> [PDF-A] Profil PDF/A-1b validé sans balise JavaScript externe</code><br>\n                        <code>> [XMP] Métadonnées réglementaires : Modèle IIIC Wallonie</code><br>\n                        <code>> [DISPOSITIF] Pacemaker Medtronic Viva XT consigné pour exérèse</code><br>\n                        <code>> [ARCHIVE] Document prêt pour conservation légale de 30 ans</code>\n                      </div>\n                    </div>\n'}, 'p4': {'tabTitle': '4. Écran de Fin ✨', 'phaseTitle': 'Document Prêt pour Remise aux Autorités', 'status': 'success', 'caption': 'Le document officiel peut être imprimé ou transmis pour la levée de corps.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Fiche Officielle Prête</span>\n                        <span class="wf-status-badge wf-badge-success">✨ Modèle IIIC Conforme</span>\n                      </div>\n                      <div class="wf-success-banner">\n                        <span class="wf-seal-icon">🩺</span>\n                        <div>\n                          <strong>Fiche Réglementaire Générée</strong>\n                          <p class="wf-subtext">Art. L1232-24 CDLD • Conforme pour signature thanatopracteur</p>\n                        </div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-gold">Télécharger / Partager le PDF/A Officiel →</button>\n                      </div>\n                    </div>\n'}}}},
    {'id': 'UC-325', 'title': "Calcul d'Itinéraire Géodésique & Boussole vers l'Arbre du Souvenir (Formule de Haversine)", 'cat': 'Guidage & Forêt Mémorielle', 'actor': 'Famille en Déplacement dans la Forêt Cinéraire DNF', 'platforms': ['Natif (iOS CoreLocation & Android Location)', 'Web Geolocation API & DeviceOrientation'], 'tags': ['Geodesie', 'Haversine', 'Boussole', 'GPS', 'ForetCineraire', 'ArbreDuSouvenir'], 'summary': "Calcul trigonométrique local par la formule de Haversine et orientation boussole en temps réel pour guider les proches jusqu'à l'Arbre du Souvenir au cœur d'un massif forestier DNF sans connexion 4G/5G.", 'badge': 'Guidage Haversine Hors-Ligne', 'legalRef': 'Convention domaniale DNF / Le Pax Funèbre pour la préservation des massifs forestiers classés.', 'legal': 'Convention domaniale DNF / Le Pax Funèbre pour la préservation des massifs forestiers classés.', 'legal_url': '#section-legal', 'preconditions': "Coordonnées GPS de l'Arbre du Souvenir lues sur la carte et capteurs GPS/magnétomètre du smartphone actifs.", 'flow': ['Lecture des coordonnées géodésiques de la sépulture mémorielle (50.4182° N, 5.8821° E).', 'Acquisition de la position GPS courante du visiteur sous la canopée forestière.', 'Calcul de la distance grand-cercle par la formule mathématique de Haversine (précision métrique in-device).', "Calcul de l'azimut (bearing) géodésique et couplage avec le capteur magnétique (boussole).", "Affichage d'une aiguille de boussole solennelle orientant le regard directement vers le chêne séculaire."], 'postconditions': "Visiteur guidé avec sérénité jusqu'au pied de l'arbre cinéraire sans signalétique physique invasive.", 'incident': {'code': 'ERR_GPS_SIGNAL_WEAK_CANOPY', 'title': 'Signal Satellite Dégradé sous Canopée', 'message': 'La densité du feuillage atténue le signal GPS au-delà du seuil de tolérance (précision > 25 m).', 'remediation': "S'avancer vers une clairière ou utiliser le plan topographique hors-ligne avec repères de sentier."}, 'wireframe': {'device': 'mobile', 'deviceLabel': 'Sanctuaire Mobile • Boussole Mémorielle Forestière', 'formFields': [{'label': 'Coordonnées Arbre du Souvenir', 'name': 'tree_gps', 'type': 'text', 'value': '50.4182° N, 5.8821° E (Chêne Séculaire #PARC-DNF-42)', 'badge': 'Arbre Scellé', 'required': False}, {'label': 'Position Visiteur en Forêt', 'name': 'user_gps', 'type': 'text', 'value': '50.4170° N, 5.8805° E (Précision : ± 2.8 mètres)', 'badge': 'GPS Fix OK', 'required': False}, {'label': 'Distance Calculée (Haversine)', 'name': 'haversine_dist', 'type': 'text', 'value': "174 mètres à vol d'oiseau (Formule R·c sur sphère WGS84)", 'badge': '174 m', 'required': False}, {'label': 'Cap & Azimut Magnétique', 'name': 'compass_azimuth', 'type': 'text', 'value': '38° Nord-Nord-Est (Aiguille gyroscopique fluide)', 'badge': '38° NNE', 'required': False}], 'actionButtons': [{'id': 'btn_calc_haversine_route', 'label': 'Calculer le Cap Géodésique & Activer la Boussole', 'role': 'primary', 'state': 'idle', 'icon': '🧭'}, {'id': 'btn_calibrate_compass', 'label': 'Étalonner le Capteur Magnétique', 'role': 'secondary', 'state': 'idle', 'icon': '🔄'}], 'validationMsg': {'title': "Guidage Géodésique Actif vers l'Arbre du Souvenir", 'badge': 'Boussole Forestière Précise', 'detail': 'Distance : 174 mètres • Azimut : 38° NNE. Aiguille orientée vers le chêne de recueillement.'}, 'errorCase': {'code': 'ERR_GPS_SIGNAL_WEAK_CANOPY', 'title': 'Précision GPS Insuffisante sous Canopée', 'condition': 'Feuillage dense et humidité réduisant la visibilité des constellations GNSS.', 'message': 'Précision géodésique dégradée (> 30 mètres).', 'remediation': "Suivre le sentier balisé DNF jusqu'à la borne cinéraire physique #B-42."}, 'phases': {'p1': {'tabTitle': '1. Avant Trigger', 'phaseTitle': 'Entrée dans le Massif Forestier DNF', 'caption': "La famille est en lisière de forêt et recherche l'arbre mémoriel.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Forêt Cinéraire</span>\n                        <span class="wf-status-badge wf-badge-neutral">Arbre #42 Enregistré</span>\n                      </div>\n                      <div class="wf-device-status-box">\n                        <span class="wf-qa-icon">🌲</span>\n                        <div><strong>Orientation vers l\'Arbre du Souvenir</strong></div>\n                        <div class="wf-subtext">Calcul trigonométrique Haversine 100% hors-ligne dans le smartphone</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary">🧭 Calculer le Cap Géodésique & Activer la Boussole</button>\n                      </div>\n                    </div>\n'}, 'p2': {'tabTitle': '2. Déclenchement ⚡', 'phaseTitle': 'Calcul de la Formule de Haversine & Azimut', 'triggerName': "Clic sur 'Calculer le Cap'", 'caption': 'Résolution des coordonnées sphériques WGS84 dans le microprocesseur.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Géodésie Locale</span>\n                        <span class="wf-status-badge wf-badge-trigger">⚡ Trigonométrie Sphérique</span>\n                      </div>\n                      <div class="wf-trigger-card wf-radar-pulse">\n                        <div class="wf-trigger-indicator">a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2) -> d = 174 m</div>\n                        <div class="wf-subtext">Calcul du bearing initial θ = atan2(sin Δλ ⋅ cos φ2, ...) = 38°</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Alignement gyroscopique...</button>\n                      </div>\n                    </div>\n'}, 'p3': {'tabTitle': '3. Traitement ⚙️', 'phaseTitle': 'Couplage Gyroscope & Boussole Magnétique', 'progress': 100, 'caption': 'Aiguille mémorielle stabilisée pointant vers le chêne cinéraire.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Capteur d\'Orientation</span>\n                        <span class="wf-status-badge wf-badge-process">⚙️ Cap Verrouillé (38° NNE)</span>\n                      </div>\n                      <div class="wf-console-log">\n                        <code>> [HAVERSINE] Distance calculée : 174.2 mètres</code><br>\n                        <code>> [BEARING] Azimut géographique : 38.4° NNE</code><br>\n                        <code>> [COMPASS] DeviceOrientation actif (précision ±1.5°)</code><br>\n                        <code>> [OFFLINE-GEO] Zéro transfert de position géographique vers l\'extérieur</code>\n                      </div>\n                    </div>\n'}, 'p4': {'tabTitle': '4. Écran de Fin ✨', 'phaseTitle': 'Boussole Active & Arbre en Vue', 'status': 'success', 'caption': "Le recueillement s'opère dans la paix des grands arbres séculaires.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">Sanctuaire • Arbre Atteint</span>\n                        <span class="wf-status-badge wf-badge-success">✨ Destination en Vue</span>\n                      </div>\n                      <div class="wf-success-banner">\n                        <span class="wf-seal-icon">🍃</span>\n                        <div>\n                          <strong>Chêne du Souvenir Localisé</strong>\n                          <p class="wf-subtext">Parcelle DNF 104/A • Vous êtes au pied de l\'Arbre mémoriel</p>\n                        </div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-gold">Ouvrir le Sanctuaire au Pied de l\'Arbre →</button>\n                      </div>\n                    </div>\n'}}}}
]
