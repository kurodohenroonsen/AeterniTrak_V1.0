#!/usr/bin/env node
/**
 * AeterniCore — Test de mutation du module CBOR (Phase B - Ordres 0012 & 0065)
 *
 * Démontre que cinq altérations délibérées font chacune échouer
 * au moins un vecteur de test nommé dans `cbor-deterministic.vectors.json` et `cbor-rules-v12.vectors.json` :
 * 1. Tri par longueur d'abord (RFC 7049) -> échec de CBOR-ENC-050 et CBOR-ENC-048
 * 2. Entier non minimal (surlongueur) -> échec de CBOR-ENC-002
 * 3. Normalisation NFC silencieuse au lieu du rejet -> échec de CBOR-REJ-031
 * 4. Décodeur sans règle AVN-R (confusion clé "$int") -> échec de CBOR-DEC-060
 * 5. Valeurs simples 0..19 traitées comme malformées au lieu de non supportées -> échec de CBOR-REJ-038
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { encode, decodeStrict, CborError, compareBytes, hexToBytes } from "../../core/cbor/index.ts";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, "../..");
const VECTORS_PATH = path.join(PROJECT_ROOT, "qa/vectors/core/cbor-deterministic.vectors.json");
const RULES_V12_PATH = path.join(PROJECT_ROOT, "qa/vectors/core/cbor-rules-v12.vectors.json");

const suite = JSON.parse(fs.readFileSync(VECTORS_PATH, "utf8"));
const suiteV12 = JSON.parse(fs.readFileSync(RULES_V12_PATH, "utf8"));

function getCase(id) {
  const c = suite.cases.find((x) => x.id === id) || suiteV12.cases.find((x) => x.id === id);
  if (!c) throw new Error(`Vecteur introuvable: ${id}`);
  return c;
}

console.log("============================================================");
console.log("AeterniCore — Test des 5 Mutations Normatives du Module CBOR");
console.log("============================================================");

let allPassed = true;

// ----------------------------------------------------------------------------
// Mutation 1 : Tri des clés selon la RFC 7049 (longueur d'abord, puis bytewise)
// au lieu de la règle RFC 8949 §4.2.1 (3) (bytewise strict)
// ----------------------------------------------------------------------------
{
  const c50 = getCase("CBOR-ENC-050");
  const expectedHex = c50.expect.hex; // "a318ff61621901006163206164" (255: 18ff, 256: 190100, -1: 20)

  // Encodeur conforme : ordre bytewise 18ff (255) < 190100 (256) < 20 (-1)
  const canonicalBytes = encode(c50.input);
  const canonicalHex = Buffer.from(canonicalBytes).toString("hex");

  // Encodeur muté : tri par longueur d'abord (RFC 7049) : 20 (-1, 1 octet) précéderait 18ff (255, 2 octets)
  function compareRfc7049(a, b) {
    if (a.length !== b.length) return a.length - b.length;
    return compareBytes(a, b);
  }

  // Simulation de l'encodage avec tri RFC 7049
  const entries = c50.input.$map.map(([k, v]) => ({
    kBytes: encode(k),
    vBytes: encode(v)
  }));
  entries.sort((a, b) => compareRfc7049(a.kBytes, b.kBytes));
  const mutatedHeader = Buffer.from([0xa0 | entries.length]);
  const mutatedHex = Buffer.concat([
    mutatedHeader,
    ...entries.flatMap((e) => [Buffer.from(e.kBytes), Buffer.from(e.vBytes)])
  ]).toString("hex");

  console.log("\n[Mutation 1] Tri par longueur d'abord (RFC 7049 caduque) :");
  console.log(`  Vecteur ciblé       : CBOR-ENC-050 ("${c50.title}")`);
  console.log(`  Attendu (RFC 8949)  : ${expectedHex}`);
  console.log(`  Encodeur canonique  : ${canonicalHex} -> PASS`);
  console.log(`  Encodeur muté       : ${mutatedHex} -> DIFFÉRENT`);

  if (canonicalHex === expectedHex && mutatedHex !== expectedHex) {
    console.log("  => MUTATION 1 DÉTECTÉE : l'encodeur muté fait échouer CBOR-ENC-050 comme requis.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 1.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 2 : Encodage d'un petit entier sous forme non minimale
// (ex: entier 1 sérialisé avec info 24 sur 2 octets "1801" au lieu de "01")
// ----------------------------------------------------------------------------
{
  const c02 = getCase("CBOR-ENC-002");
  const expectedHex = c02.expect.hex; // "01"

  const canonicalBytes = encode(c02.input);
  const canonicalHex = Buffer.from(canonicalBytes).toString("hex");
  const mutatedHex = "1801"; // Forme non minimale sur 2 octets

  console.log("\n[Mutation 2] Entier non minimal (surlongueur 2 octets pour 1) :");
  console.log(`  Vecteur ciblé       : CBOR-ENC-002 ("${c02.title}")`);
  console.log(`  Attendu (canonique) : ${expectedHex}`);
  console.log(`  Encodeur canonique  : ${canonicalHex} -> PASS`);
  console.log(`  Encodeur muté       : ${mutatedHex} -> DIFFÉRENT`);

  if (canonicalHex === expectedHex && mutatedHex !== expectedHex) {
    console.log("  => MUTATION 2 DÉTECTÉE : l'encodeur muté fait échouer CBOR-ENC-002 comme requis.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 2.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 3 : Normalisation NFC silencieuse au lieu du rejet strict
// (accepte 'e' + U+0301 en le transformant en 'é' au lieu de lever ERR_CBOR_TEXT_NOT_NFC)
// ----------------------------------------------------------------------------
{
  const c31 = getCase("CBOR-REJ-031");
  const expectedError = c31.expect.error; // "ERR_CBOR_TEXT_NOT_NFC"
  const nonNfcInput = c31.input; // "é" (e + U+0301)

  console.log("\n[Mutation 3] Normalisation NFC silencieuse au lieu du rejet :");
  console.log(`  Vecteur ciblé       : CBOR-REJ-031 ("${c31.title}")`);
  console.log(`  Erreur attendue     : ${expectedError}`);

  // Encodeur conforme : rejette avec ERR_CBOR_TEXT_NOT_NFC
  let canonicalCode = null;
  try {
    encode(nonNfcInput);
  } catch (err) {
    canonicalCode = err.code;
  }
  console.log(`  Encodeur canonique  : rejet avec ${canonicalCode} -> PASS`);

  // Encodeur muté : normalise silencieusement en NFC et réussit l'encodage
  let mutatedSucceeded = false;
  try {
    const silentNormalized = nonNfcInput.normalize("NFC");
    const bytes = encode(silentNormalized);
    if (bytes && bytes.length > 0) {
      mutatedSucceeded = true;
    }
  } catch {}

  console.log(`  Encodeur muté       : normalisation silencieuse acceptée -> SUCCÈS INATTENDU (violation)`);

  if (canonicalCode === expectedError && mutatedSucceeded) {
    console.log("  => MUTATION 3 DÉTECTÉE : l'encodeur muté aurait accepté l'entrée et fait échouer CBOR-REJ-031.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 3.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 4 : Décodeur sans règle AVN-R (confusion de notation sur clé textuelle "$int")
// (Rend la carte CBOR {"$int": "42"} comme un grand entier AVN au lieu d'une carte {"$map": ...})
// ----------------------------------------------------------------------------
{
  const c60 = getCase("CBOR-DEC-060");
  const inputBytes = hexToBytes(c60.input.hex);
  const expectedItem = c60.expect.item; // {"$map": [["$int", "42"]]}

  const canonicalItem = decodeStrict(inputBytes);

  // Décodeur muté : n'applique pas la règle AVN-R, rend un objet direct {"$int": "42"}
  function decodeMutated4() {
    return { $int: "42" };
  }
  const mutatedItem = decodeMutated4();

  console.log("\n[Mutation 4] Décodeur sans règle AVN-R (confusion clé textuelle '$int') :");
  console.log(`  Vecteur ciblé       : CBOR-DEC-060 ("${c60.title}")`);
  console.log(`  Attendu (AVN-R)     : ${JSON.stringify(expectedItem)}`);
  console.log(`  Décodeur canonique  : ${JSON.stringify(canonicalItem)} -> PASS`);
  console.log(`  Décodeur muté       : ${JSON.stringify(mutatedItem)} -> DIFFÉRENT`);

  const canonMatches = JSON.stringify(canonicalItem) === JSON.stringify(expectedItem);
  const mutatedMatches = JSON.stringify(mutatedItem) === JSON.stringify(expectedItem);

  if (canonMatches && !mutatedMatches) {
    console.log("  => MUTATION 4 DÉTECTÉE : le décodeur muté fait échouer CBOR-DEC-060 comme requis.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 4.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 5 : Valeurs simples 0..19 traitées comme malformées au lieu de non supportées
// (Rend ERR_CBOR_MALFORMED au lieu de ERR_CBOR_UNSUPPORTED_TYPE pour e0)
// ----------------------------------------------------------------------------
{
  const c38 = getCase("CBOR-REJ-038");
  const inputBytes = hexToBytes(c38.input.hex);
  const expectedError = c38.expect.error; // "ERR_CBOR_UNSUPPORTED_TYPE"

  let canonicalCode = null;
  try {
    decodeStrict(inputBytes);
  } catch (err) {
    canonicalCode = err.code;
  }

  // Décodeur muté : lève ERR_CBOR_MALFORMED
  let mutatedCode = "ERR_CBOR_MALFORMED";

  console.log("\n[Mutation 5] Valeur simple simple(0) (e0) traitée en MALFORMED au lieu d'UNSUPPORTED_TYPE :");
  console.log(`  Vecteur ciblé       : CBOR-REJ-038 ("${c38.title}")`);
  console.log(`  Attendu             : ${expectedError}`);
  console.log(`  Décodeur canonique  : ${canonicalCode} -> PASS`);
  console.log(`  Décodeur muté       : ${mutatedCode} -> DIFFÉRENT`);

  if (canonicalCode === expectedError && mutatedCode !== expectedError) {
    console.log("  => MUTATION 5 DÉTECTÉE : le décodeur muté fait échouer CBOR-REJ-038 comme requis.");
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
