#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeterniTrak V1.0 — Runtime Client Vanilla JavaScript (100% Hors-Ligne)
Grand Théâtre Vivant (Carte 3D, Mockup iPhone 16 Pro, Station ACR1552U, Cassette LFA),
Double Mode de Lecture (Famille / Expert), Simulateurs Wireframes 4 États, Synthétiseur Web Audio.
Conçu par Éléonore de Saint-Aubert & Bushi 08.
"""

JS_RUNTIME = """
    // =========================================================================
    // AeterniTrak V1.0 — Runtime Client Interactif & Grand Théâtre Vivant
    // =========================================================================

    // État global de l'application
    const appState = {
      activeTab: 'app1',
      portalMode: 'famille', // 'famille' | 'expert'
      viewModes: { app1: 'cards', app2: 'cards', app3: 'cards', app4: 'cards' },
      categoryFilters: { app1: 'all', app2: 'all', app3: 'all', app4: 'all' },
      wfStates: {}, // ucId -> { phase: 'p1', timer: null, isPlaying: false }
      modalWfState: { ucId: null, phase: 'p1', timer: null, isPlaying: false, showNominal: true },
      theater: {
        cardFlipped: false,
        sanctuaryAudioPlaying: false,
        sanctuaryInterval: null,
        acrEncoding: false,
        lfaState: 'neg'
      }
    };

    try {
      const savedMode = localStorage.getItem('aeternitrak_portal_mode');
      if (savedMode === 'expert' || savedMode === 'engineer') {
        appState.portalMode = 'expert';
      }
    } catch (e) {}

    // Répertoire consolidé de tous les cas d'usage
    const allUseCases = [...app1UseCases, ...app2UseCases, ...app3UseCases, ...app4UseCases];

    // =========================================================================
    // SYNTHÉTISEUR AUDIO WEB EMBARQUÉ (100% Hors-Ligne, ZÉRO CDN)
    // =========================================================================
    let audioCtx = null;
    function getAudioContext() {
      if (!audioCtx) {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (AudioContext) audioCtx = new AudioContext();
      }
      if (audioCtx && audioCtx.state === 'suspended') {
        audioCtx.resume();
      }
      return audioCtx;
    }

    function playTone(type) {
      try {
        const ctx = getAudioContext();
        if (!ctx) return;
        const now = ctx.currentTime;
        if (type === 'soft-bell') {
          // Bip feutré d'encodage de carte (880 Hz harmonieux avec décroissance douce)
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(880, now);
          osc.frequency.exponentialRampToValueAtTime(1760, now + 0.12);
          gain.gain.setValueAtTime(0.08, now);
          gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.45);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(now);
          osc.stop(now + 0.45);
        } else if (type === 'droplet') {
          // Gouttelette de test LFA
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(680, now);
          osc.frequency.exponentialRampToValueAtTime(320, now + 0.1);
          gain.gain.setValueAtTime(0.06, now);
          gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.16);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(now);
          osc.stop(now + 0.16);
        } else if (type === 'memorial-chord') {
          // Accord solennel doux pour le sanctuaire mémoriel
          [440, 554.37, 659.25].forEach(freq => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(freq, now);
            gain.gain.setValueAtTime(0.025, now);
            gain.gain.exponentialRampToValueAtTime(0.0001, now + 1.2);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(now);
            osc.stop(now + 1.2);
          });
        }
      } catch (e) {
        // Mode silencieux si AudioContext indisponible
      }
    }

    // =========================================================================
    // NAVIGATION DU GRAND THÉÂTRE VIVANT (LES 4 EXPÉRIENCES CLÉS)
    // =========================================================================
    function switchHeroExp(expId) {
      const exps = ['expA', 'expB', 'expC', 'expD'];
      exps.forEach(id => {
        const tab = document.getElementById(`hero-tab-${id}`);
        const panel = document.getElementById(`hero-panel-${id}`);
        if (tab) {
          if (id === expId) {
            tab.classList.add('active');
          } else {
            tab.classList.remove('active');
          }
        }
        if (panel) {
          if (id === expId) {
            panel.classList.add('active');
          } else {
            panel.classList.remove('active');
          }
        }
      });
      playTone('soft-bell');
    }

    // =========================================================================
    // BASCULE DE MODE BIMODAL : MODE FAMILLE vs MODE INGÉNIEUR / EXPERT
    // =========================================================================
    function setPortalMode(mode) {
      const isFamille = (mode === 'family' || mode === 'famille');
      const normalized = isFamille ? 'famille' : 'expert';
      appState.portalMode = normalized;
      try {
        localStorage.setItem('aeternitrak_portal_mode', normalized);
      } catch (e) {}

      const btnFamily = document.getElementById('btn-mode-family') || document.getElementById('btn-mode-famille');
      const btnEngineer = document.getElementById('btn-mode-engineer') || document.getElementById('btn-mode-expert');
      const desc = document.getElementById('portal-mode-desc');

      if (btnFamily) {
        if (isFamille) {
          btnFamily.className = btnFamily.classList.contains('bimodal-btn') ? 'bimodal-btn active-family' : 'mode-switch-btn active';
        } else {
          btnFamily.className = btnFamily.classList.contains('bimodal-btn') ? 'bimodal-btn' : 'mode-switch-btn';
        }
      }

      if (btnEngineer) {
        if (!isFamille) {
          btnEngineer.className = btnEngineer.classList.contains('bimodal-btn') ? 'bimodal-btn active-engineer' : 'mode-switch-btn active-expert';
        } else {
          btnEngineer.className = btnEngineer.classList.contains('bimodal-btn') ? 'bimodal-btn' : 'mode-switch-btn';
        }
      }

      if (desc) {
        if (isFamille) {
          desc.innerHTML = '<strong>Mode Famille & Conseiller :</strong> Présentation sereine, chaleureuse et digne axée sur la mémoire, l\\'hommage affectif et la simplicité absolue sans jargon technique.';
        } else {
          desc.innerHTML = '<strong>Mode Ingénieur & Silicium :</strong> Spécifications in-silico, flux APDU ISO/IEC 7816-4, tags CBOR RFC 8949, signatures asymétriques Ed25519 et verrous sanitaires The Iron Gate.';
        }
      }

      renderAppSection(appState.activeTab);
    }

    function setReadingMode(mode) {
      setPortalMode(mode);
    }

    // =========================================================================
    // LE GRAND THÉÂTRE VIVANT : LES 4 EXPÉRIENCES INTERACTIVES EN DIRECT
    // =========================================================================

    // EXPÉRIENCE A : SANCTUAIRE MOBILE, FLAMME & DUCKING VOCAL
    function toggleMemorialAudio() {
      const btn = document.getElementById('memorial-play-btn') || document.getElementById('btn-sanctuary-audio');
      const duckingIndicator = document.getElementById('ducking-indicator') || document.getElementById('sanctuary-ducking-status');
      const statusBadge = document.getElementById('sanctuary-audio-status');
      const bars = document.querySelectorAll('#hero-panel-expA .osc-bar, #theater-oscilloscope .osc-bar, .osc-bar');
      const state = appState.theater;

      if (state.sanctuaryAudioPlaying) {
        state.sanctuaryAudioPlaying = false;
        if (state.sanctuaryInterval) {
          clearInterval(state.sanctuaryInterval);
          state.sanctuaryInterval = null;
        }
        if (btn) btn.innerHTML = '▶ Écouter le Message';
        if (duckingIndicator) {
          duckingIndicator.innerHTML = '🔇 Veille';
          duckingIndicator.className = 'font-mono text-xs text-slate-400 bg-slate-900 px-2.5 py-0.5 rounded-full border border-slate-700';
        }
        if (statusBadge) {
          statusBadge.innerHTML = '⏸ En Veille';
          statusBadge.className = 'font-mono text-xs text-slate-400 bg-slate-900 px-2.5 py-1 rounded-full border border-slate-700 flex items-center gap-1.5';
        }
        bars.forEach(b => {
          b.style.animationPlayState = 'paused';
          b.style.height = '8px';
        });
      } else {
        state.sanctuaryAudioPlaying = true;
        playTone('memorial-chord');
        if (btn) btn.innerHTML = '⏸ Suspendre l\\'Écoute';
        if (duckingIndicator) {
          duckingIndicator.innerHTML = '🎙️ Ducking Vocal -14 dB Actif';
          duckingIndicator.className = 'font-mono text-xs text-amber-300 bg-amber-950/80 px-2.5 py-0.5 rounded-full border border-amber-500/50 font-bold animate-pulse';
        }
        if (statusBadge) {
          statusBadge.innerHTML = '<span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> ▶ En Lecture (Voix Mémorielle)';
          statusBadge.className = 'font-mono text-xs text-emerald-300 bg-emerald-950/80 px-2.5 py-1 rounded-full border border-emerald-500/40 flex items-center gap-1.5';
        }
        bars.forEach(b => {
          b.style.animationPlayState = 'running';
        });
        state.sanctuaryInterval = setInterval(() => {
          bars.forEach(b => {
            const h = Math.floor(Math.random() * 22) + 6;
            b.style.height = `${h}px`;
          });
        }, 120);
      }
    }
    function toggleSanctuaryAudio() { toggleMemorialAudio(); }

    function toggleMemorialDrawer() {
      const content = document.getElementById('memorial-drawer-content');
      const icon = document.getElementById('memorial-drawer-icon');
      if (!content) return;
      const isHidden = content.classList.contains('hidden');
      if (isHidden) {
        content.classList.remove('hidden');
        if (icon) icon.textContent = '▲';
      } else {
        content.classList.add('hidden');
        if (icon) icon.textContent = '▼';
      }
    }

    // EXPÉRIENCE B : CARTE PAXFUNÈBRE 3D RÉVERSIBLE CR-80
    function toggleCard3D() {
      appState.theater.cardFlipped = !appState.theater.cardFlipped;
      const isFlipped = appState.theater.cardFlipped;

      const cardElem = document.getElementById('card-3d-element');
      const paxCard = document.getElementById('pax-card-3d-inner');
      const btn = document.getElementById('card-flip-btn') || document.getElementById('btn-flip-card-3d');
      const indicator = document.getElementById('card-face-indicator');

      if (cardElem) {
        if (isFlipped) cardElem.classList.add('flipped');
        else cardElem.classList.remove('flipped');
      }
      if (paxCard) {
        if (isFlipped) paxCard.classList.add('flipped');
        else paxCard.classList.remove('flipped');
      }

      if (btn) {
        if (isFlipped) {
          btn.innerHTML = '↺ Retourner la Carte 3D (Voir Sanctuaire Recto)';
        } else {
          btn.innerHTML = '🔄 Retourner la Carte (Verso Directives & Puce)';
        }
      }

      if (indicator) {
        if (isFlipped) {
          indicator.textContent = 'Verso : Volontés Civiles & Médicales';
          indicator.className = 'text-xs font-mono font-bold text-emerald-400 bg-emerald-950/80 px-2.5 py-1 rounded border border-emerald-500/30';
        } else {
          indicator.textContent = 'Recto : Carte Sanctuaire Mémorielle';
          indicator.className = 'text-xs font-mono font-bold text-gold-400 bg-gold-500/10 px-2.5 py-1 rounded border border-gold-500/20';
        }
      }
      playTone('soft-bell');
    }
    function toggleCard3DFlip() { toggleCard3D(); }

    function setCard3DFinish(finish) {
      const frontFaces = document.querySelectorAll('.card-face-front, .card-3d-front');
      frontFaces.forEach(front => {
        if (finish === 'gold') {
          front.style.background = 'radial-gradient(circle at 25% 25%, #2a2312 0%, #120e06 100%)';
          front.style.borderColor = 'rgba(212, 175, 55, 0.9)';
          front.style.boxShadow = '0 16px 40px rgba(0, 0, 0, 0.9), inset 0 0 35px rgba(212, 175, 55, 0.3)';
        } else if (finish === 'obsidian') {
          front.style.background = 'radial-gradient(circle at 25% 25%, #181d29 0%, #07090e 100%)';
          front.style.borderColor = 'rgba(148, 163, 184, 0.6)';
          front.style.boxShadow = '0 16px 40px rgba(0, 0, 0, 0.95), inset 0 0 25px rgba(51, 65, 85, 0.3)';
        }
      });
      playTone('soft-bell');
    }

    // EXPÉRIENCE C : PAXSTATION ENCODAGE & LECTEUR ACR1552U
    function startPaxStationEncoding() {
      const dock = document.getElementById('paxstation-card-dock');
      const led = document.getElementById('paxstation-acr-led') || document.getElementById('acr-led-apdu');
      const terminal = document.getElementById('paxstation-log') || document.getElementById('acr-terminal-log');
      const fill = document.getElementById('paxstation-byte-fill') || document.getElementById('acr-eeprom-bar');
      const text = document.getElementById('paxstation-byte-text') || document.getElementById('acr-eeprom-text');
      const btn = document.getElementById('paxstation-start-btn') || document.getElementById('btn-acr-tap');

      if (appState.theater.acrEncoding) return;
      appState.theater.acrEncoding = true;

      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '⏳ Gravure Silicium en cours...';
      }

      if (dock) dock.classList.add('docked');

      if (led) {
        led.className = 'w-2.5 h-2.5 rounded-full bg-sky-400 shadow-[0_0_12px_#38bdf8] animate-pulse active';
      }

      playTone('soft-bell');

      const steps = [
        { time: 100, text: '<span class="text-sky-400">[00.120] CARTE DÉTECTÉE</span> : ATR 3B 8F 80 01 80 4F 0C A0 00 00 03 06 03 00 03 00 00 00', bytes: 14500, label: '14 500 / 92 160 octets (16%)' },
        { time: 500, text: '<span class="text-indigo-300">[00.520] SELECT AID</span> : CLA:00 INS:A4 P1:04 P2:00 Lc:07 A0000008450101 -> SW:9000 (ACOSJ OK)', bytes: 38200, label: '38 200 / 92 160 octets (41%)' },
        { time: 1000, text: '<span class="text-gold-300">[01.040] WRITE RECORD</span> : Profil civil + Portraits WebP 220x220 alloués', bytes: 64800, label: '64 800 / 92 160 octets (70%)' },
        { time: 1500, text: '<span class="text-emerald-400">[01.580] COSE_SIGN1</span> : Ed25519 scellé in-silico (RFC 8032, Low-S conforme)', bytes: 87500, label: '87 500 / 92 160 octets (95%)' },
        { time: 2000, text: '<span class="text-purple-300">[02.100] HARDWARE LOCK</span> : Fusible physique activé. Mémoire EEPROM immuable.', bytes: 87500, label: '87 500 / 92 160 octets (95%)' },
        { time: 2400, text: '<span class="text-emerald-300 font-bold">[02.450] SUCCÈS TOTAL</span> : Carte ACOSJ 92K gravée avec succès • Prête pour la famille.', bytes: 87500, label: '87 500 / 92 160 octets (95%) - Scellé' }
      ];

      if (terminal) terminal.innerHTML = '<span class="text-slate-400">Initialisation du couplage sans contact 13.56 MHz (WebUSB ACR1552U)...</span>';

      steps.forEach((s, idx) => {
        setTimeout(() => {
          if (terminal) {
            terminal.innerHTML += `<div>${s.text}</div>`;
            terminal.scrollTop = terminal.scrollHeight;
          }
          if (fill) {
            const pct = Math.min(100, (s.bytes / 92160) * 100);
            fill.style.width = `${pct}%`;
          }
          if (text) {
            text.textContent = s.label;
          }
          if (idx === steps.length - 1) {
            appState.theater.acrEncoding = false;
            if (dock) dock.classList.remove('docked');
            if (btn) {
              btn.disabled = false;
              btn.innerHTML = '✔ Gravure Terminée (Relancer la Gravure)';
            }
            if (led) {
              led.className = 'w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399]';
            }
            playTone('soft-bell');
          }
        }, s.time);
      });
    }
    function simulateAcr1552uTap() { startPaxStationEncoding(); }

    // EXPÉRIENCE D : CASSETTE LFA TOXICOLOGIQUE & THE IRON GATE
    function startLfaTest() {
      const droplet = document.getElementById('lfa-droplet');
      const stripFlow = document.getElementById('lfa-strip-flow');
      const lineC = document.getElementById('lfa-line-c');
      const lineT = document.getElementById('lfa-line-t');
      const banner = document.getElementById('lfa-result-banner');
      const btn = document.getElementById('lfa-start-btn');
      const flags = document.querySelectorAll('.iron-gate-flag');

      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '⏳ Dépistage et migration capillaire en cours...';
      }

      // Réinitialisation
      if (banner) banner.classList.add('hidden');
      if (stripFlow) stripFlow.style.width = '0%';
      if (lineC) {
        lineC.classList.remove('active-red');
        lineC.style.opacity = '0.25';
      }
      if (lineT) {
        lineT.classList.remove('active-red', 'invisible');
        lineT.style.opacity = '0.25';
      }
      flags.forEach(f => {
        f.style.background = '';
        f.style.borderColor = '';
        f.style.color = '';
        f.classList.remove('border-emerald-500', 'text-emerald-300');
      });

      // 1. Descente de la goutte
      playTone('droplet');
      if (droplet) {
        droplet.style.opacity = '1';
        droplet.style.transform = 'translateY(18px) scale(0.9)';
      }

      // 2. Migration sur la membrane de nitrocellulose
      setTimeout(() => {
        if (droplet) {
          droplet.style.opacity = '0';
          droplet.style.transform = 'translateY(0) scale(1)';
        }
        if (stripFlow) {
          stripFlow.style.width = '100%';
        }
      }, 400);

      // 3. Révélation C et masquage T (principe compétitif)
      setTimeout(() => {
        if (lineC) {
          lineC.classList.add('active-red');
          lineC.style.opacity = '1';
          lineC.style.background = '#dc2626';
        }
        if (lineT) {
          lineT.classList.add('invisible');
          lineT.style.opacity = '0';
        }
      }, 1000);

      // 4. Affichage de la bannière de conformité
      setTimeout(() => {
        if (banner) banner.classList.remove('hidden');
      }, 1300);

      // 5. Activation séquentielle des 10 portes de The Iron Gate (G0 à G9)
      flags.forEach((flag, idx) => {
        setTimeout(() => {
          flag.style.background = 'rgba(16, 185, 129, 0.2)';
          flag.style.borderColor = 'rgba(16, 185, 129, 0.8)';
          flag.style.color = '#6ee7b7';
          flag.classList.add('border-emerald-500', 'text-emerald-300');
        }, 1400 + idx * 80);
      });

      // 6. Fin du test et réactivation du bouton
      setTimeout(() => {
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = '✔ Dépistage Conforme Validé (Relancer le Dépistage)';
        }
        playTone('soft-bell');
      }, 1400 + flags.length * 80 + 200);
    }

    function setLfaResult(res) {
      startLfaTest();
    }

    // =========================================================================
    // NAVIGATION PRINCIPALE PAR ONGLETS MÉTIERS
    // =========================================================================
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
            btn.className = 'tab-btn px-4 py-2.5 rounded-xl text-xs sm:text-sm font-bold transition flex items-center gap-2 bg-gold-500 text-obsidian-950 shadow-md shadow-gold-500/20';
          } else {
            btn.className = 'tab-btn px-4 py-2.5 rounded-xl text-xs sm:text-sm font-bold transition flex items-center gap-2 text-slate-300 hover:text-white hover:bg-slate-800/60';
          }
        }
      });
      stopAllSimulations();
      renderAppSection(tabId);
    }

    // Modes d'Affichage (Fiches, Board Déplié, Tableur)
    function setViewMode(appId, mode) {
      appState.viewModes[appId] = mode;
      const modes = ['cards', 'board', 'table'];
      modes.forEach(m => {
        const btn = document.getElementById(`btn-mode-${appId}-${m}`);
        if (btn) {
          btn.className = (m === mode) ? 'view-mode-btn active' : 'view-mode-btn';
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
          p.className = `cat-filter-btn active cat-filter-${appId}`;
        } else {
          p.className = `cat-filter-btn cat-filter-${appId}`;
        }
      });
      renderAppSection(appId);
    }

    // Badges de plateformes
    function getPlatformBadges(platforms) {
      if (!platforms) return '';
      const map = {
        'Web NFC (Chrome Android)': '<span class="text-[10px] font-mono text-emerald-300 bg-emerald-950/80 px-2 py-0.5 rounded border border-emerald-700/60" title="Web NFC API">🌐 Web NFC</span>',
        'Natif (iOS & Android)': '<span class="text-[10px] font-mono text-indigo-300 bg-indigo-950/80 px-2 py-0.5 rounded border border-indigo-700/60" title="iOS CoreNFC & Android">📱 Natif</span>',
        'WebUSB (Chromium Desktop)': '<span class="text-[10px] font-mono text-amber-300 bg-amber-950/80 px-2 py-0.5 rounded border border-amber-700/60" title="WebUSB Chromium">🔌 WebUSB</span>',
        'PC/SC (Desktop Natif)': '<span class="text-[10px] font-mono text-orange-300 bg-orange-950/80 px-2 py-0.5 rounded border border-orange-700/60" title="Pilote PC/SC">💻 PC/SC</span>',
        'Web Standard (PWA Hors-Ligne)': '<span class="text-[10px] font-mono text-sky-300 bg-sky-950/80 px-2 py-0.5 rounded border border-sky-700/60" title="PWA 100% Hors-Ligne">🌐 PWA Offline</span>',
        'Node.js / Core Engine': '<span class="text-[10px] font-mono text-purple-300 bg-purple-950/80 px-2 py-0.5 rounded border border-purple-700/60" title="Moteur Déterministe">⚡ AeterniCore</span>'
      };
      return platforms.map(p => map[p] || `<span class="text-[10px] font-mono text-slate-400 bg-slate-800 px-2 py-0.5 rounded">${p}</span>`).join(' ');
    }

    // Accordéons
    function toggleDrawer(drawerId) {
      const el = document.getElementById(drawerId);
      if (el) {
        el.classList.toggle('open');
      }
    }

    // =========================================================================
    // WIREFRAME PLAYER (SIMULATEUR 4 ÉTATS)
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

      const phase = uc.wireframe.phases && uc.wireframe.phases[phaseKey];
      if (!phase) return;

      if (isModal) {
        appState.modalWfState.phase = phaseKey;
        ['p1', 'p2', 'p3', 'p4'].forEach(pk => {
          const pill = document.getElementById(`modal-pill-${pk}`);
          if (pill) {
            pill.className = (pk === phaseKey) ? 'wf-pill-btn active' : 'wf-pill-btn';
          }
        });
        const screenEl = document.getElementById('modal-screen-container');
        if (screenEl) screenEl.innerHTML = phase.screenHtml;
        const capTitle = document.getElementById('modal-caption-title');
        const capText = document.getElementById('modal-caption-text');
        if (capTitle) capTitle.textContent = phase.phaseTitle;
        if (capText) capText.textContent = phase.caption;
      } else {
        const state = getOrCreateWfState(ucId);
        state.phase = phaseKey;
        ['p1', 'p2', 'p3', 'p4'].forEach(pk => {
          const pill = document.getElementById(`pill-${ucId}-${pk}`);
          if (pill) {
            pill.className = (pk === phaseKey) ? 'wf-pill-btn active' : 'wf-pill-btn';
          }
        });
        const screenEl = document.getElementById(`screen-${ucId}`);
        if (screenEl) screenEl.innerHTML = phase.screenHtml;
        const capEl = document.getElementById(`caption-${ucId}`);
        if (capEl) {
          capEl.innerHTML = `<strong>${phase.phaseTitle}</strong> <span class="text-slate-300">• ${phase.caption}</span>`;
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
        clearInterval(state.timer);
        state.timer = null;
        state.isPlaying = false;
        if (btn) {
          btn.innerHTML = '▶ Simuler';
          btn.classList.remove('playing');
        }
      } else {
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
            setTimeout(() => {
              if (state.isPlaying) toggleWfSimulation(ucId, isModal);
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
            if (!state.isPlaying) toggleWfSimulation(u.id, false);
          }, i * 300);
        });
      }
    }

    function getAppUseCases(appId) {
      if (appId === 'app1') return app1UseCases;
      if (appId === 'app2') return app2UseCases;
      if (appId === 'app3') return app3UseCases;
      if (appId === 'app4') return app4UseCases;
      return [];
    }

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
          (uc.tags && uc.tags.some(t => t.toLowerCase().includes(q)))
        );
      }
      return list;
    }

    // =========================================================================
    // RENDU DES VUES (FICHES, BOARD DÉPLIÉ, TABLEUR) AVEC DOUBLE MODE
    // =========================================================================
    function renderAppSection(appId) {
      if (appId === 'legal') {
        renderLegalTable();
        return;
      }
      const mode = appState.viewModes[appId] || 'cards';
      const list = getFilteredUseCases(appId);
      const containerId = `grid-${appId}`;

      if (mode === 'cards') {
        renderCardsView(containerId, list, appId);
      } else if (mode === 'board') {
        renderBoardView(containerId, list, appId);
      } else if (mode === 'table') {
        renderTableView(containerId, list, appId);
      }
    }

    // 1. Vue Cartes Modulaires Aérées & Chaleureuses (Wireframe Player)
    function renderCardsView(containerId, list, appId) {
      const container = document.getElementById(containerId);
      if (!container) return;
      container.className = 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6';

      const isFamille = appState.portalMode === 'famille';
      const themeClass = `theme-${appId}`;

      container.innerHTML = list.map(uc => {
        const wf = uc.wireframe || {};
        const p1 = (wf.phases && wf.phases.p1) || { screenHtml: '<div class="p-6 text-sm">Aperçu en attente</div>', phaseTitle: 'Initial', caption: 'Prêt' };
        const fields = wf.formFields || [];
        const err = wf.errorCase || { code: 'N/A', title: 'Aucune', message: 'N/A', remediation: 'N/A' };

        let appAccentBadge = '';
        if (appId === 'app1') appAccentBadge = 'text-gold-400 bg-gold-500/10 border-gold-500/30';
        else if (appId === 'app2') appAccentBadge = 'text-sky-300 bg-sky-950/80 border-sky-600/40';
        else if (appId === 'app3') appAccentBadge = 'text-purple-300 bg-purple-950/80 border-purple-600/40';
        else if (appId === 'app4') appAccentBadge = 'text-emerald-300 bg-emerald-950/80 border-emerald-600/40';

        const familySummaryHtml = isFamille ? `
          <div class="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/25 text-xs text-amber-200/90 leading-relaxed flex items-start gap-2.5">
            <span class="text-base select-none">🕊️</span>
            <div>
              <strong class="text-amber-100 font-semibold block">Ce que cela garantit à la famille :</strong>
              <span>Une expérience solennelle, fluide et respectueuse : les souvenirs et volontés sont protégés in-silico, sans exposition sur Internet et sans risque de perte.</span>
            </div>
          </div>
        ` : `
          <div class="p-3 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono text-slate-300 flex items-center justify-between">
            <span class="text-sky-400 font-bold">⚡ Télémétrie Silicium :</span>
            <span class="text-slate-400">IsoDep • JavaCard AID ACOSJ • COSE_Sign1</span>
          </div>
        `;

        return `
        <div class="glass-card ${themeClass} rounded-2xl p-6 flex flex-col justify-between transition group" id="card-${uc.id}">
          <div class="space-y-4">
            <!-- En-tête de la Fiche -->
            <div class="flex items-center justify-between">
              <span class="font-mono text-xs font-bold px-2.5 py-1 rounded border ${appAccentBadge}">${uc.id}</span>
              <span class="text-[11px] uppercase font-mono font-bold text-slate-300 bg-slate-800/90 px-2.5 py-0.5 rounded">${uc.cat}</span>
            </div>
            
            <h3 class="text-lg font-bold font-title text-white group-hover:text-gold-300 transition leading-snug cursor-pointer" onclick="openUseCaseModal('${uc.id}')">
              ${uc.title}
            </h3>

            <div class="text-xs text-slate-300 flex items-center justify-between">
              <span>Acteur : <strong class="text-white">${uc.actor}</strong></span>
              <span class="text-[11px] font-mono text-gold-400/90">${wf.deviceLabel ? wf.deviceLabel.split('•')[0].trim() : 'Terminal Sécurisé'}</span>
            </div>

            <!-- Résumé Bimodal (Famille vs Expert) -->
            ${familySummaryHtml}

            <!-- MODULE WIREFRAME PLAYER (SIMULATEUR 4 ÉTATS HAUTE DÉFINITION) -->
            <div class="wf-player-card">
              <!-- Barre de Contrôles du Player -->
              <div class="wf-controls-bar">
                <div class="wf-pills-row">
                  <button id="pill-${uc.id}-p1" class="wf-pill-btn active" onclick="setWfPhase('${uc.id}', 'p1')">1. Initial</button>
                  <button id="pill-${uc.id}-p2" class="wf-pill-btn" onclick="setWfPhase('${uc.id}', 'p2')">2. Action ⚡</button>
                  <button id="pill-${uc.id}-p3" class="wf-pill-btn" onclick="setWfPhase('${uc.id}', 'p3')">3. Gravure ⚙️</button>
                  <button id="pill-${uc.id}-p4" class="wf-pill-btn" onclick="setWfPhase('${uc.id}', 'p4')">4. Scellé ✨</button>
                </div>
                <button id="sim-btn-${uc.id}" class="wf-sim-btn" onclick="toggleWfSimulation('${uc.id}')">▶ Simuler</button>
              </div>

              <!-- Écran de Maquette Stylisé -->
              <div class="device-bezel">
                <div class="device-topbar">
                  <div class="device-controls-dots">
                    <span class="dot-red"></span><span class="dot-yellow"></span><span class="dot-green"></span>
                  </div>
                  <span>${wf.deviceLabel ? wf.deviceLabel.split('•')[0].trim() : 'AeterniTrak Station'}</span>
                  <span class="text-emerald-400 font-bold">100% Hors-Ligne</span>
                </div>
                <div id="screen-${uc.id}" class="wf-screen-container">
                  ${p1.screenHtml}
                </div>
              </div>

              <!-- Légende Narrative de la Phase Active -->
              <div class="wf-caption-box" id="caption-${uc.id}">
                <span><strong>${p1.phaseTitle}</strong> <span class="text-slate-300">• ${p1.caption}</span></span>
              </div>
            </div>

            <!-- Tiroirs Accordéons : Formulaire & Erreur Normative -->
            <div class="space-y-2 pt-1">
              <button class="wf-drawer-toggle" onclick="toggleDrawer('drawer-form-${uc.id}')">
                <span>${isFamille ? '📋 Données & Options Enregistrées' : '📋 Spécification des Champs'} (${fields.length} champs)</span>
                <span class="text-xs">▼</span>
              </button>
              <div id="drawer-form-${uc.id}" class="wf-drawer-content space-y-2.5">
                <div class="font-mono text-xs text-gold-400 font-bold">${isFamille ? 'Éléments Personnalisés :' : 'Champs d\\'Interaction Silicium :'}</div>
                <div class="space-y-1.5">
                  ${fields.map(f => `
                    <div class="flex items-center justify-between text-xs bg-slate-900/90 p-2 rounded-lg border border-slate-800">
                      <div><strong class="text-slate-200">${f.label}</strong> <span class="text-slate-400 font-mono">(${f.type})</span></div>
                      <span class="text-[10px] font-mono px-1.5 py-0.5 rounded ${f.required ? 'bg-amber-950 text-amber-300 border border-amber-800' : 'bg-slate-800 text-slate-300'}">${f.badge}</span>
                    </div>
                  `).join('')}
                </div>
              </div>

              <button class="wf-drawer-toggle text-rose-300 hover:text-rose-200" onclick="toggleDrawer('drawer-err-${uc.id}')">
                <span>${isFamille ? '🛡️ Protection & Résolution d\\'Incident' : '⚠️ Cas d\\'Erreur Normative'} (${err.code})</span>
                <span class="text-xs">▼</span>
              </button>
              <div id="drawer-err-${uc.id}" class="wf-drawer-content space-y-2 border-rose-900/60 bg-rose-950/20">
                <div class="flex items-center justify-between">
                  <span class="font-mono text-xs font-bold text-rose-400">${err.code}</span>
                  <span class="text-[10px] text-slate-300">${err.title}</span>
                </div>
                <div class="text-xs text-rose-200/95 leading-relaxed"><strong>${isFamille ? 'Incident évité :' : 'Alerte :'}</strong> ${err.message}</div>
                <div class="text-xs text-emerald-300/95 leading-relaxed"><strong>${isFamille ? 'Accompagnement du conseiller :' : 'Remédiation :'}</strong> ${err.remediation}</div>
              </div>
            </div>

            <!-- Badges Plateformes -->
            <div class="pt-1 flex flex-wrap gap-1.5">
              ${getPlatformBadges(uc.platforms)}
            </div>
          </div>

          <!-- Pied de Fiche -->
          <div class="pt-4 border-t border-slate-800/80 mt-5 flex items-center justify-between">
            <div class="flex flex-wrap gap-1.5">
              ${uc.tags.map(t => `<span class="text-[10px] font-mono text-slate-300 bg-slate-900 px-2 py-0.5 rounded border border-slate-800">${t}</span>`).join('')}
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
    function renderBoardView(containerId, list, appId) {
      const container = document.getElementById(containerId);
      if (!container) return;
      container.className = 'space-y-8';

      container.innerHTML = list.map(uc => {
        const wf = uc.wireframe || {};
        const p1 = (wf.phases && wf.phases.p1) || { screenHtml: '', phaseTitle: 'Phase 1', caption: '' };
        const p2 = (wf.phases && wf.phases.p2) || { screenHtml: '', phaseTitle: 'Phase 2', caption: '' };
        const p3 = (wf.phases && wf.phases.p3) || { screenHtml: '', phaseTitle: 'Phase 3', caption: '' };
        const p4 = (wf.phases && wf.phases.p4) || { screenHtml: '', phaseTitle: 'Phase 4', caption: '' };

        return `
        <div class="glass-card rounded-2xl p-6 space-y-4">
          <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-3">
            <div class="flex items-center gap-2">
              <span class="font-mono text-xs font-bold text-gold-400 bg-gold-500/10 px-2.5 py-1 rounded border border-gold-500/30">${uc.id}</span>
              <h3 class="text-lg font-bold font-title text-white">${uc.title}</h3>
              <span class="text-xs uppercase font-mono text-slate-300 bg-slate-800 px-2 py-0.5 rounded">${uc.cat}</span>
            </div>
            <div class="flex items-center gap-3">
              <span class="text-xs font-mono text-slate-300">${wf.deviceLabel || 'Dispositif Sécurisé'}</span>
              <button onclick="openUseCaseModal('${uc.id}')" class="text-xs font-bold text-gold-400 hover:text-white bg-gold-500/10 hover:bg-gold-500 hover:text-black px-3.5 py-1.5 rounded-lg border border-gold-500/30 transition">
                Spécifications Complètes ↗
              </button>
            </div>
          </div>

          <!-- Les 4 Écrans Dépliés en Grille Panoramique Confortable -->
          <div class="wf-board-grid">
            <div class="wf-board-col">
              <div class="wf-board-badge"><span>📱 1. Avant Trigger</span> <span class="text-[10px] text-slate-400">État Initial</span></div>
              <div class="device-bezel"><div class="wf-screen-box">${p1.screenHtml}</div></div>
              <div class="text-xs text-slate-300 leading-tight">${p1.caption}</div>
            </div>

            <div class="wf-board-col">
              <div class="wf-board-badge"><span>⚡ 2. Action / Saisie</span> <span class="text-[10px] text-amber-300">Trigger Actif</span></div>
              <div class="device-bezel"><div class="wf-screen-box">${p2.screenHtml}</div></div>
              <div class="text-xs text-slate-300 leading-tight">${p2.caption}</div>
            </div>

            <div class="wf-board-col">
              <div class="wf-board-badge"><span>⚙️ 3. Traitement Silicium</span> <span class="text-[10px] text-sky-300">En Cours</span></div>
              <div class="device-bezel"><div class="wf-screen-box">${p3.screenHtml}</div></div>
              <div class="text-xs text-slate-300 leading-tight">${p3.caption}</div>
            </div>

            <div class="wf-board-col">
              <div class="wf-board-badge"><span>✨ 4. Scellement / Fin</span> <span class="text-[10px] text-emerald-300">Validé</span></div>
              <div class="device-bezel"><div class="wf-screen-box">${p4.screenHtml}</div></div>
              <div class="text-xs text-slate-300 leading-tight">${p4.caption}</div>
            </div>
          </div>
        </div>
        `;
      }).join('');
    }

    // 3. Vue Tableur d'Audit Exhaustif
    function renderTableView(containerId, list, appId) {
      const container = document.getElementById(containerId);
      if (!container) return;
      container.className = 'glass-card rounded-2xl overflow-hidden';

      container.innerHTML = `
        <div class="overflow-x-auto">
          <table class="table-summary">
            <thead>
              <tr>
                <th>ID & Titre</th>
                <th>Catégorie & Acteur</th>
                <th>Dispositif & Plateformes</th>
                <th>Formulaire (Champs)</th>
                <th>Cas d'Erreur & Remédiation</th>
                <th>Réf. Juridique</th>
                <th class="text-right">Action</th>
              </tr>
            </thead>
            <tbody>
              ${list.map(uc => {
                const wf = uc.wireframe || {};
                const fields = wf.formFields || [];
                const err = wf.errorCase || { code: 'N/A', message: 'N/A' };
                return `
                <tr>
                  <td>
                    <span class="font-mono text-xs font-bold text-gold-400 block">${uc.id}</span>
                    <strong class="text-white text-xs block mt-0.5">${uc.title}</strong>
                  </td>
                  <td>
                    <span class="text-[11px] font-mono text-slate-300 block">${uc.cat}</span>
                    <span class="text-xs text-slate-400 block">${uc.actor}</span>
                  </td>
                  <td>
                    <span class="text-xs text-slate-300 block mb-1">${wf.deviceLabel || 'Terminal'}</span>
                    <div class="flex flex-wrap gap-1">${getPlatformBadges(uc.platforms)}</div>
                  </td>
                  <td>
                    <span class="text-xs text-slate-300">${fields.length} champs (${fields.map(f => f.label).slice(0, 2).join(', ')}...)</span>
                  </td>
                  <td>
                    <span class="font-mono text-xs text-rose-400 font-bold block">${err.code}</span>
                    <span class="text-[11px] text-slate-400 leading-tight block">${err.title || err.message}</span>
                  </td>
                  <td>
                    <span class="text-xs text-slate-300 block">${uc.legal}</span>
                  </td>
                  <td class="text-right whitespace-nowrap">
                    <button onclick="openUseCaseModal('${uc.id}')" class="text-xs bg-gold-500/10 hover:bg-gold-500 hover:text-black text-gold-300 font-bold px-3 py-1.5 rounded-lg border border-gold-500/30 transition">
                      Inspecter ↗
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
    // MODALE NATIVE DE HAUTE PRÉCISION (STUDIO WIREFRAME THEATER)
    // =========================================================================
    function openUseCaseModal(ucId) {
      const uc = allUseCases.find(u => u.id === ucId);
      if (!uc) return;

      const wf = uc.wireframe || {};
      const phases = wf.phases || {};
      const fields = wf.formFields || [];
      const err = wf.errorCase || { code: 'N/A', title: 'Aucune', message: 'N/A', remediation: 'N/A' };
      const isFamille = appState.portalMode === 'famille';

      appState.modalWfState.ucId = ucId;
      appState.modalWfState.phase = 'p1';
      appState.modalWfState.isPlaying = false;

      const modalContent = document.getElementById('modalContent');
      if (!modalContent) return;

      modalContent.innerHTML = `
        <!-- Barre de titre modale -->
        <div class="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-obsidian-950">
          <div class="flex items-center gap-3">
            <span class="font-mono text-sm font-bold text-gold-400 bg-gold-500/10 px-3 py-1 rounded border border-gold-500/30">${uc.id}</span>
            <div>
              <h2 class="text-lg font-bold font-title text-white">${uc.title}</h2>
              <div class="text-xs text-slate-400 flex items-center gap-2">
                <span>Catégorie : <strong class="text-slate-200">${uc.cat}</strong></span>
                <span>•</span>
                <span>Acteur : <strong class="text-slate-200">${uc.actor}</strong></span>
              </div>
            </div>
          </div>
          <button id="modal-close-btn" onclick="closeUseCaseModal()" class="text-slate-400 hover:text-white text-2xl leading-none px-2 cursor-pointer">&times;</button>
        </div>

        <!-- Corps de la modale en deux colonnes -->
        <div class="p-6 overflow-y-auto grid grid-cols-1 lg:grid-cols-12 gap-6 flex-1">
          <!-- Colonne Gauche : Simulateur de Wireframe Pleine Échelle (7 cols) -->
          <div class="lg:col-span-7 space-y-4">
            <div class="wf-player-card">
              <div class="wf-controls-bar">
                <div class="wf-pills-row">
                  <button id="modal-pill-p1" class="wf-pill-btn active" onclick="setWfPhase('${uc.id}', 'p1', true)">1. Initial</button>
                  <button id="modal-pill-p2" class="wf-pill-btn" onclick="setWfPhase('${uc.id}', 'p2', true)">2. Action ⚡</button>
                  <button id="modal-pill-p3" class="wf-pill-btn" onclick="setWfPhase('${uc.id}', 'p3', true)">3. Gravure ⚙️</button>
                  <button id="modal-pill-p4" class="wf-pill-btn" onclick="setWfPhase('${uc.id}', 'p4', true)">4. Scellé ✨</button>
                </div>
                <button id="modal-sim-btn" class="wf-sim-btn" onclick="toggleWfSimulation('${uc.id}', true)">▶ Simuler le Cycle</button>
              </div>

              <div class="device-bezel">
                <div class="device-topbar">
                  <div class="device-controls-dots">
                    <span class="dot-red"></span><span class="dot-yellow"></span><span class="dot-green"></span>
                  </div>
                  <span>${wf.deviceLabel || 'Dispositif Sécurisé'}</span>
                  <span class="text-emerald-400 font-bold">100% Hors-Ligne</span>
                </div>
                <div id="modal-screen-container" class="wf-screen-container">
                  ${(phases.p1 && phases.p1.screenHtml) || '<div class="p-8">Écran initial</div>'}
                </div>
              </div>

              <div class="wf-caption-box">
                <div>
                  <strong id="modal-caption-title" class="text-gold-300 font-bold">${(phases.p1 && phases.p1.phaseTitle) || 'Phase 1'}</strong>
                  <div id="modal-caption-text" class="text-xs text-slate-300 mt-0.5">${(phases.p1 && phases.p1.caption) || 'Prêt'}</div>
                </div>
              </div>
            </div>

            <!-- Plateformes et Contraintes -->
            <div class="p-4 rounded-xl bg-obsidian-950 border border-slate-800 space-y-2">
              <div class="font-mono text-xs text-slate-400 uppercase font-bold">Matrice d'Exécution & Garanties :</div>
              <div class="flex flex-wrap gap-2">${getPlatformBadges(uc.platforms)}</div>
              <div class="text-xs text-slate-300 pt-1">
                <strong>Préconditions :</strong> ${uc.preconditions}
              </div>
              <div class="text-xs text-emerald-300">
                <strong>Postconditions :</strong> ${uc.postconditions}
              </div>
            </div>
          </div>

          <!-- Colonne Droite : Spécifications Métiers & Données (5 cols) -->
          <div class="lg:col-span-5 space-y-4">
            <!-- 1. Formulaire & Champs -->
            <div class="p-4 rounded-xl bg-obsidian-950 border border-slate-800 space-y-3">
              <h4 class="font-mono font-bold text-gold-400 uppercase text-xs tracking-wider">
                ${isFamille ? '📋 Données de Saisie & Personnalisation' : '📋 Spécification des Champs & Types Silicium'}
              </h4>
              <div class="space-y-2">
                ${fields.map(f => `
                  <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-between gap-2">
                    <div>
                      <span class="font-bold text-slate-200 block text-xs">${f.label}</span>
                      <span class="text-[11px] text-slate-400 font-mono">Valeur : ${f.value}</span>
                    </div>
                    <span class="text-[10px] font-mono px-2 py-0.5 rounded whitespace-nowrap ${f.required ? 'bg-amber-950 text-amber-300 border border-amber-800' : 'bg-slate-800 text-slate-400'}">${f.badge}</span>
                  </div>
                `).join('')}
              </div>
            </div>

            <!-- 2. Cas d'Erreur & Remédiation -->
            <div class="p-4 rounded-xl bg-rose-950/20 border border-rose-900/60 space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-mono text-xs font-bold text-rose-400">⚠️ ${err.code}</span>
                <span class="text-[10px] uppercase font-mono text-slate-400">${err.title}</span>
              </div>
              <div class="p-2.5 rounded bg-rose-950/40 border border-rose-900/80 text-xs text-rose-200 leading-relaxed">
                <strong>Déclencheur :</strong> ${err.message}
              </div>
              <div class="p-2.5 rounded bg-emerald-950/40 border border-emerald-900/80 text-xs text-emerald-200 leading-relaxed">
                <strong>Remédiation :</strong> ${err.remediation}
              </div>
            </div>

            <!-- 3. Déroulement Pas-à-Pas (Flow) & Référence Légale -->
            <div class="p-4 rounded-xl bg-obsidian-950 border border-slate-800 space-y-2.5">
              <h4 class="font-mono font-bold text-slate-400 uppercase text-xs tracking-wider">Déroulement Pas-à-Pas :</h4>
              <ol class="space-y-1.5 pl-4 list-decimal list-outside text-slate-300 text-xs">
                ${uc.flow.map(step => `<li class="leading-relaxed pl-1">${step}</li>`).join('')}
              </ol>

              <div class="pt-3 border-t border-slate-800 flex items-center justify-between gap-3">
                <div>
                  <span class="text-[10px] text-slate-400 font-mono block">Réf. Juridique :</span>
                  <span class="text-xs font-bold text-slate-200">${uc.legal}</span>
                </div>
                <a href="${uc.legal_url}" onclick="closeUseCaseModal(); switchTab('legal');" class="bg-gold-500 hover:bg-gold-400 text-obsidian-950 font-bold px-3 py-1.5 rounded-lg text-xs transition whitespace-nowrap">
                  Texte de Loi ↓
                </a>
              </div>
            </div>
          </div>
        </div>
      `;

      const modal = document.getElementById('ucModal');
      if (modal) {
        if (typeof modal.showModal === 'function') {
          modal.showModal();
        } else {
          modal.setAttribute('open', '');
        }
      }
    }

    function closeUseCaseModal() {
      const modal = document.getElementById('ucModal');
      if (modal) {
        if (typeof modal.close === 'function') {
          modal.close();
        } else {
          modal.removeAttribute('open');
        }
      }
    }

    function cycleModalPhase(direction) {
      const phasesSeq = ['p1', 'p2', 'p3', 'p4'];
      const curr = appState.modalWfState.phase;
      let idx = phasesSeq.indexOf(curr);
      if (idx === -1) idx = 0;
      let nextIdx = (idx + direction + phasesSeq.length) % phasesSeq.length;
      setWfPhase(appState.modalWfState.ucId, phasesSeq[nextIdx], true);
    }

    function filterUseCases() {
      renderAppSection('app1');
      renderAppSection('app2');
      renderAppSection('app3');
      renderAppSection('app4');
    }

    function renderLegalTable() {
      const tbody = document.getElementById('table-legal');
      if (!tbody) return;
      tbody.innerHTML = legalTexts.map(item => `
        <tr class="hover:bg-slate-900/40 transition align-top">
          <td class="py-4 px-4">
            <span class="text-[10px] uppercase font-mono text-slate-400 block">${item.jurisdiction}</span>
            <span class="font-mono font-bold text-gold-400 block text-xs">${item.ref}</span>
            <span class="text-xs text-slate-200 font-medium block leading-snug mt-1">${item.official_title}</span>
          </td>
          <td class="py-4 px-4 text-slate-200 text-xs leading-relaxed border-l border-slate-800/60">
            ${item.disposition}
          </td>
          <td class="py-4 px-4 text-amber-200/90 text-xs leading-relaxed border-l border-slate-800/60 bg-amber-500/[0.02]">
            ${item.project_choice}
          </td>
          <td class="py-4 px-4 text-right whitespace-nowrap border-l border-slate-800/60">
            ${item.portal_url ? `
              <a href="${item.portal_url}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 bg-slate-800 hover:bg-gold-500 hover:text-black text-slate-300 text-xs font-bold px-3 py-1.5 rounded transition border border-slate-700">
                ${item.portal_name} ↗
              </a>
            ` : `
              <a href="${item.url}" class="inline-flex items-center gap-1 bg-slate-800 hover:bg-slate-700 text-slate-400 text-xs font-mono px-3 py-1.5 rounded transition border border-slate-700">
                #section-legal
              </a>
            `}
          </td>
        </tr>
      `).join('');
    }

    // Gestion du clavier
    document.addEventListener('keydown', (e) => {
      const modal = document.getElementById('ucModal');
      if (modal && modal.open) {
        if (e.key === 'ArrowRight') cycleModalPhase(1);
        else if (e.key === 'ArrowLeft') cycleModalPhase(-1);
        else if (e.key === 'Escape') closeUseCaseModal();
        else if (e.key === ' ') {
          e.preventDefault();
          toggleWfSimulation(appState.modalWfState.ucId, true);
        }
      } else if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
        const s = document.getElementById('searchInput');
        if (s) {
          e.preventDefault();
          s.focus();
        }
      }
    });

    // Initialisation au chargement
    document.addEventListener('DOMContentLoaded', () => {
      setPortalMode(appState.portalMode);
      renderAppSection('app1');
      renderAppSection('app2');
      renderAppSection('app3');
      renderAppSection('app4');
      renderLegalTable();
    });
"""
