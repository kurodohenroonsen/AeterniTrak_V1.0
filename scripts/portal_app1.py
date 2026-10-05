#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeterniTrak V1.0 — Définition Complète des Micro Use-Cases pour App 1 : PaxStudio Design (UC-101 à UC-125)
Avec Simulateur de Wireframes Interactifs à 4 États, Spécifications des Formulaires, Actions, Validations et Erreurs Normatives.
"""

APP1_USECASES = [
    {
        "id": "UC-101",
        "title": "Choix des Modèles de Carte & Médaillons (Sanctuaire & Directives)",
        "cat": "Gabarits & Modèles",
        "actor": "Famille & Conseiller Funéraire",
        "platforms": ["Web Standard (PWA Hors-Ligne)", "Natif (iOS & Android)"],
        "tags": ["Gabarits", "CarteSanctuaire", "CarteDirectives", "Medaillon35mm"],
        "preconditions": "Ouverture de la session PaxStudio Design sur tablette ou PC en salon des familles.",
        "flow": [
            "Sélection du format physique : Carte CR-80 standard (85.6 x 53.98 mm) ou Médaillon circulaire (diamètre 35 mm).",
            "Attribution du rôle de chaque carte : Carte 1 Sanctuaire (mémoriel affectif) et Carte 2 Directives (directives civiles, médicales et administratives).",
            "Choix de la matière noble : Carte polycarbonate or satiné, résine composite noire obsidienne ou médaillon en titane anodisé.",
            "Chargement immédiat des contraintes d'impression thermique/laser et de la zone d'exclusion de l'antenne NFC."
        ],
        "postconditions": "Le gabarit vectoriel est calibré au dixième de millimètre pour le double recto/verso.",
        "legal": "Norme ISO/IEC 7810 ID-1 (spécifications des cartes physiques d'identification).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "tablet",
            "deviceLabel": "PaxStudio Pro • iPad Pro Canvas (2732×2048)",
            "formFields": [
                {"label": "Format Physique", "name": "card_format", "type": "select", "value": "Médaillon Circulaire ø35mm", "placeholder": "Sélectionner le format", "badge": "Requis", "required": True},
                {"label": "Double Support", "name": "card_role", "type": "select", "value": "Carte 1 Sanctuaire + Carte 2 Directives", "placeholder": "Rôle des cartes", "badge": "Dédié", "required": True},
                {"label": "Matière Noble", "name": "material_finish", "type": "select", "value": "Titane Anodisé Or & Obsidienne", "placeholder": "Sélectionner le matériau", "badge": "Finition", "required": True},
                {"label": "Zone Exclusion Antenne", "name": "nfc_margin", "type": "text", "value": "5.0 mm bords (ISO 7810 ID-1)", "placeholder": "Marge de sécurité", "badge": "Lecture Seule", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_validate_format", "label": "Valider le Gabarit Physique", "role": "primary", "state": "idle", "icon": "📐"},
                {"id": "btn_reset_format", "label": "Réinitialiser", "role": "secondary", "state": "idle", "icon": "↩"}
            ],
            "validationMsg": {
                "title": "Gabarit Physique Initialisé",
                "badge": "Conforme ISO/IEC 7810 ID-1",
                "detail": "Cotes 85.6x53.98mm et ø35mm verrouillées. Marge d'antenne NFC réservée (5mm)."
            },
            "errorCase": {
                "code": "ERR_INVALID_CARD_FORMAT",
                "title": "Format Physique Non Conforme",
                "condition": "Sélection d'une épaisseur hors norme (> 0.84 mm) ou dimensions non normalisées.",
                "message": "Erreur critique : Le gabarit sélectionné viole la norme ISO/IEC 7810 ID-1 pour les cartes sans contact.",
                "remediation": "Restreindre le choix aux deux gabarits officiels : CR-80 standard ou Médaillon 35mm homologué ACOSJ."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Sélection du Gabarit Vierge & Matériau",
                    "caption": "Formulaire vierge en attente. Aucun format sélectionné, bouton de validation grisé.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Configuration du Support Physique</span>
                        <span class="wf-status-badge wf-badge-neutral">En Attente de Saisie</span>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-field-group">
                          <label class="wf-label">Format de Support <span class="wf-req">*</span></label>
                          <div class="wf-select-placeholder">-- Sélectionner : CR-80 ou Médaillon ø35mm --</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Rôle des Puces Silicium <span class="wf-req">*</span></label>
                          <div class="wf-select-placeholder">Carte 1 Sanctuaire + Carte 2 Directives</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Matière Noble & Teinte</label>
                          <div class="wf-select-placeholder">Titane Anodisé Or Satiné & Obsidienne</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-disabled" disabled>📐 Valider le Gabarit (Inactif)</button>
                        <button class="wf-btn wf-btn-sub">↩ Réinitialiser</button>
                      </div>
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Tap Tactile de Sélection du Médaillon",
                    "triggerName": "Tap sur le gabarit 'Médaillon ø35mm' et clic 'Valider'",
                    "caption": "Action utilisateur en cours : mise en évidence avec onde radar dorée et activation du bouton.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Sélection Active</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Événement Tap Détecté</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">⚡ Action Déclenchante : Tap sur le Format Médaillon 35mm</div>
                        <div class="wf-selection-summary">
                          <strong>Sélectionné :</strong> Médaillon ø35mm • Titane Or & Obsidienne • Antenne Intégrée
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">📐 Valider le Gabarit Physique (Clic Actif)</button>
                      </div>
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Calibration Vectorielle Submillimétrique",
                    "progress": 72,
                    "caption": "Calcul en temps réel des zones d'exclusion antenne et des repères laser de gravure.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Moteur de Calibration Vectorielle</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Traitement Actif (72%)</span>
                      </div>
                      <div class="wf-progress-container">
                        <div class="wf-progress-bar" style="width: 72%;"></div>
                      </div>
                      <div class="wf-console-log">
                        <code>> [CAD-ENGINE] Initialisation du système de coordonnées polaires ø35.00mm...</code><br>
                        <code>> [CAD-ENGINE] Application marge de sécurité antenne RF (ISO 7810 ID-1 : 5.0mm) : OK</code><br>
                        <code>> [CAD-ENGINE] Alignement repères laser recto (portrait) & verso (épitaphe) : 100%</code>
                      </div>
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Gabarit Calibré & Zone d'Impression Scellée",
                    "status": "success",
                    "caption": "Gabarit verrouillé avec succès. Cotes vectorielles conformes et bouton 'Design 3D' déverrouillé.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Gabarit Homologué</span>
                        <span class="wf-status-badge wf-badge-success">✨ Validé & Verrouillé</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🏆</span>
                        <div>
                          <strong>Gabarit Vectoriel Prêt pour Personnalisation 3D</strong>
                          <p class="wf-subtext">Médaillon Titane ø35mm • Double Face Recto/Verso • Conforme ISO/IEC 7810 ID-1</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Passer à l'Étape 2 : Prévisualisation 3D →</button>
                      </div>
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-102",
        "title": "Prévisualisation 3D Interactive Recto/Verso avec Rendu Or & Mat",
        "cat": "Rendu 3D & Matériaux",
        "actor": "Famille",
        "platforms": ["Web Standard (PWA Hors-Ligne)", "Natif (iOS & Android)"],
        "tags": ["WebGL", "ThreeJS", "PBR", "Rendu3D"],
        "preconditions": "Modèle de carte sélectionné avec textures haute résolution chargées.",
        "flow": [
            "Génération du maillage 3D photoréaliste de la carte avec shader PBR (Physically Based Rendering).",
            "La famille fait pivoter la carte d'un simple glissement de doigt pour inspecter le recto (portrait et nom) et le verso (épitaphe et puce).",
            "Simulation réaliste de la lumière rasante révélant les dorures à chaud et le relief tactile du logo Le Pax Funèbre.",
            "Bascule instantanée entre la Carte Sanctuaire et la Carte Directives."
        ],
        "postconditions": "Validation visuelle en temps réel sans nécessiter d'impression d'épreuve papier intermédiaire.",
        "legal": "Code de droit économique belge (art. VI.45 - obligation d'information précontractuelle claire) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "tablet",
            "deviceLabel": "PaxStudio Pro • Visionneuse 3D PBR WebGL",
            "formFields": [
                {"label": "Shader PBR Actif", "name": "shader_type", "type": "select", "value": "Dorure Or 24k + Mat Velours", "placeholder": "Choix du shader", "badge": "Rendu PBR", "required": True},
                {"label": "Angle de Lumière Rasante", "name": "light_angle", "type": "range", "value": "45° Nord-Est", "placeholder": "Axe d'éclairage", "badge": "Dynamique", "required": False},
                {"label": "Face Active", "name": "view_face", "type": "radio", "value": "Recto (Portrait Mémoriel)", "placeholder": "Face affichée", "badge": "360°", "required": True}
            ],
            "actionButtons": [
                {"id": "btn_rotate_3d", "label": "Pivoter Recto / Verso (360°)", "role": "primary", "state": "idle", "icon": "🔄"},
                {"id": "btn_export_preview", "label": "Capturer Bon Visuel HD", "role": "secondary", "state": "idle", "icon": "📸"}
            ],
            "validationMsg": {
                "title": "Rendu 3D PBR Conforme",
                "badge": "60 FPS Fluidité Native",
                "detail": "Textures PBR validées. Reflets spéculaires et micro-reliefs tactilement conformes."
            },
            "errorCase": {
                "code": "ERR_WEBGL_CONTEXT_LOST",
                "title": "Perte du Contexte Graphique WebGL",
                "condition": "Saturation mémoire GPU ou mise en veille prolongée du terminal mobile.",
                "message": "Erreur d'affichage : Le moteur 3D PBR a perdu le contexte matériel GPU.",
                "remediation": "Réinitialisation automatique du contexte WebGL et bascule temporaire en rendu 2D haute définition."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Canevas 3D Initial en Attente de Manipulation",
                    "caption": "Maillage 3D neutre chargé. La carte est fixe, vue de face, prête à l'inspection tactile.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Visionneuse 3D PBR Temps Réel</span>
                        <span class="wf-status-badge wf-badge-neutral">Face Recto • Éclairage Fixe</span>
                      </div>
                      <div class="wf-3d-viewport">
                        <div class="wf-card-mockup-3d">
                          <div class="wf-gold-border"></div>
                          <div class="wf-portrait-slot">👤 Portrait Mémoriel HD</div>
                          <div class="wf-name-slot">Henri Dubois (1944 - 2026)</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🔄 Pivoter Recto / Verso (En attente de glissement)</button>
                        <button class="wf-btn wf-btn-sub">📸 Capturer Vue</button>
                      </div>
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Geste de Glissement Tactile 360° (Swipe)",
                    "triggerName": "Glissement du doigt sur l'écran tactile pour faire pivoter la carte",
                    "caption": "Mise en évidence du vecteur de rotation avec anneau de force dynamique.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Interaction Tactile 3D</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Geste Swipe Détecté</span>
                      </div>
                      <div class="wf-3d-viewport wf-radar-pulse">
                        <div class="wf-card-mockup-3d wf-rotating">
                          <div class="wf-rotation-vector">↻ Rotation Angulaire : +145° (Bascule Verso)</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">🔄 Rotation 3D en Cours...</button>
                      </div>
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Calcul du Shader PBR & Lumière Rasante 45°",
                    "progress": 85,
                    "caption": "Le moteur WebGL recalcule les ombrages, dorures à chaud et le relief de l'épitaphe.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Calcul Shaders PBR</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Rendu PBR Actif (85%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 85%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [PBR-SHADER] Éclairage spéculaire 45° sur la dorure à chaud : OK</code><br>
                        <code>> [PBR-SHADER] Rendu micro-relief logo Le Pax Funèbre : 60 FPS constant</code><br>
                        <code>> [PBR-SHADER] Texture verso ACOSJ 92k et antenne sans contact simulée</code>
                      </div>
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Verso Inspecté & Épreuve Visuelle Validée",
                    "status": "success",
                    "caption": "Carte pivotée à 180° révélant le verso solennel. Épreuve numérique sans papier acceptée.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Épreuve 3D Validée</span>
                        <span class="wf-status-badge wf-badge-success">✨ Rendu Verso Validé</span>
                      </div>
                      <div class="wf-3d-viewport">
                        <div class="wf-card-mockup-verso">
                          <div class="wf-epitaph-slot">« Le souvenir est une présence invisible dans la paix des bois »</div>
                          <div class="wf-chip-slot">💾 Emplacement Silicium JavaCard ACOSJ 92 Ko</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Valider l'Épreuve & Passer aux Couleurs →</button>
                      </div>
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-103",
        "title": "Colorimétrie, Dorures & Typographies Solennelles",
        "cat": "Design & Esthétique",
        "actor": "Conseiller & Famille",
        "platforms": ["Web Standard (PWA Hors-Ligne)", "Natif (iOS & Android)"],
        "tags": ["Palette", "Dorures", "Typographie", "Harmonie"],
        "preconditions": "Photo principale importée dans le canevas de création.",
        "flow": [
            "Extraction algorithmique de la palette chromatique dominante de la photo (couleurs chaudes, froides, sépia).",
            "Proposition automatique d'une harmonie chromatique : or impérial, argent lunaire ou noir onyx.",
            "Sélection parmi 6 polices de caractères funéraires intemporelles (Outfit, Cormorant Garamond, Cinzel, JetBrains Mono pour les données).",
            "Ajustement du contraste et contrôle de lisibilité selon les normes d'accessibilité visuelle pour personnes âgées."
        ],
        "postconditions": "Charte graphique de la carte arrêtée et conforme à la dignité de la cérémonie.",
        "legal": "Règlement général sur l'accessibilité des services (Directive européenne 2019/882) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "tablet",
            "deviceLabel": "PaxStudio Pro • Palette Chromatique & Typographies",
            "formFields": [
                {"label": "Harmonie Chromatique", "name": "color_scheme", "type": "select", "value": "Or Impérial & Noir Obsidienne", "placeholder": "Palette", "badge": "Harmonie", "required": True},
                {"label": "Police Solennelle (Titres)", "name": "font_title", "type": "select", "value": "Cormorant Garamond (Sérif Solennel)", "placeholder": "Typographie titres", "badge": "Typo", "required": True},
                {"label": "Police Technique (Données)", "name": "font_mono", "type": "text", "value": "JetBrains Mono (ISO 7816 & Hash)", "placeholder": "Typographie données", "badge": "Lecture Seule", "required": False},
                {"label": "Ratio Contraste WCAG AAA", "name": "a11y_ratio", "type": "text", "value": "14.8:1 (Seuil mini: 7.0:1)", "placeholder": "Contraste", "badge": "Accessible", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_apply_palette", "label": "Appliquer la Charte Typographique", "role": "primary", "state": "idle", "icon": "🎨"},
                {"id": "btn_a11y_check", "label": "Vérifier Lisibilité Seniors", "role": "secondary", "state": "idle", "icon": "👁"}
            ],
            "validationMsg": {
                "title": "Charte Typographique Validée",
                "badge": "Conforme Directive 2019/882",
                "detail": "Contraste 14.8:1 validé pour personnes âgées. Cormorant Garamond et dorures harmonisées."
            },
            "errorCase": {
                "code": "ERR_A11Y_CONTRAST_DEFICIT",
                "title": "Contraste Typographique Insuffisant",
                "condition": "Texte doré clair sur fond blanc ou gris perle résultant en un ratio inférieur à 4.5:1.",
                "message": "Erreur d'accessibilité : Le contraste calculé viole la Directive européenne 2019/882 pour la lisibilité des seniors.",
                "remediation": "Forcer le fond en noir obsidienne ou rehausser le liseré d'ombrage typographique."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Palette Par Défaut en Attente d'Harmonisation",
                    "caption": "Formulaire avec palette standard. L'analyse chromatique de la photo n'est pas encore lancée.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Nuancier & Typographies</span>
                        <span class="wf-status-badge wf-badge-neutral">Palette Standard Non Calibrée</span>
                      </div>
                      <div class="wf-field-group">
                        <label class="wf-label">Harmonie Proposée</label>
                        <div class="wf-select-placeholder">Palette Par Défaut (Gris neutre / Blanc)</div>
                      </div>
                      <div class="wf-field-group">
                        <label class="wf-label">Typographie Solennelle</label>
                        <div class="wf-select-placeholder">Sans-serif Standard</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🎨 Extraire Harmonie depuis la Photo</button>
                      </div>
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Clic sur 'Extraire Harmonie depuis la Photo'",
                    "triggerName": "Clic déclencheur sur l'outil d'extraction automatique de palette",
                    "caption": "Animation de scan spectral sur les pixels de la photo du défunt.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Scan Chromatique</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Scan Spectrophotométrique</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">⚡ Événement : Détection des pigments dominants de la photo</div>
                        <div class="wf-subtext">Couleurs détectées : Or sépia, ambre chaud, noir onyx profond</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Calcul de l'Harmonie Or Impérial...</button>
                      </div>
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Vérification WCAG AAA & Ajustement Typographique",
                    "progress": 90,
                    "caption": "Calcul mathématique du contraste des textes dorés selon les algorithmes WCAG 2.2.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Moteur d'Accessibilité WCAG</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Contrôle Lisibilité (90%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 90%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [A11Y] Test contraste texte 'Or #d4af37' sur fond 'Obsidienne #06070b'...</code><br>
                        <code>> [A11Y] Ratio mesuré : 14.82:1 (Exigence AAA : >= 7.0:1) : SUCCÈS</code><br>
                        <code>> [FONT] Chargement glyphes solennels Cormorant Garamond avec ligatures funéraires</code>
                      </div>
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Harmonie Or Impérial & Obsidienne Appliquée",
                    "status": "success",
                    "caption": "Typographie Cormorant Garamond dorée gravée avec succès sur le modèle de carte.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Charte Arrêtée</span>
                        <span class="wf-status-badge wf-badge-success">✨ Conforme Directive 2019/882</span>
                      </div>
                      <div class="wf-card-specimen">
                        <span class="wf-gold-title">Henri Dubois</span>
                        <span class="wf-gold-dates">1944 — 2026</span>
                        <span class="wf-a11y-badge">✓ Ratio 14.8:1 Certifié Senior</span>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Studio Photo WebP →</button>
                      </div>
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-104",
        "title": "Studio Photo & Carrousel Portraits WebP (Jalon STORAGE-001)",
        "cat": "Médias Visuels",
        "actor": "Famille & Conseiller",
        "platforms": ["Web Standard (PWA Hors-Ligne)", "Natif (iOS & Android)"],
        "tags": ["WebP", "Portraits", "Carrousel", "STORAGE-001"],
        "preconditions": "Photos de famille transmises sur clé USB ou via smartphone.",
        "flow": [
            "Import des photographies mémorielles du défunt dont le volume et le format respectent les quotas alloués par le jalon technique STORAGE-001.",
            "Outil de cadrage circulaire adapté au médaillon avec détection automatique du visage.",
            "Compression algorithmique en WebP sans perte perceptible, calibrée sous le seuil maximal de 48 Ko de la partition EF-3.",
            "Génération du carrousel de 3 portraits solennels prêts pour l'injection dans le silicium."
        ],
        "postconditions": "Portraits compressés et dimensionnés à 480×480 pixels (WebP max 20 Ko / 20 480 octets, conforme DEC-AET-12), empreintes SHA-256 enregistrées.",
        "legal": "Règlement général sur la protection des données (RGPD art. 5 - minimisation des données) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "tablet",
            "deviceLabel": "PaxStudio Pro • Studio Photo & Compression WebP (STORAGE-001)",
            "formFields": [
                {"label": "Fichier Source", "name": "source_photo", "type": "file", "value": "portrait_famille_hd.jpg (4.2 Mo)", "placeholder": "Choisir une photo", "badge": "Source HD", "required": True},
                {"label": "Résolution Cible", "name": "crop_dim", "type": "text", "value": "480 × 480 pixels (WebP max 20 Ko / 20 480 octets, conforme DEC-AET-12)", "placeholder": "Dimensions", "badge": "DEC-AET-12", "required": True},
                {"label": "Quota Partition EF-3", "name": "quota_ef3", "type": "text", "value": "Budget Max : 48 Ko (STORAGE-001)", "placeholder": "Quota puce", "badge": "Silicium", "required": False},
                {"label": "Taille Compressée", "name": "webp_size", "type": "text", "value": "12.4 Ko (Consommation : 25.8% du budget)", "placeholder": "Poids final", "badge": "Optimisé", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_crop_compress", "label": "Rogner 480×480 & Compresser WebP (DEC-AET-12)", "role": "primary", "state": "idle", "icon": "✂️"},
                {"id": "btn_add_carousel", "label": "Ajouter au Carrousel (Max 3)", "role": "secondary", "state": "idle", "icon": "➕"}
            ],
            "validationMsg": {
                "title": "Portraits WebP Validés",
                "badge": "Jalon STORAGE-001 Conforme",
                "detail": "Poids total 37.2 Ko pour 3 portraits. Quota partition EF-3 (48 Ko) respecté."
            },
            "errorCase": {
                "code": "ERR_PROFILE_TOO_LARGE",
                "title": "Dépassement du Quota Silicium EF-3",
                "condition": "Import d'images dont le poids compressé cumulé excède 48 Ko (limite matérielle de l'ACOSJ 92k).",
                "message": "Erreur critique : La taille cumulée des médias (52.4 Ko) dépasse le budget strict de 48 Ko alloué par STORAGE-001.",
                "remediation": "Abaisser la résolution de quantification WebP ou limiter le carrousel à 2 portraits."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Zone de Glisser-Déposer de Photo Brute",
                    "caption": "Photo HD de 4.2 Mo chargée. Outil de cadrage circulaire en attente, bouton de compression inactif.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Studio Photo</span>
                        <span class="wf-status-badge wf-badge-neutral">Photo Brute 4.2 Mo Chargée</span>
                      </div>
                      <div class="wf-dropzone-box">
                        <span class="wf-file-icon">🖼️</span>
                        <div><strong>portrait_famille_hd.jpg</strong> (4 210 Ko)</div>
                        <div class="wf-subtext">Cadrage circulaire 480×480 et compression WebP (max 20 Ko / 20 480 octets, conforme DEC-AET-12) requis</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">✂️ Rogner 480×480 & Compresser WebP (DEC-AET-12)</button>
                      </div>
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Clic sur 'Rogner 480×480 & Compresser WebP (DEC-AET-12)'",
                    "triggerName": "Déclenchement du rognage facial automatique 480x480 pixels (DEC-AET-12)",
                    "caption": "Détection automatique des contours du visage et application du masque médaillon.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Rognage Facial</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Détection Biométrique du Visage</span>
                      </div>
                      <div class="wf-crop-canvas wf-radar-pulse">
                        <div class="wf-circle-crop-guide">
                          <span class="wf-crop-label">Cible 480×480 px (DEC-AET-12) • Centrage automatique</span>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Encodage WebP en cours...</button>
                      </div>
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Compression Algorithmique WebP & Vérification Quota",
                    "progress": 68,
                    "caption": "Compression sans perte perceptible et vérification stricte du budget STORAGE-001 (48 Ko max).",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Compresseur WebP Local</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Compression en Cours (68%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 68%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [WEBP-CORE] Rééchantillonnage 480x480 bicubique (DEC-AET-12) : OK</code><br>
                        <code>> [WEBP-CORE] Quantification colorimétrique sans perte perceptible : 12.4 Ko</code><br>
                        <code>> [STORAGE-001] Quota partition EF-3 vérifié : 12.4 Ko / 48.0 Ko (Conforme)</code>
                      </div>
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Portrait Mémoriel Scellé dans le Carrousel",
                    "status": "success",
                    "caption": "Photo optimisée prête pour gravure silicium. Jauge mémoire verte affichée.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Photo Prête Silicium</span>
                        <span class="wf-status-badge wf-badge-success">✨ Validé (12.4 Ko)</span>
                      </div>
                      <div class="wf-carousel-preview">
                        <div class="wf-portrait-thumb">👤 Portrait 1 (12.4 Ko)</div>
                        <div class="wf-portrait-empty">+ Slot 2</div>
                        <div class="wf-portrait-empty">+ Slot 3</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Studio Vocal Waveform →</button>
                      </div>
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-105",
        "title": "Studio Vocal & Oscilloscope Waveform Crop (Anti-Gestes Android)",
        "cat": "Médias Sonores",
        "actor": "Famille & Conseiller",
        "platforms": ["Web Standard (PWA Hors-Ligne)", "Natif (iOS & Android)"],
        "tags": ["Waveform", "AudioCrop", "AntiGestesAndroid", "WebAudio"],
        "preconditions": "Fichier audio vocal brut importé (message d'adieu, bénédiction, souvenir).",
        "flow": [
            "Affichage de la forme d'onde dynamique interactive (oscilloscope WebAudio) sur l'écran tactile.",
            "Manipulation des curseurs temporels de début et fin pour rogner l'extrait solennel sans déclencher les gestes de retour système Android (zone d'exclusion gestuelle appliquée).",
            "Filtre coupe-bas automatique éliminant les bruits de souffle et de manipulation du microphone.",
            "Normalisation du niveau d'écoute à -23 LUFS (recommandation broadcast funéraire solennelle)."
        ],
        "postconditions": "Extrait audio vocal calibré à une durée maximale de 30 secondes, prêt pour l'intégration.",
        "legal": "Code de la santé publique (protection de l'intégrité morale du recueillement) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "tablet",
            "deviceLabel": "PaxStudio Pro • Oscilloscope Vocal & Anti-Gestes Android",
            "formFields": [
                {"label": "Fichier Brut", "name": "audio_raw", "type": "file", "value": "temoignage_vocal.m4a (1 min 30 s)", "placeholder": "Audio brut", "badge": "Source", "required": True},
                {"label": "Curseur Début", "name": "crop_start", "type": "text", "value": "00:05.200", "placeholder": "Début", "badge": "Découpe", "required": True},
                {"label": "Curseur Fin", "name": "crop_end", "type": "text", "value": "00:35.200 (Durée : 30.0 s)", "placeholder": "Fin", "badge": "Max 30s", "required": True},
                {"label": "Normalisation EBU R128", "name": "ebu_lufs", "type": "text", "value": "-23 LUFS (Filtre anti-souffle actif)", "placeholder": "Volume", "badge": "Audio Pro", "required": False},
                {"label": "Quota Partition EF-3 (Voice)", "name": "voice_memo_quota", "type": "text", "value": "26.1 Ko (Strictement ≤ 46 080 octets, Opus SILK)", "placeholder": "Poids audio", "badge": "≤ 46 080 B", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_crop_audio", "label": "Rogner & Normaliser EBU R128 (-23 LUFS)", "role": "primary", "state": "idle", "icon": "🎙️"},
                {"id": "btn_play_preview", "label": "▶ Écouter Extrait 30s", "role": "secondary", "state": "idle", "icon": "🔊"}
            ],
            "validationMsg": {
                "title": "Audio Vocal Mémoriel Validé",
                "badge": "Durée 30.0s • -23 LUFS",
                "detail": "Filtre anti-souffle appliqué. Normalisation broadcast EBU R128 effectuée."
            },
            "errorCase": {
                "code": "ERR_AUDIO_DURATION_OVERFLOW",
                "title": "Dépassement de la Durée Vocale Maximale",
                "condition": "Sélection d'un extrait de plus de 45 secondes excédant le budget mémoire alloué.",
                "message": "Erreur audio : La durée sélectionnée dépasse la limite stricte de 30 secondes pour le stockage silicium.",
                "remediation": "Resserrer les curseurs temporels de début et de fin pour respecter la fenêtre de 30 secondes."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Oscilloscope Brut Non Découpé",
                    "caption": "Forme d'onde brute affichée sur toute la longueur (1m30s). Curseur en attente de déplacement.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Oscilloscope Audio Brut</span>
                        <span class="wf-status-badge wf-badge-neutral">Durée Brute : 01:30.000</span>
                      </div>
                      <div class="wf-waveform-canvas">
                        <div class="wf-wave-bars"> ▂▃▅▆▇▆▅▃▂ ▂▃▅▆▇▆▅▃▂ ▂▃▅▆▇▆▅▃▂ ▂▃▅▆▇▆▅▃▂ </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">🎙️ Rogner & Normaliser EBU R128 (-23 LUFS)</button>
                      </div>
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Déplacement des Curseurs Temporels avec Marge Anti-Retour",
                    "triggerName": "Glissement tactile des balises de début (00:05) et fin (00:35)",
                    "caption": "Zone tactile sécurisée isolée des bords d'écran pour bloquer le geste de retour Android.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Recadrage Audio Tactile</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Glissement Curseur Temporel</span>
                      </div>
                      <div class="wf-waveform-canvas wf-radar-pulse">
                        <div class="wf-crop-marker wf-marker-start">Balise Début: 00:05.200</div>
                        <div class="wf-crop-window">Fenêtre Vocale 30.0 s (Isolée anti-gestes)</div>
                        <div class="wf-crop-marker wf-marker-end">Balise Fin: 00:35.200</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Traitement WebAudio en cours...</button>
                      </div>
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Traitement WebAudio & Normalisation EBU R128",
                    "progress": 78,
                    "caption": "Filtrage passe-haut anti-souffle et calcul du loudness intégré à -23 LUFS.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Processeur WebAudio</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Normalisation (-23 LUFS)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 78%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [WEBAUDIO] Filtre passe-haut 120 Hz anti-pop : Actif</code><br>
                        <code>> [WEBAUDIO] Normalisation dynamique EBU R128 : -23.0 LUFS atteint</code><br>
                        <code>> [ENCODER] Encodage Ogg Opus mono 16 kbps : 58.2 Ko alloués</code>
                      </div>
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Extrait Vocal Mémoriel 30s Prêt",
                    "status": "success",
                    "caption": "Forme d'onde finalisée avec bouton d'écoute instantanée sans latence.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Voix Mémorielle Scellée</span>
                        <span class="wf-status-badge wf-badge-success">✨ Extrait 30s Prêt (-23 LUFS)</span>
                      </div>
                      <div class="wf-player-card">
                        <button class="wf-play-circle">▶</button>
                        <div>
                          <strong>« Message d'Adieu pour mes Proches »</strong>
                          <p class="wf-subtext">00:30.000 • Ogg Opus 16 kbps • Prêt pour ducking vocal</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Musiques d'Adieu →</button>
                      </div>
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-106",
        "title": "Choix & Intégration des Musiques d'Adieu & Recueillement",
        "cat": "Médias Sonores",
        "actor": "Famille & Conseiller",
        "platforms": ["Web Standard (PWA Hors-Ligne)", "Natif (iOS & Android)"],
        "tags": ["Musique", "Recueillement", "Ambiance", "Fauré", "Satie"],
        "preconditions": "Bibliothèque musicale funéraire hors-ligne chargée dans l'application.",
        "flow": [
            "Consultation du répertoire musical solennel embarqué (In Paradisum de Gabriel Fauré, Gymnopédie de Satie, silence sacré).",
            "Écoute d'un extrait de 15 secondes pour validation par la famille.",
            "Paramétrage du point de bouclage harmonique et de la transition douce en fondu enchaîné (crossfade 3s).",
            "Association de la musique à la Carte Sanctuaire pour déclenchement automatique lors du scan NFC."
        ],
        "postconditions": "Piste musicale d'ambiance sélectionnée et configurée avec atténuation automatique (ducking).",
        "legal": "Code de la propriété intellectuelle (œuvres tombées dans le domaine public / licences acquises) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "tablet",
            "deviceLabel": "PaxStudio Pro • Ambiance Musicale & Recueillement",
            "formFields": [
                {"label": "Piste Sélectionnée", "name": "music_track", "type": "select", "value": "Gabriel Fauré — In Paradisum (Requiem Op. 48)", "placeholder": "Choisir une musique", "badge": "Domaine Public", "required": True},
                {"label": "Volume Nominal", "name": "music_volume", "type": "range", "value": "80% (Volume solennel)", "placeholder": "Niveau sonore", "badge": "Ambiance", "required": False},
                {"label": "Atténuation Ducking Vocal", "name": "ducking_level", "type": "text", "value": "-14 dB automatique lors de la voix", "placeholder": "Ducking", "badge": "Actif", "required": False},
                {"label": "Fondu Enchaîné (Crossfade)", "name": "crossfade_duration", "type": "text", "value": "3.0 s (Bouclage harmonique sans coupure)", "placeholder": "Transition", "badge": "Crossfade", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_select_music", "label": "Intégrer la Piste d'Ambiance", "role": "primary", "state": "idle", "icon": "🎵"},
                {"id": "btn_test_fade", "label": "Tester Fondu Enchaîné (3s)", "role": "secondary", "state": "idle", "icon": "🎧"}
            ],
            "validationMsg": {
                "title": "Piste Musicale Associée",
                "badge": "Ducking -14 dB Prêt",
                "detail": "In Paradisum configuré avec fondu enchaîné de 3s et ducking vocal automatique."
            },
            "errorCase": {
                "code": "ERR_AUDIO_FORMAT_UNSUPPORTED",
                "title": "Format Audio Non Conforme",
                "condition": "Fichier musical corrompu ou codec propriétaire non supporté hors-ligne.",
                "message": "Erreur sonore : Le fichier sélectionné ne respecte pas le format Ogg Opus ou WAV pur.",
                "remediation": "Sélectionner une des pistes de la bibliothèque sacrée embarquée ou convertir le fichier en WAV 44.1 kHz."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Répertoire Musical Sacré en Attente",
                    "caption": "Bibliothèque de morceaux funéraires hors-ligne affichée. Piste non encore confirmée.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Bibliothèque Musicale Sacrée</span>
                        <span class="wf-status-badge wf-badge-neutral">Sélection en Attente</span>
                      </div>
                      <div class="wf-track-list">
                        <div class="wf-track-item">🎵 Gabriel Fauré — In Paradisum (Requiem)</div>
                        <div class="wf-track-item">🎵 Erik Satie — Gymnopédie N°1</div>
                        <div class="wf-track-item">🎵 Silence Solennel & Sons de la Forêt</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">Intégrer la Piste d'Ambiance</button>
                      </div>
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Sélection de 'In Paradisum' de Gabriel Fauré",
                    "triggerName": "Clic sur la piste 'In Paradisum' et validation du volume",
                    "caption": "Surbrillance dorée de la piste sélectionnée avec prévisualisation sonore instantanée.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Piste Choise</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Sélection Active</span>
                      </div>
                      <div class="wf-track-selected wf-radar-pulse">
                        <strong>✓ Gabriel Fauré — In Paradisum (Requiem Op. 48)</strong>
                        <p class="wf-subtext">Bouclage harmonique calibré • Crossfade 3 secondes</p>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Enregistrement des Paramètres...</button>
                      </div>
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Calibration du Profil de Ducking Vocal",
                    "progress": 82,
                    "caption": "Configuration du compresseur WebAudio pour atténuer la musique à -14 dB lors du témoignage vocal.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Moteur de Ducking WebAudio</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Calibration Audio (82%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 82%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [DUCKING-DSP] Analyse du niveau RMS de la piste d'ambiance : -18 dBFS</code><br>
                        <code>> [DUCKING-DSP] Enveloppe d'atténuation : Attaque 400ms, Relâchement 1200ms</code><br>
                        <code>> [DUCKING-DSP] Seuil de déclenchement vocal synchronisé : OK</code>
                      </div>
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Ambiance Musicale Associée au Sanctuaire",
                    "status": "success",
                    "caption": "Piste validée avec succès. Elle se lancera automatiquement lors de l'apposition de la carte.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Audio Sanctuaire Prêt</span>
                        <span class="wf-status-badge wf-badge-success">✨ Profil Musical Scellé</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🎼</span>
                        <div>
                          <strong>In Paradisum (Fauré) Associé à la Carte Sanctuaire</strong>
                          <p class="wf-subtext">Ducking vocal actif (-14 dB) • Durée de recueillement infinie par bouclage</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Volontés Civiles →</button>
                      </div>
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-107",
        "title": "Saisie Guidée des Dernières Volontés Civiles & Funéraires",
        "cat": "Dernières Volontés",
        "actor": "Famille & Conseiller",
        "platforms": ["Web Standard (PWA Hors-Ligne)", "Natif (iOS & Android)"],
        "tags": ["Volontes", "Loi1971", "Ceremonie", "Sepulture"],
        "preconditions": "Famille en salon de recueillement avec le conseiller funéraire agréé.",
        "flow": [
            "Questionnaire structuré conforme à la loi belge du 20 juillet 1971 (cérémonie civile laïque ou culte religieux) (référence à confirmer par un juriste).",
            "Choix du mode de sépulture : inhumation traditionnelle, crémation cinéraire ou sarcomusation avec retour en forêt (Démonstrateur de faisabilité prospectif — Option non autorisée par le droit positif actuel (référence à confirmer par un juriste)).",
            "Désignation de la destination finale des cendres ou résidus mémoriels (arbre cinéraire privé agréé sous dérogation DEC-AET-05).",
            "Rédaction des souhaits spécifiques (fleurs, dons à une association, dispersion solennelle)."
        ],
        "postconditions": "Fiche de dernières volontés civiques encodée, horodatée et prête pour le scellement cryptographique.",
        "legal": "Loi du 20 juillet 1971 sur les funérailles et sépultures (primauté de la volonté du défunt) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "tablet",
            "deviceLabel": "PaxStudio Pro • Fiche des Volontés Civiles & Funéraires",
            "formFields": [
                {"label": "Nature de Cérémonie", "name": "ceremony_type", "type": "select", "value": "Cérémonie Civile Laïque sous les Arbres", "placeholder": "Cérémonie", "badge": "Loi 1971 (référence à confirmer par un juriste)", "required": True},
                {"label": "Mode de Sépulture", "name": "burial_mode", "type": "select", "value": "Sarcomusation & Amendement Forestier (Démonstrateur de faisabilité prospectif — Option non autorisée par le droit positif actuel (référence à confirmer par un juriste))", "placeholder": "Sépulture", "badge": "Démonstrateur Prospectif", "required": True},
                {"label": "Destination des Résidus", "name": "residue_dest", "type": "select", "value": "Arbre Cinéraire Mémoriel (Forêt Saint-Hubert)", "placeholder": "Destination", "badge": "DEC-AET-05", "required": True},
                {"label": "Message d'Adieu Public", "name": "public_message", "type": "textarea", "value": "« Que la nature accueille ma mémoire en paix auprès des grands chênes. »", "placeholder": "Message", "badge": "Facultatif", "required": False},
                {"label": "Ambiance Musicale Choisie", "name": "funeral_music", "type": "select", "value": "Gabriel Fauré — In Paradisum (Requiem Op. 48)", "placeholder": "Musique", "badge": "Ambiance", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_seal_wills", "label": "Sceller les Volontés Civiles in-silico", "role": "primary", "state": "idle", "icon": "📜"},
                {"id": "btn_preview_wills", "label": "Prévisualiser l'Acte Formel", "role": "secondary", "state": "idle", "icon": "👁"}
            ],
            "validationMsg": {
                "title": "Volontés Civiles Encodées",
                "badge": "Conforme Loi 20 juillet 1971 (référence à confirmer par un juriste)",
                "detail": "Primauté des volontés garantie. Sarcomusation (Démonstrateur de faisabilité prospectif — Option non autorisée par le droit positif actuel (référence à confirmer par un juriste)) et arbre cinéraire enregistrés."
            },
            "errorCase": {
                "code": "ERR_WILLS_SYNTAX_INVALID",
                "title": "Clauses Incompatibles avec la Législation",
                "condition": "Stipulation d'une clause contraire à l'ordre public ou refus de signature des ayants droit.",
                "message": "Erreur de conformité : La disposition funéraire renseignée contrevient au cadre légal des sépultures.",
                "remediation": "Reformuler les clauses pour s'aligner sur les options autorisées par la loi du 20 juillet 1971 (référence à confirmer par un juriste)."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Formulaire des Volontés Vierge",
                    "caption": "Questionnaire funéraire en attente d'arbitrage par la famille.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Volontés Civiles</span>
                        <span class="wf-status-badge wf-badge-neutral">Formulaire en Attente</span>
                      </div>
                      <div class="wf-field-group">
                        <label class="wf-label">Cérémonie Souhaitée <span class="wf-req">*</span></label>
                        <div class="wf-select-placeholder">-- Sélectionner : Civile, Religieuse, Hommage intime --</div>
                      </div>
                      <div class="wf-field-group">
                        <label class="wf-label">Destination Mémorielle <span class="wf-req">*</span></label>
                        <div class="wf-select-placeholder">-- Sarcomusation & Forêt cinéraire (Démonstrateur de faisabilité prospectif — Option non autorisée par le droit positif actuel (référence à confirmer par un juriste)) --</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">📜 Sceller les Volontés Civiles in-silico</button>
                      </div>
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Validation des Choix Funéraires & Signature Famille",
                    "triggerName": "Clic sur 'Sceller les Volontés Civiles in-silico'",
                    "caption": "Champs renseignés avec arbitrage formel : Sarcomusation mémorielle et arbre du souvenir.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Volontés Arrêtées</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Scellement enclenché</span>
                      </div>
                      <div class="wf-wills-summary wf-radar-pulse">
                        <div><strong>Cérémonie :</strong> Laïque solennelle</div>
                        <div><strong>Sépulture :</strong> Sarcomusation & Retour forestier (DEC-AET-05) <span class="wf-badge-warning">[Démonstrateur de faisabilité prospectif — Option non autorisée par le droit positif actuel (référence à confirmer par un juriste)]</span></div>
                        <div><strong>Arbre du Souvenir :</strong> Chêne n° F-2408 (Saint-Hubert)</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Scellement CBOR en cours...</button>
                      </div>
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Sérialisation Canonique & Chiffrement Préparatoire",
                    "progress": 75,
                    "caption": "Encodage des volontés sous format CBOR canonique déterministe (RFC 8949).",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Sérialisation CBOR</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Encodage Légal (75%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 75%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [CORE-CBOR] Sérialisation clé 1 (cérémonie) et clé 2 (destination) : OK</code><br>
                        <code>> [CORE-CBOR] Vérification conformité Loi 20 juillet 1971 (référence à confirmer par un juriste) : SUCCÈS</code><br>
                        <code>> [CORE-CBOR] Calcul du condensat SHA-256 des volontés : 8e4b...910a</code>
                      </div>
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Acte des Volontés Scellé pour la Carte Directives",
                    "status": "success",
                    "caption": "Volontés immuables gravées dans la structure de données de la Carte 2 Directives.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Volontés Scellées</span>
                        <span class="wf-status-badge wf-badge-success">✨ Conforme Loi 1971 (référence à confirmer par un juriste)</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">⚖️</span>
                        <div>
                          <strong>Volontés Funéraires Gravées in-silico</strong>
                          <p class="wf-subtext">Inaltérables • Primauté légale garantie • Carte 2 Directives prête</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Directives Médicales →</button>
                      </div>
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-108",
        "title": "Directives Médicales Post-Mortem (Pacemaker, Dons, Legs)",
        "cat": "Directives Médicales",
        "actor": "Famille & Conseiller",
        "platforms": ["Web Standard (PWA Hors-Ligne)", "Natif (iOS & Android)"],
        "tags": ["Pacemaker", "DonOrganes", "LegsCorps", "SecuriteOperateurs"],
        "preconditions": "Accès au volet de sécurité médicale post-mortem dans PaxStudio.",
        "flow": [
            "Contrôle obligatoire d'alerte sur la présence d'un stimulateur cardiaque (pacemaker) ou défibrillateur implantable (Art. L1232-24 CDLD & Modèle IIIC réglementaire).",
            "Si stimulateur présent : blocage strict imposant le renseignement de l'attestation chirurgicale d'exérèse avec numéro d'ordre du médecin.",
            "Recueil de la position sur le don d'organes (rappel de la loi belge du consentement présumé de 1986).",
            "Enregistrement éventuel d'un protocole de legs du corps à la science sous 48h auprès d'une université conventionnée."
        ],
        "postconditions": "Volet médical post-mortem validé, alerte pacemaker levée uniquement sur certificat médical officiel.",
        "legal": "Art. L1232-24 CDLD & Modèle IIIC réglementaire (exérèse obligatoire des stimulateurs cardiaques).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "tablet",
            "deviceLabel": "PaxStudio Pro • Volet Médical d'Urgence & Sécurité",
            "formFields": [
                {"label": "Porteur de Stimulateur Cardiaque (Pacemaker)", "name": "has_pacemaker", "type": "select", "value": "OUI (Présence confirmée)", "placeholder": "Sélectionner", "badge": "ALERTE VITALE", "required": True},
                {"label": "Attestation d'Exérèse Chirurgicale", "name": "pacemaker_cert", "type": "file", "value": "certificat_exerese_dr_vaneck.pdf", "placeholder": "Téléverser attestation", "badge": "Obligatoire si Oui", "required": True},
                {"label": "Médecin Certificateur & N° Ordre", "name": "pacemaker_doc", "type": "text", "value": "Dr. Marc Vaneck — INAMI 1-40912-88-004", "placeholder": "Nom et INAMI", "badge": "Vérifié", "required": True},
                {"label": "Don d'Organes (Loi 1986)", "name": "organ_donation", "type": "select", "value": "Consentement Plein et Entier Confirmé", "placeholder": "Statut don", "badge": "Loi 1986", "required": True}
            ],
            "actionButtons": [
                {"id": "btn_validate_medical", "label": "Valider le Volet Médical d'Urgence", "role": "primary", "state": "idle", "icon": "🩺"},
                {"id": "btn_verify_inami", "label": "Vérifier Validité Ordre Médecin", "role": "secondary", "state": "idle", "icon": "🔍"}
            ],
            "validationMsg": {
                "title": "Volet Médical d'Urgence Certifié",
                "badge": "Conforme Art. L1232-24 CDLD & Modèle IIIC réglementaire",
                "detail": "Exérèse chirurgicale du pacemaker certifiée par le Dr. Vaneck. Zéro risque d'explosion."
            },
            "errorCase": {
                "code": "ERR_PACEMAKER_UNVERIFIED",
                "title": "Alerte Vitale : Stimulateur Cardiaque Non Retiré",
                "condition": "Déclaration d'un pacemaker sans téléversement d'attestation médicale d'exérèse chirurgicale.",
                "message": "BLOCAGE DE SÉCURITÉ INVIOLABLE : Présence d'un pacemaker non retiré. Risque d'explosion thermique mortelle en crémation ou bioconversion.",
                "remediation": "Fournir immédiatement l'attestation officielle d'exérèse signée par un médecin avec son numéro INAMI pour déverrouiller l'encodage."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Alerte Pacemaker en Attente de Certification",
                    "caption": "Pacemaker déclaré présent. Le système bloque tout encodage tant que l'attestation n'est pas fournie.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Alerte de Sécurité Médicale</span>
                        <span class="wf-status-badge wf-badge-alert">⚠️ Stimulateur Déclaré</span>
                      </div>
                      <div class="wf-alert-card wf-alert-red">
                        <strong>ATTENTION OBLIGATOIRE : Présence d'un Pacemaker</strong>
                        <p class="wf-subtext">L'article L1232-24 CDLD & Modèle IIIC réglementaire imposent l'exérèse chirurgicale avant toute opération.</p>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-disabled" disabled>🩺 Valider le Volet Médical (Bloqué)</button>
                      </div>
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Import de l'Attestation Médicale d'Exérèse Chirurgicale",
                    "triggerName": "Téléversement du certificat de retrait signé par le Dr. Marc Vaneck",
                    "caption": "Saisie de l'identifiant INAMI du praticien et levée de l'alerte bloquante.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Attestation Médicale Reçue</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Certificat Médical Déposé</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">✓ Attestation d'exérèse reçue : Dr. Marc Vaneck (INAMI: 1-40912-88-004)</div>
                        <div class="wf-subtext">Dispositif médical retiré avec succès le 04/10/2026 à 09h15</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Valider la Conformité Médicale...</button>
                      </div>
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Vérification Algorithmique & Levée du Verrou Légal",
                    "progress": 95,
                    "caption": "Validation de la structure de l'INAMI et encodage du certificat de sécurité médicale.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Contrôle Sécurité Exérèse (Art. L1232-24 CDLD & Modèle IIIC)</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Vérification Légale (95%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 95%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [LEGAL-CHECK] Format numéro INAMI médecin : Valide</code><br>
                        <code>> [LEGAL-CHECK] Règle Art. L1232-24 CDLD & Modèle IIIC réglementaire satisfaite : Exérèse certifiée</code><br>
                        <code>> [LEGAL-CHECK] Levée formelle du verrou de pré-encodage : AUTORISÉ</code>
                      </div>
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Sceau de Sécurité Médicale Déposé",
                    "status": "success",
                    "caption": "Alerte rouge effacée, remplacée par le sceau vert de conformité chirurgicale.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Sécurité Médicale Validée</span>
                        <span class="wf-status-badge wf-badge-success">✨ Exérèse Certifiée Conforme</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🛡️</span>
                        <div>
                          <strong>Sécurité des Opérateurs Funéraires Garantie</strong>
                          <p class="wf-subtext">Visa médical Dr. Vaneck scellé in-silico • Prêt pour compilation CBOR</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Compilation CBOR Déterministe →</button>
                      </div>
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-109",
        "title": "Génération & Validation de la Capsule de Pré-Encodage CBOR",
        "cat": "Compilation & Core",
        "actor": "Conseiller & Système Core",
        "platforms": ["Web Standard (PWA Hors-Ligne)", "Node.js / Core Engine"],
        "tags": ["AeterniCore", "CBOR", "RFC8949", "Determinisme"],
        "preconditions": "Médias, volontés, charte graphique et directives médicales entièrement complétés.",
        "flow": [
            "Agrégation de l'ensemble des données des 2 cartes par le moteur AeterniCore.",
            "Application des règles de déterminisme strictes de la RFC 8949 (tri lexicographique des clés entières, entiers canoniques les plus courts).",
            "Calcul de l'empreinte cryptographique SHA-256 canonique JCS de la capsule globale.",
            "Vérification que la taille totale compilée ne dépasse pas 80 Ko, laissant une marge de sécurité sur les 92 Ko de l'ACOSJ."
        ],
        "postconditions": "Fichier binaire capsule `.cbor` généré, scellé et prêt pour l'envoi vers PaxStation.",
        "legal": "Spécification technique IETF RFC 8949 (déterminisme binaire CBOR).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "tablet",
            "deviceLabel": "PaxStudio Pro • Compilateur AeterniCore RFC 8949",
            "formFields": [
                {"label": "Moteur CBOR", "name": "cbor_engine", "type": "text", "value": "AeterniCore Deterministic v1.4.2", "placeholder": "Moteur", "badge": "RFC 8949", "required": False},
                {"label": "Tri Canonique des Clés", "name": "cbor_sorting", "type": "checkbox", "value": "Actif (Bytewise-lexicographique)", "placeholder": "Tri", "badge": "Obligatoire", "required": True},
                {"label": "Taille Finale Compilée", "name": "cbor_size", "type": "text", "value": "78 412 octets (< 80 Ko recommandés / 92 Ko EEPROM)", "placeholder": "Taille", "badge": "Conforme", "required": False},
                {"label": "Condensat SHA-256 Canonique", "name": "sha256_hash", "type": "text", "value": "a4f81c90...b1297e41 (64 hex)", "placeholder": "Empreinte", "badge": "Scellé", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_compile_cbor", "label": "Générer la Capsule CBOR Déterministe", "role": "primary", "state": "idle", "icon": "⚡"},
                {"id": "btn_audit_cbor", "label": "Auditer Syntaxe Binaire RFC 8949", "role": "secondary", "state": "idle", "icon": "🔍"}
            ],
            "validationMsg": {
                "title": "Capsule CBOR Compilée avec Succès",
                "badge": "100% Déterministe RFC 8949",
                "detail": "78 412 octets sérialisés. Zéro octet superflu. Empreinte SHA-256 générée."
            },
            "errorCase": {
                "code": "ERR_CBOR_NON_DETERMINISTIC",
                "title": "Non-Déterminisme Binaire CBOR",
                "condition": "Clés de dictionnaires non ordonnées ou entiers encodés sur un format non minimal.",
                "message": "Erreur critique de compilation : La capsule CBOR produite viole les règles canoniques de la RFC 8949 §4.2.1.",
                "remediation": "Réexécuter la canonisation AeterniCore en forçant le tri lexicographique des clés entières."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Données Rassemblées en Attente de Compilation",
                    "caption": "Toutes les sections sont prêtes. L'agrégat binaire n'est pas encore compilé.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Agrégateur AeterniCore</span>
                        <span class="wf-status-badge wf-badge-neutral">Prêt pour Compilation</span>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-mini-stat">📸 Portraits : 37.2 Ko</div>
                        <div class="wf-mini-stat">🎙️ Audio Vocal : 58.2 Ko</div>
                        <div class="wf-mini-stat">📜 Volontés : 2.1 Ko</div>
                        <div class="wf-mini-stat">🩺 Médical : 1.4 Ko</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">⚡ Générer la Capsule CBOR Déterministe</button>
                      </div>
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Clic sur 'Générer la Capsule CBOR Déterministe'",
                    "triggerName": "Lancement du pipeline de sérialisation binaire déterministe",
                    "caption": "Ordonnancement binaire des clés entières et calcul de l'arbre binaire.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Sérialisation en Cours</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Pipeline AeterniCore Actif</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">⚡ Tri Bytewise-Lexicographique des Cartes CBOR</div>
                        <div class="wf-subtext">Conversion des textes UTF-8 et injection des flux WebP/Opus</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Compilation Binaire en cours...</button>
                      </div>
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Génération du Hash SHA-256 Canonique JCS",
                    "progress": 88,
                    "caption": "Calcul de l'empreinte cryptographique de la capsule (RFC 8785 / RFC 8949).",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Calculateur Cryptographique</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Hachage SHA-256 (88%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 88%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [CBOR-SERIAL] 78 412 octets générés au format compact déterministe</code><br>
                        <code>> [JCS-HASH] Calcul SHA-256 sur sig_structure préparatoire...</code><br>
                        <code>> [JCS-HASH] Digest : a4f81c9053d867c29019b7842ef84a12...b129 : OK</code>
                      </div>
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Capsule Binaire `.cbor` Scellée avec Succès",
                    "status": "success",
                    "caption": "Fichier de pré-encodage scellé prêt pour transfert sécurisé vers PaxStation.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Capsule Prête</span>
                        <span class="wf-status-badge wf-badge-success">✨ Capsule 78 412 o Scellée</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">📦</span>
                        <div>
                          <strong>Capsule CBOR Déterministe Prête pour PaxStation</strong>
                          <p class="wf-subtext">SHA-256 : a4f8...b129 • Conforme RFC 8949 • 0 octet superflu</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Bon à Tirer (BAT) →</button>
                      </div>
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-110",
        "title": "Bon à Tirer (BAT) Numérique & Validation Familiale",
        "cat": "Validation Finale",
        "actor": "Famille & Conseiller Funéraire",
        "platforms": ["Web Standard (PWA Hors-Ligne)", "Natif (iOS & Android)"],
        "tags": ["BAT", "Emargement", "Signature", "Contrat"],
        "preconditions": "Capsule CBOR générée et visuels recto/verso des 2 cartes approuvés.",
        "flow": [
            "Affichage de la synthèse solennelle du Bon à Tirer (BAT) numérique récapitulant les médias, les textes, les directives médicales et l'empreinte de la capsule.",
            "Signature manuscrite sur écran tactile par le mandataire de la famille et le conseiller funéraire.",
            "Horodatage local certifié et scellement non répudiable du document contractuel BAT.",
            "Transmission sécurisée de l'ordre d'encodage et de gravure à l'application PaxStation de l'atelier."
        ],
        "postconditions": "Ordre d'encodage officiel émis, BAT PDF/CBOR archivé localement avec double émargement.",
        "legal": "Code civil belge (art. 1322 - valeur probante de la signature électronique) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "tablet",
            "deviceLabel": "PaxStudio Pro • Bon à Tirer (BAT) Numérique Officiel",
            "formFields": [
                {"label": "Mandataire Familial", "name": "family_signatory", "type": "text", "value": "Claire Dubois (Épouse et Mandataire désignée)", "placeholder": "Nom mandataire", "badge": "Ayant Droit", "required": True},
                {"label": "Conseiller Funéraire Agréé", "name": "pro_signatory", "type": "text", "value": "Jean-Luc Lambert (Le Pax Funèbre Namur)", "placeholder": "Nom conseiller", "badge": "Opérateur", "required": True},
                {"label": "Émargement Tactile Requis", "name": "sig_status", "type": "checkbox", "value": "Double émargement numérique apposé", "placeholder": "Signature", "badge": "Légal", "required": True},
                {"label": "Horodatage Certifié", "name": "timestamp_utc", "type": "text", "value": "2026-10-04T15:30:00Z (Horodatage local non répudiable)", "placeholder": "Horodatage", "badge": "Certifié", "required": False}
            ],
            "actionButtons": [
                {"id": "btn_sign_bat", "label": "Signer le BAT Numérique & Transmettre à PaxStation", "role": "primary", "state": "idle", "icon": "✍️"},
                {"id": "btn_print_bat", "label": "Imprimer Copie Papier Famille", "role": "secondary", "state": "idle", "icon": "🖨️"}
            ],
            "validationMsg": {
                "title": "Bon à Tirer Définitivement Validé",
                "badge": "Conforme Art. 1322 Code Civil (référence à confirmer par un juriste)",
                "detail": "Double signature enregistrée. Ordre d'encodage transmis à PaxStation pour gravure physique."
            },
            "errorCase": {
                "code": "ERR_BAT_UNAUTHORIZED_SIGNATURE",
                "title": "Défaut d'Habilitation du Signataire",
                "condition": "Absence de lien d'ayant droit ou mandat post-mortem contesté.",
                "message": "Erreur juridique : Le signataire n'a pas produit de mandat d'ayant droit valide pour engager la commande funéraire.",
                "remediation": "Vérifier le mandat post-mortem ou solliciter la signature conjointe des héritiers réservataires."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Synthèse du Bon à Tirer en Attente de Signature",
                    "caption": "Document officiel affiché. Les deux zones de signature manuscrite sont vides.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Bon à Tirer (BAT) Numérique</span>
                        <span class="wf-status-badge wf-badge-neutral">En Attente des Signatures</span>
                      </div>
                      <div class="wf-bat-summary">
                        <div><strong>Commande :</strong> Lot Duo Le Pax Funèbre (Sanctuaire + Directives)</div>
                        <div><strong>Défunt :</strong> Henri Dubois • Empreinte CBOR : a4f8...b129</div>
                        <div><strong>Sécurité :</strong> Pacemaker retiré (Dr. Vaneck) • Sarcomusation (Démonstrateur de faisabilité prospectif — Option non autorisée par le droit positif actuel (référence à confirmer par un juriste)) validée</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">✍️ Signer le BAT Numérique & Transmettre</button>
                      </div>
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Émargement Tactile Conjoint Famille & Conseiller",
                    "triggerName": "Apposition des deux signatures manuscrites au stylet sur tablette",
                    "caption": "Tracé vectoriel des deux signatures avec surbrillance dorée instantanée.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Émargement Électronique</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Double Signature Apposée</span>
                      </div>
                      <div class="wf-signature-boxes wf-radar-pulse">
                        <div class="wf-sig-box">✒️ Signature Famille (Claire Dubois) : Apposée ✓</div>
                        <div class="wf-sig-box">✒️ Signature Conseiller (J-L Lambert) : Apposée ✓</div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Scellement Légal du Contrat...</button>
                      </div>
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Scellement Légal & Transmission vers PaxStation",
                    "progress": 92,
                    "caption": "Horodatage cryptographique non répudiable et émission du bon de production.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Transmission Atelier PaxStation</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Envoi Sécurisé (92%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 92%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [BAT-LEGAL] Horodatage certifié : 2026-10-04T15:30:00Z</code><br>
                        <code>> [BAT-LEGAL] Verrouillage contractuel non répudiable (Art. 1322 C. civ. — référence à confirmer par un juriste) : OK</code><br>
                        <code>> [NETWORK-LOCAL] Ordre d'encodage n° ORD-2026-0491 transmis à PaxStation</code>
                      </div>
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "BAT Verrouillé & Ordre d'Encodage Transmis",
                    "status": "success",
                    "caption": "Validation finale de PaxStudio terminée avec succès. La session bascule vers PaxStation.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Processus Terminé</span>
                        <span class="wf-status-badge wf-badge-success">✨ BAT Scellé & Transmis</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🤝</span>
                        <div>
                          <strong>Commande Validée par la Famille</strong>
                          <p class="wf-subtext">Ordre transmis à PaxStation pour gravure sur silicium ACOSJ 92k</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Bascule vers App 2 : PaxStation Encodage →</button>
                      </div>
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-111",
        "title": "Création de la Carte & Saisie Intégrale de l'Identité Civile et Mémorielle",
        "cat": "Identité Civile & Mémorielle",
        "actor": "Famille & Conseiller Funéraire",
        "platforms": ["Web Standard (PWA Hors-Ligne)", "Natif (iOS & Android)"],
        "tags": ["Identité", "ÉtatCivil", "Tag100", "CBOR", "validator.ts", "NCBI", "AeterniCore"],
        "preconditions": "Ouverture d'un nouveau projet de carte ou médaillon dans PaxStudio Pro. Choix initial du profil : être humain (subject_kind = 1) ou animal de compagnie (subject_kind = 2).",
        "flow": [
            "Sélection de la typologie du sujet mémoriel : Être humain (subject_kind = 1) ou Animal de compagnie (subject_kind = 2).",
            "Saisie obligatoire du prénom usuel (usage_name, 1 à 120 octets UTF-8, ex: « Guy » ou « Marie ») et facultative du nom patronymique / de naissance (birth_name, 1 à 120 octets, ex: « Heyman »).",
            "Saisie ordonnée des prénoms officiels secondaires dans le tableau dédié (given_names, jusqu'à 8 prénoms maximum de 1 à 80 octets chacun).",
            "Sélection calendaire de la date de naissance (birth_date, Tag 100 RFC 8949, obligatoire pour un sujet humain) et de la date de décès (death_date, Tag 100).",
            "Renseignement du code pays de rattachement au format ISO 3166-1 alpha-2 en majuscules (ex: « BE » pour la Belgique, « FR » pour la France).",
            "Attribution du code de rite cérémoniel (rite_code : entier >= 0, cérémonie civile laïque ou confessionnelle).",
            "Conditionnement taxonomique : si animal de compagnie, sélection du taxon NCBI officiel (species_taxid : Chien 9615, Chat 9685, Cheval 9796... — strictement rejeté par validator.ts si sujet humain).",
            "Rédaction de l'épitaphe et du texte d'hommage solennel avec jauge télémétrique live (1 à 1 600 octets UTF-8 maximum).",
            "Audit syntaxique déterministe immédiat via validator.ts : vérification stricte des types CBOR, contrôle des bornes de taille d'octets et validation du schéma AeterniCore v1."
        ],
        "postconditions": "Profil mémoriel sérialisé et certifié conforme par validator.ts, structure de données CBOR normalisée prête pour l'injection des portraits 480×480 (DEC-AET-12), du mémo vocal et des dernières volontés.",
        "legal": "Code civil (actes de l'état civil, art. 34 et suivants) et Règlement eIDAS (identification électronique sécurisée) (références à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "tablet",
            "deviceLabel": "PaxStudio Pro • Fiche d'Identité Civile & Mémorielle",
            "formFields": [
                {"label": "Nature du Sujet (subject_kind)", "name": "subject_kind", "type": "select", "value": "1 — Être Humain (Sujet de droit)", "placeholder": "Sélectionner le profil", "badge": "Requis (1 | 2)", "required": True},
                {"label": "Prénom Usuel (usage_name)", "name": "usage_name", "type": "text", "value": "Guy", "placeholder": "Ex: Guy, Marie", "badge": "Requis (1..120 B)", "required": True},
                {"label": "Nom Patronyme / Naissance (birth_name)", "name": "birth_name", "type": "text", "value": "Heyman", "placeholder": "Ex: Heyman", "badge": "Optionnel (1..120 B)", "required": False},
                {"label": "Prénoms Secondaires (given_names)", "name": "given_names", "type": "text", "value": "Jean, Robert, Émile (3/8 enregistrés)", "placeholder": "Prénoms séparés par virgule (max 8)", "badge": "Tableau Max 8", "required": False},
                {"label": "Date de Naissance (birth_date)", "name": "birth_date", "type": "date", "value": "1942-06-14 (Tag 100 RFC 8949)", "placeholder": "AAAA-MM-JJ", "badge": "Tag 100 Requis Humain", "required": True},
                {"label": "Date de Décès (death_date)", "name": "death_date", "type": "date", "value": "2026-10-02 (Tag 100 RFC 8949)", "placeholder": "AAAA-MM-JJ", "badge": "Tag 100 Optionnel", "required": False},
                {"label": "Code Pays (country)", "name": "country", "type": "text", "value": "BE (Belgique)", "placeholder": "Code ISO 3166-1 alpha-2 (2 majuscules)", "badge": "ISO 3166-1 α2", "required": True},
                {"label": "Rite Cérémoniel (rite_code)", "name": "rite_code", "type": "select", "value": "0 — Cérémonie Civile & Laïque sous les Arbres", "placeholder": "Code rite", "badge": "Entier >= 0", "required": True},
                {"label": "Taxon NCBI Animal (species_taxid)", "name": "species_taxid", "type": "select", "value": "N/A (Verrouillé : Sujet Humain)", "placeholder": "Taxon NCBI si animal", "badge": "Animal Uniquement", "required": False},
                {"label": "Épitaphe & Hommage (epitaph)", "name": "epitaph", "type": "textarea", "value": "« Dans le souffle du vent et la lumière des sous-bois, ta bienveillance demeure éternelle. » (142 / 1 600 octets)", "placeholder": "Épitaphe solennelle (1..1600 octets UTF-8)", "badge": "1..1600 Octets", "required": True}
            ],
            "actionButtons": [
                {"id": "btn_validate_identity", "label": "Valider l'Identité Mémorielle (validator.ts)", "role": "primary", "state": "idle", "icon": "👤"},
                {"id": "btn_toggle_species", "label": "Basculer Profil Animal (Taxon NCBI)", "role": "secondary", "state": "idle", "icon": "🐾"},
                {"id": "btn_reset_identity", "label": "Réinitialiser la Saisie", "role": "secondary", "state": "idle", "icon": "↩"}
            ],
            "validationMsg": {
                "title": "Identité Civile & Mémorielle Validée in-silico",
                "badge": "Conforme CDDL AeterniCore v1 & Tag 100",
                "detail": "Contrôles validator.ts réussis sans avertissement. Longueurs UTF-8 vérifiées, date Tag 100 normalisée et pays ISO 3166-1 certifié."
            },
            "errorCase": {
                "code": "ERR_PROFILE_MISSING_BIRTH_DATE",
                "title": "Date de Naissance Absente pour Sujet Humain",
                "condition": "Validation d'un profil humain (subject_kind = 1) sans renseigner le Tag 100 de date de naissance.",
                "message": "Violation de la règle CDDL AeterniCore §A2.2 : Pour un sujet humain, la date de naissance (Tag 100 CBOR) est strictement obligatoire dans le profil silicium.",
                "remediation": "Renseigner la date de naissance dans le sélecteur calendaire ou basculer en profil animal (subject_kind = 2) si le sujet est un animal de compagnie."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Formulaire d'Identité & État Civil en Attente",
                    "caption": "Formulaire complet déployé. Sélection du profil (humain/animal) et champs d'état civil en attente de saisie.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Identité Civile & Mémorielle</span>
                        <span class="wf-status-badge wf-badge-neutral">En Attente de Saisie</span>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-field-group">
                          <label class="wf-label">Nature du Sujet (subject_kind) <span class="wf-req">*</span></label>
                          <div class="wf-select-placeholder">1 — Être Humain (Sujet de droit)</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Prénom Usuel (usage_name) <span class="wf-req">*</span></label>
                          <div class="wf-input-placeholder">Guy</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Nom Patronyme / Naissance (birth_name)</label>
                          <div class="wf-input-placeholder">Heyman</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Prénoms Officiels Secondaires (given_names, max 8)</label>
                          <div class="wf-input-placeholder">Jean, Robert, Émile</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Date de Naissance (birth_date, Tag 100) <span class="wf-req">*</span></label>
                          <div class="wf-input-placeholder">14 / 06 / 1942</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Date de Décès (death_date, Tag 100)</label>
                          <div class="wf-input-placeholder">02 / 10 / 2026</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Code Pays (country, ISO 3166-1 α2) <span class="wf-req">*</span></label>
                          <div class="wf-select-placeholder">BE — Belgique</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Rite Cérémoniel (rite_code) <span class="wf-req">*</span></label>
                          <div class="wf-select-placeholder">0 — Cérémonie Civile & Laïque sous les Arbres</div>
                        </div>
                        <div class="wf-field-group" style="grid-column: 1 / -1;">
                          <label class="wf-label">Épitaphe Mémorielle & Hommage (1 à 1 600 octets UTF-8) <span class="wf-req">*</span></label>
                          <div class="wf-textarea-placeholder">« Dans le souffle du vent et la lumière des sous-bois, ta bienveillance demeure éternelle. »</div>
                          <div class="wf-subtext text-right font-mono">142 / 1 600 octets UTF-8 • 100% Hors-Ligne</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">👤 Valider l'Identité Mémorielle (validator.ts)</button>
                        <button class="wf-btn wf-btn-sub">🐾 Mode Animal (Taxon NCBI)</button>
                      </div>
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Validation Tactile de l'Identité Saisie",
                    "triggerName": "Tap sur 'Valider l'Identité Mémorielle (validator.ts)'",
                    "caption": "Saisie complétée pour Guy Heyman (1942 — 2026, BE, épitaphe 142 B) et déclenchement de l'audit syntaxique.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Validation Déclenchée</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Déclencheur validator.ts</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">⚡ Validation Déclenchée : Guy Heyman (1942 — 2026)</div>
                        <div class="wf-selection-summary">
                          <strong>Profil Humain :</strong> Prénom : Guy • Patronyme : Heyman • 3 Prénoms secondaires • Dates Tag 100 RFC 8949 • Pays : BE • Épitaphe : 142 octets
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Audit Syntaxique in-silico en cours...</button>
                      </div>
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Audit Syntaxique Déterministe (validator.ts)",
                    "progress": 84,
                    "caption": "Vérification des longueurs en octets UTF-8, typage strict des clés [1..13] et encodage Tag 100 RFC 8949.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Moteur de Validation AeterniCore</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Contrôle validator.ts (84%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 84%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [CORE-VAL] Lecture des clés racine CDDL [1..13] : schema_version=1 OK</code><br>
                        <code>> [CORE-VAL] Clé 2 subject_kind=1 (humain) • Clé 3 names: usage_name="Guy" (3 B), birth_name="Heyman" (6 B), 3 given_names OK</code><br>
                        <code>> [CORE-VAL] Clé 4 birth_date: Tag 100 (-869443200) • Clé 5 death_date: Tag 100 (1790908800) OK</code><br>
                        <code>> [CORE-VAL] Clé 7 country="BE" (ISO 3166-1 alpha-2) • Clé 12 epitaph: 142 B (limite 1600 B) : CONFORME</code><br>
                        <code>> [CORE-VAL] Clé 13 species_taxid: absent (interdit pour subject_kind=1) : SUCCÈS ZERO ANOMALIE</code>
                      </div>
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Profil Mémoriel Structuré & Verrouillé",
                    "status": "success",
                    "caption": "Validation in-silico réussie. Bloc Identité scellé, prêt pour l'intégration des médias et directives.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Identité Mémorielle Scellée</span>
                        <span class="wf-status-badge wf-badge-success">✨ Profil Homologué</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">🏆</span>
                        <div>
                          <strong>Identité de Guy Heyman (1942 — 2026) Validée in-silico</strong>
                          <p class="wf-subtext">Structure CBOR Tag 100 certifiée par validator.ts • Prêt pour intégration des portraits WebP 480×480 (DEC-AET-12) et des volontés</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Étape Suivante : Studio Photo WebP (UC-104) →</button>
                      </div>
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-112",
        "title": "Édition, Révision Modulaire & Contrôle Différentiel du Projet CBOR",
        "cat": "Gestion de Projet & Révision",
        "actor": "Famille & Conseiller Funéraire",
        "platforms": ["Web Standard (PWA Hors-Ligne)", "Natif (iOS & Android)"],
        "tags": ["Revision", "CapsuleCBOR", "ControleDifferentiel", "DeltaBudget", "ACOSJ92k", "AuditTrail"],
        "preconditions": "Capsule projet existante (.aetk ou archive de travail CBOR) importée dans PaxStudio Pro pour révision ou ajustement par la famille.",
        "flow": [
            "Chargement et déballage sécurisé de la capsule de travail existante (.aetk ou draft CBOR) en environnement 100% hors-ligne.",
            "Affichage modulaire du tableau de bord d'édition par section : Identité civile, Portraits WebP 480×480 (DEC-AET-12), Mémo vocal Opus SILK, Musique d'ambiance et Directives.",
            "Sélection et modification ciblée d'une ou plusieurs sections (ex: mise à jour du portrait officiel 480×480, nouvel enregistrement vocal ou réécriture de l'épitaphe).",
            "Calcul différentiel dynamique des octets (Delta-Budget Silicium ACOSJ 92 Ko) mesurant l'impact exact sur chaque partition physique (EF-1 Métadonnées, EF-2 Identité, EF-3 Médias, EF-4 Directives).",
            "Contrôle de non-régression syntaxique via validator.ts sur chaque bloc modifié afin de prévenir toute régression de schéma.",
            "Vérification stricte du plafond matériel absolu de 92 160 octets (EEPROM puce ACOSJ).",
            "Génération et scellement local de la capsule incrémentale v1.1 (.aetk) avec journal d'audit des révisions, prête pour transmission étanche à PaxStation."
        ],
        "postconditions": "Capsule révisée conforme à 100% au schéma AeterniCore v1, journal de modifications (audit trail) généré et delta-budget validé sous les 92 160 octets matériels.",
        "legal": "Règlement général sur la protection des données (RGPD art. 16 - droit de rectification) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "tablet",
            "deviceLabel": "PaxStudio Pro • Studio de Révision & Contrôle Différentiel",
            "formFields": [
                {"label": "Capsule Projet Importée", "name": "project_capsule", "type": "file", "value": "capsule_projet_guy_heyman_v1.0.aetk (34.2 Ko)", "placeholder": "Sélectionner une capsule", "badge": "Archive .aetk", "required": True},
                {"label": "Module en Édition Active", "name": "active_module", "type": "select", "value": "Section 2 : Portrait WebP 480×480 + Section 1 : Épitaphe Mémorielle", "placeholder": "Choisir le module", "badge": "Modulaire", "required": True},
                {"label": "Nouveau Portrait WebP (EF-2)", "name": "new_portrait", "type": "file", "value": "portrait_guy_sourire_480x480.webp (13.8 Ko, conforme DEC-AET-12)", "placeholder": "Importer portrait", "badge": "WebP 480×480", "required": False},
                {"label": "Réenregistrement Vocal Opus SILK", "name": "new_voice_memo", "type": "file", "value": "message_guy_adieu_v2.opus (26.1 Ko ≤ 46 080 octets)", "placeholder": "Importer audio", "badge": "Opus SILK", "required": False},
                {"label": "Ajustement Épitaphe", "name": "edit_epitaph", "type": "textarea", "value": "« Dans le souffle du vent et la lumière des sous-bois, ta bienveillance et ton sourire demeurent éternels. » (158 octets)", "placeholder": "Épitaphe mise à jour", "badge": "1..1600 Octets", "required": False},
                {"label": "Contrôle Différentiel Silicium", "name": "silicon_delta", "type": "text", "value": "+1 420 octets (Taille totale : 35.62 Ko / 92 Ko EEPROM — Marge restante : 56.38 Ko)", "placeholder": "Delta octets", "badge": "Delta Conforme", "required": False},
                {"label": "Motif de Révision (Audit Trail)", "name": "revision_reason", "type": "text", "value": "Ajustement familial : Ajout du portrait souriant et révision douce de l'épitaphe", "placeholder": "Raison de révision", "badge": "Audit Trail", "required": True}
            ],
            "actionButtons": [
                {"id": "btn_reopen_capsule", "label": "Réouvrir une Capsule Projet (.aetk)", "role": "secondary", "state": "idle", "icon": "📂"},
                {"id": "btn_calc_delta", "label": "Calculer le Delta Différentiel & Valider Révision", "role": "primary", "state": "idle", "icon": "⚖️"},
                {"id": "btn_export_revision", "label": "Générer la Capsule Révisée pour PaxStation", "role": "secondary", "state": "idle", "icon": "💾"}
            ],
            "validationMsg": {
                "title": "Projet Révisé & Delta-Budget Conforme",
                "badge": "Delta Net +1 420 Octets • Marge 56.38 Ko",
                "detail": "Toutes les modifications respectent validator.ts. Partition EF-3 et taille globale (35.62 Ko) sous le seuil matériel strict de 92 Ko de la puce ACOSJ."
            },
            "errorCase": {
                "code": "ERR_REVISION_QUOTA_OVERFLOW",
                "title": "Dépassement du Budget Silicium lors de la Révision",
                "condition": "L'import de médias plus lourds lors de la révision porte la taille totale de la capsule au-delà des 92 160 octets de la puce ACOSJ.",
                "message": "Erreur matérielle différentielle : Le delta calculé (+58.4 Ko) fait dépasser la capacité maximale de la carte (92 Ko EEPROM disponible).",
                "remediation": "Compresser le portrait WebP sous les 20 Ko (DEC-AET-12) ou resserrer la durée du mémo vocal Opus SILK pour rester sous le quota global."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Capsule Existante Chargée & Diagnostic de Partitionnement",
                    "caption": "Capsule v1.0 ouverte. Diagnostic des 4 partitions matérielles affiché, formulaire d'édition modulaire prêt.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Gestion & Révision de Projet</span>
                        <span class="wf-status-badge wf-badge-neutral">Capsule Ouverte</span>
                      </div>
                      <div class="wf-content-grid">
                        <div class="wf-field-group">
                          <label class="wf-label">Projet Chargé <span class="wf-req">*</span></label>
                          <div class="wf-select-placeholder">📁 capsule_projet_guy_heyman_v1.0.aetk (34.2 Ko)</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Statut Matériel Silicium</label>
                          <div class="wf-input-placeholder">ACOSJ 92 Ko EEPROM (34.2 Ko occupés / 57.8 Ko libres)</div>
                        </div>
                        <div class="wf-field-group" style="grid-column: 1 / -1;">
                          <label class="wf-label">Sélection du Module à Modifier</label>
                          <div class="wf-select-placeholder">✏️ Section 2 : Portrait WebP 480×480 + Section 1 : Épitaphe Mémorielle</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Nouveau Portrait WebP (EF-2)</label>
                          <div class="wf-input-placeholder">portrait_guy_sourire_480x480.webp (13.8 Ko, DEC-AET-12)</div>
                        </div>
                        <div class="wf-field-group">
                          <label class="wf-label">Mémo Vocal Opus SILK (EF-3)</label>
                          <div class="wf-input-placeholder">Conserver mémo vocal v1.0 (24.7 Ko ≤ 46 080 octets)</div>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary">⚖️ Calculer le Delta Différentiel & Valider Révision</button>
                        <button class="wf-btn wf-btn-sub">📂 Ouvrir Autre Capsule (.aetk)</button>
                      </div>
                    </div>"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Application des Modifications & Clic sur 'Calculer le Delta'",
                    "triggerName": "Tap sur 'Calculer le Delta Différentiel & Valider Révision'",
                    "caption": "Portrait remplacé (480×480 WebP), épitaphe enrichie et déclenchement de l'audit différentiel temps réel.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Révision Active</span>
                        <span class="wf-status-badge wf-badge-trigger">⚡ Déclencheur Contrôle Différentiel</span>
                      </div>
                      <div class="wf-trigger-card wf-radar-pulse">
                        <div class="wf-trigger-indicator">⚡ Calcul Différentiel Déclenché : Remplacement Portrait + Épitaphe</div>
                        <div class="wf-selection-summary">
                          <strong>Modifications :</strong> Nouveau portrait 480×480 (+1 404 B) • Épitaphe (+16 B) • Delta brut : +1 420 octets
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-primary wf-pulse-btn">Audit Différentiel Silicium en cours...</button>
                      </div>
                    </div>"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Audit Différentiel & Vérification validator.ts",
                    "progress": 88,
                    "caption": "Décompression CBOR RFC 8949, calcul du différentiel octets par partition, recalcul des empreintes SHA-256 et validation syntaxique.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Contrôleur Différentiel Silicium</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Contrôle Différentiel (88%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 88%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [DIFF-ENGINE] Déballage CBOR capsule v1.0 : 34 200 octets</code><br>
                        <code>> [DIFF-ENGINE] Partition EF-1 (Métadonnées) : delta = 0 B</code><br>
                        <code>> [DIFF-ENGINE] Partition EF-2 (Identité & Portrait 480x480) : 12 400 B -> 13 804 B (delta = +1 404 B)</code><br>
                        <code>> [DIFF-ENGINE] Partition EF-3 (Mémo Vocal Opus SILK) : 24 700 B (delta = 0 B ≤ 46 080 octets)</code><br>
                        <code>> [DIFF-ENGINE] Nouveau total prévisionnel : 35 620 octets / 92 160 octets (38.6% du budget matériel)</code><br>
                        <code>> [VALIDATOR-TS] Contrôle de non-régression syntaxique CDDL : 100% CONFORME ZERO ERREUR</code>
                      </div>
                    </div>"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Projet Révisé Scellé (v1.1) & Delta Approuvé",
                    "status": "success",
                    "caption": "Révision homologuée avec succès. Delta de +1 420 octets validé (marge restante 56.38 Ko). Capsule prête pour PaxStation.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                      <div class="wf-header-bar">
                        <span class="wf-app-title">PaxStudio Pro • Capsule Révisée Prête</span>
                        <span class="wf-status-badge wf-badge-success">✨ Projet v1.1 Scellé</span>
                      </div>
                      <div class="wf-success-banner">
                        <span class="wf-seal-icon">💾</span>
                        <div>
                          <strong>Capsule Révisée v1.1 Générée avec Succès (35.62 Ko)</strong>
                          <p class="wf-subtext">Delta-budget validé (+1 420 octets) • Marge EEPROM restante : 56.54 Ko • Conforme validator.ts</p>
                        </div>
                      </div>
                      <div class="wf-btn-row">
                        <button class="wf-btn wf-btn-gold">Transmettre la Capsule Révisée à PaxStation →</button>
                      </div>
                    </div>"""
                }
            }
        }
    },
    {
        "id": "UC-113",
        "title": "Gestion des Conflits d'État Civil & Noms Complexes UTF-8 (Forme Canonique NFC)",
        "cat": "Identité Civile & Mémorielle",
        "actor": "Famille & Conseiller Funéraire",
        "platforms": ["Web Standard (PWA Hors-Ligne)", "Natif (iOS & Android)"],
        "tags": [
    "UTF-8",
    "NFC",
    "Normalisation",
    "Unicode",
    "CBOR",
    "RFC8949",
    "AeterniCore",
    "EF-1"
],
        "preconditions": "Saisie dans PaxStudio d'un patronyme comportant des graphies complexes (ligatures œ/æ, diacritiques, apostrophes typographiques ou alphabet cyrillique/grec).",
        "flow": [
            "Saisie des noms, prénoms et mentions honorifiques de la personne défunte par le conseiller funéraire en présence de la famille.",
            "Interception par le composant AeterniCore : détection de séquences Unicode potentiellement décomposées (NFD) ou caractères ambigus.",
            "Application automatique de la normalisation Unicode Forme C (NFC - Décomposition canonique suivie de composition canonique selon UAX #15).",
            "Contrôle de conformité de l'empreinte binaire CBOR canonique selon RFC 8949 §4.2.1 sans ambiguïté de tri lexicographique.",
            "Validation de l'encodage sous la limite de 2 048 octets allouée à la partition EF-1 et affichage du sceau de conformité textuelle."
        ],
        "postconditions": "Toutes les chaînes d'identité sont canonisées en UTF-8 NFC strict et intégrées au profil mémoriel EF-1 sans risque de rupture d'empreinte.",
        "legal": "Règlement (UE) n° 910/2014 (eIDAS - intégrité des représentations textuelles) & Standard Unicode Annex #15 (Unicode Normalization Forms).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "tablet",
            "deviceLabel": "PaxStudio Pro • Module de Canonisation UTF-8 NFC (Partition EF-1)",
            "formFields": [
                {
                    "label": "Nom Patronymique Saisi",
                    "name": "raw_name",
                    "type": "text",
                    "value": "Éléonore de La Tour-d'Œüvres",
                    "placeholder": "Nom officiel",
                    "badge": "Entrée Brute",
                    "required": True
                },
                {
                    "label": "Forme Canonique NFC",
                    "name": "nfc_canonical",
                    "type": "text",
                    "value": "Éléonore de La Tour-d'Œuvres (NFC UAX#15)",
                    "badge": "Canonisé",
                    "required": False
                },
                {
                    "label": "Partition Cible EF-1",
                    "name": "ef1_budget",
                    "type": "text",
                    "value": "1 420 octets / 2 048 octets (69.3%)",
                    "badge": "STORAGE-001",
                    "required": False
                },
                {
                    "label": "Déterminisme CBOR RFC 8949",
                    "name": "cbor_determinism",
                    "type": "text",
                    "value": "VALIDÉ (Tri des clés d'état civil sans ambiguïté)",
                    "badge": "AeterniCore",
                    "required": False
                }
            ],
            "actionButtons": [
                {
                    "id": "btn_canonize_utf8",
                    "label": "Normaliser en UTF-8 NFC & Valider CBOR",
                    "role": "primary",
                    "state": "idle",
                    "icon": "🔤"
                },
                {
                    "id": "btn_reset_name",
                    "label": "Réinitialiser la Saisie",
                    "role": "secondary",
                    "state": "idle",
                    "icon": "↩"
                }
            ],
            "validationMsg": {
                "title": "Normalisation Unicode NFC & Déterminisme CBOR Validés",
                "badge": "Conforme UAX #15 / RFC 8949",
                "detail": "La chaîne patronymique est canonisée sous forme NFC. Empreinte binaire EF-1 déterministe garantie sur tout lecteur sans contact."
            },
            "errorCase": {
                "code": "ERR_UTF8_NORMALIZATION_FAILED",
                "title": "Échec de Normalisation Unicode ou Caractère de Contrôle Interdit",
                "condition": "Présence d'octets mal formés, de points de code non assignés ou de caractères de contrôle non autorisés (U+0000..U+001F).",
                "message": "Erreur critique : La chaîne d'état civil contient des séquences d'octets invalides violant les règles d'interopérabilité CBOR canonique.",
                "remediation": "Purger automatiquement les caractères de contrôle non imprimables et resoumettre la chaîne pour décomposition-recomposition NFC."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Saisie d'un Nom Complexe avec Diacritiques & Ligatures",
                    "caption": "Texte brut saisi par l'opérateur. Les ligatures et accents décomposés doivent être harmonisés avant gravure silicium.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStudio Pro • État Civil & Normalisation UTF-8</span>
                                            <span class="wf-status-badge wf-badge-neutral">Saisie Non Canonisée</span>
                                          </div>
                                          <div class="wf-content-grid">
                                            <div class="wf-field-group">
                                              <label class="wf-label">Nom Brut Saisi <span class="wf-req">*</span></label>
                                              <div class="wf-input-placeholder">Éléonore de La Tour-d'Œüvres (Caractères combinants détectés)</div>
                                            </div>
                                            <div class="wf-field-group">
                                              <label class="wf-label">Contrôle de Partition EF-1</label>
                                              <div class="wf-input-placeholder">Quota alloué : 2 048 octets (Profil CBOR)</div>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary">🔤 Normaliser en UTF-8 NFC & Valider CBOR</button>
                                          </div>
                                        </div>
"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Déclenchement du Moteur de Canonisation Unicode",
                    "triggerName": "Clic sur 'Normaliser en UTF-8 NFC & Valider CBOR'",
                    "caption": "Analyse syntaxique, recomposition des caractères diacritiques combinés en points de code précomposés canoniques.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStudio Pro • Moteur de Canonisation</span>
                                            <span class="wf-status-badge wf-badge-trigger">⚡ Analyse UAX #15 Active</span>
                                          </div>
                                          <div class="wf-trigger-card wf-radar-pulse">
                                            <div class="wf-trigger-indicator">✓ Traitement de la forme NFC : u + ̈ -> ü • OE -> Œ</div>
                                            <div class="wf-subtext">Tri déterministe des clés de la carte CBOR RFC 8949 (Tag 100 Identité Civile)</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary wf-pulse-btn">Canonisation binaire en cours...</button>
                                          </div>
                                        </div>
"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Validation de l'Empreinte Binaire & Budget EF-1",
                    "progress": 92,
                    "caption": "Encodage CBOR strict, calcul de l'empreinte SHA-256 et contrôle d'insertion sous les 2 048 octets d'EF-1.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStudio Pro • Contrôle CBOR EF-1</span>
                                            <span class="wf-status-badge wf-badge-process">⚙️ Vérification Normative (92%)</span>
                                          </div>
                                          <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 92%;"></div></div>
                                          <div class="wf-console-log">
                                            <code>> [UNICODE-NFC] Normalisation achevée : 38 caractères UTF-8 sans combinaison flottante</code><br>
                                            <code>> [CBOR-RFC8949] Tri des clés de table 100 : determinisme strict vérifié</code><br>
                                            <code>> [STORAGE-001] Partition EF-1 : 1 420 octets occupés / 2 048 octets max (69.3% du quota)</code><br>
                                            <code>> [AETERNI-CORE] Zéro discordance d'empreinte lors de la relecture sans contact</code>
                                          </div>
                                        </div>
"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Identité Civile Canonique Scellée dans EF-1",
                    "status": "success",
                    "caption": "Profil civil parfaitement normalisé. Aucune ambiguïté d'affichage ni de calcul d'empreinte pour la gravure PaxStation.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStudio Pro • État Civil Prêt</span>
                                            <span class="wf-status-badge wf-badge-success">✨ Conforme NFC & CBOR</span>
                                          </div>
                                          <div class="wf-success-banner">
                                            <span class="wf-seal-icon">📜</span>
                                            <div>
                                              <strong>Profil Civil Déterministe Généré avec Succès (1.42 Ko)</strong>
                                              <p class="wf-subtext">Canonisation UTF-8 NFC conforme UAX #15 • Prêt pour injection dans EF-1 ACOSJ 92K</p>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-gold">Intégrer au Projet & Passer à la Signature →</button>
                                          </div>
                                        </div>
"""
                }
            }
        }
    },
    {
        "id": "UC-114",
        "title": "Dépassement de Quota Audio & Ré-échantillonnage d'Urgence Opus SILK (< 46 080 octets)",
        "cat": "Médias Sonores",
        "actor": "Conseiller Funéraire & Studio Acoustique",
        "platforms": ["Web Standard (PWA Hors-Ligne)", "Natif (iOS & Android)"],
        "tags": [
    "Audio",
    "OpusSILK",
    "QuotaEF3",
    "Compression",
    "STORAGE-001",
    "WebAudio",
    "EF-3"
],
        "preconditions": "Enregistrement d'un hommage vocal dont la durée ou le débit génère un fichier dépassant le plafond strict de 46 080 octets d'EF-3.",
        "flow": [
            "Enregistrement du témoignage vocal de la famille dans l'atelier acoustique de PaxStudio.",
            "Le module de compression analyse le flux PCM brut et calcule la taille compressée prévisionnelle (ex: 51 200 octets > 46 080 octets).",
            "Détection automatique du dépassement de la partition EF-3 du jalon STORAGE-001.",
            "Engagement de l'algorithme de ré-échantillonnage dynamique : réduction contrôlée du débit Opus SILK de 16 kbps à 12 kbps mono à 16 kHz.",
            "Re-compression in-silico avec ducking et filtre vocal : la taille finale s'établit à 42 100 octets, certifiant le respect du quota d'EF-3."
        ],
        "postconditions": "L'hommage vocal tient rigoureusement dans la partition EF-3 (46 080 octets max) sans sacrifier l'intelligibilité ni l'émotion vocale.",
        "legal": "Spécification technique AeterniTrak STORAGE-001 (partitionnement silicium EF-3) & Norme IETF RFC 6716 (Codec Opus).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "tablet",
            "deviceLabel": "PaxStudio Pro • Studio Acoustique & Compresseur Opus SILK (Partition EF-3)",
            "formFields": [
                {
                    "label": "Durée Message Vocal",
                    "name": "audio_duration",
                    "type": "text",
                    "value": "29.4 secondes (Voix parlée)",
                    "badge": "Chronométré",
                    "required": False
                },
                {
                    "label": "Taille Prévisionnelle Brute",
                    "name": "raw_audio_size",
                    "type": "text",
                    "value": "51 200 octets (> 46 080 octets)",
                    "badge": "Dépassement Alerte",
                    "required": False
                },
                {
                    "label": "Algorithme Ré-échantillonnage",
                    "name": "codec_profile",
                    "type": "select",
                    "value": "Opus SILK 16 kHz Mono 12 kbps VBR",
                    "badge": "Adaptatif",
                    "required": True
                },
                {
                    "label": "Taille Finale Compressée",
                    "name": "final_audio_size",
                    "type": "text",
                    "value": "42 100 octets / 46 080 octets (91.4%)",
                    "badge": "Conforme EF-3",
                    "required": False
                }
            ],
            "actionButtons": [
                {
                    "id": "btn_resample_audio",
                    "label": "Ré-échantillonner en Opus SILK & Valider Quota",
                    "role": "primary",
                    "state": "idle",
                    "icon": "🎙️"
                },
                {
                    "id": "btn_crop_audio",
                    "label": "Rogner la Fin de l'Enregistrement",
                    "role": "secondary",
                    "state": "idle",
                    "icon": "✂️"
                }
            ],
            "validationMsg": {
                "title": "Hommage Vocal Recompressé sous le Quota EF-3",
                "badge": "Conforme STORAGE-001 EF-3",
                "detail": "Fichier audio Opus SILK calibré à 42 100 octets. Intégrité émotionnelle et intelligibilité 100% préservées."
            },
            "errorCase": {
                "code": "ERR_AUDIO_PAYLOAD_OVERFLOW",
                "title": "Dépassement de Quota Audio Irréductible (> 46 080 octets)",
                "condition": "Enregistrement excédant 35 secondes ne pouvant être compressé sous 46 080 octets même au débit plancher de 10 kbps.",
                "message": "Erreur silicium : Le fichier audio compressé (48.9 Ko) dépasse le plafond absolu de 46 080 octets alloué à la partition EF-3 de la puce ACOSJ.",
                "remediation": "Utiliser l'outil de rognage intégré pour raccourcir l'hommage à 30 secondes maximum avant ré-échantillonnage."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Alerte de Dépassement de Quota Audio EF-3",
                    "caption": "L'enregistrement vocal dépasse la capacité de la partition EF-3 (51.2 Ko mesurés contre 46.08 Ko alloués).",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStudio Pro • Moniteur Audio EF-3</span>
                                            <span class="wf-status-badge wf-badge-neutral">Dépassement de Quota</span>
                                          </div>
                                          <div class="wf-device-status-box" style="border-color: #f59e0b;">
                                            <span class="wf-qa-icon">⚠️</span>
                                            <div><strong>Dépassement de Partition Détecté</strong></div>
                                            <div class="wf-subtext">51 200 octets calculés • Plafond strict EF-3 : 46 080 octets (Dépassement : +5 120 octets)</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary">🎙️ Ré-échantillonner en Opus SILK & Valider Quota</button>
                                          </div>
                                        </div>
"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Déclenchement du Ré-échantillonnage d'Urgence",
                    "triggerName": "Clic sur 'Ré-échantillonner en Opus SILK'",
                    "caption": "Re-quantification des trames SILK, compression dynamique et ajustement psychoacoustique du spectre vocal.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStudio Pro • Moteur WebAudio</span>
                                            <span class="wf-status-badge wf-badge-trigger">⚡ Compression SILK Active</span>
                                          </div>
                                          <div class="wf-trigger-card wf-radar-pulse">
                                            <div class="wf-trigger-indicator">✓ Passage du profil 16 kbps -> 12 kbps adaptatif mono 16 kHz</div>
                                            <div class="wf-subtext">Suppression des silences aux extrémités et compression dynamique du signal</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary wf-pulse-btn">Recompression du flux vocal...</button>
                                          </div>
                                        </div>
"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Audit Binaire & Validation du Quota 46 080 Octets",
                    "progress": 95,
                    "caption": "Mesure bit-à-bit du conteneur Ogg Opus et vérification d'inviolabilité de la réserve matérielle ACOSJ.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStudio Pro • Vérification Silicium</span>
                                            <span class="wf-status-badge wf-badge-process">⚙️ Contrôle Quota (95%)</span>
                                          </div>
                                          <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 95%;"></div></div>
                                          <div class="wf-console-log">
                                            <code>> [AUDIO-ENGINE] Encodage Opus SILK 12 kbps achevé : 42 100 octets</code><br>
                                            <code>> [STORAGE-001] Partition EF-3 : 42 100 / 46 080 octets (Marge libre : 3 980 octets)</code><br>
                                            <code>> [AUDIO-QUALITY] Indice PESQ estimé : 4.1/5 (Excellente intelligibilité vocale)</code><br>
                                            <code>> [VERDICT] Intégration autorisée dans la capsule mémorielle AeterniCore</code>
                                          </div>
                                        </div>
"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Mémo Vocal Conforme Validé pour Gravure",
                    "status": "success",
                    "caption": "Le flux sonore est validé. Il respecte rigoureusement les quotas matériels de l'ACOSJ 92 Ko.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStudio Pro • Audio Homologué</span>
                                            <span class="wf-status-badge wf-badge-success">✨ 42.1 Ko • Conforme EF-3</span>
                                          </div>
                                          <div class="wf-success-banner">
                                            <span class="wf-seal-icon">🎵</span>
                                            <div>
                                              <strong>Mémo Vocal Inaltérable Calibré avec Succès (42.1 Ko)</strong>
                                              <p class="wf-subtext">Respect strict du plafond 46 080 octets d'EF-3 • Prêt pour scellement et gravure</p>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-gold">Valider l'Hommage Sonore & Continuer →</button>
                                          </div>
                                        </div>
"""
                }
            }
        }
    },
    {
        "id": "UC-115",
        "title": "Refus de Signature ou Révocation du Mandat par le Représentant Légal",
        "cat": "Validation Finale & Juridique",
        "actor": "Représentant Légal & Conseiller Funéraire",
        "platforms": ["Web Standard (PWA Hors-Ligne)", "Natif (iOS & Android)"],
        "tags": [
    "Mandat",
    "Revocation",
    "RefusSignature",
    "BAT",
    "COSE_Sign1",
    "Sécurité",
    "EF-5"
],
        "preconditions": "La capsule de pré-encodage est assemblée, mais le mandataire légal s'oppose aux dispositions présentées ou retire son mandat.",
        "flow": [
            "Présentation du Bon à Tirer (BAT) numérique récapitulant les volontés, portraits et hommages.",
            "Le représentant légal notifie formellement son refus de signer ou révoque le mandat funéraire.",
            "PaxStudio intercepte la déclaration : annulation immédiate de la procédure de scellement COSE_Sign1.",
            "Destruction sécurisée en mémoire vive de la clé de session éphémère et purge du tampon d'encodage.",
            "Génération d'un procès-verbal d'interruption horodaté et mise en sommeil du projet sous statut RÉVOQUÉ."
        ],
        "postconditions": "Aucune enveloppe COSE_Sign1 n'est générée dans EF-5 ; la puce physique ne reçoit aucune gravure illégitime.",
        "legal": "Règlement Général sur la Protection des Données (RGPD Art. 7 §3 - retrait du consentement) & Code civil (mandat et dévolution funéraire).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "tablet",
            "deviceLabel": "PaxStudio Pro • Registre de Validation & Révocation de Mandat (Partition EF-5)",
            "formFields": [
                {
                    "label": "Représentant Légal Mandant",
                    "name": "mandat_holder",
                    "type": "text",
                    "value": "Mme Sophie Dumont (Fille aînée, Mandataire)",
                    "badge": "Ayant Droit",
                    "required": True
                },
                {
                    "label": "Statut du Mandat",
                    "name": "mandat_status",
                    "type": "select",
                    "value": "RÉVOCATION FORMELLE DU MANDAT / REFUS DE BAT",
                    "badge": "Opposition",
                    "required": True
                },
                {
                    "label": "Motif Déclaré",
                    "name": "revocation_reason",
                    "type": "text",
                    "value": "Désaccord familial sur l'épitaphe et choix du portrait",
                    "badge": "Consigné",
                    "required": True
                },
                {
                    "label": "Conséquence Cryptographique",
                    "name": "crypto_action",
                    "type": "text",
                    "value": "Scellement COSE_Sign1 Interdit • Purge Clé Session",
                    "badge": "Sécurité EF-5",
                    "required": False
                }
            ],
            "actionButtons": [
                {
                    "id": "btn_confirm_revocation",
                    "label": "Activer la Révocation & Bloquer le Projet",
                    "role": "primary",
                    "state": "idle",
                    "icon": "🚫"
                },
                {
                    "id": "btn_resume_dialogue",
                    "label": "Poursuivre la Médiation Familiale",
                    "role": "secondary",
                    "state": "idle",
                    "icon": "🤝"
                }
            ],
            "validationMsg": {
                "title": "Interruption Formelle Enregistrée & Projet Mis en Réserve",
                "badge": "Projet Révocation Consignée",
                "detail": "Le scellement de la partition EF-5 est annulé. Les clés de session sont purgées. Aucun transfert vers la PaxStation n'est autorisé."
            },
            "errorCase": {
                "code": "ERR_MANDATE_REVOKED_BY_REPRESENTATIVE",
                "title": "Révocation Formelle du Mandat par l'Ayant Droit Référent",
                "condition": "Refus explicite de signer le Bon à Tirer ou notification de litige entre les héritiers légitimes.",
                "message": "Blocage légal absolu : Le mandataire a révoqué son autorisation. La génération de l'enveloppe cryptographique COSE_Sign1 est interdite.",
                "remediation": "Clôturer la session de pré-encodage, éditer le PV de suspension et orienter la famille vers la conciliation notariale."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Notification de Révocation du Mandat en Salon",
                    "caption": "L'ayant droit exprime son désaccord face au Bon à Tirer et demande l'arrêt de la procédure d'encodage.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStudio Pro • Contrôle Juridique du Mandat</span>
                                            <span class="wf-status-badge wf-badge-neutral">Opposition Signalée</span>
                                          </div>
                                          <div class="wf-content-grid">
                                            <div class="wf-field-group">
                                              <label class="wf-label">Mandataire Référent</label>
                                              <div class="wf-input-placeholder">Mme Sophie Dumont (Mandataire désigné)</div>
                                            </div>
                                            <div class="wf-field-group">
                                              <label class="wf-label">Position Exprimée</label>
                                              <div class="wf-input-placeholder">Refus d'approuver le Bon à Tirer numérique</div>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary" style="background: #e11d48; border-color: #f43f5e;">🚫 Activer la Révocation & Bloquer le Projet</button>
                                          </div>
                                        </div>
"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Interception & Verrouillage du Scellement Cryptographique",
                    "triggerName": "Clic sur 'Activer la Révocation & Bloquer le Projet'",
                    "caption": "Interdiction immédiate de la commande de signature COSE_Sign1 et blocage de la transmission vers PaxStation.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStudio Pro • Blocage de Sécurité</span>
                                            <span class="wf-status-badge wf-badge-trigger">⚡ Révocation en Cours</span>
                                          </div>
                                          <div class="wf-trigger-card wf-radar-pulse" style="border-color: #f43f5e;">
                                            <div class="wf-trigger-indicator" style="color: #fda4af;">🚫 Révocation formelle enregistrée : scellement EF-5 interdit</div>
                                            <div class="wf-subtext">Purge des clés éphémères en mémoire RAM et annulation de l'envoi réseau local</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary wf-pulse-btn">Purge des tampons de pré-encodage...</button>
                                          </div>
                                        </div>
"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Édition du Procès-Verbal d'Interruption & Archivage",
                    "progress": 100,
                    "caption": "Création du rapport légal d'opposition conformément aux obligations professionnelles funéraires.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStudio Pro • Journalisation Légale</span>
                                            <span class="wf-status-badge wf-badge-process">⚙️ Archivage d'Opposition</span>
                                          </div>
                                          <div class="wf-console-log">
                                            <code>> [LEGAL-AUDIT] Déclaration d'opposition reçue à 11:42:09 UTC</code><br>
                                            <code>> [CRYPTO-GUARD] Signature EF-5 ABORTÉE : aucune clé d'atelier engagée</code><br>
                                            <code>> [ZERO-LEAK] Destruction des artefacts de personnalisation dans le cache local</code><br>
                                            <code>> [PV-ENGINE] PV d'interruption #PV-REVOC-2026-081 édité et archivé</code>
                                          </div>
                                        </div>
"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Dossier Mis en Séquestre & Zéro Gravure Autorisée",
                    "status": "success",
                    "caption": "Protection juridique assurée. Aucune puce silicium n'est altérée. Les droits des parties sont préservés.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStudio Pro • Statut Clôturé</span>
                                            <span class="wf-status-badge wf-badge-success" style="background: rgba(225, 29, 72, 0.2); color: #fda4af;">🚫 Projet Suspendu</span>
                                          </div>
                                          <div class="wf-success-banner" style="border-color: rgba(244, 63, 94, 0.4);">
                                            <span class="wf-seal-icon">⚖️</span>
                                            <div>
                                              <strong>Procédure de Personnalisation Officiellement Suspendue</strong>
                                              <p class="wf-subtext">Mandat révoqué • Données purgées • PV d'interruption remis aux parties</p>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-sub">Retour au Tableau de Bord PaxStudio</button>
                                          </div>
                                        </div>
"""
                }
            }
        }
    },
    {
        "id": "UC-116",
        "title": "Conflit de Résolution / Ratio Portrait & Recadrage Intelligent 480x480 WebP",
        "cat": "Médias Visuels",
        "actor": "Famille & Graphiste PaxStudio",
        "platforms": ["Web Standard (PWA Hors-Ligne)", "Natif (iOS & Android)"],
        "tags": [
    "WebP",
    "480x480",
    "Recadrage",
    "Ratio1:1",
    "DEC-AET-12",
    "STORAGE-001",
    "EF-2"
],
        "preconditions": "Sélection d'une photo souvenir familiale au ratio rectangulaire (16:9, 4:3) ou de résolution non normalisée (> 3000x2000 px).",
        "flow": [
            "Importation du cliché photographique souvenir par la famille dans le studio portrait de PaxStudio.",
            "Détection d'un ratio non carré (aspect ratio != 1:1) et d'un volume binaire source dépassant les capacités de la puce.",
            "Activation du module d'assistance au cadrage : calcul automatique du centre de gravité visuel et détection du visage.",
            "Application du masque de recadrage carré 1:1 et redimensionnement strict à 480×480 pixels selon la décision DEC-AET-12.",
            "Compression WebP avec jauge de contrôle en direct : validation d'un poids final inférieur à 20 480 octets et injection dans EF-2."
        ],
        "postconditions": "L'image WebP 480×480 px pèse moins de 20 480 octets et s'intègre parfaitement dans la partition EF-2 de la puce ACOSJ.",
        "legal": "Décision Kudoro DEC-AET-12 (spécification portrait WebP 480×480) & Jalon STORAGE-001 (partition silicium EF-2).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "tablet",
            "deviceLabel": "PaxStudio Pro • Studio Graphique & Recadrage WebP 480×480 (Partition EF-2)",
            "formFields": [
                {
                    "label": "Image Source Importée",
                    "name": "source_image",
                    "type": "text",
                    "value": "vacances_famille_1998_paysage.jpg (4032×3024, 4.8 Mo)",
                    "badge": "Source 4:3",
                    "required": True
                },
                {
                    "label": "Résolution Cible DEC-AET-12",
                    "name": "target_resolution",
                    "type": "text",
                    "value": "480 × 480 pixels (Ratio 1:1 Carré Strict)",
                    "badge": "Souverain",
                    "required": False
                },
                {
                    "label": "Qualité de Compression WebP",
                    "name": "webp_quality",
                    "type": "select",
                    "value": "Qualité 82% (Poids optimisé sous 20 Ko)",
                    "badge": "Optimisé",
                    "required": True
                },
                {
                    "label": "Poids Final Partition EF-2",
                    "name": "ef2_budget",
                    "type": "text",
                    "value": "18 432 octets / 20 480 octets (90.0%)",
                    "badge": "STORAGE-001",
                    "required": False
                }
            ],
            "actionButtons": [
                {
                    "id": "btn_smart_crop",
                    "label": "Recadrer 1:1 & Convertir en WebP 480×480",
                    "role": "primary",
                    "state": "idle",
                    "icon": "🖼️"
                },
                {
                    "id": "btn_manual_crop",
                    "label": "Ajuster la Zone Focale Manuellement",
                    "role": "secondary",
                    "state": "idle",
                    "icon": "🔍"
                }
            ],
            "validationMsg": {
                "title": "Portrait WebP 480×480 Normalisé sous le Quota EF-2",
                "badge": "Conforme DEC-AET-12 / EF-2",
                "detail": "Image recadrée au ratio 1:1, résolution 480×480 px, poids calibré à 18 432 octets (inférieur au plafond strict de 20 480 octets)."
            },
            "errorCase": {
                "code": "ERR_IMAGE_ASPECT_RATIO_UNRESOLVED",
                "title": "Résolution Source Insuffisante ou Cadrage Impossible",
                "condition": "Image importée de résolution inférieure à 480×480 pixels ou flou critique empêchant la reconnaissance du sujet.",
                "message": "Erreur visuelle : La photographie fournie (320×240) est insuffisante pour garantir la dignité du portrait 480×480 sur le support physique.",
                "remediation": "Fournir un original photographique de résolution minimale 480×480 pixels ou sélectionner un autre cliché souvenir."
            },
            "phases": {
                "p1": {
                    "tabTitle": "1. Avant Trigger",
                    "phaseTitle": "Photo Source Paysage avec Alerte de Ratio",
                    "caption": "La photo importée présente un ratio 4:3 non adapté au médaillon mémoriel et dépasse les capacités mémoires.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStudio Pro • Cadreur Portrait EF-2</span>
                                            <span class="wf-status-badge wf-badge-neutral">Ratio Non Conforme (4:3)</span>
                                          </div>
                                          <div class="wf-content-grid">
                                            <div class="wf-field-group">
                                              <label class="wf-label">Cliché Importé</label>
                                              <div class="wf-input-placeholder">vacances_famille_1998.jpg (4032×3024 px - 4.8 Mo)</div>
                                            </div>
                                            <div class="wf-field-group">
                                              <label class="wf-label">Cible Silicium</label>
                                              <div class="wf-input-placeholder">EF-2 : 480×480 px WebP ≤ 20 480 octets (DEC-AET-12)</div>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary">🖼️ Recadrer 1:1 & Convertir en WebP 480×480</button>
                                          </div>
                                        </div>
"""
                },
                "p2": {
                    "tabTitle": "2. Déclenchement ⚡",
                    "phaseTitle": "Recadrage Centré & Détection Focale Visage",
                    "triggerName": "Clic sur 'Recadrer 1:1 & Convertir en WebP'",
                    "caption": "Application du centrage automatique sur le regard et génération du canvas 480×480.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStudio Pro • Moteur Visuel</span>
                                            <span class="wf-status-badge wf-badge-trigger">⚡ Recadrage Actif</span>
                                          </div>
                                          <div class="wf-trigger-card wf-radar-pulse">
                                            <div class="wf-trigger-indicator">✓ Détection focale : visage centré aux coordonnées (2016, 1512)</div>
                                            <div class="wf-subtext">Extraction de la matrice carrée 1:1 et ré-échantillonnage bi-cubique 480×480</div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-primary wf-pulse-btn">Compression WebP en cours...</button>
                                          </div>
                                        </div>
"""
                },
                "p3": {
                    "tabTitle": "3. Traitement ⚙️",
                    "phaseTitle": "Compression WebP & Contrôle du Plafond 20 480 Octets",
                    "progress": 96,
                    "caption": "Encodage WebP haute fidélité et validation stricte de l'insertion dans la partition EF-2.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStudio Pro • Contrôleur Silicium EF-2</span>
                                            <span class="wf-status-badge wf-badge-process">⚙️ Vérification Quota (96%)</span>
                                          </div>
                                          <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 96%;"></div></div>
                                          <div class="wf-console-log">
                                            <code>> [WEBP-CONVERT] Encodage 480x480 terminé : 18 432 octets générés</code><br>
                                            <code>> [STORAGE-001] Partition EF-2 : 18 432 / 20 480 octets (Marge libre : 2 048 octets)</code><br>
                                            <code>> [DEC-AET-12] Norme portrait validée sans débordement silicium</code><br>
                                            <code>> [INTEGRITY] Checksum SHA-256 calculé pour intégration dans la capsule</code>
                                          </div>
                                        </div>
"""
                },
                "p4": {
                    "tabTitle": "4. Écran de Fin ✨",
                    "phaseTitle": "Portrait Éternel Calibré & Prêt pour Scellement",
                    "status": "success",
                    "caption": "Le portrait est prêt pour orner le médaillon ou la carte mémorielle avec éclat.",
                    "screenHtml": """
                    <div class="wf-screen-box">
                                          <div class="wf-header-bar">
                                            <span class="wf-app-title">PaxStudio Pro • Portrait Scellé</span>
                                            <span class="wf-status-badge wf-badge-success">✨ 18.4 Ko • Conforme DEC-AET-12</span>
                                          </div>
                                          <div class="wf-success-banner">
                                            <span class="wf-seal-icon">🌟</span>
                                            <div>
                                              <strong>Portrait WebP 480×480 Validé avec Succès (18.44 Ko)</strong>
                                              <p class="wf-subtext">Plafond 20 480 octets EF-2 respecté • Rendu graphique optimal sur support ACOSJ</p>
                                            </div>
                                          </div>
                                          <div class="wf-btn-row">
                                            <button class="wf-btn wf-btn-gold">Insérer dans la Carte Sanctuaire & Valider →</button>
                                          </div>
                                        </div>
"""
                }
            }
        }
    },
{   'id': 'UC-117',
    'title': "Calculateur d'Empreinte Octet UTF-8 en direct vs Limite Silicium (1 900 o EF-1)",
    'cat': 'Compilation & Core',
    'actor': 'Famille & Conseiller Funéraire',
    'platforms': ['Web Standard (PWA Hors-Ligne)', 'Natif (iOS & Android)'],
    'tags': ['Silicium', 'UTF8', 'EF-1', 'Empreinte', 'JaugeOctets', 'Plafond1900', 'RFC3629'],
    'preconditions': "Saisie ou importation des textes d'épitaphe et d'hommages dans PaxStudio avec limitation "
                     'matérielle de la partition textuelle EF-1.',
    'flow': [   "L'utilisateur rédige les textes d'hommage et directives civiles dans l'éditeur de PaxStudio.",
                "Le moteur binaire intercepte chaque frappe et calcule l'empreinte en octets UTF-8 stricts selon la "
                'RFC 3629.',
                'Comparaison temps réel avec la réserve physique allouée à la partition EF-1 sur la puce ACOSJ (1 900 '
                'octets).',
                "Mise à jour de la jauge avec seuils chromatiques : vert (< 80%), orange (80-95%) et rouge d'alerte (> "
                '95%).',
                "Blocage préventif des dépassements avec proposition d'élagage automatique des espaces et ligatures."],
    'postconditions': 'Le texte est garanti inférieur ou égal à 1 900 octets UTF-8, assurant une écriture sans '
                      'débordement de tampon dans la puce.',
    'legal': 'Norme ISO/IEC 10646 (Jeu universel de caractères codés UTF-8 / RFC 3629) & Spécification AeterniTrak '
             'EF-1 (1 900 octets max).',
    'legal_url': '#section-legal',
    'wireframe': {   'device': 'tablet',
                     'deviceLabel': "PaxStudio Pro • Calculateur d'Empreinte UTF-8 vs Limite Silicium (Partition EF-1)",
                     'formFields': [   {   'label': 'Texte Mémoriel / Épitaphe Saisi',
                                           'name': 'epitaph_text',
                                           'type': 'text',
                                           'value': 'À notre père et guide vénéré, dont la bienveillance illuminera '
                                                    'nos cœurs à jamais...',
                                           'badge': 'UTF-8 Dynamique',
                                           'required': True},
                                       {   'label': 'Empreinte Binaire Réelle',
                                           'name': 'byte_count_realtime',
                                           'type': 'text',
                                           'value': '1 842 octets / 1 900 octets (Marge libre : 58 octets)',
                                           'badge': 'Jauge Silicium',
                                           'required': False},
                                       {   'label': 'Caractères Multi-Octets Détectés',
                                           'name': 'multibyte_analysis',
                                           'type': 'text',
                                           'value': '3 emojis (12 octets) • 24 caractères accentués (48 octets)',
                                           'badge': 'Analyse RFC 3629',
                                           'required': False},
                                       {   'label': 'Statut Partition EF-1',
                                           'name': 'ef1_buffer_status',
                                           'type': 'select',
                                           'value': '96.9% Utilisé (Seuil Vigilance Orange < 1 900 octets)',
                                           'badge': 'Puce ACOSJ 92K',
                                           'required': True}],
                     'actionButtons': [   {   'id': 'btn_optimize_utf8',
                                              'label': 'Élaguer Espaces & Optimiser UTF-8',
                                              'role': 'primary',
                                              'state': 'idle',
                                              'icon': '✂️'},
                                          {   'id': 'btn_simulate_ef1_burn',
                                              'label': 'Simuler Injection dans EF-1',
                                              'role': 'secondary',
                                              'state': 'idle',
                                              'icon': '💾'}],
                     'validationMsg': {   'title': 'Empreinte UTF-8 Conforme au Plafond EF-1 (1 842 / 1 900 octets)',
                                          'badge': 'Conforme Silicium EF-1',
                                          'detail': "Le volume textuel s'insère parfaitement dans la partition EF-1 "
                                                    'sans risque de troncature ni débordement.'},
                     'errorCase': {   'code': 'ERR_EF1_SILICON_OVERFLOW',
                                      'title': 'Dépassement de Capacité Silicium EF-1 (> 1 900 Octets)',
                                      'condition': "L'encodage UTF-8 du texte dépasse le plafond strict de 1 900 "
                                                   'octets alloué à la partition EF-1.',
                                      'message': 'Erreur matérielle : La mémoire allouée à la partition textuelle EF-1 '
                                                 '(1 900 o) est saturée de 42 octets.',
                                      'remediation': "Raccourcir l'épitaphe ou remplacer les caractères multi-octets "
                                                     'non essentiels pour repasser sous 1 900 octets.'},
                     'phases': {   'p1': {   'tabTitle': '1. Avant Trigger',
                                             'phaseTitle': "Texte Saisi avec Jauge d'Empreinte en Temps Réel",
                                             'caption': "L'utilisateur tape son texte d'hommage. La jauge calcule "
                                                        "l'empreinte UTF-8 à chaque frappe.",
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Calculateur UTF-8 '
                                                           'EF-1</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-neutral">Saisie Active (1 842 o / 1 900 '
                                                           'o)</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-content-grid">\n'
                                                           '                        <div class="wf-field-group">\n'
                                                           '                          <label class="wf-label">Texte '
                                                           'Hommage</label>\n'
                                                           '                          <div '
                                                           'class="wf-input-placeholder">À notre père et guide '
                                                           'vénéré... (Saisie en cours)</div>\n'
                                                           '                        </div>\n'
                                                           '                        <div class="wf-field-group">\n'
                                                           '                          <label class="wf-label">Jauge '
                                                           'Silicium EF-1</label>\n'
                                                           '                          <div '
                                                           'class="wf-input-placeholder" style="color: #f59e0b;">96.9% '
                                                           'saturé (58 octets disponibles)</div>\n'
                                                           '                        </div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-primary">✂️ Élaguer Espaces & Optimiser '
                                                           'UTF-8</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p2': {   'tabTitle': '2. Déclenchement ⚡',
                                             'phaseTitle': "Déclenchement de l'Optimisation des Espaces & Caractères",
                                             'triggerName': "Clic sur 'Élaguer Espaces & Optimiser UTF-8'",
                                             'caption': 'Nettoyage des espaces doubles, conversion des retours '
                                                        'chariots en LF simples et analyse des caractères 4-octets.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Moteur '
                                                           "d'Optimisation UTF-8</span>\n"
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-trigger">⚡ Optimisation Binaire Active</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-trigger-card '
                                                           'wf-radar-pulse">\n'
                                                           '                        <div '
                                                           'class="wf-trigger-indicator">✓ Élagage de 62 octets '
                                                           'superflus (espaces insécables, CRLF -> LF)</div>\n'
                                                           '                        <div '
                                                           'class="wf-subtext">Compression textuelle sans altération '
                                                           "sémantique de l'hommage familial</div>\n"
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-primary wf-pulse-btn">Recalcul de l\'empreinte '
                                                           'silicium...</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p3': {   'tabTitle': '3. Traitement ⚙️',
                                             'phaseTitle': "Recalcul Binaire & Validation d'Insertion dans EF-1",
                                             'progress': 92,
                                             'caption': 'Vérification de conformité RFC 3629 et contrôle du seuil de '
                                                        'sécurité de la puce ACOSJ.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Contrôleur Silicium '
                                                           'EF-1</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-process">⚙️ Contrôle Quota (92%)</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div '
                                                           'class="wf-progress-container"><div class="wf-progress-bar" '
                                                           'style="width: 92%;"></div></div>\n'
                                                           '                      <div class="wf-console-log">\n'
                                                           '                        <code>> [UTF8-ENGINE] Encodage '
                                                           'canonique RFC 3629 calculé : 1 780 octets</code><br>\n'
                                                           '                        <code>> [SILICON-ALLOC] Partition '
                                                           'EF-1 : 1 780 / 1 900 octets (Marge libre : 120 '
                                                           'octets)</code><br>\n'
                                                           '                        <code>> [INTEGRITY] Zéro caractère '
                                                           'UTF-8 malformé détecté</code><br>\n'
                                                           '                        <code>> [VERDICT] Quota validé '
                                                           'pour la gravure sur puce ACOSJ 92 Ko</code>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p4': {   'tabTitle': '4. Écran de Fin ✨',
                                             'phaseTitle': 'Empreinte Optimisée & Quota EF-1 Sécurisé',
                                             'status': 'success',
                                             'caption': 'Le texte est parfaitement dimensionné pour la mémoire '
                                                        'physique de la puce.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Texte Homologué '
                                                           'Silicium</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-success">✨ 1 780 o • Conforme EF-1</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-success-banner">\n'
                                                           '                        <span '
                                                           'class="wf-seal-icon">📜</span>\n'
                                                           '                        <div>\n'
                                                           '                          <strong>Empreinte Textuelle '
                                                           'Validée avec Succès (1 780 octets)</strong>\n'
                                                           '                          <p class="wf-subtext">Plafond 1 '
                                                           "900 octets d'EF-1 respecté • 120 octets de réserve de "
                                                           'sécurité</p>\n'
                                                           '                        </div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-gold">Insérer dans la Partition Textuelle EF-1 '
                                                           '→</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'}}}},
{   'id': 'UC-118',
    'title': 'Contrôle de Validité NISS Belge (Numéro de Registre National & Algorithme Modulo 97)',
    'cat': 'Identité Civile & Mémorielle',
    'actor': "Conseiller Funéraire & Officier d'État Civil",
    'platforms': ['Web Standard (PWA Hors-Ligne)', 'Natif (iOS & Android)'],
    'tags': ['NISS', 'RegistreNational', 'Modulo97', 'EtatCivil', 'Belgique', 'Contrôle'],
    'preconditions': "Saisie du numéro d'identification du registre national belge (NISS à 11 chiffres) du défunt ou "
                     'mandataire.',
    'flow': [   "Saisie ou numérisation du NISS belge à 11 chiffres (format AAMMJJ-SSS-CC) sur la fiche d'état civil.",
                'Vérification du format structurel : cohérence de la date de naissance et du numéro de suite '
                'journalier.',
                "Exécution de l'algorithme légal Modulo 97 : prise en compte du siècle (addition de 2 000 000 000 pour "
                "les naissances dès l'an 2000).",
                'Comparaison de la clé calculée (97 - reste) avec les deux derniers chiffres de contrôle.',
                "Affichage immédiat de l'exactitude de l'état civil ou alerte immédiate en cas de falsification ou de "
                'faute de frappe.'],
    'postconditions': 'Le NISS est mathématiquement certifié conforme aux spécifications du Registre national belge.',
    'legal': 'Loi belge du 8 août 1983 organisant un Registre national des personnes physiques & Algorithme officiel '
             'Modulo 97.',
    'legal_url': '#section-legal',
    'wireframe': {   'device': 'tablet',
                     'deviceLabel': "PaxStudio Pro • Contrôle d'État Civil & Clé Modulo 97 du Registre National (NISS)",
                     'formFields': [   {   'label': 'NISS Belge (11 chiffres)',
                                           'name': 'niss_number',
                                           'type': 'text',
                                           'value': '72.05.14-315.89',
                                           'badge': 'Registre National',
                                           'required': True},
                                       {   'label': 'Algorithme de Contrôle Légal',
                                           'name': 'modulo_check_algo',
                                           'type': 'text',
                                           'value': 'Modulo 97 • Reste = 97 - (720514315 % 97) = 89',
                                           'badge': 'Mathématique',
                                           'required': False},
                                       {   'label': 'Données Civiles Déduites',
                                           'name': 'niss_extracted_data',
                                           'type': 'text',
                                           'value': 'Date : 14/05/1972 • Sexe : Masculin (Chiffre de suite 315 impair)',
                                           'badge': 'Extraction Auto',
                                           'required': False},
                                       {   'label': 'Statut Validation État Civil',
                                           'name': 'civil_status_validation',
                                           'type': 'select',
                                           'value': 'CONFORME & CERTIFIÉ REGISTRE NATIONAL',
                                           'badge': 'Loi 08/08/1983',
                                           'required': True}],
                     'actionButtons': [   {   'id': 'btn_validate_niss',
                                              'label': 'Vérifier la Clé Modulo 97',
                                              'role': 'primary',
                                              'state': 'idle',
                                              'icon': '🇧🇪'},
                                          {   'id': 'btn_scan_eid',
                                              'label': 'Scanner Carte eID Belge',
                                              'role': 'secondary',
                                              'state': 'idle',
                                              'icon': '💳'}],
                     'validationMsg': {   'title': 'NISS Belge Authentifié avec Succès (Modulo 97 Conforme)',
                                          'badge': 'Clé 89 Valide',
                                          'detail': "Le numéro d'identification correspond parfaitement à l'algorithme "
                                                    'légal du Registre national des personnes physiques.'},
                     'errorCase': {   'code': 'ERR_INVALID_NISS_CHECKSUM',
                                      'title': 'Échec du Contrôle Modulo 97 du NISS Belge',
                                      'condition': 'La clé de contrôle saisie ne correspond pas au calcul officiel de '
                                                   'division euclidienne par 97.',
                                      'message': "Erreur d'état civil : Discordance sur la clé NISS (clé fournie != 97 "
                                                 "- reste). Risque d'erreur de saisie.",
                                      'remediation': "Vérifier la carte eID belge ou l'extrait d'acte de naissance et "
                                                     'ressaisir les 11 chiffres.'},
                     'phases': {   'p1': {   'tabTitle': '1. Avant Trigger',
                                             'phaseTitle': 'NISS Saisi en Attente de Contrôle Algorithmique',
                                             'caption': "Le conseiller a reporté le NISS de la pièce d'identité. Le "
                                                        'bouton de vérification est prêt.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Registre National '
                                                           'Belge</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-neutral">En Attente de Vérification</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-content-grid">\n'
                                                           '                        <div class="wf-field-group">\n'
                                                           '                          <label class="wf-label">NISS à '
                                                           'Contrôler</label>\n'
                                                           '                          <div '
                                                           'class="wf-input-placeholder">72.05.14-315.89</div>\n'
                                                           '                        </div>\n'
                                                           '                        <div class="wf-field-group">\n'
                                                           '                          <label '
                                                           'class="wf-label">Algorithme Légal</label>\n'
                                                           '                          <div '
                                                           'class="wf-input-placeholder">Modulo 97 (Loi du '
                                                           '08/08/1983)</div>\n'
                                                           '                        </div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-primary">🇧🇪 Vérifier la Clé Modulo 97</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p2': {   'tabTitle': '2. Déclenchement ⚡',
                                             'phaseTitle': 'Déclenchement du Calcul Modulo 97 Bicentenaire',
                                             'triggerName': "Clic sur 'Vérifier la Clé Modulo 97'",
                                             'caption': "Traitement de l'expression mathématique et vérification des "
                                                        'critères de siècle.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Moteur Arithmétique '
                                                           'NISS</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-trigger">⚡ Calcul Modulo 97</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-trigger-card '
                                                           'wf-radar-pulse">\n'
                                                           '                        <div '
                                                           'class="wf-trigger-indicator">✓ Base de calcul : 720514315 '
                                                           '% 97 = 8 ➔ Clé attendue = 97 - 8 = 89</div>\n'
                                                           '                        <div '
                                                           'class="wf-subtext">Correspondance parfaite avec la clé '
                                                           'déclarée (89)</div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-primary wf-pulse-btn">Extraction des données '
                                                           'civiles...</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p3': {   'tabTitle': '3. Traitement ⚙️',
                                             'phaseTitle': 'Validation de Cohérence Date de Naissance & Sexe',
                                             'progress': 98,
                                             'caption': 'Vérification croisée avec la date de naissance déclarée et '
                                                        'cohérence du numéro de série.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Validation État '
                                                           'Civil</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-process">⚙️ Vérification Concordance '
                                                           '(98%)</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div '
                                                           'class="wf-progress-container"><div class="wf-progress-bar" '
                                                           'style="width: 98%;"></div></div>\n'
                                                           '                      <div class="wf-console-log">\n'
                                                           '                        <code>> [NISS-CHECK] Division '
                                                           'euclidienne 720514315 % 97 = 8 : Clé 89 exacte</code><br>\n'
                                                           '                        <code>> [CIVIL-DATE] Date extraite '
                                                           ': 14 mai 1972 (Cohérence calendrier grégorien '
                                                           'validée)</code><br>\n'
                                                           '                        <code>> [CIVIL-GENDER] Numéro de '
                                                           'suite 315 impair : Sexe masculin confirmé</code><br>\n'
                                                           '                        <code>> [REGISTRY-STATUS] '
                                                           'Homologation État Civil Belge accordée</code>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p4': {   'tabTitle': '4. Écran de Fin ✨',
                                             'phaseTitle': 'NISS Homologué & Identité Civile Certifiée',
                                             'status': 'success',
                                             'caption': "L'identité est mathématiquement vérifiée. Zéro risque "
                                                        "d'erreur d'homonymie ou d'usurpation.",
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • État Civil '
                                                           'Conforme</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-success">✨ NISS Certifié Modulo 97</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-success-banner">\n'
                                                           '                        <span '
                                                           'class="wf-seal-icon">🇧🇪</span>\n'
                                                           '                        <div>\n'
                                                           '                          <strong>Numéro de Registre '
                                                           'National Validé (72.05.14-315.89)</strong>\n'
                                                           '                          <p class="wf-subtext">Clé 89 '
                                                           "certifiée conforme • Données d'état civil scellées dans le "
                                                           'projet</p>\n'
                                                           '                        </div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-gold">Enregistrer l\'Identité Civile & Continuer '
                                                           '→</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'}}}},
{   'id': 'UC-119',
    'title': 'Recherche & Autocomplétion Référentiel Communes / Codes Postaux Belges (Base INS/NIS Statbel)',
    'cat': 'Identité Civile & Mémorielle',
    'actor': 'Conseiller Funéraire & Famille',
    'platforms': ['Web Standard (PWA Hors-Ligne)', 'Natif (iOS & Android)'],
    'tags': ['Statbel', 'CodePostal', 'CommunesBelges', 'INS', 'Autocompletion', 'Localisation'],
    'preconditions': 'Saisie de la commune de décès, de cérémonie funéraire ou de concession de sépulture.',
    'flow': [   "Saisie prédictive des premiers caractères du toponyme ou du code postal belge (ex: '7000' ou 'Mons').",
                'Interrogation de la base de données embarquée Statbel (Office belge de statistique) fonctionnant 100% '
                'hors-ligne.',
                'Affichage instantané des suggestions normalisées avec code INS officiel (ex: 53053 pour Mons, 21004 '
                'pour Bruxelles).',
                "Sélection de l'entité : renseignement automatique de la province, région linguistique et "
                'arrondissement administratif.',
                'Association pérenne du code INS dans les actes de transport et de déclaration de '
                'crémation/sarcomusation.'],
    'postconditions': 'La commune et le code postal sont rigoureusement indexés sur la nomenclature officielle '
                      'Statbel.',
    'legal': 'Arrêté royal fixant la nomenclature officielle des communes et arrondissements belges (Base INS '
             'Statbel).',
    'legal_url': '#section-legal',
    'wireframe': {   'device': 'tablet',
                     'deviceLabel': 'PaxStudio Pro • Référentiel Géographique Belge Statbel (Codes INS & Postaux)',
                     'formFields': [   {   'label': 'Recherche Commune ou Code Postal',
                                           'name': 'search_postal_commune',
                                           'type': 'text',
                                           'value': '7000 Mons',
                                           'badge': 'Recherche Statbel',
                                           'required': True},
                                       {   'label': 'Code INS Statbel Associé',
                                           'name': 'ins_statbel_code',
                                           'type': 'text',
                                           'value': '53053 (Ville de Mons)',
                                           'badge': 'Officiel INS',
                                           'required': False},
                                       {   'label': 'Province & Arrondissement',
                                           'name': 'administrative_region',
                                           'type': 'text',
                                           'value': 'Province de Hainaut • Arrondissement de Mons • Wallonie',
                                           'badge': 'Région',
                                           'required': False},
                                       {   'label': 'Législation Funéraire Applicable',
                                           'name': 'regional_funeral_law',
                                           'type': 'select',
                                           'value': 'Décret funéraire wallon du 6 mars 2009 (Région Wallonne)',
                                           'badge': 'Droit Régional',
                                           'required': True}],
                     'actionButtons': [   {   'id': 'btn_confirm_commune',
                                              'label': 'Valider la Commune INS',
                                              'role': 'primary',
                                              'state': 'idle',
                                              'icon': '🏛️'},
                                          {   'id': 'btn_show_cemetery_map',
                                              'label': 'Consulter Registre Cimetières',
                                              'role': 'secondary',
                                              'state': 'idle',
                                              'icon': '🗺️'}],
                     'validationMsg': {   'title': 'Commune Belge et Code INS 53053 Validés',
                                          'badge': 'Statbel Conforme',
                                          'detail': 'Commune rattachée avec précision. Les formulaires légaux '
                                                    'appliquent automatiquement le droit funéraire régional.'},
                     'errorCase': {   'code': 'ERR_COMMUNE_NOT_FOUND_STATBEL',
                                      'title': 'Code Postal ou Entité Inconnue dans le Référentiel Statbel',
                                      'condition': "Saisie d'un code postal invalide ou toponyme introuvable dans la "
                                                   'table des unités administratives belges.',
                                      'message': "Anomalie d'adressage : La commune renseignée ne correspond à aucun "
                                                 'code INS officiel belge.',
                                      'remediation': 'Sélectionner la commune via la recherche assistée ou vérifier '
                                                     "l'orthographe du toponyme."},
                     'phases': {   'p1': {   'tabTitle': '1. Avant Trigger',
                                             'phaseTitle': 'Saisie Prédictive de la Commune ou Code Postal',
                                             'caption': "L'utilisateur tape les premiers chiffres ou lettres pour "
                                                        'déclencher la recherche dans la base Statbel.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Référentiel '
                                                           'Statbel</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-neutral">Saisie Assistée</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-content-grid">\n'
                                                           '                        <div class="wf-field-group">\n'
                                                           '                          <label '
                                                           'class="wf-label">Recherche Toponymique</label>\n'
                                                           '                          <div '
                                                           'class="wf-input-placeholder">7000 Mons...</div>\n'
                                                           '                        </div>\n'
                                                           '                        <div class="wf-field-group">\n'
                                                           '                          <label class="wf-label">Base '
                                                           'Embarquée</label>\n'
                                                           '                          <div '
                                                           'class="wf-input-placeholder">Statbel 2026 (581 Communes '
                                                           'Belges Hors-Ligne)</div>\n'
                                                           '                        </div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-primary">🏛️ Valider la Commune INS</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p2': {   'tabTitle': '2. Déclenchement ⚡',
                                             'phaseTitle': 'Interrogation Locale de la Base INS Statbel',
                                             'triggerName': "Sélection de la suggestion '7000 Mons (Code INS 53053)'",
                                             'caption': "Résolution des métadonnées régionales, de l'arrondissement "
                                                        'judiciaire et du décret applicable.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Moteur Géographique '
                                                           'Statbel</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-trigger">⚡ Correspondance Trouvée</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-trigger-card '
                                                           'wf-radar-pulse">\n'
                                                           '                        <div '
                                                           'class="wf-trigger-indicator">✓ Entité identifiée : Ville '
                                                           'de Mons • Code INS 53053</div>\n'
                                                           '                        <div class="wf-subtext">Région '
                                                           'Wallonne • Province de Hainaut • Décret funéraire wallon '
                                                           'du 06/03/2009</div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-primary wf-pulse-btn">Liaison administrative en '
                                                           'cours...</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p3': {   'tabTitle': '3. Traitement ⚙️',
                                             'phaseTitle': 'Injection des Coordonnées Officielles dans les Actes',
                                             'progress': 95,
                                             'caption': 'Mise à jour automatique des formulaires de transport de corps '
                                                        'et des déclarations communales.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Gestionnaire '
                                                           'Administratif</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-process">⚙️ Injection INS (95%)</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div '
                                                           'class="wf-progress-container"><div class="wf-progress-bar" '
                                                           'style="width: 95%;"></div></div>\n'
                                                           '                      <div class="wf-console-log">\n'
                                                           '                        <code>> [STATBEL-DB] Code postal '
                                                           '7000 lié au code INS 53053 (Mons)</code><br>\n'
                                                           '                        <code>> [JURISDICTION] '
                                                           'Arrondissement judiciaire de Mons validé</code><br>\n'
                                                           '                        <code>> [REGIONAL-LAW] Paramétrage '
                                                           "des délais légaux d'inhumation (Décret Wallonie) : "
                                                           'OK</code><br>\n'
                                                           '                        <code>> [GEO-TAG] Coordonnées '
                                                           'centroïde communal rattachées pour traçabilité</code>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p4': {   'tabTitle': '4. Écran de Fin ✨',
                                             'phaseTitle': 'Commune Rattachée & Législation Régionale Associée',
                                             'status': 'success',
                                             'caption': 'Lieu de repos rattaché à la base officielle Statbel sans '
                                                        'aucune ambiguïté géographique.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Localisation '
                                                           'Validée</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-success">✨ Code INS 53053 Scellé</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-success-banner">\n'
                                                           '                        <span '
                                                           'class="wf-seal-icon">🏛️</span>\n'
                                                           '                        <div>\n'
                                                           '                          <strong>Ville de Mons (7000) • '
                                                           'Référentiel Statbel Validé</strong>\n'
                                                           '                          <p class="wf-subtext">Code INS '
                                                           '53053 • Décret funéraire wallon activé pour les '
                                                           'formalités</p>\n'
                                                           '                        </div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-gold">Passer au Choix de la Sépulture / Concession '
                                                           '→</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'}}}},
{   'id': 'UC-120',
    'title': 'Interrogation Taxonomique NCBI Locale (TaxID & Espèces Compagnon 9615, 9685, 9796)',
    'cat': 'Identité Civile & Mémorielle',
    'actor': "Conseiller Animalier & Propriétaire de l'Animal",
    'platforms': ['Web Standard (PWA Hors-Ligne)', 'Natif (iOS & Android)'],
    'tags': ['NCBI', 'TaxID', 'Taxonomie', 'AnimauxCompagnie', 'CanisLupus', 'FelisCatus', 'EquusCaballus'],
    'preconditions': "Création d'un dossier Sanctuaire mémoriel pour un animal familier de compagnie (canin, félin, "
                     'équin).',
    'flow': [   "Sélection de l'espèce animale ou recherche par dénomination vernaculaire dans le module mémoriel "
                'animalier.',
                'Résolution locale instantanée du taxon dans la base embarquée NCBI Taxonomy (sans appel réseau).',
                'Association stricte du TaxID : Canis lupus familiaris (9615), Felis catus (9685), Equus caballus '
                '(9796).',
                "Vérification croisée avec le numéro de transpondeur RFID (ISO 11784/11785) et l'organisme "
                "d'identification (DogID / CatID).",
                "Scellement du TaxID dans la structure de données pour verrouiller l'orientation sanitaire Catégorie 1 "
                'mémorielle.'],
    'postconditions': "Le TaxID NCBI officiel est scellé dans l'en-tête de la capsule, garantissant le respect strict "
                      'de la filière sanitaire.',
    'legal': 'Base taxonomique NCBI Taxonomy & Règlement (CE) n° 1069/2009 établissant des règles sanitaires '
             'applicables aux sous-produits animaux.',
    'legal_url': '#section-legal',
    'wireframe': {   'device': 'tablet',
                     'deviceLabel': 'PaxStudio Pro • Référentiel Taxonomique NCBI & Registre Animalier (ISO 11784)',
                     'formFields': [   {   'label': "Nom Vernaculaire de l'Espèce",
                                           'name': 'vernacular_species',
                                           'type': 'select',
                                           'value': 'Chien domestique (Canis lupus familiaris)',
                                           'badge': 'Animal Familier',
                                           'required': True},
                                       {   'label': 'Identifiant Taxonomique NCBI',
                                           'name': 'ncbi_taxid_resolved',
                                           'type': 'text',
                                           'value': 'TaxID: 9615 (NCBI Reference Taxonomy)',
                                           'badge': 'Souverain NCBI',
                                           'required': False},
                                       {   'label': 'Puce Électronique RFID Vétérinaire',
                                           'name': 'vet_rfid_chip',
                                           'type': 'text',
                                           'value': '967000010294812 (ISO 11784/11785 • Registre DogID)',
                                           'badge': 'Transpondeur',
                                           'required': True},
                                       {   'label': 'Classification Sous-Produit Animal',
                                           'name': 'animal_byproduct_cat',
                                           'type': 'text',
                                           'value': 'Catégorie 1 Mémoriel Pur • Sarcomusation Homologuée',
                                           'badge': 'CE 1069/2009',
                                           'required': False}],
                     'actionButtons': [   {   'id': 'btn_lock_taxid',
                                              'label': 'Verrouiller TaxID & Filière Sanitaire',
                                              'role': 'primary',
                                              'state': 'idle',
                                              'icon': '🧬'},
                                          {   'id': 'btn_lookup_dogid',
                                              'label': 'Interroger Base DogID / CatID',
                                              'role': 'secondary',
                                              'state': 'idle',
                                              'icon': '🔍'}],
                     'validationMsg': {   'title': 'TaxID NCBI 9615 Résolu & Filière Mémorielle Verrouillée',
                                          'badge': 'Canis lupus familiaris',
                                          'detail': 'Classification biologique officielle verrouillée. Orientation '
                                                    "Catégorie 1 validée sans risque de conflit d'espèce."},
                     'errorCase': {   'code': 'ERR_UNKNOWN_TAXID_SPECIES',
                                      'title': 'Espèce Non Identifiée ou Hors Cadre Mémoriel Autorisé',
                                      'condition': "L'animal saisi ne correspond à aucun TaxID homologué pour la "
                                                   'filière mémorielle de compagnie.',
                                      'message': "Erreur de filière : L'espèce saisie ne peut être admise en "
                                                 'sarcomusation de compagnie mémorielle.',
                                      'remediation': 'Sélectionner une espèce autorisée (TaxID 9615, 9685, 9796) ou '
                                                     'orienter vers la filière agricole Catégorie 2.'},
                     'phases': {   'p1': {   'tabTitle': '1. Avant Trigger',
                                             'phaseTitle': "Sélection de l'Espèce de l'Animal Familier",
                                             'caption': "Le conseiller sélectionne la race et l'espèce pour "
                                                        'rattachement au référentiel NCBI.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Mémorial '
                                                           'Animalier</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-neutral">En Attente de Taxonomie</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-content-grid">\n'
                                                           '                        <div class="wf-field-group">\n'
                                                           '                          <label class="wf-label">Espèce / '
                                                           'Animal Familier</label>\n'
                                                           '                          <div '
                                                           'class="wf-input-placeholder">Chien domestique (Canis lupus '
                                                           'familiaris)</div>\n'
                                                           '                        </div>\n'
                                                           '                        <div class="wf-field-group">\n'
                                                           '                          <label class="wf-label">Puce '
                                                           'Transpondeur ISO 11784</label>\n'
                                                           '                          <div '
                                                           'class="wf-input-placeholder">967000010294812 '
                                                           '(DogID)</div>\n'
                                                           '                        </div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-primary">🧬 Verrouiller TaxID & Filière '
                                                           'Sanitaire</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p2': {   'tabTitle': '2. Déclenchement ⚡',
                                             'phaseTitle': 'Résolution Déterministe dans le Référentiel NCBI',
                                             'triggerName': "Clic sur 'Verrouiller TaxID & Filière Sanitaire'",
                                             'caption': "Recherche dans l'index taxonomique local et contrôle des "
                                                        "règles d'orientation vétérinaire CE 1069/2009.",
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Index Taxonomique '
                                                           'NCBI</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-trigger">⚡ Taxon Résolu (9615)</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-trigger-card '
                                                           'wf-radar-pulse">\n'
                                                           '                        <div '
                                                           'class="wf-trigger-indicator">✓ TaxID 9615 résolu : '
                                                           'Eukaryota > Metazoa > Carnivora > Canis lupus '
                                                           'familiaris</div>\n'
                                                           '                        <div '
                                                           'class="wf-subtext">Orientation sanitaire : Catégorie 1 '
                                                           'Mémoriel Pur • Règle Anti-Prion respectée</div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-primary wf-pulse-btn">Scellement de la filière '
                                                           'sanitaire...</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p3': {   'tabTitle': '3. Traitement ⚙️',
                                             'phaseTitle': 'Contrôle de Traçabilité Sanitaire & Règle Anti-Prion',
                                             'progress': 94,
                                             'caption': "Vérification qu'aucun recyclage d'espèce n'est techniquement "
                                                        'possible et scellement du TaxID.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Contrôle Biologique & '
                                                           'Sanitaire</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-process">⚙️ Contrôle Filière (94%)</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div '
                                                           'class="wf-progress-container"><div class="wf-progress-bar" '
                                                           'style="width: 94%;"></div></div>\n'
                                                           '                      <div class="wf-console-log">\n'
                                                           '                        <code>> [NCBI-TAXONOMY] TaxID 9615 '
                                                           'validé avec rang espèce exact</code><br>\n'
                                                           '                        <code>> [ANTI-PRION-RULE] '
                                                           'Verrouillage strict : Exclusion de tout débouché '
                                                           'alimentaire</code><br>\n'
                                                           '                        <code>> [CE-1069/2009] Attribution '
                                                           'filière Catégorie 1 Mémoriel Familier : OK</code><br>\n'
                                                           '                        <code>> [TRANSPONDER] Puce '
                                                           '967000010294812 liée de façon irrévocable au TaxID '
                                                           '9615</code>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p4': {   'tabTitle': '4. Écran de Fin ✨',
                                             'phaseTitle': 'Espèce Verrouillée en Filière Mémorielle Pure',
                                             'status': 'success',
                                             'caption': "L'animal est inscrit avec sa traçabilité biologique complète "
                                                        'et inaltérable.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Mémorial Animalier '
                                                           'Homologué</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-success">✨ TaxID 9615 Scellé</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-success-banner">\n'
                                                           '                        <span '
                                                           'class="wf-seal-icon">🐾</span>\n'
                                                           '                        <div>\n'
                                                           '                          <strong>Canis lupus familiaris '
                                                           '(TaxID 9615) • Filière Cat 1 Validée</strong>\n'
                                                           '                          <p class="wf-subtext">Puce DogID '
                                                           '967000010294812 rattachée • Conformité sanitaire '
                                                           'européenne scellée</p>\n'
                                                           '                        </div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-gold">Créer la Carte Sanctuaire Animalière '
                                                           '→</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'}}}},
{   'id': 'UC-121',
    'title': "Contrôle d'Accessibilité & Contraste WCAG AAA Or/Obsidienne avant Gravure",
    'cat': 'Design & Esthétique',
    'actor': 'Graphiste & Contrôleur Qualité PaxStudio',
    'platforms': ['Web Standard (PWA Hors-Ligne)', 'Natif (iOS & Android)'],
    'tags': ['Accessibilité', 'WCAG21', 'ContrasteAAA', 'Ratio7:1', 'OrObsidienne', 'GravureLaser'],
    'preconditions': 'Composition visuelle de la carte physique ou du médaillon avec choix de la typographie et des '
                     'teintes métalliques.',
    'flow': [   "Positionnement des textes d'épitaphe et patronymes sur le fond noble (fond obsidienne satiné ou "
                'titane brossé).',
                'Le moteur graphique calcule la luminance relative des couleurs de premier plan (or satiné #D4AF37) et '
                "d'arrière-plan (#0B0F19).",
                "Application de l'algorithme WCAG 2.1 pour déterminer le ratio de contraste photométrique exact.",
                "Vérification du seuil d'excellence niveau AAA : ratio supérieur ou égal à 7.0:1 pour les textes "
                'courants et 4.5:1 pour les grands titres.',
                'Validation du gabarit pour la gravure laser sans éblouissement et avec lisibilité garantie sous tous '
                'les angles de lumière.'],
    'postconditions': 'Le contraste chromatique est certifié WCAG 2.1 AAA, garantissant une lisibilité intemporelle '
                      'sur le support physique.',
    'legal': 'Recommandations internationales W3C WCAG 2.1 (Critère 1.4.6 Contraste Amélioré AAA) & Norme ergonomique '
             'ISO 9241-303.',
    'legal_url': '#section-legal',
    'wireframe': {   'device': 'tablet',
                     'deviceLabel': "PaxStudio Pro • Contrôle Optique d'Accessibilité WCAG 2.1 AAA & Gravure Laser",
                     'formFields': [   {   'label': 'Couleur Texte / Gravure Laser',
                                           'name': 'fg_color_hex',
                                           'type': 'text',
                                           'value': '#D4AF37 (Or Satiné Micro-Brossé)',
                                           'badge': 'Premier Plan',
                                           'required': True},
                                       {   'label': 'Fond du Support Physique',
                                           'name': 'bg_color_hex',
                                           'type': 'text',
                                           'value': '#0B0F19 (Noir Obsidienne Titane)',
                                           'badge': 'Arrière-Plan',
                                           'required': True},
                                       {   'label': 'Ratio de Contraste Mesuré',
                                           'name': 'contrast_measured_ratio',
                                           'type': 'text',
                                           'value': '8.24 : 1 (Exigence AAA : ≥ 7.00 : 1)',
                                           'badge': 'Optique W3C',
                                           'required': False},
                                       {   'label': 'Niveau de Conformité WCAG',
                                           'name': 'wcag_compliance_badge',
                                           'type': 'select',
                                           'value': 'NIVEAU AAA CERTIFIÉ (LISIBILITÉ MAXIMALE)',
                                           'badge': 'WCAG 2.1 AAA',
                                           'required': True}],
                     'actionButtons': [   {   'id': 'btn_audit_contrast',
                                              'label': 'Auditer le Contraste Optique',
                                              'role': 'primary',
                                              'state': 'idle',
                                              'icon': '👁️'},
                                          {   'id': 'btn_optimize_palette',
                                              'label': 'Ajuster Teinte Laser Auto',
                                              'role': 'secondary',
                                              'state': 'idle',
                                              'icon': '✨'}],
                     'validationMsg': {   'title': 'Contraste Photométrique Certifié WCAG 2.1 Niveau AAA (8.24:1)',
                                          'badge': 'WCAG AAA 8.24:1',
                                          'detail': 'Lisibilité parfaite sous lumière directe et rasante. Gravure '
                                                    'laser autorisée sur support or et obsidienne.'},
                     'errorCase': {   'code': 'ERR_INSUFFICIENT_CONTRAST_RATIO',
                                      'title': 'Contraste Insuffisant pour Gravure Noble (< 7.0:1)',
                                      'condition': 'La nuance de dorure choisie sur fond clair présente un ratio '
                                                   "inférieur au standard d'excellence AAA (ex: 3.4:1).",
                                      'message': "Défaut d'accessibilité visuelle : Le ratio mesuré (3.4:1) rendra le "
                                                 "texte difficilement déchiffrable avec l'âge.",
                                      'remediation': 'Assombrir le support ou intensifier la densité de la dorure '
                                                     'laser pour atteindre le seuil minimal de 7.0:1.'},
                     'phases': {   'p1': {   'tabTitle': '1. Avant Trigger',
                                             'phaseTitle': 'Maquette Graphique avec Palette Or Satiné / Obsidienne',
                                             'caption': "La palette de couleurs nobles est positionnée. L'audit "
                                                        "d'accessibilité est prêt à être lancé.",
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Laboratoire '
                                                           'Chromatique</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-neutral">Audit Prêt</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-content-grid">\n'
                                                           '                        <div class="wf-field-group">\n'
                                                           '                          <label class="wf-label">Premier '
                                                           'Plan (Laser)</label>\n'
                                                           '                          <div '
                                                           'class="wf-input-placeholder" style="color: '
                                                           '#d4af37;">#D4AF37 Or Satiné</div>\n'
                                                           '                        </div>\n'
                                                           '                        <div class="wf-field-group">\n'
                                                           '                          <label class="wf-label">Fond '
                                                           'Physique</label>\n'
                                                           '                          <div '
                                                           'class="wf-input-placeholder">#0B0F19 Obsidienne '
                                                           'Profonde</div>\n'
                                                           '                        </div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-primary">👁️ Auditer le Contraste Optique</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p2': {   'tabTitle': '2. Déclenchement ⚡',
                                             'phaseTitle': 'Mesure Photométrique de Luminance Relative WCAG 2.1',
                                             'triggerName': "Clic sur 'Auditer le Contraste Optique'",
                                             'caption': 'Calcul des luminances relatives normalisées L1 et L2 selon la '
                                                        'recommandation W3C.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Calculateur '
                                                           'Photométrique</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-trigger">⚡ Mesure W3C Active</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-trigger-card '
                                                           'wf-radar-pulse">\n'
                                                           '                        <div '
                                                           'class="wf-trigger-indicator">✓ Ratio calculé : (L1 + 0.05) '
                                                           '/ (L2 + 0.05) = 8.24 : 1</div>\n'
                                                           '                        <div class="wf-subtext">Seuil AAA '
                                                           'requis (7.00:1) largement dépassé • Rendu optique noble '
                                                           'garanti</div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-primary wf-pulse-btn">Simulation optique sous '
                                                           'lumière rasante...</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p3': {   'tabTitle': '3. Traitement ⚙️',
                                             'phaseTitle': 'Contrôle des Angles de Vision & Réflexion Métallique',
                                             'progress': 96,
                                             'caption': 'Simulation de la gravure laser sous éclairage oblique et '
                                                        "vérification d'absence de reflets éblouissants.",
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Simulateur Optique '
                                                           'Laser</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-process">⚙️ Contrôle ISO 9241 (96%)</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div '
                                                           'class="wf-progress-container"><div class="wf-progress-bar" '
                                                           'style="width: 96%;"></div></div>\n'
                                                           '                      <div class="wf-console-log">\n'
                                                           '                        <code>> [WCAG-CALC] Luminance '
                                                           'relative premier plan : 0.441 • Arrière-plan : '
                                                           '0.009</code><br>\n'
                                                           '                        <code>> [CONTRAST-RATIO] 8.24 : 1 '
                                                           '(Exigence WCAG 2.1 AAA respectée avec 17.7% de '
                                                           'marge)</code><br>\n'
                                                           '                        <code>> [ISO-9241-303] Lisibilité '
                                                           "sous angle d'incidence 45° : Conforme</code><br>\n"
                                                           '                        <code>> [LASER-SPEC] Puissance '
                                                           'recommandée : 28W fibre laser • Focale 160mm</code>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p4': {   'tabTitle': '4. Écran de Fin ✨',
                                             'phaseTitle': 'Contraste Optique Certifié AAA pour Gravure Noble',
                                             'status': 'success',
                                             'caption': 'La carte est garantie parfaitement lisible par tous, sans '
                                                        'fatigue visuelle ni perte de contraste.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Accessibilité '
                                                           'Validée</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-success">✨ Ratio 8.24:1 WCAG AAA</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-success-banner">\n'
                                                           '                        <span '
                                                           'class="wf-seal-icon">🏆</span>\n'
                                                           '                        <div>\n'
                                                           '                          <strong>Contraste Certifié '
                                                           'Niveau AAA (Or Satiné / Obsidienne)</strong>\n'
                                                           '                          <p class="wf-subtext">Lisibilité '
                                                           'intergénérationnelle garantie • Gabarit prêt pour la '
                                                           'gravure laser</p>\n'
                                                           '                        </div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-gold">Valider le Gabarit Visuel & Continuer '
                                                           '→</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'}}}},
{   'id': 'UC-122',
    'title': 'Débruitage & Élimination Automatique des Silences Audio Waveform (< 46 080 o)',
    'cat': 'Médias Sonores',
    'actor': 'Famille & Ingénieur du Son PaxStudio',
    'platforms': ['Web Standard (PWA Hors-Ligne)', 'Natif (iOS & Android)'],
    'tags': ['Audio', 'VAD', 'Debruitage', 'Silences', 'Opus', 'EF-3', 'Plafond46Ko'],
    'preconditions': "Importation d'un hommage vocal ou d'un mémo audio familial contenant des souffles ou des "
                     'silences prolongés.',
    'flow': [   "Génération de la forme d'onde (waveform) sonore et analyse de l'enveloppe d'énergie acoustique.",
                'Exécution du module Voice Activity Detection (VAD) avec détection et suppression des plages de '
                'silence initiales et finales.',
                "Application d'un algorithme de débruitage par soustraction spectrale pour filtrer le bruit de fond "
                'microphonique.',
                'Recompression intelligente en flux Opus SILK 12 kbps mono adapté aux contraintes de la puce silicium.',
                "Contrôle strict que le volume sonore final n'excède pas les 46 080 octets disponibles dans la "
                'partition EF-3.'],
    'postconditions': "L'onde audio est nettoyée, la voix est intelligible et le volume final respecte rigoureusement "
                      'le quota EF-3.',
    'legal': "Recommandation UIT-T G.729 (Détection d'activité vocale) & Spécification silicium AeterniTrak EF-3 (46 "
             '080 octets).',
    'legal_url': '#section-legal',
    'wireframe': {   'device': 'tablet',
                     'deviceLabel': 'PaxStudio Pro • Traitement Acoustique & Élagage des Silences (Partition EF-3)',
                     'formFields': [   {   'label': 'Fichier Audio Importé',
                                           'name': 'raw_audio_track',
                                           'type': 'text',
                                           'value': 'hommage_vocal_papa_2024.wav (01:12 • 4.2 Mo)',
                                           'badge': 'Source Brute',
                                           'required': True},
                                       {   'label': "Détection d'Activité Vocale (VAD)",
                                           'name': 'vad_silence_stripping',
                                           'type': 'text',
                                           'value': '24 secondes de silences et bruits blancs éliminés',
                                           'badge': 'Gain Audio',
                                           'required': False},
                                       {   'label': 'Débruitage Spectral Adaptatif',
                                           'name': 'spectral_denoise_profile',
                                           'type': 'select',
                                           'value': 'Atténuation Souffle Micro -14 dB (Spectre Vocal Préservé)',
                                           'badge': 'UIT-T G.729',
                                           'required': True},
                                       {   'label': 'Taille Finale Encodée EF-3',
                                           'name': 'ef3_final_encoded_size',
                                           'type': 'text',
                                           'value': '38 912 octets / 46 080 octets (84.4% de la partition)',
                                           'badge': 'Quota Respecté',
                                           'required': False}],
                     'actionButtons': [   {   'id': 'btn_strip_and_denoise',
                                              'label': 'Éliminer Silences & Débruiter',
                                              'role': 'primary',
                                              'state': 'idle',
                                              'icon': '🎙️'},
                                          {   'id': 'btn_listen_ab_test',
                                              'label': 'Écouter le Rendu Nettoyé',
                                              'role': 'secondary',
                                              'state': 'idle',
                                              'icon': '▶️'}],
                     'validationMsg': {   'title': 'Audio Nettoyé avec Succès & Intégré sous Quota EF-3',
                                          'badge': '38.9 Ko / 46 Ko Conforme',
                                          'detail': 'Voix limpide, silences éliminés, gain de 24 secondes. Fichier '
                                                    'scellé pour écriture dans la partition sonore EF-3.'},
                     'errorCase': {   'code': 'WARN_AUDIO_SN_RATIO_TOO_LOW',
                                      'title': 'Rapport Signal sur Bruit Vocal Insuffisant (< 6 dB)',
                                      'condition': "L'enregistrement présente un niveau de bruit parasite trop élevé "
                                                   'empêchant une restitution vocale digne.',
                                      'message': 'Avertissement acoustique : La voix est couverte par un bruit de fond '
                                                 'mécanique ou éolien important.',
                                      'remediation': 'Activer le filtre passe-bande vocal renforcé (300-3400 Hz) ou '
                                                     'enregistrer un message dans un lieu calme.'},
                     'phases': {   'p1': {   'tabTitle': '1. Avant Trigger',
                                             'phaseTitle': 'Piste Audio Brute avec Souffle et Plages de Silence',
                                             'caption': "L'hommage vocal importé dure 72 secondes avec 24 secondes de "
                                                        'silences et bruits de fond.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Studio '
                                                           'Acoustique</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-neutral">Audio Brut (72s • Souffle '
                                                           'Détecté)</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-content-grid">\n'
                                                           '                        <div class="wf-field-group">\n'
                                                           '                          <label '
                                                           'class="wf-label">Enregistrement Source</label>\n'
                                                           '                          <div '
                                                           'class="wf-input-placeholder">hommage_vocal_papa_2024.wav '
                                                           '(01:12)</div>\n'
                                                           '                        </div>\n'
                                                           '                        <div class="wf-field-group">\n'
                                                           '                          <label class="wf-label">Cible '
                                                           'Silicium EF-3</label>\n'
                                                           '                          <div '
                                                           'class="wf-input-placeholder">Quota strict : 46 080 octets '
                                                           'max</div>\n'
                                                           '                        </div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-primary">🎙️ Éliminer Silences & Débruiter</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p2': {   'tabTitle': '2. Déclenchement ⚡',
                                             'phaseTitle': 'Activation du Module VAD (Voice Activity Detection)',
                                             'triggerName': "Clic sur 'Éliminer Silences & Débruiter'",
                                             'caption': "Détection des plages d'énergie vocale et coupure nette des "
                                                        'silences aux extrémités.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Filtre VAD & '
                                                           'Débruitage</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-trigger">⚡ Traitement Acoustique Actif</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-trigger-card '
                                                           'wf-radar-pulse">\n'
                                                           '                        <div '
                                                           'class="wf-trigger-indicator">✓ 24.2 secondes de silences '
                                                           'élaguées • Souffle micro atténué de -14 dB</div>\n'
                                                           '                        <div class="wf-subtext">Durée '
                                                           'utile ramenée à 48 secondes • Énergie vocale '
                                                           'rehaussée</div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-primary wf-pulse-btn">Re-quantification Opus '
                                                           'SILK...</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p3': {   'tabTitle': '3. Traitement ⚙️',
                                             'phaseTitle': 'Encodage Opus SILK & Validation du Plafond EF-3',
                                             'progress': 94,
                                             'caption': 'Compression dynamique et pesée binaire pour injection dans la '
                                                        'partition silicium EF-3.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Contrôle Silicium '
                                                           'EF-3</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-process">⚙️ Contrôle Quota (94%)</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div '
                                                           'class="wf-progress-container"><div class="wf-progress-bar" '
                                                           'style="width: 94%;"></div></div>\n'
                                                           '                      <div class="wf-console-log">\n'
                                                           '                        <code>> [VAD-ENGINE] Découpage des '
                                                           'silences : Durée 47.8s (Gain de 33% en volume)</code><br>\n'
                                                           '                        <code>> [NOISE-REDUCE] '
                                                           'Soustraction spectrale appliquée sur 3 bandes '
                                                           'critiques</code><br>\n'
                                                           '                        <code>> [OPUS-ENCODE] Flux Opus '
                                                           'SILK 12 kbps généré : 38 912 octets</code><br>\n'
                                                           '                        <code>> [STORAGE-EF3] 38 912 / 46 '
                                                           '080 octets (Marge libre : 7 168 octets) : VALIDÉ</code>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p4': {   'tabTitle': '4. Écran de Fin ✨',
                                             'phaseTitle': 'Flux Vocal Épuré à 38.9 Ko (Plafond EF-3 Respecté)',
                                             'status': 'success',
                                             'caption': "La voix du défunt est immortalisée avec pureté et s'insère "
                                                        'sans contrainte dans la puce.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Voix Éternelle '
                                                           'Scellée</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-success">✨ 38.9 Ko • Conforme EF-3</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-success-banner">\n'
                                                           '                        <span '
                                                           'class="wf-seal-icon">🎵</span>\n'
                                                           '                        <div>\n'
                                                           '                          <strong>Hommage Sonore Haute '
                                                           'Définition Prêt pour Gravure</strong>\n'
                                                           '                          <p class="wf-subtext">38 912 '
                                                           'octets • Silences éliminés • Qualité vocale optimale sur '
                                                           'puce ACOSJ</p>\n'
                                                           '                        </div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-gold">Insérer dans la Partition Sonore EF-3 '
                                                           '→</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'}}}},
{   'id': 'UC-123',
    'title': "Génération & Validation du QR Code Vectoriel de Secours (Correction d'Erreur ECC Niveau M/Q)",
    'cat': 'Validation Finale & Juridique',
    'actor': 'Conseiller Funéraire & Famille',
    'platforms': ['Web Standard (PWA Hors-Ligne)', 'Natif (iOS & Android)'],
    'tags': ['QRCode', 'Secours', 'ECC', 'ReedSolomon', 'ISO18004', 'VectorielSVG', 'Redondance'],
    'preconditions': "Les données récapitulatives et l'URL de vérification sont prêtes pour l'impression physique au "
                     'dos du support.',
    'flow': [   "Extraction de l'adresse de vérification canonique et des identifiants cryptographiques essentiels.",
                'Sélection de la politique de tolérance aux pannes Reed-Solomon : Niveau M (15% de redondance) ou '
                'Niveau Q (25% de tolérance aux rayures).',
                "Génération du maillage vectoriel SVG pur garantissant des arêtes nettes à l'échelle micrométrique "
                'pour la gravure laser.',
                'Application stricte de la zone de silence (quiet zone) de 4 modules conformément à la norme ISO/IEC '
                '18004.',
                'Simulation optique de dégradations mécaniques (rayure, usure de frottement) pour certifier la '
                'lisibilité universelle par smartphone.'],
    'postconditions': 'Le QR code vectoriel est validé avec 25% de redondance matérielle, prêt pour la gravure de '
                      'secours au verso.',
    'legal': "Norme internationale ISO/IEC 18004 (Technologie de l'information - Symbologies de code à barres - QR "
             'Code 2005).',
    'legal_url': '#section-legal',
    'wireframe': {   'device': 'tablet',
                     'deviceLabel': 'PaxStudio Pro • Moteur de Gravure QR Code Vectoriel & Tolérance Reed-Solomon',
                     'formFields': [   {   'label': 'Charge Utile / URL Canonique',
                                           'name': 'qr_target_payload',
                                           'type': 'text',
                                           'value': 'https://aeternitrak.be/v?id=AET-2026-BEL-0912&sig=c4b8... (114 '
                                                    'car.)',
                                           'badge': 'Payload Scellé',
                                           'required': True},
                                       {   'label': "Correction d'Erreur Reed-Solomon",
                                           'name': 'ecc_level_choice',
                                           'type': 'select',
                                           'value': 'Niveau Q (25% de tolérance aux rayures physiques)',
                                           'badge': 'ISO 18004',
                                           'required': True},
                                       {   'label': 'Zone de Quiétude (Quiet Zone)',
                                           'name': 'quiet_zone_spec',
                                           'type': 'text',
                                           'value': '4 modules périphériques respectés au 1/100e mm',
                                           'badge': 'Contrainte Laser',
                                           'required': False},
                                       {   'label': 'Format Vectoriel Exporté',
                                           'name': 'qr_vector_format',
                                           'type': 'text',
                                           'value': 'SVG 100% Vectoriel Pur (Résolution infinie • Zéro artefact)',
                                           'badge': 'HD Gravure',
                                           'required': False}],
                     'actionButtons': [   {   'id': 'btn_generate_vector_qr',
                                              'label': 'Générer le QR Code Vectoriel',
                                              'role': 'primary',
                                              'state': 'idle',
                                              'icon': '🔲'},
                                          {   'id': 'btn_simulate_scratch_test',
                                              'label': 'Simuler Rayure & Test Décodage',
                                              'role': 'secondary',
                                              'state': 'idle',
                                              'icon': '🔬'}],
                     'validationMsg': {   'title': 'QR Code Vectoriel Généré & Tolérance Reed-Solomon Niveau Q '
                                                   'Conforme',
                                          'badge': 'ISO 18004 ECC Q',
                                          'detail': 'Le QR code est lisible même avec 25% de dégradation de surface. '
                                                    'Prêt pour gravure physique au verso.'},
                     'errorCase': {   'code': 'ERR_QR_PAYLOAD_TOO_DENSE',
                                      'title': 'Charge Utile Trop Volumineuse pour la Surface Laser Disponible',
                                      'condition': 'La longueur du texte encodé dépasse la résolution optique gravable '
                                                   'sur médaillon de 35 mm.',
                                      'message': 'Risque de non-lecture : La densité de modules dépasse les capacités '
                                                 'de résolution optique du laser.',
                                      'remediation': "Compresser l'URL ou substituer la charge utile brute par un "
                                                     'identifiant court sécurisé.'},
                     'phases': {   'p1': {   'tabTitle': '1. Avant Trigger',
                                             'phaseTitle': 'Configuration de la Redondance Optique de Secours',
                                             'caption': 'Sélection du niveau de tolérance Reed-Solomon pour le QR code '
                                                        'gravé au dos de la carte.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Secours Optique '
                                                           'QR</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-neutral">En Attente de Génération</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-content-grid">\n'
                                                           '                        <div class="wf-field-group">\n'
                                                           '                          <label class="wf-label">Charge '
                                                           'Utile Canonique</label>\n'
                                                           '                          <div '
                                                           'class="wf-input-placeholder">https://aeternitrak.be/v?id=AET-2026-BEL-0912</div>\n'
                                                           '                        </div>\n'
                                                           '                        <div class="wf-field-group">\n'
                                                           '                          <label class="wf-label">Niveau '
                                                           'Reed-Solomon</label>\n'
                                                           '                          <div '
                                                           'class="wf-input-placeholder">Niveau Q (25% Tolérance '
                                                           'Rayures)</div>\n'
                                                           '                        </div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-primary">🔲 Générer le QR Code Vectoriel</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p2': {   'tabTitle': '2. Déclenchement ⚡',
                                             'phaseTitle': 'Calcul de la Matrice QR Code avec Tolérance Reed-Solomon Q',
                                             'triggerName': "Clic sur 'Générer le QR Code Vectoriel'",
                                             'caption': 'Génération de la matrice de modules binaires et ajout des '
                                                        'blocs de parité Reed-Solomon.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Moteur ISO/IEC '
                                                           '18004</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-trigger">⚡ Matrice Vectorielle Calculée</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-trigger-card '
                                                           'wf-radar-pulse">\n'
                                                           '                        <div '
                                                           'class="wf-trigger-indicator">✓ Matrice Version 4 (33x33 '
                                                           'modules) • Masque optique 101 sélectionné</div>\n'
                                                           '                        <div class="wf-subtext">Ajout de '
                                                           '44 octets de redondance Reed-Solomon (Niveau Q - 25% '
                                                           'récupérable)</div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-primary wf-pulse-btn">Simulation de rayure '
                                                           'laser...</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p3': {   'tabTitle': '3. Traitement ⚙️',
                                             'phaseTitle': 'Vectorisation SVG Submillimétrique & Simulation de Rayure',
                                             'progress': 97,
                                             'caption': 'Vérification de la décodabilité optique avec une simulation '
                                                        "d'abrasion de 22% de la surface.",
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Banc de Résilience '
                                                           'Optique</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-process">⚙️ Test Abrasions (97%)</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div '
                                                           'class="wf-progress-container"><div class="wf-progress-bar" '
                                                           'style="width: 97%;"></div></div>\n'
                                                           '                      <div class="wf-console-log">\n'
                                                           '                        <code>> [QR-ENGINE] Traçage SVG '
                                                           'vectoriel : Coordonnées au 1/100e de '
                                                           'millimètre</code><br>\n'
                                                           '                        <code>> [QUIET-ZONE] Marge '
                                                           'périphérique de 4 modules validée</code><br>\n'
                                                           '                        <code>> [SCRATCH-SIM] Dégradation '
                                                           'simulée : 22% de la surface altérée</code><br>\n'
                                                           '                        <code>> [DECODER-CHECK] Décodage '
                                                           "Reed-Solomon 100% réussi sans perte d'information</code>\n"
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p4': {   'tabTitle': '4. Écran de Fin ✨',
                                             'phaseTitle': 'QR Code de Secours Homologué (25% Tolérance)',
                                             'status': 'success',
                                             'caption': 'La voie optique de secours est certifiée inaltérable et '
                                                        "résistante aux années d'usage.",
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Secours Optique '
                                                           'Validé</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-success">✨ ISO 18004 Niveau Q</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-success-banner">\n'
                                                           '                        <span '
                                                           'class="wf-seal-icon">🔲</span>\n'
                                                           '                        <div>\n'
                                                           '                          <strong>QR Code Vectoriel '
                                                           'Homologué pour Gravure Verso</strong>\n'
                                                           '                          <p class="wf-subtext">Tolérance '
                                                           'Reed-Solomon 25% • Résolution laser vectorielle pure '
                                                           'scellée</p>\n'
                                                           '                        </div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-gold">Intégrer au Verso de la Carte Physique '
                                                           '→</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'}}}},
{   'id': 'UC-124',
    'title': "Simulation Signature Client & Calcul d'Empreinte JCS RFC 8785",
    'cat': 'Validation Finale & Juridique',
    'actor': 'Mandataire Légal & Conseiller Funéraire',
    'platforms': ['Web Standard (PWA Hors-Ligne)', 'Natif (iOS & Android)'],
    'tags': ['JCS', 'RFC8785', 'Canonisation', 'SHA256', 'SignatureTactile', 'eIDAS', 'EF-5'],
    'preconditions': "Toutes les étapes de conception de la carte sont finalisées ; le mandataire s'apprête à valider "
                     'le projet.',
    'flow': [   "Rassemblement de l'arbre complet des métadonnées du projet mémoriel au format JSON structuré.",
                "Exécution de l'algorithme officiel JSON Canonicalization Scheme selon la RFC 8785 (tri déterministe "
                'des clés, standardisation des flottants).',
                "Calcul de l'empreinte binaire SHA-256 du document canonique, produisant un digest invariable de 32 "
                'octets.',
                'Capture sur tablette du tracé de signature biométrique du mandataire légal avec coordonnées '
                'vectorielles et horodatage.',
                "Liaison cryptographique entre le tracé de signature, l'empreinte JCS RFC 8785 et l'enveloppe finale "
                'de la partition EF-5.'],
    'postconditions': "Le document projet dispose d'une forme canonique inviolable et d'un condensat SHA-256 certifié "
                      'eIDAS.',
    'legal': 'Norme RFC 8785 (JSON Canonicalization Scheme - JCS) & Règlement UE 910/2014 (eIDAS - intégrité des actes '
             'dématérialisés).',
    'legal_url': '#section-legal',
    'wireframe': {   'device': 'tablet',
                     'deviceLabel': 'PaxStudio Pro • Canonisation JCS RFC 8785 & Signature Numérique du Mandataire',
                     'formFields': [   {   'label': 'Objet JSON du Projet Funéraire',
                                           'name': 'json_project_structure',
                                           'type': 'text',
                                           'value': 'Structure AeterniCore {v: 1.0, decedent: {...}, directives: '
                                                    '{...}}',
                                           'badge': 'Schéma 1.0',
                                           'required': False},
                                       {   'label': 'Canonisation JCS (RFC 8785)',
                                           'name': 'jcs_canon_status',
                                           'type': 'select',
                                           'value': 'CANONISATION DÉTERMINISTE RFC 8785 VALIDÉE',
                                           'badge': 'RFC 8785',
                                           'required': True},
                                       {   'label': 'Digest SHA-256 Immuable',
                                           'name': 'jcs_sha256_digest',
                                           'type': 'text',
                                           'value': '3f79e2a8c149d56b009e8d4a51e68b3c9420bf824f912e61a84f3c05e1a7b942',
                                           'badge': 'SHA-256 Digest',
                                           'required': False},
                                       {   'label': 'Mandataire Signataire',
                                           'name': 'mandat_signer_identity',
                                           'type': 'text',
                                           'value': 'Mme Sophie Dumont (Ayant Droit • Identité vérifiée eID)',
                                           'badge': 'Signataire',
                                           'required': True}],
                     'actionButtons': [   {   'id': 'btn_canonize_and_hash',
                                              'label': 'Canoniser (RFC 8785) & Calculer SHA-256',
                                              'role': 'primary',
                                              'state': 'idle',
                                              'icon': '🔒'},
                                          {   'id': 'btn_capture_signature_pad',
                                              'label': 'Capturer Signature Tactile',
                                              'role': 'secondary',
                                              'state': 'idle',
                                              'icon': '✍️'}],
                     'validationMsg': {   'title': 'Projet Canonisé selon la RFC 8785 & Empreinte SHA-256 Scellée',
                                          'badge': 'RFC 8785 SHA-256 OK',
                                          'detail': "Forme canonique binaire déterministe générée. L'empreinte SHA-256 "
                                                    'est liée de façon indélébile au tracé de signature.'},
                     'errorCase': {   'code': 'ERR_JCS_CANONICALIZATION_FAILED',
                                      'title': 'Échec de Canonisation JCS ou Clés JSON Dupliquées',
                                      'condition': 'Le document JSON comporte des structures circulaires ou des clés '
                                                   'dupliquées non conformes à la RFC 8785.',
                                      'message': "Erreur de sérialisation : Impossible d'obtenir une empreinte "
                                                 'déterministe sur le document projet.',
                                      'remediation': 'Vérifier la validité syntaxique JSON et éliminer les propriétés '
                                                     'dynamiques non sérialisables.'},
                     'phases': {   'p1': {   'tabTitle': '1. Avant Trigger',
                                             'phaseTitle': 'Dossier Funéraire Complet Prêt pour Canonisation JCS',
                                             'caption': 'Toutes les volontés et données mémorielles sont compilées. Le '
                                                        'scellement cryptographique attend la signature.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Canonisation & '
                                                           'Scellement</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-neutral">En Attente de Signature</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-content-grid">\n'
                                                           '                        <div class="wf-field-group">\n'
                                                           '                          <label class="wf-label">Projet '
                                                           'Mémoriel</label>\n'
                                                           '                          <div '
                                                           'class="wf-input-placeholder">Dossier #BAT-2026-BEL-00412 '
                                                           '(7 Partitions)</div>\n'
                                                           '                        </div>\n'
                                                           '                        <div class="wf-field-group">\n'
                                                           '                          <label class="wf-label">Standard '
                                                           'Cryptographique</label>\n'
                                                           '                          <div '
                                                           'class="wf-input-placeholder">RFC 8785 (JCS) + '
                                                           'SHA-256</div>\n'
                                                           '                        </div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-primary">🔒 Canoniser (RFC 8785) & Calculer '
                                                           'SHA-256</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p2': {   'tabTitle': '2. Déclenchement ⚡',
                                             'phaseTitle': 'Normalisation Binaire RFC 8785 & Capture de Signature',
                                             'triggerName': "Clic sur 'Canoniser (RFC 8785)' et signature sur pad "
                                                            'tactile',
                                             'caption': 'Tri lexicographique des clés en UTF-8 et recueil du tracé '
                                                        'biométrique du mandataire.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Moteur RFC '
                                                           '8785</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-trigger">⚡ Canonisation Déterministe</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-trigger-card '
                                                           'wf-radar-pulse">\n'
                                                           '                        <div '
                                                           'class="wf-trigger-indicator">✓ Canonisation binaire JCS '
                                                           'achevée • Tracé signature capturé (412 points '
                                                           'vectoriels)</div>\n'
                                                           '                        <div class="wf-subtext">Génération '
                                                           "du digest SHA-256 inaltérable à l'octet près</div>\n"
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-primary wf-pulse-btn">Calcul de l\'empreinte de '
                                                           'scellement...</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p3': {   'tabTitle': '3. Traitement ⚙️',
                                             'phaseTitle': "Calcul de l'Empreinte Déterministe SHA-256 du Document JCS",
                                             'progress': 98,
                                             'caption': "Création du jeton probatoire liant l'identité du mandataire à "
                                                        "l'intégrité intégrale du projet.",
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Module '
                                                           'Cryptographique</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-process">⚙️ Scellement Hash (98%)</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div '
                                                           'class="wf-progress-container"><div class="wf-progress-bar" '
                                                           'style="width: 98%;"></div></div>\n'
                                                           '                      <div class="wf-console-log">\n'
                                                           '                        <code>> [JCS-ENGINE] 187 clés JSON '
                                                           'triées selon les points de code Unicode UTF-8</code><br>\n'
                                                           '                        <code>> [SHA256] Empreinte : '
                                                           '3f79e2a8c149d56b009e8d4a51e68b3c9420bf824f912e61a84f3c05e1a7b942</code><br>\n'
                                                           '                        <code>> [SIGNATURE] Liaison '
                                                           'biométrique avec Sophie Dumont (eID certifiée) : '
                                                           'OK</code><br>\n'
                                                           '                        <code>> [COSE-SIGN1] Enveloppe '
                                                           'prête pour injection dans la partition EF-5</code>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p4': {   'tabTitle': '4. Écran de Fin ✨',
                                             'phaseTitle': 'BAT Numérique Canonisé & Empreinte Scellée Définitivement',
                                             'status': 'success',
                                             'caption': 'Le document projet est désormais mathématiquement '
                                                        'inaltérable.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • BAT Scellé</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-success">✨ JCS RFC 8785 Validé</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-success-banner">\n'
                                                           '                        <span '
                                                           'class="wf-seal-icon">📜</span>\n'
                                                           '                        <div>\n'
                                                           '                          <strong>BAT Funéraire Validé & '
                                                           'Scellé par Empreinte SHA-256</strong>\n'
                                                           '                          <p class="wf-subtext">Signature '
                                                           'du mandataire liée au condensat déterministe • Prêt pour '
                                                           'télétransmission atelier</p>\n'
                                                           '                        </div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-gold">Émettre & Télétransmettre le BAT Numérique '
                                                           '→</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'}}}},
{   'id': 'UC-125',
    'title': 'Émission & Télétransmission Sécurisée du BAT Numérique (Horodatage Certifié)',
    'cat': 'Validation Finale & Juridique',
    'actor': 'Conseiller Funéraire & Opérateur PaxStation',
    'platforms': ['Web Standard (PWA Hors-Ligne)', 'Natif (iOS & Android)'],
    'tags': ['BAT', 'Horodatage', 'RFC3161', 'Teletransmission', 'TLS13', 'eIDAS', 'Production'],
    'preconditions': 'Le mandataire a signé le BAT numérique et le hash JCS RFC 8785 a été validé.',
    'flow': [   "Création de la liasse de production numérique scellée contenant l'ensemble des fichiers binaires "
                '(EF-1 à EF-5).',
                "Génération de la requête d'horodatage qualifié RFC 3161 (TSA conforme eIDAS) garantissant la date et "
                "l'heure certaines.",
                "Établissement d'une session de télétransmission hautement sécurisée TLS 1.3 avec authentification "
                "mutuelle (mTLS) vers la PaxStation d'atelier.",
                'Téléversement en flux chiffré AES-256-GCM et vérification du hash de transport par le récepteur '
                "d'atelier.",
                "Réception de l'accusé de production officiel et passage du dossier au statut 'TRANSMIS POUR GRAVURE "
                "SILICIUM'."],
    'postconditions': 'Le dossier complet est transféré avec accusé de réception cryptographique, prêt pour la prise '
                      'en charge par la PaxStation.',
    'legal': 'Règlement UE n° 910/2014 (eIDAS - Services de confiance et horodatage certifié RFC 3161) & Protocole TLS '
             '1.3 (RFC 8446).',
    'legal_url': '#section-legal',
    'wireframe': {   'device': 'tablet',
                     'deviceLabel': 'PaxStudio Pro • Émission du Bon à Tirer (BAT) & Télétransmission Sécurisée '
                                    'Atelier',
                     'formFields': [   {   'label': 'Numéro de Dossier BAT',
                                           'name': 'bat_reference_number',
                                           'type': 'text',
                                           'value': 'BAT-2026-BEL-00412-MÉDAILLON-TITANE',
                                           'badge': 'Référence BAT',
                                           'required': False},
                                       {   'label': "Jeton d'Horodatage Certifié (TSA)",
                                           'name': 'tsa_timestamp_token',
                                           'type': 'text',
                                           'value': 'eIDAS TSA Qualified • 2026-10-05T08:24:12.108Z (RFC 3161)',
                                           'badge': 'Horodatage eIDAS',
                                           'required': True},
                                       {   'label': 'Canal de Télétransmission',
                                           'name': 'transfer_mtls_channel',
                                           'type': 'text',
                                           'value': 'mTLS 1.3 Sécurisé • PaxStation Atelier #01 (IP 192.168.10.42)',
                                           'badge': 'Chiffrement AES',
                                           'required': False},
                                       {   'label': 'Statut de Prise en Charge',
                                           'name': 'transfer_ack_status',
                                           'type': 'select',
                                           'value': 'ACQUITTÉ PAR PAXSTATION (STATUT : PRÊT POUR GRAVURE)',
                                           'badge': '200 OK Reçu',
                                           'required': True}],
                     'actionButtons': [   {   'id': 'btn_transmit_bat_package',
                                              'label': 'Télétransmettre le BAT Numérique',
                                              'role': 'primary',
                                              'state': 'idle',
                                              'icon': '🚀'},
                                          {   'id': 'btn_download_archive_bundle',
                                              'label': "Télécharger l'Archive Sécurisée",
                                              'role': 'secondary',
                                              'state': 'idle',
                                              'icon': '📦'}],
                     'validationMsg': {   'title': 'BAT Numérique Horodaté eIDAS & Transmis avec Succès',
                                          'badge': 'Télétransmission Réussie',
                                          'detail': 'Le dossier de production est acquitté par la PaxStation. Les '
                                                    "jetons d'horodatage RFC 3161 sont archivés."},
                     'errorCase': {   'code': 'ERR_BAT_TRANSMISSION_TIMEOUT',
                                      'title': 'Rupture de Connexion Sécurisée durant la Télétransmission',
                                      'condition': "La station d'atelier PaxStation ne répond pas sur le canal mTLS ou "
                                                   "le certificat d'authentification a expiré.",
                                      'message': 'Échec de télétransmission : Délai dépassé (timeout 15s) lors de '
                                                 "l'envoi de la liasse de production.",
                                      'remediation': "Vérifier que la PaxStation est allumée sur le réseau d'atelier "
                                                     'ou basculer en transfert par média physique sécurisé.'},
                     'phases': {   'p1': {   'tabTitle': '1. Avant Trigger',
                                             'phaseTitle': "Dossier Scellé Prêt pour Transmission Vers l'Atelier",
                                             'caption': "Le BAT est signé. Le paquet de production prêt pour l'envoi "
                                                        'sécurisé à la machine de gravure.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Passerelle '
                                                           'Atelier</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-neutral">Prêt pour Télétransmission</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-content-grid">\n'
                                                           '                        <div class="wf-field-group">\n'
                                                           '                          <label class="wf-label">Liasse '
                                                           'de Production</label>\n'
                                                           '                          <div '
                                                           'class="wf-input-placeholder">BAT-2026-BEL-00412 '
                                                           '(Horodatage eIDAS)</div>\n'
                                                           '                        </div>\n'
                                                           '                        <div class="wf-field-group">\n'
                                                           '                          <label class="wf-label">Cible '
                                                           "d'Atelier</label>\n"
                                                           '                          <div '
                                                           'class="wf-input-placeholder">PaxStation Encodage #01 (mTLS '
                                                           '1.3)</div>\n'
                                                           '                        </div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-primary">🚀 Télétransmettre le BAT '
                                                           'Numérique</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p2': {   'tabTitle': '2. Déclenchement ⚡',
                                             'phaseTitle': "Requête d'Horodatage Certifié eIDAS RFC 3161",
                                             'triggerName': "Clic sur 'Télétransmettre le BAT Numérique'",
                                             'caption': "Appel du tiers d'horodatage qualifié et émission du jeton "
                                                        'cryptographique certifié.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Tiers d\'Horodatage '
                                                           '(TSA)</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-trigger">⚡ Jeton TSA Reçu</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-trigger-card '
                                                           'wf-radar-pulse">\n'
                                                           '                        <div '
                                                           'class="wf-trigger-indicator">✓ Horodatage certifié : '
                                                           '2026-10-05T08:24:12.108Z • Autorité QuoVadis / '
                                                           'Certipost</div>\n'
                                                           '                        <div class="wf-subtext">Ouverture '
                                                           'du tunnel mTLS 1.3 avec la station de gravure '
                                                           "d'atelier</div>\n"
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-primary wf-pulse-btn">Téléversement sécurisé en '
                                                           'cours...</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p3': {   'tabTitle': '3. Traitement ⚙️',
                                             'phaseTitle': 'Tunnel mTLS 1.3 vers PaxStation & Vérification Intégrité',
                                             'progress': 99,
                                             'caption': 'Chiffrement AES-256-GCM, transmission par paquets vérifiés et '
                                                        "contrôle d'empreinte récepteur.",
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Tunnel Sécurisé '
                                                           'Atelier</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-process">⚙️ Transfert mTLS (99%)</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div '
                                                           'class="wf-progress-container"><div class="wf-progress-bar" '
                                                           'style="width: 99%;"></div></div>\n'
                                                           '                      <div class="wf-console-log">\n'
                                                           '                        <code>> [TLS-1.3] Négociation '
                                                           'cipher suite TLS_AES_256_GCM_SHA384 : Établi</code><br>\n'
                                                           '                        <code>> [CLIENT-AUTH] Certificat '
                                                           "d'atelier vérifié (CN=PaxStation-Atelier-01)</code><br>\n"
                                                           '                        <code>> [PAYLOAD-PUSH] 91.4 Ko '
                                                           'transmis en 140 ms</code><br>\n'
                                                           '                        <code>> [REMOTE-ACK] Reçu HTTP 200 '
                                                           "OK avec signature d'accusé d'enregistrement</code>\n"
                                                           '                      </div>\n'
                                                           '                    </div>'},
                                   'p4': {   'tabTitle': '4. Écran de Fin ✨',
                                             'phaseTitle': "Dossier Transmis & Statut 'Prêt pour Gravure' Acquitté",
                                             'status': 'success',
                                             'caption': "Le dossier est arrivé dans la file d'attente de la "
                                                        'PaxStation. La production peut commencer.',
                                             'screenHtml': '\n'
                                                           '                    <div class="wf-screen-box">\n'
                                                           '                      <div class="wf-header-bar">\n'
                                                           '                        <span '
                                                           'class="wf-app-title">PaxStudio Pro • Production '
                                                           'Enclenchée</span>\n'
                                                           '                        <span class="wf-status-badge '
                                                           'wf-badge-success">✨ Acquitté par PaxStation</span>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-success-banner">\n'
                                                           '                        <span '
                                                           'class="wf-seal-icon">🚀</span>\n'
                                                           '                        <div>\n'
                                                           '                          <strong>BAT Télétransmis avec '
                                                           'Succès à la Station de Gravure</strong>\n'
                                                           '                          <p class="wf-subtext">Horodaté '
                                                           'eIDAS • Dossier n° BAT-2026-BEL-00412 pris en charge par '
                                                           "l'atelier</p>\n"
                                                           '                        </div>\n'
                                                           '                      </div>\n'
                                                           '                      <div class="wf-btn-row">\n'
                                                           '                        <button class="wf-btn '
                                                           'wf-btn-gold">Télécharger le Récépissé Probatoire & Clore '
                                                           '→</button>\n'
                                                           '                      </div>\n'
                                                           '                    </div>'}}}}
]

