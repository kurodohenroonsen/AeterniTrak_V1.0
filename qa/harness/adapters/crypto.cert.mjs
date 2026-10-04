/**
 * Adaptateur de harnais QA pour la suite crypto.batch-certificate (Bushi 02 / Bushi 16)
 * Opérations supportées : cert-issue, cert-verify
 */

import crypto from "node:crypto";
import { evaluateAndSign, certVerify } from "../../../core/cert/index.ts";
import { ed25519Sign, kid } from "../../../core/cose/index.ts";
import { hexToBytes, bytesToHex } from "../../../core/cbor/index.ts";

export async function run(op, input) {
  if (op === "cert-issue") {
    const seed = hexToBytes(input.seed_hex);
    const { publicKey } = await ed25519Sign(seed, new Uint8Array(0));
    const signerKid = await kid(publicKey);

    const signer = {
      algorithm: -8,
      kid: signerKid,
      sign: async (tbs) => {
        const { signature } = await ed25519Sign(seed, tbs);
        return signature;
      }
    };

    try {
      const res = await evaluateAndSign(input.claim, input.policy, {
        signer,
        issuedAt: input.issued_at,
        policies: input.policies
      });

      const sha256 = crypto.createHash("sha256").update(res.envelope).digest("hex");

      return {
        envelope_hex: bytesToHex(res.envelope),
        len: res.envelope.length,
        sha256,
        claim_json: res.claimJson,
        kid_hex: bytesToHex(signerKid)
      };
    } catch (err) {
      if (err.refusal_reasons) {
        return {
          error: err.code || err.message,
          refusal_reasons: err.refusal_reasons
        };
      }
      return {
        error: err.code || err.message
      };
    }
  }

  if (op === "cert-verify") {
    try {
      const envelope = hexToBytes(input.envelope_hex);
      const res = await certVerify(envelope, input.claim_json, input.trust_store, {
        policies: input.policies,
        retiredRulesVersions: input.retired_rules_versions
      });
      return res;
    } catch (err) {
      return {
        error: err.code || err.message
      };
    }
  }

  throw new Error(`Opération non supportée par crypto.cert : ${op}`);
}
