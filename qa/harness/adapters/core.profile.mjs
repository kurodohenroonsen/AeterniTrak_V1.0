/**
 * Adaptateur de conformité AeterniCore Profile V1 pour le harnais QA (Bushi 16)
 * Exécute l'opération `validate-profile` sur la suite `core.profile` :
 * - input : { hex }
 * - expect : { valid: true, len } ou { error }
 * Note : L'adaptateur capture lui-même les exceptions et renvoie { error: err.code || err.message }.
 */

import { validateProfile } from "../../../core/profile/index.ts";
import { hexToBytes } from "../../../core/cbor/index.ts";

export async function run(op, input) {
  if (op === "validate-profile") {
    try {
      const bytes = hexToBytes(input.hex);
      return validateProfile(bytes);
    } catch (err) {
      return { error: err.code || err.message };
    }
  }

  throw new Error(`Unsupported operation: ${op}`);
}
