/**
 * AeterniTrak V1.0 — Runtime Client Modulaire (100% Hors-Ligne)
 * Gère le Grand Théâtre Vivant (Exp A-E), la navigation par onglets,
 * les modes de vues (cards/board/table), et l'Orchestrateur Global de Tests Unitaires.
 */

const THEATER_HTML = "\n  <!-- =========================================================================\n       LE GRAND TH\u00c9\u00c2TRE INTERACTIF & STUDIO VIVANT AETERNITRAK\n       ========================================================================= -->\n  <section id=\"interactive-theater\" class=\"glass-card p-6 md:p-8 space-y-6 relative overflow-hidden border-gold-500/40 shadow-2xl\">\n    <!-- En-t\u00eate du Th\u00e9\u00e2tre avec S\u00e9lecteur Mode Famille / Mode Ing\u00e9nieur -->\n    <div class=\"flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-5\">\n      <div>\n        <div class=\"flex items-center gap-2.5\">\n          <span class=\"text-3xl select-none\">\ud83c\udfad</span>\n          <h2 class=\"text-xl sm:text-2xl font-bold font-title text-white\">Le Grand Th\u00e9\u00e2tre Vivant AeterniTrak</h2>\n          <span class=\"px-3 py-1 rounded-full font-mono text-xs font-bold text-gold-300 bg-gold-500/15 border border-gold-500/30\">Studio Temps R\u00e9el 2026</span>\n        </div>\n        <p class=\"text-xs sm:text-sm text-slate-300 mt-1\" id=\"portal-mode-desc\">\n          Basculez entre le Mode Famille (solennel, sensible et sans jargon) et le Mode Ing\u00e9nieur (sp\u00e9cifications in-silico, APDU, cryptographie, Iron Gate).\n        </p>\n      </div>\n\n      <!-- Capsule Bimodale : Mode Famille vs Mode Ing\u00e9nieur -->\n      <div class=\"flex items-center gap-3\">\n        <div class=\"bimodal-toggle-box\">\n          <button id=\"btn-mode-family\" class=\"bimodal-btn active-family\" onclick=\"setReadingMode('family')\">\n            <span>\ud83d\udd4a\ufe0f</span> Mode Famille\n          </button>\n          <button id=\"btn-mode-engineer\" class=\"bimodal-btn\" onclick=\"setReadingMode('engineer')\">\n            <span>\u2699\ufe0f</span> Mode Ing\u00e9nieur\n          </button>\n        </div>\n      </div>\n    </div>\n\n    <!-- Navigation des 5 Exp\u00e9riences Cl\u00e9s -->\n    <div class=\"flex flex-wrap gap-2.5 border-b border-slate-800 pb-4\">\n      <button id=\"hero-tab-expA\" class=\"hero-nav-btn active\" onclick=\"switchHeroExp('expA')\">\n        <span>\ud83d\udcf1</span> Exp A : Sanctuaire Mobile & Flamme\n      </button>\n      <button id=\"hero-tab-expB\" class=\"hero-nav-btn\" onclick=\"switchHeroExp('expB')\">\n        <span>\ud83c\udfb4</span> Exp B : Carte 3D PaxFun\u00e8bre\n      </button>\n      <button id=\"hero-tab-expC\" class=\"hero-nav-btn\" onclick=\"switchHeroExp('expC')\">\n        <span>\ud83d\udda8\ufe0f</span> Exp C : PaxStation & ACR1552U\n      </button>\n      <button id=\"hero-tab-expD\" class=\"hero-nav-btn\" onclick=\"switchHeroExp('expD')\">\n        <span>\ud83e\udeb0</span> Exp D : Cassette LFA & The Iron Gate\n      </button>\n      <button id=\"hero-tab-expE\" class=\"hero-nav-btn\" onclick=\"switchHeroExp('expE')\">\n        <span>\u26d3\ufe0f</span> Exp E : Tra\u00e7abilit\u00e9 D\u00e9pouille (6 \u00c9v\u00e9nements)\n      </button>\n    </div>\n\n    <!-- PANELS DES 4 EXP\u00c9RIENCES -->\n    <div class=\"hero-panels-container\">\n\n      <!-- EXP\u00c9RIENCE A : SANCTUAIRE MOBILE & FLAMME M\u00c9MORIELLE -->\n      <div id=\"hero-panel-expA\" class=\"hero-panel active\">\n        <div class=\"grid grid-cols-1 lg:grid-cols-12 gap-8 items-center\">\n          \n          <!-- Mockup Smartphone Titanium (5/12) -->\n          <div class=\"lg:col-span-5 flex justify-center\">\n            <div class=\"phone-mockup\">\n              <div class=\"phone-screen\">\n                <!-- Dynamic Island -->\n                <div class=\"phone-dynamic-island\">\n                  <span class=\"text-emerald-400 font-bold\">09:41</span>\n                  <span class=\"text-[10px] text-gold-300\">\u25cf Sanctuaire</span>\n                  <div class=\"flex items-center gap-1 text-[10px] text-slate-300\">\n                    <span>5G</span>\n                    <div class=\"w-3.5 h-2 border border-slate-300 rounded-sm p-[1px]\"><div class=\"w-full h-full bg-emerald-400\"></div></div>\n                  </div>\n                </div>\n\n                <!-- \u00c9cran de Recueillement -->\n                <div class=\"p-4 flex flex-col items-center justify-between flex-1 text-center space-y-3\">\n                  <div class=\"space-y-1\">\n                    <span class=\"text-xs font-mono uppercase tracking-widest text-gold-400 font-bold\">Tap NFC Z\u00e9ro Login</span>\n                    <h4 class=\"text-base font-bold font-title text-white\">Sanctuaire M\u00e9moriel</h4>\n                    <p class=\"text-xs text-slate-300\">Adrien de Valcourt (1942 \u2014 2026)</p>\n                  </div>\n\n                  <!-- Flamme M\u00e9morielle SVG Anim\u00e9e -->\n                  <div class=\"relative w-20 h-24 flex items-center justify-center my-1\">\n                    <div class=\"absolute w-16 h-16 rounded-full bg-amber-500/25 blur-xl animate-pulse-slow\"></div>\n                    <svg viewBox=\"0 0 100 140\" class=\"w-16 h-20 flame-animated\">\n                      <defs>\n                        <radialGradient id=\"flameGrad\" cx=\"50%\" cy=\"80%\" r=\"60%\">\n                          <stop offset=\"0%\" stop-color=\"#ffffff\" />\n                          <stop offset=\"25%\" stop-color=\"#fef08a\" />\n                          <stop offset=\"55%\" stop-color=\"#f59e0b\" />\n                          <stop offset=\"85%\" stop-color=\"#dc2626\" />\n                          <stop offset=\"100%\" stop-color=\"transparent\" />\n                        </radialGradient>\n                        <radialGradient id=\"innerCore\" cx=\"50%\" cy=\"85%\" r=\"40%\">\n                          <stop offset=\"0%\" stop-color=\"#ffffff\" />\n                          <stop offset=\"60%\" stop-color=\"#fef08a\" />\n                          <stop offset=\"100%\" stop-color=\"#f59e0b\" />\n                        </radialGradient>\n                      </defs>\n                      <path d=\"M50,10 C58,40 85,70 85,95 C85,115 70,135 50,135 C30,135 15,115 15,95 C15,70 42,40 50,10 Z\" fill=\"url(#flameGrad)\" />\n                      <path d=\"M50,45 C54,65 70,85 70,105 C70,120 60,130 50,130 C40,130 30,120 30,105 C30,85 46,65 50,45 Z\" fill=\"url(#innerCore)\" opacity=\"0.9\" />\n                    </svg>\n                    <div class=\"absolute -bottom-1 w-2.5 h-3 bg-slate-600 rounded-t-sm\"></div>\n                  </div>\n\n                  <!-- Lecteur Vocal & Oscilloscope Waveform -->\n                  <div class=\"w-full bg-obsidian-900 border border-gold-500/30 rounded-xl p-3 space-y-2\">\n                    <div class=\"flex items-center justify-between text-xs font-mono text-slate-400\">\n                      <span>Message Vocal du D\u00e9funt</span>\n                      <span class=\"text-gold-300 font-bold\">01:42</span>\n                    </div>\n                    <div class=\"h-8 flex items-center justify-between gap-1 px-1\">\n                      <div class=\"osc-bar\"></div><div class=\"osc-bar\"></div>\n                      <div class=\"osc-bar\"></div><div class=\"osc-bar\"></div>\n                      <div class=\"osc-bar\"></div><div class=\"osc-bar\"></div>\n                      <div class=\"osc-bar\"></div><div class=\"osc-bar\"></div>\n                      <div class=\"osc-bar\"></div><div class=\"osc-bar\"></div>\n                      <div class=\"osc-bar\"></div><div class=\"osc-bar\"></div>\n                      <div class=\"osc-bar\"></div><div class=\"osc-bar\"></div>\n                    </div>\n                  </div>\n\n                  <button id=\"memorial-play-btn\" onclick=\"toggleMemorialAudio()\" class=\"wf-btn wf-btn-gold text-xs font-bold w-full py-2\">\n                    \u25b6 \u00c9couter le Message\n                  </button>\n                </div>\n              </div>\n            </div>\n          </div>\n\n          <!-- Description M\u00e9tier & Tiroir de Directives (7/12) -->\n          <div class=\"lg:col-span-7 space-y-5\">\n            <div class=\"space-y-2\">\n              <div class=\"flex items-center gap-2\">\n                <span class=\"text-xs uppercase font-mono tracking-widest text-gold-400 font-bold\">Exp\u00e9rience Grand Public</span>\n                <span id=\"ducking-indicator\" class=\"font-mono text-xs text-slate-400 bg-slate-900 px-2.5 py-0.5 rounded-full border border-slate-700\">\n                  \ud83d\udd07 Veille\n                </span>\n              </div>\n              <h3 class=\"text-2xl font-bold font-title text-white\">Le Sanctuaire M\u00e9moriel Mobile & Vocal</h3>\n              <p class=\"text-sm text-slate-300 leading-relaxed\">\n                Con\u00e7u pour offrir \u00e0 la famille et aux proches un recueillement solennel, intime et universel. Aucun compte utilisateur requis, aucun identifiant sur le cloud : le simple effleurement NFC d\u00e9clenche la lecture s\u00e9curis\u00e9e in-silico de la carte physique.\n              </p>\n            </div>\n\n            <!-- Tiroir des Directives & Volont\u00e9s Civiles -->\n            <div class=\"bg-obsidian-950/90 border border-slate-800 rounded-xl p-4 space-y-3\">\n              <button onclick=\"toggleMemorialDrawer()\" class=\"flex items-center justify-between w-full text-left font-bold text-sm text-gold-300 hover:text-gold-200\">\n                <span>\ud83d\udcdc Directives & Volont\u00e9s Enregistr\u00e9es par Adrien</span>\n                <span id=\"memorial-drawer-icon\" class=\"text-xs\">\u25bc</span>\n              </button>\n              <div id=\"memorial-drawer-content\" class=\"hidden space-y-2 pt-2 border-t border-slate-800/80 text-xs text-slate-300\">\n                <div class=\"flex items-center justify-between p-2 rounded bg-slate-900 border border-slate-800\">\n                  <span>Mode de S\u00e9pulture : <strong>Inhumation Naturelle (Biolande)</strong></span>\n                  <span class=\"text-emerald-400 font-mono\">Conforme (r\u00e9f\u00e9rence \u00e0 confirmer par un juriste)</span>\n                </div>\n                <div class=\"flex items-center justify-between p-2 rounded bg-slate-900 border border-slate-800\">\n                  <span>Don d'Organes : <strong>Favorable (Sensibilisation familiale)</strong></span>\n                  <span class=\"text-emerald-400 font-mono\">Loi 13 Juin 1986 (r\u00e9f\u00e9rence \u00e0 confirmer par un juriste)</span>\n                </div>\n                <div class=\"p-2.5 rounded bg-red-950/30 border border-red-500/50 text-red-200 flex items-center gap-2\">\n                  <span class=\"text-lg\">\u26a0\ufe0f</span>\n                  <span><strong>Alerte Vitale :</strong> Porteur d'un stimulateur cardiaque (Pacemaker). Explantation obligatoire avant toute cr\u00e9mation.</span>\n                </div>\n              </div>\n            </div>\n\n            <div class=\"flex flex-wrap gap-2 text-xs font-mono text-slate-400\">\n              <span class=\"bg-slate-900 px-3 py-1 rounded border border-slate-800\">\ud83c\udf10 100% Hors-Ligne</span>\n              <span class=\"bg-slate-900 px-3 py-1 rounded border border-slate-800\">\ud83d\udd10 Signature Ed25519</span>\n              <span class=\"bg-slate-900 px-3 py-1 rounded border border-slate-800\">\ud83c\udfa7 Ducking Vocal Automatique</span>\n            </div>\n          </div>\n\n        </div>\n      </div>\n\n      <!-- EXP\u00c9RIENCE B : CARTE 3D PAXFUN\u00c8BRE R\u00c9VERSIBLE -->\n      <div id=\"hero-panel-expB\" class=\"hero-panel\">\n        <div class=\"grid grid-cols-1 lg:grid-cols-12 gap-8 items-center\">\n          \n          <!-- Carte 3D Perspective (6/12) -->\n          <div class=\"lg:col-span-6 flex flex-col items-center space-y-4\">\n            <div class=\"card-3d-scene\" onclick=\"toggleCard3DFlip()\">\n              <div class=\"card-3d-inner\" id=\"card-3d-element\">\n\n                <!-- Face Recto : Sanctuaire & Portrait -->\n                <div class=\"card-3d-face card-3d-front card-face-front\">\n                  <div class=\"flex items-start justify-between\">\n                    <div class=\"flex items-center gap-2\">\n                      <span class=\"text-2xl\">\ud83d\udd4a\ufe0f</span>\n                      <div>\n                        <div class=\"text-xs uppercase font-mono tracking-widest text-gold-300 font-bold\">Le Pax Fun\u00e8bre</div>\n                        <div class=\"text-xs text-slate-400 font-serif\">Carte Sanctuaire M\u00e9morielle</div>\n                      </div>\n                    </div>\n                    <div class=\"chip-gold\" title=\"Puce Silicium ACOSJ 92K EEPROM\">\n                      <div></div><div></div><div></div>\n                      <div></div><div></div><div></div>\n                    </div>\n                  </div>\n\n                  <div class=\"flex items-center gap-4 my-2\">\n                    <div class=\"w-16 h-16 rounded-xl border-2 border-gold-400/80 bg-slate-900 overflow-hidden flex items-center justify-center shadow-lg relative\">\n                      <span class=\"text-3xl select-none\">\ud83d\udc64</span>\n                      <div class=\"absolute inset-0 bg-gradient-to-t from-black/60 to-transparent\"></div>\n                    </div>\n                    <div>\n                      <div class=\"text-lg font-bold font-title text-white tracking-wide\">Adrien de Valcourt</div>\n                      <div class=\"text-xs text-gold-400 font-mono\">1942 \u2014 2026 \u2022 Li\u00e8ge, Belgique</div>\n                      <div class=\"text-xs text-slate-300 italic mt-0.5\">\u00ab Toujours vivant dans la lumi\u00e8re de nos c\u0153urs \u00bb</div>\n                    </div>\n                  </div>\n\n                  <div class=\"flex items-center justify-between text-xs font-mono border-t border-gold-500/30 pt-2 text-slate-400\">\n                    <span class=\"text-emerald-400 font-bold\">NFC NDEF \u2022 Z\u00e9ro Login</span>\n                    <span class=\"text-gold-300 font-bold\">ID: PAX-2026-0842-MEM</span>\n                  </div>\n                </div>\n\n                <!-- Face Verso : Directives Civiles & Puce ACOSJ -->\n                <div class=\"card-3d-face card-3d-back card-face-back\">\n                  <div class=\"flex items-start justify-between\">\n                    <div class=\"flex items-center gap-2\">\n                      <span class=\"text-2xl\">\u2696\ufe0f</span>\n                      <div>\n                        <div class=\"text-xs uppercase font-mono tracking-widest text-emerald-400 font-bold\">Volont\u00e9s Civiles & M\u00e9dicales</div>\n                        <div class=\"text-xs text-slate-400\">Volont\u00e9s fun\u00e9raires (r\u00e9f\u00e9rence \u00e0 confirmer par un juriste)</div>\n                      </div>\n                    </div>\n                    <span class=\"text-xs font-mono text-emerald-400 bg-emerald-950/80 px-2 py-0.5 rounded border border-emerald-500/40\">Scell\u00e9 Ed25519</span>\n                  </div>\n\n                  <div class=\"bg-red-950/50 border border-red-500/70 rounded-lg p-2.5 my-1 flex items-center gap-2.5\">\n                    <span class=\"text-2xl\">\u26a0\ufe0f</span>\n                    <div>\n                      <div class=\"text-xs font-bold text-red-200 uppercase font-mono tracking-wider\">Alerte M\u00e9dicale Vitale</div>\n                      <div class=\"text-xs text-red-300 font-medium\">Porteur de Pacemaker. Explantation obligatoire avant cr\u00e9mation.</div>\n                    </div>\n                  </div>\n\n                  <div class=\"flex items-center justify-between text-xs text-slate-300\">\n                    <div>\n                      <div class=\"font-bold text-white text-sm\">Inhumation Naturelle</div>\n                      <div class=\"text-slate-400 text-xs\">Don d'organes : Favorable \u2022 C\u00e9r\u00e9monie La\u00efque</div>\n                    </div>\n                    <div class=\"w-12 h-12 bg-white rounded p-1 flex items-center justify-center shadow\">\n                      <svg viewBox=\"0 0 24 24\" class=\"w-full h-full fill-black\">\n                        <path d=\"M2,2H10V10H2V2M4,4V8H8V4H4M14,2H22V10H14V2M16,4V8H20V4H16M2,14H10V22H2V14M4,16V20H8V16H4M14,14H16V16H14V14M18,14H20V16H18V14M20,16H22V18H20V16M14,18H16V20H14V18M18,18H20V20H18V18M16,16H18V18H16V16M20,20H22V22H20V20M14,20H16V22H14V20M16,20H18V22H16V20Z\"/>\n                      </svg>\n                    </div>\n                  </div>\n\n                  <div class=\"flex items-center justify-between text-xs font-mono border-t border-slate-700 pt-2 text-slate-400\">\n                    <span>ACOSJ 92K JavaCard</span>\n                    <span class=\"text-emerald-400 font-bold\">SHA256: 7d4a...b189</span>\n                  </div>\n                </div>\n\n              </div>\n            </div>\n\n            <!-- Boutons de Retournement & Finitions Nobles -->\n            <div class=\"flex flex-wrap items-center gap-3\">\n              <button id=\"card-flip-btn\" onclick=\"toggleCard3DFlip()\" class=\"wf-btn wf-btn-gold text-xs font-bold\">\n                \ud83d\udd04 Retourner la Carte (Verso Directives & Puce)\n              </button>\n              <div class=\"flex items-center gap-1.5\">\n                <button onclick=\"setCard3DFinish('gold')\" class=\"wf-btn wf-btn-sub text-xs\">Or Satin\u00e9</button>\n                <button onclick=\"setCard3DFinish('obsidian')\" class=\"wf-btn wf-btn-sub text-xs\">Obsidienne</button>\n              </div>\n            </div>\n          </div>\n\n          <!-- Description & Cartographie M\u00e9moire (6/12) -->\n          <div class=\"lg:col-span-6 space-y-4\">\n            <h3 class=\"text-2xl font-bold font-title text-white\">La Carte PaxFun\u00e8bre R\u00e9versible CR-80</h3>\n            <p class=\"text-sm text-slate-300 leading-relaxed\">\n              Le support mat\u00e9riel sacr\u00e9 alliant haute horlogerie fun\u00e9raire et silicium cryptographique de grade bancaire. \u00c9quip\u00e9e de la puce <strong>ACOSJ JavaCard 92 Ko EEPROM</strong>, elle conserve le double recto/verso : d'un c\u00f4t\u00e9 la m\u00e9moire affective pour les proches, de l'autre les volont\u00e9s juridiques inviolables pour les soignants et officiers d'\u00e9tat civil.\n            </p>\n\n            <div class=\"bg-obsidian-950 border border-slate-800 rounded-xl p-4 space-y-2 text-xs font-mono\">\n              <div class=\"text-gold-400 font-bold uppercase text-[11px]\">Cartographie Silicium ACOSJ 92K :</div>\n              <div class=\"flex justify-between border-b border-slate-800/60 pb-1.5 text-slate-300\">\n                <span>EF.DIR (0x2F00)</span>\n                <span>Descripteur AID AeterniTrak</span>\n                <span class=\"text-emerald-400\">128 octets</span>\n              </div>\n              <div class=\"flex justify-between border-b border-slate-800/60 pb-1.5 text-slate-300\">\n                <span>EF.PROFILE (0x0001)</span>\n                <span>Capsule M\u00e9morielle CBOR + WebP</span>\n                <span class=\"text-emerald-400\">62.1 Ko</span>\n              </div>\n              <div class=\"flex justify-between border-b border-slate-800/60 pb-1.5 text-slate-300\">\n                <span>EF.SIG (0x0002)</span>\n                <span>Signature COSE_Sign1 Ed25519</span>\n                <span class=\"text-emerald-400\">64 octets</span>\n              </div>\n              <div class=\"flex justify-between text-slate-400 pt-1\">\n                <span>EEPROM Libre</span>\n                <span>R\u00e9serve d'expansion & Logs</span>\n                <span class=\"text-gold-300 font-bold\">29.7 Ko</span>\n              </div>\n            </div>\n          </div>\n\n        </div>\n      </div>\n\n      <!-- EXP\u00c9RIENCE C : PAXSTATION ENCODAGE & LECTEUR ACR1552U -->\n      <div id=\"hero-panel-expC\" class=\"hero-panel\">\n        <div class=\"grid grid-cols-1 lg:grid-cols-12 gap-8 items-center\">\n          \n          <!-- Mockup Lecteur ACR1552U (6/12) -->\n          <div class=\"lg:col-span-6 space-y-4\">\n            <div class=\"reader-mockup\">\n              <!-- Carte en attente de descente -->\n              <div id=\"paxstation-card-dock\" class=\"w-48 h-28 mx-auto rounded-xl border border-gold-500/50 bg-gradient-to-r from-obsidian-900 to-slate-900 p-2 shadow-2xl flex flex-col justify-between\">\n                <div class=\"flex justify-between items-center text-[10px] font-mono text-gold-400\">\n                  <span>ACOSJ 92K</span>\n                  <span>PAX-2026-0842</span>\n                </div>\n                <div class=\"text-center font-title text-xs text-white\">Carte Pr\u00eate pour Gravure</div>\n                <div class=\"text-[9px] font-mono text-slate-500 text-right\">WebUSB Ready</div>\n              </div>\n\n              <!-- Zone Cible Sans Contact -->\n              <div class=\"nfc-target-zone\" onclick=\"startPaxStationEncoding()\">\n                <div class=\"sonar-ring\"></div>\n                <div class=\"sonar-ring\"></div>\n                <div class=\"sonar-ring\"></div>\n                <div class=\"text-center z-10\">\n                  <span class=\"text-2xl select-none\">\ud83d\udedc</span>\n                  <div class=\"text-[10px] font-mono text-sky-300 font-bold mt-1\">Cible Contactless</div>\n                  <div class=\"text-[9px] text-slate-400\">ACR1552U 13.56 MHz</div>\n                </div>\n              </div>\n\n              <!-- Barre d'\u00e9tat & LED -->\n              <div class=\"flex items-center justify-between bg-obsidian-950 px-3 py-2 rounded-lg border border-slate-800 text-xs font-mono\">\n                <div class=\"flex items-center gap-2\">\n                  <span class=\"w-2.5 h-2.5 rounded-full bg-emerald-400\"></span>\n                  <span class=\"text-slate-300\">Alimentation USB-C OK</span>\n                </div>\n                <div class=\"flex items-center gap-2\">\n                  <span id=\"paxstation-acr-led\"></span>\n                  <span class=\"text-slate-400\">Trafic APDU</span>\n                </div>\n              </div>\n\n              <!-- Terminal APDU & Jauge EEPROM -->\n              <div class=\"wf-console-log text-[11px]\" id=\"paxstation-log\">\n                <div class=\"text-slate-400\">Lecteur ACR1552U pr\u00eat sur port WebUSB...</div>\n              </div>\n\n              <div class=\"space-y-1\">\n                <div class=\"flex justify-between text-xs font-mono\">\n                  <span class=\"text-slate-400\">Occupation EEPROM 92 Ko :</span>\n                  <span class=\"text-gold-300 font-bold\" id=\"paxstation-byte-text\">0 / 92 160 octets (0%)</span>\n                </div>\n                <div class=\"h-2 bg-slate-800 rounded-full overflow-hidden border border-slate-700\">\n                  <div id=\"paxstation-byte-fill\" class=\"h-full bg-gradient-to-r from-emerald-500 via-gold-400 to-sky-400 w-0 transition-all duration-300\"></div>\n                </div>\n              </div>\n            </div>\n\n            <button id=\"paxstation-start-btn\" onclick=\"startPaxStationEncoding()\" class=\"wf-btn wf-btn-primary text-xs font-bold w-full py-2.5\">\n              \u26a1 Poser la Carte & Lancer la Gravure Silicium (ACR1552U)\n            </button>\n          </div>\n\n          <!-- Rationale Technique PaxStation (6/12) -->\n          <div class=\"lg:col-span-6 space-y-4\">\n            <h3 class=\"text-2xl font-bold font-title text-white\">PaxStation Encodage & Silicium S\u00e9curis\u00e9</h3>\n            <p class=\"text-sm text-slate-300 leading-relaxed\">\n              La station professionnelle en salon fun\u00e9raire connect\u00e9e au lecteur de r\u00e9f\u00e9rence <strong>ACS ACR1552U</strong> via l'API WebUSB ou le pilote PC/SC natif. Elle ex\u00e9cute la cha\u00eene d'authentification mutuelle ISO/IEC 7816-4, grave le profil s\u00e9rialis\u00e9 CBOR RFC 8949, applique le scellement cryptographique asym\u00e9trique Ed25519 (COSE_Sign1 Tag 18) et proc\u00e8de au claquage in-silico du fusible anti-tamper.\n            </p>\n            <div class=\"grid grid-cols-2 gap-3 text-xs font-mono pt-2\">\n              <div class=\"p-3 rounded-lg bg-obsidian-950 border border-slate-800\">\n                <span class=\"text-gold-400 block font-bold\">IsoDep APDU 14443-4</span>\n                <span class=\"text-slate-400 text-[11px]\">D\u00e9bit max 848 kbps sans contact</span>\n              </div>\n              <div class=\"p-3 rounded-lg bg-obsidian-950 border border-slate-800\">\n                <span class=\"text-sky-300 block font-bold\">Verrou Anti-Tamper</span>\n                <span class=\"text-slate-400 text-[11px]\">Fusible mat\u00e9riel irr\u00e9versible</span>\n              </div>\n            </div>\n          </div>\n\n        </div>\n      </div>\n\n      <!-- EXP\u00c9RIENCE D : CASSETTE LFA TOXICOLOGIQUE & THE IRON GATE -->\n      <div id=\"hero-panel-expD\" class=\"hero-panel\">\n        <div class=\"grid grid-cols-1 lg:grid-cols-12 gap-8 items-center\">\n          \n          <!-- Mockup Cassette LFA (6/12) -->\n          <div class=\"lg:col-span-6 space-y-4\">\n            <div class=\"lfa-cassette space-y-3\">\n              <div class=\"flex justify-between items-center text-xs font-bold text-slate-700 border-b border-slate-300 pb-2\">\n                <span>CASSETTE IMMUNOLOGIQUE LFA-PENTO-V1</span>\n                <span class=\"font-mono text-slate-500\">LOT #HL-2026-B84</span>\n              </div>\n\n              <!-- Puits & Fen\u00eatre de Migration -->\n              <div class=\"flex items-center gap-4\">\n                <!-- Puits d'\u00c9chantillon S -->\n                <div class=\"w-14 h-14 rounded-full border-2 border-slate-400 bg-slate-200 flex flex-col items-center justify-center relative shadow-inner\">\n                  <span class=\"text-[10px] font-mono font-bold text-slate-600\">PUITS S</span>\n                  <div id=\"lfa-droplet\" class=\"w-3 h-3 rounded-full bg-emerald-500 absolute -top-4\"></div>\n                </div>\n\n                <!-- Fen\u00eatre R\u00e9actionnelle Membrane -->\n                <div class=\"lfa-window flex-1 relative overflow-hidden\">\n                  <div id=\"lfa-strip-flow\" class=\"absolute left-0 top-0 bottom-0 pointer-events-none\"></div>\n                  <div class=\"flex flex-col items-center z-10\">\n                    <span class=\"text-[11px] font-mono font-bold text-slate-700\">C</span>\n                    <div id=\"lfa-line-c\" class=\"lfa-line-c mt-1\"></div>\n                  </div>\n                  <div class=\"flex flex-col items-center z-10\">\n                    <span class=\"text-[11px] font-mono font-bold text-slate-700\">T</span>\n                    <div id=\"lfa-line-t\" class=\"lfa-line-t mt-1\"></div>\n                  </div>\n                </div>\n              </div>\n\n              <!-- Banni\u00e8re de R\u00e9sultat -->\n              <div id=\"lfa-result-banner\" class=\"hidden p-3 rounded-lg bg-emerald-950/80 border border-emerald-500 text-emerald-200 text-xs leading-snug\">\n                <strong>\u2714 D\u00c9PISTAGE CONFORME :</strong> Lignes C et T visibles (principe comp\u00e9titif). Absence de mol\u00e9cule de pentobarbital d\u00e9tect\u00e9e dans la d\u00e9pouille. Fili\u00e8re sarcomusation autoris\u00e9e.\n              </div>\n            </div>\n\n            <button id=\"lfa-start-btn\" onclick=\"startLfaTest()\" class=\"wf-btn wf-btn-gold text-xs font-bold w-full py-2.5\">\n              \ud83e\uddea D\u00e9poser l'\u00c9chantillon & Lancer le D\u00e9pistage LFA\n            </button>\n          </div>\n\n          <!-- The Iron Gate Oracle (6/12) -->\n          <div class=\"lg:col-span-6 space-y-4\">\n            <h3 class=\"text-2xl font-bold font-title text-white\">The Iron Gate (G0 \u00e0 G9) & Fili\u00e8re Sarcomusation</h3>\n            <p class=\"text-sm text-slate-300 leading-relaxed\">\n              L'oracle sanitaire d\u00e9terministe r\u00e9gissant la fili\u00e8re des larves d'<em>Hermetia illucens</em>. Emp\u00eache math\u00e9matiquement tout recyclage intrasp\u00e9cifique (r\u00e8gle d'or anti-prion et feed-ban europ\u00e9en strict) et bloque la signature cryptographique du lot en cas de d\u00e9passement toxicologique.\n            </p>\n\n            <div class=\"space-y-1.5 bg-obsidian-950 border border-slate-800 rounded-xl p-4\">\n              <span class=\"text-xs uppercase font-mono text-gold-400 font-bold block mb-2\">Les 10 Portes Sanitaires Infranchissables :</span>\n              <div class=\"grid grid-cols-2 gap-2 text-xs\">\n                <span class=\"iron-gate-flag px-2 py-1 rounded font-mono bg-slate-900 border border-slate-800 text-slate-400\">G0: Destination &amp; Cibles</span>\n                <span class=\"iron-gate-flag px-2 py-1 rounded font-mono bg-slate-900 border border-slate-800 text-slate-400\">G1: Taxonomie &amp; Lignage</span>\n                <span class=\"iron-gate-flag px-2 py-1 rounded font-mono bg-slate-900 border border-slate-800 text-slate-400\">G2: Protection Restes Humains</span>\n                <span class=\"iron-gate-flag px-2 py-1 rounded font-mono bg-slate-900 border border-slate-800 text-slate-400\">G3: Cat\u00e9gories &amp; Substrats</span>\n                <span class=\"iron-gate-flag px-2 py-1 rounded font-mono bg-slate-900 border border-slate-800 text-slate-400\">G4: D\u00e9pistage Pentobarbital</span>\n                <span class=\"iron-gate-flag px-2 py-1 rounded font-mono bg-slate-900 border border-slate-800 text-slate-400\">G5: Feed-Ban Source Ruminant</span>\n                <span class=\"iron-gate-flag px-2 py-1 rounded font-mono bg-slate-900 border border-slate-800 text-slate-400\">G6: Feed-Ban Cible Ruminant</span>\n                <span class=\"iron-gate-flag px-2 py-1 rounded font-mono bg-slate-900 border border-slate-800 text-slate-400\">G7: R\u00e8gle d'Or Anti-Cannibalisme</span>\n                <span class=\"iron-gate-flag px-2 py-1 rounded font-mono bg-slate-900 border border-slate-800 text-slate-400\">G8: Feed-Ban Groupes &amp; Esp\u00e8ces</span>\n                <span class=\"iron-gate-flag px-2 py-1 rounded font-mono bg-slate-900 border border-slate-800 text-slate-400\">G9: Traitement Sanitaire &amp; Preuve</span>\n              </div>\n            </div>\n          </div>\n\n        </div>\n      </div>\n\n      <!-- EXP\u00c9RIENCE E : GRAND SIMULATEUR \u00c9V\u00c9NEMENTIEL DE TRA\u00c7ABILIT\u00c9 DE LA D\u00c9POUILLE (6 \u00c9V\u00c9NEMENTS) -->\n      <div id=\"hero-panel-expE\" class=\"hero-panel\">\n        <div class=\"space-y-6\">\n          \n          <!-- En-t\u00eate du Simulateur \u00c9v\u00e9nementiel & S\u00e9lecteur de Profils -->\n          <div class=\"flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4\">\n            <div>\n              <div class=\"flex items-center gap-2\">\n                <span class=\"text-xs uppercase font-mono tracking-widest text-emerald-400 font-bold\">App 4 \u00b7 Fili\u00e8re Post-Mortem &amp; Bioconversion</span>\n                <span id=\"trace-live-badge\" class=\"font-mono text-xs text-emerald-300 bg-emerald-950/80 px-2.5 py-0.5 rounded-full border border-emerald-500/40\">\n                  \u25cf Cha\u00eene Active Ed25519\n                </span>\n              </div>\n              <h3 class=\"text-xl sm:text-2xl font-bold font-title text-white mt-1\">Simulateur \u00c9v\u00e9nementiel de Tra\u00e7abilit\u00e9 de la D\u00e9pouille</h3>\n              <p class=\"text-xs sm:text-sm text-slate-300\">\n                Suivi inviolable et horodat\u00e9 \u00e0 chaque \u00e9tape : du constat m\u00e9dical initial au transport frigorifique (2-4\u00b0C), \u00e0 la r\u00e9ception, aux contr\u00f4les amonts (ex\u00e9r\u00e8se pacemaker &amp; LFA pentobarbital), \u00e0 la bioconversion Hermetia illucens et \u00e0 la cl\u00f4ture The Iron Gate.\n              </p>\n            </div>\n\n            <!-- Commandes du Simulateur (Auto-Play & Profils) -->\n            <div class=\"flex flex-wrap items-center gap-2\">\n              <div class=\"flex items-center gap-1 bg-obsidian-950 p-1 rounded-xl border border-slate-800 text-xs font-mono\">\n                <button id=\"btn-trace-prof-p1\" onclick=\"setTraceProfile('p1')\" class=\"px-2.5 py-1.5 rounded-lg font-bold bg-gold-500 text-obsidian-950 shadow\">\n                  \ud83d\udc3e Profil 1 (Compagnie)\n                </button>\n                <button id=\"btn-trace-prof-p2\" onclick=\"setTraceProfile('p2')\" class=\"px-2.5 py-1.5 rounded-lg text-slate-300 hover:text-white\">\n                  \ud83d\udc17 Profil 2 (Faune DNF)\n                </button>\n                <button id=\"btn-trace-prof-p3\" onclick=\"setTraceProfile('p3')\" class=\"px-2.5 py-1.5 rounded-lg text-slate-300 hover:text-white\">\n                  \ud83d\udc04 Profil 3 (Ferme)\n                </button>\n                <button id=\"btn-trace-prof-p4\" onclick=\"setTraceProfile('p4')\" class=\"px-2.5 py-1.5 rounded-lg text-slate-300 hover:text-white\">\n                  \ud83c\udfed Profil 4 (Abattoir)\n                </button>\n              </div>\n\n              <button id=\"btn-trace-autoplay\" onclick=\"toggleTraceAutoPlay()\" class=\"wf-btn wf-btn-primary text-xs font-bold py-2 px-3 flex items-center gap-1.5\">\n                <span>\u26a1</span> Auto-Play (6 \u00c9v\u00e9nements)\n              </button>\n              <button onclick=\"resetTraceTimeline()\" class=\"wf-btn wf-btn-sub text-xs py-2 px-2.5\" title=\"R\u00e9initialiser au D\u00e9c\u00e8s\">\n                <span>\u21ba</span>\n              </button>\n            </div>\n          </div>\n\n          <!-- FRISE CHRONOLOGIQUE INTERACTIVE (6 \u00c9V\u00c9NEMENTS) -->\n          <div class=\"trace-stepper-wrap\">\n            <div class=\"trace-progress-track\">\n              <div id=\"trace-progress-fill\" class=\"trace-progress-fill\" style=\"width: 16.66%;\"></div>\n            </div>\n            <div class=\"trace-stepper\" id=\"trace-stepper-container\">\n              <button class=\"trace-step-node active\" id=\"trace-node-1\" onclick=\"goToTraceStep(1)\">\n                <div class=\"trace-node-circle\">\ud83d\udccb</div>\n                <div class=\"trace-node-label\">1. Constat &amp; Scell\u00e9</div>\n              </button>\n              <button class=\"trace-step-node\" id=\"trace-node-2\" onclick=\"goToTraceStep(2)\">\n                <div class=\"trace-node-circle\">\ud83d\ude90</div>\n                <div class=\"trace-node-label\">2. Transport Froid (2-4\u00b0C)</div>\n              </button>\n              <button class=\"trace-step-node\" id=\"trace-node-3\" onclick=\"goToTraceStep(3)\">\n                <div class=\"trace-node-circle\">\u2696\ufe0f</div>\n                <div class=\"trace-node-label\">3. Admission &amp; Cellule</div>\n              </button>\n              <button class=\"trace-step-node\" id=\"trace-node-4\" onclick=\"goToTraceStep(4)\">\n                <div class=\"trace-node-circle\">\ud83e\ude7a</div>\n                <div class=\"trace-node-label\">4. Contr\u00f4les Amonts</div>\n              </button>\n              <button class=\"trace-step-node\" id=\"trace-node-5\" onclick=\"goToTraceStep(5)\">\n                <div class=\"trace-node-circle\">\ud83e\udeb0</div>\n                <div class=\"trace-node-label\">5. Bioconversion &amp; Chauffe</div>\n              </button>\n              <button class=\"trace-step-node\" id=\"trace-node-6\" onclick=\"goToTraceStep(6)\">\n                <div class=\"trace-node-circle\">\ud83d\udd4a\ufe0f</div>\n                <div class=\"trace-node-label\">6. The Iron Gate &amp; Remise</div>\n              </button>\n            </div>\n          </div>\n\n          <!-- PANNEAU CENTRAL DE L'\u00c9V\u00c9NEMENT ACTIF (2 COLONNES) -->\n          <div class=\"grid grid-cols-1 lg:grid-cols-12 gap-6\">\n\n            <!-- Colonne Gauche : Formulaire Acteur & Saisie \u00c9v\u00e9nementielle (7/12) -->\n            <div class=\"lg:col-span-7 space-y-4\">\n              <div class=\"trace-panel-body space-y-4\">\n                \n                <!-- En-t\u00eate \u00c9v\u00e9nement & Acteur Responsable -->\n                <div class=\"flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-3\">\n                  <div>\n                    <span id=\"trace-event-stage-badge\" class=\"text-[11px] font-mono font-bold text-gold-400 uppercase tracking-wider block\">\n                      \u00c9v\u00e9nement 1 / 6 \u2022 D\u00e9claration Initiale\n                    </span>\n                    <h4 id=\"trace-event-title\" class=\"text-lg font-bold font-title text-white\">\n                      Constat de D\u00e9c\u00e8s &amp; Pose du Scell\u00e9 Inviolable\n                    </h4>\n                  </div>\n                  <div class=\"text-right\">\n                    <span id=\"trace-actor-badge\" class=\"px-2.5 py-1 rounded-md text-xs font-mono bg-slate-900 border border-slate-700 text-slate-300\">\n                      \ud83e\ude7a V\u00e9t\u00e9rinaire / M\u00e9decin Agr\u00e9\u00e9\n                    </span>\n                    <div id=\"trace-actor-cred\" class=\"text-[10px] text-slate-400 font-mono mt-0.5\">INAMI / AFSCA #VET-BEL-84912</div>\n                  </div>\n                </div>\n\n                <!-- Carte R\u00e9sum\u00e9 de la D\u00e9pouille -->\n                <div class=\"p-3 rounded-xl bg-obsidian-950 border border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs\">\n                  <div>\n                    <span class=\"text-slate-400 block text-[10px] uppercase font-mono\">D\u00e9pouille Identifi\u00e9e</span>\n                    <strong id=\"trace-depouille-name\" class=\"text-white text-sm\">Adrien de Valcourt (ou Canis familiaris TaxID 9615)</strong>\n                    <span id=\"trace-depouille-id\" class=\"text-gold-400 font-mono text-[11px] block\">DEP-2026-BEL-99201</span>\n                  </div>\n                  <div class=\"text-right font-mono\">\n                    <span class=\"text-slate-400 block text-[10px] uppercase\">R\u00e9gime Sanitaire</span>\n                    <span id=\"trace-channel-badge\" class=\"px-2 py-0.5 rounded bg-emerald-950 border border-emerald-500/40 text-emerald-300 font-bold\">\n                      Profil 1 \u00b7 Cat\u00e9gorie 1 M\u00e9moriel\n                    </span>\n                  </div>\n                </div>\n\n                <!-- Formulaire Interactif de l'\u00c9v\u00e9nement -->\n                <div class=\"space-y-3\" id=\"trace-form-fields-container\">\n                  <!-- Rempli dynamiquement selon l'\u00e9v\u00e9nement -->\n                </div>\n\n                <!-- R\u00e9sum\u00e9 Explicatif M\u00e9tier -->\n                <p id=\"trace-event-summary\" class=\"text-xs text-slate-300 bg-slate-900/60 p-3 rounded-lg border border-slate-800 leading-relaxed\">\n                  Constat officiel de fin de vie, horodatage certifi\u00e9 RFC 3339, g\u00e9olocalisation par balise RTK, v\u00e9rification de l'identit\u00e9 du d\u00e9funt ou de l'animal, et scellement physique et cryptographique imm\u00e9diat par scell\u00e9 inviolable NFC/QR \u00e0 signature Ed25519.\n                </p>\n\n                <!-- Boutons d'Action & D\u00e9clencheur d'Anomalie -->\n                <div class=\"flex flex-wrap items-center gap-3 pt-2\">\n                  <button id=\"btn-trace-action\" onclick=\"nextTraceStep()\" class=\"wf-btn wf-btn-gold text-xs font-bold flex-1 py-2.5\">\n                    \u26a1 Valider &amp; Sceller l'\u00c9v\u00e9nement (Suivant)\n                  </button>\n                  <button id=\"btn-trace-anomaly\" onclick=\"simulateTraceAnomaly()\" class=\"wf-btn wf-btn-sub text-xs text-rose-300 border-rose-500/30 hover:bg-rose-950/40 py-2.5 px-3\" title=\"Tester la r\u00e9action du syst\u00e8me face \u00e0 une violation\">\n                    \u26a0\ufe0f Simuler Anomalie\n                  </button>\n                </div>\n\n                <!-- Banni\u00e8re d'Alerte Anomalie (Masqu\u00e9e par d\u00e9faut) -->\n                <div id=\"trace-anomaly-banner\" class=\"hidden p-3 rounded-lg bg-red-950/80 border border-red-500 text-red-200 text-xs space-y-1\">\n                  <!-- Rempli dynamiquement lors d'une anomalie -->\n                </div>\n\n              </div>\n            </div>\n\n            <!-- Colonne Droite : T\u00e9l\u00e9m\u00e9trie, Scell\u00e9, Cha\u00eene du Froid & Console Cryptographique (5/12) -->\n            <div class=\"lg:col-span-5 space-y-4\">\n\n              <!-- Box 1 : Statut du Scell\u00e9 Inviolable NFC / Ed25519 -->\n              <div class=\"trace-seal-card space-y-2\">\n                <div class=\"flex items-center justify-between text-xs\">\n                  <div class=\"flex items-center gap-2\">\n                    <span class=\"text-xl\">\ud83d\udd12</span>\n                    <span class=\"font-bold text-white uppercase tracking-wider font-mono text-[11px]\">Scell\u00e9 Inviolable Ed25519</span>\n                  </div>\n                  <span id=\"trace-seal-status-badge\" class=\"px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-950 text-emerald-300 border border-emerald-500/40\">\n                    INT\u00c8GRE &bull; NON ROMPU\n                  </span>\n                </div>\n                <div class=\"flex items-center justify-between text-xs font-mono bg-obsidian-950/80 p-2 rounded border border-slate-800\">\n                  <span class=\"text-slate-400\">ID Scell\u00e9 Physique :</span>\n                  <span id=\"trace-seal-id-val\" class=\"text-sky-300 font-bold\">SCELL-2026-BEL-0982-NFC</span>\n                </div>\n                <div class=\"text-[10px] font-mono text-slate-400 flex items-center justify-between\">\n                  <span>Cryptosyst\u00e8me : RFC 8032 Ed25519 (alg: -8)</span>\n                  <span class=\"text-emerald-400\">Tag 18 COSE</span>\n                </div>\n              </div>\n\n              <!-- Box 2 : Thermom\u00e8tre Num\u00e9rique & Cha\u00eene du Froid -->\n              <div class=\"trace-thermometer-box space-y-2\">\n                <div class=\"flex items-center justify-between text-xs\">\n                  <div class=\"flex items-center gap-2\">\n                    <span id=\"trace-temp-icon\" class=\"text-lg\">\u2744\ufe0f</span>\n                    <span class=\"font-bold text-white uppercase tracking-wider font-mono text-[11px]\">Monitoring Thermique Continu</span>\n                  </div>\n                  <span id=\"trace-temp-badge\" class=\"px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-sky-950 text-sky-300 border border-sky-500/40\">\n                    CONFORME (2-4\u00b0C)\n                  </span>\n                </div>\n                <div class=\"flex items-baseline justify-between\">\n                  <div class=\"text-2xl font-bold font-mono text-white\" id=\"trace-temp-readout\">+3.2\u00b0C</div>\n                  <span class=\"text-xs font-mono text-slate-400\" id=\"trace-temp-target\">Consigne : +2.0\u00b0C \u00e0 +4.0\u00b0C</span>\n                </div>\n                <div class=\"trace-gauge-bar\">\n                  <div id=\"trace-temp-fill\" class=\"trace-gauge-fill bg-sky-400\" style=\"width: 32%;\"></div>\n                </div>\n              </div>\n\n              <!-- Box 3 : T\u00e9l\u00e9m\u00e9trie GPS & \u00c9margement -->\n              <div class=\"bg-obsidian-950 border border-slate-800 rounded-xl p-3 space-y-1.5 text-xs font-mono\">\n                <div class=\"text-slate-400 uppercase text-[10px] font-bold\">Balise GPS &amp; Horodatage Certifi\u00e9 :</div>\n                <div class=\"flex items-center justify-between text-slate-300\">\n                  <span>\ud83d\udccd GPS RTK :</span>\n                  <span id=\"trace-gps-val\" class=\"text-gold-300\">50.6333\u00b0 N, 5.5667\u00b0 E</span>\n                </div>\n                <div class=\"flex items-center justify-between text-slate-300\">\n                  <span>\u23f1\ufe0f Horodatage :</span>\n                  <span id=\"trace-time-val\" class=\"text-slate-400\">2026-10-05 08:15 UTC</span>\n                </div>\n                <div class=\"flex items-center justify-between text-slate-300\">\n                  <span>\ud83d\ude90 Logistique :</span>\n                  <span id=\"trace-carrier-val\" class=\"text-slate-300 truncate max-w-[200px]\">V\u00e9hicule 1-AFR-842</span>\n                </div>\n              </div>\n\n              <!-- Box 4 : Console Cryptographique & The Iron Gate Live -->\n              <div class=\"space-y-1\">\n                <div class=\"flex items-center justify-between text-xs font-mono text-slate-400\">\n                  <span>Journal Cryptographique In-Silico</span>\n                  <span class=\"text-emerald-400 text-[10px]\">Ed25519 &bull; SHA-256</span>\n                </div>\n                <div class=\"trace-crypto-terminal\" id=\"trace-crypto-log\">\n                  <div class=\"text-slate-400\">> [INIT] Cha\u00eene de tra\u00e7abilit\u00e9 AeterniTrak V1.0 initialis\u00e9e...</div>\n                  <div class=\"text-emerald-400\">> [SCELL\u00c9] SCELL-2026-BEL-0982-NFC li\u00e9 \u00e0 DEP-2026-BEL-99201</div>\n                  <div class=\"text-sky-300\">> [SIGNATURE] alg: -8 (Ed25519) digest valid\u00e9 in-silico</div>\n                </div>\n              </div>\n\n            </div>\n\n          </div>\n\n        </div>\n      </div>\n\n    </div>\n  </section>\n";

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
          desc.innerHTML = '<strong>Mode Famille & Conseiller :</strong> Présentation sereine, chaleureuse et digne axée sur la mémoire, l\'hommage affectif et la simplicité absolue sans jargon technique.';
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
        if (btn) btn.innerHTML = '⏸ Suspendre l\'Écoute';
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
        legal: "Arrêté royal du 27 avril 2007 & Arbitrage Kudoro DEC-AET-05 (références à confirmer par un juriste)"
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
        legal: "Règlement (CE) n° 1069/2009 & Code forestier wallon (références à confirmer par un juriste)"
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
        legal: "Règlement (CE) n° 1069/2009 & Identification Sanitel AFSCA (références à confirmer par un juriste)"
      },
      p4: {
        id: "p4",
        name: "Profil 4 — Déchets d'Abattoir (Cat 1 MRS Dénaturé)",
        badge: "Profil 4 · Déchets Abattoir MRS C1",
        badgeClass: "bg-purple-950 border border-purple-500/40 text-purple-300",
        species: "Bos taurus (Matériel à Risque Spécifié MRS - Crâne & Moelle)",
        deceased: "Lot Déchets Abattoir Liège #ABT-2026-MRS-44",
        depouilleId: "MRS-2026-ABT-0914",
        carrier: "Conteneur Hermétique Plombé #CONT-MRS-12",
        thermalTarget: "Dénaturation Bleu 0,5% + Méthode 1 (133°C, 3 bars, 20 min)",
        thermalCore: "134.5°C, 3.3 bars absolus pendant 25 minutes",
        dest: "Incinération Dédiée Haute Température Cimenterie (Catégorie 1 MRS)",
        legal: "Règlement (CE) n° 999/2001 annexe V (règles MRS anti-prion) (référence à confirmer par un juriste)"
      }
    };

    function setTraceProfile(profId) {
      if (!TRACE_PROFILES_DATA[profId]) return;
      appState.traceability.selectedProfile = profId;
      ["p1", "p2", "p3", "p4"].forEach(id => {
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
      if (cur < 6) {
        goToTraceStep(cur + 1);
      } else {
        addTraceCryptoLog("[CLÔTURE] Traçabilité complète 6/6 validée. Certificat Ed25519 émis.");
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
      const banner = document.getElementById("trace-anomaly-banner");
      const node = document.getElementById(`trace-node-${cur}`);
      const sealBadge = document.getElementById("trace-seal-status-badge");
      const tempBadge = document.getElementById("trace-temp-badge");

      let code = "ERR_ANOMALY";
      let title = "Anomalie Détectée";
      let desc = "";

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
      if (stageBadge) stageBadge.textContent = evt.stage_label;

      const titleEl = document.getElementById("trace-event-title");
      if (titleEl) titleEl.textContent = evt.name;

      const actorBadge = document.getElementById("trace-actor-badge");
      if (actorBadge) actorBadge.textContent = evt.actor_role;

      const actorCred = document.getElementById("trace-actor-cred");
      if (actorCred) actorCred.textContent = evt.actor_badge;

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
      if (summaryEl) summaryEl.textContent = evt.summary;

      // Bouton d'action
      const actBtn = document.getElementById("btn-trace-action");
      if (actBtn) {
        if (appState.traceability.currentStep === 6) {
          actBtn.innerHTML = "⚡ Émettre le Certificat de Lot Signé Ed25519 &amp; Clôturer";
          actBtn.className = "wf-btn wf-btn-gold text-xs font-bold flex-1 py-2.5";
        } else {
          actBtn.innerHTML = `⚡ ${evt.action_label} (Étape ${appState.traceability.currentStep + 1})`;
          actBtn.className = "wf-btn wf-btn-gold text-xs font-bold flex-1 py-2.5";
        }
        actBtn.onclick = nextTraceStep;
      }

      // Formulaire dynamique
      const formContainer = document.getElementById("trace-form-fields-container");
      if (formContainer && evt.form_fields) {
        let fieldsHtml = "";
        evt.form_fields.forEach(f => {
          let val = f.value;
          if (f.name === "depouille_id" && prof) val = prof.depouilleId;
          if (f.name === "identity_name" && prof) val = prof.deceased;
          if (f.name === "species_taxid" && prof) val = prof.species;
          if (f.name === "vehicle_id" && prof) val = prof.carrier;
          if (f.name === "target_channel" && prof) val = prof.name;
          if (f.name === "thermal_protocol" && prof) val = prof.thermalTarget;
          if (f.name === "core_temp" && prof) val = prof.thermalCore;
          if (f.name === "relics_destination" && prof) val = prof.dest;

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

      // Box Scellé
      const sealIdVal = document.getElementById("trace-seal-id-val");
      if (sealIdVal) sealIdVal.textContent = evt.seal_id;

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
        if (evt.step === 1) {
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
      if (gpsVal) gpsVal.textContent = evt.gps_coords;

      const timeVal = document.getElementById("trace-time-val");
      if (timeVal) timeVal.textContent = evt.timestamp_iso;

      const carrierVal = document.getElementById("trace-carrier-val");
      if (carrierVal && prof) carrierVal.textContent = prof.carrier;

      addTraceCryptoLog(`[ÉTAPE ${evt.step}/6] ${evt.name} — Scellé: ${evt.seal_status_code}`);
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
                <div class="font-mono text-xs text-gold-400 font-bold">${isFamille ? 'Éléments Personnalisés :' : 'Champs d\'Interaction Silicium :'}</div>
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
                <span>${isFamille ? '🛡️ Protection & Résolution d\'Incident' : '⚠️ Cas d\'Erreur Normative'} (${err.code})</span>
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

// Montage dynamique du Grand Théâtre dans le Hub
function renderInteractiveTheater(targetId = 'interactive-theater-container') {
  const el = document.getElementById(targetId);
  if (el) {
    el.innerHTML = THEATER_HTML;
    renderTraceStep();
  }
}

// =========================================================================
// ORCHESTRATEUR GLOBAL DE TESTS UNITAIRES (RUNNER IFRAME DÉCOUPLÉ)
// =========================================================================
const globalTestRunner = {
  total: 48,
  currentIdx: 0,
  passed: 0,
  failed: 0,
  isRunning: false,
  suite: [],

  init(list) {
    this.suite = list;
    this.total = list.length;
    window.addEventListener('message', (e) => {
      if (e.data && e.data.type === 'AETERNI_TEST_RESULT') {
        this.onTestResult(e.data);
      }
    });
  },

  start() {
    if (this.isRunning) return;
    this.isRunning = true;
    this.currentIdx = 0;
    this.passed = 0;
    this.failed = 0;
    this.updateUI();
    this.runNext();
  },

  runNext() {
    if (this.currentIdx >= this.suite.length) {
      this.finish();
      return;
    }
    const uc = this.suite[this.currentIdx];
    const iframe = document.getElementById('test-runner-iframe');
    if (iframe) {
      iframe.src = `${uc.app}/${uc.id}.html?autotest=1`;
    }
  },

  onTestResult(res) {
    if (res.success) this.passed++;
    else this.failed++;

    const badge = document.getElementById(`hub-badge-${res.ucId}`);
    if (badge) {
      badge.className = res.success ? 'test-badge test-badge-pass text-[10px]' : 'test-badge test-badge-fail text-[10px]';
      badge.textContent = res.success ? `PASS (${res.duration} ms)` : 'FAIL';
    }

    this.currentIdx++;
    this.updateUI();
    setTimeout(() => this.runNext(), 35);
  },

  updateUI() {
    const pct = Math.round((this.currentIdx / this.total) * 100);
    const fill = document.getElementById('global-progress-fill');
    const label = document.getElementById('global-test-status');
    const countPassed = document.getElementById('hub-count-passed');
    const countFailed = document.getElementById('hub-count-failed');

    if (fill) fill.style.width = `${pct}%`;
    if (label) label.textContent = `${this.currentIdx} / ${this.total} testés (${pct}%)`;
    if (countPassed) countPassed.textContent = this.passed;
    if (countFailed) countFailed.textContent = this.failed;
  },

  finish() {
    this.isRunning = false;
    const label = document.getElementById('global-test-status');
    if (label) {
      label.innerHTML = `<strong>SUITE TERMINÉE :</strong> ${this.passed} / ${this.total} PASS • 100% Hors-Ligne`;
    }
    const btn = document.getElementById('btn-run-all-tests');
    if (btn) btn.textContent = '▶ Relancer Tous les Tests Unitaires';
  }
};
