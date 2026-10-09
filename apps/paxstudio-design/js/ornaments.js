/**
 * PaxStudio Design — Ornements vectoriels purs (aucune image matricielle).
 * Icônes au trait (grille 24), guilloches paramétriques, rosaces, insignes, camée.
 * Exposé en global `PaxOrnaments`.
 */
(function (root) {
  "use strict";

  const f = n => Math.round(n * 1000) / 1000;

  /** Icônes au trait, grille 24×24, stroke = couleur courante. */
  const ICONS = {
    stone: "M6 21V9a6 6 0 0 1 12 0v12M4 21h16M12 9v6M9.5 11.5h5",
    vault: "M3 21h18M5 21V10l7-5 7 5v11M9 21v-6h6v6M12 8v3",
    lawn: "M3 20h18M5 20c0-3 1-5 2-6M8 20c0-4 .5-6 1.5-8M12 20c0-4 0-7 0-9M16 20c0-4-.5-6-1.5-8M19 20c0-3-1-5-2-6M12 6.5a1.2 1.2 0 1 0 0-.1M8 4.5a1 1 0 1 0 0-.1M16 4.5a1 1 0 1 0 0-.1",
    columbarium: "M3 4h18v16H3zM3 9.3h18M3 14.6h18M9 4v16M15 4v16",
    sea: "M2 9c2.5-2 4.5-2 7 0s4.5 2 7 0 4.5-2 6 0M2 14c2.5-2 4.5-2 7 0s4.5 2 7 0 4.5-2 6 0M2 19c2.5-2 4.5-2 7 0s4.5 2 7 0 4.5-2 6 0",
    urn: "M9 3h6M10 3v2.5C7 7 5.5 9.5 5.5 13c0 4 3 7 6.5 7s6.5-3 6.5-7c0-3.5-1.5-6-4.5-7.5V3M8 21h8",
    home: "M3 11 12 4l9 7M5.5 9.5V20h13V9.5M10 20v-5h4v5",
    tree: "M12 21v-7M12 14l-3-3M12 15l3-3M12 3c-4 0-7 3-7 6.5S8 15 12 15s7-2 7-5.5S16 3 12 3z",
    science: "M9 3h6M10 3v6L4.5 18.5A1.8 1.8 0 0 0 6 21h12a1.8 1.8 0 0 0 1.5-2.5L14 9V3M7 15h10",
    heart: "M12 20s-7.5-4.6-7.5-10A4.3 4.3 0 0 1 12 7a4.3 4.3 0 0 1 7.5 3c0 5.4-7.5 10-7.5 10z",
    ban: "M12 3a9 9 0 1 0 0 18 9 9 0 1 0 0-18zM5.6 5.6l12.8 12.8",
    radiation: "M12 10.2a1.8 1.8 0 1 0 0 3.6 1.8 1.8 0 1 0 0-3.6zM10 8.5 7.2 3.7A9.5 9.5 0 0 0 2.6 11.6h5.6M14 8.5l2.8-4.8a9.5 9.5 0 0 1 4.6 7.9h-5.6M10.3 15.2l-2.8 4.9a9.5 9.5 0 0 0 9 0l-2.8-4.9",
    biohazard: "M12 13.5a2 2 0 1 0 0-.1M12 3.5a4.5 4.5 0 0 0-2 8.5M12 3.5a4.5 4.5 0 0 1 2 8.5M4.6 17.5a4.5 4.5 0 0 0 7.4 0M19.4 17.5a4.5 4.5 0 0 1-7.4 0M4.6 17.5a4.5 4.5 0 0 1 5.4-5.5M19.4 17.5a4.5 4.5 0 0 0-5.4-5.5",
    check: "M12 3a9 9 0 1 0 0 18 9 9 0 1 0 0-18zM7.5 12.3l3 3 6-6.3",
    alert: "M12 3.5 2.5 20h19zM12 10v4.5M12 17.3v.2",
    flame: "M12 21c-4 0-6.5-2.7-6.5-6.2 0-3.6 3-5.4 3.6-9.3 2 1.3 3 3.2 3 5 1-.6 1.8-1.8 2-3.2 2.2 1.8 3.4 4.6 3.4 7.5 0 3.5-2.5 6.2-5.5 6.2z",
    lock: "M6 11h12v10H6zM8.5 11V8a3.5 3.5 0 0 1 7 0v3M12 15v2.5",
    mic: "M12 3a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V6a3 3 0 0 0-3-3zM5.5 11.5a6.5 6.5 0 0 0 13 0M12 18v3M9 21h6",
    camera: "M3 8h4l2-2.5h6L17 8h4v12H3zM12 10.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 1 0 0-7z",
    music: "M9 18V5l11-2v13M9 18a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0zM20 16a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0z",
    bolt: "M13 2 4.5 13.5H11L10 22l8.5-11.5H13z",
    doc: "M6 3h8l4 4v14H6zM14 3v4h4M9 12h6M9 16h6",
    rite: "M12 3v18M7.5 8h9M5 21h14"
  };

  function icon(name, x, y, size, color, sw) {
    const d = ICONS[name] || ICONS.doc;
    const s = size / 24;
    return `<g transform="translate(${f(x)} ${f(y)}) scale(${f(s)})" fill="none" stroke="${color}" stroke-width="${f((sw || 0.16) / s)}" stroke-linecap="round" stroke-linejoin="round"><path d="${d}"/></g>`;
  }

  /** Lignes de sécurité ondulées (guilloche linéaire) couvrant un rectangle. */
  function guillocheWaves(x, y, w, h, density, color, opacity) {
    const n = 4 + density * 3;
    let paths = "";
    for (let i = 0; i < n; i++) {
      const y0 = y + (h * (i + 0.5)) / n;
      const amp = h / n * 1.6;
      const phase = (i * Math.PI) / 3.7;
      let d = "";
      for (let xx = 0; xx <= w; xx += 0.8) {
        const yy = y0 + amp * Math.sin((xx / w) * Math.PI * 6 + phase) * Math.cos((xx / w) * Math.PI * 1.3 + i * 0.4);
        d += (xx === 0 ? "M" : "L") + f(x + xx) + " " + f(yy);
      }
      paths += `<path d="${d}"/>`;
    }
    return `<g fill="none" stroke="${color}" stroke-width="0.06" opacity="${opacity}">${paths}</g>`;
  }

  /** Rosace guillochée : anneaux polaires déphasés (effet moiré). */
  function rosette(cx, cy, R, density, color, opacity) {
    const rings = 3 + Math.round(density / 2);
    const petals = 9 + density * 2;
    let paths = "";
    for (let k = 0; k < rings; k++) {
      const rr = R * (0.45 + (0.55 * (k + 1)) / rings);
      for (let p = 0; p < 2; p++) {
        let d = "";
        const ph = (p * Math.PI) / petals + k * 0.35;
        for (let t = 0; t <= 360; t += 2) {
          const a = (t * Math.PI) / 180;
          const r = rr * (1 + 0.14 * Math.sin(petals * a + ph));
          d += (t === 0 ? "M" : "L") + f(cx + r * Math.cos(a)) + " " + f(cy + r * Math.sin(a));
        }
        paths += `<path d="${d}Z"/>`;
      }
    }
    return `<g fill="none" stroke="${color}" stroke-width="0.07" opacity="${opacity}">${paths}</g>`;
  }

  /** Hypotrochoïde (spirographe) — médaillon de sécurité central. */
  function spiro(cx, cy, R, r, d, scale, color, opacity) {
    let p = "";
    const turns = r / gcd(R, r);
    const steps = Math.round(360 * turns / 2);
    for (let i = 0; i <= steps; i++) {
      const t = (i / steps) * 2 * Math.PI * turns;
      const x = (R - r) * Math.cos(t) + d * Math.cos(((R - r) / r) * t);
      const y = (R - r) * Math.sin(t) - d * Math.sin(((R - r) / r) * t);
      p += (i === 0 ? "M" : "L") + f(cx + x * scale) + " " + f(cy + y * scale);
    }
    return `<path d="${p}" fill="none" stroke="${color}" stroke-width="0.06" opacity="${opacity}"/>`;
  }
  function gcd(a, b) { return b ? gcd(b, a % b) : a; }

  /** Colombe ciselée (boîte 20×20). */
  function dove(x, y, size, fill) {
    const s = size / 20;
    return `<g transform="translate(${f(x)} ${f(y)}) scale(${f(s)})" fill="${fill}">
      <path d="M1.5 12.2c2.6-2.4 6-3 9-1.8.8-4 3.6-7.4 8-8.4-1.6 2.6-2.4 5.4-2.8 8 1.4.2 2.6 1 3.2 2.2-1 .2-2 .1-2.8.4-.6 2.6-3 4.6-6.4 4.8-2.6.2-4.8-.6-6.6-2.2 1.2-.1 2.3-.6 3-1.3-1.6.2-3.2-.3-4.6-1.7z"/>
      <path d="M17.6 12.4c.8.4 1.6.5 2.4.4" stroke="${fill}" stroke-width=".4" fill="none"/>
      <path d="M6 16.5c-1 1.4-1.4 2.4-1.2 3.3M8.2 17c-.4 1.2-.4 2.2 0 3" stroke="${fill}" stroke-width=".35" fill="none" stroke-linecap="round"/>
    </g>`;
  }

  /** Feuille de chêne lobée, générée en coordonnées polaires. */
  function oakLeaf(cx, cy, len, angle, fill) {
    let d = "";
    const n = 60;
    for (let i = 0; i <= n; i++) {
      const t = i / n;
      const along = t * len;
      const width = Math.sin(Math.PI * t) * len * 0.22 * (1 + 0.35 * Math.cos(t * Math.PI * 9));
      d += (i === 0 ? "M" : "L") + f(along) + " " + f(-width);
    }
    for (let i = n; i >= 0; i--) {
      const t = i / n;
      const along = t * len;
      const width = Math.sin(Math.PI * t) * len * 0.22 * (1 + 0.35 * Math.cos(t * Math.PI * 9 + 0.6));
      d += "L" + f(along) + " " + f(width);
    }
    return `<g transform="translate(${f(cx)} ${f(cy)}) rotate(${f(angle)})"><path d="${d}Z" fill="${fill}"/><path d="M0 0L${f(len * 0.92)} 0" stroke="rgba(0,0,0,.25)" stroke-width="${f(len * 0.02)}"/></g>`;
  }

  /** Rameau de chêne des Ardennes (boîte ≈ size × size). */
  function oakBranch(x, y, size, fill) {
    const s = size;
    const stem = `<path d="M${f(x + s * 0.1)} ${f(y + s * 0.9)} Q${f(x + s * 0.45)} ${f(y + s * 0.55)} ${f(x + s * 0.9)} ${f(y + s * 0.15)}" fill="none" stroke="${fill}" stroke-width="${f(s * 0.035)}" stroke-linecap="round"/>`;
    const leaves = [
      oakLeaf(x + s * 0.3, y + s * 0.7, s * 0.42, -120, fill),
      oakLeaf(x + s * 0.42, y + s * 0.58, s * 0.4, -10, fill),
      oakLeaf(x + s * 0.6, y + s * 0.4, s * 0.38, -105, fill),
      oakLeaf(x + s * 0.72, y + s * 0.3, s * 0.34, 5, fill)
    ].join("");
    const acorn = (ax, ay) => `<ellipse cx="${f(ax)}" cy="${f(ay + s * 0.05)}" rx="${f(s * 0.045)}" ry="${f(s * 0.065)}" fill="${fill}" opacity=".85"/><path d="M${f(ax - s * 0.055)} ${f(ay)}a${f(s * 0.055)} ${f(s * 0.04)} 0 0 1 ${f(s * 0.11)} 0z" fill="${fill}"/>`;
    return `<g>${stem}${leaves}${acorn(x + s * 0.2, y + s * 0.62)}${acorn(x + s * 0.27, y + s * 0.55)}</g>`;
  }

  /** Silhouette de profil (camée), boîte 20×24. */
  const CAMEO_PATH = "M10 3c3.5 0 5.5 2.5 5.5 5.5 0 1 1 2 .8 2.5-.3.5-.9.6-.9 1.2 0 .8-.3 1.4-1.1 1.6-.8.2-.9 1.2-.7 2.2 1.9.6 4.4 1.5 5.4 4V24H1v-4c1-2.5 4-3.7 6-4.2.5-1-.0-2.3-1-3.3-1-1.2-1.4-2.7-1.4-4C4.6 5.3 7 3 10 3z";

  function cameo(cx, cy, rx, ry, fill, bg) {
    const w = rx * 1.5;
    const s = w / 20;
    return `<ellipse cx="${f(cx)}" cy="${f(cy)}" rx="${f(rx)}" ry="${f(ry)}" fill="${bg}"/>` +
      `<g transform="translate(${f(cx - w / 2)} ${f(cy + ry - 24 * s)}) scale(${f(s)})"><path d="${CAMEO_PATH}" fill="${fill}"/></g>`;
  }

  /** Cible concentrique d'effleurement NFC. */
  function nfcTarget(cx, cy, r, color) {
    let g = "";
    for (let i = 1; i <= 4; i++) {
      g += `<circle cx="${f(cx)}" cy="${f(cy)}" r="${f((r * i) / 4)}" fill="none" stroke="${color}" stroke-width="${i === 4 ? 0.22 : 0.1}" opacity="${0.35 + i * 0.15}"/>`;
    }
    const a = r * 0.3;
    g += `<g fill="none" stroke="${color}" stroke-width="0.22" stroke-linecap="round">
      <path d="M${f(cx - a * 0.6)} ${f(cy - a)}a${f(a * 1.2)} ${f(a * 1.2)} 0 0 1 0 ${f(a * 2)}"/>
      <path d="M${f(cx - a * 0.1)} ${f(cy - a * 1.45)}a${f(a * 1.7)} ${f(a * 1.7)} 0 0 1 0 ${f(a * 2.9)}"/>
      <path d="M${f(cx + a * 0.4)} ${f(cy - a * 1.9)}a${f(a * 2.2)} ${f(a * 2.2)} 0 0 1 0 ${f(a * 3.8)}"/>
    </g><circle cx="${f(cx - a * 0.9)}" cy="${f(cy)}" r="${f(a * 0.22)}" fill="${color}"/>`;
    return g;
  }

  root.PaxOrnaments = { ICONS, icon, guillocheWaves, rosette, spiro, dove, oakBranch, cameo, nfcTarget, CAMEO_PATH };
})(typeof self !== "undefined" ? self : this);
