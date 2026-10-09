/**
 * PaxStudio Design — Gestionnaire de persistance IndexedDB (DEC-AET-08 / Offline-first).
 * Stocke de façon robuste et asynchrone toutes les personnalisations multimédias
 * (jusqu'à 4 photos haute résolution avec recadrage/zoom, 4 enregistrements vocaux,
 * 4 morceaux musicaux et coordonnées de drag & drop WYSIWYG) sans limitation de quota localStorage.
 */
(function (root) {
  "use strict";

  const DB_NAME = "PaxStudioDB";
  const DB_VERSION = 1;
  const STORE_MEMORIAL = "memorial_customizations";

  let dbPromise = null;

  function openDb() {
    if (dbPromise) return dbPromise;
    dbPromise = new Promise((resolve, reject) => {
      if (typeof indexedDB === "undefined") {
        return reject(new Error("IndexedDB non disponible dans cet environnement."));
      }
      const request = indexedDB.open(DB_NAME, DB_VERSION);

      request.onupgradeneeded = event => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains(STORE_MEMORIAL)) {
          db.createObjectStore(STORE_MEMORIAL, { keyPath: "caseId" });
        }
      };

      request.onsuccess = event => {
        resolve(event.target.result);
      };

      request.onerror = event => {
        console.error("Erreur d'ouverture IndexedDB :", event.target.error);
        reject(event.target.error);
      };
    });
    return dbPromise;
  }

  /**
   * Sauvegarde les personnalisations d'une carte mémorielle pour un cas donné.
   * @param {string} caseId Identifiant du dossier (ex: PAVS_01_CH, SATURATION_01_CENTURION_MAX)
   * @param {Object} memorialState Données (photos, voices, musics, customPositions, etc.)
   */
  async function saveMemorial(caseId, memorialState) {
    if (!caseId) return false;
    try {
      const db = await openDb();
      return new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_MEMORIAL, "readwrite");
        const store = tx.objectStore(STORE_MEMORIAL);
        const record = {
          caseId: String(caseId),
          updatedAt: new Date().toISOString(),
          photos: memorialState.photos || [],
          voices: memorialState.voices || [],
          musics: memorialState.musics || [],
          activeVoiceIndex: memorialState.activeVoiceIndex ?? 0,
          activeMusicIndex: memorialState.activeMusicIndex ?? 0,
          customPositions: memorialState.customPositions || {},
          layout: memorialState.layout,
          years: memorialState.years,
          quote: memorialState.quote
        };
        const req = store.put(record);
        req.onsuccess = () => resolve(true);
        req.onerror = err => {
          console.warn("Échec sauvegarde IndexedDB :", err);
          reject(err);
        };
      });
    } catch (e) {
      console.warn("IndexedDB saveMemorial inaccessible :", e);
      return false;
    }
  }

  /**
   * Charge les personnalisations mémorielles enregistrées pour un cas donné.
   * @param {string} caseId
   * @returns {Promise<Object|null>}
   */
  async function loadMemorial(caseId) {
    if (!caseId) return null;
    try {
      const db = await openDb();
      return new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_MEMORIAL, "readonly");
        const store = tx.objectStore(STORE_MEMORIAL);
        const req = store.get(String(caseId));
        req.onsuccess = () => resolve(req.result || null);
        req.onerror = err => {
          console.warn("Échec lecture IndexedDB :", err);
          resolve(null);
        };
      });
    } catch (e) {
      console.warn("IndexedDB loadMemorial inaccessible :", e);
      return null;
    }
  }

  /**
   * Efface les personnalisations d'un cas donné (réinitialisation d'usine).
   * @param {string} caseId
   */
  async function clearMemorial(caseId) {
    if (!caseId) return false;
    try {
      const db = await openDb();
      return new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_MEMORIAL, "readwrite");
        const store = tx.objectStore(STORE_MEMORIAL);
        const req = store.delete(String(caseId));
        req.onsuccess = () => resolve(true);
        req.onerror = err => reject(err);
      });
    } catch (e) {
      return false;
    }
  }

  /**
   * Exporte l'ensemble des personnalisations stockées (sauvegarde/backup).
   */
  async function exportAll() {
    try {
      const db = await openDb();
      return new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_MEMORIAL, "readonly");
        const store = tx.objectStore(STORE_MEMORIAL);
        const req = store.getAll();
        req.onsuccess = () => resolve(req.result || []);
        req.onerror = err => reject(err);
      });
    } catch (e) {
      return [];
    }
  }

  root.PaxDb = {
    openDb,
    saveMemorial,
    loadMemorial,
    clearMemorial,
    exportAll
  };
})(typeof self !== "undefined" ? self : this);
