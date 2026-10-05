#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeterniTrak V1.0 — Définition Complète des Micro Use-Cases pour App 3 : Sanctuaire Mémoriel Mobile (UC-301 à UC-312)
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
        "title": "Affichage Sanctuaire Certifié en Recueillement Nominal",
        "cat": "Expérience Sanctuaire",
        "actor": "Famille & Proches",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["Sanctuaire", "Recueillement", "PortraitHD", "Epitaphe", "Design"],
        "preconditions": "Carte authentifiée par la vérification cryptographique.",
        "flow": [
            "Affichage solennel du portrait haute définition du défunt au centre d'un halo doré doux.",
            "Présentation des dates de vie, de l'épitaphe personnalisée et du carrousel de portraits familiaux.",
            "Lancement automatique de la musique d'adieu sélectionnée (In Paradisum de Fauré) en fondu d'entrée doux (fade-in 2s).",
            "Bouton d'accès solennel au témoignage vocal gravé in-silico.",
            "Disponibilité immédiate en mode 100% hors-ligne (fonctionne en pleine forêt, au cimetière ou en salon familial privé)."
        ],
        "postconditions": "Espace de recueillement complet affiché, ambiance sonore solennelle en cours d'exécution.",
        "legal": "Respect de la dignité des défunts et de la solennité des hommages funéraires.",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "mobile",
            "deviceLabel": "Sanctuaire Mobile • Espace de Recueillement Solennel",
            "formFields": [
                {"label": "Défunt Honoré", "name": "deceased_name", "type": "text", "value": "Henri Dubois (1944 — 2026)", "placeholder": "Nom", "badge": "Certifié", "required": False},
                {"label": "Épitaphe Mémorielle", "name": "epitaph_text", "type": "text", "value": "« Le souvenir est une présence invisible dans la paix des bois »", "placeholder": "Épitaphe", "badge": "Gravé", "required": False},
                {"label": "Ambiance Musicale", "name": "music_state", "type": "text", "value": "In Paradisum (Fauré) — Lecture douce en cours", "placeholder": "Musique", "badge": "Audio Actif", "required": False},
                {"label": "Mode Réseau", "name": "network_status", "type": "text", "value": "100% HORS-LIGNE (Zéro connexion Internet requise)", "placeholder": "Réseau", "badge": "Offline", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_listen_voice", "label": "🎙️ Écouter le Témoignage Vocal (Ducking -14 dB)", "role": "primary", "state": "idle", "icon": "🎙️"},
                {"id": "btn_view_wills", "label": "📜 Consulter les Dernières Volontés Civiles", "role": "secondary", "state": "idle", "icon": "📜"}
            ],
            "validationMsg": {
                "title": "Sanctuaire Nominal Affiché",
                "badge": "100% Hors-Ligne • Audio Actif",
                "detail": "Ambiance solennelle active. Portrait 480x480 (DEC-AET-12) rendu avec halo doré noble."
            },
            "errorCase": {
                "code": "ERR_SANCTUARY_OFFLINE_CACHE",
                "title": "Ressources Locales Manquantes en Mode Hors-Ligne",
                "condition": "Navigateur ayant vidé le cache de l'application PWA lors d'un nettoyage système agressif.",
                "message": "Erreur d'exécution : Les polices ou scripts locaux du Sanctuaire sont indisponibles hors-ligne.",
                "remediation": "Recharger une seule fois la page avec une connexion Internet pour restaurer le cache permanent ServiceWorker."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Transition Douce vers le Sanctuaire",
                    "caption": "Rideau mémoriel noir obsidienne en cours d'ouverture solennelle.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Ouverture Mémorielle</span>
                        <span class="wf-status-badge wf-badge-neutral">Fondu d'Entrée</span>
                      </div>
                      <div class="wf-device-status-box">
                        <div><strong>Ouverture de l'arche mémorielle d'Henri Dubois...</strong></div>
                        <div class="wf-subtext">Chargement de la palette Or & Obsidienne et du portrait 480x480 (DEC-AET-12)</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">Entrer dans l'Espace de Recueillement</button>
                      </div>
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Révélation du Portrait & Lancement Musical Fondu 2s",
                    "triggerName": "Apparition du portrait central avec halo doré et démarrage audio",
                    "caption": "Le moteur WebAudio déclenche la musique 'In Paradisum' avec montée progressive du volume.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Recueillement Actif</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Musique d'Ambiance Lancée</span>
                      </div>
                      <div class="wf-sanctuary-center wf-radar-pulse">
                        <div class="wf-portrait-halo">👤 Portrait HD d'Henri Dubois</div>
                        <div class="wf-gold-title">Henri Dubois (1944 — 2026)</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Recueillement en cours...</button>
                      </div>
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Bouclage Harmonique & Lecture de l'Épitaphe",
                    "progress": 90,
                    "caption": "La musique d'ambiance boucle de manière transparente. Les textes solennels s'animent en douceur.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Moteur Audio & Textes</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Immersion (90%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 90%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [AUDIO-CORE] Piste In Paradisum : Boucle harmonique sans couture active</code><br>
                        <code>> [DSP-VOLUME] Volume stabilisé à 80% solennel</code><br>
                        <code>> [TEXT-RENDER] Épitaphe affichée en Cormorant Garamond avec contraste AAA</code>
                      </div>
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Sanctuaire Mémoriel Nominal Complet",
                    "status": "success",
                    "caption": "Expérience familiale sereine. La famille peut écouter le message vocal ou consulter les volontés.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Henri Dubois</span>
                        <span class="wf-status-badge wf-badge-success">✨ Recueillement Nominal</span>
                      </div>
                      <div class="wf-sanctuary-full">
                        <div class="wf-portrait-circle">👤</div>
                        <div class="wf-epitaph-quote">« Le souvenir est une présence invisible dans la paix des bois »</div>
                        <div class="wf-music-indicator">🎵 In Paradisum (Fauré) en cours de lecture douce</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🎙️ Écouter le Témoignage Vocal (Ducking)</button>
                        <button class="wf-btn wf-btn-sub">📜 Volontés Civiles</button>
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
        "title": "Alerte Médicale d'Urgence : Exérèse Pacemaker / DAE (référence à confirmer par un juriste)",
        "cat": "Directives Médicales & Sécurité",
        "actor": "Pompes Funèbres, Crématorium & Médecin Légiste",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["Pacemaker", "DAE", "AlerteRouge", "Explosion", "CDLD"],
        "preconditions": "Carte Directives présentée par un opérateur funéraire avant mise en bière.",
        "flow": [
            "Scan instantané de la Carte Directives par l'agent funéraire ou le responsable de crématorium.",
            "Détection immédiate dans le compartiment médical de la mention d'un pacemaker ou défibrillateur implanté actif.",
            "Affichage d'un écran d'alerte de sécurité prioritaire rouge vif :",
            "- Mention expresse du risque d'explosion thermique.",
            "- Référence à l'article L1232-17 §2 du CDLD (référence à confirmer par un juriste) imposant l'exérèse chirurgicale préalable.",
            "- Affichage du statut : soit 'Exérèse déjà certifiée par le Dr. Vaneck', soit 'ATTENTION : Exérèse non certifiée — Interdiction stricte de mise en bière'.",
            "Bouton d'appel d'urgence du praticien désigné."
        ],
        "postconditions": "Sécurité physique absolue des agents funéraires garantie, zéro risque d'explosion au four crématoire ou autoclave.",
        "legal": "Article L1232-17 §2 du CDLD wallon (exérèse obligatoire des stimulateurs cardiaques) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "mobile",
            "deviceLabel": "Sanctuaire Mobile • Moniteur de Sécurité Vitale Pacemaker",
            "formFields": [
                {"label": "Dispositif Médical Actif", "name": "medical_implant", "type": "text", "value": "Stimulateur Cardiaque Actif (Pacemaker)", "placeholder": "Implant", "badge": "ALERTE VITALE", "required": False},
                {"label": "Risque Physique", "name": "explosion_risk", "type": "text", "value": "Explosion Thermique Majeure (> 250°C)", "placeholder": "Risque", "badge": "Danger Mortel", "required": False},
                {"label": "Statut de Retrait Chirurgical", "name": "removal_status", "type": "text", "value": "CERTIFIÉ RETIRÉ (Dr. Marc Vaneck — INAMI 1-40912-88-004)", "placeholder": "Statut", "badge": "Exérèse OK", "required": False},
                {"label": "Fondement Légal", "name": "legal_cdld", "type": "text", "value": "Art. L1232-17 §2 CDLD (référence à confirmer par un juriste)", "placeholder": "Loi", "badge": "Imposé", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_view_medical_cert", "label": "Consulter le Certificat d'Exérèse Officiel", "role": "primary", "state": "idle", "icon": "🩺"},
                {"id": "btn_call_doctor", "label": "Appel d'Urgence Dr. Vaneck", "role": "secondary", "state": "idle", "icon": "📞"}
            ],
            "validationMsg": {
                "title": "Alerte Pacemaker Traitée & Certifiée",
                "badge": "Exérèse Vérifiée Conforme",
                "detail": "Stimulateur retiré chirurgicalement. Feu vert pour mise en bière et opérations funéraires."
            },
            "errorCase": {
                "code": "ERR_PACEMAKER_CRITICAL_RISK",
                "title": "Alerte Rouge : Pacemaker Présent Non Retiré",
                "condition": "Scan d'un corps porteur d'un stimulateur sans certificat d'exérèse renseigné.",
                "message": "DANGER DE MORT / EXPLOSION : Un stimulateur cardiaque actif est présent dans le corps. Mise en bière et crémation formellement interdites par la loi (Art. L1232-17 §2 CDLD — référence à confirmer par un juriste).",
                "remediation": "Exiger l'intervention immédiate d'un médecin pour procéder à l'exérèse chirurgicale avant toute manipulation."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Opérateur Approchant la Carte avant Mise en Bière",
                    "caption": "Scan pré-opératoire de sécurité. L'opérateur vérifie l'absence de dispositifs explosifs.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Contrôle Sécurité Opérateur</span>
                        <span class="wf-status-badge wf-badge-neutral">Scan Pré-Opératoire</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-alert-icon">⚠️</span>
                        <div><strong>Contrôle Obligatoire Dispositifs Actifs (référence à confirmer par un juriste)</strong></div>
                        <div class="wf-subtext">Approchez la Carte Directives pour vérification pacemaker / DAE</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">Vérifier Présence Pacemaker</button>
                      </div>
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Détection Immédiate de la Présence d'un Stimulateur",
                    "triggerName": "Scan NFC de la Carte Directives révélant la balise Pacemaker",
                    "caption": "Activation de l'écran d'alerte rouge clignotant et vérification du visa d'exérèse.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Alerte Vitale Détectée</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Dispositif Actif Identifié</span>
                      </div>
                      <div class="wf-alert-card wf-alert-red wf-radar-pulse">
                        <div class="wf-trigger-indicator">⚠️ ATTENTION : Défunt Porteur d'un Pacemaker</div>
                        <div class="wf-subtext">Risque d'explosion thermique • Consultation immédiate du visa médical</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-danger wf-pulse-btn">Contrôle du visa d'exérèse...</button>
                      </div>
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Vérification du Certificat Chirurgical du Dr. Vaneck",
                    "progress": 98,
                    "caption": "Le système contrôle la validité de l'attestation numérique d'exérèse enregistrée in-silico.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Vérification Visa Médical</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Contrôle INAMI (98%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 98%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [LEGAL-CHECK] Recherche visa d'exérèse sur partition médicale...</code><br>
                        <code>> [LEGAL-CHECK] Visa trouvé : Signé par Dr. Marc Vaneck (INAMI 1-40912-88-004)</code><br>
                        <code>> [SAFETY] Exérèse chirurgicale validée : Zéro risque d'explosion</code>
                      </div>
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Feu Vert de Sécurité pour Mise en Bière",
                    "status": "success",
                    "caption": "Alerte levée avec succès. L'attestation officielle du médecin décharge les opérateurs.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">Sanctuaire • Feu Vert Sécurité</span>
                        <span class="wf-status-badge wf-badge-success">✨ Exérèse Validée</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🟢</span>
                        <div>
                          <strong>Exérèse Chirurgicale Certifiée par Praticien</strong>
                          <p class="wf-subtext">Conforme Art. L1232-17 §2 CDLD (référence à confirmer par un juriste) • Mise en bière et cérémonies autorisées</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Don d'Organes →</button>
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
    }
]
