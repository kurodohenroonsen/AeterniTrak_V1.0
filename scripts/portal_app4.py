#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeterniTrak V1.0 — Définition Complète des Micro Use-Cases pour App 4 : Filière & Traçabilité (UC-401 à UC-425)
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
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Saisie Déclarative Sanitel/CERISE →</button>
                      </div>
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-410",
        "title": "Saisie Déclarative & Attestation Sanitel / CERISE (Phase 1, DEC-AET-02)",
        "cat": "Interopérabilité & Registres (DEC-AET-02)",
        "actor": "Éleveur Déclarant & Vétérinaire Agréé",
        "platforms": ["Node.js / Core Engine", "Web Standard (PWA Hors-Ligne)"],
        "tags": ["Sanitel", "CERISE", "ARSIA", "Tracabilite", "SaisieDeclarative", "Attestation", "SHA-256", "ControleAmont", "DEC-AET-02", "DEC-AET-13"],
        "preconditions": "Numéro de boucle nationale Sanitel (BE xxxxxxxxx) et attestation vétérinaire de respect du temps d'attente médicamenteux disponibles.",
        "flow": [
            "Saisie du numéro d'identification Sanitel / boucle auriculaire officielle (format BE xxxxxxxxx) et du code d'exploitation agricole ARSIA/DGZ (DEC-AET-02).",
            "Téléversement du document d'attestation vétérinaire certifiant le respect strict du temps d'attente médicamenteux post-administration.",
            "Calcul instantané de l'empreinte cryptographique SHA-256 de la pièce justificative en environnement local 100% hors-ligne.",
            "Contrôle d'intégrité local et validation de conformité sans dépendance d'API en ligne (DEC-AET-02 / DEC-AET-13).",
            "Agrégation de l'empreinte SHA-256 et des métadonnées déclaratives au dossier numérique de lot pour instruction par The Iron Gate."
        ],
        "postconditions": "Attestation sanitaire scellée par empreinte SHA-256 en local hors-ligne, traçabilité garantie sans faille réseau.",
        "legal": "Arrêté ministériel du 28 juin 2013 (modalités d'accès et d'échange de données Sanitel) & Arbitrage Kudoro DEC-AET-02 (références à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "industrial",
            "deviceLabel": "Terminal Terrain DNF / AFSCA • Saisie Déclarative Sanitel & Hachage SHA-256",
            "formFields": [
                {"label": "Numéro de Boucle Auriculaire Sanitel", "name": "sanitel_tag", "type": "text", "value": "BE 5 1284 9901", "placeholder": "BE xxxxxxxxx", "badge": "Sanitel Officiel", "required": True},
                {"label": "Code Exploitation Élevage", "name": "farm_holding_id", "type": "text", "value": "BE-EXP-0412 (Bovin Blanc Bleu Belge)", "placeholder": "Code ARSIA / DGZ", "badge": "Exploitation", "required": True},
                {"label": "Attestation Vétérinaire (Temps d'Attente)", "name": "vet_attestation_file", "type": "text", "value": "ATTEST-VET-2026-098.pdf (45j respectés)", "placeholder": "Fichier attestation", "badge": "Téléversé", "required": True},
                {"label": "Empreinte SHA-256 de la Pièce", "name": "attestation_sha256", "type": "text", "value": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "placeholder": "Hash SHA-256", "badge": "Scellé Local", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_hash_attestation", "label": "Hacher la Pièce Justificative (SHA-256 Local)", "role": "primary", "state": "idle", "icon": "🔒"},
                {"id": "btn_verify_offline", "label": "Vérifier l'Intégrité Hors-Ligne (DEC-AET-02)", "role": "secondary", "state": "idle", "icon": "📄"}
            ],
            "validationMsg": {
                "title": "Attestation Sanitaire Scellée Localement",
                "badge": "Attestation & SHA-256 100% Validés",
                "detail": "Boucle Sanitel BE 5 1284 9901 et attestation vétérinaire certifiées hors-ligne avec empreinte SHA-256 (DEC-AET-02)."
            },
            "errorCase": {
                "code": "ERR_SANITEL_DOCUMENT_CORRUPTED",
                "title": "Empreinte SHA-256 Non Concordante ou Fichier Corrompu",
                "condition": "Le fichier d'attestation téléversé ne correspond pas à l'empreinte SHA-256 enregistrée ou est incomplet.",
                "message": "Erreur de validation locale : L'attestation vétérinaire de temps d'attente est corrompue ou altérée.",
                "remediation": "Sélectionner à nouveau le document d'attestation original émis par le vétérinaire agréé et recalculer le hachage SHA-256."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Saisie Déclarative Sanitel & Document en Attente",
                    "caption": "Boucle BE 5 1284 9901 saisie, attestation vétérinaire prête pour le hachage local hors-ligne.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Saisie Déclarative Sanitel</span>
                        <span class="wf-status-badge wf-badge-neutral">Attestation Prête</span>
                      </div>
                      <div class="wf-device-status-box">
                        <span class="wf-cloud-icon">📋</span>
                        <div><strong>Boucle BE 5 1284 9901 • Exploitation BE-EXP-0412</strong></div>
                        <div class="wf-subtext">Attestation vétérinaire sélectionnée : ATTEST-VET-2026-098.pdf</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔒 Hacher la Pièce Justificative (SHA-256)</button>
                      </div>
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Calcul Local de l'Empreinte SHA-256",
                    "triggerName": "Clic sur 'Hacher la Pièce Justificative' et calcul SHA-256 hors-ligne",
                    "caption": "Génération cryptographique de l'empreinte sans connexion réseau (DEC-AET-02).",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Hachage Cryptographique</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Hachage SHA-256 Local</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Empreinte SHA-256 calculée en local hors-ligne</div>
                        <div class="wf-subtext">Fichier : ATTEST-VET-2026-098.pdf • Taille : 248 Ko • Zéro fuite réseau</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Scellement de l'empreinte...</button>
                      </div>
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Contrôle d'Intégrité Hors-Ligne & Délais Médicamenteux",
                    "progress": 95,
                    "caption": "Vérification locale de l'intégrité du document et de la validité du délai d'attente de 45 jours.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Contrôle d'Intégrité</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Vérification Locale (95%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 95%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [DECLARATIF] Boucle : BE 5 1284 9901 | Exploitation : BE-EXP-0412</code><br>
                        <code>> [SHA-256] Empreinte : e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</code><br>
                        <code>> [DELAI-MED] Attestation vétérinaire conforme : Temps d'attente 45j respecté</code>
                      </div>
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Attestation Validée & Dossier Scellé Hors-Ligne",
                    "status": "success",
                    "caption": "Empreinte SHA-256 et données déclaratives scellées dans le dossier de lot (DEC-AET-02).",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">AeterniTrak • Attestation Scellée</span>
                        <span class="wf-status-badge wf-badge-success">✨ Déclaratif Sanitel Validé</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">📜</span>
                        <div>
                          <strong>Attestation Sanitel / CERISE Validée Hors-Ligne</strong>
                          <p class="wf-subtext">Empreinte SHA-256 scellée • Temps d'attente certifié • Conforme DEC-AET-02</p>
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
    },
    {
        "id": "UC-415",
        "title": "Obstacle Médico-Légal Absolu & Enquête Judiciaire (Mise sous Scellés Parquet)",
        "cat": "Constat Civil & Police Judiciaire",
        "actor": "Médecin Légiste, Parquet & Officier de Police Judiciaire",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": [
    "ObstacleMedicoLegal",
    "Parquet",
    "ScellésJudiciaires",
    "InterdictionBioconversion",
    "Police",
    "TheIronGate"
],
        "preconditions": "Constat d'un décès de cause suspecte, violente ou non élucidée nécessitant l'intervention immédiate de la justice.",
        "flow": [
            "Le médecin certificateur ou l'officier de police judiciaire constate un obstacle médico-légal absolu lors de l'examen initial.",
            "Notification immédiate de l'obstacle dans le système d'aiguillage AeterniTrak The Iron Gate.",
            "Verrouillage irrévocable de la porte d'entrée G0 : interdiction absolue de toute introduction en sas de bioconversion.",
            "Pose d'un scellé judiciaire inviolable et transfert de la dépouille vers l'institut médico-légal sous mandat du Procureur du Roi.",
            "Consignation de la décision judiciaire dans le registre de traçabilité immuable scellé par signature Ed25519 de l'OPJ."
        ],
        "postconditions": "La dépouille est placée sous main de justice ; toute opération de transformation biologique est formellement bloquée.",
        "legal": "Code d'instruction criminelle belge (art. 44 - réquisition judiciaire et autopsie) & Décret funéraire wallon.",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "industrial",
            "deviceLabel": "Borne Judiciaire & Sas Réception • Module d'Obstacle Légal (The Iron Gate)",
            "formFields": [
                {
                    "label": "Magistrat / Parquet Compétent",
                    "name": "prosecutor_office",
                    "type": "text",
                    "value": "Parquet du Procureur du Roi de Namur",
                    "badge": "Justice",
                    "required": True
                },
                {
                    "label": "Constat Médico-Légal",
                    "name": "medical_legal_flag",
                    "type": "select",
                    "value": "OBSTACLE MÉDICO-LÉGAL ABSOLU COCHÉ (Art. 44 CIC)",
                    "badge": "Alerte Rouge",
                    "required": True
                },
                {
                    "label": "Scellé Judiciaire Posé",
                    "name": "judicial_seal_id",
                    "type": "text",
                    "value": "SCELLÉ-PARQUET #JUST-2026-NAM-0912",
                    "badge": "Sous Main de Justice",
                    "required": True
                },
                {
                    "label": "Statut The Iron Gate",
                    "name": "gate_status",
                    "type": "text",
                    "value": "PORTE G0 VERROUILLÉE • BIOCONVERSION STRICTEMENT INTERDITE",
                    "badge": "Blocage 100%",
                    "required": False
                }
            ],
            "actionButtons": [
                {
                    "id": "btn_lock_judicial_seal",
                    "label": "Poser les Scellés Judiciaires & Bloquer la Filière",
                    "role": "primary",
                    "state": "idle",
                    "icon": "⚖️"
                },
                {
                    "id": "btn_export_judicial_pv",
                    "label": "Éditer le PV de Réquisition Parquet",
                    "role": "secondary",
                    "state": "idle",
                    "icon": "📄"
                }
            ],
            "validationMsg": {
                "title": "Obstacle Médico-Légal Enregistré & Filière Verrouillée",
                "badge": "Scellés Judiciaires Actifs",
                "detail": "Porte G0 verrouillée irrévocablement. Dépouille mise sous protection judiciaire. Zéro manipulation biologique autorisée."
            },
            "errorCase": {
                "code": "ERR_MEDICO_LEGAL_OBSTACLE_MANDATORY_SEAL",
                "title": "Obstacle Médico-Légal Absolu & Enquête Judiciaire en Cours",
                "condition": "Signalement d'un obstacle médico-légal sur le certificat de décès ou réquisition formelle du Parquet.",
                "message": "INTERDICTION JUDICIAIRE ABSOLUE : La dépouille fait l'objet d'une enquête pénale. Tout acte de bioconversion est un délit pénal.",
                "remediation": "Transférer immédiatement le corps vers la morgue médico-légale et consigner le procès-verbal aux autorités judiciaires."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Notification d'un Obstacle Médico-Légal",
                    "caption": "Le médecin certificateur relève des éléments suspects imposant la saisine immédiate du Parquet.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">The Iron Gate • Contrôle Judiciaire G0</span>
                                            <span class="wf-status-badge wf-badge-neutral">Examen Initial</span>
                                          </div>
                                          <div class="wf-device-status-box" style="border-color: #ef4444;">
                                            <span class="wf-qa-icon">⚖️</span>
                                            <div><strong>Obstacle Médico-Légal Signalé</strong></div>
                                            <div class="wf-subtext">Mort suspecte ou violente • Obligation légale de saisine du Procureur du Roi</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary" style="background: #e11d48; border-color: #f43f5e;">⚖️ Poser les Scellés Judiciaires & Bloquer la Filière</button>
                                          </div>
                                        </div>
"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Verrouillage Infranchissable de la Porte G0",
                    "triggerName": "Clic sur 'Poser les Scellés Judiciaires'",
                    "caption": "Blocage algorithmique instantané dans l'oracle The Iron Gate et alerte des équipes de logistique.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">The Iron Gate • Verrouillage Porte G0</span>
                                            <span class="wf-status-badge wf-badge-trigger" style="background: rgba(225, 29, 72, 0.2); color: #fda4af;">⚡ Filière Bloquée</span>
                                          </div>
                                          <div class="wf-trigger-card wf-radar-pulse" style="border-color: #f43f5e;">
                                            <div class="wf-trigger-indicator" style="color: #fda4af;">🚫 Porte G0 VERROUILLÉE : Scellé Parquet #JUST-2026-NAM-0912</div>
                                            <div class="wf-subtext">Bioconversion formellement interdite • Réquisition de transfert IML émise</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary wf-pulse-btn">Édition des scellés numériques...</button>
                                          </div>
                                        </div>
"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Émission du Scellé Numérique Ed25519 & Traçabilité",
                    "progress": 100,
                    "caption": "Signature de l'interdiction par la clé judiciaire et journalisation dans le registre déterministe.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">The Iron Gate • Registre Judiciaire</span>
                                            <span class="wf-status-badge wf-badge-process">⚙️ Scellement Déterministe</span>
                                          </div>
                                          <div class="wf-console-log">
                                            <code>> [PARQUET-ORDER] Réquisition judiciaire enregistrée sous signature Ed25519</code><br>
                                            <code>> [IRON-GATE-G0] Porte G0 : REJET CATÉGORIQUE • Code ERR_MEDICO_LEGAL</code><br>
                                            <code>> [CHAIN-LOG] Journalisation déterministe inviolable dans le bloc #TRA-2026-881</code><br>
                                            <code>> [BODY-TRANSFER] Transfert vers l'Institut Médico-Légal de Liège ordonné</code>
                                          </div>
                                        </div>
"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Dépouille Placée sous Main de Justice",
                    "status": "success",
                    "caption": "Sécurité juridique totale. L'intégrité de l'enquête criminelle est scrupuleusement garantie.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">The Iron Gate • Statut Légal</span>
                                            <span class="wf-status-badge wf-badge-success" style="background: rgba(225, 29, 72, 0.2); color: #fda4af;">⚖️ Sous Main de Justice</span>
                                          </div>
                                          <div class="wf-success-banner" style="border-color: rgba(244, 63, 94, 0.4);">
                                            <span class="wf-seal-icon">⚖️</span>
                                            <div>
                                              <strong>Dépouille Protégée sous Scellés Judiciaires</strong>
                                              <p class="wf-subtext">Bioconversion interdite • Registre de traçabilité à disposition du juge d'instruction</p>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-sub">Consulter le Registre Judiciaire de Traçabilité</button>
                                          </div>
                                        </div>
"""
                }
            }
        }
    },
    {
        "id": "UC-416",
        "title": "Rupture de la Chaîne du Froid pendant le Transport Post-Mortem (> +4°C pendant > 2h, Déclassement C2)",
        "cat": "Contrôle Logistique & Biosécurité",
        "actor": "Chauffeur-Livreur Agréé & Responsable Qualité Sas Réception",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": [
    "ChaineDuFroid",
    "RuptureThermique",
    "DeclassementC2",
    "CapteurNFC",
    "TheIronGate",
    "Biosécurité"
],
        "preconditions": "Acheminement d'une dépouille ou de matières post-mortem sous caisson frigorifique régulé (plage 0°C..+4°C).",
        "flow": [
            "Le véhicule de transport subit une avarie du groupe frigorifique ou une immobilisation prolongée lors du transit.",
            "L'enregistreur de température connecté NFC enregistre une dérive thermique supérieure à +4.0°C pendant plus de 2 heures consécutives.",
            "À l'arrivée au sas de réception, la borne AeterniTrak effectue la lecture sans fil du profil chronothermique complet.",
            "Constat du dépassement des seuils critiques : déclenchement automatique du protocole de déclassement sanitaire.",
            "Refus formel d'accès à la filière mémorielle Catégorie 1 et réorientation obligatoire vers la valorisation industrielle Catégorie 2."
        ],
        "postconditions": "La valorisation mémorielle ou cinéraire est révoquée ; aucune prolifération bactérienne incontrôlée ne pénètre le sas mémoriel.",
        "legal": "Règlement (CE) n° 1069/2009 (règles sanitaires applicables aux sous-produits animaux) & Prescriptions de transport frigorifique.",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "industrial",
            "deviceLabel": "Sas Réception • Enregistreur Chronothermique & Déclassement Sanitaire (G1/G2)",
            "formFields": [
                {
                    "label": "Véhicule de Transport",
                    "name": "transport_vehicle",
                    "type": "text",
                    "value": "Fourgon Frigorifique SPW #1-PFN-884",
                    "badge": "Agrément Sanitaire",
                    "required": False
                },
                {
                    "label": "Données Capteur NFC Température",
                    "name": "nfc_temp_log",
                    "type": "text",
                    "value": "+8.4°C mesuré pendant 2h 24min en continu",
                    "badge": "Rupture Critique",
                    "required": False
                },
                {
                    "label": "Décision Sanitaire Automatique",
                    "name": "sanitary_decision",
                    "type": "select",
                    "value": "DÉCLASSEMENT CATÉGORIE 2 (Inapte Filière Mémorielle C1)",
                    "badge": "Déclassement C2",
                    "required": True
                },
                {
                    "label": "Aiguillage Filière de Secours",
                    "name": "rerouting_destination",
                    "type": "text",
                    "value": "Unité Industrielle Technique (Biodiesel / Combustion Sécurisée)",
                    "badge": "Industriel",
                    "required": False
                }
            ],
            "actionButtons": [
                {
                    "id": "btn_confirm_c2_downgrade",
                    "label": "Confirmer le Déclassement Sanitaire Catégorie 2",
                    "role": "primary",
                    "state": "idle",
                    "icon": "❄️"
                },
                {
                    "id": "btn_print_thermal_log",
                    "label": "Éditer le Rapport Chronothermique d'Avarie",
                    "role": "secondary",
                    "state": "idle",
                    "icon": "📊"
                }
            ],
            "validationMsg": {
                "title": "Déclassement Sanitaire Exécuté avec Rigueur",
                "badge": "Déclassement C2 Validé",
                "detail": "Rupture de chaîne du froid documentée. Rejet de la filière mémorielle C1 et réorientation industrielle conforme au CE 1069/2009."
            },
            "errorCase": {
                "code": "ERR_COLD_CHAIN_BREACH_EXCEEDED",
                "title": "Rupture Critique de la Chaîne du Froid (> +4°C pendant > 2h)",
                "condition": "Température de conservation supérieure à +4°C pendant une durée continue excédant 120 minutes.",
                "message": "Violation sanitaire grave : La chaîne du froid a été rompue. La dépouille ne peut plus être traitée sous statut mémoriel Catégorie 1.",
                "remediation": "Appliquer immédiatement le déclassement sanitaire en Catégorie 2 et acheminer vers une filière technique agréée."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Déchargement au Sas avec Alerte Thermique",
                    "caption": "Le capteur de température autonome fixé sur le caisson clignote en rouge à l'ouverture des portes du sas.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">The Iron Gate • Contrôle Thermique Sas</span>
                                            <span class="wf-status-badge wf-badge-neutral">Alerte Capteur NFC</span>
                                          </div>
                                          <div class="wf-device-status-box" style="border-color: #ef4444;">
                                            <span class="wf-qa-icon">❄️</span>
                                            <div><strong>Rupture Chronothermique Détectée</strong></div>
                                            <div class="wf-subtext">+8.4°C enregistré pendant 144 minutes consécutives (> seuil légal 120 min)</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary">❄️ Confirmer le Déclassement Sanitaire Catégorie 2</button>
                                          </div>
                                        </div>
"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Rejet de la Porte G2 & Déclassement Sanitaire",
                    "triggerName": "Clic sur 'Confirmer le Déclassement Sanitaire'",
                    "caption": "Rejet immédiat de l'admission mémorielle et génération du certificat de transfert Catégorie 2.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">The Iron Gate • Aiguillage Sanitaire</span>
                                            <span class="wf-status-badge wf-badge-trigger" style="background: rgba(245, 158, 11, 0.2); color: #fcd34d;">⚡ Déclassement C2</span>
                                          </div>
                                          <div class="wf-trigger-card wf-radar-pulse" style="border-color: #f59e0b;">
                                            <div class="wf-trigger-indicator" style="color: #fcd34d;">⚠️ Profil 1 Mémoriel REFUSÉ • Reclassement en Profil 3/4 Technique</div>
                                            <div class="wf-subtext">Porte G2 (Chaîne du Froid) : ÉCHEC • Transfert vers filière de valorisation technique</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary wf-pulse-btn">Génération du manifeste sanitaire...</button>
                                          </div>
                                        </div>
"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Scellement du Manifeste d'Avarie & Notification AFSCA",
                    "progress": 100,
                    "caption": "Journalisation dans le registre déterministe avec signature électronique du contrôleur sanitaire.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">The Iron Gate • Journalisation Biosécurité</span>
                                            <span class="wf-status-badge wf-badge-process">⚙️ Traçabilité Rebut</span>
                                          </div>
                                          <div class="wf-console-log">
                                            <code>> [TEMP-LOGGER] 144 relevés au-dessus de +4.0°C validés par horodatage</code><br>
                                            <code>> [GATE-G2] Verdict : NON-COMPLIANT (Rupture chaîne du froid)</code><br>
                                            <code>> [RECLASSIFY] Passage statut CAT-1-MEMORIEL -> CAT-2-INDUSTRIEL</code><br>
                                            <code>> [SAFETY-SEAL] Manifeste de transport SPW réémis avec mention technique</code>
                                          </div>
                                        </div>
"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Biosécurité Garantie & Réorientation Achevée",
                    "status": "success",
                    "caption": "La chaîne biologique reste saine. Zéro matière impropre n'est entrée dans l'unité de recueillement.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">The Iron Gate • Sécurité Sanitaire</span>
                                            <span class="wf-status-badge wf-badge-success">✨ Biosécurité Préservée</span>
                                          </div>
                                          <div class="wf-success-banner">
                                            <span class="wf-seal-icon">🛡️</span>
                                            <div>
                                              <strong>Filière Mémorielle Protégée contre Tout Risque Sanitaire</strong>
                                              <p class="wf-subtext">Déclassement C2 acté conformément au Règlement (CE) 1069/2009 • Traçabilité parfaite</p>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-gold">Éditer le Bon d'Expédition Catégorie 2 →</button>
                                          </div>
                                        </div>
"""
                }
            }
        }
    },
    {
        "id": "UC-417",
        "title": "Test Toxicologique LFA Pentobarbital Douteux ou Invalide (Absence Ligne C -> Quarantaine et Contre-Expertise)",
        "cat": "Contrôle Toxicologique & Quarantaine",
        "actor": "Vétérinaire Contrôleur Sanitaire",
        "platforms": ["Natif (iOS & Android)", "Web Standard (PWA Hors-Ligne)"],
        "tags": [
    "Pentobarbital",
    "LFA",
    "LigneC",
    "Quarantaine",
    "HPLC-MS",
    "ContreExpertise",
    "PorteG4"
],
        "preconditions": "Réalisation du test immunochromatographique rapide (LFA) sur prélèvement hépatique ou sanguin pour détecter le pentobarbital.",
        "flow": [
            "Le vétérinaire sanitaire applique l'échantillon extrait sur la cassette de test rapide LFA.",
            "À l'issue du temps de migration réglementaire (10 minutes), la fenêtre optique ne fait apparaître aucune ligne de contrôle C.",
            "L'algorithme de vision de la borne mobile analyse la bandelette : détection formelle de l'absence de la ligne de contrôle (test invalide).",
            "La borne refuse d'ouvrir la porte G4 et déclenche le transfert immédiat de la dépouille vers le sas de quarantaine thermique #Q-02.",
            "Émission automatique d'une réquisition d'analyse confirmatoire par chromatographie liquide haute performance (HPLC-MS) en laboratoire agréé."
        ],
        "postconditions": "Aucune dépouille suspecte n'est admise en bioréacteur sans validation irréfutable de l'absence totale de toxiques létaux.",
        "legal": "Règlement (CE) n° 142/2011 (recherche de résidus médicamenteux) & Notice technique officielle cassettes LFA AFSCA.",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "industrial",
            "deviceLabel": "Borne Vétérinaire Sas • Analyseur Optique LFA & Sas Quarantaine (Porte G4)",
            "formFields": [
                {
                    "label": "Numéro de Lot Cassette LFA",
                    "name": "lfa_lot_batch",
                    "type": "text",
                    "value": "Lot LFA-PENTO #2026-B089 (Périssable 2027)",
                    "badge": "Test Rapide",
                    "required": False
                },
                {
                    "label": "Résultat Lecture Optique",
                    "name": "optical_reading_result",
                    "type": "text",
                    "value": "ABSENCE LIGNE DE CONTRÔLE C • TEST INVALIDE / AMBIGU",
                    "badge": "Invalide Alerte",
                    "required": False
                },
                {
                    "label": "Mesure de Biosécurité Immédiate",
                    "name": "biosecurity_order",
                    "type": "select",
                    "value": "Mise en Quarantaine Hermétique #Q-02 & Analyse HPLC-MS",
                    "badge": "Quarantaine",
                    "required": True
                },
                {
                    "label": "Statut Porte G4 (Pentobarbital)",
                    "name": "gate_g4_status",
                    "type": "text",
                    "value": "PORTE G4 BLOQUÉE • ZÉRO ADMISSION EN BIOCONVERSION",
                    "badge": "Porte Fermée",
                    "required": False
                }
            ],
            "actionButtons": [
                {
                    "id": "btn_quarantine_payload",
                    "label": "Placer en Quarantaine Hermétique & Ordonner HPLC-MS",
                    "role": "primary",
                    "state": "idle",
                    "icon": "☣️"
                },
                {
                    "id": "btn_retry_lfa_strip",
                    "label": "Réaliser un Second Test LFA (Autre Lot)",
                    "role": "secondary",
                    "state": "idle",
                    "icon": "🔄"
                }
            ],
            "validationMsg": {
                "title": "Quarantaine Hermétique Activée & Contre-Expertise Ordonnée",
                "badge": "Quarantaine Active",
                "detail": "Porte G4 fermée hermétiquement. Absence de ligne C interceptée. Échantillon scellé pour spectrométrie HPLC-MS."
            },
            "errorCase": {
                "code": "ERR_LFA_INVALID_CONTROL_LINE_ABSENT",
                "title": "Cassette LFA Invalide ou Résultat Inconcluant (Ligne C Absente)",
                "condition": "Absence de révélation de la ligne de contrôle C sur la membrane immunochromatographique après 10 minutes.",
                "message": "Alerte qualité critique : La cassette de dépistage du pentobarbital est défectueuse ou le prélèvement est altéré. Risque de faux négatif.",
                "remediation": "Mettre immédiatement en quarantaine hermétique à 0°C..+4°C et faire analyser un échantillon scellé par HPLC-MS."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Lecture Optique d'une Cassette LFA Invalide",
                    "caption": "Le lecteur de bandelette constate que le solvant n'a pas migré correctement : aucune ligne C visible.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">The Iron Gate • Sas Quarantaine G4</span>
                                            <span class="wf-status-badge wf-badge-neutral">Test Non Concluant</span>
                                          </div>
                                          <div class="wf-device-status-box" style="border-color: #ef4444;">
                                            <span class="wf-qa-icon">☣️</span>
                                            <div><strong>Anomalie Détection Ligne de Contrôle C</strong></div>
                                            <div class="wf-subtext">Absence de ligne C : test nul et non avenu • Risque de contamination des larves</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary" style="background: #e11d48; border-color: #f43f5e;">☣️ Placer en Quarantaine & Ordonner HPLC-MS</button>
                                          </div>
                                        </div>
"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Verrouillage de la Porte G4 & Mise en Quarantaine",
                    "triggerName": "Clic sur 'Placer en Quarantaine Hermétique'",
                    "caption": "Isolement de la dépouille dans le box thermique hermétique #Q-02 et scellement de l'échantillon laboratoire.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">The Iron Gate • Isolement Sanitaire</span>
                                            <span class="wf-status-badge wf-badge-trigger" style="background: rgba(225, 29, 72, 0.2); color: #fda4af;">⚡ Box Q-02 Scellé</span>
                                          </div>
                                          <div class="wf-trigger-card wf-radar-pulse" style="border-color: #f43f5e;">
                                            <div class="wf-trigger-indicator" style="color: #fda4af;">☣️ Porte G4 (Pentobarbital) REFUSÉE • Sas de Quarantaine #Q-02 Actif</div>
                                            <div class="wf-subtext">Échantillon flacon scellé Ed25519 #LAB-2026-088 pour analyse HPLC-MS</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary wf-pulse-btn">Édition du bon de quarantaine...</button>
                                          </div>
                                        </div>
"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Transmission au Laboratoire Agréé & Suivi Temporel",
                    "progress": 100,
                    "caption": "Enregistrement de la mise en quarantaine dans la chaîne de traçabilité déterministe.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">The Iron Gate • Suivi Quarantaine</span>
                                            <span class="wf-status-badge wf-badge-process">⚙️ Contrôle HPLC-MS</span>
                                          </div>
                                          <div class="wf-console-log">
                                            <code>> [LFA-SCAN] Détection optique : Ligne C = ABSENTE • Statut = INVALIDE</code><br>
                                            <code>> [GATE-G4] Porte G4 : BLOCAGE DE SÉCURITÉ BIOLOGIQUE</code><br>
                                            <code>> [QUARANTINE-CELL] Cellule froide hermétique #Q-02 verrouillée à +2.1°C</code><br>
                                            <code>> [HPLC-ORDER] Réquisition transmise au Laboratoire Toxicologique Régional</code>
                                          </div>
                                        </div>
"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Quarantaine Hermétique Sous Contrôle",
                    "status": "success",
                    "caption": "Rigueur toxicologique absolue. Zéro risque de résidus d'euthanasique dans le procédé de bioconversion.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">The Iron Gate • Quarantaine Sécurisée</span>
                                            <span class="wf-status-badge wf-badge-success">✨ Sécurité Absolue</span>
                                          </div>
                                          <div class="wf-success-banner">
                                            <span class="wf-seal-icon">🔬</span>
                                            <div>
                                              <strong>Mesure de Protection Biologique Opérationnelle</strong>
                                              <p class="wf-subtext">Sujet isolé en quarantaine • Aucune admission en réacteur sans verdict HPLC-MS certifié</p>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-sub">Suivre le Statut de l'Analyse HPLC-MS</button>
                                          </div>
                                        </div>
"""
                }
            }
        }
    },
    {
        "id": "UC-418",
        "title": "Refus Municipal du Permis de Sépulture ou Discordance d'Identité Bracelet Scellé",
        "cat": "Légalité Administrative & Régulation",
        "actor": "Officier d'État Civil Municipal & Directeur de Filière",
        "platforms": ["Web Standard (PWA Hors-Ligne)", "Natif (iOS & Android)"],
        "tags": [
    "PermisSepulture",
    "DiscordanceIdentite",
    "BraceletScelle",
    "EtatCivil",
    "Commune",
    "TheIronGate"
],
        "preconditions": "Présentation du dossier de déclaration de décès auprès de l'officier d'état civil de la commune du lieu de décès.",
        "flow": [
            "L'officier communal examine les pièces d'état civil et procède à la confrontation avec le numéro du bracelet scellé inviolable.",
            "Constat d'une anomalie bloquante : discordance entre l'identité portée sur le bracelet et l'acte de décès ou refus de délivrance du permis de sépulture.",
            "L'administration municipale refuse le permis d'inhumer / bioconvertir en application du décret funéraire.",
            "Transmission immédiate de la notification de refus dans The Iron Gate : blocage en porte G0 de l'admission en filière.",
            "Placement de la dépouille en chambre de repos agréée et suspension de toute opération dans l'attente d'un acte de notoriété rectificatif."
        ],
        "postconditions": "Respect scrupuleux des prérogatives de police des funérailles du Bourgmestre ; zéro manipulation clandestine.",
        "legal": "Décret wallon du 6 mars 2009 relatif aux funérailles et sépultures & Code de la démocratie locale et de la décentralisation.",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "industrial",
            "deviceLabel": "Guichet Administratif Municipal • Contrôle de Légalité & Permis de Sépulture",
            "formFields": [
                {
                    "label": "Commune Compétente",
                    "name": "municipality_name",
                    "type": "text",
                    "value": "Ville de Namur • Service de l'État Civil et des Sépultures",
                    "badge": "Autorité Municipale",
                    "required": False
                },
                {
                    "label": "Statut du Permis Municipal",
                    "name": "permit_status",
                    "type": "select",
                    "value": "REFUS DE PERMIS • DISCORDANCE IDENTITAIRE BRACELET SCELLÉ",
                    "badge": "Refus Légal",
                    "required": True
                },
                {
                    "label": "Discordance Constatée",
                    "name": "mismatch_details",
                    "type": "text",
                    "value": "Nom acte : Heyman Guy • Bracelet : Heymans Guillaume (Incohérence)",
                    "badge": "Contrôle Identité",
                    "required": True
                },
                {
                    "label": "Conséquence Immédiate The Iron Gate",
                    "name": "iron_gate_action",
                    "type": "text",
                    "value": "PORTE G0 SUSPENDUE • REPOS EN CHAMBRE AGRÉÉE",
                    "badge": "Gél Administratif",
                    "required": False
                }
            ],
            "actionButtons": [
                {
                    "id": "btn_record_permit_refusal",
                    "label": "Consigner le Refus Communal & Geler le Dossier",
                    "role": "primary",
                    "state": "idle",
                    "icon": "🏛️"
                },
                {
                    "id": "btn_request_civil_rectification",
                    "label": "Émettre une Demande de Rectification d'État Civil",
                    "role": "secondary",
                    "state": "idle",
                    "icon": "📝"
                }
            ],
            "validationMsg": {
                "title": "Refus Communal Consigné & Suspension de Filière Validée",
                "badge": "Légalité Municipale Respectée",
                "detail": "Porte G0 verrouillée. Dépouille maintenue en chambre de repos agréée. Procédure de rectification engagée."
            },
            "errorCase": {
                "code": "ERR_MUNICIPAL_PERMIT_REFUSED_OR_ID_MISMATCH",
                "title": "Refus Municipal du Permis de Sépulture ou Discordance d'Identité",
                "condition": "Non-concordance entre les mentions de l'acte officiel et le bracelet scellé, ou refus de permis par l'officier civil.",
                "message": "Défaut d'autorisation administrative : Aucun acte funéraire ou de bioconversion ne peut être accompli sans permis communal valide.",
                "remediation": "Régulariser l'acte de décès auprès de l'officier de l'état civil ou produire un jugement rectificatif avant réévaluation."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Contrôle Communal au Guichet de l'État Civil",
                    "caption": "L'officier constate une discordance d'orthographe entre l'acte de décès et le bracelet physique scellé.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">État Civil • Permis de Sépulture</span>
                                            <span class="wf-status-badge wf-badge-neutral">Discordance Détectée</span>
                                          </div>
                                          <div class="wf-device-status-box" style="border-color: #f59e0b;">
                                            <span class="wf-qa-icon">🏛️</span>
                                            <div><strong>Refus de Délivrance du Permis d'Inhumer / Bioconvertir</strong></div>
                                            <div class="wf-subtext">Divergence patronymique entre bracelet scellé et registre de la population</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary">🏛️ Consigner le Refus Communal & Geler le Dossier</button>
                                          </div>
                                        </div>
"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Suspension Immédiate des Opérations dans The Iron Gate",
                    "triggerName": "Clic sur 'Consigner le Refus Communal'",
                    "caption": "Interdiction d'admission dans l'unité de bioconversion et gel des autorisations logistiques.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">The Iron Gate • Régulation Administrative</span>
                                            <span class="wf-status-badge wf-badge-trigger" style="background: rgba(245, 158, 11, 0.2); color: #fcd34d;">⚡ Gel Administratif</span>
                                          </div>
                                          <div class="wf-trigger-card wf-radar-pulse" style="border-color: #f59e0b;">
                                            <div class="wf-trigger-indicator" style="color: #fcd34d;">⚠️ Porte G0 (Admission) : SUSPENDUE en attente de permis communal</div>
                                            <div class="wf-subtext">Mise en chambre de repos agréée • Délai de régularisation : 48 heures</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary wf-pulse-btn">Journalisation du gel communal...</button>
                                          </div>
                                        </div>
"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Enregistrement Déterministe & Alerte Régulateurs",
                    "progress": 100,
                    "caption": "Notification instantanée transmise à l'autorité communale et au directeur de la régulation.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">The Iron Gate • Traçabilité Administrative</span>
                                            <span class="wf-status-badge wf-badge-process">⚙️ Gel Déterministe</span>
                                          </div>
                                          <div class="wf-console-log">
                                            <code>> [CIVIL-CHECK] Réf. acte #NAM-DEC-2026-081 vs Bracelet #SCELL-0982 : MISMATCH</code><br>
                                            <code>> [MUNICIPAL-BLOCK] Permis communal de sépulture non délivré</code><br>
                                            <code>> [IRON-GATE-G0] Entrée bloquée hermétiquement sous signature administrative</code><br>
                                            <code>> [REST-ROOM] Affectation cellule de repos temporaire #CELL-REP-04 validée</code>
                                          </div>
                                        </div>
"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Légalité Républicaine et Municipale Protégée",
                    "status": "success",
                    "caption": "La filière opère dans la légalité absolue. Aucune dérogation administrative n'est tolérée.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">The Iron Gate • Statut Régularisation</span>
                                            <span class="wf-status-badge wf-badge-success">✨ Légalité Assurée</span>
                                          </div>
                                          <div class="wf-success-banner">
                                            <span class="wf-seal-icon">🏛️</span>
                                            <div>
                                              <strong>Procédure Administrative Conforme au Décret Wallon</strong>
                                              <p class="wf-subtext">Dossier gelé dans l'attente du permis officiel • Sécurité légale absolue démontrée</p>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-gold">Émettre la Fiche Navette de Rectification d'État Civil →</button>
                                          </div>
                                        </div>
"""
                }
            }
        }
    }
,
    {'id': 'UC-419', 'title': 'Contrôle Ordre des Médecins / Vétérinaires & Numéro INAMI dans Registre Local', 'cat': 'Constat Civil & Tri', 'actor': 'Vétérinaire Sanitaire & Médecin Légiste', 'platforms': ['Natif (iOS & Android)', 'Web Standard (PWA Hors-Ligne Registres)'], 'tags': ['INAMI', 'OrdreMedecins', 'OrdreVeterinaires', 'Habilitation', 'LocalRegistry'], 'summary': "Vérification cryptographique instantanée du numéro INAMI ou d'inscription à l'Ordre des Médecins / Vétérinaires dans une table de référence locale chiffrée afin de valider l'habilitation légale du certificateur.", 'badge': 'Habilitation INAMI Active', 'legalRef': "Arrêté royal n° 78 relatif à l'exercice des professions de santé & Code de déontologie vétérinaire belge.", 'legal': "Arrêté royal n° 78 relatif à l'exercice des professions de santé & Code de déontologie vétérinaire belge.", 'legal_url': '#section-legal', 'preconditions': "Praticien se présentant pour signer le constat initial ou le bon d'admission sanitaire.", 'flow': ['Saisie ou scan du badge professionnel du praticien (numéro INAMI / matricule Ordre).', 'Hachage et consultation indexée de la base de confiance locale des praticiens agréés (synchronisation asynchrone).', "Contrôle de l'absence de suspension ordinale ou de radiation administrative.", "Affichage du certificat d'agrément sanitaire AFSCA ou Santé Publique.", "Autorisation d'engagement de la signature du constat de décès (EVT-01)."], 'postconditions': 'Identité et habilitation légale du praticien validées sans contestation possible.', 'incident': {'code': 'ERR_PRACTITIONER_NOT_REGISTERED', 'title': 'Numéro INAMI / Ordre Inconnu ou Praticien Suspendu', 'message': "Le praticien ne figure pas dans l'annuaire des professionnels habilités.", 'remediation': "Vérifier le numéro d'ordre saisi ou requérir un confrère habilité."}, 'wireframe': {'device': 'industrial', 'deviceLabel': 'Terminal Terrain DNF / AFSCA • Registre Ordinal Décentralisé', 'formFields': [{'label': "Numéro d'Agrément / INAMI", 'name': 'practitioner_inami', 'type': 'text', 'value': '1-84920-44-001 (Dr. Marc Desmet • Vétérinaire Sanitaire)', 'badge': 'INAMI Valide', 'required': True}, {'label': 'Ordre Professionnel Référent', 'name': 'professional_order', 'type': 'text', 'value': 'Ordre des Médecins Vétérinaires (Conseil Francophone #OMV-942)', 'badge': 'Tableau Actif', 'required': False}, {'label': 'Habilitation Sanitaire AeterniTrak', 'name': 'sanitary_clearance', 'type': 'text', 'value': 'Praticien Certificateur Post-Mortem & Dépistage LFA', 'badge': 'Habilité', 'required': False}, {'label': 'Statut Disciplinaire Décentralisé', 'name': 'disciplinary_status', 'type': 'text', 'value': 'AUCUNE SANCTION / PLEIN EXERCICE DU DROIT', 'badge': 'Conforme', 'required': False}], 'actionButtons': [{'id': 'btn_verify_practitioner', 'label': "Valider l'Habilitation dans le Registre Médical Local", 'role': 'primary', 'state': 'idle', 'icon': '🩺'}, {'id': 'btn_report_practitioner_anomaly', 'label': 'Signaler une Anomalie de Référencement', 'role': 'secondary', 'state': 'idle', 'icon': '⚠️'}], 'validationMsg': {'title': 'Habilitation Ordinale & Sanitaire Confirmée', 'badge': 'Praticien Agréé INAMI', 'detail': 'Dr. Marc Desmet habilité pour les constats civils et dépistages biologiques. Signature autorisée.'}, 'errorCase': {'code': 'ERR_PRACTITIONER_NOT_REGISTERED', 'title': 'Praticien Non Identifié ou Suspendu', 'condition': "Matricule ordinal inexistant ou suspension temporaire signalée par l'Ordre.", 'message': "Le praticien certificateur n'est pas habilité à signer un constat post-mortem.", 'remediation': 'Transférer le dossier au vétérinaire de garde ou au médecin inspecteur de zone.'}, 'phases': {'p1': {'tabTitle': '1. Avant Trigger', 'phaseTitle': 'Identification du Praticien Certificateur', 'caption': "Saisie du numéro d'ordre ou INAMI avant engagement du constat officiel.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">AeterniTrak • Contrôle des Habilitations</span>\n                        <span class="wf-status-badge wf-badge-neutral">En Attente de Saisie</span>\n                      </div>\n                      <div class="wf-device-status-box">\n                        <span class="wf-qa-icon">🩺</span>\n                        <div><strong>Vérification Ordinale & INAMI Requise</strong></div>\n                        <div class="wf-subtext">Consultation de la TrustBase locale des praticiens de santé agréés</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary">🩺 Valider l\'Habilitation dans le Registre Médical Local</button>\n                      </div>\n                    </div>\n'}, 'p2': {'tabTitle': '2. Déclenchement ⚡', 'phaseTitle': 'Recherche Indexée dans le Registre Décentralisé', 'triggerName': "Clic sur 'Valider l'Habilitation'", 'caption': 'Interrogation locale chiffrée de la table ordinale sans dépendance externe.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">AeterniTrak • Registre des Praticiens</span>\n                        <span class="wf-status-badge wf-badge-trigger">⚡ Requête Indexée</span>\n                      </div>\n                      <div class="wf-trigger-card wf-radar-pulse">\n                        <div class="wf-trigger-indicator">SELECT * FROM ordinale_trustbase WHERE inami = \'1-84920-44-001\'</div>\n                        <div class="wf-subtext">Contrôle croisé AFSCA / SPF Santé Publique in-cache</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Vérification en cours...</button>\n                      </div>\n                    </div>\n'}, 'p3': {'tabTitle': '3. Traitement ⚙️', 'phaseTitle': 'Statut Disciplinaire et Habilitations Vérifiés', 'progress': 100, 'caption': 'Plein exercice du droit médical confirmé avec visa sanitaire actif.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">AeterniTrak • Visa Ordinal</span>\n                        <span class="wf-status-badge wf-badge-process">⚙️ Praticien Actif (100%)</span>\n                      </div>\n                      <div class="wf-console-log">\n                        <code>> [ORDRE] Dr. Marc Desmet, Conseil Régional Francophone</code><br>\n                        <code>> [INAMI] 1-84920-44-001 -> Statut ACTIF & VALIDE</code><br>\n                        <code>> [DISCIPLINE] Zéro sanction disciplinaire enregistrée</code><br>\n                        <code>> [HABILITATION] Signature autorisée pour EVT-01 Constat Initial</code>\n                      </div>\n                    </div>\n'}, 'p4': {'tabTitle': '4. Écran de Fin ✨', 'phaseTitle': 'Habilitation Sanitaire Accordée', 'status': 'success', 'caption': 'Le praticien est habilité à initier le constat et apposer le scellé initial.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">AeterniTrak • Habilitation Certifiée</span>\n                        <span class="wf-status-badge wf-badge-success">✨ Praticien Validé</span>\n                      </div>\n                      <div class="wf-success-banner">\n                        <span class="wf-seal-icon">🏛️</span>\n                        <div>\n                          <strong>Praticien Agréé & Reconnu</strong>\n                          <p class="wf-subtext">Dr. Marc Desmet • Prêt pour signature du constat EVT-01</p>\n                        </div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-gold">Ouvrir le Formulaire de Constat de Décès →</button>\n                      </div>\n                    </div>\n'}}}},
    {'id': 'UC-420', 'title': "Scellement Cryptographique Ed25519 de l'Événement de Transport Primaire", 'cat': 'Logistique & Scellement', 'actor': 'Chauffeur Funéraire Agréé / Transporteur Sanitaire', 'platforms': ['Terminal Véhicule Durci (Android IP68)', 'PWA Hors-Ligne'], 'tags': ['TransportPrimaire', 'ScellementEd25519', 'NfcSeal', 'COSE', 'GeoTracking'], 'summary': 'Apposition physique et signature Ed25519 du scellé RFID/NFC lors de la prise en charge dans le véhicule funéraire agréé, créant le maillon immuable EVT-02 de la chaîne de garde.', 'badge': 'EVT-02 Scellé Ed25519', 'legalRef': 'Décret wallon du 6 mars 2009 relatif aux funérailles et sépultures & Règlement (CE) n° 1069/2009.', 'legal': 'Décret wallon du 6 mars 2009 relatif aux funérailles et sépultures & Règlement (CE) n° 1069/2009.', 'legal_url': '#section-legal', 'preconditions': 'Constat EVT-01 validé et dépouille conditionnée en housse ou cercueil agréé.', 'flow': ['Pose du scellé inviolable RFID/NFC haute sécurité sur le fermoir du caisson de transport.', 'Scan NFC sans contact du scellé avec le terminal durci du véhicule.', "Agrégation des données d'événement : identifiant dépouille, ID scellé, plaque d'immatriculation, horodatage UTC et coordonnées GPS.", 'Signature cryptographique Ed25519 par la clé privée matérielle du chauffeur.', "Émission de la preuve COSE_Sign1 ancrée dans le journal d'audit local du véhicule."], 'postconditions': 'Événement de transport primaire EVT-02 cryptographiquement inviolable et vérifiable hors-ligne.', 'incident': {'code': 'ERR_TRANSPORT_SEAL_MISMATCH', 'title': 'Discordance de Numéro de Scellé', 'message': "Le scellé scanné ne correspond pas à l'attribution délivrée lors du constat.", 'remediation': 'Réaffecter le scellé sous supervision du responsable logistique avec justification tracée.'}, 'wireframe': {'device': 'industrial', 'deviceLabel': 'Terminal Embarqué Véhicule • Scellement Transport EVT-02', 'formFields': [{'label': 'Identifiant Scellé Inviolable', 'name': 'nfc_seal_id', 'type': 'text', 'value': 'SCELL-2026-BEL-0982-NFC (Puce RFID Haute Sécurité)', 'badge': 'Inviolable', 'required': True}, {'label': 'Véhicule Funéraire Agréé', 'name': 'transport_vehicle', 'type': 'text', 'value': '1-AFR-842 (Fourgon Isotherme Agrément Wallonie #AGR-FUN-12)', 'badge': 'Agréé C1/C2', 'required': False}, {'label': 'Point GPS & Horodatage Prise en Charge', 'name': 'pickup_telemetry', 'type': 'text', 'value': '2026-10-05T09:12:04Z • 50.4501° N, 5.0210° E (Namur)', 'badge': 'Horodaté UTC', 'required': False}, {'label': 'Signature Cryptographique Chauffeur', 'name': 'driver_crypto_sig', 'type': 'text', 'value': 'ed25519:5c6d7e8f9a0b1c2d... (Clé Chauffeur #CHAUFF-88)', 'badge': 'Ed25519', 'required': False}], 'actionButtons': [{'id': 'btn_seal_transport_evt', 'label': 'Signer & Sceller la Prise en Charge Transport (Ed25519)', 'role': 'primary', 'state': 'idle', 'icon': '🔒'}, {'id': 'btn_scan_nfc_vehicle_seal', 'label': 'Vérifier le Scellé Physiquement par NFC', 'role': 'secondary', 'state': 'idle', 'icon': '📱'}], 'validationMsg': {'title': 'Événement de Transport EVT-02 Scellé', 'badge': 'Chaîne de Garde Inviolable', 'detail': 'Scellé SCELL-0982 lié au véhicule 1-AFR-842. Signature Ed25519 générée et ancrée localement.'}, 'errorCase': {'code': 'ERR_TRANSPORT_SEAL_MISMATCH', 'title': "Divergence d'Identifiant de Scellé", 'condition': 'Le tag NFC détecté ne concorde pas avec la référence allouée au départ du centre.', 'message': 'Impossible de sceller : le scellé apposé est non conforme au manifeste de transport.', 'remediation': "Remplacer par le scellé officiel référencé et consigner l'incident au journal."}, 'phases': {'p1': {'tabTitle': '1. Avant Trigger', 'phaseTitle': 'Chargement Effectué dans le Véhicule Agréé', 'caption': 'Le caisson de transport est clos, le scellé physique est apposé.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">AeterniTrak • Scellement Véhicule</span>\n                        <span class="wf-status-badge wf-badge-neutral">Scellé Apposé</span>\n                      </div>\n                      <div class="wf-device-status-box">\n                        <span class="wf-qa-icon">🔒</span>\n                        <div><strong>Scellement Inviolable Transport Requis</strong></div>\n                        <div class="wf-subtext">Association véhicule 1-AFR-842 + Scellé NFC + Télémétrie GPS</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary">🔒 Signer & Sceller la Prise en Charge Transport (Ed25519)</button>\n                      </div>\n                    </div>\n'}, 'p2': {'tabTitle': '2. Déclenchement ⚡', 'phaseTitle': 'Acquisition NFC & Empreinte Télémetrique', 'triggerName': 'Scan du Scellé & Signature Chauffeur', 'caption': 'Lecture de la puce sans contact et horodatage UTC par le modem durci.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">AeterniTrak • Capture NFC</span>\n                        <span class="wf-status-badge wf-badge-trigger">⚡ Scan Scellé 0982</span>\n                      </div>\n                      <div class="wf-trigger-card wf-radar-pulse">\n                        <div class="wf-trigger-indicator">NFC UID: 04:9A:88:F2 -> Scellé vérifié intact</div>\n                        <div class="wf-subtext">Signature matérielle Ed25519 en cours d\'application par le terminal</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Scellement cryptographique...</button>\n                      </div>\n                    </div>\n'}, 'p3': {'tabTitle': '3. Traitement ⚙️', 'phaseTitle': 'Génération de la Preuve COSE_Sign1 EVT-02', 'progress': 100, 'caption': 'Chaîne de garde complétée avec coordonnées GPS de départ.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">AeterniTrak • Chaîne de Garde</span>\n                        <span class="wf-status-badge wf-badge-process">⚙️ EVT-02 Scellé (100%)</span>\n                      </div>\n                      <div class="wf-console-log">\n                        <code>> [TRANSPORT] Véhicule 1-AFR-842, chauffeur #CHAUFF-88</code><br>\n                        <code>> [SEAL] SCELL-2026-BEL-0982-NFC vérifié non altéré</code><br>\n                        <code>> [TELEMETRY] 50.4501° N, 5.0210° E @ 09:12:04 UTC</code><br>\n                        <code>> [CHAIN] Ancrage parent EVT-01 -> hash validé</code>\n                      </div>\n                    </div>\n'}, 'p4': {'tabTitle': '4. Écran de Fin ✨', 'phaseTitle': 'Départ Transport Autorisé & Tracé', 'status': 'success', 'caption': 'Le véhicule est autorisé à prendre la route vers le centre de traitement.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">AeterniTrak • Feu Vert Transport</span>\n                        <span class="wf-status-badge wf-badge-success">✨ Trajet Déverrouillé</span>\n                      </div>\n                      <div class="wf-success-banner">\n                        <span class="wf-seal-icon">🚛</span>\n                        <div>\n                          <strong>Prise en Charge Officiellement Scellée</strong>\n                          <p class="wf-subtext">EVT-02 enregistré • Suivi continu de la chaîne du froid activé</p>\n                        </div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-gold">Activer le Monitoring Thermique de Route →</button>\n                      </div>\n                    </div>\n'}}}},
    {'id': 'UC-421', 'title': "Déchargement Datalogger Thermique & Calcul de l'Intégrale Temps/Température", 'cat': 'Contrôle Logistique & Biosécurité', 'actor': 'Opérateur de Réception Sanitaire / Gestionnaire Frigorifique', 'platforms': ['Station de Réception PC/Mac', 'Terminal Tablette USB/Bluetooth'], 'tags': ['Datalogger', 'ChaineDuFroid', 'IntegraleThermique', 'DegreeHours', 'Biosécurite'], 'summary': "Acquisition de la télémétrie thermique embarquée durant le transit et calcul de l'intégrale temps/température pour certifier l'absence d'excursion critique avant admission.", 'badge': 'Intégrale Thermique 0.0 °C·h', 'legalRef': 'Norme EN 12830 (enregistreurs de température pour le transport) & Décision Kudoro DEC-AET-03.', 'legal': 'Norme EN 12830 (enregistreurs de température pour le transport) & Décision Kudoro DEC-AET-03.', 'legal_url': '#section-legal', 'preconditions': 'Arrivée du véhicule au centre de traitement avec datalogger actif dans le caisson.', 'flow': ['Connexion sans contact (NFC ou Bluetooth Low Energy) ou USB au datalogger thermique.', 'Téléchargement du relevé chronologique complet (mesures cadencées toutes les 30 secondes).', "Calcul de l'intégrale d'excursion : ∫ max(0, T(t) - 4°C) dt sur l'ensemble du trajet.", 'Vérification du seuil critique (tolérance zéro excursion prolongée > 2 heures à +4°C).', "Certification numérique de la chaîne du froid et injection dans l'événement EVT-03."], 'postconditions': 'Chaîne du froid certifiée sans rupture ; autorisation de déchargement vers la cellule froide.', 'incident': {'code': 'ERR_COLD_CHAIN_INTEGRAL_BREACH', 'title': 'Rupture Critique de la Chaîne du Froid', 'message': "L'intégrale thermique dépasse 8.0 °C·h au-delà de +4°C durant le transport.", 'remediation': 'Déclassement immédiat de la carcasse en Catégorie 2 technique industrielle (combustion/cimenterie).'}, 'wireframe': {'device': 'industrial', 'deviceLabel': 'Station Réception Sanitaire • Calculateur Thermique EN 12830', 'formFields': [{'label': 'Relevé Télémétrique Datalogger', 'name': 'datalogger_points', 'type': 'text', 'value': '428 points de mesure sur 2h45 (Échantillonnage 30s • Précision ±0.1°C)', 'badge': 'EN 12830', 'required': False}, {'label': 'Température Maximale Atteinte', 'name': 'temp_max', 'type': 'text', 'value': '+3.4°C (Respect parfait de la limite légale +4.0°C)', 'badge': 'Maximum OK', 'required': False}, {'label': 'Intégrale Temps/Température (>4°C)', 'name': 'thermal_integral', 'type': 'text', 'value': '0.00 °C·heure (Aucune excursion hors tolérance)', 'badge': '0.0 °C·h', 'required': False}, {'label': 'Bilan Sanitaire Chaîne du Froid', 'name': 'cold_chain_verdict', 'type': 'text', 'value': 'CONFORME À 100% (Préservation optimale des tissus)', 'badge': 'Chaîne Froid OK', 'required': False}], 'actionButtons': [{'id': 'btn_ingest_datalogger', 'label': "Décharger la Télémétrie & Calculer l'Intégrale", 'role': 'primary', 'state': 'idle', 'icon': '📉'}, {'id': 'btn_view_temp_curve', 'label': 'Afficher la Courbe Chronologique de Température', 'role': 'secondary', 'state': 'idle', 'icon': '📊'}], 'validationMsg': {'title': 'Chaîne du Froid Certifiée Conforme', 'badge': 'Intégrale Thermique Validée', 'detail': "Excursion nulle constatée. Température moyenne stabilisée à +2.6°C sur l'ensemble du transit."}, 'errorCase': {'code': 'ERR_COLD_CHAIN_INTEGRAL_BREACH', 'title': "Dépassement Critique de l'Intégrale Thermique", 'condition': 'Panne du groupe frigorifique durant le trajet causant une élévation prolongée de température.', 'message': 'ALERTE BIOSÉCURITÉ : La dépouille a dépassé le seuil de tolérance thermique (+6°C pendant > 2h).', 'remediation': "Refuser l'admission en ligne mémorielle et réorienter vers la filière industrielle C2."}, 'phases': {'p1': {'tabTitle': '1. Avant Trigger', 'phaseTitle': 'Datalogger Prêt pour Déchargement', 'caption': 'Le boîtier enregistreur est branché à la borne de déchargement rapide.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">AeterniTrak • Contrôle Thermique</span>\n                        <span class="wf-status-badge wf-badge-neutral">Datalogger Connecté</span>\n                      </div>\n                      <div class="wf-device-status-box">\n                        <span class="wf-qa-icon">📉</span>\n                        <div><strong>Vérification de la Chaîne du Froid Transport</strong></div>\n                        <div class="wf-subtext">Téléchargement des 428 points de mesure PT100 et calcul de l\'intégrale</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary">📉 Décharger la Télémétrie & Calculer l\'Intégrale</button>\n                      </div>\n                    </div>\n'}, 'p2': {'tabTitle': '2. Déclenchement ⚡', 'phaseTitle': "Calcul Numérique de l'Intégrale Temps/Température", 'triggerName': 'Déchargement & Intégration', 'caption': 'Sommation des écarts thermiques au-dessus de la ligne de consigne +4.0°C.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">AeterniTrak • Intégrale Degrés-Heures</span>\n                        <span class="wf-status-badge wf-badge-trigger">⚡ Calcul Mathématique</span>\n                      </div>\n                      <div class="wf-trigger-card wf-radar-pulse">\n                        <div class="wf-trigger-indicator">∫ max(0, T - 4°C) dt = 0.000 °C·h sur 165 minutes</div>\n                        <div class="wf-subtext">Plage relevée : min +1.8°C, max +3.4°C, moyenne +2.6°C</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Calcul de conformité...</button>\n                      </div>\n                    </div>\n'}, 'p3': {'tabTitle': '3. Traitement ⚙️', 'phaseTitle': 'Conformité Normative EN 12830 Validée', 'progress': 100, 'caption': 'Intégrité biologique garantie, absence de multiplication bactérienne précoce.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">AeterniTrak • Bilan Froid</span>\n                        <span class="wf-status-badge wf-badge-process">⚙️ Chaîne Validée (100%)</span>\n                      </div>\n                      <div class="wf-console-log">\n                        <code>> [THERMAL-EN12830] 428 points importés sans rupture</code><br>\n                        <code>> [MAX-TEMP] +3.4°C mesuré à 10:04 UTC (sous la limite +4°C)</code><br>\n                        <code>> [INTEGRAL] 0.00 °C·h -> Aucune dérive biologique</code><br>\n                        <code>> [STATUS] Feu vert pour admission en cellule de stockage #B4</code>\n                      </div>\n                    </div>\n'}, 'p4': {'tabTitle': '4. Écran de Fin ✨', 'phaseTitle': 'Chaîne du Froid Certifiée & Scellée', 'status': 'success', 'caption': "Le visa thermique est injecté dans le dossier d'admission EVT-03.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">AeterniTrak • Admission Déverrouillée</span>\n                        <span class="wf-status-badge wf-badge-success">✨ Chaîne du Froid Parfaite</span>\n                      </div>\n                      <div class="wf-success-banner">\n                        <span class="wf-seal-icon">❄️</span>\n                        <div>\n                          <strong>Conservation Optimale Démontrée</strong>\n                          <p class="wf-subtext">Zéro excursion thermique • Autorisation de transfert en chambre froide</p>\n                        </div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-gold">Assigner la Cellule Frigorifique de Conservation →</button>\n                      </div>\n                    </div>\n'}}}},
    {'id': 'UC-422', 'title': 'Assignation Dynamique Cellule Frigorifique & Badging RFID Rayonnage', 'cat': 'Logistique & Stockage Sanitaire', 'actor': 'Gestionnaire de Cellules Réfrigérées / Opérateur Logistique', 'platforms': ['Terminal Industriel Embarqué Rayonnage', 'PWA Mobile'], 'tags': ['CelluleFrigorifique', 'RFID', 'Emplacement', 'Segregation', 'ColdStorage'], 'summary': "Attribution dynamique d'une cellule de conservation réfrigérée individuelle (+2°C/+4°C) respectant la ségrégation stricte des filières et scellement de l'emplacement par badging RFID physique.", 'badge': 'Cellule #B4 Verrouillée', 'legalRef': 'Règlement (CE) n° 1069/2009 (ségrégation et stockage étanche des sous-produits animaux).', 'legal': 'Règlement (CE) n° 1069/2009 (ségrégation et stockage étanche des sous-produits animaux).', 'legal_url': '#section-legal', 'preconditions': 'Contrôle thermique du transport validé et dépouille prête à être introduite en stockage.', 'flow': ['Interrogation algorithmique des disponibilités dans la chambre froide ségréguée.', 'Filtrage étanche : la dépouille de compagnie Profil 1 ne peut être admise que dans le compartiment Mémoriel.', 'Attribution de la cellule froide individuelle #B4 (régulation active +2.5°C à +3.5°C).', "L'opérateur dépose la dépouille et passe son badge lecteur sur l'étiquette RFID de la cellule.", "Verrouillage électromagnétique du casier et horodatage de l'entrée en conservation."], 'postconditions': 'Dépouille en conservation sécurisée, localisation inaltérable et ségrégation garantie.', 'incident': {'code': 'ERR_CELL_COMPATIBILITY_CONFLICT', 'title': 'Conflit de Ségrégation de Cellule Frigorifique', 'message': "Tentative d'affectation dans une cellule réservée à un autre profil sanitaire incompatible.", 'remediation': "Le système refuse l'ouverture du casier et oriente l'opérateur vers le compartiment mémoriel dédié."}, 'wireframe': {'device': 'industrial', 'deviceLabel': 'Chambre Frigorifique Ségréguée • Badging RFID Rayonnage', 'formFields': [{'label': 'Profil Sanitaire Dépouille', 'name': 'depouille_profile', 'type': 'text', 'value': 'PROFIL 1 : Compagnie (Catégorie 1 Mémorielle Exclusive)', 'badge': 'Profil 1 Exclusif', 'required': False}, {'label': 'Cellule Assignée Algorithmiquement', 'name': 'assigned_cell_id', 'type': 'text', 'value': 'Cellule Frigorifique Individuelle #B4 (Zone A - Mémorielle)', 'badge': 'Cellule #B4', 'required': False}, {'label': 'Température Régulée Casier', 'name': 'cell_temp', 'type': 'text', 'value': '+2.8°C (Sonde PT100 Calibrée • PID Régulé)', 'badge': '+2.8°C OK', 'required': False}, {'label': 'Scan Tag RFID Emplacement', 'name': 'rfid_location_tag', 'type': 'text', 'value': 'RFID-LOC-B4-9910 (Lecture sans contact confirmée)', 'badge': 'RFID Confirmé', 'required': False}], 'actionButtons': [{'id': 'btn_assign_cold_cell', 'label': "Valider l'Assignation & Verrouiller la Cellule #B4", 'role': 'primary', 'state': 'idle', 'icon': '❄️'}, {'id': 'btn_unlock_cell_door', 'label': "Déverrouiller le Sas d'Accès Sécurisé", 'role': 'secondary', 'state': 'idle', 'icon': '🔓'}], 'validationMsg': {'title': 'Dépouille Consignée en Cellule Frigorifique #B4', 'badge': 'Stockage Ségrégué Conforme', 'detail': 'Verrouillage électromécanique activé. Séparation hermétique garantie selon Règlement (CE) n° 1069/2009.'}, 'errorCase': {'code': 'ERR_CELL_COMPATIBILITY_CONFLICT', 'title': 'Violation de Ségrégation Sanitaire', 'condition': 'Tentative de consigner une carcasse de compagnie dans un rayonnage de transit agricole ou abattoir.', 'message': 'ALERTE SÉGRÉGATION : Conflit de profil sanitaire détecté. Casier incompatible.', 'remediation': "Sélectionner exclusivement les cellules de l'aile mémorielle étanche (Casier B1 à B12)."}, 'phases': {'p1': {'tabTitle': '1. Avant Trigger', 'phaseTitle': 'Sélection Automatique de Cellule Ségréguée', 'caption': "L'algorithme analyse l'inventaire frigorifique pour attribuer un casier dédié.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">AeterniTrak • Gestion Emplacements</span>\n                        <span class="wf-status-badge wf-badge-neutral">Casier Libre : #B4</span>\n                      </div>\n                      <div class="wf-device-status-box">\n                        <span class="wf-qa-icon">❄️</span>\n                        <div><strong>Assignation Cellule Frigorifique Sécurisée</strong></div>\n                        <div class="wf-subtext">Contrôle de ségrégation hermétique (Profil 1 Mémoriel exclusif)</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary">❄️ Valider l\'Assignation & Verrouiller la Cellule #B4</button>\n                      </div>\n                    </div>\n'}, 'p2': {'tabTitle': '2. Déclenchement ⚡', 'phaseTitle': "Badging RFID de l'Emplacement Physique", 'triggerName': 'Scan RFID du Rayonnage', 'caption': "L'opérateur effleure la pastille RFID fixée sur le montant du casier #B4.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">AeterniTrak • Badging Emplacement</span>\n                        <span class="wf-status-badge wf-badge-trigger">⚡ Scan Tag RFID-B4</span>\n                      </div>\n                      <div class="wf-trigger-card wf-radar-pulse">\n                        <div class="wf-trigger-indicator">Tag RFID-LOC-B4 détecté -> Corrélation physique validée</div>\n                        <div class="wf-subtext">Vérification de la régulation PT100 casier (+2.8°C stable)</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Scellement de l\'emplacement...</button>\n                      </div>\n                    </div>\n'}, 'p3': {'tabTitle': '3. Traitement ⚙️', 'phaseTitle': 'Verrouillage Électromécanique & Enregistrement', 'progress': 100, 'caption': "La cellule est scellée, l'accès est consigné dans le journal sécurisé.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">AeterniTrak • Consigne Frigorifique</span>\n                        <span class="wf-status-badge wf-badge-process">⚙️ Casier Verrouillé (100%)</span>\n                      </div>\n                      <div class="wf-console-log">\n                        <code>> [RFID-LOC] Rayon B, Niveau 2, Casier #B4 confirmé</code><br>\n                        <code>> [LOCK] Pêne électromagnétique engagé (Contact magnétique fermé)</code><br>\n                        <code>> [TEMP-MONITOR] Température courante : +2.8°C (Seuil alerte > +4.0°C)</code><br>\n                        <code>> [SÉGRÉGATION] Aucune cohabitation inter-profil permise</code>\n                      </div>\n                    </div>\n'}, 'p4': {'tabTitle': '4. Écran de Fin ✨', 'phaseTitle': 'Dépouille Sécurisée en Attente de Soins', 'status': 'success', 'caption': "La conservation est assurée jusqu'aux opérations amonts (LFA & Pacemaker).", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">AeterniTrak • Conservation Active</span>\n                        <span class="wf-status-badge wf-badge-success">✨ Stockage Certifié</span>\n                      </div>\n                      <div class="wf-success-banner">\n                        <span class="wf-seal-icon">🛡️</span>\n                        <div>\n                          <strong>Cellule #B4 Sécurisée</strong>\n                          <p class="wf-subtext">Température +2.8°C sous surveillance continue • Traçabilité scellée</p>\n                        </div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-gold">Passer aux Contrôles Amonts (LFA & Pacemaker) →</button>\n                      </div>\n                    </div>\n'}}}},
    {'id': 'UC-423', 'title': "Analyse Spectrophotométrique Courbe d'Absorption Bandelette LFA (Ratio C/T)", 'cat': 'Contrôle Biologique', 'actor': "Technicien de Laboratoire BioLab / Praticien d'Admission", 'platforms': ['Lecteur Optique LFA Connecté (USB/BLE)', 'Terminal Mobile Caméra Haute Résolution'], 'tags': ['LFA', 'Spectrophotometrie', 'Pentobarbital', 'Ratio_C_T', 'OpticalDensity'], 'summary': "Mesure optique quantitative de la densité de couleur des bandes Contrôle (C) et Test (T) sur la cassette LFA, calcul mathématique du ratio C/T pour objectiver l'absence de pentobarbital (seuil 20 ng/mL).", 'badge': 'Ratio C/T 0.944 (Négatif)', 'legalRef': 'Notice technique AFSCA pour le dépistage des barbituriques & Décision Kudoro DEC-AET-01.', 'legal': 'Notice technique AFSCA pour le dépistage des barbituriques & Décision Kudoro DEC-AET-01.', 'legal_url': '#section-legal', 'preconditions': 'Écouvillonnage hépatique/sanguin réalisé et bandelette immunochromatographique incubée 10 minutes.', 'flow': ['Introduction de la cassette LFA dans le tiroir du spectrophotomètre portable ou numérisation sous flux calibré.', "Balayage optique des bandes d'extinction à la longueur d'onde de résonance des nanoparticules d'or colloïdal (525 nm).", 'Calcul des densités optiques surfaciques : OD_C (Ligne de Contrôle) et OD_T (Ligne de Test).', "Vérification du ratio C/T : présence nette de la ligne T confirmant l'absence de drogue compétitive.", "Émission du visa toxicologique numérique avec courbe d'extinction spectrophotométrique scellée."], 'postconditions': 'Verdict toxicologique quantifié, reproductible et incontestable ; Porte G4 déverrouillée.', 'incident': {'code': 'ERR_LFA_LINE_C_ABSENT_INVALID', 'title': 'Bandelette LFA Invalide (Absence Ligne C)', 'message': "La ligne de contrôle interne n'a pas migré (OD_C < 0.150 AU). Le test est biologiquement nul.", 'remediation': "Mettre l'échantillon en quarantaine et renouveler le test avec une nouvelle cassette."}, 'wireframe': {'device': 'industrial', 'deviceLabel': 'BioLab AeterniCore • Spectrophotomètre Numérique LFA (525 nm)', 'formFields': [{'label': 'Densité Optique Ligne Contrôle (C)', 'name': 'od_control', 'type': 'text', 'value': "OD_C = 0.842 AU (Pic d'absorption net à 525 nm • Migration valide)", 'badge': 'Ligne C Valide', 'required': False}, {'label': 'Densité Optique Ligne Test (T)', 'name': 'od_test', 'type': 'text', 'value': 'OD_T = 0.795 AU (Présente = Molécule absente du prélèvement)', 'badge': 'Ligne T Valide', 'required': False}, {'label': "Ratio d'Extinction Relatif (C/T)", 'name': 'ct_ratio', 'type': 'text', 'value': '0.944 (Seuil de conformité exigé > 0.600)', 'badge': 'Conforme', 'required': False}, {'label': 'Quantification Pentobarbital Estimée', 'name': 'pento_conc', 'type': 'text', 'value': '< 5.0 ng/mL (Cut-off réglementaire AFSCA fixé à 20 ng/mL)', 'badge': 'NÉGATIF', 'required': False}], 'actionButtons': [{'id': 'btn_run_lfa_spectro', 'label': 'Acquérir le Spectre Optique & Calculer le Ratio C/T', 'role': 'primary', 'state': 'idle', 'icon': '🔬'}, {'id': 'btn_calibrate_optical_sensor', 'label': 'Étalonner la Caméra avec Carte de Référence', 'role': 'secondary', 'state': 'idle', 'icon': '🎯'}], 'validationMsg': {'title': 'Analyse Spectrophotométrique LFA Certifiée Conforme', 'badge': 'NÉGATIF PENTOBARBITAL (Ratio C/T 0.944)', 'detail': 'Absence de barbituriques démontrée scientifiquement. Porte G4 de The Iron Gate validée.'}, 'errorCase': {'code': 'ERR_LFA_LINE_C_ABSENT_INVALID', 'title': 'Bandelette LFA Défectueuse ou Pression Échantillon Insuffisante', 'condition': 'Absence de coloration sur la ligne de contrôle C (OD_C < 0.150 AU).', 'message': "TEST BIOLOGIQUEMENT INVALIDE : La réaction de contrôle n'a pas fonctionné.", 'remediation': 'Isoler la dépouille en quarantaine temporaire et effectuer un second prélèvement LFA.'}, 'phases': {'p1': {'tabTitle': '1. Avant Trigger', 'phaseTitle': 'Cassette LFA Insérée dans la Fente Optique', 'caption': 'Incubation terminée (10 minutes). La cassette attend la mesure spectrophotométrique.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">BioLab • Spectrophotomètre LFA</span>\n                        <span class="wf-status-badge wf-badge-neutral">Prêt à Scanner</span>\n                      </div>\n                      <div class="wf-device-status-box">\n                        <span class="wf-qa-icon">🔬</span>\n                        <div><strong>Analyse Toxicologique Quantitative LFA</strong></div>\n                        <div class="wf-subtext">Mesure de réflectance optique à 525 nm pour objectivation mathématique</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary">🔬 Acquérir le Spectre Optique & Calculer le Ratio C/T</button>\n                      </div>\n                    </div>\n'}, 'p2': {'tabTitle': '2. Déclenchement ⚡', 'phaseTitle': 'Numérisation des Bandes C et T sous LED Calibrée', 'triggerName': 'Balayage Optique LFA', 'caption': 'Capture spectrophotométrique haute résolution du gradient de nanoparticules.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">BioLab • Balayage Optique</span>\n                        <span class="wf-status-badge wf-badge-trigger">⚡ Scan Spectro 525 nm</span>\n                      </div>\n                      <div class="wf-trigger-card wf-radar-pulse">\n                        <div class="wf-trigger-indicator">Intégration surfacique : Ligne C = 0.842 AU | Ligne T = 0.795 AU</div>\n                        <div class="wf-subtext">Calcul du ratio : OD_T / OD_C = 0.944 (Absence de molécule inhibitrice)</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Calcul photométrique...</button>\n                      </div>\n                    </div>\n'}, 'p3': {'tabTitle': '3. Traitement ⚙️', 'phaseTitle': 'Évaluation Contre le Cut-Off Réglementaire AFSCA', 'progress': 100, 'caption': 'Le ratio C/T dépasse largement le seuil minimal de 0.600.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">BioLab • Bilan Toxicologique</span>\n                        <span class="wf-status-badge wf-badge-process">⚙️ Spectre Conforme (100%)</span>\n                      </div>\n                      <div class="wf-console-log">\n                        <code>> [SPECTRO] Longueur d\'onde 525 nm calibrée</code><br>\n                        <code>> [PEAK-C] Contrôle présent à OD 0.842 AU (Validité biologique assurée)</code><br>\n                        <code>> [PEAK-T] Test présent à OD 0.795 AU (Pentobarbital < 5.0 ng/mL)</code><br>\n                        <code>> [VERDICT] NÉGATIF / CONFORME -> Porte G4 ouverte</code>\n                      </div>\n                    </div>\n'}, 'p4': {'tabTitle': '4. Écran de Fin ✨', 'phaseTitle': 'Visa Toxicologique Certifié', 'status': 'success', 'caption': "La dépouille est biologiquement apte pour l'alimentation des larves.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">BioLab • Visa Accordé</span>\n                        <span class="wf-status-badge wf-badge-success">✨ Zéro Barbiturique</span>\n                      </div>\n                      <div class="wf-success-banner">\n                        <span class="wf-seal-icon">🧬</span>\n                        <div>\n                          <strong>Dépistage Pentobarbital Conforme</strong>\n                          <p class="wf-subtext">Ratio C/T 0.944 • Protection absolue de l\'élevage d\'Hermetia illucens</p>\n                        </div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-gold">Valider l\'Exérèse Pacemaker & Passer à The Iron Gate →</button>\n                      </div>\n                    </div>\n'}}}},
    {'id': 'UC-424', 'title': 'Exécution Individuelle Interactive des 10 Portes The Iron Gate (G0 à G9)', 'cat': 'Validation Algorithmique', 'actor': 'The Iron Gate Oracle / Superviseur Qualité Filière', 'platforms': ['Terminal Industriel AeterniTrak', "Serveur de Consensus d'Usine"], 'tags': ['TheIronGate', 'G0_G9', 'AntiPrion', '10Portes', 'AutomateDeterministe', 'COSE'], 'summary': "Parcours interactif et séquentiel de l'automate d'évaluation déterministe The Iron Gate vérifiant pas-à-pas les 10 barrières de conformité jusqu'à l'interdiction absolue du recyclage intra-espèce (Règle d'or G7).", 'badge': '10/10 Portes Franchies (AUTHORISED)', 'legalRef': 'Règlement (CE) n° 999/2001 (anti-prion) & Spécification The Iron Gate V1.0.', 'legal': 'Règlement (CE) n° 999/2001 (anti-prion) & Spécification The Iron Gate V1.0.', 'legal_url': '#section-legal', 'preconditions': 'Toutes les données de traçabilité (constat, chaîne du froid, LFA, pacemaker, thermique) consolidées en mémoire.', 'flow': ["Engagement du cycle d'évaluation déterministe de The Iron Gate.", "Vérification séquentielle des Portes G0 à G4 : G0 (Destination & Whitelist), G1 (Taxonomie & Résolution), G2 (Protection Restes Humains), G3 (Catégorie SPA & Substrats), G4 (Dépistage Pentobarbital).", "Application stricte du Feed-Ban européen et de la Règle d'Or Anti-Prion : G5 (Exclusion Ruminants en Source), G6 (Exclusion Ruminants en Cible), G7 (Règle d'Or Anti-Cannibalisme Intra-Espèce).", "Validation des contrôles inter-groupes et thermiques : G8 (Feed-Ban Groupes & Espèces) et G9 (Traitement Sanitaire Requis & Preuve Thermique).", "Délivrance solennelle du verdict : 'AUTHORISED' et calcul du hash de lot."], 'postconditions': 'Lot officiellement autorisé pour scellement cryptographique Ed25519.', 'incident': {'code': 'ERR_IRON_GATE_G7_PRION_BREACH', 'title': "Violation de la Règle d'Or Anti-Prion (Porte G7)", 'message': "Détection d'une destination intra-espèce (feed-ban européen violé). Blocage irrévocable du lot.", 'remediation': 'Séquestre immédiat de la production et destruction sous contrôle vétérinaire officiel.'}, 'wireframe': {'device': 'industrial', 'deviceLabel': "The Iron Gate • Banc d'Évaluation Déterministe G0 à G9", 'formFields': [{'label': 'Matrice des 10 Portes de Fer', 'name': 'gates_matrix', 'type': 'text', 'value': 'G0:OK | G1:OK | G2:OK | G3:OK | G4:OK | G5:OK | G6:OK | G7:OK | G8:OK | G9:OK', 'badge': '10/10 Conforme', 'required': False}, {'label': 'Porte G5 (Exclusion Ruminants en Source)', 'name': 'gate_g5_ruminant_source', 'type': 'text', 'value': 'Source Canis familiaris (TaxID 9615, CARNIVORE) — Zéro Ruminant Source Détecté', 'badge': 'Ruminant Source Exclu', 'required': False}, {'label': 'Porte G6 (Exclusion Ruminants en Cible)', 'name': 'gate_g6_ruminant_target', 'type': 'text', 'value': 'Usage memorial_forestry — Zéro Ruminant Cible Alimentaire', 'badge': 'Ruminant Cible Exclu', 'required': False}, {'label': "Porte G7 (Règle d'Or Anti-Cannibalisme Intra-Espèce)", 'name': 'gate_g7_prion', 'type': 'text', 'value': "TaxID 9615 -> Destination Mémorielle Sylvicole (Règle d'Or Anti-Cannibalisme Respectée)", 'badge': 'Anti-Cannibalisme OK', 'required': False}, {'label': 'Porte G9 (Traitement Sanitaire Requis & Preuve Thermique)', 'name': 'gate_g9_thermal', 'type': 'text', 'value': 'Pasteurisation 70°C continue 62 min (Preuve Thermique SHA-256 Validée)', 'badge': 'Preuve Thermique OK', 'required': False}, {'label': 'Verdict Automate The Iron Gate', 'name': 'gate_verdict', 'type': 'text', 'value': 'AUTHORISED (Certificat de Lot Déverrouillé pour Scellement Ed25519)', 'badge': 'AUTHORISED', 'required': False}], 'actionButtons': [{'id': 'btn_execute_iron_gate_full', 'label': "Lancer l'Évaluation Séquentielle G0 → G9", 'role': 'primary', 'state': 'idle', 'icon': '🛡️'}, {'id': 'btn_step_by_step_gates', 'label': 'Inspecter la Preuve Cryptographique de Chaque Porte', 'role': 'secondary', 'state': 'idle', 'icon': '🔍'}], 'validationMsg': {'title': 'Verdict The Iron Gate : AUTHORISED (10 / 10 Portes Franchies)', 'badge': "Règle d'Or Anti-Prion 100% Respectée", 'detail': 'Toutes les barrières mathématiques franchies. Zéro risque de contamination croisée intra-espèce.'}, 'errorCase': {'code': 'ERR_IRON_GATE_G7_PRION_BREACH', 'title': 'Violation Sanitaire Règle Anti-Prion (G7)', 'condition': 'Tentative de valoriser des protéines animales transformées dans la nutrition de la même espèce animale.', 'message': "BLOCAGE PHYSIQUE IRRÉVOCABLE : Risque de transmission d'encéphalopathies spongiformes (prions).", 'remediation': 'Destruction immédiate du lot par incinération en filière agréée Catégorie 1.'}, 'phases': {'p1': {'tabTitle': '1. Avant Trigger', 'phaseTitle': "Banc d'Évaluation G0-G9 en Attente", 'caption': 'Les 10 Portes de Fer canoniques (G0 à G9) sont chargées pour examen unitaire déterministe.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">The Iron Gate • Barrière Cryptographique</span>\n                        <span class="wf-status-badge wf-badge-neutral">10 Portes Prêtes</span>\n                      </div>\n                      <div class="wf-device-status-box">\n                        <span class="wf-qa-icon">🛡️</span>\n                        <div><strong>Évaluation Déterministe Inviolable G0 à G9</strong></div>\n                        <div class="wf-subtext">Vérification des 10 Portes de Fer canoniques (evaluator.ts) : Destination, Taxonomie, Restes Humains, SPA, Pentobarbital, Feed-Ban et Preuve Thermique</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary">🛡️ Lancer l\'Évaluation Séquentielle G0 → G9</button>\n                      </div>\n                    </div>\n'}, 'p2': {'tabTitle': '2. Déclenchement ⚡', 'phaseTitle': 'Franchissement Déterministe des Portes G0 à G6', 'triggerName': "Exécution de l'Automate", 'caption': 'Validation pas-à-pas des preuves matérielles et sanitaires G0 à G6.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">The Iron Gate • Pipeline Actif</span>\n                        <span class="wf-status-badge wf-badge-trigger">⚡ Test Portes G0-G6</span>\n                      </div>\n                      <div class="wf-trigger-card wf-radar-pulse">\n                        <div class="wf-trigger-indicator">G0: Dest OK | G1: Taxon OK | G2: Restes Humains OK | G3: Cat/Substrats OK | G4: Pentobarbital OK | G5: Non-Ruminant Source OK | G6: Non-Ruminant Cible OK</div>\n                        <div class="wf-subtext">Engin d\'inférence prêt pour la porte critique G7 (Règle d\'Or Anti-Cannibalisme Intra-Espèce)</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Évaluation de la règle anti-prion...</button>\n                      </div>\n                    </div>\n'}, 'p3': {'tabTitle': '3. Traitement ⚙️', 'phaseTitle': "Contrôle Porte G7 : Règle d'Or Anti-Cannibalisme Intra-Espèce", 'progress': 100, 'caption': 'Espèce Canis familiaris : zéro recyclage intra-espèce, portes G8 et G9 franchies.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">The Iron Gate • Porte G7 Validée</span>\n                        <span class="wf-status-badge wf-badge-process">⚙️ Feed-Ban Strict (100%)</span>\n                      </div>\n                      <div class="wf-console-log">\n                        <code>> [GATE-G0] Destination & Whitelist : memorial_forestry supportée</code><br>\n                        <code>> [GATE-G1] Taxonomie & Résolution : TaxID 9615 (Canis familiaris, CARNIVORE)</code><br>\n                        <code>> [GATE-G2] Protection Restes Humains : Matière 100% non-humaine validée</code><br>\n                        <code>> [GATE-G3] Catégorie SPA & Substrats : Catégorie 1 mémorielle exclusive</code><br>\n                        <code>> [GATE-G4] Dépistage Pentobarbital : Négatif LFA qualitatif certifié</code><br>\n                        <code>> [GATE-G5] Exclusion Ruminants en Source : Zéro ruminant source détecté</code><br>\n                        <code>> [GATE-G6] Exclusion Ruminants en Cible : Zéro ruminant cible alimentaire</code><br>\n                        <code>> [GATE-G7] Règle d\'Or Anti-Cannibalisme Intra-Espèce : Zéro recyclage intra-espèce</code><br>\n                        <code>> [GATE-G8] Feed-Ban Groupes & Espèces : Absence de croisement prohibé</code><br>\n                        <code>> [GATE-G9] Traitement Sanitaire Requis & Preuve Thermique : Pasteurisation 70°C / 62 min conforme</code><br>\n                        <code>> [ORACLE-VERDICT] Statut global : AUTHORISED (10 / 10 Portes Canoniques Validées)</code>\n                      </div>\n                    </div>\n'}, 'p4': {'tabTitle': '4. Écran de Fin ✨', 'phaseTitle': 'Feu Vert Émis : Certificat de Lot Déverrouillé', 'status': 'success', 'caption': "The Iron Gate autorise l'émission du certificat officiel AET-SPEC-CERT-001.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">The Iron Gate • Verdict Définitif</span>\n                        <span class="wf-status-badge wf-badge-success">✨ AUTHORISED</span>\n                      </div>\n                      <div class="wf-success-banner">\n                        <span class="wf-seal-icon">🏆</span>\n                        <div>\n                          <strong>Conformité Totale Filière Démontrée</strong>\n                          <p class="wf-subtext">10/10 Portes Canoniques Franchies (G0 à G9) • Règle d\'Or Anti-Prion et Sécurité Sanitaire Garanties</p>\n                        </div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-gold">Signer le Certificat de Lot Ed25519 (AET-SPEC-CERT-001) →</button>\n                      </div>\n                    </div>\n'}}}},
    {'id': 'UC-425', 'title': 'Contrôle Concession Forestière ARNE / DNF & Approbation Parcelle Mémorielle', 'cat': 'Destination Finale', 'actor': 'Garde-Forestier DNF / Agent SPW ARNE', 'platforms': ['Terminal Terrain Robuste DNF', 'PWA Cartographique Hors-Ligne'], 'tags': ['DNF', 'SPW_ARNE', 'ConcessionForestiere', 'CadastreForet', 'ParcelleMémorielle', 'DEC-AET-05'], 'summary': "Validation administrative et écologique par le garde-forestier DNF du titre de concession cinéraire en forêt domaniale, vérification de la capacité d'accueil du sol avant remise des reliques mémorielles.", 'badge': 'Concession DNF Approuvée', 'legalRef': 'Code forestier wallon du 15 juillet 2008 & Accord cadre DNF / Le Pax Funèbre (DEC-AET-05).', 'legal': 'Code forestier wallon du 15 juillet 2008 & Accord cadre DNF / Le Pax Funèbre (DEC-AET-05).', 'legal_url': '#section-legal', 'preconditions': "Certificat de lot AET-SPEC-CERT-001 émis et famille sollicitant l'arbre du souvenir en massif domanial.", 'flow': ['Saisie de la référence de concession forestière DNF (ex: CONC-DNF-2026-LIEGE-0482).', 'Vérification cartographique SIG de la parcelle cadastrale boisée (Cantonnement de Liège / Sart-Tilman).', "Contrôle du quota d'amendement phosphocalcique toléré pour le biome forestier (seuil < 0.50 kg/m²).", "Signature numérique de l'agrément parcellaire par le garde-forestier DNF habilité.", 'Inscription définitive au registre des concessions cinéraires séculaires sous dérogation DEC-AET-05.'], 'postconditions': "Autorisation d'inhumation/épandage cinéraire accordée, parcelle protégée pour 99 ans.", 'incident': {'code': 'ERR_FORESTRY_PARCEL_CAPACITY_EXCEEDED', 'title': 'Capacité Écologique de la Parcelle Forestière Saturée', 'message': "Le quota d'arbres mémoriels ou d'amendement minéral de la parcelle est atteint.", 'remediation': 'Réaffecter la concession cinéraire vers une parcelle adjacente sous gestion durable DNF.'}, 'wireframe': {'device': 'industrial', 'deviceLabel': 'Terminal DNF Mobile • Cadastre des Sépultures Forestières', 'formFields': [{'label': 'Titre de Concession DNF', 'name': 'dnf_concession_ref', 'type': 'text', 'value': 'CONC-DNF-2026-LIEGE-0482 (Massif Domanial du Sart-Tilman)', 'badge': 'Bail Cinéraire', 'required': True}, {'label': 'Parcelle Cadastrale & Arbre', 'name': 'dnf_parcel_tree', 'type': 'text', 'value': 'Division 4, Section B, Parcelle 104/A • Chêne Noble #42', 'badge': 'Arbre Répertorié', 'required': False}, {'label': 'Charge Minérale Sol Mesurée', 'name': 'soil_mineral_load', 'type': 'text', 'value': "0.14 kg/m² (Seuil d'équilibre sylvicole maximal : 0.50 kg/m²)", 'badge': 'Équilibre Vert', 'required': False}, {'label': 'Agent DNF Instrumentant', 'name': 'dnf_agent_badge', 'type': 'text', 'value': 'Matricule DNF-AGENT-5491 (Cantonnement de Liège - SPW ARNE)', 'badge': 'Garde Forestier', 'required': False}], 'actionButtons': [{'id': 'btn_approve_dnf_parcel', 'label': "Approuver la Concession & Signer l'Affectation Parcellaire", 'role': 'primary', 'state': 'idle', 'icon': '🌲'}, {'id': 'btn_inspect_forestry_cadastre', 'label': 'Consulter le Registre Cadastral DNF Hors-Ligne', 'role': 'secondary', 'state': 'idle', 'icon': '🗺️'}], 'validationMsg': {'title': 'Concession Forestière DNF Approuvée', 'badge': 'Parcelle 104/A Validée', 'detail': 'Amendement mémoriel conforme aux équilibres sylvicoles. Inscription au cadastre DNF scellée pour 99 ans.'}, 'errorCase': {'code': 'ERR_FORESTRY_PARCEL_CAPACITY_EXCEEDED', 'title': 'Quota Écologique de Parcelle Atteint', 'condition': 'La charge minérale cumulée dépasse le seuil sylvicole autorisé pour la protection des sols.', 'message': "ALERTE ÉCOLOGIQUE : La parcelle a atteint son quota d'accueil mémoriel pour cette décennie.", 'remediation': 'Proposer à la famille un chêne de substitution sur la parcelle 105/C en régénération.'}, 'phases': {'p1': {'tabTitle': '1. Avant Trigger', 'phaseTitle': 'Examen de la Concession Cinéraire Forestière', 'caption': "Le garde DNF vérifie l'éligibilité de la parcelle pour le repos mémoriel.", 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">DNF • Sépultures Forestières</span>\n                        <span class="wf-status-badge wf-badge-neutral">Dossier en Attente</span>\n                      </div>\n                      <div class="wf-device-status-box">\n                        <span class="wf-qa-icon">🌲</span>\n                        <div><strong>Agrément Sylvicole Parcelle 104/A</strong></div>\n                        <div class="wf-subtext">Contrôle de la capacité phosphocalcique et affectation du Chêne #42</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary">🌲 Approuver la Concession & Signer l\'Affectation Parcellaire</button>\n                      </div>\n                    </div>\n'}, 'p2': {'tabTitle': '2. Déclenchement ⚡', 'phaseTitle': 'Vérification Cadastrale SIG & Charge du Sol', 'triggerName': 'Validation Garde DNF', 'caption': 'Contrôle cartographique et balance écologique du sol forestier.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">DNF • SIG Cadastral</span>\n                        <span class="wf-status-badge wf-badge-trigger">⚡ Analyse Sol 104/A</span>\n                      </div>\n                      <div class="wf-trigger-card wf-radar-pulse">\n                        <div class="wf-trigger-indicator">Charge minérale : 0.14 kg/m² sur limite tolérée 0.50 kg/m²</div>\n                        <div class="wf-subtext">Parcelle écologiquement réceptive • Zéro impact négatif sur la faune</div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Scellement de la concession...</button>\n                      </div>\n                    </div>\n'}, 'p3': {'tabTitle': '3. Traitement ⚙️', 'phaseTitle': 'Signature Numérique Garde-Forestier & Ancrage', 'progress': 100, 'caption': 'Bail cinéraire forestier scellé pour 99 ans sous dérogation DEC-AET-05.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">DNF • Visa Forestier</span>\n                        <span class="wf-status-badge wf-badge-process">⚙️ Agrément Émis (100%)</span>\n                      </div>\n                      <div class="wf-console-log">\n                        <code>> [DNF-CADASTRE] Parcelle 104/A, Cantonnement Liège</code><br>\n                        <code>> [ARBRE] Chêne séculaire #42 géoréférencé 50.4182° N, 5.8821° E</code><br>\n                        <code>> [DÉROGATION] DEC-AET-05 appliquée pour valorisation cinéraire noble</code><br>\n                        <code>> [SIGNATURE] Agent DNF-5491 -> Approbation enregistrée</code>\n                      </div>\n                    </div>\n'}, 'p4': {'tabTitle': '4. Écran de Fin ✨', 'phaseTitle': 'Sanctuaire Forestier Officiellement Consacré', 'status': 'success', 'caption': 'La famille peut désormais se recueillir en toute sérénité sous les frondaisons.', 'screenHtml': '\n                    <div class="wf-screen-box">\n                      <div class="wf-header-bar">\n                        <span class="wf-app-title">DNF • Sanctuaire Ouvert</span>\n                        <span class="wf-status-badge wf-badge-success">✨ Parcelle Consacrée</span>\n                      </div>\n                      <div class="wf-success-banner">\n                        <span class="wf-seal-icon">🍃</span>\n                        <div>\n                          <strong>Concession Cinéraire Active</strong>\n                          <p class="wf-subtext">Repos mémoriel garanti sous la protection du Code forestier wallon</p>\n                        </div>\n                      </div>\n                      <div class="wf-btn-row">\n                        <button class="wf-btn wf-btn-gold">Générer le Livret Mémoriel Forestier de la Famille →</button>\n                      </div>\n                    </div>\n'}}}}
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
        "location_name": "Domicile du déclarant / Clinique (Liège)",
        "location_details": "Domicile du déclarant / Clinique Vétérinaire (Liège, Sart-Tilman - GPS: 50.6333° N, 5.5667° E)",
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
        "location_name": "Itinéraire Transit Agréé E25 (Rocade Sud)",
        "location_details": "Trajet Domicile -> Centre Logistique Liège (Transit E25 / Rocade Sud - GPS: 50.6120° N, 5.5340° E)",
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
        "location_name": "Unité Centrale AeterniTrak Liège (Cellule #B4)",
        "location_details": "Unité Centrale AeterniTrak Liège, Rue de l'Énergie 12, Sart-Tilman (GPS: 50.6412° N, 5.5721° E)",
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
        "location_name": "Salle Technique Stérile & BioLab AeterniCore",
        "location_details": "Laboratoire de Préparation Stérile & Contrôles Amonts, Liège (GPS: 50.6412° N, 5.5721° E)",
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
        "summary": "Préparation sanitaire amont obligatoire : exérèse validée du stimulateur cardiaque (pacemaker) selon Art. L1232-24 CDLD & Modèle IIIC réglementaire avant toute incinération ou traitement thermique, dépistage toxicologique qualitatif LFA du pentobarbital (cassette C+T visibles = absence de produit létal, conforme), et prélèvements PCR épizooties selon le profil de dépouille.",
        "form_fields": [
            {"label": "Exérèse Stimulateur Cardiaque", "name": "pacemaker_excision", "type": "select", "value": "Explantation Validée • Dispositif Medtronic S/N 84920 Retiré", "badge": "Sécurité Incendie/Explosion"},
            {"label": "Test LFA Pentobarbital (Barbituriques)", "name": "lfa_pento_result", "type": "select", "value": "NÉGATIF / CONFORME (Lignes C et T Visibles)", "badge": "Conforme Sans Résidu"},
            {"label": "Dépistage Épizooties (PCR)", "name": "pcr_screening", "type": "text", "value": "Non requis pour chien de compagnie (Prélèvement conservé)", "badge": "Profil 1 Exclusif"},
            {"label": "Dénaturation Chimique (si Cat 1 MRS)", "name": "denaturation_blue", "type": "text", "value": "Sans objet pour Profil 1 (Réservé abattoir MRS)", "badge": "Ligne Mémorielle"},
            {"label": "Feu Vert Sanitaire Amont", "name": "upstream_clearance", "type": "text", "value": "ACCORDÉ : Autorisation de passage en bioconversion", "badge": "Porte G4 Ouverte"}
        ],
        "action_label": "⚡ Valider les Contrôles Amonts & Signer l'Exérèse",
        "linked_ucs": ["UC-403", "UC-407", "UC-411"],
        "legal_basis": "Art. L1232-24 CDLD & Modèle IIIC réglementaire (exérèse stimulateurs cardiaques) & Notice officielle kits LFA AFSCA"
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
        "location_name": "Sas Hermétique de Bioconversion & Autoclaves HP",
        "location_details": "Unité de Bioconversion Hermetia illucens & Traitement Thermique, Liège (GPS: 50.6412° N, 5.5721° E)",
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
        "location_name": "Salon Solennel d'Hommage & Forêt DNF",
        "location_details": "Salon de Remise Solennelle PaxFunèbre Liège & Forêt DNF (GPS: 50.6412° N, 5.5721° E)",
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
