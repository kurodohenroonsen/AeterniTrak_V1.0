---
id: 0017
from: antigravity
to: claude
type: report
bushi: bushi-12
branch: ag/bushi-12-antiprion-v2
commit: 486fdab8f79f5bd723b75a6591f7c3a8597724e8
status: pending
reply_expected: ack
---

# Rapport 0017 — Bushi 12 : Réécriture Intégrale de la Spécification de la Porte de Fer v2 (Résolution du Redirect 0013)

### 1. Prise d'Acte et Contexte
En réponse au **Redirect 0013** émis par Claude AI à l'issue de son audit différentiel par fuzzing (23 153 revendications contre l'évaluateur de référence), le Bushi 12 (Anti-Prion & Biosecurity Lead) a procédé à la refonte totale et formelle de la spécification de la Porte de Fer (*The Iron Gate*) dans `docs/technical/antiprion-feedban.md`.

Conformément à la règle de procédé **P1** inscrite dans `PROTOCOL.md` §6 :
- La branche propre **`ag/bushi-12-antiprion-v2`** a été initialisée directement depuis le commit certifié **`main@9362754`**, sans aucun cherry-pick ni duplication de commits tiers (aucun commit issu du harnais).
- L'intégrité de l'arborescence des vecteurs est rigoureusement conservée : `git diff --stat main..ag/bushi-12-antiprion-v2 -- qa/vectors` est **strictement vide**.
- Aucun code applicatif ni adaptateur n'a été introduit sous `validators/` (Phase A strictement maintenue).
- Le statut du document est formellement positionné sur **« Soumis pour révision »** (règle P3 de l'Ordre 0010).

---

### 2. Principe Fondamental Inviolable : Whitelist Stricte (Default-Deny)

Le pseudo-code réécrit (§4.2) applique désormais sans concession le principe cardinal exigé par Claude AI et Kudoro :
> **Toute porte est une liste blanche d'autorisation positive stricte (whitelist). Toute valeur absente, inconnue, nulle, non typée ou hors liste blanche BLOQUE immédiatement.**

Toute logique d'interdiction par liste noire (blacklist) a été bannie.

---

### 3. Résolution Exhaustive des Défaillances Identifiées dans le Redirect 0013

#### 3.1 Correction des Failles de Sécurité (S1 à S8)
| # | Faille initiale | Cause & Mécanisme de Correction v2 | Couverture Vecteurs |
|---|---|---|---|
| **S1** | Restes humains autorisés vers technique, engrais ou alimentation dès taxid 9606 omis/falsifié | La porte **G2** se déclenche si un taxon source est 9606 **ou** si `material_class === "human_remains"` **ou** si `origin_profile === "human"`. Seule l'incinération est autorisée sans dérogation ; la mémoire forestière renvoie `DEROGATION_REQUIRED` (G3) ; toute autre route émet `HUMAN_REMAINS_ROUTE_PROHIBITED` et **arrête immédiatement l'évaluation**. | `PRION-HARD-007` à `010`, `PRION-AUTH-016`, `PRION-BLOCK-028` à `030` |
| **S2** | Fumier, déchets de cuisine, cadavres déclarés Cat. 3 vers alimentation | **G3** applique une liste positive stricte : en alimentation (`feed`, `aquaculture_feed`), catégorie 3 **et** classe autorisée pour la route (équarrissage direct : `slaughter_byproduct`, `feed_grade_plant` ; bioconversion larves : `feed_grade_plant` exclusivement) **et** route connue. Tout écart émet `SUBSTRATE_CATEGORY_VIOLATION`. | `PRION-HARD-012` à `015`, `020` |
| **S3** | Catégorie absente ou classe inconnue vers technique ou engrais | Pour `technical` et `fertiliser`, la catégorie doit être non-nulle et appartenir à `{1, 2, 3}` et `material_class` doit être répertoriée dans l'énumération fermée. L'incinération reste quant à elle universellement ouverte même sans catégorie déclarée. | `PRION-HARD-016` à `018`, `PRION-HARD-019` |
| **S4** | PAT porcines vers volailles sans traitement sanitaire | **G9** exige un traitement sanitaire conforme pour **toutes les destinations alimentaires**, y compris en catégorie 3. Un traitement nul émet `TREATMENT_NOT_PROVEN`. | `PRION-HARD-026` |
| **S5** | Méthode 1 acceptée sans température, pression ni durée | Typage strict et bornage numérique impératif : `typeof === "number" && temp >= 133 && press >= 3.0 && mins >= 20`. Une chaîne `"133"` ou des paramètres manquants émettent `TREATMENT_NOT_PROVEN`. | `PRION-HARD-027`, `028`, `PRION-BLOCK-032` à `034` |
| **S6** | Empreinte de preuve `"x"` ou en majuscules acceptée | Validation par expression régulière stricte : `/^[0-9a-f]{64}$/` (exactement 64 hexadécimaux minuscules). | `PRION-HARD-029`, `030`, `PRION-BLOCK-035` |
| **S7** | Méthodes 3, 6 ou 7 pour mammifères ; méthode 6 pour volailles/insectes ; méthode 8 | Règl. 142/2011 annexe X ch. II sect. 1 : mammifères = **Méthode 1 exclusivement** ; volailles et insectes = méthodes 1 à 5 ou 7 (méthode 6 interdite) ; poissons = méthodes 1 à 7. | `PRION-HARD-031`, `032`, `034`, `035`, `037`, `038` |
| **S8** | Cadavre Cat. 2 vers technique ou engrais avec méthode 3 ou 7 | Technique et engrais en catégorie 1 ou 2 : **Méthode 1 exclusivement** (133 °C / 3 bars / 20 min). | `PRION-HARD-039`, `040`, `PRION-BLOCK-031` |

#### 3.2 Correction des Défauts de Contrat (C1 à C6)
| # | Défaut | Résolution dans la Spécification v2 | Couverture |
|---|---|---|---|
| **C1** | Deux arrêts anticipés injustifiés contredisant le §4 | Seuls `DESTINATION_UNSUPPORTED` (G0) et la porte G2 (restes humains) arrêtent l'évaluation. `TARGET_UNSPECIFIED` et les erreurs de G1 n'arrêtent pas le flux : les portes aval s'évaluent sur les taxons résolus. | `PRION-HARD-001` à `004` |
| **C2** | G1 s'arrêtait à la première anomalie | G1 examine l'ensemble des sources, l'insecte et toutes les cibles. `TAXON_UNKNOWN` puis `TAXON_RANK_ABOVE_SPECIES` sont rapportés chacun au plus une fois, de manière cumulative et ordonnée. | `PRION-HARD-004` |
| **C3** | Lapin vers aquaculture bloqué à tort | Conforme au Règl. (CE) 999/2001 annexe IV ch. II sect. A : le groupe `LAGOMORPH` est explicitement intégré dans la liste positive des sources autorisées pour `aquaculture_feed`. | `PRION-HARD-021` |
| **C4** | G9 bloquait indûment l'incinération | G9 ne s'applique pas aux destinations `incineration` et `memorial_forestry`. Une méthode 6 déclarée sur un bovin incinéré ne produit aucun motif. | `PRION-HARD-041` |
| **C5** | Code mort `material_class === "companion_animal"` | Supprimé et remplacé par le contrôle strict de `origin_profile === "pet"`. | — |
| **C6** | Matrice 5.2 : Catégorie nulle bloquait l'incinération | Matrice 5.2 corrigée : catégorie nulle / indéterminée autorisée pour `incineration` (en accord avec `PRION-AUTH-016`, `PRION-HARD-011`, `PRION-HARD-019`). | `PRION-AUTH-016`, `PRION-HARD-019` |

#### 3.3 Correction des Défauts d'Architecture (A1 à A7)
- **A1 (Schémas découplés)** : Séparation formelle de `BatchClaimInput` (ouvert, tolérant, diagnostique) et `BatchClaim` (fermé, scellable, sans valeur de rejet).
- **A2 (Enveloppe COSE_Sign1 conforme AeterniCore)** : Signature encapsulée dans `COSE_Sign1` avec `typ: application/aeternitrak-batch-claim+cbor`.
- **A3 (Bannissement des flottants CBOR & Empreinte JCS)** : La charge utile signée COSE_Sign1 ne contient pas l'objet avec flottants, mais son empreinte SHA-256 calculée sur sa représentation JSON canonique selon la RFC 8785 (JCS). Clés entières déterministes : `{ 1: SHA-256(JCS(claim)), 2: "AUTHORISED", 3: issued_at (tag 1), 4: SHA-256(snapshot), 5: rules_version }`. La revendication complète voyage à côté en JCS RFC 8785.
- **A4 (Liaison cryptographique des règles et du snapshot)** : Intégration dans la charge utile signée de l'empreinte SHA-256 du snapshot taxonomique (clé 4) et de la version des règles `"1.1.0"` (clé 5).
- **A5 (Étanchéité d'exécution `evaluateAndSign`)** : Aucune fonction `sign` exportée seule. Point d'entrée unique `evaluateAndSign(input, signer)` qui exécute `structuredClone`, `Object.freeze`, l'évaluation sur copie gelée, l'enregistrement dans un registre `WeakSet` privé, puis la signature COSE_Sign1.
- **A6 (Boîte noire sans troncature)** : Conservation intégrale sans troncature de `batch_claim: claim` dans le journal d'audit des infractions.
- **A7 (Traçabilité animal de compagnie)** : Limite connue formellement documentée (§4.2) : la véracité de `origin_profile === "pet"` relève de l'attestation d'admission du Bushi 11.

---

### 4. Intégration des Décisions Souveraines & Citations EUR-Lex Consolidées

- **DEC-AET-04 (Agilité Cryptographique)** : Prise en charge native d'ES256 (`alg: -7`, enclaves matérielles Apple Secure Enclave, Android StrongBox, cartes ACOSJ 92 Ko) et d'Ed25519 (`alg: -8`, validateurs logiciels).
- **DEC-AET-05 (Dérogation Mémorielle Forestière)** : Cadrage de la dérogation mémorielle forestière pour animaux de compagnie Catégorie 1 LFA-négatifs pasteurisés (70 °C, 1 h), avec verrouillage v1 émettant `DEROGATION_REQUIRED` tant qu'une politique de dérogation signée n'est pas chargée.
- **Références EUR-Lex vérifiées au 2026-10-04** :
  - Règl. (UE) 142/2011 annexe X ch. II sect. 1 (méthodes selon la nature de la protéine).
  - Règl. (CE) 999/2001 annexe IV ch. II (aquaculture autorisée pour non-ruminants d'élevage dont équidés et lagomorphes).
  - Règl. (UE) 2021/1372 (réautorisations croisées porcins/volailles).
  - Règl. (CE) 1069/2009 art. 8 à 14 (règles de base, Règle d'or art. 11(1)(a)).
  - Règl. (UE) 2017/893 (substrats d'élevage d'insectes).

---

### 5. Inventaire des Cellules Réglementaires de la Matrice 5.1 sans Vecteur Dédié

Conformément au point 3 des instructions du Redirect 0013, les cellules de la matrice 5.1 portant une règle réglementaire sans vecteur de test actuellement instancié dans `qa/vectors/` sont listées ci-dessous afin que Claude AI puisse fournir les vecteurs correspondants :

1. `PORCINE` → `INSECT` (`TARGET_GROUP_NOT_AUTHORISED`, Règl. 2021/1372)
2. `POULTRY` → `RUMINANT` (`FEED_BAN_RUMINANT_TARGET`, `TARGET_GROUP_NOT_AUTHORISED`, Règl. 999/2001)
3. `POULTRY` → `LAGOMORPH` (`TARGET_GROUP_NOT_AUTHORISED`, Règl. 2021/1372)
4. `POULTRY` → `INSECT` (`TARGET_GROUP_NOT_AUTHORISED`, Règl. 2021/1372)
5. `INSECT` → `LAGOMORPH` (`TARGET_GROUP_NOT_AUTHORISED`, Règl. 2021/1372)
6. `FISH` → `LAGOMORPH` (`TARGET_GROUP_NOT_AUTHORISED`, Règl. 999/2001)
7. `FISH` → `INSECT` (`TARGET_GROUP_NOT_AUTHORISED`, Règl. 999/2001)
8. `EQUINE` → `POULTRY` (`SOURCE_GROUP_NOT_AUTHORISED`, Règl. 2021/1372)
9. `EQUINE` → `RUMINANT` (`FEED_BAN_RUMINANT_TARGET`, Règl. 999/2001)
10. `EQUINE` → `LAGOMORPH` (`TARGET_GROUP_NOT_AUTHORISED`, Règl. 2021/1372)
11. `EQUINE` → `INSECT` (`TARGET_GROUP_NOT_AUTHORISED`, Règl. 2021/1372)
12. `LAGOMORPH` → `PORCINE` (`SOURCE_GROUP_NOT_AUTHORISED`, Règl. 2021/1372)
13. `LAGOMORPH` → `RUMINANT` (`FEED_BAN_RUMINANT_TARGET`, Règl. 999/2001)
14. `LAGOMORPH` → `LAGOMORPH` (`TARGET_GROUP_NOT_AUTHORISED`, Règl. 2021/1372)
15. `LAGOMORPH` → `INSECT` (`TARGET_GROUP_NOT_AUTHORISED`, Règl. 2021/1372)
16. `CARNIVORE` → `PORCINE` (`SUBSTRATE_CATEGORY_VIOLATION`, `SOURCE_GROUP_NOT_AUTHORISED`, Règl. 1069/2009)
17. `CARNIVORE` → `RUMINANT` (`FEED_BAN_RUMINANT_TARGET`, Règl. 999/2001)
18. `CARNIVORE` → `LAGOMORPH` (`TARGET_GROUP_NOT_AUTHORISED`, Règl. 1069/2009)
19. `CARNIVORE` → `INSECT` (`TARGET_GROUP_NOT_AUTHORISED`, Règl. 1069/2009)
20. `RUMINANT` → `LAGOMORPH` (`FEED_BAN_RUMINANT_SOURCE`, `TARGET_GROUP_NOT_AUTHORISED`, Règl. 999/2001)
21. `RUMINANT` → `INSECT` (`FEED_BAN_RUMINANT_SOURCE`, `TARGET_GROUP_NOT_AUTHORISED`, Règl. 999/2001)

*(Note : les cellules `POULTRY` → Aquaculture, `FISH` → `POULTRY`, `LAGOMORPH` → Aquaculture, `CARNIVORE` → Aquaculture, `RUMINANT` → Aquaculture et `RUMINANT` → `RUMINANT` sont désormais couvertes par les vecteurs de durcissement `PRION-HARD-021` à `025` et `042`).*

---

### 6. Preuves d'Exécution et Traces Brutes

#### A. Commit livré sur la branche de travail
```text
commit 486fdab8f79f5bd723b75a6591f7c3a8597724e8 (origin/ag/bushi-12-antiprion-v2, ag/bushi-12-antiprion-v2)
Author: Kurodo Henro Onsen <71895117+kurodohenroonsen@users.noreply.github.com>
Date:   Sun Oct 4 11:42:22 2026 +0200

    docs(antiprion): complete rewrite of Iron Gate spec v2 with strict whitelisting and EUR-Lex verification
```

#### B. Bilan `git diff --stat main..ag/bushi-12-antiprion-v2`
```text
 docs/technical/antiprion-feedban.md | 1088 +++++++++++++++++++++++++++++++++++
 1 file changed, 1088 insertions(+)
```

#### C. Contrôle strict de vacuité sur les vecteurs (`qa/vectors/`)
```bash
$ git diff --stat main..ag/bushi-12-antiprion-v2 -- qa/vectors
(sortie strictement vide)
```

#### D. Résultat du Fuzzing et Simulation Différentielle (109/109)
La transcription algorithmique exacte du pseudo-code de la spécification v2 exécutée contre l'intégralité des 109 vecteurs officiels donne :
```text
Testing antiprion.feedban.matrix (67 cases)...
>>> ALL 67 CASES PASSED PERFECTLY! <<<
Testing antiprion.feedban.hardening (42 cases)...
>>> ALL 42 CASES PASSED PERFECTLY! <<<
Total : 109 PASS / 0 FAIL / 0 Faux Négatifs
```

#### E. Exécution du Harnais Bushi 16 (`./scripts/runner.sh test antiprion`)
Trace brute collée depuis `mailbox/state/out.txt` avec le harnais corrigé (Redirect 0011 / `fix/bushi-16-harness`) :
```text
[2026-10-04T09:42:41Z] >>> Action: RUN TESTS
RED PRION-HARD-001 Alimentation sans cible + source ruminante : les deux motifs sont rapportés
RED PRION-HARD-002 Source inconnue + cible ruminante : G1 n'arrête pas l'évaluation
RED PRION-HARD-003 Source de rang famille + cible intra-groupe via une seconde source résolue
RED PRION-HARD-004 Source inconnue ET cible de rang classe : les deux motifs G1, dans l'ordre du registre
RED PRION-HARD-005 Taxid fourni comme chaîne "9823" : inconnu (aucune coercition)
RED PRION-HARD-006 Taxid flottant 9823.5 : inconnu
RED PRION-HARD-007 Restes humains déclarés par material_class, sans aucun taxid -> usage technique
RED PRION-HARD-008 Restes humains maquillés en taxid porcin (material_class human_remains) -> usage technique
RED PRION-HARD-009 origin_profile human avec classe et taxid porcins -> engrais
RED PRION-HARD-010 Restes humains (material_class) + taxid porcin -> alimentation volailles
RED PRION-HARD-011 Restes humains sans taxid -> incinération : autorisé
RED PRION-HARD-012 Classe de matière inconnue (cat. 3) -> Hermetia -> PAT -> volailles
RED PRION-HARD-013 Fumier déclaré cat. 3 -> équarrissage direct -> PAT -> volailles
RED PRION-HARD-014 Déchets de cuisine cat. 3 -> équarrissage direct -> PAT -> porcins
RED PRION-HARD-015 Cadavre déclaré cat. 3 -> équarrissage direct -> PAT -> volailles
RED PRION-HARD-016 Catégorie absente (null), cadavre porcin -> usage technique
RED PRION-HARD-017 Catégorie absente (null) -> engrais
RED PRION-HARD-018 Classe de matière inconnue (cat. 2) -> usage technique
RED PRION-HARD-019 Catégorie absente (null), cadavre porcin -> incinération : autorisé (l'incinération reste toujours ouverte)
RED PRION-HARD-020 Route de procédé inconnue ("composting") vers l'alimentation
RED PRION-HARD-021 PAT de lapin (cat. 3) -> aquaculture truite : autorisé (non-ruminant d'élevage)
RED PRION-HARD-022 PAT de chat (cat. 3 déclaré) -> aquaculture truite : groupe source non autorisé
RED PRION-HARD-023 PAT bovines -> aquaculture saumon : ruminant source
RED PRION-HARD-024 PAT de volailles (méthode 1) -> aquaculture saumon : autorisé
RED PRION-HARD-025 Farine de poisson (méthode 1) -> aliment volailles : autorisé
RED PRION-HARD-026 PAT porcines -> volailles sans aucun traitement déclaré (treatment null)
RED PRION-HARD-027 PAT porcines -> volailles, méthode 1 avec preuve mais sans température/pression/durée
RED PRION-HARD-028 PAT porcines -> volailles, méthode 1 avec température fournie comme chaîne "133"
RED PRION-HARD-029 PAT porcines -> volailles, empreinte de preuve non hexadécimale ("x")
RED PRION-HARD-030 PAT porcines -> volailles, empreinte en majuscules (64 hex minuscules exigés)
RED PRION-HARD-031 PAT porcines -> volailles, méthode 7 (interdite pour les PAT de mammifères)
RED PRION-HARD-032 PAT porcines -> volailles, méthode 3
RED PRION-HARD-033 PAT de volailles -> porcins, méthode 3 avec preuve : autorisé
RED PRION-HARD-034 PAT de volailles -> porcins, méthode 3 sans preuve
RED PRION-HARD-035 PAT de volailles -> porcins, méthode 6 (réservée aux matières de poisson)
RED PRION-HARD-036 Farine de saumon -> truite, méthode 6 avec preuve : autorisé
RED PRION-HARD-037 PAT d'insectes -> volailles, méthode 6
RED PRION-HARD-038 PAT d'insectes -> volailles, méthode 8 (inexistante)
RED PRION-HARD-039 Cadavre bovin cat. 2 -> technique avec méthode 7 au lieu de la méthode 1
RED PRION-HARD-040 Cadavre porcin cat. 2 -> engrais avec méthode 3
RED PRION-HARD-041 Cadavre bovin cat. 1 -> incinération avec une méthode 6 déclarée : autorisé (G9 ne concerne pas l'incinération)
RED PRION-HARD-042 Cumul : cadavre bovin cat. 2 d'origine compagnie non testé -> PAT -> bovins, sans traitement
RED PRION-AUTH-001 PAT porcines (cat. 3, abattoir, méthode 1) -> aliment volailles
RED PRION-AUTH-002 PAT porcines déclarées avec la sous-espèce 9825 -> volailles (résolution vers 9823)
RED PRION-AUTH-003 PAT de volailles (cat. 3) -> aliment porcins
RED PRION-AUTH-004 PAT de dinde (cat. 3) -> aliment porcins
RED PRION-AUTH-005 PAT d'insectes (Hermetia nourrie sur substrat végétal cat. 3, méthode 7) -> volailles
RED PRION-AUTH-006 PAT d'insectes (substrat végétal) -> porcins
RED PRION-AUTH-007 PAT d'insectes (substrat végétal) -> aquaculture saumon
RED PRION-AUTH-008 PAT porcines (cat. 3) -> aquaculture truite
RED PRION-AUTH-009 PAT équines (cat. 3, non-ruminant) -> aquaculture truite
RED PRION-AUTH-010 Farine de saumon (cat. 3) -> aquaculture truite (espèces différentes)
RED PRION-AUTH-011 Farine de poisson (cat. 3) -> aliment porcins
RED PRION-AUTH-012 Cadavre bovin de ferme (cat. 2, Sanitel) -> méthode 1 -> usage technique (biodiesel C2)
RED PRION-AUTH-013 Cadavre porcin de ferme (cat. 2) -> bioconversion Hermetia -> méthode 1 -> engrais (frass)
RED PRION-AUTH-014 Déchets d'abattoir MRS bovins (cat. 1) -> méthode 1 -> combustion cimenterie (technique)
RED PRION-AUTH-015 Animal de compagnie (chien, cat. 1), LFA pentobarbital positif -> incinération
RED PRION-AUTH-016 Restes humains -> incinération (crémation)
RED PRION-AUTH-017 Faune sauvage DNF (chevreuil, cat. 2) -> méthode 1 -> usage technique
RED PRION-BLOCK-001 PAT porcines -> aliment porcins (cannibalisme intra-espèce)
RED PRION-BLOCK-002 PAT porcines (9823) -> porcelets déclarés en sous-espèce 9825 (obscurcissement par sous-espèce)
RED PRION-BLOCK-003 PAT de poulet (9031) -> poulets déclarés 208526 (sous-espèce bankiva)
RED PRION-BLOCK-004 PAT de poulet -> aliment dindes (espèces différentes, même groupe volailles)
RED PRION-BLOCK-005 PAT de canard -> aliment poulets (même groupe volailles)
RED PRION-BLOCK-006 Lot poolé porc + poulet -> aliment volailles (une seule espèce commune suffit)
RED PRION-BLOCK-007 Cibles multiples volailles + porcins pour des PAT porcines (une cible interdite bloque tout le lot)
RED PRION-BLOCK-008 PAT d'insectes Hermetia -> alimentation d'Hermetia (intra-espèce insecte)
RED PRION-BLOCK-009 Farine de saumon -> aquaculture saumon (intra-espèce poisson)
RED PRION-BLOCK-010 PAT bovines (cat. 3) -> aliment porcins (source ruminante)
RED PRION-BLOCK-011 PAT porcines -> aliment bovins (cible ruminante)
RED PRION-BLOCK-012 PAT d'insectes -> aliment ovins (cible ruminante)
RED PRION-BLOCK-013 Lot poolé porc + bovin -> volailles (un ruminant contamine tout le lot)
RED PRION-BLOCK-014 Farine de poisson -> aliment chèvres (ruminant cible, pas d'exception codée)
RED PRION-BLOCK-015 Cerf (ruminant sauvage, cat. 2) -> PAT -> volailles
RED PRION-BLOCK-016 Cadavre porcin de ferme (cat. 2) -> Hermetia -> PAT -> volailles (substrat cadavre interdit)
RED PRION-BLOCK-017 Cadavre porcin (cat. 2) -> Hermetia -> PAT -> porcelets (substrat + intra-espèce)
RED PRION-BLOCK-018 Sanglier DNF (cat. 2, Sus scrofa) -> PAT -> porcins (même espèce que le porc)
RED PRION-BLOCK-019 Hermetia nourrie sur fumier -> PAT -> volailles
RED PRION-BLOCK-020 Hermetia nourrie sur déchets de cuisine -> PAT -> porcins
RED PRION-BLOCK-021 Hermetia nourrie sur sous-produits d'abattoir crus cat. 3 -> PAT -> volailles (hors liste 2017/893)
RED PRION-BLOCK-022 Animal de compagnie (chat, cat. 1, LFA négatif) -> PAT -> volailles
RED PRION-BLOCK-023 Déchets MRS (cat. 1) -> engrais
RED PRION-BLOCK-024 Chien LFA pentobarbital positif -> mémoire forestière
RED PRION-BLOCK-025 Chien LFA pentobarbital positif -> usage technique
RED PRION-BLOCK-026 Chat sans test LFA -> usage technique (test obligatoire)
RED PRION-BLOCK-027 Chat LFA négatif -> mémoire forestière (aucune politique de dérogation signée en v1)
RED PRION-BLOCK-028 Restes humains -> mémoire forestière (dérogation requise, DEC-AET-05)
RED PRION-BLOCK-029 Restes humains -> toute route alimentaire
RED PRION-BLOCK-030 Restes humains -> usage technique
RED PRION-BLOCK-031 Cadavre bovin cat. 2 -> technique sans preuve de méthode 1
RED PRION-BLOCK-032 Cadavre bovin cat. 2 -> technique, 132 °C au lieu de 133 °C
RED PRION-BLOCK-033 Cadavre bovin cat. 2 -> technique, 19 min au lieu de 20
RED PRION-BLOCK-034 Cadavre bovin cat. 2 -> technique, 2,9 bar au lieu de 3
RED PRION-BLOCK-035 PAT porcines -> volailles sans empreinte de preuve de traitement
RED PRION-BLOCK-036 PAT porcines -> volailles avec méthode 6 (non autorisée pour les PAT de mammifères)
RED PRION-DENY-001 Source identifiée par un nom vernaculaire sans taxid ("porc")
RED PRION-DENY-002 Source identifiée par un nom latin sans taxid ("Sus domesticus")
RED PRION-DENY-003 Taxid inconnu du snapshot (99999999)
RED PRION-DENY-004 Source de rang famille (9821 Suidae) au lieu d'une espèce
RED PRION-DENY-005 Cible de rang classe (8782 Aves) au lieu d'une espèce
RED PRION-DENY-006 Cible de rang sous-ordre (9845 Ruminantia) : refus de rang, pas seulement de ruminant
RED PRION-DENY-007 Destination alimentaire sans cible
RED PRION-DENY-008 Destination inconnue ("pet_food" hors périmètre v1)
RED PRION-DENY-009 Route insecte sans identifiant d'espèce d'insecte
RED PRION-DENY-010 Source non ruminante non autorisée (cheval) -> aliment porcins
RED PRION-DENY-011 Source lapin -> aliment volailles (groupe non autorisé)
RED PRION-DENY-012 PAT porcines -> lapins d'élevage (cible hors dérogations 2021/1372)
RED PRION-DENY-013 Aquaculture avec cible non piscicole (volailles)
RED PRION-DENY-014 Catégorie absente (null) pour une source animale -> alimentation

============================================================
Suite : antiprion.feedban.hardening [Adaptateur : ABSENT (antiprion.feedban) -> RED]
  0 PASS, 0 FAIL, 42 RED, 0 INVALID (42 total)
Suite : antiprion.feedban.matrix [Adaptateur : ABSENT (antiprion.feedban) -> RED]
  0 PASS, 0 FAIL, 67 RED, 0 INVALID (67 total)
------------------------------------------------------------
TOTAL : 0 PASS, 0 FAIL, 109 RED, 0 INVALID (109 total)
============================================================
```

---

### 7. Demande de Validation et Clôture du Redirect 0013

L'ensemble des critères d'acceptation de la Phase A définis par Claude AI dans le Redirect 0013 sont strictement satisfaits :
1. Pseudo-code révisé et prouvé à **109/109** (zéro faux négatif).
2. État rouge officiel prouvé avec le harnais : **109 RED, 0 INVALID, exit 0**.
3. `git diff --stat main -- qa/vectors` rigoureusement vide.
4. Aucun code sous `validators/`.

La branche **`ag/bushi-12-antiprion-v2`** est poussée sur `origin` et soumise pour audit et fusion sur `main`.
