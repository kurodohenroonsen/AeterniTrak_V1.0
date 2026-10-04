/**
 * Moteur pur d'évaluation sanitaire The Iron Gate (La Porte de Fer)
 * Conforme à AET-SPEC-PRION-001 v1.3.0 et aux règles P1 à P14
 */

import type {
  BatchClaimInput,
  PolicyInput,
  EvaluationResult,
  ResolvedTaxon,
  TaxonEntry,
  SubstrateInput,
  ProcessInput,
  DestinationInput,
  TreatmentInput,
  PasteurisationInput
} from "./types.ts";
import { TAXONOMY_MAP, resolveTaxon } from "./taxonomy.ts";

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

const HEX_SHA256_REGEX = /^[0-9a-f]{64}$/;

/**
 * Fonction pure d'évaluation d'une revendication de lot.
 * Évalue de manière séquentielle et exhaustive les 10 portes de fer (G0 à G9).
 * Ne dépend d'aucun état mutable externe.
 */
export function evaluate(
  claimInput: unknown,
  policyInput: unknown = null,
  taxonomyMap: Map<number, TaxonEntry> = TAXONOMY_MAP
): EvaluationResult {
  const reasons: string[] = [];

  const claim = (claimInput && typeof claimInput === "object") ? (claimInput as BatchClaimInput) : {};
  const policy = (policyInput && typeof policyInput === "object") ? (policyInput as PolicyInput) : null;

  // =========================================================================
  // PORTE G0 : Destination & Spécification des cibles
  // =========================================================================
  const dest: DestinationInput | undefined = claim.destination;
  const use = dest?.use;

  // Whitelist d'usage : arrêt anticipé si usage non supporté
  if (!use || typeof use !== "string" || !SUPPORTED_USES.has(use)) {
    return {
      verdict: "BLOCKED",
      reasons: ["DESTINATION_UNSUPPORTED"],
      signature_permitted: false
    };
  }

  // Règle P11 : L'incinération est toujours autorisée de plein droit.
  // Après G0, aucune porte ne produit de motif pour l'incinération.
  if (use === "incineration") {
    return {
      verdict: "AUTHORISED",
      reasons: [],
      signature_permitted: true
    };
  }

  const isFeed = (use === "feed" || use === "aquaculture_feed");
  let targetTaxids: unknown[] = [];

  if (isFeed) {
    if (!Array.isArray(dest?.target_taxids) || dest.target_taxids.length === 0) {
      reasons.push("TARGET_UNSPECIFIED");
    } else {
      targetTaxids = dest.target_taxids;
    }
  } else if (Array.isArray(dest?.target_taxids)) {
    targetTaxids = dest.target_taxids;
  }

  // =========================================================================
  // PORTE G1 : Taxonomie, Résolution & Default-Deny (Règles P2, P8, P9)
  // =========================================================================
  let hasTaxonUnknown = false;
  let hasTaxonRankAbove = false;

  const resolvedSources: ResolvedTaxon[] = [];
  const substrate: SubstrateInput | undefined = claim.substrate;
  const sources = substrate?.sources;
  const proc: ProcessInput | undefined = claim.process;
  const route = proc?.route;

  // Règle P9 & P15 : substrate.sources doit être un tableau.
  // Absent ou d'un autre type => TAXON_UNKNOWN (hors incinération).
  // En alimentation (feed ou aquaculture_feed), un tableau sources vide vaut TAXON_UNKNOWN
  // pour toute route autre que insect_bioconversion (P15).
  if (!Array.isArray(sources)) {
    hasTaxonUnknown = true;
  } else {
    if (isFeed && route !== "insect_bioconversion" && sources.length === 0) {
      hasTaxonUnknown = true;
    }
    for (const s of sources) {
      if (!s || typeof s !== "object" || !("taxid" in s)) {
        hasTaxonUnknown = true;
        continue;
      }
      const res = resolveTaxon((s as { taxid: unknown }).taxid, taxonomyMap);
      if (!res.success) {
        if (res.error === "TAXON_UNKNOWN") hasTaxonUnknown = true;
        else if (res.error === "TAXON_RANK_ABOVE_SPECIES") hasTaxonRankAbove = true;
      } else {
        resolvedSources.push(res.taxon);
      }
    }
  }

  let resolvedInsect: ResolvedTaxon | null = null;
  if (route === "insect_bioconversion") {
    const insectTaxid = proc?.insect_taxid;
    if (insectTaxid === undefined || insectTaxid === null) {
      hasTaxonUnknown = true;
    } else {
      const res = resolveTaxon(insectTaxid, taxonomyMap);
      if (!res.success) {
        if (res.error === "TAXON_UNKNOWN") hasTaxonUnknown = true;
        else if (res.error === "TAXON_RANK_ABOVE_SPECIES") hasTaxonRankAbove = true;
      } else if (res.taxon.group !== "INSECT") {
        // Règle P14 : L'organisme de bioconversion doit être un insecte résolu
        hasTaxonUnknown = true;
      } else {
        resolvedInsect = res.taxon;
      }
    }
  }

  const resolvedTargets: ResolvedTaxon[] = [];
  for (const tid of targetTaxids) {
    const res = resolveTaxon(tid, taxonomyMap);
    if (!res.success) {
      if (res.error === "TAXON_UNKNOWN") hasTaxonUnknown = true;
      else if (res.error === "TAXON_RANK_ABOVE_SPECIES") hasTaxonRankAbove = true;
    } else {
      resolvedTargets.push(res.taxon);
    }
  }

  if (hasTaxonUnknown) reasons.push("TAXON_UNKNOWN");
  if (hasTaxonRankAbove) reasons.push("TAXON_RANK_ABOVE_SPECIES");

  // =========================================================================
  // PORTE G2 : Protection des Restes Humains (Règles P3, P11, P12, P15)
  // =========================================================================
  // Règle P15 : G1 s'évalue en entier avant G2. Sur des restes humains, les motifs
  // G1 (TAXON_UNKNOWN, TAXON_RANK_ABOVE_SPECIES) précèdent HUMAN_REMAINS_ROUTE_PROHIBITED.
  const isHuman = (
    resolvedSources.some(s => s.species_taxid === 9606 || s.group === "HUMAN") ||
    substrate?.material_class === "human_remains" ||
    substrate?.origin_profile === "human"
  );

  if (isHuman) {
    // Règle P12 : G2 arrête l'évaluation pour toute destination (hors incinération).
    // La mémoire forestière humaine renvoie DEROGATION_REQUIRED et s'arrête.
    if (use === "memorial_forestry") {
      reasons.push("DEROGATION_REQUIRED");
      return {
        verdict: "BLOCKED",
        reasons,
        signature_permitted: false
      };
    } else {
      reasons.push("HUMAN_REMAINS_ROUTE_PROHIBITED");
      return {
        verdict: "BLOCKED",
        reasons,
        signature_permitted: false
      };
    }
  }

  // =========================================================================
  // PORTE G3 : Catégorie de Matières & Substrats (Règles P4, P10, P12, P16, P17, DEC-AET-05)
  // =========================================================================
  const category = substrate?.category;
  const materialClass = substrate?.material_class;

  // Règle P16 : « Source déclarée » au sens de P10 : tout élément du tableau sources compte,
  // qu'il se résolve ou non (null, taxid mal typé, taxid hors snapshot, rang > espèce, nom sans taxid).
  const hasDeclaredSource = Array.isArray(sources) && sources.length > 0;
  const isPlantCategoryViolation = (materialClass === "feed_grade_plant" && hasDeclaredSource);

  let inDerogationScope = false;

  if (isFeed) {
    let feedViolation = false;
    if (category !== 3) {
      feedViolation = true;
    } else if (route === "direct_rendering") {
      if (materialClass !== "slaughter_byproduct" && materialClass !== "feed_grade_plant") {
        feedViolation = true;
      }
    } else if (route === "insect_bioconversion") {
      if (materialClass !== "feed_grade_plant") {
        feedViolation = true;
      }
    } else {
      feedViolation = true;
    }
    if (feedViolation || isPlantCategoryViolation) {
      reasons.push("SUBSTRATE_CATEGORY_VIOLATION");
    }
  } else if (use === "technical" || use === "fertiliser") {
    // Règle P12 : Portes indépendantes sans chaîne « sinon »
    const isInvalidCategory = (category !== 1 && category !== 2 && category !== 3);
    const isInvalidMaterial = (typeof materialClass !== "string" || !KNOWN_MATERIAL_CLASSES.has(materialClass));

    if (isInvalidCategory || isInvalidMaterial || isPlantCategoryViolation) {
      reasons.push("SUBSTRATE_CATEGORY_VIOLATION");
    }
    if (category === 1 && use === "fertiliser") {
      reasons.push("CATEGORY_DESTINATION_PROHIBITED");
    }
  } else if (use === "memorial_forestry") {
    // Règle P17 : Les contrôles de substrat (P4 et P10) s'appliquent à memorial_forestry.
    // SUBSTRATE_CATEGORY_VIOLATION précède DEROGATION_REQUIRED, avec ou sans politique.
    const isInvalidCategory = (category !== 1 && category !== 2 && category !== 3);
    const isInvalidMaterial = (typeof materialClass !== "string" || !KNOWN_MATERIAL_CLASSES.has(materialClass));

    if (isInvalidCategory || isInvalidMaterial || isPlantCategoryViolation) {
      reasons.push("SUBSTRATE_CATEGORY_VIOLATION");
    }

    // Dérogation souveraine DEC-AET-05 (§4.3)
    const isPolicyValid = (
      policy !== null &&
      typeof policy === "object" &&
      policy.policy_id === "DEC-AET-05" &&
      typeof policy.legal_basis === "string" &&
      policy.legal_basis.trim() !== "" &&
      typeof policy.authority_reference === "string" &&
      policy.authority_reference.trim() !== ""
    );

    const hasRuminantSource = resolvedSources.some(
      s => s.group === "RUMINANT" || s.lineage_markers.includes(9845)
    );

    // Règle P14 : insect_taxid doit impérativement avoir pour groupe résolu "INSECT"
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
  }

  // =========================================================================
  // PORTE G4 : Contrôle Pentobarbital (Animaux de Compagnie)
  // =========================================================================
  if (substrate?.origin_profile === "pet") {
    const lfa = substrate.pentobarbital_lfa;
    if (lfa === "positive") {
      reasons.push("PENTOBARBITAL_POSITIVE");
    } else if (lfa !== "negative") {
      reasons.push("PENTOBARBITAL_NOT_TESTED");
    }
  }

  // =========================================================================
  // PORTES G5 à G8 : Feed-Ban Européen (Alimentation Terrestre & Aquacole)
  // =========================================================================
  if (isFeed) {
    // G5 : Interdiction des Ruminants en Source (Règl. 999/2001)
    const hasRuminantSource = resolvedSources.some(
      s => s.group === "RUMINANT" || s.lineage_markers.includes(9845)
    );
    if (hasRuminantSource) {
      reasons.push("FEED_BAN_RUMINANT_SOURCE");
    }

    // G6 : Interdiction des Ruminants en Cible (Règl. 999/2001)
    const hasRuminantTarget = resolvedTargets.some(
      t => t.group === "RUMINANT" || t.lineage_markers.includes(9845)
    );
    if (hasRuminantTarget) {
      reasons.push("FEED_BAN_RUMINANT_TARGET");
    }

    // G7 : Règle d'Or Anti-Cannibalisme Intra-Espèce (Règl. 1069/2009 art. 11(1)(a))
    const allSourceSpecies = new Set(resolvedSources.map(s => s.species_taxid));
    if (route === "insect_bioconversion" && resolvedInsect) {
      allSourceSpecies.add(resolvedInsect.species_taxid);
    }
    const hasIntraSpecies = resolvedTargets.some(t => allSourceSpecies.has(t.species_taxid));
    if (hasIntraSpecies) {
      reasons.push("FEED_BAN_INTRA_SPECIES_VIOLATION");
    }

    // G8 : Interdictions de Groupe & Groupes Positifs (Règl. 2021/1372 & 999/2001)
    const effectiveSourceGroups = new Set(resolvedSources.map(s => s.group));
    if (route === "insect_bioconversion" && resolvedInsect) {
      // Le groupe de l'organisme provient toujours de la résolution du snapshot (Règle P14)
      effectiveSourceGroups.add(resolvedInsect.group);
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
      if (!sourceGroupAuthorized) {
        reasons.push("SOURCE_GROUP_NOT_AUTHORISED");
      }
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

  // =========================================================================
  // PORTE G9 : Traitement Sanitaire Requis & Preuve (Règles P6, P7, P8, P12, P13, DEC-AET-05)
  // =========================================================================
  if (isFeed || ((use === "technical" || use === "fertiliser") && category !== 3)) {
    const treatment: TreatmentInput | undefined = proc?.treatment as TreatmentInput | undefined;
    if (!treatment || typeof treatment !== "object") {
      reasons.push("TREATMENT_NOT_PROVEN");
    } else {
      const method = treatment.method;
      const evidence = treatment.evidence_sha256;
      const hasValidEvidence = typeof evidence === "string" && HEX_SHA256_REGEX.test(evidence);

      let methodAuthorized = false;
      if (use === "technical" || use === "fertiliser") {
        methodAuthorized = (method === 1);
      } else { // isFeed
        if (route === "insect_bioconversion") {
          methodAuthorized = (typeof method === "number" && [1, 2, 3, 4, 5, 7].includes(method));
        } else {
          // direct_rendering
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
            // Règle P13 : Natures mêlées => Méthode 1 exclusivement
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

        const paramsValid = (
          typeof temp === "number" && !Number.isNaN(temp) && temp >= 133 &&
          typeof press === "number" && !Number.isNaN(press) && press >= 3.0 &&
          typeof mins === "number" && !Number.isNaN(mins) && mins >= 20
        );

        if (!paramsValid) {
          reasons.push("TREATMENT_NOT_PROVEN");
        }
      }
    }
  } else if (use === "memorial_forestry" && inDerogationScope) {
    // Dérogation DEC-AET-05 : pasteurisation thermique obligatoire (70 °C, 60 min)
    const pasteurisation: PasteurisationInput | undefined = proc?.pasteurisation as PasteurisationInput | undefined;
    if (!pasteurisation || typeof pasteurisation !== "object") {
      reasons.push("TREATMENT_NOT_PROVEN");
    } else {
      const temp = pasteurisation.core_temp_c;
      const mins = pasteurisation.minutes;
      const evidence = pasteurisation.evidence_sha256;
      const hasValidEvidence = typeof evidence === "string" && HEX_SHA256_REGEX.test(evidence);

      const paramsValid = (
        typeof temp === "number" && !Number.isNaN(temp) && temp >= 70 &&
        typeof mins === "number" && !Number.isNaN(mins) && mins >= 60 &&
        hasValidEvidence
      );

      if (!paramsValid) {
        reasons.push("TREATMENT_NOT_PROVEN");
      }
    }
  }

  // =========================================================================
  // Décision Finale & Invariance Mathématique
  // =========================================================================
  const isAuthorised = (reasons.length === 0);
  return {
    verdict: isAuthorised ? "AUTHORISED" : "BLOCKED",
    reasons,
    signature_permitted: isAuthorised
  };
}
