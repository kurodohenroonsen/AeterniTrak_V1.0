/**
 * AeterniTrak V1.0 — Registre Normatif des Exceptions et Erreurs COSE
 * Conformité : AET-SPEC-CRYPTO-001 v1.1.0 & qa/vectors/README.md §4.8
 */

export type CoseErrorCode =
  | "ERR_COSE_INVALID_ENVELOPE"
  | "ERR_COSE_UNSUPPORTED_ALGORITHM"
  | "ERR_COSE_TYPE_MISMATCH"
  | "ERR_COSE_MISSING_KID"
  | "ERR_COSE_INVALID_TRUST_STORE"
  | "ERR_COSE_UNKNOWN_KID"
  | "ERR_COSE_REVOKED_KEY"
  | "ERR_COSE_ALGORITHM_MISMATCH"
  | "ERR_COSE_KEY_USAGE_MISMATCH"
  | "ERR_COSE_INVALID_PUBLIC_KEY"
  | "ERR_COSE_MALLEABLE_SIGNATURE"
  | "ERR_COSE_INVALID_SIGNATURE"
  | "ERR_COSE_ISSUANCE_DATE_MISSING"
  | "ERR_COSE_EXPIRED_KEY"
  | "ERR_COSE_UNVERIFIED_PAYLOAD_ACCESS";

export class CoseError extends Error {
  public readonly code: CoseErrorCode;

  constructor(code: CoseErrorCode, message: string) {
    super(message);
    this.name = "CoseError";
    this.code = code;
    Object.setPrototypeOf(this, CoseError.prototype);
  }
}
