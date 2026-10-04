/**
 * AeterniCore Strict CBOR Decoder
 * Conformité : RFC 8949 §4.2.1, RFC 8943 (Tag 100), RFC 8610 & profil AeterniCore v1
 */

import { CborError } from "./errors.ts";
import { compareBytes, bytesToHex } from "./writer.ts";

/**
 * Décode un flux d'octets CBOR sous le profil de validation le plus strict.
 *
 * @param inputBytes - Buffer d'octets CBOR à vérifier et décoder.
 * @returns Structure décomposée en notation JavaScript native ou AVN.
 * @throws {CborError} Dès qu'une non-conformité déterministe ou de profil est détectée.
 */
export function decodeStrict(inputBytes: Uint8Array): unknown {
  const buf = inputBytes instanceof Uint8Array ? inputBytes : new Uint8Array(inputBytes);

  if (buf.length === 0) {
    throw new CborError("ERR_CBOR_TRUNCATED", "Empty buffer", 0);
  }

  let offset = 0;
  const textDecoder = new TextDecoder("utf-8", { fatal: true });
  const dataView = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);

  function readUint(info: number, major: number): bigint | number {
    if (info < 24) {
      return info;
    }
    if (info === 24) {
      if (offset + 1 > buf.length) {
        throw new CborError("ERR_CBOR_TRUNCATED", "Truncated uint8", offset);
      }
      const v = buf[offset++];
      // Règle de compacité la plus courte (RFC 8949 §4.2.1 (1))
      if (v < 24) {
        throw new CborError("ERR_CBOR_NOT_SHORTEST", `Integer ${v} encoded in 2 bytes (info 24)`, offset - 1);
      }
      return v;
    }
    if (info === 25) {
      if (offset + 2 > buf.length) {
        throw new CborError("ERR_CBOR_TRUNCATED", "Truncated uint16", offset);
      }
      const v = dataView.getUint16(offset, false);
      offset += 2;
      if (v < 256) {
        throw new CborError("ERR_CBOR_NOT_SHORTEST", `Integer ${v} encoded in 3 bytes (info 25)`, offset - 2);
      }
      return v;
    }
    if (info === 26) {
      if (offset + 4 > buf.length) {
        throw new CborError("ERR_CBOR_TRUNCATED", "Truncated uint32", offset);
      }
      const v = dataView.getUint32(offset, false);
      offset += 4;
      if (v < 65536) {
        throw new CborError("ERR_CBOR_NOT_SHORTEST", `Integer ${v} encoded in 5 bytes (info 26)`, offset - 4);
      }
      return v;
    }
    if (info === 27) {
      if (offset + 8 > buf.length) {
        throw new CborError("ERR_CBOR_TRUNCATED", "Truncated uint64", offset);
      }
      const v = dataView.getBigUint64(offset, false);
      offset += 8;
      if (v < 4294967296n) {
        throw new CborError("ERR_CBOR_NOT_SHORTEST", `Integer ${v} encoded in 9 bytes (info 27)`, offset - 8);
      }
      return v;
    }
    if (info === 31) {
      throw new CborError("ERR_CBOR_INDEFINITE_LENGTH", "Indefinite length is forbidden by deterministic profile", offset);
    }
    throw new CborError("ERR_CBOR_MALFORMED", `Reserved additional information ${info}`, offset);
  }

  function decodeItem(): unknown {
    if (offset >= buf.length) {
      throw new CborError("ERR_CBOR_TRUNCATED", "Unexpected end of CBOR buffer", offset);
    }

    const itemStart = offset;
    const initialByte = buf[offset++];
    const major = initialByte >> 5;
    const info = initialByte & 0x1f;

    // Major 0 : Entier non-négatif
    if (major === 0) {
      const val = readUint(info, 0);
      if (typeof val === "bigint") {
        if (val <= BigInt(Number.MAX_SAFE_INTEGER)) {
          return Number(val);
        }
        return { $int: val.toString() };
      }
      return val;
    }

    // Major 1 : Entier négatif
    if (major === 1) {
      const val = readUint(info, 1);
      if (typeof val === "bigint") {
        const neg = -1n - val;
        if (neg >= BigInt(Number.MIN_SAFE_INTEGER)) {
          return Number(neg);
        }
        return { $int: neg.toString() };
      }
      return -1 - val;
    }

    // Major 2 : Chaîne d'octets
    if (major === 2) {
      const len = Number(readUint(info, 2));
      if (offset + len > buf.length) {
        throw new CborError("ERR_CBOR_TRUNCATED", "Truncated byte string", offset);
      }
      const bytes = buf.subarray(offset, offset + len);
      offset += len;
      return { $bytes: bytesToHex(bytes) };
    }

    // Major 3 : Texte UTF-8
    if (major === 3) {
      const len = Number(readUint(info, 3));
      if (offset + len > buf.length) {
        throw new CborError("ERR_CBOR_TRUNCATED", "Truncated text string", offset);
      }
      const rawBytes = buf.subarray(offset, offset + len);
      offset += len;

      let str: string;
      try {
        str = textDecoder.decode(rawBytes);
      } catch (e: unknown) {
        throw new CborError("ERR_CBOR_INVALID_UTF8", (e as Error).message, itemStart);
      }

      if (str.normalize("NFC") !== str) {
        throw new CborError("ERR_CBOR_TEXT_NOT_NFC", "Text string is not NFC-normalized", itemStart);
      }
      return str;
    }

    // Major 4 : Tableau
    if (major === 4) {
      const len = Number(readUint(info, 4));
      const arr: unknown[] = [];
      for (let i = 0; i < len; i++) {
        arr.push(decodeItem());
      }
      return arr;
    }

    // Major 5 : Carte
    if (major === 5) {
      const len = Number(readUint(info, 5));
      const entries: [unknown, unknown][] = [];
      let allStringKeys = true;
      let prevKeyBytes: Uint8Array | null = null;
      const seenKeys = new Set<string>();

      for (let i = 0; i < len; i++) {
        const keyStart = offset;
        const k = decodeItem();
        const keyEnd = offset;
        const keyBytes = buf.subarray(keyStart, keyEnd);

        // Vérification du tri lexicographique bytewise strict (RFC 8949 §4.2.1 (3))
        if (prevKeyBytes !== null) {
          const cmp = compareBytes(prevKeyBytes, keyBytes);
          if (cmp === 0) {
            throw new CborError("ERR_CBOR_DUPLICATE_KEY", "Duplicate map key detected", keyStart);
          }
          if (cmp > 0) {
            throw new CborError("ERR_CBOR_MAP_UNSORTED", "Map keys must be sorted in bytewise lexicographic order", keyStart);
          }
        }

        const keyHex = bytesToHex(keyBytes);
        if (seenKeys.has(keyHex)) {
          throw new CborError("ERR_CBOR_DUPLICATE_KEY", "Duplicate map key detected", keyStart);
        }
        seenKeys.add(keyHex);
        prevKeyBytes = keyBytes;

        const v = decodeItem();
        if (typeof k !== "string") {
          allStringKeys = false;
        }
        entries.push([k, v]);
      }

      if (allStringKeys) {
        const obj: Record<string, unknown> = {};
        for (const [k, v] of entries) {
          obj[k as string] = v;
        }
        return obj;
      }
      return { $map: entries };
    }

    // Major 6 : Étiquette sémantique (Tag)
    if (major === 6) {
      const tag = Number(readUint(info, 6));
      if (tag !== 1 && tag !== 100) {
        throw new CborError("ERR_CBOR_UNSUPPORTED_TAG", `Tag ${tag} is not supported by profile`, itemStart);
      }

      const val = decodeItem();

      if (tag === 100) {
        const isInt =
          typeof val === "number" ||
          typeof val === "bigint" ||
          (val !== null && typeof val === "object" && typeof (val as Record<string, unknown>).$int === "string");
        if (!isInt) {
          throw new CborError("ERR_CBOR_TAG_CONTENT", "Tag 100 content must be an integer", itemStart);
        }
      }

      if (tag === 1) {
        const isNonNegInt =
          (typeof val === "number" && val >= 0) ||
          (typeof val === "bigint" && val >= 0n) ||
          (val !== null && typeof val === "object" && typeof (val as Record<string, unknown>).$int === "string" && BigInt((val as Record<string, unknown>).$int as string) >= 0n);
        if (!isNonNegInt) {
          throw new CborError("ERR_CBOR_TAG_CONTENT", "Tag 1 content must be a non-negative integer", itemStart);
        }
      }

      return { $tag: tag, $value: val };
    }

    // Major 7 : Valeurs simples et flottants
    if (major === 7) {
      if (info === 20) return false;
      if (info === 21) return true;
      if (info === 22) return null;
      if (info === 23) {
        throw new CborError("ERR_CBOR_UNSUPPORTED_TYPE", "Undefined is forbidden by profile", itemStart);
      }
      if (info === 24) {
        if (offset >= buf.length) {
          throw new CborError("ERR_CBOR_TRUNCATED", "Truncated simple value", offset);
        }
        const sVal = buf[offset++];
        if (sVal < 32) {
          throw new CborError("ERR_CBOR_MALFORMED", "Simple value < 32 encoded in 2 bytes", itemStart);
        }
        throw new CborError("ERR_CBOR_UNSUPPORTED_TYPE", `Simple value simple(${sVal}) is forbidden by profile`, itemStart);
      }
      if (info === 25 || info === 26 || info === 27) {
        throw new CborError("ERR_CBOR_UNSUPPORTED_TYPE", "Floating point values are forbidden by profile", itemStart);
      }
      if (info === 31) {
        throw new CborError("ERR_CBOR_MALFORMED", "Break stop code outside indefinite structure", itemStart);
      }
      throw new CborError("ERR_CBOR_MALFORMED", `Reserved simple value ${info}`, itemStart);
    }

    throw new CborError("ERR_CBOR_MALFORMED", `Unknown major type ${major}`, itemStart);
  }

  const result = decodeItem();

  // Contrôle des octets résiduels orphelins (RFC 8949 §4.2.1)
  if (offset !== buf.length) {
    throw new CborError("ERR_CBOR_TRAILING_BYTES", `Trailing bytes (${buf.length - offset} extra bytes)`, offset);
  }

  return result;
}
