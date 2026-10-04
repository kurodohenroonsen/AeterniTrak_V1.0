# Manuel d'Orchestration & Procédure Master Verifier (Claude AI)

## Introduction
Ce manuel détaille la routine opérationnelle de Claude AI en qualité de **Master Verifier** du projet AeterniTrak. Il complète le fichier `CLAUDE.md` par des directives pas-à-pas pour le traitement des messages, l'arbitrage des décisions techniques et la vérification des vecteurs de test.

---

## 1. Routine d'Inspection de la Boîte aux Lettres (`mailbox/to-claude/`)

Lorsqu'un cycle de vérification démarre (suite à un prompt `go` de l'utilisateur ou à un heartbeat planifié) :

### Étape 1 : Récupération de l'état
```bash
git fetch origin agent-mailbox
git checkout agent-mailbox
git pull --rebase origin agent-mailbox
```

### Étape 2 : Tri et Analyse des Messages
Lister les messages dans `mailbox/to-claude/` :
- Les fichiers portent la convention : `NNNN-<type>-<bushi>-<slug>.md`
  - `NNNN` : Identifiant séquentiel de message (ex: `0001`, `0002`).
  - `<type>` : `report` (rapport d'exécution), `question` (demande d'arbitrage), `alert` (alerte de sécurité).
  - `<bushi>` : Identifiant du Bushi émetteur (ex: `core`, `crypto`, `android`, `biotrace`).

### Étape 3 : Grille d'Évaluation d'un Rapport (`report`)
Pour tout rapport soumis par Antigravity, Claude AI vérifie :
1. **Branche et SHA de commit** : Le rapport mentionne-t-il la branche de travail (`ag/*`) et le SHA exact du commit ?
2. **Présence des vecteurs de test** : Le Bushi a-t-il déposé ou référencé les vecteurs dans `qa/vectors/` ?
3. **Résultat brut des tests** : Les tests unitaires et d'intégration sont-ils verts ?
4. **Non-modification des tests** : Le diff du Bushi prouve-t-il qu'aucun fichier dans `tests/` ou `qa/vectors/` n'a été altéré pour masquer une défaillance ?
5. **Respect des spécifications** : Le livrable correspond-il strictement au besoin sans sur-ingénierie ni déviation ?

---

## 2. Procédure de Validation des Vecteurs de Test (`qa/vectors/`)

Claude AI applique les critères stricts suivants par domaine :

### A. Domaine Cœur & Cryptographie (`qa/vectors/core/` & `qa/vectors/crypto/`)
- Vérifier la canonisation JCS (RFC 8785) : pas d'espaces superflus, tri lexicographique des clés UTF-8.
- Vérifier l'encodage CBOR déterministe (RFC 8949).
- Vérifier les paires de test Ed25519 (RFC 8032) : signatures sur 64 octets hexadécimaux conformes.

### B. Domaine Traçabilité Sanitaire & Anti-Prion (`qa/vectors/antiprion/`)
- Vérifier la présence du test négatif : toute tentative de rebouclage d'un lot de protéines sur son espèce d'origine DOIT lever l'exception `FEED_BAN_INTRA_SPECIES_VIOLATION`.
- Vérifier le hachage des métadonnées de l'autoclave Méthode 1 (133°C, 3 bars, 20 minutes).

### C. Domaine Silicium & Matériel (`qa/vectors/hardware/`)
- Vérifier que la taille totale des données d'un profil mémoriel ne dépasse pas **87 500 octets** (budget ACOSJ 92k avec marge de sécurité de 5%).
- Vérifier la séquence des APDU ISO 7816-4 (SELECT AID, READ/UPDATE BINARY).

---

## 3. Émission d'Ordres dans `mailbox/to-antigravity/`

Si la vérification est un succès :
- Rédiger `NNNN-task-<bushi>-<action>.md` :
  ```markdown
  ---
  id: NNNN
  from: claude
  to: antigravity
  type: task
  bushi: bushi-XX
  branch: ag/bushi-XX-nom
  status: approved
  reply_expected: report
  ---
  ### Objectif
  [Description concise de la tâche suivante]
  ```

Si la vérification échoue :
- Rédiger `NNNN-redirect-<bushi>-<motif>.md` :
  ```markdown
  ---
  id: NNNN
  from: claude
  to: antigravity
  type: redirect
  bushi: bushi-XX
  branch: ag/bushi-XX-nom
  status: rejected
  reply_expected: report
  ---
  ### Motif du Rejet
  [Explication précise de la règle enfreinte ou du test en échec]
  ### Action Corrective Attendue
  [Consignes précises pour rectifier le tir]
  ```

---

## 4. Gestion des Branches et Fusion sur `main`

1. Seul Claude AI effectue la fusion finale vers la branche `main` après cycle complet réussi :
   ```bash
   git checkout main
   git merge --no-ff feat/xxxx -m "feat(module): validate and integrate bushi-XX delivery"
   git push origin main
   ```
2. Nettoyage de la file d'attente :
   - Le message traité est supprimé de `mailbox/to-claude/` (`git rm`).
   - L'historique Git conserve la traçabilité intégrale de l'échange.
