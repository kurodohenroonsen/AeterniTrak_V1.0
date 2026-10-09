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
        care_intensity: "", refused_therapies: { artificial_nutrition: null, mechanical_ventilation: null, other_refusals: "" },
        preferred_care_setting: "", accepted_hospitalizations: "", comments: "",
        preferred_end_of_life_place: "", desired_support: { types: [], special_wishes: "" },
        essential_priority: "", other_wishes: "",
        post_mortem_wills: { leave_choice_to_relatives: false, funeral_home_choice: "", has_funeral_insurance: false, funeral_insurance_ref: "", rites: "", other_wishes: "" }
      },
      medical_record: {
        has_pacemaker: false, pacemaker_details: null, pacemaker_exeresis: null, has_radioisotopes: false,
        biological_hazard_level: 0, biological_hazard_label: "Standard", organ_donation_status: 2, body_donation_science: false,
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
    pyroStatus, batStatus, healthBadges, donationSummary, blankCase
  };
})(typeof self !== "undefined" ? self : this);
