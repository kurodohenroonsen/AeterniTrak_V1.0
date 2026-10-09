/**
 * PaxStudio Design — Contrôleur de l'application (état, liaisons, rendu, export, impression).
 * Une seule source de vérité : `state.data` (un dossier au format des 44 cas PAVS).
 */
(function () {
  "use strict";

  const R = window.PaxRules;
  const C = window.PaxCards;
  const STORE_KEY = "paxstudio.mesPavs.v1";
  const $ = sel => document.querySelector(sel);
  const $$ = sel => Array.from(document.querySelectorAll(sel));

  const CATEGORY_LABELS = {
    MES_PAVS: "Mes PAVS",
    PAVS_FLAGSHIP: "Dossier titulaire",
    PAVS_SOINS_THERAPIES: "Projet de soins & thérapies",
    PAVS_SARCOMUSATION: "Sarcomusation (démonstrateur prospectif)",
    PAVS_CREMATION: "Crémation",
    PAVS_INHUMATION: "Inhumation & humusation",
    PAVS_PYROTECHNIQUE: "Sécurité pyrotechnique & sanitaire",
    PAVS_DONS_SCIENCE: "Dons & legs à la science",
    PAVS_REPRESENTANTS: "Représentants & rites",
    PAVS_MULTIMEDIA: "Obsèques & multimédia"
  };

  const LAYOUT_NAMES = { A: "A · Majestueux — médaillon d'or", B: "B · Diptyque — encadrement biseauté", C: "C · Triptyque — trois arcades", D: "D · Mosaïque — archives multiples", E: "E · Typographie pure — stèle épigraphique" };

  const FONT_FILES = {
    cinzel: ["Cinzel", [["cinzel-latin-400-normal", 400, "normal"], ["cinzel-latin-600-normal", 600, "normal"], ["cinzel-latin-700-normal", 700, "normal"]]],
    cormorant: ["Cormorant Garamond", [["cormorant-garamond-latin-400-normal", 400, "normal"], ["cormorant-garamond-latin-400-italic", 400, "italic"], ["cormorant-garamond-latin-600-normal", 600, "normal"], ["cormorant-garamond-latin-600-italic", 600, "italic"]]],
    playfair: ["Playfair Display", [["playfair-display-latin-400-normal", 400, "normal"], ["playfair-display-latin-400-italic", 400, "italic"], ["playfair-display-latin-700-normal", 700, "normal"]]],
    inter: ["Inter", [["inter-latin-400-normal", 400, "normal"], ["inter-latin-500-normal", 500, "normal"], ["inter-latin-600-normal", 600, "normal"]]],
    fira: ["Fira Code", [["fira-code-latin-400-normal", 400, "normal"], ["fira-code-latin-500-normal", 500, "normal"]]]
  };

  const state = {
    cases: (window.PAX_TEST_CASES || []).map(c => Object.assign({}, c, { category: c.category })),
    saved: loadSaved(),
    data: null,
    tab: "card1",
    view: "side",
    crop: false,
    safe: false,
    zoom: 1,
    flipped: false,
    design: {
      material: "ivoire", fontTitle: "cinzel", fontBody: "cormorant", fontScale: 1, gold: C.MATERIALS.ivoire.accent,
      guillocheOpacity: 0.35, guillocheDensity: 5, emblem: "dove", layout: "A", pulse: true,
      portrait: null, portraitBytes: 0, exemplaire: 1, epitaph: "", years: "", quote: "", voiceExtract: "", fingerprint: ""
    }
  };

  // ------------------------------------------------------------ stockage local (confort par appareil)
  function loadSaved() {
    try { return JSON.parse(localStorage.getItem(STORE_KEY) || "[]"); } catch (e) { return []; }
  }
  function persistSaved() {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(state.saved)); return true; } catch (e) { return false; }
  }

  // ------------------------------------------------------------ chemins
  function getPath(obj, path) {
    return path.split(".").reduce((o, k) => (o == null ? undefined : o[k]), obj);
  }
  function setPath(obj, path, value) {
    const keys = path.split(".");
    let o = obj;
    keys.slice(0, -1).forEach(k => {
      if (o[k] == null || typeof o[k] !== "object") o[k] = {};
      o = o[k];
    });
    o[keys[keys.length - 1]] = value;
  }
  const clone = o => JSON.parse(JSON.stringify(o));

  function convert(raw, type) {
    if (type === "number") return raw === "" ? 0 : Number(raw);
    if (type === "bool") return raw === true || raw === "true";
    if (type === "tristate") return raw === "null" ? null : raw === "true";
    return raw;
  }

  // ------------------------------------------------------------ cohérence du dossier
  /** Recopie les champs miroir (post_mortem_wills, libellés) et recalcule le statut B.A.T. */
  function syncMirrors(c) {
    const mode = R.burialMode(c.funeral_wills.burial_mode);
    c.funeral_wills.burial_mode_label = mode.label;
    const pm = c.pavs_record.post_mortem_wills = c.pavs_record.post_mortem_wills || {};
    pm.organ_donation = Number(c.medical_record.organ_donation_status) === 1;
    pm.body_donation_science = !!c.medical_record.body_donation_science;
    pm.burial_desire = mode.label;
    pm.burial_destination = c.funeral_wills.residue_destination;
    pm.has_pacemaker = !!c.medical_record.has_pacemaker;
    pm.funeral_home_choice = c.funeral_wills.chosen_funeral_home;
    pm.has_funeral_insurance = !!c.funeral_wills.has_funeral_insurance;
    const bio = Number(c.medical_record.biological_hazard_level) || 0;
    c.medical_record.biological_hazard_label = ["Standard", "Hygiène renforcée", "Cercueil zingué (Biohazard 2)", "Alerte Prion (CE 999/2001)"][bio];
    const niss = R.validateNiss(c.civil_identity.national_id_niss, c.civil_identity.birth_date, c.civil_identity.gender);
    c.civil_identity.niss_valid = niss.valid;
    c.multimedia_memorial.audio_choice.has_voice_memo = Number(c.multimedia_memorial.audio_choice.voice_memo_duration_sec) > 0;
    c.bat_status = R.batStatus(c);
    return c;
  }

  // ------------------------------------------------------------ sélection d'un dossier
  function allCases() {
    return state.saved.map(c => Object.assign(c, { category: "MES_PAVS" })).concat(state.cases);
  }

  function populateSelect() {
    const sel = $("#caseSelect");
    const groups = {};
    allCases().forEach(c => { (groups[c.category] = groups[c.category] || []).push(c); });
    sel.innerHTML = Object.keys(groups).map(k =>
      `<optgroup label="${escapeHtml(CATEGORY_LABELS[k] || k)}">` +
      groups[k].map(c => `<option value="${escapeHtml(c.id)}">${escapeHtml(c.category === "MES_PAVS" ? (c.civil_identity.full_name || "PAVS sans nom") + " · " + c.id : c.label)}</option>`).join("") +
      `</optgroup>`).join("");
    if (state.data) sel.value = state.data.id;
  }

  function selectCase(id) {
    const src = allCases().find(c => c.id === id) || state.cases[0];
    state.data = clone(src);
    // Normalisation des champs ajoutés par le formulaire PAVS
    const pr = state.data.pavs_record;
    pr.post_mortem_wills = pr.post_mortem_wills || {};
    pr.desired_support = pr.desired_support || { types: [], special_wishes: "" };
    pr.refused_therapies = pr.refused_therapies || { artificial_nutrition: null, mechanical_ventilation: null, other_refusals: "" };
    const mm = state.data.multimedia_memorial;
    const d = state.design;
    d.epitaph = mm.epitaph || "";
    d.years = mm.lifespan_display || "";
    d.quote = (mm.epitaph || "").replace(/^Pour moi, l'essentiel c'est\s*:\s*/i, "");
    d.voiceExtract = pr.desired_support.special_wishes && pr.desired_support.special_wishes !== (pr.desired_support.types || [])[0]
      ? pr.desired_support.special_wishes : pr.essential_priority || "";
    d.exemplaire = 1;
    $("#caseSelect").value = state.data.id;
    syncMirrors(state.data);
    refreshInputs();
    refresh();
  }

  // ------------------------------------------------------------ liaisons formulaire ↔ données
  function refreshInputs(except) {
    const c = state.data;
    $$("[data-bind]").forEach(el => {
      if (el === except) return;
      const v = getPath(c, el.dataset.bind);
      if (el.type === "checkbox") el.checked = !!v;
      else el.value = v == null ? "" : v;
    });
    $$("[data-radio]").forEach(group => {
      const path = group.dataset.radio;
      const v = getPath(c, path);
      const radios = Array.from(group.querySelectorAll('input[type="radio"]'));
      let matched = false;
      radios.forEach(r => {
        if (r.value === "__other") return;
        const on = String(v) === r.value || (v == null && r.value === "null");
        r.checked = on;
        matched = matched || on;
      });
      const other = radios.find(r => r.value === "__other");
      if (other) {
        other.checked = !matched && !!v;
        const txt = group.querySelector(".other-text");
        if (txt !== except) txt.value = !matched && v ? v : "";
      }
    });
    $$("[data-list]").forEach(group => {
      const list = getPath(c, group.dataset.list) || [];
      const presets = Array.from(group.querySelectorAll("input")).map(i => i.value);
      group.querySelectorAll("input").forEach(i => { i.checked = list.includes(i.value); });
      const extra = list.filter(v => !presets.includes(v));
      const hint = group.parentElement.querySelector(".list-extra");
      if (hint) hint.textContent = extra.length ? `Autre(s) accompagnement(s) déclaré(s) : ${extra.join(", ")}` : "";
    });
    $$("[data-design]").forEach(el => {
      if (el === except) return;
      const v = state.design[el.dataset.design];
      if (el.type === "checkbox") el.checked = !!v;
      else el.value = v == null ? "" : v;
    });
    $$("[data-out]").forEach(o => {
      const v = state.design[o.dataset.out];
      o.textContent = o.dataset.out === "guillocheOpacity" ? `${Math.round(v * 100)} %` : o.dataset.out === "fontScale" ? `${Math.round(v * 100)} %` : v;
    });
    $$("[data-show]").forEach(el => { el.hidden = !getPath(c, el.dataset.show); });
  }

  function bindInputs() {
    $$("[data-bind]").forEach(el => {
      const ev = el.tagName === "SELECT" || el.type === "checkbox" || el.type === "date" ? "change" : "input";
      el.addEventListener(ev, () => {
        const val = el.type === "checkbox" ? el.checked : el.value;
        setPath(state.data, el.dataset.bind, convert(val, el.dataset.type));
        dataChanged(el);
      });
    });
    $$("[data-radio]").forEach(group => {
      const name = "r-" + group.dataset.radio.replace(/\./g, "-");
      group.querySelectorAll('input[type="radio"]').forEach(r => {
        r.name = name;
        r.addEventListener("change", () => {
          if (r.value === "__other") {
            const txt = group.querySelector(".other-text");
            txt.focus();
            setPath(state.data, group.dataset.radio, txt.value);
          } else setPath(state.data, group.dataset.radio, convert(r.value, group.dataset.type));
          dataChanged(r);
        });
      });
      const txt = group.querySelector(".other-text");
      if (txt) txt.addEventListener("input", () => {
        group.querySelector('input[value="__other"]').checked = true;
        setPath(state.data, group.dataset.radio, txt.value);
        dataChanged(txt);
      });
    });
    $$("[data-list]").forEach(group => {
      group.querySelectorAll("input").forEach(i => i.addEventListener("change", () => {
        const list = (getPath(state.data, group.dataset.list) || []).filter(v => v !== i.value);
        if (i.checked) list.push(i.value);
        setPath(state.data, group.dataset.list, list);
        dataChanged(i);
      }));
    });
    $$("[data-design]").forEach(el => {
      const ev = el.tagName === "SELECT" || el.type === "checkbox" ? "change" : "input";
      el.addEventListener(ev, () => {
        const k = el.dataset.design;
        let v = el.type === "checkbox" ? el.checked : el.value;
        if (el.type === "range" || el.type === "number") v = Number(v);
        state.design[k] = v;
        refreshInputs(el);
        scheduleRender();
      });
    });
  }

  function dataChanged(source) {
    syncMirrors(state.data);
    refreshInputs(source);
    persistIfMine();
    scheduleRender();
    scheduleFingerprint();
  }

  let persistTimer = 0;
  function persistIfMine() {
    const i = state.saved.findIndex(c => c.id === state.data.id);
    if (i < 0) return;
    clearTimeout(persistTimer);
    persistTimer = setTimeout(() => {
      state.saved[i] = clone(state.data);
      persistSaved();
      const opt = $(`#caseSelect option[value="${CSS.escape(state.data.id)}"]`);
      if (opt) opt.textContent = `${state.data.civil_identity.full_name || "PAVS sans nom"} · ${state.data.id}`;
    }, 400);
  }

  // ------------------------------------------------------------ empreinte SHA-256 (dossier canonique)
  function canonical(v) {
    if (Array.isArray(v)) return `[${v.map(canonical).join(",")}]`;
    if (v && typeof v === "object") return `{${Object.keys(v).sort().map(k => JSON.stringify(k) + ":" + canonical(v[k])).join(",")}}`;
    return JSON.stringify(v);
  }
  let fpTimer = 0;
  function scheduleFingerprint() {
    clearTimeout(fpTimer);
    fpTimer = setTimeout(async () => {
      try {
        const bytes = new TextEncoder().encode(canonical(state.data));
        const buf = await crypto.subtle.digest("SHA-256", bytes);
        state.design.fingerprint = Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, "0")).join("");
      } catch (e) {
        state.design.fingerprint = "";
      }
      scheduleRender();
    }, 250);
  }

  // ------------------------------------------------------------ rendu
  let raf = 0;
  function scheduleRender() {
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(refresh);
  }

  function currentCard() { return state.tab === "card2" ? 2 : 1; }

  function refresh() {
    const c = state.data;
    if (!c) return;
    document.body.dataset.tab = state.tab;
    const card = currentCard();
    const opts = { crop: state.crop, safe: state.safe };
    if (state.tab !== "pavs") {
      // Un seul jeu de faces dans le DOM à la fois : les identifiants SVG (dégradés, découpes) restent uniques.
      const side = state.view === "side";
      const recto = C.render(card, "recto", c, state.design, Object.assign({ prefix: side ? "r" : "fr" }, opts));
      const verso = C.render(card, "verso", c, state.design, Object.assign({ prefix: side ? "v" : "fv" }, opts));
      $("#holderRecto").innerHTML = side ? recto : "";
      $("#holderVerso").innerHTML = side ? verso : "";
      $("#flipFront").innerHTML = side ? "" : recto;
      $("#flipBack").innerHTML = side ? "" : verso;
      $("#miniPreview").innerHTML = "";
    } else {
      $("#holderRecto").innerHTML = $("#holderVerso").innerHTML = $("#flipFront").innerHTML = $("#flipBack").innerHTML = "";
      $("#miniPreview").innerHTML =
        `<p class="field-label">Aperçu Carte 1 (en direct)</p>` +
        C.render(1, "recto", c, state.design, { prefix: "mr" }) + C.render(1, "verso", c, state.design, { prefix: "mv" });
    }
    $("#canvas").classList.toggle("pulse", !!state.design.pulse && card === 2);
    document.documentElement.style.setProperty("--zoom", state.zoom);
    renderStatus();
    renderNotices();
  }

  function renderStatus() {
    const c = state.data;
    const ci = c.civil_identity;
    const bat = c.bat_status;
    const niss = R.validateNiss(ci.national_id_niss, ci.birth_date, ci.gender);
    const pyro = R.pyroStatus(c);
    const tone = bat.ready_to_print ? "ok" : ["ATTENTION_RADIO_ISOTOPES", "INCOMPLET_IDENTITE"].includes(bat.carte_1_status) ? "warn" : "danger";
    const portrait = state.design.portraitBytes;
    const ef = [
      ["EF-0", "Métadonnées", 512], ["EF-1", "Profil CBOR", 2048], ["EF-2", "Portrait WebP", 20480],
      ["EF-3", "Mémo vocal", 46080], ["EF-4", "Directives", 15360], ["EF-5", "Sceau COSE", 2048]
    ];
    $("#statusCard").innerHTML = `
      <div class="status-head">
        <span class="badge ${tone}">${escapeHtml(R.BAT_LABELS[bat.carte_1_status] || bat.carte_1_status)}</span>
        <code>${escapeHtml(c.id)}</code>
      </div>
      <p class="status-title">${escapeHtml(c.label || "")}</p>
      <ul class="checks">
        <li class="${niss.valid ? "ok" : "danger"}">NISS modulo 97 : ${niss.valid ? "valide" : "invalide (" + escapeHtml(niss.reason) + ")"}${niss.sexOk === false ? " · parité séquence/genre incohérente" : ""}</li>
        <li class="${pyro.level}">${escapeHtml(pyro.title)}</li>
      </ul>
      <details class="ef"><summary>Budget silicium ACOSJ 92 Ko</summary>
        <table>${ef.map(([id, label, q]) => `<tr><td>${id}</td><td>${label}</td><td>${id === "EF-2" && portrait ? `${portrait.toLocaleString("fr-BE")} / ` : ""}${q.toLocaleString("fr-BE")} o</td></tr>`).join("")}
        <tr class="total"><td colspan="2">Utile · réserve 5 632 o (6,11 %)</td><td>86 528 / 92 160 o</td></tr></table>
      </details>`;
    const hint = niss.valid ? "✓ modulo 97" : ci.national_id_niss ? `✗ ${niss.reason}` : "";
    $$("#nissHint, .niss-hint").forEach(h => { h.textContent = hint; h.className = `hint ${niss.valid ? "ok" : "danger"} ${h.id ? "" : "niss-hint"}`; });
  }

  function renderNotices() {
    const c = state.data;
    const sarco = R.isSarco(c.funeral_wills.burial_mode);
    $$(".sarco-notice").forEach(n => { n.hidden = !sarco; n.textContent = `Sarcomusation : ${R.SARCO_NOTICE} (DEC-AET-15). Les 5 destinations cinéraires et le verrou pyrotechnique s'appliquent comme pour la crémation.`; });
    const pyro = R.pyroStatus(c);
    $$(".pyro-notice").forEach(n => {
      n.hidden = !c.medical_record.has_pacemaker;
      n.className = `notice pyro-notice ${pyro.level}`;
      n.textContent = `${pyro.title} — ${pyro.detail}`;
    });
    $$(".science-hint").forEach(n => { n.hidden = !c.medical_record.body_donation_science; });
  }

  // ------------------------------------------------------------ portrait (DEC-AET-12 : WebP 480×480 ≤ 20 480 o)
  async function loadPortrait(file) {
    const info = $("#portraitInfo");
    try {
      const bmp = await createImageBitmap(file);
      const side = Math.min(bmp.width, bmp.height);
      const cv = document.createElement("canvas");
      cv.width = cv.height = 480;
      cv.getContext("2d").drawImage(bmp, (bmp.width - side) / 2, (bmp.height - side) / 2, side, side, 0, 0, 480, 480);
      let blob = null;
      let q = 0.8;
      for (; q >= 0.2; q -= 0.05) {
        blob = await new Promise(res => cv.toBlob(res, "image/webp", q));
        if (!blob || blob.type !== "image/webp" || blob.size <= 20480) break;
      }
      if (!blob || blob.type !== "image/webp") {
        info.textContent = "Ce navigateur ne sait pas encoder le WebP : portrait non retenu.";
        info.className = "hint danger";
        return;
      }
      state.design.portrait = await new Promise(res => { const r = new FileReader(); r.onload = () => res(r.result); r.readAsDataURL(blob); });
      state.design.portraitBytes = blob.size;
      const ok = blob.size <= 20480;
      info.textContent = `WebP 480×480 · ${blob.size.toLocaleString("fr-BE")} o · q ${q.toFixed(2).replace(".", ",")} ${ok ? "✓ EF-2" : "✗ dépasse EF-2"}`;
      info.className = `hint ${ok ? "ok" : "danger"}`;
      state.data.multimedia_memorial.has_portrait = true;
      scheduleRender();
    } catch (e) {
      info.textContent = "Image illisible.";
      info.className = "hint danger";
    }
  }

  // ------------------------------------------------------------ export SVG (polices embarquées si possible)
  async function fontFaceCss() {
    const keys = new Set([state.design.fontTitle, state.design.fontBody, "inter", "fira"]);
    let css = "";
    for (const k of keys) {
      const [family, files] = FONT_FILES[k] || [];
      if (!family) continue;
      for (const [file, weight, style] of files) {
        const resp = await fetch(`fonts/${file}.woff2`);
        if (!resp.ok) throw new Error("font");
        const buf = new Uint8Array(await resp.arrayBuffer());
        let bin = "";
        for (let i = 0; i < buf.length; i += 0x8000) bin += String.fromCharCode.apply(null, buf.subarray(i, i + 0x8000));
        css += `@font-face{font-family:'${family}';font-weight:${weight};font-style:${style};src:url(data:font/woff2;base64,${btoa(bin)}) format('woff2');}`;
      }
    }
    return css;
  }

  async function exportSvg(side) {
    const card = currentCard();
    let svg = C.render(card, side, state.data, state.design, { export: true, crop: state.crop, safe: state.safe, prefix: "x" });
    let embedded = true;
    try {
      svg = svg.replace("<defs>", `<defs><style>${await fontFaceCss()}</style>`);
    } catch (e) {
      embedded = false;
    }
    const name = `aeternitrak_carte${card}_${side}_${slug(state.data.civil_identity.full_name || state.data.id)}.svg`;
    download(name, `<?xml version="1.0" encoding="UTF-8"?>\n${svg}`, "image/svg+xml");
    toast(embedded ? `${name} exporté (polices embarquées).` : `${name} exporté — polices non embarquées (ouvrez l'app via un serveur local pour les inclure).`);
  }

  function download(name, content, type) {
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([content], { type }));
    a.download = name;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
  }

  // ------------------------------------------------------------ impression B.A.T. 1:1
  function printBat() {
    const c = state.data;
    const card = currentCard();
    const opts = { print: true, crop: true, safe: state.safe };
    const bat = c.bat_status;
    const today = new Date().toLocaleDateString("fr-BE");
    const blocked = card === 1 && !bat.ready_to_print;
    $("#printSheet").innerHTML = `
      <div class="ps-page">
        <header class="ps-head">
          <strong>Bon à tirer · AeterniTrak · Carte ${card} ${card === 1 ? "Volontés & sécurité" : "Mémorial & acoustique"}</strong>
          <span>${escapeHtml(c.civil_identity.full_name || "")} · ${escapeHtml(c.id)} · ${today}</span>
        </header>
        ${blocked ? `<p class="ps-blocked">B.A.T. NON VALIDABLE — ${escapeHtml(R.BAT_LABELS[bat.carte_1_status])}. Épreuve de contrôle uniquement.</p>` : ""}
        <div class="ps-faces">
          <figure>${C.render(card, "recto", c, state.design, Object.assign({ prefix: "pr" }, opts))}<figcaption>Recto</figcaption></figure>
          <figure>${C.render(card, "verso", c, state.design, Object.assign({ prefix: "pv" }, opts))}<figcaption>Verso</figcaption></figure>
        </div>
        <svg class="ps-ruler" xmlns="http://www.w3.org/2000/svg" width="100mm" height="6mm" viewBox="0 0 100 6">
          <path d="M0 5.5H100${Array.from({ length: 11 }, (_, i) => `M${i * 10} 5.5V${i % 5 ? 3 : 1}`).join("")}" stroke="#000" stroke-width=".15" fill="none"/>
        </svg>
        <p class="ps-foot">Échelle 1:1 — la règle doit mesurer exactement 100 mm et chaque carte 85,60 × 53,98 mm (imprimer à 100 %, sans « ajuster à la page »). Traits de coupe 5 mm, fond perdu 2 mm${state.safe ? ", zone de sécurité 3 mm (cyan)" : ""}, ligne de découpe magenta. Rendu vectoriel : résolution ≥ 300 DPI garantie par l'imprimante.</p>
      </div>`;
    document.body.classList.add("printing-bat");
    window.print();
  }

  function printPavs() {
    const c = state.data;
    const ci = c.civil_identity;
    const pr = c.pavs_record;
    const pm = pr.post_mortem_wills || {};
    const yn = v => (v === true ? "Oui" : v === false ? "Non" : "—");
    const refuse = v => (v === true ? "Je refuse" : v === false ? "J'accepte" : "Sans avis");
    const contact = o => (o && (o.name || o.phone) ? `${o.name || ""}${o.phone ? " · " + o.phone : ""}` : "—");
    const don = { 1: "Oui", 3: "Non (opposition expresse)", 2: "Je ne me prononce pas" }[Number(c.medical_record.organ_donation_status)] || "—";
    const row = (q, a) => `<tr><th>${escapeHtml(q)}</th><td>${escapeHtml(a == null || a === "" ? "—" : a)}</td></tr>`;
    const mode = R.burialMode(c.funeral_wills.burial_mode);
    $("#printSheet").innerHTML = `
      <div class="ps-page pavs-print">
        <h1>PAVS — Plan anticipé de volontés et soins</h1>
        <p class="ps-sub">Résumé du Projet de soins personnalisé et anticipé (PSPA) · enregistré le ${C.shortDate(pr.registered_date)}</p>
        <h2>Cinq points d'attention</h2>
        <ol class="ps-attention">
          <li>Lieu de conservation du PSPA : <strong>${escapeHtml(pr.conservation_place || "—")}</strong></li>
          <li>À tout moment, vous avez la possibilité de modifier votre PSPA et votre PAVS.</li>
          <li>Le PSPA et le PAVS ne sont utiles que si vous n’êtes plus en capacité de vous exprimer.</li>
          <li>Il est conseillé de compléter ce document en concertation avec un professionnel de la santé et/ou un proche.</li>
          <li>Ce document ne sera plus accessible sur le Réseau Santé Wallon après le décès : conservez cette copie.</li>
        </ol>
        <h2>Mes données administratives</h2>
        <table>${row("Nom et prénom", ci.full_name)}${row("Téléphone", ci.phone)}${row("Numéro de registre national", ci.national_id_niss)}${row("Genre", ci.gender)}
          ${row("Institution(s)", contact(pr.institution))}${row("Médecin traitant", contact({ name: (ci.certifying_physician || {}).name, phone: (ci.certifying_physician || {}).phone }))}
          ${row("Personne(s) à contacter", contact(pr.contact_person))}${row("Mandataire (soins de santé)", contact(pr.health_proxy))}
          ${row("Mandataire extrajudiciaire", contact(pr.extrajudicial_proxy))}${row("Personne(s) de confiance", contact(pr.trusted_person))}
          ${row("Administrateur de biens et/ou de la personne", contact(pr.property_administrator))}</table>
        <h2>Mon projet de soins</h2>
        <table>${row("Projet global (intensité des soins)", pr.care_intensity)}
          ${row("Alimentation artificielle", refuse(pr.refused_therapies.artificial_nutrition))}${row("Aide à la respiration", refuse(pr.refused_therapies.mechanical_ventilation))}
          ${pr.refused_therapies.other_refusals ? row("Autre(s) refus", pr.refused_therapies.other_refusals) : ""}
          ${row("À soins égaux je préfère être", pr.preferred_care_setting)}${row("Types d’hospitalisations acceptés", pr.accepted_hospitalizations)}${row("Commentaires", pr.comments)}</table>
        <h2>Mes souhaits de fin de vie</h2>
        <table>${row("Fin de vie dans mon lieu de vie habituel", pr.preferred_end_of_life_place ? (pr.preferred_end_of_life_place.startsWith("Lieu de vie") ? "Oui" : "Non") : "")}
          ${row("Accompagnement désiré", (pr.desired_support.types || []).join(", "))}${row("À propos de mon accompagnement", pr.desired_support.special_wishes)}
          ${row("Pour moi, l’essentiel c’est", pr.essential_priority)}${row("Mes autres souhaits", pr.other_wishes)}</table>
        <h2>Mes volontés pour l’après-décès</h2>
        <table>${row("J’accepte de donner mes organes", don)}${row("Je donne mon corps à la science", yn(!!c.medical_record.body_donation_science))}
          ${row("Je désire être", mode.label + (R.isSarco(mode.id) ? " — " + R.SARCO_NOTICE : ""))}${row("J'ai un pacemaker", yn(!!c.medical_record.has_pacemaker) + (c.medical_record.has_pacemaker ? " — " + R.pyroStatus(c).title : ""))}
          ${row("Je laisse à mes proches le choix de mes obsèques", yn(pm.leave_choice_to_relatives))}
          ${row("Rite(s) / rituel(s) à respecter", [c.funeral_wills.ceremony_nature, c.funeral_wills.residue_destination].filter(Boolean).join(" · "))}
          ${row("Pompes funèbres de mon choix", c.funeral_wills.chosen_funeral_home)}
          ${row("Assurance obsèques", yn(!!c.funeral_wills.has_funeral_insurance) + (pm.funeral_insurance_ref ? " · " + pm.funeral_insurance_ref : ""))}
          ${row("Mes autres souhaits", pm.other_wishes)}</table>
        <p class="ps-foot">Formulaire PAVS · Réseau Santé Wallon · FRATEM asbl © 2026 · Copie générée par PaxStudio Design (AeterniTrak) · Signature : ______________________ Date : ____________</p>
      </div>`;
    document.body.classList.add("printing-bat");
    window.print();
  }

  // ------------------------------------------------------------ « Ajouter un PAVS »
  function newPavs() {
    const id = `MON_PAVS_${Date.now().toString(36).toUpperCase()}`;
    const c = R.blankCase(id);
    state.saved.unshift(c);
    persistSaved();
    populateSelect();
    selectCase(id);
    setTab("pavs");
    toast("Nouveau PAVS créé — il est enregistré sur cet appareil au fil de la saisie.");
    const first = $('#pavsView [data-bind="civil_identity.full_name"]');
    if (first) first.focus();
  }

  function savePavs() {
    const mine = state.saved.findIndex(c => c.id === state.data.id);
    if (mine >= 0) {
      state.saved[mine] = clone(state.data);
    } else {
      const copy = clone(state.data);
      copy.id = `MON_PAVS_${Date.now().toString(36).toUpperCase()}`;
      copy.label = `Copie de ${state.data.label}`;
      state.saved.unshift(copy);
      state.data = clone(copy);
    }
    const ok = persistSaved();
    populateSelect();
    $("#caseSelect").value = state.data.id;
    toast(ok ? "PAVS enregistré dans « Mes PAVS » (sur cet appareil)." : "Stockage local indisponible : exportez le PAVS en JSON pour le conserver.");
  }

  function importPavs(file) {
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const c = JSON.parse(reader.result);
        if (!c || !c.civil_identity || !c.pavs_record || !c.funeral_wills || !c.medical_record) throw new Error("format");
        const base = R.blankCase(c.id || "IMPORT");
        const merged = Object.assign(base, c);
        if (allCases().some(x => x.id === merged.id)) merged.id = `MON_PAVS_${Date.now().toString(36).toUpperCase()}`;
        merged.multimedia_memorial = Object.assign(R.blankCase("x").multimedia_memorial, c.multimedia_memorial || {});
        state.saved.unshift(syncMirrors(merged));
        persistSaved();
        populateSelect();
        selectCase(merged.id);
        toast("PAVS importé.");
      } catch (e) {
        toast("Fichier JSON non reconnu comme dossier PAVS.");
      }
    };
    reader.readAsText(file);
  }

  // ------------------------------------------------------------ navigation & interface
  function setTab(tab) {
    state.tab = tab;
    $$(".tab").forEach(t => { const on = t.dataset.tab === tab; t.classList.toggle("active", on); t.setAttribute("aria-selected", on); });
    $("#pavsView").hidden = tab !== "pavs";
    $("#canvas").hidden = tab === "pavs";
    $("#cardToolbar").hidden = tab === "pavs";
    $$("[data-only=card2]").forEach(el => { el.hidden = tab !== "card2"; });
    refresh();
  }

  function setView(view) {
    state.view = view;
    $$("[data-view]").forEach(b => b.classList.toggle("on", b.dataset.view === view));
    $("#faces").hidden = view !== "side";
    $("#flipWrap").hidden = view !== "flip";
    refresh();
  }

  function buildControls() {
    const modes = R.BURIAL_MODES.reduce((acc, m) => {
      (acc[m.family] = acc[m.family] || []).push(m);
      return acc;
    }, {});
    const famLabel = { inhumation: "Inhumation", cremation: "Crémation (procédé thermique)", sarco: "Sarcomusation (démonstrateur prospectif · thermique)", humusation: "Humusation", science: "Science" };
    $$(".burial-select").forEach(sel => {
      sel.innerHTML = Object.keys(modes).map(f => `<optgroup label="${famLabel[f]}">${modes[f].map(m => `<option value="${m.id}">${m.id}. ${escapeHtml(m.label)}</option>`).join("")}</optgroup>`).join("");
    });
    $$(".font-select").forEach(sel => {
      sel.innerHTML = Object.entries(C.FONTS).map(([k, v]) => `<option value="${k}" style="font-family:${v.stack}">${v.label}</option>`).join("");
    });
    $("#materialSwatches").innerHTML = Object.entries(C.MATERIALS).map(([k, m]) =>
      `<button role="radio" data-material="${k}" aria-checked="${k === state.design.material}" title="${escapeHtml(m.label)}" style="--sw1:${m.bg1};--sw2:${m.bg2};--swa:${m.accent}"><span></span>${escapeHtml(m.label.split(" ")[0])}</button>`).join("");
    $$("[data-material]").forEach(b => b.addEventListener("click", () => {
      state.design.material = b.dataset.material;
      state.design.gold = C.MATERIALS[b.dataset.material].accent;
      $$("[data-material]").forEach(x => x.setAttribute("aria-checked", x === b));
      refreshInputs();
      scheduleRender();
    }));
    $$("[data-layout]").forEach(b => b.addEventListener("click", () => {
      state.design.layout = b.dataset.layout;
      updateLayoutButtons();
      scheduleRender();
    }));
    updateLayoutButtons();
  }

  function updateLayoutButtons() {
    $$("[data-layout]").forEach(b => { b.classList.toggle("on", b.dataset.layout === state.design.layout); b.setAttribute("aria-checked", b.dataset.layout === state.design.layout); });
    $("#layoutName").textContent = LAYOUT_NAMES[state.design.layout];
  }

  function bindUi() {
    $$(".tab").forEach(t => t.addEventListener("click", () => setTab(t.dataset.tab)));
    $$("[data-view]").forEach(b => b.addEventListener("click", () => setView(b.dataset.view)));
    $("#caseSelect").addEventListener("change", e => selectCase(e.target.value));
    $("#btnNewPavs").addEventListener("click", newPavs);
    $("#chkCrop").addEventListener("change", e => { state.crop = e.target.checked; scheduleRender(); });
    $("#chkSafe").addEventListener("change", e => { state.safe = e.target.checked; scheduleRender(); });
    $("#zoom").addEventListener("input", e => { state.zoom = Number(e.target.value); scheduleRender(); });
    $("#flipper").addEventListener("click", () => { state.flipped = !state.flipped; $("#flipper").classList.toggle("flipped", state.flipped); });
    $("#btnSvgRecto").addEventListener("click", () => exportSvg("recto"));
    $("#btnSvgVerso").addEventListener("click", () => exportSvg("verso"));
    $("#btnPrint").addEventListener("click", printBat);
    $("#btnPavsPrint").addEventListener("click", printPavs);
    $("#btnPavsSave").addEventListener("click", savePavs);
    $("#btnPavsExport").addEventListener("click", () => {
      download(`PAVS_${slug(state.data.civil_identity.full_name || state.data.id)}.json`, JSON.stringify(syncMirrors(state.data), null, 2), "application/json");
    });
    $("#pavsImport").addEventListener("change", e => { if (e.target.files[0]) importPavs(e.target.files[0]); e.target.value = ""; });
    $("#portraitInput").addEventListener("change", e => { if (e.target.files[0]) loadPortrait(e.target.files[0]); e.target.value = ""; });
    $("#btnPortraitClear").addEventListener("click", () => {
      state.design.portrait = null;
      state.design.portraitBytes = 0;
      $("#portraitInfo").textContent = "Aucun portrait : camée vectoriel.";
      $("#portraitInfo").className = "hint";
      scheduleRender();
    });
    window.addEventListener("afterprint", () => document.body.classList.remove("printing-bat"));
  }

  // ------------------------------------------------------------ utilitaires UI
  function escapeHtml(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, ch => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]));
  }
  function slug(s) {
    return String(s).normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^A-Za-z0-9]+/g, "_").replace(/^_|_$/g, "");
  }
  let toastTimer = 0;
  function toast(msg) {
    const t = $("#toast");
    t.textContent = msg;
    t.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => t.classList.remove("show"), 4200);
  }

  // ------------------------------------------------------------ démarrage
  document.addEventListener("DOMContentLoaded", () => {
    buildControls();
    bindInputs();
    bindUi();
    populateSelect();
    const start = allCases().find(c => c.id === "PAVS_01_CH") || allCases()[0];
    selectCase(start.id);
    setTab("card1");
    scheduleFingerprint();
    // Re-rendu une fois les polices chargées (mesures de texte exactes)
    if (document.fonts && document.fonts.load) {
      const faces = ["600 10px Cinzel", "400 10px 'Cormorant Garamond'", "italic 400 10px 'Cormorant Garamond'", "600 10px 'Cormorant Garamond'",
        "italic 600 10px 'Cormorant Garamond'", "400 10px 'Playfair Display'", "700 10px 'Playfair Display'", "400 10px Inter", "600 10px Inter",
        "400 10px 'Fira Code'", "500 10px 'Fira Code'"];
      Promise.all(faces.map(face => document.fonts.load(face).catch(() => null))).then(scheduleRender);
    }
  });
})();
