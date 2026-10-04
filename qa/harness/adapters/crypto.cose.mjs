/**
 * Adaptateur QA pour la suite crypto.cose.sign1 (Bushi 16 / Bushi 02)
 * Opérations : kid, protected-header, sig-structure, cose-sign, cose-verify
 */

import crypto from "node:crypto";
import {
  kid,
  protectedHeader,
  sigStructure,
  coseSign,
  coseVerify,
  coseOpen,
  ed25519Sign
} from "../../../core/cose/index.ts";
import { hexToBytes, bytesToHex } from "../../../core/cbor/index.ts";

export async function run(op, input) {
  if (op === "kid") {
    const pub = hexToBytes(input.public_key_hex);
    const k = await kid(pub);
    return { kid_hex: bytesToHex(k) };
  }

  if (op === "protected-header") {
    const hdr = protectedHeader(input.alg, input.typ);
    return { hex: bytesToHex(hdr) };
  }

  if (op === "sig-structure") {
    const prot = hexToBytes(input.protected_hex);
    const pay = hexToBytes(input.payload_hex);
    const tbs = sigStructure(prot, pay);
    const sha256 = crypto.createHash("sha256").update(tbs).digest("hex");
    return { hex: bytesToHex(tbs), sha256 };
  }

  if (op === "cose-sign") {
    const seed = hexToBytes(input.seed_hex);
    const pay = hexToBytes(input.payload_hex);
    const envelope = await coseSign(seed, input.typ, pay);
    const len = envelope.length;
    const sha256 = crypto.createHash("sha256").update(envelope).digest("hex");

    const { publicKey } = await ed25519Sign(seed, new Uint8Array(0));
    const signerKid = await kid(publicKey);

    return {
      envelope_hex: bytesToHex(envelope),
      len,
      sha256,
      kid_hex: bytesToHex(signerKid)
    };
  }

  if (op === "cose-verify") {
    try {
      const envelope = hexToBytes(input.envelope_hex);
      const res = await coseVerify(envelope, input.expected_typ, input.trust_store);
      return {
        valid: true,
        payload_hex: res.payload_hex,
        kid: res.kid
      };
    } catch (err) {
      return { error: err.code || err.message };
    }
  }

  if (op === "cose-open") {
    const envelope = hexToBytes(input.envelope_hex);
    const res = await coseOpen(envelope, input.expected_typ, input.trust_store);
    if (res.status === "VERIFIED") {
      return {
        status: "VERIFIED",
        payload_hex: res.payload_hex,
        kid: res.kid
      };
    }
    if (res.status === "UNVERIFIED") {
      return {
        status: "UNVERIFIED",
        reason: res.reason,
        payload_hex: res.payload_hex
      };
    }
    return {
      status: "BLOCKED",
      error: res.error
    };
  }

  throw new Error(`Opération non supportée par crypto.cose : ${op}`);
}
