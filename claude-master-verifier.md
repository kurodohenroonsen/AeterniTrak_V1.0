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
6. **Alignement Applicatif (`DEC-AET-08`)** : Le livrable s'inscrit-il clairement dans l'une des 4 applications souveraines (App 1 PaxStudio, App 2 PaxStation, App 3 Sanctuaire, App 4 Filière) ?

---

## 2. Procédure de Validation des Vecteurs de Test (`qa/vectors/`)

Claude AI applique les critères stricts suivants par domaine :

### A. Domaine Cœur & Cryptographie (`qa/vectors/core/` & `qa/vectors/crypto/`)
- Vérifier la canonisation JCS (RFC 8785) : pas d'espaces superflus, tri lexicographique des clés UTF-8.
- Vérifier l'encodage CBOR déterministe canonique (RFC 8949 §4.2.1) : entiers minimaux, tri strict des clés.
- **Contrôle systématique de l'agilité COSE ES256 & Ed25519 (`DEC-AET-04`)** :
  - Vérifier la prise en charge bidirectionnelle de l'enveloppe `COSE_Sign1` (RFC 9052) :
    - **ES256** (`alg: -7`, NIST P-256) : signature de 64 octets ($r \parallel s$), réservée aux enclaves matérielles certifiées (Apple Secure Enclave, Android StrongBox, ACOSJ 92 Ko).
    - **Ed25519** (`alg: -8`, Edwards Ed25519 / RFC 8032) : signature de 64 octets, pour les signatures logicielles et la filière décentralisée.
  - **Contrôle anti-malléabilité du $s$ bas (BSI TR-03111)** : Exiger impérativement $s \le \lfloor n/2 \rfloor$ pour toute signature ES256. Rejeter sans exception toute signature en forme $s$ haut ($s > \lfloor n/2 \rfloor$).
  - Vérifier l'identifiant de clé `kid` : strictement constitué des 16 premiers octets du SHA-256 de la clé publique brute non compressée.
  - Vérifier la conformité des types MIME protégés `typ` (`application/aeternitrak-profile+cbor` pour les profils et `application/aeternitrak-batch-claim+cbor` pour les certificats de lot).

### B. Domaine Traçabilité Sanitaire & Anti-Prion (`qa/vectors/antiprion/`)
- Vérifier la présence du test négatif : toute tentative de rebouclage d'un lot de protéines sur son espèce d'origine DOIT lever l'exception `FEED_BAN_INTRA_SPECIES_VIOLATION`.
- Vérifier le hachage des métadonnées de l'autoclave Méthode 1 (133°C, 3 bars, 20 minutes).
- Vérifier la ségrégation stricte des 4 profils de dépouilles (Compagnie, Faune Sauvage DNF, Ferme, Abattoir/MRS).

### C. Domaine Silicium & Matériel (`qa/vectors/hardware/`)
- **Consécration exclusive de l'ACOSJ 92 Ko (`DEC-AET-01`)** :
  - Rejeter catégoriquement toute référence à des cibles 32 Ko obsolètes.
  - La cible matérielle unique est la puce cryptographique JavaCard ACOSJ 92 Ko (capacité totale : 92 160 octets).
- **Vérification du partitionnement strict `STORAGE-001` (EF-0 à EF-5)** :
  - `EF-0` (`0x0000`) : En-tête silicium TLV propriétaire, UID matériel, compteur monotone et flags (512 octets / 0,55 %).
  - `EF-1` (`0x0001` / `EF.ID`) : Profil civil CBOR canonique RFC 8949 (2 048 octets / 2 Ko / 2,22 %).
  - `EF-2` (`0x0002` / `EF.IMG`) : Portrait visuel WebP haute définition (20 480 octets / 20 Ko / 22,22 %).
  - `EF-3` (`0x0003` / `EF.VOX`) : Mémo vocal Opus SILK 16 kHz (46 080 octets / 45 Ko / 50,00 %).
  - `EF-4` (`0x0004` / `EF.HOM`) : Registre sépulture, volontés & hommages CBOR (15 360 octets / 15 Ko / 16,67 %).
  - `EF-5` (`0x0005` / `EF.SIG`) : Enveloppe cryptographique COSE_Sign1 RFC 9052 (2 048 octets / 2 Ko / 2,22 %).
- **Contrôle du budget mémoire et réserve matérielle** :
  - Cumul des fichiers de données `EF-0` à `EF-5` : **86 528 octets** (93,89 %).
  - Réserve matérielle EEPROM inviolable : **5 632 octets** (6,11 % > seuil normatif de 5 % pour l'usure matérielle et wear-leveling).
- **Dialogue APDU ISO/IEC 7816-4 & Intégrité Silicium** :
  - Vérifier la séquence ordonnée `SELECT AID`, `READ BINARY`, `UPDATE BINARY`.
  - Vérifier le protocole atomique `COMMIT_FLAG` anti-arrachage RF et le scellement définitif par fusible matériel `LOCK_FUSE` (`80 DE 01 00`).

### D. Grille d'Audit des 4 Applications Souveraines (`DEC-AET-08`)
Vérifier l'étanchéité, les interfaces et la conformité des livrables selon les 4 applications souveraines :
1. **Application 1 : PaxStudio Design B2C/B2B** (Bushi 09, 15) :
   - Conception du double support physique : Carte Sanctuaire mémorielle vs Carte Directives civiles/médicales.
   - Studio photo : compression WebP dans la limite stricte de 20 Ko alloués par `STORAGE-001`.
   - Audio : ducking sonore (-14 dB) et enregistrement Opus SILK dans la limite de 45 Ko.
   - Sortie : capsule de pré-encodage scellée CBOR.
2. **Application 2 : PaxStation Encodage B2B** (Bushi 03, 05, 10) :
   - Environnement d'atelier pour lecteur ACR1552U (WebUSB / PC/SC).
   - Formatage silicium et partitionnement des 6 Elementary Files selon `STORAGE-001`.
   - Scellement irrémédiable du fusible physique (`LOCK_FUSE`) rendant la carte perpétuellement non modifiable.
3. **Application 3 : Sanctuaire Mémoriel B2C** (Bushi 04, 06, 07, 08, 14) :
   - Recueillement hors-ligne pour les familles, zéro-téléchargement et zéro-compte (`DEC-AET-09`).
   - Déclenchement universel : App Clip SwiftUI sur iOS, Web NFC / PWA Chrome sur Android.
   - Lecture directe de la puce ACOSJ 92 Ko en trames IsoDep / CoreNFC.
   - Application stricte de `DEC-AET-07` Option B : affichage solennel avec bandeau de réserve ambré bienveillant si la clé publique n'est pas répertoriée dans la TrustList locale.
4. **Application 4 : Filière Sarcomusation & Traçabilité** (Bushi 11, 12, 13) :
   - Traçabilité des 4 profils de dépouilles (Compagnie, Faune Sauvage DNF, Ferme, Abattoir/MRS).
   - The Iron Gate : blocage absolu de la signature de conformité de lot en cas de tentative de recyclage intra-espèce (feed ban strict).
   - Contrôle du barème Méthode 1 (133°C, 3 bars, 20 min) et dépistage LFA Pentobarbital pour dérogation mémorielle forestière (`DEC-AET-05`).

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
