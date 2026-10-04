#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeterniTrak V1.0 — Styles CSS Pur & Embarqué (100% Hors-Ligne, Zéro CDN)
Design System Obsidienne Sombre, Dorures Nobles, Grand Théâtre Interactif,
Mockups iPhone 16 Pro, Cartes 3D CR-80, Lecteur ACR1552U, Cassette LFA & Wireframes Confortables.
Conçu par Éléonore de Saint-Aubert (Lead UX Sanctuaire & Human Empathy) & Bushi 08.
"""

CSS_STYLES = r"""
    /* =========================================================================
       AeterniTrak V1.0 — Design System Obsidienne & Grand Théâtre Vivant
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
      --emerald-600: #059669;
      --sky-300: #7dd3fc;
      --sky-400: #38bdf8;
      --sky-500: #0284c7;
      --amber-400: #fbbf24;
      --amber-500: #f59e0b;
      --rose-400: #fb7185;
      --rose-500: #f43f5e;
      --red-500: #ef4444;
      --indigo-300: #a5b4fc;
      --indigo-400: #818cf8;
      --purple-300: #d8b4fe;
      --purple-400: #c084fc;
      --purple-500: #a855f7;
      --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      --font-serif: "Georgia", "Charter", "Palatino", serif;
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
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: var(--bg-obsidian-900); }
    ::-webkit-scrollbar-thumb { background: #1e2436; border-radius: 4px; border: 1px solid rgba(212,175,55,0.1); }
    ::-webkit-scrollbar-thumb:hover { background: var(--gold-500); }

    /* Composants & Cartes Glassmorphism */
    .glass-card {
      background: rgba(20, 24, 36, 0.85);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(212, 175, 55, 0.22);
      border-radius: 1.25rem;
      transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .glass-card:hover {
      border-color: rgba(212, 175, 55, 0.55);
      box-shadow: 0 14px 40px -10px rgba(212, 175, 55, 0.22);
      transform: translateY(-2px);
    }

    /* Thèmes par Application (Code Couleur Harmonieux) */
    .theme-app1 {
      --app-accent: var(--gold-500);
      --app-accent-light: var(--gold-300);
      --app-accent-bg: rgba(212, 175, 55, 0.12);
      --app-accent-border: rgba(212, 175, 55, 0.3);
      --app-glow: rgba(212, 175, 55, 0.25);
    }
    .theme-app2 {
      --app-accent: var(--sky-400);
      --app-accent-light: var(--sky-300);
      --app-accent-bg: rgba(56, 189, 248, 0.12);
      --app-accent-border: rgba(56, 189, 248, 0.3);
      --app-glow: rgba(56, 189, 248, 0.25);
    }
    .theme-app3 {
      --app-accent: var(--purple-400);
      --app-accent-light: var(--purple-300);
      --app-accent-bg: rgba(192, 132, 252, 0.12);
      --app-accent-border: rgba(192, 132, 252, 0.3);
      --app-glow: rgba(192, 132, 252, 0.25);
    }
    .theme-app4 {
      --app-accent: var(--emerald-400);
      --app-accent-light: var(--emerald-300);
      --app-accent-bg: rgba(16, 185, 129, 0.12);
      --app-accent-border: rgba(16, 185, 129, 0.3);
      --app-glow: rgba(16, 185, 129, 0.25);
    }

    .gold-gradient-text {
      background: linear-gradient(135deg, #fff0b3 0%, #d4af37 50%, #aa8015 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    /* Header & Navigation */
    header {
      border-bottom: 1px solid rgba(51, 65, 85, 0.8);
      background: rgba(11, 13, 20, 0.97);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      position: sticky;
      top: 0;
      z-index: 50;
      padding: 0.85rem 1.75rem;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 1.25rem;
    }

    /* =========================================================================
       BIMODAL TOGGLE : VUE FAMILLE vs VUE INGÉNIEUR / EXPERT
       ========================================================================= */
    .bimodal-toggle-box, .mode-switch-capsule {
      display: inline-flex;
      align-items: center;
      background: rgba(6, 7, 11, 0.9);
      border: 1.5px solid rgba(212, 175, 55, 0.4);
      border-radius: 9999px;
      padding: 3px;
      gap: 3px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6);
    }
    .bimodal-btn, .mode-switch-btn {
      padding: 0.45rem 1rem;
      border-radius: 9999px;
      font-size: 0.78rem;
      font-weight: 700;
      cursor: pointer;
      border: none;
      background: transparent;
      color: var(--slate-400);
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      transition: all 0.25s ease;
      font-family: inherit;
    }
    .bimodal-btn:hover, .mode-switch-btn:hover {
      color: #fff;
    }
    .bimodal-btn.active-family, .mode-switch-btn.active {
      background: linear-gradient(135deg, #d4af37, #b38f24) !important;
      color: #000 !important;
      font-weight: 800;
      box-shadow: 0 2px 12px rgba(212, 175, 55, 0.45);
    }
    .bimodal-btn.active-engineer, .mode-switch-btn.active-expert {
      background: linear-gradient(135deg, #0284c7, #0369a1) !important;
      color: #fff !important;
      font-weight: 800;
      box-shadow: 0 2px 12px rgba(56, 189, 248, 0.45);
    }

    .tab-btn {
      padding: 0.6rem 1.15rem;
      border-radius: 0.85rem;
      font-size: 0.82rem;
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
      padding: 1.25rem;
      max-width: 78rem;
      width: 100%;
      margin: auto;
    }
    dialog#ucModal::backdrop {
      background: rgba(0, 0, 0, 0.9);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
    }
    dialog#ucModal:focus {
      outline: none;
    }

    /* =========================================================================
       LE GRAND THÉÂTRE VIVANT & PODS INTERACTIFS
       ========================================================================= */

    /* POD 1 : CARTE 3D RÉVERSIBLE CR-80 */
    .card-3d-scene {
      perspective: 1200px;
      width: 100%;
      max-width: 480px;
      height: 275px;
      margin: 0 auto;
      cursor: pointer;
    }
    .card-3d-inner {
      width: 100%;
      height: 100%;
      position: relative;
      transform-style: preserve-3d;
      transition: transform 0.85s cubic-bezier(0.34, 1.4, 0.64, 1);
      border-radius: 1rem;
    }
    .card-3d-inner.flipped {
      transform: rotateY(180deg);
    }
    .card-3d-face {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      border-radius: 1rem;
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
    }
    .card-3d-front {
      background: radial-gradient(circle at 25% 25%, #1c2233 0%, #0d0f17 100%);
      border: 1.5px solid rgba(212, 175, 55, 0.75);
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.9), inset 0 0 25px rgba(212, 175, 55, 0.15);
    }
    .card-3d-back {
      transform: rotateY(180deg);
      background: radial-gradient(circle at 75% 25%, #182030 0%, #090c14 100%);
      border: 1.5px solid rgba(16, 185, 129, 0.7);
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.9), inset 0 0 25px rgba(16, 185, 129, 0.12);
    }

    /* Puce Contact Dorée ACOSJ */
    .chip-gold {
      width: 48px;
      height: 38px;
      border-radius: 6px;
      background: linear-gradient(135deg, #f6e088 0%, #d4af37 50%, #996515 100%);
      border: 1px solid #ffe082;
      box-shadow: inset 0 0 4px rgba(0,0,0,0.5), 0 2px 6px rgba(0,0,0,0.6);
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      grid-template-rows: repeat(2, 1fr);
      gap: 1.5px;
      padding: 2.5px;
    }
    .chip-gold > div {
      background: rgba(0, 0, 0, 0.28);
      border-radius: 1px;
    }

    /* POD 2 : MOCKUP SMARTPHONE (iPHONE 16 PRO) & FLAMME */
    .phone-mockup {
      width: 100%;
      max-width: 320px;
      margin: 0 auto;
      border-radius: 38px;
      background: #000;
      border: 3.5px solid #2f3440;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.95), 0 0 0 1px #444b58;
      padding: 10px;
      position: relative;
    }
    .phone-screen {
      background: #050608;
      border-radius: 30px;
      min-height: 480px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
      border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .phone-dynamic-island {
      width: 100px;
      height: 26px;
      background: #000;
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 16px;
      margin: 6px auto 8px auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 10px;
      font-size: 10px;
      color: #fff;
    }

    .flame-animated {
      animation: flameMotion 2s infinite ease-in-out alternate;
      transform-origin: bottom center;
      filter: drop-shadow(0 0 16px #f59e0b) drop-shadow(0 0 28px rgba(253, 224, 71, 0.7));
    }
    @keyframes flameMotion {
      0% { transform: scale(0.96) rotate(-1.5deg); }
      50% { transform: scale(1.06, 0.98) rotate(1deg); }
      100% { transform: scale(1) rotate(-0.5deg); }
    }
    @keyframes pulse-slow {
      0%, 100% { opacity: 0.6; transform: scale(0.9); }
      50% { opacity: 1; transform: scale(1.15); }
    }
    .animate-pulse-slow {
      animation: pulse-slow 3s infinite ease-in-out;
    }

    /* Oscilloscope Vocal */
    .osc-bar {
      flex: 1;
      min-width: 3px;
      max-width: 6px;
      height: 8px;
      background: linear-gradient(180deg, var(--gold-300), var(--gold-600));
      border-radius: 3px;
      animation: oscPlay 0.7s infinite alternate ease-in-out;
      transition: height 0.1s ease;
    }
    @keyframes oscPlay {
      0% { height: 4px; }
      100% { height: 26px; }
    }

    /* POD 3 : LECTEUR ACR1552U & SONAR */
    .reader-mockup {
      background: #07090e;
      border: 1.5px solid rgba(56, 189, 248, 0.3);
      border-radius: 1rem;
      padding: 1.25rem;
      space-y: 1rem;
      display: flex;
      flex-direction: column;
      gap: 0.85rem;
    }
    .nfc-target-zone {
      width: 140px;
      height: 140px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(56, 189, 248, 0.15) 0%, rgba(15, 23, 42, 0.8) 70%);
      border: 1.5px dashed rgba(56, 189, 248, 0.5);
      margin: 0 auto;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
    }
    .sonar-ring {
      position: absolute;
      inset: 0;
      border-radius: 50%;
      border: 1.5px solid rgba(56, 189, 248, 0.6);
      animation: sonarPing 2.2s infinite cubic-bezier(0, 0.2, 0.8, 1);
    }
    .sonar-ring:nth-child(2) { animation-delay: 0.7s; }
    .sonar-ring:nth-child(3) { animation-delay: 1.4s; }
    @keyframes sonarPing {
      0% { transform: scale(0.8); opacity: 0.9; }
      100% { transform: scale(1.6); opacity: 0; }
    }

    /* POD 4 : CASSETTE LFA PENTOBARBITAL */
    .lfa-cassette {
      background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
      border: 1.5px solid #cbd5e1;
      border-radius: 1rem;
      padding: 1.25rem;
      box-shadow: 0 8px 24px rgba(0,0,0,0.6);
    }
    .lfa-window {
      background: #f1f5f9;
      border: 1.5px solid #94a3b8;
      border-radius: 8px;
      height: 48px;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: space-around;
      padding: 0 2rem;
      box-shadow: inset 0 2px 5px rgba(0,0,0,0.25);
    }
    .lfa-line-c, .lfa-line-t {
      width: 4px;
      height: 34px;
      border-radius: 2px;
      transition: all 0.3s ease;
    }
    .lfa-line-c {
      background: #dc2626 !important;
      box-shadow: 0 0 6px rgba(220, 38, 38, 0.8);
    }
    .lfa-line-t {
      background: #dc2626;
      box-shadow: 0 0 6px rgba(220, 38, 38, 0.8);
    }
    .lfa-line-t.invisible {
      opacity: 0 !important;
      background: transparent !important;
      box-shadow: none !important;
    }

    /* Grille et Mise en Page Utilitaires */
    .grid { display: grid; }
    .grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
    @media (min-width: 768px) {
      .md\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
    @media (min-width: 1024px) {
      .lg\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
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
    .max-w-7xl { max-width: 82rem; }
    .mx-auto { margin-left: auto; margin-right: auto; }
    .space-y-1\.5 > * + * { margin-top: 0.375rem; }
    .space-y-2 > * + * { margin-top: 0.5rem; }
    .space-y-3 > * + * { margin-top: 0.75rem; }
    .space-y-4 > * + * { margin-top: 1rem; }
    .space-y-6 > * + * { margin-top: 1.5rem; }
    .space-y-8 > * + * { margin-top: 2rem; }

    /* =========================================================================
       MODULE WIREFRAME PLAYER & CARTE WIREFRAME HAUTE DÉFINITION
       ========================================================================= */
    .wf-player-card {
      background: var(--bg-obsidian-900);
      border: 1px solid rgba(212, 175, 55, 0.25);
      border-radius: 1rem;
      padding: 1rem;
      margin-top: 0.85rem;
      display: flex;
      flex-direction: column;
      gap: 0.8rem;
    }

    .wf-controls-bar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
      border-bottom: 1px solid rgba(51, 65, 85, 0.5);
      padding-bottom: 0.65rem;
    }

    .wf-pills-row {
      display: flex;
      flex-wrap: wrap;
      gap: 0.35rem;
    }

    .wf-pill-btn {
      font-family: var(--font-mono);
      font-size: 0.72rem;
      font-weight: 700;
      padding: 0.3rem 0.65rem;
      border-radius: 0.55rem;
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
      box-shadow: 0 0 12px rgba(212, 175, 55, 0.45);
      font-weight: 800;
    }

    .wf-sim-btn {
      font-family: var(--font-mono);
      font-size: 0.72rem;
      font-weight: 700;
      padding: 0.3rem 0.75rem;
      border-radius: 0.55rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      border: 1px solid rgba(212, 175, 55, 0.4);
      background: rgba(212, 175, 55, 0.15);
      color: var(--gold-300);
      transition: all 0.2s ease;
    }
    .wf-sim-btn:hover {
      background: var(--gold-500);
      color: #000;
      box-shadow: 0 0 14px rgba(212, 175, 55, 0.55);
    }
    .wf-sim-btn.playing {
      background: rgba(239, 68, 68, 0.25);
      border-color: var(--red-500);
      color: #fca5a5;
    }

    /* Device Mockup Bezels */
    .device-bezel {
      background: #030407;
      border: 1.5px solid rgba(212, 175, 55, 0.3);
      border-radius: 0.85rem;
      overflow: hidden;
      box-shadow: 0 10px 30px -6px rgba(0, 0, 0, 0.85);
    }

    .device-topbar {
      background: rgba(15, 18, 28, 0.98);
      border-bottom: 1px solid rgba(51, 65, 85, 0.5);
      padding: 0.45rem 0.85rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: var(--slate-300);
    }

    .device-controls-dots {
      display: flex;
      gap: 0.35rem;
    }
    .dot-red { width: 8px; height: 8px; border-radius: 50%; background: #ef4444; }
    .dot-yellow { width: 8px; height: 8px; border-radius: 50%; background: #f59e0b; }
    .dot-green { width: 8px; height: 8px; border-radius: 50%; background: #10b981; }

    /* Screen Canvas & Content Styles — MIN HEIGHT AGRANDI À 290px POUR LE CONFORT */
    .wf-screen-box {
      padding: 1.15rem;
      min-height: 290px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 0.85rem;
      background: linear-gradient(180deg, rgba(14, 17, 26, 0.96) 0%, rgba(6, 7, 11, 0.99) 100%);
      font-size: 0.84rem;
      line-height: 1.45;
    }

    .wf-header-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
      border-bottom: 1px solid rgba(51, 65, 85, 0.45);
      padding-bottom: 0.5rem;
    }

    .wf-app-title {
      font-weight: 700;
      color: var(--slate-100);
      font-size: 0.84rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .wf-status-badge {
      font-family: var(--font-mono);
      font-size: 0.68rem;
      font-weight: 700;
      padding: 0.2rem 0.55rem;
      border-radius: 0.45rem;
      white-space: nowrap;
    }
    .wf-badge-neutral { background: rgba(51, 65, 85, 0.6); color: var(--slate-200); }
    .wf-badge-trigger { background: rgba(212, 175, 55, 0.25); color: var(--gold-300); border: 1px solid var(--gold-500); }
    .wf-badge-process { background: rgba(16, 185, 129, 0.22); color: var(--emerald-400); border: 1px solid var(--emerald-500); }
    .wf-badge-success { background: rgba(16, 185, 129, 0.3); color: #6ee7b7; border: 1px solid var(--emerald-400); }
    .wf-badge-alert { background: rgba(239, 68, 68, 0.3); color: #fca5a5; border: 1px solid var(--red-500); }

    .wf-content-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 0.65rem;
    }
    .wf-field-group {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }
    .wf-label {
      font-size: 0.72rem;
      color: var(--slate-400);
      font-family: var(--font-mono);
    }
    .wf-req { color: var(--gold-400); font-weight: bold; }
    .wf-select-placeholder {
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid rgba(51, 65, 85, 0.7);
      padding: 0.38rem 0.55rem;
      border-radius: 0.45rem;
      color: var(--slate-200);
      font-size: 0.78rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .wf-btn-row {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      padding-top: 0.5rem;
      border-top: 1px solid rgba(51, 65, 85, 0.4);
    }
    .wf-btn {
      font-size: 0.76rem;
      font-weight: 700;
      padding: 0.35rem 0.75rem;
      border-radius: 0.5rem;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.18s ease;
      font-family: inherit;
    }
    .wf-btn-primary { background: rgba(212, 175, 55, 0.22); border-color: var(--gold-500); color: var(--gold-300); }
    .wf-btn-primary:hover { background: var(--gold-500); color: #000; }
    .wf-btn-gold { background: var(--gold-500); color: #000; font-weight: bold; }
    .wf-btn-gold:hover { background: var(--gold-400); }
    .wf-btn-sub { background: rgba(30, 41, 59, 0.7); border-color: rgba(51, 65, 85, 0.85); color: var(--slate-300); }
    .wf-btn-sub:hover { color: #fff; border-color: var(--slate-300); }
    .wf-btn-disabled { background: rgba(30, 41, 59, 0.35); border-color: rgba(51, 65, 85, 0.45); color: var(--slate-600); cursor: not-allowed; }
    .wf-btn-danger { background: rgba(239, 68, 68, 0.25); border-color: var(--red-500); color: #fca5a5; }

    .wf-trigger-card {
      background: rgba(212, 175, 55, 0.1);
      border: 1.5px dashed var(--gold-500);
      border-radius: 0.65rem;
      padding: 0.75rem;
      text-align: center;
    }
    .wf-trigger-indicator {
      font-weight: 700;
      color: var(--gold-300);
      font-size: 0.82rem;
    }
    .wf-subtext {
      font-size: 0.72rem;
      color: var(--slate-300);
      margin-top: 0.25rem;
    }

    .wf-progress-container {
      height: 8px;
      background: rgba(30, 41, 59, 0.9);
      border-radius: 6px;
      overflow: hidden;
      margin: 0.45rem 0;
    }

    .wf-console-log {
      background: #040508;
      border: 1px solid rgba(51, 65, 85, 0.7);
      border-radius: 0.55rem;
      padding: 0.55rem;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: #38bdf8;
      max-height: 95px;
      overflow-y: auto;
      line-height: 1.4;
    }
    .wf-console-log code { display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

    .wf-success-banner {
      background: rgba(16, 185, 129, 0.14);
      border: 1px solid rgba(16, 185, 129, 0.5);
      border-radius: 0.65rem;
      padding: 0.75rem;
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }
    .wf-seal-icon { font-size: 1.75rem; }

    .wf-caption-box {
      font-size: 0.78rem;
      color: var(--slate-200);
      background: rgba(15, 23, 42, 0.75);
      padding: 0.55rem 0.85rem;
      border-radius: 0.55rem;
      border-left: 3px solid var(--gold-500);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.75rem;
      line-height: 1.4;
    }

    /* Tiroirs Dépliables */
    .wf-drawer-toggle {
      font-family: var(--font-mono);
      font-size: 0.72rem;
      font-weight: 700;
      color: var(--slate-300);
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(51, 65, 85, 0.7);
      border-radius: 0.55rem;
      padding: 0.4rem 0.75rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      text-align: left;
      transition: all 0.18s ease;
    }
    .wf-drawer-toggle:hover {
      color: #fff;
      border-color: var(--gold-500);
    }
    .wf-drawer-content {
      background: rgba(6, 7, 11, 0.97);
      border: 1px solid rgba(51, 65, 85, 0.7);
      border-radius: 0.55rem;
      padding: 0.75rem;
      font-size: 0.78rem;
      display: none;
      margin-top: 0.4rem;
    }
    .wf-drawer-content.open { display: block; }

    /* Mode Board Déplié */
    .wf-board-grid {
      display: grid;
      grid-template-columns: repeat(1, minmax(0, 1fr));
      gap: 1rem;
    }
    @media (min-width: 1024px) {
      .wf-board-grid {
        grid-template-columns: repeat(4, minmax(0, 1fr));
      }
    }
    .wf-board-col {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }
    .wf-board-badge {
      font-family: var(--font-mono);
      font-size: 0.74rem;
      font-weight: 700;
      padding: 0.35rem 0.65rem;
      border-radius: 0.5rem;
      background: rgba(30, 41, 59, 0.85);
      border: 1px solid rgba(51, 65, 85, 0.85);
      color: var(--slate-200);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    /* Sélecteur de Mode d'Affichage */
    .view-mode-bar {
      background: rgba(11, 13, 20, 0.9);
      border: 1px solid rgba(51, 65, 85, 0.7);
      border-radius: 0.95rem;
      padding: 0.55rem 1rem;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 0.75rem;
    }
    .view-mode-btn {
      font-family: var(--font-mono);
      font-size: 0.76rem;
      font-weight: 700;
      padding: 0.38rem 0.8rem;
      border-radius: 0.55rem;
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
      font-size: 0.82rem;
    }
    .table-summary th {
      background: rgba(15, 23, 42, 0.98);
      padding: 0.75rem 1rem;
      text-align: left;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: var(--slate-300);
      border-bottom: 1px solid rgba(51, 65, 85, 0.85);
    }
    .table-summary td {
      padding: 0.75rem 1rem;
      border-bottom: 1px solid rgba(30, 41, 59, 0.7);
      vertical-align: top;
    }
    .table-summary tr:hover { background: rgba(30, 41, 59, 0.35); }

    /* Raccourci Recherche */
    .search-input-wrapper {
      position: relative;
      width: 100%;
      max-width: 24rem;
    }
    .search-input {
      width: 100%;
      background: var(--bg-obsidian-950);
      border: 1.5px solid rgba(51, 65, 85, 0.8);
      border-radius: 0.85rem;
      padding: 0.6rem 1rem 0.6rem 2.4rem;
      font-size: 0.8rem;
      color: var(--slate-200);
      transition: all 0.2s ease;
    }
    .search-input:focus {
      outline: none;
      border-color: var(--gold-500);
      box-shadow: 0 0 12px rgba(212, 175, 55, 0.3);
    }

    .cat-filter-btn {
      padding: 0.4rem 0.85rem;
      border-radius: 0.65rem;
      font-size: 0.75rem;
      font-family: var(--font-mono);
      cursor: pointer;
      transition: all 0.2s ease;
      border: 1px solid rgba(51, 65, 85, 0.8);
      background: rgba(15, 23, 42, 0.6);
      color: var(--slate-300);
    }
    .cat-filter-btn:hover {
      color: #fff;
      border-color: var(--gold-400);
    }
    .cat-filter-btn.active {
      background: var(--gold-500);
      color: var(--bg-obsidian-950);
      font-weight: 800;
      border-color: var(--gold-400);
      box-shadow: 0 2px 10px rgba(212, 175, 55, 0.35);
    }

    /* =========================================================================
       STYLES ADDITIONNELS DU GRAND THÉÂTRE & EXPÉRIENCES A, B, C, D
       ========================================================================= */
    .hero-nav-btn {
      padding: 0.65rem 1.25rem;
      border-radius: 0.85rem;
      font-size: 0.85rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(51, 65, 85, 0.7);
      color: var(--slate-300);
      transition: all 0.25s ease;
      font-family: inherit;
    }
    .hero-nav-btn:hover {
      color: #fff;
      border-color: var(--gold-400);
      background: rgba(30, 41, 59, 0.9);
      transform: translateY(-1px);
    }
    .hero-nav-btn.active {
      background: linear-gradient(135deg, #fce07f 0%, #d4af37 100%) !important;
      color: #05070c !important;
      font-weight: 800;
      box-shadow: 0 4px 18px rgba(212, 175, 55, 0.4);
      border-color: var(--gold-300) !important;
    }
    .hero-panel {
      display: none;
    }
    .hero-panel.active {
      display: block;
      animation: fadeInHero 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes fadeInHero {
      from { opacity: 0; transform: translateY(8px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Exp C : Station d'encodage & lecteur */
    #paxstation-card-dock {
      transition: transform 0.65s cubic-bezier(0.34, 1.4, 0.64, 1);
    }
    #paxstation-card-dock.docked {
      transform: translateY(28px) scale(0.96);
    }
    #paxstation-acr-led {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #475569;
      transition: all 0.3s ease;
    }
    #paxstation-acr-led.active {
      background: #38bdf8 !important;
      box-shadow: 0 0 12px #38bdf8;
      animation: pulse 0.5s infinite alternate;
    }

    /* Exp D : Cassette LFA & The Iron Gate */
    #lfa-droplet {
      transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
      opacity: 0;
    }
    #lfa-strip-flow {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, rgba(212, 175, 55, 0.35), rgba(56, 189, 248, 0.35));
      transition: width 1.2s ease-in-out;
    }
    .lfa-line-c, .lfa-line-t {
      width: 4px;
      height: 34px;
      border-radius: 2px;
      background: #94a3b8;
      opacity: 0.25;
      transition: all 0.4s ease;
    }
    .lfa-line-c.active-red, .lfa-line-t.active-red {
      background: #dc2626 !important;
      opacity: 1 !important;
      box-shadow: 0 0 8px rgba(220, 38, 38, 0.9);
    }

    .iron-gate-flag {
      transition: all 0.3s ease;
    }

"""
