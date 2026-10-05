/**
 * AeterniTrak V1.0 — Framework de Test Unitaire pour Micro Cas d'Usage
 * Conforme aux spécifications DEC-AET-08 & DEC-AET-09.
 * 100% Hors-Ligne & Zéro Dépendance Distante.
 */

class MicroUseCaseTest {
  constructor(ucId, title, options = {}) {
    this.ucId = ucId;
    this.title = title;
    this.options = options;
    this.assertions = 0;
    this.passed = 0;
    this.failed = 0;
    this.errors = [];
    this.startTime = null;
    this.endTime = null;
    this.duration = 0;
    this.consoleEl = options.consoleEl || (typeof document !== 'undefined' ? document.getElementById('test-console') : null);
    this.badgeEl = options.badgeEl || (typeof document !== 'undefined' ? document.getElementById('test-status-badge') : null);
  }

  log(msg, type = 'info') {
    const time = new Date().toISOString().substring(11, 19);
    if (typeof document !== 'undefined' && this.consoleEl) {
      const line = document.createElement('div');
      line.className = `test-log-line test-log-${type}`;
      let icon = 'ℹ️';
      if (type === 'pass') icon = '✅';
      if (type === 'fail') icon = '❌';
      if (type === 'warn') icon = '⚠️';
      if (type === 'phase') icon = '⚡';
      line.innerHTML = `<span class="opacity-50 font-mono text-[10px]">[${time}]</span> <span class="font-bold">${icon}</span> <span>${this.escapeHtml(msg)}</span>`;
      this.consoleEl.appendChild(line);
      this.consoleEl.scrollTop = this.consoleEl.scrollHeight;
    } else {
      console.log(`[${this.ucId}] [${type.toUpperCase()}] ${msg}`);
    }
  }

  escapeHtml(str) {
    if (typeof str !== 'string') return String(str);
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  setup() {
    this.assertions = 0;
    this.passed = 0;
    this.failed = 0;
    this.errors = [];
    this.startTime = (typeof performance !== 'undefined' && performance.now) ? performance.now() : Date.now();
    if (this.consoleEl) this.consoleEl.innerHTML = '';
    if (this.badgeEl) {
      this.badgeEl.className = 'test-badge test-badge-running';
      this.badgeEl.textContent = 'EN COURS...';
    }
    this.log(`Initialisation des fixtures et de l'état pour ${this.ucId} : ${this.title}`, 'info');
  }

  assertTrue(condition, message) {
    this.assertions++;
    if (condition) {
      this.passed++;
      this.log(`PASS : ${message}`, 'pass');
      return true;
    } else {
      this.failed++;
      this.errors.push(message);
      this.log(`FAIL : ${message}`, 'fail');
      return false;
    }
  }

  assertEquals(actual, expected, message) {
    const ok = actual === expected;
    const detail = ok ? message : `${message} (attendu: ${JSON.stringify(expected)}, obtenu: ${JSON.stringify(actual)})`;
    return this.assertTrue(ok, detail);
  }

  assertBytesBudget(bytes, maxLimit, partitionName) {
    const ok = bytes <= maxLimit;
    const remaining = maxLimit - bytes;
    const pct = Math.round((bytes / maxLimit) * 100);
    const detail = `Budget partition '${partitionName}' : ${bytes} / ${maxLimit} octets (${pct}%, reste: ${remaining} o)`;
    return this.assertTrue(ok, ok ? `${detail} [CONFORME SILICIUM]` : `${detail} [DÉPASSEMENT EEPROM]`);
  }

  async computeSha256(input) {
    let data;
    if (typeof input === 'string') {
      data = new TextEncoder().encode(input);
    } else if (input instanceof Uint8Array) {
      data = input;
    } else {
      data = new TextEncoder().encode(JSON.stringify(input));
    }
    const hashBuf = await globalThis.crypto.subtle.digest('SHA-256', data);
    const hashBytes = new Uint8Array(hashBuf);
    let hex = '';
    for (let i = 0; i < hashBytes.length; i++) {
      hex += hashBytes[i].toString(16).padStart(2, '0');
    }
    return hex;
  }

  computeModulo97(nissOrNumber, isPost2000 = false) {
    const clean = String(nissOrNumber).replace(/[^0-9]/g, '');
    const baseStr = isPost2000 ? ('2' + clean) : clean;
    const n = BigInt(baseStr);
    const remainder = Number(n % 97n);
    const checksum = remainder === 0 ? 97 : (97 - remainder);
    return {
      raw: baseStr,
      remainder,
      checksum,
      valid: checksum >= 1 && checksum <= 97
    };
  }

  async verifyLocalSignature(keySecret, message, testTamper = true) {
    const enc = new TextEncoder();
    const keyData = enc.encode(keySecret || 'AeterniTrak-Local-Hardware-Root-Key');
    const msgData = enc.encode(message || 'AeterniTrak-Canonical-TBS-Payload');

    const cryptoKey = await globalThis.crypto.subtle.importKey(
      'raw',
      keyData,
      { name: 'HMAC', hash: 'SHA-256' },
      false,
      ['sign', 'verify']
    );

    const sigBuf = await globalThis.crypto.subtle.sign('HMAC', cryptoKey, msgData);
    const signature = new Uint8Array(sigBuf);

    // Vérification nominale
    const valid = await globalThis.crypto.subtle.verify('HMAC', cryptoKey, signature, msgData);

    // Contrôle d'altération (anti-falsification)
    let tamperDetected = true;
    if (testTamper) {
      const tamperedSig = new Uint8Array(signature);
      tamperedSig[0] ^= 0x01; // Altération d'un seul bit
      const tamperedCheck = await globalThis.crypto.subtle.verify('HMAC', cryptoKey, tamperedSig, msgData);
      tamperDetected = !tamperedCheck;
    }

    let sigHex = '';
    for (let i = 0; i < signature.length; i++) {
      sigHex += signature[i].toString(16).padStart(2, '0');
    }

    return {
      valid,
      tamperDetected,
      signatureHex: sigHex
    };
  }

  finishTest() {
    const now = (typeof performance !== 'undefined' && performance.now) ? performance.now() : Date.now();
    this.endTime = now;
    this.duration = Math.max(1, Math.round(this.endTime - this.startTime));
    const success = this.failed === 0;

    if (this.badgeEl) {
      if (success) {
        this.badgeEl.className = 'test-badge test-badge-pass';
        this.badgeEl.textContent = `PASS (${this.duration} ms)`;
      } else {
        this.badgeEl.className = 'test-badge test-badge-fail';
        this.badgeEl.textContent = `FAIL (${this.failed} échec${this.failed > 1 ? 's' : ''})`;
      }
    }

    this.log(
      `------------------------------------------------------------\n` +
      `Verdict final : ${success ? 'SUCCÈS (PASS)' : 'ÉCHEC (FAIL)'} • ` +
      `${this.passed}/${this.assertions} assertions valides • Durée : ${this.duration} ms`,
      success ? 'pass' : 'fail'
    );

    const resultPayload = {
      type: 'AETERNI_TEST_RESULT',
      ucId: this.ucId,
      title: this.title,
      success,
      passed: this.passed,
      failed: this.failed,
      assertions: this.assertions,
      duration: this.duration
    };

    if (typeof window !== 'undefined') {
      if (window.parent && window.parent !== window) {
        window.parent.postMessage(resultPayload, '*');
      }
      window.dispatchEvent(new CustomEvent('aeterni-test-completed', { detail: resultPayload }));
    }

    return success;
  }
}

if (typeof globalThis !== 'undefined') {
  globalThis.MicroUseCaseTest = MicroUseCaseTest;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { MicroUseCaseTest };
} else if (typeof window !== 'undefined') {
  window.MicroUseCaseTest = MicroUseCaseTest;
}
