/**
 * AeterniCore COSE_Sign1 Module
 * Conformité : RFC 9052, RFC 9053, RFC 8032, RFC 9596, FIPS 186-5, BSI TR-03111, SEC 1 v2.0
 */

export { CoseError } from "./errors.ts";
export type { CoseErrorCode } from "./errors.ts";

export type {
  TrustStore,
  TrustedIssuerEntry,
  VerifyResult,
  VerifySuccess,
  OpenResult,
  OpenVerified,
  OpenUnverified,
  OpenBlocked
} from "./types.ts";

export {
  kid,
  ed25519Sign,
  ed25519Verify,
  es256Verify,
  checkP256PublicKey,
  checkP256Signature,
  checkEd25519Signature,
  P256_P,
  P256_N,
  P256_HALF_N,
  P256_B,
  ED25519_L
} from "./crypto.ts";

export {
  protectedHeader,
  sigStructure,
  coseSign,
  coseVerify,
  extractBytes,
  normalizeBytes
} from "./envelope.ts";

export {
  coseOpen
} from "./open.ts";
