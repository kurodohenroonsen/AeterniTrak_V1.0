/**
 * AeterniCore Deterministic CBOR Encoder
 * Conformité : RFC 8949 §4.2.1, RFC 8943 (Tag 100), RFC 8610 & profil AeterniCore v1
 */

import { CborError } from "./errors.ts";
import { ByteWriter, compareBytes, bytesToHex, hexToBytes } from "./writer.ts";

/**
 * Encode récursivement un élément JavaScript ou structure AVN vers le flux CBOR canonique.
 */
function encodeItem(item: unknown, writer: ByteWriter): void {
  // 1. Valeurs simples et null
  if (item === null) {
    writer.writeByte(0xf6);
    return;
  }
  if (typeof item === "boolean") {
    writer.writeByte(item ? 0xf5 : 0xf4);
    return;
  }

  // 2. Nombres entiers
  if (typeof item === "number") {
    if (!Number.isFinite(item) || !Number.isInteger(item) || Object.is(item, -0)) {
      throw new CborError("ERR_CBOR_UNSUPPORTED_TYPE", "Floating point, NaN, Infinity, and -0 are unsupported");
    }
    if (item >= 0) {
      writer.writeUint(0, item);
    } else {
      writer.writeUint(1, -1 - item);
    }
    return;
  }

  // 3. BigInt natif
  if (typeof item === "bigint") {
    if (item >= 0n) {
      writer.writeUint(0, item);
    } else {
      writer.writeUint(1, -1n - item);
    }
    return;
  }

  // 4. Chaînes textuelles UTF-8 (NFC obligatoire sans normalisation silencieuse)
  if (typeof item === "string") {
    if (item.normalize("NFC") !== item) {
      throw new CborError("ERR_CBOR_TEXT_NOT_NFC", "Text string must be NFC-normalized before encoding");
    }
    const bytes = new TextEncoder().encode(item);
    writer.writeUint(3, bytes.length);
    writer.writeBytes(bytes);
    return;
  }

  // 5. Tableaux de longueur définie
  if (Array.isArray(item)) {
    writer.writeUint(4, item.length);
    for (const elem of item) {
      encodeItem(elem, writer);
    }
    return;
  }

  // 6. Chaînes d'octets brutes (Uint8Array)
  if (item instanceof Uint8Array) {
    writer.writeUint(2, item.length);
    writer.writeBytes(item);
    return;
  }

  // 7. Objets et structures AVN
  if (typeof item === "object") {
    const obj = item as Record<string, unknown>;

    // Interdiction formelle des flottants déguisés AVN
    if ("$float" in obj) {
      throw new CborError("ERR_CBOR_UNSUPPORTED_TYPE", "Floating point values are forbidden by profile");
    }

    // Entier étendu AVN ($int)
    if ("$int" in obj) {
      const b = BigInt(obj.$int as string);
      if (b >= 0n) {
        writer.writeUint(0, b);
      } else {
        writer.writeUint(1, -1n - b);
      }
      return;
    }

    // Chaîne d'octets hexadécimale AVN ($bytes)
    if ("$bytes" in obj) {
      const bytes = hexToBytes(obj.$bytes as string);
      writer.writeUint(2, bytes.length);
      writer.writeBytes(bytes);
      return;
    }

    // Étiquette sémantique AVN ($tag)
    if ("$tag" in obj) {
      const tag = Number(obj.$tag);
      if (tag !== 1 && tag !== 100) {
        throw new CborError("ERR_CBOR_UNSUPPORTED_TAG", `Tag ${tag} is not supported by profile`);
      }
      const val = obj.$value;

      // Vérification du contenu du tag
      if (tag === 100) {
        const isInt =
          (typeof val === "number" && Number.isInteger(val) && !Object.is(val, -0)) ||
          typeof val === "bigint" ||
          (val !== null && typeof val === "object" && typeof (val as Record<string, unknown>).$int === "string");
        if (!isInt) {
          throw new CborError("ERR_CBOR_TAG_CONTENT", "Tag 100 content must be an integer");
        }
      }
      if (tag === 1) {
        const isNonNegInt =
          (typeof val === "number" && Number.isInteger(val) && val >= 0) ||
          (typeof val === "bigint" && val >= 0n) ||
          (val !== null && typeof val === "object" && typeof (val as Record<string, unknown>).$int === "string" && BigInt((val as Record<string, unknown>).$int as string) >= 0n);
        if (!isNonNegInt) {
          throw new CborError("ERR_CBOR_TAG_CONTENT", "Tag 1 content must be a non-negative integer");
        }
      }

      writer.writeUint(6, tag);
      encodeItem(val, writer);
      return;
    }

    // Carte arbitraire AVN ($map)
    if ("$map" in obj) {
      const pairs = obj.$map as [unknown, unknown][];
      const encodedPairs = pairs.map(([k, v]) => {
        const kw = new ByteWriter();
        encodeItem(k, kw);
        const kb = kw.getBytes();
        return { k, v, keyBytes: kb, keyHex: bytesToHex(kb) };
      });

      // Contrôle de l'unicité stricte des clés
      const seen = new Set<string>();
      for (const p of encodedPairs) {
        if (seen.has(p.keyHex)) {
          throw new CborError("ERR_CBOR_DUPLICATE_KEY", "Duplicate map key detected");
        }
        seen.add(p.keyHex);
      }

      // Tri bytewise-lexicographique des clés encodées (RFC 8949 §4.2.1 (3))
      encodedPairs.sort((a, b) => compareBytes(a.keyBytes, b.keyBytes));

      writer.writeUint(5, encodedPairs.length);
      for (const p of encodedPairs) {
        writer.writeBytes(p.keyBytes);
        encodeItem(p.v, writer);
      }
      return;
    }

    // Objet JavaScript ordinaire (carte à clés chaînes)
    const keys = Object.keys(obj);
    const encodedPairs = keys.map((k) => {
      const kw = new ByteWriter();
      encodeItem(k, kw);
      const kb = kw.getBytes();
      return { k, v: obj[k], keyBytes: kb, keyHex: bytesToHex(kb) };
    });

    const seen = new Set<string>();
    for (const p of encodedPairs) {
      if (seen.has(p.keyHex)) {
        throw new CborError("ERR_CBOR_DUPLICATE_KEY", "Duplicate map key detected");
      }
      seen.add(p.keyHex);
    }

    encodedPairs.sort((a, b) => compareBytes(a.keyBytes, b.keyBytes));

    writer.writeUint(5, encodedPairs.length);
    for (const p of encodedPairs) {
      writer.writeBytes(p.keyBytes);
      encodeItem(p.v, writer);
    }
    return;
  }

  // Type non pris en charge (undefined, Symbol, Function, etc.)
  throw new CborError("ERR_CBOR_UNSUPPORTED_TYPE", `Unsupported value type: ${typeof item}`);
}

/**
 * Encode un élément JavaScript ou structure AVN vers sa représentation CBOR déterministe canonique.
 *
 * @param item - Donnée à sérialiser.
 * @returns Uint8Array contenant l'encodage CBOR canonique minimal.
 * @throws {CborError} Si l'entrée enfreint les règles du profil AeterniCore.
 */
export function encode(item: unknown): Uint8Array {
  const writer = new ByteWriter();
  encodeItem(item, writer);
  return writer.getBytes();
}
