/**
 * Adaptateur de conformité AeterniCore CBOR pour le harnais QA (Bushi 16)
 * Exécute les opérations sur la suite `core.cbor.deterministic` :
 * - encode : { hex, len, sha256 }
 * - decode : { item }
 * - reject-decode : lève CborError avec code d'erreur exact
 * - reject-encode : lève CborError avec code d'erreur exact
 */

import crypto from "node:crypto";
import { encode, decodeStrict, bytesToHex, hexToBytes } from "../../../core/cbor/index.ts";

export async function run(op, input) {
  if (op === "encode") {
    const bytes = encode(input);
    const hex = bytesToHex(bytes);
    const len = bytes.length;
    const sha256 = crypto.createHash("sha256").update(bytes).digest("hex");
    return { hex, len, sha256 };
  }

  if (op === "decode") {
    const bytes = hexToBytes(input.hex);
    const item = decodeStrict(bytes);
    return { item };
  }

  if (op === "reject-decode") {
    const bytes = hexToBytes(input.hex);
    const item = decodeStrict(bytes);
    return { item };
  }

  if (op === "reject-encode") {
    const bytes = encode(input);
    const hex = bytesToHex(bytes);
    return { hex, len: bytes.length };
  }

  throw new Error(`Unsupported operation: ${op}`);
}
