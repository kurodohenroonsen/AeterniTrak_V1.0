/**
 * PaxStudio Design — Historique d'annulation / rétablissement (pile d'instantanés).
 *
 * Chaque action validée (déplacement, rotation, style, saisie du formulaire…) pousse un instantané
 * complet de l'état éditable. La pile n'a pas de limite de profondeur ; elle est persistée par
 * dossier dans IndexedDB (PaxDb.saveHistory) et restaurée à la réouverture, y compris la position
 * courante : on peut donc annuler après un rafraîchissement ou la fermeture de l'onglet.
 *
 * Exposé en global `PaxHistory` (sans DOM : testable en Node).
 */
(function (root) {
  "use strict";

  /**
   * @param {{ capture: () => string, restore: (snap: string) => void, persist?: (h) => void, onChange?: (h) => void }} io
   */
  function create(io) {
    const h = { entries: [], index: -1 };
    let timer = 0;
    let pendingLabel = "";

    function notify() {
      if (io.persist) io.persist({ index: h.index, entries: h.entries });
      if (io.onChange) io.onChange(api.state());
    }

    /** Enregistre l'état courant ; supprime la branche de rétablissement. Ignore les doublons. */
    function push(label) {
      clearTimeout(timer);
      pendingLabel = "";
      const snap = io.capture();
      if (h.index >= 0 && h.entries[h.index].snap === snap) return false;
      h.entries = h.entries.slice(0, h.index + 1);
      h.entries.push({ label: label || "Modification", at: Date.now(), snap });
      h.index = h.entries.length - 1;
      notify();
      return true;
    }

    /** Regroupe les saisies rapprochées (curseurs, frappe) en une seule entrée. */
    function pushDebounced(label, delay) {
      pendingLabel = label;
      clearTimeout(timer);
      timer = setTimeout(() => push(pendingLabel), delay ?? 600);
    }

    function flush() {
      if (pendingLabel) push(pendingLabel);
    }

    function go(index) {
      flush();
      if (index < 0 || index >= h.entries.length || index === h.index) return false;
      h.index = index;
      io.restore(h.entries[index].snap);
      notify();
      return true;
    }

    /** Recharge une pile persistée (ou démarre une pile neuve avec l'état courant). */
    function load(saved, label) {
      clearTimeout(timer);
      pendingLabel = "";
      if (saved && Array.isArray(saved.entries) && saved.entries.length) {
        h.entries = saved.entries;
        h.index = Math.min(Math.max(saved.index ?? saved.entries.length - 1, 0), saved.entries.length - 1);
        io.restore(h.entries[h.index].snap);
        if (io.onChange) io.onChange(api.state());
        return true;
      }
      h.entries = [{ label: label || "Ouverture du dossier", at: Date.now(), snap: io.capture() }];
      h.index = 0;
      notify();
      return false;
    }

    function clear() {
      h.entries = [{ label: "Historique vidé", at: Date.now(), snap: io.capture() }];
      h.index = 0;
      notify();
    }

    const api = {
      push,
      pushDebounced,
      flush,
      load,
      clear,
      go,
      undo: () => go(h.index - 1),
      redo: () => go(h.index + 1),
      canUndo: () => h.index > 0,
      canRedo: () => h.index < h.entries.length - 1,
      state: () => ({ index: h.index, entries: h.entries.map(e => ({ label: e.label, at: e.at })) })
    };
    return api;
  }

  root.PaxHistory = { create };
})(typeof self !== "undefined" ? self : this);
