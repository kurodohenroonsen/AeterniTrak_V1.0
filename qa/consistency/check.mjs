#!/usr/bin/env node
/**
 * AeterniTrak V1.0 — Garde-Fou Automatisé de Cohérence Inter-Fichiers
 * Conforme à DEC-AET-14 (Main gelée & check:consistency obligatoire)
 *
 * Ce script vérifie l'intégrité absolue de la cohérence inter-fichiers :
 * - V1 : Décisions souveraines (DEC-AET-XX existant dans DECISIONS-KUDORO.md)
 * - V2 : Cas d'usage (UC-XXX référencés dans docs existant dans scripts/portal_app*.py)
 * - V3 : Valeurs interdites (Blacklist : EF01-03, budgets EEPROM caducs, 4.40, termes juridiques sans réserve)
 * - V4 : Démonstrateur de faisabilité prospectif (sarcomusation humaine qualifiée selon DEC-AET-15)
 * - V5 : Zéro ressource distante (100% hors-ligne dans docs/*.html)
 */

import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, "../..");

// Couleurs ANSI
const RED = "\x1b[31m";
const GREEN = "\x1b[32m";
const YELLOW = "\x1b[33m";
const BLUE = "\x1b[34m";
const CYAN = "\x1b[36m";
const BOLD = "\x1b[1m";
const RESET = "\x1b[0m";

// Dossiers et extensions à ignorer pour les scans actifs
const IGNORE_PATTERNS = [
  /node_modules/,
  /\.git/,
  /\/archive\//,
  /qa\/vectors\//,
  /qa\/reports\//,
  /\.pyc$/,
  /\.DS_Store$/
];

function shouldIgnore(filePath) {
  const norm = filePath.replace(/\\/g, "/");
  return IGNORE_PATTERNS.some(pattern => pattern.test(norm));
}

function collectFiles(dir, filterFn) {
  const results = [];
  if (!fs.existsSync(dir)) return results;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (shouldIgnore(fullPath)) continue;
    if (entry.isDirectory()) {
      results.push(...collectFiles(fullPath, filterFn));
    } else if (entry.isFile() && (!filterFn || filterFn(fullPath))) {
      results.push(fullPath);
    }
  }
  return results;
}

// -----------------------------------------------------------------------------
// Structure des résultats
// -----------------------------------------------------------------------------
const violations = [];

function addViolation(ruleId, ruleTitle, filePath, lineNumber, snippet, reason) {
  const relPath = path.relative(PROJECT_ROOT, filePath).replace(/\\/g, "/");
  violations.push({
    ruleId,
    ruleTitle,
    file: relPath,
    line: lineNumber,
    snippet: snippet.trim(),
    reason
  });
}

// =============================================================================
// VÉRIFICATION 1 : Décisions Souveraines (DEC-AET-XX)
// =============================================================================
function verifySovereignDecisions() {
  const decisionsFile = path.join(PROJECT_ROOT, "DECISIONS-KUDORO.md");
  if (!fs.existsSync(decisionsFile)) {
    violations.push({
      ruleId: "V1",
      ruleTitle: "Décisions souveraines",
      file: "DECISIONS-KUDORO.md",
      line: 1,
      snippet: "",
      reason: "Le fichier souverain DECISIONS-KUDORO.md est introuvable."
    });
    return;
  }

  const decisionsContent = fs.readFileSync(decisionsFile, "utf-8");
  const knownDecisions = new Set();
  const decisionRegex = /\bDEC-AET-(\d{2})\b/g;
  let dMatch;
  while ((dMatch = decisionRegex.exec(decisionsContent)) !== null) {
    knownDecisions.add(`DEC-AET-${dMatch[1]}`);
  }

  // Fichiers à auditer : bushi/*.md, docs/*.md, AGENTS.md, CLAUDE.md, BACKLOG.md
  const targetFiles = [];
  const bushiFiles = collectFiles(path.join(PROJECT_ROOT, "bushi"), f => f.endsWith(".md"));
  const docsFiles = collectFiles(path.join(PROJECT_ROOT, "docs"), f => f.endsWith(".md"));
  targetFiles.push(...bushiFiles, ...docsFiles);

  for (const rootDoc of ["AGENTS.md", "CLAUDE.md", "BACKLOG.md"]) {
    const p = path.join(PROJECT_ROOT, rootDoc);
    if (fs.existsSync(p)) targetFiles.push(p);
  }

  for (const file of targetFiles) {
    const content = fs.readFileSync(file, "utf-8");
    const lines = content.split("\n");
    lines.forEach((line, idx) => {
      // Ignore les placeholders comme DEC-AET-XX
      const refRegex = /\bDEC-AET-([0-9A-Za-z_-]+)\b/g;
      let match;
      while ((match = refRegex.exec(line)) !== null) {
        const fullToken = match[0];
        const suffix = match[1];
        if (suffix === "XX" || suffix === "X") continue; // Placeholder de documentation
        if (!knownDecisions.has(fullToken)) {
          addViolation(
            "V1",
            "Décision souveraine non répertoriée",
            file,
            idx + 1,
            line,
            `L'identifiant souverain '${fullToken}' est cité mais n'existe pas formellement dans DECISIONS-KUDORO.md.`
          );
        }
      }
    });
  }
}

// =============================================================================
// VÉRIFICATION 2 : Cas d'Usage (UC-XXX)
// =============================================================================
function verifyUseCases() {
  const scriptsDir = path.join(PROJECT_ROOT, "scripts");
  const portalScripts = collectFiles(scriptsDir, f => /portal_app.*\.py$/.test(path.basename(f)));
  const knownUCs = new Set();

  for (const script of portalScripts) {
    const content = fs.readFileSync(script, "utf-8");
    const ucRegex = /\bUC-\d{3}\b/g;
    let match;
    while ((match = ucRegex.exec(content)) !== null) {
      knownUCs.add(match[0]);
    }
  }

  // Fichiers doc à auditer : docs/*.md, bushi/*.md, AGENTS.md, CLAUDE.md, BACKLOG.md
  const docFiles = [
    ...collectFiles(path.join(PROJECT_ROOT, "docs"), f => f.endsWith(".md")),
    ...collectFiles(path.join(PROJECT_ROOT, "bushi"), f => f.endsWith(".md"))
  ];
  for (const rootDoc of ["AGENTS.md", "CLAUDE.md", "BACKLOG.md"]) {
    const p = path.join(PROJECT_ROOT, rootDoc);
    if (fs.existsSync(p)) docFiles.push(p);
  }

  for (const file of docFiles) {
    const content = fs.readFileSync(file, "utf-8");
    const lines = content.split("\n");
    lines.forEach((line, idx) => {
      const refRegex = /\bUC-([0-9A-Za-z_-]+)\b/g;
      let match;
      while ((match = refRegex.exec(line)) !== null) {
        const fullToken = match[0];
        const suffix = match[1];
        if (suffix === "XXX" || suffix === "YYY" || suffix === "NNN") continue; // Placeholders
        if (!knownUCs.has(fullToken)) {
          addViolation(
            "V2",
            "Cas d'usage non implémenté",
            file,
            idx + 1,
            line,
            `Le cas d'usage '${fullToken}' référencé dans la documentation n'existe dans aucun fichier scripts/portal_app*.py.`
          );
        }
      }
    });
  }
}

// =============================================================================
// VÉRIFICATION 3 : Valeurs Interdites (Blacklist)
// =============================================================================
function verifyBlacklist() {
  const filesToScan = [
    ...collectFiles(path.join(PROJECT_ROOT, "docs"), f => f.endsWith(".md") || f.endsWith(".html")),
    ...collectFiles(path.join(PROJECT_ROOT, "bushi"), f => f.endsWith(".md")),
    ...collectFiles(path.join(PROJECT_ROOT, "scripts"), f => f.endsWith(".py") || f.endsWith(".mjs")),
    ...collectFiles(path.join(PROJECT_ROOT, "qa"), f => (f.endsWith(".mjs") || f.endsWith(".ts") || f.endsWith(".js")) && !f.includes("/consistency/"))
  ];

  for (const rootDoc of ["AGENTS.md", "CLAUDE.md", "BACKLOG.md"]) {
    const p = path.join(PROJECT_ROOT, rootDoc);
    if (fs.existsSync(p)) filesToScan.push(p);
  }

  // Regex pour la blacklist
  const obsoleteEfRegex = /\bEF0[1-9]\b/i;
  const obsoleteEepromBudgetRegex = /\b(87[\s\u00A0]?500|87[\s\u00A0]?560|4[\s\u00A0]?600|7[\s\u00A0]?680)\b/;
  const arbitraryPriceRegex = /\b4[,\.]40\b/;
  const legalTermRegex = /\b(force\s+exécutoire|opposable)\b/i;
  const legalReserveRegex = /(?:sans|aucun[e]?|n'a\s+pas\s+de|pas\s+de|ne\s+bénéficie\s+d'aucune|réserve|reserve|confirmer\s+par\s+un\s+juriste|non\s+opposable|inopposable)/i;

  for (const file of filesToScan) {
    const content = fs.readFileSync(file, "utf-8");
    const lines = content.split("\n");

    lines.forEach((line, idx) => {
      // 3.1 Refus de nomenclature EF caduque (EF01, EF02, EF03...)
      const efMatch = obsoleteEfRegex.exec(line);
      if (efMatch) {
        addViolation(
          "V3-EF",
          "Nomenclature EF caduque",
          file,
          idx + 1,
          line,
          `Nomenclature caduque '${efMatch[0]}' détectée. La norme canonique est 'EF-0' à 'EF-5'.`
        );
      }

      // 3.2 Refus des budgets EEPROM caducs (87 500, 87 560, 4 600, 7 680)
      const eepromMatch = obsoleteEepromBudgetRegex.exec(line);
      if (eepromMatch) {
        addViolation(
          "V3-EEPROM",
          "Budget EEPROM caduc",
          file,
          idx + 1,
          line,
          `Valeur de budget EEPROM caduque '${eepromMatch[0]}' détectée. Les valeurs canoniques sont 92 160 total, 86 528 utile, 5 632 réserve.`
        );
      }

      // 3.3 Refus de prix arbitraire (4,40 ou 4.40)
      const priceMatch = arbitraryPriceRegex.exec(line);
      if (priceMatch) {
        addViolation(
          "V3-PRICE",
          "Prix chiffré arbitraire proscrit",
          file,
          idx + 1,
          line,
          `Mention de prix chiffré arbitraire '${priceMatch[0]}' détectée. Directive DEC-AET-11 : discrétion tarifaire absolue imposée.`
        );
      }

      // 3.4 Refus des termes juridiques abusifs sans réserve expresse
      const legalMatch = legalTermRegex.exec(line);
      if (legalMatch) {
        if (!legalReserveRegex.test(line)) {
          addViolation(
            "V3-LEGAL",
            "Terme juridique abusif sans réserve",
            file,
            idx + 1,
            line,
            `Terme juridique '${legalMatch[0]}' employé comme assertion positive sans réserve légale expresse (ex. 'sous réserve d'homologation', 'référence à confirmer par un juriste').`
          );
        }
      }
    });
  }
}

// =============================================================================
// VÉRIFICATION 4 : Démonstrateur de Faisabilité Prospectif (DEC-AET-15)
// =============================================================================
function verifyProspectiveDemonstrator() {
  const filesToScan = [
    ...collectFiles(path.join(PROJECT_ROOT, "docs/functional"), f => f.endsWith(".md")),
    ...collectFiles(path.join(PROJECT_ROOT, "scripts"), f => /portal_app.*\.py$/.test(path.basename(f))),
    path.join(PROJECT_ROOT, "docs/usecases/index.html")
  ].filter(f => fs.existsSync(f));

  // Détection de sarcomusation appliquée aux dépouilles humaines ou human_remains
  const humanSarcoRegex = /(?:sarcomusation\s+(?:des?\s+)?(?:dépouilles?\s+)?humaine?s?|sarcomusation\s+appliquée\s+à\s+l'humain|human_remains)/i;
  const qualifierRegex = /(?:démonstrateur|demonstrateur|prospecti[fv])/i;

  for (const file of filesToScan) {
    const content = fs.readFileSync(file, "utf-8");
    const lines = content.split("\n");

    lines.forEach((line, idx) => {
      if (humanSarcoRegex.test(line)) {
        // Vérifie si la ligne ou les lignes adjacentes contiennent 'Démonstrateur' ou 'Prospectif'
        const windowContext = [
          lines[idx - 1] || "",
          line,
          lines[idx + 1] || ""
        ].join(" ");

        if (!qualifierRegex.test(windowContext)) {
          addViolation(
            "V4",
            "Sarcomusation humaine non qualifiée",
            file,
            idx + 1,
            line,
            "Toute mention de sarcomusation humaine / human_remains doit impérativement comporter le terme 'Démonstrateur' ou 'Prospectif' (directive DEC-AET-15)."
          );
        }
      }
    });
  }
}

// =============================================================================
// VÉRIFICATION 5 : Zéro Ressource Distante (100% Hors-Ligne)
// =============================================================================
function verifyZeroRemoteResources() {
  const htmlFiles = collectFiles(path.join(PROJECT_ROOT, "docs"), f => f.endsWith(".html"));
  const remoteTagRegex = /<(link|script|img)\b[^>]*\b(href|src)\s*=\s*["'](https?:\/\/[^"']+)["'][^>]*>/gi;

  for (const file of htmlFiles) {
    const content = fs.readFileSync(file, "utf-8");
    const lines = content.split("\n");

    lines.forEach((line, idx) => {
      let match;
      remoteTagRegex.lastIndex = 0;
      while ((match = remoteTagRegex.exec(line)) !== null) {
        const tagName = match[1];
        const url = match[3];
        addViolation(
          "V5",
          "Ressource distante détectée dans HTML hors-ligne",
          file,
          idx + 1,
          line,
          `Le tag <${tagName}> charge une ressource externe distante (${url}). L'architecture AeterniTrak impose le mode 100% hors-ligne local.`
        );
      }
    });
  }
}

// =============================================================================
// Exécution Principale
// =============================================================================
function main() {
  console.log(`${BOLD}${CYAN}============================================================${RESET}`);
  console.log(`${BOLD}${CYAN}   AeterniTrak V1.0 — Garde-Fou Automatisé de Cohérence      ${RESET}`);
  console.log(`${BOLD}${CYAN}   Vérifications Inter-Fichiers & Audit Réglementaire        ${RESET}`);
  console.log(`${BOLD}${CYAN}============================================================${RESET}\n`);

  verifySovereignDecisions();
  verifyUseCases();
  verifyBlacklist();
  verifyProspectiveDemonstrator();
  verifyZeroRemoteResources();

  if (violations.length === 0) {
    console.log(`${GREEN}${BOLD}✓ SUCCÈS TOTAL : 100% des vérifications de cohérence sont conformes.${RESET}`);
    console.log(`  - V1 : Toutes les décisions citées existent dans DECISIONS-KUDORO.md.`);
    console.log(`  - V2 : Tous les cas d'usage référencés existent dans scripts/portal_app*.py.`);
    console.log(`  - V3 : Aucune valeur blacklistée (EF, budgets EEPROM, tarifs, assertions juridiques sans réserve).`);
    console.log(`  - V4 : Conformité prospective DEC-AET-15 pour la sarcomusation.`);
    console.log(`  - V5 : Aucune ressource distante dans la documentation HTML (100% hors-ligne).\n`);
    process.exit(0);
  } else {
    console.error(`${RED}${BOLD}✗ ÉCHEC DU CONTRÔLE DE COHÉRENCE : ${violations.length} violation(s) détectée(s) :${RESET}\n`);

    // Groupement par règle
    const grouped = new Map();
    for (const v of violations) {
      if (!grouped.has(v.ruleId)) grouped.set(v.ruleId, []);
      grouped.get(v.ruleId).push(v);
    }

    for (const [ruleId, list] of grouped.entries()) {
      console.error(`${BOLD}${YELLOW}[${ruleId}] ${list[0].ruleTitle} (${list.length} occurrence${list.length > 1 ? "s" : ""}) :${RESET}`);
      for (const item of list) {
        console.error(`  ${RED}• ${item.file}:${item.line}${RESET}`);
        console.error(`    ${BOLD}Raison  :${RESET} ${item.reason}`);
        console.error(`    ${BOLD}Extrait :${RESET} ${CYAN}${item.snippet}${RESET}\n`);
      }
    }

    console.error(`${RED}${BOLD}Arrêt avec code d'erreur 1. Veuillez corriger les anomalies ci-dessus.${RESET}\n`);
    process.exit(1);
  }
}

main();
