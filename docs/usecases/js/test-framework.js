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
    const detail = `Budget partition '${partitionName}' : ${bytes} / ${maxLimit} octets (${Math.round(bytes / maxLimit * 100)}%)`;
    return this.assertTrue(ok, ok ? `${detail} [CONFORME]` : `${detail} [DÉPASSEMENT EEPROM]`);
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

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { MicroUseCaseTest };
} else if (typeof window !== 'undefined') {
  window.MicroUseCaseTest = MicroUseCaseTest;
}
