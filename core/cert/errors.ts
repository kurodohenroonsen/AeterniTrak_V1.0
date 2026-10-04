/**
 * AeterniTrak V1.0 — Registre d'Erreurs du Certificat de Lot (Batch Certificate)
 * Conformité : AET-SPEC-CERT-001 v1.1.0 §4.3.2, qa/vectors/README.md §4.14
 */

export class CertError extends Error {
  readonly code: string;
  readonly refusal_reasons?: string[];

  constructor(code: string, message: string, refusal_reasons?: string[]) {
    super(message);
    this.name = "CertError";
    this.code = code;
    if (refusal_reasons !== undefined) {
      this.refusal_reasons = refusal_reasons;
    }
  }
}
