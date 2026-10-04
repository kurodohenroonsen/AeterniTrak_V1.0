/**
 * AeterniCore CBOR Error Registry
 * Conformité : qa/vectors/README.md §4.1 & docs/technical/aeternicore.md A6.2
 */

export type CborErrorCode =
  | "ERR_CBOR_NOT_SHORTEST"
  | "ERR_CBOR_INDEFINITE_LENGTH"
  | "ERR_CBOR_MAP_UNSORTED"
  | "ERR_CBOR_DUPLICATE_KEY"
  | "ERR_CBOR_TRAILING_BYTES"
  | "ERR_CBOR_TRUNCATED"
  | "ERR_CBOR_MALFORMED"
  | "ERR_CBOR_INVALID_UTF8"
  | "ERR_CBOR_TEXT_NOT_NFC"
  | "ERR_CBOR_UNSUPPORTED_TYPE"
  | "ERR_CBOR_UNSUPPORTED_TAG"
  | "ERR_CBOR_TAG_CONTENT";

export class CborError extends Error {
  readonly code: CborErrorCode;
  readonly offset?: number;

  constructor(code: CborErrorCode, message: string, offset?: number) {
    super(`[${code}] ${message}${offset !== undefined ? ` at offset ${offset}` : ""}`);
    this.name = "CborError";
    this.code = code;
    this.offset = offset;
    Object.setPrototypeOf(this, CborError.prototype);
  }
}
