#!/usr/bin/env node
/**
 * PaxStudio Design — Tests de l'atelier : modèle de nœuds, cohérence rendu ↔ atelier,
 * historique d'annulation et calculs du pré-vol.
 * Usage : node apps/paxstudio-design/tests/atelier.test.mjs
 */
import fs from "node:fs";
import vm from "node:vm";
import path from "node:path";
import { fileURLToPath } from "node:url";

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const ctx = { window: {}, self: {}, setTimeout, clearTimeout };
vm.createContext(ctx);
for (const f of ["js/rules.js", "data/paxfunebre_44_test_cases.js", "js/ornaments.js", "js/cards.js", "js/history.js", "js/preflight.js", "js/editor.js"]) {
  vm.runInContext(fs.readFileSync(path.join(APP, f), "utf8"), ctx);
}
const { PaxCards: C, PaxRules: R, PaxHistory: Hist, PaxPreflight: PF, PaxEditor: E } = ctx.self;
const CASES = ctx.window.PAX_TEST_CASES;

let pass = 0;
let fail = 0;
function check(name, cond, info = "") {
  if (cond) pass++;
  else { fail++; console.error(`✗ ${name} ${info}`); }
}
const near = (a, b, eps = 1e-6) => Math.abs(a - b) < eps;
const prep = c => R.syncOfficial(R.normalizePavs(JSON.parse(JSON.stringify(c))));
const FACES = [[1, "recto"], [1, "verso"], [2, "recto"], [2, "verso"]];

// ---------------------------------------------------------------- 1. Rendu de toutes les faces, tous gabarits
for (const c0 of CASES) {
  const c = prep(c0);
  for (const layout of ["A", "B", "C", "D", "E"]) {
    for (const [card, side] of FACES) {
      if (card === 1 && layout !== "A") continue;
      const svg = C.render(card, side, c, { material: "ivoire", layout, nodes: {} }, {});
      if (svg.includes("\u0000")) check(`${c0.id} ${card}${side} ${layout} : marqueur résiduel`, false);
      const ids = (svg.match(/data-node-id="([^"]+)"/g) || []).map(s => s.slice(14, -1));
      if (new Set(ids).size !== ids.length) check(`${c0.id} ${card}${side} ${layout} : identifiants de nœud uniques`, false, ids.join(","));
    }
  }
}
check("Rendu des 44 cas × 4 faces × 5 gabarits sans marqueur ni doublon", true);
const c1 = prep(CASES[0]);
const index = side => { C.render(1, side, c1, { material: "ivoire", nodes: {} }, {}); return C.NODE_INDEX[`1${side}`]; };
check("Carte 1 recto : ≥ 20 calques", index("recto").length >= 20, index("recto").length);
check("Carte 1 verso : ≥ 20 calques", index("verso").length >= 20, index("verso").length);
check("Fonds, guilloches et filets verrouillés par défaut", index("recto").filter(n => n.decor).every(n => n.locked));
check("Cible NFC typée « nfc »", index("verso").some(n => n.kind === "nfc"));

// ---------------------------------------------------------------- 2. Modèle de nœud
const render1 = nodes => C.render(1, "recto", c1, { material: "ivoire", nodes }, {});
let svg = render1({ "c1r-title": { hidden: true } });
check("Calque masqué → display=none", /data-node-id="c1r-title"[^>]*display="none"/.test(svg.replace(/<g class="movable-node[^>]*data-node-id="c1r-title"[^>]*>/, m => m)) || /<g [^>]*display="none"[^>]*data-node-id="c1r-title"|<g [^>]*data-node-id="c1r-title"[^>]*display="none"/.test(svg));
svg = render1({ "c1r-name": { z: -5 } });
check("Ordre z : le nom passe sous le fond", svg.indexOf('data-node-id="c1r-name"') < svg.indexOf('data-node-id="c1r-background"'));
svg = render1({ "c1r-name": { z: 999 } });
check("Ordre z : le nom passe au premier plan", svg.indexOf('data-node-id="c1r-name"') > svg.indexOf('data-node-id="c1r-ref"'));
svg = render1({ "c1r-footer": { locked: true } });
check("Verrouillage → data-locked", /data-node-id="c1r-footer"[^>]*data-locked="true"|data-locked="true"[^>]*data-node-id="c1r-footer"/.test(svg) || svg.includes('data-locked="true" data-metal') || /c1r-footer[\s\S]{0,200}data-locked="true"/.test(svg));
svg = render1({ "c1r-name": { effect: "emboss" }, "c1r-title": { effect: "hologram" }, "c1r-subtitle": { effect: "deboss" } });
check("Effet gaufrage → filtre emboss", /c1r-name[\s\S]{0,200}filter="url\(#c1r-emboss\)"/.test(svg));
check("Effet débossage → filtre deboss", /c1r-subtitle[\s\S]{0,200}filter="url\(#c1r-deboss\)"/.test(svg));
check("Hologramme → masque irisé et data-metal", /c1r-title[^>]*data-metal="true"/.test(svg) && svg.includes("c1r-holo-c1r-title"));
svg = render1({ "c1r-name": { text: { size: 4, font: "playfair", weight: 700, italic: true, tracking: 0.5, align: "middle", finish: "whitegold" } } });
const nameText = /data-node-id="c1r-name"[\s\S]*?(<text [^>]*>)/.exec(svg)[1];
check("Typo : corps", nameText.includes('font-size="4"'));
check("Typo : police", nameText.includes("Playfair Display"));
check("Typo : graisse", nameText.includes('font-weight="700"'));
check("Typo : italique", nameText.includes('font-style="italic"'));
check("Typo : interlettrage", nameText.includes('letter-spacing="0.5"'));
check("Typo : alignement", nameText.includes('text-anchor="middle"'));
check("Typo : or blanc métallisé", nameText.includes("foil-whitegold") && /c1r-name[^>]*data-metal="true"/.test(svg));
// Interlignage et corps proportionnels sur un nœud multi-lignes
const multi = '<text x="0" y="10" font-size="2" fill="#000">a</text><text x="0" y="12.4" font-size="1" fill="#000">b</text>';
const styled = C.applyTextStyle(multi, { size: 4, leading: 1.5 }, "p");
check("Corps proportionnel aux lignes suivantes", styled.includes('font-size="2"') && styled.includes('font-size="4"'));
check("Interlignage appliqué (10 + 2,4 × 2 × 1,5 = 17,2)", styled.includes('y="17.2"'));
// Ancien format customPositions toujours lu
svg = C.render(2, "verso", c1, { material: "ivoire", customPositions: { "c2v-wave": { dx: 3, dy: -1 } } }, {});
check("Compatibilité customPositions {dx, dy}", /c2v-wave[\s\S]{0,120}transform="translate\(3 -1\)"/.test(svg) || /transform="translate\(3 -1\)"[^>]*c2v-wave/.test(svg));

// ---------------------------------------------------------------- 3. Cohérence rendu ↔ atelier (même transformation)
function parseTransform(str) {
  let m = [1, 0, 0, 1, 0, 0];
  const mul = (a, b) => [a[0] * b[0] + a[2] * b[1], a[1] * b[0] + a[3] * b[1], a[0] * b[2] + a[2] * b[3], a[1] * b[2] + a[3] * b[3], a[0] * b[4] + a[2] * b[5] + a[4], a[1] * b[4] + a[3] * b[5] + a[5]];
  for (const [, fn, args] of str.matchAll(/(\w+)\(([^)]*)\)/g)) {
    const v = args.split(/[\s,]+/).filter(Boolean).map(Number);
    if (fn === "translate") m = mul(m, [1, 0, 0, 1, v[0], v[1] || 0]);
    else if (fn === "scale") m = mul(m, [v[0], 0, 0, v[1] ?? v[0], 0, 0]);
    else if (fn === "rotate") {
      const a = (v[0] * Math.PI) / 180;
      const cx = v[1] || 0;
      const cy = v[2] || 0;
      m = mul(m, [1, 0, 0, 1, cx, cy]);
      m = mul(m, [Math.cos(a), Math.sin(a), -Math.sin(a), Math.cos(a), 0, 0]);
      m = mul(m, [1, 0, 0, 1, -cx, -cy]);
    }
  }
  return p => ({ x: m[0] * p.x + m[2] * p.y + m[4], y: m[1] * p.x + m[3] * p.y + m[5] });
}
let seed = 7;
const rnd = (a, b) => { seed = (seed * 16807) % 2147483647; return a + ((seed % 10000) / 10000) * (b - a); };
for (let i = 0; i < 200; i++) {
  const rec = { dx: rnd(-20, 20), dy: rnd(-20, 20), sx: rnd(0.2, 3) * (i % 7 ? 1 : -1), sy: rnd(0.2, 3), rot: rnd(0, 360), cx: rnd(0, 85), cy: rnd(0, 54) };
  const tr = parseTransform(C.nodeTransform(rec));
  const pt = { x: rnd(0, 85), y: rnd(0, 54) };
  const a = tr(pt);
  const b = E.math.toWorld(rec, pt);
  if (!near(a.x, b.x, 1e-3) || !near(a.y, b.y, 1e-3)) { check(`transformation #${i}`, false, JSON.stringify({ rec, a, b })); break; }
}
check("200 transformations aléatoires : rendu SVG ≡ géométrie de l'atelier", true);
// Ancre fixe lors du redimensionnement : d' = d + R·(S − S')·(a − c)
{
  const r0 = { dx: 2, dy: -1, sx: 1.2, sy: 0.8, rot: 33, cx: 20, cy: 10 };
  const anchor = { x: 12, y: 6 };
  const w0 = E.math.toWorld(r0, anchor);
  const r1 = Object.assign({}, r0, { sx: 2.1, sy: 1.7 });
  const v = E.math.rotate({ x: (r0.sx - r1.sx) * (anchor.x - r0.cx), y: (r0.sy - r1.sy) * (anchor.y - r0.cy) }, r0.rot);
  r1.dx = r0.dx + v.x;
  r1.dy = r0.dy + v.y;
  const w1 = E.math.toWorld(r1, anchor);
  check("Redimensionnement : la poignée opposée reste fixe", near(w0.x, w1.x) && near(w0.y, w1.y));
}

// ---------------------------------------------------------------- 4. Historique
{
  let state = { v: 0 };
  const persisted = [];
  const h = Hist.create({ capture: () => JSON.stringify(state), restore: s => { state = JSON.parse(s); }, persist: x => persisted.push(x) });
  h.load(null);
  check("Historique : entrée initiale", h.state().entries.length === 1 && !h.canUndo());
  state.v = 1; h.push("a");
  state.v = 2; h.push("b");
  check("Doublon ignoré", h.push("b bis") === false && h.state().entries.length === 3);
  h.undo();
  check("Annuler restaure l'état précédent", state.v === 1 && h.canRedo());
  h.undo();
  check("Annuler jusqu'à l'origine", state.v === 0 && !h.canUndo());
  h.redo(); h.redo();
  check("Rétablir", state.v === 2 && !h.canRedo());
  h.undo();
  state.v = 9; h.push("branche");
  check("Nouvelle action après annulation : la branche de rétablissement est coupée", !h.canRedo() && h.state().entries.length === 3);
  const saved = persisted[persisted.length - 1];
  let state2 = { v: -1 };
  const h2 = Hist.create({ capture: () => JSON.stringify(state2), restore: s => { state2 = JSON.parse(s); } });
  h2.load(JSON.parse(JSON.stringify(saved)));
  check("Rechargement : état et position restaurés", state2.v === 9 && h2.canUndo());
  h2.undo();
  check("Rechargement : annulation possible après réouverture", state2.v === 1);
  for (let i = 0; i < 1500; i++) { state2.v = 100 + i; h2.push(`n${i}`); }
  check("Pile non tronquée (1 500 actions)", h2.state().entries.length > 1500);
}

// ---------------------------------------------------------------- 5. Pré-vol : calculs
check("Contraste noir/blanc = 21:1", near(PF.contrastRatio([0, 0, 0], [255, 255, 255]), 21, 1e-9));
check("Contraste #777/#fff ≈ 4,48:1", near(PF.contrastRatio(PF.parseColor("#777"), PF.parseColor("#fff")), 4.48, 0.01));
check("Couleur rgba lue", JSON.stringify(PF.parseColor("rgba(168,130,47,0.5)")) === "[168,130,47]");
check("Aire d'intersection", PF.intersectArea({ x: 0, y: 0, w: 10, h: 10 }, { x: 5, y: 5, w: 10, h: 10 }) === 25);
check("Aire nulle hors recouvrement", PF.intersectArea({ x: 0, y: 0, w: 1, h: 1 }, { x: 2, y: 2, w: 1, h: 1 }) === 0);
const z = PF.nfcZones(85.6, 53.98, { x: 70, y: 40 });
check("Module de puce 15 × 15 mm centré", near(z.module.x, 62.5) && near(z.module.w, 15));
check("Bande d'antenne : 4 rectangles d'aire positive", z.band.length === 4 && z.bandArea > 0);
check("Seuil micro-texte 0,86 mm (2,44 pt)", PF.CONFIG.microTextMm === 0.86 && near(0.86 / 0.3528, 2.44, 0.01));

console.log(`PaxStudio Design · atelier : ${pass} PASS, ${fail} FAIL`);
process.exit(fail ? 1 : 0);
