#!/usr/bin/env node
/**
 * AeterniTrak V1.0 — Test Vector Harness (Bushi 16 QA)
 *
 * Conforme aux spécifications de qa/vectors/README.md §5, Ordre 0005 et Redirect 0011.
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
// 1. Découverte dynamique récursive des suites (H1)
// ============================================================================
const EXCLUSION_PATTERNS = [
  /\/schema\//i,
  /snapshot.*\.json$/i,
  /\.schema\.json$/i
];

function discoverSuites(baseDir) {
  const suites = [];

  function walk(currentDir) {
    if (!fs.existsSync(currentDir)) return;
    const entries = fs.readdirSync(currentDir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);
      if (entry.isDirectory()) {
        walk(fullPath);
      } else if (entry.isFile()) {
        const normalized = fullPath.replace(/\\/g, "/");
        if (entry.name.endsWith(".vectors.json")) {
          const isExcluded = EXCLUSION_PATTERNS.some((pat) => pat.test(normalized));
          if (!isExcluded) {
            suites.push(fullPath);
          }
        }
      }
    }
  }

  walk(baseDir);

  // Tri par chemin relatif alphabétique
  suites.sort((a, b) => {
    const relA = path.relative(baseDir, a);
    const relB = path.relative(baseDir, b);
    return relA.localeCompare(relB);
  });

  return suites;
}

// ============================================================================
// 2. Décodeur CBOR de contrôle strict indépendant (H2, RFC 8949 §4.2.1 + AVN)
// ============================================================================
function decodeCborStrict(buf) {
  if (!Buffer.isBuffer(buf)) {
    buf = Buffer.from(buf);
  }
  if (buf.length === 0) {
    throw new Error("ERR_CBOR_TRUNCATED: Empty buffer");
  }

  let offset = 0;
  const textDecoder = new TextDecoder("utf-8", { fatal: true });

  function readUint(info, major) {
    if (info < 24) return info;
    if (info === 24) {
      if (offset + 1 > buf.length) throw new Error("ERR_CBOR_TRUNCATED: Truncated uint8");
      const v = buf.readUInt8(offset);
      offset += 1;
      if (v < 24) throw new Error(`ERR_CBOR_NOT_SHORTEST: Integer ${v} encoded in 1 byte (info 24)`);
      return v;
    }
    if (info === 25) {
      if (offset + 2 > buf.length) throw new Error("ERR_CBOR_TRUNCATED: Truncated uint16");
      const v = buf.readUInt16BE(offset);
      offset += 2;
      if (v < 256) throw new Error(`ERR_CBOR_NOT_SHORTEST: Integer ${v} encoded in 2 bytes (info 25)`);
      return v;
    }
    if (info === 26) {
      if (offset + 4 > buf.length) throw new Error("ERR_CBOR_TRUNCATED: Truncated uint32");
      const v = buf.readUInt32BE(offset);
      offset += 4;
      if (v < 65536) throw new Error(`ERR_CBOR_NOT_SHORTEST: Integer ${v} encoded in 4 bytes (info 26)`);
      return v;
    }
    if (info === 27) {
      if (offset + 8 > buf.length) throw new Error("ERR_CBOR_TRUNCATED: Truncated uint64");
      const v = buf.readBigUInt64BE(offset);
      offset += 8;
      if (v < 4294967296n) throw new Error(`ERR_CBOR_NOT_SHORTEST: Integer ${v} encoded in 8 bytes (info 27)`);
      return v;
    }
    if (info === 31) {
      throw new Error("ERR_CBOR_INDEFINITE_LENGTH: Indefinite length is forbidden by profile");
    }
    throw new Error(`ERR_CBOR_MALFORMED: Reserved additional info ${info}`);
  }

  function decodeItem() {
    if (offset >= buf.length) throw new Error("ERR_CBOR_TRUNCATED: Unexpected end of CBOR buffer");
    const initialByte = buf[offset++];
    const major = initialByte >> 5;
    const info = initialByte & 0x1f;

    if (major === 0) {
      const val = readUint(info, 0);
      if (typeof val === "bigint") {
        if (val <= BigInt(Number.MAX_SAFE_INTEGER)) return Number(val);
        return { $int: val.toString() };
      }
      return val;
    }
    if (major === 1) {
      const val = readUint(info, 1);
      if (typeof val === "bigint") {
        const neg = -1n - val;
        if (neg >= BigInt(Number.MIN_SAFE_INTEGER)) return Number(neg);
        return { $int: neg.toString() };
      }
      return -1 - val;
    }
    if (major === 2) {
      const len = Number(readUint(info, 2));
      if (offset + len > buf.length) throw new Error("ERR_CBOR_TRUNCATED: Truncated byte string");
      const bytes = buf.subarray(offset, offset + len);
      offset += len;
      return { $bytes: bytes.toString("hex") };
    }
    if (major === 3) {
      const len = Number(readUint(info, 3));
      if (offset + len > buf.length) throw new Error("ERR_CBOR_TRUNCATED: Truncated text string");
      const rawBytes = buf.subarray(offset, offset + len);
      offset += len;
      let str;
      try {
        str = textDecoder.decode(rawBytes);
      } catch (e) {
        throw new Error("ERR_CBOR_INVALID_UTF8: " + e.message);
      }
      if (str.normalize("NFC") !== str) {
        throw new Error("ERR_CBOR_TEXT_NOT_NFC: Text string is not normalized to NFC");
      }
      return str;
    }
    if (major === 4) {
      const len = Number(readUint(info, 4));
      const arr = [];
      for (let i = 0; i < len; i++) {
        arr.push(decodeItem());
      }
      return arr;
    }
    if (major === 5) {
      const len = Number(readUint(info, 5));
      const entries = [];
      let allStringKeys = true;
      let prevKeyBytes = null;
      const seenKeys = new Set();

      for (let i = 0; i < len; i++) {
        const keyStart = offset;
        const k = decodeItem();
        const keyEnd = offset;
        const keyBytes = buf.subarray(keyStart, keyEnd);

        if (prevKeyBytes !== null) {
          const cmp = Buffer.compare(prevKeyBytes, keyBytes);
          if (cmp === 0) {
            throw new Error("ERR_CBOR_DUPLICATE_KEY: Duplicate map key detected");
          }
          if (cmp > 0) {
            throw new Error("ERR_CBOR_MAP_UNSORTED: Map keys must be sorted in bytewise lexicographic order");
          }
        }
        const keyHex = keyBytes.toString("hex");
        if (seenKeys.has(keyHex)) {
          throw new Error("ERR_CBOR_DUPLICATE_KEY: Duplicate map key detected");
        }
        seenKeys.add(keyHex);
        prevKeyBytes = keyBytes;

        const v = decodeItem();
        if (typeof k !== "string") allStringKeys = false;
        entries.push([k, v]);
      }

      if (allStringKeys) {
        const hasDollarKey = entries.some(([k]) => typeof k === "string" && k.startsWith("$"));
        if (!hasDollarKey) {
          const obj = {};
          for (const [k, v] of entries) {
            obj[k] = v;
          }
          return obj;
        } else {
          return { $map: entries };
        }
      } else {
        return { $map: entries };
      }
    }
    if (major === 6) {
      const tag = Number(readUint(info, 6));
      if (tag !== 1 && tag !== 100) {
        throw new Error(`ERR_CBOR_UNSUPPORTED_TAG: Tag ${tag} is not supported by profile`);
      }
      const val = decodeItem();
      if (tag === 100) {
        const isInt = typeof val === "number" || typeof val === "bigint" || (val && typeof val === "object" && typeof val.$int === "string");
        if (!isInt) {
          throw new Error("ERR_CBOR_TAG_CONTENT: Tag 100 content must be an integer");
        }
      }
      if (tag === 1) {
        const isInt = typeof val === "number" || typeof val === "bigint" || (val && typeof val === "object" && typeof val.$int === "string");
        if (!isInt) {
          throw new Error("ERR_CBOR_TAG_CONTENT: Tag 1 content must be an integer");
        }
        if ((typeof val === "number" && val < 0) || (typeof val === "bigint" && val < 0n) || (val && typeof val === "object" && typeof val.$int === "string" && val.$int.startsWith("-"))) {
          throw new Error("ERR_CBOR_TAG_CONTENT: Tag 1 content must be non-negative integer");
        }
      }
      return { $tag: tag, $value: val };
    }
    if (major === 7) {
      if (info === 20) return false;
      if (info === 21) return true;
      if (info === 22) return null;
      if (info === 23) {
        throw new Error("ERR_CBOR_UNSUPPORTED_TYPE: Undefined is forbidden by profile");
      }
      if (info < 20) {
        throw new Error(`ERR_CBOR_UNSUPPORTED_TYPE: Simple value simple(${info}) is forbidden by profile`);
      }
      if (info === 24) {
        if (offset >= buf.length) throw new Error("ERR_CBOR_TRUNCATED: Truncated simple value");
        const sVal = buf[offset++];
        if (sVal < 32) {
          throw new Error("ERR_CBOR_MALFORMED: Simple value < 32 encoded in 2 bytes");
        }
        throw new Error(`ERR_CBOR_UNSUPPORTED_TYPE: Simple value simple(${sVal}) is forbidden by profile`);
      }
      if (info === 25 || info === 26 || info === 27) {
        throw new Error("ERR_CBOR_UNSUPPORTED_TYPE: Floating point values are forbidden by profile");
      }
      if (info === 31) {
        throw new Error("ERR_CBOR_MALFORMED: Break stop code outside indefinite structure");
      }
      throw new Error(`ERR_CBOR_MALFORMED: Reserved simple value ${info}`);
    }
    throw new Error(`ERR_CBOR_MALFORMED: Unknown major type ${major}`);
  }

  const result = decodeItem();
  if (offset !== buf.length) {
    throw new Error(`ERR_CBOR_TRAILING_BYTES: Trailing bytes (${buf.length - offset} extra bytes)`);
  }
  return result;
}

// ============================================================================
// 3. Égalité sémantique AVN (AeterniTrak Vector Notation)
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
// 4. Canoniseur JCS de contrôle indépendant (Bushi 16, RFC 8785)
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
// 5. Validateur de Schéma JSON transparent (H4)
// ============================================================================
let schemaValidatorName = null;
let ajvValidateFn = null;

try {
  const { default: Ajv2020 } = await import("ajv/dist/2020.js");
  let ajvVer = "8.20.0";
  try {
    const pkg = JSON.parse(fs.readFileSync(path.join(PROJECT_ROOT, "node_modules/ajv/package.json"), "utf8"));
    ajvVer = pkg.version || ajvVer;
  } catch {}

  if (fs.existsSync(SCHEMA_FILE)) {
    const schemaContent = JSON.parse(fs.readFileSync(SCHEMA_FILE, "utf8"));
    const ajv = new Ajv2020({ allErrors: true });
    ajvValidateFn = ajv.compile(schemaContent);
    schemaValidatorName = `ajv ${ajvVer}`;
  }
} catch {
  ajvValidateFn = null;
  schemaValidatorName = "fallback";
}

if (!schemaValidatorName) {
  schemaValidatorName = "fallback";
}

function validateSuiteSchema(suiteData) {
  if (ajvValidateFn) {
    const valid = ajvValidateFn(suiteData);
    if (!valid) {
      return ajvValidateFn.errors.map((e) => `${e.instancePath || "/"} ${e.message}`).join("; ");
    }
    return null;
  }

  // Repli de validation structurelle si ajv non chargé
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
// 6. Vérification d'auto-cohérence, unicité (H3) et contrôle croisé strict (H2)
// ============================================================================
function verifyCaseExpectation(caseObj, globalDuplicateIds = new Set()) {
  // H3 : Unicité globale des identifiants
  if (globalDuplicateIds.has(caseObj.id)) {
    return { valid: false, reason: `Identifiant dupliqué globalement: "${caseObj.id}"` };
  }

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

  // H2 : Contrôles stricts CBOR
  if (caseObj.op === "encode") {
    if (exp.hex !== undefined) {
      try {
        const decoded = decodeCborStrict(Buffer.from(exp.hex, "hex"));
        if (!avnEqual(decoded, caseObj.input)) {
          return {
            valid: false,
            reason: `Contrôle croisé CBOR encode: le décodeur strict n'a pas retrouvé l'entrée AVN (décodé: ${JSON.stringify(decoded)}, entrée: ${JSON.stringify(caseObj.input)})`
          };
        }
      } catch (err) {
        return { valid: false, reason: `Contrôle croisé CBOR encode en échec: ${err.message}` };
      }
    }
  } else if (caseObj.op === "decode") {
    if (caseObj.input && typeof caseObj.input.hex === "string") {
      try {
        const decoded = decodeCborStrict(Buffer.from(caseObj.input.hex, "hex"));
        if (!avnEqual(decoded, exp.item)) {
          return {
            valid: false,
            reason: `Contrôle croisé CBOR decode: le décodeur strict n'a pas retrouvé expect.item (décodé: ${JSON.stringify(decoded)}, attendu: ${JSON.stringify(exp.item)})`
          };
        }
      } catch (err) {
        return { valid: false, reason: `Contrôle croisé CBOR decode en échec: ${err.message}` };
      }
    }
  } else if (caseObj.op === "reject-decode") {
    if (caseObj.input && typeof caseObj.input.hex === "string") {
      let rejected = false;
      try {
        decodeCborStrict(Buffer.from(caseObj.input.hex, "hex"));
      } catch {
        rejected = true;
      }
      if (!rejected) {
        return {
          valid: false,
          reason: "Contrôle croisé CBOR reject-decode: le décodeur strict aurait dû rejeter input.hex mais l'a accepté"
        };
      }
    }
  } else if (caseObj.op === "canonicalize") {
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
  } else if (caseObj.op === "validate-profile") {
    if (caseObj.id.startsWith("PROF-OK") || exp.valid === true) {
      if (!caseObj.input || typeof caseObj.input.hex !== "string") {
        return {
          valid: false,
          reason: "Cas validate-profile PROF-OK requiert input.hex sous forme de chaîne"
        };
      }
      try {
        decodeCborStrict(Buffer.from(caseObj.input.hex, "hex"));
      } catch (err) {
        return {
          valid: false,
          reason: `Contrôle croisé validate-profile: input.hex doit être accepté par le décodeur strict (${err.message})`
        };
      }
    }
  }

  return { valid: true };
}

// ============================================================================
// 7. Moteur d'exécution des suites
// ============================================================================
async function executeSuite(suitePath, globalDuplicateIds = new Set(), options = {}) {
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
    const check = verifyCaseExpectation(c, globalDuplicateIds);
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
// 8. Auto-test étendu à 7 corruptions (H5)
// ============================================================================
async function runSelfTest(outputLog) {
  outputLog(">>> Démarrage de l'auto-test (--selftest) : simulation de 7 corruptions dans un environnement temporaire...");
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "aeternitrak-selftest-"));

  try {
    const cborOrig = path.join(VECTORS_DIR, "core/cbor-deterministic.vectors.json");
    const jcsOrig = path.join(VECTORS_DIR, "core/jcs-rfc8785.vectors.json");
    const prionMatrixOrig = path.join(VECTORS_DIR, "antiprion/feedban-matrix.vectors.json");
    const prionHardenOrig = path.join(VECTORS_DIR, "antiprion/feedban-hardening.vectors.json");

    const tmpCoreDir = path.join(tmpDir, "core");
    const tmpPrionDir = path.join(tmpDir, "antiprion");
    const tmpNewSubDir = path.join(tmpDir, "new-sub-undeclared");

    fs.mkdirSync(tmpCoreDir, { recursive: true });
    fs.mkdirSync(tmpPrionDir, { recursive: true });
    fs.mkdirSync(tmpNewSubDir, { recursive: true });

    const cborData = JSON.parse(fs.readFileSync(cborOrig, "utf8"));
    const jcsData = JSON.parse(fs.readFileSync(jcsOrig, "utf8"));
    const prionMatrixData = JSON.parse(fs.readFileSync(prionMatrixOrig, "utf8"));
    const prionHardenData = JSON.parse(fs.readFileSync(prionHardenOrig, "utf8"));

    // Mutation 1: corruption d'un octet de hex (CBOR-ENC-001)
    const case1 = cborData.cases.find((c) => c.id === "CBOR-ENC-001");
    case1.expect.hex = "01"; // au lieu de "00"

    // Mutation 2: corruption d'un sha256 (CBOR-ENC-003)
    const case2 = cborData.cases.find((c) => c.id === "CBOR-ENC-003");
    case2.expect.sha256 = "0000000000000000000000000000000000000000000000000000000000000000";

    // Mutation 3: corruption d'une liste reasons (PRION-BLOCK-001)
    const case3 = prionMatrixData.cases.find((c) => c.id === "PRION-BLOCK-001");
    case3.expect.reasons = ["FEED_BAN_INTRA_SPECIES_VIOLATION", "MUTATED_INVALID_REASON"];

    // Mutation 4: carte non triée cohérente avec son sha256 (CBOR-ENC-045)
    const case4 = cborData.cases.find((c) => c.id === "CBOR-ENC-045");
    const unsortedHex = "a2616201616102"; // {"b":1,"a":2}
    case4.expect.hex = unsortedHex;
    case4.expect.len = unsortedHex.length / 2;
    case4.expect.sha256 = crypto.createHash("sha256").update(Buffer.from(unsortedHex, "hex")).digest("hex");

    // Mutation 5: entier non minimal cohérent avec son sha256 (CBOR-ENC-002)
    const case5 = cborData.cases.find((c) => c.id === "CBOR-ENC-002");
    const nonMinimalHex = "1801"; // 1 encodé en 2 octets
    case5.expect.hex = nonMinimalHex;
    case5.expect.len = nonMinimalHex.length / 2;
    case5.expect.sha256 = crypto.createHash("sha256").update(Buffer.from(nonMinimalHex, "hex")).digest("hex");

    // Mutation 6: identifiant dupliqué (JCS-ENC-002 duplique l'ID JCS-ENC-001)
    const case6 = jcsData.cases.find((c) => c.id === "JCS-ENC-002");
    case6.id = "JCS-ENC-001";

    // Mutation 7: suite non déclarée dans un nouveau sous-répertoire temporaire avec anomalie
    const extraSuiteData = {
      suite: "qa.probe.extra",
      version: "1.0.0",
      issued_by: "bushi-16",
      issued_at: "2026-10-04",
      status: "approved",
      spec: ["qa/vectors/README.md §5"],
      adapter: "core.cbor",
      description: "Suite sonde de découverte dynamique dans un sous-répertoire temporaire",
      cases: [
        {
          id: "PROBE-EXTRA-001",
          title: "sonde dans sous-répertoire temporaire avec sha256 altéré",
          op: "encode",
          input: 42,
          expect: {
            hex: "182a",
            len: 2,
            sha256: "0000000000000000000000000000000000000000000000000000000000000000"
          },
          rule: "Dynamic discovery probe",
          tags: ["probe"]
        }
      ]
    };

    const tmpCborPath = path.join(tmpCoreDir, "cbor-deterministic.vectors.json");
    const tmpJcsPath = path.join(tmpCoreDir, "jcs-rfc8785.vectors.json");
    const tmpPrionMatrixPath = path.join(tmpPrionDir, "feedban-matrix.vectors.json");
    const tmpPrionHardenPath = path.join(tmpPrionDir, "feedban-hardening.vectors.json");
    const tmpExtraSuitePath = path.join(tmpNewSubDir, "probe-extra.vectors.json");

    fs.writeFileSync(tmpCborPath, JSON.stringify(cborData, null, 2));
    fs.writeFileSync(tmpJcsPath, JSON.stringify(jcsData, null, 2));
    fs.writeFileSync(tmpPrionMatrixPath, JSON.stringify(prionMatrixData, null, 2));
    fs.writeFileSync(tmpPrionHardenPath, JSON.stringify(prionHardenData, null, 2));
    fs.writeFileSync(tmpExtraSuitePath, JSON.stringify(extraSuiteData, null, 2));

    // Découverte dynamique sur tmpDir (H1)
    const discoveredSuites = discoverSuites(tmpDir);

    // Calcul des identifiants dupliqués sur toutes les suites découvertes (H3)
    const idFrequency = new Map();
    for (const sp of discoveredSuites) {
      const suiteContent = JSON.parse(fs.readFileSync(sp, "utf8"));
      if (Array.isArray(suiteContent.cases)) {
        for (const c of suiteContent.cases) {
          idFrequency.set(c.id, (idFrequency.get(c.id) || 0) + 1);
        }
      }
    }
    const globalDuplicateIds = new Set();
    for (const [id, count] of idFrequency.entries()) {
      if (count > 1) {
        globalDuplicateIds.add(id);
      }
    }

    const suiteReports = [];
    const totalSummary = { pass: 0, fail: 0, red: 0, invalid: 0, total: 0 };

    for (const sp of discoveredSuites) {
      const rep = await executeSuite(sp, globalDuplicateIds);
      suiteReports.push(rep);
      totalSummary.pass += rep.summary.pass;
      totalSummary.fail += rep.summary.fail;
      totalSummary.red += rep.summary.red;
      totalSummary.invalid += rep.summary.invalid;
      totalSummary.total += rep.summary.total;

      for (const c of rep.cases) {
        if (c.status === "INVALID") {
          outputLog(`${c.status} ${c.id} ${c.title}`);
          if (c.error) {
            outputLog(`  -> ${c.error}`);
          }
        }
      }
    }

    // Vérification unitaire de chaque sonde (1 à 7)
    const allCases = suiteReports.flatMap((s) => s.cases);
    const probeResults = {
      probe1_hex: allCases.some((c) => c.id === "CBOR-ENC-001" && c.status === "INVALID"),
      probe2_sha256: allCases.some((c) => c.id === "CBOR-ENC-003" && c.status === "INVALID"),
      probe3_reasons: allCases.some((c) => c.id === "PRION-BLOCK-001" && c.status === "INVALID"),
      probe4_unsorted_map: allCases.some((c) => c.id === "CBOR-ENC-045" && c.status === "INVALID" && (c.error || "").includes("UNSORTED")),
      probe5_non_minimal_int: allCases.some((c) => c.id === "CBOR-ENC-002" && c.status === "INVALID" && (c.error || "").includes("SHORTEST")),
      probe6_duplicate_id: allCases.filter((c) => c.id === "JCS-ENC-001" && c.status === "INVALID" && (c.error || "").includes("dupliqué")).length >= 2,
      probe7_undeclared_suite: suiteReports.some((s) => s.suite === "qa.probe.extra" && s.cases.some((c) => c.id === "PROBE-EXTRA-001" && c.status === "INVALID"))
    };

    outputLog("\n--- Bilan des 7 sondes de corruption simulées ---");
    outputLog(`[Sonde 1/7] Un octet de hex altéré (CBOR-ENC-001) : ${probeResults.probe1_hex ? "DÉTECTÉ" : "ÉCHEC"}`);
    outputLog(`[Sonde 2/7] Un sha256 altéré (CBOR-ENC-003) : ${probeResults.probe2_sha256 ? "DÉTECTÉ" : "ÉCHEC"}`);
    outputLog(`[Sonde 3/7] Une liste reasons altérée (PRION-BLOCK-001) : ${probeResults.probe3_reasons ? "DÉTECTÉ" : "ÉCHEC"}`);
    outputLog(`[Sonde 4/7] Une carte non triée cohérente avec son sha256 (CBOR-ENC-045) : ${probeResults.probe4_unsorted_map ? "DÉTECTÉ" : "ÉCHEC"}`);
    outputLog(`[Sonde 5/7] Un entier non minimal cohérent avec son sha256 (CBOR-ENC-002) : ${probeResults.probe5_non_minimal_int ? "DÉTECTÉ" : "ÉCHEC"}`);
    outputLog(`[Sonde 6/7] Un identifiant dupliqué (JCS-ENC-001, marqué 2x INVALID) : ${probeResults.probe6_duplicate_id ? "DÉTECTÉ" : "ÉCHEC"}`);
    outputLog(`[Sonde 7/7] Une suite non déclarée dans un sous-répertoire (qa.probe.extra) : ${probeResults.probe7_undeclared_suite ? "DÉTECTÉ" : "ÉCHEC"}`);

    const detectedCount = Object.values(probeResults).filter(Boolean).length;

    outputLog("\n============================================================");
    outputLog(`RÉSULTAT SELFTEST : ${detectedCount}/7 corruptions détectées (${totalSummary.invalid} cas INVALID)`);
    outputLog("============================================================");

    if (detectedCount === 7) {
      outputLog("[SELFTEST OK] 7 corruptions détectées sur 7.");
      return { totalSummary, suiteReports, exitCode: 0 };
    } else {
      outputLog(`[SELFTEST ANOMALIE] Seulement ${detectedCount}/7 corruptions détectées.`);
      return { totalSummary, suiteReports, exitCode: 3 };
    }
  } finally {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  }
}

// ============================================================================
// 9. Point d'entrée principal
// ============================================================================
async function main() {
  const logBuffer = [];
  function outputLog(line = "") {
    process.stdout.write(line + "\n");
    logBuffer.push(line);
  }

  // H4 : Affichage obligatoire du validateur dès la première ligne
  outputLog(`Validateur de schéma : ${schemaValidatorName}`);

  const rawArgs = process.argv.slice(2);
  const args = rawArgs.filter((a) => a !== "test");
  const isSelftest = args.includes("--selftest");
  const allowFallback = args.includes("--allow-fallback");
  const filter = args.find((a) => !a.startsWith("--"));

  if (schemaValidatorName === "fallback") {
    outputLog("AVERTISSEMENT : Mode fallback actif (ajv absent).");
    if (!allowFallback) {
      outputLog("Erreur : le mode fallback n'est pas autorisé sans l'option --allow-fallback.");
      // Sauvegarde du log avant sortie
      try {
        fs.mkdirSync(path.dirname(OUT_FILE), { recursive: true });
        fs.appendFileSync(OUT_FILE, logBuffer.join("\n") + "\n");
      } catch {}
      process.exit(2);
    }
  }

  // Résolution du SHA et de la branche git
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
    // Découverte dynamique récursive des suites (H1)
    const discoveredSuites = discoverSuites(VECTORS_DIR);

    const activeSuites = discoveredSuites.filter((f) => {
      if (!filter) return true;
      const rel = path.relative(PROJECT_ROOT, f);
      return rel.includes(filter) || path.basename(f).includes(filter);
    });

    if (activeSuites.length === 0) {
      outputLog(`Aucune suite trouvée pour le filtre "${filter}".`);
      process.exit(0);
    }

    // Calcul de l'unicité globale des identifiants (H3)
    const idFrequency = new Map();
    for (const sp of activeSuites) {
      try {
        const content = JSON.parse(fs.readFileSync(sp, "utf8"));
        if (Array.isArray(content.cases)) {
          for (const c of content.cases) {
            idFrequency.set(c.id, (idFrequency.get(c.id) || 0) + 1);
          }
        }
      } catch {}
    }
    const globalDuplicateIds = new Set();
    for (const [id, count] of idFrequency.entries()) {
      if (count > 1) {
        globalDuplicateIds.add(id);
      }
    }

    for (const sp of activeSuites) {
      const rep = await executeSuite(sp, globalDuplicateIds);
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
    const reportFileName = isSelftest
      ? `${dateStr}-${shortSha}-selftest.json`
      : `${dateStr}-${shortSha}.json`;
    const reportPath = path.join(REPORTS_DIR, reportFileName);
    const reportData = {
      date: dateStr,
      commit: shortSha,
      branch: branchName,
      validator: schemaValidatorName,
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
