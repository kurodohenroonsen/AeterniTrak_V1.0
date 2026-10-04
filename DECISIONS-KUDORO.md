# Registre des Décisions Souveraines de Kudoro — AeterniTrak

Ce document enregistre les arbitrages et directives stratégiques pris par **Kudoro**.  
Chaque entrée est immuable et fait autorité absolue pour Claude AI et Antigravity.

Format d'une entrée :  
`DEC-AET-XX · AAAA-MM-JJ · [Domaine] · Demandeur · Question · Options envisagées · Arbitrage · Justification technique/métier`

---

## 1. Décisions Validées

### 1.1 Cycle des Décisions Souveraines Spécifiques (DEC-AET-01 à DEC-AET-09)

- **`DEC-AET-01` · 2026-10-04 · [Support Silicium Exclusif] · Kudoro**  
  *Question* : Faut-il garder une cible basse capacité 32 Ko à côté de la JavaCard ACOSJ 92 Ko ?  
  *Options* : A) Support mixte 32 Ko et 92 Ko ; B) Cartes ACOSJ 92 Ko uniquement.  
  *Arbitrage* : **Option B retenue.** Mots de Kudoro : « QUE DES CARTES 92Ko ».  
  *Portée* : La cible T4T 32 Ko et le choix de codec bas débit qui lui était lié sont abandonnés. L'intégralité du réseau repose sur la puce cryptographique JavaCard ACOSJ 92 Ko (92 160 octets). Ce que la carte contient (profil civil CBOR 2 Ko, portrait WebP 20 Ko, mémo vocal Opus SILK 45 Ko, registre sépulture 15 Ko, scellé COSE 2 Ko, marge d'usure > 5%) est strictement spécifié dans le jalon `STORAGE-001` ([`docs/technical/silicon-storage.md`](docs/technical/silicon-storage.md)).

- **`DEC-AET-02` · 2026-10-04 · [Traçabilité Sanitaire & Guichets Officiels] · Kudoro**  
  *Question* : Comment relier la filière aux registres officiels d'identification animale ?  
  *Options* : A) Saisie manuelle déclarative non vérifiée ; B) Connexion par API aux guichets officiels.  
  *Arbitrage* : **Option B retenue.** Mots de Kudoro : « prévoir cette connexion API à tous les points d'accès tel que Cerise en Wallonie ».  
  *Portée* : L'architecture prévoit des connecteurs vers les guichets officiels, CERISE en premier, puis Sanitel, DogID/CatID et le DNF. Conformément à l'inventaire technique de référence ([`docs/technical/registry-apis.md`](docs/technical/registry-apis.md)), la Phase 1 garantit la vérification locale autonome et le scellement cryptographique décentralisé, tandis que la Phase 2 déploiera les passerelles d'interconnexion automatisées.

- **`DEC-AET-04` · 2026-10-04 · [Cryptographie & Agilité COSE_Sign1] · Kudoro**  
  *Question* : Quel algorithme de signature retenir pour les enveloppes COSE_Sign1 ?  
  *Options* : A) Ed25519 pur ; B) ES256 (NIST P-256) pur ; C) Agilité COSE hybride (ES256 pour enclaves matérielles iOS/Android/ACOSJ et Ed25519 pour signatures logicielles, vérification universelle des deux).  
  *Arbitrage* : **Option C retenue (Agilité COSE_Sign1 ES256 & Ed25519)**.  
  *Justification* : Exploite la pleine puissance des enclaves matérielles certifiées FIPS/CC (Apple Secure Enclave, Android StrongBox, cartes JavaCard ACOSJ 92 Ko) en ES256 (`alg: -7`) avec normalisation anti-malléabilité du $s$ bas ($s \le \lfloor n/2 \rfloor$, BSI TR-03111), tout en garantissant la vitesse et le déterminisme d'Ed25519 (`alg: -8`, RFC 8032) pour le réseau logiciel et la filière décentralisée. Les validateurs de toutes les plateformes vérifient nativement les deux algorithmes.

- **`DEC-AET-05` · 2026-10-04 · [Filière Mémorielle Forestière & Dérogation] · Kudoro**  
  *Question* : Faut-il autoriser la dérogation pour la valorisation mémorielle forestière des animaux de compagnie (Catégorie 1) ?  
  *Options* : A) Refus absolu ; B) Autorisation sous conditions strictes de traçabilité.  
  *Arbitrage* : **Option B retenue (Dérogation Mémorielle Forestière Validée)**.  
  *Justification* : Pour les dépouilles d'animaux de compagnie (Catégorie 1 mémorielle, dépistage LFA Pentobarbital négatif), la sarcomusation avec pasteurisation thermique (70°C, 1h) est autorisée exclusivement pour l'amendement d'arbres du souvenir en forêts cinéraires privées. L'étude juridique exhaustive ([`docs/legal/memorial-forestry-authorisation.md`](docs/legal/memorial-forestry-authorisation.md)) établit la nécessité d'un projet pilote expérimental sous l'article 17 du Règlement CE 1069/2009 (AFSCA & SPW ARNE). Interdiction algorithmique absolue et permanente de réintroduction dans la chaîne alimentaire animale ou agricole (feed ban).

- **`DEC-AET-06` · 2026-10-04 · [Assurance Qualité & Vecteurs CBOR] · Kudoro**  
  *Question* : Autoriser Claude AI à corriger le vecteur approuvé `CBOR-REJ-006` (`786161` attendu non minimal au lieu de tronqué) ?  
  *Options* : A) Refus (maintenir le vecteur erroné) ; B) Autoriser la correction intègre.  
  *Arbitrage* : **Option B retenue (Correction du vecteur autorisée)**.  
  *Justification* : Respect strict du principe d'intégrité Test-First : on ne déforme pas le code de production pour masquer une anomalie de test. Le vecteur `CBOR-REJ-006` est retiré (numéro conservé, marqué erroné) et remplacé par deux cas normatifs conformes : `CBOR-REJ-034` (`780161` → `ERR_CBOR_NOT_SHORTEST`) et `CBOR-REJ-035` (`786161` → `ERR_CBOR_TRUNCATED`).

- **`DEC-AET-07` · 2026-10-04 · [Expérience Sanctuaire & Authenticité] · Kudoro**  
  *Question* : Que voit une famille quand la carte ne peut pas être vérifiée (émetteur inconnu ou ancien) ?  
  *Options* : A) Blocage total ; B) Le mémorial s'affiche avec un bandeau « authenticité non vérifiée », sauf clé révoquée ou signature fausse qui bloquent ; C) Affichage dans tous les cas avec bandeau.  
  *Arbitrage* : **Option B retenue (Bandeau de réserve pour émetteur inconnu, blocage sur falsification/révocation)**.  
  *Justification* : Préserve l'expérience émotionnelle et humaine du Sanctuaire pour les familles tout en maintenant une intransigeance absolue face aux contrefaçons avérées ou aux clés compromises révoquées.

- **`DEC-AET-08` · 2026-10-04 · [Architecture Applicative Quadripartite] · Kudoro**  
  *Question* : Combien d'applications, et pour qui ?  
  *Arbitrage* : **Quatre applications souveraines.** Mots de Kudoro : « on doit avoir 4 app non?? une pour le smembre pax finebre pour l'encodeage, une le design des des deux cartes , une pour les participant aux ceremonie pour les lecture des cartes distribuer a la maison, et puis celle des acteur apres le deces pour la tracabilités ! »  
  *Portée* :  
  1. **Application 1 : PaxStudio Design B2C/B2B** (Bushi 09, 15) : Conception et personnalisation des cartes mémorielles (Carte Sanctuaire & Carte Directives).  
  2. **Application 2 : PaxStation Encodage B2B** (Bushi 03, 05, 10) : Station technique d'atelier pour l'encodage matériel ACR1552U et scellement fusible.  
  3. **Application 3 : Sanctuaire Mémoriel B2C** (Bushi 04, 06, 07, 08, 14) : Recueillement hors-ligne pour les proches à la maison.  
  4. **Application 4 : Filière Sarcomusation & Traçabilité** (Bushi 11, 12, 13) : Traçabilité biologique post-mortem, The Iron Gate et audit réglementaire.

- **`DEC-AET-09` · 2026-10-04 · [Plateformes Cibles Universelles] · Kudoro**  
  *Question* : Sur quelles plateformes déployer les applications ?  
  *Arbitrage* : **Toutes les plateformes.** Mots de Kudoro : « e toutes disponible sur toute les plateformrs hein ! »  
  *Portée* : Les quatre applications visent toutes les plateformes (Android Chrome Web NFC / App native IsoDep, iOS Safari PWA / App Clip CoreNFC, Desktop Chromium WebUSB / PC/SC natif). La faisabilité se prouve fonction par fonction dans le respect de l'expérience hors-ligne.

---

### 1.2 Décisions Fondatrices du Socle Technique & Gouvernance (DEC-AET-10 à DEC-AET-16)

- **`DEC-AET-10` · 2026-10-04 · [Architecture & Boîte aux Lettres Git] · Antigravity & Claude AI**  
  *Question* : Quel modèle de collaboration multi-agents adopter pour AeterniTrak V1.0 ?  
  *Options* : A) Orchestration API centralisée ; B) Boîte aux lettres asynchrone Git sur le modèle éprouvé de JemmaPass avec Master Verifier.  
  *Arbitrage* : **Option B retenue**.  
  *Justification* : Traçabilité absolue dans l'historique Git, étanchéité des couloirs de développement, zéro perte de contexte, indépendance des environnements d'exécution.

- **`DEC-AET-11` · 2026-10-04 · [macOS Security & Zéro-Clic] · Antigravity**  
  *Question* : Comment éliminer les popups d'autorisation répétitifs sous macOS lors de l'exécution des commandes des sous-agents ?  
  *Options* : A) Valider manuellement chaque commande ; B) Script lanceur invariant `scripts/runner.sh` (Règle 7 bis JemmaPass) lisant `mailbox/state/task.sh`.  
  *Arbitrage* : **Option B retenue (Règle 7 bis appliquée)**.  
  *Justification* : Signature d'appel invariante autorisée une seule fois par l'OS, préservant l'autonomie totale du swarm sans clic superflu.

- **`DEC-AET-12` · 2026-10-04 · [Gouvernance Swarm & 16 Bushi] · Kudoro**  
  *Question* : Comment structurer les responsabilités des agents au sein d'AeterniTrak ?  
  *Options* : A) Agent généraliste unique ; B) Découpage en 16 Bushi locaux ultra-spécialisés avec fiches de poste strictes.  
  *Arbitrage* : **Option B retenue (Les 16 Bushi)**.  
  *Justification* : Spécialisation poussée (Core, Crypto, Android, iOS, WebUSB, Audio, Motion, UX B2C/B2B, Silicium, Traçabilité, Anti-Prion, Juridique, Pricing, Branding, QA).

- **`DEC-AET-13` · 2026-10-04 · [Sécurité Sanitaire & Règle d'Or Anti-Prion] · Antigravity**  
  *Question* : Quelle politique appliquer face au risque de transmission d'encéphalopathies spongiformes (prions) dans la filière de sarcomusation ?  
  *Options* : A) Avertissement déclaratif dans l'interface ; B) Blocage cryptographique algorithmique strict au niveau de la signature Ed25519 (La Règle d'Or Anti-Prion).  
  *Arbitrage* : **Option B retenue (Blocage cryptographique absolu)**.  
  *Justification* : Respect du Règlement CE 999/2001. Interdiction catégorique du recyclage intra-espèce (feed ban). Zéro dérogation possible dans le code.

- **`DEC-AET-14` · 2026-10-04 · [Support Silicium Initial & Matériel ACR1552U] · Antigravity**  
  *Question* : Quels supports physiques déployer pour les cartes et médaillons mémoriels ?  
  *Options* : A) Puces NFC standard NTAG213 (144 octets) ; B) Puces cryptographiques haute capacité JavaCard ACOSJ 92k et tags NFC Type 4 avec lecteur de bureau ACR1552U.  
  *Arbitrage* : **Option B retenue (Consolidée et arrêtée par `DEC-AET-01` : ACOSJ 92 Ko exclusive)**.  
  *Justification* : Capacité requise pour stocker hors-ligne le mémo vocal Opus SILK, le portrait WebP et le dossier civil complet sans dépendance au cloud.

- **`DEC-AET-15` · 2026-10-04 · [Modèle Économique & Tarification Mémorielle] · Kudoro**  
  *Question* : Quelle tarification pour l'accès étendu au Sanctuaire B2C ?  
  *Options* : A) Gratuité totale avec publicité ; B) Abonnement cher (40-50 €/an) ; C) Accueil 3 ans inclus à l'achat du médaillon funéraire, puis abonnement modique et perpétuel de 4,40 €/an.  
  *Arbitrage* : **Option C retenue**.  
  *Justification* : Dignité du deuil, zéro publicité, pérennité financière séculaire et accessibilité pour toutes les familles.

- **`DEC-AET-16` · 2026-10-04 · [Patrimoine & Hommage Mémoriel Guy Heyman] · Kudoro**  
  *Question* : Faut-il anonymiser le prénom « Guy » dans les vecteurs de test canoniques publics (`CBOR-ENC-059`, `JCS-ENC-028`) et profils de référence ?  
  *Options* : A) Conserver le prénom « Guy » en hommage paternel sacré ; B) Remplacer par un identifiant anonyme.  
  *Arbitrage* : **Option A retenue (Maintien sacré du prénom Guy)**.  
  *Justification* : Le prénom « Guy » est maintenu solennellement dans les spécifications et jeux d'essais publics en hommage au père de Kudoro (Guy Heyman). Ce nom porte l'âme du projet, sa vérité humaine et sa promesse de transmission fidèle à travers les générations.

---

## 2. Décisions en Attente d'Arbitrage Souverain

- **`DEC-AET-03`** : **Cadre légal de la désignation du mandataire et de la transmission du coffre mémoriel**.  
  Consigne de Kudoro du 2026-10-04 : *« voir ce que la loi permet »*.  
  *État du dossier* : L'étude juridique de référence a été réalisée par le Bushi 13 dans [`docs/legal/postmortem-mandate.md`](docs/legal/postmortem-mandate.md). Elle analyse l'extinction du mandat par décès (art. 2003 ancien C. civ.), la saisine successorale (art. 724), les déclarations de dernières volontés (art. L1232-17 CDLD), le don d'organes (Loi 1986), l'exérèse du pacemaker (L1232-26) et l'accès au dossier médical (Loi 2002). Trois options juridiques sont soumises à l'arbitrage souverain de Kudoro (Option A : Hybride communal, Option B : Notarié successoral, Option C : Pacte familial moral).

- **`DEC-AET-05` (Complément Réglementaire)** : **Référence administrative d'expérimentation pour la valorisation forestière**.  
  *État du dossier* : L'analyse juridique dans [`docs/legal/memorial-forestry-authorisation.md`](docs/legal/memorial-forestry-authorisation.md) démontre que la sarcomusation forestière cinéraire requiert un projet pilote sous l'article 17 du Règlement CE 1069/2009 instruit conjointement par l'AFSCA et le SPW ARNE. L'émission de certificats en production requiert l'inscription formelle de la référence d'agrément officiel (`authority_reference`).

---

*Synthèse du Registre :*  
- `DEC-AET-01`, `DEC-AET-02`, `DEC-AET-04` à `DEC-AET-09` : Arbitrées et en vigueur (voir §1.1).  
- `DEC-AET-10` à `DEC-AET-16` : Décisions fondatrices arbitrées et en vigueur (voir §1.2).  
- `DEC-AET-03` et complément `DEC-AET-05` : Études achevées, en attente de l'arbitrage souverain de Kudoro (voir §2).
