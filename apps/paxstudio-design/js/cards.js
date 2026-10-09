/**
 * PaxStudio Design — Moteur de rendu SVG des deux cartes ID-1 (85,60 × 53,98 mm).
 *
 * Toutes les coordonnées sont en millimètres (viewBox = mm), ce qui garantit
 * l'échelle 1:1 à l'impression et un export SVG vectoriel pur.
 *   PaxCards.render(card, side, data, design, opts) → chaîne SVG
 *   card : 1 (Volontés & Sécurité) | 2 (Mémorial & Acoustique) ; side : "recto" | "verso"
 *   opts : { crop, safe, prefix, print }
 */
(function (root) {
  "use strict";

  const R = root.PaxRules;
  const O = root.PaxOrnaments;
  const W = 85.6;
  const H = 53.98;
  const CORNER = 3.18; // rayon d'angle ISO/IEC 7810
  const M = 4.5; // marge de composition (zone de sécurité 3 mm + respiration)
  const f = n => Math.round(n * 1000) / 1000;

  const FONTS = {
    cinzel: { label: "Cinzel", stack: "Cinzel, 'Trajan Pro', Georgia, serif" },
    cormorant: { label: "Cormorant Garamond", stack: "'Cormorant Garamond', Garamond, Georgia, serif" },
    playfair: { label: "Playfair Display", stack: "'Playfair Display', Didot, Georgia, serif" },
    inter: { label: "Inter", stack: "Inter, 'Segoe UI', system-ui, sans-serif" },
    fira: { label: "Fira Code", stack: "'Fira Code', Consolas, 'Courier New', monospace" }
  };

  const MATERIALS = {
    ivoire: { label: "Ivoire astral & or fin", bg1: "#f8f1df", bg2: "#e6d7b4", ink: "#2a2219", muted: "#76664a", accent: "#a8822f", texture: "paper" },
    bois: { label: "Chêne des Ardennes", bg1: "#7d5535", bg2: "#4a2f1d", ink: "#f8ecd3", muted: "#d9c39d", accent: "#dcb86c", texture: "wood" },
    albatre: { label: "Albâtre minéral & platine", bg1: "#fdfcf9", bg2: "#e4e3de", ink: "#1d1f24", muted: "#5f6670", accent: "#8a95a3", texture: "marble" },
    obsidienne: { label: "Obsidienne nuit & silicium", bg1: "#1c212b", bg2: "#06070a", ink: "#ece6d6", muted: "#a29e94", accent: "#c9a85a", texture: "silicon" }
  };

  const TONES = { danger: "#b42318", warn: "#a86b12", ok: "#2f7d4f", info: "#2b5f9e", muted: "#6b6b6b" };

  // ---------------------------------------------------------------- utilitaires
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, ch => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]));
  }

  function hexToRgb(hex) {
    const h = hex.replace("#", "");
    const n = parseInt(h.length === 3 ? h.split("").map(x => x + x).join("") : h, 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }
  function mix(a, b, t) {
    const A = hexToRgb(a);
    const B = hexToRgb(b);
    return "#" + A.map((v, i) => Math.round(v + (B[i] - v) * t).toString(16).padStart(2, "0")).join("");
  }
  function rgba(hex, a) {
    const [r, g, b] = hexToRgb(hex);
    return `rgba(${r},${g},${b},${a})`;
  }

  let measureCtx = null;
  /** Largeur d'un texte en mm (canvas si disponible, estimation sinon). */
  function measure(text, size, family, weight, style) {
    if (typeof document !== "undefined") {
      measureCtx = measureCtx || document.createElement("canvas").getContext("2d");
      measureCtx.font = `${style || "normal"} ${weight || 400} ${size * 10}px ${family}`;
      return measureCtx.measureText(String(text)).width / 10;
    }
    return String(text).length * size * 0.52;
  }

  /** Réduit la taille jusqu'à tenir dans maxW ; tronque avec « … » sous minSize. */
  function fit(text, maxW, size, fam, weight, minSize, style) {
    let s = size;
    while (s > minSize && measure(text, s, fam, weight, style) > maxW) s -= 0.05;
    let t = String(text);
    while (t.length > 1 && measure(t, s, fam, weight, style) > maxW) t = t.slice(0, -2) + "…";
    return { text: t, size: s };
  }

  /** Coupe en lignes de largeur maxW (au plus maxLines, la dernière tronquée). */
  function wrap(text, maxW, size, fam, maxLines, style) {
    const words = String(text || "").split(/\s+/).filter(Boolean);
    const lines = [];
    let cur = "";
    for (const w of words) {
      const test = cur ? cur + " " + w : w;
      if (measure(test, size, fam, 400, style) <= maxW || !cur) cur = test;
      else { lines.push(cur); cur = w; }
    }
    if (cur) lines.push(cur);
    if (lines.length > maxLines) {
      const kept = lines.slice(0, maxLines);
      let last = kept[maxLines - 1] + "…";
      while (last.length > 2 && measure(last, size, fam, 400, style) > maxW) last = last.slice(0, -2) + "…";
      kept[maxLines - 1] = last;
      return kept;
    }
    return lines;
  }

  function T(x, y, text, o) {
    const a = [
      `x="${f(x)}"`, `y="${f(y)}"`, `font-family="${esc(o.fam)}"`, `font-size="${f(o.size)}"`,
      `fill="${o.fill}"`
    ];
    if (o.weight) a.push(`font-weight="${o.weight}"`);
    if (o.anchor) a.push(`text-anchor="${o.anchor}"`);
    if (o.ls) a.push(`letter-spacing="${f(o.ls)}"`);
    if (o.italic) a.push(`font-style="italic"`);
    if (o.opacity) a.push(`opacity="${o.opacity}"`);
    if (o.cls) a.push(`class="${o.cls}"`);
    return `<text ${a.join(" ")}>${esc(text)}</text>`;
  }

  function hash(str) {
    let h = 2166136261;
    for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); }
    return h >>> 0;
  }

  const MONTHS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"];
  function longDate(iso) {
    const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso || "");
    return m ? `${Number(m[3])} ${MONTHS[Number(m[2]) - 1]} ${m[1]}` : "—";
  }
  function shortDate(iso) {
    const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso || "");
    return m ? `${m[3]}/${m[2]}/${m[1]}` : "—";
  }

  // ---------------------------------------------------------------- contexte de rendu
  function context(card, side, data, design, opts) {
    const mat = MATERIALS[design.material] || MATERIALS.ivoire;
    const accent = design.gold || mat.accent;
    const scale = Number(design.fontScale) || 1;
    return {
      p: opts.prefix || `c${card}${side[0]}`,
      data, design, opts, mat, accent,
      accentLight: mix(accent, "#ffffff", 0.45),
      accentDark: mix(accent, "#000000", 0.35),
      ink: mat.ink, muted: mat.muted,
      dark: mat.texture === "wood" || mat.texture === "silicon",
      title: (FONTS[design.fontTitle] || FONTS.cinzel).stack,
      body: (FONTS[design.fontBody] || FONTS.cormorant).stack,
      mono: FONTS.fira.stack,
      dfam: (FONTS[design.fontData] || FONTS.inter).stack,
      sans: FONTS.inter.stack,
      s: v => v * scale,
      gOpacity: Number(design.guillocheOpacity ?? 0.35),
      gDensity: Number(design.guillocheDensity ?? 5)
    };
  }

  function defs(x) {
    const { p, mat, accent, accentLight, accentDark } = x;
    return `<defs>
      <linearGradient id="${p}-bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${mat.bg1}"/><stop offset="1" stop-color="${mat.bg2}"/></linearGradient>
      <linearGradient id="${p}-gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${accentLight}"/><stop offset=".45" stop-color="${accent}"/><stop offset=".55" stop-color="${accentDark}"/><stop offset="1" stop-color="${accentLight}"/></linearGradient>
      <linearGradient id="${p}-goldv" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="${accentDark}"/><stop offset=".6" stop-color="${accent}"/><stop offset="1" stop-color="${accentLight}"/></linearGradient>
      <radialGradient id="${p}-sheen" cx=".25" cy=".15" r="1"><stop offset="0" stop-color="#fff" stop-opacity="${x.dark ? 0.1 : 0.45}"/><stop offset=".6" stop-color="#fff" stop-opacity="0"/></radialGradient>
      <pattern id="${p}-hatch" width="1.6" height="1.6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="1.6" height="1.6" fill="#8f1616"/><rect width=".7" height="1.6" fill="#a61d1d"/></pattern>
      <clipPath id="${p}-trim"><rect x="0" y="0" width="${W}" height="${H}" rx="${CORNER}"/></clipPath>
    </defs>`;
  }

  /** Fond matière (déborde de 2 mm en mode traits de coupe). */
  function background(x) {
    const b = x.opts.crop ? 2 : 0;
    const r = `x="${-b}" y="${-b}" width="${W + 2 * b}" height="${H + 2 * b}"`;
    let tex = "";
    const h = hash(x.p + x.mat.texture);
    if (x.mat.texture === "wood") {
      for (let i = 0; i < 46; i++) {
        const y0 = -b + (i * (H + 2 * b)) / 46;
        const amp = 0.4 + ((h >> (i % 24)) & 7) / 6;
        let d = `M${-b} ${f(y0)}`;
        for (let xx = -b; xx <= W + b; xx += 2) d += `L${f(xx)} ${f(y0 + amp * Math.sin(xx / (7 + (i % 5)) + i))}`;
        tex += `<path d="${d}" stroke="${i % 3 ? "#2b190d" : "#c08a5a"}" stroke-width="${i % 4 ? 0.12 : 0.3}" fill="none" opacity="${i % 3 ? 0.35 : 0.18}"/>`;
      }
    } else if (x.mat.texture === "marble") {
      for (let i = 0; i < 6; i++) {
        const y0 = (i * H) / 5 + ((h >> i) & 7);
        tex += `<path d="M${-b} ${f(y0)}C${f(W * 0.3)} ${f(y0 - 9 + i * 3)} ${f(W * 0.6)} ${f(y0 + 10 - i)} ${f(W + b)} ${f(y0 - 4)}" stroke="#9aa0a8" stroke-width="${0.08 + (i % 3) * 0.06}" fill="none" opacity=".35"/>`;
      }
    } else if (x.mat.texture === "silicon") {
      for (let i = 0; i < 14; i++) {
        const y0 = 4 + i * 3.6;
        const x0 = 52 + ((h >> i) & 15);
        tex += `<path d="M${W + b} ${f(y0)}H${f(x0)}l-2 2" stroke="${x.accent}" stroke-width=".08" fill="none" opacity=".22"/><circle cx="${f(x0 - 2)}" cy="${f(y0 + 2)}" r=".25" fill="${x.accent}" opacity=".3"/>`;
      }
    }
    return `<rect ${r} fill="url(#${x.p}-bg)"/>${tex}<rect ${r} fill="url(#${x.p}-sheen)"/>`;
  }

  function guilloche(x, rosettes) {
    const c = x.dark ? x.accentLight : x.accent;
    let g = O.guillocheWaves(0, 0, W, H, x.gDensity, c, x.gOpacity * 0.55);
    for (const r of rosettes) g += O.rosette(r[0], r[1], r[2], x.gDensity, c, x.gOpacity);
    return `<g class="guilloche">${g}</g>`;
  }

  function fillets(x) {
    return `<rect x="1.5" y="1.5" width="${f(W - 3)}" height="${f(H - 3)}" rx="2" fill="none" stroke="url(#${x.p}-gold)" stroke-width=".28"/>
      <rect x="2.15" y="2.15" width="${f(W - 4.3)}" height="${f(H - 4.3)}" rx="1.5" fill="none" stroke="url(#${x.p}-gold)" stroke-width=".08"/>`;
  }

  function goldRule(x, x1, x2, y) {
    const mid = (x1 + x2) / 2;
    return `<path d="M${f(x1)} ${f(y)}H${f(mid - 1.4)}M${f(mid + 1.4)} ${f(y)}H${f(x2)}" stroke="url(#${x.p}-gold)" stroke-width=".18"/>
      <path d="M${f(mid)} ${f(y - 0.8)}l.8 .8-.8 .8-.8-.8z" fill="url(#${x.p}-gold)"/>`;
  }

  function pill(xx, y, label, tone, iconName, x, size) {
    const fs = size || 1.2;
    const w = measure(label, fs, x.sans, 600) + (iconName ? 3.6 : 2);
    const col = TONES[tone] || TONES.muted;
    return {
      w,
      svg: `<g><rect x="${f(xx)}" y="${f(y)}" width="${f(w)}" height="${f(fs * 2.2)}" rx="${f(fs * 1.1)}" fill="${col}"/>` +
        (iconName ? O.icon(iconName, xx + 0.7, y + fs * 0.35, fs * 1.5, "#fff", 0.16) : "") +
        T(xx + (iconName ? 2.75 : 1), y + fs * 1.5, label, { fam: x.sans, size: fs, weight: 600, fill: "#fff" }) + `</g>`
    };
  }

  /** Portrait photo (si fourni) ou camée vectoriel, découpé dans une forme. */
  function portrait(x, shape, id) {
    const clip = `${x.p}-${id}`;
    const shapeEl = shape.kind === "ellipse"
      ? `<ellipse cx="${f(shape.cx)}" cy="${f(shape.cy)}" rx="${f(shape.rx)}" ry="${f(shape.ry)}"/>`
      : shape.kind === "arch"
        ? `<path d="M${f(shape.x)} ${f(shape.y + shape.h)}V${f(shape.y + shape.w / 2)}a${f(shape.w / 2)} ${f(shape.w / 2)} 0 0 1 ${f(shape.w)} 0V${f(shape.y + shape.h)}z"/>`
        : `<rect x="${f(shape.x)}" y="${f(shape.y)}" width="${f(shape.w)}" height="${f(shape.h)}" rx="${f(shape.r || 0)}"/>`;
    const bx = shape.kind === "ellipse" ? { x: shape.cx - shape.rx, y: shape.cy - shape.ry, w: shape.rx * 2, h: shape.ry * 2 } : shape;
    let inner;
    if (x.design.portrait) {
      inner = `<image href="${x.design.portrait}" x="${f(bx.x)}" y="${f(bx.y)}" width="${f(bx.w)}" height="${f(bx.h)}" preserveAspectRatio="xMidYMid slice"/>`;
    } else {
      const panel = x.dark ? rgba("#000000", 0.35) : rgba(x.accent, 0.12);
      inner = `<rect x="${f(bx.x)}" y="${f(bx.y)}" width="${f(bx.w)}" height="${f(bx.h)}" fill="${panel}"/>` +
        O.spiro(bx.x + bx.w / 2, bx.y + bx.h / 2, 7, 4, 3.2, Math.min(bx.w, bx.h) / 26, x.accent, 0.35) +
        O.cameo(bx.x + bx.w / 2, bx.y + bx.h / 2, bx.w * 0.36, bx.h * 0.4, `url(#${x.p}-goldv)`, "none");
    }
    return `<clipPath id="${clip}">${shapeEl}</clipPath><g clip-path="url(#${clip})">${inner}</g>` +
      shapeEl.replace("/>", ` fill="none" stroke="url(#${x.p}-gold)" stroke-width=".35"/>`);
  }

  function emblem(x, cx, cy, size) {
    return x.design.emblem === "oak"
      ? O.oakBranch(cx - size / 2, cy - size / 2, size, `url(#${x.p}-gold)`)
      : O.dove(cx - size / 2, cy - size / 2, size, `url(#${x.p}-gold)`);
  }

  // ---------------------------------------------------------------- CARTE 1 · densité intégrale du PAVS
  // Aucun libellé texte : chaque donnée est portée par un pictogramme (légende dans l'application et sur le B.A.T.).
  // Les cases à cocher du formulaire officiel deviennent des matrices de pictogrammes : coché = vif + pastille,
  // non coché = estompé. Un corps de texte UNIQUE pour les deux faces est calculé (la plus grande taille ≤ DATA_MAX
  // où tout tient) : aucune donnée n'est dominante, la photo est une vignette.
  const DATA_MAX = 1.3;
  const DATA_MIN = 0.8;
  const L = 3.4; // zone de sécurité 3 mm + 0,4 mm
  const RR = W - 3.4;
  const has = v => v != null && v !== false && String(v).trim() !== "";
  const person = o => (o ? [o.name, o.phone].filter(has) : []);
  const yn = v => (v === true || v === "Oui" ? "yes" : v === false || v === "Non" ? "no" : v === "X" ? "presumed" : "unset");

  /** Modèle de données de la Carte 1 (toutes les rubriques du formulaire officiel + compléments AeterniTrak). */
  function card1Model(c) {
    const ci = c.civil_identity || {};
    const pr = c.pavs_record || {};
    const med = c.medical_record || {};
    const fw = c.funeral_wills || {};
    const care = pr.care || {};
    const pm = pr.post_mortem_wills || {};
    const ds = pr.desired_support || {};
    const P = R.PAVS;
    const phy = ci.certifying_physician || {};
    const mode = R.burialMode(fw.burial_mode);
    const pyro = R.pyroStatus(c);
    const bio = Number(med.biological_hazard_level) || 0;
    const att = pr.attachments || [];

    const contacts = [
      { name: "Institution(s)", icon: "institution", lines: person(pr.institution) },
      { name: "Médecin traitant", icon: "physician", lines: [phy.name, has(phy.inami) && `INAMI ${phy.inami}`, phy.phone].filter(has) },
      { name: "Personne(s) à contacter", icon: "contact", lines: person(pr.contact_person) },
      { name: "Mandataire (soins de santé)", icon: "proxyHealth", lines: person(pr.health_proxy) },
      { name: "Mandataire extrajudiciaire", icon: "proxyLegal", lines: person(pr.extrajudicial_proxy) },
      { name: "Personne(s) de confiance", icon: "trusted", lines: person(pr.trusted_person) },
      { name: "Administrateur de biens et/ou de la personne", icon: "keyAdmin", lines: person(pr.property_administrator) },
      { name: "Lieu de conservation du PSPA", icon: "archive", lines: has(pr.conservation_place) ? [pr.conservation_place] : [] }
    ];

    const refusals = care.refusals || [];
    const careRows = [
      { name: "Projet global", icon: "gauge", cells: [
        ...P.INTENSITY.map(i => ({ icon: i.icon, state: care.intensity === i.id ? "yes" : "off" })),
        { icon: "careComfort", state: care.comfort ? "yes" : "off" },
        { icon: "euthanasia", state: care.euthanasia_declaration ? "yes" : "off" }
      ] },
      { name: "Thérapies refusées", icon: "ban", cells: P.REFUSALS.map((r, i, a) => ({
        icon: r.icon, state: refusals.includes(r.id) ? "no" : "off", gapBefore: i > 0 && (r.group || a[i - 1].group) && r.group !== a[i - 1].group
      })) },
      { name: "À soins égaux je préfère être", icon: "bed", cells: P.SETTINGS.map(s => ({ icon: s.icon, state: (care.settings || []).includes(s.id) ? "yes" : "off" })) },
      { name: "Types d'hospitalisations acceptés", icon: "hospital", cells: [
        { icon: "reanimation", state: care.reanimation === "avec" ? "yes" : care.reanimation === "sans" ? "no" : "off" },
        { icon: "fracture", state: care.exceptional_hospitalization ? "yes" : "off" }
      ] }
    ];
    const careFlow = [has(pr.comments) && { name: "Commentaires", icon: "bubble", text: pr.comments }].filter(Boolean);

    const versoRows = [
      { name: "Mes souhaits de fin de vie", icon: "bed", cells: [
        { icon: "home", state: yn(pr.eol_at_home) },
        ...P.SUPPORT.map(s => ({ icon: s.icon, state: (ds.choices || []).includes(s.id) ? "yes" : "off", gapBefore: s.id === "PSYCHOLOGIQUE" }))
      ] },
      { name: "Mes volontés pour l'après-décès", icon: "scroll", cells: [
        { icon: "heart", state: ({ 1: "yes", 3: "no", 2: "presumed" })[Number(med.organ_donation_status)] || "unset" },
        { icon: "science", state: yn(pm.body_donation) },
        { icon: (P.DISPOSITION.find(d => d.id === pm.body_disposition) || P.DISPOSITION[2]).icon, state: pm.body_disposition ? (pm.body_disposition === "X" ? "presumed" : "yes") : "unset" },
        { icon: "pacemaker", state: med.has_pacemaker ? (pyro.code === "BLOCK" ? "alert" : "yes") : "no" },
        { icon: "relatives", state: yn(pm.leave_choice_to_relatives) },
        { icon: "insurance", state: yn(fw.has_funeral_insurance) },
        { icon: "paperclip", state: att.length ? "yes" : "off", label: att.length ? String(att.length) : "" }
      ] },
      { name: "Compléments AeterniTrak", icon: "nfc", cells: [
        { icon: mode.icon, state: "yes", label: String(mode.id) },
        med.has_radioisotopes && { icon: "radiation", state: "alert", label: "I-125" },
        bio > 0 && { icon: "biohazard", state: bio >= 3 ? "alert" : "yes", label: `BH${bio}` },
        Number(med.organ_donation_status) === 1 && pm.body_donation === "Oui" && { icon: "medcross", state: "yes", label: "48 h" }
      ].filter(Boolean) }
    ];

    const rites = String(pm.rites || "");
    const inRites = v => has(v) && rites.toLowerCase().includes(String(v).toLowerCase());
    const pmText = [pacemakerText(med)].filter(has).join("");
    const versoFlow = [
      has(ds.special_wishes) && { name: "À propos de mon accompagnement", icon: "star", text: ds.special_wishes },
      has(pr.essential_priority) && { name: "Pour moi, l'essentiel c'est", icon: "quote", text: pr.essential_priority, italic: true },
      has(pr.other_wishes) && { name: "Mes autres souhaits (fin de vie)", icon: "feather", text: pr.other_wishes },
      has(rites) && { name: "Rite(s) / rituel(s)", icon: "rite", text: rites },
      has(fw.chosen_funeral_home) && { name: "Pompes funèbres", icon: "funeralHome", text: fw.chosen_funeral_home },
      has(pm.funeral_insurance_ref) && { name: "Assurance obsèques", icon: "insurance", text: pm.funeral_insurance_ref },
      has(pm.other_wishes) && { name: "Mes autres souhaits (après-décès)", icon: "scroll", text: pm.other_wishes },
      { name: "Mode de sépulture (carte)", icon: mode.icon, text: mode.label + (R.isSarco(mode.id) ? " — démonstrateur prospectif (DEC-AET-15)" : "") },
      has(fw.residue_destination) && !inRites(fw.residue_destination) && { name: "Destination", icon: "pin", text: fw.residue_destination },
      has(fw.ceremony_nature) && !inRites(fw.ceremony_nature) && { name: "Cérémonie", icon: "rite", text: fw.ceremony_nature },
      has(fw.coffin_material) && { name: "Cercueil", icon: "coffin", text: fw.coffin_material },
      has(pmText) && { name: "Stimulateur cardiaque", icon: "pacemaker", text: pmText },
      bio > 0 && { name: "Risque biologique", icon: "biohazard", text: med.biological_hazard_label || `Niveau ${bio}` },
      att.length && { name: "Annexes", icon: "paperclip", text: att.map(a => a.name).join(", ") }
    ].filter(Boolean);

    return { contacts, careRows, careFlow, versoRows, versoFlow, mode, pyro };
  }

  function pacemakerText(med) {
    if (!med.has_pacemaker) return "";
    const ex = med.pacemaker_exeresis;
    return [med.pacemaker_details, ex && ex.certified_removed && `exérèse ${ex.surgeon_name || ""}${ex.surgeon_inami ? " · INAMI " + ex.surgeon_inami : ""}${ex.exeresis_date ? " · " + shortDate(ex.exeresis_date) : ""}`].filter(has).join(" · ");
  }

  /** Texte continu à retrait suspendu (pictogramme en marge), réparti en colonnes. */
  function flowLayout(items, s, fam, colW, h, cols) {
    const lh = s * 1.2;
    const gap = s * 0.3;
    const ind = s * 1.5;
    const lines = [];
    const overflow = [];
    let col = 0;
    let y = 0;
    for (const it of items) {
      const ls = wrap(it.text, colW - ind, s, fam, 999, it.italic ? "italic" : null);
      ls.forEach((t, i) => {
        if (y + lh > h + 1e-6) { col++; y = 0; }
        if (col < cols) lines.push({ col, y, t, first: i === 0, it });
        else if (!overflow.includes(it)) overflow.push(it);
        y += lh;
      });
      y += gap;
    }
    return { fits: overflow.length === 0, lines, lh, ind, overflow };
  }

  const GEO = {
    cell: { w: 19.27, h: 6.15, gap: 0.57, y: 16.25, icon: 2.5 },
    care: { y: 29.75, h: 14.75, matrixW: 47.5 },
    verso: { rowsY: 7.65, flowY: 19.4, flowH: 24.6 }
  };

  function contactFits(cell, s, fam) {
    const w = GEO.cell.w - GEO.cell.icon - 1.1;
    return flowLayout(cell.lines.map(t => ({ text: t })), s, fam, w + s * 1.5, GEO.cell.h - 0.5, 1);
  }

  /** Corps unique : plus grande taille où contacts, commentaires et texte du verso tiennent. */
  function card1Metrics(x) {
    const m = card1Model(x.data);
    const fam = x.dfam;
    const recW = RR - (L + GEO.care.matrixW + 1);
    const colW = (RR - L - 1.6) / 2;
    const maxS = DATA_MAX * (Number(x.design.fontScale) || 1);
    const test = s => m.contacts.every(cl => contactFits(cl, s, fam).fits) &&
      flowLayout(m.careFlow, s, fam, recW, GEO.care.h, 1).fits &&
      flowLayout(m.versoFlow, s, fam, colW, GEO.verso.flowH, 2).fits;
    let s = maxS;
    while (s > DATA_MIN && !test(s)) s = Math.round((s - 0.02) * 1000) / 1000;
    s = Math.max(s, DATA_MIN);
    const overflow = [];
    if (!test(s)) {
      m.contacts.forEach(cl => { if (!contactFits(cl, s, fam).fits) overflow.push(cl.name); });
      flowLayout(m.careFlow, s, fam, recW, GEO.care.h, 1).overflow.forEach(it => overflow.push(it.name));
      flowLayout(m.versoFlow, s, fam, colW, GEO.verso.flowH, 2).overflow.forEach(it => overflow.push(it.name));
    }
    return { m, s, overflow, recW, colW };
  }

  function renderFlow(x, layout, X, Y, colW, colGap, s) {
    let g = "";
    const last = layout.lines[layout.lines.length - 1];
    for (const ln of layout.lines) {
      const x0 = X + ln.col * (colW + colGap);
      if (ln.first && ln.it.icon) g += O.icon(ln.it.icon, x0, Y + ln.y + (layout.lh - s * 1.15) / 2, s * 1.15, x.accent, 0.13);
      const text = !layout.fits && ln === last ? ln.t.replace(/.{0,2}$/, "…") : ln.t;
      g += T(x0 + layout.ind, Y + ln.y + s * 0.93, text, { fam: x.dfam, size: s, fill: x.ink, italic: ln.it.italic });
    }
    return g;
  }

  /** Matrice de pictogrammes : une ligne = une rubrique du formulaire. */
  function renderMatrix(x, rows, X, Y, rowH) {
    let g = "";
    const cs = rowH - 0.35;
    rows.forEach((row, ri) => {
      const y = Y + ri * rowH;
      g += O.icon(row.icon, X, y + (cs - 2.3) / 2, 2.3, x.muted, 0.15);
      g += `<path d="M${f(X + 3)} ${f(y + 0.4)}V${f(y + cs - 0.4)}" stroke="url(#${x.p}-gold)" stroke-width=".1"/>`;
      let cx = X + 3.5;
      row.cells.forEach(cell => {
        if (cell.gapBefore) cx += 0.7;
        const lw = cell.label ? measure(cell.label, 0.95, x.sans, 700) + 0.4 : 0;
        const w = cs + lw;
        const on = cell.state !== "off" && cell.state !== "unset";
        g += `<rect x="${f(cx)}" y="${f(y)}" width="${f(w)}" height="${f(cs)}" rx=".55" fill="${rgba(x.accent, on ? (x.dark ? 0.2 : 0.14) : 0.04)}" stroke="${rgba(x.accent, on ? 0.75 : 0.25)}" stroke-width=".1"/>`;
        g += `<g opacity="${on ? 1 : 0.32}">${O.icon(cell.icon, cx + cs * 0.14, y + cs * 0.12, cs * 0.72, on ? x.ink : x.muted, 0.15)}</g>`;
        if (cell.label) g += T(cx + cs - 0.1, y + cs * 0.68, cell.label, { fam: x.sans, size: 0.95, weight: 700, fill: x.ink });
        if (on) g += O.mark(cx + w - 0.45, y + cs - 0.45, 0.62, cell.state);
        cx += w + 0.38;
      });
    });
    return g;
  }

  // ---------------------------------------------------------------- CARTE 1 · RECTO (données administratives & projet de soins)
  function card1Recto(x) {
    const c = x.data;
    const ci = c.civil_identity || {};
    const pr = c.pavs_record || {};
    const { m, s, recW } = card1Metrics(x);
    let g = background(x) + guilloche(x, [[69, 26, 15]]) + fillets(x);

    g += T(L, 5.55, "AETERNITRAK", { fam: x.title, size: 1.7, weight: 600, fill: `url(#${x.p}-gold)`, ls: 0.25 });
    g += T(L + measure("AETERNITRAK", 1.7, x.title, 600) + 3.2, 5.45, "DERNIÈRES VOLONTÉS · PAVS", { fam: x.sans, size: 0.85, weight: 600, fill: x.muted, ls: 0.14 });
    g += T(RR, 5.45, "ID-1 · NFC ACOSJ 92 Ko", { fam: x.sans, size: 0.8, fill: x.muted, anchor: "end", ls: 0.08 });
    g += goldRule(x, L, RR, 6.85);

    // Identité (vignette : la photo n'est jamais dominante)
    g += portrait(x, { kind: "rect", x: L, y: 7.65, w: 6.3, h: 7.9, r: 0.45 }, "pt");
    const X = L + 7.2;
    const nameS = Math.min(s * 1.45, 2.0);
    const nm = fit(ci.full_name || "Nom Prénom", RR - X, nameS, x.title, 600, s);
    g += T(X, 9.95, nm.text, { fam: x.title, size: nm.size, weight: 600, fill: x.ink, ls: 0.06 });
    const niss = R.validateNiss(ci.national_id_niss, ci.birth_date, ci.gender);
    const rowA = [
      { icon: ci.gender === "F" ? "genderF" : ci.gender === "M" ? "genderM" : "genderX" },
      { icon: "birth", text: [ci.birth_date && shortDate(ci.birth_date), ci.birth_place].filter(has).join(" · ") },
      { icon: "phone", text: ci.phone }
    ];
    const rowB = [
      { icon: "idcard", text: niss.formatted || "—", mono: true, mark: niss.valid ? "yes" : "no" },
      { icon: "calendar", text: pr.registered_date ? shortDate(pr.registered_date) : "" }
    ];
    g += inlineRow(x, rowA, X, 12.5, RR - X, s) + inlineRow(x, rowB, X, 15.0, RR - X, s);

    // Contacts (8 cellules)
    m.contacts.forEach((cl, i) => {
      const cx = L + (i % 4) * (GEO.cell.w + GEO.cell.gap);
      const cy = GEO.cell.y + Math.floor(i / 4) * (GEO.cell.h + GEO.cell.gap);
      const empty = !cl.lines.length;
      g += `<rect x="${f(cx)}" y="${f(cy)}" width="${GEO.cell.w}" height="${GEO.cell.h}" rx=".6" fill="${rgba(x.accent, empty ? 0.03 : x.dark ? 0.13 : 0.08)}" stroke="${rgba(x.accent, empty ? 0.2 : 0.5)}" stroke-width=".1"/>`;
      g += `<g opacity="${empty ? 0.35 : 1}">${O.icon(cl.icon, cx + 0.45, cy + 0.5, GEO.cell.icon, x.accent, 0.15)}</g>`;
      if (empty) {
        g += T(cx + GEO.cell.icon + 1.1, cy + 2.2, "—", { fam: x.dfam, size: s, fill: x.muted });
        return;
      }
      const lay = contactFits(cl, s, x.dfam);
      lay.lines.forEach((ln, k) => {
        const t = !lay.fits && k === lay.lines.length - 1 ? ln.t.replace(/.{0,2}$/, "…") : ln.t;
        g += T(cx + GEO.cell.icon + 1.0, cy + 0.35 + ln.y + s * 0.93, t, { fam: x.dfam, size: s, fill: x.ink, weight: k === 0 ? 500 : 400 });
      });
    });

    // Projet de soins : matrices de cases + commentaires
    g += renderMatrix(x, m.careRows, L, GEO.care.y, GEO.care.h / 4);
    const fx = L + GEO.care.matrixW + 1;
    if (m.careFlow.length) {
      g += renderFlow(x, flowLayout(m.careFlow, s, x.dfam, recW, GEO.care.h, 1), fx, GEO.care.y, recW, 0, s);
    } else {
      g += T(fx, GEO.care.y + 1.5, "", { fam: x.dfam, size: s, fill: x.muted });
    }

    // Bandeau pyrotechnique (sécurité du four) — fin, jamais dominant
    const pyro = m.pyro;
    const danger = pyro.level === "danger";
    const by = 45.15;
    const bh = 3.7;
    g += `<g class="${danger ? "pyro-danger" : "pyro-ok"}"><rect x="${L}" y="${by}" width="${f(RR - L)}" height="${bh}" rx=".8" fill="${danger ? `url(#${x.p}-hatch)` : "#1f6a45"}"/>`;
    g += O.icon(danger ? "alert" : "pacemaker", L + 0.6, by + 0.6, 2.5, "#fff", 0.2);
    const title = pyro.title.toUpperCase();
    const ts = 1.05;
    const tw = measure(title, ts, x.sans, 700);
    g += T(L + 3.8, by + 2.45, title, { fam: x.sans, size: ts, weight: 700, fill: "#fff", ls: 0.04 });
    const det = fit(pyro.detail, RR - L - 4.6 - tw - 1.5, 0.95, x.sans, 400, 0.7);
    g += T(L + 3.8 + tw + 1.5, by + 2.45, det.text, { fam: x.sans, size: det.size, fill: "#fff", opacity: 0.9 });
    g += `</g>`;

    g += T(L, 50.55, "Intégralité du PAVS scellée dans la puce NFC sans contact · JavaCard ACOSJ 92 Ko", { fam: x.sans, size: 0.78, fill: x.muted });
    g += T(RR, 50.55, c.id || "", { fam: x.mono, size: 0.72, fill: x.muted, anchor: "end" });
    return g;
  }

  /** Ligne de données « pictogramme + valeur » ; le dernier élément est tronqué si nécessaire. */
  function inlineRow(x, items, X, y, maxW, s) {
    let g = "";
    let cx = X;
    const is = s * 1.2;
    for (const it of items) {
      if (cx > X + maxW - is) break;
      g += O.icon(it.icon, cx, y - s * 0.95, is, x.accent, 0.13);
      cx += is + 0.45;
      if (has(it.text)) {
        const fam = it.mono ? x.mono : x.dfam;
        const t = fit(it.text, X + maxW - cx - (it.mark ? 1.6 : 0), s, fam, 400, s);
        g += T(cx, y, t.text, { fam, size: s, fill: x.ink });
        cx += measure(t.text, s, fam, 400) + 0.5;
      }
      if (it.mark) { g += O.mark(cx + 0.55, y - s * 0.35, 0.55, it.mark); cx += 1.4; }
      cx += 1.5;
    }
    return g;
  }

  // ---------------------------------------------------------------- CARTE 1 · VERSO (fin de vie, après-décès, compléments)
  function card1Verso(x) {
    const c = x.data;
    const fw = c.funeral_wills || {};
    const mm = c.multimedia_memorial || {};
    const { m, s, colW } = card1Metrics(x);
    let g = background(x) + guilloche(x, [[71.3, 26, 13]]) + fillets(x);

    g += T(L, 5.55, "DERNIÈRES VOLONTÉS", { fam: x.title, size: 1.7, weight: 600, fill: `url(#${x.p}-gold)`, ls: 0.22 });
    g += T(RR, 5.45, "Loi du 20 juillet 1971 sur les funérailles et sépultures", { fam: x.body, size: 0.9, fill: x.muted, anchor: "end", italic: true });
    g += goldRule(x, L, RR, 6.85);

    g += renderMatrix(x, m.versoRows, L, GEO.verso.rowsY, 3.85);

    g += `<path d="M${L} ${f(GEO.verso.flowY - 0.45)}H${RR}" stroke="${rgba(x.accent, 0.35)}" stroke-width=".08"/>`;
    g += renderFlow(x, flowLayout(m.versoFlow, s, x.dfam, colW, GEO.verso.flowH, 2), L, GEO.verso.flowY, colW, 1.6, s);

    // Bande inférieure : multimédia scellé, permis, cible NFC
    g += goldRule(x, L, RR - 6.5, 44.5);
    const ac = mm.audio_choice || {};
    const media = [
      { icon: "camera", text: `${mm.photo_count || 0}` },
      { icon: "mic", text: ac.has_voice_memo ? `${ac.voice_memo_duration_sec || 0} s` : "—" },
      { icon: "music", text: (mm.chosen_music || {}).title || "—" }
    ];
    g += inlineRow(x, media, L, 46.85, RR - L - 7, s);
    const lv = fw.legal_validation || {};
    g += inlineRow(x, [{ icon: "doc", text: lv.permit_number || "—", mono: true }], L, 49.55, RR - L - 7, s * 0.9);
    g += O.nfcTarget(RR - 2.9, 47.4, 2.8, x.accent);
    return g;
  }

  /** Rapport de densité (pour l'interface) : corps retenu et rubriques éventuellement tronquées. */
  function card1Report(data, design) {
    const x = context(1, "recto", data, design, { prefix: "rep" });
    const r = card1Metrics(x);
    return { size: r.s, pt: r.s / 0.3528, overflow: r.overflow };
  }

  /** Légende des pictogrammes de la Carte 1 (application, B.A.T. et prompts). */
  function card1Legend() {
    const P = R.PAVS;
    return [
      { group: "Identité", items: [["genderF", "Femme"], ["genderM", "Homme"], ["birth", "Date et lieu de naissance"], ["phone", "Téléphone"], ["idcard", "Numéro de registre national"], ["calendar", "Date d'enregistrement du PAVS"]] },
      { group: "Contacts", items: [["institution", "Institution(s)"], ["physician", "Médecin traitant"], ["contact", "Personne(s) à contacter"], ["proxyHealth", "Mandataire (soins de santé)"], ["proxyLegal", "Mandataire extrajudiciaire"], ["trusted", "Personne(s) de confiance"], ["keyAdmin", "Administrateur de biens et/ou de la personne"], ["archive", "Lieu de conservation du PSPA"]] },
      { group: "Projet de soins", items: [["gauge", "Projet global (intensité des soins)"], ...P.INTENSITY.map(i => [i.icon, i.label]), ["careComfort", "Soins de confort/palliatifs"], ["euthanasia", "Déclaration anticipée d'euthanasie signée"], ["ban", "Thérapies refusées"], ...P.REFUSALS.map(r => [r.icon, r.label]), ["bed", "À soins égaux je préfère être"], ...P.SETTINGS.map(r => [r.icon, r.label]), ["reanimation", "Hospitalisation avec (✓) ou sans (✕) réanimation"], ["fracture", "Hospitalisation exceptionnelle"], ["bubble", "Commentaires"]] },
      { group: "Fin de vie", items: [["home", "Fin de vie dans mon lieu de vie habituel"], ...P.SUPPORT.map(r => [r.icon, `Accompagnement ${r.label.toLowerCase()}`]), ["star", "À propos de mon accompagnement"], ["quote", "Pour moi, l'essentiel c'est"], ["feather", "Mes autres souhaits (fin de vie)"]] },
      { group: "Après-décès", items: [["heart", "Don d'organes"], ["science", "Don du corps à la science"], ["flame", "Incinéré(e)"], ["stone", "Inhumé(e)"], ["disposition", "Sans préférence"], ["pacemaker", "Pacemaker"], ["relatives", "Choix des obsèques laissé aux proches"], ["insurance", "Assurance obsèques"], ["paperclip", "Annexe(s)"], ["rite", "Rite(s)/rituel(s)"], ["funeralHome", "Pompes funèbres"], ["scroll", "Mes autres souhaits (après-décès)"]] },
      { group: "Compléments AeterniTrak", items: [["pin", "Destination"], ["coffin", "Cercueil"], ["radiation", "Radio-isotopes actifs"], ["biohazard", "Risque biologique"], ["camera", "Photos"], ["mic", "Message vocal"], ["music", "Musique"], ["doc", "Permis d'inhumation / transport"]] },
      { group: "Réponses", marks: [["yes", "Oui / coché"], ["no", "Non / refusé"], ["presumed", "Sans préférence"], ["alert", "Alerte"]] }
    ];
  }

  // ---------------------------------------------------------------- CARTE 2 · RECTO (5 gabarits)
  function memorialText(x, cx, top, maxW, opts) {
    const c = x.data;
    const { s } = x;
    const o = Object.assign({ header: true, quoteLines: 3, nameSize: 3.6 }, opts);
    let g = "";
    let y = top;
    if (o.header) {
      const hf = fit("EN MÉMOIRE ÉTERNELLE DE", maxW, s(1.2), x.sans, 600, s(0.8));
      g += T(cx, y, hf.text, { fam: x.sans, size: hf.size, weight: 600, fill: x.muted, anchor: "middle", ls: 0.32 });
      y += 6.2;
    }
    const nm = (c.civil_identity || {}).full_name || "Nom Prénom";
    const nameLines = wrap(nm, maxW, s(o.nameSize), x.title, 2);
    const ns = nameLines.length > 1 ? s(o.nameSize * 0.82) : fit(nm, maxW, s(o.nameSize), x.title, 600, s(2.2)).size;
    nameLines.forEach((ln, i) => {
      g += T(cx, y + i * ns * 1.15, ln, { fam: x.title, size: ns, weight: 600, fill: x.ink, anchor: "middle", ls: 0.12 });
    });
    y += (nameLines.length - 1) * ns * 1.15 + 5;
    g += T(cx, y, x.design.years ?? (c.multimedia_memorial || {}).lifespan_display ?? "", { fam: x.body, size: s(2.3), weight: 600, fill: `url(#${x.p}-gold)`, anchor: "middle", ls: 0.2 });
    y += 2.6;
    g += goldRule(x, cx - Math.min(12, maxW / 2), cx + Math.min(12, maxW / 2), y);
    y += 3.6;
    const quote = x.design.quote ?? "";
    if (quote) {
      wrap(quote, maxW, s(1.65), x.body, o.quoteLines, "italic").forEach((ln, i) => {
        g += T(cx, y + i * 2.15, ln, { fam: x.body, size: s(1.65), fill: x.ink, anchor: "middle", italic: true, opacity: 0.92 });
      });
    }
    return g;
  }

  function card2Recto(x) {
    const layout = x.design.layout || "A";
    let g = background(x);
    if (layout === "A") {
      g += guilloche(x, [[22, 28, 17]]) + fillets(x);
      g += `<circle cx="22" cy="28" r="15" fill="none" stroke="url(#${x.p}-gold)" stroke-width=".12"/>`;
      g += portrait(x, { kind: "ellipse", cx: 22, cy: 28, rx: 12.6, ry: 12.6 }, "med");
      g += `<circle cx="22" cy="28" r="13.4" fill="none" stroke="url(#${x.p}-gold)" stroke-width=".5"/>`;
      g += emblem(x, 61, 7.5, 6.5);
      g += memorialText(x, 61, 14.6, 39, {});
    } else if (layout === "B") {
      g += guilloche(x, [[23, 27, 14], [64, 27, 14]]) + fillets(x);
      g += `<rect x="${M}" y="${M + 0.5}" width="35" height="${f(H - 2 * M - 1)}" rx="1" fill="${rgba("#000000", x.dark ? 0.25 : 0.06)}" stroke="url(#${x.p}-gold)" stroke-width=".4"/>`;
      g += `<path d="M${M} ${M + 0.5}l1.4 1.4M${M + 35} ${M + 0.5}l-1.4 1.4M${M} ${f(H - M - 0.5)}l1.4 -1.4M${M + 35} ${f(H - M - 0.5)}l-1.4 -1.4" stroke="url(#${x.p}-gold)" stroke-width=".2"/>`;
      g += portrait(x, { kind: "rect", x: M + 1.4, y: M + 1.9, w: 32.2, h: H - 2 * M - 3.8, r: 0.4 }, "dip");
      g += `<path d="M42.7 ${M + 2}V21.5M42.7 32.5V${f(H - M - 2)}" stroke="url(#${x.p}-gold)" stroke-width=".15"/>`;
      g += O.oakBranch(39.4, 23.3, 6.6, `url(#${x.p}-gold)`);
      g += emblem(x, 64, 7.8, 6.2);
      g += memorialText(x, 64, 14.8, 32, { nameSize: 3.2 });
    } else if (layout === "C") {
      g += guilloche(x, [[42.8, 27, 18]]) + fillets(x);
      const arches = [{ x: 5.5, w: 21 }, { x: 31.3, w: 23 }, { x: 59.1, w: 21 }];
      const ay = 11;
      const ah = 31;
      arches.forEach(a => {
        g += `<path d="M${f(a.x)} ${ay + ah}V${f(ay + a.w / 2)}a${f(a.w / 2)} ${f(a.w / 2)} 0 0 1 ${f(a.w)} 0V${ay + ah}" fill="${rgba(x.accent, x.dark ? 0.1 : 0.06)}" stroke="url(#${x.p}-gold)" stroke-width=".3"/>`;
      });
      g += T(42.8, 7.3, "EN MÉMOIRE ÉTERNELLE DE", { fam: x.sans, size: x.s(1.15), weight: 600, fill: x.muted, anchor: "middle", ls: 0.32 });
      g += portrait(x, { kind: "arch", x: 32.5, y: ay + 1.2, w: 20.6, h: ah - 2.4 }, "tri");
      g += emblem(x, 16, 24, 9);
      g += T(16, 35, ((x.design.years ?? (x.data.multimedia_memorial || {}).lifespan_display) || "").replace(/\s*—\s*/, " — "), { fam: x.body, size: x.s(1.7), weight: 600, fill: `url(#${x.p}-gold)`, anchor: "middle" });
      const q = wrap(x.design.quote || "", 17, x.s(1.4), x.body, 6, "italic");
      const qy = 27 - (q.length * 1.8) / 2 + 1.4;
      q.forEach((ln, i) => { g += T(69.6, qy + i * 1.8, ln, { fam: x.body, size: x.s(1.4), fill: x.ink, anchor: "middle", italic: true }); });
      const nm = fit((x.data.civil_identity || {}).full_name || "", 72, x.s(3.1), x.title, 600, x.s(2));
      g += T(42.8, 48.6, nm.text, { fam: x.title, size: nm.size, weight: 600, fill: x.ink, anchor: "middle", ls: 0.15 });
    } else if (layout === "D") {
      g += guilloche(x, [[64, 28, 14]]) + fillets(x);
      const cells = [[M, M + 0.6, 19, 21.6], [M + 20, M + 0.6, 19, 10.3], [M + 20, M + 11.9, 19, 10.3], [M, M + 23.2, 9.2, 21], [M + 10.2, M + 23.2, 28.8, 21]];
      const count = Math.max(1, Number((x.data.multimedia_memorial || {}).photo_count) || 1);
      cells.forEach((cl, i) => {
        const [cx, cy, cw, chh] = cl;
        if (i === 0 || i < count) {
          g += portrait(x, { kind: "rect", x: cx, y: cy, w: cw, h: chh, r: 0.6 }, `mo${i}`);
        } else {
          g += `<rect x="${f(cx)}" y="${f(cy)}" width="${cw}" height="${chh}" rx=".6" fill="${rgba(x.accent, x.dark ? 0.12 : 0.08)}" stroke="url(#${x.p}-gold)" stroke-width=".2"/>`;
          g += O.rosette(cx + cw / 2, cy + chh / 2, Math.min(cw, chh) * 0.32, x.gDensity, x.accent, 0.5);
          if (i === 4) g += emblem(x, cx + cw / 2, cy + chh / 2, Math.min(cw, chh) * 0.45);
        }
      });
      g += emblem(x, 64, 7.8, 6.2);
      g += memorialText(x, 64, 14.8, 32, { nameSize: 3.2 });
    } else {
      // E · Typographie pure : stèle épigraphique
      g += guilloche(x, [[42.8, 30, 20]]) + fillets(x);
      g += `<path d="M14 49V16a28.8 12 0 0 1 57.6 0V49" fill="${rgba(x.accent, x.dark ? 0.08 : 0.05)}" stroke="url(#${x.p}-gold)" stroke-width=".3"/>`;
      g += `<path d="M15.2 49V16.3a27.6 11 0 0 1 55.2 0V49" fill="none" stroke="url(#${x.p}-gold)" stroke-width=".08"/>`;
      g += emblem(x, 42.8, 9.4, 6);
      g += memorialText(x, 42.8, 17.6, 50, { nameSize: 3.8, quoteLines: 3 });
    }
    return g;
  }

  // ---------------------------------------------------------------- CARTE 2 · VERSO
  function card2Verso(x) {
    const c = x.data;
    const mm = c.multimedia_memorial || {};
    const ac = mm.audio_choice || {};
    const { s } = x;
    const right = W - M;
    let g = background(x) + guilloche(x, [[69, 25, 13]]) + fillets(x);

    g += T(M, 7.4, "HOMMAGE SOLENNEL & ACOUSTIQUE", { fam: x.title, size: s(2.15), weight: 600, fill: `url(#${x.p}-gold)`, ls: 0.16 });
    g += T(right, 7.2, "13,56 MHz", { fam: x.mono, size: s(1.2), fill: x.muted, anchor: "end" });
    g += goldRule(x, M, right, 10.1);

    // Onde sonore : 20 barres or dégradées (enveloppe déterministe dérivée du titre)
    const title = (mm.chosen_music || {}).title || "Silence recueilli";
    const preset = R.AMBIENT_PRESETS[ac.ambient_preset] || R.AMBIENT_PRESETS.A_MAJOR_CELESTIAL;
    const hh = hash(title + ac.ambient_preset);
    const bx0 = M + 0.5;
    const bw = 1.55;
    const gap = 0.75;
    const mid = 18.6;
    let bars = "";
    for (let i = 0; i < 20; i++) {
      const env = Math.sin((Math.PI * (i + 0.5)) / 20);
      const jitter = ((hh >> (i % 28)) & 15) / 15;
      const h = 2 + 11 * env * (0.55 + 0.45 * jitter);
      bars += `<rect x="${f(bx0 + i * (bw + gap))}" y="${f(mid - h / 2)}" width="${bw}" height="${f(h)}" rx=".5" fill="url(#${x.p}-goldv)" style="animation-delay:${(i % 10) * 0.09}s"/>`;
    }
    g += `<path d="M${M} ${mid}H${f(bx0 + 20 * (bw + gap))}" stroke="${rgba(x.accent, 0.35)}" stroke-width=".08"/>`;
    g += `<g class="wave-bars">${bars}</g>`;
    const tt = fit(title, 31, s(1.9), x.body, 600, s(1.2), "italic");
    g += T(M, 28.6, tt.text, { fam: x.body, size: tt.size, weight: 600, fill: x.ink, italic: true });
    const kb = pill(M + measure(tt.text, tt.size, x.body, 600, "italic") + 1.5, 26.6, preset.key, "info", "music", x, s(0.95));
    if (M + measure(tt.text, tt.size, x.body, 600, "italic") + 1.5 + kb.w < 52) g += kb.svg;
    else g += pill(M, 29.6, preset.key, "info", "music", x, s(0.95)).svg;

    // Message vocal d'adieu
    const vy = 32.4;
    g += O.icon("mic", M, vy, 3.2, x.accent, 0.2);
    const dur = ac.has_voice_memo ? `${ac.voice_memo_duration_sec || 0} s` : "aucun";
    g += T(M + 4, vy + 1.5, `MESSAGE VOCAL D'ADIEU · ${dur}`, { fam: x.sans, size: s(0.98), weight: 700, fill: x.muted, ls: 0.1 });
    g += T(M + 4, vy + 3.3, `Enregistré le ${shortDate((c.pavs_record || {}).registered_date)}`, { fam: x.sans, size: s(0.95), fill: x.muted });
    const extract = x.design.voiceExtract ?? (c.pavs_record || {}).essential_priority ?? "";
    wrap(extract ? `« ${extract} »` : "", 47, s(1.4), x.body, 2, "italic").forEach((ln, i) => {
      g += T(M, vy + 6.2 + i * 1.8, ln, { fam: x.body, size: s(1.4), fill: x.ink, italic: true });
    });

    // Appel à l'action NFC
    const nx = 68.6;
    g += `<rect x="55.4" y="12.2" width="${f(right - 55.4)}" height="27" rx="1.2" fill="${rgba(x.accent, x.dark ? 0.12 : 0.07)}" stroke="url(#${x.p}-gold)" stroke-width=".18"/>`;
    g += O.nfcTarget(nx, 21.4, 6.6, x.accent);
    g += T(nx, 31.2, "Approchez votre", { fam: x.body, size: s(1.55), weight: 600, fill: x.ink, anchor: "middle" });
    g += T(nx, 33.3, "smartphone", { fam: x.body, size: s(1.55), weight: 600, fill: x.ink, anchor: "middle" });
    const latW = pill(0, 0, "38 ms", "ok", "bolt", x, s(0.95)).w;
    g += pill(nx - latW / 2, 35.0, "38 ms", "ok", "bolt", x, s(0.95)).svg;

    // Numérotation d'audience & empreinte
    g += goldRule(x, M, right, 44.4);
    const total = mm.audience_cards_count || 50;
    const ex = Math.min(Number(x.design.exemplaire) || 1, total);
    g += T(M, 47.6, `Tirage d'audience : Exemplaire n° ${ex} sur ${total}`, { fam: x.body, size: s(1.55), weight: 600, fill: x.ink });
    const fp = x.design.fingerprint || "";
    const fpShort = fp ? fp.slice(0, 32).replace(/(.{4})/g, "$1 ").trim() + " …" : "calcul en cours…";
    g += T(M, 50.9, `SHA-256 · ${fpShort}`, { fam: x.mono, size: s(0.92), fill: x.muted });
    g += T(right, 50.9, "COSE_Sign1 · ES256", { fam: x.mono, size: s(0.92), fill: x.muted, anchor: "end" });
    return g;
  }

  // ---------------------------------------------------------------- habillage d'impression
  function printMarks(opts) {
    let g = "";
    if (opts.safe) {
      g += `<rect x="3" y="3" width="${f(W - 6)}" height="${f(H - 6)}" rx="${f(CORNER - 1)}" fill="none" stroke="#00a3d9" stroke-width=".12" stroke-dasharray=".8 .5"/>`;
    }
    if (opts.crop) {
      const k = "#000";
      const L = 5;
      const off = 2.5;
      const lines = [];
      for (const [cx, sx] of [[0, -1], [W, 1]]) {
        for (const [cy, sy] of [[0, -1], [H, 1]]) {
          lines.push(`M${f(cx + sx * off)} ${f(cy)}h${f(sx * L)}`, `M${f(cx)} ${f(cy + sy * off)}v${f(sy * L)}`);
        }
      }
      g += `<path d="${lines.join("")}" stroke="${k}" stroke-width=".1"/>`;
      // Repères de centrage
      const reg = (cx, cy) => `<circle cx="${f(cx)}" cy="${f(cy)}" r="1" fill="none" stroke="${k}" stroke-width=".1"/><path d="M${f(cx - 1.8)} ${f(cy)}h3.6M${f(cx)} ${f(cy - 1.8)}v3.6" stroke="${k}" stroke-width=".1"/>`;
      g += reg(W / 2, -5) + reg(W / 2, H + 5) + reg(-5, H / 2) + reg(W + 5, H / 2);
      g += `<rect x="0" y="0" width="${W}" height="${H}" rx="${CORNER}" fill="none" stroke="#e5007e" stroke-width=".08"/>`;
    }
    return g;
  }

  const RENDERERS = { "1recto": card1Recto, "1verso": card1Verso, "2recto": card2Recto, "2verso": card2Verso };

  function render(card, side, data, design, opts) {
    opts = opts || {};
    const x = context(card, side, data, design, opts);
    const body = RENDERERS[`${card}${side}`](x);
    const m = opts.crop ? 9 : 0;
    const vb = `${-m} ${-m} ${f(W + 2 * m)} ${f(H + 2 * m)}`;
    const size = opts.print || opts.export ? ` width="${f(W + 2 * m)}mm" height="${f(H + 2 * m)}mm"` : "";
    const clipped = opts.crop ? body : `<g clip-path="url(#${x.p}-trim)">${body}</g>`;
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb}"${size} class="card-svg" role="img" aria-label="Carte ${card} — ${side}">` +
      `<title>AeterniTrak · Carte ${card} · ${side}</title>${defs(x)}${clipped}${printMarks(opts)}</svg>`;
  }

  root.PaxCards = { render, FONTS, MATERIALS, W, H, longDate, shortDate, card1Report, card1Legend };
})(typeof self !== "undefined" ? self : this);
