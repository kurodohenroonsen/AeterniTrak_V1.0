/**
 * PaxStudio Design — Moteur de règles métier (sans DOM).
 *
 * Contient : les 14 modes de sépulture, la validation Modulo 97 du NISS belge,
 * le verrou pyrotechnique (procédés thermiques 3 à 12) et le statut B.A.T.
 * Exposé en global `PaxRules` (navigateur) ; chargé tel quel par les tests Node via `vm`.
 */
(function (root) {
  "use strict";

  /** Familles de procédés. `thermal` = admission au four / appareil > 800 °C. */
  const FAMILIES = {
    inhumation: { label: "Inhumation", thermal: false },
    cremation: { label: "Crémation", thermal: true },
    sarco: { label: "Sarcomusation", thermal: true },
    humusation: { label: "Humusation", thermal: false },
    science: { label: "Legs à la science", thermal: false }
  };

  /** Les 14 modes de sépulture. `icon` référence une icône vectorielle de icons.js. */
  const BURIAL_MODES = [
    { id: 1, family: "inhumation", icon: "stone", short: "Inhumation en pleine terre", label: "Inhumation en pleine terre" },
    { id: 2, family: "inhumation", icon: "vault", short: "Inhumation en caveau", label: "Inhumation en caveau familial" },
    { id: 3, family: "cremation", icon: "lawn", short: "Crémation · dispersion", label: "Crémation avec dispersion des cendres (pelouse cinéraire)" },
    { id: 4, family: "cremation", icon: "columbarium", short: "Crémation · columbarium", label: "Crémation avec dépôt de l'urne en columbarium" },
    { id: 5, family: "cremation", icon: "sea", short: "Crémation · mer", label: "Crémation avec dispersion en mer territoriale belge" },
    { id: 6, family: "cremation", icon: "urn", short: "Crémation · cavurne", label: "Crémation avec inhumation de l'urne en cavurne" },
    { id: 7, family: "cremation", icon: "home", short: "Crémation · domicile", label: "Crémation avec conservation de l'urne au domicile" },
    { id: 8, family: "sarco", icon: "lawn", short: "Sarcomusation · dispersion", label: "Sarcomusation avec dispersion sur pelouse cinéraire" },
    { id: 9, family: "sarco", icon: "columbarium", short: "Sarcomusation · columbarium", label: "Sarcomusation avec dépôt de l'urne en columbarium" },
    { id: 10, family: "sarco", icon: "sea", short: "Sarcomusation · mer", label: "Sarcomusation avec dispersion en mer territoriale belge" },
    { id: 11, family: "sarco", icon: "urn", short: "Sarcomusation · cavurne", label: "Sarcomusation avec inhumation de l'urne en cavurne" },
    { id: 12, family: "sarco", icon: "home", short: "Sarcomusation · domicile", label: "Sarcomusation avec conservation de l'urne au domicile" },
    { id: 13, family: "humusation", icon: "tree", short: "Humusation sylvestre", label: "Humusation forestière (Living Lab)" },
    { id: 14, family: "science", icon: "science", short: "Legs à la science", label: "Legs du corps à la science (transfert sous 48 h)" }
  ];

  /** Mention imposée par DEC-AET-15 pour toute option de sarcomusation. */
  const SARCO_NOTICE = "Démonstrateur de faisabilité — option prospective non autorisée par le droit positif actuel (référence à confirmer par un juriste)";

  const ORGAN_DONATION = {
    1: { label: "Don d'organes consenti", detail: "Consentement exprès (Loi du 13/06/1986)" },
    2: { label: "Consentement présumé", detail: "Aucune volonté exprimée (Loi du 13/06/1986)" },
    3: { label: "Opposition au don d'organes", detail: "Opposition expresse enregistrée" }
  };

  const AMBIENT_PRESETS = {
    A_MAJOR_CELESTIAL: { label: "Nappe céleste", key: "La majeur · 440 Hz" },
    REQUIEM_FAURE: { label: "Requiem, op. 48", key: "Ré mineur · Fauré" },
    BACH_SUITE: { label: "Suite pour violoncelle n° 1", key: "Sol majeur · BWV 1007" }
  };

  function burialMode(id) {
    return BURIAL_MODES.find(m => m.id === Number(id)) || BURIAL_MODES[0];
  }

  function isThermal(modeId) {
    return FAMILIES[burialMode(modeId).family].thermal;
  }

  function isSarco(modeId) {
    return burialMode(modeId).family === "sarco";
  }

  /** Année de naissance à 4 chiffres depuis "AAAA-MM-JJ" (ou null). */
  function birthYear(birthDate) {
    const m = /^(\d{4})/.exec(birthDate || "");
    return m ? Number(m[1]) : null;
  }

  /**
   * Validation Modulo 97 du numéro de registre national belge.
   * Avant 2000 : 97 − (base9 mod 97) ; dès 2000 : 97 − ((2 000 000 000 + base9) mod 97) ; 0 → 97.
   * Retourne { valid, formatted, expected, sexOk, reason }.
   */
  function validateNiss(niss, birthDate, gender) {
    const digits = String(niss || "").replace(/\D/g, "");
    const out = { valid: false, formatted: String(niss || ""), expected: null, sexOk: null, reason: "" };
    if (digits.length !== 11) {
      out.reason = "11 chiffres requis";
      return out;
    }
    out.formatted = `${digits.slice(0, 2)}.${digits.slice(2, 4)}.${digits.slice(4, 6)}-${digits.slice(6, 9)}.${digits.slice(9)}`;
    const base = Number(digits.slice(0, 9));
    const check = Number(digits.slice(9));
    const year = birthYear(birthDate);
    const calc = b => { const r = 97 - (b % 97); return r === 0 ? 97 : r; };
    const pre2000 = calc(base);
    const post2000 = calc(2000000000 + base);
    if (year !== null) {
      out.expected = year >= 2000 ? post2000 : pre2000;
      out.valid = check === out.expected;
      const [y, mm, dd] = String(birthDate).split("-");
      if (out.valid && mm && dd) {
        if (digits.slice(0, 6) !== `${y.slice(2)}${mm}${dd}`) {
          out.valid = false;
          out.reason = "date de naissance incohérente";
        }
      }
    } else {
      out.valid = check === pre2000 || check === post2000;
    }
    if (!out.valid && !out.reason) out.reason = `contrôle attendu ${String(out.expected).padStart(2, "0")}`;
    const seq = Number(digits.slice(6, 9));
    if (gender === "M") out.sexOk = seq % 2 === 1;
    else if (gender === "F") out.sexOk = seq % 2 === 0;
    return out;
  }

  /** Calcule les deux chiffres de contrôle d'une base à 9 chiffres (aide à la saisie). */
  function nissCheckDigits(base9, year) {
    const b = Number(String(base9).replace(/\D/g, "").slice(0, 9));
    const r = 97 - ((year >= 2000 ? 2000000000 + b : b) % 97);
    return String(r === 0 ? 97 : r).padStart(2, "0");
  }

  function exeresisCertified(med) {
    return !!(med && med.pacemaker_exeresis && med.pacemaker_exeresis.certified_removed);
  }

  /**
   * Verrou pyrotechnique (CDLD & modèle IIIC).
   * level : "danger" (bloquant) | "ok".
   */
  function pyroStatus(c) {
    const med = c.medical_record || {};
    const mode = (c.funeral_wills || {}).burial_mode;
    const thermal = isThermal(mode);
    const fam = FAMILIES[burialMode(mode).family].label.toLowerCase();
    if (!med.has_pacemaker) {
      return { code: "NO_DEVICE", level: "ok", title: thermal ? "Aucun stimulateur · admis au four" : "Aucun stimulateur implanté",
        detail: thermal ? `Procédé thermique (${fam}) autorisé sans réserve pyrotechnique.` : "Aucune contrainte pyrotechnique." };
    }
    if (exeresisCertified(med)) {
      const ex = med.pacemaker_exeresis;
      return { code: "EXERESE_OK", level: "ok", title: "Exérèse certifiée · conforme four",
        detail: `PV d'exérèse : ${ex.surgeon_name || "praticien agréé"} · INAMI ${ex.surgeon_inami || "—"}` };
    }
    if (thermal) {
      return { code: "BLOCK", level: "danger", title: "Traitement thermique interdit",
        detail: `Stimulateur non extrait (${med.pacemaker_details || "modèle non précisé"}) — exérèse certifiée requise avant ${fam}.` };
    }
    return { code: "INHUMATION_OK", level: "ok", title: "Stimulateur en place · inhumation valide",
      detail: "Aucun procédé thermique : l'exérèse n'est pas requise." };
  }

  /**
   * Statut B.A.T. de la Carte 1, reproduit à l'identique sur les 44 cas de référence.
   * Ordre : verrou pyrotechnique, radio-isotopes actifs, prion × humusation, identité (nom + NISS valide).
   */
  function batStatus(c) {
    const med = c.medical_record || {};
    const ci = c.civil_identity || {};
    const mode = (c.funeral_wills || {}).burial_mode;
    let status = "VALIDE";
    if (pyroStatus(c).code === "BLOCK") status = "ALERTE_BLOCAGE_PACEMAKER";
    else if (med.has_radioisotopes) status = "ATTENTION_RADIO_ISOTOPES";
    else if (Number(med.biological_hazard_level) >= 3 && burialMode(mode).family === "humusation") status = "ALERTE_PRION_HUMUSATION";
    else if (!ci.full_name || !validateNiss(ci.national_id_niss, ci.birth_date, ci.gender).valid) status = "INCOMPLET_IDENTITE";
    return { carte_1_status: status, ready_to_print: status === "VALIDE" };
  }

  const BAT_LABELS = {
    VALIDE: "Bon à tirer",
    ALERTE_BLOCAGE_PACEMAKER: "Bloqué · pacemaker",
    ATTENTION_RADIO_ISOTOPES: "Attention · radio-isotopes",
    ALERTE_PRION_HUMUSATION: "Bloqué · prion × humusation",
    INCOMPLET_IDENTITE: "Incomplet · identité / NISS"
  };

  /** Badges sanitaires et dons, dans l'ordre d'affichage. */
  function healthBadges(c) {
    const med = c.medical_record || {};
    const mode = (c.funeral_wills || {}).burial_mode;
    const out = [];
    if (med.has_radioisotopes) out.push({ icon: "radiation", tone: "warn", label: "Radio-isotopes I-125" });
    const bio = Number(med.biological_hazard_level) || 0;
    if (bio >= 3) out.push({ icon: "biohazard", tone: "danger", label: "Prion · Biohazard 3" });
    else if (bio === 2) out.push({ icon: "biohazard", tone: "warn", label: "Cercueil zingué · BH2" });
    else if (bio === 1) out.push({ icon: "biohazard", tone: "info", label: "Hygiène renforcée" });
    if (burialMode(mode).family === "science" || med.body_donation_science) out.push({ icon: "science", tone: "info", label: "Legs science · 48 h" });
    else if (Number(med.organ_donation_status) === 1) out.push({ icon: "heart", tone: "ok", label: "Don d'organes" });
    else if (Number(med.organ_donation_status) === 3) out.push({ icon: "ban", tone: "muted", label: "Opposition don" });
    return out;
  }

  function donationSummary(c) {
    const med = c.medical_record || {};
    if (burialMode((c.funeral_wills || {}).burial_mode).family === "science" || med.body_donation_science) {
      return { icon: "science", label: "Legs du corps à la science", detail: "Transfert impératif sous 48 h vers l'Institut d'anatomie" };
    }
    const d = ORGAN_DONATION[Number(med.organ_donation_status)] || ORGAN_DONATION[2];
    return { icon: Number(med.organ_donation_status) === 3 ? "ban" : "heart", label: d.label, detail: d.detail };
  }


  // ---------------------------------------------------------------- PAVS : vocabulaire du formulaire officiel (Réseau Santé Wallon, conçu par UNESSA)
  const PAVS = {
    INTENSITY: [
      { id: "max", label: "Soins maximums", icon: "careMax" },
      { id: "usual", label: "Soins usuels", icon: "careUsual" }
    ],
    REFUSALS: [
      { id: "ANTIBIOTHERAPIE", label: "Antibiothérapie", icon: "antibiotic" },
      { id: "PERFUSION_HYDRATANTE", label: "Perfusion hydratante", icon: "hydration" },
      { id: "ALIM_ENTERALE", group: "nutrition", label: "Entérale (sonde par le nez)", icon: "tubeNose" },
      { id: "ALIM_PARENTERALE", group: "nutrition", label: "Parentérale (en intraveineuse)", icon: "ivDrip" },
      { id: "ALIM_GASTROSTOMIE", group: "nutrition", label: "Par sonde de gastrostomie (dans le ventre)", icon: "gastro" },
      { id: "DIALYSE", label: "Dialyse", icon: "dialysis" },
      { id: "OXYGENOTHERAPIE", group: "respiration", label: "Oxygénothérapie", icon: "oxygen" },
      { id: "VNI", group: "respiration", label: "Ventilation non invasive (VNI)", icon: "mask" },
      { id: "INTUBATION", group: "respiration", label: "Intubation", icon: "intubation" },
      { id: "SEDATION_PALLIATIVE", label: "Sédation palliative", icon: "sedation" },
      { id: "ALTERATION_CONSCIENCE", label: "Traitement altérant l'état de conscience", icon: "consciousness" }
    ],
    SETTINGS: [
      { id: "DOMICILE", label: "à mon domicile", icon: "home" },
      { id: "INSTITUTION", label: "dans mon institution", icon: "institution" },
      { id: "HOPITAL", label: "à l'hôpital", icon: "hospital" },
      { id: "USP", label: "en unité de soins palliatifs", icon: "palliativeUnit" }
    ],
    SUPPORT: [
      { id: "PSYCHOLOGIQUE", label: "Psychologique", icon: "psych" },
      { id: "PHILOSOPHIQUE", label: "Philosophique", icon: "book" },
      { id: "RELIGIEUX", label: "Religieux", icon: "candle" },
      { id: "SPIRITUEL", label: "Spirituel", icon: "lotus" },
      { id: "AUTRE", label: "Autre", icon: "star" },
      { id: "AUCUN", label: "Aucun", icon: "none" }
    ],
    DISPOSITION: [
      { id: "incinere", label: "Incinéré(e)", icon: "flame" },
      { id: "inhume", label: "Inhumé(e)", icon: "stone" },
      { id: "X", label: "Sans préférence", icon: "disposition" }
    ],
    ATTACHMENTS_MAX: 3,
    ATTACHMENTS_MAX_BYTES: 6 * 1024 * 1024,
    ATTACHMENTS_EXT: ["pdf", "png", "jpeg", "jpg", "bmp", "doc"]
  };

  /** Ancien libellé libre → niveau officiel (migration des 44 cas). */
  function careLevel(text) {
    const t = String(text || "");
    if (/maxim|performant|curatif|réanimation complète|réanimation cardio/i.test(t)) return "max";
    if (/usuel|actif|mesur|limitation/i.test(t)) return "usual";
    if (/palliat|confort/i.test(t)) return "comfort";
    return null;
  }

  const SUPPORT_RULES = [
    [/psych/i, "PSYCHOLOGIQUE"], [/cult|cathol|musul|isra[ée]l|relig|protest|orthod/i, "RELIGIEUX"],
    [/spirit|boudd|médit/i, "SPIRITUEL"], [/la[iï]q|philos|humanis|libre pens/i, "PHILOSOPHIQUE"]
  ];

  /**
   * Migre un dossier (ancien schéma des 44 cas) vers le schéma du formulaire officiel. Idempotent.
   * Les champs historiques sont conservés et resynchronisés par `syncOfficial`.
   */
  function normalizePavs(c) {
    const pr = c.pavs_record = c.pavs_record || {};
    const med = c.medical_record = c.medical_record || {};
    const fw = c.funeral_wills = c.funeral_wills || {};
    const pm = pr.post_mortem_wills = pr.post_mortem_wills || {};
    const ds = pr.desired_support = pr.desired_support || { types: [], special_wishes: "" };
    if (!pr.care) {
      const rt = pr.refused_therapies || {};
      const lvl = careLevel(pr.care_intensity);
      const refusals = [];
      if (rt.artificial_nutrition === true) refusals.push("ALIM_ENTERALE", "ALIM_PARENTERALE", "ALIM_GASTROSTOMIE");
      if (rt.mechanical_ventilation === true) refusals.push("VNI", "INTUBATION");
      const settings = [];
      const setting = String(pr.preferred_care_setting || "");
      if (/hospital|hôpital/i.test(setting)) settings.push("HOPITAL");
      else if (/domicile|lieu de vie/i.test(setting)) settings.push(pr.institution && pr.institution.name ? "INSTITUTION" : "DOMICILE");
      const comments = [];
      const acc = String(pr.accepted_hospitalizations || "").trim();
      if (acc && /^(CH|Grand|Ambroise|Clinique|Hôpital|CHU|CHR)/i.test(acc) && !(pr.institution && pr.institution.name)) {
        pr.institution = { name: acc, phone: "" };
      } else if (acc) {
        comments.push(acc);
      }
      if (pr.care_intensity && !["max", "usual", "comfort"].includes(lvl)) comments.push(pr.care_intensity);
      if (rt.other_refusals) comments.push(`Autres refus : ${rt.other_refusals}`);
      pr.care = {
        intensity: lvl === "max" || lvl === "usual" ? lvl : null,
        comfort: lvl === "comfort",
        euthanasia_declaration: false,
        refusals,
        settings,
        reanimation: lvl === "max" ? "avec" : null,
        exceptional_hospitalization: false
      };
      if (!pr.comments && comments.length) pr.comments = comments.join(" · ");
    }
    if (pr.eol_at_home === undefined) {
      const eol = String(pr.preferred_end_of_life_place || "");
      pr.eol_at_home = /domicile|lieu de vie/i.test(eol) ? "Oui" : /hospital|hôpital/i.test(eol) ? "Non" : null;
    }
    if (!Array.isArray(ds.choices)) {
      const choices = [];
      for (const t of ds.types || []) {
        const hit = SUPPORT_RULES.find(([re]) => re.test(t));
        const id = hit ? hit[1] : "AUTRE";
        if (!choices.includes(id)) choices.push(id);
      }
      ds.choices = choices;
      // Un libellé libre d'origine (hors libellés officiels) est conservé dans « je souhaite en particulier ».
      const free = (ds.types || []).filter(t => t && !PAVS.SUPPORT.some(x => x.label === t));
      if (free.length && !ds.special_wishes) ds.special_wishes = free.join(", ");
    }
    if (pm.body_donation === undefined) {
      pm.body_donation = med.body_donation_science || burialMode(fw.burial_mode).family === "science" ? "Oui" : "Non";
    }
    if (pm.body_disposition === undefined) {
      const fam = burialMode(fw.burial_mode).family;
      pm.body_disposition = fam === "cremation" ? "incinere" : fam === "inhumation" ? "inhume" : "X";
    }
    if (pm.rites === undefined || pm.rites === "") {
      pm.rites = [fw.ceremony_nature, fw.residue_destination].filter(v => v && String(v).trim()).join(" — ");
    }
    if (pm.leave_choice_to_relatives === undefined) pm.leave_choice_to_relatives = false;
    if (!Array.isArray(pr.attachments)) pr.attachments = [];
    return c;
  }

  /** Recopie les réponses officielles vers les champs historiques lus par les cartes et la filière. */
  function syncOfficial(c) {
    const pr = c.pavs_record;
    const care = pr.care;
    const med = c.medical_record;
    const pm = pr.post_mortem_wills;
    const rt = pr.refused_therapies = pr.refused_therapies || {};
    const ref = care.refusals || [];
    rt.artificial_nutrition = ref.some(id => id.startsWith("ALIM_"));
    rt.mechanical_ventilation = ref.includes("VNI") || ref.includes("INTUBATION");
    pr.care_intensity = [care.intensity && PAVS.INTENSITY.find(i => i.id === care.intensity).label, care.comfort && "Soins de confort/palliatifs"].filter(Boolean).join(" + ");
    pr.preferred_care_setting = (care.settings || []).map(id => PAVS.SETTINGS.find(x => x.id === id).label).join(", ");
    pr.preferred_end_of_life_place = pr.eol_at_home === "Oui" ? "Lieu de vie habituel (domicile)" : pr.eol_at_home === "Non" ? "Autre que le lieu de vie habituel" : "";
    pr.desired_support.types = (pr.desired_support.choices || []).map(id => PAVS.SUPPORT.find(x => x.id === id).label);
    med.body_donation_science = pm.body_donation === "Oui";
    return c;
  }

  /** Points d'attention (conseils issus des fiches didactiques ; n'affectent pas le statut B.A.T.). */
  function pavsWarnings(c) {
    const pr = c.pavs_record || {};
    const care = pr.care || {};
    const pm = pr.post_mortem_wills || {};
    const med = c.medical_record || {};
    const out = [];
    if (care.intensity === "max" && (care.refusals || []).length) {
      out.push({ level: "warn", text: "Soins maximums : ils impliquent la réanimation et la respiration artificielle ; les thérapies refusées ne devraient pas être complétées (fiche « Type de soins »)." });
    }
    if (care.intensity === "max" && care.reanimation === "sans") {
      out.push({ level: "warn", text: "Soins maximums mais hospitalisation sans réanimation : choix à clarifier." });
    }
    if (care.euthanasia_declaration) {
      out.push({ level: "info", text: "Déclaration anticipée d'euthanasie : à durée illimitée si établie depuis le 02/04/2020 ; antérieure, elle doit avoir été établie ou confirmée moins de 5 ans avant l'incapacité." });
    }
    const fam = burialMode((c.funeral_wills || {}).burial_mode).family;
    if ((pm.body_disposition === "incinere" && fam === "inhumation") || (pm.body_disposition === "inhume" && fam === "cremation")) {
      out.push({ level: "warn", text: "« Je désire être » ne correspond pas au mode de sépulture précis choisi pour la carte." });
    }
    if (pm.body_donation === "Oui") {
      out.push({ level: "info", text: "Don du corps : document écrit, daté et signé adressé à l'université choisie ; transfert au plus tard dans les 48 h." });
      if (Number(med.organ_donation_status) === 1) out.push({ level: "info", text: "Don d'organes et don du corps sont compatibles ; le don d'organes est prioritaire." });
    }
    return out;
  }

  /** Gabarit vierge pour « Ajouter un PAVS ». */
  function blankCase(id) {
    const today = new Date().toISOString().slice(0, 10);
    return {
      id, category: "MES_PAVS", label: "Nouveau PAVS", scenario: "PAVS saisi dans PaxStudio Design.",
      civil_identity: {
        full_name: "", birth_date: "", birth_place: "", death_date: "", death_time: "", death_place: "", death_municipality: "",
        national_id_niss: "", niss_valid: false, gender: "", phone: "",
        certifying_physician: { name: "", inami: "", certified_at: null }
      },
      pavs_record: {
        registered_date: today, designer: "FRATEM asbl © 2026", conservation_place: "",
        institution: null, health_proxy: null, extrajudicial_proxy: null, trusted_person: null, property_administrator: null,
        care_intensity: "", refused_therapies: { artificial_nutrition: false, mechanical_ventilation: false, other_refusals: "" },
        care: { intensity: null, comfort: false, euthanasia_declaration: false, refusals: [], settings: [], reanimation: null, exceptional_hospitalization: false },
        eol_at_home: null, attachments: [],
        preferred_care_setting: "", accepted_hospitalizations: "", comments: "",
        preferred_end_of_life_place: "", desired_support: { types: [], choices: [], special_wishes: "" },
        essential_priority: "", other_wishes: "", contact_person: null,
        post_mortem_wills: { body_donation: null, body_disposition: null, leave_choice_to_relatives: null, funeral_home_choice: "", has_funeral_insurance: false, funeral_insurance_ref: "", rites: "", other_wishes: "" }
      },
      medical_record: {
        has_pacemaker: false, pacemaker_details: null, pacemaker_exeresis: null, has_radioisotopes: false,
        biological_hazard_level: 0, biological_hazard_label: "Standard", organ_donation_status: null, body_donation_science: false,
        thanatopraxy: { performed: false, technique: "", operator_name: "" }
      },
      funeral_wills: {
        burial_mode: 1, burial_mode_label: BURIAL_MODES[0].label, ceremony_type: 1, ceremony_nature: "",
        residue_destination: "", coffin_material: "", chosen_funeral_home: "", has_funeral_insurance: false,
        legal_validation: { permit_number: `PERMIS-${today.slice(0, 4)}-${id}`, permit_date: today, permit_officer: "Officier de l'État civil", registry_locked: false }
      },
      multimedia_memorial: {
        has_portrait: false, photo_count: 0, portrait_style: "CAMEE_VECTORIEL", lifespan_display: "", epitaph: "",
        audio_choice: { has_voice_memo: false, voice_memo_duration_sec: 0, ambient_preset: "A_MAJOR_CELESTIAL", ducking_enabled: true, ducking_level_db: -14 },
        chosen_music: { title: "" }, audience_cards_count: 50
      },
      bat_status: { carte_1_status: "VALIDE", ready_to_print: true }
    };
  }

  root.PaxRules = {
    FAMILIES, BURIAL_MODES, SARCO_NOTICE, ORGAN_DONATION, AMBIENT_PRESETS, BAT_LABELS,
    burialMode, isThermal, isSarco, birthYear, validateNiss, nissCheckDigits,
    pyroStatus, batStatus, healthBadges, donationSummary, blankCase,
    PAVS, careLevel, normalizePavs, syncOfficial, pavsWarnings
  };
})(typeof self !== "undefined" ? self : this);
