/**
 * PaxStudio Design — Atelier de manipulation vectorielle (mode « Atelier »).
 *
 * Travaille directement dans le repère des cartes (viewBox en millimètres) :
 *   - sélection simple / multiple (Maj), cadre de sélection (lasso rectangulaire) ;
 *   - boîte englobante orientée à 8 poignées + poignée de rotation (Maj : ratio / paliers de 45°) ;
 *   - déplacement à la souris et au clavier (flèches 0,1 mm, Maj + flèches 1 mm) ;
 *   - aimantation (centres de la carte, marges de sécurité 3 mm, fond perdu 2 mm, découpe,
 *     bords et centres des autres éléments) avec guides magenta et infobulle X/Y/W/H/angle.
 *
 * La transformation d'un nœud vit dans son enregistrement (design.nodes[id]) :
 *   monde(p) = d + c + R(rot) · S(sx, sy) · (p − c), avec c = centre de référence (cx, cy).
 * Elle est identique à PaxCards.nodeTransform(), utilisée pour le rendu et l'export.
 *
 * Exposé en global `PaxEditor`.
 */
(function (root) {
  "use strict";

  const C = root.PaxCards;
  const W = C.W;
  const H = C.H;
  const SNAP_PX = 7; // seuil d'aimantation en pixels écran
  const HANDLE_PX = 7;
  const ROT_PX = 22;
  const HANDLES = ["nw", "n", "ne", "e", "se", "s", "sw", "w"];
  const r2 = n => Math.round(n * 100) / 100;
  const fmt = n => r2(n).toFixed(2).replace(".", ",");

  // ---------------------------------------------------------------- géométrie
  const rad = a => (a * Math.PI) / 180;
  function rotate(v, deg) {
    const a = rad(deg);
    return { x: v.x * Math.cos(a) - v.y * Math.sin(a), y: v.x * Math.sin(a) + v.y * Math.cos(a) };
  }
  /** Point local (contenu non transformé) → monde (repère carte). */
  function toWorld(rec, p) {
    const cx = rec.cx ?? 0;
    const cy = rec.cy ?? 0;
    const v = rotate({ x: (p.x - cx) * (rec.sx ?? 1), y: (p.y - cy) * (rec.sy ?? 1) }, rec.rot || 0);
    return { x: (rec.dx || 0) + cx + v.x, y: (rec.dy || 0) + cy + v.y };
  }
  function corners(b) {
    return [{ x: b.x, y: b.y }, { x: b.x + b.width, y: b.y }, { x: b.x + b.width, y: b.y + b.height }, { x: b.x, y: b.y + b.height }];
  }
  function aabb(points) {
    const xs = points.map(p => p.x);
    const ys = points.map(p => p.y);
    const x = Math.min(...xs);
    const y = Math.min(...ys);
    return { x, y, w: Math.max(...xs) - x, h: Math.max(...ys) - y };
  }
  function union(boxes) {
    return aabb(boxes.flatMap(b => [{ x: b.x, y: b.y }, { x: b.x + b.w, y: b.y + b.h }]));
  }
  /** Position locale d'une poignée dans la boîte de contenu. */
  function handlePoint(b, h) {
    const x = h.includes("w") ? b.x : h.includes("e") ? b.x + b.width : b.x + b.width / 2;
    const y = h.includes("n") ? b.y : h.includes("s") ? b.y + b.height : b.y + b.height / 2;
    return { x, y };
  }
  const OPPOSITE = { nw: "se", n: "s", ne: "sw", e: "w", se: "nw", s: "n", sw: "ne", w: "e" };

  function create(opts) {
    const api = {};
    const sel = { face: null, ids: [] };
    let enabled = false;
    let action = null;
    let tooltip = null;
    let nudgeTimer = 0;

    // ---------------------------------------------------------------- accès DOM
    function holders() { return opts.getHolders(); }
    function svgOf(face) {
      const h = holders().find(x => x.face === face);
      return h ? h.el.querySelector("svg.card-svg") : null;
    }
    function nodeEl(face, id) {
      const svg = svgOf(face);
      return svg ? svg.querySelector(`.movable-node[data-node-id="${CSS.escape(id)}"]`) : null;
    }
    function svgPoint(svg, ev) {
      const pt = svg.createSVGPoint();
      pt.x = ev.clientX;
      pt.y = ev.clientY;
      return pt.matrixTransform(svg.getScreenCTM().inverse());
    }
    /** Millimètres par pixel écran (pour des poignées de taille constante). */
    function mmPerPx(svg) {
      const m = svg.getScreenCTM();
      return m ? 1 / Math.hypot(m.a, m.b) : 0.1;
    }

    /** Boîte du contenu non transformé d'un nœud (repère local). */
    function contentBox(face, id) {
      const el = nodeEl(face, id);
      if (!el || el.getAttribute("display") === "none") return null;
      const nc = el.querySelector(":scope > .nc, :scope > g > .nc") || el;
      try {
        const b = nc.getBBox();
        return b.width || b.height ? b : null;
      } catch (e) {
        return null;
      }
    }

    /** Garantit le centre de référence d'un nœud (requis pour rotation et échelle). */
    function ensureCenter(face, id) {
      const rec = opts.getRecord(id);
      if (rec.cx == null || rec.cy == null) {
        const b = contentBox(face, id);
        if (b) {
          rec.cx = r2(b.x + b.width / 2);
          rec.cy = r2(b.y + b.height / 2);
        }
      }
      return rec;
    }

    /** Géométrie monde d'un nœud : coins orientés, AABB, taille, angle. */
    function geometry(face, id) {
      const b = contentBox(face, id);
      if (!b) return null;
      const rec = Object.assign({ dx: 0, dy: 0, sx: 1, sy: 1, rot: 0 }, opts.getRecord(id, true) || {});
      if (rec.cx == null) { rec.cx = b.x + b.width / 2; rec.cy = b.y + b.height / 2; }
      const pts = corners(b).map(p => toWorld(rec, p));
      return { box: b, rec, pts, aabb: aabb(pts), w: b.width * Math.abs(rec.sx), h: b.height * Math.abs(rec.sy), rot: rec.rot || 0 };
    }
    api.geometry = geometry;

    /** Tous les nœuds d'une face avec leur géométrie (pour l'aimantation et le pré-vol). */
    function faceNodes(face) {
      const svg = svgOf(face);
      if (!svg) return [];
      return Array.from(svg.querySelectorAll(".movable-node")).map(el => ({
        id: el.dataset.nodeId,
        el,
        kind: el.dataset.kind,
        locked: el.dataset.locked === "true",
        decor: el.dataset.kind === "decor",
        geo: geometry(face, el.dataset.nodeId)
      })).filter(n => n.geo);
    }
    api.faceNodes = faceNodes;

    function applyLive(face, id) {
      const el = nodeEl(face, id);
      if (!el) return;
      const tr = C.nodeTransform(opts.getRecord(id));
      if (tr) el.setAttribute("transform", tr);
      else el.removeAttribute("transform");
    }

    // ---------------------------------------------------------------- superposition (poignées, guides, lasso)
    function overlay(face) {
      const svg = svgOf(face);
      if (!svg) return null;
      let g = svg.querySelector(":scope > g.ed-overlay");
      if (!g) {
        g = document.createElementNS("http://www.w3.org/2000/svg", "g");
        g.setAttribute("class", "ed-overlay");
        svg.appendChild(g);
      }
      return g;
    }

    function draw(extra) {
      holders().forEach(h => {
        const svg = h.el.querySelector("svg.card-svg");
        if (!svg) return;
        const ov = svg.querySelector(":scope > g.ed-overlay");
        if (ov) ov.remove();
      });
      if (!enabled) return;
      holders().forEach(h => h.el.classList.toggle("ed-active-face", h.face === sel.face));
      const face = sel.face;
      const ov = face && overlay(face);
      if (!ov) return;
      const svg = svgOf(face);
      const k = mmPerPx(svg);
      let html = "";
      const geos = sel.ids.map(id => ({ id, g: geometry(face, id) })).filter(x => x.g);
      for (const { g } of geos) {
        html += `<polygon class="ed-box" points="${g.pts.map(p => `${r2(p.x)},${r2(p.y)}`).join(" ")}" stroke-width="${k * 1.2}"/>`;
      }
      if (geos.length === 1 && !opts.isLocked(geos[0].id)) {
        const { g } = geos[0];
        const hs = HANDLE_PX * k;
        for (const h of HANDLES) {
          const p = toWorld(g.rec, handlePoint(g.box, h));
          html += `<rect class="ed-handle h-${h}" data-handle="${h}" x="${r2(p.x - hs / 2)}" y="${r2(p.y - hs / 2)}" width="${hs}" height="${hs}" stroke-width="${k}" transform="rotate(${r2(g.rot)} ${r2(p.x)} ${r2(p.y)})"/>`;
        }
        const top = toWorld(g.rec, handlePoint(g.box, "n"));
        const up = rotate({ x: 0, y: -ROT_PX * k }, g.rot);
        const rp = { x: top.x + up.x, y: top.y + up.y };
        html += `<line class="ed-rotline" x1="${r2(top.x)}" y1="${r2(top.y)}" x2="${r2(rp.x)}" y2="${r2(rp.y)}" stroke-width="${k}"/>`;
        html += `<circle class="ed-handle h-rot" data-handle="rot" cx="${r2(rp.x)}" cy="${r2(rp.y)}" r="${hs * 0.6}" stroke-width="${k}"/>`;
      } else if (geos.length > 1) {
        const u = union(geos.map(x => x.g.aabb));
        html += `<rect class="ed-group" x="${r2(u.x)}" y="${r2(u.y)}" width="${r2(u.w)}" height="${r2(u.h)}" stroke-width="${k}" stroke-dasharray="${k * 4} ${k * 3}"/>`;
      }
      if (extra && extra.guides) {
        for (const gd of extra.guides) {
          html += gd.axis === "x"
            ? `<line class="ed-guide" x1="${r2(gd.at)}" y1="-4" x2="${r2(gd.at)}" y2="${r2(H + 4)}" stroke-width="${k}"/>`
            : `<line class="ed-guide" x1="-4" y1="${r2(gd.at)}" x2="${r2(W + 4)}" y2="${r2(gd.at)}" stroke-width="${k}"/>`;
        }
      }
      if (extra && extra.marquee) {
        const m = extra.marquee;
        html += `<rect class="ed-marquee" x="${r2(m.x)}" y="${r2(m.y)}" width="${r2(m.w)}" height="${r2(m.h)}" stroke-width="${k}"/>`;
      }
      if (extra && extra.zones) html += extra.zones;
      ov.innerHTML = html;
    }
    api.redraw = () => draw(api.persistentOverlay ? { zones: api.persistentOverlay() } : null);

    // ---------------------------------------------------------------- infobulle
    function tip(ev, text) {
      if (!tooltip) {
        tooltip = document.createElement("div");
        tooltip.className = "ed-tooltip";
        document.body.appendChild(tooltip);
      }
      if (!text) { tooltip.hidden = true; return; }
      tooltip.hidden = false;
      tooltip.textContent = text;
      tooltip.style.left = `${ev.clientX + 16}px`;
      tooltip.style.top = `${ev.clientY + 18}px`;
    }
    function geoText(face) {
      const geos = sel.ids.map(id => geometry(face, id)).filter(Boolean);
      if (!geos.length) return "";
      const u = union(geos.map(g => g.aabb));
      const wh = geos.length === 1 ? { w: geos[0].w, h: geos[0].h } : { w: u.w, h: u.h };
      return `X ${fmt(u.x)} · Y ${fmt(u.y)} mm   W ${fmt(wh.w)} · H ${fmt(wh.h)} mm`;
    }

    // ---------------------------------------------------------------- aimantation
    function snapTargets(face, exclude) {
      const xs = [{ at: W / 2, label: "centre" }, { at: 3 }, { at: W - 3 }, { at: -2 }, { at: W + 2 }, { at: 0 }, { at: W }];
      const ys = [{ at: H / 2, label: "centre" }, { at: 3 }, { at: H - 3 }, { at: -2 }, { at: H + 2 }, { at: 0 }, { at: H }];
      for (const n of faceNodes(face)) {
        if (exclude.includes(n.id) || n.decor || n.el.getAttribute("display") === "none") continue;
        const b = n.geo.aabb;
        xs.push({ at: b.x }, { at: b.x + b.w / 2 }, { at: b.x + b.w });
        ys.push({ at: b.y }, { at: b.y + b.h / 2 }, { at: b.y + b.h });
      }
      return { xs, ys };
    }
    /** Décalage d'aimantation d'une boîte sur un axe ; renvoie { off, guide }. */
    function snapAxis(cands, targets, thr) {
      let best = null;
      for (const c of cands) {
        for (const t of targets) {
          const d = t.at - c;
          if (Math.abs(d) <= thr && (!best || Math.abs(d) < Math.abs(best.off))) best = { off: d, at: t.at };
        }
      }
      return best;
    }

    // ---------------------------------------------------------------- interactions pointeur
    function onPointerDown(ev, face) {
      if (!enabled || ev.button !== 0) return;
      const svg = svgOf(face);
      if (!svg) return;
      const p = svgPoint(svg, ev);
      const handle = ev.target.closest("[data-handle]");
      const nodeElt = ev.target.closest(".movable-node");
      ev.preventDefault();
      svg.setPointerCapture(ev.pointerId);

      if (handle && sel.face === face && sel.ids.length === 1) {
        const id = sel.ids[0];
        const rec = ensureCenter(face, id);
        const g = geometry(face, id);
        action = { type: handle.dataset.handle === "rot" ? "rotate" : "resize", handle: handle.dataset.handle, face, id, svg,
          start: p, rec0: Object.assign({}, rec), box: g.box,
          center: toWorld(rec, { x: rec.cx, y: rec.cy }) };
        return;
      }

      let id = nodeElt && nodeElt.dataset.nodeId;
      let selectable = id && !opts.isLocked(id);
      if (!selectable) {
        // Repli : calque déverrouillé le plus haut dont la boîte contient le point (clic entre deux glyphes).
        const hit = faceNodes(face).filter(n => !opts.isLocked(n.id) && n.el.getAttribute("display") !== "none" &&
          p.x >= n.geo.aabb.x && p.x <= n.geo.aabb.x + n.geo.aabb.w && p.y >= n.geo.aabb.y && p.y <= n.geo.aabb.y + n.geo.aabb.h).pop();
        if (hit) { id = hit.id; selectable = true; }
      }
      if (selectable) {
        if (sel.face !== face) { sel.face = face; sel.ids = []; }
        if (ev.shiftKey) {
          sel.ids = sel.ids.includes(id) ? sel.ids.filter(x => x !== id) : sel.ids.concat(id);
        } else if (!sel.ids.includes(id)) {
          sel.ids = [id];
        }
        opts.onSelect(api.getSelection());
        if (!sel.ids.includes(id)) { draw(); return; }
        const recs = sel.ids.filter(x => !opts.isLocked(x)).map(x => ({ id: x, rec0: Object.assign({ dx: 0, dy: 0 }, opts.getRecord(x, true) || {}) }));
        action = { type: "move", face, svg, start: p, recs, targets: snapTargets(face, sel.ids),
          box0: union(sel.ids.map(x => geometry(face, x)).filter(Boolean).map(g => g.aabb)), moved: false };
        draw();
        return;
      }

      // Fond : cadre de sélection
      if (sel.face !== face || !ev.shiftKey) {
        sel.face = face;
        sel.ids = ev.shiftKey ? sel.ids : [];
        opts.onSelect(api.getSelection());
      }
      action = { type: "marquee", face, svg, start: p, base: sel.ids.slice() };
      draw();
    }

    function onPointerMove(ev) {
      if (!action) return;
      const { svg, face } = action;
      const p = svgPoint(svg, ev);
      const thr = SNAP_PX * mmPerPx(svg);
      const snapOn = !ev.altKey;

      if (action.type === "move") {
        let dx = p.x - action.start.x;
        let dy = p.y - action.start.y;
        if (Math.abs(dx) + Math.abs(dy) > 0.02) action.moved = true;
        const guides = [];
        if (snapOn) {
          const b = action.box0;
          const sx = snapAxis([b.x + dx, b.x + b.w / 2 + dx, b.x + b.w + dx], action.targets.xs, thr);
          const sy = snapAxis([b.y + dy, b.y + b.h / 2 + dy, b.y + b.h + dy], action.targets.ys, thr);
          if (sx) { dx += sx.off; guides.push({ axis: "x", at: sx.at }); }
          if (sy) { dy += sy.off; guides.push({ axis: "y", at: sy.at }); }
        }
        for (const r of action.recs) {
          const rec = opts.getRecord(r.id);
          rec.dx = r2((r.rec0.dx || 0) + dx);
          rec.dy = r2((r.rec0.dy || 0) + dy);
          applyLive(face, r.id);
        }
        draw({ guides });
        tip(ev, geoText(face));
        return;
      }

      if (action.type === "rotate") {
        const c = action.center;
        const a0 = Math.atan2(action.start.y - c.y, action.start.x - c.x);
        const a1 = Math.atan2(p.y - c.y, p.x - c.x);
        let deg = (action.rec0.rot || 0) + ((a1 - a0) * 180) / Math.PI;
        deg = ((deg % 360) + 360) % 360;
        if (ev.shiftKey) deg = (Math.round(deg / 45) * 45) % 360;
        const rec = opts.getRecord(action.id);
        rec.rot = r2(deg);
        applyLive(face, action.id);
        draw();
        tip(ev, `Rotation ${fmt(deg)}°`);
        return;
      }

      if (action.type === "resize") {
        const r0 = action.rec0;
        const rec = opts.getRecord(action.id);
        const b = action.box;
        const h = action.handle;
        const anchorL = handlePoint(b, OPPOSITE[h]);
        const handleL = handlePoint(b, h);
        const anchorW = toWorld(r0, anchorL);
        let pp = p;
        // Aimantation des bords tirés (élément non pivoté)
        const guides = [];
        if (snapOn && !(r0.rot % 360)) {
          const t = snapTargets(face, [action.id]);
          const ax = h.includes("e") || h.includes("w") ? snapAxis([p.x], t.xs, thr) : null;
          const ay = h.includes("n") || h.includes("s") ? snapAxis([p.y], t.ys, thr) : null;
          pp = { x: p.x + (ax ? ax.off : 0), y: p.y + (ay ? ay.off : 0) };
          if (ax) guides.push({ axis: "x", at: ax.at });
          if (ay) guides.push({ axis: "y", at: ay.at });
        }
        const v = rotate({ x: pp.x - anchorW.x, y: pp.y - anchorW.y }, -(r0.rot || 0));
        const wv = { x: handleL.x - anchorL.x, y: handleL.y - anchorL.y };
        let sx = r0.sx ?? 1;
        let sy = r0.sy ?? 1;
        if (Math.abs(wv.x) > 1e-6) sx = v.x / wv.x;
        if (Math.abs(wv.y) > 1e-6) sy = v.y / wv.y;
        const clamp = s => (Math.abs(s) < 0.05 ? 0.05 * (s < 0 ? -1 : 1) : s);
        sx = clamp(sx);
        sy = clamp(sy);
        if (ev.shiftKey) {
          const ratio0 = (r0.sy ?? 1) / (r0.sx ?? 1);
          if (h === "n" || h === "s") sx = sy / ratio0;
          else if (h === "e" || h === "w") sy = sx * ratio0;
          else {
            const k = Math.max(Math.abs(sx / (r0.sx ?? 1)), Math.abs(sy / (r0.sy ?? 1)));
            sx = (r0.sx ?? 1) * k * Math.sign(sx || 1);
            sy = (r0.sy ?? 1) * k * Math.sign(sy || 1);
          }
        }
        rec.sx = r2(sx * 1000) / 1000;
        rec.sy = r2(sy * 1000) / 1000;
        // L'ancre (poignée opposée) reste fixe : d' = d + R·(S − S')·(a − c)
        const ac = { x: anchorL.x - r0.cx, y: anchorL.y - r0.cy };
        const corr = rotate({ x: ((r0.sx ?? 1) - rec.sx) * ac.x, y: ((r0.sy ?? 1) - rec.sy) * ac.y }, r0.rot || 0);
        rec.dx = r2((r0.dx || 0) + corr.x);
        rec.dy = r2((r0.dy || 0) + corr.y);
        applyLive(face, action.id);
        draw({ guides });
        tip(ev, geoText(face));
        return;
      }

      if (action.type === "marquee") {
        const m = aabb([action.start, p]);
        const hits = faceNodes(face).filter(n => !opts.isLocked(n.id) && n.el.getAttribute("display") !== "none" &&
          n.geo.aabb.x < m.x + m.w && n.geo.aabb.x + n.geo.aabb.w > m.x && n.geo.aabb.y < m.y + m.h && n.geo.aabb.y + n.geo.aabb.h > m.y).map(n => n.id);
        sel.ids = Array.from(new Set(action.base.concat(hits)));
        draw({ marquee: m });
      }
    }

    function onPointerUp(ev) {
      if (!action) return;
      const a = action;
      action = null;
      tip(ev, "");
      try { a.svg.releasePointerCapture(ev.pointerId); } catch (e) { /* déjà relâché */ }
      if (a.type === "move" && a.moved) opts.onCommit(sel.ids.length > 1 ? `Déplacement de ${sel.ids.length} éléments` : "Déplacement");
      else if (a.type === "rotate") opts.onCommit("Rotation");
      else if (a.type === "resize") opts.onCommit("Redimensionnement");
      opts.onSelect(api.getSelection());
      draw();
    }

    // ---------------------------------------------------------------- clavier
    function onKey(ev) {
      if (!enabled) return;
      const t = ev.target;
      if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
      const mod = ev.ctrlKey || ev.metaKey;
      if (mod && ev.key.toLowerCase() === "a" && sel.face) {
        ev.preventDefault();
        sel.ids = faceNodes(sel.face).filter(n => !opts.isLocked(n.id) && n.el.getAttribute("display") !== "none").map(n => n.id);
        opts.onSelect(api.getSelection());
        draw();
        return;
      }
      if (!sel.ids.length) return;
      const steps = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1] };
      if (steps[ev.key] && !mod) {
        ev.preventDefault();
        const step = ev.shiftKey ? 1 : 0.1;
        for (const id of sel.ids) {
          if (opts.isLocked(id)) continue;
          const rec = opts.getRecord(id);
          rec.dx = r2((rec.dx || 0) + steps[ev.key][0] * step);
          rec.dy = r2((rec.dy || 0) + steps[ev.key][1] * step);
          applyLive(sel.face, id);
        }
        draw();
        clearTimeout(nudgeTimer);
        nudgeTimer = setTimeout(() => opts.onCommit(`Décalage clavier (${ev.shiftKey ? "1 mm" : "0,1 mm"})`), 450);
        return;
      }
      if (ev.key === "Escape") {
        sel.ids = [];
        opts.onSelect(api.getSelection());
        draw();
      } else if (ev.key === "Delete" || ev.key === "Backspace") {
        ev.preventDefault();
        for (const id of sel.ids) opts.getRecord(id).hidden = true;
        sel.ids = [];
        opts.onCommit("Masquer");
      }
    }

    // ---------------------------------------------------------------- cycle de vie
    const bound = new WeakSet();
    api.attach = function () {
      for (const h of holders()) {
        if (bound.has(h.el)) continue;
        bound.add(h.el);
        const el = h.el;
        el.addEventListener("pointerdown", ev => {
          const cur = holders().find(x => x.el === el);
          if (cur) onPointerDown(ev, cur.face);
        });
        el.addEventListener("pointermove", onPointerMove);
        el.addEventListener("pointerup", onPointerUp);
        el.addEventListener("pointercancel", onPointerUp);
      }
      if (sel.face && !holders().some(h => h.face === sel.face)) { sel.face = null; sel.ids = []; }
      api.redraw();
    };
    api.setEnabled = on => {
      enabled = !!on;
      if (!enabled) { sel.ids = []; holders().forEach(h => h.el.classList.remove("ed-active-face")); }
      api.redraw();
    };
    api.isEnabled = () => enabled;
    api.getSelection = () => ({ face: sel.face, ids: sel.ids.slice() });
    api.select = (face, ids) => {
      sel.face = face;
      sel.ids = (ids || []).slice();
      opts.onSelect(api.getSelection());
      api.redraw();
    };
    api.toWorld = toWorld;
    api.ensureCenter = ensureCenter;
    api.applyLive = applyLive;
    document.addEventListener("keydown", onKey);
    return api;
  }

  root.PaxEditor = { create, math: { toWorld, rotate, aabb, handlePoint } };
})(typeof self !== "undefined" ? self : this);
