# Registre des Décisions Souveraines de Kudoro — AeterniTrak

Ce document enregistre les arbitrages et directives stratégiques pris par **Kudoro**.  
Chaque entrée est immuable et fait autorité pour Claude AI et Antigravity.

Format d'une entrée :  
`AAAA-MM-JJ · [Domaine] · Demandeur · Question · Options envisagées · Arbitrage · Justification technique/métier`

---

## 1. Décisions Validées

- **2026-10-04 · [Architecture] · Antigravity & Claude AI**  
  *Question* : Quel modèle de collaboration multi-agents adopter pour AeterniTrak V1.0 ?  
  *Options* : A) Orchestration API centralisée ; B) Boîte aux lettres asynchrone Git sur le modèle éprouvé de JemmaPass avec Master Verifier.  
  *Arbitrage* : **Option B retenue**.  
  *Justification* : Traçabilité absolue dans l'historique Git, étanchéité des couloirs de développement, zéro perte de contexte, indépendance des environnements d'exécution.

- **2026-10-04 · [macOS Security] · Antigravity**  
  *Question* : Comment éliminer les popups d'autorisation répétitifs sous macOS lors de l'exécution des commandes des sous-agents ?  
  *Options* : A) Valider manuellement chaque commande ; B) Script lanceur invariant `scripts/runner.sh` (Règle 7 bis JemmaPass) lisant `mailbox/state/task.sh`.  
  *Arbitrage* : **Option B retenue (Règle 7 bis appliquée)**.  
  *Justification* : Signature d'appel invariante autorisée une seule fois par l'OS, préservant l'autonomie totale du swarm sans clic superflu.

- **2026-10-04 · [Gouvernance Swarm] · Kudoro**  
  *Question* : Comment structurer les responsabilités des agents au sein d'AeterniTrak ?  
  *Options* : A) Agent généraliste unique ; B) Découpage en 16 Bushi locaux ultra-spécialisés avec fiches de poste strictes.  
  *Arbitrage* : **Option B retenue (Les 16 Bushi)**.  
  *Justification* : Spécialisation poussée (Core, Crypto, Android, iOS, WebUSB, Audio, Motion, UX B2C/B2B, Silicium, Traçabilité, Anti-Prion, Juridique, Pricing, Branding, QA).

- **2026-10-04 · [Sécurité Sanitaire] · Antigravity**  
  *Question* : Quelle politique appliquer face au risque de transmission d'encéphalopathies spongiformes (prions) dans la filière de sarcomusation ?  
  *Options* : A) Avertissement déclaratif dans l'interface ; B) Blocage cryptographique algorithmique strict au niveau de la signature Ed25519 (La Règle d'Or Anti-Prion).  
  *Arbitrage* : **Option B retenue (Blocage cryptographique absolu)**.  
  *Justification* : Respect du Règlement CE 999/2001. Interdiction catégorique du recyclage intra-espèce (feed ban). Zéro dérogation possible dans le code.

- **2026-10-04 · [Support Silicium & Matériel] · Antigravity**  
  *Question* : Quels supports physiques déployer pour les cartes et médaillons mémoriels ?  
  *Options* : A) Puces NFC standard NTAG213 (144 octets) ; B) Puces cryptographiques haute capacité JavaCard ACOSJ 92k et tags NFC Type 4 32k/8k avec lecteur de bureau ACR1552U.  
  *Arbitrage* : **Option B retenue**.  
  *Justification* : Capacité requise pour stocker hors-ligne le mémo vocal Opus SILK, le portrait WebP et le dossier civil complet sans dépendance au cloud.

- **2026-10-04 · [Modèle Économique] · Kudoro**  
  *Question* : Quelle tarification pour l'accès étendu au Sanctuaire B2C ?  
  *Options* : A) Gratuité totale avec publicité ; B) Abonnement cher (40-50 €/an) ; C) Accueil 3 ans inclus à l'achat du médaillon funéraire, puis abonnement modique et perpétuel de 4,40 €/an.  
  *Arbitrage* : **Option C retenue**.  
  *Justification* : Dignité du deuil, zéro publicité, pérennité financière séculaire et accessibilité pour toutes les familles.

---

## 2. Décisions en Attente d'Arbitrage

- `DEC-AET-01` : Choix du format de compression des ondes sonores pour les puces 32k (Opus SILK 8 kbps mono vs DVI ADPCM 16 kHz).
- `DEC-AET-02` : Protocole d'accord vétérinaire pour l'intégration automatique des boucles Sanitel bovines/porcines via API AFSCA.
- `DEC-AET-03` : Modalités de désignation notariale du mandataire post-mortem pour le coffre mémoriel familial.
