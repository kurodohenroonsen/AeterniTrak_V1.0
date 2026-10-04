/**
 * AeterniCore Profile V1 Validator
 * Conforme à RFC 8949 §4.2.1, RFC 8610 (CDDL), RFC 8943 (Tag 100), docs/technical/aeternicore.md §A2, qa/vectors/README.md §4.7
 */

import { decodeStrict } from "../cbor/index.ts";
import { ProfileError } from "./errors.ts";

interface MapEntry {
  key: unknown;
  value: unknown;
}

const textEncoder = new TextEncoder();

/**
 * Extrait les entrées clé-valeur d'un objet décodé par decodeStrict.
 * Si l'élément n'est pas une carte CBOR, retourne null.
 */
function extractMapEntries(item: unknown): MapEntry[] | null {
  if (item === null || typeof item !== "object") {
    return null;
  }
  if (Array.isArray(item)) {
    return null;
  }
  const obj = item as Record<string, unknown>;
  // Objets AVN spéciaux qui ne sont pas des cartes CBOR
  if ("$bytes" in obj || "$tag" in obj || "$int" in obj) {
    return null;
  }
  if ("$map" in obj) {
    if (Array.isArray(obj.$map)) {
      return obj.$map.map(([k, v]) => ({ key: k, value: v }));
    }
    return null;
  }
  // Carte dont toutes les clés étaient textuelles (ou carte vide {})
  return Object.entries(obj).map(([k, v]) => ({ key: k, value: v }));
}

/**
 * Vérifie si une valeur est une date Tag 100 valide contenant un entier (#6.100(int)).
 */
function isTag100Date(val: unknown): boolean {
  if (val === null || typeof val !== "object") return false;
  const obj = val as Record<string, unknown>;
  if (obj.$tag !== 100) return false;
  const v = obj.$value;
  if (typeof v === "number" && Number.isInteger(v)) return true;
  if (typeof v === "bigint") return true;
  if (v !== null && typeof v === "object" && typeof (v as Record<string, unknown>).$int === "string") return true;
  return false;
}

/**
 * Valide une référence d'actif (portrait ou mémo vocal).
 */
function validateAssetRef(
  val: unknown,
  maxLen: number,
  tooLargeCode: "ERR_PROFILE_PORTRAIT_TOO_LARGE" | "ERR_PROFILE_VOICE_TOO_LARGE"
): void {
  const entries = extractMapEntries(val);
  if (entries === null) {
    throw new ProfileError("ERR_PROFILE_INVALID_ASSET_REF", "Asset reference must be a map");
  }

  // 1. Types des clés : entiers requis
  for (const e of entries) {
    if (typeof e.key !== "number" || !Number.isInteger(e.key)) {
      throw new ProfileError("ERR_PROFILE_INVALID_KEY_TYPE", "Asset reference keys must be integers");
    }
  }

  // 2. Clés inconnues : seules clés 1 et 2 autorisées
  for (const e of entries) {
    const k = e.key as number;
    if (k < 1 || k > 2) {
      throw new ProfileError("ERR_PROFILE_UNKNOWN_FIELD", `Unknown field ${k} in asset reference`);
    }
  }

  // 3. Clés obligatoires : 1 (asset_sha256) et 2 (len)
  const entry1 = entries.find((e) => e.key === 1);
  const entry2 = entries.find((e) => e.key === 2);
  if (!entry1 || !entry2) {
    throw new ProfileError("ERR_PROFILE_MISSING_FIELD", "Asset reference requires key 1 and key 2");
  }

  // 4. Clé 1 : asset_sha256 (bstr .size 32)
  const hashVal = entry1.value;
  if (
    hashVal === null ||
    typeof hashVal !== "object" ||
    typeof (hashVal as Record<string, unknown>).$bytes !== "string"
  ) {
    throw new ProfileError("ERR_PROFILE_INVALID_ASSET_REF", "asset_sha256 must be a byte string");
  }
  const hex = (hashVal as Record<string, unknown>).$bytes as string;
  if (hex.length !== 64) {
    throw new ProfileError("ERR_PROFILE_INVALID_HASH_LENGTH", `asset_sha256 must be 32 bytes (got ${hex.length / 2})`);
  }

  // 5. Clé 2 : uint .le maxLen
  const lenVal = entry2.value;
  if (typeof lenVal !== "number" || !Number.isInteger(lenVal) || lenVal < 0) {
    throw new ProfileError("ERR_PROFILE_INVALID_ASSET_REF", "Asset length must be an unsigned integer");
  }
  if (lenVal > maxLen) {
    throw new ProfileError(tooLargeCode, `Asset length ${lenVal} exceeds maximum ${maxLen}`);
  }
}

/**
 * Valide une charge utile CBOR de profil mémoriel V1 selon les règles normatives AeterniCore.
 *
 * @param inputBytes - Buffer d'octets CBOR de la charge utile (budget maximal 1 900 octets).
 * @returns Résultat de validation { valid: true, len: number }.
 * @throws {ProfileError|CborError} Dès qu'une non-conformité de profil ou CBOR est détectée.
 */
export function validateProfile(inputBytes: Uint8Array): { valid: true; len: number } {
  const bytes = inputBytes instanceof Uint8Array ? inputBytes : new Uint8Array(inputBytes);

  // 1. Contrôle de taille avant tout décodage : budget maximal 1 900 octets
  if (bytes.length > 1900) {
    throw new ProfileError("ERR_PROFILE_TOO_LARGE", `Profile payload size (${bytes.length} bytes) exceeds 1900 bytes`);
  }

  // 2. Décodage strict CBOR : les erreurs remontent avec leur code ERR_CBOR_* sans doublon
  const decoded = decodeStrict(bytes);

  // 3. La racine n'est pas une carte : ERR_PROFILE_NOT_A_MAP
  const rootEntries = extractMapEntries(decoded);
  if (rootEntries === null) {
    throw new ProfileError("ERR_PROFILE_NOT_A_MAP", "Profile root must be a CBOR map");
  }

  // 4. Une clé de la racine n'est pas un entier : ERR_PROFILE_INVALID_KEY_TYPE
  for (const e of rootEntries) {
    if (typeof e.key !== "number" || !Number.isInteger(e.key)) {
      throw new ProfileError("ERR_PROFILE_INVALID_KEY_TYPE", "Root map keys must be integers");
    }
  }

  // 5. Clé 1 absente : ERR_PROFILE_MISSING_FIELD ; différente de l'entier 1 : ERR_PROFILE_UNSUPPORTED_VERSION
  const entry1 = rootEntries.find((e) => e.key === 1);
  if (!entry1) {
    throw new ProfileError("ERR_PROFILE_MISSING_FIELD", "Missing schema_version (key 1)");
  }
  if (typeof entry1.value !== "number" || !Number.isInteger(entry1.value) || entry1.value !== 1) {
    throw new ProfileError("ERR_PROFILE_UNSUPPORTED_VERSION", "Unsupported schema_version (must be integer 1)");
  }

  // 6. Clé hors de [1, 13] : ERR_PROFILE_UNKNOWN_FIELD
  for (const e of rootEntries) {
    const k = e.key as number;
    if (k < 1 || k > 13) {
      throw new ProfileError("ERR_PROFILE_UNKNOWN_FIELD", `Unknown field key ${k} in profile`);
    }
  }

  // 7. Clé obligatoire absente (2, 3, 7, 10, 11) : ERR_PROFILE_MISSING_FIELD
  const REQUIRED_ROOT_KEYS = [2, 3, 7, 10, 11];
  for (const reqKey of REQUIRED_ROOT_KEYS) {
    if (!rootEntries.some((e) => e.key === reqKey)) {
      throw new ProfileError("ERR_PROFILE_MISSING_FIELD", `Missing required field ${reqKey}`);
    }
  }

  // Conversion en Map pour accès direct par clé
  const fields = new Map<number, unknown>();
  for (const e of rootEntries) {
    fields.set(e.key as number, e.value);
  }

  // 8. Champs dans l'ordre croissant des clés :

  // Clé 2 : subject_kind (1 = human, 2 = animal)
  const subjectKind = fields.get(2);
  if (
    typeof subjectKind !== "number" ||
    !Number.isInteger(subjectKind) ||
    (subjectKind !== 1 && subjectKind !== 2)
  ) {
    throw new ProfileError("ERR_PROFILE_INVALID_SUBJECT_KIND", "subject_kind must be 1 (human) or 2 (animal)");
  }

  // Clé 3 : names
  const namesVal = fields.get(3);
  const namesEntries = extractMapEntries(namesVal);
  if (namesEntries === null) {
    throw new ProfileError("ERR_PROFILE_INVALID_NAME", "names must be a map");
  }

  for (const e of namesEntries) {
    if (typeof e.key !== "number" || !Number.isInteger(e.key)) {
      throw new ProfileError("ERR_PROFILE_INVALID_KEY_TYPE", "names map keys must be integers");
    }
  }

  for (const e of namesEntries) {
    const k = e.key as number;
    if (k < 1 || k > 3) {
      throw new ProfileError("ERR_PROFILE_UNKNOWN_FIELD", `Unknown field ${k} in names map`);
    }
  }

  const usageNameEntry = namesEntries.find((e) => e.key === 1);
  if (!usageNameEntry) {
    throw new ProfileError("ERR_PROFILE_MISSING_FIELD", "Missing usage_name (key 1) in names map");
  }

  const usageName = usageNameEntry.value;
  if (typeof usageName !== "string") {
    throw new ProfileError("ERR_PROFILE_INVALID_NAME", "usage_name must be a string");
  }
  const usageNameBytes = textEncoder.encode(usageName).length;
  if (usageNameBytes < 1 || usageNameBytes > 120) {
    throw new ProfileError("ERR_PROFILE_INVALID_NAME", `usage_name length in bytes (${usageNameBytes}) must be in 1..120`);
  }

  const birthNameEntry = namesEntries.find((e) => e.key === 2);
  if (birthNameEntry) {
    const birthName = birthNameEntry.value;
    if (typeof birthName !== "string") {
      throw new ProfileError("ERR_PROFILE_INVALID_NAME", "birth_name must be a string");
    }
    const birthNameBytes = textEncoder.encode(birthName).length;
    if (birthNameBytes < 1 || birthNameBytes > 120) {
      throw new ProfileError("ERR_PROFILE_INVALID_NAME", `birth_name length in bytes (${birthNameBytes}) must be in 1..120`);
    }
  }

  const givenNamesEntry = namesEntries.find((e) => e.key === 3);
  if (givenNamesEntry) {
    const givenNames = givenNamesEntry.value;
    if (!Array.isArray(givenNames)) {
      throw new ProfileError("ERR_PROFILE_INVALID_NAME", "given_names must be an array");
    }
    if (givenNames.length > 8) {
      throw new ProfileError("ERR_PROFILE_TOO_MANY_NAMES", `given_names array length (${givenNames.length}) exceeds 8`);
    }
    for (const item of givenNames) {
      if (typeof item !== "string") {
        throw new ProfileError("ERR_PROFILE_INVALID_NAME", "given_name must be a string");
      }
      const itemBytes = textEncoder.encode(item).length;
      if (itemBytes < 1 || itemBytes > 80) {
        throw new ProfileError("ERR_PROFILE_INVALID_NAME", `given_name length in bytes (${itemBytes}) must be in 1..80`);
      }
    }
  }

  // Clé 4 : birth_date
  const hasBirthDate = fields.has(4);
  if (hasBirthDate) {
    const birthDate = fields.get(4);
    if (!isTag100Date(birthDate)) {
      throw new ProfileError("ERR_PROFILE_INVALID_DATE_TYPE", "birth_date must be a tag 100 integer");
    }
  } else if (subjectKind === 1) {
    throw new ProfileError("ERR_PROFILE_MISSING_BIRTH_DATE", "birth_date is mandatory for human subjects");
  }

  // Clé 5 : death_date
  if (fields.has(5)) {
    const deathDate = fields.get(5);
    if (!isTag100Date(deathDate)) {
      throw new ProfileError("ERR_PROFILE_INVALID_DATE_TYPE", "death_date must be a tag 100 integer");
    }
  }

  // Clé 6 : rite_code
  if (fields.has(6)) {
    const rite = fields.get(6);
    if (typeof rite !== "number" || !Number.isInteger(rite) || rite < 0) {
      throw new ProfileError("ERR_PROFILE_INVALID_RITE", "rite_code must be an unsigned integer");
    }
  }

  // Clé 7 : country (ISO 3166-1 alpha-2)
  const country = fields.get(7);
  if (typeof country !== "string" || !/^[A-Z]{2}$/.test(country)) {
    throw new ProfileError("ERR_PROFILE_INVALID_COUNTRY", "country must be an ISO 3166-1 alpha-2 uppercase string");
  }

  // Clé 8 : portrait_ref
  if (fields.has(8)) {
    validateAssetRef(fields.get(8), 20480, "ERR_PROFILE_PORTRAIT_TOO_LARGE");
  }

  // Clé 9 : voice_memo_ref
  if (fields.has(9)) {
    validateAssetRef(fields.get(9), 46080, "ERR_PROFILE_VOICE_TOO_LARGE");
  }

  // Clé 10 : issuer_id
  const issuerId = fields.get(10);
  if (typeof issuerId !== "string") {
    throw new ProfileError("ERR_PROFILE_INVALID_ISSUER_ID", "issuer_id must be a string");
  }
  const issuerIdBytes = textEncoder.encode(issuerId).length;
  if (issuerIdBytes < 4 || issuerIdBytes > 64) {
    throw new ProfileError("ERR_PROFILE_INVALID_ISSUER_ID", `issuer_id length in bytes (${issuerIdBytes}) must be in 4..64`);
  }

  // Clé 11 : issued_at
  const issuedAt = fields.get(11);
  if (!isTag100Date(issuedAt)) {
    throw new ProfileError("ERR_PROFILE_INVALID_DATE_TYPE", "issued_at must be a tag 100 integer");
  }

  // Clé 12 : epitaph
  if (fields.has(12)) {
    const epitaph = fields.get(12);
    if (typeof epitaph !== "string") {
      throw new ProfileError("ERR_PROFILE_INVALID_EPITAPH", "epitaph must be a string");
    }
    const epitaphBytes = textEncoder.encode(epitaph).length;
    if (epitaphBytes < 1 || epitaphBytes > 1600) {
      throw new ProfileError("ERR_PROFILE_INVALID_EPITAPH", `epitaph length in bytes (${epitaphBytes}) must be in 1..1600`);
    }
  }

  // Clé 13 : species_taxid
  if (fields.has(13)) {
    if (subjectKind !== 2) {
      throw new ProfileError("ERR_PROFILE_INVALID_SPECIES", "species_taxid is only allowed for animal subjects");
    }
    const taxid = fields.get(13);
    if (typeof taxid !== "number" || !Number.isInteger(taxid) || taxid <= 0) {
      throw new ProfileError("ERR_PROFILE_INVALID_SPECIES", "species_taxid must be a positive integer");
    }
  }

  return { valid: true, len: bytes.length };
}
