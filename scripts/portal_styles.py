#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeterniTrak V1.0 — Styles CSS Pur & Embarqué (100% Hors-Ligne, Zéro CDN)
Design System Obsidienne Sombre, Dorures Nobles & Wireframes Haute Définition.
"""

CSS_STYLES = r"""
    /* =========================================================================
       AeterniTrak V1.0 — Design System Obsidienne & Living Wireframes Studio
       Styles 100% Hors-Ligne & Embarqués (Phase A pure, ZÉRO ressource distante)
       ========================================================================= */
    :root {
      --bg-obsidian-950: #06070b;
      --bg-obsidian-900: #0b0d14;
      --bg-obsidian-850: #0f121c;
      --bg-obsidian-800: #141824;
      --bg-obsidian-750: #1a2030;
      --slate-900: #0f172a;
      --slate-850: #162032;
      --slate-800: #1e293b;
      --slate-700: #334155;
      --slate-600: #475569;
      --slate-500: #64748b;
      --slate-400: #94a3b8;
      --slate-300: #cbd5e1;
      --slate-200: #e2e8f0;
      --gold-300: #f6e088;
      --gold-400: #e5c058;
      --gold-500: #d4af37;
      --gold-600: #b38f24;
      --gold-700: #8a6d17;
      --emerald-400: #34d399;
      --emerald-500: #10b981;
      --sky-400: #38bdf8;
      --amber-400: #fbbf24;
      --amber-500: #f59e0b;
      --rose-400: #fb7185;
      --rose-500: #f43f5e;
      --red-500: #ef4444;
      --indigo-300: #a5b4fc;
      --indigo-400: #818cf8;
      --purple-300: #d8b4fe;
      --purple-400: #c084fc;
      --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      --font-mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
    }

    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-obsidian-950);
      color: var(--slate-200);
      font-family: var(--font-sans);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      line-height: 1.5;
    }

    ::selection {
      background: var(--gold-500);
      color: #000;
    }

    /* Scrollbars */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-obsidian-900); }
    ::-webkit-scrollbar-thumb { background: #1e2436; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--gold-500); }

    /* Composants & Cartes Glassmorphism */
    .glass-card {
      background: rgba(20, 24, 36, 0.78);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(212, 175, 55, 0.2);
      border-radius: 1rem;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .glass-card:hover {
      border-color: rgba(212, 175, 55, 0.5);
      box-shadow: 0 12px 35px -10px rgba(212, 175, 55, 0.22);
      transform: translateY(-2px);
    }

    .gold-gradient-text {
      background: linear-gradient(135deg, #fff0b3 0%, #d4af37 50%, #aa8015 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    /* Header & Navigation */
    header {
      border-bottom: 1px solid rgba(51, 65, 85, 0.8);
      background: rgba(11, 13, 20, 0.96);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      position: sticky;
      top: 0;
      z-index: 50;
      padding: 0.75rem 1.5rem;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
    }

    .tab-btn {
      padding: 0.5rem 1rem;
      border-radius: 0.75rem;
      font-size: 0.75rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      background: transparent;
      border: 1px solid transparent;
      color: var(--slate-400);
      transition: all 0.2s ease;
      font-family: inherit;
    }
    .tab-btn:hover {
      color: #fff;
      background: rgba(30, 41, 59, 0.6);
      border-color: rgba(212, 175, 55, 0.2);
    }
    .tab-btn.bg-gold-500 {
      background: var(--gold-500) !important;
      color: var(--bg-obsidian-950) !important;
      box-shadow: 0 4px 14px 0 rgba(212, 175, 55, 0.35);
      border-color: var(--gold-400) !important;
    }

    .tab-content.hidden {
      display: none !important;
    }

    /* Modale / Dialogue Native */
    dialog#ucModal {
      border: none;
      background: transparent;
      padding: 1rem;
      max-width: 72rem;
      width: 100%;
      margin: auto;
    }
    dialog#ucModal::backdrop {
      background: rgba(0, 0, 0, 0.88);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
    }
    dialog#ucModal:focus {
      outline: none;
    }

    /* Animations de Déclenchement & Traitement */
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.92); }
    }
    .animate-pulse {
      animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    @keyframes radar-pulse {
      0% {
        box-shadow: 0 0 0 0 rgba(212, 175, 55, 0.85);
        border-color: var(--gold-400);
      }
      70% {
        box-shadow: 0 0 0 14px rgba(212, 175, 55, 0);
        border-color: var(--gold-500);
      }
      100% {
        box-shadow: 0 0 0 0 rgba(212, 175, 55, 0);
        border-color: var(--gold-400);
      }
    }
    .wf-radar-pulse {
      animation: radar-pulse 1.8s infinite ease-out;
      border: 1px solid var(--gold-500) !important;
    }

    @keyframes progress-stripes {
      from { background-position: 1rem 0; }
      to { background-position: 0 0; }
    }
    .wf-progress-bar {
      height: 100%;
      background: linear-gradient(45deg, rgba(212, 175, 55, 0.85) 25%, rgba(246, 224, 136, 0.95) 50%, rgba(212, 175, 55, 0.85) 75%);
      background-size: 1rem 1rem;
      animation: progress-stripes 0.8s linear infinite;
      border-radius: 4px;
      transition: width 0.3s ease;
    }

    @keyframes gold-shimmer {
      0% { background-position: -200% 0; }
      100% { background-position: 200% 0; }
    }

    /* Grille et Mise en Page Utilitaires */
    .grid { display: grid; }
    .grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
    @media (min-width: 768px) {
      .md\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
    @media (min-width: 1024px) {
      .lg\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    }
    .gap-1 { gap: 0.25rem; }
    .gap-1\.5 { gap: 0.375rem; }
    .gap-2 { gap: 0.5rem; }
    .gap-3 { gap: 0.75rem; }
    .gap-4 { gap: 1rem; }
    .gap-5 { gap: 1.25rem; }
    .gap-6 { gap: 1.5rem; }

    .flex { display: flex; }
    .flex-col { flex-direction: column; }
    .flex-wrap { flex-wrap: wrap; }
    .flex-1 { flex: 1 1 0%; }
    .items-center { align-items: center; }
    .items-start { align-items: flex-start; }
    .justify-between { justify-content: space-between; }
    .justify-center { justify-content: center; }

    .w-full { width: 100%; }
    .max-w-3xl { max-width: 48rem; }
    .max-w-6xl { max-width: 72rem; }
    .max-w-7xl { max-width: 80rem; }
    .mx-auto { margin-left: auto; margin-right: auto; }
    .m-auto { margin: auto; }
    .space-y-1\.5 > * + * { margin-top: 0.375rem; }
    .space-y-2 > * + * { margin-top: 0.5rem; }
    .space-y-3 > * + * { margin-top: 0.75rem; }
    .space-y-4 > * + * { margin-top: 1rem; }
    .space-y-5 > * + * { margin-top: 1.25rem; }
    .space-y-6 > * + * { margin-top: 1.5rem; }

    /* =========================================================================
       MODULE WIREFRAME PLAYER & DEVICE BEZELS
       ========================================================================= */
    .wf-player-card {
      background: var(--bg-obsidian-900);
      border: 1px solid rgba(212, 175, 55, 0.22);
      border-radius: 0.75rem;
      padding: 0.75rem;
      margin-top: 0.75rem;
      display: flex;
      flex-direction: column;
      gap: 0.6rem;
    }

    .wf-controls-bar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 0.4rem;
      border-bottom: 1px solid rgba(51, 65, 85, 0.5);
      padding-bottom: 0.5rem;
    }

    .wf-pills-row {
      display: flex;
      flex-wrap: wrap;
      gap: 0.3rem;
    }

    .wf-pill-btn {
      font-family: var(--font-mono);
      font-size: 0.65rem;
      font-weight: 700;
      padding: 0.25rem 0.55rem;
      border-radius: 0.5rem;
      cursor: pointer;
      border: 1px solid rgba(51, 65, 85, 0.8);
      background: rgba(15, 23, 42, 0.7);
      color: var(--slate-400);
      transition: all 0.15s ease;
    }
    .wf-pill-btn:hover {
      color: #fff;
      border-color: var(--gold-500);
    }
    .wf-pill-btn.active {
      background: var(--gold-500);
      color: var(--bg-obsidian-950);
      border-color: var(--gold-400);
      box-shadow: 0 0 10px rgba(212, 175, 55, 0.4);
    }

    .wf-sim-btn {
      font-family: var(--font-mono);
      font-size: 0.65rem;
      font-weight: 700;
      padding: 0.25rem 0.65rem;
      border-radius: 0.5rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.3rem;
      border: 1px solid rgba(212, 175, 55, 0.4);
      background: rgba(212, 175, 55, 0.12);
      color: var(--gold-300);
      transition: all 0.2s ease;
    }
    .wf-sim-btn:hover {
      background: var(--gold-500);
      color: #000;
      box-shadow: 0 0 12px rgba(212, 175, 55, 0.5);
    }
    .wf-sim-btn.playing {
      background: rgba(239, 68, 68, 0.2);
      border-color: var(--red-500);
      color: #fca5a5;
    }

    /* Device Mockup Bezels */
    .device-bezel {
      background: #030407;
      border: 1px solid rgba(212, 175, 55, 0.25);
      border-radius: 0.65rem;
      overflow: hidden;
      box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.8);
    }

    .device-topbar {
      background: rgba(15, 18, 28, 0.95);
      border-bottom: 1px solid rgba(51, 65, 85, 0.4);
      padding: 0.3rem 0.6rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 0.62rem;
      color: var(--slate-400);
    }

    .device-controls-dots {
      display: flex;
      gap: 0.25rem;
    }
    .dot-red { width: 6px; height: 6px; border-radius: 50%; background: #ef4444; }
    .dot-yellow { width: 6px; height: 6px; border-radius: 50%; background: #f59e0b; }
    .dot-green { width: 6px; height: 6px; border-radius: 50%; background: #10b981; }

    /* Screen Canvas & Content Styles */
    .wf-screen-box {
      padding: 0.65rem;
      min-height: 185px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 0.5rem;
      background: linear-gradient(180deg, rgba(11, 13, 20, 0.95) 0%, rgba(6, 7, 11, 0.98) 100%);
      font-size: 0.72rem;
    }

    .wf-header-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.4rem;
      border-bottom: 1px solid rgba(51, 65, 85, 0.35);
      padding-bottom: 0.3rem;
    }

    .wf-app-title {
      font-weight: 700;
      color: var(--slate-200);
      font-size: 0.68rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .wf-status-badge {
      font-family: var(--font-mono);
      font-size: 0.58rem;
      font-weight: 700;
      padding: 0.15rem 0.4rem;
      border-radius: 0.35rem;
      white-space: nowrap;
    }
    .wf-badge-neutral { background: rgba(51, 65, 85, 0.5); color: var(--slate-300); }
    .wf-badge-trigger { background: rgba(212, 175, 55, 0.25); color: var(--gold-300); border: 1px solid var(--gold-500); }
    .wf-badge-process { background: rgba(16, 185, 129, 0.2); color: var(--emerald-400); border: 1px solid var(--emerald-500); }
    .wf-badge-success { background: rgba(16, 185, 129, 0.25); color: #6ee7b7; border: 1px solid var(--emerald-400); }
    .wf-badge-alert { background: rgba(239, 68, 68, 0.25); color: #fca5a5; border: 1px solid var(--red-500); }

    .wf-content-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 0.4rem;
    }
    .wf-field-group {
      display: flex;
      flex-direction: column;
      gap: 0.15rem;
    }
    .wf-label {
      font-size: 0.6rem;
      color: var(--slate-400);
      font-family: var(--font-mono);
    }
    .wf-req { color: var(--gold-400); font-weight: bold; }
    .wf-select-placeholder {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(51, 65, 85, 0.6);
      padding: 0.25rem 0.4rem;
      border-radius: 0.35rem;
      color: var(--slate-300);
      font-size: 0.65rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .wf-btn-row {
      display: flex;
      flex-wrap: wrap;
      gap: 0.35rem;
      padding-top: 0.35rem;
      border-top: 1px solid rgba(51, 65, 85, 0.35);
    }
    .wf-btn {
      font-size: 0.65rem;
      font-weight: 700;
      padding: 0.25rem 0.6rem;
      border-radius: 0.4rem;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.15s ease;
      font-family: inherit;
    }
    .wf-btn-primary { background: rgba(212, 175, 55, 0.18); border-color: var(--gold-500); color: var(--gold-300); }
    .wf-btn-primary:hover { background: var(--gold-500); color: #000; }
    .wf-btn-gold { background: var(--gold-500); color: #000; font-weight: bold; }
    .wf-btn-gold:hover { background: var(--gold-400); }
    .wf-btn-sub { background: rgba(30, 41, 59, 0.6); border-color: rgba(51, 65, 85, 0.8); color: var(--slate-400); }
    .wf-btn-sub:hover { color: #fff; border-color: var(--slate-400); }
    .wf-btn-disabled { background: rgba(30, 41, 59, 0.3); border-color: rgba(51, 65, 85, 0.4); color: var(--slate-600); cursor: not-allowed; }
    .wf-btn-danger { background: rgba(239, 68, 68, 0.2); border-color: var(--red-500); color: #fca5a5; }

    .wf-trigger-card {
      background: rgba(212, 175, 55, 0.08);
      border: 1px dashed var(--gold-500);
      border-radius: 0.5rem;
      padding: 0.45rem;
      text-align: center;
    }
    .wf-trigger-indicator {
      font-weight: 700;
      color: var(--gold-300);
      font-size: 0.68rem;
    }
    .wf-subtext {
      font-size: 0.6rem;
      color: var(--slate-400);
      margin-top: 0.15rem;
    }

    .wf-progress-container {
      height: 6px;
      background: rgba(30, 41, 59, 0.8);
      border-radius: 4px;
      overflow: hidden;
      margin: 0.3rem 0;
    }

    .wf-console-log {
      background: #040508;
      border: 1px solid rgba(51, 65, 85, 0.6);
      border-radius: 0.4rem;
      padding: 0.35rem;
      font-family: var(--font-mono);
      font-size: 0.58rem;
      color: #38bdf8;
      max-height: 65px;
      overflow-y: auto;
      line-height: 1.3;
    }
    .wf-console-log code { display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

    .wf-success-banner {
      background: rgba(16, 185, 129, 0.1);
      border: 1px solid rgba(16, 185, 129, 0.4);
      border-radius: 0.5rem;
      padding: 0.5rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .wf-seal-icon { font-size: 1.4rem; }

    .wf-alert-card {
      border-radius: 0.5rem;
      padding: 0.5rem;
      font-size: 0.65rem;
    }
    .wf-alert-red { background: rgba(239, 68, 68, 0.12); border: 1px solid var(--red-500); color: #fca5a5; }
    .wf-alert-amber { background: rgba(245, 158, 11, 0.12); border: 1px solid var(--amber-500); color: #fde68a; }

    .wf-caption-box {
      font-size: 0.65rem;
      color: var(--slate-300);
      background: rgba(15, 23, 42, 0.6);
      padding: 0.35rem 0.5rem;
      border-radius: 0.4rem;
      border-left: 2px solid var(--gold-500);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
    }

    /* Tiroirs Dépliables (Formulaires & Erreurs) */
    .wf-drawer-toggle {
      font-family: var(--font-mono);
      font-size: 0.62rem;
      font-weight: 700;
      color: var(--slate-400);
      background: rgba(15, 23, 42, 0.5);
      border: 1px solid rgba(51, 65, 85, 0.6);
      border-radius: 0.4rem;
      padding: 0.25rem 0.5rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      text-align: left;
      transition: all 0.15s ease;
    }
    .wf-drawer-toggle:hover {
      color: #fff;
      border-color: var(--gold-500);
    }
    .wf-drawer-content {
      background: rgba(6, 7, 11, 0.95);
      border: 1px solid rgba(51, 65, 85, 0.6);
      border-radius: 0.4rem;
      padding: 0.5rem;
      font-size: 0.65rem;
      display: none;
      margin-top: 0.3rem;
    }
    .wf-drawer-content.open { display: block; }

    /* Mode Board Déplié (4 Écrans Simultanés) */
    .wf-board-grid {
      display: grid;
      grid-template-columns: repeat(1, minmax(0, 1fr));
      gap: 0.75rem;
    }
    @media (min-width: 1024px) {
      .wf-board-grid {
        grid-template-columns: repeat(4, minmax(0, 1fr));
      }
    }
    .wf-board-col {
      display: flex;
      flex-direction: column;
      gap: 0.4rem;
    }
    .wf-board-badge {
      font-family: var(--font-mono);
      font-size: 0.65rem;
      font-weight: 700;
      padding: 0.25rem 0.5rem;
      border-radius: 0.4rem;
      background: rgba(30, 41, 59, 0.7);
      border: 1px solid rgba(51, 65, 85, 0.8);
      color: var(--slate-300);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    /* Sélecteur de Mode d'Affichage dans les En-têtes */
    .view-mode-bar {
      background: rgba(11, 13, 20, 0.85);
      border: 1px solid rgba(51, 65, 85, 0.6);
      border-radius: 0.75rem;
      padding: 0.4rem 0.75rem;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
    }
    .view-mode-btn {
      font-family: var(--font-mono);
      font-size: 0.7rem;
      font-weight: 700;
      padding: 0.3rem 0.6rem;
      border-radius: 0.5rem;
      cursor: pointer;
      border: 1px solid transparent;
      background: transparent;
      color: var(--slate-400);
      transition: all 0.2s ease;
    }
    .view-mode-btn:hover { color: #fff; }
    .view-mode-btn.active {
      background: var(--gold-500);
      color: #000;
      font-weight: bold;
    }

    /* Tableau Synthétique */
    .table-summary {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.72rem;
    }
    .table-summary th {
      background: rgba(15, 23, 42, 0.95);
      padding: 0.6rem 0.75rem;
      text-align: left;
      font-family: var(--font-mono);
      font-size: 0.65rem;
      color: var(--slate-400);
      border-bottom: 1px solid rgba(51, 65, 85, 0.8);
    }
    .table-summary td {
      padding: 0.6rem 0.75rem;
      border-bottom: 1px solid rgba(30, 41, 59, 0.6);
      vertical-align: top;
    }
    .table-summary tr:hover { background: rgba(30, 41, 59, 0.3); }
"""
