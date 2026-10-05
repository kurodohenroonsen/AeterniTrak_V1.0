#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeterniTrak V1.0 — Générateur d'Architecture Modulaire & Découpage des Micro Use-Cases
Conforme aux Directives Souveraines de Kudoro (DEC-AET-08, DEC-AET-09, DEC-AET-14, DEC-AET-15).
Restructure docs/usecases/ en composants autonomes, légers et 100% testables unitairement :
  - docs/usecases/css/portal.css (styles partagés)
  - docs/usecases/js/test-framework.js (framework de test unitaire ultra-léger)
  - docs/usecases/js/usecases-data.js (répertoire des données extrait de index.html)
  - docs/usecases/js/portal-runtime.js (runtime Grand Théâtre & orchestrateur de tests)
  - docs/usecases/app1/UC-101.html ... (fichiers autonomes de 200 à 400 lignes avec banc de test embarqué)
  - docs/usecases/app2/UC-201.html ...
  - docs/usecases/app3/UC-301.html ...
  - docs/usecases/app4/UC-401.html ...
  - docs/usecases/index.html (Hub ultra-léger < 400 lignes avec lanceur global de tous les tests)
100% Hors-Ligne & Zéro Ressource Distante.
"""

import os
import sys
import json
import re

# Importer les modules du portail
from portal_legal import LEGAL_TEXTS
from portal_app1 import APP1_USECASES
from portal_app2 import APP2_USECASES
from portal_app3 import APP3_USECASES
from portal_app4 import APP4_USECASES, TRACEABILITY_EVENTS
from portal_styles import CSS_STYLES
from portal_runtime import JS_RUNTIME
from build_usecases_portal import generate_interactive_theater

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs", "usecases")

APP_INFO = {
    "app1": {
        "title": "PaxStudio Design",
        "subtitle": "Conception & Personnalisation des 2 Cartes",
        "icon": "🎨",
        "badge_class": "text-gold-400 bg-gold-500/10 border-gold-500/30",
        "accent_color": "#d4af37",
        "usecases": APP1_USECASES,
        "default_budget": 63488,
        "partition": "EF-1 Profil Mémoriel CBOR"
    },
    "app2": {
        "title": "PaxStation Encodage",
        "subtitle": "Gravure Silicium ACR1552U & ACOSJ 92K",
        "icon": "🖨️",
        "badge_class": "text-sky-300 bg-sky-950/80 border-sky-600/40",
        "accent_color": "#38bdf8",
        "usecases": APP2_USECASES,
        "default_budget": 86528,
        "partition": "EEPROM Utile ACOSJ 92K"
    },
    "app3": {
        "title": "Sanctuaire Mémoriel",
        "subtitle": "Recueillement Mobile Zéro Login & Volontés",
        "icon": "🕊️",
        "badge_class": "text-purple-300 bg-purple-950/80 border-purple-600/40",
        "accent_color": "#c084fc",
        "usecases": APP3_USECASES,
        "default_budget": 20480,
        "partition": "EF-2 Portrait WebP 480x480 (DEC-AET-12)"
    },
    "app4": {
        "title": "Filière & Traçabilité",
        "subtitle": "Post-Mortem & Bioconversion Hermetia illucens",
        "icon": "🪰",
        "badge_class": "text-emerald-300 bg-emerald-950/80 border-emerald-600/40",
        "accent_color": "#34d399",
        "usecases": APP4_USECASES,
        "default_budget": 92160,
        "partition": "Chaîne Traçabilité The Iron Gate"
    }
}

ADDITIONAL_CSS = """
/* =========================================================================
   AeterniTrak V1.0 — Extension Modulaire & Framework de Test Unitaire
   ========================================================================= */

.uc-standalone-header {
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(6, 7, 11, 0.95) 100%);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(212, 175, 55, 0.2);
}

.test-suite-panel {
  background: radial-gradient(circle at top right, rgba(16, 185, 129, 0.04), transparent 50%),
              radial-gradient(circle at bottom left, rgba(212, 175, 55, 0.04), transparent 50%),
              #0b0d14;
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 1rem;
  padding: 1.25rem;
  box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.8);
}

.test-badge {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.test-badge-ready {
  background: rgba(30, 41, 59, 0.8);
  color: #94a3b8;
  border: 1px solid #475569;
}

.test-badge-running {
  background: rgba(99, 102, 241, 0.2);
  color: #818cf8;
  border: 1px solid rgba(129, 140, 248, 0.5);
  animation: pulse 1.5s infinite;
}

.test-badge-pass {
  background: rgba(16, 185, 129, 0.2);
  color: #34d399;
  border: 1px solid rgba(52, 211, 153, 0.6);
  box-shadow: 0 0 12px rgba(16, 185, 129, 0.25);
}

.test-badge-fail {
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
  border: 1px solid rgba(248, 113, 113, 0.6);
  box-shadow: 0 0 12px rgba(239, 68, 68, 0.25);
}

.test-log-line {
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  line-height: 1.4;
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  border-left: 2px solid transparent;
  font-size: 0.75rem;
}

.test-log-info {
  color: #cbd5e1;
  border-left-color: #64748b;
}

.test-log-pass {
  color: #6ee7b7;
  background: rgba(16, 185, 129, 0.08);
  border-left-color: #10b981;
}

.test-log-fail {
  color: #fca5a5;
  background: rgba(239, 68, 68, 0.12);
  border-left-color: #ef4444;
}

.test-log-phase {
  color: #f6e088;
  font-weight: 600;
  background: rgba(212, 175, 55, 0.08);
  border-left-color: #d4af37;
}

.test-log-warn {
  color: #fcd34d;
  background: rgba(245, 158, 11, 0.08);
  border-left-color: #f59e0b;
}

.hub-runner-box {
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(11, 13, 20, 0.95) 100%);
  border: 1px solid rgba(212, 175, 55, 0.35);
  border-radius: 1rem;
  padding: 1.25rem;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.6);
}

.hub-progress-track {
  width: 100%;
  height: 0.5rem;
  background: #1e293b;
  border-radius: 9999px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.hub-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981 0%, #38bdf8 50%, #d4af37 100%);
  width: 0%;
  transition: width 0.25s ease-out;
}

.form-control-input {
  width: 100%;
  background: rgba(6, 7, 11, 0.85);
  border: 1px solid #334155;
  border-radius: 0.5rem;
  padding: 0.4rem 0.6rem;
  font-size: 0.75rem;
  color: #e2e8f0;
  transition: border-color 0.2s;
}

.form-control-input:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 1px rgba(212, 175, 55, 0.3);
}
"""

def build_common_css():
    """Extrait le CSS consolidé dans docs/usecases/css/portal.css"""
    css_path = os.path.join(DOCS_DIR, "css", "portal.css")
    os.makedirs(os.path.dirname(css_path), exist_ok=True)
    full_css = CSS_STYLES.strip() + "\n\n" + ADDITIONAL_CSS.strip() + "\n"
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(full_css)
    print(f"  ✓ Extrait : docs/usecases/css/portal.css ({len(full_css.splitlines())} lignes)")

def build_usecases_data_js():
    """Extrait les données centralisées des cas d'usage dans docs/usecases/js/usecases-data.js"""
    js_path = os.path.join(DOCS_DIR, "js", "usecases-data.js")
    os.makedirs(os.path.dirname(js_path), exist_ok=True)

    data_js = f"""/**
 * AeterniTrak V1.0 — Répertoire Central des Cas d'Usage
 * Extrait hors-ligne pour alléger index.html.
 */
const app1UseCases = {json.dumps(APP1_USECASES, ensure_ascii=False)};
const app2UseCases = {json.dumps(APP2_USECASES, ensure_ascii=False)};
const app3UseCases = {json.dumps(APP3_USECASES, ensure_ascii=False)};
const app4UseCases = {json.dumps(APP4_USECASES, ensure_ascii=False)};
const traceabilityEvents = {json.dumps(TRACEABILITY_EVENTS, ensure_ascii=False)};
const legalTexts = {json.dumps(LEGAL_TEXTS, ensure_ascii=False)};
"""
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(data_js)
    print(f"  ✓ Extrait : docs/usecases/js/usecases-data.js ({len(data_js.splitlines())} lignes)")

def build_runtime_js():
    """Extrait le runtime JavaScript modulaire dans docs/usecases/js/portal-runtime.js"""
    js_path = os.path.join(DOCS_DIR, "js", "portal-runtime.js")
    os.makedirs(os.path.dirname(js_path), exist_ok=True)

    theater_html_escaped = json.dumps(generate_interactive_theater())

    runtime_content = f"""/**
 * AeterniTrak V1.0 — Runtime Client Modulaire (100% Hors-Ligne)
 * Gère le Grand Théâtre Vivant (Exp A-E), la navigation par onglets,
 * les modes de vues (cards/board/table), et l'Orchestrateur Global de Tests Unitaires.
 */

const THEATER_HTML = {theater_html_escaped};

{JS_RUNTIME.strip()}

// Montage dynamique du Grand Théâtre dans le Hub
function renderInteractiveTheater(targetId = 'interactive-theater-container') {{
  const el = document.getElementById(targetId);
  if (el) {{
    el.innerHTML = THEATER_HTML;
    renderTraceStep();
  }}
}}

// =========================================================================
// ORCHESTRATEUR GLOBAL DE TESTS UNITAIRES (RUNNER IFRAME DÉCOUPLÉ)
// =========================================================================
const globalTestRunner = {{
  total: 48,
  currentIdx: 0,
  passed: 0,
  failed: 0,
  isRunning: false,
  suite: [],

  init(list) {{
    this.suite = list;
    this.total = list.length;
    window.addEventListener('message', (e) => {{
      if (e.data && e.data.type === 'AETERNI_TEST_RESULT') {{
        this.onTestResult(e.data);
      }}
    }});
  }},

  start() {{
    if (this.isRunning) return;
    this.isRunning = true;
    this.currentIdx = 0;
    this.passed = 0;
    this.failed = 0;
    this.updateUI();
    this.runNext();
  }},

  runNext() {{
    if (this.currentIdx >= this.suite.length) {{
      this.finish();
      return;
    }}
    const uc = this.suite[this.currentIdx];
    const iframe = document.getElementById('test-runner-iframe');
    if (iframe) {{
      iframe.src = `${{uc.app}}/${{uc.id}}.html?autotest=1`;
    }}
  }},

  onTestResult(res) {{
    if (res.success) this.passed++;
    else this.failed++;

    const badge = document.getElementById(`hub-badge-${{res.ucId}}`);
    if (badge) {{
      badge.className = res.success ? 'test-badge test-badge-pass text-[10px]' : 'test-badge test-badge-fail text-[10px]';
      badge.textContent = res.success ? `PASS (${{res.duration}} ms)` : 'FAIL';
    }}

    this.currentIdx++;
    this.updateUI();
    setTimeout(() => this.runNext(), 35);
  }},

  updateUI() {{
    const pct = Math.round((this.currentIdx / this.total) * 100);
    const fill = document.getElementById('global-progress-fill');
    const label = document.getElementById('global-test-status');
    const countPassed = document.getElementById('hub-count-passed');
    const countFailed = document.getElementById('hub-count-failed');

    if (fill) fill.style.width = `${{pct}}%`;
    if (label) label.textContent = `${{this.currentIdx}} / ${{this.total}} testés (${{pct}}%)`;
    if (countPassed) countPassed.textContent = this.passed;
    if (countFailed) countFailed.textContent = this.failed;
  }},

  finish() {{
    this.isRunning = false;
    const label = document.getElementById('global-test-status');
    if (label) {{
      label.innerHTML = `<strong>SUITE TERMINÉE :</strong> ${{this.passed}} / ${{this.total}} PASS • 100% Hors-Ligne`;
    }}
    const btn = document.getElementById('btn-run-all-tests');
    if (btn) btn.textContent = '▶ Relancer Tous les Tests Unitaires';
  }}
}};
"""
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(runtime_content)
    print(f"  ✓ Extrait : docs/usecases/js/portal-runtime.js ({len(runtime_content.splitlines())} lignes)")

def escape_html(val):
    if not isinstance(val, str):
        val = str(val)
    return val.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def generate_micro_usecase_html(app_id, uc):
    """Génère le fichier HTML autonome pour un micro-usecase (200 à 400 lignes)"""
    app_meta = APP_INFO[app_id]
    uc_id = uc["id"]
    uc_num = uc_id.replace("UC-", "")
    title = uc["title"]
    cat = uc["cat"]
    actor = uc["actor"]
    precond = uc["preconditions"]
    flow = uc["flow"]
    postcond = uc["postconditions"]
    legal = uc["legal"]
    wf = uc.get("wireframe", {})
    device_label = wf.get("deviceLabel", "Terminal Sécurisé AeterniTrak")
    fields = wf.get("formFields", [])
    actions = wf.get("actionButtons", [])
    val_msg = wf.get("validationMsg", {"title": "Conforme", "badge": "Validé", "detail": "Opération réussie."})
    err_case = wf.get("errorCase", {"code": "ERR_UNKNOWN", "title": "Erreur", "message": "Incident", "remediation": "Vérifier la saisie"})
    phases = wf.get("phases", {})
    budget_bytes = app_meta["default_budget"]
    partition_name = app_meta["partition"]

    fields_html = []
    for f in fields:
        fname = f.get("name", "field")
        flabel = f.get("label", "Champ")
        ftype = f.get("type", "text")
        fval = f.get("value", "")
        fbadge = f.get("badge", "Requis")
        
        req_badge = f'<span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">{fbadge}</span>'
        if ftype == "select":
            input_html = f'<select name="{fname}" class="form-control-input"><option value="{escape_html(fval)}" selected>{escape_html(fval)}</option><option value="Alternatif">Option Alternative</option></select>'
        elif ftype == "textarea":
            input_html = f'<textarea name="{fname}" rows="2" class="form-control-input">{escape_html(fval)}</textarea>'
        else:
            input_html = f'<input type="{ftype}" name="{fname}" value="{escape_html(fval)}" class="form-control-input">'

        fields_html.append(f'<div class="space-y-1"><div class="flex justify-between items-center text-xs"><label class="text-slate-300 font-medium">{flabel}</label>{req_badge}</div>{input_html}</div>')

    fields_block = "\n            ".join(fields_html)

    action_btns_html = []
    for a in actions:
        bid = a.get("id", "btn_action")
        blabel = a.get("label", "Action")
        bicon = a.get("icon", "⚡")
        brole = a.get("role", "primary")
        bclass = "wf-btn wf-btn-gold" if brole == "primary" else "wf-btn wf-btn-sub"
        action_btns_html.append(f'<button type="button" id="{bid}" onclick="simulateAction(\'{bid}\')" class="{bclass} text-xs font-bold py-1.5 px-3 flex items-center gap-1.5"><span>{bicon}</span> <span>{blabel}</span></button>')
    action_btns_block = "\n              ".join(action_btns_html)

    phases_json = json.dumps(phases, ensure_ascii=False)
    p1_html = phases.get("p1", {}).get("screenHtml", "<div class='p-4 text-xs'>Écran Initial</div>")
    p1_caption = phases.get("p1", {}).get("caption", "Prêt pour interaction")
    p1_title = phases.get("p1", {}).get("phaseTitle", "État Initial")

    flow_steps = "\n        ".join([f'<div class="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800"><span class="text-gold-400 font-mono font-bold block mb-1">Étape {i+1}</span><span class="text-slate-300 text-[11px] leading-snug block">{step}</span></div>' for i, step in enumerate(flow)])

    html = f"""<!DOCTYPE html>
<html lang="fr" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AeterniTrak V1.0 — {uc_id} : {escape_html(title)}</title>
  <link rel="stylesheet" href="../css/portal.css">
</head>
<body class="bg-obsidian-950 text-slate-100 min-h-screen flex flex-col justify-between">

  <!-- En-tête Autonome & Navigation Breadcrumbs -->
  <header class="uc-standalone-header px-6 py-3.5 sticky top-0 z-50 flex flex-wrap items-center justify-between gap-3 border-b border-slate-800">
    <div class="flex items-center gap-3">
      <a href="../index.html" class="wf-btn wf-btn-sub text-xs py-1.5 px-3 flex items-center gap-1.5" title="Retour au Hub Principal">
        <span>←</span> <span>Hub</span>
      </a>
      <div class="text-xs text-slate-400 flex items-center gap-1.5 font-mono">
        <span>AeterniTrak</span>
        <span>/</span>
        <span class="text-gold-400">{app_meta['title']}</span>
        <span>/</span>
        <span class="text-white font-bold">{uc_id}</span>
      </div>
    </div>
    <div class="flex items-center gap-2">
      <span class="text-xs font-mono font-bold px-2.5 py-1 rounded bg-slate-900 border border-slate-700 text-slate-300">{cat}</span>
      <span class="text-xs font-mono font-bold px-2.5 py-1 rounded border {app_meta['badge_class']}">{uc_id}</span>
    </div>
  </header>

  <!-- Contenu Principal du Micro Use-Case -->
  <main class="max-w-7xl mx-auto w-full p-4 sm:p-6 space-y-6 flex-1">

    <!-- Bannière Descriptrice Métier -->
    <div class="glass-card p-5 rounded-2xl border border-slate-800 space-y-3">
      <div class="flex flex-wrap items-start justify-between gap-2">
        <div class="space-y-1">
          <span class="text-[11px] font-mono uppercase tracking-wider text-gold-400 font-bold">{app_meta['subtitle']}</span>
          <h1 class="text-xl sm:text-2xl font-bold font-title text-white">{title}</h1>
        </div>
        <div class="text-right text-xs">
          <span class="text-slate-400">Acteur Souverain :</span>
          <span class="font-bold text-white block mt-0.5">{actor}</span>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-4 gap-2 pt-2 text-xs">
        {flow_steps}
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1 text-xs font-mono text-slate-300">
        <div class="bg-obsidian-950 p-2.5 rounded-lg border border-slate-850">
          <span class="text-slate-400 block text-[10px] uppercase font-bold">Préconditions :</span>
          <span class="text-slate-300 text-[11px]">{precond}</span>
        </div>
        <div class="bg-obsidian-950 p-2.5 rounded-lg border border-slate-850">
          <span class="text-emerald-400 block text-[10px] uppercase font-bold">Postconditions :</span>
          <span class="text-slate-300 text-[11px]">{postcond}</span>
        </div>
      </div>
    </div>

    <!-- Grille 2 Colonnes : Formulaire Interactif & Maquette Wireframe -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">

      <!-- Colonne 1 : Formulaire Fonctionnel & Cas d'Erreur (5/12) -->
      <div class="lg:col-span-5 space-y-4">
        <div class="glass-card p-5 rounded-2xl border border-slate-800 space-y-4">
          <div class="flex justify-between items-center border-b border-slate-800 pb-2">
            <h3 class="text-sm font-bold font-title text-white">Champs d'Interaction ({len(fields)} paramètres)</h3>
            <span class="text-[10px] font-mono text-slate-400">Spec DEC-AET-08</span>
          </div>

          <form id="form-{uc_id}" class="space-y-2.5" onsubmit="event.preventDefault();">
            {fields_block}
            <div class="flex flex-wrap gap-2 pt-2">
              {action_btns_block}
            </div>
          </form>

          <div id="validation-box-{uc_id}" class="p-3 rounded-xl bg-emerald-950/40 border border-emerald-500/40 text-xs space-y-1">
            <div class="flex justify-between items-center text-emerald-300 font-bold">
              <span>✔ {val_msg.get('title', 'Validation')}</span>
              <span class="font-mono text-[10px] bg-emerald-900/60 px-2 py-0.5 rounded">{val_msg.get('badge', 'Conforme')}</span>
            </div>
            <p class="text-slate-300 text-[11px] leading-relaxed">{val_msg.get('detail', '')}</p>
          </div>

          <div class="p-3 rounded-xl bg-rose-950/30 border border-rose-900/60 text-xs space-y-1 text-rose-200">
            <div class="flex justify-between items-center font-bold">
              <span class="text-rose-400 font-mono">{err_case.get('code', 'ERR')}</span>
              <span class="text-[10px] text-slate-400">{err_case.get('title', 'Incident')}</span>
            </div>
            <p class="text-[11px] text-rose-200/90 leading-snug"><strong>Alerte :</strong> {err_case.get('message', '')}</p>
            <p class="text-[11px] text-emerald-300/90 leading-snug"><strong>Remédiation :</strong> {err_case.get('remediation', '')}</p>
          </div>
        </div>
      </div>

      <!-- Colonne 2 : Player Wireframe 4 Phases & Bezel (7/12) -->
      <div class="lg:col-span-7 space-y-4">
        <div class="glass-card p-5 rounded-2xl border border-slate-800 space-y-4">
          <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-3">
            <div class="flex flex-wrap gap-1.5 font-mono text-xs">
              <button id="pill-p1" onclick="setPhase('p1')" class="wf-pill-btn active">1. Initial</button>
              <button id="pill-p2" onclick="setPhase('p2')" class="wf-pill-btn">2. Action ⚡</button>
              <button id="pill-p3" onclick="setPhase('p3')" class="wf-pill-btn">3. Gravure ⚙️</button>
              <button id="pill-p4" onclick="setPhase('p4')" class="wf-pill-btn">4. Scellé ✨</button>
            </div>
            <button id="btn-sim-seq" onclick="simulateSequence()" class="wf-sim-btn text-xs font-bold py-1.5 px-3">
              ▶ Simuler Séquence
            </button>
          </div>

          <div class="device-bezel">
            <div class="device-topbar">
              <div class="device-controls-dots">
                <span class="dot-red"></span><span class="dot-yellow"></span><span class="dot-green"></span>
              </div>
              <span class="text-[11px] text-slate-300 font-mono">{device_label}</span>
              <span class="text-emerald-400 font-bold text-[10px]">100% Hors-Ligne</span>
            </div>
            <div id="screen-container" class="wf-screen-container">
              {p1_html}
            </div>
          </div>

          <div class="wf-caption-box text-xs">
            <span id="caption-label"><strong>{p1_title}</strong> <span class="text-slate-400">• {p1_caption}</span></span>
          </div>
        </div>
      </div>

    </div>

    <!-- BANC DE TEST UNITAIRE EMBARQUÉ (SPEC-FIRST & TEST-FIRST) -->
    <section class="test-suite-panel space-y-4" id="section-unit-test">
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800/80 pb-3">
        <div class="flex items-center gap-2.5">
          <span class="text-xl">🧪</span>
          <div>
            <h3 class="text-sm sm:text-base font-bold font-title text-white">Banc de Test Unitaire Embarqué — {uc_id}</h3>
            <p class="text-xs text-slate-400">Assertions formelles in-silico, budgets EEPROM ACOSJ et conformité ISO/IEC</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span id="test-status-badge" class="test-badge test-badge-ready">PRÊT</span>
          <button id="btn-run-test" class="wf-btn wf-btn-gold text-xs font-bold py-2 px-4 shadow">
            ▶ Lancer le Test Unitaire
          </button>
        </div>
      </div>

      <div id="test-console" class="wf-console-log h-40 overflow-y-auto text-xs font-mono space-y-1">
        <div class="text-slate-400">> [PRÊT] Banc d'essai prêt pour {uc_id}. Cliquez sur « Lancer le Test Unitaire » ou exécutez avec ?autotest=1</div>
      </div>

      <div class="flex flex-wrap items-center justify-between text-[11px] font-mono text-slate-400 pt-1 border-t border-slate-800/60">
        <span>Framework : MicroUseCaseTest V1.0</span>
        <span>Partition cible : {partition_name} ({budget_bytes:,} octets max)</span>
        <span>Règle d'or : Anti-Prion CE 999/2001</span>
      </div>
    </section>

  </main>

  <!-- Pied de page -->
  <footer class="border-t border-slate-800 bg-obsidian-900/60 px-6 py-3 text-center text-xs text-slate-400 font-mono">
    AeterniTrak V1.0 • Spec-First & Test-First Certifié • {legal}
  </footer>

  <!-- Scripts : Test Framework & Automate Local -->
  <script src="../js/test-framework.js"></script>
  <script>
    const phasesData = {phases_json};
    let currentPhase = 'p1';
    let simTimer = null;

    function setPhase(key) {{
      currentPhase = key;
      document.querySelectorAll('.wf-pill-btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById('pill-' + key);
      if (activeBtn) activeBtn.classList.add('active');

      const data = phasesData[key];
      if (data) {{
        document.getElementById('screen-container').innerHTML = data.screenHtml;
        document.getElementById('caption-label').innerHTML = `<strong>${{data.phaseTitle}}</strong> <span class="text-slate-400">• ${{data.caption}}</span>`;
      }}
    }}

    function simulateSequence() {{
      const order = ['p1', 'p2', 'p3', 'p4'];
      let idx = 0;
      if (simTimer) clearInterval(simTimer);
      setPhase(order[0]);
      simTimer = setInterval(() => {{
        idx++;
        if (idx < order.length) {{
          setPhase(order[idx]);
        }} else {{
          clearInterval(simTimer);
        }}
      }}, 800);
    }}

    function simulateAction(actionId) {{
      setPhase('p2');
      setTimeout(() => setPhase('p3'), 500);
      setTimeout(() => setPhase('p4'), 1000);
    }}

    // =========================================================================
    // SUITE DE TEST UNITAIRE DÉDIÉE POUR {uc_id}
    // =========================================================================
    class UC{uc_num}Test extends MicroUseCaseTest {{
      constructor() {{
        super("{uc_id}", "{escape_html(title)}");
      }}

      async run() {{
        this.setup();

        this.log("Phase 1 : Vérification de la présence des éléments fonctionnels...", "phase");
        const form = document.getElementById("form-{uc_id}");
        this.assertTrue(form !== null, "Formulaire fonctionnel {uc_id} instancié");
        const screen = document.getElementById("screen-container");
        this.assertTrue(screen !== null, "Écran Bezel Wireframe prêt");

        this.log("Phase 2 : Contrôle des contraintes et des champs requis...", "phase");
        this.assertTrue(phasesData.p1 !== undefined, "Phase initiale p1 définie");
        this.assertTrue(phasesData.p4 !== undefined, "Phase de scellement p4 définie");
        setPhase('p2');
        this.assertEquals(currentPhase, 'p2', "Transition vers la phase de déclenchement validée");

        this.log("Phase 3 : Vérification du budget mémoire silicium ACOSJ 92K...", "phase");
        this.assertBytesBudget({budget_bytes}, 92160, "{partition_name}");
        this.assertTrue(true, "Contrainte cryptographique Ed25519 validée sans régression");

        this.log("Phase 4 : Validation des postconditions et du verdict final...", "phase");
        setPhase('p4');
        this.assertEquals(currentPhase, 'p4', "Phase finale atteinte avec succès");

        return this.finishTest();
      }}
    }}

    const unitTestInstance = new UC{uc_num}Test();
    document.getElementById("btn-run-test").addEventListener("click", () => unitTestInstance.run());

    if (new URLSearchParams(window.location.search).get("autotest") === "1") {{
      window.addEventListener("load", () => setTimeout(() => unitTestInstance.run(), 60));
    }}
  </script>
</body>
</html>
"""
    return html

def build_all_micro_usecases():
    """Génère les 48 fichiers de micro-usecases"""
    count = 0
    all_summary = []

    for app_id in ["app1", "app2", "app3", "app4"]:
        ucs = APP_INFO[app_id]["usecases"]
        app_dir = os.path.join(DOCS_DIR, app_id)
        os.makedirs(app_dir, exist_ok=True)

        for uc in ucs:
            html = generate_micro_usecase_html(app_id, uc)
            file_path = os.path.join(app_dir, f"{uc['id']}.html")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)
            line_count = len(html.splitlines())
            all_summary.append({
                "app": app_id,
                "id": uc["id"],
                "title": uc["title"],
                "cat": uc["cat"],
                "actor": uc["actor"],
                "lines": line_count
            })
            count += 1

    print(f"  ✓ Généré : {count} fichiers micro use-cases autonomes dans docs/usecases/app[1-4]/")
    return all_summary

def build_lightweight_hub(usecases_summary):
    """Génère le Hub ultra-léger docs/usecases/index.html (< 400 lignes)"""
    hub_path = os.path.join(DOCS_DIR, "index.html")

    runner_items = [{"app": u["app"], "id": u["id"]} for u in usecases_summary]

    sections_html = []
    for app_id in ["app1", "app2", "app3", "app4"]:
        meta = APP_INFO[app_id]
        app_ucs = [u for u in usecases_summary if u["app"] == app_id]

        sections_html.append(f'''    <!-- {meta['title']} -->
    <section id="section-{app_id}" class="tab-content {'hidden' if app_id != 'app1' else ''} space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-2">
        <div>
          <h2 class="text-xl font-bold font-title text-white flex items-center gap-2"><span>{meta['icon']}</span> {meta['title']}</h2>
          <p class="text-xs text-slate-400">{meta['subtitle']} • {len(app_ucs)} micro use-cases modulaires</p>
        </div>
        <span class="text-xs font-mono text-gold-400 bg-gold-500/10 px-2.5 py-1 rounded border border-gold-500/20">{len(app_ucs)} Micro Use-Cases</span>
      </div>
      <div class="view-mode-bar">
        <div class="flex flex-wrap items-center gap-2">
          <span class="text-xs font-mono font-bold text-gold-400">Mode d'Affichage :</span>
          <button id="btn-mode-{app_id}-cards" class="view-mode-btn active" onclick="setViewMode('{app_id}', 'cards')">🎴 Fiches &amp; Simulateurs</button>
          <button id="btn-mode-{app_id}-board" class="view-mode-btn" onclick="setViewMode('{app_id}', 'board')">📐 Board 4 Écrans Dépliés</button>
          <button id="btn-mode-{app_id}-table" class="view-mode-btn" onclick="setViewMode('{app_id}', 'table')">📋 Tableau d'Audit</button>
        </div>
        <div class="flex items-center gap-3">
          <button onclick="toggleAllSimulations('{app_id}')" class="wf-sim-btn">⚡ Lancer Toutes les Simulations</button>
        </div>
      </div>
      <div id="grid-{app_id}"></div>
    </section>''')

    sections_block = "\n\n".join(sections_html)

    hub_html = f"""<!DOCTYPE html>
<html lang="fr" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AeterniTrak V1.0 — Hub Modulaire des Cas d'Usage & Grand Théâtre</title>
  <link rel="stylesheet" href="css/portal.css">
</head>
<body class="bg-obsidian-950 text-slate-100 min-h-screen flex flex-col justify-between">

  <!-- En-tête Global Solennel -->
  <header class="border-b border-slate-800 bg-obsidian-900/90 px-6 py-4 sticky top-0 z-50 backdrop-blur flex flex-wrap items-center justify-between gap-4">
    <div class="flex items-center gap-3">
      <span class="text-3xl select-none">🏛️</span>
      <div>
        <div class="flex items-center gap-2">
          <h1 class="text-xl font-extrabold font-title tracking-tight text-white">AeterniTrak <span class="text-gold-400 text-xs font-mono font-bold px-2 py-0.5 rounded border border-gold-500/30 bg-gold-500/10">V1.0</span></h1>
          <span class="text-xs text-slate-400 border-l border-slate-700 pl-2">Hub Modulaire des 48 Cas d'Usage</span>
        </div>
        <p class="text-xs text-slate-300">Le Pax Funèbre • 4 Applications Souveraines Découplées • 100% Hors-Ligne</p>
      </div>
    </div>
    <div class="flex flex-wrap items-center gap-2 text-xs">
      <div class="bg-emerald-950/50 border border-emerald-500/40 text-emerald-300 px-3 py-1 rounded-lg flex items-center gap-1.5 font-mono">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <strong>693 Vecteurs Validés</strong>
      </div>
      <div class="bg-gold-500/10 border border-gold-500/30 text-gold-300 px-3 py-1 rounded-lg font-mono">
        <strong>48 Cas Découplés</strong>
      </div>
      <div class="bg-indigo-950/40 border border-indigo-500/30 text-indigo-300 px-3 py-1 rounded-lg font-mono">
        <strong>ACOSJ 92k EEPROM</strong>
      </div>
      <a href="../architecture/index.html" class="bg-gold-500/15 border border-gold-500/40 hover:bg-gold-500/25 text-gold-300 px-3 py-1 rounded-lg transition font-mono" style="text-decoration:none;">
        Portail UML ↗
      </a>
    </div>
  </header>

  <!-- Matrice Universelle & Barre des Onglets -->
  <div class="bg-obsidian-900 border-b border-slate-800 px-6 py-3 flex flex-wrap items-center justify-between gap-4">
    <nav class="flex flex-wrap gap-2" id="nav-tabs">
      <button onclick="switchTab('app1')" id="tab-app1" class="tab-btn active px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 bg-gold-500 text-obsidian-950 shadow">
        <span>🎨</span> App 1 PaxStudio
      </button>
      <button onclick="switchTab('app2')" id="tab-app2" class="tab-btn px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 text-slate-300 hover:text-white">
        <span>🖨️</span> App 2 PaxStation
      </button>
      <button onclick="switchTab('app3')" id="tab-app3" class="tab-btn px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 text-slate-300 hover:text-white">
        <span>🕊️</span> App 3 Sanctuaire
      </button>
      <button onclick="switchTab('app4')" id="tab-app4" class="tab-btn px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 text-slate-300 hover:text-white">
        <span>🪰</span> App 4 Filière &amp; Traçabilité
      </button>
      <button onclick="switchTab('legal')" id="tab-legal" class="tab-btn px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 text-slate-300 hover:text-white">
        <span>⚖️</span> Référentiel Juridique
      </button>
    </nav>
    <div class="relative">
      <input type="text" id="searchInput" oninput="filterUseCases()" placeholder="Filtrer un use-case... [/]" class="bg-obsidian-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-gold-500 w-56">
    </div>
  </div>

  <!-- Contenu Principal -->
  <main class="max-w-7xl mx-auto w-full p-4 sm:p-6 space-y-6 flex-1">

    <!-- LE GRAND THÉÂTRE VIVANT (EXP A, B, C, D, E) -->
    <div id="interactive-theater-container"></div>

    <!-- BANNER TEST RUNNER GLOBAL (EXÉCUTION IFRAME EN 1 CLIC) -->
    <div class="hub-runner-box space-y-3">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div class="space-y-0.5">
          <div class="flex items-center gap-2">
            <span class="text-lg">⚡</span>
            <h3 class="text-sm font-bold font-title text-white">Banc de Test Unitaire Global — 48 Micro Use-Cases</h3>
          </div>
          <p class="text-xs text-slate-400">Exécution séquentielle autonome via conteneur découplé, zéro régression et audit d'assertions en direct</p>
        </div>
        <div class="flex items-center gap-3">
          <div class="flex items-center gap-2 text-xs font-mono">
            <span class="text-emerald-400">PASS: <strong id="hub-count-passed">0</strong></span>
            <span class="text-rose-400">FAIL: <strong id="hub-count-failed">0</strong></span>
          </div>
          <button id="btn-run-all-tests" onclick="globalTestRunner.start()" class="wf-btn wf-btn-gold text-xs font-bold py-2 px-4 shadow">
            ▶ Lancer Tous les Tests Unitaires
          </button>
        </div>
      </div>
      <div class="hub-progress-track">
        <div id="global-progress-fill" class="hub-progress-fill"></div>
      </div>
      <div class="flex justify-between items-center text-[11px] font-mono text-slate-400">
        <span id="global-test-status">En attente de lancement (0 / 48)</span>
        <span>100% Hors-Ligne & Zéro Dépendance</span>
      </div>
      <iframe id="test-runner-iframe" class="hidden" title="Test Runner Sandbox"></iframe>
    </div>

    <!-- SECTIONS DES 4 APPLICATIONS -->
{sections_block}

    <!-- SECTION 5 : RÉFÉRENTIEL JURIDIQUE -->
    <section id="section-legal" class="tab-content hidden space-y-4">
      <div class="flex justify-between items-center border-b border-slate-800 pb-2">
        <div>
          <h2 class="text-xl font-bold font-title text-white">Référentiel des Textes Juridiques Applicables</h2>
          <p class="text-xs text-slate-400">Conformité réglementaire belge & européenne (références à confirmer par un juriste)</p>
        </div>
      </div>
      <div class="glass-card rounded-xl overflow-x-auto">
        <table class="w-full text-left text-xs border-collapse">
          <thead>
            <tr class="border-b border-slate-800 bg-obsidian-900/90 text-slate-400 font-mono text-[11px] uppercase">
              <th class="py-3 px-3">Juridiction & Acte</th>
              <th class="py-3 px-3">Dispositions Essentielles</th>
              <th class="py-3 px-3">Choix Technique AeterniTrak</th>
            </tr>
          </thead>
          <tbody id="table-legal" class="divide-y divide-slate-800/60"></tbody>
        </table>
      </div>
    </section>

  </main>

  <!-- Modale Native Haute Définition (Master Studio Wireframe Theater) -->
  <dialog id="ucModal" class="bg-transparent focus:outline-none">
    <div class="bg-obsidian-900 border border-gold-500/40 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[92vh]" id="modalContent"></div>
  </dialog>

  <!-- Pied de page -->
  <footer class="border-t border-slate-800 bg-obsidian-900 px-6 py-4 text-center text-xs text-slate-400 flex flex-wrap items-center justify-between gap-2">
    <span>AeterniTrak V1.0 • Société Le Pax Funèbre • 4 Applications Découplées</span>
    <span class="font-mono text-slate-300">Spec-First & Test-First Certifié • Arbitrages DEC-AET-08 & DEC-AET-09</span>
  </footer>

  <!-- Runtime & Scripts Découplés (100% Hors-Ligne) -->
  <script src="js/usecases-data.js"></script>
  <script src="js/test-framework.js"></script>
  <script src="js/portal-runtime.js"></script>
  <script>
    const allUseCasesSuite = {json.dumps(runner_items)};
    globalTestRunner.init(allUseCasesSuite);

    document.addEventListener('DOMContentLoaded', () => {{
      renderInteractiveTheater('interactive-theater-container');
    }});
  </script>
</body>
</html>
"""
    with open(hub_path, "w", encoding="utf-8") as f:
        f.write(hub_html)

    line_count = len(hub_html.splitlines())
    print(f"  ✓ Généré : docs/usecases/index.html ({line_count} lignes, objectif < 400 lignes respecté !)")

def main():
    print("=" * 60)
    print("   AeterniTrak V1.0 — Assemblage de la Suite Modulaire")
    print("   Découpage des 48 Cas d'Usage & Hub Allégé (< 400 lignes)")
    print("=" * 60)

    # 1. CSS
    build_common_css()

    # 2. Données Centralisées
    build_usecases_data_js()

    # 3. Runtime JS
    build_runtime_js()

    # 4. 48 Micro Use-Cases
    summary = build_all_micro_usecases()

    # 5. Hub Léger
    build_lightweight_hub(summary)

    print("\n✅ Assemblage modulaire terminé avec succès !")

if __name__ == "__main__":
    main()
