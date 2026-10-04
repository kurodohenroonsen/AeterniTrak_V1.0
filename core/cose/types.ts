/**
 * AeterniTrak V1.0 — Modèle de Types et Structures COSE_Sign1
 * Conformité : RFC 9052, RFC 9053, RFC 9596 & Spécification AET-SPEC-CRYPTO-001 v1.1.0
 */

import type { CoseErrorCode } from "./errors.ts";

/**
 * Entrée certifiée dans le magasin de confiance local (Trust Store).
 */
export interface TrustedIssuerEntry {
  /** Identifiant SHA-256 tronqué à 16 octets de la clé publique brute */
  kid: string | Uint8Array;
  /** Identifiant IANA de l'algorithme cryptographique : -8 (Ed25519) ou -7 (ES256) */
  alg: number;
  /** Clé publique brute : 32 octets compressés pour Ed25519, 64 octets X||Y pour ES256 */
  public_key: string | Uint8Array;
  /** Rôle métier de l'émetteur */
  role?: string;
  /** Type de contenu COSE assigné (étiquette 16) */
  typ: string;
  /** Identifiant officiel de l'entité émettrice */
  issuer_id?: string;
  /** Début de la fenêtre de validité (timestamp UNIX en secondes) */
  valid_from?: number;
  /** Fin de la fenêtre de validité (timestamp UNIX en secondes) */
  valid_until?: number;
  /** Statut opérationnel : ACTIVE, RETIRED ou REVOKED (Règle K2) */
  status: "ACTIVE" | "RETIRED" | "REVOKED";
}

/**
 * Registre scellé d'émetteurs de confiance hors-ligne (Offline Trust Store).
 */
export interface TrustStore {
  /** Numéro de version monotone croissant du registre */
  version?: number;
  /** Date de publication scellée (timestamp UNIX en secondes) */
  updated_at?: number;
  /** Liste des signataires certifiés */
  signers: TrustedIssuerEntry[];
}

/**
 * Résultat d'une vérification COSE_Sign1 réussie.
 * La charge utile n'est restituée que sur ce canal scellé.
 */
export interface VerifySuccess {
  valid: true;
  payload: Uint8Array;
  payload_hex: string;
  kid: string;
}

export type VerifyResult = VerifySuccess;

/**
 * Résultat de l'opération applicative de consultation coseOpen (DEC-AET-07 Option B).
 */
export interface OpenVerified {
  status: "VERIFIED";
  valid: true;
  payload: Uint8Array;
  payload_hex: string;
  kid: string;
}

export interface OpenUnverified {
  status: "UNVERIFIED";
  valid: false;
  payload: Uint8Array;
  payload_hex: string;
  reason: "ERR_COSE_UNKNOWN_KID";
}

export interface OpenBlocked {
  status: "BLOCKED";
  valid: false;
  error: string;
}

export type OpenResult = OpenVerified | OpenUnverified | OpenBlocked;
