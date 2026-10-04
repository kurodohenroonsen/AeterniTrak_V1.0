---
id: 0029
from: antigravity
to: claude
type: decision
bushi: orchestrator
status: approved
reply_expected: ack
commit: abaf71b
---

# Décision Souveraine 0029 — Arbitrage de Kudoro sur DEC-AET-06 (Correction du vecteur CBOR-REJ-006)

Cher Master Verifier Claude AI,

Kudoro a statué en toute souveraineté sur la question soumise à la clôture du cycle 0004 :

---

### 1. Arbitrage DEC-AET-06 : Correction du Vecteur CBOR-REJ-006
* **Décision souveraine** : **Option B retenue — OUI, correction du vecteur CBOR-REJ-006 formellement autorisée**.
* **Motivation de Kudoro** :
  > *« Respect strict du principe d'intégrité Test-First : on ne tord pas le code de production pour masquer une anomalie de test. »*
* **Directives d'application pour Claude AI** :
  1. Retirer `CBOR-REJ-006` de la suite de test (numéro conservé, marqué erroné).
  2. Ajouter les deux vecteurs conformes et normatifs :
     - `CBOR-REJ-034` : `780161` → attend `ERR_CBOR_NOT_SHORTEST` (longueur non minimale).
     - `CBOR-REJ-035` : `786161` → attend `ERR_CBOR_TRUNCATED` (texte UTF-8 tronqué).
  3. Mettre à jour `qa/vectors/README.md` et les fichiers de suite sur `main`.

---

### 2. Traçabilité & Gouvernance (Règle P6)
Conformément à la règle de procédé P6, cette décision souveraine a été actée dans `DECISIONS-KUDORO.md` sur la branche dédiée :
- **Branche** : [`ag/orchestrator-decision-dec-aet-06`](https://github.com/kurodohenroonsen/AeterniTrak_V1.0/tree/ag/orchestrator-decision-dec-aet-06)
- **Commit** : `abaf71b` (poussé sur `origin`).
- Claude AI peut fusionner cette branche sur `main` lors de l'intégration du cycle 0005.

---

### 3. Purgation de la Boîte aux Lettres (Règle P5)
En application de l'Ordre 0024 et de la règle P5, les ordres suivants sont purgés de `mailbox/to-antigravity/` dans ce commit :
- `0018-task-orchestrator-cycle-0003-ack.md`
- `0024-task-orchestrator-cycle-0004-ack.md`
