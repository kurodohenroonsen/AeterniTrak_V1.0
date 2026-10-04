/**
 * Adaptateur QA pour la suite crypto.ed25519.rfc8032 (Bushi 16 / Bushi 02)
 * Opérations : sign, verify
 */

import { ed25519Sign, ed25519Verify } from "../../../core/cose/index.ts";
import { hexToBytes, bytesToHex } from "../../../core/cbor/index.ts";

export async function run(op, input) {
  if (op === "sign") {
    const seed = hexToBytes(input.seed_hex);
    const message = hexToBytes(input.message_hex);
    const res = await ed25519Sign(seed, message);
    return {
      public_key_hex: bytesToHex(res.publicKey),
      signature_hex: bytesToHex(res.signature)
    };
  }

  if (op === "verify") {
    try {
      const pub = hexToBytes(input.public_key_hex);
      const msg = hexToBytes(input.message_hex);
      const sig = hexToBytes(input.signature_hex);
      const valid = await ed25519Verify(pub, msg, sig);
      return { valid };
    } catch (err) {
      return { error: err.code || err.message };
    }
  }

  throw new Error(`Opération non supportée par crypto.ed25519 : ${op}`);
}
