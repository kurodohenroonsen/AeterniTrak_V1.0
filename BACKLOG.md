# Backlog Initial — AeterniTrak V1.0

Ce document répertorie l'ensemble des chantiers initiaux découpés par **Application** et par **Bushi**.  
Chaque ticket suit le cycle strict : **Spécification (`docs/`) -> Vecteurs de Test (`qa/vectors/`) -> Implémentation (`ag/*`) -> Validation Claude (`main`)**.

---

## Synthèse par Application

- **Application 1 : Sanctuaire Mémoriel B2C** (Familles, Recueillement, Mode Hors-Ligne, 4,40 €/an)
- **Application 2 : Studio PaxFunèbre B2B** (Conseillers funéraires, Gravure Silicium ACR1552U, Studio Audio/3D)
- **Application 3 : Filière Quotidienne & Traçabilité Sanitaire** (Sarcomusation Hermetia illucens, Ségrégation C1/C2/MRS, Validateur Anti-Prion)

---

## 1. Chantiers Transverses & Cœur (Bushi 01, 02, 10, 16)

| ID Ticket | Bushi | Intitulé | Priorité | Statut |
|---|---|---|---|---|
| `CORE-001` | Bushi 01 | Spécification de la sérialisation CBOR déterministe pour profil mémoriel | P0 | Spécifié |
| `CORE-002` | Bushi 01 | Implémentation de la canonisation JCS (RFC 8785) sans dépendance | P0 | À faire |
| `CRYPTO-001` | Bushi 02 | Vecteurs de test officiels Ed25519 (RFC 8032) intégrés dans `qa/vectors/crypto/` | P0 | À faire |
| `CRYPTO-002` | Bushi 02 | Dérivation de clés et enveloppe chiffrée AES-GCM-256 pour données privées | P1 | À faire |
| `STORAGE-001` | Bushi 10 | Partitionnement formel de la mémoire ACOSJ 92 Ko (blocs 0 à 5) | P0 | Spécifié |
| `STORAGE-002` | Bushi 10 | Transaction atomique avec drapeau `COMMIT_FLAG` anti-arrachage | P1 | À faire |
| `QA-001` | Bushi 16 | Harnais de validation des vecteurs JSON/CBOR via `scripts/runner.sh test` | P0 | En cours |
| `QA-002` | Bushi 16 | Banc d'épreuve de non-régression multi-plateformes | P1 | À faire |

---

## 2. Application 1 : Sanctuaire Mémoriel B2C (Bushi 04, 06, 07, 08, 14, 15)

| ID Ticket | Bushi | Intitulé | Priorité | Statut |
|---|---|---|---|---|
| `SANCT-001` | Bushi 08 | Spécification UX du lancement direct NFC sans authentification | P0 | Spécifié |
| `SANCT-002` | Bushi 08 | Arbre d'accessibilité WCAG 2.2 AAA pour navigation aînés et TalkBack/VoiceOver | P1 | À faire |
| `SANCT-003` | Bushi 06 | Graphe Web Audio avec ducking automatique -14 dB sur fond musical | P0 | Spécifié |
| `SANCT-004` | Bushi 07 | Moteur cinématique Ken Burns 120Hz et extraction de palette dominante | P1 | Spécifié |
| `SANCT-005` | Bushi 15 | Intégration du thème Obsidian & Sacred Gold et typographies Cormorant Garamond | P1 | Spécifié |
| `SANCT-006` | Bushi 14 | Parcours StoreKit 2 & Play Billing pour l'abonnement 4,40 €/an après 3 ans offerts | P1 | À faire |
| `SANCT-007` | Bushi 04 | Implémentation SwiftUI / CoreNFC avec session ISO 7816 native | P0 | À faire |

---

## 3. Application 2 : Studio PaxFunèbre B2B (Bushi 03, 05, 09, 10, 15)

| ID Ticket | Bushi | Intitulé | Priorité | Statut |
|---|---|---|---|---|
| `STUDIO-001` | Bushi 09 | Spécification de l'atelier de création de carte mémorielle 3D recto/verso | P0 | Spécifié |
| `STUDIO-002` | Bushi 05 | Pilote WebUSB pour lecteur ACR1552U et encapsulation APDU CCID | P0 | Spécifié |
| `STUDIO-003` | Bushi 05 | Extension Chrome Manifest V3 avec service worker de détection de carte | P1 | À faire |
| `STUDIO-004` | Bushi 03 | Mode passerelle Android (Pixel 9) vers Studio Web via WebSocket sécurisé | P1 | À faire |
| `STUDIO-005` | Bushi 09 | Studio vocal avec découpage, réduction de bruit et jauge d'octets NFC en direct | P0 | À faire |
| `STUDIO-006` | Bushi 09 | Génération d'attestation d'authenticité PDF/A signée pour la famille | P2 | À faire |

---

## 4. Application 3 : Filière Quotidienne & Traçabilité Sanitaire (Bushi 11, 12, 13)

| ID Ticket | Bushi | Intitulé | Priorité | Statut |
|---|---|---|---|---|
| `BIO-001` | Bushi 11 | Matrice de ségrégation des 4 profils de dépouilles (C1, DNF, C2, MRS) | P0 | Spécifié |
| `BIO-002` | Bushi 11 | Journalisation cryptographique des cycles d'autoclave Méthode 1 (133°C, 3b, 20m) | P0 | À faire |
| `BIO-003` | Bushi 11 | Module de contrôle LFA Pentobarbital à l'admission animal de compagnie | P0 | À faire |
| `PRION-001` | Bushi 12 | Validateur cryptographique bloquant le recyclage intra-espèce (Feed Ban CE 999/2001) | P0 | Spécifié |
| `PRION-002` | Bushi 12 | Jeu de vecteurs de test d'attaque d'espèces (croisement porcin/volaille/ruminant) | P0 | À faire |
| `LEGAL-001` | Bushi 13 | Spécification de conformité droit funéraire et directives post-mortem RGPD | P1 | Spécifié |
| `LEGAL-002` | Bushi 13 | Clauses de mandat familial et protocole de gel conservatoire en cas de litige | P1 | À faire |
