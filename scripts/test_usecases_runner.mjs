#!/usr/bin/env node
/**
 * AeterniTrak V1.0 — Lanceur Headless Automatisé des 100 Micro Use-Cases
 * Conforme à DEC-AET-08 & DEC-AET-09.
 * Exécute l'intégralité des bancs de test unitaires in-silico des 100 micro use-cases.
 */

import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, "..");
const DOCS_DIR = path.join(PROJECT_ROOT, "docs", "usecases");

// Importer le test-framework
const frameworkCode = fs.readFileSync(path.join(DOCS_DIR, "js", "test-framework.js"), "utf8");

// Couleurs ANSI
const GREEN = "\x1b[32m";
const RED = "\x1b[31m";
const CYAN = "\x1b[36m";
const BOLD = "\x1b[1m";
const RESET = "\x1b[0m";

console.log(`${BOLD}============================================================${RESET}`);
console.log(`${BOLD}AeterniTrak V1.0 — Audit Headless des 100 Micro Use-Cases${RESET}`);
console.log(`${BOLD}Exécution In-Silico des Bancs de Test Unitaires Embarqués${RESET}`);
console.log(`${BOLD}============================================================${RESET}`);

let totalCases = 0;
let passedCases = 0;
let failedCases = 0;
const failures = [];

for (const appId of ["app1", "app2", "app3", "app4"]) {
  const appDir = path.join(DOCS_DIR, appId);
  if (!fs.existsSync(appDir)) continue;

  const files = fs.readdirSync(appDir).filter(f => f.startsWith("UC-") && f.endsWith(".html")).sort();
  console.log(`\n${CYAN}--- ${appId.toUpperCase()} (${files.length} use-cases) ---${RESET}`);

  for (const file of files) {
    totalCases++;
    const filePath = path.join(appDir, file);
    const html = fs.readFileSync(filePath, "utf8");

    // Extraire les données de phases et le script du test
    const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>\s*<\/body>/);
    if (!scriptMatch) {
      failedCases++;
      failures.push({ file, reason: "Balise <script> de test introuvable" });
      console.log(`  ${RED}FAIL${RESET} ${file} : Script de test manquant`);
      continue;
    }

    const scriptCode = scriptMatch[1];

    // Créer un environnement DOM simulé et isolé dans une VM Node
    const logs = [];
    const contextObj = {
      console: {
        log: (...args) => logs.push(args.join(" ")),
        error: (...args) => logs.push("[ERR] " + args.join(" "))
      },
      crypto: globalThis.crypto,
      globalThis: null,
      TextEncoder: globalThis.TextEncoder,
      TextDecoder: globalThis.TextDecoder,
      BigInt: globalThis.BigInt,
      Number: globalThis.Number,
      String: globalThis.String,
      Math: globalThis.Math,
      JSON: globalThis.JSON,
      Date: globalThis.Date,
      performance: globalThis.performance,
      CustomEvent: class CustomEvent { constructor(type, opts) { this.type = type; this.detail = opts?.detail; } },
      URLSearchParams: class { get() { return "0"; } },
      document: {
        getElementById: (id) => ({
          id,
          innerHTML: "",
          appendChild: () => {},
          classList: { remove: () => {}, add: () => {} },
          scrollTop: 0,
          scrollHeight: 100,
          addEventListener: () => {}
        }),
        querySelectorAll: () => [],
        createElement: (tag) => ({
          tag,
          className: "",
          innerHTML: ""
        })
      },
      window: {
        location: { search: "" },
        addEventListener: () => {},
        dispatchEvent: () => {}
      },
      setTimeout: (fn) => fn(),
      setInterval: () => 1,
      clearInterval: () => {}
    };
    contextObj.globalThis = contextObj;
    contextObj.window.parent = contextObj.window;

    const vmContext = vm.createContext(contextObj);

    try {
      // 1. Charger le test framework
      vm.runInContext(frameworkCode, vmContext);

      // 2. Charger et exécuter le script du micro use-case, et renvoyer l'instance
      const instance = vm.runInContext(scriptCode + "\n; unitTestInstance;", vmContext);
      if (!instance) {
        throw new Error("Variable unitTestInstance non instanciée");
      }

      const res = await instance.run();
      if (res && instance.failed === 0) {
        passedCases++;
        console.log(`  ${GREEN}PASS${RESET} ${file} : ${instance.title} (${instance.passed} assertions, ${instance.duration} ms)`);
      } else {
        failedCases++;
        failures.push({ file, reason: `${instance.failed} échecs d'assertion` });
        console.log(`  ${RED}FAIL${RESET} ${file} : ${instance.failed} assertions échouées`);
      }
    } catch (err) {
      failedCases++;
      failures.push({ file, reason: err.message });
      console.log(`  ${RED}FAIL${RESET} ${file} : Exception: ${err.message}`);
    }
  }
}

console.log(`\n${BOLD}============================================================${RESET}`);
console.log(`BILAN GLOBAL : ${passedCases} / ${totalCases} PASS (100% Hors-Ligne)`);
console.log(`${BOLD}============================================================${RESET}`);

if (failedCases > 0) {
  console.error(`\n${RED}Échecs détectés (${failedCases}) :${RESET}`);
  failures.forEach(f => console.error(`  - ${f.file}: ${f.reason}`));
  process.exit(1);
} else {
  console.log(`\n${GREEN}✓ PERFECTION ABSOLUE : Les 100 Micro Use-Cases sont 100% verts !${RESET}`);
  process.exit(0);
}
