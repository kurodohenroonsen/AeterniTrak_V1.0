/**
 * AeterniCore Profile V1 Error Registry
 * Registre normatif ERR_PROFILE_* selon qa/vectors/README.md §4.7
 */

export type ProfileErrorCode =
  | "ERR_PROFILE_TOO_LARGE"
  | "ERR_PROFILE_NOT_A_MAP"
  | "ERR_PROFILE_INVALID_KEY_TYPE"
  | "ERR_PROFILE_MISSING_FIELD"
  | "ERR_PROFILE_UNSUPPORTED_VERSION"
  | "ERR_PROFILE_UNKNOWN_FIELD"
  | "ERR_PROFILE_INVALID_SUBJECT_KIND"
  | "ERR_PROFILE_INVALID_NAME"
  | "ERR_PROFILE_TOO_MANY_NAMES"
  | "ERR_PROFILE_INVALID_DATE_TYPE"
  | "ERR_PROFILE_MISSING_BIRTH_DATE"
  | "ERR_PROFILE_INVALID_RITE"
  | "ERR_PROFILE_INVALID_COUNTRY"
  | "ERR_PROFILE_INVALID_ASSET_REF"
  | "ERR_PROFILE_INVALID_HASH_LENGTH"
  | "ERR_PROFILE_PORTRAIT_TOO_LARGE"
  | "ERR_PROFILE_VOICE_TOO_LARGE"
  | "ERR_PROFILE_INVALID_ISSUER_ID"
  | "ERR_PROFILE_INVALID_EPITAPH"
  | "ERR_PROFILE_INVALID_SPECIES";

export class ProfileError extends Error {
  readonly code: ProfileErrorCode;

  constructor(code: ProfileErrorCode, message: string) {
    super(`[${code}] ${message}`);
    this.name = "ProfileError";
    this.code = code;
  }
}
