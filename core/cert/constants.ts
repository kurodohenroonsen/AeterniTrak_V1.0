/**
 * AeterniTrak V1.0 — Constantes Normatives du Certificat de Lot
 * Conformité : AET-SPEC-CERT-001 v1.1.0, qa/vectors/README.md §4.14
 */

import { canonicalizeJsonString } from "../jcs/canonicalize.ts";
import { bytesToHex } from "../cbor/writer.ts";
import { RULES_VERSION, EMBEDDED_TAXONOMY_SNAPSHOT } from "../../validators/antiprion/index.ts";

export { RULES_VERSION };

/**
 * Calcul dynamique et canonique de l'empreinte taxonomique embarquée :
 * SHA-256(UTF-8(JCS(taxonomy_snapshot)))
 * Ne jamais la copier en dur afin de détecter immédiatement toute dérive de taxonomy.ts.
 */
const snapshotJcs = canonicalizeJsonString(EMBEDDED_TAXONOMY_SNAPSHOT);
const snapshotBytes = new TextEncoder().encode(snapshotJcs);
const snapshotHashBuf = await globalThis.crypto.subtle.digest("SHA-256", snapshotBytes);

export const TAXONOMY_SNAPSHOT_SHA256: Uint8Array = new Uint8Array(snapshotHashBuf);
export const TAXONOMY_SNAPSHOT_HEX: string = bytesToHex(TAXONOMY_SNAPSHOT_SHA256);
