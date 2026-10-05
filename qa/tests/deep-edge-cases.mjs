#!/usr/bin/env node
/**
 * AeterniTrak V1.0 — Suite de Tests Unitaires Ultra-Poussée & Cas Limites Extrêmes (Deep Edge Cases)
 *
 * Couvre les cas limites mathématiques, cryptographiques et logiques les plus sévères :
 * - CBOR / JCS Corner Cases :
 *     * Clés de map UTF-8 multiniveaux (émojis 4 octets, tri lexicographique bytewise RFC 8949 vs UTF-16 RFC 8785)
 *     * Diacritiques combinés NFD rejetés au profit strict de NFC (RFC 8949 §4.2.1)
 *     * Entiers 64 bits aux limites (2^53 - 1, 2^53, 2^64 - 1, rejets d'overflow)
 *     * Rejets canoniques non-shortest (0, 23, 255, 65535, 4294967295)
 *     * Tableaux imbriqués à profondeur extrême & détection de récursion
 * - COSE / Crypto Boundary Conditions :
 *     * Rejet strict de signatures ASN.1/DER au profit du format brut r || s (BSI TR-03111 / SEC 1)
 *     * Signatures P-256 avec r = 0, s = 0, r >= n, s >= n, s > floor(n/2) (low-s anti-malléabilité)
 *     * Clés publiques P-256 hors courbe de Weierstrass (y^2 != x^3 - 3x + b mod p)
 *     * Point à l'infini (0, 0) et coordonnées non canoniques (x >= p ou y >= p)
 *     * Signatures Ed25519 avec composante scalaire non canonique S >= L (RFC 8032 §5.1.7)
 * - Algorithmes Métier Poussés :
 *     * Validation NISS belge (modulo 97, distinction naissances pré/post-2000 avec préfixe 2, clé 97)
 *     * Formule géodésique de Haversine (distance zéro, antipodes stricts, passage de l'antiméridien)
 *     * Résolution taxonomique récursive multi-niveaux (3 niveaux de sous-espèces arborescentes)
 *     * Dépistage spectrophotométrique LFA (courbes d'absorption limites, ratio C/T = 0.5 test douteux / quarantaine)
 */

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

import {
  encode as cborEncode,
  decodeStrict as cborDecodeStrict,
  decodeToCborValue,
  cborValueToAvn,
  CborError,
  compareBytes,
  bytesToHex,
  hexToBytes
} from "../../core/cbor/index.ts";

import {
  canonicalizeJson,
  canonicalizeJsonString,
  JcsError
} from "../../core/jcs/index.ts";

import {
  es256Verify,
  ed25519Verify,
  ed25519Sign,
  checkP256PublicKey,
  checkP256Signature,
  checkEd25519Signature,
  P256_P,
  P256_N,
  P256_HALF_N,
  P256_B,
  ED25519_L,
  CoseError
} from "../../core/cose/index.ts";

import {
  resolveTaxon,
  TAXONOMY_MAP
} from "../../validators/antiprion/index.ts";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, "../..");

// Couleurs ANSI
const GREEN = "\x1b[32m";
const RED = "\x1b[31m";
const YELLOW = "\x1b[33m";
const CYAN = "\x1b[36m";
const BOLD = "\x1b[1m";
const RESET = "\x1b[0m";

let totalAssertions = 0;
let totalPassed = 0;
let totalFailed = 0;
const failureDetails = [];

function assert(condition, testId, description) {
  totalAssertions++;
  if (condition) {
    totalPassed++;
    console.log(`  ${GREEN}PASS${RESET} [${testId}] ${description}`);
    return true;
  } else {
    totalFailed++;
    failureDetails.push({ testId, description });
    console.log(`  ${RED}FAIL${RESET} [${testId}] ${description}`);
    return false;
  }
}

function assertThrows(fn, expectedErrorCodeOrType, testId, description) {
  totalAssertions++;
  try {
    fn();
    totalFailed++;
    failureDetails.push({ testId, description: `${description} (Aucune exception levée)` });
    console.log(`  ${RED}FAIL${RESET} [${testId}] ${description} — Aucune exception levée`);
    return false;
  } catch (err) {
    const codeMatch =
      err.code === expectedErrorCodeOrType ||
      err.name === expectedErrorCodeOrType ||
      (typeof expectedErrorCodeOrType === "function" && err instanceof expectedErrorCodeOrType);

    if (codeMatch) {
      totalPassed++;
      console.log(`  ${GREEN}PASS${RESET} [${testId}] ${description} (Exception: ${err.code || err.name})`);
      return true;
    } else {
      totalFailed++;
      failureDetails.push({
        testId,
        description: `${description} (Exception reçue: ${err.code || err.name}, attendu: ${expectedErrorCodeOrType})`
      });
      console.log(`  ${RED}FAIL${RESET} [${testId}] ${description} — Exception inattendue: ${err.code || err.name}`);
      return false;
    }
  }
}

async function assertRejects(promiseFn, expectedErrorCodeOrType, testId, description) {
  totalAssertions++;
  try {
    await promiseFn();
    totalFailed++;
    failureDetails.push({ testId, description: `${description} (Aucun rejet de promesse)` });
    console.log(`  ${RED}FAIL${RESET} [${testId}] ${description} — Aucun rejet de promesse`);
    return false;
  } catch (err) {
    const codeMatch =
      err.code === expectedErrorCodeOrType ||
      err.name === expectedErrorCodeOrType ||
      (typeof expectedErrorCodeOrType === "function" && err instanceof expectedErrorCodeOrType);

    if (codeMatch) {
      totalPassed++;
      console.log(`  ${GREEN}PASS${RESET} [${testId}] ${description} (Rejet: ${err.code || err.name})`);
      return true;
    } else {
      totalFailed++;
      failureDetails.push({
        testId,
        description: `${description} (Rejet inattendu: ${err.code || err.name}, attendu: ${expectedErrorCodeOrType})`
      });
      console.log(`  ${RED}FAIL${RESET} [${testId}] ${description} — Rejet inattendu: ${err.code || err.name}`);
      return false;
    }
  }
}

console.log(`${BOLD}============================================================${RESET}`);
console.log(`${BOLD}AeterniTrak V1.0 — Suite Deep Edge Cases (Durcissement Extrême)${RESET}`);
console.log(`${BOLD}Cas Limites Mathématiques, Cryptographiques et Métier${RESET}`);
console.log(`${BOLD}============================================================${RESET}`);

// ============================================================================
// MODULE 1 : CBOR & JCS CORNER CASES
// ============================================================================
console.log(`\n${CYAN}--- SECTION 1 : CBOR / JCS Corner Cases ---${RESET}`);

// 1.1 UTF-8 multiniveaux (émojis 4 octets) et tri canonique
{
  const emojiStr = "🐈🐾🕊️⚡🛡️";
  const encoded = cborEncode(emojiStr);
  const decoded = cborDecodeStrict(encoded);
  assert(decoded === emojiStr, "CBOR-UTF8-001", "Aller-retour canonique CBOR sur chaîne à émojis UTF-8 4 octets");

  // Tri bytewise RFC 8949 vs UTF-16 RFC 8785
  // String A: \uFFFD (3 octets UTF-8: EF BF BD, UTF-16: FFFD)
  // String B: \u{1F600} (4 octets UTF-8: F0 9F 98 80, UTF-16: D83D DC00)
  // En UTF-16 (JCS RFC 8785) : B (D83D) < A (FFFD) -> B avant A
  // En UTF-8 bytewise (CBOR RFC 8949) : A (EF) < B (F0) -> A avant B
  const jcsResult = canonicalizeJsonString({ "\uFFFD": 1, "\u{1F600}": 2 });
  assert(
    jcsResult.indexOf('"\u{1F600}":2') < jcsResult.indexOf('"\uFFFD":1'),
    "JCS-SORT-001",
    "Tri JCS RFC 8785 par code units UTF-16 : surrogate pair emoji précède U+FFFD"
  );

  const cborMapObj = {
    $map: [
      ["\u{1F600}", 2],
      ["\uFFFD", 1]
    ]
  };
  const cborEncodedMap = cborEncode(cborMapObj);
  // Dans le flux CBOR encodé, la clé \uFFFD (EF BF BD) doit précéder \u{1F600} (F0 9F 98 80)
  const posA = bytesToHex(cborEncodedMap).indexOf("efbfbd");
  const posB = bytesToHex(cborEncodedMap).indexOf("f09f9880");
  assert(
    posA !== -1 && posB !== -1 && posA < posB,
    "CBOR-SORT-001",
    "Tri CBOR RFC 8949 par octets UTF-8 : clé 3 octets (EF..) précède clé 4 octets (F0..)"
  );
}

// 1.2 Diacritiques combinés NFD rejetés au profit de NFC
{
  const nfcString = "Café Réservé";
  const nfdString = "Cafe\u0301 Re\u0301serve\u0301"; // NFD décomposé avec U+0301

  // Encode NFC doit réussir
  const encodedNfc = cborEncode(nfcString);
  assert(cborDecodeStrict(encodedNfc) === nfcString, "CBOR-NFC-001", "Chaîne NFC acceptée et décode fidèlement");

  // Encode NFD doit être rejeté sans normalisation silencieuse
  assertThrows(
    () => cborEncode(nfdString),
    "ERR_CBOR_TEXT_NOT_NFC",
    "CBOR-NFD-001",
    "Rejet de chaîne NFD lors de l'encodage (ERR_CBOR_TEXT_NOT_NFC)"
  );

  // Encode NFD dans une clé de map doit être rejeté
  assertThrows(
    () => cborEncode({ [nfdString]: "valeur" }),
    "ERR_CBOR_TEXT_NOT_NFC",
    "CBOR-NFD-002",
    "Rejet d'une clé d'objet NFD lors de l'encodage (ERR_CBOR_TEXT_NOT_NFC)"
  );

  // Décodage strict d'un buffer injecté en NFD doit lever une erreur
  const nfdUtf8Bytes = new TextEncoder().encode(nfdString);
  const nfdCborBytes = new Uint8Array(1 + nfdUtf8Bytes.length);
  nfdCborBytes[0] = 0x60 | nfdUtf8Bytes.length; // major 3 (text), longueur directe
  nfdCborBytes.set(nfdUtf8Bytes, 1);

  assertThrows(
    () => cborDecodeStrict(nfdCborBytes),
    "ERR_CBOR_TEXT_NOT_NFC",
    "CBOR-NFD-003",
    "Décodage CBOR strict rejette le flux binaire contenant du texte NFD"
  );
}

// 1.3 Entiers 64 bits aux limites (2^53 - 1, 2^64 - 1, rejets d'overflow)
{
  // Limite JavaScript MAX_SAFE_INTEGER = 2^53 - 1 (9007199254740991)
  const maxSafe = 9007199254740991n;
  const encMaxSafe = cborEncode(maxSafe);
  assert(
    bytesToHex(encMaxSafe) === "1b001fffffffffffff",
    "CBOR-INT-001",
    "Encodage canonique de 2^53 - 1 en uint64 (info 27, 9 octets)"
  );
  assert(
    cborDecodeStrict(encMaxSafe) === Number(maxSafe),
    "CBOR-INT-002",
    "Décodage exact de 2^53 - 1 sous forme numérique sans altération de bit"
  );

  // Limite au-delà de MAX_SAFE_INTEGER = 2^53 (9007199254740992)
  const beyondSafe = 9007199254740992n;
  const encBeyondSafe = cborEncode(beyondSafe);
  const decBeyondSafe = cborDecodeStrict(encBeyondSafe);
  assert(
    typeof decBeyondSafe === "object" && decBeyondSafe.$int === "9007199254740992",
    "CBOR-INT-003",
    "Décodage de 2^53 en notation AVN ($int) pour préserver la précision 64 bits"
  );

  // Limite maximale uint64 = 2^64 - 1 (18446744073709551615)
  const maxUint64 = 18446744073709551615n;
  const encMaxUint64 = cborEncode(maxUint64);
  assert(
    bytesToHex(encMaxUint64) === "1bffffffffffffffff",
    "CBOR-INT-004",
    "Encodage de 2^64 - 1 en uint64 maximal (0x1B + 8 octets 0xFF)"
  );
  const decMaxUint64 = cborDecodeStrict(encMaxUint64);
  assert(
    decMaxUint64.$int === "18446744073709551615",
    "CBOR-INT-005",
    "Décodage de 2^64 - 1 préservé en AVN $int"
  );

  // Overflow au-delà de 2^64 - 1 (2^64 = 18446744073709551616)
  const overflowUint64 = 18446744073709551616n;
  assertThrows(
    () => cborEncode(overflowUint64),
    "ERR_CBOR_MALFORMED",
    "CBOR-INT-006",
    "Rejet de l'entier non-signé hors plage 64 bits 2^64 (ERR_CBOR_MALFORMED)"
  );

  // Entier négatif maximal 64 bits = -1 - (2^64 - 1) = -18446744073709551616
  const minNegInt64 = -18446744073709551616n;
  const encMinNeg = cborEncode(minNegInt64);
  assert(
    bytesToHex(encMinNeg) === "3bffffffffffffffff",
    "CBOR-INT-007",
    "Encodage canonique entier négatif 64 bits maximal (major 1, info 27, 0x3B...)"
  );
  const decMinNeg = cborDecodeStrict(encMinNeg);
  assert(
    decMinNeg.$int === "-18446744073709551616",
    "CBOR-INT-008",
    "Décodage exact de -2^64 en notation AVN $int"
  );

  // Rejet entier négatif en-deçà de -2^64
  assertThrows(
    () => cborEncode(-18446744073709551617n),
    "ERR_CBOR_MALFORMED",
    "CBOR-INT-009",
    "Rejet de l'entier négatif hors plage 64 bits (ERR_CBOR_MALFORMED)"
  );
}

// 1.4 Rejets canoniques non-shortest (RFC 8949 §4.2.1 (1))
{
  const nonShortestVectors = [
    { hex: "1800", expected: "ERR_CBOR_NOT_SHORTEST", label: "0 encodé en 2 octets (info 24)" },
    { hex: "190000", expected: "ERR_CBOR_NOT_SHORTEST", label: "0 encodé en 3 octets (info 25)" },
    { hex: "1a00000000", expected: "ERR_CBOR_NOT_SHORTEST", label: "0 encodé en 5 octets (info 26)" },
    { hex: "1b0000000000000000", expected: "ERR_CBOR_NOT_SHORTEST", label: "0 encodé en 9 octets (info 27)" },
    { hex: "1817", expected: "ERR_CBOR_NOT_SHORTEST", label: "23 encodé en 2 octets au lieu de valeur directe" },
    { hex: "190018", expected: "ERR_CBOR_NOT_SHORTEST", label: "24 encodé en 3 octets au lieu de 2 octets" },
    { hex: "1900ff", expected: "ERR_CBOR_NOT_SHORTEST", label: "255 encodé en 3 octets au lieu de 2 octets" },
    { hex: "1a00000100", expected: "ERR_CBOR_NOT_SHORTEST", label: "256 encodé en 5 octets au lieu de 3 octets" },
    { hex: "1a0000ffff", expected: "ERR_CBOR_NOT_SHORTEST", label: "65535 encodé en 5 octets au lieu de 3 octets" },
    { hex: "1b0000000000010000", expected: "ERR_CBOR_NOT_SHORTEST", label: "65536 encodé en 9 octets au lieu de 5 octets" },
    { hex: "1b00000000ffffffff", expected: "ERR_CBOR_NOT_SHORTEST", label: "4294967295 encodé en 9 octets au lieu de 5 octets" }
  ];

  nonShortestVectors.forEach((v, idx) => {
    const raw = hexToBytes(v.hex);
    assertThrows(
      () => cborDecodeStrict(raw),
      v.expected,
      `CBOR-CANON-${String(idx + 1).padStart(3, "0")}`,
      `Rejet non-shortest : ${v.label}`
    );
  });
}

// 1.5 Tableaux imbriqués à profondeur extrême (détection de récursion / stack overflow)
{
  // Test profondeur nominale supportée (300 niveaux)
  let nestedNominal = 42;
  for (let i = 0; i < 300; i++) {
    nestedNominal = [nestedNominal];
  }
  const encNominal = cborEncode(nestedNominal);
  const decNominal = cborDecodeStrict(encNominal);
  let depthNominal = 0;
  let cur = decNominal;
  while (Array.isArray(cur)) {
    depthNominal++;
    cur = cur[0];
  }
  assert(
    depthNominal === 300 && cur === 42,
    "CBOR-DEPTH-001",
    "Imbrication récursive nominale à 300 niveaux encodée et décodée avec intégrité"
  );

  // Test profondeur extrême : génère un flux binaire CBOR imbriquant 15 000 tableaux (0x81...)
  const extremeDepth = 15000;
  const extremeBytes = new Uint8Array(extremeDepth + 1);
  extremeBytes.fill(0x81, 0, extremeDepth); // 0x81 = array of 1 item
  extremeBytes[extremeDepth] = 0x00;        // innermost item = 0

  let caughtRecursionError = false;
  try {
    cborDecodeStrict(extremeBytes);
  } catch (err) {
    if (err instanceof RangeError || err.code === "ERR_CBOR_MAX_DEPTH") {
      caughtRecursionError = true;
    }
  }
  assert(
    caughtRecursionError,
    "CBOR-DEPTH-002",
    "Garde-fou récursion : profondeur extrême (15 000) interceptée sans crash incontrôlé (RangeError)"
  );
}

// ============================================================================
// MODULE 2 : COSE & CRYPTO BOUNDARY CONDITIONS
// ============================================================================
console.log(`\n${CYAN}--- SECTION 2 : COSE / Crypto Boundary Conditions ---${RESET}`);

// 2.1 Rejet strict de la signature ASN.1/DER (rejet au profit du format brut r || s)
{
  // Exemple de signature ECDSA ASN.1/DER valide (71 octets)
  // SEQUENCE (0x30, len=0x45)
  //   INTEGER r (0x02, len=0x20, ...)
  //   INTEGER s (0x02, len=0x21, 0x00, ...)
  const derSignature = hexToBytes(
    "304502207fffffffffffffffffffffffffffffff5d576e7357a4501ddfe92f46681b20a0" +
    "0221006b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296"
  );

  assert(derSignature.length === 71, "COSE-DER-001", "Signature de test au format ASN.1/DER (71 octets)");

  // checkP256Signature doit lever ERR_COSE_INVALID_SIGNATURE
  assertThrows(
    () => checkP256Signature(derSignature),
    "ERR_COSE_INVALID_SIGNATURE",
    "COSE-DER-002",
    "checkP256Signature rejette immédiatement le format ASN.1/DER (longueur != 64 octets)"
  );

  // Clé publique P-256 valide issue de RFC 6979 A.2.5
  const validP256PubKeyRef = hexToBytes(
    "60fed4ba255a9d31c961eb74c6356d68c049b8923b61fa6ce669622e60f29fb6" +
    "7903fe1008b8bc99a41ae9e95628bc64f2f1b20c2d7e9f5177a3c294d4462299"
  );
  const testMsg = new TextEncoder().encode("injection-tbs-payload");

  // Tentative d'injection directe de signature ASN.1/DER dans es256Verify
  await assertRejects(
    () => es256Verify(validP256PubKeyRef, testMsg, derSignature),
    "ERR_COSE_INVALID_SIGNATURE",
    "COSE-DER-003",
    "Tentative d'injection directe de signature ASN.1/DER dans es256Verify formellement rejetée"
  );
}

// 2.2 Signatures P-256 avec r = 0, s = 0, r >= n, s >= n
{
  const dummy64 = new Uint8Array(64);
  dummy64.fill(0x01); // Signature valide par défaut

  // r = 0
  const rZero = new Uint8Array(dummy64);
  rZero.fill(0x00, 0, 32);
  assertThrows(
    () => checkP256Signature(rZero),
    "ERR_COSE_INVALID_SIGNATURE",
    "COSE-SCAL-001",
    "Rejet signature P-256 avec scalaire r = 0"
  );

  // s = 0
  const sZero = new Uint8Array(dummy64);
  sZero.fill(0x00, 32, 64);
  assertThrows(
    () => checkP256Signature(sZero),
    "ERR_COSE_INVALID_SIGNATURE",
    "COSE-SCAL-002",
    "Rejet signature P-256 avec scalaire s = 0"
  );

  // r = n
  const rEqualN = new Uint8Array(dummy64);
  const nBytes = hexToBytes(P256_N.toString(16).padStart(64, "0"));
  rEqualN.set(nBytes, 0);
  assertThrows(
    () => checkP256Signature(rEqualN),
    "ERR_COSE_INVALID_SIGNATURE",
    "COSE-SCAL-003",
    "Rejet signature P-256 avec scalaire r = n (hors de [1, n-1])"
  );

  // r = n + 1
  const rAboveN = new Uint8Array(dummy64);
  const rAboveVal = hexToBytes((P256_N + 1n).toString(16).padStart(64, "0"));
  rAboveN.set(rAboveVal, 0);
  assertThrows(
    () => checkP256Signature(rAboveN),
    "ERR_COSE_INVALID_SIGNATURE",
    "COSE-SCAL-004",
    "Rejet signature P-256 avec scalaire r = n + 1"
  );

  // s = n
  const sEqualN = new Uint8Array(dummy64);
  sEqualN.set(nBytes, 32);
  assertThrows(
    () => checkP256Signature(sEqualN),
    "ERR_COSE_INVALID_SIGNATURE",
    "COSE-SCAL-005",
    "Rejet signature P-256 avec scalaire s = n"
  );

  // s = n + 1
  const sAboveN = new Uint8Array(dummy64);
  sAboveN.set(rAboveVal, 32);
  assertThrows(
    () => checkP256Signature(sAboveN),
    "ERR_COSE_INVALID_SIGNATURE",
    "COSE-SCAL-006",
    "Rejet signature P-256 avec scalaire s = n + 1"
  );

  // s = floor(n/2) (s bas valide aux bornes)
  const sHalfN = new Uint8Array(dummy64);
  const halfNBytes = hexToBytes(P256_HALF_N.toString(16).padStart(64, "0"));
  sHalfN.set(halfNBytes, 32);
  let halfNCheckPassed = false;
  try {
    checkP256Signature(sHalfN);
    halfNCheckPassed = true;
  } catch {
    halfNCheckPassed = false;
  }
  assert(
    halfNCheckPassed,
    "COSE-SCAL-007",
    "Validation du scalaire limite s = floor(n/2) (borne supérieure exacte du low-s)"
  );

  // s = floor(n/2) + 1 (premier s haut, rejet malléabilité BSI TR-03111)
  const sHighFirst = new Uint8Array(dummy64);
  const highFirstBytes = hexToBytes((P256_HALF_N + 1n).toString(16).padStart(64, "0"));
  sHighFirst.set(highFirstBytes, 32);
  assertThrows(
    () => checkP256Signature(sHighFirst),
    "ERR_COSE_MALLEABLE_SIGNATURE",
    "COSE-SCAL-008",
    "Rejet du premier s haut floor(n/2) + 1 pour malléabilité (ERR_COSE_MALLEABLE_SIGNATURE)"
  );
}

// 2.3 Clés publiques P-256 hors courbe (y^2 != x^3 - 3x + b mod p)
{
  // Clé publique P-256 valide issue de RFC 6979 A.2.5
  const validP256PubKey = hexToBytes(
    "60fed4ba255a9d31c961eb74c6356d68c049b8923b61fa6ce669622e60f29fb6" +
    "7903fe1008b8bc99a41ae9e95628bc64f2f1b20c2d7e9f5177a3c294d4462299"
  );

  let validKeyPass = false;
  try {
    checkP256PublicKey(validP256PubKey);
    validKeyPass = true;
  } catch {
    validKeyPass = false;
  }
  assert(validKeyPass, "COSE-CURVE-001", "Clé publique P-256 conforme sur la courbe de Weierstrass");

  // Clé altérée (dernier octet de Y inversé)
  const offCurveKey1 = new Uint8Array(validP256PubKey);
  offCurveKey1[63] ^= 0x01;
  assertThrows(
    () => checkP256PublicKey(offCurveKey1),
    "ERR_COSE_INVALID_PUBLIC_KEY",
    "COSE-CURVE-002",
    "Rejet de clé P-256 hors courbe (1 bit modifié sur l'ordonnée Y)"
  );

  // Coordonnées arbitraires dans F_p mais ne satisfaisant pas Weierstrass
  const arbitraryCoordinates = hexToBytes(
    "0000000000000000000000000000000000000000000000000000000000000002" +
    "0000000000000000000000000000000000000000000000000000000000000003"
  );
  assertThrows(
    () => checkP256PublicKey(arbitraryCoordinates),
    "ERR_COSE_INVALID_PUBLIC_KEY",
    "COSE-CURVE-003",
    "Rejet de coordonnées (2, 3) non situées sur la courbe NIST P-256"
  );
}

// 2.4 Point à l'infini et coordonnées non canoniques (x >= p ou y >= p)
{
  // Point à l'infini (0, 0)
  const pointAtInfinity = new Uint8Array(64); // 64 octets à 0
  assertThrows(
    () => checkP256PublicKey(pointAtInfinity),
    "ERR_COSE_INVALID_PUBLIC_KEY",
    "COSE-INF-001",
    "Rejet du point à l'infini (0, 0) non représentable en coordonnées affines"
  );

  // x = p
  const pBytes = hexToBytes(P256_P.toString(16).padStart(64, "0"));
  const xEqualP = hexToBytes(
    P256_P.toString(16).padStart(64, "0") +
    "7903fe1008b8bc99a41ae9e95628bc64f2f1b20c2d7e9f5177a3c294d4462299"
  );
  assertThrows(
    () => checkP256PublicKey(xEqualP),
    "ERR_COSE_INVALID_PUBLIC_KEY",
    "COSE-INF-002",
    "Rejet coordonnée x = p (hors du corps fini F_p)"
  );

  // x = p + 1
  const xAboveP = hexToBytes(
    (P256_P + 1n).toString(16).padStart(64, "0") +
    "7903fe1008b8bc99a41ae9e95628bc64f2f1b20c2d7e9f5177a3c294d4462299"
  );
  assertThrows(
    () => checkP256PublicKey(xAboveP),
    "ERR_COSE_INVALID_PUBLIC_KEY",
    "COSE-INF-003",
    "Rejet coordonnée x = p + 1"
  );

  // y = p
  const yEqualP = hexToBytes(
    "60fed4ba255a9d31c961eb74c6356d68c049b8923b61fa6ce669622e60f29fb6" +
    P256_P.toString(16).padStart(64, "0")
  );
  assertThrows(
    () => checkP256PublicKey(yEqualP),
    "ERR_COSE_INVALID_PUBLIC_KEY",
    "COSE-INF-004",
    "Rejet coordonnée y = p (hors du corps fini F_p)"
  );

  // y = 2^256 - 1
  const yMaxWord = hexToBytes(
    "60fed4ba255a9d31c961eb74c6356d68c049b8923b61fa6ce669622e60f29fb6" +
    "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
  );
  assertThrows(
    () => checkP256PublicKey(yMaxWord),
    "ERR_COSE_INVALID_PUBLIC_KEY",
    "COSE-INF-005",
    "Rejet coordonnée y = 2^256 - 1 (débordement de champ P-256)"
  );
}

// 2.5 Vecteurs Ed25519 avec composante S >= L (malléabilité RFC 8032 §5.1.7)
{
  const dummyEdSig = new Uint8Array(64);
  dummyEdSig.fill(0x02);

  // S = L exact (L = 2^252 + 27742317777372353535851937790883648493)
  // Ed25519 stocke S en little-endian sur les octets 32..64
  function writeBigIntLE32(val) {
    const buf = new Uint8Array(32);
    let cur = val;
    for (let i = 0; i < 32; i++) {
      buf[i] = Number(cur & 0xffn);
      cur >>= 8n;
    }
    return buf;
  }

  const sEqualL = new Uint8Array(dummyEdSig);
  sEqualL.set(writeBigIntLE32(ED25519_L), 32);
  assertThrows(
    () => checkEd25519Signature(sEqualL),
    "ERR_COSE_INVALID_SIGNATURE",
    "ED-MALL-001",
    "Rejet signature Ed25519 avec composante S = L (RFC 8032 §5.1.7)"
  );

  // S = L + 1
  const sAboveL = new Uint8Array(dummyEdSig);
  sAboveL.set(writeBigIntLE32(ED25519_L + 1n), 32);
  assertThrows(
    () => checkEd25519Signature(sAboveL),
    "ERR_COSE_INVALID_SIGNATURE",
    "ED-MALL-002",
    "Rejet signature Ed25519 avec composante S = L + 1"
  );

  // S = 2^255 - 19
  const sMaxField = new Uint8Array(dummyEdSig);
  sMaxField.set(writeBigIntLE32((1n << 255n) - 19n), 32);
  assertThrows(
    () => checkEd25519Signature(sMaxField),
    "ERR_COSE_INVALID_SIGNATURE",
    "ED-MALL-003",
    "Rejet signature Ed25519 avec S = 2^255 - 19 (non canonique)"
  );

  // S = L - 1 (scalaire maximal canonique accepté)
  const sCanonMax = new Uint8Array(dummyEdSig);
  sCanonMax.set(writeBigIntLE32(ED25519_L - 1n), 32);
  let sCanonPassed = false;
  try {
    checkEd25519Signature(sCanonMax);
    sCanonPassed = true;
  } catch {
    sCanonPassed = false;
  }
  assert(
    sCanonPassed,
    "ED-MALL-004",
    "Validation du scalaire Ed25519 limite canonique S = L - 1"
  );
}

// ============================================================================
// MODULE 3 : ALGORITHMES MÉTIER POUSSÉS
// ============================================================================
console.log(`\n${CYAN}--- SECTION 3 : Algorithmes Métier Poussés ---${RESET}`);

// 3.1 Validation NISS belge (modulo 97 avec naissances post-2000, préfixe 2)
class BelgianNissValidator {
  static validate(nissRaw) {
    if (typeof nissRaw !== "string") {
      return { valid: false, code: "ERR_INVALID_NISS_FORMAT", message: "Le NISS doit être une chaîne textuelle" };
    }
    const clean = nissRaw.replace(/[^0-9]/g, "");
    if (clean.length !== 11) {
      return { valid: false, code: "ERR_INVALID_NISS_LENGTH", message: "Le NISS doit comporter exactement 11 chiffres" };
    }

    const baseStr = clean.substring(0, 9);
    const checksumExpected = parseInt(clean.substring(9, 11), 10);
    const baseNum = BigInt(baseStr);

    // Cas A : Naissance avant 2000
    const remPre = baseNum % 97n;
    const calcPre = remPre === 0n ? 97 : Number(97n - remPre);
    if (calcPre === checksumExpected) {
      return { valid: true, era: "pre-2000", checksum: calcPre };
    }

    // Cas B : Naissance en ou après 2000 (préfixe 2 ajouté devant les 9 chiffres)
    const basePostNum = BigInt("2" + baseStr);
    const remPost = basePostNum % 97n;
    const calcPost = remPost === 0n ? 97 : Number(97n - remPost);
    if (calcPost === checksumExpected) {
      return { valid: true, era: "post-2000", checksum: calcPost };
    }

    return {
      valid: false,
      code: "ERR_INVALID_NISS_CHECKSUM",
      message: `Échec modulo 97 (fourni: ${checksumExpected}, calculé pre-2000: ${calcPre}, post-2000: ${calcPost})`
    };
  }
}

{
  // Test vecteur pré-2000 : 72.05.14-262.89 (720514262 % 97 = 8 -> 97 - 8 = 89)
  const vPre = BelgianNissValidator.validate("72.05.14-262.89");
  assert(
    vPre.valid && vPre.era === "pre-2000" && vPre.checksum === 89,
    "NISS-MOD97-001",
    "Validation nominale NISS pré-2000 (72.05.14-262.89, clé 89)"
  );

  // Test vecteur post-2000 : 04.05.12-123.53 (né en 2004, avec préfixe '2' : 2040512123 % 97 = 44 -> 97 - 44 = 53)
  const vPost = BelgianNissValidator.validate("04.05.12-123.53");
  assert(
    vPost.valid && vPost.era === "post-2000" && vPost.checksum === 53,
    "NISS-MOD97-002",
    "Validation nominale NISS post-2000 avec préfixe 2 (04.05.12-123.53, clé 53)"
  );

  // Vérification de la collision de siècle : sans le préfixe 2, le NISS post-2000 est rejeté
  const checkWithoutPrefix2 = Number(97n - (BigInt("040512123") % 97n));
  assert(
    checkWithoutPrefix2 === 24 && vPost.checksum !== checkWithoutPrefix2,
    "NISS-MOD97-003",
    "Démonstration que le calcul sans préfixe 2 donnerait 24 au lieu de 53 (rejet impératif)"
  );

  // Test cas limite reste = 0 -> clé = 97
  // Base 970000000 : 970000000 % 97 = 0 -> clé 97
  const vRem0 = BelgianNissValidator.validate("97.00.00-000.97");
  assert(
    vRem0.valid && vRem0.checksum === 97,
    "NISS-MOD97-004",
    "Cas limite modulo 97 : division exacte (reste 0) confère la clé 97"
  );

  // Détection d'altération (1 bit / chiffre modifié)
  const vCorrupted = BelgianNissValidator.validate("72.05.14-262.88");
  assert(
    !vCorrupted.valid && vCorrupted.code === "ERR_INVALID_NISS_CHECKSUM",
    "NISS-MOD97-005",
    "Rejet immédiat d'un NISS avec clé corrompue (ERR_INVALID_NISS_CHECKSUM)"
  );

  // Détection de transposition de 2 chiffres adjacents
  const vTransposed = BelgianNissValidator.validate("72.05.41-262.89");
  assert(
    !vTransposed.valid && vTransposed.code === "ERR_INVALID_NISS_CHECKSUM",
    "NISS-MOD97-006",
    "Rejet robuste sur transposition de chiffres d'état civil (14 -> 41)"
  );
}

// 3.2 Formule géodésique de Haversine (distance zéro, antipodes stricts, passage de l'antiméridien)
function haversineDistance(lat1, lon1, lat2, lon2, radius = 6371000) {
  const toRad = Math.PI / 180;
  const phi1 = lat1 * toRad;
  const phi2 = lat2 * toRad;
  const deltaPhi = (lat2 - lat1) * toRad;

  // Normalisation du delta de longitude pour shortest path sur la sphère [-pi, pi]
  let deltaLambda = (lon2 - lon1) * toRad;
  deltaLambda = ((deltaLambda + Math.PI) % (2 * Math.PI)) - Math.PI;

  const sinHalfPhi = Math.sin(deltaPhi / 2);
  const sinHalfLambda = Math.sin(deltaLambda / 2);

  const a = sinHalfPhi * sinHalfPhi + Math.cos(phi1) * Math.cos(phi2) * sinHalfLambda * sinHalfLambda;

  // Protection contre les micro-dépassements IEEE-754 (évite NaN sur racine carrée)
  const aClamped = Math.max(0, Math.min(1, a));
  const c = 2 * Math.atan2(Math.sqrt(aClamped), Math.sqrt(1 - aClamped));

  return radius * c;
}

{
  // 1. Distance zéro (même coordonnée géodésique)
  const distZero = haversineDistance(50.4182, 5.8821, 50.4182, 5.8821);
  assert(distZero === 0, "HAVERSINE-001", "Distance Haversine nulle entre points identiques");

  // 2. Sentier forestier DNF UC-325 (Parc cinéraire : ~174 mètres)
  const distTrail = haversineDistance(50.4170, 5.8805, 50.4182, 5.8821);
  assert(
    Math.abs(distTrail - 174.2) < 2.0,
    "HAVERSINE-002",
    `Vérification de distance locale sous canopée UC-325 : ${distTrail.toFixed(1)} m attendu ~174 m`
  );

  // 3. Antipodes stricts : distance = pi * R (~20 015 087 mètres)
  const distAntipodesEquator = haversineDistance(0, 0, 0, 180);
  const expectedHalfCircumference = Math.PI * 6371000;
  assert(
    Math.abs(distAntipodesEquator - expectedHalfCircumference) < 1.0,
    "HAVERSINE-003",
    `Antipodes stricts à l'équateur (0,0 -> 0,180) : ${Math.round(distAntipodesEquator)} m (pi * R)`
  );

  const distAntipodesPoles = haversineDistance(90, 0, -90, 0);
  assert(
    Math.abs(distAntipodesPoles - expectedHalfCircumference) < 1.0,
    "HAVERSINE-004",
    "Antipodes stricts Pôle Nord (90) vers Pôle Sud (-90) sans instabilité numérique NaN"
  );

  // 4. Passage de l'antiméridien (longitude +179.95 vers -179.95)
  // Distance directe = 0.1 degré le long de l'équateur = (0.1 * pi / 180) * 6371000 = ~11 119.5 mètres
  const distAntimeridian = haversineDistance(0, 179.95, 0, -179.95);
  const expectedShortDistance = ((0.1 * Math.PI) / 180) * 6371000;
  assert(
    Math.abs(distAntimeridian - expectedShortDistance) < 2.0,
    "HAVERSINE-005",
    `Passage de l'antiméridien résolu par le plus court chemin : ${Math.round(distAntimeridian)} m (vs ~40 000 km si non-normalisé)`
  );
}

// 3.3 Résolution taxonomique récursive sous-espèces multiples (3 niveaux d'arborescence)
{
  const customTaxonomyMap = new Map(TAXONOMY_MAP);

  // Échelon 0 : Espèce souche (Poulet / Gallus gallus = 9031)
  // Créons une lignée arborescente à 3 niveaux de sous-espèces :
  // Espèce souche : 500000 (species, group POULTRY, marker 8782)
  // Sous-espèce N1 : 500001 (subspecies, parent 500000, marker 51001)
  // Sous-espèce N2 : 500002 (subspecies, parent 500001, marker 51002)
  // Sous-espèce N3 : 500003 (subspecies, parent 500002, marker 51003)

  customTaxonomyMap.set(500000, {
    taxid: 500000,
    scientific_name: "Testus soucheus",
    rank: "species",
    group: "POULTRY",
    lineage_markers: [8782]
  });

  customTaxonomyMap.set(500001, {
    taxid: 500001,
    scientific_name: "Testus soucheus subsp1",
    rank: "subspecies",
    parent_taxid: 500000,
    group: "POULTRY",
    lineage_markers: [51001]
  });

  customTaxonomyMap.set(500002, {
    taxid: 500002,
    scientific_name: "Testus soucheus subsp2",
    rank: "subspecies",
    parent_taxid: 500001,
    group: "POULTRY",
    lineage_markers: [51002]
  });

  customTaxonomyMap.set(500003, {
    taxid: 500003,
    scientific_name: "Testus soucheus subsp3",
    rank: "subspecies",
    parent_taxid: 500002,
    group: "POULTRY",
    lineage_markers: [51003]
  });

  // Résolution de la sous-espèce de niveau 3 vers l'espèce souche
  const resN3 = resolveTaxon(500003, customTaxonomyMap);
  assert(
    resN3.success && resN3.taxon.species_taxid === 500000,
    "TAXON-TREE-001",
    "Résolution récursive 3 niveaux : taxid 500003 rattaché à l'espèce souche 500000"
  );
  assert(
    resN3.taxon.group === "POULTRY",
    "TAXON-TREE-002",
    "Préservation du groupe taxonomique 'POULTRY' à travers l'arborescence"
  );
  assert(
    resN3.taxon.lineage_markers.includes(8782) &&
    resN3.taxon.lineage_markers.includes(51001) &&
    resN3.taxon.lineage_markers.includes(51002) &&
    resN3.taxon.lineage_markers.includes(51003),
    "TAXON-TREE-003",
    "Accumulation complète des marqueurs de lignée des 3 niveaux de sous-espèces"
  );

  // Rejet rang supérieur à l'espèce (famille / ordre)
  customTaxonomyMap.set(500099, {
    taxid: 500099,
    scientific_name: "Testus ordus",
    rank: "order",
    group: "POULTRY",
    lineage_markers: []
  });
  const resOrder = resolveTaxon(500099, customTaxonomyMap);
  assert(
    !resOrder.success && resOrder.error === "TAXON_RANK_ABOVE_SPECIES",
    "TAXON-TREE-004",
    "Rejet strict des rangs supérieurs à l'espèce (TAXON_RANK_ABOVE_SPECIES)"
  );
}

// 3.4 Dépistage spectrophotométrique LFA (courbes d'absorption limites, ratio C/T = 0.5 test douteux)
function evaluateLfaSpectrophotometry(odControl, odTest, options = {}) {
  const minControlOD = options.minControlOD || 150; // Seuil minimal bandelette valide (mAU)
  const posRatioCutoff = options.posRatioCutoff || 0.15; // Ratio T/C <= 0.15 = Positif Pentobarbital (inhibition complète)
  const negRatioCutoff = options.negRatioCutoff || 0.80; // Ratio T/C >= 0.80 = Négatif Pentobarbital (absence produit)

  // 1. Contrôle d'intégrité de la bandelette : la ligne C doit être présente et nette
  if (typeof odControl !== "number" || odControl < minControlOD) {
    return {
      verdict: "INVALID",
      status: "REJET_TECHNIQUE",
      code: "ERR_LFA_INVALID_CONTROL_LINE",
      message: `Bandelette LFA invalide : Ligne de contrôle C insuffisante (${odControl} mAU < ${minControlOD} mAU)`,
      remediation: "Recommencer avec une nouvelle cassette LFA et un nouvel écouvillon"
    };
  }

  // 2. Calcul du ratio d'absorption T/C (Test / Contrôle)
  const ratioTC = odTest / odControl;
  const ratioCT = odTest > 0 ? odControl / odTest : Infinity;

  // 3. Interprétation du test compétitif barbituriques
  if (ratioTC <= posRatioCutoff) {
    return {
      verdict: "POSITIVE",
      status: "REJET_SANITAIRE",
      code: "REJ_PENTOBARBITAL_POSITIVE",
      ratioTC,
      ratioCT,
      message: `Pentobarbital détecté : ligne T fortement inhibée (T/C = ${ratioTC.toFixed(2)})`,
      remediation: "Rejet immédiat de la dépouille vers l'incinération Catégorie 1 (aucun recyclage possible)"
    };
  }

  if (ratioTC >= negRatioCutoff) {
    return {
      verdict: "NEGATIVE",
      status: "CONFORME",
      code: "OK_PENTOBARBITAL_ABSENT",
      ratioTC,
      ratioCT,
      message: `Pentobarbital non détecté : lignes C et T visibles (T/C = ${ratioTC.toFixed(2)})`,
      remediation: "Admission validée pour pasteurisation 70°C 1h et destination mémorielle forestière"
    };
  }

  // 4. Zone intermédiaire douteuse (0.15 < T/C < 0.80, incluant ratio limite C/T = 0.5 ou T/C = 0.5)
  return {
    verdict: "DOUBTFUL",
    status: "QUARANTAINE",
    code: "WARN_LFA_DOUBTFUL_RATIO",
    ratioTC,
    ratioCT,
    message: `Test LFA douteux : signal optique intermédiaire (T/C = ${ratioTC.toFixed(2)}, C/T = ${ratioCT.toFixed(2)})`,
    remediation: "Mise en quarantaine immédiate de la dépouille et analyse confirmative HPLC-MS/MS (UC-417 & UC-423)"
  };
}

{
  // Ligne C défaillante (< 150 mAU) -> Invalide
  const resBadControl = evaluateLfaSpectrophotometry(80, 50);
  assert(
    resBadControl.verdict === "INVALID" && resBadControl.code === "ERR_LFA_INVALID_CONTROL_LINE",
    "LFA-SPECTRO-001",
    "Détection d'absence de ligne C valide (test technique non conforme)"
  );

  // Négatif franc (Pentobarbital absent, lignes C et T franches, T/C = 0.90)
  const resNeg = evaluateLfaSpectrophotometry(500, 450);
  assert(
    resNeg.verdict === "NEGATIVE" && resNeg.status === "CONFORME",
    "LFA-SPECTRO-002",
    "Dépistage négatif franc : T/C = 0.90 conforme pour valorisation mémorielle"
  );

  // Positif franc (Pentobarbital présent, ligne T absente, T/C = 0.04)
  const resPos = evaluateLfaSpectrophotometry(500, 20);
  assert(
    resPos.verdict === "POSITIVE" && resPos.code === "REJ_PENTOBARBITAL_POSITIVE",
    "LFA-SPECTRO-003",
    "Dépistage positif franc : T/C = 0.04 aiguillage direct vers incinération C1"
  );

  // Cas Limite Critique : Ratio C/T = 0.5 (T/C = 0.50, odControl=400, odTest=200)
  // Ligne T partiellement atténuée (concentration au seuil limite)
  const resDoubtful = evaluateLfaSpectrophotometry(400, 200);
  assert(
    resDoubtful.verdict === "DOUBTFUL" &&
    resDoubtful.code === "WARN_LFA_DOUBTFUL_RATIO" &&
    resDoubtful.status === "QUARANTAINE",
    "LFA-SPECTRO-004",
    "Cas limite ratio T/C = 0.50 (C/T = 2.0) classé DOUBTFUL avec mise en quarantaine obligatoire"
  );

  // Cas limite borne basse : T/C = 0.20
  const resLowDoubt = evaluateLfaSpectrophotometry(500, 100);
  assert(
    resLowDoubt.verdict === "DOUBTFUL" && resLowDoubt.status === "QUARANTAINE",
    "LFA-SPECTRO-005",
    "Seuil suspect T/C = 0.20 sécurisé par protocole de remédiation et contre-expertise"
  );
}

// ============================================================================
// BILAN ET SYNTHÈSE DES TESTS
// ============================================================================
console.log(`\n${BOLD}============================================================${RESET}`);
console.log(
  `RÉSULTAT TOTAL : ${totalPassed} PASS, ${totalFailed} FAIL (Total : ${totalAssertions} assertions)`
);
console.log(`${BOLD}============================================================${RESET}`);

if (totalFailed > 0) {
  console.error(`\n${RED}Échecs détectés (${totalFailed}) :${RESET}`);
  failureDetails.forEach(f => console.error(`  - [${f.testId}] ${f.description}`));
  process.exit(1);
} else {
  console.log(`\n${GREEN}✓ SUCCÈS TOTAL : 100% des cas limites extrêmes validés avec rigueur mathématique !${RESET}`);
  process.exit(0);
}
