/**
 * AeterniCore JCS Error Types
 * Conformité : RFC 8785
 */

export class JcsError extends Error {
  readonly code: string;

  constructor(code: string, message: string) {
    super(`[${code}] ${message}`);
    this.name = "JcsError";
    this.code = code;
    Object.setPrototypeOf(this, JcsError.prototype);
  }
}
