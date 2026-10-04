/**
 * Point d'entrée du validateur anti-prion The Iron Gate
 * Exportations publiques pour l'évaluateur pur
 */

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
