#!/usr/bin/env node
/**
 * PaxStudio Design — Tests du moteur de règles sur les 44 cas PAVS de référence.
 * Usage : node apps/paxstudio-design/tests/rules.test.mjs
 */
import fs from "node:fs";
import vm from "node:vm";
import path from "node:path";
import { fileURLToPath } from "node:url";

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const ctx = { window: {}, self: {} };
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(APP, "js/rules.js"), "utf8"), ctx);
vm.runInContext(fs.readFileSync(path.join(APP, "data/paxfunebre_44_test_cases.js"), "utf8"), ctx);
vm.runInContext(fs.readFileSync(path.join(APP, "js/ornaments.js"), "utf8"), ctx);
vm.runInContext(fs.readFileSync(path.join(APP, "js/cards.js"), "utf8"), ctx);
const Cards = ctx.self.PaxCards;
const R = ctx.self.PaxRules;
const CASES = ctx.window.PAX_TEST_CASES;

let pass = 0;
let fail = 0;
function check(name, cond, info = "") {
  if (cond) pass++;
  else { fail++; console.error(`✗ ${name} ${info}`); }
}

check("44 cas chargés", CASES.length === 44, `(${CASES.length})`);
check("14 modes de sépulture", R.BURIAL_MODES.length === 14);
for (let m = 1; m <= 14; m++) check(`mode ${m} thermique`, R.isThermal(m) === (m >= 3 && m <= 12));
for (let m = 8; m <= 12; m++) check(`mode ${m} sarcomusation`, R.isSarco(m));

for (const c of CASES) {
  const ci = c.civil_identity;
  const n = R.validateNiss(ci.national_id_niss, ci.birth_date, ci.gender);
  check(`${c.id} NISS modulo 97`, n.valid, n.reason);
  check(`${c.id} NISS parité sexe`, n.sexOk === true);
  const bat = R.batStatus(c);
  check(`${c.id} statut B.A.T.`, bat.carte_1_status === c.bat_status.carte_1_status, `${bat.carte_1_status} ≠ ${c.bat_status.carte_1_status}`);
  check(`${c.id} prêt à imprimer`, bat.ready_to_print === c.bat_status.ready_to_print);
  check(`${c.id} aucune date de décès du vivant`, !ci.death_date);
}

// Verrou pyrotechnique : matrice explicite
const base = R.blankCase("T");
const withPm = (mode, exeresis) => ({
  ...base,
  funeral_wills: { ...base.funeral_wills, burial_mode: mode },
  medical_record: { ...base.medical_record, has_pacemaker: true,
    pacemaker_exeresis: exeresis ? { certified_removed: true, surgeon_name: "Dr X", surgeon_inami: "1-00000-00-000" } : null }
});
for (let m = 1; m <= 14; m++) {
  const expected = m >= 3 && m <= 12 ? "BLOCK" : "INHUMATION_OK";
  check(`pacemaker non extrait mode ${m}`, R.pyroStatus(withPm(m, false)).code === expected);
  check(`pacemaker extrait mode ${m}`, R.pyroStatus(withPm(m, true)).code === "EXERESE_OK");
}

// NISS : cas limites
check("NISS post-2000 (constante 2 000 000 000)", R.validateNiss("04.03.15-142.27", "2004-03-15", "F").valid);
check("NISS post-2000 refusé avec formule pré-2000", !R.validateNiss("04.03.15-142.27", "1904-03-15", "F").valid);
check("NISS date incohérente refusé", !R.validateNiss("79.04.04-381.22", "1979-04-05").valid);
check("NISS longueur invalide", !R.validateNiss("79.04.04-381", "1979-04-04").valid);
check("Chiffres de contrôle calculés", R.nissCheckDigits("790404381", 1979) === "22");
check("Prion × humusation bloqué", R.batStatus({ ...base, funeral_wills: { ...base.funeral_wills, burial_mode: 13 },
  medical_record: { ...base.medical_record, biological_hazard_level: 3 } }).carte_1_status === "ALERTE_PRION_HUMUSATION");

check("PAVS vierge non imprimable (identité incomplète)", R.batStatus(base).carte_1_status === "INCOMPLET_IDENTITE");

// Migration vers le formulaire officiel (Réseau Santé Wallon)
const byId = id => JSON.parse(JSON.stringify(CASES.find(c => c.id === id)));
for (const c0 of CASES) {
  const c = R.syncOfficial(R.normalizePavs(JSON.parse(JSON.stringify(c0))));
  const again = R.syncOfficial(R.normalizePavs(JSON.parse(JSON.stringify(c))));
  check(`${c0.id} migration idempotente`, JSON.stringify(c) === JSON.stringify(again));
  check(`${c0.id} B.A.T. inchangé après migration`, R.batStatus(c).carte_1_status === c0.bat_status.carte_1_status);
  const care = c.pavs_record.care;
  check(`${c0.id} refus = identifiants officiels`, care.refusals.every(id => R.PAVS.REFUSALS.some(r => r.id === id)));
  check(`${c0.id} accompagnement = choix officiels`, c.pavs_record.desired_support.choices.every(id => R.PAVS.SUPPORT.some(r => r.id === id)));
}
const m = id => R.normalizePavs(byId(id)).pavs_record;
check("PAVS_03 : refus ventilation → VNI + intubation seulement", JSON.stringify(m("PAVS_03_REFUS_RESP_SEULE").care.refusals) === JSON.stringify(["VNI", "INTUBATION"]));
check("PAVS_02 : refus alimentation → 3 techniques", m("PAVS_02_REFUS_ALIM_SEULE").care.refusals.length === 3);
check("PAVS_05 : soins maximums avec réanimation", m("PAVS_05_SOINS_CURATIFS_PLEINS").care.intensity === "max" && m("PAVS_05_SOINS_CURATIFS_PLEINS").care.reanimation === "avec");
check("PAVS_07 : lieu de soins = institution", m("PAVS_07_MAISON_REPOS_INSTITUTION").care.settings[0] === "INSTITUTION");
check("PAVS_38 : culte musulman → Religieux", m("PAVS_38_RITE_MUSULMAN").desired_support.choices.includes("RELIGIEUX"));
check("PAVS_40 : bouddhiste → Spirituel", m("PAVS_40_RITE_BOUDDHISTE_MEDITATIF").desired_support.choices.includes("SPIRITUEL"));
check("PAVS_28 : don du corps = Oui", R.normalizePavs(byId("PAVS_28_DON_SCIENCE_48H")).pavs_record.post_mortem_wills.body_donation === "Oui");
check("PAVS_18 : inhumé(e)", R.normalizePavs(byId("PAVS_18_INHUMATION_TERRE")).pavs_record.post_mortem_wills.body_disposition === "inhume");
const maxRefus = R.normalizePavs(byId("PAVS_05_SOINS_CURATIFS_PLEINS"));
maxRefus.pavs_record.care.refusals = ["DIALYSE"];
check("Avertissement : soins maximums + refus", R.pavsWarnings(maxRefus).some(w => /maximums/.test(w.text)));

// Carte 1 : densité intégrale (mesure estimée hors navigateur)
const design = { material: "ivoire", fontTitle: "cinzel", fontBody: "cormorant", fontData: "inter", fontScale: 1 };
for (const c0 of CASES) {
  const c = R.syncOfficial(R.normalizePavs(JSON.parse(JSON.stringify(c0))));
  const rep = Cards.card1Report(c, design);
  check(`${c0.id} Carte 1 : toutes les données affichées`, rep.overflow.length === 0, rep.overflow.join(", "));
  const svg = Cards.render(1, "recto", c, design, {}) + Cards.render(1, "verso", c, design, {});
  check(`${c0.id} Carte 1 : aucune date de décès`, !/décès le|décédé/i.test(svg));
}
const full = R.normalizePavs(byId("PAVS_34_MANDATAIRE_EXTRAJUDICIAIRE"));
const long = "Je souhaite être accompagné avec douceur, entouré de mes proches, dans le calme, avec de la musique douce et la lumière du jardin, sans acharnement.";
Object.assign(full.pavs_record, { comments: long, other_wishes: long, essential_priority: long });
full.pavs_record.desired_support.special_wishes = long;
Object.assign(full.pavs_record.post_mortem_wills, { rites: long, other_wishes: long });
full.funeral_wills.chosen_funeral_home = long;
full.pavs_record.care.refusals = R.PAVS.REFUSALS.map(r => r.id);
for (const k of ["institution", "contact_person", "extrajudicial_proxy", "property_administrator"]) full.pavs_record[k] = { name: "Résidence Les Tilleuls de Gembloux", phone: "+32 81 00 00 00" };
const fullRep = Cards.card1Report(R.syncOfficial(full), design);
check("PAVS saturé : tout tient sur la Carte 1", fullRep.overflow.length === 0, fullRep.overflow.join(", "));
check("PAVS saturé : corps ≥ 0,8 mm", fullRep.size >= 0.8);

console.log(`PaxStudio Design · règles : ${pass} PASS, ${fail} FAIL`);
process.exit(fail ? 1 : 0);
