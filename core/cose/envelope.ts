/**
 * AeterniTrak V1.0 — Enveloppe COSE_Sign1 & Moteur de Vérification Formelle
 * Conformité : RFC 9052 §4.2-§4.4, RFC 9053, RFC 9596, AET-SPEC-CRYPTO-001 v1.1.0
 */

import { encode, decodeStrict } from "../cbor/index.ts";
import { bytesToHex, hexToBytes, compareBytes } from "../cbor/writer.ts";
import { CoseError } from "./errors.ts";
import type { TrustStore, TrustedIssuerEntry, VerifyResult } from "./types.ts";
import { kid, ed25519Sign, ed25519Verify, es256Verify } from "./crypto.ts";

/**
 * Extrait un Uint8Array à partir d'un élément décodé par AeterniCore (Uint8Array ou {$bytes: hex}).
 */
export function extractBytes(item: unknown): Uint8Array | null {
  if (item instanceof Uint8Array) {
    return item;
  }
  if (item !== null && typeof item === "object" && typeof (item as Record<string, unknown>).$bytes === "string") {
    return hexToBytes((item as Record<string, unknown>).$bytes as string);
  }
  return null;
}

/**
 * Normalise une clé publique ou un kid en Uint8Array (gère les entrées hexadécimales ou Uint8Array).
 */
export function normalizeBytes(val: string | Uint8Array): Uint8Array {
  if (typeof val === "string") {
    return hexToBytes(val);
  }
  return val;
}

/**
 * Génère l'en-tête protégé sérialisé de manière déterministe {1: alg, 16: typ}.
 *
 * @param alg - Algorithme (-8 pour Ed25519, -7 pour ES256).
 * @param typ - Type de contenu (étiquette 16, RFC 9596).
 * @returns Uint8Array contenant les octets CBOR déterministes de la carte d'en-tête.
 */
export function protectedHeader(alg: number, typ: string): Uint8Array {
  return encode({
    $map: [
      [1, alg],
      [16, typ]
    ]
  });
}

/**
 * Construit la structure canonique à signer Sig_structure (RFC 9052 §4.4).
 * Sig_structure = ["Signature1", protectedBytes, h'', payload]
 *
 * @param protectedBytes - Octets bruts de l'en-tête protégé.
 * @param payload - Octets bruts de la charge utile.
 * @returns Uint8Array contenant l'encodage CBOR strict de Sig_structure (TBS).
 */
export function sigStructure(protectedBytes: Uint8Array, payload: Uint8Array): Uint8Array {
  return encode([
    "Signature1",
    protectedBytes,
    new Uint8Array(0),
    payload
  ]);
}

/**
 * Signe une charge utile sous enveloppe COSE_Sign1 (Ed25519 seul, pour tests et filière logicielle).
 *
 * @param seed - Graine secrète de 32 octets.
 * @param typ - Identifiant de type (étiquette 16).
 * @param payload - Octets bruts de la charge utile attachée.
 * @returns Enveloppe complète balisée par Tag 18 (0xd2).
 */
export async function coseSign(
  seed: Uint8Array,
  typ: string,
  payload: Uint8Array
): Promise<Uint8Array> {
  const protectedBytes = protectedHeader(-8, typ);
  const tbs = sigStructure(protectedBytes, payload);

  const { publicKey, signature } = await ed25519Sign(seed, tbs);
  const signerKid = await kid(publicKey);

  const unprotected = {
    $map: [[4, signerKid]]
  };

  const arrayBytes = encode([
    protectedBytes,
    unprotected,
    payload,
    signature
  ]);

  // Préfixage avec Tag 18 (0xd2)
  const envelope = new Uint8Array(1 + arrayBytes.length);
  envelope[0] = 0xd2;
  envelope.set(arrayBytes, 1);

  return envelope;
}

/**
 * Valide une enveloppe COSE_Sign1 selon l'ordre normatif strict des 12 étapes.
 *
 * @param envelope - Octets bruts complets de l'enveloppe.
 * @param expectedTyp - Type de contenu attendu (étiquette 16).
 * @param trustStore - Registre de confiance scellé des émetteurs autorisés.
 * @returns VerifyResult déverrouillant la charge utile uniquement après validation 100%.
 * @throws {CoseError} Dès qu'une non-conformité de sécurité est détectée.
 */
export async function coseVerify(
  envelope: Uint8Array,
  expectedTyp: string,
  trustStore: TrustStore
): Promise<VerifyResult> {
  // --------------------------------------------------------------------------
  // Étape 1 : Entrée vide ou premier octet différent de 0xd2 (Tag 18) (Règle K4)
  // --------------------------------------------------------------------------
  if (!envelope || envelope.length === 0 || envelope[0] !== 0xd2) {
    throw new CoseError("ERR_COSE_INVALID_ENVELOPE", "Envelope must start with Tag 18 byte 0xd2");
  }

  // --------------------------------------------------------------------------
  // Étape 2 : Décodage strict du reste du flux CBOR (propagation ERR_CBOR_*)
  // --------------------------------------------------------------------------
  // Le décodeur strict AeterniCore lève CborError avec code natif (ex. ERR_CBOR_TRAILING_BYTES)
  const decoded = decodeStrict(envelope.subarray(1));

  // --------------------------------------------------------------------------
  // Étape 3 : Forme de l'enveloppe [bstr, carte, bstr, bstr de 64 octets]
  // --------------------------------------------------------------------------
  if (!Array.isArray(decoded) || decoded.length !== 4) {
    throw new CoseError("ERR_COSE_INVALID_ENVELOPE", "COSE_Sign1 structure must be an array of exactly 4 elements");
  }

  const protectedBytes = extractBytes(decoded[0]);
  if (!protectedBytes) {
    throw new CoseError("ERR_COSE_INVALID_ENVELOPE", "Protected header must be a byte string (bstr)");
  }

  // En-tête non protégé : carte CBOR ne portant aucune autre clé que la clé entière 4
  const unprotRaw = decoded[1];
  let unprotEntries: [unknown, unknown][] = [];
  if (unprotRaw !== null && typeof unprotRaw === "object") {
    if (Array.isArray((unprotRaw as Record<string, unknown>).$map)) {
      unprotEntries = (unprotRaw as Record<string, unknown>).$map as [unknown, unknown][];
    } else if (!("$bytes" in (unprotRaw as Record<string, unknown>)) && !("$int" in (unprotRaw as Record<string, unknown>))) {
      unprotEntries = Object.entries(unprotRaw);
    } else {
      throw new CoseError("ERR_COSE_INVALID_ENVELOPE", "Unprotected header must be a map");
    }
  } else {
    throw new CoseError("ERR_COSE_INVALID_ENVELOPE", "Unprotected header must be a map");
  }

  for (const [k] of unprotEntries) {
    if (typeof k !== "number" || !Number.isInteger(k) || k !== 4) {
      throw new CoseError("ERR_COSE_INVALID_ENVELOPE", `Unprotected header contains unauthorized key: ${k}`);
    }
  }

  // Charge utile
  const payloadBytes = extractBytes(decoded[2]);
  if (!payloadBytes) {
    throw new CoseError("ERR_COSE_INVALID_ENVELOPE", "Payload must be an attached byte string (bstr)");
  }

  // Signature (exactement 64 octets)
  const signatureBytes = extractBytes(decoded[3]);
  if (!signatureBytes || signatureBytes.length !== 64) {
    throw new CoseError("ERR_COSE_INVALID_ENVELOPE", "Signature must be a byte string of exactly 64 bytes");
  }

  // --------------------------------------------------------------------------
  // Étape 4 : En-tête protégé : décodable strictement, carte, déterministe, clés entières 1 et 16
  // --------------------------------------------------------------------------
  let protDecoded: unknown;
  try {
    protDecoded = decodeStrict(protectedBytes);
  } catch {
    throw new CoseError("ERR_COSE_INVALID_ENVELOPE", "Protected header is not strictly decodable CBOR");
  }

  let protEntries: [unknown, unknown][] = [];
  if (protDecoded !== null && typeof protDecoded === "object") {
    if (Array.isArray((protDecoded as Record<string, unknown>).$map)) {
      protEntries = (protDecoded as Record<string, unknown>).$map as [unknown, unknown][];
    } else if (!("$bytes" in (protDecoded as Record<string, unknown>)) && !("$int" in (protDecoded as Record<string, unknown>))) {
      protEntries = Object.entries(protDecoded);
    } else {
      throw new CoseError("ERR_COSE_INVALID_ENVELOPE", "Protected header must be a CBOR map");
    }
  } else {
    throw new CoseError("ERR_COSE_INVALID_ENVELOPE", "Protected header must be a CBOR map");
  }

  if (protEntries.length === 0) {
    throw new CoseError("ERR_COSE_INVALID_ENVELOPE", "Protected header cannot be an empty map");
  }

  for (const [k] of protEntries) {
    if (typeof k !== "number" || !Number.isInteger(k) || (k !== 1 && k !== 16)) {
      throw new CoseError("ERR_COSE_INVALID_ENVELOPE", `Protected header contains unauthorized key: ${k}`);
    }
  }

  // Contrôle du déterminisme strict : le ré-encodage canonique doit correspondre octet par octet
  const reEncodedProt = encode({ $map: protEntries });
  if (compareBytes(protectedBytes, reEncodedProt) !== 0) {
    throw new CoseError("ERR_COSE_INVALID_ENVELOPE", "Protected header is not encoded in deterministic CBOR order");
  }

  let algVal: unknown = undefined;
  let typVal: unknown = undefined;

  for (const [k, v] of protEntries) {
    if (k === 1) {
      algVal = v;
    } else if (k === 16) {
      typVal = v;
    } else {
      throw new CoseError("ERR_COSE_INVALID_ENVELOPE", `Protected header contains unauthorized key: ${k}`);
    }
  }

  // --------------------------------------------------------------------------
  // Étape 5 : alg absent, non entier ou hors de {-8, -7}
  // --------------------------------------------------------------------------
  if (
    algVal === undefined ||
    typeof algVal !== "number" ||
    !Number.isInteger(algVal) ||
    Object.is(algVal, -0) ||
    (algVal !== -8 && algVal !== -7)
  ) {
    throw new CoseError("ERR_COSE_UNSUPPORTED_ALGORITHM", `Unsupported algorithm: ${algVal}`);
  }

  // --------------------------------------------------------------------------
  // Étape 6 : typ absent, non textuel ou différent de expectedTyp
  // --------------------------------------------------------------------------
  if (typeof typVal !== "string" || typVal !== expectedTyp) {
    throw new CoseError("ERR_COSE_TYPE_MISMATCH", `Content type mismatch: got '${typVal}', expected '${expectedTyp}'`);
  }

  // --------------------------------------------------------------------------
  // Étape 7 : kid absent ou d'une taille différente de 16 octets
  // --------------------------------------------------------------------------
  let kidBytes: Uint8Array | null = null;
  for (const [k, v] of unprotEntries) {
    if (k === 4) {
      kidBytes = extractBytes(v);
    }
  }

  if (!kidBytes || kidBytes.length !== 16) {
    throw new CoseError("ERR_COSE_MISSING_KID", "Unprotected header missing key 4 (kid) of exactly 16 bytes");
  }

  // --------------------------------------------------------------------------
  // Étape 8 : Liste de confiance incohérente (Règles K5 et K2)
  // --------------------------------------------------------------------------
  if (!trustStore || !Array.isArray(trustStore.signers)) {
    throw new CoseError("ERR_COSE_INVALID_TRUST_STORE", "Invalid TrustStore: missing signers array");
  }

  const seenKids = new Set<string>();
  for (const s of trustStore.signers) {
    // Statut obligatoire : "ACTIVE", "RETIRED" ou "REVOKED"
    if (s.status !== "ACTIVE" && s.status !== "RETIRED" && s.status !== "REVOKED") {
      throw new CoseError("ERR_COSE_INVALID_TRUST_STORE", `Invalid signer status: ${s.status}`);
    }

    // Contrôle de la fenêtre temporelle de validité (Règle K2)
    const hasFrom = s.valid_from !== undefined;
    const hasUntil = s.valid_until !== undefined;

    // Soit les deux sont présents, soit aucun des deux n'est présent
    if (hasFrom !== hasUntil) {
      throw new CoseError("ERR_COSE_INVALID_TRUST_STORE", "Signer validity window must have both valid_from and valid_until or neither");
    }

    // RETIRED impose obligatoirement une fenêtre temporelle
    if (s.status === "RETIRED" && !hasFrom) {
      throw new CoseError("ERR_COSE_INVALID_TRUST_STORE", "RETIRED signer must have a validity window");
    }

    if (hasFrom && hasUntil) {
      const from = s.valid_from;
      const until = s.valid_until;

      if (
        typeof from !== "number" ||
        !Number.isInteger(from) ||
        Object.is(from, -0) ||
        from < 0
      ) {
        throw new CoseError("ERR_COSE_INVALID_TRUST_STORE", `Invalid valid_from timestamp: ${from}`);
      }

      if (
        typeof until !== "number" ||
        !Number.isInteger(until) ||
        Object.is(until, -0) ||
        until < 0
      ) {
        throw new CoseError("ERR_COSE_INVALID_TRUST_STORE", `Invalid valid_until timestamp: ${until}`);
      }

      if (from > until) {
        throw new CoseError("ERR_COSE_INVALID_TRUST_STORE", `valid_from (${from}) cannot be greater than valid_until (${until})`);
      }
    }

    const sKidBytes = normalizeBytes(s.kid);
    if (sKidBytes.length !== 16) {
      throw new CoseError("ERR_COSE_INVALID_TRUST_STORE", "Signer kid must be exactly 16 bytes");
    }
    const sKidHex = bytesToHex(sKidBytes).toLowerCase();
    if (seenKids.has(sKidHex)) {
      throw new CoseError("ERR_COSE_INVALID_TRUST_STORE", `Duplicate kid in TrustStore: ${sKidHex}`);
    }
    seenKids.add(sKidHex);

    const sPubBytes = normalizeBytes(s.public_key);
    if (s.alg === -8 && sPubBytes.length !== 32) {
      throw new CoseError("ERR_COSE_INVALID_TRUST_STORE", "Ed25519 signer public key must be 32 bytes");
    }
    if (s.alg === -7 && sPubBytes.length !== 64) {
      throw new CoseError("ERR_COSE_INVALID_TRUST_STORE", "ES256 signer public key must be 64 bytes");
    }
    if (s.alg !== -8 && s.alg !== -7) {
      throw new CoseError("ERR_COSE_INVALID_TRUST_STORE", `Unsupported algorithm in TrustStore: ${s.alg}`);
    }

    const computedKid = await kid(sPubBytes);
    if (bytesToHex(computedKid).toLowerCase() !== sKidHex) {
      throw new CoseError("ERR_COSE_INVALID_TRUST_STORE", `TrustStore entry kid mismatch for ${sKidHex}`);
    }
  }

  // --------------------------------------------------------------------------
  // Étape 9 : Résolution du kid et contrôle de révocation
  // --------------------------------------------------------------------------
  const kidHex = bytesToHex(kidBytes).toLowerCase();
  const entry = trustStore.signers.find((s) => {
    const sKidHex = bytesToHex(normalizeBytes(s.kid)).toLowerCase();
    return sKidHex === kidHex;
  });

  if (!entry) {
    throw new CoseError("ERR_COSE_UNKNOWN_KID", `Signer key ${kidHex} is unknown to local trust store`);
  }

  if (entry.status === "REVOKED") {
    throw new CoseError("ERR_COSE_REVOKED_KEY", `Signer key ${kidHex} is REVOKED`);
  }

  // --------------------------------------------------------------------------
  // Étape 10 : Concordance alg déclaré vs Trust Store
  // --------------------------------------------------------------------------
  if (algVal !== entry.alg) {
    throw new CoseError("ERR_COSE_ALGORITHM_MISMATCH", `Algorithm mismatch: envelope declared ${algVal}, key requires ${entry.alg}`);
  }

  // --------------------------------------------------------------------------
  // Étape 11 : Liaison clé-type / Usage de clé (Règle K3)
  // --------------------------------------------------------------------------
  if (typVal !== entry.typ) {
    throw new CoseError("ERR_COSE_KEY_USAGE_MISMATCH", `Key usage mismatch: envelope type '${typVal}' vs key type '${entry.typ}'`);
  }

  // --------------------------------------------------------------------------
  // Étape 12 : Vérification cryptographique de la signature
  // --------------------------------------------------------------------------
  const trustedPubBytes = normalizeBytes(entry.public_key);
  const tbs = sigStructure(protectedBytes, payloadBytes);

  if (algVal === -7) {
    // ES256 (valide la clé sur courbe, les scalaires, low-s et WebCrypto)
    await es256Verify(trustedPubBytes, tbs, signatureBytes);
  } else if (algVal === -8) {
    // Ed25519 (valide la taille, canonicité de S et WebCrypto)
    await ed25519Verify(trustedPubBytes, tbs, signatureBytes);
  }

  // --------------------------------------------------------------------------
  // Étape 13 : Contrôle de validité temporelle post-signature (Règle K2)
  // --------------------------------------------------------------------------
  if (entry.valid_from !== undefined && entry.valid_until !== undefined) {
    // 1. Décodage strict de la charge utile (propagation native ERR_CBOR_*)
    const payloadDecoded = decodeStrict(payloadBytes);

    // 2. La charge utile doit être une carte CBOR
    if (
      payloadDecoded === null ||
      typeof payloadDecoded !== "object" ||
      Array.isArray(payloadDecoded) ||
      "$bytes" in (payloadDecoded as Record<string, unknown>) ||
      "$int" in (payloadDecoded as Record<string, unknown>)
    ) {
      throw new CoseError("ERR_COSE_ISSUANCE_DATE_MISSING", "Payload is not a CBOR map");
    }

    let mapEntries: [unknown, unknown][] = [];
    if (Array.isArray((payloadDecoded as Record<string, unknown>).$map)) {
      mapEntries = (payloadDecoded as Record<string, unknown>).$map as [unknown, unknown][];
    } else {
      // Toutes les clés sont textuelles dans un objet simple : aucune clé entière
      throw new CoseError("ERR_COSE_ISSUANCE_DATE_MISSING", "Payload map contains no integer keys");
    }

    // 3. Extraction de la date d'émission selon expectedTyp
    if (expectedTyp === "application/aeternitrak-profile+cbor") {
      // Profil mémoriel : clé entière 11, tag CBOR 100
      let rawDateVal: unknown = undefined;
      let foundKey11 = false;
      for (const [k, v] of mapEntries) {
        if (k === 11) {
          foundKey11 = true;
          rawDateVal = v;
          break;
        }
      }

      if (!foundKey11) {
        throw new CoseError("ERR_COSE_ISSUANCE_DATE_MISSING", "Missing issuance date (key 11) in profile");
      }

      if (
        rawDateVal === null ||
        typeof rawDateVal !== "object" ||
        (rawDateVal as Record<string, unknown>).$tag !== 100
      ) {
        throw new CoseError("ERR_COSE_ISSUANCE_DATE_MISSING", "Profile issuance date must have CBOR tag 100");
      }

      const tagVal = (rawDateVal as Record<string, unknown>).$value;
      let D: number;
      if (typeof tagVal === "number" && Number.isInteger(tagVal)) {
        D = tagVal;
      } else if (typeof tagVal === "bigint") {
        D = Number(tagVal);
      } else if (
        tagVal !== null &&
        typeof tagVal === "object" &&
        typeof (tagVal as Record<string, unknown>).$int === "string"
      ) {
        D = Number((tagVal as Record<string, unknown>).$int);
      } else {
        throw new CoseError("ERR_COSE_ISSUANCE_DATE_MISSING", "Invalid profile issuance date value");
      }

      const fromDay = Math.floor(entry.valid_from / 86400);
      const untilDay = Math.floor(entry.valid_until / 86400);

      if (D < fromDay || D > untilDay) {
        throw new CoseError(
          "ERR_COSE_EXPIRED_KEY",
          `Profile issuance day ${D} is outside key validity window [${fromDay}, ${untilDay}]`
        );
      }
    } else if (expectedTyp === "application/aeternitrak-batch-claim+cbor") {
      // Certificat de lot : clé entière 3, tag CBOR 1
      let rawDateVal: unknown = undefined;
      let foundKey3 = false;
      for (const [k, v] of mapEntries) {
        if (k === 3) {
          foundKey3 = true;
          rawDateVal = v;
          break;
        }
      }

      if (!foundKey3) {
        throw new CoseError("ERR_COSE_ISSUANCE_DATE_MISSING", "Missing issuance date (key 3) in batch claim");
      }

      if (
        rawDateVal === null ||
        typeof rawDateVal !== "object" ||
        (rawDateVal as Record<string, unknown>).$tag !== 1
      ) {
        throw new CoseError("ERR_COSE_ISSUANCE_DATE_MISSING", "Batch claim issuance date must have CBOR tag 1");
      }

      const tagVal = (rawDateVal as Record<string, unknown>).$value;
      let S: number;
      if (
        typeof tagVal === "number" &&
        Number.isInteger(tagVal) &&
        tagVal >= 0 &&
        !Object.is(tagVal, -0)
      ) {
        S = tagVal;
      } else if (typeof tagVal === "bigint" && tagVal >= 0n) {
        S = Number(tagVal);
      } else if (
        tagVal !== null &&
        typeof tagVal === "object" &&
        typeof (tagVal as Record<string, unknown>).$int === "string" &&
        BigInt((tagVal as Record<string, unknown>).$int as string) >= 0n
      ) {
        S = Number((tagVal as Record<string, unknown>).$int);
      } else {
        throw new CoseError("ERR_COSE_ISSUANCE_DATE_MISSING", "Invalid batch claim issuance date value");
      }

      if (S < entry.valid_from || S > entry.valid_until) {
        throw new CoseError(
          "ERR_COSE_EXPIRED_KEY",
          `Batch claim issuance timestamp ${S} is outside key validity window [${entry.valid_from}, ${entry.valid_until}]`
        );
      }
    } else {
      throw new CoseError("ERR_COSE_ISSUANCE_DATE_MISSING", `Unsupported typ for key validity check: ${expectedTyp}`);
    }
  }

  // Déverrouillage sécurisé strict : payload n'est retourné qu'ici
  return {
    valid: true,
    payload: payloadBytes,
    payload_hex: bytesToHex(payloadBytes),
    kid: kidHex
  };
}
