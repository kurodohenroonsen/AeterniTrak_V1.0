/**
 * AeterniCore JSON Canonicalization Scheme (JCS)
 * Conformité : RFC 8785
 */

import { JcsError } from "./errors.ts";

/**
 * Échappe une chaîne de caractères selon les règles minimales et strictes de la RFC 8785 §3.2.2.2 :
 * - Caractères obligatoirement échappés : guillemet `"` (`\"`) et antislash `\` (`\\`).
 * - Caractères de contrôle standard : `\b`, `\t`, `\n`, `\f`, `\r`.
 * - Caractères de contrôle U+0000 à U+001F restants : format hexadécimal `\u00xx` en minuscules.
 * - Tout autre caractère (y compris DEL U+007F, barre oblique `/` et non-ASCII) est émis littéralement.
 */
function escapeString(str: string): string {
  let out = '"';
  for (let i = 0; i < str.length; i++) {
    const c = str.charCodeAt(i);
    if (c === 0x22) {
      out += '\\"';
    } else if (c === 0x5c) {
      out += "\\\\";
    } else if (c === 0x08) {
      out += "\\b";
    } else if (c === 0x09) {
      out += "\\t";
    } else if (c === 0x0a) {
      out += "\\n";
    } else if (c === 0x0c) {
      out += "\\f";
    } else if (c === 0x0d) {
      out += "\\r";
    } else if (c < 0x20) {
      out += "\\u" + c.toString(16).padStart(4, "0");
    } else {
      out += str[i];
    }
  }
  return out + '"';
}

/**
 * Sérialise récursivement une valeur JSON vers sa forme canonique textuelle (RFC 8785).
 */
export function canonicalizeJsonString(val: unknown): string {
  if (val === null) {
    return "null";
  }
  if (val === true) {
    return "true";
  }
  if (val === false) {
    return "false";
  }

  if (typeof val === "number") {
    if (!Number.isFinite(val)) {
      throw new JcsError("ERR_JCS_INVALID_NUMBER", "NaN and Infinity are not permitted in JSON");
    }
    // Règle RFC 8785 §3.2.2.3 : -0 sérialisé en "0"
    if (Object.is(val, -0)) {
      return "0";
    }
    // Formatage ECMAScript Number::toString (7.1.12.1)
    return val.toString();
  }

  if (typeof val === "string") {
    return escapeString(val);
  }

  if (Array.isArray(val)) {
    return "[" + val.map(canonicalizeJsonString).join(",") + "]";
  }

  if (typeof val === "object") {
    const obj = val as Record<string, unknown>;
    // Tri lexicographique strict selon les code units UTF-16 (RFC 8785 §3.2.3)
    const keys = Object.keys(obj).sort((a, b) => (a < b ? -1 : a > b ? 1 : 0));
    return "{" + keys.map((k) => escapeString(k) + ":" + canonicalizeJsonString(obj[k])).join(",") + "}";
  }

  throw new JcsError("ERR_JCS_UNSUPPORTED_TYPE", `Unsupported type for JSON canonicalization: ${typeof val}`);
}

/**
 * Canonise une structure JSON selon la spécification RFC 8785 (JCS).
 *
 * @param value - Donnée JSON à canoniser.
 * @returns Flux d'octets UTF-8 canonisé représentant le JSON scellé.
 * @throws {JcsError} En cas de valeur non sérialisable (cycles, NaN, Infinity).
 */
export function canonicalizeJson(value: unknown): Uint8Array {
  const str = canonicalizeJsonString(value);
  return new TextEncoder().encode(str);
}
