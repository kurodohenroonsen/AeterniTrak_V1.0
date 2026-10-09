/**
 * PaxStudio Design — Panneaux de l'atelier : Calques, Inspecteur, Ennoblissement, Pré-vol, Historique.
 * Exposé en global `PaxStudio`. Toute la logique d'état passe par l'objet `host` fourni par app.js.
 */
(function (root) {
  "use strict";

  const C = root.PaxCards;
  const P = root.PaxPreflight;
  const PT = 1 / 0.3528;
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, ch => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]));
  const num = (v, d = 2) => Number(v).toFixed(d).replace(".", ",");
  const ico = d => `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="${d}" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
  const I = {
    eye: "M2.5 12s3.5-6.5 9.5-6.5S21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12zM12 9a3 3 0 1 0 0 6 3 3 0 1 0 0-6z",
    eyeOff: "M3 3l18 18M10.6 6.1A9.8 9.8 0 0 1 12 6c6 0 9.5 6 9.5 6a17 17 0 0 1-3 3.6M6.3 7.4C3.9 9 2.5 12 2.5 12s3.5 6.5 9.5 6.5c1.6 0 3-.4 4.3-1",
    lock: "M6 11h12v10H6zM8.5 11V8a3.5 3.5 0 0 1 7 0v3",
    unlock: "M6 11h12v10H6zM8.5 11V8a3.5 3.5 0 0 1 6.8-1.2",
    text: "M5 6V4h14v2M12 4v16M9 20h6",
    image: "M3 5h18v14H3zM3 16l5-5 4 4 3-3 6 6M15.5 8.5h.1",
    group: "M4 4h7v7H4zM13 13h7v7h-7zM13 4h7v7h-7z",
    decor: "M12 3a9 9 0 1 0 0 18 9 9 0 1 0 0-18zM12 7a5 5 0 1 0 0 10 5 5 0 1 0 0-10z",
    nfc: "M6 8.5a5 5 0 0 1 0 7M9.5 6a8.5 8.5 0 0 1 0 12M13 3.5a12 12 0 0 1 0 17",
    front: "M12 20V8M6 14l6-6 6 6M5 4h14",
    up: "M12 19V5M6 11l6-6 6 6",
    down: "M12 5v14M6 13l6 6 6-6",
    back: "M12 4v12M6 10l6 6 6-6M5 20h14",
    grip: "M9 6h.1M15 6h.1M9 12h.1M15 12h.1M9 18h.1M15 18h.1"
  };

  function create(host) {
    const el = document.getElementById("studio");
    let tab = "layers";
    let layerFace = null;
    let lastPreflight = null;
    const api = {};

    // ---------------------------------------------------------------- squelette
    el.innerHTML = `
      <nav class="studio-tabs" role="tablist">
        <button data-stab="layers" class="on" role="tab">Calques</button>
        <button data-stab="inspect" role="tab">Inspecteur</button>
        <button data-stab="finish" role="tab">Ennoblissement</button>
        <button data-stab="preflight" role="tab">Pré-vol <b class="pf-badge" id="pfBadge"></b></button>
        <button data-stab="history" role="tab">Historique</button>
      </nav>
      <section class="spane" data-spane="layers"></section>
      <section class="spane" data-spane="inspect" hidden></section>
      <section class="spane" data-spane="finish" hidden></section>
      <section class="spane" data-spane="preflight" hidden></section>
      <section class="spane" data-spane="history" hidden></section>`;
    const pane = k => el.querySelector(`[data-spane="${k}"]`);
    el.querySelectorAll("[data-stab]").forEach(b => b.addEventListener("click", () => {
      tab = b.dataset.stab;
      el.querySelectorAll("[data-stab]").forEach(x => x.classList.toggle("on", x === b));
      el.querySelectorAll("[data-spane]").forEach(p => { p.hidden = p.dataset.spane !== tab; });
      api.refresh();
    }));

    const sel = () => host.editor.getSelection();
    const faces = () => [`${host.currentCard()}recto`, `${host.currentCard()}verso`];
    function activeFace() {
      const s = sel();
      if (s.face && faces().includes(s.face)) return s.face;
      if (!layerFace || !faces().includes(layerFace)) layerFace = faces()[0];
      return layerFace;
    }
    /** Nœuds d'une face dans l'ordre de superposition (premier plan en tête). */
    function layerList(face) {
      return (C.NODE_INDEX[face] || []).slice().sort((a, b) => b.z - a.z || b.order - a.order);
    }

    // ---------------------------------------------------------------- Calques
    function renderLayers() {
      const face = activeFace();
      const s = sel();
      const list = layerList(face);
      pane("layers").innerHTML = `
        <div class="seg face-switch">${faces().map(f => `<button data-face="${f}" class="${f === face ? "on" : ""}">${f.endsWith("recto") ? "Recto" : "Verso"}</button>`).join("")}</div>
        <div class="zbar" role="toolbar" aria-label="Ordre de superposition">
          <button data-z="front" title="Premier plan">${ico(I.front)}</button><button data-z="up" title="Monter">${ico(I.up)}</button>
          <button data-z="down" title="Descendre">${ico(I.down)}</button><button data-z="back" title="Arrière-plan">${ico(I.back)}</button>
          <span class="count">${list.length} calques</span>
        </div>
        <ol class="layers" id="layerList">${list.map(n => {
          const rec = host.getRecord(n.id, true) || {};
          const locked = host.isLocked(n.id);
          return `<li draggable="true" data-id="${esc(n.id)}" class="${s.face === face && s.ids.includes(n.id) ? "sel" : ""} ${rec.hidden ? "is-hidden" : ""}">
            <span class="grip">${ico(I.grip)}</span>
            <button class="lv" data-act="vis" title="${rec.hidden ? "Afficher" : "Masquer"}">${ico(rec.hidden ? I.eyeOff : I.eye)}</button>
            <button class="lv ${locked ? "on" : ""}" data-act="lock" title="${locked ? "Déverrouiller" : "Verrouiller"}">${ico(locked ? I.lock : I.unlock)}</button>
            <span class="kind">${ico(I[n.kind] || I.group)}</span>
            <span class="lname" title="Double-cliquer pour renommer">${esc(n.label)}</span>
          </li>`;
        }).join("")}</ol>
        <p class="hint">Glisser pour réordonner · double-clic pour renommer · Maj+clic pour sélection multiple.</p>`;
    }

    function setZOrder(face, orderedIds) {
      // orderedIds : arrière-plan → premier plan
      orderedIds.forEach((id, i) => { host.getRecord(id).z = i; });
    }

    function onLayersClick(ev) {
      const face = activeFace();
      const fb = ev.target.closest("[data-face]");
      if (fb) { layerFace = fb.dataset.face; host.editor.select(fb.dataset.face, []); return; }
      const zb = ev.target.closest("[data-z]");
      if (zb) {
        const s = sel();
        if (!s.ids.length) { host.toast("Sélectionnez d'abord un calque."); return; }
        const order = layerList(face).reverse().map(n => n.id); // arrière → avant
        const picked = order.filter(id => s.ids.includes(id));
        let rest = order.filter(id => !s.ids.includes(id));
        let next;
        if (zb.dataset.z === "front") next = rest.concat(picked);
        else if (zb.dataset.z === "back") next = picked.concat(rest);
        else {
          next = order.slice();
          const dir = zb.dataset.z === "up" ? 1 : -1;
          const idxs = picked.map(id => next.indexOf(id)).sort((a, b) => dir * (b - a));
          for (const i of idxs) {
            const j = i + dir;
            if (j < 0 || j >= next.length || picked.includes(next[j])) continue;
            [next[i], next[j]] = [next[j], next[i]];
          }
        }
        setZOrder(face, next);
        host.commit({ "front": "Premier plan", "back": "Arrière-plan", "up": "Monter d'un niveau", "down": "Descendre d'un niveau" }[zb.dataset.z]);
        return;
      }
      const li = ev.target.closest("li[data-id]");
      if (!li) return;
      const id = li.dataset.id;
      const act = ev.target.closest("[data-act]");
      if (act) {
        const rec = host.getRecord(id);
        if (act.dataset.act === "vis") { rec.hidden = !rec.hidden; host.commit(rec.hidden ? "Masquer le calque" : "Afficher le calque"); }
        else { rec.locked = !host.isLocked(id); host.commit(rec.locked ? "Verrouiller le calque" : "Déverrouiller le calque"); }
        return;
      }
      if (host.isLocked(id)) { host.toast("Calque verrouillé : déverrouillez-le pour le sélectionner sur la carte."); }
      const s = sel();
      const ids = ev.shiftKey && s.face === face ? (s.ids.includes(id) ? s.ids.filter(x => x !== id) : s.ids.concat(id)) : [id];
      host.editor.select(face, ids.filter(x => !host.isLocked(x)).length ? ids.filter(x => !host.isLocked(x)) : []);
    }

    function onLayersDblClick(ev) {
      const name = ev.target.closest(".lname");
      if (!name) return;
      const li = name.closest("li");
      const id = li.dataset.id;
      const input = document.createElement("input");
      input.className = "rename";
      input.value = name.textContent;
      name.replaceWith(input);
      input.focus();
      input.select();
      const done = ok => {
        if (ok && input.value.trim()) { host.getRecord(id).name = input.value.trim(); host.commit("Renommer le calque"); }
        else renderLayers();
      };
      input.addEventListener("keydown", e => { if (e.key === "Enter") done(true); if (e.key === "Escape") done(false); });
      input.addEventListener("blur", () => done(true), { once: true });
    }

    let dragId = null;
    function bindLayerDnD(container) {
      container.addEventListener("dragstart", e => {
        const li = e.target.closest("li[data-id]");
        if (!li) return;
        dragId = li.dataset.id;
        e.dataTransfer.effectAllowed = "move";
        e.dataTransfer.setData("text/plain", dragId);
        li.classList.add("dragging");
      });
      container.addEventListener("dragover", e => {
        const li = e.target.closest("li[data-id]");
        if (!li || !dragId) return;
        e.preventDefault();
        const r = li.getBoundingClientRect();
        container.querySelectorAll(".drop-before,.drop-after").forEach(x => x.classList.remove("drop-before", "drop-after"));
        li.classList.add(e.clientY < r.top + r.height / 2 ? "drop-before" : "drop-after");
      });
      container.addEventListener("drop", e => {
        const li = e.target.closest("li[data-id]");
        if (!li || !dragId) return;
        e.preventDefault();
        const face = activeFace();
        const top = layerList(face).map(n => n.id).filter(id => id !== dragId); // premier plan → arrière
        let i = top.indexOf(li.dataset.id);
        if (li.classList.contains("drop-after")) i += 1;
        top.splice(i, 0, dragId);
        setZOrder(face, top.reverse());
        dragId = null;
        host.commit("Réorganisation des calques");
      });
      container.addEventListener("dragend", () => {
        dragId = null;
        container.querySelectorAll(".dragging,.drop-before,.drop-after").forEach(x => x.classList.remove("dragging", "drop-before", "drop-after"));
      });
    }
    pane("layers").addEventListener("click", onLayersClick);
    pane("layers").addEventListener("dblclick", onLayersDblClick);
    bindLayerDnD(pane("layers"));

    // ---------------------------------------------------------------- Inspecteur
    function firstText(face, id) {
      const g = host.editor.faceNodes(face).find(n => n.id === id);
      return g ? g.el.querySelector("text") : null;
    }
    function fontKey(stack) {
      const hit = Object.entries(C.FONTS).find(([, v]) => v.stack.replace(/&#39;/g, "'") === String(stack).replace(/&#39;/g, "'"));
      return hit ? hit[0] : "";
    }

    function renderInspect() {
      const s = sel();
      const p = pane("inspect");
      if (!s.ids.length) {
        p.innerHTML = `<p class="hint">Activez l'atelier puis sélectionnez un élément sur la carte ou dans les calques.</p>`;
        return;
      }
      const geos = s.ids.map(id => host.editor.geometry(s.face, id)).filter(Boolean);
      if (!geos.length) { p.innerHTML = `<p class="hint">Élément masqué.</p>`; return; }
      const u = geos.reduce((a, g) => ({ x: Math.min(a.x, g.aabb.x), y: Math.min(a.y, g.aabb.y) }), { x: Infinity, y: Infinity });
      const single = s.ids.length === 1 ? s.ids[0] : null;
      const g = geos[0];
      const rec = single ? (host.getRecord(single, true) || {}) : {};
      const label = single ? ((C.NODE_INDEX[s.face] || []).find(n => n.id === single) || {}).label : `${s.ids.length} éléments`;
      let html = `<h4 class="ins-title">${esc(label)}</h4>
        <div class="ins-grid">
          <label>X <span class="u">mm</span><input type="number" step="0.1" data-geo="x" value="${u.x.toFixed(2)}"></label>
          <label>Y <span class="u">mm</span><input type="number" step="0.1" data-geo="y" value="${u.y.toFixed(2)}"></label>
          ${single ? `<label>W <span class="u">mm</span><input type="number" step="0.1" min="0.1" data-geo="w" value="${g.w.toFixed(2)}"></label>
          <label>H <span class="u">mm</span><input type="number" step="0.1" min="0.1" data-geo="h" value="${g.h.toFixed(2)}"></label>
          <label>Rotation <span class="u">°</span><input type="number" step="1" data-geo="rot" value="${(rec.rot || 0).toFixed(1)}"></label>
          <label>Opacité <span class="u">%</span><input type="number" step="5" min="0" max="100" data-geo="opacity" value="${Math.round((rec.opacity ?? 1) * 100)}"></label>` : ""}
        </div>
        ${single ? `<label class="check"><input type="checkbox" id="insRatio" checked> Conserver les proportions</label>` : ""}`;
      const t = single && firstText(s.face, single);
      if (t) {
        const st = rec.text || {};
        const scale = Math.sqrt(Math.abs((rec.sx ?? 1) * (rec.sy ?? 1)));
        const size = Number(st.size || t.getAttribute("font-size")) || 1;
        const font = st.font || fontKey(t.getAttribute("font-family"));
        const weight = String(st.weight || t.getAttribute("font-weight") || 400);
        const italic = st.italic ?? t.getAttribute("font-style") === "italic";
        const tracking = st.tracking ?? Number(t.getAttribute("letter-spacing") || 0);
        const align = st.align || t.getAttribute("text-anchor") || "start";
        html += `<h4 class="ins-sub">Typographie</h4>
          <label>Police<select data-ts="font"><option value="">(d'origine)</option>${Object.entries(C.FONTS).map(([k, v]) => `<option value="${k}" ${k === font ? "selected" : ""} style="font-family:${esc(v.stack)}">${v.label}</option>`).join("")}</select></label>
          <label>Corps <output>${num(size)} mm · ${num(size * PT, 1)} pt${scale !== 1 ? ` · effectif ${num(size * scale)} mm` : ""}</output>
            <div class="rng"><input type="range" min="0.86" max="12" step="0.01" data-ts="size" value="${Math.max(0.86, size)}"><input type="number" min="0.86" max="12" step="0.01" data-ts="size" value="${size.toFixed(2)}"></div></label>
          <div class="ins-row">
            <label>Graisse<select data-ts="weight">${["400", "600", "700"].map(w => `<option ${w === weight ? "selected" : ""}>${w}</option>`).join("")}</select></label>
            <label class="check"><input type="checkbox" data-ts="italic" ${italic ? "checked" : ""}> Italique</label>
          </div>
          <label>Interlettrage <output>${num(tracking)} mm</output><input type="range" min="-0.5" max="2" step="0.01" data-ts="tracking" value="${tracking}"></label>
          <label>Interlignage <output>× ${num(st.leading || 1)}</output><input type="range" min="0.6" max="2.5" step="0.05" data-ts="leading" value="${st.leading || 1}"></label>
          <div class="seg align">${[["start", "Gauche"], ["middle", "Centre"], ["end", "Droite"]].map(([v, l]) => `<button data-align="${v}" class="${v === align ? "on" : ""}">${l}</button>`).join("")}</div>
          <label>Couleur & ennoblissement<select data-ts="finish"><option value="">(d'origine)</option>${Object.entries(C.FINISHES).map(([k, v]) => `<option value="${k}" ${k === st.finish ? "selected" : ""}>${v.label}</option>`).join("")}<option value="custom" ${st.color && !st.finish ? "selected" : ""}>Couleur personnalisée…</option></select></label>
          <input type="color" data-ts="color" value="${st.color || "#2a2219"}" ${st.color && !st.finish ? "" : "hidden"}>
          <button class="btn ghost small" data-act="reset-text">Rétablir le style d'origine</button>`;
      }
      if (single) {
        html += `<h4 class="ins-sub">Calque</h4>
          <label>Nom<input data-act-input="name" value="${esc(label)}"></label>
          <button class="btn ghost small" data-act="reset-node">Réinitialiser la transformation</button>`;
      }
      p.innerHTML = html;
    }

    function onInspectInput(ev) {
      const s = sel();
      if (!s.ids.length) return;
      const t = ev.target;
      if (t.dataset.geo) {
        const v = Number(t.value);
        if (!Number.isFinite(v)) return;
        const geos = s.ids.map(id => ({ id, g: host.editor.geometry(s.face, id) })).filter(x => x.g);
        const u = geos.reduce((a, x) => ({ x: Math.min(a.x, x.g.aabb.x), y: Math.min(a.y, x.g.aabb.y) }), { x: Infinity, y: Infinity });
        if (t.dataset.geo === "x" || t.dataset.geo === "y") {
          const d = v - (t.dataset.geo === "x" ? u.x : u.y);
          for (const { id } of geos) {
            const rec = host.getRecord(id);
            if (t.dataset.geo === "x") rec.dx = Math.round(((rec.dx || 0) + d) * 100) / 100;
            else rec.dy = Math.round(((rec.dy || 0) + d) * 100) / 100;
          }
        } else {
          const id = s.ids[0];
          const rec = host.editor.ensureCenter(s.face, id);
          const g = geos[0].g;
          const keep = el.querySelector("#insRatio") && el.querySelector("#insRatio").checked;
          if (t.dataset.geo === "w" && v > 0) {
            const k = v / g.box.width / Math.abs(rec.sx ?? 1);
            rec.sx = (rec.sx ?? 1) * k;
            if (keep) rec.sy = (rec.sy ?? 1) * k;
          } else if (t.dataset.geo === "h" && v > 0) {
            const k = v / g.box.height / Math.abs(rec.sy ?? 1);
            rec.sy = (rec.sy ?? 1) * k;
            if (keep) rec.sx = (rec.sx ?? 1) * k;
          } else if (t.dataset.geo === "rot") {
            rec.rot = ((v % 360) + 360) % 360;
          } else if (t.dataset.geo === "opacity") {
            rec.opacity = Math.min(1, Math.max(0, v / 100));
          }
        }
        host.commit("Géométrie (inspecteur)", true);
        return;
      }
      if (t.dataset.ts) {
        const id = s.ids[0];
        const rec = host.getRecord(id);
        rec.text = rec.text || {};
        const k = t.dataset.ts;
        if (k === "italic") rec.text.italic = t.checked;
        else if (k === "finish") {
          if (t.value === "custom") { delete rec.text.finish; rec.text.color = rec.text.color || "#2a2219"; }
          else if (t.value) { rec.text.finish = t.value; delete rec.text.color; }
          else { delete rec.text.finish; delete rec.text.color; }
        } else if (k === "color") { rec.text.color = t.value; delete rec.text.finish; }
        else if (k === "font") { if (t.value) rec.text.font = t.value; else delete rec.text.font; }
        else rec.text[k] = k === "weight" ? Number(t.value) : Number(t.value);
        host.commit("Typographie", true);
        return;
      }
      if (t.dataset.actInput === "name" && ev.type === "change") {
        host.getRecord(s.ids[0]).name = t.value.trim() || undefined;
        host.commit("Renommer le calque");
      }
    }
    function onInspectClick(ev) {
      const s = sel();
      const a = ev.target.closest("[data-align],[data-act]");
      if (!a || !s.ids.length) return;
      const rec = host.getRecord(s.ids[0]);
      if (a.dataset.align) { rec.text = rec.text || {}; rec.text.align = a.dataset.align; host.commit("Alignement"); }
      else if (a.dataset.act === "reset-text") { delete rec.text; host.commit("Style d'origine"); }
      else if (a.dataset.act === "reset-node") {
        ["dx", "dy", "sx", "sy", "rot", "opacity"].forEach(k => delete rec[k]);
        host.commit("Réinitialiser la transformation");
      }
    }
    pane("inspect").addEventListener("input", onInspectInput);
    pane("inspect").addEventListener("change", onInspectInput);
    pane("inspect").addEventListener("click", onInspectClick);

    // ---------------------------------------------------------------- Ennoblissement & guilloches
    const GUI = [
      ["waves", "Nombre d'ondes (lignes)", 4, 60, 1, null],
      ["cycles", "Oscillations par ligne", 1, 20, 0.5, 6],
      ["ecc", "Excentricité", 0, 3, 0.05, 1],
      ["petals", "Pétales de rosace", 3, 48, 1, null],
      ["rings", "Anneaux de rosace", 1, 12, 1, null],
      ["stroke", "Épaisseur du trait (mm)", 0.02, 0.25, 0.005, 0.06]
    ];
    function renderFinish() {
      const s = sel();
      const d = host.state.design;
      const gp = d.guilloche || {};
      const rec = s.ids.length ? (host.getRecord(s.ids[0], true) || {}) : {};
      pane("finish").innerHTML = `
        <h4 class="ins-sub">Effet de la sélection</h4>
        ${s.ids.length ? `<div class="effects">${Object.entries(C.EFFECTS).map(([k, l]) => `<label class="check"><input type="radio" name="fx" value="${k}" ${(rec.effect || "none") === k ? "checked" : ""}> ${l}</label>`).join("")}</div>`
          : `<p class="hint">Sélectionnez un élément pour lui appliquer gaufrage, débossage ou hologramme.</p>`}
        <label class="check"><input type="checkbox" data-sp ${d.specular !== false ? "checked" : ""}> Reflet spéculaire dynamique au survol (dorures, hologrammes)</label>
        <h4 class="ins-sub">Générateur de guilloches & rosaces</h4>
        <label>Densité mathématique <output>${d.guillocheDensity}</output><input type="range" min="1" max="10" step="1" data-gd="guillocheDensity" value="${d.guillocheDensity}"></label>
        <label>Opacité <output>${Math.round(d.guillocheOpacity * 100)} %</output><input type="range" min="0" max="0.8" step="0.01" data-gd="guillocheOpacity" value="${d.guillocheOpacity}"></label>
        ${GUI.map(([k, l, min, max, step, def]) => {
          const v = gp[k] ?? def ?? (k === "waves" ? 4 + d.guillocheDensity * 3 : k === "petals" ? 9 + d.guillocheDensity * 2 : 3 + Math.round(d.guillocheDensity / 2));
          return `<label>${l} <output>${num(v, step < 1 ? 2 : 0)}</output><input type="range" min="${min}" max="${max}" step="${step}" data-gp="${k}" value="${v}"></label>`;
        }).join("")}
        <button class="btn ghost small" data-act="reset-guilloche">Rétablir les guilloches d'origine</button>`;
    }
    pane("finish").addEventListener("input", ev => {
      const t = ev.target;
      const d = host.state.design;
      if (t.name === "fx") {
        const s = sel();
        for (const id of s.ids) { const rec = host.getRecord(id); if (t.value === "none") delete rec.effect; else rec.effect = t.value; }
        host.commit(`Effet : ${C.EFFECTS[t.value]}`);
      } else if (t.dataset.gp) {
        d.guilloche = Object.assign({}, d.guilloche, { [t.dataset.gp]: Number(t.value) });
        t.previousElementSibling.textContent = num(t.value, Number(t.step) < 1 ? 2 : 0);
        host.commit("Guilloches", true);
      } else if (t.dataset.gd) {
        d[t.dataset.gd] = Number(t.value);
        host.commit("Guilloches", true);
      } else if (t.dataset.sp !== undefined) {
        d.specular = t.checked;
        host.commit("Reflet spéculaire");
      }
    });
    pane("finish").addEventListener("click", ev => {
      if (ev.target.closest("[data-act=reset-guilloche]")) { host.state.design.guilloche = {}; host.commit("Guilloches d'origine"); }
    });

    // ---------------------------------------------------------------- Pré-vol
    const CHECKS = { micro: "Micro-texte (< 0,86 mm)", guard: "Zone de garde (3 mm) & découpe", nfc: "Zone d'exclusion NFC", contrast: "Contraste (WCAG AA)" };
    api.runPreflight = () => {
      lastPreflight = host.runPreflight();
      const n = lastPreflight.issues.filter(i => i.level === "error").length;
      const w = lastPreflight.issues.filter(i => i.level === "warn").length;
      const b = document.getElementById("pfBadge");
      if (b) { b.textContent = n ? String(n) : w ? String(w) : "✓"; b.className = `pf-badge ${n ? "error" : w ? "warn" : "ok"}`; }
      return lastPreflight;
    };
    function renderPreflight() {
      const r = lastPreflight || api.runPreflight();
      const by = k => r.issues.filter(i => i.check === k);
      pane("preflight").innerHTML = `
        <label class="check"><input type="checkbox" id="pfZones" ${host.state.showZones ? "checked" : ""}> Afficher marges, fond perdu et zones NFC</label>
        ${Object.entries(CHECKS).map(([k, l]) => {
          const list = by(k);
          const worst = list.some(i => i.level === "error") ? "error" : list.some(i => i.level === "warn") ? "warn" : list.length ? "info" : "ok";
          return `<details class="pf-check ${worst}" ${worst === "error" || worst === "warn" ? "open" : ""}><summary><b class="dot"></b>${l}<span>${list.length ? list.length : "conforme"}</span></summary>
            <ul>${list.map(i => `<li class="${i.level}" ${i.id ? `data-face="${i.face}" data-id="${esc(i.id)}"` : ""}>${esc(i.text)}</li>`).join("") || "<li class=ok>Aucun écart.</li>"}</ul>
            ${k === "micro" && list.length ? `<button class="btn ghost small" data-act="fix-micro">Porter ces textes à 0,86 mm</button>` : ""}</details>`;
        }).join("")}
        <p class="hint">${r.stats.nodes} calques et ${r.stats.texts} textes contrôlés. Hypothèses : seuils WCAG 2.x (ISO/IEC 7810 n'en fixe pas) ; module de puce ${P.CONFIG.nfc.module} × ${P.CONFIG.nfc.module} mm centré sur la cible NFC et bande d'antenne à ${P.CONFIG.nfc.bandInner}–${P.CONFIG.nfc.bandOuter} mm du bord, à confirmer avec le fabricant de l'inlay.</p>`;
    }
    pane("preflight").addEventListener("click", ev => {
      const li = ev.target.closest("li[data-id]");
      if (li) { host.editor.select(li.dataset.face, [li.dataset.id]); return; }
      if (ev.target.closest("[data-act=fix-micro]")) {
        for (const i of (lastPreflight || { issues: [] }).issues.filter(x => x.check === "micro")) {
          const rec = host.getRecord(i.id);
          const t = firstText(i.face, i.id);
          const base = Number((rec.text && rec.text.size) || (t && t.getAttribute("font-size"))) || i.size;
          rec.text = Object.assign({}, rec.text, { size: Math.round(base * (P.CONFIG.microTextMm / i.size) * 1000 + 0.5) / 1000 });
        }
        host.commit("Correction micro-textes (0,86 mm)");
      }
    });
    pane("preflight").addEventListener("change", ev => {
      if (ev.target.id === "pfZones") { host.state.showZones = ev.target.checked; host.refreshCanvas(); }
    });

    // ---------------------------------------------------------------- Historique
    function renderHistory() {
      const h = host.history.state();
      pane("history").innerHTML = `
        <div class="hist-bar"><button class="btn small" data-h="undo" ${h.index > 0 ? "" : "disabled"}>↶ Annuler</button>
          <button class="btn small" data-h="redo" ${h.index < h.entries.length - 1 ? "" : "disabled"}>↷ Rétablir</button>
          <button class="btn ghost small" data-h="clear">Vider</button></div>
        <p class="hint">Ctrl/⌘ + Z · Ctrl/⌘ + Y ou ⌘ + Maj + Z — pile sans limite, conservée dans IndexedDB par dossier.</p>
        <ol class="hist">${h.entries.map((e, i) => `<li data-hi="${i}" class="${i === h.index ? "cur" : i > h.index ? "future" : ""}"><span>${esc(e.label)}</span><time>${new Date(e.at).toLocaleTimeString("fr-BE")}</time></li>`).reverse().join("")}</ol>`;
    }
    pane("history").addEventListener("click", ev => {
      const b = ev.target.closest("[data-h]");
      if (b) { if (b.dataset.h === "clear") host.history.clear(); else host.history[b.dataset.h](); return; }
      const li = ev.target.closest("[data-hi]");
      if (li) host.history.go(Number(li.dataset.hi));
    });

    // ---------------------------------------------------------------- API
    api.refresh = () => {
      if (el.hidden) return;
      if (tab === "layers") renderLayers();
      else if (tab === "inspect") renderInspect();
      else if (tab === "finish") renderFinish();
      else if (tab === "preflight") renderPreflight();
      else renderHistory();
    };
    api.afterRender = () => {
      api.runPreflight();
      // L'inspecteur n'est pas reconstruit pendant une saisie (garde le focus).
      if (el.contains(document.activeElement) && /^(INPUT|SELECT)$/.test(document.activeElement.tagName)) return;
      api.refresh();
    };
    api.onSelection = () => {
      if (tab === "history" || tab === "preflight") return api.refresh();
      if (sel().ids.length && tab === "layers") return renderLayers();
      api.refresh();
    };
    api.showTab = k => el.querySelector(`[data-stab="${k}"]`).click();
    api.lastPreflight = () => lastPreflight;
    return api;
  }

  root.PaxStudio = { create };
})(typeof self !== "undefined" ? self : this);
