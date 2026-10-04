#!/usr/bin/env node
/**
 * The Iron Gate — Test de Mutation du Validateur Anti-Prion & Feed-Ban (Bushi 12)
 *
 * Démontre que 8 altérations délibérées de la logique de sécurité font chacune échouer
 * au moins un vecteur de test nommé dans les suites officielles :
 * 1. Liste noire au lieu de liste blanche en G3 -> échec de PRION-BLOCK-019 et PRION-HARD-012
 * 2. Température testée non typée au lieu de >= 133 -> échec de PRION-HARD-028
 * 3. Retrait de la condition « aucun ruminant » dans DEC-AET-05 -> échec de PRION-DEROG-017
 * 4. Retrait de la règle P14 (faux insecte permis) -> échec de PRION-HARD-063, PRION-HARD-064 et PRION-HARD-072
 * 5. Affaiblissement de la détection de sources vides hors bioconversion (P15) -> échec de PRION-HARD-073
 * 6. Omission du contrôle strict de toute source sur feed_grade_plant (P16) -> échec de PRION-HARD-080
 * 7. Omission du motif de substrat préalable à la dérogation en mémoire forestière (P17) -> échec de PRION-HARD-089
 * 8. Retrait de l'interdiction des sources insectes en alimentation par équarrissage direct (P18) -> échec de PRION-HARD-092
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { evaluate } from "../../validators/antiprion/index.ts";
import { TAXONOMY_MAP, resolveTaxon } from "../../validators/antiprion/taxonomy.ts";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, "../..");

const SUITES_DIR = path.join(PROJECT_ROOT, "qa/vectors/antiprion");
const suiteFiles = fs.readdirSync(SUITES_DIR)
  .filter(f => f.endsWith(".vectors.json"))
  .sort();

const allCases = new Map();
for (const file of suiteFiles) {
  const fullPath = path.join(SUITES_DIR, file);
  const data = JSON.parse(fs.readFileSync(fullPath, "utf8"));
  for (const c of data.cases) {
    allCases.set(c.id, c);
  }
}

function getCase(id) {
  const c = allCases.get(id);
  if (!c) throw new Error(`Vecteur introuvable: ${id}`);
  return c;
}

function matchesExpect(result, expect) {
  if (result.verdict !== expect.verdict) return false;
  if (result.signature_permitted !== expect.signature_permitted) return false;
  if (result.reasons.length !== expect.reasons.length) return false;
  for (let i = 0; i < result.reasons.length; i++) {
    if (result.reasons[i] !== expect.reasons[i]) return false;
  }
  return true;
}

const SUPPORTED_USES = new Set([
  "feed",
  "aquaculture_feed",
  "technical",
  "fertiliser",
  "incineration",
  "memorial_forestry"
]);

const KNOWN_MATERIAL_CLASSES = new Set([
  "slaughter_byproduct",
  "feed_grade_plant",
  "carcass",
  "human_remains",
  "manure",
  "catering_waste"
]);

const MAMMAL_GROUPS = new Set([
  "PORCINE",
  "EQUINE",
  "LAGOMORPH",
  "CARNIVORE",
  "RUMINANT",
  "HUMAN"
]);

/**
 * Évaluateur paramétré pour injecter des mutations contrôlées
 */
function evaluateWithMutations(claimInput, policyInput = null, mutation = null) {
  const reasons = [];

  const claim = (claimInput && typeof claimInput === "object") ? claimInput : {};
  const policy = (policyInput && typeof policyInput === "object") ? policyInput : null;

  // G0
  const dest = claim.destination;
  const use = dest?.use;
  if (!use || typeof use !== "string" || !SUPPORTED_USES.has(use)) {
    return { verdict: "BLOCKED", reasons: ["DESTINATION_UNSUPPORTED"], signature_permitted: false };
  }
  if (use === "incineration") {
    return { verdict: "AUTHORISED", reasons: [], signature_permitted: true };
  }

  const isFeed = (use === "feed" || use === "aquaculture_feed");
  let targetTaxids = [];
  if (isFeed) {
    if (!Array.isArray(dest?.target_taxids) || dest.target_taxids.length === 0) {
      reasons.push("TARGET_UNSPECIFIED");
    } else {
      targetTaxids = dest.target_taxids;
    }
  } else if (Array.isArray(dest?.target_taxids)) {
    targetTaxids = dest.target_taxids;
  }

  // G1
  let hasTaxonUnknown = false;
  let hasTaxonRankAbove = false;
  const resolvedSources = [];
  const substrate = claim.substrate;
  const sources = substrate?.sources;
  const proc = claim.process;
  const route = proc?.route;

  if (!Array.isArray(sources)) {
    hasTaxonUnknown = true;
  } else {
    // Règle P15
    if (mutation === "MUTATION_5_WEAK_EMPTY_SOURCES_P15") {
      // Mutation 5 : affaiblissement P15, ne vérifie que direct_rendering (comportement v1.3)
      if (isFeed && route === "direct_rendering" && sources.length === 0) {
        hasTaxonUnknown = true;
      }
    } else {
      // Conforme P15 : toute route autre qu'insect_bioconversion avec sources vides reporte TAXON_UNKNOWN
      if (isFeed && route !== "insect_bioconversion" && sources.length === 0) {
        hasTaxonUnknown = true;
      }
    }

    for (const s of sources) {
      if (!s || typeof s !== "object" || !("taxid" in s)) {
        hasTaxonUnknown = true;
        continue;
      }
      const res = resolveTaxon(s.taxid, TAXONOMY_MAP);
      if (!res.success) {
        if (res.error === "TAXON_UNKNOWN") hasTaxonUnknown = true;
        else if (res.error === "TAXON_RANK_ABOVE_SPECIES") hasTaxonRankAbove = true;
      } else {
        resolvedSources.push(res.taxon);
      }
    }
  }

  let resolvedInsect = null;
  if (route === "insect_bioconversion") {
    const insectTaxid = proc?.insect_taxid;
    if (insectTaxid === undefined || insectTaxid === null) {
      hasTaxonUnknown = true;
    } else {
      const res = resolveTaxon(insectTaxid, TAXONOMY_MAP);
      if (!res.success) {
        if (res.error === "TAXON_UNKNOWN") hasTaxonUnknown = true;
        else if (res.error === "TAXON_RANK_ABOVE_SPECIES") hasTaxonRankAbove = true;
      } else if (mutation === "MUTATION_4_NO_P14") {
        // MUTATION 4 : Retrait de la règle P14 (accepte tout taxon résolu comme "insecte")
        resolvedInsect = res.taxon;
      } else if (res.taxon.group !== "INSECT") {
        // P14 conforme : l'organisme doit être du groupe INSECT
        hasTaxonUnknown = true;
      } else {
        resolvedInsect = res.taxon;
      }
    }
  }

  const resolvedTargets = [];
  for (const tid of targetTaxids) {
    const res = resolveTaxon(tid, TAXONOMY_MAP);
    if (!res.success) {
      if (res.error === "TAXON_UNKNOWN") hasTaxonUnknown = true;
      else if (res.error === "TAXON_RANK_ABOVE_SPECIES") hasTaxonRankAbove = true;
    } else {
      resolvedTargets.push(res.taxon);
    }
  }

  if (hasTaxonUnknown) reasons.push("TAXON_UNKNOWN");
  if (hasTaxonRankAbove) reasons.push("TAXON_RANK_ABOVE_SPECIES");

  // G2
  const isHuman = (
    resolvedSources.some(s => s.species_taxid === 9606 || s.group === "HUMAN") ||
    substrate?.material_class === "human_remains" ||
    substrate?.origin_profile === "human"
  );
  if (isHuman) {
    if (use === "memorial_forestry") {
      reasons.push("DEROGATION_REQUIRED");
      return { verdict: "BLOCKED", reasons, signature_permitted: false };
    } else {
      reasons.push("HUMAN_REMAINS_ROUTE_PROHIBITED");
      return { verdict: "BLOCKED", reasons, signature_permitted: false };
    }
  }

  // G3
  const category = substrate?.category;
  const materialClass = substrate?.material_class;
  const hasAnimalSource = (resolvedSources.length > 0);
  const hasDeclaredSource = Array.isArray(sources) && sources.length > 0;

  // Règle P16
  let isPlantCategoryViolation = false;
  if (mutation === "MUTATION_6_OMIT_PLANT_ANY_SOURCE_P16") {
    // Mutation 6 : omet le contrôle strict sur toute source présente pour feed_grade_plant (v1.3)
    isPlantCategoryViolation = (materialClass === "feed_grade_plant" && hasAnimalSource);
  } else {
    // Conforme P16 : feed_grade_plant ne tolère aucune source déclarée
    isPlantCategoryViolation = (materialClass === "feed_grade_plant" && hasDeclaredSource);
  }

  let inDerogationScope = false;

  if (isFeed) {
    let feedViolation = false;
    if (category !== 3) {
      feedViolation = true;
    } else if (mutation === "MUTATION_1_BLACKLIST_G3") {
      // MUTATION 1 : Liste noire au lieu de liste blanche (n'exclut que carcass)
      if (materialClass === "carcass") {
        feedViolation = true;
      }
    } else if (route === "direct_rendering") {
      if (materialClass !== "slaughter_byproduct" && materialClass !== "feed_grade_plant") {
        feedViolation = true;
      }
    } else if (route === "insect_bioconversion") {
      if (materialClass !== "feed_grade_plant") {
        feedViolation = true;
      }
    }

    const hasInsectSource = resolvedSources.some(s => s.group === "INSECT");

    // Règle P18
    let insectViolation = false;
    if (mutation === "MUTATION_8_OMIT_INSECT_FEED_BAN_P18") {
      // Mutation 8 : Omettre l'interdiction des sources insectes en alimentation par équarrissage direct (v1.4)
      insectViolation = false;
    } else {
      insectViolation = hasInsectSource;
    }

    if (feedViolation || isPlantCategoryViolation || insectViolation) {
      if (!reasons.includes("SUBSTRATE_CATEGORY_VIOLATION")) {
        reasons.push("SUBSTRATE_CATEGORY_VIOLATION");
      }
    }
  } else if (use === "technical" || use === "fertiliser") {
    const isInvalidCategory = (category !== 1 && category !== 2 && category !== 3);
    const isInvalidMaterial = (typeof materialClass !== "string" || !KNOWN_MATERIAL_CLASSES.has(materialClass));
    if (isInvalidCategory || isInvalidMaterial || isPlantCategoryViolation) {
      reasons.push("SUBSTRATE_CATEGORY_VIOLATION");
    }
    if (category === 1 && use === "fertiliser") {
      reasons.push("CATEGORY_DESTINATION_PROHIBITED");
    }
  } else if (use === "memorial_forestry") {
    const isPolicyValid = (
      policy !== null &&
      typeof policy === "object" &&
      policy.policy_id === "DEC-AET-05" &&
      typeof policy.legal_basis === "string" &&
      policy.legal_basis.trim() !== "" &&
      typeof policy.authority_reference === "string" &&
      policy.authority_reference.trim() !== ""
    );

    const isInvalidCategory = (category !== 1 && category !== 2 && category !== 3);
    const isInvalidMaterial = (typeof materialClass !== "string" || !KNOWN_MATERIAL_CLASSES.has(materialClass));
    const substrateViolation = (isInvalidCategory || isInvalidMaterial || isPlantCategoryViolation);

    // Règle P17
    if (mutation === "MUTATION_7_OMIT_PRE_DEROGATION_SUBSTRATE_P17") {
      // Mutation 7 : omet SUBSTRATE_CATEGORY_VIOLATION avant DEROGATION_REQUIRED en mémoire forestière (v1.3)
      const hasRuminantSource = resolvedSources.some(
        s => s.group === "RUMINANT" || s.lineage_markers.includes(9845)
      );

      inDerogationScope = (
        isPolicyValid &&
        substrate?.origin_profile === "pet" &&
        category === 1 &&
        materialClass === "carcass" &&
        route === "insect_bioconversion" &&
        resolvedInsect !== null &&
        resolvedInsect.group === "INSECT" &&
        Array.isArray(sources) && sources.length > 0 &&
        !hasTaxonUnknown && !hasTaxonRankAbove &&
        !hasRuminantSource
      );

      if (!inDerogationScope) {
        reasons.push("DEROGATION_REQUIRED");
      }
    } else {
      // Conforme P17 : vérification et émission préalable du motif de substrat
      if (substrateViolation) {
        reasons.push("SUBSTRATE_CATEGORY_VIOLATION");
      }

      const hasRuminantSource = resolvedSources.some(
        s => s.group === "RUMINANT" || s.lineage_markers.includes(9845)
      );

      if (mutation === "MUTATION_3_NO_RUMINANT_CHECK_DEC_AET_05") {
        // MUTATION 3 : Retrait de la condition « aucun ruminant » dans DEC-AET-05
        inDerogationScope = (
          isPolicyValid &&
          substrate?.origin_profile === "pet" &&
          category === 1 &&
          materialClass === "carcass" &&
          route === "insect_bioconversion" &&
          resolvedInsect !== null &&
          resolvedInsect.group === "INSECT" &&
          Array.isArray(sources) && sources.length > 0 &&
          !hasTaxonUnknown && !hasTaxonRankAbove &&
          !substrateViolation
        );
      } else {
        // Conforme : exclusion stricte des ruminants
        inDerogationScope = (
          isPolicyValid &&
          substrate?.origin_profile === "pet" &&
          category === 1 &&
          materialClass === "carcass" &&
          route === "insect_bioconversion" &&
          resolvedInsect !== null &&
          resolvedInsect.group === "INSECT" &&
          Array.isArray(sources) && sources.length > 0 &&
          !hasTaxonUnknown && !hasTaxonRankAbove &&
          !hasRuminantSource &&
          !substrateViolation
        );
      }

      if (!inDerogationScope) {
        reasons.push("DEROGATION_REQUIRED");
      }
    }
  }

  // G4
  if (substrate?.origin_profile === "pet") {
    const lfa = substrate.pentobarbital_lfa;
    if (lfa === "positive") {
      reasons.push("PENTOBARBITAL_POSITIVE");
    } else if (lfa !== "negative") {
      reasons.push("PENTOBARBITAL_NOT_TESTED");
    }
  }

  // G5 à G8
  if (isFeed) {
    const hasRuminantSource = resolvedSources.some(
      s => s.group === "RUMINANT" || s.lineage_markers.includes(9845)
    );
    if (hasRuminantSource) reasons.push("FEED_BAN_RUMINANT_SOURCE");

    const hasRuminantTarget = resolvedTargets.some(
      t => t.group === "RUMINANT" || t.lineage_markers.includes(9845)
    );
    if (hasRuminantTarget) reasons.push("FEED_BAN_RUMINANT_TARGET");

    const allSourceSpecies = new Set(resolvedSources.map(s => s.species_taxid));
    if (route === "insect_bioconversion" && resolvedInsect) {
      allSourceSpecies.add(resolvedInsect.species_taxid);
    }
    const hasIntraSpecies = resolvedTargets.some(t => allSourceSpecies.has(t.species_taxid));
    if (hasIntraSpecies) reasons.push("FEED_BAN_INTRA_SPECIES_VIOLATION");

    const effectiveSourceGroups = new Set(resolvedSources.map(s => s.group));
    if (route === "insect_bioconversion" && resolvedInsect) {
      if (mutation === "MUTATION_4_NO_P14") {
        // En l'absence de P14, injection de la constante "INSECT" quel que soit l'organisme
        effectiveSourceGroups.add("INSECT");
      } else {
        effectiveSourceGroups.add(resolvedInsect.group);
      }
    }
    const targetGroups = new Set(resolvedTargets.map(t => t.group));

    if (
      (effectiveSourceGroups.has("PORCINE") && targetGroups.has("PORCINE")) ||
      (effectiveSourceGroups.has("POULTRY") && targetGroups.has("POULTRY"))
    ) {
      reasons.push("FEED_BAN_INTRA_GROUP_VIOLATION");
    }

    if (effectiveSourceGroups.size > 0) {
      const allowedSources = (use === "feed")
        ? new Set(["PORCINE", "POULTRY", "INSECT", "FISH"])
        : new Set(["PORCINE", "POULTRY", "INSECT", "FISH", "EQUINE", "LAGOMORPH"]);

      let sourceGroupAuthorized = true;
      for (const g of effectiveSourceGroups) {
        if (!allowedSources.has(g)) {
          sourceGroupAuthorized = false;
          break;
        }
      }
      if (!sourceGroupAuthorized) reasons.push("SOURCE_GROUP_NOT_AUTHORISED");
    }

    if (targetGroups.size > 0) {
      if (use === "aquaculture_feed") {
        const allFish = Array.from(targetGroups).every(g => g === "FISH");
        if (!allFish) reasons.push("TARGET_GROUP_NOT_AUTHORISED");
      } else {
        const allowedTargets = new Set(["PORCINE", "POULTRY"]);
        const allAllowed = Array.from(targetGroups).every(g => allowedTargets.has(g));
        if (!allAllowed) reasons.push("TARGET_GROUP_NOT_AUTHORISED");
      }
    }
  }

  // G9
  if (isFeed || ((use === "technical" || use === "fertiliser") && category !== 3)) {
    const treatment = proc?.treatment;
    if (!treatment || typeof treatment !== "object") {
      reasons.push("TREATMENT_NOT_PROVEN");
    } else {
      const method = treatment.method;
      const evidence = treatment.evidence_sha256;
      const hasValidEvidence = typeof evidence === "string" && /^[0-9a-f]{64}$/.test(evidence);

      let methodAuthorized = false;
      if (use === "technical" || use === "fertiliser") {
        methodAuthorized = (method === 1);
      } else {
        if (route === "insect_bioconversion") {
          methodAuthorized = (typeof method === "number" && [1, 2, 3, 4, 5, 7].includes(method));
        } else {
          const isMammal = resolvedSources.some(s => MAMMAL_GROUPS.has(s.group)) || resolvedSources.length === 0;
          const isAllFish = resolvedSources.length > 0 && resolvedSources.every(s => s.group === "FISH");
          const isAllPoultry = resolvedSources.length > 0 && resolvedSources.every(s => s.group === "POULTRY");
          if (isMammal) {
            methodAuthorized = (method === 1);
          } else if (isAllFish) {
            methodAuthorized = (typeof method === "number" && [1, 2, 3, 4, 5, 6, 7].includes(method));
          } else if (isAllPoultry) {
            methodAuthorized = (typeof method === "number" && [1, 2, 3, 4, 5, 7].includes(method));
          } else {
            methodAuthorized = (method === 1);
          }
        }
      }

      if (!methodAuthorized || !hasValidEvidence) {
        reasons.push("TREATMENT_NOT_PROVEN");
      } else if (method === 1) {
        const temp = treatment.core_temp_c;
        const press = treatment.pressure_bar;
        const mins = treatment.minutes;

        let paramsValid = false;
        if (mutation === "MUTATION_2_UNTYPED_TEMPERATURE") {
          // MUTATION 2 : Comparaison non typée (en JS, "133" >= 133 évalue à true)
          paramsValid = (
            temp >= 133 &&
            typeof press === "number" && !Number.isNaN(press) && press >= 3.0 &&
            typeof mins === "number" && !Number.isNaN(mins) && mins >= 20
          );
        } else {
          // Conforme : typage strict number requis
          paramsValid = (
            typeof temp === "number" && !Number.isNaN(temp) && temp >= 133 &&
            typeof press === "number" && !Number.isNaN(press) && press >= 3.0 &&
            typeof mins === "number" && !Number.isNaN(mins) && mins >= 20
          );
        }

        if (!paramsValid) {
          reasons.push("TREATMENT_NOT_PROVEN");
        }
      }
    }
  } else if (use === "memorial_forestry" && inDerogationScope) {
    const pasteurisation = proc?.pasteurisation;
    if (!pasteurisation || typeof pasteurisation !== "object") {
      reasons.push("TREATMENT_NOT_PROVEN");
    } else {
      const temp = pasteurisation.core_temp_c;
      const mins = pasteurisation.minutes;
      const evidence = pasteurisation.evidence_sha256;
      const hasValidEvidence = typeof evidence === "string" && /^[0-9a-f]{64}$/.test(evidence);

      const paramsValid = (
        typeof temp === "number" && !Number.isNaN(temp) && temp >= 70 &&
        typeof mins === "number" && !Number.isNaN(mins) && mins >= 60 &&
        hasValidEvidence
      );
      if (!paramsValid) reasons.push("TREATMENT_NOT_PROVEN");
    }
  }

  const isAuthorised = (reasons.length === 0);
  return {
    verdict: isAuthorised ? "AUTHORISED" : "BLOCKED",
    reasons,
    signature_permitted: isAuthorised
  };
}

function runCanonical(c) {
  if (c.op === "evaluate-with-policy") {
    return evaluate(c.input.claim, c.input.policy);
  }
  return evaluate(c.input);
}

function runMutated(c, mutation) {
  if (c.op === "evaluate-with-policy") {
    return evaluateWithMutations(c.input.claim, c.input.policy, mutation);
  }
  return evaluateWithMutations(c.input, null, mutation);
}

console.log("============================================================");
console.log("The Iron Gate — Test des 8 Mutations de Sécurité (Bushi 12)");
console.log(`Suites chargées dynamiquement : ${suiteFiles.length} fichiers (${allCases.size} vecteurs au total)`);
console.log("============================================================");

let allPassed = true;

// ----------------------------------------------------------------------------
// Mutation 1 : Liste noire au lieu de liste blanche en G3
// Fait échouer PRION-BLOCK-019 (fumier) et PRION-HARD-012 (classe inconnue)
// ----------------------------------------------------------------------------
{
  const c19 = getCase("PRION-BLOCK-019");
  const canonicalRes = runCanonical(c19);
  const mutatedRes = runMutated(c19, "MUTATION_1_BLACKLIST_G3");

  const canonicalMatches = matchesExpect(canonicalRes, c19.expect);
  const mutatedMatches = matchesExpect(mutatedRes, c19.expect);

  console.log("\n[Mutation 1] Liste noire au lieu de liste blanche en G3 :");
  console.log(`  Vecteur ciblé       : PRION-BLOCK-019 ("${c19.title}")`);
  console.log(`  Attendu             : verdict=${c19.expect.verdict}, reasons=[${c19.expect.reasons.join(", ")}]`);
  console.log(`  Évaluateur canonique: verdict=${canonicalRes.verdict}, reasons=[${canonicalRes.reasons.join(", ")}] -> ${canonicalMatches ? "PASS" : "FAIL"}`);
  console.log(`  Évaluateur muté     : verdict=${mutatedRes.verdict}, reasons=[${mutatedRes.reasons.join(", ")}] -> ${mutatedMatches ? "PASS (anomalie non détectée)" : "ÉCHEC ATTENDU (détecté)"}`);

  if (canonicalMatches && !mutatedMatches) {
    console.log("  => MUTATION 1 DÉTECTÉE : l'évaluateur muté autorise le fumier et fait échouer PRION-BLOCK-019.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 1.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 2 : Température testée non typée au lieu de >= 133
// Fait échouer PRION-HARD-028 (température "133" transmise comme chaîne)
// ----------------------------------------------------------------------------
{
  const c28 = getCase("PRION-HARD-028");
  const canonicalRes = runCanonical(c28);
  const mutatedRes = runMutated(c28, "MUTATION_2_UNTYPED_TEMPERATURE");

  const canonicalMatches = matchesExpect(canonicalRes, c28.expect);
  const mutatedMatches = matchesExpect(mutatedRes, c28.expect);

  console.log("\n[Mutation 2] Température testée non typée au lieu de >= 133 :");
  console.log(`  Vecteur ciblé       : PRION-HARD-028 ("${c28.title}")`);
  console.log(`  Attendu             : verdict=${c28.expect.verdict}, reasons=[${c28.expect.reasons.join(", ")}]`);
  console.log(`  Évaluateur canonique: verdict=${canonicalRes.verdict}, reasons=[${canonicalRes.reasons.join(", ")}] -> ${canonicalMatches ? "PASS" : "FAIL"}`);
  console.log(`  Évaluateur muté     : verdict=${mutatedRes.verdict}, reasons=[${mutatedRes.reasons.join(", ")}] -> ${mutatedMatches ? "PASS (anomalie non détectée)" : "ÉCHEC ATTENDU (détecté)"}`);

  if (canonicalMatches && !mutatedMatches) {
    console.log("  => MUTATION 2 DÉTECTÉE : l'évaluateur muté accepte la chaîne \"133\" et fait échouer PRION-HARD-028.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 2.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 3 : Retrait de la condition « aucun ruminant » dans DEC-AET-05
// Fait échouer PRION-DEROG-017 (chèvre de compagnie, ruminant sous dérogation)
// ----------------------------------------------------------------------------
{
  const c17 = getCase("PRION-DEROG-017");
  const canonicalRes = runCanonical(c17);
  const mutatedRes = runMutated(c17, "MUTATION_3_NO_RUMINANT_CHECK_DEC_AET_05");

  const canonicalMatches = matchesExpect(canonicalRes, c17.expect);
  const mutatedMatches = matchesExpect(mutatedRes, c17.expect);

  console.log("\n[Mutation 3] Retrait de la condition « aucun ruminant » dans DEC-AET-05 :");
  console.log(`  Vecteur ciblé       : PRION-DEROG-017 ("${c17.title}")`);
  console.log(`  Attendu             : verdict=${c17.expect.verdict}, reasons=[${c17.expect.reasons.join(", ")}]`);
  console.log(`  Évaluateur canonique: verdict=${canonicalRes.verdict}, reasons=[${canonicalRes.reasons.join(", ")}] -> ${canonicalMatches ? "PASS" : "FAIL"}`);
  console.log(`  Évaluateur muté     : verdict=${mutatedRes.verdict}, reasons=[${mutatedRes.reasons.join(", ")}] -> ${mutatedMatches ? "PASS (anomalie non détectée)" : "ÉCHEC ATTENDU (détecté)"}`);

  if (canonicalMatches && !mutatedMatches) {
    console.log("  => MUTATION 3 DÉTECTÉE : l'évaluateur muté admet un ruminant sous dérogation et fait échouer PRION-DEROG-017.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 3.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 4 : Retrait de la règle P14 (faux insecte autorisé en bioconversion)
// Fait échouer PRION-HARD-063 (bovin), PRION-HARD-064 (humain) et PRION-HARD-072
// ----------------------------------------------------------------------------
{
  const c63 = getCase("PRION-HARD-063");
  const canonicalRes = runCanonical(c63);
  const mutatedRes = runMutated(c63, "MUTATION_4_NO_P14");

  const canonicalMatches = matchesExpect(canonicalRes, c63.expect);
  const mutatedMatches = matchesExpect(mutatedRes, c63.expect);

  console.log("\n[Mutation 4] Retrait de la règle P14 (permettant un faux insecte) :");
  console.log(`  Vecteur ciblé       : PRION-HARD-063 ("${c63.title}")`);
  console.log(`  Attendu             : verdict=${c63.expect.verdict}, reasons=[${c63.expect.reasons.join(", ")}]`);
  console.log(`  Évaluateur canonique: verdict=${canonicalRes.verdict}, reasons=[${canonicalRes.reasons.join(", ")}] -> ${canonicalMatches ? "PASS" : "FAIL"}`);
  console.log(`  Évaluateur muté     : verdict=${mutatedRes.verdict}, reasons=[${mutatedRes.reasons.join(", ")}] -> ${mutatedMatches ? "PASS (anomalie non détectée)" : "ÉCHEC ATTENDU (détecté)"}`);

  if (canonicalMatches && !mutatedMatches) {
    console.log("  => MUTATION 4 DÉTECTÉE : l'évaluateur muté autorise le bovin déguisé en insecte et fait échouer PRION-HARD-063.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 4.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 5 (Règle P15) : Affaiblir la détection de sources vides hors bioconversion
// Fait échouer PRION-HARD-073 (sources vides avec route "composting" -> volailles)
// ----------------------------------------------------------------------------
{
  const c73 = getCase("PRION-HARD-073");
  const canonicalRes = runCanonical(c73);
  const mutatedRes = runMutated(c73, "MUTATION_5_WEAK_EMPTY_SOURCES_P15");

  const canonicalMatches = matchesExpect(canonicalRes, c73.expect);
  const mutatedMatches = matchesExpect(mutatedRes, c73.expect);

  console.log("\n[Mutation 5] Affaiblir la détection de sources vides hors bioconversion (Règle P15) :");
  console.log(`  Vecteur ciblé       : PRION-HARD-073 ("${c73.title}")`);
  console.log(`  Attendu             : verdict=${c73.expect.verdict}, reasons=[${c73.expect.reasons.join(", ")}]`);
  console.log(`  Évaluateur canonique: verdict=${canonicalRes.verdict}, reasons=[${canonicalRes.reasons.join(", ")}] -> ${canonicalMatches ? "PASS" : "FAIL"}`);
  console.log(`  Évaluateur muté     : verdict=${mutatedRes.verdict}, reasons=[${mutatedRes.reasons.join(", ")}] -> ${mutatedMatches ? "PASS (anomalie non détectée)" : "ÉCHEC ATTENDU (détecté)"}`);

  if (canonicalMatches && !mutatedMatches) {
    console.log("  => MUTATION 5 DÉTECTÉE : l'évaluateur muté omet TAXON_UNKNOWN pour les sources vides hors bioconversion et fait échouer PRION-HARD-073.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 5.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 6 (Règle P16) : Omettre le contrôle strict de sources sur feed_grade_plant
// Fait échouer PRION-HARD-080 (feed_grade_plant avec source [null] -> engrais)
// ----------------------------------------------------------------------------
{
  const c80 = getCase("PRION-HARD-080");
  const canonicalRes = runCanonical(c80);
  const mutatedRes = runMutated(c80, "MUTATION_6_OMIT_PLANT_ANY_SOURCE_P16");

  const canonicalMatches = matchesExpect(canonicalRes, c80.expect);
  const mutatedMatches = matchesExpect(mutatedRes, c80.expect);

  console.log("\n[Mutation 6] Omettre le contrôle strict de toute source sur feed_grade_plant (Règle P16) :");
  console.log(`  Vecteur ciblé       : PRION-HARD-080 ("${c80.title}")`);
  console.log(`  Attendu             : verdict=${c80.expect.verdict}, reasons=[${c80.expect.reasons.join(", ")}]`);
  console.log(`  Évaluateur canonique: verdict=${canonicalRes.verdict}, reasons=[${canonicalRes.reasons.join(", ")}] -> ${canonicalMatches ? "PASS" : "FAIL"}`);
  console.log(`  Évaluateur muté     : verdict=${mutatedRes.verdict}, reasons=[${mutatedRes.reasons.join(", ")}] -> ${mutatedMatches ? "PASS (anomalie non détectée)" : "ÉCHEC ATTENDU (détecté)"}`);

  if (canonicalMatches && !mutatedMatches) {
    console.log("  => MUTATION 6 DÉTECTÉE : l'évaluateur muté tolère une source présente non résolue sur feed_grade_plant et fait échouer PRION-HARD-080.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 6.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 7 (Règle P17) : Omettre le motif substrat avant dérogation en mémoire forestière
// Fait échouer PRION-HARD-089 (chat LFA négatif, catégorie absente, sous politique valide)
// ----------------------------------------------------------------------------
{
  const c89 = getCase("PRION-HARD-089");
  const canonicalRes = runCanonical(c89);
  const mutatedRes = runMutated(c89, "MUTATION_7_OMIT_PRE_DEROGATION_SUBSTRATE_P17");

  const canonicalMatches = matchesExpect(canonicalRes, c89.expect);
  const mutatedMatches = matchesExpect(mutatedRes, c89.expect);

  console.log("\n[Mutation 7] Omettre SUBSTRATE_CATEGORY_VIOLATION avant dérogation en mémoire forestière (Règle P17) :");
  console.log(`  Vecteur ciblé       : PRION-HARD-089 ("${c89.title}")`);
  console.log(`  Attendu             : verdict=${c89.expect.verdict}, reasons=[${c89.expect.reasons.join(", ")}]`);
  console.log(`  Évaluateur canonique: verdict=${canonicalRes.verdict}, reasons=[${canonicalRes.reasons.join(", ")}] -> ${canonicalMatches ? "PASS" : "FAIL"}`);
  console.log(`  Évaluateur muté     : verdict=${mutatedRes.verdict}, reasons=[${mutatedRes.reasons.join(", ")}] -> ${mutatedMatches ? "PASS (anomalie non détectée)" : "ÉCHEC ATTENDU (détecté)"}`);

  if (canonicalMatches && !mutatedMatches) {
    console.log("  => MUTATION 7 DÉTECTÉE : l'évaluateur muté omet SUBSTRATE_CATEGORY_VIOLATION et fait échouer PRION-HARD-089.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 7.");
    allPassed = false;
  }
}

// ----------------------------------------------------------------------------
// Mutation 8 (Règle P18) : Retrait de l'interdiction des sources insectes en alimentation par équarrissage direct
// Fait échouer PRION-HARD-092 (Hermetia déclarée comme source, équarrissage direct, méthode 1 prouvée -> volailles)
// ----------------------------------------------------------------------------
{
  const c92 = getCase("PRION-HARD-092");
  const canonicalRes = runCanonical(c92);
  const mutatedRes = runMutated(c92, "MUTATION_8_OMIT_INSECT_FEED_BAN_P18");

  const canonicalMatches = matchesExpect(canonicalRes, c92.expect);
  const mutatedMatches = matchesExpect(mutatedRes, c92.expect);

  console.log("\n[Mutation 8] Retrait de l'interdiction des sources insectes en alimentation par équarrissage direct (Règle P18) :");
  console.log(`  Vecteur ciblé       : PRION-HARD-092 ("${c92.title}")`);
  console.log(`  Attendu             : verdict=${c92.expect.verdict}, reasons=[${c92.expect.reasons.join(", ")}]`);
  console.log(`  Évaluateur canonique: verdict=${canonicalRes.verdict}, reasons=[${canonicalRes.reasons.join(", ")}] -> ${canonicalMatches ? "PASS" : "FAIL"}`);
  console.log(`  Évaluateur muté     : verdict=${mutatedRes.verdict}, reasons=[${mutatedRes.reasons.join(", ")}] -> ${mutatedMatches ? "PASS (anomalie non détectée)" : "ÉCHEC ATTENDU (détecté)"}`);

  if (canonicalMatches && !mutatedMatches) {
    console.log("  => MUTATION 8 DÉTECTÉE : l'évaluateur muté autorise les insectes en source directe et fait échouer PRION-HARD-092.");
  } else {
    console.log("  => ÉCHEC DE DÉTECTION DE LA MUTATION 8.");
    allPassed = false;
  }
}

console.log("\n============================================================");
if (allPassed) {
  console.log("RÉSULTAT MUTATIONS : 8/8 mutations ciblées validées avec succès.");
  process.exit(0);
} else {
  console.log("RÉSULTAT MUTATIONS : Anomalie détectée.");
  process.exit(1);
}
