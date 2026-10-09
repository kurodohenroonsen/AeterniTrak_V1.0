/**
 * PaxStudio Design — Pré-vol prépresse (contrôle qualité avant B.A.T.).
 *
 * Quatre contrôles, recalculés à chaque rendu sur les deux faces de la carte active :
 *   1. Micro-texte : corps effectif (taille × échelle du calque) < 0,86 mm (≈ 2,44 pt).
 *   2. Zone de garde : élément hors de la marge de sécurité de 3 mm, ou qui mord sur la découpe.
 *   3. Zone d'exclusion NFC : recouvrement des surfaces métallisées (dorure à chaud, hologramme)
 *      sur le module de la puce et la bande d'antenne.
 *   4. Contraste : rapport de luminance WCAG 2.x entre chaque texte et son fond.
 *
 * Hypothèses explicites : ISO/IEC 7810 ne fixe ni seuil de contraste ni gabarit d'antenne ;
 * les seuils WCAG AA (4,5:1) servent de référence, et la géométrie de l'inlay (module 15 × 15 mm,
 * bande d'antenne entre 3 et 7 mm du bord) est une hypothèse de travail à confirmer avec le
 * fabricant de l'inlay ACOSJ ; le module est centré sur la cible NFC (en miroir sur l'autre face).
 * Ces valeurs sont réglables dans PaxPreflight.CONFIG.
 *
 * Exposé en global `PaxPreflight`.
 */
(function (root) {
  "use strict";

  const CONFIG = {
    microTextMm: 0.86,
    safeMm: 3,
    tolerance: 0.05,
    contrastAA: 4.5,
    contrastMin: 3,
    nfc: { module: 15, bandInner: 3, bandOuter: 7, moduleMaxCover: 0.1, bandMaxCover: 0.15 }
  };
  const PT_PER_MM = 1 / 0.3528;

  // ---------------------------------------------------------------- couleurs (WCAG 2.x)
  function parseColor(str) {
    if (!str) return null;
    const s = String(str).trim().toLowerCase();
    let m = /^#([0-9a-f]{3}|[0-9a-f]{6})$/.exec(s);
    if (m) {
      const h = m[1].length === 3 ? m[1].split("").map(c => c + c).join("") : m[1];
      const n = parseInt(h, 16);
      return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
    }
    m = /^rgba?\(([^)]+)\)$/.exec(s);
    if (m) return m[1].split(",").slice(0, 3).map(v => Number(v));
    if (s === "white") return [255, 255, 255];
    if (s === "black") return [0, 0, 0];
    return null;
  }
  function luminance(rgb) {
    const c = rgb.map(v => {
      const x = v / 255;
      return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
  }
  function contrastRatio(a, b) {
    const la = luminance(a);
    const lb = luminance(b);
    return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
  }
  function mixRgb(a, b, t) { return a.map((v, i) => Math.round(v + (b[i] - v) * t)); }

  // ---------------------------------------------------------------- géométrie
  function intersectArea(a, b) {
    const w = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x);
    const h = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
    return w > 0 && h > 0 ? w * h : 0;
  }
  /** Zones d'exclusion NFC : module de puce (carré centré sur la cible NFC) et bande d'antenne. */
  function nfcZones(W, H, chipCenter) {
    const k = CONFIG.nfc;
    const c = chipCenter || { x: W / 2, y: H / 2 };
    const module = { x: c.x - k.module / 2, y: c.y - k.module / 2, w: k.module, h: k.module };
    const i = k.bandInner;
    const o = k.bandOuter;
    const band = [
      { x: i, y: i, w: W - 2 * i, h: o - i }, { x: i, y: H - o, w: W - 2 * i, h: o - i },
      { x: i, y: o, w: o - i, h: H - 2 * o }, { x: W - o, y: o, w: o - i, h: H - 2 * o }
    ];
    return { module, band, bandArea: band.reduce((s, r) => s + r.w * r.h, 0) };
  }

  // ---------------------------------------------------------------- exécution sur le DOM rendu
  /**
   * @param {{ faces: {face:string, svg:SVGSVGElement}[], editor, getRecord:(id)=>object,
   *           materialBg:string[], accent:string, W:number, H:number }} ctx
   */
  function run(ctx) {
    const issues = [];
    const stats = { texts: 0, nodes: 0 };
    const bgDefault = mixRgb(parseColor(ctx.materialBg[0]), parseColor(ctx.materialBg[1]), 0.5);
    const accent = parseColor(ctx.accent) || [168, 130, 47];
    const foil = { gold: accent, whitegold: [201, 206, 214], rosegold: [215, 154, 134] };
    const faceLabel = f => (f.endsWith("recto") ? "Recto" : "Verso");

    // La puce occupe la même position physique sur les deux faces : au recto, la cible NFC du verso
    // apparaît en miroir horizontal (retournement de la carte autour de son axe vertical).
    let chip = null;
    for (const { face, svg } of ctx.faces) {
      if (!svg) continue;
      const n = ctx.editor.faceNodes(face).find(x => x.kind === "nfc");
      if (n) {
        const c = { x: n.geo.aabb.x + n.geo.aabb.w / 2, y: n.geo.aabb.y + n.geo.aabb.h / 2 };
        chip = { face, c };
        if (face.endsWith("verso")) break;
      }
    }
    const chipOn = face => (!chip ? null : chip.face === face ? chip.c : { x: ctx.W - chip.c.x, y: chip.c.y });

    for (const { face, svg } of ctx.faces) {
      if (!svg) continue;
      const nodes = ctx.editor.faceNodes(face);
      stats.nodes += nodes.length;
      const nfcCenter = chipOn(face);
      const zones = nfcZones(ctx.W, ctx.H, nfcCenter);
      let moduleCover = 0;
      let bandCover = 0;
      const metalNodes = [];

      for (const n of nodes) {
        if (n.el.getAttribute("display") === "none") continue;
        const rec = ctx.getRecord(n.id) || {};
        const label = n.el.dataset.label || n.id;
        const required = n.el.dataset.required === "true";
        const scale = Math.sqrt(Math.abs((rec.sx ?? 1) * (rec.sy ?? 1)));
        const b = n.geo.aabb;

        // 2. Zone de garde
        if (!n.decor && n.el.dataset.bleed !== "true") {
          const t = CONFIG.tolerance;
          const s = CONFIG.safeMm;
          if (b.x < -t || b.y < -t || b.x + b.w > ctx.W + t || b.y + b.h > ctx.H + t) {
            issues.push({ check: "guard", level: "error", face, id: n.id, text: `${faceLabel(face)} · « ${label} » mord sur la découpe.` });
          } else if (b.x < s - t || b.y < s - t || b.x + b.w > ctx.W - s + t || b.y + b.h > ctx.H - s + t) {
            issues.push({ check: "guard", level: "warn", face, id: n.id, text: `${faceLabel(face)} · « ${label} » déborde de la marge de sécurité de 3 mm.` });
          }
        }

        // 3. Surfaces métallisées
        if (n.el.dataset.metal === "true") {
          metalNodes.push(label);
          moduleCover += intersectArea(b, zones.module);
          bandCover += zones.band.reduce((s, r) => s + intersectArea(b, r), 0);
        }

        // 1 & 4. Textes du nœud
        let minSize = Infinity;
        let minRatio = Infinity;
        for (const t of n.el.querySelectorAll("text")) {
          stats.texts++;
          const size = (Number(t.getAttribute("font-size")) || 0) * scale;
          if (size) minSize = Math.min(minSize, size);
          const fill = t.getAttribute("fill") || "";
          let fg = parseColor(fill);
          const fm = /url\(#[^)]*-(gold|goldv|foil-whitegold|foil-rosegold|rainbow)\)/.exec(fill);
          if (fm) fg = fm[1] === "foil-whitegold" ? foil.whitegold : fm[1] === "foil-rosegold" ? foil.rosegold : fm[1] === "rainbow" ? null : foil.gold;
          if (!fg) continue;
          const bgEl = t.closest("[data-bg]:not([data-bg=''])");
          const bg = bgEl ? parseColor(bgEl.getAttribute("data-bg")) || bgDefault : bgDefault;
          minRatio = Math.min(minRatio, contrastRatio(fg, bg));
        }
        if (minSize < CONFIG.microTextMm) {
          issues.push({ check: "micro", level: required ? "error" : "warn", face, id: n.id, size: minSize,
            text: `${faceLabel(face)} · « ${label} » : corps ${minSize.toFixed(2).replace(".", ",")} mm (${(minSize * PT_PER_MM).toFixed(2).replace(".", ",")} pt) < 0,86 mm.` });
        }
        if (minRatio < CONFIG.contrastAA) {
          const level = minRatio < CONFIG.contrastMin ? (required ? "error" : "warn") : (required ? "warn" : "info");
          issues.push({ check: "contrast", level, face, id: n.id, ratio: minRatio,
            text: `${faceLabel(face)} · « ${label} » : contraste ${minRatio.toFixed(2).replace(".", ",")}:1 (AA : 4,5:1).` });
        }
      }

      const mc = moduleCover / (zones.module.w * zones.module.h);
      const bc = bandCover / zones.bandArea;
      if (mc > CONFIG.nfc.moduleMaxCover) {
        issues.push({ check: "nfc", level: "error", face, text: `${faceLabel(face)} · ${Math.round(mc * 100)} % du module de puce recouvert de surfaces métallisées (${metalNodes.join(", ")}).` });
      }
      if (bc > CONFIG.nfc.bandMaxCover) {
        issues.push({ check: "nfc", level: "warn", face, text: `${faceLabel(face)} · ${Math.round(bc * 100)} % de la bande d'antenne recouverte de surfaces métallisées.` });
      }
      issues.push({ check: "nfc-info", level: "ok", face, zones, cover: { module: mc, band: bc } });
    }
    return { issues: issues.filter(i => i.level !== "ok"), zones: issues.filter(i => i.level === "ok"), stats };
  }

  /** Superposition SVG des zones contrôlées (sécurité, fond perdu, exclusion NFC). */
  function zonesOverlay(W, H, zones, k) {
    const sw = k || 0.1;
    let g = `<rect class="pf-bleed" x="-2" y="-2" width="${W + 4}" height="${H + 4}" stroke-width="${sw}"/>`;
    g += `<rect class="pf-safe" x="3" y="3" width="${W - 6}" height="${H - 6}" stroke-width="${sw}"/>`;
    if (zones) {
      for (const r of zones.band) g += `<rect class="pf-band" x="${r.x}" y="${r.y}" width="${r.w}" height="${r.h}"/>`;
      const m = zones.module;
      g += `<rect class="pf-module" x="${m.x}" y="${m.y}" width="${m.w}" height="${m.h}" stroke-width="${sw}"/>`;
    }
    return g;
  }

  root.PaxPreflight = { CONFIG, parseColor, luminance, contrastRatio, intersectArea, nfcZones, run, zonesOverlay };
})(typeof self !== "undefined" ? self : this);
