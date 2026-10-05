# Backlog Référentiel — AeterniTrak V1.0

Ce document répertorie l'ensemble des chantiers découpés par **Application souveraine** (`DEC-AET-08`) et par **Bushi**.  
Chaque ticket suit le cycle strict : **Spécification (`docs/`) -> Vecteurs de Test (`qa/vectors/`) -> Implémentation (`ag/*`) -> Validation Claude (`main`)**.  
*Règle C1 : Un ticket n'est « Spécifié » que lorsque son fichier formel dans `docs/` existe effectivement sur `main`.*  
*État certifié sur `main` (`e6dda35`) : 18 suites normatives, **693 vecteurs (100% PASS, 0 FAIL, 0 RED, 0 INVALID)**, 5 bancs de mutations (**34/34 mutations détectées**, 100% sensibilité).*

---

## Synthèse par Application Souveraine (`DEC-AET-08`)

- **Application 1 : PaxStudio Design** (Conception cartes et médaillons, famille & conseiller, Bushi 09, 15)  
  *Conception graphique, recueil des volontés, BAT numérique et prévisualisation 3D des deux cartes (Carte Sanctuaire & Carte Directives).*  
  *Spécification formelle :* [`docs/functional/app1-paxstudio-design.md`](docs/functional/app1-paxstudio-design.md) (10 micro-UCs : `UC-101` à `UC-110`).
- **Application 2 : PaxStation Encodage** (Atelier gravure silicium ACR1552U, opérateur pro, Bushi 03, 05, 10)  
  *Station technique d'atelier funéraire, dialogue APDU ISO 7816-4 via ACR1552U WebUSB/PC/SC CCID, partitionnement EF ACOSJ 92 Ko (`STORAGE-001`), scellement COSE_Sign1 et fusible matériel in-silico `80 DE 01 00`.*  
  *Spécification formelle :* [`docs/functional/app2-paxstation-encodage.md`](docs/functional/app2-paxstation-encodage.md) (10 micro-UCs : `UC-201` à `UC-210`).
- **Application 3 : Sanctuaire Mémoriel** (Recueillement 100% hors-ligne, zéro login, Bushi 04, 06, 07, 08, 14)  
  *Application de recueillement hors-ligne pour les familles et proches, NFC Tap instantané sans compte, lecteur vocal Opus SILK 16 kHz avec ducking -14 dB, cinématique Ken Burns 120 FPS, consultation sous réserve (bandeau ambré `DEC-AET-07 Option B`), tiroir des volontés civiles et médicales et modèle séculaire 4,40 €/an.*  
  *Spécification formelle :* [`docs/functional/app3-sanctuaire-memoriel.md`](docs/functional/app3-sanctuaire-memoriel.md) (12 micro-UCs : `UC-301` à `UC-312`).
- **Application 4 : Filière Sarcomusation & Traçabilité** (The Iron Gate, Hermetia illucens, C1/C2/MRS, Bushi 11, 12, 13)  
  *Gestion quotidienne de la filière de biodégradation par Hermetia illucens, ségrégation stricte des 4 profils de dépouilles (C1, Faune DNF, C2 Sanitel, MRS), The Iron Gate G0-G9 anti-prion (Règlement CE 999/2001), journalisation des cycles autoclaves/pasteurisation, certification de lot scellée Ed25519 et audits réglementaires AFSCA/DNF hors-ligne.*  
  *Spécification formelle :* [`docs/functional/app4-filiere-sarcomusation.md`](docs/functional/app4-filiere-sarcomusation.md) (14 micro-UCs : `UC-401` à `UC-414`).

---

## 1. Chantiers Transverses & Cœur (Bushi 01, 02, 10, 16)

| ID Ticket | Bushi | Intitulé | Priorité | Statut | Vecteurs & Références |
|---|---|---|---|---|---|
| `CORE-001` | Bushi 01 | Spécification de la sérialisation CBOR déterministe pour profil mémoriel (RFC 8949 §4.2.1) | P0 | Validé | `qa/vectors/core/cbor-deterministic.vectors.json` (152 PASS) |
| `CORE-002` | Bushi 01 | Implémentation de la canonisation JCS (RFC 8785) sans dépendance | P0 | Validé | `qa/vectors/core/jcs-rfc8785.vectors.json` (28 PASS) |
| `CORE-003` | Bushi 16 | Vecteurs du profil mémoriel v1 (validation des champs 1 à 13) | P0 | Validé | `qa/vectors/core/profile-v1.vectors.json` (66 PASS) |
| `CORE-004` | Bushi 01 | Validateur de Profil mémoriel v1 avec contrôle strict de taille (≤ 1 900 octets) | P0 | Validé | `core/profile/validator.ts` |
| `CRYPTO-001` | Bushi 02 | Vecteurs de test officiels Ed25519 (RFC 8032) intégrés dans `qa/vectors/crypto/` | P0 | Validé | `qa/vectors/crypto/ed25519-rfc8032.vectors.json` (16 PASS) |
| `CRYPTO-002` | Bushi 02 | Dérivation de clés PBKDF2 (100k itérations) et coffre chiffré AES-GCM-256 pour cache local | P1 | Validé / Spécifié | `docs/technical/silicon-storage.md` §7 |
| `CRYPTO-003` | Bushi 02 | Moteur COSE_Sign1 v1.2 — Agilité ES256/Ed25519 (`DEC-AET-04`), coseOpen et règle temporelle K2 | P0 | Validé | `qa/vectors/crypto/cose-*.vectors.json` (115 PASS) |
| `CRYPTO-004` | Bushi 02 | Vérificateur ECDSA P-256 (ES256) avec contrôle strict anti-malléabilité du s bas (BSI TR-03111) | P0 | Validé | `qa/vectors/crypto/es256-verify.vectors.json` (18 PASS) |
| `STORAGE-001` | Bushi 10 | Partitionnement formel ACOSJ 92 Ko (EF-0 à EF-5, 92 160 octets, `DEC-AET-01`, réserve > 5%) | P0 | Spécifié / Validé | [`docs/technical/silicon-storage.md`](docs/technical/silicon-storage.md) |
| `STORAGE-002` | Bushi 10 | Transaction atomique avec drapeau `COMMIT_FLAG` anti-arrachage RF et fusible `80 DE 01 00` | P1 | Validé / Spécifié | `docs/technical/silicon-storage.md` §4 |
| `QA-001` | Bushi 16 | Harnais de validation des 18 suites de test via `./scripts/runner.sh test` (693 PASS) | P0 | Validé | `qa/harness/run.mjs` (693 PASS, 0 FAIL) |
| `QA-002` | Bushi 16 | Banc d'épreuve de sensibilité aux mutations normatives (34/34 mutations détectées) | P0 | Validé | `qa/tests/mutations*.mjs` (34/34 PASS) |

---

## 2. Application 1 : PaxStudio Design (Conception cartes et médaillons, famille & conseiller, Bushi 09, 15)

*Micro-Use Cases : `UC-101` à `UC-110` formalisés dans [`docs/functional/app1-paxstudio-design.md`](docs/functional/app1-paxstudio-design.md).*

| ID Ticket | Bushi | Intitulé | Priorité | Statut | Vecteurs & Références |
|---|---|---|---|---|---|
| `STUDIO-001` | Bushi 09 | Atelier de conception graphique et prévisualisation 3D temps réel des deux cartes (`UC-101`, `UC-102`) | P0 | Spécifié | `docs/functional/app1-paxstudio-design.md` |
| `STUDIO-002` | Bushi 09 | Studio de recueil vocal avec compression Opus SILK 16 kHz et jauge d'octets en direct (`UC-104`) | P0 | Spécifié | Budget EF-3 (≤ 45 Ko) |
| `STUDIO-003` | Bushi 09 | Optimisation et recadrage d'image WebP 480×480 px avec extraction de palette dominante (`UC-103`) | P0 | Spécifié | Budget EF-2 (≤ 20 Ko) |
| `STUDIO-004` | Bushi 09 | Recueil des dernières volontés, directives anticipées et désignation du mandataire (`UC-105`) | P0 | Spécifié | `docs/legal/postmortem-mandate.md` |
| `STUDIO-005` | Bushi 15 | Intégration du Design System Obsidienne & Or Sacré (100% hors-ligne, zéro CDN) (`UC-107`) | P1 | Validé | `docs/architecture/index.html` |
| `STUDIO-006` | Bushi 09 | Validation conjointe famille / conseiller et signature du BAT numérique (`UC-109`, `UC-110`) | P0 | Spécifié | Capsule d'échange locale `.aetk` |

---

## 3. Application 2 : PaxStation Encodage (Atelier gravure silicium ACR1552U, opérateur pro, Bushi 03, 05, 10)

*Micro-Use Cases : `UC-201` à `UC-210` formalisés dans [`docs/functional/app2-paxstation-encodage.md`](docs/functional/app2-paxstation-encodage.md).*

| ID Ticket | Bushi | Intitulé | Priorité | Statut | Vecteurs & Références |
|---|---|---|---|---|---|
| `STATION-001` | Bushi 05 | Pilote WebUSB / PC/SC CCID pour lecteur ACR1552U avec neutralisation du buzzer (`UC-201`) | P0 | Spécifié | `docs/technical/silicon-storage.md` §5 |
| `STATION-002` | Bushi 03 | Détection ISO 14443-4, vérification ATS et sélection de l'Applet AeterniTrak Core (`UC-202`) | P0 | Spécifié | AID `A00000084501` |
| `STATION-003` | Bushi 10 | Formatage EEPROM et création des 6 Fichiers Élémentaires EF-0 à EF-5 (`UC-203`) | P0 | Spécifié | `AET-SPEC-STORAGE-001` |
| `STATION-004` | Bushi 05 | Ingestion de la capsule `.aetk` et découpage en trames APDU Extended Length (`UC-204`, `UC-205`) | P0 | Spécifié | 306 blocs de 255 o ou Extended |
| `STATION-005` | Bushi 03 | Scellement cryptographique COSE_Sign1 (Ed25519 / ES256 s-bas) sur la puce (`UC-206`, `UC-207`) | P0 | Spécifié | `core/cose/` |
| `STATION-006` | Bushi 10 | Verrouillage irréversible par fusible matériel in-silico `80 DE 01 00` (`UC-208`) | P0 | Spécifié | Protection anti-tamper |
| `STATION-007` | Bushi 05 | Impression physique ID-1 600 DPI et procès-verbal officiel de remise scellé (`UC-209`, `UC-210`) | P1 | Spécifié | Norme ISO/IEC 7810 |

---

## 4. Application 3 : Sanctuaire Mémoriel (Recueillement 100% hors-ligne, zéro login, Bushi 04, 06, 07, 08, 14)

*Micro-Use Cases : `UC-301` à `UC-312` formalisés dans [`docs/functional/app3-sanctuaire-memoriel.md`](docs/functional/app3-sanctuaire-memoriel.md).*

| ID Ticket | Bushi | Intitulé | Priorité | Statut | Vecteurs & Références |
|---|---|---|---|---|---|
| `SANCT-001` | Bushi 08 | Lancement instantané par NFC Tap sans authentification ni compte (`UC-301`) | P0 | Spécifié | Zéro-login, 100% hors-ligne |
| `SANCT-002` | Bushi 04 | Implémentation native iOS CoreNFC / App Clip et Android IsoDep (`UC-302`) | P0 | Spécifié | `docs/technical/ios-nfc-web-comparative.md` |
| `SANCT-003` | Bushi 08 | Gestion de l'authenticité sous réserve avec bandeau ambré (`DEC-AET-07 Option B`, `UC-303`) | P0 | Validé | `core/cose/open.ts` |
| `SANCT-004` | Bushi 06 | Moteur Web Audio avec ducking automatique -14 dB sur fond musical sacré (`UC-304`) | P0 | Spécifié | `bushi/bushi-06-acoustic-webaudio.md` |
| `SANCT-005` | Bushi 07 | Cinématique Ken Burns 120 FPS via lissage quintique d'Hermite (`UC-305`) | P1 | Spécifié | `bushi/bushi-07-cinematic-motion.md` |
| `SANCT-006` | Bushi 08 | Tiroir des volontés civiles et médicales (pacemaker L1232-26, don d'organes) (`UC-308`) | P0 | Spécifié | `docs/legal/postmortem-mandate.md` |
| `SANCT-007` | Bushi 14 | Parcours StoreKit 2 & Play Billing pour l'accueil mémoriel à 4,40 €/an après 3 ans offerts (`UC-311`) | P1 | Spécifié | `DEC-AET-15` |
| `SANCT-008` | Bushi 08 | Ergonomie aînés et accessibilité universelle WCAG 2.2 AAA (`UC-312`) | P1 | Spécifié | Cibles tactiles 56×56 dp |

---

## 5. Application 4 : Filière Sarcomusation & Traçabilité (The Iron Gate, Hermetia illucens, C1/C2/MRS, Bushi 11, 12, 13)

*Micro-Use Cases : `UC-401` à `UC-414` formalisés dans [`docs/functional/app4-filiere-sarcomusation.md`](docs/functional/app4-filiere-sarcomusation.md).*

| ID Ticket | Bushi | Intitulé | Priorité | Statut | Vecteurs & Références |
|---|---|---|---|---|---|
| `BIO-001` | Bushi 11 | Constat d'admission et ségrégation stricte des 4 profils de dépouilles (`UC-401` à `UC-404`) | P0 | Spécifié | Règl. CE 1069/2009 & CE 142/2011 |
| `BIO-002` | Bushi 11 | Dépistage LFA Pentobarbital animal de compagnie (< 10 ppb) et aiguillage mémoriel forestier (`UC-402`) | P0 | Spécifié | `DEC-AET-05` |
| `BIO-003` | Bushi 11 | Collecte faune sauvage DNF avec géolocalisation GPS et tests PCR épizooties (`UC-403`) | P0 | Spécifié | PPA sangliers, CWD cervidés |
| `BIO-004` | Bushi 11 | Contrôle sanitaire bétail d'élevage Sanitel et identification auriculaire (`UC-404`) | P0 | Spécifié | Traçabilité Cerise (`DEC-AET-02`) |
| `BIO-005` | Bushi 11 | Journalisation cryptographique des autoclaves Méthode 1 (133°C, 3b, 20m) et pasteurisation (`UC-408`) | P0 | Spécifié | Hash machine scellé |
| `PRION-001` | Bushi 12 | The Iron Gate : Validateur Anti-Prion G0-G9 bloquant le recyclage intra-espèce (Règle d'or) | P0 | Validé | `validators/antiprion/` (212 PASS) |
| `PRION-002` | Bushi 12 | Émission et vérification du certificat de lot sanitaire scellé Ed25519 (`UC-411`) | P0 | Validé | `core/cert/` (70 PASS) |
| `LEGAL-001` | Bushi 13 | Audit réglementaire inopiné AFSCA / DNF en mode 100% déconnecté (`UC-412`) | P0 | Spécifié | Export scellé infalsifiable |
| `LEGAL-002` | Bushi 13 | Encadrement juridique de la dérogation mémorielle forestière (art. 17 CE 1069/2009) | P0 | Validé / Spécifié | [`docs/legal/memorial-forestry-authorisation.md`](docs/legal/memorial-forestry-authorisation.md) |
| `LEGAL-003` | Bushi 13 | Étude du mandat post-mortem et dévolution des volontés en droit civil belge | P0 | Validé / Spécifié | [`docs/legal/postmortem-mandate.md`](docs/legal/postmortem-mandate.md) |
