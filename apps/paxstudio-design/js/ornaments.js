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
    rite: "M12 3v18M7.5 8h9M5 21h14",
    // — Pictogrammes du PAVS (Carte 1) —
    person: "M12 4a3.5 3.5 0 1 0 0 7 3.5 3.5 0 1 0 0-7zM5 20c0-3.9 3.1-7 7-7s7 3.1 7 7",
    genderF: "M12 3a5 5 0 1 0 0 10 5 5 0 1 0 0-10zM12 13v8M9 18h6",
    genderM: "M10 9a5.5 5.5 0 1 0 0 11 5.5 5.5 0 1 0 0-11zM14 10l6-6M15 4h5v5",
    genderX: "M12 3a9 9 0 1 0 0 18 9 9 0 1 0 0-18zM8.5 8.5l7 7M15.5 8.5l-7 7",
    birth: "M4 20h16M6 20v-7h12v7M6 16c2 1.5 4-1.5 6 0s4 1.5 6 0M12 13V9.5M12 5c.9.9.9 2.1 0 2.6-.9-.5-.9-1.7 0-2.6z",
    pin: "M12 21s-6.5-6.2-6.5-11A6.5 6.5 0 0 1 18.5 10c0 4.8-6.5 11-6.5 11zM12 7.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 1 0 0-5z",
    idcard: "M3 6h18v12H3zM6 10.5a2 2 0 1 0 4 0 2 2 0 1 0-4 0M5 16c.5-1.5 1.5-2.2 3-2.2s2.5.7 3 2.2M13 10h5M13 13h5",
    phone: "M6.5 3h3l1.5 4.5-2 1.3a10 10 0 0 0 6.2 6.2l1.3-2L21 14.5v3a2 2 0 0 1-2 2A16 16 0 0 1 4.5 5a2 2 0 0 1 2-2z",
    calendar: "M4 6h16v14H4zM4 10h16M8 3v5M16 3v5",
    archive: "M3 4h18v4H3zM5 8v12h14V8M10 12h4",
    institution: "M4 21V5l8-2v18M12 8h8v13M7 8h2M7 12h2M7 16h2M15 12h2M15 16h2M3 21h18",
    physician: "M6 3v6a4 4 0 0 0 8 0V3M10 13v2a5 5 0 0 0 10 0v-2M20 9a2 2 0 1 0 0 4 2 2 0 1 0 0-4zM5 3h2M13 3h2",
    contact: "M9 4a3 3 0 1 0 0 6 3 3 0 1 0 0-6zM3 19c0-3.3 2.7-6 6-6s6 2.7 6 6M17 7a4 4 0 0 1 0 5M19.5 5a7 7 0 0 1 0 9",
    proxyHealth: "M12 3 4.5 6v5.5c0 4.5 3.2 8.2 7.5 9.5 4.3-1.3 7.5-5 7.5-9.5V6zM12 8.5v6M9 11.5h6",
    proxyLegal: "M12 3v18M7 21h10M5 7h14M5 7l-2.5 6a2.5 2.5 0 0 0 5 0zM19 7l-2.5 6a2.5 2.5 0 0 0 5 0zM12 3l-1 1.5h2z",
    trusted: "M3 14h4l4 3h5a2 2 0 0 0 0-4h-4M7 14v6M3 20h4M15.5 4.2c-.9-.9-2.4-.9-3.3 0l-.2.2-.2-.2c-.9-.9-2.4-.9-3.3 0s-.9 2.4 0 3.3L12 11l3.5-3.5c.9-.9.9-2.4 0-3.3z",
    keyAdmin: "M8 11a4 4 0 1 0 0 8 4 4 0 1 0 0-8zM11 12l9-9M17 6l2 2M15 8l2 2",
    gauge: "M4 17a8 8 0 1 1 16 0M12 17l4-5M3 17h2M19 17h2M12 9V7M7 11.5 5.8 10.3M17 11.5l1.2-1.2",
    nutrition: "M8 3h8v9a4 4 0 0 1-8 0zM8 7h8M12 16v2M12 18c0 1.5-1 3-3 3",
    lungs: "M12 3v8M12 11c-1 1-3 1-3 3M12 11c1 1 3 1 3 3M9 7c-3 0-5 4-5 9 0 2 1 4 3 4 2 0 2-2 2-4zM15 7c3 0 5 4 5 9 0 2-1 4-3 4-2 0-2-2-2-4z",
    hospital: "M4 21V7h16v14M3 21h18M12 10v6M9 13h6M9 3h6v4H9z",
    bubble: "M4 5h16v11H9l-5 4z",
    bed: "M3 18V7M3 13h18v5M21 18v-3M6 13v-2a2 2 0 0 1 2-2h3v4M14 9h4a3 3 0 0 1 3 3",
    family: "M8 5a2.6 2.6 0 1 0 0 5.2 2.6 2.6 0 1 0 0-5.2zM16 5a2.6 2.6 0 1 0 0 5.2 2.6 2.6 0 1 0 0-5.2zM3 19c0-2.8 2.2-5 5-5 1.6 0 3 .7 4 1.9 1-1.2 2.4-1.9 4-1.9 2.8 0 5 2.2 5 5",
    medcross: "M9.5 3h5v6.5H21v5h-6.5V21h-5v-6.5H3v-5h6.5z",
    psych: "M9 21v-3.5C6.5 16.5 5 14 5 11a7 7 0 0 1 14 0c0 1-.3 2-.7 3l1.7 3h-2v2.5h-3V21M10 9.5a2 2 0 0 1 3.5 1.5c0 1.2-1.5 1.5-1.5 2.5",
    book: "M4 5c3-1 6-1 8 1 2-2 5-2 8-1v14c-3-1-6-1-8 1-2-2-5-2-8-1zM12 6v14",
    candle: "M10 10h4v11h-4zM12 3c1.5 2 1.5 3.5 0 5-1.5-1.5-1.5-3 0-5zM7 21h10",
    volunteers: "M2.5 12 7 8l3.5 3M21.5 12 17 8l-3.5 3M7 8h3l2 2 2-2h3M4.5 14l5 5h5l5-5M10 15l2 2 2-2",
    star: "M12 3l2.6 5.6 6.1.7-4.5 4.1 1.2 6L12 16.4 6.6 19.4l1.2-6L3.3 9.3l6.1-.7z",
    quote: "M5 11h4v6H4v-5c0-3 1.5-5 4-6M15 11h4v6h-5v-5c0-3 1.5-5 4-6",
    feather: "M20 4c-7 0-12 5-12 11v1l-4 5M8 16h5c4 0 7-4 7-12M9 12h6",
    scroll: "M6 4h11a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H7M6 4a2 2 0 0 0-2 2v1h4V6a2 2 0 0 0-2-2zM7 20a2 2 0 0 1-2-2v-1h4v1a2 2 0 0 1-2 2zM9.5 9h6M9.5 12.5h6M9.5 16h3.5",
    pacemaker: "M12 20s-7.5-4.6-7.5-10A4.3 4.3 0 0 1 12 7a4.3 4.3 0 0 1 7.5 3c0 5.4-7.5 10-7.5 10zM6 12h3l1.5-2.5 2 5 1.5-2.5h4",
    relatives: "M8 6a2.5 2.5 0 1 0 0 5 2.5 2.5 0 1 0 0-5zM3 19c0-2.8 2.2-5 5-5s5 2.2 5 5M15.5 7.5a2.5 2.5 0 1 1 3.5 2.3c-.8.4-1.5 1-1.5 2v1M17.5 16v.3",
    funeralHome: "M4 21V10l8-5 8 5v11M3 21h18M12 9.5v8M9.5 12.5h5",
    insurance: "M12 3 4.5 6v5.5c0 4.5 3.2 8.2 7.5 9.5 4.3-1.3 7.5-5 7.5-9.5V6zM8.5 12l2.5 2.5 4.5-5",
    coffin: "M9 2h6l3 5-2 15H8L6 7zM12 8v6M10 10h4",
    careMax: "M3 5h18v11H3zM3 10.5h4l1.5-3 3 6 1.5-3H21M8 20h8M12 16v4",
    careUsual: "M7 4h10v17H7zM10 2.5h4v3h-4zM12 9.5v6M9 12.5h6",
    antibiotic: "M10.6 3.9a4.8 4.8 0 0 1 6.8 6.8l-6.7 6.7a4.8 4.8 0 0 1-6.8-6.8zM7.2 7.3l6.8 6.8",
    hydration: "M8 2.5h8v9a4 4 0 0 1-8 0zM12 6.5c1.4 1.7 1.4 2.9 0 3.6-1.4-.7-1.4-1.9 0-3.6zM12 15.5V19a2 2 0 0 1-2 2H8",
    tubeNose: "M15 4c-3 0-5 2.5-5 5.5 0 1-1 1.8-1.6 2.3.6.5 1.6.7 1.6 1.7v2.5c0 1.5 1 2.5 2.5 2.5H14v2M9.5 11.5c-2 0-3.5 1.5-3.5 3.5v6M6 21h3",
    ivDrip: "M7 3h7v8a3.5 3.5 0 0 1-7 0zM10.5 14.5V17c0 1.7 1.3 3 3 3h3M16.5 20l4-4M18.5 14l2 2M5 3h11",
    gastro: "M9 4v3c-3 1-5 4-5 7.5 0 3.6 2.8 6.5 6.3 6.5 3.3 0 5.7-2.6 5.7-6v-1c0-1.7 1.3-3 3-3h1M13.5 13.5h3.5v6M15 19.5h4",
    dialysis: "M6 3h12v6H6zM6 15h12v6H6zM9 9v6M15 9v6M9 12h6M12 3V1.5M12 22.5V21",
    oxygen: "M12 3a9 9 0 1 0 0 18 9 9 0 1 0 0-18zM10.2 9a2.6 3 0 1 0 0 6 2.6 3 0 1 0 0-6zM14.5 14.2h2.3l-2.2 2.6h2.4",
    mask: "M5 9c0-2.8 3.1-5 7-5s7 2.2 7 5v3c0 3.9-3.1 7-7 7s-7-3.1-7-7zM2 10h3M19 10h3M9 12.5h6M12 19v3",
    intubation: "M8 3h3v3H8zM9.5 6v7a5 5 0 0 0 5 5H19M17 15.5l2.5 2.5-2.5 2.5M5 6h9",
    consciousness: "M2.5 12s3.5-6 9.5-6 9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6zM12 9.5a2.5 2.5 0 1 1-2.5 2.5M12 12h.1",
    palliativeUnit: "M3 18V8M3 14h18v4M21 18v-3M7 14v-2.5a1.5 1.5 0 0 1 1.5-1.5H11v4M16.5 11.5s-2.3-1.4-2.3-3a1.2 1.2 0 0 1 2.3-.7 1.2 1.2 0 0 1 2.3.7c0 1.6-2.3 3-2.3 3z",
    lotus: "M12 20c-4 0-8-2-9-6 3-.5 6 .5 9 3 3-2.5 6-3.5 9-3-1 4-5 6-9 6zM12 17c-2-2-2.5-6 0-11 2.5 5 2 9 0 11zM8 14.5C6.5 12 6.6 9.5 7.5 7.5c1.6 1 2.6 2.3 3.1 3.7M16 14.5c1.5-2.5 1.4-5 .5-7-1.6 1-2.6 2.3-3.1 3.7",
    none: "M12 3a9 9 0 1 0 0 18 9 9 0 1 0 0-18zM8 12h8",
    disposition: "M12 3a9 9 0 1 0 0 18 9 9 0 1 0 0-18zM9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6v.6M12 16.5v.2",
    reanimation: "M12 20s-7.5-4.6-7.5-10A4.3 4.3 0 0 1 12 7a4.3 4.3 0 0 1 7.5 3c0 5.4-7.5 10-7.5 10zM13 8.5l-2.5 4h3l-2.5 4",
    fracture: "M6.5 3.5a2 2 0 0 1 3 2.5l2.2 2.2L10 10l1.6 1.6L13.4 10l2.2 2.2-1.8 1.8 2.2 2.2a2 2 0 1 1-2.5 3 2 2 0 1 1-3-2.5l1.6-1.6-6.4-6.4a2 2 0 1 1-2.5-3 2 2 0 0 1 3.3-1.2z",
    paperclip: "M20 11.5l-8 8a5 5 0 0 1-7-7l8.5-8.5a3.3 3.3 0 0 1 4.7 4.7l-8.5 8.5a1.7 1.7 0 0 1-2.4-2.4l7.8-7.8",
    careComfort: "M12 14.5s-3-1.8-3-4a1.7 1.7 0 0 1 3-1 1.7 1.7 0 0 1 3 1c0 2.2-3 4-3 4zM3 9c0 6.5 4 11 9 11s9-4.5 9-11M3 9l2-3M21 9l-2-3",
    sedation: "M3.5 11c2.5 3 5.3 4.5 8.5 4.5s6-1.5 8.5-4.5M7 14.3 5.5 16.5M12 15.5V18M17 14.3l1.5 2.2M16 4.5a3.5 3.5 0 1 0 3.5 4.3A4 4 0 0 1 16 4.5z",
    euthanasia: "M6 3h8l4 4v14H6zM14 3v4h4M12 18s-2.6-1.6-2.6-3.4a1.4 1.4 0 0 1 2.6-.8 1.4 1.4 0 0 1 2.6.8c0 1.8-2.6 3.4-2.6 3.4zM9 9.5h4",
    university: "M2 9l10-5 10 5-10 5zM6 11v5c3 2 9 2 12 0v-5M22 9v6",
    cells: "M8 8a4 4 0 1 0 0 .1M16.5 7a2.5 2.5 0 1 0 0 .1M15 16a3.5 3.5 0 1 0 0 .1M8 8h.1M15 16h.1",
    nfc: "M6 8.5a5 5 0 0 1 0 7M9.5 6a8.5 8.5 0 0 1 0 12M13 3.5a12 12 0 0 1 0 17M3.5 12h.1"
  };

  /** Marqueur de réponse (pastille) : yes ✓, no ✕, unknown –, presumed ≈, alert !. */
  const MARK_TONES = { yes: "#2f7d4f", no: "#9b2c22", unknown: "#7b766c", presumed: "#2b5f9e", alert: "#c21c1c" };
  function mark(cx, cy, r, kind) {
    const col = MARK_TONES[kind] || MARK_TONES.unknown;
    const k = r / 1;
    const glyph = {
      yes: `M${f(cx - 0.45 * k)} ${f(cy + 0.02 * k)}l${f(0.3 * k)} ${f(0.32 * k)} ${f(0.62 * k)} ${f(-0.68 * k)}`,
      no: `M${f(cx - 0.38 * k)} ${f(cy - 0.38 * k)}l${f(0.76 * k)} ${f(0.76 * k)}M${f(cx + 0.38 * k)} ${f(cy - 0.38 * k)}l${f(-0.76 * k)} ${f(0.76 * k)}`,
      unknown: `M${f(cx - 0.42 * k)} ${f(cy)}h${f(0.84 * k)}`,
      presumed: `M${f(cx - 0.45 * k)} ${f(cy - 0.18 * k)}q${f(0.22 * k)} ${f(-0.22 * k)} ${f(0.45 * k)} 0t${f(0.45 * k)} 0M${f(cx - 0.45 * k)} ${f(cy + 0.24 * k)}q${f(0.22 * k)} ${f(-0.22 * k)} ${f(0.45 * k)} 0t${f(0.45 * k)} 0`,
      alert: `M${f(cx)} ${f(cy - 0.5 * k)}v${f(0.6 * k)}M${f(cx)} ${f(cy + 0.42 * k)}v${f(0.05 * k)}`
    }[kind] || "";
    return `<circle cx="${f(cx)}" cy="${f(cy)}" r="${f(r)}" fill="${col}" stroke="#fff" stroke-width="${f(r * 0.18)}"/><path d="${glyph}" fill="none" stroke="#fff" stroke-width="${f(r * 0.26)}" stroke-linecap="round" stroke-linejoin="round"/>`;
  }

  function icon(name, x, y, size, color, sw) {
    const d = ICONS[name] || ICONS.doc;
    const s = size / 24;
    return `<g transform="translate(${f(x)} ${f(y)}) scale(${f(s)})" fill="none" stroke="${color}" stroke-width="${f((sw || 0.16) / s)}" stroke-linecap="round" stroke-linejoin="round"><path d="${d}"/></g>`;
  }

  /** Lignes de sécurité ondulées (guilloche linéaire) couvrant un rectangle. */
  /**
   * Lignes de sécurité ondulées (guilloche linéaire) couvrant un rectangle.
   * opts (générateur paramétrique) : waves = nombre de lignes, cycles = ondes par ligne,
   * ecc = excentricité (amplitude relative), stroke = épaisseur du trait (mm).
   */
  function guillocheWaves(x, y, w, h, density, color, opacity, opts) {
    const o = opts || {};
    const n = Math.max(1, Math.round(o.waves || 4 + density * 3));
    const cycles = o.cycles || 6;
    const ecc = o.ecc ?? 1;
    let paths = "";
    for (let i = 0; i < n; i++) {
      const y0 = y + (h * (i + 0.5)) / n;
      const amp = (h / n) * 1.6 * ecc;
      const phase = (i * Math.PI) / 3.7;
      let d = "";
      for (let xx = 0; xx <= w; xx += 0.8) {
        const yy = y0 + amp * Math.sin((xx / w) * Math.PI * cycles + phase) * Math.cos((xx / w) * Math.PI * 1.3 + i * 0.4);
        d += (xx === 0 ? "M" : "L") + f(x + xx) + " " + f(yy);
      }
      paths += `<path d="${d}"/>`;
    }
    return `<g fill="none" stroke="${color}" stroke-width="${f(o.stroke || 0.06)}" opacity="${opacity}">${paths}</g>`;
  }

  /**
   * Rosace guillochée : anneaux polaires déphasés (effet moiré).
   * opts : petals = nombre de pétales, rings = anneaux, ecc = excentricité, stroke = épaisseur (mm).
   */
  function rosette(cx, cy, R, density, color, opacity, opts) {
    const o = opts || {};
    const rings = Math.max(1, Math.round(o.rings || 3 + Math.round(density / 2)));
    const petals = Math.max(3, Math.round(o.petals || 9 + density * 2));
    const ecc = 0.14 * (o.ecc ?? 1);
    let paths = "";
    for (let k = 0; k < rings; k++) {
      const rr = R * (0.45 + (0.55 * (k + 1)) / rings);
      for (let p = 0; p < 2; p++) {
        let d = "";
        const ph = (p * Math.PI) / petals + k * 0.35;
        for (let t = 0; t <= 360; t += 2) {
          const a = (t * Math.PI) / 180;
          const r = rr * (1 + ecc * Math.sin(petals * a + ph));
          d += (t === 0 ? "M" : "L") + f(cx + r * Math.cos(a)) + " " + f(cy + r * Math.sin(a));
        }
        paths += `<path d="${d}Z"/>`;
      }
    }
    return `<g fill="none" stroke="${color}" stroke-width="${f(o.stroke || 0.07)}" opacity="${opacity}">${paths}</g>`;
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

  root.PaxOrnaments = { ICONS, MARK_TONES, mark, icon, guillocheWaves, rosette, spiro, dove, oakBranch, cameo, nfcTarget, CAMEO_PATH };
})(typeof self !== "undefined" ? self : this);
