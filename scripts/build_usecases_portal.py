#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeterniTrak V1.0 — Assemblage du Portail Vivant des Cas d'Usage avec Grand Théâtre Vivant
Génère docs/usecases/index.html 100% Hors-Ligne & Embarqué (Zero CDN, Zero Ressource Distante).
Conçu par Bushi 07 (Lead Cinematic & Motion) & Bushi 15 (Lead Design System & Typography).
"""

import json
import os
import sys

# Importer les modules de données et de styles
from portal_legal import LEGAL_TEXTS
from portal_app1 import APP1_USECASES
from portal_app2 import APP2_USECASES
from portal_app3 import APP3_USECASES
from portal_app4 import APP4_USECASES, TRACEABILITY_EVENTS
from portal_styles import CSS_STYLES
from portal_runtime import JS_RUNTIME

def generate_category_pills(app_id, usecases):
    cats = sorted(list(set(u['cat'] for u in usecases)))
    pills = [f'<button class="cat-filter-btn active cat-filter-{app_id}" data-cat="all" onclick="filterByCategory(\'{app_id}\', \'all\')">Tous ({len(usecases)})</button>']
    for cat in cats:
        count = sum(1 for u in usecases if u['cat'] == cat)
        pills.append(f'<button class="cat-filter-btn cat-filter-{app_id}" data-cat="{cat}" onclick="filterByCategory(\'{app_id}\', \'{cat}\')">{cat} ({count})</button>')
    return '\n        '.join(pills)

def generate_interactive_theater():
    return """
  <!-- =========================================================================
       LE GRAND THÉÂTRE INTERACTIF & STUDIO VIVANT AETERNITRAK
       ========================================================================= -->
  <section id="interactive-theater" class="glass-card p-6 md:p-8 space-y-6 relative overflow-hidden border-gold-500/40 shadow-2xl">
    <!-- En-tête du Théâtre avec Sélecteur Mode Famille / Mode Ingénieur -->
    <div class="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-5">
      <div>
        <div class="flex items-center gap-2.5">
          <span class="text-3xl select-none">🎭</span>
          <h2 class="text-xl sm:text-2xl font-bold font-title text-white">Le Grand Théâtre Vivant AeterniTrak</h2>
          <span class="px-3 py-1 rounded-full font-mono text-xs font-bold text-gold-300 bg-gold-500/15 border border-gold-500/30">Studio Temps Réel 2026</span>
        </div>
        <p class="text-xs sm:text-sm text-slate-300 mt-1" id="portal-mode-desc">
          Basculez entre le Mode Famille (solennel, sensible et sans jargon) et le Mode Ingénieur (spécifications in-silico, APDU, cryptographie, Iron Gate).
        </p>
      </div>

      <!-- Capsule Bimodale : Mode Famille vs Mode Ingénieur -->
      <div class="flex items-center gap-3">
        <div class="bimodal-toggle-box">
          <button id="btn-mode-family" class="bimodal-btn active-family" onclick="setReadingMode('family')">
            <span>🕊️</span> Mode Famille
          </button>
          <button id="btn-mode-engineer" class="bimodal-btn" onclick="setReadingMode('engineer')">
            <span>⚙️</span> Mode Ingénieur
          </button>
        </div>
      </div>
    </div>

    <!-- Navigation des 5 Expériences Clés -->
    <div class="flex flex-wrap gap-2.5 border-b border-slate-800 pb-4">
      <button id="hero-tab-expA" class="hero-nav-btn active" onclick="switchHeroExp('expA')">
        <span>📱</span> Exp A : Sanctuaire Mobile & Flamme
      </button>
      <button id="hero-tab-expB" class="hero-nav-btn" onclick="switchHeroExp('expB')">
        <span>🎴</span> Exp B : Carte 3D PaxFunèbre
      </button>
      <button id="hero-tab-expC" class="hero-nav-btn" onclick="switchHeroExp('expC')">
        <span>🖨️</span> Exp C : PaxStation & ACR1552U
      </button>
      <button id="hero-tab-expD" class="hero-nav-btn" onclick="switchHeroExp('expD')">
        <span>🪰</span> Exp D : Cassette LFA & The Iron Gate
      </button>
      <button id="hero-tab-expE" class="hero-nav-btn" onclick="switchHeroExp('expE')">
        <span>⛓️</span> Exp E : Traçabilité Dépouille (6 Événements)
      </button>
    </div>

    <!-- PANELS DES 4 EXPÉRIENCES -->
    <div class="hero-panels-container">

      <!-- EXPÉRIENCE A : SANCTUAIRE MOBILE & FLAMME MÉMORIELLE -->
      <div id="hero-panel-expA" class="hero-panel active">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          
          <!-- Mockup Smartphone Titanium (5/12) -->
          <div class="lg:col-span-5 flex justify-center">
            <div class="phone-mockup">
              <div class="phone-screen">
                <!-- Dynamic Island -->
                <div class="phone-dynamic-island">
                  <span class="text-emerald-400 font-bold">09:41</span>
                  <span class="text-[10px] text-gold-300">● Sanctuaire</span>
                  <div class="flex items-center gap-1 text-[10px] text-slate-300">
                    <span>5G</span>
                    <div class="w-3.5 h-2 border border-slate-300 rounded-sm p-[1px]"><div class="w-full h-full bg-emerald-400"></div></div>
                  </div>
                </div>

                <!-- Écran de Recueillement -->
                <div class="p-4 flex flex-col items-center justify-between flex-1 text-center space-y-3">
                  <div class="space-y-1">
                    <span class="text-xs font-mono uppercase tracking-widest text-gold-400 font-bold">Tap NFC Zéro Login</span>
                    <h4 class="text-base font-bold font-title text-white">Sanctuaire Mémoriel</h4>
                    <p class="text-xs text-slate-300">Adrien de Valcourt (1942 — 2026)</p>
                  </div>

                  <!-- Flamme Mémorielle SVG Animée -->
                  <div class="relative w-20 h-24 flex items-center justify-center my-1">
                    <div class="absolute w-16 h-16 rounded-full bg-amber-500/25 blur-xl animate-pulse-slow"></div>
                    <svg viewBox="0 0 100 140" class="w-16 h-20 flame-animated">
                      <defs>
                        <radialGradient id="flameGrad" cx="50%" cy="80%" r="60%">
                          <stop offset="0%" stop-color="#ffffff" />
                          <stop offset="25%" stop-color="#fef08a" />
                          <stop offset="55%" stop-color="#f59e0b" />
                          <stop offset="85%" stop-color="#dc2626" />
                          <stop offset="100%" stop-color="transparent" />
                        </radialGradient>
                        <radialGradient id="innerCore" cx="50%" cy="85%" r="40%">
                          <stop offset="0%" stop-color="#ffffff" />
                          <stop offset="60%" stop-color="#fef08a" />
                          <stop offset="100%" stop-color="#f59e0b" />
                        </radialGradient>
                      </defs>
                      <path d="M50,10 C58,40 85,70 85,95 C85,115 70,135 50,135 C30,135 15,115 15,95 C15,70 42,40 50,10 Z" fill="url(#flameGrad)" />
                      <path d="M50,45 C54,65 70,85 70,105 C70,120 60,130 50,130 C40,130 30,120 30,105 C30,85 46,65 50,45 Z" fill="url(#innerCore)" opacity="0.9" />
                    </svg>
                    <div class="absolute -bottom-1 w-2.5 h-3 bg-slate-600 rounded-t-sm"></div>
                  </div>

                  <!-- Lecteur Vocal & Oscilloscope Waveform -->
                  <div class="w-full bg-obsidian-900 border border-gold-500/30 rounded-xl p-3 space-y-2">
                    <div class="flex items-center justify-between text-xs font-mono text-slate-400">
                      <span>Message Vocal du Défunt</span>
                      <span class="text-gold-300 font-bold">01:42</span>
                    </div>
                    <div class="h-8 flex items-center justify-between gap-1 px-1">
                      <div class="osc-bar"></div><div class="osc-bar"></div>
                      <div class="osc-bar"></div><div class="osc-bar"></div>
                      <div class="osc-bar"></div><div class="osc-bar"></div>
                      <div class="osc-bar"></div><div class="osc-bar"></div>
                      <div class="osc-bar"></div><div class="osc-bar"></div>
                      <div class="osc-bar"></div><div class="osc-bar"></div>
                      <div class="osc-bar"></div><div class="osc-bar"></div>
                    </div>
                  </div>

                  <button id="memorial-play-btn" onclick="toggleMemorialAudio()" class="wf-btn wf-btn-gold text-xs font-bold w-full py-2">
                    ▶ Écouter le Message
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Description Métier & Tiroir de Directives (7/12) -->
          <div class="lg:col-span-7 space-y-5">
            <div class="space-y-2">
              <div class="flex items-center gap-2">
                <span class="text-xs uppercase font-mono tracking-widest text-gold-400 font-bold">Expérience Grand Public</span>
                <span id="ducking-indicator" class="font-mono text-xs text-slate-400 bg-slate-900 px-2.5 py-0.5 rounded-full border border-slate-700">
                  🔇 Veille
                </span>
              </div>
              <h3 class="text-2xl font-bold font-title text-white">Le Sanctuaire Mémoriel Mobile & Vocal</h3>
              <p class="text-sm text-slate-300 leading-relaxed">
                Conçu pour offrir à la famille et aux proches un recueillement solennel, intime et universel. Aucun compte utilisateur requis, aucun identifiant sur le cloud : le simple effleurement NFC déclenche la lecture sécurisée in-silico de la carte physique.
              </p>
            </div>

            <!-- Tiroir des Directives & Volontés Civiles -->
            <div class="bg-obsidian-950/90 border border-slate-800 rounded-xl p-4 space-y-3">
              <button onclick="toggleMemorialDrawer()" class="flex items-center justify-between w-full text-left font-bold text-sm text-gold-300 hover:text-gold-200">
                <span>📜 Directives & Volontés Enregistrées par Adrien</span>
                <span id="memorial-drawer-icon" class="text-xs">▼</span>
              </button>
              <div id="memorial-drawer-content" class="hidden space-y-2 pt-2 border-t border-slate-800/80 text-xs text-slate-300">
                <div class="flex items-center justify-between p-2 rounded bg-slate-900 border border-slate-800">
                  <span>Mode de Sépulture : <strong>Inhumation Naturelle (Biolande)</strong></span>
                  <span class="text-emerald-400 font-mono">Conforme (référence à confirmer par un juriste)</span>
                </div>
                <div class="flex items-center justify-between p-2 rounded bg-slate-900 border border-slate-800">
                  <span>Don d'Organes : <strong>Favorable (Sensibilisation familiale)</strong></span>
                  <span class="text-emerald-400 font-mono">Loi 13 Juin 1986 (référence à confirmer par un juriste)</span>
                </div>
                <div class="p-2.5 rounded bg-red-950/30 border border-red-500/50 text-red-200 flex items-center gap-2">
                  <span class="text-lg">⚠️</span>
                  <span><strong>Alerte Vitale :</strong> Porteur d'un stimulateur cardiaque (Pacemaker). Explantation obligatoire avant toute crémation.</span>
                </div>
              </div>
            </div>

            <div class="flex flex-wrap gap-2 text-xs font-mono text-slate-400">
              <span class="bg-slate-900 px-3 py-1 rounded border border-slate-800">🌐 100% Hors-Ligne</span>
              <span class="bg-slate-900 px-3 py-1 rounded border border-slate-800">🔐 Signature Ed25519</span>
              <span class="bg-slate-900 px-3 py-1 rounded border border-slate-800">🎧 Ducking Vocal Automatique</span>
            </div>
          </div>

        </div>
      </div>

      <!-- EXPÉRIENCE B : CARTE 3D PAXFUNÈBRE RÉVERSIBLE -->
      <div id="hero-panel-expB" class="hero-panel">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          
          <!-- Carte 3D Perspective (6/12) -->
          <div class="lg:col-span-6 flex flex-col items-center space-y-4">
            <div class="card-3d-scene" onclick="toggleCard3DFlip()">
              <div class="card-3d-inner" id="card-3d-element">

                <!-- Face Recto : Sanctuaire & Portrait -->
                <div class="card-3d-face card-3d-front card-face-front">
                  <div class="flex items-start justify-between">
                    <div class="flex items-center gap-2">
                      <span class="text-2xl">🕊️</span>
                      <div>
                        <div class="text-xs uppercase font-mono tracking-widest text-gold-300 font-bold">Le Pax Funèbre</div>
                        <div class="text-xs text-slate-400 font-serif">Carte Sanctuaire Mémorielle</div>
                      </div>
                    </div>
                    <div class="chip-gold" title="Puce Silicium ACOSJ 92K EEPROM">
                      <div></div><div></div><div></div>
                      <div></div><div></div><div></div>
                    </div>
                  </div>

                  <div class="flex items-center gap-4 my-2">
                    <div class="w-16 h-16 rounded-xl border-2 border-gold-400/80 bg-slate-900 overflow-hidden flex items-center justify-center shadow-lg relative">
                      <span class="text-3xl select-none">👤</span>
                      <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                    </div>
                    <div>
                      <div class="text-lg font-bold font-title text-white tracking-wide">Adrien de Valcourt</div>
                      <div class="text-xs text-gold-400 font-mono">1942 — 2026 • Liège, Belgique</div>
                      <div class="text-xs text-slate-300 italic mt-0.5">« Toujours vivant dans la lumière de nos cœurs »</div>
                    </div>
                  </div>

                  <div class="flex items-center justify-between text-xs font-mono border-t border-gold-500/30 pt-2 text-slate-400">
                    <span class="text-emerald-400 font-bold">NFC NDEF • Zéro Login</span>
                    <span class="text-gold-300 font-bold">ID: PAX-2026-0842-MEM</span>
                  </div>
                </div>

                <!-- Face Verso : Directives Civiles & Puce ACOSJ -->
                <div class="card-3d-face card-3d-back card-face-back">
                  <div class="flex items-start justify-between">
                    <div class="flex items-center gap-2">
                      <span class="text-2xl">⚖️</span>
                      <div>
                        <div class="text-xs uppercase font-mono tracking-widest text-emerald-400 font-bold">Volontés Civiles & Médicales</div>
                        <div class="text-xs text-slate-400">Volontés funéraires (référence à confirmer par un juriste)</div>
                      </div>
                    </div>
                    <span class="text-xs font-mono text-emerald-400 bg-emerald-950/80 px-2 py-0.5 rounded border border-emerald-500/40">Scellé Ed25519</span>
                  </div>

                  <div class="bg-red-950/50 border border-red-500/70 rounded-lg p-2.5 my-1 flex items-center gap-2.5">
                    <span class="text-2xl">⚠️</span>
                    <div>
                      <div class="text-xs font-bold text-red-200 uppercase font-mono tracking-wider">Alerte Médicale Vitale</div>
                      <div class="text-xs text-red-300 font-medium">Porteur de Pacemaker. Explantation obligatoire avant crémation.</div>
                    </div>
                  </div>

                  <div class="flex items-center justify-between text-xs text-slate-300">
                    <div>
                      <div class="font-bold text-white text-sm">Inhumation Naturelle</div>
                      <div class="text-slate-400 text-xs">Don d'organes : Favorable • Cérémonie Laïque</div>
                    </div>
                    <div class="w-12 h-12 bg-white rounded p-1 flex items-center justify-center shadow">
                      <svg viewBox="0 0 24 24" class="w-full h-full fill-black">
                        <path d="M2,2H10V10H2V2M4,4V8H8V4H4M14,2H22V10H14V2M16,4V8H20V4H16M2,14H10V22H2V14M4,16V20H8V16H4M14,14H16V16H14V14M18,14H20V16H18V14M20,16H22V18H20V16M14,18H16V20H14V18M18,18H20V20H18V18M16,16H18V18H16V16M20,20H22V22H20V20M14,20H16V22H14V20M16,20H18V22H16V20Z"/>
                      </svg>
                    </div>
                  </div>

                  <div class="flex items-center justify-between text-xs font-mono border-t border-slate-700 pt-2 text-slate-400">
                    <span>ACOSJ 92K JavaCard</span>
                    <span class="text-emerald-400 font-bold">SHA256: 7d4a...b189</span>
                  </div>
                </div>

              </div>
            </div>

            <!-- Boutons de Retournement & Finitions Nobles -->
            <div class="flex flex-wrap items-center gap-3">
              <button id="card-flip-btn" onclick="toggleCard3DFlip()" class="wf-btn wf-btn-gold text-xs font-bold">
                🔄 Retourner la Carte (Verso Directives & Puce)
              </button>
              <div class="flex items-center gap-1.5">
                <button onclick="setCard3DFinish('gold')" class="wf-btn wf-btn-sub text-xs">Or Satiné</button>
                <button onclick="setCard3DFinish('obsidian')" class="wf-btn wf-btn-sub text-xs">Obsidienne</button>
              </div>
            </div>
          </div>

          <!-- Description & Cartographie Mémoire (6/12) -->
          <div class="lg:col-span-6 space-y-4">
            <h3 class="text-2xl font-bold font-title text-white">La Carte PaxFunèbre Réversible CR-80</h3>
            <p class="text-sm text-slate-300 leading-relaxed">
              Le support matériel sacré alliant haute horlogerie funéraire et silicium cryptographique de grade bancaire. Équipée de la puce <strong>ACOSJ JavaCard 92 Ko EEPROM</strong>, elle conserve le double recto/verso : d'un côté la mémoire affective pour les proches, de l'autre les volontés juridiques inviolables pour les soignants et officiers d'état civil.
            </p>

            <div class="bg-obsidian-950 border border-slate-800 rounded-xl p-4 space-y-2 text-xs font-mono">
              <div class="text-gold-400 font-bold uppercase text-[11px]">Cartographie Silicium ACOSJ 92K :</div>
              <div class="flex justify-between border-b border-slate-800/60 pb-1.5 text-slate-300">
                <span>EF.DIR (0x2F00)</span>
                <span>Descripteur AID AeterniTrak</span>
                <span class="text-emerald-400">128 octets</span>
              </div>
              <div class="flex justify-between border-b border-slate-800/60 pb-1.5 text-slate-300">
                <span>EF.PROFILE (0x0001)</span>
                <span>Capsule Mémorielle CBOR + WebP</span>
                <span class="text-emerald-400">62.1 Ko</span>
              </div>
              <div class="flex justify-between border-b border-slate-800/60 pb-1.5 text-slate-300">
                <span>EF.SIG (0x0002)</span>
                <span>Signature COSE_Sign1 Ed25519</span>
                <span class="text-emerald-400">64 octets</span>
              </div>
              <div class="flex justify-between text-slate-400 pt-1">
                <span>EEPROM Libre</span>
                <span>Réserve d'expansion & Logs</span>
                <span class="text-gold-300 font-bold">29.7 Ko</span>
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- EXPÉRIENCE C : PAXSTATION ENCODAGE & LECTEUR ACR1552U -->
      <div id="hero-panel-expC" class="hero-panel">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          
          <!-- Mockup Lecteur ACR1552U (6/12) -->
          <div class="lg:col-span-6 space-y-4">
            <div class="reader-mockup">
              <!-- Carte en attente de descente -->
              <div id="paxstation-card-dock" class="w-48 h-28 mx-auto rounded-xl border border-gold-500/50 bg-gradient-to-r from-obsidian-900 to-slate-900 p-2 shadow-2xl flex flex-col justify-between">
                <div class="flex justify-between items-center text-[10px] font-mono text-gold-400">
                  <span>ACOSJ 92K</span>
                  <span>PAX-2026-0842</span>
                </div>
                <div class="text-center font-title text-xs text-white">Carte Prête pour Gravure</div>
                <div class="text-[9px] font-mono text-slate-500 text-right">WebUSB Ready</div>
              </div>

              <!-- Zone Cible Sans Contact -->
              <div class="nfc-target-zone" onclick="startPaxStationEncoding()">
                <div class="sonar-ring"></div>
                <div class="sonar-ring"></div>
                <div class="sonar-ring"></div>
                <div class="text-center z-10">
                  <span class="text-2xl select-none">🛜</span>
                  <div class="text-[10px] font-mono text-sky-300 font-bold mt-1">Cible Contactless</div>
                  <div class="text-[9px] text-slate-400">ACR1552U 13.56 MHz</div>
                </div>
              </div>

              <!-- Barre d'état & LED -->
              <div class="flex items-center justify-between bg-obsidian-950 px-3 py-2 rounded-lg border border-slate-800 text-xs font-mono">
                <div class="flex items-center gap-2">
                  <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
                  <span class="text-slate-300">Alimentation USB-C OK</span>
                </div>
                <div class="flex items-center gap-2">
                  <span id="paxstation-acr-led"></span>
                  <span class="text-slate-400">Trafic APDU</span>
                </div>
              </div>

              <!-- Terminal APDU & Jauge EEPROM -->
              <div class="wf-console-log text-[11px]" id="paxstation-log">
                <div class="text-slate-400">Lecteur ACR1552U prêt sur port WebUSB...</div>
              </div>

              <div class="space-y-1">
                <div class="flex justify-between text-xs font-mono">
                  <span class="text-slate-400">Occupation EEPROM 92 Ko :</span>
                  <span class="text-gold-300 font-bold" id="paxstation-byte-text">0 / 92 160 octets (0%)</span>
                </div>
                <div class="h-2 bg-slate-800 rounded-full overflow-hidden border border-slate-700">
                  <div id="paxstation-byte-fill" class="h-full bg-gradient-to-r from-emerald-500 via-gold-400 to-sky-400 w-0 transition-all duration-300"></div>
                </div>
              </div>
            </div>

            <button id="paxstation-start-btn" onclick="startPaxStationEncoding()" class="wf-btn wf-btn-primary text-xs font-bold w-full py-2.5">
              ⚡ Poser la Carte & Lancer la Gravure Silicium (ACR1552U)
            </button>
          </div>

          <!-- Rationale Technique PaxStation (6/12) -->
          <div class="lg:col-span-6 space-y-4">
            <h3 class="text-2xl font-bold font-title text-white">PaxStation Encodage & Silicium Sécurisé</h3>
            <p class="text-sm text-slate-300 leading-relaxed">
              La station professionnelle en salon funéraire connectée au lecteur de référence <strong>ACS ACR1552U</strong> via l'API WebUSB ou le pilote PC/SC natif. Elle exécute la chaîne d'authentification mutuelle ISO/IEC 7816-4, grave le profil sérialisé CBOR RFC 8949, applique le scellement cryptographique asymétrique Ed25519 (COSE_Sign1 Tag 18) et procède au claquage in-silico du fusible anti-tamper.
            </p>
            <div class="grid grid-cols-2 gap-3 text-xs font-mono pt-2">
              <div class="p-3 rounded-lg bg-obsidian-950 border border-slate-800">
                <span class="text-gold-400 block font-bold">IsoDep APDU 14443-4</span>
                <span class="text-slate-400 text-[11px]">Débit max 848 kbps sans contact</span>
              </div>
              <div class="p-3 rounded-lg bg-obsidian-950 border border-slate-800">
                <span class="text-sky-300 block font-bold">Verrou Anti-Tamper</span>
                <span class="text-slate-400 text-[11px]">Fusible matériel irréversible</span>
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- EXPÉRIENCE D : CASSETTE LFA TOXICOLOGIQUE & THE IRON GATE -->
      <div id="hero-panel-expD" class="hero-panel">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          
          <!-- Mockup Cassette LFA (6/12) -->
          <div class="lg:col-span-6 space-y-4">
            <div class="lfa-cassette space-y-3">
              <div class="flex justify-between items-center text-xs font-bold text-slate-700 border-b border-slate-300 pb-2">
                <span>CASSETTE IMMUNOLOGIQUE LFA-PENTO-V1</span>
                <span class="font-mono text-slate-500">LOT #HL-2026-B84</span>
              </div>

              <!-- Puits & Fenêtre de Migration -->
              <div class="flex items-center gap-4">
                <!-- Puits d'Échantillon S -->
                <div class="w-14 h-14 rounded-full border-2 border-slate-400 bg-slate-200 flex flex-col items-center justify-center relative shadow-inner">
                  <span class="text-[10px] font-mono font-bold text-slate-600">PUITS S</span>
                  <div id="lfa-droplet" class="w-3 h-3 rounded-full bg-emerald-500 absolute -top-4"></div>
                </div>

                <!-- Fenêtre Réactionnelle Membrane -->
                <div class="lfa-window flex-1 relative overflow-hidden">
                  <div id="lfa-strip-flow" class="absolute left-0 top-0 bottom-0 pointer-events-none"></div>
                  <div class="flex flex-col items-center z-10">
                    <span class="text-[11px] font-mono font-bold text-slate-700">C</span>
                    <div id="lfa-line-c" class="lfa-line-c mt-1"></div>
                  </div>
                  <div class="flex flex-col items-center z-10">
                    <span class="text-[11px] font-mono font-bold text-slate-700">T</span>
                    <div id="lfa-line-t" class="lfa-line-t mt-1"></div>
                  </div>
                </div>
              </div>

              <!-- Bannière de Résultat -->
              <div id="lfa-result-banner" class="hidden p-3 rounded-lg bg-emerald-950/80 border border-emerald-500 text-emerald-200 text-xs leading-snug">
                <strong>✔ DÉPISTAGE CONFORME :</strong> Lignes C et T visibles (principe compétitif). Absence de molécule de pentobarbital détectée dans la dépouille. Filière sarcomusation autorisée.
              </div>
            </div>

            <button id="lfa-start-btn" onclick="startLfaTest()" class="wf-btn wf-btn-gold text-xs font-bold w-full py-2.5">
              🧪 Déposer l'Échantillon & Lancer le Dépistage LFA
            </button>
          </div>

          <!-- The Iron Gate Oracle (6/12) -->
          <div class="lg:col-span-6 space-y-4">
            <h3 class="text-2xl font-bold font-title text-white">The Iron Gate (G0 à G9) & Filière Sarcomusation</h3>
            <p class="text-sm text-slate-300 leading-relaxed">
              L'oracle sanitaire déterministe régissant la filière des larves d'<em>Hermetia illucens</em>. Empêche mathématiquement tout recyclage intraspécifique (règle d'or anti-prion et feed-ban européen strict) et bloque la signature cryptographique du lot en cas de dépassement toxicologique.
            </p>

            <div class="space-y-1.5 bg-obsidian-950 border border-slate-800 rounded-xl p-4">
              <span class="text-xs uppercase font-mono text-gold-400 font-bold block mb-2">Les 10 Portes Sanitaires Infranchissables :</span>
              <div class="grid grid-cols-2 gap-2 text-xs">
                <span class="iron-gate-flag px-2 py-1 rounded font-mono bg-slate-900 border border-slate-800 text-slate-400">G0: Destination &amp; Cibles</span>
                <span class="iron-gate-flag px-2 py-1 rounded font-mono bg-slate-900 border border-slate-800 text-slate-400">G1: Taxonomie &amp; Lignage</span>
                <span class="iron-gate-flag px-2 py-1 rounded font-mono bg-slate-900 border border-slate-800 text-slate-400">G2: Protection Restes Humains</span>
                <span class="iron-gate-flag px-2 py-1 rounded font-mono bg-slate-900 border border-slate-800 text-slate-400">G3: Catégories &amp; Substrats</span>
                <span class="iron-gate-flag px-2 py-1 rounded font-mono bg-slate-900 border border-slate-800 text-slate-400">G4: Dépistage Pentobarbital</span>
                <span class="iron-gate-flag px-2 py-1 rounded font-mono bg-slate-900 border border-slate-800 text-slate-400">G5: Feed-Ban Source Ruminant</span>
                <span class="iron-gate-flag px-2 py-1 rounded font-mono bg-slate-900 border border-slate-800 text-slate-400">G6: Feed-Ban Cible Ruminant</span>
                <span class="iron-gate-flag px-2 py-1 rounded font-mono bg-slate-900 border border-slate-800 text-slate-400">G7: Règle d'Or Anti-Cannibalisme</span>
                <span class="iron-gate-flag px-2 py-1 rounded font-mono bg-slate-900 border border-slate-800 text-slate-400">G8: Feed-Ban Groupes &amp; Espèces</span>
                <span class="iron-gate-flag px-2 py-1 rounded font-mono bg-slate-900 border border-slate-800 text-slate-400">G9: Traitement Sanitaire &amp; Preuve</span>
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- EXPÉRIENCE E : GRAND SIMULATEUR ÉVÉNEMENTIEL DE TRAÇABILITÉ DE LA DÉPOUILLE (6 ÉVÉNEMENTS) -->
      <div id="hero-panel-expE" class="hero-panel">
        <div class="space-y-6">
          
          <!-- En-tête du Simulateur Événementiel & Sélecteur de Profils -->
          <div class="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
            <div>
              <div class="flex items-center gap-2">
                <span class="text-xs uppercase font-mono tracking-widest text-emerald-400 font-bold">App 4 · Filière Post-Mortem &amp; Bioconversion</span>
                <span id="trace-live-badge" class="font-mono text-xs text-emerald-300 bg-emerald-950/80 px-2.5 py-0.5 rounded-full border border-emerald-500/40">
                  ● Chaîne Active Ed25519
                </span>
              </div>
              <h3 class="text-xl sm:text-2xl font-bold font-title text-white mt-1">Simulateur Événementiel de Traçabilité de la Dépouille</h3>
              <p class="text-xs sm:text-sm text-slate-300">
                Suivi inviolable et horodaté à chaque étape : du constat médical initial au transport frigorifique (2-4°C), à la réception, aux contrôles amonts (exérèse pacemaker &amp; LFA pentobarbital), à la bioconversion Hermetia illucens et à la clôture The Iron Gate.
              </p>
            </div>

            <!-- Commandes du Simulateur (Auto-Play & Profils) -->
            <div class="flex flex-wrap items-center gap-2">
              <div class="flex items-center gap-1 bg-obsidian-950 p-1 rounded-xl border border-slate-800 text-xs font-mono">
                <button id="btn-trace-prof-p0" onclick="setTraceProfile('p0')" class="px-2.5 py-1.5 rounded-lg text-slate-300 hover:text-white">
                  👤 Profil Humain
                </button>
                <button id="btn-trace-prof-p1" onclick="setTraceProfile('p1')" class="px-2.5 py-1.5 rounded-lg font-bold bg-gold-500 text-obsidian-950 shadow">
                  🐾 Profil 1 (Compagnie)
                </button>
                <button id="btn-trace-prof-p2" onclick="setTraceProfile('p2')" class="px-2.5 py-1.5 rounded-lg text-slate-300 hover:text-white">
                  🐗 Profil 2 (Faune DNF)
                </button>
                <button id="btn-trace-prof-p3" onclick="setTraceProfile('p3')" class="px-2.5 py-1.5 rounded-lg text-slate-300 hover:text-white">
                  🐄 Profil 3 (Ferme)
                </button>
                <button id="btn-trace-prof-p4" onclick="setTraceProfile('p4')" class="px-2.5 py-1.5 rounded-lg text-slate-300 hover:text-white">
                  🏭 Profil 4 (Abattoir)
                </button>
              </div>

              <button id="btn-trace-autoplay" onclick="toggleTraceAutoPlay()" class="wf-btn wf-btn-primary text-xs font-bold py-2 px-3 flex items-center gap-1.5">
                <span>⚡</span> Auto-Play (6 Événements)
              </button>
              <button onclick="resetTraceTimeline()" class="wf-btn wf-btn-sub text-xs py-2 px-2.5" title="Réinitialiser au Décès">
                <span>↺</span>
              </button>
            </div>
          </div>

          <!-- FRISE CHRONOLOGIQUE INTERACTIVE (6 ÉVÉNEMENTS) -->
          <div class="trace-stepper-wrap">
            <div class="trace-progress-track">
              <div id="trace-progress-fill" class="trace-progress-fill" style="width: 16.66%;"></div>
            </div>
            <div class="trace-stepper" id="trace-stepper-container">
              <button class="trace-step-node active" id="trace-node-1" onclick="goToTraceStep(1)">
                <div class="trace-node-circle">📋</div>
                <div class="trace-node-label">1. Constat &amp; Scellé</div>
              </button>
              <button class="trace-step-node" id="trace-node-2" onclick="goToTraceStep(2)">
                <div class="trace-node-circle">🚐</div>
                <div class="trace-node-label">2. Transport Froid (2-4°C)</div>
              </button>
              <button class="trace-step-node" id="trace-node-3" onclick="goToTraceStep(3)">
                <div class="trace-node-circle">⚖️</div>
                <div class="trace-node-label">3. Admission &amp; Cellule</div>
              </button>
              <button class="trace-step-node" id="trace-node-4" onclick="goToTraceStep(4)">
                <div class="trace-node-circle">🩺</div>
                <div class="trace-node-label">4. Contrôles Amonts</div>
              </button>
              <button class="trace-step-node" id="trace-node-5" onclick="goToTraceStep(5)">
                <div class="trace-node-circle">🪰</div>
                <div class="trace-node-label">5. Bioconversion &amp; Chauffe</div>
              </button>
              <button class="trace-step-node" id="trace-node-6" onclick="goToTraceStep(6)">
                <div class="trace-node-circle">🕊️</div>
                <div class="trace-node-label">6. The Iron Gate &amp; Remise</div>
              </button>
            </div>
          </div>

          <!-- PANNEAU CENTRAL DE L'ÉVÉNEMENT ACTIF (2 COLONNES) -->
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

            <!-- Colonne Gauche : Formulaire Acteur & Saisie Événementielle (7/12) -->
            <div class="lg:col-span-7 space-y-4">
              <div class="trace-panel-body space-y-4">
                
                <!-- En-tête Événement & Acteur Responsable -->
                <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-3">
                  <div>
                    <span id="trace-event-stage-badge" class="text-[11px] font-mono font-bold text-gold-400 uppercase tracking-wider block">
                      Événement 1 / 6 • Déclaration Initiale
                    </span>
                    <h4 id="trace-event-title" class="text-lg font-bold font-title text-white">
                      Constat de Décès &amp; Pose du Scellé Inviolable
                    </h4>
                  </div>
                  <div class="text-right">
                    <span id="trace-actor-badge" class="px-2.5 py-1 rounded-md text-xs font-mono bg-slate-900 border border-slate-700 text-slate-300">
                      🩺 Vétérinaire / Médecin Agréé
                    </span>
                    <div id="trace-actor-cred" class="text-[10px] text-slate-400 font-mono mt-0.5">INAMI / AFSCA #VET-BEL-84912</div>
                  </div>
                </div>

                <!-- Carte Résumé de la Dépouille -->
                <div class="p-3 rounded-xl bg-obsidian-950 border border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs">
                  <div>
                    <span class="text-slate-400 block text-[10px] uppercase font-mono">Dépouille Identifiée</span>
                    <strong id="trace-depouille-name" class="text-white text-sm">Adrien de Valcourt (ou Canis familiaris TaxID 9615)</strong>
                    <span id="trace-depouille-id" class="text-gold-400 font-mono text-[11px] block">DEP-2026-BEL-99201</span>
                  </div>
                  <div class="text-right font-mono">
                    <span class="text-slate-400 block text-[10px] uppercase">Régime Sanitaire</span>
                    <span id="trace-channel-badge" class="px-2 py-0.5 rounded bg-emerald-950 border border-emerald-500/40 text-emerald-300 font-bold">
                      Profil 1 · Catégorie 1 Mémoriel
                    </span>
                  </div>
                </div>

                <!-- Cadre Lieu & Réglementation Souveraine -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
                  <div class="p-2.5 rounded-xl bg-obsidian-950 border border-slate-800 flex items-start gap-2.5">
                    <span class="text-base mt-0.5">📍</span>
                    <div class="min-w-0 flex-1">
                      <span class="text-[10px] uppercase font-mono text-slate-400 block">Lieu Réglementaire Précis</span>
                      <strong id="trace-event-location" class="text-slate-200 text-xs block leading-snug">Domicile du déclarant / Clinique (Liège)</strong>
                    </div>
                  </div>
                  <div class="p-2.5 rounded-xl bg-obsidian-950 border border-slate-800 flex items-start gap-2.5">
                    <span class="text-base mt-0.5">⚖️</span>
                    <div class="min-w-0 flex-1">
                      <span class="text-[10px] uppercase font-mono text-gold-400 block">Cadre Réglementaire &amp; Loi</span>
                      <strong id="trace-event-legal" class="text-slate-200 text-xs block leading-snug">Règlement (CE) n° 1069/2009 &amp; Arrêté royal 2007 (références à confirmer par un juriste)</strong>
                    </div>
                  </div>
                </div>

                <!-- Formulaire Interactif de l'Événement -->
                <div class="space-y-3" id="trace-form-fields-container">
                  <!-- Rempli dynamiquement selon l'événement -->
                </div>

                <!-- Résumé Explicatif Métier -->
                <p id="trace-event-summary" class="text-xs text-slate-300 bg-slate-900/60 p-3 rounded-lg border border-slate-800 leading-relaxed">
                  Constat officiel de fin de vie, horodatage certifié RFC 3339, géolocalisation par balise RTK, vérification de l'identité du défunt ou de l'animal, et scellement physique et cryptographique immédiat par scellé inviolable NFC/QR à signature Ed25519.
                </p>

                <!-- Boutons d'Action & Déclencheur d'Anomalie -->
                <div class="flex flex-wrap items-center gap-3 pt-2">
                  <button id="btn-trace-action" onclick="nextTraceStep()" class="wf-btn wf-btn-gold text-xs font-bold flex-1 py-2.5">
                    ⚡ Valider &amp; Sceller l'Événement (Suivant)
                  </button>
                  <button id="btn-trace-anomaly" onclick="simulateTraceAnomaly()" class="wf-btn wf-btn-sub text-xs text-rose-300 border-rose-500/30 hover:bg-rose-950/40 py-2.5 px-3" title="Tester la réaction du système face à une violation">
                    ⚠️ Simuler Anomalie
                  </button>
                </div>

                <!-- Bannière d'Alerte Anomalie (Masquée par défaut) -->
                <div id="trace-anomaly-banner" class="hidden p-3 rounded-lg bg-red-950/80 border border-red-500 text-red-200 text-xs space-y-1">
                  <!-- Rempli dynamiquement lors d'une anomalie -->
                </div>

              </div>
            </div>

            <!-- Colonne Droite : Télémétrie, Scellé, Chaîne du Froid & Console Cryptographique (5/12) -->
            <div class="lg:col-span-5 space-y-4">

              <!-- Box 1 : Statut du Scellé Inviolable NFC / Ed25519 -->
              <div class="trace-seal-card space-y-2">
                <div class="flex items-center justify-between text-xs">
                  <div class="flex items-center gap-2">
                    <span class="text-xl">🔒</span>
                    <span class="font-bold text-white uppercase tracking-wider font-mono text-[11px]">Scellé Inviolable Ed25519</span>
                  </div>
                  <span id="trace-seal-status-badge" class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-950 text-emerald-300 border border-emerald-500/40">
                    INTÈGRE &bull; NON ROMPU
                  </span>
                </div>
                <div class="flex items-center justify-between text-xs font-mono bg-obsidian-950/80 p-2 rounded border border-slate-800">
                  <span class="text-slate-400">ID Scellé Physique :</span>
                  <span id="trace-seal-id-val" class="text-sky-300 font-bold">SCELL-2026-BEL-0982-NFC</span>
                </div>
                <div class="text-[10px] font-mono text-slate-400 flex items-center justify-between">
                  <span>Cryptosystème : RFC 8032 Ed25519 (alg: -8)</span>
                  <span class="text-emerald-400">Tag 18 COSE</span>
                </div>
              </div>

              <!-- Box 2 : Thermomètre Numérique & Chaîne du Froid -->
              <div class="trace-thermometer-box space-y-2">
                <div class="flex items-center justify-between text-xs">
                  <div class="flex items-center gap-2">
                    <span id="trace-temp-icon" class="text-lg">❄️</span>
                    <span class="font-bold text-white uppercase tracking-wider font-mono text-[11px]">Monitoring Thermique Continu</span>
                  </div>
                  <span id="trace-temp-badge" class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-sky-950 text-sky-300 border border-sky-500/40">
                    CONFORME (2-4°C)
                  </span>
                </div>
                <div class="flex items-baseline justify-between">
                  <div class="text-2xl font-bold font-mono text-white" id="trace-temp-readout">+3.2°C</div>
                  <span class="text-xs font-mono text-slate-400" id="trace-temp-target">Consigne : +2.0°C à +4.0°C</span>
                </div>
                <div class="trace-gauge-bar">
                  <div id="trace-temp-fill" class="trace-gauge-fill bg-sky-400" style="width: 32%;"></div>
                </div>
              </div>

              <!-- Box 3 : Télémétrie GPS & Émargement -->
              <div class="bg-obsidian-950 border border-slate-800 rounded-xl p-3 space-y-1.5 text-xs font-mono">
                <div class="text-slate-400 uppercase text-[10px] font-bold">Balise GPS &amp; Horodatage Certifié :</div>
                <div class="flex items-center justify-between text-slate-300">
                  <span>📍 GPS RTK :</span>
                  <span id="trace-gps-val" class="text-gold-300">50.6333° N, 5.5667° E</span>
                </div>
                <div class="flex items-center justify-between text-slate-300">
                  <span>🏛️ Lieu Événement :</span>
                  <span id="trace-location-box-val" class="text-slate-200 truncate max-w-[200px]" title="Lieu">Liège</span>
                </div>
                <div class="flex items-center justify-between text-slate-300">
                  <span>⏱️ Horodatage :</span>
                  <span id="trace-time-val" class="text-slate-400">2026-10-05 08:15 UTC</span>
                </div>
                <div class="flex items-center justify-between text-slate-300">
                  <span>🚐 Logistique :</span>
                  <span id="trace-carrier-val" class="text-slate-300 truncate max-w-[200px]">Véhicule 1-AFR-842</span>
                </div>
              </div>

              <!-- Box 4 : Console Cryptographique & The Iron Gate Live -->
              <div class="space-y-1">
                <div class="flex items-center justify-between text-xs font-mono text-slate-400">
                  <span>Journal Cryptographique In-Silico</span>
                  <span class="text-emerald-400 text-[10px]">Ed25519 &bull; SHA-256</span>
                </div>
                <div class="trace-crypto-terminal" id="trace-crypto-log">
                  <div class="text-slate-400">> [INIT] Chaîne de traçabilité AeterniTrak V1.0 initialisée...</div>
                  <div class="text-emerald-400">> [SCELLÉ] SCELL-2026-BEL-0982-NFC lié à DEP-2026-BEL-99201</div>
                  <div class="text-sky-300">> [SIGNATURE] alg: -8 (Ed25519) digest validé in-silico</div>
                </div>
              </div>

            </div>

          </div>

        </div>
      </div>

    </div>
  </section>
"""

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
    theater_html = generate_interactive_theater()

    html_content = f"""<!DOCTYPE html>
<html lang="fr" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AeterniTrak V1.0 — Architecture 4 Applications & Grand Théâtre Vivant des Wireframes</title>
  <style>
{CSS_STYLES}
  </style>
</head>
<body>

  <!-- En-tête Global Solennel -->
  <header>
    <div class="flex items-center gap-3">
      <span class="text-3xl select-none">🏛️</span>
      <div>
        <div class="flex items-center gap-2.5">
          <h1 class="text-xl font-extrabold font-title tracking-tight text-white">AeterniTrak <span class="text-gold-400 text-xs font-mono font-bold px-2 py-0.5 rounded border border-gold-500/30 bg-gold-500/10">V1.0</span></h1>
          <span class="text-xs text-slate-400 border-l border-slate-700 pl-2.5">Référentiel Fonctionnel & Grand Théâtre Vivant des Wireframes</span>
        </div>
        <p class="text-xs text-slate-300">Le Pax Funèbre • 4 Applications Multiplateformes Étanches • Spec-First & Test-First Certifié</p>
      </div>
    </div>

    <!-- Badges Métriques & Statut -->
    <div class="flex flex-wrap items-center gap-2.5 text-xs">
      <div class="bg-emerald-950/50 border border-emerald-500/40 text-emerald-300 px-3 py-1.5 rounded-lg flex items-center gap-2 font-mono text-xs shadow-sm">
        <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
        <strong id="badge-vectors">693 Vecteurs</strong>
        <span class="text-emerald-400/80">• 100% Validé</span>
      </div>
      <div class="bg-gold-500/15 border border-gold-500/30 text-gold-300 px-3 py-1.5 rounded-lg flex items-center gap-1.5 text-xs">
        <span>📐</span> <strong>{total_ucs} Wireframes Dédiés (4 États)</strong>
      </div>
      <div class="bg-blue-950/40 border border-blue-500/30 text-blue-300 px-3 py-1.5 rounded-lg flex items-center gap-1.5 text-xs">
        <span>🌍</span> <strong>100% Multiplateforme</strong>
      </div>
      <div class="bg-indigo-950/40 border border-indigo-500/30 text-indigo-300 px-3 py-1.5 rounded-lg flex items-center gap-1.5 text-xs">
        <span>🛡️</span> <strong>ACOSJ 92k EEPROM</strong>
      </div>
      <a href="../architecture/index.html" class="bg-gold-500/15 border border-gold-500/40 hover:bg-gold-500/25 text-gold-300 px-3 py-1.5 rounded-lg flex items-center gap-1.5 text-xs transition" style="text-decoration:none;">
        <span>📐</span> <strong>Portail UML 3-Tiers</strong>
      </a>
    </div>
  </header>

  <!-- Bannière d'Universalité Multiplateforme (DEC-AET-09) -->
  <div class="bg-gradient-to-r from-obsidian-900 via-slate-900 to-obsidian-900 border-b border-slate-800 px-6 py-3 flex flex-wrap items-center justify-between text-xs sm:text-sm text-slate-300 gap-3">
    <div class="flex items-center gap-2">
      <span class="text-gold-400 font-bold">Matrice d'Exécution Universelle :</span>
      <span class="text-slate-300">Les 4 applications s'exécutent avec le même niveau d'excellence sur tous les terminaux :</span>
    </div>
    <div class="flex flex-wrap items-center gap-3 font-mono text-xs">
      <span class="flex items-center gap-1.5 text-emerald-400 bg-emerald-950/50 px-2.5 py-1 rounded border border-emerald-800/40">📱 Android (NFC IsoDep & StrongBox)</span>
      <span class="flex items-center gap-1.5 text-slate-200 bg-slate-800/70 px-2.5 py-1 rounded border border-slate-700/60">🍎 iOS & iPadOS (CoreNFC & Secure Enclave)</span>
      <span class="flex items-center gap-1.5 text-sky-400 bg-sky-950/50 px-2.5 py-1 rounded border border-sky-800/40">🌐 Web PWA (Offline & WebCrypto/WebAudio)</span>
      <span class="flex items-center gap-1.5 text-amber-400 bg-amber-950/50 px-2.5 py-1 rounded border border-amber-800/40">💻 Desktop Mac/Win/Linux (WebUSB & ACR1552U)</span>
      <span class="text-gold-300 font-bold px-2 py-0.5 bg-gold-500/10 rounded border border-gold-500/20">~85% Code Partagé AeterniCore</span>
    </div>
  </div>

  <!-- Navigation par Onglets Métiers & Recherche Instantanée -->
  <div class="bg-obsidian-900 border-b border-slate-800/80 px-6 py-3.5 flex flex-wrap items-center justify-between gap-4 sticky top-[73px] z-50 backdrop-blur-md bg-obsidian-900/95">
    <nav class="flex flex-wrap gap-2" id="nav-tabs">
      <button onclick="switchTab('app1')" id="tab-app1" class="tab-btn px-4 py-2.5 rounded-xl text-xs sm:text-sm font-bold transition flex items-center gap-2 bg-gold-500 text-obsidian-950 shadow-md shadow-gold-500/20">
        <span>🎨</span> App 1 : PaxStudio Design
        <span id="count-tab-app1" class="bg-black/20 text-xs px-2 py-0.5 rounded-full font-mono">{len(APP1_USECASES)} UC</span>
      </button>
      <button onclick="switchTab('app2')" id="tab-app2" class="tab-btn px-4 py-2.5 rounded-xl text-xs sm:text-sm font-bold transition flex items-center gap-2 text-slate-300 hover:text-white hover:bg-slate-800/60">
        <span>🖨️</span> App 2 : PaxStation Encodage
        <span id="count-tab-app2" class="bg-slate-800 text-xs px-2 py-0.5 rounded-full font-mono">{len(APP2_USECASES)} UC</span>
      </button>
      <button onclick="switchTab('app3')" id="tab-app3" class="tab-btn px-4 py-2.5 rounded-xl text-xs sm:text-sm font-bold transition flex items-center gap-2 text-slate-300 hover:text-white hover:bg-slate-800/60">
        <span>🕊️</span> App 3 : Sanctuaire Mémoriel
        <span id="count-tab-app3" class="bg-slate-800 text-xs px-2 py-0.5 rounded-full font-mono">{len(APP3_USECASES)} UC</span>
      </button>
      <button onclick="switchTab('app4')" id="tab-app4" class="tab-btn px-4 py-2.5 rounded-xl text-xs sm:text-sm font-bold transition flex items-center gap-2 text-slate-300 hover:text-white hover:bg-slate-800/60">
        <span>🪰</span> App 4 : Filière & Traçabilité
        <span id="count-tab-app4" class="bg-slate-800 text-xs px-2 py-0.5 rounded-full font-mono">{len(APP4_USECASES)} UC</span>
      </button>
      <button onclick="switchTab('legal')" id="tab-legal" class="tab-btn px-4 py-2.5 rounded-xl text-xs sm:text-sm font-bold transition flex items-center gap-2 text-slate-300 hover:text-white hover:bg-slate-800/60">
        <span>⚖️</span> Référentiel Juridique
        <span class="bg-slate-800 text-xs px-2 py-0.5 rounded-full font-mono">{len(LEGAL_TEXTS)} Textes</span>
      </button>
    </nav>

    <!-- Recherche Instantanée avec Surbrillance & Raccourci '/' -->
    <div class="search-input-wrapper">
      <span class="absolute left-3 top-3 text-slate-400 text-sm">🔍</span>
      <input type="text" id="searchInput" oninput="filterUseCases()" placeholder="Filtrer instantanément (ex: pacemaker, lfa, 92k...) [/]" class="search-input">
    </div>
  </div>

  <!-- Contenu Principal -->
  <main class="flex-1 p-6 max-w-7xl mx-auto w-full space-y-8">

    <!-- LE GRAND THÉÂTRE INTERACTIF (SHOWCASE TEMPS RÉEL) -->
    {theater_html}

    <!-- Onglet 1 : App 1 PaxStudio Design -->
    <section id="section-app1" class="tab-content space-y-6">
      <div class="bg-gradient-to-r from-obsidian-850 to-slate-900 border border-gold-500/20 rounded-2xl p-6 relative overflow-hidden">
        <div class="max-w-3xl space-y-2 relative z-10">
          <div class="flex flex-wrap items-center gap-2">
            <span class="text-xs uppercase font-extrabold tracking-wider text-gold-400">Application 1 · Outil Créatif & Pré-Encodage (Famille & Conseiller)</span>
            <span class="text-xs font-mono bg-gold-500/10 text-gold-300 border border-gold-500/20 px-2 py-0.5 rounded">Multiplateforme : Web • Android • iOS • Mac • Windows</span>
          </div>
          <h2 class="text-2xl font-bold font-title text-white">PaxStudio Design — Personnalisation des 2 Cartes & Médaillons</h2>
          <p class="text-sm text-slate-300 leading-relaxed">
            L'espace de co-création visuelle et mémorielle pour la famille et son conseiller funéraire. Permet le design recto/verso des deux cartes (Carte Sanctuaire mémorielle et Carte Directives médicales/civiles), le choix des finitions dorées, la prévisualisation 3D temps réel, le carrousel photo 480x480 (DEC-AET-12) WebP, l'oscilloscope vocal et la génération de la <strong>capsule de pré-encodage scellée</strong> prête pour l'agence.
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
      <div class="flex flex-wrap gap-2" id="cat-filters-app1">
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
            <span class="text-xs font-mono bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 px-2 py-0.5 rounded">Multiplateforme : Navigateurs Chromium Desktop (WebUSB) • Applications Natives PC/SC</span>
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
      <div class="flex flex-wrap gap-2" id="cat-filters-app2">
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
            <span class="text-xs font-mono bg-purple-500/10 text-purple-300 border border-purple-500/20 px-2 py-0.5 rounded">Multiplateforme : iOS CoreNFC • Android NFC • Web NFC Chrome • PWA Hors-Ligne</span>
          </div>
          <h2 class="text-2xl font-bold font-title text-white">Sanctuaire Mémoriel Mobile — Recueillement & Directives</h2>
          <p class="text-sm text-slate-300 leading-relaxed">
            L'application universelle de recueillement destinée aux familles et proches du défunt. Déclenchée instantanément par simple <strong>tap NFC sans aucun mot de passe</strong> (Zéro Login). Procède à la vérification cryptographique décentralisée COSE_Sign1, applique le bandeau de réserve DEC-AET-07 Option B en cas d'émetteur inconnu, orchestre le sanctuaire acoustique avec ducking vocal automatique (-14 dB), et garantit la consultation solennelle des volontés civiles et des directives d'urgence (alerte exérèse pacemaker, don d'organes, legs à la science — références à confirmer par un juriste).
          </p>
          <div class="flex flex-wrap gap-2 pt-2 text-xs">
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">📱 NFC Instantané Zéro Login</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">🔐 Vérification Ed25519 / ES256</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">🎙️ Ducking Vocal Vivant</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">📜 Consultation Volontés Civiles</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">⚠️ Alerte Vitale Pacemaker (référence à confirmer par un juriste)</span>
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
      <div class="flex flex-wrap gap-2" id="cat-filters-app3">
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
            <span class="text-xs font-mono bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 px-2 py-0.5 rounded">Multiplateforme : Terminaux durcis IP68 • PWA Offline • Moteur AeterniCore CLI</span>
          </div>
          <h2 class="text-2xl font-bold font-title text-white">Filière Sarcomusation & Traçabilité Post-Décès</h2>
          <p class="text-sm text-slate-300 leading-relaxed">
            La chaîne logistique et sanitaire complète régissant la décomposition biologique par les larves d'<em>Hermetia illucens</em> (mouche soldat noire). Assure la ségrégation des 4 profils de dépouilles (Compagnie, Faune sauvage DNF, Élevage Sanitel, Déchets abattoir MRS), le dépistage toxicologique qualitatif LFA du pentobarbital, la pasteurisation 70°C/1h, la stérilisation Méthode 1 (133°C, 3 bars, 20 min), et l'évaluation par l'oracle mathématique <strong>The Iron Gate (G0 à G9)</strong> garantissant le respect absolu de la règle d'or anti-prion et du feed-ban européen.
          </p>
          <div class="flex flex-wrap gap-2 pt-2 text-xs">
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">🪰 Larves Hermetia illucens (343691)</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">🧪 Dépistage qualitatif LFA Pentobarbital</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">♨️ Stérilisation Méthode 1 (133°C/3b)</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">🛡️ The Iron Gate (G0-G9 Anti-Prion)</span>
            <span class="bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700">📜 Certificat de Lot Ed25519</span>
          </div>
        </div>
      </div>

      <!-- Vitrine Interactive du Simulateur Événementiel de Traçabilité -->
      <div class="glass-card p-5 border-emerald-500/40 rounded-2xl flex flex-wrap items-center justify-between gap-4 bg-gradient-to-r from-emerald-950/40 via-obsidian-900 to-obsidian-950 shadow-xl">
        <div class="flex items-center gap-3.5">
          <span class="text-3xl select-none">⛓️</span>
          <div>
            <div class="flex items-center gap-2">
              <h3 class="text-base sm:text-lg font-bold text-white font-title">Simulateur Événementiel de Traçabilité Post-Mortem de la Dépouille</h3>
              <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">6 Événements Inviolables</span>
            </div>
            <p class="text-xs text-slate-300 mt-0.5">
              Chaîne de traçabilité complète de la dépouille : Constat &amp; Scellé Ed25519, Transport Frigo (2-4°C), Admission &amp; Cellule, Contrôles Amonts (Exérèse Pacemaker &amp; LFA Pentobarbital), Bioconversion Hermetia illucens et Clôture The Iron Gate.
            </p>
          </div>
        </div>
        <button onclick="switchHeroExp('expE'); document.getElementById('interactive-theater').scrollIntoView();" class="wf-btn wf-btn-gold text-xs font-bold py-2.5 px-4 flex items-center gap-2">
          <span>🎭</span> Lancer le Simulateur Événementiel dans le Grand Théâtre
        </button>
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
      <div class="flex flex-wrap gap-2" id="cat-filters-app4">
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
          <table class="w-full text-left text-xs sm:text-sm border-collapse">
            <thead>
              <tr class="border-b border-slate-800 bg-obsidian-900/90 text-slate-300 font-mono text-xs uppercase tracking-wider">
                <th class="py-4 px-4">Juridiction & Acte Officiel</th>
                <th class="py-4 px-4">Dispositions Essentielles Citées</th>
                <th class="py-4 px-4">Choix de Conception AeterniTrak V1.0</th>
                <th class="py-4 px-4 text-right">Lien Documentaire</th>
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

  <!-- Pied de page Solennel -->
  <footer class="border-t border-slate-800/80 bg-obsidian-900 px-6 py-6 text-center text-xs sm:text-sm text-slate-400 flex flex-wrap items-center justify-between gap-4 mt-8">
    <span>AeterniTrak V1.0 • Société Le Pax Funèbre • 4 Applications Multiplateformes Étanches</span>
    <span class="font-mono text-slate-300">Spec-First & Test-First Certifié • Arbitrages Kudoro DEC-AET-08 & DEC-AET-09</span>
  </footer>

  <!-- Injection des Données et du Runtime Applicatif -->
  <script>
    const app1UseCases = {json.dumps(APP1_USECASES, ensure_ascii=False, indent=2)};
    const app2UseCases = {json.dumps(APP2_USECASES, ensure_ascii=False, indent=2)};
    const app3UseCases = {json.dumps(APP3_USECASES, ensure_ascii=False, indent=2)};
    const app4UseCases = {json.dumps(APP4_USECASES, ensure_ascii=False, indent=2)};
    const traceabilityEvents = {json.dumps(TRACEABILITY_EVENTS, ensure_ascii=False, indent=2)};
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
