/**
 * AeterniCore JCS Error Types
 * Conformité : RFC 8785
 */

export type JcsErrorCode = "ERR_JCS_INVALID_NUMBER" | "ERR_JCS_UNSUPPORTED_TYPE";

export class JcsError extends Error {
  readonly code: JcsErrorCode;

  constructor(code: JcsErrorCode, message: string) {
    super(`[${code}] ${message}`);
    this.name = "JcsError";
    this.code = code;
    Object.setPrototypeOf(this, JcsError.prototype);
  }
}

