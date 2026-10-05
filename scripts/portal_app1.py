#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeterniTrak V1.0 — Définition Complète des Micro Use-Cases pour App 1 : PaxStudio Design (UC-101 à UC-110)
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
                {"label": "Normalisation EBU R128", "name": "ebu_lufs", "type": "text", "value": "-23 LUFS (Filtre anti-souffle actif)", "placeholder": "Volume", "badge": "Audio Pro", "required": False}
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
                {"label": "Atténuation Ducking Vocal", "name": "ducking_level", "type": "text", "value": "-14 dB automatique lors de la voix", "placeholder": "Ducking", "badge": "Actif", "required": False}
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
                {"label": "Message d'Adieu Public", "name": "public_message", "type": "textarea", "value": "« Que la nature accueille ma mémoire en paix auprès des grands chênes. »", "placeholder": "Message", "badge": "Facultatif", "required": False}
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
            "Contrôle obligatoire d'alerte sur la présence d'un stimulateur cardiaque (pacemaker) ou défibrillateur implantable (Art. L1232-17 §2 CDLD — référence à confirmer par un juriste).",
            "Si stimulateur présent : blocage strict imposant le renseignement de l'attestation chirurgicale d'exérèse avec numéro d'ordre du médecin.",
            "Recueil de la position sur le don d'organes (rappel de la loi belge du consentement présumé de 1986 — référence à confirmer par un juriste).",
            "Enregistrement éventuel d'un protocole de legs du corps à la science sous 48h auprès d'une université conventionnée."
        ],
        "postconditions": "Volet médical post-mortem validé, alerte pacemaker levée uniquement sur certificat médical officiel.",
        "legal": "Article L1232-17 §2 du CDLD (exérèse obligatoire des stimulateurs cardiaques) (référence à confirmer par un juriste).",
        "legal_url": "#section-legal",
        "wireframe": {
            "device": "tablet",
            "deviceLabel": "PaxStudio Pro • Volet Médical d'Urgence & Sécurité",
            "formFields": [
                {"label": "Porteur de Stimulateur Cardiaque (Pacemaker)", "name": "has_pacemaker", "type": "select", "value": "OUI (Présence confirmée)", "placeholder": "Sélectionner", "badge": "ALERTE VITALE", "required": True},
                {"label": "Attestation d'Exérèse Chirurgicale", "name": "pacemaker_cert", "type": "file", "value": "certificat_exerese_dr_vaneck.pdf", "placeholder": "Téléverser attestation", "badge": "Obligatoire si Oui", "required": True},
                {"label": "Médecin Certificateur & N° Ordre", "name": "pacemaker_doc", "type": "text", "value": "Dr. Marc Vaneck — INAMI 1-40912-88-004", "placeholder": "Nom et INAMI", "badge": "Vérifié", "required": True},
                {"label": "Don d'Organes (Loi 1986 — référence à confirmer par un juriste)", "name": "organ_donation", "type": "select", "value": "Consentement Plein et Entier Confirmé", "placeholder": "Statut don", "badge": "Loi 1986 (référence à confirmer par un juriste)", "required": True}
            ],
            "actionButtons": [
                {"id": "btn_validate_medical", "label": "Valider le Volet Médical d'Urgence", "role": "primary", "state": "idle", "icon": "🩺"},
                {"id": "btn_verify_inami", "label": "Vérifier Validité Ordre Médecin", "role": "secondary", "state": "idle", "icon": "🔍"}
            ],
            "validationMsg": {
                "title": "Volet Médical d'Urgence Certifié",
                "badge": "Conforme Art. L1232-17 CDLD (référence à confirmer par un juriste)",
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
                        <p class="wf-subtext">L'article L1232-17 §2 CDLD (référence à confirmer par un juriste) impose l'exérèse chirurgicale avant toute opération.</p>
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
                        <span class="wf-app-title">PaxStudio Pro • Contrôle Sécurité Exérèse (référence à confirmer par un juriste)</span>
                        <span class="wf-status-badge wf-badge-process">⚙️ Vérification Légale (95%)</span>
                      </div>
                      <div class="wf-progress-container"><div class="wf-progress-bar" style="width: 95%;"></div></div>
                      <div class="wf-console-log">
                        <code>> [LEGAL-CHECK] Format numéro INAMI médecin : Valide</code><br>
                        <code>> [LEGAL-CHECK] Règle Art. L1232-17 §2 satisfaite (référence à confirmer par un juriste) : Exérèse certifiée</code><br>
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
    }
]
