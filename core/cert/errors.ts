/**
 * AeterniTrak V1.0 — Registre d'Erreurs du Certificat de Lot (Batch Certificate)
 * Conformité : AET-SPEC-CERT-001 v1.1.0 §4.3.2, qa/vectors/README.md §4.14
 */

export type CertErrorCode =
  | "ERR_CERT_INVALID_ISSUED_AT"
  | "ERR_CERT_UNKNOWN_POLICY"
  | "ERR_CERT_ISSUANCE_REFUSED"
  | "ERR_CERT_INVALID_FIELD"
  | "ERR_CERT_UNAUTHORIZED_PAYLOAD_KEY"
  | "ERR_CERT_MISSING_MANDATORY_FIELD"
  | "ERR_CERT_VERDICT_NOT_AUTHORISED"
  | "ERR_CERT_CLAIM_NOT_CANONICAL"
  | "ERR_CERT_CLAIM_HASH_MISMATCH"
  | "ERR_CERT_UNKNOWN_TAXONOMY_SNAPSHOT"
  | "ERR_CERT_UNKNOWN_RULES_VERSION"
  | "ERR_CERT_RULES_VERSION_RETIRED"
  | "ERR_CERT_UNEXPECTED_POLICY"
  | "ERR_CERT_DEROGATION_UNBOUND"
  | "ERR_CERT_RE_EVALUATION_FAILED";

export class CertError extends Error {
  readonly code: CertErrorCode;
  readonly refusal_reasons?: string[];

  constructor(code: CertErrorCode, message: string, refusal_reasons?: string[]) {
    super(message);
    this.name = "CertError";
    this.code = code;
    if (refusal_reasons !== undefined) {
      this.refusal_reasons = refusal_reasons;
    }
    Object.setPrototypeOf(this, CertError.prototype);
  }
}

