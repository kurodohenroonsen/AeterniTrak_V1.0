/**
 * Point d'entrée du validateur anti-prion The Iron Gate
 * Exportations publiques pour l'évaluateur pur
 */

export const RULES_VERSION = "1.5.0";
export { evaluate } from "./evaluator.ts";
export { resolveTaxon, TAXONOMY_MAP } from "./taxonomy.ts";
export type {
  TaxonEntry,
  ResolvedTaxon,
  TaxonResolutionResult,
  PolicyInput,
  EvaluationResult,
  BatchClaimInput
} from "./types.ts";
