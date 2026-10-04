/**
 * Résolution taxonomique locale et autonome
 * Importe le snapshot taxonomique officiel qa/vectors/antiprion/taxonomy-snapshot.json
 */

import taxonomySnapshot from "../../qa/vectors/antiprion/taxonomy-snapshot.json" with { type: "json" };
import type { TaxonEntry, ResolvedTaxon, TaxonResolutionResult } from "./types.ts";

export const TAXONOMY_MAP: Map<number, TaxonEntry> = new Map();

for (const taxon of taxonomySnapshot.taxa) {
  TAXONOMY_MAP.set(taxon.taxid, taxon as TaxonEntry);
}

/**
 * Résout un identifiant taxonomique vers son espèce de rattachement.
 * Typage strict (P8) : seul un entier valide est accepté.
 * Résolution des sous-espèces vers l'espèce parente.
 * Rejet des rangs supérieurs à l'espèce (TAXON_RANK_ABOVE_SPECIES).
 */
export function resolveTaxon(
  taxid: unknown,
  taxonomyMap: Map<number, TaxonEntry> = TAXONOMY_MAP
): TaxonResolutionResult {
  if (typeof taxid !== "number" || !Number.isInteger(taxid)) {
    return { success: false, error: "TAXON_UNKNOWN" };
  }

  const entry = taxonomyMap.get(taxid);
  if (!entry) {
    return { success: false, error: "TAXON_UNKNOWN" };
  }

  if (entry.rank !== "species" && entry.rank !== "subspecies") {
    return { success: false, error: "TAXON_RANK_ABOVE_SPECIES" };
  }

  let current = entry;
  const markers = [...(entry.lineage_markers || [])];

  while (current.rank === "subspecies") {
    if (!current.parent_taxid) {
      return { success: false, error: "TAXON_UNKNOWN" };
    }
    const parent = taxonomyMap.get(current.parent_taxid);
    if (!parent) {
      return { success: false, error: "TAXON_UNKNOWN" };
    }
    current = parent;
    if (current.lineage_markers) {
      markers.push(...current.lineage_markers);
    }
  }

  return {
    success: true,
    taxon: {
      taxid: entry.taxid,
      species_taxid: current.taxid,
      rank: entry.rank,
      group: current.group || entry.group,
      lineage_markers: markers
    }
  };
}
