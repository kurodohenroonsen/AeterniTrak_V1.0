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

  // ---------------------------------------------------------------- CARTE 1 · RECTO
  function card1Recto(x) {
    const c = x.data;
    const ci = c.civil_identity || {};
    const { s } = x;
    const right = W - M;
    let g = background(x) + guilloche(x, [[69, 26, 15]]) + fillets(x);

    g += T(M, 7.4, "AETERNITRAK", { fam: x.title, size: s(2.9), weight: 600, fill: `url(#${x.p}-gold)`, ls: 0.32 });
    g += T(right, 5.9, "CARTE 1 · VOLONTÉS & SÉCURITÉ", { fam: x.sans, size: s(1.2), weight: 600, fill: x.muted, anchor: "end", ls: 0.12 });
    g += T(right, 8.0, "PAVS · ISO/IEC 7810 ID-1", { fam: x.sans, size: s(1.05), fill: x.muted, anchor: "end", ls: 0.1 });
    g += goldRule(x, M, right, 10.1);

    g += portrait(x, { kind: "rect", x: M, y: 12.2, w: 17, h: 21.4, r: 1 }, "pt");

    const X = 24.4;
    const colW = right - X;
    const name = fit(ci.full_name || "Nom Prénom", colW, s(3.3), x.title, 600, s(2.1));
    g += T(X, 15.9, name.text, { fam: x.title, size: name.size, weight: 600, fill: x.ink, ls: 0.08 });
    const born = ci.gender === "F" ? "Née" : ci.gender === "M" ? "Né" : "Né(e)";
    const birth = fit(`${born} le ${longDate(ci.birth_date)}${ci.birth_place ? " · " + ci.birth_place : ""}`, colW, s(2.05), x.body, 500, s(1.5));
    g += T(X, 19.7, birth.text, { fam: x.body, size: birth.size, weight: 500, fill: x.ink });

    g += T(X, 23.3, "N° DE REGISTRE NATIONAL (NISS)", { fam: x.sans, size: s(0.98), weight: 600, fill: x.muted, ls: 0.12 });
    const niss = R.validateNiss(ci.national_id_niss, ci.birth_date, ci.gender);
    const nissText = niss.formatted || "—";
    g += T(X, 26.4, nissText, { fam: x.mono, size: s(2.2), weight: 500, fill: x.ink, ls: 0.06 });
    const nw = measure(nissText, s(2.2), x.mono, 500) + nissText.length * 0.06;
    const badge = pill(X + nw + 1.4, 24.1, niss.valid ? "MOD 97 VALIDE" : "MOD 97 INVALIDE", niss.valid ? "ok" : "danger", niss.valid ? "check" : "alert", x, s(1.0));
    g += badge.svg;

    g += T(X, 29.7, "MÉDECIN RÉFÉRENT · INAMI", { fam: x.sans, size: s(0.98), weight: 600, fill: x.muted, ls: 0.12 });
    const phy = ci.certifying_physician || {};
    const doc = fit(`${phy.name || "—"}${phy.inami ? " · " + phy.inami : ""}`, colW, s(1.75), x.body, 500, s(1.3));
    g += T(X, 32.4, doc.text, { fam: x.body, size: doc.size, weight: 500, fill: x.ink });

    // Badges sanitaires
    let bx = M;
    const badges = R.healthBadges(c);
    if (!badges.length) badges.push({ icon: "check", tone: "muted", label: "Aucune réserve sanitaire" });
    for (const b of badges) {
      const pl = pill(bx, 35.0, b.label, b.tone, b.icon, x, s(1.05));
      if (bx + pl.w > right) break;
      g += pl.svg;
      bx += pl.w + 1;
    }

    // Bandeau master d'alerte pyrotechnique
    const pyro = R.pyroStatus(c);
    const danger = pyro.level === "danger";
    const by = 39.4;
    const bh = 7.8;
    g += `<g class="${danger ? "pyro-danger" : "pyro-ok"}">`;
    g += `<rect x="${M}" y="${by}" width="${f(right - M)}" height="${bh}" rx="1.2" fill="${danger ? `url(#${x.p}-hatch)` : "#1f6a45"}"/>`;
    g += `<rect x="${M + 0.35}" y="${by + 0.35}" width="${f(right - M - 0.7)}" height="${f(bh - 0.7)}" rx=".95" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width=".1"/>`;
    g += O.icon(danger ? "alert" : pyro.code === "INHUMATION_OK" ? "stone" : pyro.code === "NO_DEVICE" ? "flame" : "check", M + 1.3, by + 1.4, 5, "#fff", 0.32);
    const tt = fit(`${danger ? "⛔ " : ""}${pyro.title.toUpperCase()}`, right - M - 9, s(1.85), x.sans, 700, s(1.3));
    g += T(M + 7.6, by + 3.3, tt.text, { fam: x.sans, size: tt.size, weight: 700, fill: "#fff", ls: 0.06 });
    const dt = fit(pyro.detail, right - M - 9, s(1.25), x.sans, 400, s(0.95));
    g += T(M + 7.6, by + 5.9, dt.text, { fam: x.sans, size: dt.size, fill: "#fff", opacity: 0.9 });
    g += `</g>`;

    g += O.icon("bolt", M - 0.2, 49.3, 2.1, x.accent, 0.18);
    g += T(M + 2.2, 50.9, "Puce NFC sans contact · JavaCard ACOSJ 92 Ko · 13,56 MHz", { fam: x.sans, size: s(1.08), fill: x.muted, ls: 0.04 });
    g += T(right, 50.9, c.id || "", { fam: x.mono, size: s(0.95), fill: x.muted, anchor: "end" });
    return g;
  }

  // ---------------------------------------------------------------- CARTE 1 · VERSO
  function card1Verso(x) {
    const c = x.data;
    const fw = c.funeral_wills || {};
    const mm = c.multimedia_memorial || {};
    const { s } = x;
    const right = W - M;
    const mode = R.burialMode(fw.burial_mode);
    let g = background(x) + guilloche(x, [[71.3, 21, 13]]) + fillets(x);

    g += T(M, 7.4, "VOLONTÉS FUNÉRAIRES", { fam: x.title, size: s(2.6), weight: 600, fill: `url(#${x.p}-gold)`, ls: 0.22 });
    g += T(right, 5.9, "Loi du 20 juillet 1971", { fam: x.body, size: s(1.45), fill: x.muted, anchor: "end", italic: true });
    g += T(right, 8.0, "sur les funérailles et sépultures", { fam: x.body, size: s(1.2), fill: x.muted, anchor: "end", italic: true });
    g += goldRule(x, M, right, 10.1);

    const don = R.donationSummary(c);
    const tiles = [
      { icon: mode.icon, label: `SÉPULTURE · MODE ${mode.id}`, value: mode.short },
      { icon: "rite", label: "CÉRÉMONIE · RITE", value: fw.ceremony_nature || "Non précisé" },
      { icon: mode.family === "inhumation" ? "stone" : mode.icon, label: "DESTINATION", value: fw.residue_destination || "Non précisée" },
      { icon: R.isThermal(mode.id) ? "flame" : "vault", label: "CERCUEIL", value: fw.coffin_material || "Non précisé" },
      { icon: don.icon, label: "DON", value: don.label },
      { icon: "doc", label: "POMPES FUNÈBRES", value: fw.chosen_funeral_home || "Libre choix des proches" }
    ];
    const tw = 27.3;
    const th = 6.3;
    tiles.forEach((t, i) => {
      const tx = M + (i % 2) * (tw + 1.1);
      const ty = 11.5 + Math.floor(i / 2) * (th + 0.9);
      g += `<rect x="${f(tx)}" y="${f(ty)}" width="${tw}" height="${th}" rx=".8" fill="${rgba(x.accent, x.dark ? 0.14 : 0.09)}" stroke="${rgba(x.accent, 0.55)}" stroke-width=".1"/>`;
      g += O.icon(t.icon, tx + 0.9, ty + 1.3, 3.7, x.accent, 0.2);
      g += T(tx + 5.4, ty + 2.4, t.label, { fam: x.sans, size: s(0.88), weight: 600, fill: x.muted, ls: 0.1 });
      const v = fit(t.value, tw - 6.1, s(1.5), x.body, 600, s(1.05));
      g += T(tx + 5.4, ty + 4.9, v.text, { fam: x.body, size: v.size, weight: 600, fill: x.ink });
    });

    g += O.nfcTarget(71.3, 20.6, 8.2, x.accent);
    g += T(71.3, 31.6, "EFFLEUREZ ICI", { fam: x.sans, size: s(0.95), weight: 600, fill: x.muted, anchor: "middle", ls: 0.18 });

    // Cartouche multimédia scellé
    const ac = mm.audio_choice || {};
    const cy = 33.3;
    g += `<rect x="${M}" y="${cy}" width="${f(right - M)}" height="4.4" rx=".8" fill="${rgba(x.accent, x.dark ? 0.16 : 0.1)}" stroke="url(#${x.p}-gold)" stroke-width=".12"/>`;
    g += O.icon("lock", M + 0.8, cy + 0.85, 2.7, x.accent, 0.2);
    g += T(M + 4, cy + 2.85, "COFFRE MULTIMÉDIA SCELLÉ", { fam: x.sans, size: s(0.9), weight: 700, fill: x.muted, ls: 0.1 });
    let mx = M + 4 + measure("COFFRE MULTIMÉDIA SCELLÉ", s(0.9), x.sans, 700) + 3.5;
    const items = [
      ["camera", `${mm.photo_count || 0} photo${(mm.photo_count || 0) > 1 ? "s" : ""}`],
      ["mic", ac.has_voice_memo ? `${ac.voice_memo_duration_sec || 0} s` : "—"],
      ["music", (mm.chosen_music || {}).title || "—"]
    ];
    items.forEach(([ic, label], i) => {
      g += O.icon(ic, mx, cy + 0.95, 2.5, x.accent, 0.2);
      const maxW = i === 2 ? right - mx - 3.6 : 20;
      const lt = fit(label, maxW, s(1.3), x.body, 600, s(1));
      g += T(mx + 3.1, cy + 2.95, lt.text, { fam: x.body, size: lt.size, weight: 600, fill: x.ink });
      mx += 3.1 + measure(lt.text, lt.size, x.body, 600) + 3;
    });

    // Épitaphe testamentaire
    const ey = 38.6;
    const eh = 8.8;
    g += `<rect x="${M}" y="${ey}" width="${f(right - M)}" height="${eh}" rx="1" fill="${rgba(x.accent, x.dark ? 0.08 : 0.05)}" stroke="url(#${x.p}-gold)" stroke-width=".22"/>`;
    g += `<rect x="${M + 0.6}" y="${ey + 0.6}" width="${f(right - M - 1.2)}" height="${eh - 1.2}" rx=".6" fill="none" stroke="url(#${x.p}-gold)" stroke-width=".07"/>`;
    for (const [cx0, cy0] of [[M + 0.6, ey + 0.6], [right - 0.6, ey + 0.6], [M + 0.6, ey + eh - 0.6], [right - 0.6, ey + eh - 0.6]]) {
      g += `<path d="M${f(cx0)} ${f(cy0 - 0.7)}l.7 .7-.7 .7-.7-.7z" fill="url(#${x.p}-gold)"/>`;
    }
    const quote = x.design.epitaph ?? mm.epitaph ?? "";
    const lines = wrap(`« ${quote || "Pour moi, l'essentiel c'est…"} »`, right - M - 5, s(1.62), x.body, 2, "italic");
    lines.forEach((ln, i) => {
      g += T(W / 2, ey + 3.2 + i * 2.15 + (lines.length === 1 ? 1 : 0), ln, { fam: x.body, size: s(1.62), fill: x.ink, anchor: "middle", italic: true });
    });
    g += T(W / 2, ey + eh - 1.15, `— ${(c.civil_identity || {}).full_name || ""}`, { fam: x.title, size: s(0.95), fill: x.muted, anchor: "middle", ls: 0.15 });

    const lv = fw.legal_validation || {};
    const permit = fit(`Permis d'inhumation / transport n° ${lv.permit_number || "—"}`, 38, s(1.0), x.mono, 400, 0.7);
    g += T(M, 50.9, permit.text, { fam: x.mono, size: permit.size, fill: x.muted });
    const note = R.isSarco(mode.id)
      ? fit("Sarcomusation : démonstrateur prospectif (DEC-AET-15)", 37, s(1.0), x.sans, 600, 0.7)
      : fit("Aucune date de décès imprimée · encodage NFC post-mortem", 37, s(1.0), x.sans, 400, 0.7);
    g += T(right, 50.9, note.text, { fam: x.sans, size: note.size, weight: R.isSarco(mode.id) ? 600 : 400, fill: R.isSarco(mode.id) ? TONES.warn : x.muted, anchor: "end" });
    return g;
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

  root.PaxCards = { render, FONTS, MATERIALS, W, H, longDate, shortDate };
})(typeof self !== "undefined" ? self : this);
