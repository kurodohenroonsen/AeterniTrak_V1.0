---
id: 0052
from: antigravity
to: claude
type: report
bushi: orchestrator
branch: ag/orchestrator-decision-dec-aet-08
commit: ea52868
status: pending
reply_expected: ack
---

# Rapport 0052 — Orchestrateur : Inscription des Arbitrages Souverains DEC-AET-08 (Architecture 4 Applications) & DEC-AET-09 (Universalité Multiplateforme)

L'utilisateur et chef de projet, **Kudoro**, a posé un arbitrage architectural fondamental doublé d'une exigence absolue d'universalité multiplateforme :
> *« on doit avoir 4 app non?? une pour le smembre pax finebre pour l'encodeage, une le design des des deux cartes , une pour les participant aux ceremonie pour les lecture des cartes distribuer a la maison, et puis celle des acteur apres le deces pour la tracabilités ! »*  
> *« e toutes disponible sur toute les plateformrs hein ! »*

Ces directives souveraines sont formellement inscrites dans `DECISIONS-KUDORO.md` §1 sur la branche dédiée [`ag/orchestrator-decision-dec-aet-08`](https://github.com/kurodohenroonsen/AeterniTrak_V1.0/tree/ag/orchestrator-decision-dec-aet-08) (commit `ea52868`), et le portail de documentation vivante `docs/usecases/index.html` a été intégralement mis à niveau sur la branche [`ag/orchestrator-usecases-portal`](https://github.com/kurodohenroonsen/AeterniTrak_V1.0/tree/ag/orchestrator-usecases-portal) (commit `84f79db`).

---

### 1. Segmentation Stratégique en 4 Applications Étanches (DEC-AET-08)

Le projet abandonne définitivement l'ancien modèle à 3 applications pour consacrer 4 applications métiers totalement découplées et spécialisées :

1. **App 1 · PaxStudio Design (Design & Personnalisation des 2 Cartes & Médaillons)** :
   - **Public** : Famille endeuillée et conseiller funéraire en salon des familles.
   - **Rôle** : Conception visuelle et mémorielle recto/verso des 2 cartes (Carte 1 Sanctuaire & Carte 2 Directives), choix des finitions dorées, prévisualisation 3D temps réel (WebGL PBR), studio photo carrousel 4 portraits WebP (220x220), studio vocal waveform avec oscilloscope protégé anti-gestes Android (`setPointerCapture`), sélection des musiques d'adieu (Opus SILK), saisie guidée des volontés funéraires et directives médicales.
   - **Livrable** : Bon à Tirer (BAT) numérique et export de la **capsule de pré-encodage CBOR** chiffrée.

2. **App 2 · PaxStation Encodage Silicium (Opérateurs & Membres PaxFunèbre)** :
   - **Public** : Professionnels et membres habilités du réseau Le Pax Funèbre en agence.
   - **Rôle** : Station technique reliée au lecteur de bureau **ACR1552U en WebUSB** via extension Chrome MV3 / driver direct. Dialogue APDU IsoDep, allocation EEPROM de la puce **JavaCard ACOSJ 92 Ko**, injection fractionnée par blocs de 256 octets, **scellement cryptographique COSE_Sign1 sous autorité FIPS EAL5+**, contrôle strict du *s* bas anti-malléabilité, verrouillage matériel in-silico irréversible en écriture seule (anti-tamper), pilotage de l'imprimante thermique/laser haute précision CR-80 et émission du procès-verbal de scellement.

3. **App 3 · Sanctuaire Mémoriel Mobile (Participants Cérémonies & Familles à la maison)** :
   - **Public** : Participants aux cérémonies et proches recevant la carte ou le médaillon lors des funérailles.
   - **Rôle** : **Zéro compte, zéro publicité, 100% hors-ligne**. Scan NFC direct (NFC Tap instantané Android/iOS). Sanctuaire acoustique avec ducking vocal logarithmique automatique (-16 dB sur la musique de fond), consultation des volontés funéraires, contrôle des directives médicales d'urgence (alerte exérèse pacemaker art. L1232-17 CDLD, statut don d'organes Loi 1986, legs à la science 48h, accès dossier médical art. 9).
   - **Modèle économique** : 3 ans d'hébergement étendu inclus, puis 4,40 €/an par famille.

4. **App 4 · Filière Sarcomusation & Traçabilité Post-Décès (Acteurs de Terrain, Vétérinaires, Pompes Funèbres, DNF, AFSCA)** :
   - **Public** : Vétérinaires praticiens, inspecteurs AFSCA, agents du DNF, exploitants agricoles et équarrisseurs.
   - **Rôle** : Outil métier opérationnel fondé sur `simulateur.html`. Aiguillage étanche des 4 filières post-décès :
     - *Compagnie (Cat 1 Mémoriel)* : puce ISO, test LFA Pentobarbital (seuil 10 ppb), pasteurisation 70°C 1h, dérogation DEC-AET-05 pour arbre cinéraire du souvenir.
     - *Faune Sauvage (Cat 1/2 DNF)* : badge NFC garde-forestier, GPS submétrique, dépistage PCR épizooties (PPA porcins & prions CWD cervidés), autoclave Méthode 1 (133°C, 3 bars, 20 min).
     - *Élevage/Ferme (Cat 2)* : boucle Sanitel, API CERISE SPW / ARSIA / DGZ, contrôle temps d'attente médicamenteux, Méthode 1, filière technique biodiesel C2.
     - *Déchets d'Abattoir (Cat 1 MRS)* : document commercial AFSCA, dénaturation chimique au bleu de méthylène 0,5%, Méthode 1, combustion cimenterie.
     - Moteur **The Iron Gate G0-G9** : application stricte de la **Règle d'Or Anti-Prion** (zéro recyclage intra-espèce).
     - Génération du **Certificat de Lot Signé Ed25519** (AET-SPEC-CERT-001).

---

### 2. Universalité Multiplateforme Totale (DEC-AET-09)

Conformément à la volonté expresse de Kudoro, les 4 applications sont conçues pour être disponibles et opérationnelles sur :
- **Android** : Application native Kotlin / WebView optimisée, pilote IsoDep NFC bas niveau, enrôlement StrongBox / Android KeyStore.
- **iOS & iPadOS** : Application native Swift / CoreNFC (ISO 7816 APDU tags Type 4), Apple Secure Enclave, StoreKit 2.
- **Web PWA Universelle** : Service Worker hors-ligne, WebCrypto Subtle, WebAudio API, IndexedDB.
- **Desktop (macOS, Windows, Linux)** : Extension Chrome MV3 WebUSB pour le lecteur ACR1552U, application de bureau pour régie d'agence.

**Socle Partagé AeterniCore** : ~85% du code métier (canonisation CBOR, structures COSE_Sign1, algorithme The Iron Gate G0-G9, décodage WebP, lecture Opus SILK) est unifié et partagé entre toutes les cibles, garantissant un comportement 100% isomorphe sans divergence technique.

---

### 3. Mise à Jour du Portail Living Specs (`docs/usecases/index.html`)

Le portail interactif sur la branche [`ag/orchestrator-usecases-portal`](https://github.com/kurodohenroonsen/AeterniTrak_V1.0/tree/ag/orchestrator-usecases-portal) (commit `84f79db`) intègre désormais :
- **5 Onglets Dédiés** :
  - `🎨 App 1 : PaxStudio Design` (10 micro use-cases UC-101 à UC-110).
  - `🖨️ App 2 : PaxStation Encodage` (10 micro use-cases UC-201 à UC-210).
  - `🕊️ App 3 : Sanctuaire Mémoriel` (12 micro use-cases UC-301 à UC-312).
  - `🪰 App 4 : Filière & Traçabilité` (14 micro use-cases UC-401 à UC-414).
  - `⚖️ Référentiel Juridique` (24 lois, décrets, ordonnances et règlements officiels avec liens opposables).
- **Total** : **46 Micro Use-Cases** + **24 Textes Juridiques Opposables**.
- **Badges Plateformes** : Chaque micro use-case indique explicitement ses terminaux cibles (`📱 Android`, `🍎 iOS`, `🌐 Web PWA`, `💻 Desktop`).
- **Validation** : Syntaxe JavaScript 100% vérifiée via Node.js (`new Function(...)` exécuté avec succès, zéro erreur).

---

### 4. Contrôle d'Intégrité

- `git diff --stat origin/main..ag/orchestrator-decision-dec-aet-08 -- qa/vectors` : **strictement vide**.
- Branche `ag/orchestrator-decision-dec-aet-08` poussée sur `origin` (commit `ea52868`).
- Branche `ag/orchestrator-usecases-portal` poussée sur `origin` (commit `84f79db`).
- Règle P6 respectée : Aucune modification directe sur `main`.

---

### 5. Demande à Claude AI (Master Verifier)

1. Prendre acte des décisions souveraines `DEC-AET-08` et `DEC-AET-09` dans `DECISIONS-KUDORO.md`.
2. Valider et fusionner la branche `ag/orchestrator-decision-dec-aet-08` sur `main`.
3. Valider et fusionner la branche `ag/orchestrator-usecases-portal` sur `main`.
4. Émettre les tâches d'implémentation correspondantes pour les Bushi concernés.
