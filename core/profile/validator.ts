/**
 * AeterniCore Profile V1 Validator
 * Conforme à RFC 8949 §4.2.1, RFC 8610 (CDDL), RFC 8943 (Tag 100), docs/technical/aeternicore.md §A2, qa/vectors/README.md §4.7
 */

import { decodeToCborValue, type CborValue } from "../cbor/index.ts";
import { ProfileError } from "./errors.ts";

const textEncoder = new TextEncoder();

/**
 * Vérifie si une valeur est une date Tag 100 valide contenant un entier (#6.100(int)).
 * Contrôle direct sur le type majeur réel CBOR (pas sur la notation).
 */
function isTag100Date(val: CborValue): boolean {
  if (val.type !== "tag" || val.tag !== 100) return false;
  if (val.value.type === "uint" || val.value.type === "negint") return true;
  return false;
}

/**
 * Valide une référence d'actif (portrait ou mémo vocal).
 */
function validateAssetRef(
  val: CborValue,
  maxLen: number,
  tooLargeCode: "ERR_PROFILE_PORTRAIT_TOO_LARGE" | "ERR_PROFILE_VOICE_TOO_LARGE"
): void {
  if (val.type !== "map") {
    throw new ProfileError("ERR_PROFILE_INVALID_ASSET_REF", "Asset reference must be a map");
  }

  // 1. Types des clés : entiers requis
  for (const [k] of val.entries) {
    if (k.type !== "uint" || typeof k.value !== "number" || !Number.isInteger(k.value)) {
      throw new ProfileError("ERR_PROFILE_INVALID_KEY_TYPE", "Asset reference keys must be integers");
    }
  }

  // 2. Clés inconnues : seules clés 1 et 2 autorisées
  for (const [k] of val.entries) {
    const keyNum = Number(k.value);
    if (keyNum < 1 || keyNum > 2) {
      throw new ProfileError("ERR_PROFILE_UNKNOWN_FIELD", `Unknown field ${keyNum} in asset reference`);
    }
  }

  // 3. Clés obligatoires : 1 (asset_sha256) et 2 (len)
  const entry1 = val.entries.find(([k]) => k.type === "uint" && Number(k.value) === 1);
  const entry2 = val.entries.find(([k]) => k.type === "uint" && Number(k.value) === 2);
  if (!entry1 || !entry2) {
    throw new ProfileError("ERR_PROFILE_MISSING_FIELD", "Asset reference requires key 1 and key 2");
  }

  // 4. Clé 1 : asset_sha256 (bstr .size 32)
  const hashVal = entry1[1];
  if (hashVal.type !== "bytes") {
    throw new ProfileError("ERR_PROFILE_INVALID_ASSET_REF", "asset_sha256 must be a byte string");
  }
  if (hashVal.value.length !== 32) {
    throw new ProfileError("ERR_PROFILE_INVALID_HASH_LENGTH", `asset_sha256 must be 32 bytes (got ${hashVal.value.length})`);
  }

  // 5. Clé 2 : uint .le maxLen
  const lenVal = entry2[1];
  if (lenVal.type !== "uint" || typeof lenVal.value !== "number" || !Number.isInteger(lenVal.value) || lenVal.value < 0) {
    throw new ProfileError("ERR_PROFILE_INVALID_ASSET_REF", "Asset length must be an unsigned integer");
  }
  if (lenVal.value > maxLen) {
    throw new ProfileError(tooLargeCode, `Asset length ${lenVal.value} exceeds maximum ${maxLen}`);
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
  const root = decodeToCborValue(bytes);

  // 3. La racine n'est pas une carte : ERR_PROFILE_NOT_A_MAP
  if (root.type !== "map") {
    throw new ProfileError("ERR_PROFILE_NOT_A_MAP", "Profile root must be a CBOR map");
  }

  // 4. Une clé de la racine n'est pas un entier : ERR_PROFILE_INVALID_KEY_TYPE
  for (const [k] of root.entries) {
    if (k.type !== "uint" || typeof k.value !== "number" || !Number.isInteger(k.value)) {
      throw new ProfileError("ERR_PROFILE_INVALID_KEY_TYPE", "Root map keys must be integers");
    }
  }

  // 5. Clé 1 absente : ERR_PROFILE_MISSING_FIELD ; différente de l'entier 1 : ERR_PROFILE_UNSUPPORTED_VERSION
  const entry1 = root.entries.find(([k]) => k.type === "uint" && Number(k.value) === 1);
  if (!entry1) {
    throw new ProfileError("ERR_PROFILE_MISSING_FIELD", "Missing schema_version (key 1)");
  }
  if (entry1[1].type !== "uint" || entry1[1].value !== 1) {
    throw new ProfileError("ERR_PROFILE_UNSUPPORTED_VERSION", "Unsupported schema_version (must be integer 1)");
  }

  // 6. Clé hors de [1, 13] : ERR_PROFILE_UNKNOWN_FIELD
  for (const [k] of root.entries) {
    const keyNum = Number(k.value);
    if (keyNum < 1 || keyNum > 13) {
      throw new ProfileError("ERR_PROFILE_UNKNOWN_FIELD", `Unknown field key ${keyNum} in profile`);
    }
  }

  // 7. Clé obligatoire absente (2, 3, 7, 10, 11) : ERR_PROFILE_MISSING_FIELD
  const REQUIRED_ROOT_KEYS = [2, 3, 7, 10, 11];
  for (const reqKey of REQUIRED_ROOT_KEYS) {
    if (!root.entries.some(([k]) => k.type === "uint" && Number(k.value) === reqKey)) {
      throw new ProfileError("ERR_PROFILE_MISSING_FIELD", `Missing required field ${reqKey}`);
    }
  }

  // Conversion en Map pour accès direct par clé
  const fields = new Map<number, CborValue>();
  for (const [k, v] of root.entries) {
    fields.set(Number(k.value), v);
  }

  // 8. Champs dans l'ordre croissant des clés :

  // Clé 2 : subject_kind (1 = human, 2 = animal)
  const subjectKindVal = fields.get(2)!;
  if (
    subjectKindVal.type !== "uint" ||
    (subjectKindVal.value !== 1 && subjectKindVal.value !== 2)
  ) {
    throw new ProfileError("ERR_PROFILE_INVALID_SUBJECT_KIND", "subject_kind must be 1 (human) or 2 (animal)");
  }
  const subjectKind = Number(subjectKindVal.value);

  // Clé 3 : names
  const namesVal = fields.get(3)!;
  if (namesVal.type !== "map") {
    throw new ProfileError("ERR_PROFILE_INVALID_NAME", "names must be a map");
  }

  for (const [k] of namesVal.entries) {
    if (k.type !== "uint" || typeof k.value !== "number" || !Number.isInteger(k.value)) {
      throw new ProfileError("ERR_PROFILE_INVALID_KEY_TYPE", "names map keys must be integers");
    }
  }

  for (const [k] of namesVal.entries) {
    const keyNum = Number(k.value);
    if (keyNum < 1 || keyNum > 3) {
      throw new ProfileError("ERR_PROFILE_UNKNOWN_FIELD", `Unknown field ${keyNum} in names map`);
    }
  }

  const usageNameEntry = namesVal.entries.find(([k]) => k.type === "uint" && Number(k.value) === 1);
  if (!usageNameEntry) {
    throw new ProfileError("ERR_PROFILE_MISSING_FIELD", "Missing usage_name (key 1) in names map");
  }

  if (usageNameEntry[1].type !== "text") {
    throw new ProfileError("ERR_PROFILE_INVALID_NAME", "usage_name must be a string");
  }
  const usageName = usageNameEntry[1].value;
  const usageNameBytes = textEncoder.encode(usageName).length;
  if (usageNameBytes < 1 || usageNameBytes > 120) {
    throw new ProfileError("ERR_PROFILE_INVALID_NAME", `usage_name length in bytes (${usageNameBytes}) must be in 1..120`);
  }

  const birthNameEntry = namesVal.entries.find(([k]) => k.type === "uint" && Number(k.value) === 2);
  if (birthNameEntry) {
    if (birthNameEntry[1].type !== "text") {
      throw new ProfileError("ERR_PROFILE_INVALID_NAME", "birth_name must be a string");
    }
    const birthName = birthNameEntry[1].value;
    const birthNameBytes = textEncoder.encode(birthName).length;
    if (birthNameBytes < 1 || birthNameBytes > 120) {
      throw new ProfileError("ERR_PROFILE_INVALID_NAME", `birth_name length in bytes (${birthNameBytes}) must be in 1..120`);
    }
  }

  const givenNamesEntry = namesVal.entries.find(([k]) => k.type === "uint" && Number(k.value) === 3);
  if (givenNamesEntry) {
    if (givenNamesEntry[1].type !== "array") {
      throw new ProfileError("ERR_PROFILE_INVALID_NAME", "given_names must be an array");
    }
    const givenNames = givenNamesEntry[1].value;
    if (givenNames.length > 8) {
      throw new ProfileError("ERR_PROFILE_TOO_MANY_NAMES", `given_names array length (${givenNames.length}) exceeds 8`);
    }
    for (const item of givenNames) {
      if (item.type !== "text") {
        throw new ProfileError("ERR_PROFILE_INVALID_NAME", "given_name must be a string");
      }
      const itemBytes = textEncoder.encode(item.value).length;
      if (itemBytes < 1 || itemBytes > 80) {
        throw new ProfileError("ERR_PROFILE_INVALID_NAME", `given_name length in bytes (${itemBytes}) must be in 1..80`);
      }
    }
  }

  // Clé 4 : birth_date
  if (fields.has(4)) {
    const birthDate = fields.get(4)!;
    if (!isTag100Date(birthDate)) {
      throw new ProfileError("ERR_PROFILE_INVALID_DATE_TYPE", "birth_date must be a tag 100 integer");
    }
  } else if (subjectKind === 1) {
    throw new ProfileError("ERR_PROFILE_MISSING_BIRTH_DATE", "birth_date is mandatory for human subjects");
  }

  // Clé 5 : death_date
  if (fields.has(5)) {
    const deathDate = fields.get(5)!;
    if (!isTag100Date(deathDate)) {
      throw new ProfileError("ERR_PROFILE_INVALID_DATE_TYPE", "death_date must be a tag 100 integer");
    }
  }

  // Clé 6 : rite_code
  if (fields.has(6)) {
    const rite = fields.get(6)!;
    if (rite.type !== "uint" || typeof rite.value !== "number" || !Number.isInteger(rite.value) || rite.value < 0) {
      throw new ProfileError("ERR_PROFILE_INVALID_RITE", "rite_code must be an unsigned integer");
    }
  }

  // Clé 7 : country (ISO 3166-1 alpha-2)
  const countryVal = fields.get(7)!;
  if (countryVal.type !== "text" || !/^[A-Z]{2}$/.test(countryVal.value)) {
    throw new ProfileError("ERR_PROFILE_INVALID_COUNTRY", "country must be an ISO 3166-1 alpha-2 uppercase string");
  }

  // Clé 8 : portrait_ref
  if (fields.has(8)) {
    validateAssetRef(fields.get(8)!, 20480, "ERR_PROFILE_PORTRAIT_TOO_LARGE");
  }

  // Clé 9 : voice_memo_ref
  if (fields.has(9)) {
    validateAssetRef(fields.get(9)!, 46080, "ERR_PROFILE_VOICE_TOO_LARGE");
  }

  // Clé 10 : issuer_id
  const issuerIdVal = fields.get(10)!;
  if (issuerIdVal.type !== "text") {
    throw new ProfileError("ERR_PROFILE_INVALID_ISSUER_ID", "issuer_id must be a string");
  }
  const issuerIdBytes = textEncoder.encode(issuerIdVal.value).length;
  if (issuerIdBytes < 4 || issuerIdBytes > 64) {
    throw new ProfileError("ERR_PROFILE_INVALID_ISSUER_ID", `issuer_id length in bytes (${issuerIdBytes}) must be in 4..64`);
  }

  // Clé 11 : issued_at
  const issuedAtVal = fields.get(11)!;
  if (!isTag100Date(issuedAtVal)) {
    throw new ProfileError("ERR_PROFILE_INVALID_DATE_TYPE", "issued_at must be a tag 100 integer");
  }

  // Clé 12 : epitaph
  if (fields.has(12)) {
    const epitaphVal = fields.get(12)!;
    if (epitaphVal.type !== "text") {
      throw new ProfileError("ERR_PROFILE_INVALID_EPITAPH", "epitaph must be a string");
    }
    const epitaphBytes = textEncoder.encode(epitaphVal.value).length;
    if (epitaphBytes < 1 || epitaphBytes > 1600) {
      throw new ProfileError("ERR_PROFILE_INVALID_EPITAPH", `epitaph length in bytes (${epitaphBytes}) must be in 1..1600`);
    }
  }

  // Clé 13 : species_taxid
  if (fields.has(13)) {
    if (subjectKind !== 2) {
      throw new ProfileError("ERR_PROFILE_INVALID_SPECIES", "species_taxid is only allowed for animal subjects");
    }
    const taxidVal = fields.get(13)!;
    if (taxidVal.type !== "uint" || typeof taxidVal.value !== "number" || !Number.isInteger(taxidVal.value) || taxidVal.value <= 0) {
      throw new ProfileError("ERR_PROFILE_INVALID_SPECIES", "species_taxid must be a positive integer");
    }
  }

  return { valid: true, len: bytes.length };
}
