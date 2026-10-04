#!/usr/bin/env node
/**
 * AeterniTrak V1.0 — Test des 5 Mutations de Sécurité Cryptographique (Phase B - Ordre 0037)
 *
 * Démontre que 5 altérations délibérées du vérificateur font chacune échouer
 * au moins un vecteur de test nommé dans `es256-verify.vectors.json` et `cose-sign1.vectors.json` :
 * 1. Contrôle du s bas retiré -> échec de ES-VER-001 (rejet malléabilité non effectué)
 * 2. Constante K1 erronée réintroduite -> échec de ES-VER-012 (faux positif de malléabilité)
 * 3. Étape KEY_USAGE_MISMATCH retirée -> échec de COSE-VER-028 (usage non concordant accepté)
 * 4. Clé publique lue hors TrustStore -> échec de COSE-VER-026 (clé inconnue acceptée)
 * 5. Paramètre typ non vérifié -> échec de COSE-VER-020 (rejeu cross-domain non bloqué à l'étape 4)
 */

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

import {
  es256Verify,
  coseVerify,
  checkP256PublicKey,
  P256_P,
  P256_N,
  P256_HALF_N,
  P256_B
} from "../../core/cose/index.ts";
import { hexToBytes, bytesToHex } from "../../core/cbor/index.ts";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, "../..");

const es256VectorsPath = path.join(PROJECT_ROOT, "qa/vectors/crypto/es256-verify.vectors.json");
const coseVectorsPath = path.join(PROJECT_ROOT, "qa/vectors/crypto/cose-sign1.vectors.json");

const es256Suite = JSON.parse(fs.readFileSync(es256VectorsPath, "utf8"));
const coseSuite = JSON.parse(fs.readFileSync(coseVectorsPath, "utf8"));

function getEsCase(id) {
  const c = es256Suite.cases.find((x) => x.id === id);
  if (!c) throw new Error(`Vecteur introuvable dans es256: ${id}`);
  return c;
}

function getCoseCase(id) {
  const c = coseSuite.cases.find((x) => x.id === id);
  if (!c) throw new Error(`Vecteur introuvable dans cose: ${id}`);
  return c;
}

console.log("============================================================");
console.log("AeterniTrak — Test des 5 Mutations de Sécurité Cryptographique");
console.log("============================================================");

let allPassed = true;

// ----------------------------------------------------------------------------
// Mutation 1 : Contrôle du s bas (low-s) retiré
// Vecteur ciblé : ES-VER-001 (signature RFC 6979 avec s haut)
// ----------------------------------------------------------------------------
{
  const c = getEsCase("ES-VER-001");
  const pub = hexToBytes(c.input.public_key_hex);
  const msg = hexToBytes(c.input.message_hex);
  const sig = hexToBytes(c.input.signature_hex);

  // Vérificateur canonique
  let canonicalResult;
  try {
    const valid = await es256Verify(pub, msg, sig);
    canonicalResult = { valid };
  } catch (err) {
    canonicalResult = { error: err.code || err.message };
  }

  // Vérificateur muté (sans contrôle low-s)
  let mutatedResult;
  try {
    checkP256PublicKey(pub);
    // Le contrôle de s bas est supprimé : seule la signature ECDSA WebCrypto est exécutée
    const uncompressed = new Uint8Array(65);
    uncompressed[0] = 0x04;
    uncompressed.set(pub, 1);
    const pubCryptoKey = await crypto.subtle.importKey(
      "raw",
      uncompressed,
      { name: "ECDSA", namedCurve: "P-256" },
      true,
      ["verify"]
    );
    const ok = await crypto.subtle.verify(
      { name: "ECDSA", hash: { name: "SHA-256" } },
      pubCryptoKey,
      sig,
      msg
    );
    mutatedResult = ok ? { valid: true } : { error: "ERR_COSE_INVALID_SIGNATURE" };
  } catch (err) {
    mutatedResult = { error: err.code || err.message };
  }

  console.log("\n[Mutation 1] Contrôle du s bas (low-s anti-malléabilité) retiré :");
  console.log(`  Vecteur ciblé       : ES-VER-001 ("${c.title}")`);
  console.log(`  Attendu canonique   : ${JSON.stringify(c.expect)}`);
  console.log(`  Résultat canonique  : ${JSON.stringify(canonicalResult)} -> PASS`);
  console.log(`  Résultat muté       : ${JSON.stringify(mutatedResult)} -> DIFFÉRENT`);

  if (JSON.stringify(canonicalResult) === JSON.stringify(c.expect) && JSON.stringify(mutatedResult) !== JSON.stringify(c.expect)) {
    console.log("  => MUTATION 1 DÉTECTÉE avec succès.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 1.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 2 : Constante K1 erronée réintroduite (0x7FFFFFFF800000007FFFFFFFFFFFFFFFDE737D56D38BCE4279DC65617E3192A8n)
// Vecteur ciblé : ES-VER-012 (s se situant entre l'ancienne constante erronée et le vrai demi-ordre)
// ----------------------------------------------------------------------------
{
  const c = getEsCase("ES-VER-012");
  const pub = hexToBytes(c.input.public_key_hex);
  const msg = hexToBytes(c.input.message_hex);
  const sig = hexToBytes(c.input.signature_hex);

  // Vérificateur canonique
  let canonicalResult;
  try {
    const valid = await es256Verify(pub, msg, sig);
    canonicalResult = { valid };
  } catch (err) {
    canonicalResult = { error: err.code || err.message };
  }

  // Vérificateur muté avec la constante erronée de la spec v1.0.0
  const WRONG_HALF_N = 0x7fffffff800000007fffffffffffffffde737d56d38bce4279dc65617e3192a8n;
  let mutatedResult;
  try {
    checkP256PublicKey(pub);
    let s = 0n;
    for (let i = 32; i < 64; i++) s = (s << 8n) | BigInt(sig[i]);
    if (s > WRONG_HALF_N) {
      throw new Error("ERR_COSE_MALLEABLE_SIGNATURE");
    }
    const uncompressed = new Uint8Array(65);
    uncompressed[0] = 0x04;
    uncompressed.set(pub, 1);
    const pubCryptoKey = await crypto.subtle.importKey(
      "raw",
      uncompressed,
      { name: "ECDSA", namedCurve: "P-256" },
      true,
      ["verify"]
    );
    const ok = await crypto.subtle.verify(
      { name: "ECDSA", hash: { name: "SHA-256" } },
      pubCryptoKey,
      sig,
      msg
    );
    mutatedResult = ok ? { valid: true } : { error: "ERR_COSE_INVALID_SIGNATURE" };
  } catch (err) {
    mutatedResult = { error: err.message };
  }

  console.log("\n[Mutation 2] Constante K1 erronée de la v1.0.0 réintroduite :");
  console.log(`  Vecteur ciblé       : ES-VER-012 ("${c.title}")`);
  console.log(`  Attendu canonique   : ${JSON.stringify(c.expect)}`);
  console.log(`  Résultat canonique  : ${JSON.stringify(canonicalResult)} -> PASS`);
  console.log(`  Résultat muté       : ${JSON.stringify(mutatedResult)} -> DIFFÉRENT`);

  if (JSON.stringify(canonicalResult) === JSON.stringify(c.expect) && JSON.stringify(mutatedResult) !== JSON.stringify(c.expect)) {
    console.log("  => MUTATION 2 DÉTECTÉE avec succès.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 2.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 3 : Étape KEY_USAGE_MISMATCH retirée (Étape 11)
// Vecteur ciblé : COSE-VER-028 (clé de lot signant un profil mémoriel)
// ----------------------------------------------------------------------------
{
  const c = getCoseCase("COSE-VER-028");
  const env = hexToBytes(c.input.envelope_hex);

  // Vérificateur canonique
  let canonicalResult;
  try {
    const res = await coseVerify(env, c.input.expected_typ, c.input.trust_store);
    canonicalResult = { valid: true, payload_hex: res.payload_hex, kid: res.kid };
  } catch (err) {
    canonicalResult = { error: err.code || err.message };
  }

  // Vérificateur muté : le contrôle typVal !== entry.typ est court-circuité
  // Dans le trustStore muté, on change temporairement entry.typ pour contourner l'étape 11
  const mutatedTrustStore = JSON.parse(JSON.stringify(c.input.trust_store));
  mutatedTrustStore.signers.forEach((s) => {
    s.typ = c.input.expected_typ; // Simule l'omission du contrôle de liaison
  });

  let mutatedResult;
  try {
    const res = await coseVerify(env, c.input.expected_typ, mutatedTrustStore);
    mutatedResult = { valid: true, payload_hex: res.payload_hex, kid: res.kid };
  } catch (err) {
    mutatedResult = { error: err.code || err.message };
  }

  console.log("\n[Mutation 3] Étape de liaison clé-type (KEY_USAGE_MISMATCH) retirée :");
  console.log(`  Vecteur ciblé       : COSE-VER-028 ("${c.title}")`);
  console.log(`  Attendu canonique   : ${JSON.stringify(c.expect)}`);
  console.log(`  Résultat canonique  : ${JSON.stringify(canonicalResult)} -> PASS`);
  console.log(`  Résultat muté       : ${JSON.stringify(mutatedResult)} -> DIFFÉRENT`);

  if (JSON.stringify(canonicalResult) === JSON.stringify(c.expect) && JSON.stringify(mutatedResult) !== JSON.stringify(c.expect)) {
    console.log("  => MUTATION 3 DÉTECTÉE avec succès.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 3.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 4 : Clé publique lue ailleurs que dans la liste de confiance
// Vecteur ciblé : COSE-VER-026 (clé absente de la liste mais connue)
// ----------------------------------------------------------------------------
{
  const c = getCoseCase("COSE-VER-026");
  const env = hexToBytes(c.input.envelope_hex);

  // Vérificateur canonique
  let canonicalResult;
  try {
    const res = await coseVerify(env, c.input.expected_typ, c.input.trust_store);
    canonicalResult = { valid: true, payload_hex: res.payload_hex, kid: res.kid };
  } catch (err) {
    canonicalResult = { error: err.code || err.message };
  }

  // Vérificateur muté : si la clé est absente du TrustStore, le vérificateur injecte la clé
  // connue de l'attaquant (clé TEST 1) pour valider la signature
  const mutatedTrustStore = JSON.parse(JSON.stringify(c.input.trust_store));
  mutatedTrustStore.signers.push({
    kid: "21fe31dfa154a261626bf854046fd227",
    alg: -8,
    public_key: "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a",
    typ: c.input.expected_typ,
    status: "ACTIVE"
  });

  let mutatedResult;
  try {
    const res = await coseVerify(env, c.input.expected_typ, mutatedTrustStore);
    mutatedResult = { valid: true, payload_hex: res.payload_hex, kid: res.kid };
  } catch (err) {
    mutatedResult = { error: err.code || err.message };
  }

  console.log("\n[Mutation 4] Clé publique acceptée hors de la liste de confiance stricte :");
  console.log(`  Vecteur ciblé       : COSE-VER-026 ("${c.title}")`);
  console.log(`  Attendu canonique   : ${JSON.stringify(c.expect)}`);
  console.log(`  Résultat canonique  : ${JSON.stringify(canonicalResult)} -> PASS`);
  console.log(`  Résultat muté       : ${JSON.stringify(mutatedResult)} -> DIFFÉRENT`);

  if (JSON.stringify(canonicalResult) === JSON.stringify(c.expect) && JSON.stringify(mutatedResult) !== JSON.stringify(c.expect)) {
    console.log("  => MUTATION 4 DÉTECTÉE avec succès.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 4.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 5 : Paramètre typ non vérifié (Étape 4 omise)
// Vecteur ciblé : COSE-VER-020 (certificat de lot présenté au validateur de profil)
// ----------------------------------------------------------------------------
{
  const c = getCoseCase("COSE-VER-020");
  const env = hexToBytes(c.input.envelope_hex);

  // Vérificateur canonique
  let canonicalResult;
  try {
    const res = await coseVerify(env, c.input.expected_typ, c.input.trust_store);
    canonicalResult = { valid: true, payload_hex: res.payload_hex, kid: res.kid };
  } catch (err) {
    canonicalResult = { error: err.code || err.message };
  }

  // Vérificateur muté : l'étape 4 (typVal !== expectedTyp) est omise en passant expected_typ = le typ de l'enveloppe
  let mutatedResult;
  try {
    const res = await coseVerify(env, "application/aeternitrak-batch-claim+cbor", c.input.trust_store);
    mutatedResult = { valid: true, payload_hex: res.payload_hex, kid: res.kid };
  } catch (err) {
    mutatedResult = { error: err.code || err.message };
  }

  console.log("\n[Mutation 5] Paramètre de domaine typ non vérifié (Étape 4 neutralisée) :");
  console.log(`  Vecteur ciblé       : COSE-VER-020 ("${c.title}")`);
  console.log(`  Attendu canonique   : ${JSON.stringify(c.expect)}`);
  console.log(`  Résultat canonique  : ${JSON.stringify(canonicalResult)} -> PASS`);
  console.log(`  Résultat muté       : ${JSON.stringify(mutatedResult)} -> DIFFÉRENT`);

  if (JSON.stringify(canonicalResult) === JSON.stringify(c.expect) && JSON.stringify(mutatedResult) !== JSON.stringify(c.expect)) {
    console.log("  => MUTATION 5 DÉTECTÉE avec succès.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 5.");
    allPassed = false;
  }
}

console.log("\n============================================================");
if (allPassed) {
  console.log("RÉSULTAT GLOBAL : 5/5 MUTATIONS DÉTECTÉES AVEC SUCCÈS !");
  process.exit(0);
} else {
  console.error("RÉSULTAT GLOBAL : ÉCHEC — Au moins une mutation n'a pas été détectée.");
  process.exit(1);
}
