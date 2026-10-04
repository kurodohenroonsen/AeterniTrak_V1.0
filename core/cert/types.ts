/**
 * AeterniTrak V1.0 — Types & Interfaces du Certificat de Lot
 * Conformité : AET-SPEC-CERT-001 v1.1.0 §4.1.2, qa/vectors/README.md §4.14
 */

import type { TrustStore } from "../cose/types.ts";

/**
 * Interface d'abstraction matérielle de signature de certificat de lot.
 * Aucune clé privée ni graine ne réside dans le tas mémoire applicatif (A10).
 */
export interface BatchSigner {
  /** Algorithme cryptographique matériel : -7 (ES256) ou -8 (Ed25519) */
  readonly algorithm: -7 | -8;
  /** Identifiant SHA-256 tronqué à 16 octets de la clé publique de l'autorité */
  readonly kid: Uint8Array;
  /**
   * Appose la signature cryptographique sur la structure canonique Sig_structure (TBS).
   * @param tbs - Octets CBOR stricts de Sig_structure.
   * @returns Signature brute de 64 octets (IEEE P1363 pour ES256, RFC 8032 pour Ed25519).
   */
  sign(tbs: Uint8Array): Promise<Uint8Array>;
}

/**
 * Contexte d'émission d'un certificat de conformité sanitaire.
 */
export interface BatchIssuanceContext {
  signer: BatchSigner;
  issuedAt: unknown;
  policies?: unknown[];
}

/**
 * Résultat de l'émission d'un certificat de conformité.
 */
export interface CertIssueResult {
  envelope: Uint8Array;
  claimJson: string;
}

/**
 * Options de vérification d'un certificat de conformité sanitaire.
 */
export interface CertVerifyOptions {
  policies?: unknown[];
  retiredRulesVersions?: string[];
}

/**
 * Résultat de la vérification de conformité sanitaire.
 */
export interface CertVerifyResult {
  valid: true;
  kid: string;
  issued_at: number;
  rules_version: string;
  derogation: boolean;
}

export type { TrustStore };
