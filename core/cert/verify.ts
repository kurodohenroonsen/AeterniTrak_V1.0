/**
 * AeterniTrak V1.0 — Vérification Séquentielle Normative du Certificat de Lot
 * Conformité : AET-SPEC-CERT-001 v1.1.0 §4.3.3 (10 étapes), qa/vectors/README.md §4.14
 */

import { decodeToCborValue, type CborValue } from "../cbor/decoder.ts";
import { compareBytes } from "../cbor/writer.ts";
import { canonicalizeJsonString } from "../jcs/canonicalize.ts";
import { coseVerify } from "../cose/index.ts";
import { evaluate } from "../../validators/antiprion/index.ts";
import { CertError } from "./errors.ts";
import { TAXONOMY_SNAPSHOT_SHA256, RULES_VERSION } from "./constants.ts";
import type { TrustStore, CertVerifyOptions, CertVerifyResult } from "./types.ts";

/**
 * Vérifie un certificat de conformité sanitaire selon les 10 étapes séquentielles normatives.
 * Arrêt immédiat dès la première défaillance (Fail-Fast).
 *
 * @param envelope - Octets bruts de l'enveloppe COSE_Sign1 scellée.
 * @param claimJson - Chaîne brute de la revendication présentée.
 * @param trustStore - Liste de confiance officielle du vérificateur.
 * @param options - Options de vérification (registre de politiques, versions de règles retirées).
 * @returns { valid: true, kid, issued_at, rules_version, derogation }
 * @throws {CoseError | CborError | CertError}
 */
export async function certVerify(
  envelope: Uint8Array,
  claimJson: string,
  trustStore: TrustStore,
  options?: CertVerifyOptions
): Promise<CertVerifyResult> {
  // ==========================================================================
  // Étape 1 : Validation intégrale de l'enveloppe COSE_Sign1 (13 étapes K1-K2)
  // Jamais de cose-open ni d'état UNVERIFIED : un émetteur inconnu bloque irrémédiablement.
  // ==========================================================================
  const coseResult = await coseVerify(
    envelope,
    "application/aeternitrak-batch-claim+cbor",
    trustStore
  );

  // ==========================================================================
  // Étape 2 : Décodage déterministe de la charge utile CBOR
  // Doit être obligatoirement une carte CBOR déterministe.
  // ==========================================================================
  const payloadVal = decodeToCborValue(coseResult.payload);
  if (payloadVal.type !== "map") {
    throw new CertError("ERR_CERT_INVALID_FIELD", "Batch certificate payload must be a CBOR map");
  }

  // ==========================================================================
  // Étape 3 : Contrôle ordonné de structure et de typage (clés & valeurs)
  // ==========================================================================
  const seenKeys = new Map<number, CborValue>();

  // 1. Contrôle des types de clés et plage autorisée {1..6}
  for (const [k, v] of payloadVal.entries) {
    if (k.type !== "uint") {
      throw new CertError("ERR_CERT_UNAUTHORIZED_PAYLOAD_KEY", "Payload map key must be an unsigned integer");
    }
    const kNum = typeof k.value === "bigint" ? Number(k.value) : k.value;
    if (!Number.isInteger(kNum) || kNum < 1 || kNum > 6) {
      throw new CertError("ERR_CERT_UNAUTHORIZED_PAYLOAD_KEY", `Unauthorized payload key: ${kNum}`);
    }
    seenKeys.set(kNum, v);
  }

  // 2. Présence impérative des clés obligatoires 1 à 5
  for (let k = 1; k <= 5; k++) {
    if (!seenKeys.has(k)) {
      throw new CertError("ERR_CERT_MISSING_MANDATORY_FIELD", `Missing mandatory payload key ${k}`);
    }
  }

  // 3. Typage strict des valeurs
  const val1 = seenKeys.get(1)!;
  if (val1.type !== "bytes" || val1.value.length !== 32) {
    throw new CertError("ERR_CERT_INVALID_FIELD", "Key 1 (claim_sha256) must be a 32-byte string");
  }

  const val4 = seenKeys.get(4)!;
  if (val4.type !== "bytes" || val4.value.length !== 32) {
    throw new CertError("ERR_CERT_INVALID_FIELD", "Key 4 (snapshot_sha256) must be a 32-byte string");
  }

  const val5 = seenKeys.get(5)!;
  if (val5.type !== "text") {
    throw new CertError("ERR_CERT_INVALID_FIELD", "Key 5 (rules_version) must be a text string");
  }

  const val6 = seenKeys.get(6);
  if (val6 !== undefined) {
    if (val6.type !== "bytes" || val6.value.length !== 32) {
      throw new CertError("ERR_CERT_INVALID_FIELD", "Key 6 (policy_sha256) must be a 32-byte string");
    }
  }

  // ==========================================================================
  // Étape 4 : Contrôle du verdict scellé (clé 2)
  // ==========================================================================
  const val2 = seenKeys.get(2)!;
  if (val2.type !== "text" || val2.value !== "AUTHORISED") {
    throw new CertError("ERR_CERT_VERDICT_NOT_AUTHORISED", 'Key 2 (verdict) must be strictly "AUTHORISED"');
  }

  // ==========================================================================
  // Étape 5 : Contrôle de la date d'émission (clé 3)
  // ==========================================================================
  const val3 = seenKeys.get(3)!;
  if (val3.type !== "tag" || val3.tag !== 1 || val3.value.type !== "uint") {
    throw new CertError("ERR_CERT_INVALID_ISSUED_AT", "Key 3 (issued_at) must have CBOR tag 1 over non-negative integer");
  }

  const rawIssuedAt = val3.value.value;
  const issuedAt = typeof rawIssuedAt === "bigint" ? Number(rawIssuedAt) : rawIssuedAt;
  if (!Number.isInteger(issuedAt) || issuedAt < 0 || Object.is(issuedAt, -0)) {
    throw new CertError("ERR_CERT_INVALID_ISSUED_AT", "Key 3 (issued_at) must be a non-negative integer");
  }

  // ==========================================================================
  // Étape 6 : Contrôle de canonicalité JCS & concordance de la revendication (clé 1)
  // ==========================================================================
  let claimParsed: unknown;
  try {
    claimParsed = JSON.parse(claimJson);
  } catch {
    throw new CertError("ERR_CERT_CLAIM_NOT_CANONICAL", "claimJson is not valid JSON");
  }

  let canonicalClaim: string;
  try {
    canonicalClaim = canonicalizeJsonString(claimParsed);
  } catch {
    throw new CertError("ERR_CERT_CLAIM_NOT_CANONICAL", "claimJson could not be canonicalized with JCS");
  }

  if (canonicalClaim !== claimJson) {
    throw new CertError("ERR_CERT_CLAIM_NOT_CANONICAL", "claimJson does not match canonical JCS representation");
  }

  const claimBytes = new TextEncoder().encode(claimJson);
  const claimHashBuf = await globalThis.crypto.subtle.digest("SHA-256", claimBytes);
  const claimSha256 = new Uint8Array(claimHashBuf);

  if (compareBytes(claimSha256, val1.value) !== 0) {
    throw new CertError("ERR_CERT_CLAIM_HASH_MISMATCH", "Claim SHA-256 does not match key 1 sealed in certificate");
  }

  // ==========================================================================
  // Étape 7 : Résolution du snapshot taxonomique (clé 4)
  // ==========================================================================
  if (compareBytes(val4.value, TAXONOMY_SNAPSHOT_SHA256) !== 0) {
    throw new CertError("ERR_CERT_UNKNOWN_TAXONOMY_SNAPSHOT", "Taxonomy snapshot hash is unknown to validator");
  }

  // ==========================================================================
  // Étape 8 : Résolution et qualification du moteur de règles (clé 5)
  // ==========================================================================
  if (val5.value !== RULES_VERSION) {
    throw new CertError("ERR_CERT_UNKNOWN_RULES_VERSION", `Unknown rules version: ${val5.value}`);
  }

  if (options?.retiredRulesVersions && options.retiredRulesVersions.includes(val5.value)) {
    throw new CertError("ERR_CERT_RULES_VERSION_RETIRED", `Rules version ${val5.value} has been retired`);
  }

  // ==========================================================================
  // Étape 9 : Contrôle ordonné de liaison dérogatoire (clé 6)
  // ==========================================================================
  const isMemorial =
    claimParsed !== null &&
    typeof claimParsed === "object" &&
    !Array.isArray(claimParsed) &&
    (claimParsed as Record<string, unknown>).destination !== null &&
    typeof (claimParsed as Record<string, unknown>).destination === "object" &&
    ((claimParsed as Record<string, unknown>).destination as Record<string, unknown>).use === "memorial_forestry";

  if (!isMemorial && val6 !== undefined) {
    throw new CertError("ERR_CERT_UNEXPECTED_POLICY", "Key 6 is present on a non-memorial batch certificate");
  }

  if (isMemorial && val6 === undefined) {
    throw new CertError("ERR_CERT_DEROGATION_UNBOUND", "Key 6 is missing for memorial forestry batch certificate");
  }

  let resolvedPolicy: unknown = null;
  if (isMemorial && val6 !== undefined) {
    const policySha256Bytes = val6.value;
    if (!options?.policies || !Array.isArray(options.policies) || options.policies.length === 0) {
      throw new CertError("ERR_CERT_UNKNOWN_POLICY", "Policy registry is empty or missing");
    }

    let foundPolicy: unknown = null;
    for (const pol of options.policies) {
      try {
        const polJson = canonicalizeJsonString(pol);
        const polHashBuf = await globalThis.crypto.subtle.digest("SHA-256", new TextEncoder().encode(polJson));
        if (compareBytes(new Uint8Array(polHashBuf), policySha256Bytes) === 0) {
          foundPolicy = pol;
          break;
        }
      } catch {
        // ignore invalid policy entries in registry
      }
    }

    if (!foundPolicy) {
      throw new CertError("ERR_CERT_UNKNOWN_POLICY", "Policy hash from key 6 not found in local policy registry");
    }
    resolvedPolicy = foundPolicy;
  }

  // ==========================================================================
  // Étape 10 : Ré-évaluation complète indépendante par The Iron Gate
  // Zéro confiance aveugle en la signature : The Iron Gate tranche en dernier ressort.
  // ==========================================================================
  const reEval = evaluate(claimParsed, resolvedPolicy);
  if (reEval.verdict !== "AUTHORISED" || reEval.signature_permitted !== true) {
    throw new CertError(
      "ERR_CERT_RE_EVALUATION_FAILED",
      "Independent sanitary re-evaluation failed: claim is BLOCKED by The Iron Gate",
      reEval.reasons
    );
  }

  return {
    valid: true,
    kid: coseResult.kid,
    issued_at: issuedAt,
    rules_version: val5.value,
    derogation: isMemorial
  };
}
