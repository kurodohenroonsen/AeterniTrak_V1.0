# Protocole de Gouvernance et de Boîte aux Lettres — AeterniTrak V1.0

> **Canal Unique** : Branche Git `agent-mailbox`.  
> **Acteurs** : Claude AI (Master Verifier) ⇄ Antigravity (Orchestrateur & Swarm des 16 Bushi).  
> **Autorité Suprême** : Kudoro (Décisions souveraines dans `DECISIONS-KUDORO.md`).

---

## 1. Principe Fondateur de la Boîte aux Lettres Git

La branche `agent-mailbox` est le **seul et unique canal de transmission** asynchrone entre Claude AI et Antigravity.  
Kudoro ne copie-colle aucun prompt entre les deux intelligences artificielles : il donne le top départ (`go`), ou les tâches planifiées assurent le relais automatique.

### Cycle d'exécution d'un agent au réveil (`go` ou heartbeat) :
```bash
git fetch origin agent-mailbox
git checkout agent-mailbox && git pull --rebase origin agent-mailbox
```

1. **Lire `PROTOCOL.md`** et **sa boîte dédiée** :
   - Pour Antigravity : `mailbox/to-antigravity/`
   - Pour Claude AI : `mailbox/to-claude/`
2. **Si la boîte est vide** :
   - Consulter `BACKLOG.md` pour les tâches de fond ou s'arrêter. **Interdiction d'inventer des tâches non approuvées.**
3. **Si la boîte contient des messages** :
   - Traiter les messages **dans l'ordre numérique strict** (du plus petit au plus grand).
4. **Pour chaque message traité, un seul commit Git atomique** sur `agent-mailbox` qui :
   - Dépose la réponse dans la boîte du destinataire (`to-claude/NNNN-report-*.md` ou `to-antigravity/NNNN-task-*.md`) ;
   - **Supprime** le message d'origine traité de sa propre boîte via `git rm` (la boîte est une file d'attente FIFO, l'historique Git assure l'archivage) ;
   - Met à jour son fichier d'état dans `mailbox/state/` (`claude.md` ou `antigravity.md`).
5. **Synchronisation distante** :
   ```bash
   git pull --rebase origin agent-mailbox && git push origin agent-mailbox
   ```
   Chaque agent n'écrivant que dans la boîte de l'autre et dans son propre fichier d'état, aucun conflit Git n'est possible. En cas de rejet : `git pull --rebase` puis re-push. **Jamais de `--force`**.

---

## 2. Format Normalisé d'un Message

Nom de fichier : `NNNN-<type>-<bushi>-<slug>.md`  
Exemples : `0001-task-core-cbor-encoder.md`, `0002-report-crypto-ed25519-vectors.md`

En-tête YAML obligatoire :
```yaml
---
id: 0001
from: claude              # claude | antigravity
to: antigravity           # antigravity | claude
type: task                # task | report | redirect | question | alert | ack
bushi: bushi-01           # identifiant du Bushi concerné
branch: ag/bushi-01-cbor  # branche de travail associée
status: pending           # pending | in_progress | approved | rejected
reply_expected: report    # report | ack | decision
---
```

Corps du message :
- **Objectif** en une phrase claire.
- **Étapes d'action** numérotées.
- **Critères d'acceptation** et preuves attendues (chemins des vecteurs dans `qa/vectors/`, SHA de commit, logs bruts).

---

## 3. Matrice de Propriété des Branches & Fichiers

| Branche / Répertoire | Propriétaire Écriture | Propriétaire Lecture |
|---|---|---|
| `main` | **Claude AI** (après validation) | Tous |
| `agent-mailbox` | **Claude AI & Antigravity** (selon §1) | Tous |
| `ag/bushi-*` | **Antigravity** (via le Bushi délégué) | Claude AI |
| `qa/vectors/` | Claude AI (spécification) & Bushi 16 | Tous |
| `docs/functional/` | Antigravity (Bushi UX/Legal/Bio) & Claude | Tous |
| `docs/technical/` | Antigravity (Bushi Core/Crypto/HW) & Claude | Tous |

---

## 4. Règle Zéro-Clic macOS (Règle 7 bis JemmaPass)

Pour garantir une autonomie totale sans solliciter répétitivement l'utilisateur via des popups d'autorisation système macOS :
1. **Signature Invariante** : Antigravity et ses sous-agents ne lancent les commandes système que via :
   ```bash
   ./scripts/runner.sh
   ./scripts/runner.sh exec
   ./scripts/runner.sh task <fichier_tâche>
   ./scripts/runner.sh <action_prédéfinie>
   ```
2. **Fichier de commande dédié** : Toute commande ponctuelle est inscrite au préalable dans `mailbox/state/task.sh` puis exécutée via `./scripts/runner.sh exec`.
3. **Sorties capturées** : Les résultats sont systématiquement consignés dans `mailbox/state/out.txt` et lus via les outils d'inspection de fichiers.

---

## 5. Règle d'Or Métier & Règle Anti-Prion

1. **Règle d'Or Anti-Prion (Règlement CE 999/2001 & CE 142/2011)** :
   - Aucun lot de protéines transformées ne peut être attribué à la même espèce biologique (feed ban européen strict).
   - Le validateur cryptographique (Bushi 12) refuse catégoriquement d'émettre la signature Ed25519 en cas de correspondance d'espèces.
2. **Ségrégation des 4 Profils de Dépouilles** :
   - *Compagnie (Cat 1 mémoriel)* : Test LFA Pentobarbital obligatoire. Si positif -> Rejet incinération C1. Si négatif -> Pasteurisation 70°C 1h pour mémoire forestière.
   - *Faune Sauvage (Cat 1/2 DNF)* : Badge garde DNF, GPS, PCR épizooties, Stérilisation Méthode 1 (133°C, 3 bars, 20 min).
   - *Ferme (Cat 2)* : Boucle Sanitel, temps d'attente médicamenteux, Méthode 1, valorisation technique exclusive (biodiesel C2).
   - *Déchets d'Abattoir (Cat 1 / MRS)* : Document AFSCA, dénaturation bleu de méthylène 0,5%, Méthode 1, combustion cimenterie.

---

## 6. Cycle d'Amélioration Spec-First & Test-First

Tout travail respecte le cycle en 5 temps :
1. **Observer** : Constat factuel avec preuve (fichier, numéro de ligne, vecteur manquant).
2. **Proposer** : Rédiger la spécification dans `docs/`.
3. **Tester d'Abord** : Émettre le vecteur de test rouge dans `qa/vectors/`.
4. **Implémenter** : Réaliser la modification minimale faisant passer le vecteur au vert sur la branche `ag/bushi-*`.
5. **Valider** : Claude AI vérifie sur pièces, valide et fusionne sur `main`.

---

## 7. Réunions et Décisions

- **Réunions de Synchronisation** : Compte-rendus dans `mailbox/meetings/<AAAA-MM-JJ>/`.
- **Décisions Souveraines** : Seul Kudoro arbitre les changements de modèle économique, les ouvertures de branches critiques ou les questions juridiques majeures. Ses décisions sont consignées dans `DECISIONS-KUDORO.md`.
