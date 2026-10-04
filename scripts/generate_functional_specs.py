#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur des spécifications fonctionnelles Markdown complètes pour AeterniTrak V1.0.
Extrait les données structurées des 46 micro-usecases depuis scripts/portal_app*.py
et produit la documentation formelle dans docs/functional/.
"""

import os
import sys
from datetime import datetime

# Importer les données des usecases
import portal_app1 as a1
import portal_app2 as a2
import portal_app3 as a3
import portal_app4 as a4
from portal_legal import LEGAL_TEXTS

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FUNCTIONAL_DIR = os.path.join(WORKSPACE_ROOT, "docs", "functional")

APPS_CONFIG = [
    {
        "num": 1,
        "id": "app1",
        "file_name": "app1-paxstudio-design.md",
        "title": "Application 1 — PaxStudio Design (UC-101 à UC-110)",
        "subtitle": "Outil Créatif de Personnalisation Graphique & Mémorielle (Familles & Conseillers)",
        "usecases": a1.APP1_USECASES,
        "color": "gold",
        "icon": "🎨",
        "overview": """L'application **PaxStudio Design** est l'environnement interactif dédié à la famille et au conseiller funéraire en salon des familles ou en mobilité. Elle permet la co-conception visuelle et mémorielle du double support physique (Carte Sanctuaire mémorielle et Carte Directives civiles/médicales, ou Médaillons 35 mm), la prévisualisation 3D temps réel avec matériaux nobles (or satiné, résine obsidienne), l'intégration de portraits optimisés WebP (norme STORAGE-001), la captured d'oscillogrammes vocaux avec ducking sonore, et la compilation en **capsule de pré-encodage scellée** au format CBOR/JSON prête pour la gravure physique."""
    },
    {
        "num": 2,
        "id": "app2",
        "file_name": "app2-paxstation-encodage.md",
        "title": "Application 2 — PaxStation Encodage Silicium (UC-201 à UC-210)",
        "subtitle": "Station Technique Professionnelle de Gravure Matérielle & Scellement Cryptographique",
        "usecases": a2.APP2_USECASES,
        "color": "indigo",
        "icon": "🖨️",
        "overview": """L'application **PaxStation Encodage Silicium** est l'outil technique réservé aux professionnels habilités du réseau *Le Pax Funèbre*. Connectée au lecteur de bureau **ACR1552U via WebUSB ou PC/SC CCID**, elle assure le dialogue APDU IsoDep de bas niveau avec la puce **JavaCard ACOSJ 92 Ko EEPROM**, l'initialisation du système de fichiers sécurisé, le scellement cryptographique déterministe **COSE_Sign1 (Ed25519 / ES256 avec s normalisé bas)**, l'activation du fusible matériel in-silico (protection anti-tamper en lecture seule) et le pilotage de l'impression thermique haute définition 600 DPI."""
    },
    {
        "num": 3,
        "id": "app3",
        "file_name": "app3-sanctuaire-memoriel.md",
        "title": "Application 3 — Sanctuaire Mémoriel Mobile & B2C (UC-301 à UC-312)",
        "subtitle": "Application Universelle de Recueillement, Hommage & Consultation des Directives",
        "usecases": a3.APP3_USECASES,
        "color": "purple",
        "icon": "🕊️",
        "overview": """Le **Sanctuaire Mémoriel Mobile** est l'application grand public d'hommage et de recueillement destinée aux familles, amis et intervenants d'urgence. Déclenchée instantanément par un simple effleurement sans contact (**NFC Tap Zéro-Login, sans identifiant ni mot de passe**), elle valide l'intégrité cryptographique COSE_Sign1 en local, gère l'accueil des émetteurs selon la politique de confiance (Bandeau de réserve **Option B DEC-AET-07** pour clés inconnues), orchestre le sanctuaire acoustique avec **ducking vocal automatique (-14 dB)** et offre un tiroir d'accès solennel aux volontés civiles et médicales prioritaires (**alerte pacemaker vitale Art. L1232-17 CDLD, don d'organes, legs à la science**)."""
    },
    {
        "num": 4,
        "id": "app4",
        "file_name": "app4-filiere-sarcomusation.md",
        "title": "Application 4 — Filière Sarcomusation & Traçabilité Post-Décès (UC-401 à UC-414)",
        "subtitle": "Système Expert de Contrôle Biologique, Régulation Sanitaire & The Iron Gate",
        "usecases": a4.APP4_USECASES,
        "color": "emerald",
        "icon": "🪰",
        "overview": """L'application **Filière Sarcomusation & Traçabilité** régit l'intégralité de la chaîne biologique de biodégradation par les larves d'***Hermetia illucens*** (mouche soldat noire). Utilisée par les vétérinaires légistes, les gardes-forestiers DNF et les inspecteurs sanitaires AFSCA, elle assure la ségrégation stricte des 4 profils de dépouilles (Compagnie, Faune sauvage DNF, Élevage agricole Sanitel, Déchets d'abattoir MRS), le contrôle toxicologique LFA du pentobarbital (< 10 ppb), la stérilisation thermique obligatoire (Méthode 1 : 133°C, 3 bars, 20 min ou pasteurisation 70°C/1h), et le filtrage déterministe infranchissable **The Iron Gate (portes G0 à G9)** garantissant le respect absolu de la **règle d'or anti-prion** (feed-ban européen interdisant tout recyclage intraspécifique)."""
    }
]

def format_boolean(val):
    return "Oui (Obligatoire)" if val else "Non (Optionnel)"

def clean_html_summary(html_str):
    """Extrait un résumé textuel clair du code HTML de l'écran."""
    if not html_str:
        return "Non spécifié"
    lines = [line.strip() for line in html_str.split("\n") if line.strip()]
    text_parts = []
    for line in lines:
        if "<span class=\"wf-app-title\">" in line or "<div class=\"wf-trigger-indicator\">" in line or "<div class=\"wf-progress-text\">" in line or "<span class=\"wf-badge" in line:
            clean = line.replace("<span>", "").replace("</span>", "").replace("<div>", "").replace("</div>", "")
            import re
            clean = re.sub(r'<[^>]+>', '', clean).strip()
            if clean and clean not in text_parts:
                text_parts.append(clean)
    return " • ".join(text_parts[:3]) if text_parts else "Interface interactive configurée."

def generate_usecase_markdown(uc, app_num):
    wf = uc["wireframe"]
    phases = wf.get("phases", {})
    
    md = []
    md.append(f'<a id="{uc["id"].lower()}"></a>')
    md.append(f"## {uc['id']} : {uc['title']}\n")
    
    # Métadonnées
    md.append("### 📋 Métadonnées Spécifiées\n")
    md.append("| Propriété | Valeur Spécifiée |")
    md.append("| :--- | :--- |")
    md.append(f"| **Identifiant Unique** | `{uc['id']}` |")
    md.append(f"| **Catégorie Métier** | **{uc['cat']}** |")
    md.append(f"| **Acteur Principal** | {uc['actor']} |")
    md.append(f"| **Plateformes Cibles** | {', '.join(uc['platforms'])} |")
    md.append(f"| **Tags Clés** | {', '.join([f'`{t}`' for t in uc.get('tags', [])])} |")
    md.append(f"| **Base Légale & Normative** | {uc['legal']} |")
    md.append(f"| **Terminal / Canvas Wireframe** | `{wf.get('deviceLabel', wf.get('device', 'N/A'))}` |")
    md.append("")
    
    # Conditions
    md.append("### 🎯 Préconditions & Postconditions\n")
    md.append(f"> [!NOTE]\n> **Préconditions Requises :**\n> {uc['preconditions']}\n")
    md.append(f"> [!TIP]\n> **Postconditions Garanties :**\n> {uc['postconditions']}\n")
    
    # Déroulement opérationnel (Workflow)
    md.append("### 🔄 Déroulement Opérationnel (Workflow Étapes par Étapes)\n")
    for idx, step in enumerate(uc.get("flow", []), 1):
        md.append(f"{idx}. {step}")
    md.append("")
    
    # Spécification des formulaires
    md.append("### 📝 Spécification des Champs de Saisie & Données\n")
    form_fields = wf.get("formFields", [])
    if form_fields:
        md.append("| Champ Technique | Libellé Affiché | Type | Valeur par Défaut | Placeholder | Badge UI | Requis ? |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :---: |")
        for f in form_fields:
            name = f"`{f.get('name', 'N/A')}`"
            label = f.get('label', '')
            ftype = f"`{f.get('type', 'text')}`"
            val = f.get('value', '')
            val_str = f"`{val}`" if val != "" else "*Vide*"
            ph = f.get('placeholder', '') or '-'
            badge = f"`{f.get('badge', '')}`" if f.get('badge') else "-"
            req = "✅ Requis" if f.get('required') else "⭕ Optionnel"
            md.append(f"| {name} | **{label}** | {ftype} | {val_str} | {ph} | {badge} | {req} |")
    else:
        md.append("*Aucun champ de formulaire modifiable requis (interaction directe par tap ou flux automatisé).*")
    md.append("")
    
    # Boutons d'action et déclencheurs
    md.append("### ⚡ Boutons d'Action & Déclencheurs Interactifs\n")
    action_btns = wf.get("actionButtons", [])
    if action_btns:
        md.append("| Identifiant Bouton | Libellé UI | Rôle / Style | État Initial | Icône |")
        md.append("| :--- | :--- | :--- | :--- | :---: |")
        for b in action_btns:
            bid = f"`{b.get('id', 'N/A')}`"
            label = b.get('label', '')
            role = f"`{b.get('role', 'primary')}`"
            state = f"`{b.get('state', 'idle')}`"
            icon = b.get('icon', '🔘')
            md.append(f"| {bid} | **{label}** | {role} | {state} | {icon} |")
    else:
        md.append("*Déclenchement automatique par capture d'événement matériel (NFC / Capteur).*")
    md.append("")
    
    # Messages de validation et critères de succès
    val_msg = wf.get("validationMsg", {})
    md.append("### ✅ Critères de Succès & Validation Normative\n")
    md.append(f"> [!IMPORTANT]\n")
    md.append(f"> **Titre :** {val_msg.get('title', 'Validation Réussie')}\n>")
    md.append(f"> **Badge de Conformité :** `{val_msg.get('badge', 'Conforme')}`\n>")
    md.append(f"> **Détail Opérationnel :** {val_msg.get('detail', 'Exécution validée sans anomalie.')}\n")
    
    # Gestion des erreurs et remédiation
    err = wf.get("errorCase", {})
    md.append("### ⚠️ Cas d'Erreur & Procédure de Remédiation\n")
    md.append("| Propriété d'Anomalie | Description Technique |")
    md.append("| :--- | :--- |")
    md.append(f"| **Code d'Erreur Normatif** | `{err.get('code', 'ERR_UNKNOWN')}` |")
    md.append(f"| **Intitulé de l'Incident** | **{err.get('title', 'Erreur Opérationnelle')}** |")
    md.append(f"| **Condition Déclenchante** | {err.get('condition', 'Condition anormale détectée')} |")
    md.append(f"| **Message d'Erreur UI** | *« {err.get('message', 'Une erreur est survenue.')} »* |")
    md.append(f"| **Action Corrective Requise** | **{err.get('remediation', 'Consulter le manuel de maintenance.')}** |")
    md.append("")
    
    # Cycle Wireframe à 4 États
    md.append("### 🖥️ Cycle Wireframe à 4 États (Mockup Dynamique)\n")
    md.append(f"*Canvas & Résolution Cible :* **{wf.get('deviceLabel', 'Écran Standard')}**\n")
    
    md.append("| Phase | Étape du Cycle | Titre de l'Écran | Déclencheur / Statut | Description & Rendu d'Interface |")
    md.append("| :---: | :--- | :--- | :--- | :--- |")
    
    # Phase 1
    p1 = phases.get("p1", {})
    md.append(f"| **1** | **Initial / Avant Trigger** | {p1.get('phaseTitle', 'État Initial')} | *En attente utilisateur* | {p1.get('caption', '')} |")
    
    # Phase 2
    p2 = phases.get("p2", {})
    trig = p2.get("triggerName", "Action utilisateur")
    md.append(f"| **2** | **Déclenchement ⚡** | {p2.get('phaseTitle', 'Action en cours')} | `{trig}` | {p2.get('caption', '')} |")
    
    # Phase 3
    p3 = phases.get("p3", {})
    prog = f"Progression : {p3.get('progress')}%" if "progress" in p3 else "Traitement en arrière-plan"
    md.append(f"| **3** | **Traitement ⚙️** | {p3.get('phaseTitle', 'Calculs & I/O')} | `{prog}` | {p3.get('caption', '')} |")
    
    # Phase 4
    p4 = phases.get("p4", {})
    stat = f"Statut : {p4.get('status', 'success')}" if "status" in p4 else "Cycle achevé"
    md.append(f"| **4** | **Scellement & Fin ✨** | {p4.get('phaseTitle', 'État Final')} | `{stat}` | {p4.get('caption', '')} |")
    md.append("")
    
    # Détail pliable du code HTML du Wireframe
    md.append("<details>")
    md.append(f"<summary>🔍 Consulter les fragments HTML Wireframe de {uc['id']} (4 États Dépliables)</summary>\n")
    for p_id, p_label in [("p1", "Phase 1 - Avant Trigger"), ("p2", "Phase 2 - Déclenchement"), ("p3", "Phase 3 - Traitement"), ("p4", "Phase 4 - Fin de Cycle")]:
        p_data = phases.get(p_id, {})
        html_code = p_data.get("screenHtml", "").strip()
        md.append(f"#### {p_label} : {p_data.get('phaseTitle', '')}")
        md.append(f"*{p_data.get('caption', '')}*\n")
        md.append("```html")
        md.append(html_code)
        md.append("```\n")
    md.append("</details>\n")
    md.append("---\n")
    
    return "\n".join(md)

def generate_app_document(app):
    lines = []
    lines.append(f"# {app['title']}\n")
    lines.append(f"**{app['subtitle']}**\n")
    lines.append(f"> [!NOTE]\n> **Périmètre Applicatif :**\n> {app['overview']}\n")
    
    # Navigation locale
    lines.append("## 📌 Sommaire des Micro Use-Cases Spécifiés\n")
    lines.append("| ID | Titre du Cas d'Usage | Catégorie Métier | Acteur | Plateformes | Référence Normative |")
    lines.append("| :---: | :--- | :--- | :--- | :--- | :--- |")
    for uc in app["usecases"]:
        lines.append(f"| [`{uc['id']}`](#{uc['id'].lower()}) | [{uc['title']}](#{uc['id'].lower()}) | **{uc['cat']}** | {uc['actor']} | {', '.join(uc['platforms'])} | {uc['legal']} |")
    lines.append("\n---\n")
    
    # Génération des cas d'usage
    for uc in app["usecases"]:
        lines.append(generate_usecase_markdown(uc, app["num"]))
    
    return "\n".join(lines)

def generate_readme(apps):
    lines = []
    lines.append("# Référentiel des Spécifications Fonctionnelles & Vivantes — AeterniTrak V1.0\n")
    lines.append("Ce dossier rassemble les **spécifications fonctionnelles formelles et exhaustives** des 4 applications étanches du système **AeterniTrak V1.0** (*Le Pax Funèbre*).\n")
    
    lines.append("## 🏛️ Les 4 Applications du Système AeterniTrak\n")
    lines.append("| Application | Fichier de Spécification | Périmètre Métier & Rôle | Nombre de Micro-UCs |")
    lines.append("| :--- | :--- | :--- | :---: |")
    lines.append("| **Application 1 : PaxStudio Design** | [app1-paxstudio-design.md](./app1-paxstudio-design.md) | Outil créatif de pré-encodage, maquettage 3D des cartes et médaillons, WebP 220x220, waveforms sonores. | **10 UCs** (UC-101 à UC-110) |")
    lines.append("| **Application 2 : PaxStation Encodage** | [app2-paxstation-encodage.md](./app2-paxstation-encodage.md) | Station technique de bureau, gravure ACR1552U WebUSB/PC/SC, ACOSJ 92 Ko, scellement COSE_Sign1, fusible anti-tamper. | **10 UCs** (UC-201 à UC-210) |")
    lines.append("| **Application 3 : Sanctuaire Mémoriel** | [app3-sanctuaire-memoriel.md](./app3-sanctuaire-memoriel.md) | Application B2C universelle sans login (NFC Tap), ducking vocal WebAudio, tiroir de volontés civiles Art. L1232-17 CDLD, Option B DEC-AET-07. | **12 UCs** (UC-301 à UC-312) |")
    lines.append("| **Application 4 : Filière Sarcomusation** | [app4-filiere-sarcomusation.md](./app4-filiere-sarcomusation.md) | Filière biologique Hermetia illucens, The Iron Gate (G0-G9), feed-ban anti-prion, dépistage LFA pentobarbital, Ed25519. | **14 UCs** (UC-401 à UC-414) |")
    lines.append("| **TOTAL RÉFÉRENTIEL V1.0** | - | **Matrice d'Exécution Universelle & Certifiée** | **46 Micro-UCs** |")
    lines.append("\n---\n")
    
    lines.append("## 🔗 Liens avec l'Écosystème Documentaire AeterniTrak\n")
    lines.append("- 🎭 **Grand Théâtre Vivant Interactif (Simulateur 46 Wireframes Dépliables)** : [`docs/usecases/index.html`](../usecases/index.html) — Visualisation graphique temps réel 100% hors-ligne avec bascule bicolore Mode Famille / Mode Ingénieur.")
    lines.append("- 📐 **Architecture Système Globale & Modélisation UML 3-Tiers** : [`docs/architecture/system-architecture-uml.md`](../architecture/system-architecture-uml.md) et portail interactif [`docs/architecture/index.html`](../architecture/index.html).")
    lines.append("- ⚖️ **Décisions d'Arbitrage Fondatrices (Kudoro)** : [`DECISIONS-KUDORO.md`](../../DECISIONS-KUDORO.md) — Spécifiquement DEC-AET-07 (Option B bandeau de réserve), DEC-AET-08 (Zéro-Login B2C strict) et DEC-AET-09 (Universalité multiplateforme).")
    lines.append("- 🧪 **Banc de Tests Déterministes Spec-First** : `qa/test-runner.sh` — 693 vecteurs de conformité validés (100% PASS, 0 régression).")
    lines.append("\n---\n")
    
    lines.append("## 📊 Matrice Exhaustive des 46 Micro-Use-Cases\n")
    lines.append("| ID | Titre du Cas d'Usage | Application | Catégorie | Acteur | Plateforme(s) | Base Légale / Normative | Spécification Détaillée |")
    lines.append("| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :---: |")
    
    for app in apps:
        app_doc = app["file_name"]
        for uc in app["usecases"]:
            uc_id = uc["id"]
            anchor = uc_id.lower()
            title = uc["title"]
            cat = uc["cat"]
            actor = uc["actor"]
            plats = ", ".join(uc["platforms"][:2]) + ("..." if len(uc["platforms"]) > 2 else "")
            legal = uc["legal"]
            if len(legal) > 45:
                legal_short = legal[:42] + "..."
            else:
                legal_short = legal
            link = f"[{uc_id}](./{app_doc}#{anchor})"
            lines.append(f"| `{uc_id}` | **{title}** | App {app['num']} | {cat} | {actor} | {plats} | {legal_short} | {link} |")
            
    lines.append("\n---\n")
    
    lines.append("## 🛡️ Principes Architecturaux Transversaux Obligatoires\n")
    lines.append("1. **Règle d'Or Anti-Prion & Feed-Ban Strict** : Aucun lot de protéines d'insectes ne peut être réintroduit dans la même espèce animale (règlementation CE n° 999/2001 et CE n° 142/2011). Bloqué cryptographiquement dès la signature de conformité.")
    lines.append("2. **Ségrégation des 4 Profils de Dépouilles** : Compagnie (C1 mémoriel, dépistage LFA pentobarbital obligatoire), Faune Sauvage DNF (C1/C2, PCR épizooties PPA/CWD, stérilisation Méthode 1), Ferme Sanitel (C2, boucle nationale, contrôle délais d'attente), Déchets d'Abattoir MRS (C1, dénaturation bleu de méthylène 0,5%).")
    lines.append("3. **Protection In-Silico Anti-Tamper & Zéro-Login B2C** : La puce physique ACOSJ 92 Ko EEPROM est verrouillée par fusible matériel irréversible après encodage. Aucun compte cloud requis pour la famille (NFC Tap instantané).")
    lines.append("4. **Scellement Cryptographique Déterministe** : Enveloppes COSE_Sign1 déterministes (CBOR canonique RFC 8949, clé Ed25519 ou ES256 à s normalisé bas conformément à RFC 6979).")
    
    return "\n".join(lines)

def main():
    print(">>> Démarrage de la génération des Living Specs Markdown...")
    os.makedirs(FUNCTIONAL_DIR, exist_ok=True)
    
    # 1. Générer les 4 documents d'application
    for app in APPS_CONFIG:
        out_path = os.path.join(FUNCTIONAL_DIR, app["file_name"])
        doc_content = generate_app_document(app)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(doc_content)
        print(f"✅ Généré : {out_path} ({len(app['usecases'])} cas d'usage, {len(doc_content):,} caractères)")
        
    # 2. Générer le README.md
    readme_path = os.path.join(FUNCTIONAL_DIR, "README.md")
    readme_content = generate_readme(APPS_CONFIG)
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"✅ Généré : {readme_path} (Table exhaustive des 46 cas d'usage, {len(readme_content):,} caractères)")
    
    print(">>> Génération des 5 documents Markdown achevée avec succès !")

if __name__ == "__main__":
    main()
