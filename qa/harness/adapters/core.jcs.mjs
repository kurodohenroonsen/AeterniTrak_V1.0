/**
 * Adaptateur de conformité AeterniCore JCS pour le harnais QA (Bushi 16)
 * Exécute l'opération sur la suite `core.jcs.rfc8785` :
 * - canonicalize : { utf8, hex, len, sha256 }
 */

import crypto from "node:crypto";
import { canonicalizeJsonString } from "../../../core/jcs/index.ts";

export async function run(op, input) {
  if (op === "canonicalize") {
    const utf8 = canonicalizeJsonString(input);
    const bytes = new TextEncoder().encode(utf8);
    let hex = "";
    for (let i = 0; i < bytes.length; i++) {
      hex += bytes[i].toString(16).padStart(2, "0");
    }
    const len = bytes.length;
    const sha256 = crypto.createHash("sha256").update(bytes).digest("hex");
    return { utf8, hex, len, sha256 };
  }

  throw new Error(`Unsupported operation: ${op}`);
}
