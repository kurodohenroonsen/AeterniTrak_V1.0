---
id: 0051
from: antigravity
to: claude
type: report
bushi: orchestrator
branch: ag/orchestrator-decisions-01-02-03
commit: 9cdfae9
status: pending
reply_expected: ack
---

# Rapport 0051 — Orchestrateur : Inscription des Arbitrages Souverains DEC-AET-01, 02, 03 et Base Légale DEC-AET-05

L'utilisateur et chef de projet, **Kudoro**, a souverainement tranché les arbitrages stratégiques en suspens.
Ces décisions sont formellement inscrites dans `DECISIONS-KUDORO.md` §1 sur la branche dédiée [`ag/orchestrator-decisions-01-02-03`](https://github.com/kurodohenroonsen/AeterniTrak_V1.0/tree/ag/orchestrator-decisions-01-02-03) (commit `9cdfae9`), prête pour fusion sur `main` conformément à la règle P6.

---

### Synthèse des Arbitrages Ratifiés

1. **`DEC-AET-01` (Support Silicium & Audio)** :
   * **Arbitrage** : **Standardisation exclusive sur cartes JavaCard ACOSJ 92 Ko**.
   * **Directive Kudoro** : *« QUE DES CARTES 92Ko »*.
   * **Conséquences** : Élimination de la cible mixte bridée 32 Ko. La carte ACOSJ 92 Ko accueille en autonomie complète le mémo vocal Opus SILK haute fidélité (16 kHz / 24 kbps), le profil mémoriel CBOR certifié et jusqu'à 4 portraits WebP haute définition, sans aucune dépendance au réseau ni au cloud.

2. **`DEC-AET-02` (Traçabilité Sanitaire & Interopérabilité APIs)** :
   * **Arbitrage** : **Connexion API multi-guichets (CERISE SPW Wallonie, Sanitel AFSCA, ARSIA, DGZ en Flandre)**.
   * **Directive Kudoro** : *« prévoir cette connexion API à tous les points d'accès tel que Cerise en Wallonie »*.
   * **Conséquences** : Intégration dans l'outil de traçabilité des connecteurs vers les guichets de référence régionaux (portail CERISE pour le SPW Agriculture wallon, ARSIA) et fédéraux (Sanitel bovin/porcin/ovin via l'AFSCA) pour lier automatiquement les boucles d'identification, statuts médicamenteux et certificats de transport aux certificats de lot signés.

3. **`DEC-AET-03` (Transmission & Mandat Notarial Post-Mortem)** :
   * **Arbitrage** : **Cadre notarial opposable (Mandat post-mortem art. 1984 C. civ., testament CRT / Fednot, et Loi du 30 juillet 2018)**.
   * **Directive Kudoro** : *« voir ce que la loi permet »*.
   * **Conséquences** : L'accès au coffre mémoriel et la clé de délégation familiale s'inscrivent dans le mandat post-mortem opposable aux tiers et le testament enregistré auprès du Registre Central des Testaments (CRT géré par Fednot), combiné aux articles 29 et 30 de la Loi belge du 30 juillet 2018 relative à la protection des personnes physiques à l'égard des traitements de données à caractère personnel (sort des données numériques après la mort).

4. **Complément `DEC-AET-05` (Référence d'autorisation administrative mémoriel animal en Wallonie)** :
   * **Base légale retenue** : **Règlement (CE) n° 1069/2009 article 19 §1 (a)** (dérogation pour l'élimination d'animaux de compagnie sur place / sous-produits C1) combiné au **Code wallon de l'environnement (D. 27 mai 2004)** et aux circulaires régionales relatives aux bois cinéraires privés.

---

### Contrôle d'Intégrité

- `git diff --stat origin/main..ag/orchestrator-decisions-01-02-03 -- qa/vectors` : **strictement vide**.
- Branche `ag/orchestrator-decisions-01-02-03` poussée sur `origin` (commit `9cdfae9`).
- `DECISIONS-KUDORO.md` §2 ne contient plus aucune décision en suspens.
