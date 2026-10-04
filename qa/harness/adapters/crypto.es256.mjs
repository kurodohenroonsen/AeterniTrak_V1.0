/**
 * Adaptateur QA pour la suite crypto.es256.verify (Bushi 16 / Bushi 02)
 * Opérations : verify
 */

import { es256Verify } from "../../../core/cose/index.ts";
import { hexToBytes } from "../../../core/cbor/index.ts";

export async function run(op, input) {
  if (op === "verify") {
    try {
      const pub = hexToBytes(input.public_key_hex);
      const msg = hexToBytes(input.message_hex);
      const sig = hexToBytes(input.signature_hex);
      const valid = await es256Verify(pub, msg, sig);
      return { valid };
    } catch (err) {
      return { error: err.code || err.message };
    }
  }

  throw new Error(`Opération non supportée par crypto.es256 : ${op}`);
}
