/**
 * Adaptateur de harnais pour le validateur anti-prion The Iron Gate
 * Opérations supportées : evaluate, evaluate-with-policy
 */

import { evaluate } from "../../../validators/antiprion/index.ts";

export async function run(op, input) {
  if (op === "evaluate") {
    return evaluate(input);
  }
  if (op === "evaluate-with-policy") {
    return evaluate(input?.claim, input?.policy);
  }
  throw new Error(`Opération non supportée par l'adaptateur antiprion.feedban : ${op}`);
}
