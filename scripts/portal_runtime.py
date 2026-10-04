#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeterniTrak V1.0 — Runtime Client Vanilla JavaScript (100% Hors-Ligne)
Gestion des Simulateurs de Wireframes, Modes d'Affichage, Modale Studio & Filtres.
"""

JS_RUNTIME = """
    // =========================================================================
    // AeterniTrak V1.0 — Runtime Client Interactif & Simulateurs Wireframes
    // =========================================================================

    // État global de l'application
    const appState = {
      activeTab: 'app1',
      viewModes: { app1: 'cards', app2: 'cards', app3: 'cards', app4: 'cards' },
      categoryFilters: { app1: 'all', app2: 'all', app3: 'all', app4: 'all' },
      wfStates: {}, // ucId -> { phase: 'p1', timer: null, isPlaying: false }
      modalWfState: { ucId: null, phase: 'p1', timer: null, isPlaying: false, showNominal: true }
    };

    // Répertoire consolidé de tous les cas d'usage
    const allUseCases = [...app1UseCases, ...app2UseCases, ...app3UseCases, ...app4UseCases];

    // Navigation principale par onglets
    function switchTab(tabId) {
      appState.activeTab = tabId;
      const tabs = ['app1', 'app2', 'app3', 'app4', 'legal'];
      tabs.forEach(t => {
        const sec = document.getElementById(`section-${t}`);
        const btn = document.getElementById(`tab-${t}`);
        if (sec) {
          if (t === tabId) {
            sec.classList.remove('hidden');
          } else {
            sec.classList.add('hidden');
          }
        }
        if (btn) {
          if (t === tabId) {
            btn.className = 'tab-btn px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 bg-gold-500 text-obsidian-950 shadow-md shadow-gold-500/20';
          } else {
            btn.className = 'tab-btn px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 text-slate-400 hover:text-white hover:bg-slate-800/50';
          }
        }
      });
      // Réinitialiser les timers en changeant d'onglet
      stopAllSimulations();
    }

    // Gestion des modes d'affichage (Fiches, Board Déplié, Tableur)
    function setViewMode(appId, mode) {
      appState.viewModes[appId] = mode;
      const modes = ['cards', 'board', 'table'];
      modes.forEach(m => {
        const btn = document.getElementById(`btn-mode-${appId}-${m}`);
        if (btn) {
          if (m === mode) {
            btn.className = 'view-mode-btn active';
          } else {
            btn.className = 'view-mode-btn';
          }
        }
      });
      renderAppSection(appId);
    }

    // Filtre par catégorie métier
    function filterByCategory(appId, category) {
      appState.categoryFilters[appId] = category;
      const pills = document.querySelectorAll(`.cat-filter-${appId}`);
      pills.forEach(p => {
        if (p.getAttribute('data-cat') === category) {
          p.className = `cat-filter-${appId} px-3 py-1 rounded-lg text-xs font-mono font-bold transition bg-gold-500 text-obsidian-950 shadow-sm`;
        } else {
          p.className = `cat-filter-${appId} px-3 py-1 rounded-lg text-xs font-mono transition text-slate-400 hover:text-white bg-slate-800/60`;
        }
      });
      renderAppSection(appId);
    }

    // Badges de plateformes
    function getPlatformBadges(platforms) {
      if (!platforms) return '';
      const map = {
        'Web NFC (Chrome Android)': '<span class="text-[9px] font-mono text-emerald-300 bg-emerald-950/80 px-1.5 py-0.5 rounded border border-emerald-700/60" title="Web NFC API">🌐 Web NFC</span>',
        'Natif (iOS & Android)': '<span class="text-[9px] font-mono text-indigo-300 bg-indigo-950/80 px-1.5 py-0.5 rounded border border-indigo-700/60" title="iOS CoreNFC & Android">📱 Natif</span>',
        'WebUSB (Chromium Desktop)': '<span class="text-[9px] font-mono text-amber-300 bg-amber-950/80 px-1.5 py-0.5 rounded border border-amber-700/60" title="WebUSB Chromium">🔌 WebUSB</span>',
        'PC/SC (Desktop Natif)': '<span class="text-[9px] font-mono text-orange-300 bg-orange-950/80 px-1.5 py-0.5 rounded border border-orange-700/60" title="Pilote PC/SC">💻 PC/SC</span>',
        'Web Standard (PWA Hors-Ligne)': '<span class="text-[9px] font-mono text-sky-300 bg-sky-950/80 px-1.5 py-0.5 rounded border border-sky-700/60" title="PWA 100% Hors-Ligne">🌐 PWA Offline</span>',
        'Node.js / Core Engine': '<span class="text-[9px] font-mono text-purple-300 bg-purple-950/80 px-1.5 py-0.5 rounded border border-purple-700/60" title="Moteur Déterministe">⚡ AeterniCore</span>'
      };
      return platforms.map(p => map[p] || `<span class="text-[9px] font-mono text-slate-400 bg-slate-800 px-1.5 py-0.5 rounded">${p}</span>`).join(' ');
    }

    // Bascule des tiroirs accordéons
    function toggleDrawer(drawerId) {
      const el = document.getElementById(drawerId);
      if (el) {
        el.classList.toggle('open');
      }
    }

    // =========================================================================
    // LOGIQUE DU WIREFRAME PLAYER (SIMULATEUR 4 ÉTATS)
    // =========================================================================

    function getOrCreateWfState(ucId) {
      if (!appState.wfStates[ucId]) {
        appState.wfStates[ucId] = { phase: 'p1', timer: null, isPlaying: false };
      }
      return appState.wfStates[ucId];
    }

    function setWfPhase(ucId, phaseKey, isModal = false) {
      const uc = allUseCases.find(u => u.id === ucId);
      if (!uc || !uc.wireframe) return;

      const phase = uc.wireframe.phases[phaseKey];
      if (!phase) return;

      if (isModal) {
        appState.modalWfState.phase = phaseKey;
        // Mettre à jour les pills modale
        ['p1', 'p2', 'p3', 'p4'].forEach(pk => {
          const pill = document.getElementById(`modal-pill-${pk}`);
          if (pill) {
            pill.className = (pk === phaseKey) ? 'wf-pill-btn active' : 'wf-pill-btn';
          }
        });
        // Mettre à jour l'écran modale
        const screenEl = document.getElementById('modal-screen-container');
        if (screenEl) {
          screenEl.innerHTML = phase.screenHtml;
        }
        // Mettre à jour la légende
        const capTitle = document.getElementById('modal-caption-title');
        const capText = document.getElementById('modal-caption-text');
        if (capTitle) capTitle.textContent = phase.phaseTitle;
        if (capText) capText.textContent = phase.caption;
      } else {
        const state = getOrCreateWfState(ucId);
        state.phase = phaseKey;
        // Mettre à jour les pills de la carte
        ['p1', 'p2', 'p3', 'p4'].forEach(pk => {
          const pill = document.getElementById(`pill-${ucId}-${pk}`);
          if (pill) {
            pill.className = (pk === phaseKey) ? 'wf-pill-btn active' : 'wf-pill-btn';
          }
        });
        // Mettre à jour l'écran de la carte
        const screenEl = document.getElementById(`screen-${ucId}`);
        if (screenEl) {
          screenEl.innerHTML = phase.screenHtml;
        }
        // Mettre à jour la légende
        const capEl = document.getElementById(`caption-${ucId}`);
        if (capEl) {
          capEl.innerHTML = `<strong>${phase.phaseTitle}</strong> <span class="text-slate-400">• ${phase.caption}</span>`;
        }
      }
    }

    function toggleWfSimulation(ucId, isModal = false) {
      const uc = allUseCases.find(u => u.id === ucId);
      if (!uc || !uc.wireframe) return;

      const state = isModal ? appState.modalWfState : getOrCreateWfState(ucId);
      const phasesSeq = ['p1', 'p2', 'p3', 'p4'];
      const btnId = isModal ? 'modal-sim-btn' : `sim-btn-${ucId}`;
      const btn = document.getElementById(btnId);

      if (state.isPlaying) {
        // Stopper
        clearInterval(state.timer);
        state.timer = null;
        state.isPlaying = false;
        if (btn) {
          btn.innerHTML = '▶ Simuler';
          btn.classList.remove('playing');
        }
      } else {
        // Démarrer
        state.isPlaying = true;
        if (btn) {
          btn.innerHTML = '⏸ Pause';
          btn.classList.add('playing');
        }

        let currIndex = phasesSeq.indexOf(state.phase);
        if (currIndex === -1 || currIndex === 3) {
          currIndex = 0;
          setWfPhase(ucId, phasesSeq[0], isModal);
        }

        state.timer = setInterval(() => {
          currIndex = (currIndex + 1) % phasesSeq.length;
          setWfPhase(ucId, phasesSeq[currIndex], isModal);
          if (currIndex === 3) {
            // Arrêter après le cycle complet ou laisser en pause
            setTimeout(() => {
              if (state.isPlaying) {
                toggleWfSimulation(ucId, isModal);
              }
            }, 3000);
          }
        }, 1800);
      }
    }

    function stopAllSimulations() {
      Object.keys(appState.wfStates).forEach(id => {
        const s = appState.wfStates[id];
        if (s && s.isPlaying) {
          clearInterval(s.timer);
          s.isPlaying = false;
          const btn = document.getElementById(`sim-btn-${id}`);
          if (btn) {
            btn.innerHTML = '▶ Simuler';
            btn.classList.remove('playing');
          }
        }
      });
      if (appState.modalWfState.isPlaying) {
        clearInterval(appState.modalWfState.timer);
        appState.modalWfState.isPlaying = false;
      }
    }

    function toggleAllSimulations(appId) {
      const ucs = getAppUseCases(appId);
      const anyPlaying = ucs.some(u => appState.wfStates[u.id] && appState.wfStates[u.id].isPlaying);
      if (anyPlaying) {
        stopAllSimulations();
      } else {
        ucs.forEach((u, i) => {
          setTimeout(() => {
            const state = getOrCreateWfState(u.id);
            if (!state.isPlaying) {
              toggleWfSimulation(u.id, false);
            }
          }, i * 300);
        });
      }
    }

    // Récupération des cas d'usage par App
    function getAppUseCases(appId) {
      if (appId === 'app1') return app1UseCases;
      if (appId === 'app2') return app2UseCases;
      if (appId === 'app3') return app3UseCases;
      if (appId === 'app4') return app4UseCases;
      return [];
    }

    // Filtrage des cas d'usage
    function getFilteredUseCases(appId) {
      let list = getAppUseCases(appId);
      const cat = appState.categoryFilters[appId];
      if (cat && cat !== 'all') {
        list = list.filter(u => u.cat === cat);
      }
      const q = document.getElementById('searchInput') ? document.getElementById('searchInput').value.toLowerCase().trim() : '';
      if (q) {
        list = list.filter(uc =>
          uc.id.toLowerCase().includes(q) ||
          uc.title.toLowerCase().includes(q) ||
          uc.cat.toLowerCase().includes(q) ||
          uc.preconditions.toLowerCase().includes(q) ||
          uc.legal.toLowerCase().includes(q) ||
          (uc.tags && uc.tags.some(t => t.toLowerCase().includes(q))) ||
          (uc.wireframe && uc.wireframe.errorCase && uc.wireframe.errorCase.code.toLowerCase().includes(q))
        );
      }
      return list;
    }

    // =========================================================================
    // RENDU DES VUES (Fiches, Board Déplié, Tableur)
    // =========================================================================

    function renderAppSection(appId) {
      const mode = appState.viewModes[appId] || 'cards';
      const list = getFilteredUseCases(appId);
      const containerId = `grid-${appId}`;

      if (mode === 'cards') {
        renderCardsView(containerId, list);
      } else if (mode === 'board') {
        renderBoardView(containerId, list);
      } else if (mode === 'table') {
        renderTableView(containerId, list);
      }
    }

    // 1. Vue Cartes Modulaires avec Player Intégré
    function renderCardsView(containerId, list) {
      const container = document.getElementById(containerId);
      if (!container) return;
      container.className = 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5';

      container.innerHTML = list.map(uc => {
        const wf = uc.wireframe || {};
        const p1 = (wf.phases && wf.phases.p1) || { screenHtml: '<div class="p-4 text-xs">Aperçu en attente</div>', phaseTitle: 'Initial', caption: 'Prêt' };
        const fields = wf.formFields || [];
        const actions = wf.actionButtons || [];
        const err = wf.errorCase || { code: 'N/A', title: 'Aucune', message: 'N/A', remediation: 'N/A' };

        return `
        <div class="glass-card rounded-2xl p-5 flex flex-col justify-between transition group" id="card-${uc.id}">
          <div class="space-y-3">
            <!-- En-tête de la Fiche -->
            <div class="flex items-center justify-between">
              <span class="font-mono text-xs font-bold text-gold-400 bg-gold-500/10 px-2 py-0.5 rounded border border-gold-500/20">${uc.id}</span>
              <span class="text-[10px] uppercase font-mono font-bold text-slate-400 bg-slate-800/80 px-2 py-0.5 rounded">${uc.cat}</span>
            </div>
            <h3 class="text-base font-bold font-title text-white group-hover:text-gold-300 transition leading-snug cursor-pointer" onclick="openUseCaseModal('${uc.id}')">${uc.title}</h3>
            <div class="text-[11px] text-slate-400 flex items-center justify-between">
              <span>Acteur : <strong class="text-slate-300">${uc.actor}</strong></span>
              <span class="text-[10px] font-mono text-gold-400/90">${wf.deviceLabel || 'Dispositif Sécurisé'}</span>
            </div>

            <!-- MODULE WIREFRAME PLAYER (SIMULATEUR 4 ÉTATS) -->
            <div class="wf-player-card">
              <!-- Barre de Contrôles du Player -->
              <div class="wf-controls-bar">
                <div class="wf-pills-row">
                  <button id="pill-${uc.id}-p1" class="wf-pill-btn active" onclick="setWfPhase('${uc.id}', 'p1')">1. Initial</button>
                  <button id="pill-${uc.id}-p2" class="wf-pill-btn" onclick="setWfPhase('${uc.id}', 'p2')">2. Trigger ⚡</button>
                  <button id="pill-${uc.id}-p3" class="wf-pill-btn" onclick="setWfPhase('${uc.id}', 'p3')">3. Traitement ⚙️</button>
                  <button id="pill-${uc.id}-p4" class="wf-pill-btn" onclick="setWfPhase('${uc.id}', 'p4')">4. Fin ✨</button>
                </div>
                <button id="sim-btn-${uc.id}" class="wf-sim-btn" onclick="toggleWfSimulation('${uc.id}')">▶ Simuler</button>
              </div>

              <!-- Écran de Maquette Stylisé (Device Frame) -->
              <div class="device-bezel">
                <div class="device-topbar">
                  <div class="device-controls-dots">
                    <span class="dot-red"></span><span class="dot-yellow"></span><span class="dot-green"></span>
                  </div>
                  <span>${wf.deviceLabel ? wf.deviceLabel.split('•')[0].trim() : 'Terminal AeterniTrak'}</span>
                  <span>100% Offline</span>
                </div>
                <div id="screen-${uc.id}" class="wf-screen-container">
                  ${p1.screenHtml}
                </div>
              </div>

              <!-- Légende Narrative de la Phase Active -->
              <div class="wf-caption-box" id="caption-${uc.id}">
                <span><strong>${p1.phaseTitle}</strong> <span class="text-slate-400">• ${p1.caption}</span></span>
              </div>
            </div>

            <!-- Tiroirs Accordéons : Formulaire & Erreur Normative -->
            <div class="space-y-1.5 pt-1">
              <button class="wf-drawer-toggle" onclick="toggleDrawer('drawer-form-${uc.id}')">
                <span>📋 Formulaire & Boutons Détaillés (${fields.length} champs)</span>
                <span class="text-[9px]">▼</span>
              </button>
              <div id="drawer-form-${uc.id}" class="wf-drawer-content space-y-2">
                <div class="font-mono text-[10px] text-gold-400 font-bold">Champs d'Interaction :</div>
                <div class="space-y-1">
                  ${fields.map(f => `
                    <div class="flex items-center justify-between text-[10px] bg-slate-900/80 p-1.5 rounded border border-slate-800">
                      <div><strong class="text-slate-200">${f.label}</strong> <span class="text-slate-500 font-mono">(${f.type})</span></div>
                      <span class="text-[9px] font-mono px-1 rounded ${f.required ? 'bg-amber-950 text-amber-300 border border-amber-800' : 'bg-slate-800 text-slate-400'}">${f.badge}</span>
                    </div>
                  `).join('')}
                </div>
                <div class="font-mono text-[10px] text-gold-400 font-bold pt-1">Boutons d'Action :</div>
                <div class="flex flex-wrap gap-1">
                  ${actions.map(a => `
                    <span class="text-[9px] font-mono bg-slate-800 text-slate-300 px-1.5 py-0.5 rounded border border-slate-700">${a.icon || '🔘'} ${a.label}</span>
                  `).join('')}
                </div>
              </div>

              <button class="wf-drawer-toggle text-rose-300 hover:text-rose-200" onclick="toggleDrawer('drawer-err-${uc.id}')">
                <span>⚠️ Cas d'Erreur & Remédiation (${err.code})</span>
                <span class="text-[9px]">▼</span>
              </button>
              <div id="drawer-err-${uc.id}" class="wf-drawer-content space-y-1.5 border-rose-900/60 bg-rose-950/20">
                <div class="flex items-center justify-between">
                  <span class="font-mono text-[10px] font-bold text-rose-400">${err.code}</span>
                  <span class="text-[9px] text-slate-400">${err.title}</span>
                </div>
                <div class="text-[10px] text-rose-200/90 leading-tight"><strong>Alerte :</strong> ${err.message}</div>
                <div class="text-[10px] text-emerald-300/90 leading-tight"><strong>Remédiation :</strong> ${err.remediation}</div>
              </div>
            </div>

            <!-- Plateformes Compatibles -->
            <div class="pt-1 flex flex-wrap gap-1">
              ${getPlatformBadges(uc.platforms)}
            </div>
          </div>

          <!-- Pied de Fiche -->
          <div class="pt-4 border-t border-slate-850/80 mt-4 flex items-center justify-between">
            <div class="flex flex-wrap gap-1">
              ${uc.tags.map(t => `<span class="text-[9px] font-mono text-slate-400 bg-slate-900 px-1.5 py-0.5 rounded border border-slate-800">${t}</span>`).join('')}
            </div>
            <button onclick="openUseCaseModal('${uc.id}')" class="text-xs text-gold-400 font-bold hover:translate-x-1 transition flex items-center gap-1 cursor-pointer">
              Inspecter Studio →
            </button>
          </div>
        </div>
        `;
      }).join('');
    }

    // 2. Vue Living Wireframe Board (4 Écrans Dépliés Simultanés)
    function renderBoardView(containerId, list) {
      const container = document.getElementById(containerId);
      if (!container) return;
      container.className = 'space-y-8';

      container.innerHTML = list.map(uc => {
        const wf = uc.wireframe || {};
        const p1 = (wf.phases && wf.phases.p1) || { screenHtml: '', phaseTitle: 'Phase 1' };
        const p2 = (wf.phases && wf.phases.p2) || { screenHtml: '', phaseTitle: 'Phase 2' };
        const p3 = (wf.phases && wf.phases.p3) || { screenHtml: '', phaseTitle: 'Phase 3' };
        const p4 = (wf.phases && wf.phases.p4) || { screenHtml: '', phaseTitle: 'Phase 4' };

        return `
        <div class="glass-card rounded-2xl p-6 space-y-4">
          <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-3">
            <div class="flex items-center gap-2">
              <span class="font-mono text-xs font-bold text-gold-400 bg-gold-500/10 px-2.5 py-1 rounded border border-gold-500/30">${uc.id}</span>
              <h3 class="text-base font-bold font-title text-white">${uc.title}</h3>
              <span class="text-xs uppercase font-mono text-slate-400 bg-slate-800 px-2 py-0.5 rounded">${uc.cat}</span>
            </div>
            <div class="flex items-center gap-3">
              <span class="text-xs font-mono text-slate-400">${wf.deviceLabel || 'Dispositif Sécurisé'}</span>
              <button onclick="openUseCaseModal('${uc.id}')" class="text-xs font-bold text-gold-400 hover:text-white bg-gold-500/10 hover:bg-gold-500 hover:text-black px-3 py-1 rounded-lg border border-gold-500/30 transition">
                Spécifications Complètes ↗
              </button>
            </div>
          </div>

          <!-- Les 4 Écrans Dépliés en Grille Panoramique -->
          <div class="wf-board-grid">
            <div class="wf-board-col">
              <div class="wf-board-badge"><span>📱 1. Avant Trigger</span> <span class="text-[9px] text-slate-400">État Initial</span></div>
              <div class="device-bezel"><div class="wf-screen-box">${p1.screenHtml}</div></div>
              <div class="text-[10px] text-slate-400 leading-tight">${p1.caption}</div>
            </div>

            <div class="wf-board-col">
              <div class="wf-board-badge border-gold-500/40 text-gold-300"><span>⚡ 2. Déclenchement</span> <span class="text-[9px] text-gold-400">L'Événement</span></div>
              <div class="device-bezel border-gold-500/50"><div class="wf-screen-box">${p2.screenHtml}</div></div>
              <div class="text-[10px] text-slate-400 leading-tight">${p2.caption}</div>
            </div>

            <div class="wf-board-col">
              <div class="wf-board-badge border-emerald-500/40 text-emerald-300"><span>⚙️ 3. Traitement</span> <span class="text-[9px] text-emerald-400">Temps Réel</span></div>
              <div class="device-bezel border-emerald-500/50"><div class="wf-screen-box">${p3.screenHtml}</div></div>
              <div class="text-[10px] text-slate-400 leading-tight">${p3.caption}</div>
            </div>

            <div class="wf-board-col">
              <div class="wf-board-badge border-gold-500/40 text-gold-300"><span>✨ 4. Écran de Fin</span> <span class="text-[9px] text-gold-400">Scellement</span></div>
              <div class="device-bezel border-gold-500/50"><div class="wf-screen-box">${p4.screenHtml}</div></div>
              <div class="text-[10px] text-slate-400 leading-tight">${p4.caption}</div>
            </div>
          </div>
        </div>
        `;
      }).join('');
    }

    // 3. Vue Synthétique Tableur
    function renderTableView(containerId, list) {
      const container = document.getElementById(containerId);
      if (!container) return;
      container.className = 'glass-card rounded-2xl overflow-hidden';

      container.innerHTML = `
        <div class="overflow-x-auto">
          <table class="table-summary">
            <thead>
              <tr>
                <th>ID & Cas d'Usage</th>
                <th>Acteur & Plateforme</th>
                <th>Formulaire & Champs Clés</th>
                <th>Déclencheur (Trigger)</th>
                <th>Traitement & Évolution</th>
                <th>Fin & Validation</th>
                <th>Code d'Erreur & Remédiation</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800">
              ${list.map(uc => {
                const wf = uc.wireframe || {};
                const fields = wf.formFields || [];
                const err = wf.errorCase || { code: 'N/A', message: 'N/A', remediation: 'N/A' };
                const p2 = (wf.phases && wf.phases.p2) || {};
                const p3 = (wf.phases && wf.phases.p3) || {};
                const p4 = (wf.phases && wf.phases.p4) || {};

                return `
                <tr>
                  <td>
                    <span class="font-mono text-xs font-bold text-gold-400 block">${uc.id}</span>
                    <strong class="text-white text-xs block mt-0.5">${uc.title}</strong>
                    <span class="text-[10px] text-slate-400 uppercase font-mono">${uc.cat}</span>
                  </td>
                  <td>
                    <span class="text-xs text-slate-200 block">${uc.actor}</span>
                    <span class="text-[10px] text-slate-400 font-mono block mt-1">${wf.deviceLabel || 'Terminal'}</span>
                  </td>
                  <td>
                    <span class="text-[11px] text-slate-300 block font-bold">${fields.length} champs définis :</span>
                    <div class="text-[10px] text-slate-400 space-y-0.5 mt-1">
                      ${fields.slice(0, 2).map(f => `• ${f.label} (${f.badge})`).join('<br>')}
                      ${fields.length > 2 ? `<span class="text-slate-500">+${fields.length - 2} autres</span>` : ''}
                    </div>
                  </td>
                  <td>
                    <span class="text-xs text-gold-300 block font-mono">⚡ ${p2.triggerName || 'Action'}</span>
                  </td>
                  <td>
                    <span class="text-xs text-emerald-300 block font-mono">⚙️ ${p3.phaseTitle || 'Traitement'}</span>
                    <span class="text-[10px] text-slate-400 block mt-0.5">${p3.caption || ''}</span>
                  </td>
                  <td>
                    <span class="text-xs text-gold-400 block font-bold">✨ ${p4.phaseTitle || 'Validé'}</span>
                    <span class="text-[10px] text-slate-300 block mt-0.5">${wf.validationMsg ? wf.validationMsg.badge : 'Conforme'}</span>
                  </td>
                  <td>
                    <span class="font-mono text-xs text-rose-400 font-bold block">${err.code}</span>
                    <span class="text-[10px] text-slate-300 block mt-0.5 line-clamp-2">${err.message}</span>
                  </td>
                  <td>
                    <button onclick="openUseCaseModal('${uc.id}')" class="bg-slate-800 hover:bg-gold-500 hover:text-black text-slate-300 text-xs font-bold px-2.5 py-1.5 rounded transition whitespace-nowrap">
                      Studio ↗
                    </button>
                  </td>
                </tr>
                `;
              }).join('')}
            </tbody>
          </table>
        </div>
      `;
    }

    // =========================================================================
    // MODALE STUDIO HAUTE DÉFINITION (THEATER PLAYER & SPECS COMPLÈTES)
    // =========================================================================

    function openUseCaseModal(ucId) {
      const uc = allUseCases.find(u => u.id === ucId);
      if (!uc) return;

      const wf = uc.wireframe || {};
      const fields = wf.formFields || [];
      const actions = wf.actionButtons || [];
      const validation = wf.validationMsg || { title: 'Conforme', badge: 'Validé', detail: 'Conforme' };
      const err = wf.errorCase || { code: 'N/A', title: 'N/A', condition: 'N/A', message: 'N/A', remediation: 'N/A' };
      const phases = wf.phases || {};
      const p1 = phases.p1 || { screenHtml: '', phaseTitle: '1. Initial', caption: 'Prêt' };

      // Configurer l'état de la modale
      appState.modalWfState = {
        ucId: ucId,
        phase: 'p1',
        timer: null,
        isPlaying: false,
        showNominal: true
      };

      const modalContent = document.getElementById('modalContent');
      modalContent.innerHTML = `
        <!-- Barre Supérieure Modale -->
        <div class="p-6 border-b border-slate-800 flex items-start justify-between gap-4 bg-obsidian-950">
          <div>
            <div class="flex items-center gap-2">
              <span class="font-mono text-xs font-bold text-gold-400 bg-gold-500/10 px-2 py-0.5 rounded border border-gold-500/30">${uc.id}</span>
              <span class="text-xs uppercase font-mono font-bold text-slate-400">${uc.cat}</span>
              <span class="text-xs font-mono text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/40">${wf.deviceLabel || 'Dispositif Sécurisé'}</span>
            </div>
            <h2 class="text-2xl font-bold font-title text-white mt-2">${uc.title}</h2>
            <div class="text-xs text-slate-400 mt-1 flex flex-wrap items-center gap-3">
              <span>Acteur : <strong class="text-gold-300">${uc.actor}</strong></span>
              <span class="border-l border-slate-700 pl-3">Plateformes : ${getPlatformBadges(uc.platforms)}</span>
            </div>
          </div>
          <button onclick="document.getElementById('ucModal').close()" class="w-8 h-8 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center justify-center text-sm font-bold transition">✕</button>
        </div>

        <!-- Corps de la Modale : 2 Colonnes Majeures (Théâtre Wireframe & Living Specs) -->
        <div class="p-6 overflow-y-auto grid grid-cols-1 lg:grid-cols-12 gap-6 text-xs text-slate-300 bg-obsidian-900">

          <!-- COLONNE GAUCHE (7/12) : GRAND THÉÂTRE DE SIMULATION DU WIREFRAME -->
          <div class="lg:col-span-7 space-y-4">
            <div class="flex items-center justify-between">
              <h4 class="font-mono font-bold text-gold-400 uppercase text-[11px] tracking-wider flex items-center gap-2">
                <span>🖥️</span> Simulateur de Wireframe Dédié à 4 États
              </h4>
              <div class="flex items-center gap-2">
                <button onclick="cycleModalPhase(-1)" class="bg-slate-800 hover:bg-slate-700 text-slate-300 px-2 py-1 rounded text-xs">◀ Précédent</button>
                <button id="modal-sim-btn" onclick="toggleWfSimulation('${uc.id}', true)" class="wf-sim-btn">▶ Lancer Simulation</button>
                <button onclick="cycleModalPhase(1)" class="bg-slate-800 hover:bg-slate-700 text-slate-300 px-2 py-1 rounded text-xs">Suivant ▶</button>
              </div>
            </div>

            <!-- Onglets de Sélection des 4 Phases -->
            <div class="flex flex-wrap gap-1.5 bg-slate-900/90 p-1.5 rounded-xl border border-slate-800">
              <button id="modal-pill-p1" class="wf-pill-btn active flex-1 text-center" onclick="setWfPhase('${uc.id}', 'p1', true)">1. Avant Trigger</button>
              <button id="modal-pill-p2" class="wf-pill-btn flex-1 text-center" onclick="setWfPhase('${uc.id}', 'p2', true)">2. Déclenchement ⚡</button>
              <button id="modal-pill-p3" class="wf-pill-btn flex-1 text-center" onclick="setWfPhase('${uc.id}', 'p3', true)">3. Traitement ⚙️</button>
              <button id="modal-pill-p4" class="wf-pill-btn flex-1 text-center" onclick="setWfPhase('${uc.id}', 'p4', true)">4. Écran de Fin ✨</button>
            </div>

            <!-- Maquette de l'Écran Haute Définition -->
            <div class="device-bezel shadow-2xl border-gold-500/40">
              <div class="device-topbar bg-obsidian-950">
                <div class="device-controls-dots">
                  <span class="dot-red"></span><span class="dot-yellow"></span><span class="dot-green"></span>
                </div>
                <span class="font-bold text-slate-300">${wf.deviceLabel || 'Dispositif Sécurisé'}</span>
                <span class="text-emerald-400">● 100% Autonome in-silico</span>
              </div>
              <div id="modal-screen-container" class="min-h-[260px] p-4 flex flex-col justify-between bg-gradient-to-b from-obsidian-900 to-obsidian-950 text-sm">
                ${p1.screenHtml}
              </div>
            </div>

            <!-- Légende & Télémétrie de l'Étape Active -->
            <div class="p-3 rounded-xl bg-obsidian-950 border border-slate-800 space-y-1">
              <div class="font-mono text-xs font-bold text-gold-300" id="modal-caption-title">${p1.phaseTitle}</div>
              <div class="text-xs text-slate-400 leading-relaxed" id="modal-caption-text">${p1.caption}</div>
            </div>
          </div>

          <!-- COLONNE DROITE (5/12) : LIVING SPECIFICATIONS, FORMULAIRE & ERREURS -->
          <div class="lg:col-span-5 space-y-4">
            <!-- 1. Définition Complète du Formulaire & Actions -->
            <div class="p-4 rounded-xl bg-obsidian-950 border border-slate-800 space-y-2.5">
              <h4 class="font-mono font-bold text-slate-400 uppercase text-[10px] tracking-wider flex items-center justify-between">
                <span>📋 Formulaire & Champs d'Interaction (${fields.length})</span>
                <span class="text-gold-400 text-[10px]">Contrat Validé</span>
              </h4>
              <div class="space-y-1.5 max-h-48 overflow-y-auto pr-1">
                ${fields.map(f => `
                  <div class="p-2 rounded bg-slate-900 border border-slate-800/80 flex items-center justify-between gap-2">
                    <div>
                      <span class="font-bold text-slate-200 block text-[11px]">${f.label}</span>
                      <span class="text-[10px] text-slate-400 font-mono">Valeur : ${f.value}</span>
                    </div>
                    <span class="text-[9px] font-mono px-1.5 py-0.5 rounded whitespace-nowrap ${f.required ? 'bg-amber-950 text-amber-300 border border-amber-800' : 'bg-slate-800 text-slate-400'}">${f.badge}</span>
                  </div>
                `).join('')}
              </div>

              <div class="pt-2 border-t border-slate-800">
                <span class="font-mono text-[10px] text-slate-400 uppercase font-bold block mb-1">Boutons d'Action & États :</span>
                <div class="flex flex-wrap gap-1.5">
                  ${actions.map(a => `
                    <span class="text-[10px] font-mono bg-slate-900 text-slate-300 px-2 py-1 rounded border border-slate-700 flex items-center gap-1">
                      <span>${a.icon || '🔘'}</span> <strong>${a.label}</strong>
                    </span>
                  `).join('')}
                </div>
              </div>
            </div>

            <!-- 2. Cas d'Erreur Normative & Remédiation -->
            <div class="p-4 rounded-xl bg-rose-950/20 border border-rose-900/60 space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-mono text-xs font-bold text-rose-400">⚠️ ${err.code}</span>
                <span class="text-[10px] uppercase font-mono text-slate-400">${err.title}</span>
              </div>
              <div class="text-[11px] text-slate-300"><strong>Déclencheur :</strong> ${err.condition}</div>
              <div class="p-2 rounded bg-rose-950/40 border border-rose-900/80 text-[11px] text-rose-200 leading-tight">
                <strong>Message d'Erreur :</strong> ${err.message}
              </div>
              <div class="p-2 rounded bg-emerald-950/40 border border-emerald-900/80 text-[11px] text-emerald-200 leading-tight">
                <strong>Instruction de Remédiation :</strong> ${err.remediation}
              </div>
            </div>

            <!-- 3. Déroulement Pas-à-Pas (Flow) & Pré/Post-conditions -->
            <div class="p-4 rounded-xl bg-obsidian-950 border border-slate-800 space-y-2.5">
              <h4 class="font-mono font-bold text-slate-400 uppercase text-[10px] tracking-wider">Déroulement Pas-à-Pas (Flow) :</h4>
              <ol class="space-y-1.5 pl-4 list-decimal list-outside text-slate-300 text-[11px]">
                ${uc.flow.map(step => `<li class="leading-relaxed pl-1">${step}</li>`).join('')}
              </ol>

              <div class="pt-2 border-t border-slate-800 flex items-center justify-between gap-3">
                <div>
                  <span class="text-[10px] text-slate-500 font-mono block">Réf. Juridique :</span>
                  <span class="text-[11px] font-bold text-slate-200">${uc.legal}</span>
                </div>
                <a href="${uc.legal_url}" onclick="document.getElementById('ucModal').close(); switchTab('legal');" class="bg-gold-500 hover:bg-gold-400 text-obsidian-950 font-bold px-2.5 py-1 rounded text-xs transition whitespace-nowrap">
                  Texte de Loi ↓
                </a>
              </div>
            </div>
          </div>
        </div>
      `;

      document.getElementById('ucModal').showModal();
    }

    function cycleModalPhase(direction) {
      const phasesSeq = ['p1', 'p2', 'p3', 'p4'];
      const curr = appState.modalWfState.phase;
      let idx = phasesSeq.indexOf(curr);
      if (idx === -1) idx = 0;
      let nextIdx = (idx + direction + phasesSeq.length) % phasesSeq.length;
      setWfPhase(appState.modalWfState.ucId, phasesSeq[nextIdx], true);
    }

    // Recherche instantanée
    function filterUseCases() {
      renderAppSection('app1');
      renderAppSection('app2');
      renderAppSection('app3');
      renderAppSection('app4');
    }

    // Rendu de la table juridique
    function renderLegalTable() {
      const tbody = document.getElementById('table-legal');
      if (!tbody) return;
      tbody.innerHTML = legalTexts.map(item => `
        <tr class="hover:bg-slate-900/40 transition align-top">
          <td class="py-3 px-4">
            <span class="text-[10px] uppercase font-mono text-slate-400 block">${item.jurisdiction}</span>
            <span class="font-mono font-bold text-gold-400 block text-xs">${item.ref}</span>
            <span class="text-[11px] text-slate-300 font-medium block leading-tight mt-1">${item.official_title}</span>
          </td>
          <td class="py-3 px-4 text-slate-200 text-xs leading-relaxed border-l border-slate-800/60">
            ${item.disposition}
          </td>
          <td class="py-3 px-4 text-amber-200/90 text-xs leading-relaxed border-l border-slate-800/60 bg-amber-500/[0.02]">
            ${item.project_choice}
          </td>
          <td class="py-3 px-4 text-right whitespace-nowrap border-l border-slate-800/60">
            ${item.portal_url ? `
              <a href="${item.portal_url}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 bg-slate-800 hover:bg-gold-500 hover:text-black text-slate-300 text-[11px] font-bold px-2.5 py-1.5 rounded transition border border-slate-700">
                ${item.portal_name} ↗
              </a>
            ` : `
              <a href="${item.url}" class="inline-flex items-center gap-1 bg-slate-800 hover:bg-slate-700 text-slate-400 text-[11px] font-mono px-2.5 py-1.5 rounded transition border border-slate-700">
                #section-legal
              </a>
            `}
          </td>
        </tr>
      `).join('');
    }

    // Gestion du clavier (Escape pour fermer, Flèches pour phases en modale)
    document.addEventListener('keydown', (e) => {
      const modal = document.getElementById('ucModal');
      if (modal && modal.open) {
        if (e.key === 'ArrowRight') {
          cycleModalPhase(1);
        } else if (e.key === 'ArrowLeft') {
          cycleModalPhase(-1);
        } else if (e.key === ' ') {
          e.preventDefault();
          toggleWfSimulation(appState.modalWfState.ucId, true);
        }
      }
    });

    // Initialisation au chargement
    document.addEventListener('DOMContentLoaded', () => {
      renderAppSection('app1');
      renderAppSection('app2');
      renderAppSection('app3');
      renderAppSection('app4');
      renderLegalTable();
    });
"""
