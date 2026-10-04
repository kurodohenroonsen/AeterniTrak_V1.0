/**
 * AeterniTrak V1.0 — Émission du Certificat de Lot (evaluateAndSign)
 * Conformité : AET-SPEC-CERT-001 v1.1.0 §4.1.3, qa/vectors/README.md §4.14
 */

import { encode } from "../cbor/index.ts";
import { compareBytes } from "../cbor/writer.ts";
import { canonicalizeJsonString } from "../jcs/canonicalize.ts";
import { protectedHeader, sigStructure } from "../cose/index.ts";
import { evaluate } from "../../validators/antiprion/index.ts";
import { CertError } from "./errors.ts";
import { TAXONOMY_SNAPSHOT_SHA256, RULES_VERSION } from "./constants.ts";
import type { BatchIssuanceContext, CertIssueResult } from "./types.ts";

/**
 * Fonction d'émission d'un certificat de conformité sanitaire de lot.
 * Évalue la conformité selon The Iron Gate et scelle l'enveloppe COSE_Sign1.
 * RÈGLE D'OR : Si le verdict sanitaire est BLOCKED, la méthode signer.sign() n'est JAMAIS appelée.
 *
 * @param claimInput - Revendication sanitaire de lot (objet ou valeur JSON).
 * @param policyInput - Politique dérogatoire optionnelle (DEC-AET-05).
 * @param context - Contexte d'émission (signataire matériel, date d'émission, registre de politiques).
 * @returns { envelope: Uint8Array, claimJson: string }
 * @throws {CertError}
 */
export async function evaluateAndSign(
  claimInput: unknown,
  policyInput: unknown | null | undefined,
  context: BatchIssuanceContext
): Promise<CertIssueResult> {
  // 1. Contrôle de validité de issued_at
  if (
    context === null ||
    typeof context !== "object" ||
    typeof context.issuedAt !== "number" ||
    !Number.isInteger(context.issuedAt) ||
    context.issuedAt < 0 ||
    Object.is(context.issuedAt, -0)
  ) {
    throw new CertError("ERR_CERT_INVALID_ISSUED_AT", "issued_at must be a non-negative integer");
  }

  // 2. Contrôle de la politique dérogatoire à l'émission
  // Si une politique est fournie, elle DOIT être reconnue dans le registre local avant toute évaluation.
  let policySha256Bytes: Uint8Array | null = null;
  if (policyInput !== null && policyInput !== undefined) {
    try {
      const policyJson = canonicalizeJsonString(policyInput);
      const buf = await globalThis.crypto.subtle.digest("SHA-256", new TextEncoder().encode(policyJson));
      policySha256Bytes = new Uint8Array(buf);
    } catch {
      throw new CertError("ERR_CERT_UNKNOWN_POLICY", "Policy canonicalization failed");
    }

    let foundInRegistry = false;
    if (Array.isArray(context.policies)) {
      for (const pol of context.policies) {
        try {
          const pJson = canonicalizeJsonString(pol);
          const pBuf = await globalThis.crypto.subtle.digest("SHA-256", new TextEncoder().encode(pJson));
          if (compareBytes(new Uint8Array(pBuf), policySha256Bytes) === 0) {
            foundInRegistry = true;
            break;
          }
        } catch {
          // ignore uncanonicalizable policy in registry
        }
      }
    }

    if (!foundInRegistry) {
      throw new CertError("ERR_CERT_UNKNOWN_POLICY", "Policy is unknown to issuer registry");
    }
  }

  // 3. Canonisation JCS et découplage absolu de la revendication (A5)
  let claimJson: string;
  try {
    claimJson = canonicalizeJsonString(claimInput);
  } catch {
    throw new CertError("ERR_CERT_CLAIM_NOT_CANONICAL", "claimInput could not be canonicalized");
  }

  const claimBytes = new TextEncoder().encode(claimJson);
  const claimSha256Buf = await globalThis.crypto.subtle.digest("SHA-256", claimBytes);
  const claimSha256 = new Uint8Array(claimSha256Buf);

  // Évaluation stricte sur JSON.parse(claimJson)
  const claimEvaluated = JSON.parse(claimJson);

  // 4. Détermination de la dérogation
  const isMemorial =
    claimEvaluated !== null &&
    typeof claimEvaluated === "object" &&
    !Array.isArray(claimEvaluated) &&
    claimEvaluated.destination !== null &&
    typeof claimEvaluated.destination === "object" &&
    claimEvaluated.destination.use === "memorial_forestry";

  const policyForEval =
    isMemorial && policyInput !== null && policyInput !== undefined
      ? JSON.parse(canonicalizeJsonString(policyInput))
      : null;

  // 5. Évaluation sanitaire par The Iron Gate
  const evalResult = evaluate(claimEvaluated, policyForEval);

  // RÈGLE D'OR : Aucun certificat pour une revendication rejetée !
  // Si le verdict n'est pas strictement AUTHORISED, signer n'est JAMAIS appelé.
  if (evalResult.verdict !== "AUTHORISED" || evalResult.signature_permitted !== true) {
    throw new CertError(
      "ERR_CERT_ISSUANCE_REFUSED",
      "Sanitary evaluation refused batch claim issuance",
      evalResult.reasons
    );
  }

  // 6. Construction de la charge utile CBOR canonique (clés entières 1 à 6)
  const mapEntries: [number, unknown][] = [
    [1, claimSha256],
    [2, "AUTHORISED"],
    [3, { $tag: 1, $value: context.issuedAt }],
    [4, TAXONOMY_SNAPSHOT_SHA256],
    [5, RULES_VERSION]
  ];

  // Règle d'unicité absolue de la clé 6 : présente ssi destination.use === "memorial_forestry"
  if (isMemorial) {
    if (!policySha256Bytes) {
      throw new CertError("ERR_CERT_DEROGATION_UNBOUND", "Policy SHA-256 missing for memorial forestry");
    }
    mapEntries.push([6, policySha256Bytes]);
  }

  const payloadBytes = encode({ $map: mapEntries });

  // 7. Scellage de l'enveloppe COSE_Sign1 (Tag 18)
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
