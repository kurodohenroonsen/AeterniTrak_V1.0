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

console.log(`PaxStudio Design · règles : ${pass} PASS, ${fail} FAIL`);
process.exit(fail ? 1 : 0);
