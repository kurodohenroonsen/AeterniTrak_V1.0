/**
 * AeterniTrak V1.0 — Opération Applicative coseOpen (DEC-AET-07 Option B)
 * Conformité : qa/vectors/README.md §4.9, DECISIONS-KUDORO.md DEC-AET-07
 *
 * Sémantique de consultation sous réserve :
 * - VERIFIED : Enveloppe authentique signée par un émetteur de confiance actif.
 * - UNVERIFIED : UNIQUEMENT pour ERR_COSE_UNKNOWN_KID. Les étapes 1 à 7 ont réussi.
 *   La charge utile est délivrée avec reason: "ERR_COSE_UNKNOWN_KID" pour affichage sous réserve.
 * - BLOCKED : Pour toute autre anomalie (clé révoquée, fausse signature, type non concordant, etc.).
 *   Aucune charge utile n'est restituée.
 */

import { decodeToCborValue } from "../cbor/index.ts";
import { bytesToHex } from "../cbor/writer.ts";
import { CoseError } from "./errors.ts";
import { coseVerify } from "./envelope.ts";
import type { TrustStore, OpenResult } from "./types.ts";

/**
 * Tente d'ouvrir et de valider une enveloppe COSE_Sign1 selon le modèle DEC-AET-07 Option B.
 *
 * @param envelope - Octets bruts complets de l'enveloppe COSE_Sign1.
 * @param expectedTyp - Type de contenu attendu (étiquette 16).
 * @param trustStore - Registre de confiance scellé.
 * @returns Promise<OpenResult> (VERIFIED, UNVERIFIED ou BLOCKED).
 */
export async function coseOpen(
  envelope: Uint8Array,
  expectedTyp: string,
  trustStore: TrustStore
): Promise<OpenResult> {
  try {
    const res = await coseVerify(envelope, expectedTyp, trustStore);
    return {
      status: "VERIFIED",
      valid: true,
      payload: res.payload,
      payload_hex: res.payload_hex,
      kid: res.kid
    };
  } catch (err: unknown) {
    const errCode =
      err instanceof CoseError
        ? err.code
        : typeof (err as Record<string, unknown>)?.code === "string"
        ? ((err as Record<string, unknown>).code as string)
        : (err as Error)?.message || "ERR_COSE_UNKNOWN_ERROR";

    // Seul ERR_COSE_UNKNOWN_KID autorise la délivrance de la charge utile (Option B)
    if (errCode === "ERR_COSE_UNKNOWN_KID") {
      try {
        const decoded = decodeToCborValue(envelope.subarray(1));
        if (decoded.type === "array" && decoded.value.length === 4 && decoded.value[2].type === "bytes") {
          const payloadBytes = decoded.value[2].value;
          return {
            status: "UNVERIFIED",
            valid: false,
            payload: payloadBytes,
            payload_hex: bytesToHex(payloadBytes),
            reason: "ERR_COSE_UNKNOWN_KID"
          };
        }
      } catch {
        // En cas d'anomalie imprévue d'extraction, bascule sur blocage strict
      }
    }

    return {
      status: "BLOCKED",
      valid: false,
      error: errCode
    };
  }
}
