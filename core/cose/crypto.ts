/**
 * AeterniTrak V1.0 — Primitives Cryptographiques & Vérifications Mathématiques Strictes
 * Algorithmes : Ed25519 (alg: -8, RFC 8032) & ES256 (alg: -7, NIST P-256 / FIPS 186-5)
 * Conformité : RFC 9053, BSI TR-03111, SEC 1 v2.0, AET-SPEC-CRYPTO-001 v1.1.0
 */

import crypto from "node:crypto";
import { CoseError } from "./errors.ts";
import { bytesToHex, hexToBytes } from "../cbor/writer.ts";

// ============================================================================
// Constantes Mathématiques P-256 (FIPS 186-5 & SEC 1 v2.0)
// ============================================================================
export const P256_P = (1n << 256n) - (1n << 224n) + (1n << 192n) + (1n << 96n) - 1n;
export const P256_N = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551n;
/** Demi-ordre de la courbe P-256 calculé par décalage binaire exact (Règle K1) */
export const P256_HALF_N = P256_N >> 1n;
export const P256_B = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604bn;

// ============================================================================
// Constantes Mathématiques Ed25519 (RFC 8032 §5.1)
// ============================================================================
export const ED25519_L = (1n << 252n) + 27742317777372353535851937790883648493n;

// Préfixe standard PKCS#8 ASN.1 pour Ed25519 (RFC 8410 v1, 16 octets)
const ED25519_PKCS8_PREFIX = new Uint8Array([
  0x30, 0x2e, 0x02, 0x01, 0x00, 0x30, 0x05, 0x06, 0x03, 0x2b, 0x65, 0x70, 0x04, 0x22, 0x04, 0x20
]);

/**
 * Calcule l'opération modulo positif pour BigInt.
 */
function mod(a: bigint, m: bigint): bigint {
  const r = a % m;
  return r >= 0n ? r : r + m;
}

/**
 * Lit un entier BigInt non-signé 256 bits encodé en little-endian.
 */
function readUint256LE(buf: Uint8Array): bigint {
  let res = 0n;
  for (let i = 31; i >= 0; i--) {
    res = (res << 8n) | BigInt(buf[i]);
  }
  return res;
}

/**
 * Lit un entier BigInt non-signé 256 bits encodé en big-endian.
 */
function readUint256BE(buf: Uint8Array): bigint {
  let res = 0n;
  for (let i = 0; i < 32; i++) {
    res = (res << 8n) | BigInt(buf[i]);
  }
  return res;
}

/**
 * Calcule l'identifiant de clé `kid` normalisé : les 16 premiers octets du SHA-256 de la clé brute.
 *
 * @param publicKey - Octets bruts de la clé publique (32 octets pour Ed25519, 64 octets pour ES256).
 * @returns Uint8Array de 16 octets.
 */
export function kid(publicKey: Uint8Array): Uint8Array {
  const hash = crypto.createHash("sha256").update(publicKey).digest();
  return new Uint8Array(hash.buffer, hash.byteOffset, 16);
}

/**
 * Valide les coordonnées affines et l'appartenance à la courbe P-256 (SEC 1 §3.2.2.1).
 *
 * @param publicKey - Concaténation de 64 octets des coordonnées X || Y.
 * @throws {CoseError} "ERR_COSE_INVALID_PUBLIC_KEY" si le point est invalide ou hors courbe.
 */
export function checkP256PublicKey(publicKey: Uint8Array): void {
  if (!(publicKey instanceof Uint8Array) || publicKey.length !== 64) {
    throw new CoseError("ERR_COSE_INVALID_PUBLIC_KEY", "P-256 public key must be exactly 64 bytes (X || Y)");
  }

  const x = readUint256BE(publicKey.subarray(0, 32));
  const y = readUint256BE(publicKey.subarray(32, 64));

  // Point à l'infini ou hors du corps F_p
  if (x >= P256_P || y >= P256_P || (x === 0n && y === 0n)) {
    throw new CoseError("ERR_COSE_INVALID_PUBLIC_KEY", "P-256 public key coordinates are out of field range or point at infinity");
  }

  // Équation de Weierstrass : y^2 ≡ x^3 - 3x + b (mod p)
  const lhs = mod(y * y, P256_P);
  const rhs = mod(x * x * x - 3n * x + P256_B, P256_P);

  if (lhs !== rhs) {
    throw new CoseError("ERR_COSE_INVALID_PUBLIC_KEY", "P-256 public key does not satisfy curve equation y^2 = x^3 - 3x + b (mod p)");
  }
}

/**
 * Valide les composantes r et s d'une signature ECDSA P-256 (low-s anti-malléabilité, BSI TR-03111).
 *
 * @param signature - Signature brute IEEE P1363 de 64 octets (r || s).
 * @throws {CoseError} "ERR_COSE_INVALID_SIGNATURE" ou "ERR_COSE_MALLEABLE_SIGNATURE".
 */
export function checkP256Signature(signature: Uint8Array): void {
  if (!(signature instanceof Uint8Array) || signature.length !== 64) {
    throw new CoseError("ERR_COSE_INVALID_SIGNATURE", "P-256 signature must be exactly 64 bytes (r || s)");
  }

  const r = readUint256BE(signature.subarray(0, 32));
  const s = readUint256BE(signature.subarray(32, 64));

  if (r < 1n || r >= P256_N || s < 1n || s >= P256_N) {
    throw new CoseError("ERR_COSE_INVALID_SIGNATURE", "ECDSA signature scalars r and s must be in range [1, n-1]");
  }

  // Règle du s bas (Low-s requirement)
  if (s > P256_HALF_N) {
    throw new CoseError("ERR_COSE_MALLEABLE_SIGNATURE", "Malleable ECDSA signature rejected: s exceeds floor(n/2)");
  }
}

/**
 * Valide le scalaire S d'une signature Ed25519 (RFC 8032 §5.1.7).
 *
 * @param signature - Signature brute de 64 octets (R || S).
 * @throws {CoseError} "ERR_COSE_INVALID_SIGNATURE" si la taille ou la canonicité est violée.
 */
export function checkEd25519Signature(signature: Uint8Array): void {
  if (!(signature instanceof Uint8Array) || signature.length !== 64) {
    throw new CoseError("ERR_COSE_INVALID_SIGNATURE", "Ed25519 signature must be exactly 64 bytes (R || S)");
  }

  const s = readUint256LE(signature.subarray(32, 64));
  if (s >= ED25519_L) {
    throw new CoseError("ERR_COSE_INVALID_SIGNATURE", "Non-canonical Ed25519 scalar S >= L rejected (RFC 8032 §5.1.7)");
  }
}

/**
 * Signe un message avec l'algorithme Ed25519 via la graine secrète de 32 octets.
 *
 * @param seed - Graine secrète de 32 octets (RFC 8032).
 * @param message - Octets du message à signer (généralement la structure Sig_structure).
 * @returns Paire { publicKey, signature } au format binaire brut.
 */
export async function ed25519Sign(
  seed: Uint8Array,
  message: Uint8Array
): Promise<{ publicKey: Uint8Array; signature: Uint8Array }> {
  if (!(seed instanceof Uint8Array) || seed.length !== 32) {
    throw new Error("Ed25519 seed must be exactly 32 bytes");
  }

  const pkcs8 = new Uint8Array(ED25519_PKCS8_PREFIX.length + seed.length);
  pkcs8.set(ED25519_PKCS8_PREFIX, 0);
  pkcs8.set(seed, ED25519_PKCS8_PREFIX.length);

  const privKey = await crypto.subtle.importKey(
    "pkcs8",
    pkcs8,
    { name: "Ed25519" },
    true,
    ["sign"]
  );

  const jwk = await crypto.subtle.exportKey("jwk", privKey);
  if (!jwk.x) {
    throw new Error("Failed to derive Ed25519 public key from private key JWK");
  }
  const publicKey = Buffer.from(jwk.x, "base64url");

  const sigBuffer = await crypto.subtle.sign({ name: "Ed25519" }, privKey, message);
  const signature = new Uint8Array(sigBuffer);

  return { publicKey: new Uint8Array(publicKey), signature };
}

/**
 * Vérifie une signature Ed25519 (alg: -8) conformément à la RFC 8032 et WebCrypto.
 *
 * @param publicKey - Clé publique brute de 32 octets.
 * @param message - Message signé (TBS).
 * @param signature - Signature brute de 64 octets.
 * @returns true si la signature est valide.
 * @throws {CoseError} "ERR_COSE_INVALID_SIGNATURE" si la vérification échoue.
 */
export async function ed25519Verify(
  publicKey: Uint8Array,
  message: Uint8Array,
  signature: Uint8Array
): Promise<boolean> {
  if (!(publicKey instanceof Uint8Array) || publicKey.length !== 32) {
    throw new CoseError("ERR_COSE_INVALID_SIGNATURE", "Ed25519 public key must be exactly 32 bytes");
  }

  checkEd25519Signature(signature);

  let pubCryptoKey: CryptoKey;
  try {
    pubCryptoKey = await crypto.subtle.importKey(
      "raw",
      publicKey,
      { name: "Ed25519" },
      true,
      ["verify"]
    );
  } catch (err) {
    throw new CoseError("ERR_COSE_INVALID_SIGNATURE", `Failed to import Ed25519 public key: ${(err as Error).message}`);
  }

  let ok = false;
  try {
    ok = await crypto.subtle.verify(
      { name: "Ed25519" },
      pubCryptoKey,
      signature,
      message
    );
  } catch (err) {
    throw new CoseError("ERR_COSE_INVALID_SIGNATURE", `Ed25519 verification error: ${(err as Error).message}`);
  }

  if (!ok) {
    throw new CoseError("ERR_COSE_INVALID_SIGNATURE", "Ed25519 mathematical verification failed");
  }

  return true;
}

/**
 * Vérifie une signature ECDSA P-256 (alg: -7) avec contrôle manuel low-s et validation sur courbe.
 *
 * @param publicKey - Clé publique brute de 64 octets (coordonnées affines X || Y).
 * @param message - Message signé (TBS).
 * @param signature - Signature brute IEEE P1363 de 64 octets (r || s).
 * @returns true si la signature est valide.
 * @throws {CoseError}
 */
export async function es256Verify(
  publicKey: Uint8Array,
  message: Uint8Array,
  signature: Uint8Array
): Promise<boolean> {
  // 1. Validation de la clé publique sur la courbe P-256
  checkP256PublicKey(publicKey);

  // 2. Validation de la signature et règle du s bas
  checkP256Signature(signature);

  // 3. Import WebCrypto au format SEC1 uncompressé (0x04 || X || Y sur 65 octets)
  const uncompressed = new Uint8Array(65);
  uncompressed[0] = 0x04;
  uncompressed.set(publicKey, 1);

  let pubCryptoKey: CryptoKey;
  try {
    pubCryptoKey = await crypto.subtle.importKey(
      "raw",
      uncompressed,
      { name: "ECDSA", namedCurve: "P-256" },
      true,
      ["verify"]
    );
  } catch (err) {
    throw new CoseError("ERR_COSE_INVALID_PUBLIC_KEY", `Failed to import P-256 key: ${(err as Error).message}`);
  }

  let ok = false;
  try {
    ok = await crypto.subtle.verify(
      { name: "ECDSA", hash: { name: "SHA-256" } },
      pubCryptoKey,
      signature,
      message
    );
  } catch (err) {
    throw new CoseError("ERR_COSE_INVALID_SIGNATURE", `ES256 verification error: ${(err as Error).message}`);
  }

  if (!ok) {
    throw new CoseError("ERR_COSE_INVALID_SIGNATURE", "ES256 mathematical verification failed");
  }

  return true;
}
