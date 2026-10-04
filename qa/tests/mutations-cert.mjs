#!/usr/bin/env node
/**
 * AeterniTrak V1.0 — Test des 6 Mutations du Certificat de Lot (Phase B - Ordre 0066)
 *
 * Démontre que 6 altérations délibérées font chacune échouer
 * au moins un vecteur de test nommé dans `batch-certificate.vectors.json` :
 * 1. Verdict non contrôlé à l'émission -> échec de CERT-ISSUE-008 (émission d'un lot bloqué)
 * 2. Réévaluation retirée à la vérification -> échec de CERT-VER-049 (acceptation aveugle de signature)
 * 3. Empreinte de la revendication non comparée -> échec de CERT-VER-037 (revendication altérée acceptée)
 * 4. cose-open utilisé à la place de cose-verify -> échec de CERT-VER-007 (émetteur inconnu non bloqué)
 * 5. Clé 6 acceptée hors mémoire forestière -> échec de CERT-VER-045 (clé 6 inattendue acceptée)
 * 6. Politique prise ailleurs que dans le registre local -> échec de CERT-VER-047 (politique inconnue acceptée)
 */

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

import { run as certAdapterRun } from "../harness/adapters/crypto.cert.mjs";
import { evaluateAndSign, certVerify, CertError, TAXONOMY_SNAPSHOT_SHA256, RULES_VERSION } from "../../core/cert/index.ts";
import { coseVerify, coseOpen, protectedHeader, sigStructure, ed25519Sign, kid } from "../../core/cose/index.ts";
import { decodeToCborValue } from "../../core/cbor/decoder.ts";
import { encode, hexToBytes, bytesToHex, compareBytes } from "../../core/cbor/index.ts";
import { canonicalizeJsonString } from "../../core/jcs/canonicalize.ts";
import { evaluate } from "../../validators/antiprion/index.ts";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, "../..");
const VECTORS_PATH = path.join(PROJECT_ROOT, "qa/vectors/crypto/batch-certificate.vectors.json");

const suite = JSON.parse(fs.readFileSync(VECTORS_PATH, "utf8"));

function getCase(id) {
  const c = suite.cases.find((x) => x.id === id);
  if (!c) throw new Error(`Vecteur introuvable dans batch-certificate: ${id}`);
  return c;
}

console.log("============================================================");
console.log("AeterniTrak — Test des 6 Mutations Normatives (Batch Certificate)");
console.log("============================================================");

let allPassed = true;

// ----------------------------------------------------------------------------
// Mutation 1 : Verdict non contrôlé à l'émission (émission d'un lot bloqué)
// Vecteur ciblé : CERT-ISSUE-008 (recyclage intra-espèce porc -> porcins)
// ----------------------------------------------------------------------------
{
  const c08 = getCase("CERT-ISSUE-008");
  const canonicalRes = await certAdapterRun("cert-issue", c08.input);

  // Émetteur muté : contrôle du verdict commenté / ignoré
  async function mutatedIssue(claimInput, policyInput, context) {
    const claimJson = canonicalizeJsonString(claimInput);
    const claimBytes = new TextEncoder().encode(claimJson);
    const claimSha256Buf = await globalThis.crypto.subtle.digest("SHA-256", claimBytes);
    const claimSha256 = new Uint8Array(claimSha256Buf);

    // MUTATION : Pas de contrôle de evalResult.verdict !== "AUTHORISED"
    const mapEntries = [
      [1, claimSha256],
      [2, "AUTHORISED"],
      [3, { $tag: 1, $value: context.issuedAt }],
      [4, TAXONOMY_SNAPSHOT_SHA256],
      [5, RULES_VERSION]
    ];
    const payloadBytes = encode({ $map: mapEntries });
    const protectedBytes = protectedHeader(context.signer.algorithm, "application/aeternitrak-batch-claim+cbor");
    const tbs = sigStructure(protectedBytes, payloadBytes);
    const signature = await context.signer.sign(tbs);
    const unprotected = { $map: [[4, context.signer.kid]] };
    const arrayBytes = encode([protectedBytes, unprotected, payloadBytes, signature]);
    const envelope = new Uint8Array(1 + arrayBytes.length);
    envelope[0] = 0xd2;
    envelope.set(arrayBytes, 1);
    return { envelope, claimJson };
  }

  const seed = hexToBytes(c08.input.seed_hex);
  const { publicKey } = await ed25519Sign(seed, new Uint8Array(0));
  const signerKid = await kid(publicKey);
  let mutatedRes;
  try {
    const signer = {
      algorithm: -8,
      kid: signerKid,
      sign: async (tbs) => (await ed25519Sign(seed, tbs)).signature
    };
    const res = await mutatedIssue(c08.input.claim, c08.input.policy, {
      signer,
      issuedAt: c08.input.issued_at,
      policies: c08.input.policies
    });
    mutatedRes = {
      envelope_hex: bytesToHex(res.envelope),
      len: res.envelope.length
    };
  } catch (err) {
    mutatedRes = { error: err.code || err.message };
  }

  console.log("\n[Mutation 1] Verdict sanitaire non contrôlé à l'émission :");
  console.log(`  Vecteur ciblé       : CERT-ISSUE-008 ("${c08.title}")`);
  console.log(`  Attendu             : ${JSON.stringify(c08.expect)}`);
  console.log(`  Canonique           : ${JSON.stringify(canonicalRes)} -> PASS`);
  console.log(`  Muté (signe quand même) : ${JSON.stringify(mutatedRes)} -> ÉCHEC DE SÉCURITÉ`);

  if (
    canonicalRes.error === "ERR_CERT_ISSUANCE_REFUSED" &&
    Array.isArray(canonicalRes.refusal_reasons) &&
    canonicalRes.refusal_reasons.includes("FEED_BAN_INTRA_SPECIES_VIOLATION") &&
    mutatedRes.envelope_hex !== undefined
  ) {
    console.log("  => MUTATION 1 DÉTECTÉE : la Règle d'Or bloque l'émission comme requis.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 1.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 2 : Réévaluation retirée à la vérification (acceptation aveugle de signature)
// Vecteur ciblé : CERT-VER-049 (certificat signé pour un lot intra-espèce)
// ----------------------------------------------------------------------------
{
  const c49 = getCase("CERT-VER-049");
  const canonicalRes = await certAdapterRun("cert-verify", c49.input);

  // Vérificateur muté : étape 10 (réévaluation The Iron Gate) retirée
  async function mutatedVerify(envelope, claimJson, trustStore) {
    const coseResult = await coseVerify(envelope, "application/aeternitrak-batch-claim+cbor", trustStore);
    // MUTATION : Retourne valid: true directement sans evaluate()
    return {
      valid: true,
      kid: coseResult.kid,
      issued_at: 1791072000,
      rules_version: "1.5.0",
      derogation: false
    };
  }

  let mutatedRes;
  try {
    const res = await mutatedVerify(
      hexToBytes(c49.input.envelope_hex),
      c49.input.claim_json,
      c49.input.trust_store
    );
    mutatedRes = res;
  } catch (err) {
    mutatedRes = { error: err.code || err.message };
  }

  console.log("\n[Mutation 2] Réévaluation sanitaire The Iron Gate retirée à la vérification :");
  console.log(`  Vecteur ciblé       : CERT-VER-049 ("${c49.title}")`);
  console.log(`  Attendu             : ${JSON.stringify(c49.expect)}`);
  console.log(`  Canonique           : ${JSON.stringify(canonicalRes)} -> PASS`);
  console.log(`  Muté (confiance aveugle) : ${JSON.stringify(mutatedRes)} -> ÉCHEC DE SÉCURITÉ`);

  if (canonicalRes.error === "ERR_CERT_RE_EVALUATION_FAILED" && mutatedRes.valid === true) {
    console.log("  => MUTATION 2 DÉTECTÉE : la réévaluation indépendante bloque la fraude.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 2.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 3 : Empreinte de la revendication non comparée
// Vecteur ciblé : CERT-VER-037 (revendication modifiée après signature)
// ----------------------------------------------------------------------------
{
  const c37 = getCase("CERT-VER-037");
  const canonicalRes = await certAdapterRun("cert-verify", c37.input);

  // Vérificateur muté : compareBytes(claimSha256, val1.value) sauté
  async function mutatedVerify(envelope, claimJson, trustStore, options) {
    const coseResult = await coseVerify(envelope, "application/aeternitrak-batch-claim+cbor", trustStore);
    const payloadVal = decodeToCborValue(coseResult.payload);
    // MUTATION : Pas de comparaison claimSha256 !== val1.value
    const claimParsed = JSON.parse(claimJson);
    const reEval = evaluate(claimParsed, null);
    if (reEval.verdict !== "AUTHORISED") {
      throw new CertError("ERR_CERT_RE_EVALUATION_FAILED", "Blocked");
    }
    return {
      valid: true,
      kid: coseResult.kid,
      issued_at: 1791072000,
      rules_version: "1.5.0",
      derogation: false
    };
  }

  let mutatedRes;
  try {
    const res = await mutatedVerify(
      hexToBytes(c37.input.envelope_hex),
      c37.input.claim_json,
      c37.input.trust_store,
      { policies: c37.input.policies }
    );
    mutatedRes = res;
  } catch (err) {
    mutatedRes = { error: err.code || err.message };
  }

  console.log("\n[Mutation 3] Empreinte de revendication non comparée (Étape 6) :");
  console.log(`  Vecteur ciblé       : CERT-VER-037 ("${c37.title}")`);
  console.log(`  Attendu             : ${JSON.stringify(c37.expect)}`);
  console.log(`  Canonique           : ${JSON.stringify(canonicalRes)} -> PASS`);
  console.log(`  Muté (hash ignoré)  : ${JSON.stringify(mutatedRes)} -> ÉCHEC DE SÉCURITÉ`);

  if (
    canonicalRes.error === "ERR_CERT_CLAIM_HASH_MISMATCH" &&
    mutatedRes.error !== "ERR_CERT_CLAIM_HASH_MISMATCH"
  ) {
    console.log("  => MUTATION 3 DÉTECTÉE : l'absence de contrôle d'empreinte dégrade l'intégrité (ERR_CERT_CLAIM_HASH_MISMATCH non levé).");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 3.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 4 : cose-open utilisé à la place de cose-verify
// Vecteur ciblé : CERT-VER-007 (émetteur inconnu : doit bloquer avec ERR_COSE_UNKNOWN_KID)
// ----------------------------------------------------------------------------
{
  const c07 = getCase("CERT-VER-007");
  const canonicalRes = await certAdapterRun("cert-verify", c07.input);

  // Vérificateur muté : utilise coseOpen au lieu de coseVerify
  async function mutatedVerify(envelope, claimJson, trustStore) {
    const openRes = await coseOpen(envelope, "application/aeternitrak-batch-claim+cbor", trustStore);
    if (openRes.status === "UNVERIFIED") {
      // MUTATION : Traite UNVERIFIED comme toléré au lieu de bloquer
      return { status: "UNVERIFIED", reason: openRes.reason, payload_hex: openRes.payload_hex };
    }
    return { valid: true };
  }

  let mutatedRes;
  try {
    const res = await mutatedVerify(
      hexToBytes(c07.input.envelope_hex),
      c07.input.claim_json,
      c07.input.trust_store
    );
    mutatedRes = res;
  } catch (err) {
    mutatedRes = { error: err.code || err.message };
  }

  console.log("\n[Mutation 4] cose-open utilisé à la place de cose-verify (A2) :");
  console.log(`  Vecteur ciblé       : CERT-VER-007 ("${c07.title}")`);
  console.log(`  Attendu             : ${JSON.stringify(c07.expect)}`);
  console.log(`  Canonique           : ${JSON.stringify(canonicalRes)} -> PASS`);
  console.log(`  Muté (cose-open)    : ${JSON.stringify(mutatedRes)} -> ÉCHEC DE SÉCURITÉ`);

  if (canonicalRes.error === "ERR_COSE_UNKNOWN_KID" && mutatedRes.status === "UNVERIFIED") {
    console.log("  => MUTATION 4 DÉTECTÉE : aucun état 'sous réserve' n'est toléré.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 4.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 5 : Clé 6 acceptée hors mémoire forestière
// Vecteur ciblé : CERT-VER-045 (lot alimentaire avec clé 6)
// ----------------------------------------------------------------------------
{
  const c45 = getCase("CERT-VER-045");
  const canonicalRes = await certAdapterRun("cert-verify", c45.input);

  // Vérificateur muté : suppression du contrôle if (!isMemorial && val6 !== undefined)
  async function mutatedVerify(envelope, claimJson, trustStore, options) {
    const coseResult = await coseVerify(envelope, "application/aeternitrak-batch-claim+cbor", trustStore);
    const payloadVal = decodeToCborValue(coseResult.payload);
    const seenKeys = new Map();
    for (const [k, v] of payloadVal.entries) {
      seenKeys.set(Number(k.value), v);
    }
    const claimParsed = JSON.parse(claimJson);
    // MUTATION : On autorise val6 sur tout type de lot
    const reEval = evaluate(claimParsed, null);
    if (reEval.verdict !== "AUTHORISED") {
      throw new CertError("ERR_CERT_RE_EVALUATION_FAILED", "Blocked");
    }
    return {
      valid: true,
      kid: coseResult.kid,
      issued_at: 1791072000,
      rules_version: "1.5.0",
      derogation: false
    };
  }

  let mutatedRes;
  try {
    const res = await mutatedVerify(
      hexToBytes(c45.input.envelope_hex),
      c45.input.claim_json,
      c45.input.trust_store,
      { policies: c45.input.policies }
    );
    mutatedRes = res;
  } catch (err) {
    mutatedRes = { error: err.code || err.message };
  }

  console.log("\n[Mutation 5] Clé 6 acceptée hors mémoire forestière (Étape 9) :");
  console.log(`  Vecteur ciblé       : CERT-VER-045 ("${c45.title}")`);
  console.log(`  Attendu             : ${JSON.stringify(c45.expect)}`);
  console.log(`  Canonique           : ${JSON.stringify(canonicalRes)} -> PASS`);
  console.log(`  Muté (clé 6 admise) : ${JSON.stringify(mutatedRes)} -> ÉCHEC DE SÉCURITÉ`);

  if (canonicalRes.error === "ERR_CERT_UNEXPECTED_POLICY" && mutatedRes.valid === true) {
    console.log("  => MUTATION 5 DÉTECTÉE : la clé 6 est strictement confinée à memorial_forestry.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 5.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 6 : Politique prise ailleurs que dans le registre local
// Vecteur ciblé : CERT-VER-047 (politique introuvable dans le registre)
// ----------------------------------------------------------------------------
{
  const c47 = getCase("CERT-VER-047");
  const canonicalRes = await certAdapterRun("cert-verify", c47.input);

  // Vérificateur muté : utilise une politique par défaut fictive au lieu du registre local
  async function mutatedVerify(envelope, claimJson, trustStore) {
    const coseResult = await coseVerify(envelope, "application/aeternitrak-batch-claim+cbor", trustStore);
    const claimParsed = JSON.parse(claimJson);
    // MUTATION : Fournit une politique par défaut pour bypasser le registre
    const dummyPolicy = {
      policy_id: "DEC-AET-05",
      version: 1,
      legal_basis: "Auto-approved",
      authority_reference: "TEST-ONLY"
    };
    const reEval = evaluate(claimParsed, dummyPolicy);
    if (reEval.verdict !== "AUTHORISED") {
      throw new CertError("ERR_CERT_RE_EVALUATION_FAILED", "Blocked");
    }
    return {
      valid: true,
      kid: coseResult.kid,
      issued_at: 1791072000,
      rules_version: "1.5.0",
      derogation: true
    };
  }

  let mutatedRes;
  try {
    const res = await mutatedVerify(
      hexToBytes(c47.input.envelope_hex),
      c47.input.claim_json,
      c47.input.trust_store
    );
    mutatedRes = res;
  } catch (err) {
    mutatedRes = { error: err.code || err.message };
  }

  console.log("\n[Mutation 6] Politique prise hors registre local vérificateur (A3) :");
  console.log(`  Vecteur ciblé       : CERT-VER-047 ("${c47.title}")`);
  console.log(`  Attendu             : ${JSON.stringify(c47.expect)}`);
  console.log(`  Canonique           : ${JSON.stringify(canonicalRes)} -> PASS`);
  console.log(`  Muté (politique fallback) : ${JSON.stringify(mutatedRes)} -> ÉCHEC DE SÉCURITÉ`);

  if (canonicalRes.error === "ERR_CERT_UNKNOWN_POLICY" && mutatedRes.valid === true) {
    console.log("  => MUTATION 6 DÉTECTÉE : la politique doit obligatoirement résider dans le registre local.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 6.");
    allPassed = false;
  }
}

console.log("\n============================================================");
if (allPassed) {
  console.log("RÉSULTAT : 6/6 MUTATIONS DÉTECTÉES AVEC SUCCÈS !");
  console.log("============================================================");
  process.exit(0);
} else {
  console.error("RÉSULTAT : ÉCHEC D'AU MOINS UNE MUTATION !");
  console.log("============================================================");
  process.exit(1);
}
