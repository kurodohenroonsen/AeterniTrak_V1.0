/**
 * Types et interfaces pour le validateur anti-prion Iron Gate
 * Conforme à la spécification AET-SPEC-PRION-001 v1.3.0 et aux règles P1 à P14
 */

export interface TaxonEntry {
  taxid: number;
  scientific_name: string;
  rank: string;
  parent_taxid?: number;
  lineage_markers: number[];
  group: string;
  common_name_fr?: string;
}

export interface ResolvedTaxon {
  taxid: number;
  species_taxid: number;
  rank: string;
  group: string;
  lineage_markers: number[];
}

export type TaxonResolutionResult =
  | { success: true; taxon: ResolvedTaxon }
  | { success: false; error: "TAXON_UNKNOWN" | "TAXON_RANK_ABOVE_SPECIES" };

export interface PolicyInput {
  policy_id: string;
  version?: number;
  legal_basis: string;
  authority_reference: string;
}

export interface EvaluationResult {
  verdict: "AUTHORISED" | "BLOCKED";
  reasons: string[];
  signature_permitted: boolean;
}

export interface SourceItemInput {
  taxid?: unknown;
  label?: unknown;
  [key: string]: unknown;
}

export interface SubstrateInput {
  category?: unknown;
  material_class?: unknown;
  origin_profile?: unknown;
  sources?: unknown;
  pentobarbital_lfa?: unknown;
  [key: string]: unknown;
}

export interface TreatmentInput {
  method?: unknown;
  core_temp_c?: unknown;
  pressure_bar?: unknown;
  minutes?: unknown;
  evidence_sha256?: unknown;
  [key: string]: unknown;
}

export interface PasteurisationInput {
  core_temp_c?: unknown;
  minutes?: unknown;
  evidence_sha256?: unknown;
  [key: string]: unknown;
}

export interface ProcessInput {
  route?: unknown;
  insect_taxid?: unknown;
  treatment?: unknown;
  pasteurisation?: unknown;
  [key: string]: unknown;
}

export interface DestinationInput {
  use?: unknown;
  target_taxids?: unknown;
  [key: string]: unknown;
}

export interface BatchClaimInput {
  batch_id?: unknown;
  substrate?: SubstrateInput;
  process?: ProcessInput;
  product?: unknown;
  destination?: DestinationInput;
  [key: string]: unknown;
}
