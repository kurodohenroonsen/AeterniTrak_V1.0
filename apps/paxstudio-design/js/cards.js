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

  const TONES = { danger: "#a61d1d", warn: "#a86b12", ok: "#1f6a45", info: "#2b5f9e", muted: "#6b6b6b", accent: "#966f27" };

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

  function guilloche(x, rosettes, isVerso) {
    const c = x.dark ? x.accentLight : x.accent;
    const opFactor = isVerso ? 0.35 : 1.0;
    let g = O.guillocheWaves(0, 0, W, H, x.gDensity, c, x.gOpacity * 0.55 * opFactor);
    for (const r of rosettes) g += O.rosette(r[0], r[1], r[2], x.gDensity, c, x.gOpacity * opFactor);
    return `<g class="guilloche">${g}</g>`;
  }

  function fillets(x) {
    return `<rect x="2.0" y="2.0" width="${f(W - 4.0)}" height="${f(H - 4.0)}" rx="2.2" fill="none" stroke="url(#${x.p}-gold)" stroke-width=".26"/>
      <rect x="2.5" y="2.5" width="${f(W - 5.0)}" height="${f(H - 5.0)}" rx="1.8" fill="none" stroke="url(#${x.p}-gold)" stroke-width=".08"/>`;
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

  // ---------------------------------------------------------------- CARTE 1 · LISIBILITÉ & BALANCEMENT INTÉGRAL DU PAVS
  // Recto : Identité civile, contacts d'urgence qualifiés (sans tirets vides), directives de soins
  // et thérapies refusées sous forme de badges explicites à fort contraste avec libellés en français.
  // Verso : Deux colonnes équilibrées exploitant 100 % de la surface ID-1 :
  // - Colonne 1 : Volontés funéraires, sépulture (Loi 1971), dons légaux et dispositions corporelles.
  // - Colonne 2 : Souhaits de fin de vie, cartouche d'honneur « Parole essentielle » et mémorial acoustique.
  const DATA_MAX = 1.3;
  const DATA_MIN = 0.8;
  const L = 3.4; // marge de sécurité 3 mm + 0,4 mm
  const RR = W - 3.4;
  const has = v => v != null && v !== false && String(v).trim() !== "";
  const person = o => (o ? [o.name, o.phone].filter(has) : []);

  function badgePill(xx, y, label, tone, iconName, x, fs) {
    const is = fs * 1.3;
    const tw = measure(label, fs, x.sans, 600);
    const w = tw + (iconName ? is + 2.2 : 2.0);
    const h = fs * 2.1;
    const col = TONES[tone] || TONES.muted;
    const isFilled = tone === "danger" || tone === "ok" || tone === "warn";
    const bg = isFilled ? col : rgba(x.accent, x.dark ? 0.22 : 0.12);
    const stroke = isFilled ? col : rgba(x.accent, 0.6);
    const textCol = isFilled ? "#fff" : x.ink;
    const iconCol = isFilled ? "#fff" : (TONES[tone] || x.accent);

    return {
      w, h,
      svg: `<g><rect x="${f(xx)}" y="${f(y)}" width="${f(w)}" height="${f(h)}" rx="${f(h / 2)}" fill="${bg}" stroke="${stroke}" stroke-width=".1"/>` +
        (iconName ? O.icon(iconName, xx + 0.9, y + (h - is) / 2, is, iconCol, 0.16) : "") +
        T(xx + (iconName ? is + 1.6 : 1.0), y + h * 0.72, label, { fam: x.sans, size: fs, weight: 600, fill: textCol }) + `</g>`
    };
  }

  function pacemakerText(med) {
    if (!med.has_pacemaker) return "Aucun stimulateur";
    const ex = med.pacemaker_exeresis;
    return [med.pacemaker_details, ex && ex.certified_removed && `exérèse ${ex.surgeon_name || ""}${ex.surgeon_inami ? " · INAMI " + ex.surgeon_inami : ""}${ex.exeresis_date ? " · " + shortDate(ex.exeresis_date) : ""}`].filter(has).join(" · ") || "Présent · non extrait";
  }

  /** Modèle de données enrichi et structuré de la Carte 1 */
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
    const mm = c.multimedia_memorial || {};
    const ac = mm.audio_choice || {};
    const lv = fw.legal_validation || {};

    const allContacts = [
      { name: "Institution(s)", icon: "institution", label: "Institution", lines: person(pr.institution) },
      { name: "Médecin traitant", icon: "physician", label: "Médecin traitant", lines: [phy.name, has(phy.inami) && `INAMI ${phy.inami}`, phy.phone].filter(has) },
      { name: "Personne(s) à contacter", icon: "contact", label: "Contact urgence", lines: person(pr.contact_person) },
      { name: "Mandataire (soins de santé)", icon: "proxyHealth", label: "Mandataire santé", lines: person(pr.health_proxy) },
      { name: "Mandataire extrajudiciaire", icon: "proxyLegal", label: "Mandataire extraj.", lines: person(pr.extrajudicial_proxy) },
      { name: "Personne(s) de confiance", icon: "trusted", label: "Pers. de confiance", lines: person(pr.trusted_person) },
      { name: "Administrateur de biens et/ou de la personne", icon: "keyAdmin", label: "Administrateur", lines: person(pr.property_administrator) },
      { name: "Lieu de conservation du PSPA", icon: "archive", label: "Conservation PSPA", lines: has(pr.conservation_place) ? [pr.conservation_place] : [] }
    ];
    const contacts = allContacts.filter(cl => cl.lines.length > 0);

    // Directives médicales (badges explicites pour le Recto)
    const carePills = [];
    if (bio >= 3) {
      carePills.push({ text: "Alerte Prion · Biohazard 3", tone: "danger", icon: "biohazard" });
    } else if (bio === 2) {
      carePills.push({ text: "Risque bio 2 · Cercueil zingué", tone: "warn", icon: "biohazard" });
    } else if (med.has_radioisotopes) {
      carePills.push({ text: "Radio-isotopes actifs (I-125)", tone: "warn", icon: "radiation" });
    }

    if (care.comfort) {
      carePills.push({ text: "Soins confort / palliatifs", tone: "ok", icon: "careComfort" });
    } else {
      if (care.intensity === "max") carePills.push({ text: "Soins maximums", tone: "info", icon: "careMax" });
      else if (care.intensity === "usual") carePills.push({ text: "Soins usuels", tone: "info", icon: "careUsual" });
    }
    if (care.euthanasia_declaration) carePills.push({ text: "Déclaration euthanasie", tone: "accent", icon: "euthanasia" });

    (care.settings || []).forEach(s => {
      if (s === "DOMICILE") carePills.push({ text: "Maintien domicile", tone: "info", icon: "home" });
      else if (s === "INSTITUTION") carePills.push({ text: "Institution", tone: "info", icon: "institution" });
      else if (s === "HOPITAL") carePills.push({ text: "Hôpital", tone: "info", icon: "hospital" });
      else if (s === "USP") carePills.push({ text: "Soins palliatifs (USP)", tone: "info", icon: "palliativeUnit" });
    });

    if (care.reanimation === "avec") carePills.push({ text: "Hospit. avec réanimation", tone: "info", icon: "reanimation" });
    else if (care.reanimation === "sans") carePills.push({ text: "Hospit. SANS réanimation", tone: "danger", icon: "ban" });
    if (care.exceptional_hospitalization) carePills.push({ text: "Hospit. except. (fracture)", tone: "warn", icon: "fracture" });

    const refusals = care.refusals || [];
    const REFUSAL_MAP = {
      ANTIBIOTHERAPIE: { text: "Refus antibiothérapie", icon: "antibiotic" },
      PERFUSION_HYDRATANTE: { text: "Refus perf. hydratante", icon: "hydration" },
      ALIM_ENTERALE: { text: "Refus sonde entérale", icon: "tubeNose" },
      ALIM_PARENTERALE: { text: "Refus alim. parentérale", icon: "ivDrip" },
      ALIM_GASTROSTOMIE: { text: "Refus sonde gastrostomie", icon: "gastro" },
      DIALYSE: { text: "Refus dialyse", icon: "dialysis" },
      OXYGENOTHERAPIE: { text: "Refus oxygénothérapie", icon: "oxygen" },
      VNI: { text: "Refus ventilation VNI", icon: "mask" },
      INTUBATION: { text: "Refus intubation", icon: "intubation" },
      SEDATION_PALLIATIVE: { text: "Refus sédation palliative", icon: "sedation" },
      ALTERATION_CONSCIENCE: { text: "Refus altération conscience", icon: "consciousness" }
    };
    if (refusals.length === 0) {
      carePills.push({ text: "Aucun refus de thérapie", tone: "ok", icon: "check" });
    } else {
      refusals.forEach(id => {
        const def = REFUSAL_MAP[id] || { text: `Refus ${id}`, icon: "ban" };
        carePills.push({ text: def.text, tone: "danger", icon: def.icon });
      });
    }

    // Verso Colonne 1 : Volontés funéraires, sépulture et dispositions légales
    const col1 = [];
    col1.push({ name: "Sépulture", icon: mode.icon, text: `${mode.label} (Mode ${mode.id})` + (R.isSarco(mode.id) ? " · Protocole prospectif encadré" : "") });
    if (has(fw.residue_destination)) col1.push({ name: "Destination", icon: "pin", text: `Destination : ${fw.residue_destination}` });
    if (has(fw.coffin_material)) col1.push({ name: "Cercueil", icon: "coffin", text: `Cercueil : ${fw.coffin_material}` });
    const ritesText = fw.ceremony_nature || pm.rites;
    if (has(ritesText)) col1.push({ name: "Cérémonie", icon: "rite", text: `Cérémonie & rites : ${ritesText}` });
    if (has(fw.chosen_funeral_home)) col1.push({ name: "Pompes funèbres", icon: "funeralHome", text: `Pompes funèbres : ${fw.chosen_funeral_home}` });
    if (fw.has_funeral_insurance || has(pm.funeral_insurance_ref)) {
      col1.push({ name: "Assurance", icon: "insurance", text: `Assurance obsèques : ${pm.funeral_insurance_ref || (fw.has_funeral_insurance ? "Contrat souscrit" : "Non")}` });
    }
    const organStatus = Number(med.organ_donation_status);
    const organText = organStatus === 1 ? "Don d'organes : Favorable (Loi 1986)" : organStatus === 3 ? "Don d'organes : Refus formel" : "Don d'organes : Sans opposition enregistrée";
    col1.push({ name: "Don d'organes", icon: organStatus === 3 ? "ban" : "heart", text: organText });
    const scienceText = (pm.body_donation === "Oui" || R.burialMode(fw.burial_mode).family === "science") ? "Corps à la science : Oui (Transfert 48 h)" : "Corps à la science : Non";
    col1.push({ name: "Corps à la science", icon: "science", text: scienceText });
    col1.push({ name: "Stimulateur", icon: "pacemaker", text: `Stimulateur : ${pacemakerText(med)}` });
    if (bio > 0) col1.push({ name: "Risque bio", icon: "biohazard", text: med.biological_hazard_label || `Risque biologique : Niveau ${bio}` });
    if (med.has_radioisotopes) col1.push({ name: "Radio-isotopes", icon: "radiation", text: "Radio-isotopes actifs (I-125)" });

    // Verso Colonne 2 : Souhaits de fin de vie, cartouche d'honneur et mémorial
    const col2 = [];
    const eolPlace = pr.eol_at_home === "Oui" ? "Lieu de vie habituel (domicile)" : pr.eol_at_home === "Non" ? "Établissement de soins" : "Sans préférence";
    col2.push({ name: "Fin de vie", icon: "home", text: `Fin de vie : ${eolPlace}` });
    if ((ds.choices || []).length) {
      const supp = ds.choices.map(c => (P.SUPPORT.find(s => s.id === c) || {}).label || c).join(" · ");
      col2.push({ name: "Accompagnement", icon: "lotus", text: `Accompagnement : ${supp}` });
    }
    if (has(ds.special_wishes)) col2.push({ name: "Souhaits accompagnement", icon: "star", text: `Souhaits : ${ds.special_wishes}` });
    if (has(pr.other_wishes)) col2.push({ name: "Autres souhaits fin de vie", icon: "feather", text: `Autres souhaits : ${pr.other_wishes}` });

    // Cartouche d'Honneur : Parole Essentielle
    const essential = pr.essential_priority;

    // Multimédia & Hommage
    const musicTitle = (mm.chosen_music || {}).title;
    col2.push({ name: "Musique", icon: "music", text: `Musique : ${musicTitle || "Silence recueilli"}` });
    if (ac.has_voice_memo) col2.push({ name: "Mémo vocal", icon: "mic", text: `Mémo vocal : ${ac.voice_memo_duration_sec || 0} s d'adieu scellées` });
    col2.push({ name: "Album photo", icon: "camera", text: `Album mémoriel : ${mm.photo_count || 0} cliché(s) scellé(s)` });
    if (att.length) col2.push({ name: "Annexes", icon: "paperclip", text: `Annexes PSPA : ${att.length} document(s)` });
    if (pm.leave_choice_to_relatives === "Oui") col2.push({ name: "Choix obsèques", icon: "relatives", text: "Obsèques : Choix laissé aux proches" });
    if (has(pm.other_wishes)) col2.push({ name: "Autres volontés après-décès", icon: "scroll", text: `Autres volontés : ${pm.other_wishes}` });

    return { contacts, allContacts, carePills, comments: pr.comments, col1, col2, essential, mode, pyro, bio, att, lv, ci, pr, med, fw, mm, ac };
  }

  function card1Metrics(x) {
    const m = card1Model(x.data);
    const maxS = DATA_MAX * (Number(x.design?.fontScale) || 1);
    const minS = DATA_MIN;
    const colW = (RR - L - 1.6) / 2;
    const ind = 2.8;

    const test = s => {
      const lh = s * 1.22;
      // Recto
      const contactRows = Math.ceil(m.contacts.length / 2);
      const cH = m.contacts.length <= 2 ? 4.4 : m.contacts.length <= 4 ? 3.8 : 3.2;
      const contactH = contactRows * (cH + 0.4);
      let pillX = 0;
      let pillRows = 1;
      const pillW_base = RR - L;
      for (const p of m.carePills) {
        const pw = measure(p.text, s * 0.88, x.sans, 600) + s * 0.88 * 1.3 + 2.2;
        if (pillX + pw > pillW_base && pillX > 0) {
          pillRows++;
          pillX = pw + 1.2;
        } else {
          pillX += pw + 1.2;
        }
      }
      const pillsH = pillRows * (s * 2.05 + 0.8);
      let commentsH = 0;
      if (has(m.comments)) {
        const lines = wrap(`« ${m.comments} »`, pillW_base - 3.5, s * 0.9, 2);
        commentsH = lines.length * (s * 1.15) + 2.0;
      }
      const totalRectoH = contactH + pillsH + commentsH + 3.0;
      if (totalRectoH > 28.5) return false;

      // Verso Col 1
      let h1 = 0;
      for (const it of m.col1) {
        const lines = wrap(it.text, colW - ind, s, 3);
        h1 += lines.length * lh + s * 0.35;
      }
      if (h1 > 36.35) return false;

      // Verso Col 2
      let h2 = 0;
      for (const it of m.col2) {
        const lines = wrap(it.text, colW - ind, s, 2);
        h2 += lines.length * lh + s * 0.35;
      }
      if (has(m.essential)) {
        const qLines = wrap(`« ${m.essential} »`, colW - 4.5, s * 0.98, 4);
        h2 += qLines.length * (lh * 1.05) + 4.8;
      }
      if (h2 > 36.35) return false;

      return true;
    };

    let s = maxS;
    while (s > minS && !test(s)) s = Math.round((s - 0.02) * 1000) / 1000;
    s = Math.max(s, minS);
    const overflow = [];
    if (!test(s)) {
      overflow.push("Contenu saturé");
    }
    return { m, s, overflow, colW };
  }

  // ---------------------------------------------------------------- CARTE 1 · RECTO
  function card1Recto(x) {
    const c = x.data;
    const ci = c.civil_identity || {};
    const pr = c.pavs_record || {};
    const { m, s } = card1Metrics(x);
    let g = background(x) + guilloche(x, [[42.8, 27, 16]]) + fillets(x);

    // En-tête solennel
    g += T(L, 5.55, "AETERNITRAK", { fam: x.title, size: 1.65, weight: 600, fill: `url(#${x.p}-gold)`, ls: 0.22 });
    g += T(26.0, 5.45, "DERNIÈRES VOLONTÉS · SOINS ANTICIPÉS", { fam: x.sans, size: 0.82, weight: 600, fill: x.muted, ls: 0.08 });
    g += T(RR, 5.45, "ID-1 · NFC ACOSJ 92 Ko", { fam: x.sans, size: 0.8, fill: x.muted, anchor: "end", ls: 0.08 });
    g += goldRule(x, L, RR, 6.85);

    // Identité (vignette photo ou camée vectoriel)
    const cameoShape = `<rect x="${L}" y="7.65" width="6.3" height="7.9" rx=".45"/>`;
    g += `<clipPath id="${x.p}-pt">${cameoShape}</clipPath><g clip-path="url(#${x.p}-pt)">` +
      `<rect x="${L}" y="7.65" width="6.3" height="7.9" fill="${rgba(x.accent, x.dark ? 0.35 : 0.12)}"/>` +
      O.spiro(L + 3.15, 11.6, 7, 4, 3.2, 0.24, x.accent, 0.35) +
      O.cameo(L + 3.15, 11.6, 2.3, 3.2, `url(#${x.p}-goldv)`, "none") + `</g>` +
      cameoShape.replace("/>", ` fill="none" stroke="url(#${x.p}-gold)" stroke-width=".35"/>`);

    const X = L + 7.5;
    const nameS = Math.min(s * 1.45, 2.0);
    const nm = fit(ci.full_name || "Nom Prénom", RR - X - 22, nameS, x.title, 600, s);
    g += T(X, 9.95, nm.text, { fam: x.title, size: nm.size, weight: 600, fill: x.ink, ls: 0.06 });

    const niss = R.validateNiss(ci.national_id_niss, ci.birth_date, ci.gender);
    const modPill = badgePill(RR - 20, 7.8, niss.valid ? "✓ MODULO 97" : "✗ INVALIDE", niss.valid ? "ok" : "danger", null, x, 0.82);
    g += modPill.svg;

    // Ligne identité 2
    const gIcon = ci.gender === "F" ? "genderF" : ci.gender === "M" ? "genderM" : "genderX";
    let curX = X;
    g += O.icon(gIcon, curX, 11.3, 2.0, x.accent, 0.15);
    curX += 2.6;
    const birthStr = [ci.birth_date && shortDate(ci.birth_date), ci.birth_place].filter(has).join(" · ");
    if (birthStr) {
      g += O.icon("birth", curX, 11.3, 2.0, x.accent, 0.15);
      curX += 2.5;
      g += T(curX, 12.7, birthStr, { fam: x.dfam, size: s * 0.95, fill: x.ink });
      curX += measure(birthStr, s * 0.95, x.dfam, 400) + 3.0;
    }
    if (ci.phone) {
      g += O.icon("phone", curX, 11.3, 2.0, x.accent, 0.15);
      curX += 2.5;
      g += T(curX, 12.7, ci.phone, { fam: x.dfam, size: s * 0.95, fill: x.ink });
    }

    // Ligne identité 3
    curX = X;
    g += O.icon("idcard", curX, 13.6, 2.0, x.accent, 0.15);
    curX += 2.5;
    g += T(curX, 15.0, niss.formatted || "—", { fam: x.mono, size: s * 0.95, fill: x.ink });
    curX += measure(niss.formatted || "—", s * 0.95, x.mono, 400) + 3.5;
    if (pr.registered_date) {
      g += O.icon("calendar", curX, 13.6, 2.0, x.accent, 0.15);
      curX += 2.5;
      g += T(curX, 15.0, `Enregistré le ${shortDate(pr.registered_date)}`, { fam: x.dfam, size: s * 0.9, fill: x.muted });
    }

    // Filet séparateur
    g += `<path d="M${L} 16.0H${RR}" stroke="${rgba(x.accent, 0.35)}" stroke-width=".08"/>`;

    // Contacts d'urgence qualifiés (grille adaptative sans tirets vides)
    const contactColW = (RR - L - 1.6) / 2;
    const contactRows = Math.ceil(m.contacts.length / 2);
    const cH = m.contacts.length <= 2 ? 4.4 : m.contacts.length <= 4 ? 3.8 : 3.2;
    const contactH = contactRows * (cH + 0.4);

    m.contacts.forEach((cl, i) => {
      const col = i % 2;
      const row = Math.floor(i / 2);
      const cx = L + col * (contactColW + 1.6);
      const cy = 16.5 + row * (cH + 0.4);
      g += `<rect x="${f(cx)}" y="${f(cy)}" width="${f(contactColW)}" height="${f(cH)}" rx=".6" fill="${rgba(x.accent, x.dark ? 0.12 : 0.06)}" stroke="${rgba(x.accent, 0.35)}" stroke-width=".1"/>`;
      g += O.icon(cl.icon, cx + 0.6, cy + (cH - 2.0) / 2, 2.0, x.accent, 0.15);

      const txtX = cx + 3.1;
      const line1 = cl.label;
      const line2 = cl.lines.join(" · ");
      const fitLine2 = fit(line2, contactColW - 3.8, s * 0.88, x.dfam, 400, 0.7);

      g += T(txtX, cy + cH * 0.45, line1, { fam: x.sans, size: s * 0.85, weight: 700, fill: x.accent });
      g += T(txtX, cy + cH * 0.85, fitLine2.text, { fam: x.dfam, size: fitLine2.size, fill: x.ink });
    });

    // Directives médicales & Thérapies refusées
    const secY = 16.5 + contactH + 0.6;
    g += `<path d="M${L} ${f(secY)}H${RR}" stroke="${rgba(x.accent, 0.35)}" stroke-width=".08"/>`;
    g += T(L, secY + 2.1, "DIRECTIVES MÉDICALES & THÉRAPIES REFUSÉES", { fam: x.sans, size: 0.8, weight: 700, fill: x.accent, ls: 0.1 });

    let pX = L;
    let pY = secY + 3.2;
    const pillH = s * 2.05;
    const maxW = RR;

    for (const p of m.carePills) {
      const b = badgePill(pX, pY, p.text, p.tone, p.icon, x, s * 0.88);
      if (pX + b.w > maxW && pX > L) {
        pX = L;
        pY += pillH + 0.8;
        const b2 = badgePill(pX, pY, p.text, p.tone, p.icon, x, s * 0.88);
        g += b2.svg;
        pX += b2.w + 1.2;
      } else {
        g += b.svg;
        pX += b.w + 1.2;
      }
    }

    // Commentaires éventuels
    if (has(m.comments)) {
      const cY = pY + pillH + 1.4;
      g += O.icon("bubble", L, cY - 0.4, 2.0, x.accent, 0.15);
      const cLines = wrap(`« ${m.comments} »`, RR - L - 3.5, s * 0.9, 2);
      cLines.forEach((ln, li) => {
        g += T(L + 3.2, cY + 1.0 + li * s * 1.15, ln, { fam: x.dfam, size: s * 0.9, fill: x.ink, italic: true });
      });
    }

    // Bandeau pyrotechnique (sécurité crématoire)
    const pyro = m.pyro;
    const danger = pyro.level === "danger";
    const by = 44.85;
    const bh = 4.15;
    g += `<g class="${danger ? "pyro-danger" : "pyro-ok"}"><rect x="${L}" y="${by}" width="${f(RR - L)}" height="${bh}" rx=".8" fill="${danger ? `url(#${x.p}-hatch)` : "#1f6a45"}"/>`;
    g += O.icon(danger ? "alert" : "pacemaker", L + 0.8, by + (bh - 2.5) / 2, 2.5, "#fff", 0.2);
    const title = pyro.title.toUpperCase();
    const det = fit(pyro.detail, RR - L - 5.5, 0.84, x.sans, 400, 0.72);
    g += T(L + 4.0, by + 1.85, title, { fam: x.sans, size: 0.95, weight: 700, fill: "#fff", ls: 0.04 });
    g += T(L + 4.0, by + 3.42, det.text, { fam: x.sans, size: det.size, fill: "#fff", opacity: 0.92 });
    g += `</g>`;

    g += T(L, 50.55, "Intégralité du PAVS scellée dans la puce NFC sans contact · JavaCard ACOSJ 92 Ko", { fam: x.sans, size: 0.78, fill: x.muted });
    g += T(RR, 50.55, c.id || "", { fam: x.mono, size: 0.72, fill: x.muted, anchor: "end" });
    return g;
  }

  // ---------------------------------------------------------------- CARTE 1 · VERSO
  function card1Verso(x) {
    const c = x.data;
    const fw = c.funeral_wills || {};
    const { m, s, colW } = card1Metrics(x);
    const ind = 2.8;
    const lh = s * 1.22;

    let g = background(x) + guilloche(x, [[42.8, 26, 17]], true) + fillets(x);

    // En-tête
    g += T(L, 5.55, "DERNIÈRES VOLONTÉS & DISPOSITIONS LÉGALES", { fam: x.title, size: 1.6, weight: 600, fill: `url(#${x.p}-gold)`, ls: 0.2 });
    g += T(RR, 5.45, "Loi du 20 juillet 1971 · Funérailles & Sépultures", { fam: x.body, size: 0.85, fill: x.muted, anchor: "end", italic: true });
    g += goldRule(x, L, RR, 6.85);

    // Filet séparateur vertical entre les deux colonnes
    g += `<path d="M42.75 8.2V43.5" stroke="url(#${x.p}-gold)" stroke-width=".12" stroke-dasharray="1.2 .6"/>`;

    // Colonne 1 (Gauche : Volontés Funéraires & Sépulture)
    const col1X = L;
    g += T(col1X, 8.8, "VOLONTÉS FUNÉRAIRES & SÉPULTURE", { fam: x.sans, size: 0.76, weight: 700, fill: x.accent, ls: 0.1 });

    let y1 = 10.2;
    for (const it of m.col1) {
      if (y1 > 43.5) break;
      g += O.icon(it.icon, col1X, y1, 1.8, x.accent, 0.15);
      const lines = wrap(it.text, colW - ind, s, 3);
      lines.forEach((ln, li) => {
        g += T(col1X + ind, y1 + 1.2 + li * lh, ln, { fam: x.dfam, size: s, fill: x.ink, weight: li === 0 && it.name === "Sépulture" ? 600 : 400 });
      });
      y1 += lines.length * lh + s * 0.35;
    }

    // Colonne 2 (Droite : Fin de vie, Parole essentielle & Mémorial)
    const col2X = 44.0;
    g += T(col2X, 8.8, "FIN DE VIE, PAROLE & MÉMORIAL", { fam: x.sans, size: 0.76, weight: 700, fill: x.accent, ls: 0.1 });

    let y2 = 10.2;
    for (const it of m.col2.slice(0, 3)) {
      if (y2 > 43.5) break;
      g += O.icon(it.icon, col2X, y2, 1.8, x.accent, 0.15);
      const lines = wrap(it.text, colW - ind, s, 2);
      lines.forEach((ln, li) => {
        g += T(col2X + ind, y2 + 1.2 + li * lh, ln, { fam: x.dfam, size: s, fill: x.ink });
      });
      y2 += lines.length * lh + s * 0.35;
    }

    // Cartouche d'Honneur : Parole Essentielle
    if (has(m.essential)) {
      const qLines = wrap(`« ${m.essential} »`, colW - 4.5, s * 0.98, 4);
      const cartH = qLines.length * (lh * 1.05) + 4.8;
      g += `<rect x="${f(col2X)}" y="${f(y2)}" width="${f(colW)}" height="${f(cartH)}" rx="1.0" fill="${rgba(x.accent, x.dark ? 0.14 : 0.08)}" stroke="url(#${x.p}-gold)" stroke-width=".2"/>`;
      g += `<rect x="${f(col2X + 0.45)}" y="${f(y2 + 0.45)}" width="${f(colW - 0.9)}" height="${f(cartH - 0.9)}" rx="0.6" fill="none" stroke="url(#${x.p}-gold)" stroke-width=".07" opacity=".65"/>`;
      g += T(col2X + colW / 2, y2 + 2.0, "✦ PAROLE ESSENTIELLE ✦", { fam: x.title, size: 0.76, weight: 600, fill: x.accent, anchor: "middle", ls: 0.16 });
      qLines.forEach((ln, li) => {
        g += T(col2X + colW / 2, y2 + 3.8 + li * (lh * 1.05), ln, { fam: x.body, size: s * 0.98, fill: x.ink, anchor: "middle", italic: true });
      });
      y2 += cartH + 1.2;
    }

    // Multimédia & compléments
    for (const it of m.col2.slice(3)) {
      if (y2 > 43.5) break;
      g += O.icon(it.icon, col2X, y2, 1.8, x.accent, 0.15);
      const lines = wrap(it.text, colW - ind, s, 2);
      lines.forEach((ln, li) => {
        g += T(col2X + ind, y2 + 1.2 + li * lh, ln, { fam: x.dfam, size: s, fill: x.ink });
      });
      y2 += lines.length * lh + s * 0.35;
    }

    // Filet et bande inférieure : Permis légal et cible NFC
    g += goldRule(x, L, RR - 6.5, 44.5);
    const lv = fw.legal_validation || {};
    g += O.icon("doc", L, 45.6, 2.0, x.accent, 0.15);
    g += T(L + 2.6, 47.0, `Permis n° ${lv.permit_number || "PERMIS-EN-COURS"}`, { fam: x.mono, size: s * 0.92, fill: x.ink });
    g += T(L + 2.6, 49.5, `Scellé COSE_Sign1 ES256 · JavaCard ACOSJ 92 Ko`, { fam: x.sans, size: 0.76, fill: x.muted });

    g += O.nfcTarget(RR - 2.9, 47.4, 2.8, x.accent);
    g += T(RR - 6.2, 47.7, "Toucher pour écouter", { fam: x.sans, size: 0.72, fill: x.muted, anchor: "end", italic: true });
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
