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
      },
      traceability: {
        currentStep: 1,
        selectedProfile: 'p1',
        isPlaying: false,
        timer: null,
        anomaly: null
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
    // NAVIGATION DU GRAND THÉÂTRE VIVANT (LES 5 EXPÉRIENCES CLÉS)
    // =========================================================================
    function switchHeroExp(expId) {
      const exps = ['expA', 'expB', 'expC', 'expD', 'expE'];
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
      if (expId === 'expE') {
        renderTraceStep();
      }
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
        { time: 1000, text: '<span class="text-gold-300">[01.040] WRITE RECORD</span> : Profil civil + Portraits WebP 480x480 (DEC-AET-12) alloués', bytes: 64800, label: '64 800 / 92 160 octets (70%)' },
        { time: 1500, text: '<span class="text-emerald-400">[01.580] COSE_SIGN1</span> : Scellement cryptographique par PaxStation (COSE_Sign1, Tag 18, DEC-AET-10)', bytes: 86528, label: '86 528 / 92 160 octets (94%)' },
        { time: 2000, text: '<span class="text-purple-300">[02.100] HARDWARE LOCK</span> : Fusible physique activé. Mémoire EEPROM immuable.', bytes: 86528, label: '86 528 / 92 160 octets (94%)' },
        { time: 2400, text: '<span class="text-emerald-300 font-bold">[02.450] SUCCÈS TOTAL</span> : Carte ACOSJ 92K gravée avec succès • Prête pour la famille.', bytes: 86528, label: '86 528 / 92 160 octets (94%) - Scellé' }
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

      // 3. Révélation des lignes C et T (test compétitif : C+T visibles = NÉGATIF / CONFORME)
      setTimeout(() => {
        if (lineC) {
          lineC.classList.add('active-red');
          lineC.style.opacity = '1';
          lineC.style.background = '#dc2626';
        }
        if (lineT) {
          lineT.classList.add('active-red');
          lineT.classList.remove('invisible');
          lineT.style.opacity = '1';
          lineT.style.background = '#dc2626';
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
    // EXPÉRIENCE E : GRAND SIMULATEUR ÉVÉNEMENTIEL DE TRAÇABILITÉ DE LA DÉPOUILLE
    // =========================================================================

    const TRACE_PROFILES_DATA = {
      p0: {
        id: "p0",
        name: "Profil Humain — Dignité Post-Mortem & Démonstrateur Mémoriel",
        badge: "Profil Humain · Sujet de Droit",
        badgeClass: "bg-purple-950 border border-purple-500/40 text-purple-300",
        species: "Homo sapiens (TaxID NCBI: 9606 - Être Humain)",
        deceased: "Guy Heyman (1942 — 2026, Matricule État Civil #NAM-2026-0814)",
        depouilleId: "AET-HUM-2026-BE-0814",
        carrier: "Fourgon Funéraire Agréé SPW #1-PFN-884 (Caisson Isotherme 0°C à +4°C)",
        thermalTarget: "Crémation Homologuée 850°C OU Démonstrateur Sarcomusation (70°C/1h) - DEC-AET-15",
        thermalCore: "70.2°C en continu pendant 62 minutes (Bioréacteur Démonstrateur Hermetia illucens)",
        dest: "Urne Cinéraire Noble & Arbre du Souvenir en Forêt Cinéraire Privée (DEC-AET-05)",
        legal: "Loi du 20 juillet 1971, Décret wallon du 6 mars 2009 modifiant le CDLD, Art. L1232-24 CDLD & Modèle IIIC réglementaire",
        events: {
          1: {
            title: "Constat de Décès & Déclaration Initiale",
            stage_label: "Événement 1 / 6 • Survenance & Constat de Décès",
            location_name: "Domicile du défunt / Chambre d'Hôpital (Rue Saint-Aubain, Namur)",
            location_details: "Domicile du défunt / Chambre d'Hôpital (ex: Rue Saint-Aubain, Namur - GPS: 50.4674° N, 4.8719° E)",
            gps_coords: "50.4674° N, 4.8719° E (Namur - Domicile/Hôpital) [±0.5 m RTK]",
            actor: "Médecin traitant / Médecin légiste (Certificat Modèle III C / III D)",
            actor_role: "Médecin Traitant / Médecin Légiste",
            actor_badge: "INAMI #1-84912-22 • Certificat Modèle III C / III D",
            seal_id: "SCL-HUM-2026-INIT",
            seal_status: "Bracelet Poignet Inviolable NFC/QR Ed25519 Posé & Scellé",
            seal_status_code: "SCL-HUM-2026-INIT (SCEL_INITIALISE_NON_ROMPU)",
            temp_readout: "18.5°C",
            temp_badge: "AMBIANTE INITIALE",
            temp_target: "Avant prise en charge en caisson réfrigéré",
            temp_fill: "25%",
            temp_fill_class: "trace-gauge-fill bg-slate-500",
            temp_icon: "🌡️",
            legal: "Loi du 20 juillet 1971 sur les funérailles et sépultures & Loi du 13 juin 1986 sur le don d'organes",
            summary: "Constat de la réalité du décès par le médecin traitant / légiste, visa d'absence d'obstacle médico-légal (parquet non saisi), consultation du registre SPF Santé Publique pour don d'organes (Loi 13 juin 1986, consentement présumé), pose du bracelet inamovible inviolable au poignet avec scellé NFC/QR Ed25519 (SCL-HUM-2026-INIT).",
            action_label: "⚡ Sceller le Bracelet Inviolable NFC/QR & Signer le Modèle III C",
            form_fields: [
              { label: "Identifiant Dépouille & Matricule", name: "depouille_id", badge: "État Civil #NAM", value: "AET-HUM-2026-BE-0814 (Matricule État Civil #NAM-2026-0814)" },
              { label: "Identité Défunt & Espèce", name: "identity_name", badge: "Sujet de Droit", value: "Guy Heyman (1942 — 2026, TaxID NCBI: 9606)" },
              { label: "Médecin Certificateur Assermenté", name: "officer_name", badge: "INAMI Agréé", value: "Dr. Bernard Moreau (INAMI #1-84912-22, Certificat Modèle III C / III D)" },
              { label: "Lieu de Survenance du Décès", name: "location_event", badge: "Namur", value: "Domicile du défunt / Chambre d'Hôpital (ex: Rue Saint-Aubain, Namur - GPS: 50.4674° N, 4.8719° E)" },
              { label: "Contrôle Réglementaire Parquet", name: "legal_obstacle", badge: "Parquet Non Saisi", value: "Visa d'absence d'obstacle médico-légal (cause naturelle, parquet non saisi)" },
              { label: "Don d'Organes (SPF Santé Publique)", name: "organ_donation", badge: "Loi 13/06/1986", value: "Registre SPF Santé Publique consulté (Loi 13 juin 1986, consentement présumé)" },
              { label: "Scellé Bracelet Inviolable Poignet", name: "seal_number", badge: "Ed25519 NFC/QR", value: "SCL-HUM-2026-INIT (Bracelet inamovible inviolable scellé)" }
            ]
          },
          2: {
            title: "Prise en Charge & Transport Primaire du Corps",
            stage_label: "Événement 2 / 6 • Logistique Funéraire & Chaîne du Froid",
            location_name: "Trajet Domicile ➔ Salon Funéraire PaxFunèbre (Itinéraire Agréé N4, Namur)",
            location_details: "Trajet Domicile ➔ Salon Funéraire PaxFunèbre (Itinéraire Agréé N4, Namur - GPS: 50.4632° N, 4.8631° E)",
            gps_coords: "50.4632° N, 4.8631° E (Namur - Itinéraire Agréé N4) [±0.8 m RTK]",
            actor: "Chauffeur-porteur agréé funéraire & Police communale",
            actor_role: "Chauffeur-Porteur Agréé Funéraire",
            actor_badge: "Habilitation Funéraire SPW #PFN-WAL-2026-44 • Police Communale",
            seal_id: "SCL-HUM-2026-INIT",
            seal_status: "Scellé de Housse de Transport Intact sous Surveillance Télématique",
            seal_status_code: "SCL-HUM-2026-INIT (SCEL_INTACT_EN_TRANSIT)",
            temp_readout: "+2.8°C",
            temp_badge: "CONFORME (0°C à +4°C)",
            temp_target: "Consigne caisson réfrigéré : 0.0°C à +4.0°C",
            temp_fill: "28%",
            temp_fill_class: "trace-gauge-fill bg-sky-400",
            temp_icon: "❄️",
            legal: "Décret wallon du 6 mars 2009 modifiant le CDLD & Règlement de police (références à confirmer par un juriste)",
            summary: "Autorisation communale de transport de corps avant mise en bière (délai légal < 24h/48h sous froid), fourgon funéraire habilité SPW, monitoring continu de la chaîne du froid (+2.8°C consigne 0°C..+4°C), scellé de housse de transport intact.",
            action_label: "⚡ Valider le Transport Réfrigéré SPW & Émarger le Bon de Conduite",
            form_fields: [
              { label: "Fourgon Funéraire Agréé SPW", name: "vehicle_id", badge: "Habilité SPW", value: "Fourgon Funéraire Agréé SPW #1-PFN-884 (Caisson Isotherme 0°C à +4°C)" },
              { label: "Chauffeur-Porteur Titulaire", name: "driver_name", badge: "Carte Pro SPW", value: "Laurent Delcroix (Chauffeur-porteur agréé funéraire & Police communale)" },
              { label: "Autorisation Communale Transport", name: "police_clearance", badge: "Délai Légal OK", value: "Autorisation communale de transport avant mise en bière (délai < 24h/48h sous froid)" },
              { label: "Monitoring Chaîne du Froid", name: "temp_sensor", badge: "Conforme ❄️", value: "+2.8°C continu (Consigne 0°C à +4°C régulée en caisson isotherme)" },
              { label: "Scellé de Housse de Transport", name: "seal_check", badge: "Non Rompu 🔒", value: "Scellé de housse de transport intact • 0 infraction de confinement" },
              { label: "Lieu & Itinéraire de Transit", name: "transit_route", badge: "N4 Namur", value: "Trajet Domicile ➔ Salon Funéraire PaxFunèbre (Itinéraire Agréé N4, Namur - GPS: 50.4632° N, 4.8631° E)" }
            ]
          },
          3: {
            title: "Salon Funéraire / Laboratoire de Thanatopraxie",
            stage_label: "Événement 3 / 6 • Thanatopraxie & Contrôle Pacemaker Obligatoire",
            location_name: "Funérarium PaxFunèbre, Rue Saint-Aubain 14, 5000 Namur (Cellule #C3)",
            location_details: "Funérarium PaxFunèbre, Rue Saint-Aubain 14, 5000 Namur (Cellule de conservation frigorifique #C3)",
            gps_coords: "50.4674° N, 4.8719° E (Funérarium PaxFunèbre, Rue Saint-Aubain 14, Namur)",
            actor: "Thanatopracteur certifié & Maître de cérémonie",
            actor_role: "Thanatopracteur Certifié & Maître de Cérémonie",
            actor_badge: "Diplôme Thanatopraxie #WAL-THAN-2026-12 • Salon PaxFunèbre",
            seal_id: "SCL-HUM-2026-INIT",
            seal_status: "Scellé Vérifié Non Rompu • Enregistrement au Registre Funéraire",
            seal_status_code: "SCL-HUM-2026-INIT (SCEL_VERIFIE_NON_ROMPU)",
            temp_readout: "+2.8°C",
            temp_badge: "CELLULE #C3 (CONFORME)",
            temp_target: "Régulation cellule frigorifique : +2.0°C à +3.5°C",
            temp_fill: "28%",
            temp_fill_class: "trace-gauge-fill bg-sky-400",
            temp_icon: "❄️",
            legal: "Art. L1232-24 CDLD & Modèle IIIC réglementaire (exérèse pacemaker obligatoire) & Décret wallon du 6 mars 2009",
            summary: "Contrôle d'exérèse chirurgicale OBLIGATOIRE du stimulateur cardiaque (Pacemaker / DAE) selon Art. L1232-24 CDLD & Modèle IIIC réglementaire (danger d'explosion pyrotechnique 850°C-1050°C et pollution), attestation médicale INAMI de neutralisation de la pile au lithium, mise en bière cercueil agréé.",
            action_label: "⚡ Certifier l'Exérèse Pacemaker & Sceller la Mise en Bière",
            form_fields: [
              { label: "Cellule de Conservation Frigorifique", name: "assigned_cell", badge: "Cellule #C3", value: "Funérarium PaxFunèbre, Rue Saint-Aubain 14, Namur (Cellule frigorifique #C3, +2.8°C)" },
              { label: "Exérèse Stimulateur Cardiaque", name: "pacemaker_excision", badge: "Art. L1232-24 & Modèle IIIC", value: "OBLIGATOIRE : Contrôle d'exérèse chirurgicale du stimulateur cardiaque (Pacemaker / DAE) selon Art. L1232-24 CDLD & Modèle IIIC validé" },
              { label: "Neutralisation Pile Lithium", name: "lithium_clearance", badge: "Visa INAMI", value: "Attestation médicale INAMI de neutralisation de la pile au lithium certifiée (anti-explosion > 250°C)" },
              { label: "Soins & Toilette Mortuaire", name: "thanato_care", badge: "Thanatopraxie", value: "Soins de thanatopraxie accomplis dans le strict respect de la dignité post-mortem" },
              { label: "Mise en Bière Cercueil Agréé", name: "coffin_boxing", badge: "Agrément SPW", value: "Mise en bière validée en cercueil agréé avec pose des scellés funéraires" }
            ]
          },
          4: {
            title: "Maison Communale / Mairie (Déclaration & Autorisation)",
            stage_label: "Événement 4 / 6 • Déclaration d'État Civil & Permis Officiel",
            location_name: "Hôtel de Ville de Namur, Service Population & État Civil, Esplanade de l'Hôtel de Ville",
            location_details: "Hôtel de Ville de Namur, Service Population & État Civil, Esplanade de l'Hôtel de Ville, 5000 Namur",
            gps_coords: "50.4649° N, 4.8654° E (Hôtel de Ville de Namur, Esplanade)",
            actor: "Officier de l'État Civil / Bourgmestre",
            actor_role: "Officier de l'État Civil / Bourgmestre",
            actor_badge: "Ville de Namur • Sceau Municipal #ETAT-CIVIL-NAM-04",
            seal_id: "SCL-MUN-NAM-2026-0814",
            seal_status: "Sceau Municipal de Cercueil Apposé (Officier État Civil)",
            seal_status_code: "SCL-MUN-NAM-2026-0814 (SCEL_MUNICIPAL_VALIDE)",
            temp_readout: "20.0°C",
            temp_badge: "AMB. ÉTAT CIVIL",
            temp_target: "Guichet administratif officiel",
            temp_fill: "38%",
            temp_fill_class: "trace-gauge-fill bg-indigo-400",
            temp_icon: "🏛️",
            legal: "Loi du 20 juillet 1971 & Décret wallon du 6 mars 2009 modifiant le CDLD, Art. 15 (références à confirmer par un juriste)",
            summary: "Acte de décès n° 0814/2026, vérification des dernières volontés du défunt (Loi 1971 / Art. 15 CDLD : sépulture, rite, mode de sépulture), délivrance du permis officiel de sépulture / crémation, scellement municipal du cercueil.",
            action_label: "⚡ Délivrer le Permis Officiel & Sceller l'Autorisation Municipale",
            form_fields: [
              { label: "Lieu de Déclaration Officielle", name: "city_hall_loc", badge: "Hôtel de Ville", value: "Hôtel de Ville de Namur, Service Population & État Civil, Esplanade de l'Hôtel de Ville" },
              { label: "Acte de Décès État Civil", name: "death_act_num", badge: "Acte #0814/2026", value: "Acte de décès n° 0814/2026 valablement enregistré aux registres de Namur" },
              { label: "Vérification Dernières Volontés", name: "last_wishes_check", badge: "Loi 1971 / Art. 15", value: "Dernières volontés vérifiées : respect du mode de sépulture mémoriel et du rite déclaré" },
              { label: "Permis Officiel de Sépulture", name: "burial_permit", badge: "Permis Délivré", value: "Délivrance du permis officiel de sépulture / crémation n° PERM-2026-NAM-0814" },
              { label: "Scellement Municipal Cercueil", name: "municipal_seal", badge: "Sceau Posé", value: "Scellement municipal du cercueil apposé par le délégué du Bourgmestre" }
            ]
          },
          5: {
            title: "Crématorium Agréé OU Unité de Sarcomusation (Transformation)",
            stage_label: "Événement 5 / 6 • Procédé Thermique & Verrou The Iron Gate G2",
            location_name: "Crématorium du Cœur de Wallonie, Ciney OU Unité Hermetia illucens (Démonstrateur Prospectif)",
            location_details: "Crématorium du Cœur de Wallonie, Ciney (GPS: 50.2841° N, 5.0933° E) OU Unité de Sarcomusation Mémorielle Hermetia illucens (Démonstrateur Prospectif)",
            gps_coords: "50.2841° N, 5.0933° E (Crématorium Ciney / Unité Hermetia illucens)",
            actor: "Opérateur de crémation / Responsable de bioconversion mémorielle",
            actor_role: "Opérateur Crémation / Démonstrateur Mémoriel",
            actor_badge: "Agrément Intercommunal Crématorium Ciney #CRM-WAL-02 • Démonstrateur DEC-AET-15",
            seal_id: "SCL-SAS-CRMCIN-0814",
            seal_status: "Sas Four / Bioréacteur Verrouillé sous Scellé Horodaté",
            seal_status_code: "SCL-SAS-CRMCIN-0814 (SAS_INSPECTE_VERROUILLE)",
            temp_readout: "850.0°C / 70.2°C",
            temp_badge: "CRÉMATION 850°C OU DÉMONSTRATEUR 70.2°C",
            temp_target: "Four crématoire : 850°C | Bioréacteur démonstrateur : 70°C/1h",
            temp_fill: "95%",
            temp_fill_class: "trace-gauge-fill bg-amber-500",
            temp_icon: "🔥",
            legal: "Décret wallon du 6 mars 2009 modifiant le CDLD & Décision Kudoro DEC-AET-15 (démonstrateur prospectif) (références à confirmer par un juriste)",
            summary: "Visa d'exérèse pacemaker obligatoire avant introduction, four crématoire 850°C OU Bioréacteur démonstrateur (pasteurisation 70°C/1h continue selon DEC-AET-05/15), verrou absolu The Iron Gate Gate G2 (démonstrateur prospectif : HUMAN_REMAINS_DETECTED ➔ interdiction mathématique de toute filière alimentaire/technique), recueil des reliques purifiées.",
            action_label: "⚡ Certifier le Cycle Thermique & Verrouiller les Reliques Purifiées",
            form_fields: [
              { label: "Lieu de Transformation Agréé", name: "crematorium_loc", badge: "Ciney / Sas Dédié", value: "Crématorium du Cœur de Wallonie, Ciney (GPS: 50.2841° N, 5.0933° E) OU Unité Hermetia illucens" },
              { label: "Visa Exérèse Pacemaker Amont", name: "pacemaker_visa", badge: "VISA CONFORME", value: "Visa d'exérèse pacemaker obligatoire vérifié avant toute introduction" },
              { label: "Cycle Thermique Homologué", name: "thermal_protocol", badge: "DEC-AET-15", value: "Crémation Homologuée 850°C OU Démonstrateur Sarcomusation (70°C/1h) - DEC-AET-15" },
              { label: "Température Cœur Mesurée", name: "core_temp", badge: "Télémétrie P-T-t", value: "70.2°C en continu pendant 62 minutes (Bioréacteur Démonstrateur Hermetia illucens)" },
              { label: "Verrou The Iron Gate Gate G2", name: "iron_gate_g2", badge: "Porte G2 Inviolable", value: "HUMAN_REMAINS_DETECTED : Interdiction mathématique de toute filière alimentaire/technique (démonstrateur prospectif)" },
              { label: "Recueil Reliques Purifiées", name: "relics_recovery", badge: "Dignité 100%", value: "Recueil des reliques purifiées en urne cinéraire étanche sans mélange" }
            ]
          },
          6: {
            title: "Lieu de Sépulture & Recueillement Final",
            stage_label: "Événement 6 / 6 • The Iron Gate, Sépulture & Clôture Ed25519",
            location_name: "Forêt Cinéraire Privée de la Basse-Sambre (Parcelle Mémorielle #FM-08)",
            location_details: "Forêt Cinéraire Privée de la Basse-Sambre (Parcelle Mémorielle de repos éternel #FM-08)",
            gps_coords: "50.4485° N, 4.6712° E (Forêt Cinéraire Privée de la Basse-Sambre, Parcelle #FM-08)",
            actor: "Garde-forestier DNF, Conseiller funéraire & Famille",
            actor_role: "Garde-Forestier DNF & Conseiller Funéraire",
            actor_badge: "Assermentation DNF #DNF-WAL-8810 • Master Key Ed25519 PaxFunèbre",
            seal_id: "CERT-HUM-2026-LOT-0814-ED25519",
            seal_status: "Certificat de Sépulture & Clôture Scellé Ed25519 (AET-SPEC-CERT-001)",
            seal_status_code: "CERT-HUM-2026-LOT-0814-ED25519 (LOT_SIGNE_ET_REMIS)",
            temp_readout: "18.0°C",
            temp_badge: "REPOS ÉTERNEL",
            temp_target: "Ambiance solennelle forêt cinéraire",
            temp_fill: "35%",
            temp_fill_class: "trace-gauge-fill bg-emerald-400",
            temp_icon: "🕊️",
            legal: "Loi du 20 juillet 1971, Décret wallon sur les sépultures & Arbitrage Kudoro DEC-AET-05 (références à confirmer par un juriste)",
            summary: "Remise solennelle du Médaillon / Carte mémorielle ACOSJ 92 Ko avec l'acte d'hommage et le mémo vocal, amendement biologique au pied de l'arbre du souvenir familial (dérogation mémorielle forestière DEC-AET-05), scellement Ed25519 du certificat de sépulture inviolable final.",
            action_label: "✔ Traçabilité Humaine 100% Validée & Scellée (Relancer dès le Début)",
            form_fields: [
              { label: "Lieu de Sépulture & Repos Éternel", name: "burial_plot", badge: "Forêt Cinéraire", value: "Forêt Cinéraire Privée de la Basse-Sambre (Parcelle Mémorielle de repos éternel #FM-08)" },
              { label: "Support Silicium ACOSJ 92K", name: "acosj_support", badge: "ACOSJ 92 Ko", value: "Remise solennelle du Médaillon / Carte mémorielle ACOSJ 92 Ko avec l'acte d'hommage et le mémo vocal" },
              { label: "Amendement & Arbre du Souvenir", name: "relics_destination", badge: "DEC-AET-05", value: "Amendement biologique au pied de l'arbre du souvenir familial (dérogation mémorielle forestière DEC-AET-05)" },
              { label: "Certificat de Sépulture Inviolable", name: "batch_cert_id", badge: "Ed25519 Scellé", value: "Scellement Ed25519 du certificat de sépulture inviolable final (AET-SPEC-CERT-001)" },
              { label: "Recueillement & Hommage Familial", name: "family_handover", badge: "Recueillement", value: "Remise solennelle effectuée auprès des proches dans le respect absolu des volontés du défunt" }
            ]
          }
        }
      },
      p1: {
        id: "p1",
        name: "Profil 1 — Compagnie (Catégorie 1 Mémoriel)",
        badge: "Profil 1 · Catégorie 1 Mémoriel",
        badgeClass: "bg-emerald-950 border border-emerald-500/40 text-emerald-300",
        species: "Canis familiaris (TaxID NCBI: 9615 - Chien de Compagnie)",
        deceased: "Adrien de Valcourt (ou Canis familiaris TaxID 9615)",
        depouilleId: "DEP-2026-BEL-99201",
        carrier: "Fourgon Funéraire Agréé 1-AFR-842 (Frigo bi-température)",
        thermalTarget: "Pasteurisation Continue (70°C, 1 heure continue) - DEC-AET-05",
        thermalCore: "70.4°C en continu pendant 62 minutes (Pression atmosphérique)",
        dest: "Urne Cinéraire Noble & Arbre du Souvenir Forêt DNF (DEC-AET-05)",
        legal: "Arrêté royal du 27 avril 2007 & Arbitrage Kudoro DEC-AET-05 (références à confirmer par un juriste)",
        locations: {
          1: "Domicile du déclarant / Clinique Vétérinaire (Liège, Sart-Tilman - GPS: 50.6333° N, 5.5667° E)",
          2: "Trajet Domicile -> Centre Logistique Liège (Transit E25 / Rocade Sud - GPS: 50.6120° N, 5.5340° E)",
          3: "Unité Centrale AeterniTrak Liège, Rue de l'Énergie 12, Sart-Tilman (GPS: 50.6412° N, 5.5721° E)",
          4: "Laboratoire de Préparation Stérile & Contrôles Amonts, Liège (GPS: 50.6412° N, 5.5721° E)",
          5: "Unité de Bioconversion Hermetia illucens & Traitement Thermique, Liège (GPS: 50.6412° N, 5.5721° E)",
          6: "Salon de Remise Solennelle PaxFunèbre Liège & Forêt DNF (GPS: 50.6412° N, 5.5721° E)"
        },
        location_names: {
          1: "Domicile du déclarant / Clinique (Liège)",
          2: "Itinéraire Transit Agréé E25 (Rocade Sud)",
          3: "Unité Centrale AeterniTrak Liège (Cellule #B4)",
          4: "Salle Technique Stérile & BioLab AeterniCore",
          5: "Sas Hermétique de Bioconversion & Autoclaves HP",
          6: "Salon Solennel d'Hommage & Forêt DNF"
        }
      },
      p2: {
        id: "p2",
        name: "Profil 2 — Faune Sauvage (Catégorie 1/2 DNF)",
        badge: "Profil 2 · Faune Sauvage DNF",
        badgeClass: "bg-amber-950 border border-amber-500/40 text-amber-300",
        species: "Sus scrofa (TaxID NCBI: 9823 - Sanglier d'Europe)",
        deceased: "Sanglier Mâle Adulte ~85 kg (Balisage Forêt Saint-Hubert)",
        depouilleId: "DNF-2026-ARD-0418",
        carrier: "Véhicule Tout-Terrain Sanitaire DNF #WL-4890",
        thermalTarget: "Stérilisation Européenne Méthode 1 (133°C, 3 bars, 20 min)",
        thermalCore: "133.8°C, 3.1 bars absolus pendant 22 minutes",
        dest: "Valorisation Énergétique / Biocarburant Industriel Agréé (Cat 2)",
        legal: "Règlement (CE) n° 1069/2009 & Code forestier wallon (références à confirmer par un juriste)",
        locations: {
          1: "Massif Forestier DNF de Saint-Hubert (Balisage GPS: 50.0267° N, 5.3742° E)",
          2: "Transit Véhicule Tout-Terrain DNF #WL-4890 vers Centre Sanitaire (Ardenne)",
          3: "Centre Sanitaire Régional Collecteur DNF Arlon/Marche",
          4: "Laboratoire Vétérinaire Régional (Dépistage PCR PPA & CWD prions)",
          5: "Unité Autoclave Haute Pression (Méthode 1 : 133°C, 3 bars, 20 min)",
          6: "Usine de Biocarburant Agréée Cat 2 / Valorisation Énergétique"
        },
        location_names: {
          1: "Massif Forestier DNF de Saint-Hubert",
          2: "Transit Véhicule Sanitaire DNF #WL-4890",
          3: "Centre Sanitaire Régional DNF",
          4: "Laboratoire Vétérinaire Régional",
          5: "Autoclave Haute Pression Méthode 1",
          6: "Usine Biocarburant Cat 2"
        }
      },
      p3: {
        id: "p3",
        name: "Profil 3 — Élevage / Ferme (Catégorie 2 Sanitel)",
        badge: "Profil 3 · Élevage Sanitel C2",
        badgeClass: "bg-indigo-950 border border-indigo-500/40 text-indigo-300",
        species: "Bos taurus (TaxID NCBI: 9913 - Bovin Domestique)",
        deceased: "Génisse Laitière (Boucle Auriculaire BE-0492-8172)",
        depouilleId: "SAN-2026-AGR-7731",
        carrier: "Camion Benne Étanche Sanitaire Élevage #2-AGR-109",
        thermalTarget: "Stérilisation Européenne Méthode 1 (133°C, 3 bars, 20 min)",
        thermalCore: "134.1°C, 3.2 bars absolus pendant 20 minutes",
        dest: "Combustion Cimenterie & Graisses Techniques (Catégorie 2)",
        legal: "Règlement (CE) n° 1069/2009 & Identification Sanitel AFSCA (références à confirmer par un juriste)",
        locations: {
          1: "Exploitation Agricole Bovine, Ciney (GPS: 50.2956° N, 5.1011° E)",
          2: "Transit Camion Benne Sanitaire #2-AGR-109 (Réseau agricole N97)",
          3: "Quai de Déchargement Hermétique Usine Sous-Produits C2",
          4: "Poste de Contrôle Sanitaire (Boucle Sanitel & Temps d'attente médicamenteux)",
          5: "Autoclave Industriel Réglementaire (Méthode 1 : 133°C, 3 bars, 20 min)",
          6: "Cimenterie Agréée / Graisses Techniques Industrielles (Catégorie 2)"
        },
        location_names: {
          1: "Exploitation Agricole Bovine, Ciney",
          2: "Transit Camion Sanitaire Élevage",
          3: "Quai Usine Sous-Produits C2",
          4: "Poste Contrôle Sanitaire & Sanitel",
          5: "Autoclave Méthode 1 (133°C/3 bars)",
          6: "Cimenterie Agréée / Graisses C2"
        }
      },
      p4: {
        id: "p4",
        name: "Profil 4 — Déchets d'Abattoir (Cat 1 MRS Dénaturé)",
        badge: "Profil 4 · Déchets Abattoir MRS C1",
        badgeClass: "bg-rose-950 border border-rose-500/40 text-rose-300",
        species: "Bos taurus (Matériel à Risque Spécifié MRS - Crâne & Moelle)",
        deceased: "Lot Déchets Abattoir Liège #ABT-2026-MRS-44",
        depouilleId: "MRS-2026-ABT-0914",
        carrier: "Conteneur Hermétique Plombé #CONT-MRS-12",
        thermalTarget: "Dénaturation Bleu 0,5% + Méthode 1 (133°C, 3 bars, 20 min)",
        thermalCore: "134.5°C, 3.3 bars absolus pendant 25 minutes",
        dest: "Incinération Dédiée Haute Température Cimenterie (Catégorie 1 MRS)",
        legal: "Règlement (CE) n° 999/2001 annexe V (règles MRS anti-prion) (référence à confirmer par un juriste)",
        locations: {
          1: "Abattoir Industriel Agréé de Liège (GPS: 50.6512° N, 5.5418° E)",
          2: "Transit Conteneur Hermétique Plombé #CONT-MRS-12",
          3: "Plateforme Déchets Haut Risque Catégorie 1 MRS",
          4: "Poste de Dénaturation Chimique Obligatoire au Bleu de Méthylène 0,5%",
          5: "Traitement Thermique Combiné Dénaturation + Méthode 1 (133°C, 3 bars, 20 min)",
          6: "Combustion Haute Température en Cimenterie Agréée (Catégorie 1 MRS)"
        },
        location_names: {
          1: "Abattoir Industriel Agréé de Liège",
          2: "Transit Conteneur Plombé #CONT-MRS-12",
          3: "Plateforme Déchets Cat 1 MRS",
          4: "Poste Dénaturation Bleu de Méthylène 0,5%",
          5: "Traitement Dénaturation + Méthode 1",
          6: "Incinération Cimenterie Cat 1 MRS"
        }
      }
    };

    function setTraceProfile(profId) {
      if (!TRACE_PROFILES_DATA[profId]) return;
      appState.traceability.selectedProfile = profId;
      ["p0", "p1", "p2", "p3", "p4"].forEach(id => {
        const btn = document.getElementById(`btn-trace-prof-${id}`);
        if (btn) {
          if (id === profId) {
            btn.className = "px-2.5 py-1.5 rounded-lg font-bold bg-gold-500 text-obsidian-950 shadow";
          } else {
            btn.className = "px-2.5 py-1.5 rounded-lg text-slate-300 hover:text-white";
          }
        }
      });
      addTraceCryptoLog(`[PROFIL] Sélection du profil : ${TRACE_PROFILES_DATA[profId].name}`);
      playTone("soft-bell");
      renderTraceStep();
    }

    function goToTraceStep(stepNum) {
      if (stepNum < 1 || stepNum > 6) return;
      appState.traceability.currentStep = stepNum;
      appState.traceability.anomaly = null;
      const anomalyBanner = document.getElementById("trace-anomaly-banner");
      if (anomalyBanner) anomalyBanner.classList.add("hidden");
      renderTraceStep();
      playTone("soft-bell");
    }

    function nextTraceStep() {
      const cur = appState.traceability.currentStep;
      const profKey = appState.traceability.selectedProfile || "p1";
      if (cur < 6) {
        goToTraceStep(cur + 1);
      } else {
        if (profKey === "p0") {
          addTraceCryptoLog("[CLÔTURE] Traçabilité humaine 6/6 validée. Certificat de sépulture Ed25519 émis.");
        } else {
          addTraceCryptoLog("[CLÔTURE] Traçabilité complète 6/6 validée. Certificat Ed25519 émis.");
        }
        playTone("memorial-chord");
        const actionBtn = document.getElementById("btn-trace-action");
        if (actionBtn) {
          actionBtn.innerHTML = "✔ Traçabilité 100% Validée &amp; Scellée (Relancer dès le Début)";
          actionBtn.className = "wf-btn wf-btn-primary text-xs font-bold flex-1 py-2.5";
          actionBtn.onclick = function() {
            actionBtn.onclick = nextTraceStep;
            goToTraceStep(1);
          };
        }
      }
    }

    function prevTraceStep() {
      const cur = appState.traceability.currentStep;
      if (cur > 1) goToTraceStep(cur - 1);
    }

    function resetTraceTimeline() {
      stopTraceAutoPlay();
      appState.traceability.currentStep = 1;
      appState.traceability.anomaly = null;
      const anomalyBanner = document.getElementById("trace-anomaly-banner");
      if (anomalyBanner) anomalyBanner.classList.add("hidden");
      addTraceCryptoLog("[RÉINITIALISATION] Retour à l'Événement 1 (Constat de Décès)");
      renderTraceStep();
      playTone("soft-bell");
    }

    function toggleTraceAutoPlay() {
      const state = appState.traceability;
      const btn = document.getElementById("btn-trace-autoplay");
      if (state.isPlaying) {
        stopTraceAutoPlay();
      } else {
        state.isPlaying = true;
        if (btn) {
          btn.innerHTML = "⏸ Suspendre Auto-Play";
          btn.classList.add("active");
        }
        if (state.currentStep >= 6) {
          state.currentStep = 1;
        }
        renderTraceStep();
        playTone("soft-bell");
        state.timer = setInterval(() => {
          if (state.currentStep < 6) {
            goToTraceStep(state.currentStep + 1);
          } else {
            stopTraceAutoPlay();
          }
        }, 2200);
      }
    }

    function stopTraceAutoPlay() {
      const state = appState.traceability;
      state.isPlaying = false;
      if (state.timer) {
        clearInterval(state.timer);
        state.timer = null;
      }
      const btn = document.getElementById("btn-trace-autoplay");
      if (btn) {
        btn.innerHTML = "<span>⚡</span> Auto-Play (6 Événements)";
        btn.classList.remove("active");
      }
    }

    function addTraceCryptoLog(msg) {
      const terminal = document.getElementById("trace-crypto-log");
      if (!terminal) return;
      const now = new Date().toISOString().substring(11, 23);
      const div = document.createElement("div");
      div.className = msg.includes("[ALERTE]") || msg.includes("VIOLATION") ? "text-rose-400 font-bold" : (msg.includes("[SUCCÈS]") || msg.includes("[CLÔTURE]") ? "text-emerald-400" : "text-slate-300");
      div.textContent = `> [${now}] ${msg}`;
      terminal.appendChild(div);
      terminal.scrollTop = terminal.scrollHeight;
    }

    function simulateTraceAnomaly() {
      const state = appState.traceability;
      const cur = state.currentStep;
      const profKey = state.selectedProfile || "p1";
      const banner = document.getElementById("trace-anomaly-banner");
      const node = document.getElementById(`trace-node-${cur}`);
      const sealBadge = document.getElementById("trace-seal-status-badge");
      const tempBadge = document.getElementById("trace-temp-badge");

      let code = "ERR_ANOMALY";
      let title = "Anomalie Détectée";
      let desc = "";

      if (profKey === "p0") {
        if (cur === 1) {
          code = "ERR_MEDICO_LEGAL_OBSTACLE";
          title = "Obstacle Médico-Légal / Saisie du Parquet";
          desc = "Suspicion de mort violente ou indéterminée. Saisie immédiate du Procureur du Roi (Loi 1971). Interdiction absolue de toute levée de corps ou manipulation avant ordonnance de levée d'obstacle.";
          if (sealBadge) {
            sealBadge.textContent = "🚨 PARQUET SAISI";
            sealBadge.className = "px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-rose-950 text-rose-300 border border-rose-500/60 animate-pulse";
          }
        } else if (cur === 2) {
          code = "ERR_TRANSPORT_TIME_EXCEEDED";
          title = "Dépassement du Délai Légal de Transport sans Froid (> 24h)";
          desc = "Délai légal de transport avant mise en bière sans maintien sous froid excédé selon le décret funéraire wallon. Blocage administratif et signalement à la Police communale.";
          if (tempBadge) {
            tempBadge.textContent = "🚨 EXCURSION THERMIQUE (+8.6°C)";
            tempBadge.className = "px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-rose-950 text-rose-300 border border-rose-500/60 animate-pulse";
          }
        } else if (cur === 3) {
          code = "ERR_PACEMAKER_EXPLOSION_HAZARD";
          title = "Présence de Stimulateur Cardiaque Non Neutralisé (Art. L1232-24 CDLD & Modèle IIIC réglementaire)";
          desc = "Dispositif cardiaque actif ou pile lithium détectée. Risque majeur d'explosion pyrotechnique (> 250°C) et de pollution environnementale. Refus d'admission en crémation ou bioconversion tant que l'exérèse n'est pas certifiée par médecin INAMI.";
          if (sealBadge) {
            sealBadge.textContent = "🚨 ALERTE PACEMAKER";
            sealBadge.className = "px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-rose-950 text-rose-300 border border-rose-500/60 animate-pulse";
          }
        } else if (cur === 4) {
          code = "ERR_CIVIL_PERMIT_REFUSED";
          title = "Absence de Permis de Crémation / Déclaration Incomplète";
          desc = "Incohérence entre les dernières volontés déclarées et la demande de la famille (Loi 1971 / Art. 15 CDLD). Permis municipal suspendu par l'officier de l'état civil.";
        } else if (cur === 5) {
          code = "ERR_IRON_GATE_G2_HUMAN_REMAINS";
          title = "Alerte The Iron Gate Gate G2 : Dépouille Humaine Détectée (Démonstrateur Prospectif)";
          desc = "Oracle The Iron Gate : déclenchement du verrou absolu (démonstrateur prospectif : HUMAN_REMAINS_DETECTED ➔ interdiction mathématique et irrévocable de toute filière alimentaire animale ou valorisation technique). Traitement mémoriel exclusif.";
        } else if (cur === 6) {
          code = "ERR_MEMORIAL_FOREST_DECREE";
          title = "Non-Conformité de Sépulture Forestière (DEC-AET-05)";
          desc = "Incompatibilité de la parcelle mémorielle avec le Code forestier wallon ou urne non biodégradable. Émission du certificat Ed25519 bloquée.";
        }
      } else {
        if (cur === 1) {
          code = "ERR_SEAL_INIT_FAILURE";
          title = "Défaut de Scellement NFC / Clé Inconnue";
          desc = "La puce NFC du scellé physique présente un identifiant révoqué ou corrompu. Blocage immédiat de la prise en charge.";
          if (sealBadge) {
            sealBadge.textContent = "🚨 SCELLÉ INVALIDE";
            sealBadge.className = "px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-rose-950 text-rose-300 border border-rose-500/60 animate-pulse";
          }
        } else if (cur === 2) {
          code = "ERR_COLD_CHAIN_EXCURSION";
          title = "Rupture de la Chaîne du Froid (> +6.0°C)";
          desc = "Sonde thermique télématique mesurant +8.4°C pendant plus de 15 minutes. Alerte transmise immédiatement à l'AFSCA et mise sous séquestre.";
          if (tempBadge) {
            tempBadge.textContent = "🚨 EXCURSION THERMIQUE (+8.4°C)";
            tempBadge.className = "px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-rose-950 text-rose-300 border border-rose-500/60 animate-pulse";
          }
        } else if (cur === 3) {
          code = "ERR_SEAL_TAMPERED";
          title = "Rupture de Scellé Constatée à l'Admission";
          desc = "Contrôle accélérométrique ou rupture mécanique du fil de scellé Ed25519 détectée. Refus d'admission en salon funéraire sans enquête préalable.";
          if (sealBadge) {
            sealBadge.textContent = "🚨 RUPTURE DE SCELLÉ";
            sealBadge.className = "px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-rose-950 text-rose-300 border border-rose-500/60 animate-pulse";
          }
        } else if (cur === 4) {
          code = "ERR_PENTOBARBITAL_POSITIVE";
          title = "Dépistage LFA Pentobarbital Positif (Ligne C Seule)";
          desc = "Présence avérée de barbituriques létaux dans l'échantillon. Filière sarcomusation mémorielle INTERDITE : Rejet et incinération Catégorie 1 obligatoire.";
        } else if (cur === 5) {
          code = "ERR_THERMAL_DROP";
          title = "Chute de Température sous le Seuil Réglementaire";
          desc = "Baisse de température à 62°C (< 70°C) ou chute de pression autoclave (< 3 bars). Le cycle thermique est invalidé et doit être réinitialisé.";
        } else if (cur === 6) {
          code = "ERR_IRON_GATE_G7_PRION";
          title = "Violation Règle d'Or Anti-Prion (Porte G7)";
          desc = "Tentative de recyclage au sein de la même espèce détectée par l'oracle The Iron Gate. Signature Ed25519 bloquée de manière permanente.";
        }
      }

      state.anomaly = code;
      if (node) node.classList.add("anomaly");
      if (banner) {
        banner.innerHTML = `<strong>⚠️ ${code} : ${title}</strong><p class="text-[11px] text-red-300 mt-0.5">${desc}</p><button onclick="goToTraceStep(${cur})" class="mt-2 px-2.5 py-1 rounded bg-slate-900 text-slate-200 border border-slate-700 text-[10px] font-mono hover:text-white">✔ Restaurer la Conformité</button>`;
        banner.classList.remove("hidden");
      }
      addTraceCryptoLog(`[ALERTE] ${code} : ${title}`);
    }

    function renderTraceStep() {
      if (typeof traceabilityEvents === "undefined" || !traceabilityEvents || traceabilityEvents.length === 0) return;
      const stepIdx = appState.traceability.currentStep - 1;
      const evt = traceabilityEvents[stepIdx] || traceabilityEvents[0];
      const profKey = appState.traceability.selectedProfile || "p1";
      const prof = TRACE_PROFILES_DATA[profKey];
      const evtProfData = prof && prof.events && prof.events[appState.traceability.currentStep];

      // Mise à jour de la frise chronologique (stepper)
      const pct = (appState.traceability.currentStep / 6) * 100;
      const fillBar = document.getElementById("trace-progress-fill");
      if (fillBar) fillBar.style.width = `${pct}%`;

      for (let s = 1; s <= 6; s++) {
        const node = document.getElementById(`trace-node-${s}`);
        if (!node) continue;
        node.classList.remove("active", "completed", "anomaly");
        if (s < appState.traceability.currentStep) {
          node.classList.add("completed");
        } else if (s === appState.traceability.currentStep) {
          node.classList.add("active");
        }
      }

      // Mise à jour des en-têtes
      const stageBadge = document.getElementById("trace-event-stage-badge");
      if (stageBadge) stageBadge.textContent = (evtProfData && evtProfData.stage_label) ? evtProfData.stage_label : evt.stage_label;

      const titleEl = document.getElementById("trace-event-title");
      if (titleEl) titleEl.textContent = (evtProfData && evtProfData.title) ? evtProfData.title : evt.name;

      const actorBadge = document.getElementById("trace-actor-badge");
      if (actorBadge) actorBadge.textContent = (evtProfData && evtProfData.actor_role) ? evtProfData.actor_role : evt.actor_role;

      const actorCred = document.getElementById("trace-actor-cred");
      if (actorCred) actorCred.textContent = (evtProfData && evtProfData.actor_badge) ? evtProfData.actor_badge : evt.actor_badge;

      // Lieu et Base Légale
      const locEl = document.getElementById("trace-event-location");
      const legalEl = document.getElementById("trace-event-legal");
      const locBoxVal = document.getElementById("trace-location-box-val");

      let locText = "";
      if (evtProfData && evtProfData.location_details) {
        locText = evtProfData.location_details;
      } else if (prof && prof.locations && prof.locations[appState.traceability.currentStep]) {
        locText = prof.locations[appState.traceability.currentStep];
      } else if (evt.location_details) {
        locText = evt.location_details;
      } else {
        locText = evt.gps_coords;
      }
      if (locEl) locEl.textContent = locText;

      let locShortText = "";
      if (evtProfData && evtProfData.location_name) {
        locShortText = evtProfData.location_name;
      } else if (prof && prof.location_names && prof.location_names[appState.traceability.currentStep]) {
        locShortText = prof.location_names[appState.traceability.currentStep];
      } else if (evt.location_name) {
        locShortText = evt.location_name;
      } else {
        locShortText = locText.split("(")[0].trim();
      }
      if (locBoxVal) {
        locBoxVal.textContent = locShortText;
        locBoxVal.title = locText;
      }

      let legalText = "";
      if (evtProfData && evtProfData.legal) {
        legalText = evtProfData.legal;
      } else if (prof && prof.legal) {
        legalText = prof.legal;
      } else if (evt.legal_basis) {
        legalText = evt.legal_basis;
      }
      if (legalEl) legalEl.textContent = legalText;

      // Dépouille et filière
      const depName = document.getElementById("trace-depouille-name");
      if (depName) depName.textContent = prof ? prof.deceased : evt.identity_name;

      const depId = document.getElementById("trace-depouille-id");
      if (depId) depId.textContent = prof ? prof.depouilleId : evt.depouille_id;

      const chanBadge = document.getElementById("trace-channel-badge");
      if (chanBadge && prof) {
        chanBadge.textContent = prof.badge;
        chanBadge.className = `px-2 py-0.5 rounded text-[11px] font-bold ${prof.badgeClass}`;
      }

      // Résumé
      const summaryEl = document.getElementById("trace-event-summary");
      if (summaryEl) summaryEl.textContent = (evtProfData && evtProfData.summary) ? evtProfData.summary : evt.summary;

      // Bouton d'action
      const actBtn = document.getElementById("btn-trace-action");
      if (actBtn) {
        if (appState.traceability.currentStep === 6) {
          if (evtProfData && evtProfData.action_label) {
            actBtn.innerHTML = evtProfData.action_label;
          } else {
            actBtn.innerHTML = "⚡ Émettre le Certificat de Lot Signé Ed25519 &amp; Clôturer";
          }
          actBtn.className = "wf-btn wf-btn-gold text-xs font-bold flex-1 py-2.5";
        } else {
          if (evtProfData && evtProfData.action_label) {
            actBtn.innerHTML = `${evtProfData.action_label} (Étape ${appState.traceability.currentStep + 1})`;
          } else {
            actBtn.innerHTML = `⚡ ${evt.action_label} (Étape ${appState.traceability.currentStep + 1})`;
          }
          actBtn.className = "wf-btn wf-btn-gold text-xs font-bold flex-1 py-2.5";
        }
        actBtn.onclick = nextTraceStep;
      }

      // Formulaire dynamique
      const formContainer = document.getElementById("trace-form-fields-container");
      if (formContainer) {
        let fieldsToRender = (evtProfData && evtProfData.form_fields) ? evtProfData.form_fields : evt.form_fields;
        if (fieldsToRender) {
          let fieldsHtml = "";
          fieldsToRender.forEach(f => {
            let val = f.value;
            if (!evtProfData) {
              if (f.name === "depouille_id" && prof) val = prof.depouilleId;
              if (f.name === "identity_name" && prof) val = prof.deceased;
              if (f.name === "species_taxid" && prof) val = prof.species;
              if (f.name === "vehicle_id" && prof) val = prof.carrier;
              if (f.name === "target_channel" && prof) val = prof.name;
              if (f.name === "thermal_protocol" && prof) val = prof.thermalTarget;
              if (f.name === "core_temp" && prof) val = prof.thermalCore;
              if (f.name === "relics_destination" && prof) val = prof.dest;
            }

            fieldsHtml += `
              <div class="wf-field-group">
                <div class="flex items-center justify-between mb-1">
                  <label class="wf-label">${f.label}</label>
                  <span class="text-[10px] font-mono text-gold-400 bg-gold-500/10 px-1.5 py-0.5 rounded border border-gold-500/20">${f.badge}</span>
                </div>
                <input type="text" class="wf-input font-mono text-xs" value="${val}" readonly style="background: rgba(15, 23, 42, 0.9); color: #f8fafc; border-color: rgba(51, 65, 85, 0.8);">
              </div>
            `;
          });
          formContainer.innerHTML = fieldsHtml;
        }
      }

      // Box Scellé
      const sealIdVal = document.getElementById("trace-seal-id-val");
      if (sealIdVal) sealIdVal.textContent = (evtProfData && evtProfData.seal_id) ? evtProfData.seal_id : evt.seal_id;

      const sealBadge = document.getElementById("trace-seal-status-badge");
      if (sealBadge) {
        sealBadge.textContent = "INTÈGRE • NON ROMPU";
        sealBadge.className = "px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-950 text-emerald-300 border border-emerald-500/40";
      }

      // Box Thermique
      const tempReadout = document.getElementById("trace-temp-readout");
      const tempBadge = document.getElementById("trace-temp-badge");
      const tempTarget = document.getElementById("trace-temp-target");
      const tempFill = document.getElementById("trace-temp-fill");
      const tempIcon = document.getElementById("trace-temp-icon");

      if (tempReadout && tempBadge && tempTarget && tempFill) {
        if (evtProfData && evtProfData.temp_readout) {
          tempIcon.textContent = evtProfData.temp_icon || "🌡️";
          tempReadout.textContent = evtProfData.temp_readout;
          tempBadge.textContent = evtProfData.temp_badge;
          tempTarget.textContent = evtProfData.temp_target;
          tempFill.style.width = evtProfData.temp_fill;
          tempFill.className = evtProfData.temp_fill_class;
        } else if (evt.step === 1) {
          tempIcon.textContent = "🌡️";
          tempReadout.textContent = "12.4°C";
          tempBadge.textContent = "AMBIANTE INITIALE";
          tempBadge.className = "px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-900 text-slate-300 border border-slate-700";
          tempTarget.textContent = "Avant prise en charge réfrigérée";
          tempFill.style.width = "24%";
          tempFill.className = "trace-gauge-fill bg-slate-500";
        } else if (evt.step === 2) {
          tempIcon.textContent = "❄️";
          tempReadout.textContent = "+3.2°C";
          tempBadge.textContent = "CONFORME (2-4°C)";
          tempBadge.className = "px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-sky-950 text-sky-300 border border-sky-500/40";
          tempTarget.textContent = "Consigne : +2.0°C à +4.0°C";
          tempFill.style.width = "32%";
          tempFill.className = "trace-gauge-fill bg-sky-400";
        } else if (evt.step === 3) {
          tempIcon.textContent = "❄️";
          tempReadout.textContent = "+2.8°C";
          tempBadge.textContent = "CELLULE #B4 (CONFORME)";
          tempBadge.className = "px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-sky-950 text-sky-300 border border-sky-500/40";
          tempTarget.textContent = "Régulation : +2.5°C à +3.5°C";
          tempFill.style.width = "28%";
          tempFill.className = "trace-gauge-fill bg-sky-400";
        } else if (evt.step === 4) {
          tempIcon.textContent = "🩺";
          tempReadout.textContent = "+14.0°C";
          tempBadge.textContent = "SALLE STÉRILE SOINS";
          tempBadge.className = "px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-indigo-950 text-indigo-300 border border-indigo-500/40";
          tempTarget.textContent = "Température stérile contrôlée";
          tempFill.style.width = "35%";
          tempFill.className = "trace-gauge-fill bg-indigo-400";
        } else if (evt.step === 5) {
          tempIcon.textContent = "🔥";
          if (profKey === "p1") {
            tempReadout.textContent = "70.4°C";
            tempBadge.textContent = "PASTEURISATION 1H (DEC-AET-05)";
            tempTarget.textContent = "Consigne continue : 70.0°C";
            tempFill.style.width = "70%";
          } else {
            tempReadout.textContent = "133.8°C (3.1 bars)";
            tempBadge.textContent = "MÉTHODE 1 EUROPÉENNE";
            tempTarget.textContent = "Consigne : 133°C / 3 bars / 20 min";
            tempFill.style.width = "100%";
          }
          tempBadge.className = "px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-950 text-amber-300 border border-amber-500/40";
          tempFill.className = "trace-gauge-fill bg-amber-500";
        } else if (evt.step === 6) {
          tempIcon.textContent = "🕊️";
          tempReadout.textContent = "20.5°C";
          tempBadge.textContent = "SALON D'HOMMAGE";
          tempBadge.className = "px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-950 text-emerald-300 border border-emerald-500/40";
          tempTarget.textContent = "Ambiance de recueillement";
          tempFill.style.width = "40%";
          tempFill.className = "trace-gauge-fill bg-emerald-400";
        }
      }

      // Box Télémétrie GPS
      const gpsVal = document.getElementById("trace-gps-val");
      if (gpsVal) gpsVal.textContent = (evtProfData && evtProfData.gps_coords) ? evtProfData.gps_coords : evt.gps_coords;

      const timeVal = document.getElementById("trace-time-val");
      if (timeVal) timeVal.textContent = (evtProfData && evtProfData.timestamp_iso) ? evtProfData.timestamp_iso : evt.timestamp_iso;

      const carrierVal = document.getElementById("trace-carrier-val");
      if (carrierVal && prof) carrierVal.textContent = prof.carrier;

      addTraceCryptoLog(`[ÉTAPE ${evt.step}/6] ${evt.name} — Scellé: ${(evtProfData && evtProfData.seal_id) ? evtProfData.seal_id : evt.seal_status_code}`);
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
