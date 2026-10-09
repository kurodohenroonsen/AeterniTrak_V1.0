/**
 * PaxStudio Design — Contrôleur de l'application (état, liaisons, rendu, export, impression).
 * Une seule source de vérité : `state.data` (un dossier au format des 44 cas PAVS).
 */
(function () {
  "use strict";

  const R = window.PaxRules;
  const C = window.PaxCards;
  const STORE_KEY = "paxstudio.mesPavs.v1";
  const $ = sel => document.querySelector(sel);
  const $$ = sel => Array.from(document.querySelectorAll(sel));

  const CATEGORY_LABELS = {
    MES_PAVS: "Mes PAVS",
    PAVS_FLAGSHIP: "Dossier titulaire",
    PAVS_SOINS_THERAPIES: "Projet de soins & thérapies",
    PAVS_SARCOMUSATION: "Sarcomusation (démonstrateur prospectif)",
    PAVS_CREMATION: "Crémation",
    PAVS_INHUMATION: "Inhumation & humusation",
    PAVS_PYROTECHNIQUE: "Sécurité pyrotechnique & sanitaire",
    PAVS_DONS_SCIENCE: "Dons & legs à la science",
    PAVS_REPRESENTANTS: "Représentants & rites",
    PAVS_MULTIMEDIA: "Obsèques & multimédia",
    PAVS_SATURATION: "Épreuves de saturation maximale (stress-test)"
  };

  const LAYOUT_NAMES = { A: "A · Majestueux — médaillon d'or", B: "B · Diptyque — encadrement biseauté", C: "C · Triptyque — trois arcades", D: "D · Mosaïque — archives multiples", E: "E · Typographie pure — stèle épigraphique" };

  const FONT_FILES = {
    cinzel: ["Cinzel", [["cinzel-latin-400-normal", 400, "normal"], ["cinzel-latin-600-normal", 600, "normal"], ["cinzel-latin-700-normal", 700, "normal"]]],
    cormorant: ["Cormorant Garamond", [["cormorant-garamond-latin-400-normal", 400, "normal"], ["cormorant-garamond-latin-400-italic", 400, "italic"], ["cormorant-garamond-latin-600-normal", 600, "normal"], ["cormorant-garamond-latin-600-italic", 600, "italic"]]],
    playfair: ["Playfair Display", [["playfair-display-latin-400-normal", 400, "normal"], ["playfair-display-latin-400-italic", 400, "italic"], ["playfair-display-latin-700-normal", 700, "normal"]]],
    inter: ["Inter", [["inter-latin-400-normal", 400, "normal"], ["inter-latin-500-normal", 500, "normal"], ["inter-latin-600-normal", 600, "normal"]]],
    fira: ["Fira Code", [["fira-code-latin-400-normal", 400, "normal"], ["fira-code-latin-500-normal", 500, "normal"]]]
  };

  const SATURATION_CASES = [
    {
      id: "SATURATION_01_CENTURION_MAX",
      category: "PAVS_SATURATION",
      label: "Centurion Max · Saturation absolue (8 contacts, 11 refus, textes max)",
      scenario: "Épreuve de charge maximale : toutes rubriques remplies au plafond légal et textuel.",
      civil_identity: {
        full_name: "Éléonore Anne-Sophie de VILLENEUVE-MONTGOMERY",
        national_id_niss: "62.08.14-388.65",
        birth_date: "1962-08-14",
        birth_place: "Bruxelles (Watermael-Boitsfort)",
        gender: "F",
        phone: "+32 470 12 34 56",
        certifying_physician: {
          name: "Prof. Dr Jean-Christophe de LA ROCHEFOUCAULD",
          inami: "1-98765-43-001",
          phone: "+32 81 22 33 44"
        }
      },
      medical_record: {
        has_pacemaker: true,
        pacemaker_details: "Medtronic Micra AV transcatheter TPS",
        pacemaker_exeresis: {
          certified_removed: true,
          surgeon_name: "Dr Laurent VANDENBERGHE",
          surgeon_inami: "1-44556-77-889",
          exeresis_date: "2026-10-08"
        },
        organ_donation_status: 1,
        has_radioisotopes: true,
        biological_hazard_level: 1,
        biological_hazard_label: "Précautions sanitaires renforcées BH1"
      },
      pavs_record: {
        registered_date: "2026-10-09",
        designer: "FRATEM asbl © 2026",
        conservation_place: "Réseau Santé Wallon (RSW) & Archives Notariales de Namur",
        institution: { name: "Résidence Médicalisée Universitaire Les Tilleuls", phone: "+32 81 99 88 77" },
        contact_person: { name: "Godefroy de VILLENEUVE", phone: "+32 495 11 22 33" },
        health_proxy: { name: "Me Charlotte DUPONT-VERMEULEN", phone: "+32 472 33 44 55" },
        extrajudicial_proxy: { name: "Me Henri de MONTGOMERY", phone: "+32 473 55 66 77" },
        trusted_person: { name: "Docteur Claire LAMBERT", phone: "+32 474 77 88 99" },
        property_administrator: { name: "Administration Judiciaire de Namur", phone: "+32 81 12 34 56" },
        care: {
          intensity: "usual",
          comfort: true,
          euthanasia_declaration: true,
          refusals: ["ANTIBIOTHERAPIE", "PERFUSION_HYDRATANTE", "ALIM_ENTERALE", "ALIM_PARENTERALE", "ALIM_GASTROSTOMIE", "DIALYSE", "OXYGENOTHERAPIE", "VNI", "INTUBATION", "SEDATION_PALLIATIVE", "ALTERATION_CONSCIENCE"],
          settings: ["DOMICILE", "USP"],
          reanimation: "sans",
          exceptional_hospitalization: true
        },
        comments: "Je souhaite privilégier le confort absolu, le soulagement complet de toute douleur et la paix intérieure, sans aucune manœuvre invasive ni prolongation artificielle.",
        eol_at_home: "Oui",
        desired_support: {
          choices: ["PSYCHOLOGIQUE", "PHILOSOPHIQUE", "SPIRITUEL"],
          special_wishes: "Accompagnement continu par l'équipe mobile de soins palliatifs, présence bienveillante de ma famille et écoute philosophique sereine."
        },
        essential_priority: "Partir en paix et dans la dignité, entourée de musique et de tendresse, sans acharnement technique ni souffrance inutile.",
        other_wishes: "Fenêtre ouverte sur le parc, lumière douce du crépuscule et parfum de lavande dans la chambre.",
        post_mortem_wills: {
          body_donation: "Oui",
          body_disposition: "incinere",
          leave_choice_to_relatives: false,
          rites: "Cérémonie laïque d'hommage et recueillement poétique sous les chênes centenaires",
          funeral_insurance_ref: "DELA Assurance Sérénité n° POL-884920-BE",
          other_wishes: "Dispersion écologique des cendres en lisière forestière communale et don mémorial à la fondation médicale."
        },
        attachments: [
          { name: "Directives_anticipées_signées.pdf", size: 1450000 },
          { name: "Mandat_extrajudiciaire_notarié.pdf", size: 2100000 },
          { name: "Attestation_leg_corps_science_ULiege.pdf", size: 850000 }
        ]
      },
      funeral_wills: {
        burial_mode: 8,
        burial_mode_label: "Sarcomusation (Procédé thermo-solaire)",
        residue_destination: "Jardin des mémoires écologiques et cinéraires de Gembloux",
        coffin_material: "Cercueil écologique thermo-conforme en fibres de cellulose naturelle",
        ceremony_nature: "Hommage républicain et laïque solennel",
        chosen_funeral_home: "Maison Funéraire Générale & Crématorium des Ardennes",
        has_funeral_insurance: true,
        legal_validation: {
          permit_number: "PERMIS-2026-WAL-SAT-001-MAX",
          permit_date: "2026-10-09",
          permit_officer: "Officier de l'État Civil de Namur"
        }
      },
      multimedia_memorial: {
        photo_count: 5,
        chosen_music: { title: "Gabriel Fauré — Requiem Op. 48 (In Paradisum)" },
        audio_choice: { has_voice_memo: true, voice_memo_duration_sec: 118, ambient_preset: "REQUIEM_FAURE" },
        audience_cards_count: 100
      },
      bat_status: { carte_1_status: "VALIDE", ready_to_print: true }
    },
    {
      id: "SATURATION_02_CURATIF_INTENSIF",
      category: "PAVS_SATURATION",
      label: "Curatif Intensif & Réanimation (Alerte Pyrotechnique & Biohazard 3)",
      scenario: "Soins curatifs maximums avec réanimation active, stimulateur non extrait au four crématophore et alerte prion.",
      civil_identity: {
        full_name: "Alexandre Maxime VANDERMEERSCH",
        national_id_niss: "85.11.23-147.55",
        birth_date: "1985-11-23",
        birth_place: "Liège",
        gender: "M",
        phone: "+32 475 88 99 00",
        certifying_physician: {
          name: "Dr Marc-Antoine DE SMET",
          inami: "1-12345-67-890",
          phone: "+32 4 366 22 22"
        }
      },
      medical_record: {
        has_pacemaker: true,
        pacemaker_details: "Biotronik Evia DR-T (Lithium haute énergie)",
        pacemaker_exeresis: null,
        organ_donation_status: 1,
        has_radioisotopes: false,
        biological_hazard_level: 3,
        biological_hazard_label: "Alerte Prion · Risque biologique majeur BH3"
      },
      pavs_record: {
        registered_date: "2026-10-09",
        designer: "FRATEM asbl © 2026",
        conservation_place: "Dossier Médical Partagé (DMP) RSW & CHU de Liège",
        institution: { name: "CHU Sart-Tilman Liège — Soins Intensifs", phone: "+32 4 366 77 77" },
        contact_person: { name: "Nathalie VANDERMEERSCH", phone: "+32 498 12 34 56" },
        health_proxy: { name: "Dr Julien VANDERMEERSCH", phone: "+32 477 65 43 21" },
        care: {
          intensity: "max",
          comfort: false,
          euthanasia_declaration: false,
          refusals: [],
          settings: ["HOPITAL"],
          reanimation: "avec",
          exceptional_hospitalization: false
        },
        comments: "Engager l'ensemble des thérapeutiques de réanimation avancée tant qu'un bénéfice pronostique est documenté par l'équipe collégiale.",
        eol_at_home: "Non",
        desired_support: { choices: ["PSYCHOLOGIQUE"], special_wishes: "Soutien psychologique permanent pour mes enfants et mon épouse." },
        essential_priority: "Lutter jusqu'au bout avec les technologies de pointe de la médecine réanimatoire.",
        post_mortem_wills: {
          body_donation: "Non",
          body_disposition: "inhume",
          leave_choice_to_relatives: true,
          rites: "Culte catholique en la Cathédrale Saint-Paul de Liège",
          funeral_insurance_ref: "Assurance Décès AG Insurance n° AG-992140",
          other_wishes: "Inhumation en caveau scellé hermétique avec respect des protocoles sanitaires renforcés."
        },
        attachments: [{ name: "Protocole_therapeutique_CHU.pdf", size: 980000 }]
      },
      funeral_wills: {
        burial_mode: 2,
        burial_mode_label: "Inhumation en caveau familial concédé",
        residue_destination: "Caveau familial concessions de Sainte-Walburge",
        coffin_material: "Cercueil étanche zingué avec filtre épurateur agréé",
        ceremony_nature: "Office religieux catholique avec homélie solennelle",
        chosen_funeral_home: "Centre Funéraire Liégeois Robermont",
        has_funeral_insurance: true,
        legal_validation: {
          permit_number: "PERMIS-2026-LIEGE-SANTE-002",
          permit_date: "2026-10-09",
          permit_officer: "Bourgmestre de la Ville de Liège"
        }
      },
      multimedia_memorial: {
        photo_count: 3,
        chosen_music: { title: "Jean-Sébastien Bach — Suite pour violoncelle n° 1 en Sol Majeur" },
        audio_choice: { has_voice_memo: true, voice_memo_duration_sec: 45, ambient_preset: "BACH_SUITE" },
        audience_cards_count: 50
      },
      bat_status: { carte_1_status: "VALIDE", ready_to_print: true }
    },
    {
      id: "SATURATION_03_SERENITE_PALLIATIVE",
      category: "PAVS_SATURATION",
      label: "Sérénité Palliative & Mer du Nord (Soins Confort & 6 refus)",
      scenario: "Soins palliatifs exclusifs, 6 refus ciblés et dispersion marine en mer territoriale belge.",
      civil_identity: {
        full_name: "Madeleine Hélène Françoise PEETERS-VERMEER",
        national_id_niss: "42.04.18-256.17",
        birth_date: "1942-04-18",
        birth_place: "Ostende",
        gender: "F",
        phone: "+32 59 11 22 33",
        certifying_physician: {
          name: "Dr Thérèse VAN DER BIEST",
          inami: "1-77889-11-222",
          phone: "+32 59 44 55 66"
        }
      },
      medical_record: {
        has_pacemaker: false,
        organ_donation_status: 1,
        has_radioisotopes: false,
        biological_hazard_level: 0
      },
      pavs_record: {
        registered_date: "2026-10-09",
        designer: "FRATEM asbl © 2026",
        conservation_place: "Réseau Santé Wallon & Notaire dépositaire à Knokke",
        institution: { name: "Villa Sérénité — Soins Palliatifs Côté Mer", phone: "+32 59 77 88 99" },
        contact_person: { name: "Lucie PEETERS", phone: "+32 496 77 88 99" },
        health_proxy: { name: "Me Bernard DUMONT", phone: "+32 471 22 33 44" },
        trusted_person: { name: "Sœur Emmanuelle", phone: "+32 59 33 22 11" },
        care: {
          intensity: "usual",
          comfort: true,
          euthanasia_declaration: true,
          refusals: ["ALIM_ENTERALE", "ALIM_PARENTERALE", "ALIM_GASTROSTOMIE", "INTUBATION", "VNI", "DIALYSE"],
          settings: ["DOMICILE", "USP"],
          reanimation: "sans",
          exceptional_hospitalization: false
        },
        comments: "Privilégier la présence des miens, l'apaisement par la musique classique et la sérénité du grand large face à l'horizon maritime.",
        eol_at_home: "Oui",
        desired_support: { choices: ["PHILOSOPHIQUE", "SPIRITUEL", "PSYCHOLOGIQUE"], special_wishes: "Lectures poétiques quotidiennes, méditation au coucher du soleil et accompagnement bienveillant." },
        essential_priority: "La liberté de l'océan, le souffle du vent du large et la paix infinie retrouvée auprès des miens.",
        other_wishes: "Entourée de mes petits-enfants, sans tuyaux ni moniteurs sonores intrusifs.",
        post_mortem_wills: {
          body_donation: "Non",
          body_disposition: "incinere",
          leave_choice_to_relatives: false,
          rites: "Dispersion au large des côtes belges au départ du port d'Ostende au son du violoncelle",
          funeral_insurance_ref: "Contrat Obsèques Corona Direct n° CR-448102",
          other_wishes: "Fleurs blanches jetées à la mer à l'instant de la dispersion des cendres."
        },
        attachments: [
          { name: "Directives_anticipées_PSPA.pdf", size: 1200000 },
          { name: "Declaration_euthanasie_enregistree.pdf", size: 650000 }
        ]
      },
      funeral_wills: {
        burial_mode: 7,
        burial_mode_label: "Crémation avec dispersion des cendres en mer territoriale belge",
        residue_destination: "Mer du Nord territoriale belge (au large d'Ostende)",
        coffin_material: "Cercueil écologique en pin massif issu de forêts durables FSC",
        ceremony_nature: "Cérémonie poétique en mer avec recueillement musical",
        chosen_funeral_home: "Pompes Funèbres Maritimes de la Côte",
        has_funeral_insurance: true,
        legal_validation: {
          permit_number: "PERMIS-2026-OST-MER-003",
          permit_date: "2026-10-09",
          permit_officer: "Commissaire Maritime d'Ostende"
        }
      },
      multimedia_memorial: {
        photo_count: 4,
        chosen_music: { title: "Claude Debussy — La Mer (Dialogue du vent et de la mer)" },
        audio_choice: { has_voice_memo: true, voice_memo_duration_sec: 54, ambient_preset: "A_MAJOR_CELESTIAL" },
        audience_cards_count: 80
      },
      bat_status: { carte_1_status: "VALIDE", ready_to_print: true }
    }
  ];
  window.SATURATION_CASES = SATURATION_CASES;

  const state = {
    cases: (window.PAX_TEST_CASES || []).map(c => Object.assign({}, c, { category: c.category })),
    saturationCases: SATURATION_CASES,
    saved: loadSaved(),

    data: null,
    tab: "card1",
    view: "side",
    crop: false,
    safe: false,
    zoom: 1,
    flipped: false,
    wysiwygMode: false,
    atelier: false,
    showZones: false,
    recordingState: { active: false, type: null, slotIndex: -1, seconds: 0 },
    design: {
      material: "ivoire", fontTitle: "cinzel", fontBody: "cormorant", fontData: "inter", fontScale: 1, gold: C.MATERIALS.ivoire.accent,
      guillocheOpacity: 0.35, guillocheDensity: 5, emblem: "dove", layout: "A", pulse: true,
      portrait: null, portraitBytes: 0, exemplaire: 1, epitaph: "", years: "", quote: "", voiceExtract: "", fingerprint: "",
      photos: [null, null, null, null],
      voices: [null, null, null, null],
      musics: [null, null, null, null],
      activeVoiceIndex: 0,
      activeMusicIndex: 0,
      customPositions: {},
      nodes: {},
      guilloche: {},
      specular: true
    }
  };

  // ------------------------------------------------------------ stockage local (confort par appareil)
  function loadSaved() {
    try { return JSON.parse(localStorage.getItem(STORE_KEY) || "[]"); } catch (e) { return []; }
  }
  function persistSaved() {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(state.saved)); return true; } catch (e) { return false; }
  }

  // ------------------------------------------------------------ chemins
  function getPath(obj, path) {
    return path.split(".").reduce((o, k) => (o == null ? undefined : o[k]), obj);
  }
  function setPath(obj, path, value) {
    const keys = path.split(".");
    let o = obj;
    keys.slice(0, -1).forEach(k => {
      if (o[k] == null || typeof o[k] !== "object") o[k] = {};
      o = o[k];
    });
    o[keys[keys.length - 1]] = value;
  }
  const clone = o => JSON.parse(JSON.stringify(o));

  function convert(raw, type) {
    if (type === "number") return raw === "" ? 0 : Number(raw);
    if (type === "bool") return raw === true || raw === "true";
    if (type === "tristate") return raw === "null" ? null : raw === "true";
    return raw;
  }

  // ------------------------------------------------------------ cohérence du dossier
  /** Recopie les champs miroir (post_mortem_wills, libellés) et recalcule le statut B.A.T. */
  function syncMirrors(c) {
    R.syncOfficial(R.normalizePavs(c));
    const mode = R.burialMode(c.funeral_wills.burial_mode);
    c.funeral_wills.burial_mode_label = mode.label;
    const pm = c.pavs_record.post_mortem_wills = c.pavs_record.post_mortem_wills || {};
    pm.organ_donation = Number(c.medical_record.organ_donation_status) === 1;
    pm.body_donation_science = !!c.medical_record.body_donation_science;
    c.funeral_wills.ceremony_nature = c.funeral_wills.ceremony_nature || "";
    pm.burial_desire = mode.label;
    pm.burial_destination = c.funeral_wills.residue_destination;
    pm.has_pacemaker = !!c.medical_record.has_pacemaker;
    pm.funeral_home_choice = c.funeral_wills.chosen_funeral_home;
    pm.has_funeral_insurance = !!c.funeral_wills.has_funeral_insurance;
    const bio = Number(c.medical_record.biological_hazard_level) || 0;
    c.medical_record.biological_hazard_label = ["Standard", "Hygiène renforcée", "Cercueil zingué (Biohazard 2)", "Alerte Prion (CE 999/2001)"][bio];
    const niss = R.validateNiss(c.civil_identity.national_id_niss, c.civil_identity.birth_date, c.civil_identity.gender);
    c.civil_identity.niss_valid = niss.valid;
    c.multimedia_memorial.audio_choice.has_voice_memo = Number(c.multimedia_memorial.audio_choice.voice_memo_duration_sec) > 0;
    c.bat_status = R.batStatus(c);
    return c;
  }

  // ------------------------------------------------------------ sélection d'un dossier
  function allCases() {
    return state.saved.map(c => Object.assign(c, { category: "MES_PAVS" }))
      .concat(state.saturationCases || [])
      .concat(state.cases);
  }


  function populateSelect() {
    const sel = $("#caseSelect");
    const groups = {};
    allCases().forEach(c => { (groups[c.category] = groups[c.category] || []).push(c); });
    sel.innerHTML = Object.keys(groups).map(k =>
      `<optgroup label="${escapeHtml(CATEGORY_LABELS[k] || k)}">` +
      groups[k].map(c => `<option value="${escapeHtml(c.id)}">${escapeHtml(c.category === "MES_PAVS" ? (c.civil_identity.full_name || "PAVS sans nom") + " · " + c.id : c.label)}</option>`).join("") +
      `</optgroup>`).join("");
    if (state.data) sel.value = state.data.id;
  }

  // ------------------------------------------------------------ Persistance IndexedDB & Mémorial multimédia
  const dbManager = window.PaxDb;

  async function loadFromIndexedDb(caseId) {
    if (!dbManager) return;
    try {
      const record = await dbManager.loadMemorial(caseId);
      const badge = $("#idbBadge");
      if (record) {
        if (Array.isArray(record.photos) && record.photos.length) {
          state.design.photos = record.photos;
          if (record.photos[0]?.url) {
            state.design.portrait = record.photos[0].url;
          }
        }
        if (Array.isArray(record.voices) && record.voices.length) {
          state.design.voices = record.voices;
        }
        if (Array.isArray(record.musics) && record.musics.length) {
          state.design.musics = record.musics;
        }
        if (record.activeVoiceIndex != null) state.design.activeVoiceIndex = record.activeVoiceIndex;
        if (record.activeMusicIndex != null) state.design.activeMusicIndex = record.activeMusicIndex;
        if (record.customPositions) state.design.customPositions = record.customPositions;
        if (record.nodes) state.design.nodes = record.nodes;
        if (record.guilloche) state.design.guilloche = record.guilloche;
        if (record.specular != null) state.design.specular = record.specular;
        if (record.layout) {
          state.design.layout = record.layout;
          updateLayoutButtons();
        }
        if (record.years) state.design.years = record.years;
        if (record.quote) state.design.quote = record.quote;

        if (badge) {
          badge.textContent = "💾 Restauré (IndexedDB)";
          badge.className = "idb-badge";
        }
      } else {
        if (badge) {
          badge.textContent = "💾 IndexedDB";
          badge.className = "idb-badge";
        }
      }
    } catch (e) {
      console.warn("Erreur chargement IndexedDB :", e);
    }
  }

  let idbSaveTimer = 0;
  function persistToIndexedDb() {
    if (!dbManager || !state.data) return;
    const badge = $("#idbBadge");
    if (badge) {
      badge.textContent = "💾 Sauvegarde...";
      badge.className = "idb-badge saving";
    }
    clearTimeout(idbSaveTimer);
    idbSaveTimer = setTimeout(async () => {
      try {
        await dbManager.saveMemorial(state.data.id, {
          photos: state.design.photos,
          voices: state.design.voices,
          musics: state.design.musics,
          activeVoiceIndex: state.design.activeVoiceIndex,
          activeMusicIndex: state.design.activeMusicIndex,
          customPositions: state.design.customPositions,
          nodes: state.design.nodes,
          guilloche: state.design.guilloche,
          specular: state.design.specular,
          layout: state.design.layout,
          years: state.design.years,
          quote: state.design.quote
        });
        if (badge) {
          badge.textContent = "💾 Sauvegardé";
          badge.className = "idb-badge";
          setTimeout(() => { if (badge) badge.textContent = "💾 IndexedDB"; }, 2500);
        }
      } catch (err) {
        console.warn("Erreur sauvegarde IndexedDB :", err);
        if (badge) {
          badge.textContent = "⚠️ Échec IDB";
          badge.className = "idb-badge saving";
        }
      }
    }, 350);
  }

  async function selectCase(id) {
    const src = allCases().find(c => c.id === id) || state.cases[0];
    state.data = R.normalizePavs(clone(src));
    state.pristine = clone(state.data);
    const pr = state.data.pavs_record;
    const mm = state.data.multimedia_memorial;
    const d = state.design;
    d.epitaph = mm.epitaph || "";
    d.years = mm.lifespan_display || "";
    d.quote = (mm.epitaph || "").replace(/^Pour moi, l'essentiel c'est\s*:\s*/i, "");
    d.voiceExtract = pr.desired_support.special_wishes && pr.desired_support.special_wishes !== (pr.desired_support.types || [])[0]
      ? pr.desired_support.special_wishes : pr.essential_priority || "";
    d.exemplaire = 1;
    $("#caseSelect").value = state.data.id;

    // Réinitialisation des slots par défaut
    d.photos = [null, null, null, null];
    d.voices = [null, null, null, null];
    d.musics = [null, null, null, null];
    d.activeVoiceIndex = 0;
    d.activeMusicIndex = 0;
    d.customPositions = {};
    d.nodes = {};
    d.guilloche = {};

    if (d.portrait) {
      d.photos[0] = { id: 0, url: d.portrait, name: "Portrait principal", crop: { scale: 1.0, x: 0, y: 0, rotation: 0 } };
    }
    const ac = mm.audio_choice || {};
    if (ac.has_voice_memo) {
      d.voices[0] = {
        id: 0,
        url: "",
        name: "Mémo vocal d'adieu",
        duration: ac.voice_memo_duration_sec || 0,
        date: C.shortDate(pr.registered_date),
        extract: d.voiceExtract
      };
    }
    const cm = mm.chosen_music || {};
    if (cm.title) {
      d.musics[0] = {
        id: 0,
        url: "",
        name: cm.title,
        title: cm.title,
        composer: "",
        duration: 180,
        ambientPreset: ac.ambient_preset || "A_MAJOR_CELESTIAL"
      };
    }

    // Chargement automatique des personnalisations stockées en IndexedDB
    await loadFromIndexedDb(state.data.id);

    // Historique d'annulation persistant : restaure la position exacte de la pile
    if (history) {
      restoring = true;
      const savedHistory = dbManager && dbManager.loadHistory ? await dbManager.loadHistory(state.data.id) : null;
      history.load(savedHistory, "Ouverture du dossier");
      restoring = false;
    }
    if (editor) editor.select(null, []);

    syncMirrors(state.data);
    refreshInputs();
    renderAnnexes();
    renderPhotosPanel();
    renderVoicesPanel();
    renderMusicsPanel();
    refresh();
  }

  // ------------------------------------------------------------ Galerie Photos (jusqu'à 4 photos)
  function renderPhotosPanel() {
    const el = $("#photosPanel");
    if (!el) return;
    const photos = state.design.photos || [];
    let html = "";
    for (let i = 0; i < 4; i++) {
      const p = photos[i];
      const isSlot0 = i === 0;
      const slotTitle = isSlot0 ? "Photo 1 (Principale)" : `Photo ${i + 1}`;
      const crop = p?.crop || { scale: 1.0, x: 0, y: 0, rotation: 0 };
      html += `
        <div class="photo-slot-card" data-slot="${i}">
          <div class="slot-header">
            <span>${slotTitle}</span>
            ${p?.url ? `<span class="badge">Chargée</span>` : `<span class="badge" style="opacity:0.6">Vide</span>`}
          </div>
          <div class="photo-thumb-wrap">
            ${p?.url ? `<img src="${p.url}" class="photo-thumb" alt="${slotTitle}">` : `<div class="photo-thumb" style="display:grid;place-items:center;color:var(--muted);font-size:20px;">🖼️</div>`}
            <div class="photo-actions">
              <label class="btn file" style="padding:4px 8px;font-size:12px;">
                ${p?.url ? "Remplacer" : "Importer photo"}
                <input type="file" accept="image/*" data-photo-upload="${i}" hidden>
              </label>
              ${p?.url ? `<button type="button" class="btn ghost" data-photo-delete="${i}" style="padding:4px 8px;font-size:12px;color:var(--danger)">Supprimer</button>` : ""}
            </div>
          </div>
          ${p?.url ? `
            <details class="crop-controls" ${p.openCrop ? "open" : ""}>
              <summary style="font-size:11.5px;cursor:pointer;color:var(--gold-2)">📐 Cadrage &amp; Zoom</summary>
              <div class="crop-slider-row">
                <span>Zoom</span>
                <input type="range" min="0.5" max="3.0" step="0.05" value="${crop.scale || 1.0}" data-crop-prop="scale" data-photo-idx="${i}">
                <output>${Math.round((crop.scale || 1.0) * 100)}%</output>
              </div>
              <div class="crop-slider-row">
                <span>Pan X</span>
                <input type="range" min="-30" max="30" step="0.5" value="${crop.x || 0}" data-crop-prop="x" data-photo-idx="${i}">
                <output>${crop.x || 0} mm</output>
              </div>
              <div class="crop-slider-row">
                <span>Pan Y</span>
                <input type="range" min="-30" max="30" step="0.5" value="${crop.y || 0}" data-crop-prop="y" data-photo-idx="${i}">
                <output>${crop.y || 0} mm</output>
              </div>
              <div class="crop-slider-row">
                <span>Rotation</span>
                <input type="range" min="-180" max="180" step="1" value="${crop.rotation || 0}" data-crop-prop="rotation" data-photo-idx="${i}">
                <output>${crop.rotation || 0}°</output>
              </div>
              <button type="button" class="btn ghost" data-crop-reset="${i}" style="padding:3px 6px;font-size:11px;margin-top:4px;">↺ Réinitialiser cadrage</button>
            </details>
          ` : ""}
        </div>
      `;
    }
    el.innerHTML = html;
  }

  function loadPhotoSlot(slotIndex, file) {
    const reader = new FileReader();
    reader.onload = () => {
      state.design.photos = state.design.photos || [];
      state.design.photos[slotIndex] = {
        id: slotIndex,
        url: reader.result,
        name: file.name,
        crop: { scale: 1.0, x: 0, y: 0, rotation: 0 },
        openCrop: true
      };
      if (slotIndex === 0) {
        state.design.portrait = reader.result;
        state.design.portraitBytes = file.size;
        state.data.multimedia_memorial.has_portrait = true;
      }
      renderPhotosPanel();
      scheduleRender();
      persistToIndexedDb();
      toast(`Photo ${slotIndex + 1} chargée et sauvegardée en IndexedDB.`);
    };
    reader.readAsDataURL(file);
  }

  // ------------------------------------------------------------ Voix & Mémos vocaux
  let mediaRecorder = null;
  let audioChunks = [];
  let recordInterval = null;

  function formatTimer(sec) {
    const m = Math.floor(sec / 60).toString().padStart(2, "0");
    const s = (sec % 60).toString().padStart(2, "0");
    return `${m}:${s}`;
  }

  function renderVoicesPanel() {
    const el = $("#voicesPanel");
    if (!el) return;
    const voices = state.design.voices || [];
    const activeIdx = state.design.activeVoiceIndex ?? 0;
    const rec = state.recordingState;
    let html = "";
    for (let i = 0; i < 4; i++) {
      const v = voices[i];
      const isRec = rec.active && rec.type === "voice" && rec.slotIndex === i;
      const isActive = activeIdx === i;
      html += `
        <div class="voice-slot-card" data-slot="${i}">
          <div class="slot-header">
            <span>Voix ${i + 1}</span>
            <label class="active-slot-check">
              <input type="radio" name="activeVoiceSlot" value="${i}" ${isActive ? "checked" : ""}>
              Diffuser sur Carte 2
            </label>
          </div>
          ${isRec ? `
            <div class="rec-box">
              <span class="rec-dot"></span>
              <span>Enregistrement en direct :</span>
              <span class="rec-timer">${formatTimer(rec.seconds)}</span>
              <button type="button" class="btn danger" data-audio-stop="voice" style="margin-left:auto;padding:4px 8px;font-size:12px;">⏹️ Terminer</button>
            </div>
          ` : v?.url ? `
            <audio controls src="${v.url}" class="audio-player"></audio>
            <div style="font-size:11.5px;color:var(--muted);display:flex;justify-content:space-between;">
              <span>Durée : ${v.duration || 0} s</span>
              <span>${v.date || ""}</span>
            </div>
            <label style="font-size:11.5px;display:grid;gap:3px;margin-top:4px;">
              Extrait textuel / Paroles d'adieu
              <input type="text" data-voice-extract="${i}" value="${escapeHtml(v.extract || "")}" placeholder="« Citation extraite... »">
            </label>
            <div style="display:flex;gap:6px;margin-top:4px;">
              <button type="button" class="btn" data-audio-record="voice" data-slot="${i}" style="padding:4px 8px;font-size:11px;">🎙️ Ré-enregistrer</button>
              <label class="btn file" style="padding:4px 8px;font-size:11px;">
                Remplacer fichier
                <input type="file" accept="audio/*" data-voice-upload="${i}" hidden>
              </label>
              <button type="button" class="btn ghost" data-voice-delete="${i}" style="padding:4px 8px;font-size:11px;color:var(--danger)">Supprimer</button>
            </div>
          ` : `
            <p style="font-size:11.5px;color:var(--muted);margin:2px 0;">Aucun enregistrement vocal sur ce slot.</p>
            <div style="display:flex;gap:6px;">
              <button type="button" class="btn" data-audio-record="voice" data-slot="${i}" style="padding:4px 8px;font-size:12px;">🎙️ Enregistrer</button>
              <label class="btn file" style="padding:4px 8px;font-size:12px;">
                📁 Importer audio
                <input type="file" accept="audio/*" data-voice-upload="${i}" hidden>
              </label>
            </div>
          `}
        </div>
      `;
    }
    el.innerHTML = html;
  }

  // ------------------------------------------------------------ Œuvres Musicales (fichiers audio directs)
  function renderMusicsPanel() {
    const el = $("#musicsPanel");
    if (!el) return;
    const musics = state.design.musics || [];
    const activeIdx = state.design.activeMusicIndex ?? 0;
    const rec = state.recordingState;
    let html = "";
    for (let i = 0; i < 4; i++) {
      const m = musics[i];
      const isRec = rec.active && rec.type === "music" && rec.slotIndex === i;
      const isActive = activeIdx === i;
      html += `
        <div class="music-slot-card" data-slot="${i}">
          <div class="slot-header">
            <span>Morceau ${i + 1}</span>
            <label class="active-slot-check">
              <input type="radio" name="activeMusicSlot" value="${i}" ${isActive ? "checked" : ""}>
              Graver sur Carte 2
            </label>
          </div>
          ${isRec ? `
            <div class="rec-box">
              <span class="rec-dot"></span>
              <span>Enregistrement direct :</span>
              <span class="rec-timer">${formatTimer(rec.seconds)}</span>
              <button type="button" class="btn danger" data-audio-stop="music" style="margin-left:auto;padding:4px 8px;font-size:12px;">⏹️ Terminer</button>
            </div>
          ` : m?.url ? `
            <audio controls src="${m.url}" class="audio-player"></audio>
            <div style="font-size:11.5px;color:var(--muted);display:flex;justify-content:space-between;align-items:center;">
              <span>Durée : ${m.duration || 0} s</span>
              <span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:140px;" title="${escapeHtml(m.name || "")}">${escapeHtml(m.name || "")}</span>
            </div>
            <div style="display:flex;gap:6px;margin-top:4px;">
              <button type="button" class="btn" data-audio-record="music" data-slot="${i}" style="padding:4px 8px;font-size:11px;">🎙️ Ré-enregistrer</button>
              <label class="btn file" style="padding:4px 8px;font-size:11px;">
                Remplacer fichier
                <input type="file" accept="audio/*" data-music-upload="${i}" hidden>
              </label>
              <button type="button" class="btn ghost" data-music-delete="${i}" style="padding:4px 8px;font-size:11px;color:var(--danger)">Supprimer</button>
            </div>
          ` : `
            <p style="font-size:11.5px;color:var(--muted);margin:2px 0;">Aucun fichier musical sur ce slot.</p>
            <div style="display:flex;gap:6px;">
              <button type="button" class="btn" data-audio-record="music" data-slot="${i}" style="padding:4px 8px;font-size:12px;">🎙️ Enregistrer</button>
              <label class="btn file" style="padding:4px 8px;font-size:12px;">
                📁 Importer audio
                <input type="file" accept="audio/*" data-music-upload="${i}" hidden>
              </label>
            </div>
          `}
        </div>
      `;
    }
    el.innerHTML = html;
  }

  // ------------------------------------------------------------ Audio Recorder (Microphone) & File Uploads
  async function startAudioRecording(type, slotIndex) {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      toast("L'API MediaRecorder n'est pas supportée sur ce navigateur.");
      return;
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioChunks = [];
      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = e => {
        if (e.data && e.data.size > 0) audioChunks.push(e.data);
      };

      mediaRecorder.onstop = () => {
        clearInterval(recordInterval);
        const blob = new Blob(audioChunks, { type: "audio/webm" });
        const reader = new FileReader();
        reader.onloadend = () => {
          const dataUrl = reader.result;
          const dur = Math.max(1, state.recordingState.seconds);
          if (type === "voice") {
            state.design.voices = state.design.voices || [];
            state.design.voices[slotIndex] = {
              id: slotIndex,
              url: dataUrl,
              name: `Enregistrement vocal ${slotIndex + 1}`,
              duration: dur,
              date: C.shortDate(new Date().toISOString()),
              extract: state.design.voices[slotIndex]?.extract || state.design.voiceExtract || ""
            };
            state.design.activeVoiceIndex = slotIndex;
            renderVoicesPanel();
          } else {
            state.design.musics = state.design.musics || [];
            state.design.musics[slotIndex] = {
              id: slotIndex,
              url: dataUrl,
              name: `Enregistrement musical ${slotIndex + 1}`,
              duration: dur
            };
            state.design.activeMusicIndex = slotIndex;
            renderMusicsPanel();
          }
          state.recordingState = { active: false, type: null, slotIndex: -1, seconds: 0 };
          scheduleRender();
          persistToIndexedDb();
          toast("Enregistrement audio réussi et sauvegardé en IndexedDB !");
        };
        reader.readAsDataURL(blob);
        stream.getTracks().forEach(t => t.stop());
      };

      mediaRecorder.start(200);
      state.recordingState = { active: true, type, slotIndex, seconds: 0 };
      if (type === "voice") renderVoicesPanel();
      else renderMusicsPanel();

      recordInterval = setInterval(() => {
        state.recordingState.seconds++;
        const timerEl = document.querySelector(".rec-timer");
        if (timerEl) timerEl.textContent = formatTimer(state.recordingState.seconds);
      }, 1000);
    } catch (err) {
      console.error("Microphone non disponible :", err);
      toast("Impossible d'accéder au microphone (permission requise).");
    }
  }

  function stopAudioRecording() {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
      mediaRecorder.stop();
    }
  }

  function loadAudioFileSlot(type, slotIndex, file) {
    const reader = new FileReader();
    reader.onload = () => {
      const dataUrl = reader.result;
      const audio = new Audio(dataUrl);
      audio.onloadedmetadata = () => {
        const dur = Math.round(audio.duration) || 30;
        if (type === "voice") {
          state.design.voices = state.design.voices || [];
          state.design.voices[slotIndex] = {
            id: slotIndex,
            url: dataUrl,
            name: file.name,
            duration: dur,
            date: C.shortDate(new Date().toISOString()),
            extract: state.design.voices[slotIndex]?.extract || state.design.voiceExtract || ""
          };
          state.design.activeVoiceIndex = slotIndex;
          renderVoicesPanel();
        } else {
          state.design.musics = state.design.musics || [];
          state.design.musics[slotIndex] = {
            id: slotIndex,
            url: dataUrl,
            name: file.name,
            duration: dur
          };
          state.design.activeMusicIndex = slotIndex;
          renderMusicsPanel();
        }
        scheduleRender();
        persistToIndexedDb();
        toast(`Fichier audio importé sur le slot ${slotIndex + 1}.`);
      };
    };
    reader.readAsDataURL(file);
  }

  // ------------------------------------------------------------ Atelier (manipulation vectorielle, calques, pré-vol, historique)
  let editor = null;
  let studio = null;
  let history = null;
  let restoring = false;
  const DESIGN_MEDIA = ["photos", "voices", "musics", "portrait", "portraitBytes", "fingerprint"];

  /** Enregistrement d'un nœud ; `peek` = lecture seule (aucune création). */
  function getRecord(id, peek) {
    const nodes = state.design.nodes = state.design.nodes || {};
    if (!nodes[id]) {
      if (peek) return nodes[id] || null;
      const legacy = (state.design.customPositions || {})[id];
      nodes[id] = legacy ? { dx: legacy.dx || 0, dy: legacy.dy || 0 } : {};
    }
    return nodes[id];
  }
  function nodeMeta(id) {
    for (const k of Object.keys(C.NODE_INDEX)) {
      const m = (C.NODE_INDEX[k] || []).find(n => n.id === id);
      if (m) return m;
    }
    return null;
  }
  function isLocked(id) {
    const rec = (state.design.nodes || {})[id];
    if (rec && rec.locked != null) return rec.locked;
    const m = nodeMeta(id);
    return !!(m && m.locked);
  }

  function captureSnapshot() {
    const design = {};
    for (const [k, v] of Object.entries(state.design)) if (!DESIGN_MEDIA.includes(k)) design[k] = v;
    return JSON.stringify({ data: state.data, design });
  }
  function restoreSnapshot(snap) {
    const o = JSON.parse(snap);
    restoring = true;
    state.data = o.data;
    for (const [k, v] of Object.entries(o.design)) state.design[k] = v;
    if (!o.design.nodes) state.design.nodes = {};
    syncMirrors(state.data);
    refreshInputs();
    renderAnnexes();
    updateLayoutButtons();
    $$("[data-material]").forEach(x => x.setAttribute("aria-checked", x.dataset.material === state.design.material));
    persistToIndexedDb();
    persistIfMine();
    restoring = false;
    scheduleRender();
  }
  let historySaveTimer = 0;
  function persistHistory(h) {
    if (!dbManager || !dbManager.saveHistory || !state.data) return;
    const id = state.data.id;
    clearTimeout(historySaveTimer);
    historySaveTimer = setTimeout(() => dbManager.saveHistory(id, h), 400);
  }
  function updateHistoryButtons() {
    if (!history) return;
    $("#btnUndo").disabled = !history.canUndo();
    $("#btnRedo").disabled = !history.canRedo();
  }

  /** Valide une action de l'atelier : historique, persistance, rendu. */
  function commit(label, debounced) {
    if (restoring) return;
    if (debounced) history.pushDebounced(label, 500);
    else history.push(label);
    persistToIndexedDb();
    scheduleRender();
  }

  function setAtelier(on) {
    state.atelier = !!on && state.tab !== "pavs";
    document.body.classList.toggle("atelier", state.atelier);
    $("#btnAtelier").classList.toggle("active-wysiwyg", state.atelier);
    $("#btnAtelier").setAttribute("aria-pressed", String(state.atelier));
    $("#studio").hidden = !state.atelier;
    $("#atelierHelp").hidden = !state.atelier;
    if (state.atelier && state.view !== "side") setView("side");
    editor.setEnabled(state.atelier);
    scheduleRender();
  }

  /** Superposition des zones contrôlées par le pré-vol (marges, fond perdu, exclusion NFC). */
  function drawZones() {
    const pf = studio && studio.lastPreflight();
    for (const [face, el] of [[`${currentCard()}recto`, $("#holderRecto")], [`${currentCard()}verso`, $("#holderVerso")]]) {
      const svg = el.querySelector("svg.card-svg");
      if (!svg) continue;
      const old = svg.querySelector(":scope > g.pf-zones");
      if (old) old.remove();
      if (!state.atelier || !state.showZones) continue;
      const z = pf && pf.zones.find(x => x.face === face);
      const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
      g.setAttribute("class", "pf-zones");
      g.innerHTML = window.PaxPreflight.zonesOverlay(C.W, C.H, z && z.zones, 0.12);
      svg.insertBefore(g, svg.querySelector(":scope > g.ed-overlay"));
    }
  }

  function runPreflight() {
    const card = currentCard();
    const mat = C.MATERIALS[state.design.material] || C.MATERIALS.ivoire;
    return window.PaxPreflight.run({
      faces: [[`${card}recto`, $("#holderRecto")], [`${card}verso`, $("#holderVerso")]].map(([face, el]) => ({ face, svg: el.querySelector("svg.card-svg") })),
      editor, getRecord: id => getRecord(id, true), materialBg: [mat.bg1, mat.bg2], accent: state.design.gold || mat.accent, W: C.W, H: C.H
    });
  }

  /** Reflet spéculaire : oriente les dégradés de dorure et d'hologramme selon la souris. */
  function bindSpecular() {
    ["#holderRecto", "#holderVerso"].forEach(sel => {
      const holder = $(sel);
      holder.addEventListener("pointermove", e => {
        if (state.design.specular === false) return;
        const r = holder.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width - 0.5;
        const py = (e.clientY - r.top) / r.height - 0.5;
        holder.querySelectorAll("linearGradient.foil").forEach(gr => {
          const holo = gr.classList.contains("holo");
          gr.setAttribute("gradientTransform", holo
            ? `translate(${(px * 14).toFixed(2)} ${(py * 6).toFixed(2)}) rotate(${(px * 40).toFixed(1)})`
            : `rotate(${(px * 70).toFixed(1)} .5 .5) translate(${(px * 0.35).toFixed(3)} ${(py * 0.35).toFixed(3)})`);
        });
      });
      holder.addEventListener("pointerleave", () => holder.querySelectorAll("linearGradient.foil").forEach(gr => gr.removeAttribute("gradientTransform")));
    });
  }

  function bindAtelier() {
    history = window.PaxHistory.create({
      capture: captureSnapshot,
      restore: restoreSnapshot,
      persist: persistHistory,
      onChange: () => { updateHistoryButtons(); if (studio) studio.refresh(); }
    });
    editor = window.PaxEditor.create({
      getHolders: () => (state.view === "side" && state.tab !== "pavs"
        ? [{ face: `${currentCard()}recto`, el: $("#holderRecto") }, { face: `${currentCard()}verso`, el: $("#holderVerso") }] : []),
      getRecord,
      isLocked,
      onSelect: () => { if (studio) studio.onSelection(); },
      onCommit: label => commit(label)
    });
    studio = window.PaxStudio.create({ state, editor, history, getRecord, isLocked, commit, currentCard, runPreflight, toast, refreshCanvas: scheduleRender });

    $("#btnAtelier").addEventListener("click", () => {
      setAtelier(!state.atelier);
      toast(state.atelier ? "Atelier activé : sélectionnez, déplacez, redimensionnez et faites pivoter les éléments." : "Atelier fermé.");
    });
    $("#btnUndo").addEventListener("click", () => history.undo());
    $("#btnRedo").addEventListener("click", () => history.redo());
    $("#btnResetPositions").addEventListener("click", () => {
      const prefix = `c${currentCard()}`;
      for (const id of Object.keys(state.design.nodes || {})) if (id.startsWith(prefix)) delete state.design.nodes[id];
      for (const id of Object.keys(state.design.customPositions || {})) if (id.startsWith(prefix)) delete state.design.customPositions[id];
      editor.select(null, []);
      commit("Réinitialiser la mise en page");
      toast("Mise en page d'origine rétablie pour cette carte.");
    });

    // Raccourcis d'historique (les champs de saisie gardent leur annulation native)
    document.addEventListener("keydown", e => {
      const t = e.target;
      if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
      const mod = e.ctrlKey || e.metaKey;
      if (!mod) return;
      const k = e.key.toLowerCase();
      if (k === "z" && !e.shiftKey) { e.preventDefault(); history.undo(); }
      else if (k === "y" || (k === "z" && e.shiftKey)) { e.preventDefault(); history.redo(); }
    });

    // Zoom à la molette sur une photo (atelier)
    ["#holderRecto", "#holderVerso"].forEach(sel => {
      $(sel).addEventListener("wheel", e => {
        if (!state.atelier) return;
        const photoGroup = e.target.closest("[data-photo-idx]");
        if (!photoGroup) return;
        e.preventDefault();
        const idx = Number(photoGroup.dataset.photoIdx);
        const p = state.design.photos && state.design.photos[idx];
        if (!p) return;
        p.crop = p.crop || { scale: 1.0, x: 0, y: 0, rotation: 0 };
        p.crop.scale = Math.max(0.5, Math.min(3.0, Number((p.crop.scale + (e.deltaY < 0 ? 0.05 : -0.05)).toFixed(2))));
        renderPhotosPanel();
        scheduleRender();
        persistToIndexedDb();
      }, { passive: false });
    });
    bindSpecular();
  }

  // ------------------------------------------------------------ Événements des Panneaux Carte 2
  function bindPanels() {
    const phPanel = $("#photosPanel");
    if (phPanel) {
      phPanel.addEventListener("change", e => {
        const up = e.target.closest("[data-photo-upload]");
        if (up && e.target.files[0]) {
          loadPhotoSlot(Number(up.dataset.photoUpload), e.target.files[0]);
          e.target.value = "";
        }
      });
      phPanel.addEventListener("input", e => {
        const cropProp = e.target.dataset.cropProp;
        if (cropProp) {
          const idx = Number(e.target.dataset.photoIdx);
          if (state.design.photos && state.design.photos[idx]) {
            const p = state.design.photos[idx];
            p.crop = p.crop || { scale: 1.0, x: 0, y: 0, rotation: 0 };
            p.crop[cropProp] = Number(e.target.value);
            const row = e.target.closest(".crop-slider-row");
            if (row && row.querySelector("output")) {
              row.querySelector("output").textContent = cropProp === "scale" ? `${Math.round(p.crop[cropProp] * 100)}%` : cropProp === "rotation" ? `${p.crop[cropProp]}°` : `${p.crop[cropProp]} mm`;
            }
            scheduleRender();
            persistToIndexedDb();
          }
        }
      });
      phPanel.addEventListener("click", e => {
        const del = e.target.closest("[data-photo-delete]");
        if (del) {
          const idx = Number(del.dataset.photoDelete);
          if (state.design.photos) state.design.photos[idx] = null;
          if (idx === 0) {
            state.design.portrait = null;
            state.design.portraitBytes = 0;
            state.data.multimedia_memorial.has_portrait = false;
          }
          renderPhotosPanel();
          scheduleRender();
          persistToIndexedDb();
          toast(`Photo ${idx + 1} supprimée.`);
        }
        const resetCrop = e.target.closest("[data-crop-reset]");
        if (resetCrop) {
          const idx = Number(resetCrop.dataset.cropReset);
          if (state.design.photos && state.design.photos[idx]) {
            state.design.photos[idx].crop = { scale: 1.0, x: 0, y: 0, rotation: 0 };
            renderPhotosPanel();
            scheduleRender();
            persistToIndexedDb();
          }
        }
      });
    }

    const vcPanel = $("#voicesPanel");
    if (vcPanel) {
      vcPanel.addEventListener("change", e => {
        const radio = e.target.closest('input[name="activeVoiceSlot"]');
        if (radio) {
          state.design.activeVoiceIndex = Number(radio.value);
          scheduleRender();
          persistToIndexedDb();
        }
        const up = e.target.closest("[data-voice-upload]");
        if (up && e.target.files[0]) {
          loadAudioFileSlot("voice", Number(up.dataset.voiceUpload), e.target.files[0]);
          e.target.value = "";
        }
      });
      vcPanel.addEventListener("input", e => {
        const ext = e.target.dataset.voiceExtract;
        if (ext != null) {
          const idx = Number(ext);
          if (state.design.voices && state.design.voices[idx]) {
            state.design.voices[idx].extract = e.target.value;
            if (state.design.activeVoiceIndex === idx) {
              state.design.voiceExtract = e.target.value;
            }
            scheduleRender();
            persistToIndexedDb();
          }
        }
      });
      vcPanel.addEventListener("click", e => {
        const recBtn = e.target.closest('[data-audio-record="voice"]');
        if (recBtn) {
          startAudioRecording("voice", Number(recBtn.dataset.slot));
        }
        const stopBtn = e.target.closest('[data-audio-stop="voice"]');
        if (stopBtn) {
          stopAudioRecording();
        }
        const del = e.target.closest("[data-voice-delete]");
        if (del) {
          const idx = Number(del.dataset.voiceDelete);
          if (state.design.voices) state.design.voices[idx] = null;
          renderVoicesPanel();
          scheduleRender();
          persistToIndexedDb();
          toast(`Enregistrement vocal ${idx + 1} effacé.`);
        }
      });
    }

    const muPanel = $("#musicsPanel");
    if (muPanel) {
      muPanel.addEventListener("change", e => {
        const radio = e.target.closest('input[name="activeMusicSlot"]');
        if (radio) {
          state.design.activeMusicIndex = Number(radio.value);
          scheduleRender();
          persistToIndexedDb();
        }
        const up = e.target.closest("[data-music-upload]");
        if (up && e.target.files[0]) {
          loadAudioFileSlot("music", Number(up.dataset.musicUpload), e.target.files[0]);
          e.target.value = "";
        }
      });
      muPanel.addEventListener("click", e => {
        const recBtn = e.target.closest('[data-audio-record="music"]');
        if (recBtn) {
          startAudioRecording("music", Number(recBtn.dataset.slot));
        }
        const stopBtn = e.target.closest('[data-audio-stop="music"]');
        if (stopBtn) {
          stopAudioRecording();
        }
        const del = e.target.closest("[data-music-delete]");
        if (del) {
          const idx = Number(del.dataset.musicDelete);
          if (state.design.musics) state.design.musics[idx] = null;
          renderMusicsPanel();
          scheduleRender();
          persistToIndexedDb();
          toast(`Fichier musical ${idx + 1} effacé.`);
        }
      });
    }
  }

  // ------------------------------------------------------------ liaisons formulaire ↔ données
  function refreshInputs(except) {
    const c = state.data;
    $$("[data-bind]").forEach(el => {
      if (el === except) return;
      const v = getPath(c, el.dataset.bind);
      if (el.type === "checkbox") el.checked = !!v;
      else el.value = v == null ? "" : v;
    });
    $$("[data-radio]").forEach(group => {
      const path = group.dataset.radio;
      const v = getPath(c, path);
      const radios = Array.from(group.querySelectorAll('input[type="radio"]'));
      let matched = false;
      radios.forEach(r => {
        if (r.value === "__other") return;
        const on = String(v) === r.value || (v == null && r.value === "null");
        r.checked = on;
        matched = matched || on;
      });
      const other = radios.find(r => r.value === "__other");
      if (other) {
        other.checked = !matched && !!v;
        const txt = group.querySelector(".other-text");
        if (txt !== except) txt.value = !matched && v ? v : "";
      }
    });
    $$("[data-list]").forEach(group => {
      const list = getPath(c, group.dataset.list) || [];
      const presets = Array.from(group.querySelectorAll("input")).map(i => i.value);
      group.querySelectorAll("input").forEach(i => { i.checked = list.includes(i.value); });
      const extra = list.filter(v => !presets.includes(v));
      const hint = group.parentElement.querySelector(".list-extra");
      if (hint) hint.textContent = extra.length ? `Autre(s) accompagnement(s) déclaré(s) : ${extra.join(", ")}` : "";
    });
    $$("[data-design]").forEach(el => {
      if (el === except) return;
      const v = state.design[el.dataset.design];
      if (el.type === "checkbox") el.checked = !!v;
      else el.value = v == null ? "" : v;
    });
    $$("[data-out]").forEach(o => {
      const v = state.design[o.dataset.out];
      o.textContent = o.dataset.out === "guillocheOpacity" ? `${Math.round(v * 100)} %` : o.dataset.out === "fontScale" ? `${Math.round(v * 100)} %` : v;
    });
    $$("[data-show]").forEach(el => { el.hidden = !getPath(c, el.dataset.show); });
  }

  function bindInputs() {
    $$("[data-bind]").forEach(el => {
      const ev = el.tagName === "SELECT" || el.type === "checkbox" || el.type === "date" ? "change" : "input";
      el.addEventListener(ev, () => {
        const val = el.type === "checkbox" ? el.checked : el.value;
        setPath(state.data, el.dataset.bind, convert(val, el.dataset.type));
        dataChanged(el);
      });
    });
    $$("[data-radio]").forEach(group => {
      const name = "r-" + group.dataset.radio.replace(/\./g, "-");
      group.querySelectorAll('input[type="radio"]').forEach(r => {
        r.name = name;
        r.addEventListener("change", () => {
          if (r.value === "__other") {
            const txt = group.querySelector(".other-text");
            txt.focus();
            setPath(state.data, group.dataset.radio, txt.value);
          } else setPath(state.data, group.dataset.radio, convert(r.value, group.dataset.type));
          dataChanged(r);
        });
      });
      const txt = group.querySelector(".other-text");
      if (txt) txt.addEventListener("input", () => {
        group.querySelector('input[value="__other"]').checked = true;
        setPath(state.data, group.dataset.radio, txt.value);
        dataChanged(txt);
      });
    });
    $$("[data-list]").forEach(group => {
      group.querySelectorAll("input").forEach(i => i.addEventListener("change", () => {
        const excl = group.dataset.exclusive;
        let list = (getPath(state.data, group.dataset.list) || []).filter(v => v !== i.value);
        if (i.checked) {
          // « Aucun » efface les autres choix, et inversement (comportement du formulaire officiel).
          list = i.value === excl ? [] : list.filter(v => v !== excl);
          list.push(i.value);
        }
        setPath(state.data, group.dataset.list, list);
        dataChanged(i);
      }));
    });
    $$("[data-design]").forEach(el => {
      const ev = el.tagName === "SELECT" || el.type === "checkbox" ? "change" : "input";
      el.addEventListener(ev, () => {
        const k = el.dataset.design;
        let v = el.type === "checkbox" ? el.checked : el.value;
        if (el.type === "range" || el.type === "number") v = Number(v);
        state.design[k] = v;
        refreshInputs(el);
        scheduleRender();
        if (history && !restoring) history.pushDebounced("Réglage du design");
      });
    });
  }

  function dataChanged(source) {
    if (!state.data) return;
    syncMirrors(state.data);
    refreshInputs(source);
    persistIfMine();
    scheduleRender();
    scheduleFingerprint();
    if (history && !restoring) history.pushDebounced("Saisie du dossier");
  }

  let persistTimer = 0;
  function persistIfMine() {
    const i = state.saved.findIndex(c => c.id === state.data.id);
    if (i < 0) return;
    clearTimeout(persistTimer);
    persistTimer = setTimeout(() => {
      state.saved[i] = clone(state.data);
      persistSaved();
      const opt = $(`#caseSelect option[value="${CSS.escape(state.data.id)}"]`);
      if (opt) opt.textContent = `${state.data.civil_identity.full_name || "PAVS sans nom"} · ${state.data.id}`;
    }, 400);
  }

  // ------------------------------------------------------------ empreinte SHA-256 (dossier canonique)
  function canonical(v) {
    if (Array.isArray(v)) return `[${v.map(canonical).join(",")}]`;
    if (v && typeof v === "object") return `{${Object.keys(v).sort().map(k => JSON.stringify(k) + ":" + canonical(v[k])).join(",")}}`;
    return JSON.stringify(v);
  }
  let fpTimer = 0;
  function scheduleFingerprint() {
    clearTimeout(fpTimer);
    fpTimer = setTimeout(async () => {
      try {
        const bytes = new TextEncoder().encode(canonical(state.data));
        const buf = await crypto.subtle.digest("SHA-256", bytes);
        state.design.fingerprint = Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, "0")).join("");
      } catch (e) {
        state.design.fingerprint = "";
      }
      scheduleRender();
    }, 250);
  }

  // ------------------------------------------------------------ rendu
  let raf = 0;
  function scheduleRender() {
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(refresh);
  }

  function currentCard() { return state.tab === "card2" ? 2 : 1; }

  function refresh() {
    const c = state.data;
    if (!c) return;
    document.body.dataset.tab = state.tab;
    const card = currentCard();
    const opts = { crop: state.crop, safe: state.safe };
    if (state.tab !== "pavs") {
      // Un seul jeu de faces dans le DOM à la fois : les identifiants SVG (dégradés, découpes) restent uniques.
      const side = state.view === "side";
      const recto = C.render(card, "recto", c, state.design, Object.assign({ prefix: side ? "r" : "fr" }, opts));
      const verso = C.render(card, "verso", c, state.design, Object.assign({ prefix: side ? "v" : "fv" }, opts));
      $("#holderRecto").innerHTML = side ? recto : "";
      $("#holderVerso").innerHTML = side ? verso : "";
      $("#flipFront").innerHTML = side ? "" : recto;
      $("#flipBack").innerHTML = side ? "" : verso;
      $("#miniPreview").innerHTML = "";
    } else {
      $("#holderRecto").innerHTML = $("#holderVerso").innerHTML = $("#flipFront").innerHTML = $("#flipBack").innerHTML = "";
      $("#miniPreview").innerHTML =
        `<p class="field-label">Aperçu Carte 1 (en direct)</p>` +
        C.render(1, "recto", c, state.design, { prefix: "mr" }) + C.render(1, "verso", c, state.design, { prefix: "mv" });
    }
    if (editor && state.tab !== "pavs") {
      editor.attach();
      if (state.atelier) studio.afterRender();
      drawZones();
    }
    $("#canvas").classList.toggle("pulse", !!state.design.pulse && card === 2);
    document.documentElement.style.setProperty("--zoom", state.zoom);
    renderStatus();
    renderNotices();
  }

  function renderStatus() {
    const c = state.data;
    const ci = c.civil_identity;
    const bat = c.bat_status;
    const niss = R.validateNiss(ci.national_id_niss, ci.birth_date, ci.gender);
    const pyro = R.pyroStatus(c);
    const tone = bat.ready_to_print ? "ok" : ["ATTENTION_RADIO_ISOTOPES", "INCOMPLET_IDENTITE"].includes(bat.carte_1_status) ? "warn" : "danger";
    const portrait = state.design.portraitBytes;
    const ef = [
      ["EF-0", "Métadonnées", 512], ["EF-1", "Profil CBOR", 2048], ["EF-2", "Portrait WebP", 20480],
      ["EF-3", "Mémo vocal", 46080], ["EF-4", "Directives", 15360], ["EF-5", "Sceau COSE", 2048]
    ];
    $("#statusCard").innerHTML = `
      <div class="status-head">
        <span class="badge ${tone}">${escapeHtml(R.BAT_LABELS[bat.carte_1_status] || bat.carte_1_status)}</span>
        <code>${escapeHtml(c.id)}</code>
      </div>
      <p class="status-title">${escapeHtml(c.label || "")}</p>
      <ul class="checks">
        <li class="${niss.valid ? "ok" : "danger"}">NISS modulo 97 : ${niss.valid ? "valide" : "invalide (" + escapeHtml(niss.reason) + ")"}${niss.sexOk === false ? " · parité séquence/genre incohérente" : ""}</li>
        <li class="${pyro.level}">${escapeHtml(pyro.title)}</li>
      </ul>
      <details class="ef"><summary>Budget silicium ACOSJ 92 Ko</summary>
        <table>${ef.map(([id, label, q]) => `<tr><td>${id}</td><td>${label}</td><td>${id === "EF-2" && portrait ? `${portrait.toLocaleString("fr-BE")} / ` : ""}${q.toLocaleString("fr-BE")} o</td></tr>`).join("")}
        <tr class="total"><td colspan="2">Utile · réserve 5 632 o (6,11 %)</td><td>86 528 / 92 160 o</td></tr></table>
      </details>`;
    const rep = C.card1Report(c, state.design);
    const warnings = R.pavsWarnings(c);
    $("#statusCard").insertAdjacentHTML("beforeend", `
      <p class="density ${rep.overflow.length ? "danger" : rep.pt < 3.4 ? "warn" : "ok"}">Carte 1 · corps unique ${rep.size.toFixed(2).replace(".", ",")} mm (≈ ${rep.pt.toFixed(1).replace(".", ",")} pt)${rep.overflow.length ? ` · tronqué : ${escapeHtml(rep.overflow.join(", "))}` : " · toutes les données affichées"}${!rep.overflow.length && rep.pt < 3.4 ? " · micro-texte : lecture à la loupe" : ""}</p>
      ${warnings.length ? `<ul class="warnings">${warnings.map(w => `<li class="${w.level}">${escapeHtml(w.text)}</li>`).join("")}</ul>` : ""}`);
    const pw = $("#pavsWarnings");
    if (pw) pw.innerHTML = warnings.map(w => `<li class="${w.level}">${escapeHtml(w.text)}</li>`).join("");
    const hint = niss.valid ? "✓ modulo 97" : ci.national_id_niss ? `✗ ${niss.reason}` : "";
    $$("#nissHint, .niss-hint").forEach(h => { h.textContent = hint; h.className = `hint ${niss.valid ? "ok" : "danger"} ${h.id ? "" : "niss-hint"}`; });
  }

  function renderNotices() {
    const c = state.data;
    const sarco = R.isSarco(c.funeral_wills.burial_mode);
    $$(".sarco-notice").forEach(n => { n.hidden = !sarco; n.textContent = `Sarcomusation : ${R.SARCO_NOTICE} (DEC-AET-15). Les 5 destinations cinéraires et le verrou pyrotechnique s'appliquent comme pour la crémation.`; });
    const pyro = R.pyroStatus(c);
    $$(".pyro-notice").forEach(n => {
      n.hidden = !c.medical_record.has_pacemaker;
      n.className = `notice pyro-notice ${pyro.level}`;
      n.textContent = `${pyro.title} — ${pyro.detail}`;
    });
    $$(".science-hint").forEach(n => { n.hidden = !c.medical_record.body_donation_science; });
  }

  // ------------------------------------------------------------ portrait (DEC-AET-12 : WebP 480×480 ≤ 20 480 o)
  async function loadPortrait(file) {
    const info = $("#portraitInfo");
    try {
      const bmp = await createImageBitmap(file);
      const side = Math.min(bmp.width, bmp.height);
      const cv = document.createElement("canvas");
      cv.width = cv.height = 480;
      cv.getContext("2d").drawImage(bmp, (bmp.width - side) / 2, (bmp.height - side) / 2, side, side, 0, 0, 480, 480);
      let blob = null;
      let q = 0.8;
      for (; q >= 0.2; q -= 0.05) {
        blob = await new Promise(res => cv.toBlob(res, "image/webp", q));
        if (!blob || blob.type !== "image/webp" || blob.size <= 20480) break;
      }
      if (!blob || blob.type !== "image/webp") {
        info.textContent = "Ce navigateur ne sait pas encoder le WebP : portrait non retenu.";
        info.className = "hint danger";
        return;
      }
      state.design.portrait = await new Promise(res => { const r = new FileReader(); r.onload = () => res(r.result); r.readAsDataURL(blob); });
      state.design.portraitBytes = blob.size;
      const ok = blob.size <= 20480;
      info.textContent = `WebP 480×480 · ${blob.size.toLocaleString("fr-BE")} o · q ${q.toFixed(2).replace(".", ",")} ${ok ? "✓ EF-2" : "✗ dépasse EF-2"}`;
      info.className = `hint ${ok ? "ok" : "danger"}`;
      state.data.multimedia_memorial.has_portrait = true;
      scheduleRender();
    } catch (e) {
      info.textContent = "Image illisible.";
      info.className = "hint danger";
    }
  }

  // ------------------------------------------------------------ export SVG (polices embarquées si possible)
  async function fontFaceCss() {
    const keys = new Set([state.design.fontTitle, state.design.fontBody, "inter", "fira"]);
    let css = "";
    for (const k of keys) {
      const [family, files] = FONT_FILES[k] || [];
      if (!family) continue;
      for (const [file, weight, style] of files) {
        const resp = await fetch(`fonts/${file}.woff2`);
        if (!resp.ok) throw new Error("font");
        const buf = new Uint8Array(await resp.arrayBuffer());
        let bin = "";
        for (let i = 0; i < buf.length; i += 0x8000) bin += String.fromCharCode.apply(null, buf.subarray(i, i + 0x8000));
        css += `@font-face{font-family:'${family}';font-weight:${weight};font-style:${style};src:url(data:font/woff2;base64,${btoa(bin)}) format('woff2');}`;
      }
    }
    return css;
  }

  async function exportSvg(side) {
    const card = currentCard();
    let svg = C.render(card, side, state.data, state.design, { export: true, crop: state.crop, safe: state.safe, prefix: "x" });
    let embedded = true;
    try {
      svg = svg.replace("<defs>", `<defs><style>${await fontFaceCss()}</style>`);
    } catch (e) {
      embedded = false;
    }
    const name = `aeternitrak_carte${card}_${side}_${slug(state.data.civil_identity.full_name || state.data.id)}.svg`;
    download(name, `<?xml version="1.0" encoding="UTF-8"?>\n${svg}`, "image/svg+xml");
    toast(embedded ? `${name} exporté (polices embarquées).` : `${name} exporté — polices non embarquées (ouvrez l'app via un serveur local pour les inclure).`);
  }

  function download(name, content, type) {
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([content], { type }));
    a.download = name;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
  }

  // ------------------------------------------------------------ impression B.A.T. 1:1
  function printBat() {
    const c = state.data;
    const card = currentCard();
    const opts = { print: true, crop: true, safe: state.safe };
    const bat = c.bat_status;
    const today = new Date().toLocaleDateString("fr-BE");
    const blocked = card === 1 && !bat.ready_to_print;
    $("#printSheet").innerHTML = `
      <div class="ps-page">
        <header class="ps-head">
          <strong>Bon à tirer · AeterniTrak · Carte ${card} ${card === 1 ? "Volontés & sécurité" : "Mémorial & acoustique"}</strong>
          <span>${escapeHtml(c.civil_identity.full_name || "")} · ${escapeHtml(c.id)} · ${today}</span>
        </header>
        ${blocked ? `<p class="ps-blocked">B.A.T. NON VALIDABLE — ${escapeHtml(R.BAT_LABELS[bat.carte_1_status])}. Épreuve de contrôle uniquement.</p>` : ""}
        <div class="ps-faces">
          <figure>${C.render(card, "recto", c, state.design, Object.assign({ prefix: "pr" }, opts))}<figcaption>Recto</figcaption></figure>
          <figure>${C.render(card, "verso", c, state.design, Object.assign({ prefix: "pv" }, opts))}<figcaption>Verso</figcaption></figure>
        </div>
        <svg class="ps-ruler" xmlns="http://www.w3.org/2000/svg" width="100mm" height="6mm" viewBox="0 0 100 6">
          <path d="M0 5.5H100${Array.from({ length: 11 }, (_, i) => `M${i * 10} 5.5V${i % 5 ? 3 : 1}`).join("")}" stroke="#000" stroke-width=".15" fill="none"/>
        </svg>
        ${card === 1 ? `<div class="ps-legend"><strong>Légende des pictogrammes</strong>${$("#legend").innerHTML}</div>` : ""}
        <p class="ps-foot">Échelle 1:1 — la règle doit mesurer exactement 100 mm et chaque carte 85,60 × 53,98 mm (imprimer à 100 %, sans « ajuster à la page »). Traits de coupe 5 mm, fond perdu 2 mm${state.safe ? ", zone de sécurité 3 mm (cyan)" : ""}, ligne de découpe magenta. Rendu vectoriel : résolution ≥ 300 DPI garantie par l'imprimante.</p>
      </div>`;
    document.body.classList.add("printing-bat");
    window.print();
  }

  function printPavs() {
    const c = syncMirrors(state.data);
    const ci = c.civil_identity;
    const pr = c.pavs_record;
    const care = pr.care;
    const pm = pr.post_mortem_wills || {};
    const P = R.PAVS;
    const box = on => (on ? "☒" : "☐");
    const opt = (list, cur) => list.map(([v, l]) => `${box(String(cur) === String(v))} ${l}`).join("   ");
    const contact = o => (o && (o.name || o.phone) ? `${o.name || ""}${o.phone ? " · " + o.phone : ""}` : "—");
    const row = (q, a) => `<tr><th>${escapeHtml(q)}</th><td>${a == null || a === "" ? "—" : a}</td></tr>`;
    const t = v => escapeHtml(v || "");
    const yesNoX = [["Oui", "Oui"], ["Non", "Non"], ["X", "Sans préférence"]];
    const phy = ci.certifying_physician || {};
    $("#printSheet").innerHTML = `
      <div class="ps-page pavs-print">
        <h1>Ajouter un PAVS (mes volontés)</h1>
        <p class="ps-sub">Plan anticipé de volontés et soins · Réseau Santé Wallon · date d'enregistrement : ${C.shortDate(pr.registered_date)}</p>
        <h2>Cinq points d'attention</h2>
        <ol class="ps-attention">
          <li>Résumé de votre PSPA — lieu de conservation : <strong>${t(pr.conservation_place) || "—"}</strong></li>
          <li>À tout moment, vous avez la possibilité de modifier votre PSPA et votre PAVS.</li>
          <li>Le PSPA et le PAVS ne sont utiles que si vous n’êtes plus en capacité de vous exprimer.</li>
          <li>Il est conseillé de compléter ce document en concertation avec un professionnel de la santé et/ou un proche.</li>
          <li>Ce document ne sera plus accessible sur le Réseau Santé Wallon après le décès : conservez-en une copie.</li>
        </ol>
        <h2>Mes données administratives</h2>
        <table>${row("Nom et prénom", t(ci.full_name))}${row("Téléphone", t(ci.phone))}${row("Numéro de registre national", t(ci.national_id_niss))}
          ${row("Genre", opt([["M", "Homme"], ["F", "Femme"]], ci.gender))}
          ${row("Institution(s)", t(contact(pr.institution)))}${row("Médecin traitant", t(contact(phy)) + (phy.inami ? ` · INAMI ${t(phy.inami)}` : ""))}
          ${row("Personne(s) à contacter", t(contact(pr.contact_person)))}${row("Mandataire (pour les soins de santé)", t(contact(pr.health_proxy)))}
          ${row("Mandataire extrajudiciaire", t(contact(pr.extrajudicial_proxy)))}${row("Personne(s) de confiance", t(contact(pr.trusted_person)))}
          ${row("Administrateur de biens et/ou de la personne", t(contact(pr.property_administrator)))}</table>
        <h2>Mon projet de soins</h2>
        <table>${row("Projet global (intensité des soins)", `${opt(P.INTENSITY.map(i => [i.id, i.label]), care.intensity)}   ${box(care.comfort)} Soins de confort/palliatifs   ${box(care.euthanasia_declaration)} Déclaration anticipée d’euthanasie signée`)}
          ${row("Thérapies refusées", P.REFUSALS.map(r => `${box(care.refusals.includes(r.id))} ${r.group === "nutrition" ? "Alimentation artificielle — " : r.group === "respiration" ? "Aide à la respiration — " : ""}${r.label}`).join("<br>"))}
          ${row("À soins égaux je préfère être", P.SETTINGS.map(x => `${box(care.settings.includes(x.id))} ${x.label}`).join("   "))}
          ${row("Types d’hospitalisations acceptés", `${opt([["avec", "Hospitalisation avec réanimation"], ["sans", "Hospitalisation sans réanimation"]], care.reanimation)}   ${box(care.exceptional_hospitalization)} Hospitalisation exceptionnelle (fracture, occlusion, etc.)`)}
          ${row("Commentaires", t(pr.comments))}</table>
        <h2>Mes souhaits de fin de vie</h2>
        <table>${row("Pour ma fin de vie, je préfère – si possible – être dans mon lieu de vie habituel", opt(yesNoX, pr.eol_at_home))}
          ${row("Je désire un accompagnement", P.SUPPORT.map(x => `${box(pr.desired_support.choices.includes(x.id))} ${x.label}`).join("   "))}
          ${row("A propos de mon accompagnement, je souhaite en particulier", t(pr.desired_support.special_wishes))}
          ${row("Pour moi, l’essentiel c’est", t(pr.essential_priority))}${row("Mes autres souhaits", t(pr.other_wishes))}</table>
        <h2>Mes volontés pour l’après-décès</h2>
        <table>${row("J’accepte de donner mes organes", opt([[1, "Oui"], [3, "Non"], [2, "Sans préférence"]], c.medical_record.organ_donation_status))}
          ${row("Je donne mon corps à la science", opt(yesNoX, pm.body_donation))}
          ${row("Je désire être", opt(P.DISPOSITION.map(d => [d.id, d.label]), pm.body_disposition))}
          ${row("J'ai un pacemaker", opt([[true, "Oui"], [false, "Non"]], !!c.medical_record.has_pacemaker))}
          ${row("Je laisse à mes proches le choix de mes obsèques", opt([[true, "Oui"], [false, "Non"]], pm.leave_choice_to_relatives))}
          ${row("Rite(s)/rituel(s) à respecter", t(pm.rites))}${row("Coordonnées des pompes funèbres de mon choix", t(c.funeral_wills.chosen_funeral_home))}
          ${row("Je dispose d’une assurance obsèques", opt([[true, "Oui"], [false, "Non"]], !!c.funeral_wills.has_funeral_insurance) + (pm.funeral_insurance_ref ? ` · ${t(pm.funeral_insurance_ref)}` : ""))}
          ${row("Mes autres souhaits", t(pm.other_wishes))}</table>
        <h2>Annexe(s) éventuelle(s)</h2>
        <p>${(pr.attachments || []).length ? pr.attachments.map(a => t(a.name)).join(" · ") : "Aucune"}</p>
        <p class="ps-foot">Formulaire conçu par UNESSA · copie générée par PaxStudio Design (AeterniTrak) · Signature : ______________________ Date : ____________</p>
      </div>`;
    document.body.classList.add("printing-bat");
    window.print();
  }

  // ------------------------------------------------------------ « Ajouter un PAVS »
  function newPavs() {
    const id = `MON_PAVS_${Date.now().toString(36).toUpperCase()}`;
    const c = R.blankCase(id);
    state.saved.unshift(c);
    persistSaved();
    populateSelect();
    selectCase(id);
    setTab("pavs");
    toast("Nouveau PAVS créé — il est enregistré sur cet appareil au fil de la saisie.");
    const first = $('#pavsView [data-bind="civil_identity.full_name"]');
    if (first) first.focus();
  }

  function savePavs() {
    const mine = state.saved.findIndex(c => c.id === state.data.id);
    if (mine >= 0) {
      state.saved[mine] = clone(state.data);
    } else {
      const copy = clone(state.data);
      copy.id = `MON_PAVS_${Date.now().toString(36).toUpperCase()}`;
      copy.label = `Copie de ${state.data.label}`;
      state.saved.unshift(copy);
      state.data = clone(copy);
    }
    const ok = persistSaved();
    state.pristine = clone(state.data);
    populateSelect();
    $("#caseSelect").value = state.data.id;
    toast(ok ? "PAVS enregistré dans « Mes PAVS » (sur cet appareil)." : "Stockage local indisponible : exportez le PAVS en JSON pour le conserver.");
  }

  function importPavs(file) {
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const c = JSON.parse(reader.result);
        if (!c || !c.civil_identity || !c.pavs_record || !c.funeral_wills || !c.medical_record) throw new Error("format");
        const base = R.blankCase(c.id || "IMPORT");
        const merged = Object.assign(base, c);
        if (allCases().some(x => x.id === merged.id)) merged.id = `MON_PAVS_${Date.now().toString(36).toUpperCase()}`;
        merged.multimedia_memorial = Object.assign(R.blankCase("x").multimedia_memorial, c.multimedia_memorial || {});
        state.saved.unshift(syncMirrors(merged));
        persistSaved();
        populateSelect();
        selectCase(merged.id);
        toast("PAVS importé.");
      } catch (e) {
        toast("Fichier JSON non reconnu comme dossier PAVS.");
      }
    };
    reader.readAsText(file);
  }

  // ------------------------------------------------------------ fiches didactiques (modales)
  function openFiche(id) {
    const tpl = document.getElementById(`fiche-${id}`);
    if (!tpl) return;
    $("#ficheTitle").textContent = tpl.dataset.title;
    const body = $("#ficheBody");
    body.innerHTML = "";
    body.appendChild(tpl.content.cloneNode(true));
    const dlg = $("#ficheDialog");
    if (typeof dlg.showModal === "function") dlg.showModal();
    else dlg.setAttribute("open", "");
    body.scrollTop = 0;
  }

  // ------------------------------------------------------------ annexes (3 fichiers, 6 Mo, extensions du formulaire officiel)
  function addAnnexes(files) {
    const list = state.data.pavs_record.attachments = state.data.pavs_record.attachments || [];
    const refused = [];
    for (const file of files) {
      const ext = (file.name.split(".").pop() || "").toLowerCase();
      const total = list.reduce((a, b) => a + b.size, 0);
      if (!R.PAVS.ATTACHMENTS_EXT.includes(ext)) refused.push(`${file.name} (extension)`);
      else if (list.length >= R.PAVS.ATTACHMENTS_MAX) refused.push(`${file.name} (3 annexes maximum)`);
      else if (total + file.size > R.PAVS.ATTACHMENTS_MAX_BYTES) refused.push(`${file.name} (6 Mo dépassés)`);
      else list.push({ name: file.name, size: file.size, type: file.type || ext });
    }
    if (refused.length) toast(`Non ajouté : ${refused.join(", ")}`);
    renderAnnexes();
    dataChanged();
  }

  function renderAnnexes() {
    const list = (state.data && state.data.pavs_record.attachments) || [];
    const total = list.reduce((a, b) => a + b.size, 0);
    const mo = n => (n / 1048576).toFixed(2).replace(".", ",");
    $("#annexCount").textContent = `Pièces jointes : ${list.length} sur ${R.PAVS.ATTACHMENTS_MAX}`;
    $("#annexSize").textContent = `${mo(total)} Mo / 6,00 Mo`;
    $("#annexBar").style.width = `${Math.min(100, (total / R.PAVS.ATTACHMENTS_MAX_BYTES) * 100)}%`;
    $("#annexList").innerHTML = list.map((a, i) => `<li><span>${escapeHtml(a.name)}</span><small>${mo(a.size)} Mo</small><button type="button" class="btn ghost" data-annex="${i}" aria-label="Retirer ${escapeHtml(a.name)}">Retirer</button></li>`).join("");
  }

  // ------------------------------------------------------------ légende des pictogrammes
  function renderLegend() {
    const O = window.PaxOrnaments;
    const ico = name => `<svg viewBox="0 0 24 24" class="lg-icon" aria-hidden="true"><path d="${O.ICONS[name]}" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
    const mk = kind => `<svg viewBox="-1.2 -1.2 2.4 2.4" class="lg-mark" aria-hidden="true">${O.mark(0, 0, 1, kind)}</svg>`;
    $("#legend").innerHTML = C.card1Legend().map(g => `<section><h4>${escapeHtml(g.group)}</h4><ul>` +
      (g.items || []).map(([i, l]) => `<li>${ico(i)}<span>${escapeHtml(l)}</span></li>`).join("") +
      (g.marks || []).map(([k, l]) => `<li>${mk(k)}<span>${escapeHtml(l)}</span></li>`).join("") + `</ul></section>`).join("") +
      `<p class="hint">Pictogramme estompé : case non cochée.</p>`;
  }

  // ------------------------------------------------------------ navigation & interface
  function setTab(tab) {
    state.tab = tab;
    $$(".tab").forEach(t => { const on = t.dataset.tab === tab; t.classList.toggle("active", on); t.setAttribute("aria-selected", on); });
    $("#pavsView").hidden = tab !== "pavs";
    $("#canvas").hidden = tab === "pavs";
    $("#cardToolbar").hidden = tab === "pavs";
    if (editor) {
      editor.select(null, []);
      if (tab === "pavs" && state.atelier) setAtelier(false);
      $("#studio").hidden = !state.atelier || tab === "pavs";
    }
    $$("[data-only=card2]").forEach(el => { el.hidden = tab !== "card2"; });
    $$("[data-only=card1]").forEach(el => { el.hidden = tab !== "card1"; });
    if (tab === "card2") {
      renderPhotosPanel();
      renderVoicesPanel();
      renderMusicsPanel();
    }
    refresh();
  }

  function setView(view) {
    if (state.atelier && view !== "side") { toast("L'atelier travaille en vue Recto · Verso."); view = "side"; }
    state.view = view;
    $$("[data-view]").forEach(b => b.classList.toggle("on", b.dataset.view === view));
    $("#faces").hidden = view !== "side";
    $("#flipWrap").hidden = view !== "flip";
    refresh();
  }

  function buildControls() {
    const modes = R.BURIAL_MODES.reduce((acc, m) => {
      (acc[m.family] = acc[m.family] || []).push(m);
      return acc;
    }, {});
    const famLabel = { inhumation: "Inhumation", cremation: "Crémation (procédé thermique)", sarco: "Sarcomusation (démonstrateur prospectif · thermique)", humusation: "Humusation", science: "Science" };
    $$(".burial-select").forEach(sel => {
      sel.innerHTML = Object.keys(modes).map(f => `<optgroup label="${famLabel[f]}">${modes[f].map(m => `<option value="${m.id}">${m.id}. ${escapeHtml(m.label)}</option>`).join("")}</optgroup>`).join("");
    });
    $$(".font-select").forEach(sel => {
      sel.innerHTML = Object.entries(C.FONTS).map(([k, v]) => `<option value="${k}" style="font-family:${v.stack}">${v.label}</option>`).join("");
    });
    $("#materialSwatches").innerHTML = Object.entries(C.MATERIALS).map(([k, m]) =>
      `<button role="radio" data-material="${k}" aria-checked="${k === state.design.material}" title="${escapeHtml(m.label)}" style="--sw1:${m.bg1};--sw2:${m.bg2};--swa:${m.accent}"><span></span>${escapeHtml(m.label.split(" ")[0])}</button>`).join("");
    $$("[data-material]").forEach(b => b.addEventListener("click", () => {
      state.design.material = b.dataset.material;
      state.design.gold = C.MATERIALS[b.dataset.material].accent;
      $$("[data-material]").forEach(x => x.setAttribute("aria-checked", x === b));
      refreshInputs();
      scheduleRender();
      if (history) history.push(`Matériau : ${C.MATERIALS[b.dataset.material].label}`);
    }));
    $$("[data-layout]").forEach(b => b.addEventListener("click", () => {
      state.design.layout = b.dataset.layout;
      updateLayoutButtons();
      scheduleRender();
      persistToIndexedDb();
      if (history) history.push(`Gabarit ${b.dataset.layout}`);
    }));
    updateLayoutButtons();
  }

  function updateLayoutButtons() {
    $$("[data-layout]").forEach(b => { b.classList.toggle("on", b.dataset.layout === state.design.layout); b.setAttribute("aria-checked", b.dataset.layout === state.design.layout); });
    $("#layoutName").textContent = LAYOUT_NAMES[state.design.layout];
  }

  function bindUi() {
    $$(".tab").forEach(t => t.addEventListener("click", () => setTab(t.dataset.tab)));
    $$("[data-view]").forEach(b => b.addEventListener("click", () => setView(b.dataset.view)));
    $("#caseSelect").addEventListener("change", e => selectCase(e.target.value));
    $("#btnNewPavs").addEventListener("click", newPavs);
    $("#chkCrop").addEventListener("change", e => { state.crop = e.target.checked; scheduleRender(); });
    $("#chkSafe").addEventListener("change", e => { state.safe = e.target.checked; scheduleRender(); });
    $("#zoom").addEventListener("input", e => { state.zoom = Number(e.target.value); scheduleRender(); });
    $("#flipper").addEventListener("click", () => { state.flipped = !state.flipped; $("#flipper").classList.toggle("flipped", state.flipped); });
    $("#btnSvgRecto").addEventListener("click", () => exportSvg("recto"));
    $("#btnSvgVerso").addEventListener("click", () => exportSvg("verso"));
    $("#btnPrint").addEventListener("click", printBat);
    $("#btnPavsPrint").addEventListener("click", printPavs);
    $("#btnPavsPublish").addEventListener("click", () => {
      state.data.pavs_record.registered_date = new Date().toISOString().slice(0, 10);
      savePavs();
      refreshInputs();
    });
    $("#btnPavsCancel").addEventListener("click", () => {
      if (!state.pristine) return;
      state.data = clone(state.pristine);
      syncMirrors(state.data);
      refreshInputs();
      renderAnnexes();
      scheduleRender();
      toast("Modifications annulées.");
    });
    $("#annexInput").addEventListener("change", e => { addAnnexes(Array.from(e.target.files)); e.target.value = ""; });
    $("#annexList").addEventListener("click", e => {
      const b = e.target.closest("[data-annex]");
      if (!b) return;
      state.data.pavs_record.attachments.splice(Number(b.dataset.annex), 1);
      renderAnnexes();
      dataChanged();
    });
    document.addEventListener("click", e => {
      const ask = e.target.closest(".ask[data-fiche]");
      if (!ask) return;
      e.preventDefault();
      openFiche(ask.dataset.fiche);
    });
    $("#ficheClose").addEventListener("click", () => $("#ficheDialog").close());
    $("#ficheDialog").addEventListener("click", e => { if (e.target === e.currentTarget) e.currentTarget.close(); });
    $("#btnPavsExport").addEventListener("click", () => {
      download(`PAVS_${slug(state.data.civil_identity.full_name || state.data.id)}.json`, JSON.stringify(syncMirrors(state.data), null, 2), "application/json");
    });
    $("#pavsImport").addEventListener("change", e => { if (e.target.files[0]) importPavs(e.target.files[0]); e.target.value = ""; });
    $("#portraitInput").addEventListener("change", e => { if (e.target.files[0]) loadPortrait(e.target.files[0]); e.target.value = ""; });
    $("#btnPortraitClear").addEventListener("click", () => {
      state.design.portrait = null;
      state.design.portraitBytes = 0;
      if (state.design.photos) state.design.photos[0] = null;
      renderPhotosPanel();
      $("#portraitInfo").textContent = "Aucun portrait : camée vectoriel.";
      $("#portraitInfo").className = "hint";
      scheduleRender();
      persistToIndexedDb();
    });
    window.addEventListener("afterprint", () => document.body.classList.remove("printing-bat"));

    // Liaison du mode WYSIWYG et des panneaux Carte 2
    bindAtelier();
    bindPanels();
  }

  // ------------------------------------------------------------ utilitaires UI
  function escapeHtml(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, ch => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]));
  }
  function slug(s) {
    return String(s).normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^A-Za-z0-9]+/g, "_").replace(/^_|_$/g, "");
  }
  let toastTimer = 0;
  function toast(msg) {
    const t = $("#toast");
    t.textContent = msg;
    t.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => t.classList.remove("show"), 4200);
  }

  // ------------------------------------------------------------ démarrage
  if (typeof document !== "undefined" && document.addEventListener) {
    document.addEventListener("DOMContentLoaded", () => {
      buildControls();
      renderLegend();
      bindInputs();
      bindUi();
      populateSelect();
      const start = allCases().find(c => c.id === "PAVS_01_CH") || allCases()[0];
      selectCase(start.id);
      setTab("card1");
      scheduleFingerprint();
      // Re-rendu une fois les polices chargées (mesures de texte exactes)
      if (document.fonts && document.fonts.load) {
        const faces = ["600 10px Cinzel", "400 10px 'Cormorant Garamond'", "italic 400 10px 'Cormorant Garamond'", "600 10px 'Cormorant Garamond'",
          "italic 600 10px 'Cormorant Garamond'", "400 10px 'Playfair Display'", "700 10px 'Playfair Display'", "400 10px Inter", "600 10px Inter",
          "400 10px 'Fira Code'", "500 10px 'Fira Code'"];
        Promise.all(faces.map(face => document.fonts.load(face).catch(() => null))).then(scheduleRender);
      }
    });
  }
})();
