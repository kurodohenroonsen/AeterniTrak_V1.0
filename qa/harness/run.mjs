#!/usr/bin/env node
/**
 * AeterniTrak V1.0 — Test Vector Harness (Bushi 16 QA)
 *
 * Conforme aux spécifications de qa/vectors/README.md §5 et Ordre 0005.
 * Exécute et vérifie les suites de vecteurs qa/vectors/**\/*.vectors.json.
 */

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import os from "node:os";
import { execSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, "../..");
const VECTORS_DIR = path.join(PROJECT_ROOT, "qa/vectors");
const SCHEMA_FILE = path.join(VECTORS_DIR, "schema/vector-suite.schema.json");
const REPORTS_DIR = path.join(PROJECT_ROOT, "qa/reports");
const OUT_FILE = path.join(PROJECT_ROOT, "mailbox/state/out.txt");

// Registre des motifs anti-prion et ordre strict des portes (README.md §4.2)
const VALID_REASONS = new Set([
  "DESTINATION_UNSUPPORTED",
  "TARGET_UNSPECIFIED",
  "TAXON_UNKNOWN",
  "TAXON_RANK_ABOVE_SPECIES",
  "HUMAN_REMAINS_ROUTE_PROHIBITED",
  "SUBSTRATE_CATEGORY_VIOLATION",
  "CATEGORY_DESTINATION_PROHIBITED",
  "DEROGATION_REQUIRED",
  "PENTOBARBITAL_POSITIVE",
  "PENTOBARBITAL_NOT_TESTED",
  "FEED_BAN_RUMINANT_SOURCE",
  "FEED_BAN_RUMINANT_TARGET",
  "FEED_BAN_INTRA_SPECIES_VIOLATION",
  "FEED_BAN_INTRA_GROUP_VIOLATION",
  "SOURCE_GROUP_NOT_AUTHORISED",
  "TARGET_GROUP_NOT_AUTHORISED",
  "TREATMENT_NOT_PROVEN"
]);

const GATE_ORDER = {
  DESTINATION_UNSUPPORTED: 0,
  TARGET_UNSPECIFIED: 0,
  TAXON_UNKNOWN: 1,
  TAXON_RANK_ABOVE_SPECIES: 1,
  HUMAN_REMAINS_ROUTE_PROHIBITED: 2,
  SUBSTRATE_CATEGORY_VIOLATION: 3,
  CATEGORY_DESTINATION_PROHIBITED: 3,
  DEROGATION_REQUIRED: 3,
  PENTOBARBITAL_POSITIVE: 4,
  PENTOBARBITAL_NOT_TESTED: 4,
  FEED_BAN_RUMINANT_SOURCE: 5,
  FEED_BAN_RUMINANT_TARGET: 6,
  FEED_BAN_INTRA_SPECIES_VIOLATION: 7,
  FEED_BAN_INTRA_GROUP_VIOLATION: 8,
  SOURCE_GROUP_NOT_AUTHORISED: 8,
  TARGET_GROUP_NOT_AUTHORISED: 8,
  TREATMENT_NOT_PROVEN: 9
};

// ============================================================================
// 1. Décodeur CBOR de contrôle indépendant (Bushi 16, RFC 8949 + AVN §3)
// ============================================================================
function decodeCborControl(buf) {
  let offset = 0;

  function readUint(info) {
    if (info < 24) return info;
    if (info === 24) {
      if (offset + 1 > buf.length) throw new Error("Truncated uint8");
      const v = buf.readUInt8(offset);
      offset += 1;
      return v;
    }
    if (info === 25) {
      if (offset + 2 > buf.length) throw new Error("Truncated uint16");
      const v = buf.readUInt16BE(offset);
      offset += 2;
      return v;
    }
    if (info === 26) {
      if (offset + 4 > buf.length) throw new Error("Truncated uint32");
      const v = buf.readUInt32BE(offset);
      offset += 4;
      return v;
    }
    if (info === 27) {
      if (offset + 8 > buf.length) throw new Error("Truncated uint64");
      const v = buf.readBigUInt64BE(offset);
      offset += 8;
      return v;
    }
    throw new Error(`Invalid CBOR uint additional info: ${info}`);
  }

  function decodeItem() {
    if (offset >= buf.length) throw new Error("Unexpected end of CBOR buffer");
    const initialByte = buf[offset++];
    const major = initialByte >> 5;
    const info = initialByte & 0x1f;

    if (major === 0) {
      const val = readUint(info);
      if (typeof val === "bigint") {
        if (val <= BigInt(Number.MAX_SAFE_INTEGER)) return Number(val);
        return { $int: val.toString() };
      }
      return val;
    }
    if (major === 1) {
      const val = readUint(info);
      if (typeof val === "bigint") {
        const neg = -1n - val;
        if (neg >= BigInt(Number.MIN_SAFE_INTEGER)) return Number(neg);
        return { $int: neg.toString() };
      }
      return -1 - val;
    }
    if (major === 2) {
      const len = Number(readUint(info));
      if (offset + len > buf.length) throw new Error("Truncated byte string");
      const bytes = buf.subarray(offset, offset + len);
      offset += len;
      return { $bytes: bytes.toString("hex") };
    }
    if (major === 3) {
      const len = Number(readUint(info));
      if (offset + len > buf.length) throw new Error("Truncated text string");
      const str = buf.subarray(offset, offset + len).toString("utf8");
      offset += len;
      return str;
    }
    if (major === 4) {
      const len = Number(readUint(info));
      const arr = [];
      for (let i = 0; i < len; i++) {
        arr.push(decodeItem());
      }
      return arr;
    }
    if (major === 5) {
      const len = Number(readUint(info));
      const entries = [];
      let allStringKeys = true;
      for (let i = 0; i < len; i++) {
        const k = decodeItem();
        const v = decodeItem();
        if (typeof k !== "string") allStringKeys = false;
        entries.push([k, v]);
      }
      if (allStringKeys) {
        const obj = {};
        for (const [k, v] of entries) {
          obj[k] = v;
        }
        return obj;
      } else {
        return { $map: entries };
      }
    }
    if (major === 6) {
      const tag = Number(readUint(info));
      const val = decodeItem();
      return { $tag: tag, $value: val };
    }
    if (major === 7) {
      if (info === 20) return false;
      if (info === 21) return true;
      if (info === 22) return null;
      throw new Error(`Unsupported simple value info: ${info}`);
    }
    throw new Error(`Unknown CBOR major type: ${major}`);
  }

  const result = decodeItem();
  if (offset !== buf.length) {
    throw new Error(`Trailing bytes in CBOR buffer (${buf.length - offset} extra bytes)`);
  }
  return result;
}

// ============================================================================
// 2. Égalité sémantique AVN (AeterniTrak Vector Notation)
// ============================================================================
function avnEqual(a, b) {
  if (a === b) return true;
  if (a === null || b === null || typeof a !== "object" || typeof b !== "object") return false;

  // Comparaison $map (ordre des paires arbitraire)
  if (a.$map && b.$map) {
    if (a.$map.length !== b.$map.length) return false;
    const matched = new Set();
    for (const [k1, v1] of a.$map) {
      let found = false;
      for (let i = 0; i < b.$map.length; i++) {
        if (!matched.has(i)) {
          const [k2, v2] = b.$map[i];
          if (avnEqual(k1, k2) && avnEqual(v1, v2)) {
            matched.add(i);
            found = true;
            break;
          }
        }
      }
      if (!found) return false;
    }
    return true;
  }

  // Comparaison tableaux
  if (Array.isArray(a) && Array.isArray(b)) {
    if (a.length !== b.length) return false;
    return a.every((item, i) => avnEqual(item, b[i]));
  }
  if (Array.isArray(a) !== Array.isArray(b)) return false;

  // Comparaison objets ordinaires (y compris $tag, $int, $bytes)
  const aKeys = Object.keys(a).sort();
  const bKeys = Object.keys(b).sort();
  if (aKeys.length !== bKeys.length) return false;
  if (!aKeys.every((k, i) => k === bKeys[i])) return false;
  return aKeys.every((k) => avnEqual(a[k], b[k]));
}

// ============================================================================
// 3. Canoniseur JCS de contrôle indépendant (Bushi 16, RFC 8785)
// ============================================================================
function canonicalizeJcsControl(val) {
  if (val === null || typeof val !== "object") {
    if (typeof val === "number" && Object.is(val, -0)) return "0";
    return JSON.stringify(val);
  }
  if (Array.isArray(val)) {
    return "[" + val.map(canonicalizeJcsControl).join(",") + "]";
  }
  const keys = Object.keys(val).sort();
  return "{" + keys.map((k) => JSON.stringify(k) + ":" + canonicalizeJcsControl(val[k])).join(",") + "}";
}

// ============================================================================
// 4. Validateur de Schéma JSON (Ajv draft 2020-12 avec repli structurel)
// ============================================================================
let ajvValidateFn = null;
try {
  const { default: Ajv2020 } = await import("ajv/dist/2020.js");
  if (fs.existsSync(SCHEMA_FILE)) {
    const schemaContent = JSON.parse(fs.readFileSync(SCHEMA_FILE, "utf8"));
    const ajv = new Ajv2020({ allErrors: true });
    ajvValidateFn = ajv.compile(schemaContent);
  }
} catch {
  ajvValidateFn = null;
}

function validateSuiteSchema(suiteData) {
  if (ajvValidateFn) {
    const valid = ajvValidateFn(suiteData);
    if (!valid) {
      return ajvValidateFn.errors.map((e) => `${e.instancePath || "/"} ${e.message}`).join("; ");
    }
    return null;
  }

  // Repli de validation structurelle pure si ajv non chargé
  const requiredFields = ["suite", "version", "issued_by", "issued_at", "status", "spec", "adapter", "description", "cases"];
  for (const f of requiredFields) {
    if (!(f in suiteData)) return `Champ obligatoire manquant: ${f}`;
  }
  if (!/^[a-z0-9]+(\.[a-z0-9-]+)+$/.test(suiteData.suite)) return `Format suite invalide: ${suiteData.suite}`;
  if (!/^[0-9]+\.[0-9]+\.[0-9]+$/.test(suiteData.version)) return `Format version invalide: ${suiteData.version}`;
  if (!["claude", "bushi-16"].includes(suiteData.issued_by)) return `issued_by invalide: ${suiteData.issued_by}`;
  if (!/^[0-9]{4}-[0-9]{2}-[0-9]{2}$/.test(suiteData.issued_at)) return `issued_at invalide: ${suiteData.issued_at}`;
  if (!["draft", "approved"].includes(suiteData.status)) return `status invalide: ${suiteData.status}`;
  if (!Array.isArray(suiteData.spec) || suiteData.spec.length === 0) return "spec doit être un tableau non vide";
  if (!/^[a-z0-9]+(\.[a-z0-9-]+)*$/.test(suiteData.adapter)) return `Format adapter invalide: ${suiteData.adapter}`;
  if (typeof suiteData.description !== "string") return "description doit être une chaîne";
  if (!Array.isArray(suiteData.cases) || suiteData.cases.length === 0) return "cases doit être un tableau non vide";

  for (const c of suiteData.cases) {
    if (!c.id || !/^[A-Z]{2,8}-[A-Z0-9]{2,12}-[0-9]{3}$/.test(c.id)) return `ID cas invalide: ${c.id}`;
    if (!c.title || typeof c.title !== "string" || c.title.length < 3) return `Titre cas invalide: ${c.id}`;
    if (!c.op || !/^[a-z]+(-[a-z]+)*$/.test(c.op)) return `Op cas invalide: ${c.id}`;
    if (c.input === undefined) return `Input manquant: ${c.id}`;
    if (!c.expect || typeof c.expect !== "object" || Object.keys(c.expect).length === 0) return `Expect invalide: ${c.id}`;
    if (!c.rule || typeof c.rule !== "string") return `Rule manquante: ${c.id}`;
  }
  return null;
}

// ============================================================================
// 5. Vérification d'auto-cohérence et contrôle croisé d'un cas
// ============================================================================
function verifyCaseExpectation(caseObj) {
  const exp = caseObj.expect;

  // Auto-cohérence binaire
  if (exp.hex !== undefined) {
    if (typeof exp.hex !== "string" || !/^[0-9a-fA-F]*$/.test(exp.hex)) {
      return { valid: false, reason: "hex n'est pas une chaîne hexadécimale valide" };
    }
    if (typeof exp.len === "number") {
      if (exp.hex.length / 2 !== exp.len) {
        return { valid: false, reason: `len mismatch: len(hex)/2 = ${exp.hex.length / 2} !== len (${exp.len})` };
      }
    }
    if (typeof exp.sha256 === "string") {
      const digest = crypto.createHash("sha256").update(Buffer.from(exp.hex, "hex")).digest("hex");
      if (digest !== exp.sha256.toLowerCase()) {
        return { valid: false, reason: `sha256 mismatch: sha256(hex) = ${digest} !== expect (${exp.sha256})` };
      }
    }
    if (typeof exp.utf8 === "string") {
      const hexUtf8 = Buffer.from(exp.utf8, "utf8").toString("hex");
      if (hexUtf8 !== exp.hex.toLowerCase()) {
        return { valid: false, reason: "utf8 mismatch: utf8 encodé en hex ne correspond pas à expect.hex" };
      }
    }
  }

  // Auto-cohérence antiprion
  if (exp.reasons !== undefined) {
    if (!Array.isArray(exp.reasons)) {
      return { valid: false, reason: "reasons doit être un tableau" };
    }
    for (const r of exp.reasons) {
      if (!VALID_REASONS.has(r)) {
        return { valid: false, reason: `Motif non répertorié dans le registre: "${r}"` };
      }
    }
    for (let i = 1; i < exp.reasons.length; i++) {
      if (GATE_ORDER[exp.reasons[i]] < GATE_ORDER[exp.reasons[i - 1]]) {
        return { valid: false, reason: `Ordre des portes non respecté: ${exp.reasons[i - 1]} -> ${exp.reasons[i]}` };
      }
    }
    if (exp.reasons.length === 0) {
      if (exp.verdict !== "AUTHORISED" || exp.signature_permitted !== true) {
        return { valid: false, reason: "Incohérence reasons vide avec verdict/signature_permitted" };
      }
    } else {
      if (exp.verdict !== "BLOCKED" || exp.signature_permitted !== false) {
        return { valid: false, reason: "Incohérence reasons non vide avec verdict/signature_permitted" };
      }
    }
  }

  // Contrôle croisé : décodeur CBOR de contrôle sur encode
  if (caseObj.op === "encode") {
    try {
      const decoded = decodeCborControl(Buffer.from(exp.hex, "hex"));
      if (!avnEqual(decoded, caseObj.input)) {
        return {
          valid: false,
          reason: `Contrôle croisé CBOR en échec: le décodeur de contrôle n'a pas retrouvé l'entrée AVN (décodé: ${JSON.stringify(decoded)}, entrée: ${JSON.stringify(caseObj.input)})`
        };
      }
    } catch (err) {
      return { valid: false, reason: `Contrôle croisé CBOR en erreur de décodage: ${err.message}` };
    }
  }

  // Contrôle croisé : canoniseur JCS de contrôle sur canonicalize
  if (caseObj.op === "canonicalize") {
    try {
      const canon = canonicalizeJcsControl(caseObj.input);
      if (canon !== exp.utf8) {
        return {
          valid: false,
          reason: `Contrôle croisé JCS en échec: attendu "${exp.utf8}", canonisé "${canon}"`
        };
      }
    } catch (err) {
      return { valid: false, reason: `Contrôle croisé JCS en erreur: ${err.message}` };
    }
  }

  return { valid: true };
}

// ============================================================================
// 6. Moteur d'exécution des suites
// ============================================================================
async function executeSuite(suitePath, options = {}) {
  const content = fs.readFileSync(suitePath, "utf8");
  const suite = JSON.parse(content);

  const schemaErr = validateSuiteSchema(suite);
  if (schemaErr) {
    return {
      suite: suite.suite || path.basename(suitePath),
      path: path.relative(PROJECT_ROOT, suitePath),
      adapter: suite.adapter,
      adapter_present: false,
      schema_error: schemaErr,
      cases: [],
      summary: { pass: 0, fail: 0, red: 0, invalid: 1, total: 1 }
    };
  }

  // Vérification de présence de l'adaptateur
  const adapterRelPath = `qa/harness/adapters/${suite.adapter}.mjs`;
  const adapterFullPath = path.join(PROJECT_ROOT, adapterRelPath);
  let adapterModule = null;
  const adapterPresent = fs.existsSync(adapterFullPath);

  if (adapterPresent) {
    try {
      adapterModule = await import(adapterFullPath);
    } catch (err) {
      return {
        suite: suite.suite,
        path: path.relative(PROJECT_ROOT, suitePath),
        adapter: suite.adapter,
        adapter_present: true,
        adapter_load_error: err.message,
        cases: [],
        summary: { pass: 0, fail: 1, red: 0, invalid: 0, total: 1 }
      };
    }
  }

  const results = [];
  const summary = { pass: 0, fail: 0, red: 0, invalid: 0, total: suite.cases.length };

  for (const c of suite.cases) {
    // 1. Contrôle croisé et cohérence
    const check = verifyCaseExpectation(c);
    if (!check.valid) {
      summary.invalid++;
      results.push({
        id: c.id,
        title: c.title,
        op: c.op,
        status: "INVALID",
        error: check.reason
      });
      continue;
    }

    // 2. Si adaptateur absent => RED
    if (!adapterPresent) {
      summary.red++;
      results.push({
        id: c.id,
        title: c.title,
        op: c.op,
        status: "RED",
        error: null
      });
      continue;
    }

    // 3. Exécution adaptateur
    try {
      let actual;
      try {
        actual = await adapterModule.run(c.op, c.input);
      } catch (err) {
        if (c.op.startsWith("reject-")) {
          actual = { error: err.code || err.message };
        } else {
          throw err;
        }
      }

      if (avnEqual(actual, c.expect)) {
        summary.pass++;
        results.push({ id: c.id, title: c.title, op: c.op, status: "PASS", error: null });
      } else {
        summary.fail++;
        results.push({
          id: c.id,
          title: c.title,
          op: c.op,
          status: "FAIL",
          error: `Attendu: ${JSON.stringify(c.expect)}, Obtenu: ${JSON.stringify(actual)}`
        });
      }
    } catch (err) {
      summary.fail++;
      results.push({
        id: c.id,
        title: c.title,
        op: c.op,
        status: "FAIL",
        error: `Exception adaptateur: ${err.message}`
      });
    }
  }

  return {
    suite: suite.suite,
    path: path.relative(PROJECT_ROOT, suitePath),
    adapter: suite.adapter,
    adapter_present: adapterPresent,
    cases: results,
    summary
  };
}

// ============================================================================
// 7. Auto-test (--selftest)
// ============================================================================
async function runSelfTest(outputLog) {
  outputLog(">>> Démarrage de l'auto-test (--selftest) : simulation de 3 corruptions dans un environnement temporaire...");
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "aeternitrak-selftest-"));

  try {
    const cborOrig = path.join(VECTORS_DIR, "core/cbor-deterministic.vectors.json");
    const jcsOrig = path.join(VECTORS_DIR, "core/jcs-rfc8785.vectors.json");
    const prionOrig = path.join(VECTORS_DIR, "antiprion/feedban-matrix.vectors.json");

    const tmpCoreDir = path.join(tmpDir, "core");
    const tmpPrionDir = path.join(tmpDir, "antiprion");
    fs.mkdirSync(tmpCoreDir, { recursive: true });
    fs.mkdirSync(tmpPrionDir, { recursive: true });

    const cborData = JSON.parse(fs.readFileSync(cborOrig, "utf8"));
    const jcsData = JSON.parse(fs.readFileSync(jcsOrig, "utf8"));
    const prionData = JSON.parse(fs.readFileSync(prionOrig, "utf8"));

    // Mutation 1: corruption d'un octet de hex (CBOR-ENC-001)
    const case1 = cborData.cases.find((c) => c.id === "CBOR-ENC-001");
    case1.expect.hex = "01"; // au lieu de "00"

    // Mutation 2: corruption d'un sha256 (CBOR-ENC-002)
    const case2 = cborData.cases.find((c) => c.id === "CBOR-ENC-002");
    case2.expect.sha256 = "00000000344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459a";

    // Mutation 3: corruption d'une liste reasons (PRION-BLOCK-001)
    const case3 = prionData.cases.find((c) => c.id === "PRION-BLOCK-001");
    case3.expect.reasons = ["FEED_BAN_INTRA_SPECIES_VIOLATION", "MUTATED_INVALID_REASON"];

    const tmpCborPath = path.join(tmpCoreDir, "cbor-deterministic.vectors.json");
    const tmpJcsPath = path.join(tmpCoreDir, "jcs-rfc8785.vectors.json");
    const tmpPrionPath = path.join(tmpPrionDir, "feedban-matrix.vectors.json");

    fs.writeFileSync(tmpCborPath, JSON.stringify(cborData, null, 2));
    fs.writeFileSync(tmpJcsPath, JSON.stringify(jcsData, null, 2));
    fs.writeFileSync(tmpPrionPath, JSON.stringify(prionData, null, 2));

    const suitePaths = [tmpCborPath, tmpJcsPath, tmpPrionPath];
    const suiteReports = [];
    const totalSummary = { pass: 0, fail: 0, red: 0, invalid: 0, total: 0 };

    for (const sp of suitePaths) {
      const rep = await executeSuite(sp);
      suiteReports.push(rep);
      totalSummary.pass += rep.summary.pass;
      totalSummary.fail += rep.summary.fail;
      totalSummary.red += rep.summary.red;
      totalSummary.invalid += rep.summary.invalid;
      totalSummary.total += rep.summary.total;

      for (const c of rep.cases) {
        outputLog(`${c.status} ${c.id} ${c.title}`);
        if (c.error) {
          outputLog(`  -> ${c.error}`);
        }
      }
    }

    outputLog("\n============================================================");
    outputLog(`RÉSULTAT SELFTEST : ${totalSummary.pass} PASS, ${totalSummary.fail} FAIL, ${totalSummary.red} RED, ${totalSummary.invalid} INVALID (${totalSummary.total} total)`);
    outputLog("============================================================");

    if (totalSummary.invalid === 3) {
      outputLog("[SELFTEST OK] Détection exacte des 3 corruptions simulées (hex, sha256, reasons).");
    } else {
      outputLog(`[SELFTEST ANOMALIE] Attendu 3 INVALID, obtenu ${totalSummary.invalid} INVALID.`);
    }

    return { totalSummary, suiteReports, exitCode: 2 };
  } finally {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  }
}

// ============================================================================
// 8. Point d'entrée principal
// ============================================================================
async function main() {
  const rawArgs = process.argv.slice(2);
  const args = rawArgs.filter((a) => a !== "test");
  const isSelftest = args.includes("--selftest");
  const filter = args.find((a) => !a.startsWith("--"));

  const logBuffer = [];
  function outputLog(line = "") {
    process.stdout.write(line + "\n");
    logBuffer.push(line);
  }

  // Résolution du SHA et de la date
  const dateStr = new Date().toISOString().slice(0, 10);
  let shortSha = "unknown";
  let branchName = "unknown";
  try {
    shortSha = execSync("git rev-parse --short HEAD", { cwd: PROJECT_ROOT, encoding: "utf8" }).trim();
    branchName = execSync("git rev-parse --abbrev-ref HEAD", { cwd: PROJECT_ROOT, encoding: "utf8" }).trim();
  } catch {}

  let totalSummary = { pass: 0, fail: 0, red: 0, invalid: 0, total: 0 };
  let suiteReports = [];
  let exitCode = 0;

  if (isSelftest) {
    const res = await runSelfTest(outputLog);
    totalSummary = res.totalSummary;
    suiteReports = res.suiteReports;
    exitCode = res.exitCode;
  } else {
    // Découverte des suites
    const candidateFiles = [
      path.join(VECTORS_DIR, "core/cbor-deterministic.vectors.json"),
      path.join(VECTORS_DIR, "core/jcs-rfc8785.vectors.json"),
      path.join(VECTORS_DIR, "antiprion/feedban-matrix.vectors.json")
    ];

    const activeSuites = candidateFiles.filter((f) => {
      if (!fs.existsSync(f)) return false;
      if (!filter) return true;
      const rel = path.relative(PROJECT_ROOT, f);
      return rel.includes(filter) || path.basename(f).includes(filter);
    });

    if (activeSuites.length === 0) {
      outputLog(`Aucune suite trouvée pour le filtre "${filter}".`);
      process.exit(0);
    }

    for (const sp of activeSuites) {
      const rep = await executeSuite(sp);
      suiteReports.push(rep);
      totalSummary.pass += rep.summary.pass;
      totalSummary.fail += rep.summary.fail;
      totalSummary.red += rep.summary.red;
      totalSummary.invalid += rep.summary.invalid;
      totalSummary.total += rep.summary.total;

      for (const c of rep.cases) {
        outputLog(`${c.status} ${c.id} ${c.title}`);
        if (c.error) {
          outputLog(`  -> ${c.error}`);
        }
      }
    }

    outputLog("\n============================================================");
    for (const rep of suiteReports) {
      const adapterStatus = rep.adapter_present ? `présent (${rep.adapter})` : `ABSENT (${rep.adapter}) -> RED`;
      outputLog(`Suite : ${rep.suite} [Adaptateur : ${adapterStatus}]`);
      outputLog(`  ${rep.summary.pass} PASS, ${rep.summary.fail} FAIL, ${rep.summary.red} RED, ${rep.summary.invalid} INVALID (${rep.summary.total} total)`);
    }
    outputLog("------------------------------------------------------------");
    outputLog(`TOTAL : ${totalSummary.pass} PASS, ${totalSummary.fail} FAIL, ${totalSummary.red} RED, ${totalSummary.invalid} INVALID (${totalSummary.total} total)`);
    outputLog("============================================================");

    if (totalSummary.invalid > 0) {
      exitCode = 2;
    } else if (totalSummary.fail > 0) {
      exitCode = 1;
    } else {
      exitCode = 0;
    }
  }

  // Écriture du rapport JSON
  try {
    fs.mkdirSync(REPORTS_DIR, { recursive: true });
    const reportPath = path.join(REPORTS_DIR, `${dateStr}-${shortSha}.json`);
    const reportData = {
      date: dateStr,
      commit: shortSha,
      branch: branchName,
      filter: filter || null,
      selftest: isSelftest,
      summary: totalSummary,
      suites: suiteReports
    };
    fs.writeFileSync(reportPath, JSON.stringify(reportData, null, 2) + "\n");
    outputLog(`Rapport généré : ${path.relative(PROJECT_ROOT, reportPath)}`);
  } catch (err) {
    outputLog(`Avertissement : impossible d'écrire le rapport JSON : ${err.message}`);
  }

  // Copie intégrale dans mailbox/state/out.txt
  try {
    fs.mkdirSync(path.dirname(OUT_FILE), { recursive: true });
    fs.appendFileSync(OUT_FILE, logBuffer.join("\n") + "\n");
  } catch (err) {
    process.stderr.write(`Erreur écriture out.txt: ${err.message}\n`);
  }

  process.exit(exitCode);
}

main().catch((err) => {
  process.stderr.write(`Fatal harness error: ${err.stack || err.message}\n`);
  process.exit(2);
});
