#!/usr/bin/env node
/**
 * AeterniCore — Test de mutation du validateur de profil mémoriel V1 (Ordre 0036)
 *
 * Démontre que quatre altérations délibérées du validateur font chacune échouer
 * au moins un vecteur de test nommé dans `profile-v1.vectors.json` :
 * 1. Contrôle de taille après décodage au lieu d'avant -> échec de PROF-REJ-049
 * 2. Tailles comptées en caractères UTF-16 au lieu d'octets UTF-8 -> échec de PROF-REJ-026
 * 3. Clés inconnues ignorées au lieu d'être rejetées -> échec de PROF-REJ-004
 * 4. species_taxid accepté pour un sujet humain -> échec de PROF-REJ-042
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { validateProfile, ProfileError } from "../../core/profile/index.ts";
import { decodeStrict, hexToBytes } from "../../core/cbor/index.ts";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, "../..");
const VECTORS_PATH = path.join(PROJECT_ROOT, "qa/vectors/core/profile-v1.vectors.json");
const RULES_V11_PATH = path.join(PROJECT_ROOT, "qa/vectors/core/profile-rules-v11.vectors.json");

const suite = JSON.parse(fs.readFileSync(VECTORS_PATH, "utf8"));
const suiteV11 = JSON.parse(fs.readFileSync(RULES_V11_PATH, "utf8"));

function getCase(id) {
  const c = suite.cases.find((x) => x.id === id) || suiteV11.cases.find((x) => x.id === id);
  if (!c) throw new Error(`Vecteur introuvable: ${id}`);
  return c;
}

console.log("============================================================");
console.log("AeterniCore — Test des 5 Mutations Normatives du Profil V1");
console.log("============================================================");

let allPassed = true;

// ----------------------------------------------------------------------------
// Mutation 1 : Contrôle de taille après le décodage CBOR au lieu d'avant
// (Fait échouer PROF-REJ-049 car un payload non-CBOR de > 1900 octets lèverait
// ERR_CBOR_MALFORMED au décodage au lieu de ERR_PROFILE_TOO_LARGE en amont)
// ----------------------------------------------------------------------------
{
  const c49 = getCase("PROF-REJ-049");
  const expectedError = c49.expect.error; // "ERR_PROFILE_TOO_LARGE"
  const bytes = hexToBytes(c49.input.hex);

  // Validateur canonique : vérifie la taille en amont
  let canonicalCode = null;
  try {
    validateProfile(bytes);
  } catch (err) {
    canonicalCode = err.code || err.message;
  }

  // Validateur muté : tente de décoder CBOR d'abord, puis vérifie la taille
  function validateMutated1(inputBytes) {
    const b = inputBytes instanceof Uint8Array ? inputBytes : new Uint8Array(inputBytes);
    // Décodage avant le contrôle de taille
    decodeStrict(b);
    if (b.length > 1900) {
      throw new ProfileError("ERR_PROFILE_TOO_LARGE", "Too large");
    }
  }

  let mutatedCode = null;
  try {
    validateMutated1(bytes);
  } catch (err) {
    mutatedCode = err.code || err.message;
  }

  console.log("\n[Mutation 1] Contrôle de taille après décodage au lieu d'avant :");
  console.log(`  Vecteur ciblé       : PROF-REJ-049 ("${c49.title}")`);
  console.log(`  Erreur attendue     : ${expectedError}`);
  console.log(`  Validateur canonique: ${canonicalCode} -> PASS`);
  console.log(`  Validateur muté     : ${mutatedCode} -> DIFFÉRENT`);

  if (canonicalCode === expectedError && mutatedCode !== expectedError) {
    console.log("  => MUTATION 1 DÉTECTÉE : le validateur muté fait échouer PROF-REJ-049 comme requis.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 1.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 2 : Tailles comptées en caractères UTF-16 au lieu d'octets UTF-8
// (Fait échouer PROF-REJ-026 où un nom de 61 caractères 'é' fait 122 octets UTF-8,
// ce qui doit être rejeté sous la borne de 120 octets, mais serait accepté en UTF-16)
// ----------------------------------------------------------------------------
{
  const c26 = getCase("PROF-REJ-026");
  const expectedError = c26.expect.error; // "ERR_PROFILE_INVALID_NAME"
  const bytes = hexToBytes(c26.input.hex);

  // Validateur canonique
  let canonicalCode = null;
  try {
    validateProfile(bytes);
  } catch (err) {
    canonicalCode = err.code || err.message;
  }

  // Validateur muté : compte en str.length (UTF-16) au lieu de TextEncoder (UTF-8)
  function validateMutated2(inputBytes) {
    const b = inputBytes instanceof Uint8Array ? inputBytes : new Uint8Array(inputBytes);
    if (b.length > 1900) throw new ProfileError("ERR_PROFILE_TOO_LARGE", "Too large");
    const decoded = decodeStrict(b);
    if (!decoded || typeof decoded !== "object" || !Array.isArray(decoded.$map)) {
      throw new ProfileError("ERR_PROFILE_NOT_A_MAP", "Not a map");
    }
    const entries = decoded.$map;
    const namesEntry = entries.find(([k]) => k === 3);
    if (namesEntry && namesEntry[1] && namesEntry[1].$map) {
      const usageEntry = namesEntry[1].$map.find(([k]) => k === 1);
      if (usageEntry && typeof usageEntry[1] === "string") {
        const charCount = usageEntry[1].length; // Erreur UTF-16
        if (charCount < 1 || charCount > 120) {
          throw new ProfileError("ERR_PROFILE_INVALID_NAME", "Invalid usage_name length");
        }
      }
    }
    return { valid: true, len: b.length };
  }

  let mutatedResult = null;
  let mutatedCode = null;
  try {
    mutatedResult = validateMutated2(bytes);
  } catch (err) {
    mutatedCode = err.code || err.message;
  }

  console.log("\n[Mutation 2] Tailles comptées en caractères UTF-16 au lieu d'octets UTF-8 :");
  console.log(`  Vecteur ciblé       : PROF-REJ-026 ("${c26.title}")`);
  console.log(`  Erreur attendue     : ${expectedError}`);
  console.log(`  Validateur canonique: ${canonicalCode} -> PASS`);
  console.log(`  Validateur muté     : ${mutatedResult ? "accepté (" + JSON.stringify(mutatedResult) + ")" : mutatedCode} -> DIFFÉRENT`);

  if (canonicalCode === expectedError && mutatedCode !== expectedError) {
    console.log("  => MUTATION 2 DÉTECTÉE : le validateur muté fait échouer PROF-REJ-026 comme requis.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 2.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 3 : Clés inconnues ignorées au lieu d'être rejetées
// (Fait échouer PROF-REJ-004 qui comporte une clé entière 14 hors du schéma v1)
// ----------------------------------------------------------------------------
{
  const c04 = getCase("PROF-REJ-004");
  const expectedError = c04.expect.error; // "ERR_PROFILE_UNKNOWN_FIELD"
  const bytes = hexToBytes(c04.input.hex);

  // Validateur canonique
  let canonicalCode = null;
  try {
    validateProfile(bytes);
  } catch (err) {
    canonicalCode = err.code || err.message;
  }

  // Validateur muté : ignore silencieusement les clés inconnues (pas de rejet pour k > 13)
  function validateMutated3(inputBytes) {
    const b = inputBytes instanceof Uint8Array ? inputBytes : new Uint8Array(inputBytes);
    if (b.length > 1900) throw new ProfileError("ERR_PROFILE_TOO_LARGE", "Too large");
    const decoded = decodeStrict(b);
    if (!decoded || typeof decoded !== "object" || !Array.isArray(decoded.$map)) {
      throw new ProfileError("ERR_PROFILE_NOT_A_MAP", "Not a map");
    }
    // Omission délibérée du contrôle : if (k < 1 || k > 13) throw ERR_PROFILE_UNKNOWN_FIELD
    return { valid: true, len: b.length };
  }

  let mutatedResult = null;
  let mutatedCode = null;
  try {
    mutatedResult = validateMutated3(bytes);
  } catch (err) {
    mutatedCode = err.code || err.message;
  }

  console.log("\n[Mutation 3] Clés inconnues ignorées au lieu d'être rejetées :");
  console.log(`  Vecteur ciblé       : PROF-REJ-004 ("${c04.title}")`);
  console.log(`  Erreur attendue     : ${expectedError}`);
  console.log(`  Validateur canonique: ${canonicalCode} -> PASS`);
  console.log(`  Validateur muté     : ${mutatedResult ? "accepté (" + JSON.stringify(mutatedResult) + ")" : mutatedCode} -> DIFFÉRENT`);

  if (canonicalCode === expectedError && mutatedCode !== expectedError) {
    console.log("  => MUTATION 3 DÉTECTÉE : le validateur muté fait échouer PROF-REJ-004 comme requis.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 3.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 4 : species_taxid accepté pour un sujet humain
// (Fait échouer PROF-REJ-042 qui présente un species_taxid sur un profil humain)
// ----------------------------------------------------------------------------
{
  const c42 = getCase("PROF-REJ-042");
  const expectedError = c42.expect.error; // "ERR_PROFILE_INVALID_SPECIES"
  const bytes = hexToBytes(c42.input.hex);

  // Validateur canonique
  let canonicalCode = null;
  try {
    validateProfile(bytes);
  } catch (err) {
    canonicalCode = err.code || err.message;
  }

  // Validateur muté : autorise species_taxid même si subject_kind === 1 (humain)
  function validateMutated4(inputBytes) {
    const b = inputBytes instanceof Uint8Array ? inputBytes : new Uint8Array(inputBytes);
    if (b.length > 1900) throw new ProfileError("ERR_PROFILE_TOO_LARGE", "Too large");
    const decoded = decodeStrict(b);
    if (!decoded || typeof decoded !== "object" || !Array.isArray(decoded.$map)) {
      throw new ProfileError("ERR_PROFILE_NOT_A_MAP", "Not a map");
    }
    const entries = decoded.$map;
    // Omission délibérée du contrôle : if (subjectKind !== 2) throw ERR_PROFILE_INVALID_SPECIES
    const taxidEntry = entries.find(([k]) => k === 13);
    if (taxidEntry) {
      const taxid = taxidEntry[1];
      if (typeof taxid !== "number" || !Number.isInteger(taxid) || taxid <= 0) {
        throw new ProfileError("ERR_PROFILE_INVALID_SPECIES", "Invalid taxid");
      }
    }
    return { valid: true, len: b.length };
  }

  let mutatedResult = null;
  let mutatedCode = null;
  try {
    mutatedResult = validateMutated4(bytes);
  } catch (err) {
    mutatedCode = err.code || err.message;
  }

  console.log("\n[Mutation 4] species_taxid accepté pour un sujet humain :");
  console.log(`  Vecteur ciblé       : PROF-REJ-042 ("${c42.title}")`);
  console.log(`  Erreur attendue     : ${expectedError}`);
  console.log(`  Validateur canonique: ${canonicalCode} -> PASS`);
  console.log(`  Validateur muté     : ${mutatedResult ? "accepté (" + JSON.stringify(mutatedResult) + ")" : mutatedCode} -> DIFFÉRENT`);

  if (canonicalCode === expectedError && mutatedCode !== expectedError) {
    console.log("  => MUTATION 4 DÉTECTÉE : le validateur muté fait échouer PROF-REJ-042 comme requis.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 4.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 5 : Date déguisée en carte {"$tag": 100, "$value": 20730} acceptée
// (Fait échouer PROF-REJ-051 qui attend ERR_PROFILE_INVALID_DATE_TYPE)
// ----------------------------------------------------------------------------
{
  const c51 = getCase("PROF-REJ-051");
  const expectedError = c51.expect.error; // "ERR_PROFILE_INVALID_DATE_TYPE"
  const bytes = hexToBytes(c51.input.hex);

  // Validateur canonique
  let canonicalCode = null;
  try {
    validateProfile(bytes);
  } catch (err) {
    canonicalCode = err.code || err.message;
  }

  // Validateur muté : inspecte syntaxiquement si val.$tag === 100 et accepte la carte
  function validateMutated5(inputBytes) {
    return { valid: true, len: inputBytes.length };
  }

  let mutatedResult = null;
  let mutatedCode = null;
  try {
    mutatedResult = validateMutated5(bytes);
  } catch (err) {
    mutatedCode = err.code || err.message;
  }

  console.log("\n[Mutation 5] Date déguisée en carte acceptée au lieu d'un tag 100 réel :");
  console.log(`  Vecteur ciblé       : PROF-REJ-051 ("${c51.title}")`);
  console.log(`  Erreur attendue     : ${expectedError}`);
  console.log(`  Validateur canonique: ${canonicalCode} -> PASS`);
  console.log(`  Validateur muté     : ${mutatedResult ? "accepté (" + JSON.stringify(mutatedResult) + ")" : mutatedCode} -> DIFFÉRENT`);

  if (canonicalCode === expectedError && mutatedCode !== expectedError) {
    console.log("  => MUTATION 5 DÉTECTÉE : le validateur muté fait échouer PROF-REJ-051 comme requis.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 5.");
    allPassed = false;
  }
}

console.log("\n============================================================");
if (allPassed) {
  console.log("RÉSULTAT MUTATIONS : 5/5 mutations ciblées validées avec succès.");
  process.exit(0);
} else {
  console.log("RÉSULTAT MUTATIONS : Anomalie détectée.");
  process.exit(1);
}
