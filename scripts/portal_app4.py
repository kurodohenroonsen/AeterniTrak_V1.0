#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeterniTrak V1.0 — Définition Complète des Micro Use-Cases pour App 4 : Filière & Traçabilité (UC-401 à UC-414)
Avec Simulateur de Wireframes Interactifs à 4 États, Spécifications des Formulaires, Actions, Validations et Erreurs Normatives.
"""

APP4_USECASES = [
    {
        "id": "UC-401",
        "title": "Constat Médical Initial & Aiguillage des 4 Filières Post-Décès",
        "cat": "Constat Civil & Tri",
        "actor": "Vétérinaire Sanitaire & Conseiller",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["Aiguillage", "Triage", "4Filieres", "Constat", "Biosecurite"],
        "preconditions": "Arrivée d'une dépouille animale au centre de collecte ou constat en exploitation.",
        "flow": [
            "Ouverture du terminal industriel AeterniTrak par le vétérinaire sanitaire agréé.",
            "Saisie des données biométriques et cliniques initiales : identification de l'espèce (TaxID NCBI), cause présumée de la mort, antécédents médicaux.",
            "Aiguillage algorithmique strict vers l'une des 4 filières étanches :",
            "- Profil 1 : Compagnie (Catégorie 1 mémorielle exclusive)",
            "- Profil 2 : Faune Sauvage (Catégorie 1/2 DNF avec badge et GPS)",
            "- Profil 3 : Élevage / Ferme (Catégorie 2 avec boucle Sanitel)",
            "- Profil 4 : Déchets d'Abattoir (Catégorie 1 MRS avec dénaturation bleue)",
            "Génération du dossier numérique de traçabilité scellé in-silico."
        ],
        "postconditions": "Dépouille affectée de manière irrévocable à sa filière réglementaire, zéro risque de contamination croisée.",
        "legal": "Règlement (CE) n° 1069/2009 (règles sanitaires applicables aux sous-produits animaux) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "industrial",
            "deviceLabel": "Terminal Terrain DNF / AFSCA • Triage Sanitaire Initial (IP68)",
            "formFields": [
                {"label": "Identifiant Unique Dépouille", "name": "depouille_id", "type": "text", "value": "DEP-2026-BEL-99201 (Génération Automatique)", "placeholder": "ID Dépouille", "badge": "RFID / QR", "required": False},
                {"label": "Taxonomie Espèce (NCBI)", "name": "species_taxid", "type": "select", "value": "Canis familiaris (TaxID 9615 - Chien de Compagnie)", "placeholder": "Espèce", "badge": "TaxID 9615", "required": True},
                {"label": "Cause du Décès", "name": "cause_death", "type": "select", "value": "Fin de vie naturelle / Vieillesse (Absence d'épizootie)", "placeholder": "Cause", "badge": "Clinique", "required": True},
                {"label": "Aiguillage Réglementaire", "name": "channel_assigned", "type": "text", "value": "PROFIL 1 : Compagnie (Catégorie 1 Mémoriel Exclusif)", "placeholder": "Filière", "badge": "Profil 1 Mémoriel", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_confirm_triage", "label": "Valider l'Aiguillage Réglementaire AeterniTrak", "role": "primary", "state": "idle", "icon": "🧭"},
                {"id": "btn_quarantine", "label": "Mise sous Séquestre Sanitaire Suspect", "role": "danger", "state": "idle", "icon": "☣️"}
            ],
            "validationMsg": {
                "title": "Aiguillage Sanitaire Réussi",
                "badge": "Profil 1 Mémoriel Assigné",
                "detail": "Espèce résolue (TaxID 9615). Ligne mémorielle hermétique réservée sans contamination."
            },
            "errorCase": {
                "code": "ERR_INITIAL_TRIAGE_INVALID",
                "title": "Suspicion d'Épizootie ou Espèce Non Répertoriée",
                "condition": "Cause de mortalité suspecte (fièvre charbonneuse, rage) ou espèce inconnue de l'arbre taxonomique.",
                "message": "ALERTE SANITAIRE : Suspicion de maladie réputée contagieuse ou anomalie taxonomique. Aiguillage normal suspendu.",
                "remediation": "Isoler immédiatement la carcasse en zone de confinement étanche et alerter les inspecteurs vétérinaires AFSCA."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Terminal Prêt au Poste de Réception des Dépouilles",
                    "caption": "Formulaire de déclaration vierge. Le vétérinaire inspecte la dépouille.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Saisie de l'Espèce & Résolution Taxonomique",
                    "triggerName": "Sélection de Canis familiaris et constat de mort naturelle sans épizootie",
                    "caption": "Recherche instantanée dans le snapshot taxonomique officiel NCBI embarqué.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Génération de l'Identifiant Unique & Verrouillage de Filière",
                    "progress": 88,
                    "caption": "Attribution irrévocable du Profil 1 Mémoriel et création du scellé numérique RFID.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Filière Mémorielle Assignée & Scellée",
                    "status": "success",
                    "caption": "La carcasse est admise dans le sas de décontamination mémoriel dédié.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-402",
        "title": "Profil 1 — Filière Compagnie (Catégorie 1 Mémoriel) & Ségrégation",
        "cat": "Profils Dépouilles",
        "actor": "Opérateur de Bioconversion",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["Compagnie", "Profil1", "Cat1Memoriel", "Segregation", "SasIndividuel"],
        "preconditions": "Animal de compagnie orienté vers le Profil 1 mémoriel.",
        "flow": [
            "Réception de la dépouille dans le sas de décontamination individuel mémoriel.",
            "Vérification de l'absence totale de contact physique ou aéraulique avec les filières d'élevage ou d'abattoir.",
            "Attribution d'un bac de sarcomusation individuel avec larves d'Hermetia illucens dédiées.",
            "Enregistrement de la traçabilité de la colonie de bioconversion (TaxID 343691).",
            "Verrouillage hermétique interdisant tout mélange de résidus entre animaux."
        ],
        "postconditions": "Ségrégation physique absolue accomplie, traçabilité individuelle garantie pour la famille.",
        "legal": "Arrêté royal du 27 avril 2007 (règles sanitaires pour les cadavres d'animaux de compagnie) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "industrial",
            "deviceLabel": "Terminal Terrain DNF / AFSCA • Sas Mémoriel Individuel (IP68)",
            "formFields": [
                {"label": "Bac de Sarcomusation", "name": "bioreactor_id", "type": "text", "value": "Caisson Mémoriel N° 04 (Ligne Hermétique)", "placeholder": "Bac", "badge": "Individuel", "required": False},
                {"label": "Colonie de Bioconversion", "name": "colony_taxid", "type": "text", "value": "Hermetia illucens (TaxID 343691 — Mouche soldat noire)", "placeholder": "Colonie", "badge": "TaxID 343691", "required": False},
                {"label": "Ségrégation Aéraulique", "name": "airlock_status", "type": "text", "value": "SAS INDIVIDUEL ÉTANCHE (Pression négative 25 Pa)", "placeholder": "Sas", "badge": "Confiné", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_seal_airlock", "label": "Sceller le Sas de Bioconversion Mémoriel", "role": "primary", "state": "idle", "icon": "🔒"},
                {"id": "btn_check_sensors", "label": "Vérifier Détecteurs de Pression Sas", "role": "secondary", "state": "idle", "icon": "📊"}
            ],
            "validationMsg": {
                "title": "Sas Individuel Scellé",
                "badge": "Ségrégation 100% Hermétique",
                "detail": "Zéro contact avec les filières agricoles. Ligne mémorielle dédiée et isolée."
            },
            "errorCase": {
                "code": "ERR_PET_CROSS_CONTAMINATION",
                "title": "Rupture de Ségrégation ou Risque de Mélange",
                "condition": "Tentative d'introduction conjointe de deux dépouilles dans le même caisson ou défaillance du sas.",
                "message": "ALERTE CRITIQUE : Rupture de confinement individuel. Risque de contamination croisée entre flux mémoriels.",
                "remediation": "Stopper immédiatement l'introduction, désinfecter le sas et rétablir le caisson individuel exclusif."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Caisson Individuel Ouvert en Attente de Dépouille",
                    "caption": "Caisson n° 04 nettoyé et stérilisé. Les larves d'Hermetia illucens sont prêtes.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Introduction de la Dépouille & Fermeture du Sas",
                    "triggerName": "Dépôt de la dépouille identifiée DEP-2026-BEL-99201 et verrouillage",
                    "caption": "Verrouillage électromagnétique du sas individuel avec retour visuel vert.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Surveillance Télémétrique de la Bioconversion",
                    "progress": 70,
                    "caption": "Suivi des capteurs de température, d'hygrométrie et d'activité des larves.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Cycle de Sarcomusation Mémorielle Scellé",
                    "status": "success",
                    "caption": "Résidus cinéraires individuels prêts pour l'étape de pasteurisation thermique.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-403",
        "title": "Dépistage Toxicologique Qualitatif LFA du Pentobarbital",
        "cat": "Contrôle Biologique",
        "actor": "Vétérinaire & Opérateur",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["Pentobarbital", "LFA", "DepistageQualitatif", "Toxicologie", "PorteG4"],
        "preconditions": "Prélèvement d'échantillon tissulaire sur dépouille de compagnie avant ou après transformation.",
        "flow": [
            "Extraction liquide rapide sur bandelette de test immunochromatographique (LFA - Lateral Flow Assay) basée sur un principe compétitif.",
            "Insertion de la bandelette dans le lecteur optique connecté au terminal.",
            "Vérification de la présence des lignes de contrôle (C) et de test (T) :",
            "- Lignes C et T visibles : RÉSULTAT NÉGATIF / CONFORME (absence de pentobarbital détecté), validation formelle 'PENTO_OK' pour la filière mémorielle.",
            "- Ligne C seule visible (ligne T absente / inhibée) : RÉSULTAT POSITIF / CONTAMINÉ (présence de pentobarbital), REJET ABSOLU, blocage irréversible de la signature et réorientation obligatoire vers incinération Catégorie 1.",
            "- Ligne C absente : test non valide, obligation de réitérer le dépistage.",
            "Évaluation de la Porte de Fer G4 (Dépistage Pentobarbital) : verrouillage déterministe.",
            "Scellement cryptographique du résultat qualitatif LFA dans la revendication de lot."
        ],
        "postconditions": "Statut toxicologique certifié, garantie absolue de l'absence de résidus d'euthanasique toxique.",
        "legal": "Directive The Iron Gate G4 et normes de sécurité toxicologique vétérinaire AFSCA (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "industrial",
            "deviceLabel": "Terminal Terrain DNF / AFSCA • Lecteur Optique LFA Pentobarbital",
            "formFields": [
                {"label": "Substance Recherchée", "name": "target_toxin", "type": "text", "value": "Pentobarbital Sodique (Agent Euthanasique Vétérinaire)", "placeholder": "Substance", "badge": "Toxique", "required": False},
                {"label": "Principe de Dépistage", "name": "screening_type", "type": "text", "value": "Test immunochromatographique compétitif LFA", "placeholder": "Principe", "badge": "Compétitif", "required": False},
                {"label": "Lecture Optique des Lignes", "name": "measured_lines", "type": "text", "value": "Lignes C et T visibles (NÉGATIF — Absence de molécule détectée)", "placeholder": "Résultat", "badge": "C+T Conforme", "required": False},
                {"label": "Verdict Porte G4", "name": "gate_g4_status", "type": "text", "value": "VALIDÉ (Absence de pentobarbital, feu vert pour pasteurisation et forêt)", "placeholder": "Porte G4", "badge": "Porte G4 OK", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_run_lfa_scan", "label": "Lancer la Lecture Optique LFA", "role": "primary", "state": "idle", "icon": "🔬"},
                {"id": "btn_simulate_pento_fail", "label": "Simuler Rejet Pentobarbital (Ligne C seule)", "role": "secondary", "state": "idle", "icon": "⚠️"}
            ],
            "validationMsg": {
                "title": "Test LFA Pentobarbital Conforme",
                "badge": "Porte G4 Franchie (Lignes C+T)",
                "detail": "Lignes C et T visibles (principe compétitif). Absence de molécule de pentobarbital. Zéro risque toxicologique pour les écosystèmes forestiers."
            },
            "errorCase": {
                "code": "ERR_PENTO_DETECTED",
                "title": "Présence de Pentobarbital Détectée (Ligne C Seule)",
                "condition": "Bandelette LFA positive : ligne C seule visible, ligne test T inhibée par la molécule de pentobarbital.",
                "message": "REJET TOXICOLOGIQUE MAJEUR (Porte G4) : Bandelette LFA positive (Ligne C seule visible, ligne T absente/inhibée). Présence de résidus d'euthanasique mortels pour la faune sylvicole. Valorisation forestière formellement interdite.",
                "remediation": "Aiguiller immédiatement le lot vers l'incinération thermique industrielle de Catégorie 1."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Bandelette LFA Insérée dans le Lecteur Optique",
                    "caption": "Bandelette de test insérée. Le lecteur attend l'ordre de numérisation optique.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Acquisition Optique de la Bandelette LFA",
                    "triggerName": "Clic sur 'Lancer la Lecture' et capture haute résolution de la bandelette",
                    "caption": "Acquisition optique et détection de contraste des lignes Contrôle (C) et Test (T).",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Vérification Porte G4 : Lignes C et T Validées (Négatif)",
                    "progress": 92,
                    "caption": "Validation du principe compétitif : présence de la ligne T confirmant l'absence de pentobarbital.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Visa Sanitaire Toxicologique Délivré",
                    "status": "success",
                    "caption": "Feu vert accordé pour la pasteurisation thermique et le retour en forêt mémorielle.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-404",
        "title": "Pasteurisation Thermique Mémorielle (70°C, 1 heure continue)",
        "cat": "Traitement Thermique",
        "actor": "Opérateur de Traitement Thermique",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["Pasteurisation", "70Degres", "1Heure", "Thermocouple", "PorteG9"],
        "preconditions": "Lot de résidus et protéines d'Hermetia illucens certifié négatif au pentobarbital.",
        "flow": [
            "Chargement des matières dans la cuve de pasteurisation thermique mémorielle.",
            "Immersion de trois thermocouples étalonnés au cœur de la matière.",
            "Montée en température progressive jusqu'à atteindre au moins 70,0°C au point le plus froid.",
            "Maintien continu et ininterrompu du palier thermique à 70,0°C pendant au moins 60 minutes.",
            "Acquisition continue des courbes de température (1 mesure par seconde) par l'automate homologué.",
            "Vérification de la Porte de Fer G9 (Traitement Sanitaire Requis & Preuve : pasteurisation mémorielle 70°C/1h sous dérogation DEC-AET-05)."
        ],
        "postconditions": "Éradication complète des bactéries pathogènes (Salmonella, Enterobacteriaceae), scellement thermique.",
        "legal": "Règlement (CE) n° 142/2011 (normes de transformation pour sous-produits animaux) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "industrial",
            "deviceLabel": "Terminal Terrain DNF / AFSCA • Moniteur Thermique de Pasteurisation (IP68)",
            "formFields": [
                {"label": "Température Cœur Actuelle", "name": "temp_core", "type": "number", "value": "70.8°C (Seuil mini réglementaire : 70.0°C)", "placeholder": "Température", "badge": "70.8°C", "required": False},
                {"label": "Durée Maintien Continu", "name": "hold_duration", "type": "text", "value": "60 min 00 s (Palier continu sans interruption)", "placeholder": "Durée", "badge": "1h Validée", "required": False},
                {"label": "Pression Manométrique", "name": "gauge_pressure", "type": "text", "value": "Pression Atmosphérique Normale (Pasteurisation)", "placeholder": "Pression", "badge": "1.0 bar", "required": False},
                {"label": "Verdict Porte G9", "name": "gate_g9_status", "type": "text", "value": "VALIDÉ (Pasteurisation conforme, éradication des pathogènes végétatifs)", "placeholder": "Porte G9", "badge": "Porte G9 OK", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_certify_pasteurisation", "label": "Certifier le Cycle de Pasteurisation Thermique", "role": "primary", "state": "idle", "icon": "🔥"},
                {"id": "btn_export_thermal_curve", "label": "Exporter Courbe Température-Temps", "role": "secondary", "state": "idle", "icon": "📈"}
            ],
            "validationMsg": {
                "title": "Cycle de Pasteurisation Conforme",
                "badge": "70°C / 1h Continue",
                "detail": "Salmonella et Enterobacteriaceae éradiquées. Courbe thermique validée par la Porte G9."
            },
            "errorCase": {
                "code": "ERR_PASTEURISATION_TEMP_DROP",
                "title": "Rupture Thermique : Baisse de Température",
                "condition": "Chute de la température au cœur sous 70.0°C à tout moment des 60 minutes de maintien.",
                "message": "CYCLE THERMIQUE INVALIDÉ : La température est descendue à 68.9°C au cours du palier. Le compteur de temps continu est remis à zéro.",
                "remediation": "Réchauffer la cuve au-dessus de 70.0°C et recommencer l'intégralité du cycle de 60 minutes continues."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Cuve Chargée en Début de Montée Thermique",
                    "caption": "Matières chargées. La température actuelle est de 42°C, en phase de préchauffage.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Franchissement du Seuil des 70.0°C & Déclenchement Chrono",
                    "triggerName": "La température au cœur atteint 70.0°C, démarrage du compteur 60 min",
                    "caption": "Activation du compte à rebours de 60 minutes avec verrouillage de cuve.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Maintien Continu : 45 min / 60 min (T° = 70.8°C)",
                    "progress": 75,
                    "caption": "Surveillance seconde par seconde. La température oscille de manière stable entre 70.5°C et 71.2°C.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Cycle de Pasteurisation 70°C/1h Validé",
                    "status": "success",
                    "caption": "Sécurité microbiologique absolue. Le lot pasteurisé peut être valorisé en forêt cinéraire.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-405",
        "title": "Valorisation Forestière Cinéraire sous Dérogation DEC-AET-05",
        "cat": "Destination Finale",
        "actor": "Garde Forestier DNF & Famille",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["ForetCineraire", "DEC-AET-05", "ArbreDuSouvenir", "Amendement", "DNF"],
        "preconditions": "Lot de compagnie sain, pasteurisé à 70°C pendant 1h, politique dérogatoire signée.",
        "flow": [
            "Vérification par The Iron Gate de l'application de la dérogation souveraine DEC-AET-05.",
            "Conditionnement des protéines et résidus sous forme d'amendement fertilisant pour arbre cinéraire du souvenir.",
            "Épandage au pied de l'arbre mémoriel désigné dans une forêt cinéraire privée agréée.",
            "Inscription de l'arbre et du défunt dans le cadastre mémoriel forestier.",
            "Verrouillage cryptographique absolu interdisant toute réintroduction dans la chaîne alimentaire agricole."
        ],
        "postconditions": "Boucle de retour à la nature accomplie dans le recueillement et le respect de la loi.",
        "legal": "Décret wallon du 15 juillet 2008 (Code forestier art. 41) et Dérogation souveraine DEC-AET-05 (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "industrial",
            "deviceLabel": "Terminal Terrain DNF / AFSCA • Cadastre Forestier Cinéraire (IP68)",
            "formFields": [
                {"label": "Cadre Dérogatoire Appliqué", "name": "derogation_policy", "type": "text", "value": "DEC-AET-05 (Amendement Mémoriel Sylvicole)", "placeholder": "Dérogation", "badge": "DEC-AET-05", "required": False},
                {"label": "Arbre Cinéraire Cadastré", "name": "tree_id", "type": "text", "value": "Chêne Mémoriel n° F-2408 (Massif de Saint-Hubert)", "placeholder": "Arbre", "badge": "Cadastré DNF", "required": True},
                {"label": "Coordonnées GPS Submétriques", "name": "tree_gps", "type": "text", "value": "50.02418° N, 5.37214° E (Précision ±0.3m)", "placeholder": "GPS", "badge": "RTK Fix", "required": False},
                {"label": "Interdiction Réinjection Agricole", "name": "feed_ban_lock", "type": "text", "value": "VERROU ABSOLU (Exclusion chaîne alimentaire agricole)", "placeholder": "Feed-Ban", "badge": "Inviolable", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_issue_forestry_cert", "label": "Émettre l'Attestation d'Épandage Cinéraire", "role": "primary", "state": "idle", "icon": "🌳"},
                {"id": "btn_check_cadastre", "label": "Vérifier Inscription Cadastrale DNF", "role": "secondary", "state": "idle", "icon": "🗺️"}
            ],
            "validationMsg": {
                "title": "Attestation Forestière Cinéraire Émise",
                "badge": "Dérogation DEC-AET-05 Validée",
                "detail": "Amendement apporté au Chêne F-2408. Cadastre forestier émargé et scellé."
            },
            "errorCase": {
                "code": "ERR_FOREST_DEROGATION_INVALID",
                "title": "Dérogation Non Signée ou Arbre Non Cadastré",
                "condition": "Tentative d'épandage sur parcelle publique non conventionnée ou absence d'accord DNF.",
                "message": "INTERDICTION D'ÉPANDAGE : La parcelle visée ne bénéficie pas de l'agrément de forêt cinéraire ou la dérogation DEC-AET-05 n'est pas scellée.",
                "remediation": "Sélectionner un arbre mémoriel agréé au cadastre DNF conventionné."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Parcelle Forestière Identifiée sur le Cadastre",
                    "caption": "Garde forestier sur site. L'arbre cinéraire est repéré par coordonnées GPS.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Apport de l'Amendement Organique & Signature Badge DNF",
                    "triggerName": "Scan du badge de l'agent DNF validant l'acte d'amendement du sol",
                    "caption": "Épandage au pied du système racinaire et enregistrement géolocalisé immédiat.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Enregistrement dans le Cadastre Mémoriel & Verrou Feed-Ban",
                    "progress": 95,
                    "caption": "Verrouillage absolu interdisant tout réemploi des terres à des fins agricoles.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Retour à la Nature Accompli dans la Dignité",
                    "status": "success",
                    "caption": "Certificat d'Arbre Mémoriel remis à la famille. Cycle de vie bouclé avec pureté.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-406",
        "title": "Profil 2 — Filière Faune Sauvage (Cat 1/2 DNF) : Badge & GPS",
        "cat": "Profils Dépouilles",
        "actor": "Garde Forestier DNF",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["FauneSauvage", "DNF", "BadgeAgent", "GPS-RTK", "Sanglier", "Cerf", "ControleAmont", "DEC-AET-13"],
        "preconditions": "Cadavre de grand gibier sauvage découvert en milieu naturel (sanglier, cerf, chevreuil).",
        "flow": [
            "Arrivée de l'agent DNF sur le lieu de signalement de la carcasse.",
            "Authentification de l'agent par scan de son badge NFC professionnel sécurisé (contrôle amont déclaratif, DEC-AET-13).",
            "Relevé automatique des coordonnées GPS satellitaires avec précision submétrique (< 1 mètre).",
            "Identification de l'espèce sauvage et encodage du TaxID NCBI (ex: 9823 pour Sus scrofa).",
            "Conditionnement en sac de confinement hermétique avec scellé numéroté DNF inviolable."
        ],
        "postconditions": "Carcasse prise en charge sous séquestre sanitaire officiel DNF.",
        "legal": "Décret wallon du 15 juillet 2008 relatif au Code forestier (missions de police sylvicole des agents DNF) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "industrial",
            "deviceLabel": "Terminal Terrain DNF / AFSCA • Module Agent DNF Faune Sauvage (IP68)",
            "formFields": [
                {"label": "Badge Agent Assermenté", "name": "dnf_badge_id", "type": "text", "value": "Agent Jean Dupont (Badge DNF-2026-771)", "placeholder": "Badge", "badge": "Assermenté", "required": True},
                {"label": "Position GPS RTK", "name": "gps_coords", "type": "text", "value": "50.41284° N, 5.82341° E (Précision: ±0.28m)", "placeholder": "GPS", "badge": "Submétrique", "required": False},
                {"label": "Grand Gibier Identifié", "name": "wild_species", "type": "select", "value": "Sus scrofa (TaxID 9823 — Sanglier d'Europe)", "placeholder": "Espèce", "badge": "TaxID 9823", "required": True},
                {"label": "Scellé de Confinement", "name": "seal_number", "type": "text", "value": "Scellé DNF-BE-2026-8891 (Sac étanche C1)", "placeholder": "Scellé", "badge": "Séquestre", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_seal_wild_corpse", "label": "Signer le Prélèvement de Faune Sauvage (Badge DNF)", "role": "primary", "state": "idle", "icon": "🐗"},
                {"id": "btn_rtk_recalibrate", "label": "Recalibrer Point GPS RTK", "role": "secondary", "state": "idle", "icon": "🛰️"}
            ],
            "validationMsg": {
                "title": "Prélèvement Faune Sauvage Enregistré",
                "badge": "Sous Séquestre DNF",
                "detail": "GPS ±0.28m et badge agent scellés. Sac étanche prêt pour transfert laboratoire."
            },
            "errorCase": {
                "code": "ERR_DNF_GPS_ACCURACY_LOW",
                "title": "Précision Satellitaire Insuffisante (> 1.0 m)",
                "condition": "Canopée dense bloquant le signal GPS RTK avec imprécision de localisation supérieure à 1 mètre.",
                "message": "Erreur géodésique : La précision GPS actuelle (±3.4m) ne respecte pas le standard submétrique imposé par le DNF.",
                "remediation": "Déplacer l'antenne RTK en clairière ou utiliser le point de repère topographique cadastré le plus proche."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Garde DNF Face à la Carcasse en Forêt",
                    "caption": "Carcasse de sanglier localisée. Le terminal DNF attend le scan du badge agent.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Scan du Badge Agent & Fix Satellitaire RTK",
                    "triggerName": "Scan du badge NFC de l'agent Jean Dupont et verrouillage GPS submétrique",
                    "caption": "Authentification de l'officier de police sylvicole et horodatage satellitaire atomique.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Génération de l'Identifiant de Séquestre Sanitaire",
                    "progress": 90,
                    "caption": "Création du dossier de surveillance épidémiologique et affectation du sac étanche.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Prélèvement Faune Sauvage Scellé pour Laboratoire",
                    "status": "success",
                    "caption": "Carcasse confinée sous contrôle étatique. Prête pour expédition au laboratoire d'analyse.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-407",
        "title": "Dépistages PCR Épizooties en Laboratoire Agréé (PPA & CWD)",
        "cat": "Contrôle Biologique",
        "actor": "Biologiste de Laboratoire Agréé (Sciensano)",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["PCR", "PPA", "CWD", "Prions", "Epizootie", "ControleAmont", "DEC-AET-13"],
        "preconditions": "Prélèvement d'organes cibles effectué par le garde DNF sur le gibier.",
        "flow": [
            "Analyse moléculaire par PCR en temps réel pour le virus de la Peste Porcine Africaine (PPA).",
            "Test Western Blot / ELISA pour le dépistage de la Maladie du Dépérissement Chronique des Cervidés (CWD - prions).",
            "Évaluation du contrôle sanitaire amont déclaratif (DEC-AET-13, Sciensano) :",
            "- Si résultat positif à une épizootie majeure : alerte d'urgence AFSCA, confinement du massif forestier et incinération C1 immédiate.",
            "- Si résultat strictement négatif : émission du visa sanitaire d'admission à la transformation.",
            "Scellement cryptographique du rapport de laboratoire dans le dossier du lot."
        ],
        "postconditions": "Statut sanitaire certifié par le laboratoire officiel avant toute bioconversion.",
        "legal": "Règlement d'exécution (UE) 2021/605 (mesures spéciales de lutte contre la peste porcine africaine) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "industrial",
            "deviceLabel": "Terminal Terrain DNF / AFSCA • Console de Laboratoire PCR (Sciensano)",
            "formFields": [
                {"label": "Test PCR PPA (Peste Porcine)", "name": "pcr_asf_result", "type": "text", "value": "NÉGATIF (Ct indéterminé > 40 cycles)", "placeholder": "PPA", "badge": "PPA Négatif", "required": False},
                {"label": "Test Prions CWD (Cervidés)", "name": "cwd_prion_result", "type": "text", "value": "NÉGATIF (Western Blot sans bande PrPSc)", "placeholder": "CWD", "badge": "CWD Négatif", "required": False},
                {"label": "Laboratoire Certificateur", "name": "lab_certifier", "type": "text", "value": "Sciensano Laboratoire de Référence Nationale", "placeholder": "Laboratoire", "badge": "Agrément AFSCA", "required": False},
                {"label": "Contrôle Amont Sanitaire", "name": "upstream_check_status", "type": "text", "value": "VALIDÉ (Contrôle déclaratif DEC-AET-13 conforme)", "placeholder": "Contrôle Amont", "badge": "DEC-AET-13 OK", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_issue_sanitary_visa", "label": "Délivrer le Visa Sanitaire d'Admission", "role": "primary", "state": "idle", "icon": "🧬"},
                {"id": "btn_simulate_asf_positive", "label": "Simuler Détection Positive PPA (Alerte Rouge)", "role": "danger", "state": "idle", "icon": "☣️"}
            ],
            "validationMsg": {
                "title": "Visa Sanitaire Laboratoire Validé",
                "badge": "Contrôle Amont Validé (DEC-AET-13)",
                "detail": "Aucun agent d'épizootie ni prion détecté. Admission pour stérilisation Méthode 1."
            },
            "errorCase": {
                "code": "ERR_EPIZOOTIC_PCR_POSITIVE",
                "title": "Alerte Épizootie Majeure : PCR PPA Positive",
                "condition": "Amplification virale PPA détectée avec Ct < 35 ou détection de prions CWD.",
                "message": "ALERTE NATIONALE DE BIOSÉCURITÉ (Contrôle Amont DEC-AET-13) : Virus PPA ou prion CWD détecté dans la carcasse. Risque épidémique majeur.",
                "remediation": "Déclencher le plan d'urgence sanitaire AFSCA, confiner le massif forestier et incinérer immédiatement la carcasse en Catégorie 1."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Échantillons d'Organes Prêts dans le Thermocycleur",
                    "caption": "Échantillon de rate et ganglions prêt. Le cycle PCR attend d'être analysé.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Fin de l'Amplification & Détection de Fluorescence",
                    "triggerName": "Lecture des courbes d'amplification temps réel (40 cycles)",
                    "caption": "Constat de l'absence totale de courbe de fluorescence pour le virus PPA.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Contrôle Amont Déclaratif (DEC-AET-13) & Scellement Cryptographique",
                    "progress": 95,
                    "caption": "Injection du certificat d'analyse officielle dans le dossier amont du lot.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Visa Sanitaire d'Admission Délivré",
                    "status": "success",
                    "caption": "Le gibier sauvage peut être admis en filière de traitement thermique haute sécurité.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-408",
        "title": "Stérilisation Européenne Méthode 1 (133°C, 3 bars, 20 minutes)",
        "cat": "Traitement Thermique",
        "actor": "Opérateur d'Autoclave Haute Pression",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["Methode1", "133Degres", "3Bars", "20Minutes", "Prions", "PorteG9"],
        "preconditions": "Matières de Catégorie 1 ou 2 nécessitant une neutralisation absolue des agents prions.",
        "flow": [
            "Broyage préalable obligatoire de la matière à une granulométrie inférieure ou égale à 50 mm.",
            "Chargement en autoclave industriel à vapeur saturée.",
            "Chauffe à une température minimale au cœur de la matière de 133,0°C sans interruption.",
            "Maintien sous pression manométrique d'au moins 3,0 bars pendant au moins 20 minutes consécutives.",
            "Acquisition horodatée et scellée des courbes Pression-Température-Temps par automate homologué.",
            "Validation de la Porte de Fer G9 (Traitement Sanitaire Requis & Preuve : Méthode 1 standard européen 133°C, 3 bars, 20 min)."
        ],
        "postconditions": "Inactivation irréversible de l'infectiosité des agents transmissibles non conventionnels (prions).",
        "legal": "Règlement (CE) n° 142/2011 (annexe IV, chapitre III - Méthode 1 de transformation standard) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "industrial",
            "deviceLabel": "Terminal Terrain DNF / AFSCA • Moniteur Autoclave Méthode 1 (IP68)",
            "formFields": [
                {"label": "Température au Cœur", "name": "temp_meth1", "type": "number", "value": "133.5°C (Seuil réglementaire : >= 133.0°C)", "placeholder": "Température", "badge": "133.5°C", "required": False},
                {"label": "Pression Vapeur Saturée", "name": "pressure_meth1", "type": "number", "value": "3.2 bars (Seuil réglementaire : >= 3.0 bars)", "placeholder": "Pression", "badge": "3.2 bars", "required": False},
                {"label": "Durée Maintien Continu", "name": "duration_meth1", "type": "text", "value": "20 min 00 s (Palier continu sans chute)", "placeholder": "Durée", "badge": "20 min", "required": False},
                {"label": "Granulométrie Préalable", "name": "grain_size", "type": "text", "value": "< 50 mm (Broyage industriel certifié)", "placeholder": "Broyat", "badge": "≤ 50 mm", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_certify_meth1", "label": "Valider la Conformité Méthode 1 (Règlement 1069/2009)", "role": "primary", "state": "idle", "icon": "♨️"},
                {"id": "btn_export_pt_curve", "label": "Télécharger Courbe P-T-t Chiffrée", "role": "secondary", "state": "idle", "icon": "📈"}
            ],
            "validationMsg": {
                "title": "Stérilisation Européenne Méthode 1 Validée",
                "badge": "133°C / 3 bars / 20 min OK",
                "detail": "Prions et agents conventionnels irréversiblement inactivés. Porte G9 satisfaite."
            },
            "errorCase": {
                "code": "ERR_METHOD1_PRESSURE_LOSS",
                "title": "Chute de Pression ou de Température sous les Seuils Légaux",
                "condition": "Pression descendant sous 3.0 bars ou température sous 133.0°C au cours des 20 minutes.",
                "message": "CYCLE MÉTHODE 1 INVALIDÉ : Pression manométrique descendue à 2.8 bars. Violation des exigences du Règlement (CE) 142/2011.",
                "remediation": "Purger la vapeur résiduelle, rétablir la pression à 3.2 bars et relancer l'intégralité du palier de 20 minutes."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Autoclave Chargé avec Broyat Calibré < 50mm",
                    "caption": "Matières broyées scellées dans la cuve. La montée en pression est en cours.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Atteinte du Palier 133°C & 3 bars : Déclenchement Chrono",
                    "triggerName": "La pression atteint 3.2 bars à 133.5°C, lancement du compteur 20 min",
                    "caption": "Verrouillage des vannes de sécurité et scellement du cycle haute pression.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Surveillance P-T-t : 15 min / 20 min (Pression Stable 3.2 b)",
                    "progress": 75,
                    "caption": "Enregistrement cryptographique continu des données de pression et température.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Cycle Méthode 1 Certifié Conforme",
                    "status": "success",
                    "caption": "Matières stérilisées au niveau réglementaire européen maximal. Inactivation validée.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-409",
        "title": "Profil 3 — Filière Élevage / Ferme (Catégorie 2) & Boucle Sanitel",
        "cat": "Profils Dépouilles",
        "actor": "Éleveur & Vétérinaire Sanitaire",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["Elevage", "Ferme", "Sanitel", "Boucle", "Cat2", "Bovine"],
        "preconditions": "Mortalité survenue dans une exploitation agricole agréée (bovins, porcins, ovins).",
        "flow": [
            "Déclaration obligatoire du décès dans les 24 heures via le terminal d'exploitation.",
            "Lecture optique et NFC de la boucle auriculaire officielle d'identification Sanitel.",
            "Vérification de l'absence de signes cliniques d'EST (ESB bovine, tremblante du mouton).",
            "Attribution exclusive de la filière de valorisation technique Catégorie 2 (biodiesel, engrais minéraux).",
            "Interdiction catégorique de tout aiguillage vers l'alimentation humaine ou animale mémorielle."
        ],
        "postconditions": "Carcasse agricole classée en Catégorie 2 prête pour la synchronisation officielle.",
        "legal": "Arrêté royal du 23 mars 2011 (identification et enregistrement des bovins dans le système Sanitel) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "industrial",
            "deviceLabel": "Terminal Terrain DNF / AFSCA • Module Sanitel Élevage (IP68)",
            "formFields": [
                {"label": "Boucle Auriculaire Sanitel", "name": "sanitel_tag", "type": "text", "value": "BE 5 1284 9901 (Scan Optique & RFID)", "placeholder": "Boucle", "badge": "Sanitel National", "required": True},
                {"label": "Exploitation Agricole", "name": "farm_id", "type": "text", "value": "Ferme du Bocage (N° Troupeau: BE 0412.981.203)", "placeholder": "Exploitation", "badge": "Agréée", "required": False},
                {"label": "Espèce Agricole", "name": "livestock_species", "type": "select", "value": "Bos taurus (TaxID 9913 — Ruminant Bovin Laitier)", "placeholder": "Espèce", "badge": "Ruminant", "required": True},
                {"label": "Filière Attribuée", "name": "assigned_category", "type": "text", "value": "CATÉGORIE 2 (Aiguillage Industriel Exclusif : Biodiesel)", "placeholder": "Filière", "badge": "Cat 2 Technique", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_validate_farm_admission", "label": "Valider l'Admission Catégorie 2 Agricole", "role": "primary", "state": "idle", "icon": "🐄"},
                {"id": "btn_verify_sanitel_online", "label": "Vérifier Déclaration Sanitel", "role": "secondary", "state": "idle", "icon": "📡"}
            ],
            "validationMsg": {
                "title": "Dépouille Agricole Admise en Catégorie 2",
                "badge": "Sanitel BE 5 1284 9901",
                "detail": "Boucle nationale validée. Aiguillage exclusif vers valorisation technique (biodiesel)."
            },
            "errorCase": {
                "code": "ERR_FARM_FOOD_CHANNEL_LEAK",
                "title": "Tentative d'Aiguillage vers la Chaîne Alimentaire",
                "condition": "Erreur d'opérateur sélectionnant une destination d'alimentation animale pour un animal d'élevage mort.",
                "message": "BLOCAGE STRICT (Feed-Ban) : Les animaux morts en élevage relèvent obligatoirement de la Catégorie 2. Toute utilisation pour l'alimentation est pénalement interdite.",
                "remediation": "Forcer l'aiguillage exclusif vers la filière technique (combustion cimenterie ou biodiesel industriel)."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Bovin Déclaré en Exploitation en Attente de Scan",
                    "caption": "Éleveur devant la dépouille. La boucle Sanitel doit être scannée par RFID.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Lecture RFID de la Boucle Auriculaire BE 5 1284 9901",
                    "triggerName": "Scan RFID de l'étiquette auriculaire officielle Sanitel",
                    "caption": "Reconnaissance instantanée du numéro national d'identification bovine.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Classification Obligatoire en Sous-Produit Catégorie 2",
                    "progress": 90,
                    "caption": "Verrouillage anti-alimentation animale et préparation de l'admission vers biodiesel.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Dépouille Classée Catégorie 2 & Tracée",
                    "status": "success",
                    "caption": "Dossier sanitaire clos. La carcasse partira en filière technique certifiée.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-410",
        "title": "Ingestion Automatisée APIs Sanitel & CERISE (Traçabilité Élevage)",
        "cat": "Interopérabilité APIs",
        "actor": "Système Core & Autorité AFSCA",
        "platforms": ["Node.js / Core Engine", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["APIs", "Sanitel", "CERISE", "ARSIA", "Tracabilite", "ControleAmont", "DEC-AET-13"],
        "preconditions": "Numéro de boucle nationale Sanitel scanné sur la dépouille agricole.",
        "flow": [
            "Appel sécurisé en temps réel aux APIs du guichet agricole wallon CERISE et du registre fédéral Sanitel (AFSCA) pour vérification déclarative amont (DEC-AET-13).",
            "Récupération de la fiche complète : race, date de naissance, historique des déplacements d'exploitation en exploitation.",
            "Contrôle automatique du registre des traitements médicamenteux vétérinaires et respect des temps d'attente.",
            "Interrogation des bases sanitaires régionales ARSIA (Wallonie) et DGZ (Flandre) pour confirmer l'absence de mise sous séquestre.",
            "Agrégation des données certifiées au dossier numérique de revendication de lot."
        ],
        "postconditions": "Zéro risque d'erreur de saisie manuelle, intégrité administrative garantie.",
        "legal": "Arrêté ministériel du 28 juin 2013 (modalités d'accès et d'échange de données avec le système Sanitel) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "industrial",
            "deviceLabel": "Terminal Terrain DNF / AFSCA • Passerelle d'Interopérabilité Sanitel/CERISE",
            "formFields": [
                {"label": "API Fédérale Sanitel (AFSCA)", "name": "api_sanitel", "type": "text", "value": "CONNECTÉ (OAuth2 Mutual TLS — Jeton Valide)", "placeholder": "API Sanitel", "badge": "Fédéral", "required": False},
                {"label": "API Régionale CERISE (SPW)", "name": "api_cerise", "type": "text", "value": "CONNECTÉ (Guichet Agricole Wallon Synchronisé)", "placeholder": "API CERISE", "badge": "Régional", "required": False},
                {"label": "Temps d'Attente Médicamenteux", "name": "withhold_period", "type": "text", "value": "RESPECTÉ (45 jours écoulés post-antibiotiques)", "placeholder": "Temps attente", "badge": "Conforme", "required": False},
                {"label": "Statut Séquestre Sanitaire", "name": "quarantine_status", "type": "text", "value": "INDEMNE (Aucune restriction sur l'élevage BE 0412)", "placeholder": "Séquestre", "badge": "Indemne", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_sync_apis", "label": "Synchroniser avec Sanitel (AFSCA) & CERISE (SPW)", "role": "primary", "state": "idle", "icon": "🔄"},
                {"id": "btn_refresh_tokens", "label": "Rafraîchir Jetons de Sécurité OAuth2", "role": "secondary", "state": "idle", "icon": "🔑"}
            ],
            "validationMsg": {
                "title": "Données Fédérales & Régionales Ingestionnées",
                "badge": "Sanitel & CERISE 100% OK",
                "detail": "Historique de vie complet et temps d'attente médicamenteux certifiés sans saisie manuelle."
            },
            "errorCase": {
                "code": "ERR_SANITEL_API_UNREACHABLE",
                "title": "API Sanitel Inaccessible ou Numéro Inexistant",
                "condition": "Panne de réseau ou numéro de boucle auriculaire non répertorié au registre national.",
                "message": "Erreur d'interopérabilité : Impossible de synchroniser la fiche avec les registres Sanitel / CERISE.",
                "remediation": "Basculer en mode cache local sécurisé et réexécuter la synchronisation dès retour du réseau."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Requête d'Interopérabilité Prête à l'Envoi",
                    "caption": "Boucle BE 5 1284 9901 en attente d'interrogation sur les passerelles fédérales.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Échange REST / OAuth2 Sécurisé avec les Registres",
                    "triggerName": "Clic sur 'Synchroniser' et appel mTLS aux serveurs de l'AFSCA",
                    "caption": "Requête chiffrée par certificat d'autorité avec rapatriement des tables généalogiques.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Contrôle Automatique des Délais d'Attente Médicamenteux",
                    "progress": 95,
                    "caption": "Vérification algorithmique du respect des 45 jours après administration d'antibiotiques.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Dossier Agricole Scellé Sans Erreur de Saisie",
                    "status": "success",
                    "caption": "Données certifiées à 100% intégrées au lot pour l'évaluation de The Iron Gate.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-411",
        "title": "Profil 4 — Filière Déchets d'Abattoir (Cat 1 MRS) & Dénaturation Bleu",
        "cat": "Profils Dépouilles",
        "actor": "Inspecteur AFSCA & Opérateur d'Abattoir",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["Abattoir", "MRS", "BleuDeMethylene", "Cat1", "Denaturation", "ControleAmont", "DEC-AET-13"],
        "preconditions": "Sous-produits animaux issus de la chaîne d'abattage industrielle agréée.",
        "flow": [
            "Ségrégation immédiate des Matériels à Risque Spécifié (MRS) : crâne, encéphale, yeux et moelle épinière des ruminants.",
            "Classification obligatoire en Sous-Produits de Catégorie 1 (risque maximal de transmission d'EST).",
            "Dénaturation chimique par pulvérisation d'une solution de bleu de méthylène à 0,5 % pour marquer visuellement la chair.",
            "Émission du Document Commercial (Commercial Document) officiel AFSCA avec code QR sécurisé (contrôle amont déclaratif, DEC-AET-13).",
            "Stérilisation Méthode 1 préalable obligatoire avant expédition en cimenterie ou réacteur biodiesel."
        ],
        "postconditions": "Flux MRS marqué de manière indélébile et tracé sous contrôle étatique.",
        "legal": "Règlement (CE) n° 999/2001 (annexe V - spécifications des Matériels à Risque Spécifié MRS) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "industrial",
            "deviceLabel": "Terminal Terrain DNF / AFSCA • Contrôleur MRS & Dénaturation Bleu (IP68)",
            "formFields": [
                {"label": "Nature des Matières", "name": "mrs_nature", "type": "text", "value": "Matériels à Risque Spécifié (Crâne, encéphale, moelle)", "placeholder": "MRS", "badge": "Cat 1 MRS", "required": False},
                {"label": "Agent de Dénaturation", "name": "dye_agent", "type": "text", "value": "Solution de Bleu de Méthylène à 0,5% pulvérisée", "placeholder": "Dénaturation", "badge": "Bleu 0.5%", "required": True},
                {"label": "Document Commercial AFSCA", "name": "com_doc_id", "type": "text", "value": "DOC-COMM-2026-MRS-49 (Code QR Sécurisé)", "placeholder": "Document", "badge": "AFSCA Officiel", "required": False},
                {"label": "Destination Exclusive", "name": "mrs_destination", "type": "text", "value": "Combustion en Cimenterie / Biodiesel Industriel", "placeholder": "Destination", "badge": "Zéro Alimentation", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_validate_denaturation", "label": "Valider la Dénaturation & Émettre Document Commercial", "role": "primary", "state": "idle", "icon": "🔵"},
                {"id": "btn_inspect_spray", "label": "Contrôler Pression Rampe de Pulvérisation", "role": "secondary", "state": "idle", "icon": "🚿"}
            ],
            "validationMsg": {
                "title": "Lot MRS Dénaturé au Bleu de Méthylène 0,5%",
                "badge": "Document Commercial Scellé",
                "detail": "Coloration indélébile validée. Stérilisation Méthode 1 imposée avant cimenterie."
            },
            "errorCase": {
                "code": "ERR_SRM_NOT_DENATURED",
                "title": "Dénaturation au Bleu Insuffisante ou Absente",
                "condition": "Concentration en bleu de méthylène inférieure à 0,5% ou pulvérisation incomplète des surfaces.",
                "message": "REJET RÉGLEMENTAIRE SÉVÈRE : Les Matériels à Risque Spécifié n'ont pas été dénaturés au bleu de manière indélébile. Interdiction de transport.",
                "remediation": "Réexécuter la pulvérisation de solution de bleu à 0,5% jusqu'à imprégnation visuelle complète avant émission du document."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Benne MRS Triée en Attente de Pulvérisation",
                    "caption": "Matières à Risque Spécifié isolées. La rampe de bleu de méthylène est prête.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Activation de la Rampe & Pulvérisation Indélébile",
                    "triggerName": "Enclenchement de la pompe de bleu de méthylène 0,5% sous 4 bars",
                    "caption": "Coloration intense et immédiate de l'ensemble des tissus cérébraux en bleu vif.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Génération du Document Commercial AFSCA Sécurisé",
                    "progress": 92,
                    "caption": "Encodage du QR code officiel de transport vers la cimenterie conventionnée.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Lot MRS Dénaturé & Prêt pour Stérilisation Méthode 1",
                    "status": "success",
                    "caption": "Traçabilité infaillible. Le lot marqué ne pourra jamais pénétrer la chaîne alimentaire.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-412",
        "title": "Évaluation Algorithmique Pure par The Iron Gate (G0 à G9, Anti-Prion)",
        "cat": "Validation Algorithmique",
        "actor": "The Iron Gate (Moteur Déterministe)",
        "platforms": ["Node.js / Core Engine", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["IronGate", "AntiPrion", "G0-G9", "FeedBan", "Whitelist"],
        "preconditions": "Revendication de lot complète soumise pour autorisation de signature.",
        "flow": [
            "G0 : Destination & Spécification des cibles (whitelist d'usages autorisés, cibles obligatoires si alimentation).",
            "G1 : Taxonomie & Lignage (résolution stricte TaxID NCBI dans le snapshot officiel, default-deny, interdiction rang > espèce).",
            "G2 : Protection Restes Humains (rejet absolu en filière générale ; en mémoire forestière : démonstrateur de faisabilité prospectif — option non autorisée par le droit positif actuel sous DEC-AET-15).",
            "G3 : Catégories & Substrats (Catégories 1, 2, 3, material classes, dérogation souveraine DEC-AET-05 pour animaux de compagnie).",
            "G4 : Dépistage Pentobarbital (Animaux de compagnie : test immunochromatographique qualitatif LFA négatif obligatoire [lignes C et T visibles] ; rejet si positif ou non testé).",
            "G5 : Feed-Ban Source Ruminant (interdiction stricte de protéines de ruminants en alimentation).",
            "G6 : Feed-Ban Cible Ruminant (interdiction stricte de nourrir des ruminants avec des PAT).",
            "G7 : LA RÈGLE D'OR ANTI-PRION / ANTI-CANNIBALISME : interdiction mathématique absolue de nourrir une espèce avec ses propres protéines (FEED_BAN_INTRA_SPECIES_VIOLATION).",
            "G8 : Feed-Ban Groupes & Espèces (vérification des filières intra-groupe et destinations positives).",
            "G9 : Traitement Sanitaire Requis & Preuve (Méthode 1 [133°C, 3 bar, 20 min] pour Cat 1/2 ou pasteurisation [70°C, 60 min] sous dérogation mémorielle DEC-AET-05, avec condensat SHA-256 de preuve).",
            "Nota : Les contrôles amont (PCR Sciensano, boucles Sanitel, documents commerciaux MRS abattoir) sont vérifiés en amont dans la chaîne documentaire déclarative (DEC-AET-13)."
        ],
        "postconditions": "Verdict déterministe émis : AUTHORISED (signature_permitted = true) ou BLOCKED avec motifs normalisés.",
        "legal": "Spécification AeterniTrak AET-SPEC-PRION-001 et Règlement (CE) n° 999/2001 (Feed-ban) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "industrial",
            "deviceLabel": "Terminal Terrain DNF / AFSCA • Oracle Algorithmique The Iron Gate (G0-G9)",
            "formFields": [
                {"label": "Portes G0-G3 (Destination, Taxon, Humain, Substrat)", "name": "gates_g0_g3", "type": "text", "value": "100% VALIDE (Format CBOR, TaxID résolu, Zéro humain, Substrat conforme)", "placeholder": "G0-G3", "badge": "G0-G3 OK", "required": False},
                {"label": "Porte G4 (Dépistage Pentobarbital)", "name": "gate_g4", "type": "text", "value": "VALIDE (LFA négatif qualitatif, lignes C et T visibles)", "placeholder": "G4", "badge": "G4 OK", "required": False},
                {"label": "Portes G5-G6 (Feed-Ban Ruminants Source & Cible)", "name": "gates_g5_g6", "type": "text", "value": "VALIDE (Zéro ruminant en source ni en cible alimentaire)", "placeholder": "G5-G6", "badge": "G5-G6 OK", "required": False},
                {"label": "Porte G7 (RÈGLE D'OR ANTI-PRION)", "name": "gate_g7", "type": "text", "value": "ZÉRO RECYCLAGE INTRA-ESPÈCE (G7 Mathématiquement Satisfaite)", "placeholder": "G7", "badge": "ANTI-PRION OK", "required": False},
                {"label": "Porte G8 (Feed-Ban Groupes & Espèces)", "name": "gate_g8", "type": "text", "value": "VALIDE (Filières intra-groupe autorisées respectées)", "placeholder": "G8", "badge": "G8 OK", "required": False},
                {"label": "Porte G9 (Traitement Sanitaire & Preuve)", "name": "gate_g9", "type": "text", "value": "VALIDE (Méthode 1 ou Pasteurisation 70°C/1h, Preuve SHA-256)", "placeholder": "G9", "badge": "G9 OK", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_evaluate_iron_gate", "label": "Évaluer The Iron Gate (G0 à G9)", "role": "primary", "state": "idle", "icon": "🛡️"},
                {"id": "btn_simulate_intra_species", "label": "Simuler Violation Règle G7 Anti-Prion", "role": "danger", "state": "idle", "icon": "☣️"}
            ],
            "validationMsg": {
                "title": "VERDICT THE IRON GATE : AUTHORISED",
                "badge": "10/10 Portes Validées",
                "detail": "signature_permitted = true. Zéro risque de prions ni de recyclage intra-espèce."
            },
            "errorCase": {
                "code": "ERR_PRION_INTRA_SPECIES",
                "title": "Violation de la Règle d'Or Anti-Prion (Porte G7)",
                "condition": "Revendication associant des protéines issues d'une espèce à la nourriture de cette même espèce (ex: Porc vers Porc).",
                "message": "REJET INVIOLABLE THE IRON GATE (Porte G7) : Recyclage intra-espèce détecté. Violation absolue du feed-ban européen et du verrou anti-prion. Signature formellement refusée (signature_permitted = false).",
                "remediation": "Aiguiller impérativement le lot vers une destination exempte de risque intra-espèce ou vers la valorisation énergétique."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Revendication de Lot Soumise aux 10 Portes",
                    "caption": "Revendication prête. Les 10 portes de sécurité G0 à G9 sont en attente d'évaluation.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Lancement du Banc de Test des 10 Portes de Sécurité",
                    "triggerName": "Clic sur 'Évaluer The Iron Gate' et exécution déterministe",
                    "caption": "Évaluation instantanée séquentielle des règles positives G0, G1, G2, G3, G4, G5, G6, G7, G8, G9.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Analyse de Matrice : 10/10 Portes Franchies sans Déviation",
                    "progress": 98,
                    "caption": "Toutes les conditions de la liste blanche positive sont rigoureusement remplies.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Verdict Solennel : AUTHORISED (Signature Autorisée)",
                    "status": "success",
                    "caption": "The Iron Gate délivre son blanc-seing. Le lot peut être cryptographiquement scellé.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-413",
        "title": "Émission du Certificat de Lot Signé Ed25519 (AET-SPEC-CERT-001)",
        "cat": "Cryptographie Filière",
        "actor": "The Iron Gate & Autorité de Conformité",
        "platforms": ["Node.js / Core Engine", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["Certificat", "Ed25519", "COSE_Sign1", "AET-SPEC-CERT-001", "HSM"],
        "preconditions": "The Iron Gate a délivré un verdict formellement AUTHORISED.",
        "flow": [
            "Calcul du hachage SHA-256 canonique JCS de la revendication de lot (Clé 1).",
            "Insertion du statut littéral 'AUTHORISED' (Clé 2) et de l'horodatage UNIX Tag 1 (Clé 3).",
            "Insertion de l'empreinte du snapshot taxonomique (Clé 4) et de la version des règles v1.4 (Clé 5).",
            "Intégration de l'empreinte de la dérogation forestière mémorielle DEC-AET-05 si applicable (Clé 6).",
            "Encodage CBOR déterministe et signature cryptographique par la clé Ed25519 officielle de l'autorité de conformité.",
            "Génération de l'enveloppe COSE_Sign1 (content type : application/aeternitrak-batch-claim+cbor)."
        ],
        "postconditions": "Certificat de lot infalsifiable délivré aux acteurs de la filière et régulateurs.",
        "legal": "Spécification technique formelle AET-SPEC-CERT-001 et Règlement (UE) 2021/1372 (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "industrial",
            "deviceLabel": "Terminal Terrain DNF / AFSCA • Autorité de Certification de Lot Ed25519",
            "formFields": [
                {"label": "Statut de Conformité", "name": "cert_status", "type": "text", "value": "AUTHORISED (Clé 2 du Certificat)", "placeholder": "Statut", "badge": "AUTHORISED", "required": False},
                {"label": "Algorithme de Scellement", "name": "cert_alg", "type": "text", "value": "Ed25519 (alg: -8, RFC 8032)", "placeholder": "Algorithme", "badge": "Ed25519", "required": False},
                {"label": "Empreinte Revendication JCS", "name": "claim_jcs_hash", "type": "text", "value": "7f3a9b1c...d84e (Clé 1 SHA-256)", "placeholder": "Hash JCS", "badge": "SHA-256", "required": False},
                {"label": "Type MIME COSE Protégé", "name": "cose_typ", "type": "text", "value": "application/aeternitrak-batch-claim+cbor (RFC 9596)", "placeholder": "typ", "badge": "Protégé", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_issue_batch_cert", "label": "Signer & Émettre le Certificat de Conformité", "role": "primary", "state": "idle", "icon": "🔏"},
                {"id": "btn_download_cbor_cert", "label": "Télécharger Certificat CBOR Déterministe", "role": "secondary", "state": "idle", "icon": "💾"}
            ],
            "validationMsg": {
                "title": "Certificat de Lot Signé Ed25519 Émis",
                "badge": "AET-SPEC-CERT-001 Conforme",
                "detail": "Enveloppe COSE_Sign1 générée avec sceau d'autorité infalsifiable. Prêt pour audit."
            },
            "errorCase": {
                "code": "ERR_BATCH_CERT_SIGN_FAILED",
                "title": "Refus de Signature : Revendication Non Autorisée",
                "condition": "Tentative d'émission d'un certificat sur un lot ayant échoué à une des portes de The Iron Gate.",
                "message": "REFUS DE SIGNATURE ABSOLU : L'oracle cryptographique est matériellement incapable d'apposer son sceau sur une revendication non AUTHORISED.",
                "remediation": "Corriger les non-conformités sanitaires identifiées par The Iron Gate avant toute nouvelle tentative."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Verdict AUTHORISED Reçu, Prêt pour Signature",
                    "caption": "The Iron Gate a validé le lot. Le module HSM prépare la structure COSE_Sign1.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Calcul du Hash Canonique & Construction de l'Enveloppe",
                    "triggerName": "Clic sur 'Signer & Émettre le Certificat de Conformité'",
                    "caption": "Injection des 6 clés canoniques du certificat et signature matérielle Ed25519.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Encodage CBOR Déterministe & Signature COSE_Sign1",
                    "progress": 98,
                    "caption": "Génération de l'enveloppe CBOR avec Tag 18 et type application/aeternitrak-batch-claim+cbor.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Certificat de Lot Infalsifiable Émis",
                    "status": "success",
                    "caption": "Passeport sanitaire officiel délivré. Les transporteurs et régulateurs peuvent auditer le lot.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-414",
        "title": "Double Audit Réglementaire AFSCA / DNF Hors-Ligne",
        "cat": "Audit & Régulateurs",
        "actor": "Inspecteur AFSCA & Contrôleur DNF",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["Audit", "AFSCA", "DNF", "HorsLigne", "DoubleControle", "Preuve"],
        "preconditions": "Contrôle inopiné d'un chargement de protéines d'insectes transformées (PAT) ou d'amendements forestiers.",
        "flow": [
            "L'inspecteur scanne le certificat cryptographique via son terminal mobile de contrôle.",
            "Double vérification autonome et instantanée exécutée sans aucune connexion réseau :",
            "1. Vérification mathématique de la signature Ed25519 par rapport à la clé publique de l'autorité AeterniTrak.",
            "2. Réévaluation intégrale en local des règles The Iron Gate G0 à G9 sur la revendication originale.",
            "Constat infaillible de l'absence totale de prions, de barbituriques et de recyclage illicite.",
            "Délivrance de l'attestation de conformité réglementaire immédiate."
        ],
        "postconditions": "Sécurité sanitaire et légale démontrée à 100% auprès des autorités publiques.",
        "legal": "Règlement (UE) 2017/625 (contrôles officiels le long de la chaîne agroalimentaire) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "industrial",
            "deviceLabel": "Terminal Terrain DNF / AFSCA • Console d'Audit Réglementaire Hors-Ligne",
            "formFields": [
                {"label": "Inspecteur Officiel", "name": "inspector_name", "type": "text", "value": "Inspecteur AFSCA & Garde DNF Assermenté", "placeholder": "Inspecteur", "badge": "Autorité Étatique", "required": False},
                {"label": "Mode d'Exécution", "name": "audit_mode", "type": "text", "value": "100% HORS-LIGNE (Zéro connexion réseau requise)", "placeholder": "Mode", "badge": "Autonome", "required": False},
                {"label": "Vérification 1 : Signature Ed25519", "name": "audit_sig_status", "type": "text", "value": "AUTHENTIQUE (Clé d'autorité AeterniTrak reconnue)", "placeholder": "Signature", "badge": "Vérifié", "required": False},
                {"label": "Vérification 2 : The Iron Gate G0-G9", "name": "audit_gate_status", "type": "text", "value": "10/10 PORTES VALIDÉES EN LOCAL (Zéro déviation)", "placeholder": "The Iron Gate", "badge": "Conforme", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_run_offline_audit", "label": "Lancer le Double Audit Réglementaire Hors-Ligne", "role": "primary", "state": "idle", "icon": "⚖️"},
                {"id": "btn_export_audit_pv", "label": "Éditer l'Attestation de Contrôle AFSCA (PDF)", "role": "secondary", "state": "idle", "icon": "📄"}
            ],
            "validationMsg": {
                "title": "Double Audit Réglementaire Réussi à 100%",
                "badge": "Conforme AFSCA / DNF",
                "detail": "Absence totale de prions, de barbituriques et de recyclage intra-espèce démontrée."
            },
            "errorCase": {
                "code": "ERR_AUDIT_REGULATORY_NON_COMPLIANT",
                "title": "Échec de Conformité Réglementaire Lors de l'Audit",
                "condition": "Signature de lot non reconnue ou réévaluation locale de The Iron Gate rejetant une porte.",
                "message": "SAISIE SANITAIRE IMMÉDIATE : Le certificat présenté est invalide ou les règles sanitaires The Iron Gate sont violées. Blocage du chargement.",
                "remediation": "Mettre le chargement immédiatement sous séquestre judiciaire et ordonner l'enquête sanitaire approfondie."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Inspecteur Face au Chargement avec Terminal Hors-Ligne",
                    "caption": "Contrôle inopiné sur route ou en usine. Le certificat CBOR est scanné.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Lancement Instantané de la Double Vérification Locale",
                    "triggerName": "Clic sur 'Lancer le Double Audit' sans aucune connexion Internet",
                    "caption": "Exécution conjointe de la vérification cryptographique et de l'oracle sanitaire.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Réévaluation Complète des Règles G0-G9 en 80 ms",
                    "progress": 98,
                    "caption": "Preuve mathématique absolue de l'absence de prions, barbituriques et recyclage illicite.",
                    "screenHtml": """
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
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Attestation de Conformité Réglementaire Délivrée",
                    "status": "success",
                    "caption": "Contrôle réussi avec félicitations. Le chargement circule en toute légalité.",
                    "screenHtml": """
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
                    </div>"""
                }
            }
        }
    }
]

# =============================================================================
# CHAÎNE ÉVÉNEMENTIELLE COMPLÈTE DE TRAÇABILITÉ POST-MORTEM (ÉVÉNEMENTS 1 À 6)
# =============================================================================
TRACEABILITY_EVENTS = [
    {
        "step": 1,
        "id": "EVT-01",
        "code": "EVT-01-CONSTAT",
        "name": "Constat de Décès & Déclaration Initiale",
        "short_title": "1. Constat & Scellé Ed25519",
        "icon": "📋",
        "stage_label": "Événement 1 / 6 • Constat & Pose du Scellé",
        "actor": "Médecin Certificateur / Vétérinaire Sanitaire / Garde DNF",
        "actor_role": "Officier de Santé / Autorité Agréée",
        "actor_badge": "INAMI / AFSCA #VET-BEL-84912 • Badge DNF #WL-7401",
        "timestamp_iso": "2026-10-05T08:15:00.000Z",
        "gps_coords": "50.6333° N, 5.5667° E (Liège, Sart-Tilman) [±0.8 m RTK]",
        "seal_id": "SCELL-2026-BEL-0982-NFC",
        "seal_status": "Scellé Inviolable Posé & Actif (Ed25519 alg: -8)",
        "seal_status_code": "SCEL_INITIALISE_NON_ROMPU",
        "cold_chain_temp": "12.4°C (Température ambiante initiale)",
        "temp_status": "ambient",
        "depouille_id": "DEP-2026-BEL-99201",
        "identity_name": "Adrien de Valcourt (ou Canis familiaris TaxID 9615)",
        "vehicle_reg": "En attente d'assignation transporteur agréé",
        "cell_id": "Non assignée (Étape amont)",
        "pacemaker_status": "Contrôle impératif requis avant toute incinération ou sarcomusation",
        "lfa_status": "Écouvillonnage programmé à l'admission",
        "thermal_status": "En attente d'orientation filière",
        "iron_gate_status": "G0 à G9 initialisées (Attente saisie complète)",
        "crypto_signature": "ed25519:7b8a1c94d0e2f5819a... (Pose du scellé NFC/QR Ed25519)",
        "summary": "Constat médical de fin de vie, horodatage certifié RFC 3339, géolocalisation par balise RTK, vérification de l'identité du défunt ou de l'animal, et scellement physique et cryptographique immédiat par scellé inviolable NFC/QR à signature Ed25519.",
        "form_fields": [
            {"label": "Identifiant Unique Dépouille", "name": "depouille_id", "type": "text", "value": "DEP-2026-BEL-99201", "badge": "RFID / QR"},
            {"label": "Identité Défunt / Espèce", "name": "identity_name", "type": "text", "value": "Adrien de Valcourt (ou Canis familiaris TaxID 9615)", "badge": "Identité Certifiée"},
            {"label": "Officier Déclarant", "name": "officer_name", "type": "text", "value": "Dr. Marc Laurent (Vétérinaire Sanitaire / Médecin)", "badge": "Agréé AFSCA/INAMI"},
            {"label": "Coordonnées GPS RTK", "name": "gps_location", "type": "text", "value": "50.6333° N, 5.5667° E (Liège, Région Wallonne)", "badge": "Précision 0.8m"},
            {"label": "Identifiant Scellé Inviolable", "name": "seal_number", "type": "text", "value": "SCELL-2026-BEL-0982-NFC", "badge": "Ed25519 Actif"}
        ],
        "action_label": "⚡ Sceller la Dépouille & Confirmer le Constat",
        "linked_ucs": ["UC-401", "UC-406", "UC-409"],
        "legal_basis": "Règlement (CE) n° 1069/2009 art. 21 & Arrêté royal du 27 avril 2007 (référence à confirmer par un juriste)"
    },
    {
        "step": 2,
        "id": "EVT-02",
        "code": "EVT-02-TRANSPORT",
        "name": "Prise en Charge & Transport Sécurisé de la Dépouille",
        "short_title": "2. Transport Sécurisé (2-4°C)",
        "icon": "🚐",
        "stage_label": "Événement 2 / 6 • Logistique & Chaîne du Froid",
        "actor": "Chauffeur Funéraire / Transporteur Sanitaire Agréé",
        "actor_role": "Conducteur Spécialisé Véhicule Agréé",
        "actor_badge": "Agrément Transport AFSCA #TRA-WAL-2026-081",
        "timestamp_iso": "2026-10-05T09:20:00.000Z",
        "gps_coords": "50.6120° N, 5.5340° E (Transit E25 / Rocade Sud)",
        "seal_id": "SCELL-2026-BEL-0982-NFC",
        "seal_status": "Scellé Intact sous Surveillance Télématique (Non Rompu)",
        "seal_status_code": "SCEL_INTACT_EN_TRANSIT",
        "cold_chain_temp": "+3.2°C (Chaîne du Froid Conforme [Consigne 2.0°C - 4.0°C])",
        "temp_status": "cold_ok",
        "depouille_id": "DEP-2026-BEL-99201",
        "identity_name": "Adrien de Valcourt (ou Canis familiaris TaxID 9615)",
        "vehicle_reg": "Fourgon Funéraire / Sanitaire Agréé 1-AFR-842 (Frigo bi-température)",
        "cell_id": "Caisson frigorifique isotherme #02",
        "pacemaker_status": "Non perturbé en transit",
        "lfa_status": "En cours de transit",
        "thermal_status": "+3.2°C régulé",
        "iron_gate_status": "Jalon transport certifié",
        "crypto_signature": "ed25519:8c9f2d1e3a4b67... (Émargement numérique chauffeur)",
        "summary": "Prise en charge dans un véhicule funéraire/sanitaire agréé, monitoring télématique continu de la température de la chaîne du froid entre 2°C et 4°C, étapes de transit géolocalisées avec horodatage balises GPS et émargement numérique du chauffeur.",
        "form_fields": [
            {"label": "Immatriculation Véhicule Agréé", "name": "vehicle_id", "type": "text", "value": "1-AFR-842 (Agrément AFSCA / SPW Cat 1/2)", "badge": "Agrément Vérifié"},
            {"label": "Chauffeur Titulaire", "name": "driver_name", "type": "text", "value": "Jean-Pierre Dumont (Permis transport funéraire)", "badge": "Émargement Prêt"},
            {"label": "Température Caisson Froid", "name": "temp_sensor", "type": "text", "value": "+3.2°C (Consigne cible 2°C - 4°C)", "badge": "Conforme ❄️"},
            {"label": "Statut Surveillance Scellé", "name": "seal_check", "type": "text", "value": "Intact • 0 choc accélérométrique détecté", "badge": "Non Rompu 🔒"},
            {"label": "Trajet & Balise Transit", "name": "transit_route", "type": "text", "value": "Lieu de décès -> Centre Logistique Liège (22.4 km)", "badge": "GPS Connecté"}
        ],
        "action_label": "⚡ Valider l'Étape de Transport & Émargement Chauffeur",
        "linked_ucs": ["UC-401", "UC-406", "UC-409"],
        "legal_basis": "Règlement (CE) n° 1069/2009 art. 21 (traçabilité et collecte) & Arrêté du Gouvernement wallon (référence à confirmer par un juriste)"
    },
    {
        "step": 3,
        "id": "EVT-03",
        "code": "EVT-03-ADMISSION",
        "name": "Admission & Réception à l'Unité / Salon Funéraire",
        "short_title": "3. Admission & Réception",
        "icon": "⚖️",
        "stage_label": "Événement 3 / 6 • Réception & Conservation",
        "actor": "Opérateur d'Admission / Maître de Cérémonie / Salon",
        "actor_role": "Gestionnaire d'Unité Funéraire & Sanitaire",
        "actor_badge": "Habilitation Funéraire AeterniTrak #ADM-042",
        "timestamp_iso": "2026-10-05T10:05:00.000Z",
        "gps_coords": "50.6412° N, 5.5721° E (Unité Centrale AeterniTrak Liège)",
        "seal_id": "SCELL-2026-BEL-0982-NFC",
        "seal_status": "Scellé Vérifié Non Rompu (Scan NFC OK • Ed25519 Validé)",
        "seal_status_code": "SCEL_VERIFIE_NON_ROMPU",
        "cold_chain_temp": "+2.8°C (Cellule Frigorifique #B4 Assignée)",
        "temp_status": "cold_ok",
        "depouille_id": "DEP-2026-BEL-99201",
        "identity_name": "Adrien de Valcourt (ou Canis familiaris TaxID 9615)",
        "vehicle_reg": "Arrivée validée véhicule 1-AFR-842",
        "cell_id": "Cellule Froide Individuelle #B4 (Régulée +2.5°C à +3.5°C)",
        "pacemaker_status": "Alerte fiche médicale : Stimulateur présent",
        "lfa_status": "Écouvillon préparé pour analyse LFA",
        "thermal_status": "+2.8°C en cellule",
        "iron_gate_status": "Porte G3 (Substrat/Catégorie) engagée",
        "crypto_signature": "ed25519:3e4f5a6b7c8d90... (Reçu d'admission horodaté)",
        "summary": "Arrivée à l'unité de destination : scan sans contact du scellé inviolable, vérification de non-rupture de scellé, pesée métrologique certifiée sur balance étalonnée classe III, et assignation automatique d'une cellule réfrigérée de conservation.",
        "form_fields": [
            {"label": "Contrôle Scellé NFC à l'Arrivée", "name": "scan_seal_result", "type": "text", "value": "SCELL-2026-BEL-0982-NFC (Signature Valide)", "badge": "Zéro Altération"},
            {"label": "Pesée Métrologique Dépouille", "name": "measured_weight", "type": "text", "value": "32.45 kg (Balance Étalonnée Classe III)", "badge": "Poids Certifié"},
            {"label": "Cellule de Conservation Assignée", "name": "assigned_cell", "type": "text", "value": "Cellule Frigorifique #B4 (+2.8°C)", "badge": "Régulation OK"},
            {"label": "Contrôle Visuel & Sanitaire", "name": "visual_sanitary", "type": "text", "value": "Aucune souillure externe, état intègre", "badge": "Conforme"},
            {"label": "Orientation Filière Validée", "name": "target_channel", "type": "text", "value": "Profil 1 Compagnie (Catégorie 1 Mémorielle)", "badge": "Ségrégation Sas"}
        ],
        "action_label": "⚡ Confirmer l'Admission & Verrouiller la Cellule #B4",
        "linked_ucs": ["UC-402", "UC-410"],
        "legal_basis": "Décret wallon sur les funérailles et sépultures & Règlement (CE) n° 1069/2009 (références à confirmer par un juriste)"
    },
    {
        "step": 4,
        "id": "EVT-04",
        "code": "EVT-04-PREPARATION",
        "name": "Préparation Sanitaire & Contrôles Amonts",
        "short_title": "4. Contrôles Amonts (Pacemaker & LFA)",
        "icon": "🩺",
        "stage_label": "Événement 4 / 6 • Sécurité Chirurgicale & Biologique",
        "actor": "Thanatopracteur Agréé / Vétérinaire / Biologiste",
        "actor_role": "Praticien Spécialiste Santé & Sécurité",
        "actor_badge": "Certificat Thanatopraxie #BE-TH-084 • BioLab #LAB-902",
        "timestamp_iso": "2026-10-05T11:30:00.000Z",
        "gps_coords": "50.6412° N, 5.5721° E (Salle de Préparation Sanitaire)",
        "seal_id": "SCELL-2026-BEL-0982-NFC",
        "seal_status": "Scellé Temporairement Ouvert sous Supervision Stérile",
        "seal_status_code": "SCEL_OUVERT_CONTROLE_STERILE",
        "cold_chain_temp": "+14.0°C (Ambiante salle technique stérile)",
        "temp_status": "sterile",
        "depouille_id": "DEP-2026-BEL-99201",
        "identity_name": "Adrien de Valcourt (ou Canis familiaris TaxID 9615)",
        "vehicle_reg": "Non applicable (En atelier technique)",
        "cell_id": "Cellule Froide #B4 -> Table de soins #01",
        "pacemaker_status": "EXÉRÈSE EFFECTUÉE : Stimulateur retiré & neutralisé",
        "lfa_status": "DÉPISTAGE LFA CONFORME (Lignes C+T Visibles = Négatif Pentobarbital)",
        "thermal_status": "Préparation validée pour traitement",
        "iron_gate_status": "Porte G4 (Pentobarbital) VALIDÉE",
        "crypto_signature": "ed25519:9a8b7c6d5e4f32... (Attestation toxicologique scellée)",
        "summary": "Préparation sanitaire amont obligatoire : exérèse validée du stimulateur cardiaque (pacemaker) avant toute incinération ou traitement thermique, dépistage toxicologique qualitatif LFA du pentobarbital (cassette C+T visibles = absence de produit létal, conforme), et prélèvements PCR épizooties selon le profil de dépouille.",
        "form_fields": [
            {"label": "Exérèse Stimulateur Cardiaque", "name": "pacemaker_excision", "type": "select", "value": "Explantation Validée • Dispositif Medtronic S/N 84920 Retiré", "badge": "Sécurité Incendie/Explosion"},
            {"label": "Test LFA Pentobarbital (Barbituriques)", "name": "lfa_pento_result", "type": "select", "value": "NÉGATIF / CONFORME (Lignes C et T Visibles)", "badge": "Conforme Sans Résidu"},
            {"label": "Dépistage Épizooties (PCR)", "name": "pcr_screening", "type": "text", "value": "Non requis pour chien de compagnie (Prélèvement conservé)", "badge": "Profil 1 Exclusif"},
            {"label": "Dénaturation Chimique (si Cat 1 MRS)", "name": "denaturation_blue", "type": "text", "value": "Sans objet pour Profil 1 (Réservé abattoir MRS)", "badge": "Ligne Mémorielle"},
            {"label": "Feu Vert Sanitaire Amont", "name": "upstream_clearance", "type": "text", "value": "ACCORDÉ : Autorisation de passage en bioconversion", "badge": "Porte G4 Ouverte"}
        ],
        "action_label": "⚡ Valider les Contrôles Amonts & Signer l'Exérèse",
        "linked_ucs": ["UC-403", "UC-407", "UC-411"],
        "legal_basis": "Décret wallon (stimulateurs cardiaques) & Notice officielle kits LFA AFSCA (références à confirmer par un juriste)"
    },
    {
        "step": 5,
        "id": "EVT-05",
        "code": "EVT-05-BIOCONVERSION",
        "name": "Bioconversion / Sarcomusation & Traitement Thermique",
        "short_title": "5. Bioconversion & Thermique",
        "icon": "🪰",
        "stage_label": "Événement 5 / 6 • Procédé Biologique & Stérilisation",
        "actor": "Bio-Ingénieur de Procédé / Opérateur Autoclave HP",
        "actor_role": "Responsable Unité Biologique & Thermique",
        "actor_badge": "Superviseur Bioréacteur AeterniCore #BIO-2026-09",
        "timestamp_iso": "2026-10-05T14:00:00.000Z",
        "gps_coords": "50.6412° N, 5.5721° E (Unité de Bioconversion & Bioréacteurs)",
        "seal_id": "SCELL-2026-BEL-0982-NFC",
        "seal_status": "Sas Hermétique Réacteur Verrouillé sous Scellé",
        "seal_status_code": "SAS_BIOCONVERSION_SCELLE",
        "cold_chain_temp": "70.2°C (Pasteurisation continue 1h) / Méthode 1: 133°C, 3 bars",
        "temp_status": "heat_ok",
        "depouille_id": "DEP-2026-BEL-99201",
        "identity_name": "Adrien de Valcourt (ou Canis familiaris TaxID 9615)",
        "vehicle_reg": "Non applicable",
        "cell_id": "Bioréacteur Dédié Mémoriel #M-03",
        "pacemaker_status": "Explanté et consigné en amont",
        "lfa_status": "Conforme (Négatif vérifié)",
        "thermal_status": "Cycle thermique validé à 100%",
        "iron_gate_status": "Porte G9 (Traitement Thermique) VALIDÉE",
        "crypto_signature": "ed25519:1a2b3c4d5e6f78... (Télémétrie P-T-t scellée)",
        "summary": "Introduction dans le sas hermétique de bioconversion dédié par les larves d'Hermetia illucens, ségrégation stricte des flux pour interdire tout mélange, et application du traitement thermique légal : pasteurisation continue à 70°C pendant 1h continue sous dérogation DEC-AET-05 mémorielle forestière exclusive, ou stérilisation Méthode 1 européenne (133°C, 3 bars, 20 min en cœur de matière) pour les autres filières.",
        "form_fields": [
            {"label": "Bioréacteur Hermetia illucens", "name": "bioreactor_id", "type": "text", "value": "Bioréacteur Hermétique Mémoriel #M-03 (Larves 343691)", "badge": "Ségrégation 100%"},
            {"label": "Traitement Thermique Appliqué", "name": "thermal_protocol", "type": "select", "value": "Pasteurisation Continue (70°C, 1 heure continue) - DEC-AET-05", "badge": "Dérogation Validée"},
            {"label": "Température Cœur de Matière Mesurée", "name": "core_temp", "type": "text", "value": "70.4°C en continu pendant 62 minutes", "badge": "Seuil Dépassé OK"},
            {"label": "Pression Autoclave (si Méthode 1)", "name": "chamber_pressure", "type": "text", "value": "Atmosphérique (ou 3.1 bars absolus si Méthode 1)", "badge": "Manomètre Conforme"},
            {"label": "Séparation Frass & Reliques Minérales", "name": "separation_status", "type": "text", "value": "Criblage doux achevé, éléments minéralisés isolés", "badge": "Criblage 100%"}
        ],
        "action_label": "⚡ Certifier le Traitement Thermique & Sceller les Reliques",
        "linked_ucs": ["UC-402", "UC-404", "UC-408"],
        "legal_basis": "Règlement (CE) n° 142/2011 annexe IV (Méthode 1) & Arbitrage Kudoro DEC-AET-05 (références à confirmer par un juriste)"
    },
    {
        "step": 6,
        "id": "EVT-06",
        "code": "EVT-06-CLOTURE",
        "name": "Clôture de Traçabilité, The Iron Gate & Remise Mémorielle",
        "short_title": "6. Clôture, The Iron Gate & Remise",
        "icon": "🕊️",
        "stage_label": "Événement 6 / 6 • The Iron Gate & Remise Solennelle",
        "actor": "The Iron Gate Oracle / Responsable Qualité / Famille",
        "actor_role": "Autorité Cryptographique & Conseiller Funéraire",
        "actor_badge": "Master Key Ed25519 #CONF-AET-01 • Sceau Le Pax Funèbre",
        "timestamp_iso": "2026-10-05T16:45:00.000Z",
        "gps_coords": "50.6412° N, 5.5721° E (Salon Solennel de Remise)",
        "seal_id": "CERT-2026-LOT-0084-ED25519",
        "seal_status": "Certificat de Lot Signé Ed25519 (AET-SPEC-CERT-001 Émis)",
        "seal_status_code": "LOT_SIGNE_ET_REMIS",
        "cold_chain_temp": "Température ambiante salon d'hommage",
        "temp_status": "final_ok",
        "depouille_id": "DEP-2026-BEL-99201",
        "identity_name": "Adrien de Valcourt (ou Canis familiaris TaxID 9615)",
        "vehicle_reg": "Non applicable",
        "cell_id": "Urne Mémorielle Scellée #URN-2026-084",
        "pacemaker_status": "Clôturé (Explantation archivée)",
        "lfa_status": "Clôturé (Conformité attestée)",
        "thermal_status": "Clôturé (70°C/1h certifié)",
        "iron_gate_status": "VERDICT THE IRON GATE : AUTHORISED (10/10 Portes Validées)",
        "crypto_signature": "ed25519:6f5e4d3c2b1a89... (Signature finale officielle du lot)",
        "summary": "Évaluation algorithmique pure et inviolable par l'oracle The Iron Gate (G0 à G9 : vérification stricte de la règle d'or anti-prion interdisant tout recyclage intra-espèce), scellement cryptographique Ed25519 du certificat de lot AET-SPEC-CERT-001 (COSE_Sign1), séparation méticuleuse des reliques et remise solennelle de l'urne cinéraire ou de l'amendement forestier à la famille.",
        "form_fields": [
            {"label": "Évaluation The Iron Gate (G0 à G9)", "name": "iron_gate_verdict", "type": "text", "value": "AUTHORISED (Portes G0 à G9 Validées sans réserve)", "badge": "10/10 Infranchissable"},
            {"label": "Règle d'Or Anti-Prion (Porte G7)", "name": "anti_prion_rule", "type": "text", "value": "CONFORME : ZÉRO Recyclage Intra-Espèce Détecté", "badge": "Feed-Ban Strict"},
            {"label": "Certificat de Lot Officiel", "name": "batch_cert_id", "type": "text", "value": "AET-SPEC-CERT-001 #LOT-2026-B84 (Ed25519)", "badge": "Signature Inviolable"},
            {"label": "Destination des Reliques Mémorielles", "name": "relics_destination", "type": "select", "value": "Urne Cinéraire Noble & Arbre du Souvenir Forêt DNF (DEC-AET-05)", "badge": "Usage Mémoriel"},
            {"label": "Remise Solennelle à la Famille", "name": "family_handover", "type": "text", "value": "Effectuée avec procès-verbal d'hommage et carte PaxFunèbre", "badge": "Recueillement Garanti"}
        ],
        "action_label": "⚡ Émettre le Certificat de Lot Signé Ed25519 & Clôturer la Traçabilité",
        "linked_ucs": ["UC-405", "UC-412", "UC-413", "UC-414"],
        "legal_basis": "Règlement (CE) n° 999/2001 (anti-prion), Spécification AET-SPEC-CERT-001 & Arbitrage Kudoro DEC-AET-05"
    }
]
