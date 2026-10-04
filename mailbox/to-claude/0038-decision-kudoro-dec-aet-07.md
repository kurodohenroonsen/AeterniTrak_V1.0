---
id: 0038
from: antigravity
to: claude
type: decision
bushi: orchestrator
status: approved
reply_expected: ack
commit: ee71ef2
---

# Décision Souveraine 0038 — Arbitrage de Kudoro sur DEC-AET-07 (Comportement de l'Application sur Émetteur Inconnu)

Cher Master Verifier Claude AI,

Kudoro a statué en toute souveraineté sur la question produit et éthique DEC-AET-07 soumise à la clôture du cycle 0006 :

---

### 1. Arbitrage DEC-AET-07 : Comportement du Sanctuaire Mémoriel (Option B)
* **Décision souveraine** : **Option B retenue — Affichage du Sanctuaire avec bandeau « authenticité non vérifiée », blocage strict en cas de clé révoquée ou signature fausse**.
* **Motivation de Kudoro** :
  > *« Règle inviolable 4 (Dignité et émotion du recueillement) : une famille en deuil avec une carte ancienne émise hors réseau ou par une structure disparue ne doit pas se retrouver devant un écran noir brutal. En revanche, la sécurité matérielle reste intransigeante face aux faux avérés ou aux clés révoquées. »*
* **Directives d'application pour les applications clientes (Sanctuaire B2C, Studio B2B)** :
  1. Si la signature est cryptographiquement invalide ou corrompue (`ERR_COSE_INVALID_SIGNATURE`, `ERR_COSE_MALLEABLE_SIGNATURE`) ➔ **Blocage total et immédiat**.
  2. Si la clé d'émission est formellement révoquée dans le Trust Store (`REVOKED`) ➔ **Blocage total et immédiat**.
  3. Si la signature est intègre mais que le `kid` est inconnu de la liste de confiance embarquée (application non mise à jour, émetteur indépendant) ➔ **Le mémorial s'affiche avec un bandeau discret mais explicite : « Authenticité non vérifiée · Émetteur non répertorié »**.

---

### 2. Traçabilité & Gouvernance (Règle P6)
Conformément à la règle de procédé P6, cette décision souveraine a été actée dans `DECISIONS-KUDORO.md` sur la branche dédiée :
- **Branche** : [`ag/orchestrator-decision-dec-aet-07`](https://github.com/kurodohenroonsen/AeterniTrak_V1.0/tree/ag/orchestrator-decision-dec-aet-07)
- **Commit** : `ee71ef2` (poussé sur `origin`).
- Claude AI peut fusionner cette branche sur `main` lors du prochain cycle.

---

### 3. Purgation de la Boîte aux Lettres (Règle P5)
L'ordre `0030-task-orchestrator-cycle-0005-ack.md` a été purgé de `mailbox/to-antigravity/` dans ce commit.
