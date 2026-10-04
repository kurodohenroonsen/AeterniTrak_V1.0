/**
 * AeterniCore CBOR Byte Writer & Lexicographical Byte Comparison
 * Conformité : RFC 8949 §4.2.1 (3)
 */

import { CborError } from "./errors.ts";

/**
 * Compare deux séquences d'octets selon l'ordre lexicographique bytewise strict (RFC 8949 §4.2.1).
 * Pour deux clés encodées, le premier octet différent détermine l'ordre.
 * Si l'une est un préfixe strict de l'autre, la plus courte précède la plus longue.
 */
export function compareBytes(a: Uint8Array, b: Uint8Array): number {
  const minLen = Math.min(a.length, b.length);
  for (let i = 0; i < minLen; i++) {
    if (a[i] !== b[i]) {
      return a[i] - b[i];
    }
  }
  return a.length - b.length;
}

/**
 * Convertit un Uint8Array en chaîne hexadécimale minuscule.
 */
export function bytesToHex(bytes: Uint8Array): string {
  let hex = "";
  for (let i = 0; i < bytes.length; i++) {
    hex += bytes[i].toString(16).padStart(2, "0");
  }
  return hex;
}

/**
 * Convertit une chaîne hexadécimale en Uint8Array.
 */
export function hexToBytes(hex: string): Uint8Array {
  if (hex.length % 2 !== 0) {
    throw new CborError("ERR_CBOR_MALFORMED", "Odd length hex string");
  }
  const bytes = new Uint8Array(hex.length / 2);
  for (let i = 0; i < bytes.length; i++) {
    const byte = parseInt(hex.substring(i * 2, i * 2 + 2), 16);
    if (Number.isNaN(byte)) {
      throw new CborError("ERR_CBOR_MALFORMED", "Invalid hex character");
    }
    bytes[i] = byte;
  }
  return bytes;
}

/**
 * Tampon dynamique d'écriture binaire déterministe à allocation géométrique.
 */
export class ByteWriter {
  private buffer: Uint8Array;
  private length: number;

  constructor(initialCap = 256) {
    this.buffer = new Uint8Array(initialCap);
    this.length = 0;
  }

  private ensure(extra: number): void {
    if (this.length + extra > this.buffer.length) {
      const newCap = Math.max(this.buffer.length * 2, this.length + extra);
      const next = new Uint8Array(newCap);
      next.set(this.buffer);
      this.buffer = next;
    }
  }

  writeByte(b: number): void {
    this.ensure(1);
    this.buffer[this.length++] = b & 0xff;
  }

  writeBytes(bytes: Uint8Array): void {
    this.ensure(bytes.length);
    this.buffer.set(bytes, this.length);
    this.length += bytes.length;
  }

  /**
   * Écrit un entier sous forme canonique la plus courte (RFC 8949 §4.2.1 (1)).
   */
  writeUint(major: number, val: bigint | number): void {
    const m = (major << 5) & 0xe0;

    if (typeof val === "number") {
      if (!Number.isFinite(val) || !Number.isInteger(val) || val < 0) {
        throw new CborError("ERR_CBOR_MALFORMED", "Invalid uint value");
      }
      if (val < 24) {
        this.writeByte(m | val);
      } else if (val <= 0xff) {
        this.writeByte(m | 24);
        this.writeByte(val);
      } else if (val <= 0xffff) {
        this.writeByte(m | 25);
        this.writeByte((val >> 8) & 0xff);
        this.writeByte(val & 0xff);
      } else if (val <= 0xffffffff) {
        this.writeByte(m | 26);
        this.writeByte((val >>> 24) & 0xff);
        this.writeByte((val >>> 16) & 0xff);
        this.writeByte((val >>> 8) & 0xff);
        this.writeByte(val & 0xff);
      } else {
        this.writeUint(major, BigInt(val));
      }
    } else if (typeof val === "bigint") {
      if (val < 0n || val > 18446744073709551615n) {
        throw new CborError("ERR_CBOR_MALFORMED", "Integer out of 64-bit range");
      }
      if (val < 24n) {
        this.writeByte(m | Number(val));
      } else if (val <= 0xffn) {
        this.writeByte(m | 24);
        this.writeByte(Number(val));
      } else if (val <= 0xffffn) {
        this.writeByte(m | 25);
        const n = Number(val);
        this.writeByte((n >> 8) & 0xff);
        this.writeByte(n & 0xff);
      } else if (val <= 0xffffffffn) {
        this.writeByte(m | 26);
        const n = Number(val);
        this.writeByte((n >>> 24) & 0xff);
        this.writeByte((n >>> 16) & 0xff);
        this.writeByte((n >>> 8) & 0xff);
        this.writeByte(n & 0xff);
      } else {
        this.writeByte(m | 27);
        const view = new DataView(new ArrayBuffer(8));
        view.setBigUint64(0, val, false);
        this.writeBytes(new Uint8Array(view.buffer));
      }
    }
  }

  getBytes(): Uint8Array {
    return this.buffer.subarray(0, this.length);
  }
}
