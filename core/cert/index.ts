/**
 * AeterniTrak V1.0 — Module Certificat de Conformité Sanitaire de Lot (Batch Certificate)
 * Conformité : AET-SPEC-CERT-001 v1.1.0, qa/vectors/README.md §4.14
 */

export { CertError, type CertErrorCode } from "./errors.ts";
export type {
  BatchSigner,
  BatchIssuanceContext,
  CertIssueResult,
  CertVerifyOptions,
  CertVerifyResult
} from "./types.ts";
export {
  RULES_VERSION,
  TAXONOMY_SNAPSHOT_SHA256,
  TAXONOMY_SNAPSHOT_HEX
} from "./constants.ts";
export { evaluateAndSign } from "./issue.ts";
export { certVerify } from "./verify.ts";
