#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeterniTrak V1.0 — Assemblage du Portail Vivant des Cas d'Usage avec Simulateurs de Wireframes
Génère docs/usecases/index.html 100% Hors-Ligne & Embarqué (Zero CDN).
"""

import json
import os
import sys

# Importer les modules de données et de styles
from portal_legal import LEGAL_TEXTS
from portal_app1 import APP1_USECASES
from portal_app2 import APP2_USECASES
from portal_app3 import APP3_USECASES
from portal_app4 import APP4_USECASES
from portal_styles import CSS_STYLES
from portal_runtime import JS_RUNTIME

def generate_category_pills(app_id, usecases):
    cats = sorted(list(set(u['cat'] for u in usecases)))
    pills = [f'<button class="cat-filter-{app_id} px-3 py-1 rounded-lg text-xs font-mono font-bold transition bg-gold-500 text-obsidian-950 shadow-sm" data-cat="all" onclick="filterByCategory(\'{app_id}\', \'all\')">Tous ({len(usecases)})</button>']
    for cat in cats:
        count = sum(1 for u in usecases if u['cat'] == cat)
        pills.append(f'<button class="cat-filter-{app_id} px-3 py-1 rounded-lg text-xs font-mono transition text-slate-400 hover:text-white bg-slate-800/60" data-cat="{cat}" onclick="filterByCategory(\'{app_id}\', \'{cat}\')">{cat} ({count})</button>')
    return '\\n        '.join(pills)

def main():
    print(">>> Démarrage de l'assemblage de docs/usecases/index.html...")

    total_ucs = len(APP1_USECASES) + len(APP2_USECASES) + len(APP3_USECASES) + len(APP4_USECASES)
    print(f"    - App 1 : {len(APP1_USECASES)} cas d'usage")
    print(f"    - App 2 : {len(APP2_USECASES)} cas d'usage")
    print(f"    - App 3 : {len(APP3_USECASES)} cas d'usage")
    print(f"    - App 4 : {len(APP4_USECASES)} cas d'usage")
    print(f"    - Total : {total_ucs} cas d'usage avec simulateurs de wireframes")

    app1_pills = generate_category_pills('app1', APP1_USECASES)
    app2_pills = generate_category_pills('app2', APP2_USECASES)
    app3_pills = generate_category_pills('app3', APP3_USECASES)
    app4_pills = generate_category_pills('app4', APP4_USECASES)

    html_content = f"""<!DOCTYPE html>
<html lang="fr" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AeterniTrak V1.0 — Architecture 4 Applications & Studio Vivant des Wireframes</title>
  <style>
{CSS_STYLES}
  </style>
</head>
<body>

  <!-- En-tête Global Solennel -->
  <header>
    <div class="flex items-center gap-3">
      <span class="text-2xl select-none">🏛️</span>
      <div>
        <div class="flex items-center gap-2">
          <h1 class="text-lg font-extrabold font-title tracking-tight text-white">AeterniTrak <span class="text-gold-400 text-xs font-mono font-bold px-1.5 py-0.5 rounded border border-gold-500/30 bg-gold-500/10">V1.0</span></h1>
          <span class="text-[10px] text-slate-400 border-l border-slate-700 pl-2">Référentiel Fonctionnel & Studio Vivant des Wireframes</span>
        </div>
        <p class="text-xs text-slate-400">Le Pax Funèbre • 4 Applications Multiplateformes Étanches • Spec-First & Test-First Certifié</p>
      </div>
    </div>

    <!-- Badges Métriques & Statut -->
    <div class="flex flex-wrap items-center gap-2 text-xs">
      <div class="bg-emerald-950/40 border border-emerald-500/30 text-emerald-400 px-2.5 py-1 rounded-lg flex items-center gap-1.5 font-mono text-[11px]">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <strong id="badge-vectors">693 Vecteurs</strong>
        <span class="text-emerald-500/80">• 100% Validé</span>
      </div>
      <div class="bg-gold-500/10 border border-gold-500/30 text-gold-300 px-2.5 py-1 rounded-lg flex items-center gap-1.5 text-[11px]">
        <span>📐</span> <strong>46 Wireframes Dédiés (4 États)</strong>
      </div>
      <div class="bg-blue-950/40 border border-blue-500/30 text-blue-300 px-2.5 py-1 rounded-lg flex items-center gap-1.5 text-[11px]">
        <span>🌍</span> <strong>100% Multiplateforme</strong>
      </div>
      <div class="bg-indigo-950/40 border border-indigo-500/30 text-indigo-300 px-2.5 py-1 rounded-lg flex items-center gap-1.5 text-[11px]">
        <span>🛡️</span> <strong>ACOSJ 92k EEPROM</strong>
      </div>
      <a href="../architecture/index.html" class="bg-gold-500/10 border border-gold-500/40 hover:bg-gold-500/20 text-gold-300 px-2.5 py-1 rounded-lg flex items-center gap-1.5 text-[11px] transition" style="text-decoration:none;">
        <span>📐</span> <strong>Portail UML 3-Tiers</strong>
      </a>
    </div>
  </header>

  <!-- Bannière d'Universalité Multiplateforme (DEC-AET-09) -->
  <div class="bg-gradient-to-r from-obsidian-900 via-slate-900 to-obsidian-900 border-b border-slate-800 px-6 py-2.5 flex flex-wrap items-center justify-between text-xs text-slate-300 gap-3">
    <div class="flex items-center gap-2">
      <span class="text-gold-400 font-bold">Matrice d'Exécution Universelle :</span>
      <span class="text-slate-400">Les 4 applications s'exécutent avec le même niveau d'excellence sur tous les terminaux :</span>
    </div>
    <div class="flex flex-wrap items-center gap-3 font-mono text-[11px]">
      <span class="flex items-center gap-1 text-emerald-400 bg-emerald-950/40 px-2 py-0.5 rounded border border-emerald-800/40">📱 Android (NFC IsoDep & StrongBox)</span>
      <span class="flex items-center gap-1 text-slate-200 bg-slate-800/60 px-2 py-0.5 rounded border border-slate-700/60">🍎 iOS & iPadOS (CoreNFC & Secure Enclave)</span>
      <span class="flex items-center gap-1 text-sky-400 bg-sky-950/40 px-2 py-0.5 rounded border border-sky-800/40">🌐 Web PWA (Offline & WebCrypto/WebAudio)</span>
      <span class="flex items-center gap-1 text-amber-400 bg-amber-950/40 px-2 py-0.5 rounded border border-amber-800/40">💻 Desktop Mac/Win/Linux (WebUSB & ACR1552U)</span>
      <span class="text-gold-300 font-bold">~85% Code Partagé AeterniCore</span>
    </div>
  </div>

  <!-- Navigation par Onglets Métiers & Recherche -->
  <div class="bg-obsidian-900 border-b border-slate-800/80 px-6 py-3 flex flex-wrap items-center justify-between gap-4">
    <nav class="flex flex-wrap gap-1.5" id="nav-tabs">
      <button onclick="switchTab('app1')" id="tab-app1" class="tab-btn px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 bg-gold-500 text-obsidian-950 shadow-md shadow-gold-500/20">
        <span>🎨</span> App 1 : PaxStudio Design
        <span class="bg-black/20 text-[10px] px-1.5 py-0.2 rounded-full font-mono">{len(APP1_USECASES)} UC</span>
      </button>
      <button onclick="switchTab('app2')" id="tab-app2" class="tab-btn px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 text-slate-400 hover:text-white hover:bg-slate-800/50">
        <span>🖨️</span> App 2 : PaxStation Encodage
        <span class="bg-slate-800 text-[10px] px-1.5 py-0.2 rounded-full font-mono">{len(APP2_USECASES)} UC</span>
      </button>
      <button onclick="switchTab('app3')" id="tab-app3" class="tab-btn px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 text-slate-400 hover:text-white hover:bg-slate-800/50">
        <span>🕊️</span> App 3 : Sanctuaire Mémoriel
        <span class="bg-slate-800 text-[10px] px-1.5 py-0.2 rounded-full font-mono">{len(APP3_USECASES)} UC</span>
      </button>
      <button onclick="switchTab('app4')" id="tab-app4" class="tab-btn px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 text-slate-400 hover:text-white hover:bg-slate-800/50">
        <span>🪰</span> App 4 : Filière & Traçabilité
        <span class="bg-slate-800 text-[10px] px-1.5 py-0.2 rounded-full font-mono">{len(APP4_USECASES)} UC</span>
      </button>
      <button onclick="switchTab('legal')" id="tab-legal" class="tab-btn px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 text-slate-400 hover:text-white hover:bg-slate-800/50">
        <span>⚖️</span> Référentiel Juridique
        <span class="bg-slate-800 text-[10px] px-1.5 py-0.2 rounded-full font-mono">{len(LEGAL_TEXTS)} Textes</span>
      </button>
    </nav>

    <!-- Recherche Instantanée -->
    <div class="relative w-full sm:w-80">
      <input type="text" id="searchInput" oninput="filterUseCases()" placeholder="Filtrer par mot-clé (ex: pacemaker, lfa, android, ios, 92k...)" class="w-full bg-obsidian-950 border border-slate-800 rounded-xl px-4 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-gold-500 transition pr-8">
      <span class="absolute right-2.5 top-2.5 text-slate-500 text-xs">🔍</span>
    </div>
  </div>

  <!-- Contenu Principal -->
  <main class="flex-1 p-6 max-w-7xl mx-auto w-full space-y-6">

    <!-- Onglet 1 : App 1 PaxStudio Design -->
    <section id="section-app1" class="tab-content space-y-6">
      <div class="bg-gradient-to-r from-obsidian-850 to-slate-900 border border-gold-500/20 rounded-2xl p-6 relative overflow-hidden">
        <div class="max-w-3xl space-y-2 relative z-10">
          <div class="flex flex-wrap items-center gap-2">
            <span class="text-xs uppercase font-extrabold tracking-wider text-gold-400">Application 1 · Outil Créatif & Pré-Encodage (Famille & Conseiller)</span>
            <span class="text-[10px] font-mono bg-gold-500/10 text-gold-300 border border-gold-500/20 px-2 py-0.5 rounded">Multiplateforme : Web • Android • iOS • Mac • Windows</span>
          </div>
          <h2 class="text-2xl font-bold font-title text-white">PaxStudio Design — Personnalisation des 2 Cartes & Médaillons</h2>
          <p class="text-sm text-slate-300 leading-relaxed">
            L'espace de co-création visuelle et mémorielle pour la famille et son conseiller funéraire. Permet le design recto/verso des deux cartes (Carte Sanctuaire mémorielle et Carte Directives médicales/civiles), le choix des finitions dorées, la prévisualisation 3D temps réel, le carrousel photo 220x220 WebP, l'oscilloscope vocal et la génération de la <strong>capsule de pré-encodage scellée</strong> prête pour l'agence.
          </p>
          <div class="flex flex-wrap gap-2 pt-2 text-xs">
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">🎨 Carte Sanctuaire & Directives</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">🧊 Prévisualisation 3D PBR</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">📸 Portraits WebP (STORAGE-001)</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">🎙️ Oscilloscope Vocal Waveform</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">📦 Export Capsule CBOR Validée</span>
          </div>
        </div>
      </div>

      <!-- Barre d'Outils Ergonomique (Modes d'Affichage & Filtres Métiers) -->
      <div class="view-mode-bar">
        <div class="flex flex-wrap items-center gap-2">
          <span class="text-xs font-mono font-bold text-gold-400">Mode d'Affichage :</span>
          <button id="btn-mode-app1-cards" class="view-mode-btn active" onclick="setViewMode('app1', 'cards')">🎴 Fiches & Simulateurs</button>
          <button id="btn-mode-app1-board" class="view-mode-btn" onclick="setViewMode('app1', 'board')">📐 Board 4 Écrans Dépliés</button>
          <button id="btn-mode-app1-table" class="view-mode-btn" onclick="setViewMode('app1', 'table')">📋 Tableau d'Audit</button>
        </div>
        <div class="flex items-center gap-3">
          <button onclick="toggleAllSimulations('app1')" class="wf-sim-btn">⚡ Lancer Toutes les Simulations</button>
        </div>
      </div>

      <!-- Filtres par Catégorie Métier -->
      <div class="flex flex-wrap gap-1.5" id="cat-filters-app1">
        {app1_pills}
      </div>

      <!-- Conteneur Dynamique App 1 -->
      <div id="grid-app1"></div>
    </section>

    <!-- Onglet 2 : App 2 PaxStation Encodage Silicium -->
    <section id="section-app2" class="tab-content hidden space-y-6">
      <div class="bg-gradient-to-r from-obsidian-850 to-slate-900 border border-indigo-500/20 rounded-2xl p-6 relative overflow-hidden">
        <div class="max-w-3xl space-y-2 relative z-10">
          <div class="flex flex-wrap items-center gap-2">
            <span class="text-xs uppercase font-extrabold tracking-wider text-indigo-400">Application 2 · Station Technique Professionnelle (Membres PaxFunèbre en Agence)</span>
            <span class="text-[10px] font-mono bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 px-2 py-0.5 rounded">Multiplateforme : Navigateurs Chromium Desktop (WebUSB) • Applications Natives PC/SC</span>
          </div>
          <h2 class="text-2xl font-bold font-title text-white">PaxStation Encodage Silicium — Gravure Sécurisée ACR1552U</h2>
          <p class="text-sm text-slate-300 leading-relaxed">
            La station d'encodage physique réservée aux opérateurs et membres du réseau Le Pax Funèbre. Connectée au lecteur de bureau <strong>ACR1552U en WebUSB / PC/SC</strong>. Assure les dialogues IsoDep APDU bas niveau, l'allocation EEPROM de la puce <strong>JavaCard ACOSJ 92 Ko</strong>, le scellement cryptographique COSE_Sign1, le contrôle anti-malléabilité du s bas, le verrouillage matériel in-silico et le pilotage de l'imprimante thermique haute résolution.
          </p>
          <div class="flex flex-wrap gap-2 pt-2 text-xs">
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">🔌 ACR1552U WebUSB / PC/SC</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">💾 JavaCard ACOSJ 92 Ko APDU</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">🔐 Scellement COSE_Sign1 Ed25519</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">🔒 Verrouillage Matériel Anti-Tamper</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">🖨️ Impression Thermique 600 DPI</span>
          </div>
        </div>
      </div>

      <!-- Barre d'Outils Ergonomique -->
      <div class="view-mode-bar">
        <div class="flex flex-wrap items-center gap-2">
          <span class="text-xs font-mono font-bold text-gold-400">Mode d'Affichage :</span>
          <button id="btn-mode-app2-cards" class="view-mode-btn active" onclick="setViewMode('app2', 'cards')">🎴 Fiches & Simulateurs</button>
          <button id="btn-mode-app2-board" class="view-mode-btn" onclick="setViewMode('app2', 'board')">📐 Board 4 Écrans Dépliés</button>
          <button id="btn-mode-app2-table" class="view-mode-btn" onclick="setViewMode('app2', 'table')">📋 Tableau d'Audit</button>
        </div>
        <div class="flex items-center gap-3">
          <button onclick="toggleAllSimulations('app2')" class="wf-sim-btn">⚡ Lancer Toutes les Simulations</button>
        </div>
      </div>

      <!-- Filtres par Catégorie Métier -->
      <div class="flex flex-wrap gap-1.5" id="cat-filters-app2">
        {app2_pills}
      </div>

      <!-- Conteneur Dynamique App 2 -->
      <div id="grid-app2"></div>
    </section>

    <!-- Onglet 3 : App 3 Sanctuaire Mémoriel Mobile -->
    <section id="section-app3" class="tab-content hidden space-y-6">
      <div class="bg-gradient-to-r from-obsidian-850 to-slate-900 border border-purple-500/20 rounded-2xl p-6 relative overflow-hidden">
        <div class="max-w-3xl space-y-2 relative z-10">
          <div class="flex flex-wrap items-center gap-2">
            <span class="text-xs uppercase font-extrabold tracking-wider text-purple-400">Application 3 · Grand Public Mobile & PWA Offline (Participants & Familles)</span>
            <span class="text-[10px] font-mono bg-purple-500/10 text-purple-300 border border-purple-500/20 px-2 py-0.5 rounded">Multiplateforme : iOS CoreNFC • Android NFC • Web NFC Chrome • PWA Hors-Ligne</span>
          </div>
          <h2 class="text-2xl font-bold font-title text-white">Sanctuaire Mémoriel Mobile — Recueillement & Directives</h2>
          <p class="text-sm text-slate-300 leading-relaxed">
            L'application universelle de recueillement destinée aux familles et proches du défunt. Déclenchée instantanément par simple <strong>tap NFC sans aucun mot de passe</strong> (Zéro Login). Procède à la vérification cryptographique décentralisée COSE_Sign1, applique le bandeau de réserve DEC-AET-07 Option B en cas d'émetteur inconnu, orchestre le sanctuaire acoustique avec ducking vocal automatique (-14 dB), et garantit la consultation solennelle des volontés civiles et des directives d'urgence (alerte pacemaker Art. L1232-17 CDLD, don d'organes, legs à la science).
          </p>
          <div class="flex flex-wrap gap-2 pt-2 text-xs">
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">📱 NFC Instantané Zéro Login</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">🔐 Vérification Ed25519 / ES256</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">🎙️ Ducking Vocal Vivant</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">📜 Consultation Volontés Civiles</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">⚠️ Alerte Vitale Pacemaker CDLD</span>
          </div>
        </div>
      </div>

      <!-- Barre d'Outils Ergonomique -->
      <div class="view-mode-bar">
        <div class="flex flex-wrap items-center gap-2">
          <span class="text-xs font-mono font-bold text-gold-400">Mode d'Affichage :</span>
          <button id="btn-mode-app3-cards" class="view-mode-btn active" onclick="setViewMode('app3', 'cards')">🎴 Fiches & Simulateurs</button>
          <button id="btn-mode-app3-board" class="view-mode-btn" onclick="setViewMode('app3', 'board')">📐 Board 4 Écrans Dépliés</button>
          <button id="btn-mode-app3-table" class="view-mode-btn" onclick="setViewMode('app3', 'table')">📋 Tableau d'Audit</button>
        </div>
        <div class="flex items-center gap-3">
          <button onclick="toggleAllSimulations('app3')" class="wf-sim-btn">⚡ Lancer Toutes les Simulations</button>
        </div>
      </div>

      <!-- Filtres par Catégorie Métier -->
      <div class="flex flex-wrap gap-1.5" id="cat-filters-app3">
        {app3_pills}
      </div>

      <!-- Conteneur Dynamique App 3 -->
      <div id="grid-app3"></div>
    </section>

    <!-- Onglet 4 : App 4 Filière & Traçabilité -->
    <section id="section-app4" class="tab-content hidden space-y-6">
      <div class="bg-gradient-to-r from-obsidian-850 to-slate-900 border border-emerald-500/20 rounded-2xl p-6 relative overflow-hidden">
        <div class="max-w-3xl space-y-2 relative z-10">
          <div class="flex flex-wrap items-center gap-2">
            <span class="text-xs uppercase font-extrabold tracking-wider text-emerald-400">Application 4 · Filière Métier & Traçabilité Industrielle (Vétérinaires, Gardes DNF & AFSCA)</span>
            <span class="text-[10px] font-mono bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 px-2 py-0.5 rounded">Multiplateforme : Terminaux durcis IP68 • PWA Offline • Moteur AeterniCore CLI</span>
          </div>
          <h2 class="text-2xl font-bold font-title text-white">Filière Sarcomusation & Traçabilité Post-Décès</h2>
          <p class="text-sm text-slate-300 leading-relaxed">
            La chaîne logistique et sanitaire complète régissant la décomposition biologique par les larves d'<em>Hermetia illucens</em> (mouche soldat noire). Assure la ségrégation des 4 profils de dépouilles (Compagnie, Faune sauvage DNF, Élevage Sanitel, Déchets abattoir MRS), le dépistage toxicologique LFA du pentobarbital (&lt; 10 ppb), la pasteurisation 70°C/1h, la stérilisation Méthode 1 (133°C, 3 bars, 20 min), et l'évaluation par l'oracle mathématique <strong>The Iron Gate (G0 à G9)</strong> garantissant le respect absolu de la règle d'or anti-prion et du feed-ban européen.
          </p>
          <div class="flex flex-wrap gap-2 pt-2 text-xs">
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">🪰 Larves Hermetia illucens (343691)</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">🧪 Dépistage LFA Pentobarbital (&lt;10 ppb)</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">♨️ Stérilisation Méthode 1 (133°C/3b)</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">🛡️ The Iron Gate (G0-G9 Anti-Prion)</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">📜 Certificat de Lot Ed25519</span>
          </div>
        </div>
      </div>

      <!-- Barre d'Outils Ergonomique -->
      <div class="view-mode-bar">
        <div class="flex flex-wrap items-center gap-2">
          <span class="text-xs font-mono font-bold text-gold-400">Mode d'Affichage :</span>
          <button id="btn-mode-app4-cards" class="view-mode-btn active" onclick="setViewMode('app4', 'cards')">🎴 Fiches & Simulateurs</button>
          <button id="btn-mode-app4-board" class="view-mode-btn" onclick="setViewMode('app4', 'board')">📐 Board 4 Écrans Dépliés</button>
          <button id="btn-mode-app4-table" class="view-mode-btn" onclick="setViewMode('app4', 'table')">📋 Tableau d'Audit</button>
        </div>
        <div class="flex items-center gap-3">
          <button onclick="toggleAllSimulations('app4')" class="wf-sim-btn">⚡ Lancer Toutes les Simulations</button>
        </div>
      </div>

      <!-- Filtres par Catégorie Métier -->
      <div class="flex flex-wrap gap-1.5" id="cat-filters-app4">
        {app4_pills}
      </div>

      <!-- Conteneur Dynamique App 4 -->
      <div id="grid-app4"></div>
    </section>

    <!-- Onglet 5 : Référentiel Juridique Applicatif -->
    <section id="section-legal" class="tab-content hidden space-y-6">
      <div class="bg-gradient-to-r from-obsidian-850 to-slate-900 border border-gold-500/20 rounded-2xl p-6 relative overflow-hidden">
        <h2 class="text-2xl font-bold font-title text-white">Référentiel des Textes Juridiques Applicables (Références à confirmer par un juriste)</h2>
        <p class="text-sm text-slate-300 leading-relaxed mt-2">
          Table exhaustive des lois fédérales belges, décrets régionaux wallons et règlements européens régissant la fin de vie, la protection des données in-silico, la gestion des stimulateurs cardiaques et la traçabilité des sous-produits animaux.
        </p>
      </div>

      <div class="glass-card rounded-2xl overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <tr class="border-b border-slate-800 bg-obsidian-900/90 text-slate-400 font-mono text-[11px] uppercase tracking-wider">
                <th class="py-3 px-4">Juridiction & Acte Officiel</th>
                <th class="py-3 px-4">Dispositions Essentielles Citées</th>
                <th class="py-3 px-4">Choix de Conception AeterniTrak V1.0</th>
                <th class="py-3 px-4 text-right">Lien Documentaire</th>
              </tr>
            </thead>
            <tbody id="table-legal" class="divide-y divide-slate-850"></tbody>
          </table>
        </div>
      </div>
    </section>

  </main>

  <!-- Modale Native Haute Définition (Master Studio Wireframe Theater) -->
  <dialog id="ucModal" class="bg-transparent focus:outline-none">
    <div class="bg-obsidian-900 border border-gold-500/40 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[92vh]" id="modalContent">
      <!-- Rempli dynamiquement par openUseCaseModal() -->
    </div>
  </dialog>

  <!-- Pied de page -->
  <footer class="border-t border-slate-800/80 bg-obsidian-900 px-6 py-4 text-center text-xs text-slate-500 flex flex-wrap items-center justify-between gap-4">
    <span>AeterniTrak V1.0 • Société Le Pax Funèbre • 4 Applications Multiplateformes Étanches</span>
    <span class="font-mono text-slate-400">Spec-First & Test-First Certifié • Arbitrages Kudoro DEC-AET-08 & DEC-AET-09</span>
  </footer>

  <!-- Injection des Données et du Runtime Applicatif -->
  <script>
    const app1UseCases = {json.dumps(APP1_USECASES, ensure_ascii=False, indent=2)};
    const app2UseCases = {json.dumps(APP2_USECASES, ensure_ascii=False, indent=2)};
    const app3UseCases = {json.dumps(APP3_USECASES, ensure_ascii=False, indent=2)};
    const app4UseCases = {json.dumps(APP4_USECASES, ensure_ascii=False, indent=2)};
    const legalTexts = {json.dumps(LEGAL_TEXTS, ensure_ascii=False, indent=2)};

{JS_RUNTIME}
  </script>
</body>
</html>
"""

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "usecases", "index.html"))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Fichier généré avec succès : {output_path}")
    print(f"   Taille : {os.path.getsize(output_path):,} octets")

if __name__ == "__main__":
    main()
