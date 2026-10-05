# Registre des Décisions Souveraines de Kudoro — AeterniTrak

Ce document enregistre les arbitrages et directives stratégiques pris par **Kudoro**.  
Chaque entrée est immuable et fait autorité pour Claude AI et Antigravity.

Format d'une entrée :  
`AAAA-MM-JJ · [Domaine] · Demandeur · Question · Options envisagées · Arbitrage · Justification technique/métier`

---

## 1. Décisions Validées

- **2026-10-04 · [Architecture] · Antigravity & Claude AI**  
  *Question* : Quel modèle de collaboration multi-agents adopter pour AeterniTrak V1.0 ?  
  *Options* : A) Orchestration API centralisée ; B) Boîte aux lettres asynchrone Git sur le modèle éprouvé de JemmaPass avec Master Verifier.  
  *Arbitrage* : **Option B retenue**.  
  *Justification* : Traçabilité absolue dans l'historique Git, étanchéité des couloirs de développement, zéro perte de contexte, indépendance des environnements d'exécution.

- **2026-10-04 · [macOS Security] · Antigravity**  
  *Question* : Comment éliminer les popups d'autorisation répétitifs sous macOS lors de l'exécution des commandes des sous-agents ?  
  *Options* : A) Valider manuellement chaque commande ; B) Script lanceur invariant `scripts/runner.sh` (Règle 7 bis JemmaPass) lisant `mailbox/state/task.sh`.  
  *Arbitrage* : **Option B retenue (Règle 7 bis appliquée)**.  
  *Justification* : Signature d'appel invariante autorisée une seule fois par l'OS, préservant l'autonomie totale du swarm sans clic superflu.

- **2026-10-04 · [Gouvernance Swarm] · Kudoro**  
  *Question* : Comment structurer les responsabilités des agents au sein d'AeterniTrak ?  
  *Options* : A) Agent généraliste unique ; B) Découpage en 16 Bushi locaux ultra-spécialisés avec fiches de poste strictes.  
  *Arbitrage* : **Option B retenue (Les 16 Bushi)**.  
  *Justification* : Spécialisation poussée (Core, Crypto, Android, iOS, WebUSB, Audio, Motion, UX B2C/B2B, Silicium, Traçabilité, Anti-Prion, Juridique, Pricing, Branding, QA).

- **2026-10-04 · [Sécurité Sanitaire] · Antigravity**  
  *Question* : Quelle politique appliquer face au risque de transmission d'encéphalopathies spongiformes (prions) dans la filière de sarcomusation ?  
  *Options* : A) Avertissement déclaratif dans l'interface ; B) Blocage cryptographique algorithmique strict au niveau de la signature Ed25519 (La Règle d'Or Anti-Prion).  
  *Arbitrage* : **Option B retenue (Blocage cryptographique absolu)**.  
  *Justification* : Respect du Règlement CE 999/2001. Interdiction catégorique du recyclage intra-espèce (feed ban). Zéro dérogation possible dans le code.

- **2026-10-04 · [Support Silicium & Matériel] · Antigravity**  
  *Question* : Quels supports physiques déployer pour les cartes et médaillons mémoriels ?  
  *Options* : A) Puces NFC standard NTAG213 (144 octets) ; B) Puces cryptographiques haute capacité JavaCard ACOSJ 92k et tags NFC Type 4 32k/8k avec lecteur de bureau ACR1552U.  
  *Arbitrage* : **Option B retenue**.  
  *Justification* : Capacité requise pour stocker hors-ligne le mémo vocal Opus SILK, le portrait WebP et le dossier civil complet sans dépendance au cloud.

- **2026-10-04 · [Modèle Économique] · Kudoro** *(Remplacée le 2026-10-05 par DEC-AET-11)*  
  *Question* : Quelle tarification pour l'accès étendu au Sanctuaire B2C ?  
  *Options* : A) Gratuité totale avec publicité ; B) Abonnement cher (40-50 €/an) ; C) Accueil 3 ans inclus à l'achat du médaillon funéraire, puis abonnement modique et perpétuel de 4,40 €/an.  
  *Arbitrage* : **Option C retenue** *(Remplacée le 2026-10-05 par DEC-AET-11 : discrétion tarifaire et suppression de tout prix chiffré dans le code et les spécifications)*.  
  *Justification* : Dignité du deuil, zéro publicité, pérennité financière séculaire et accessibilité pour toutes les familles.

- **2026-10-04 · [Cryptographie & Agilité COSE] · Kudoro (DEC-AET-04)**  
  *Question* : Quel algorithme de signature retenir pour les enveloppes COSE_Sign1 ?  
  *Options* : A) Ed25519 pur ; B) ES256 (NIST P-256) pur ; C) Agilité COSE hybride (ES256 pour enclaves matérielles iOS/Android/ACOSJ et Ed25519 pour signatures logicielles, vérification universelle des deux).  
  *Arbitrage* : **Option C retenue (Agilité COSE_Sign1 ES256 & Ed25519)**.  
  *Justification* : Exploite la pleine puissance des enclaves matérielles certifiées FIPS/CC (Apple Secure Enclave, Android StrongBox, cartes JavaCard ACOSJ 92 Ko) en ES256 (`alg: -7`) tout en garantissant la vitesse et le déterminisme d'Ed25519 (`alg: -8`) pour le réseau logiciel et décentralisé. Les décodeurs de toutes les plateformes vérifient nativement les deux algorithmes.

- **2026-10-04 · [Filière Mémorielle & Forêt] · Kudoro (DEC-AET-05)**  
  *Question* : Faut-il autoriser la dérogation pour la valorisation mémorielle forestière des animaux de compagnie (Catégorie 1) ?  
  *Options* : A) Refus absolu ; B) Autorisation sous conditions strictes de traçabilité.  
  *Arbitrage* : **Option B retenue (Dérogation Mémorielle Forestière Validée)**.  
  *Justification* : Pour les dépouilles de compagnie (Catégorie 1 mémorielle, dépistage LFA Pentobarbital négatif), la sarcomusation avec pasteurisation thermique (70°C, 1h) est autorisée exclusivement pour l'amendement d'arbres du souvenir en forêts cinéraires privées. Interdiction algorithmique absolue et permanente de réintroduction dans la chaîne alimentaire animale ou agricole (feed ban).

- **2026-10-04 · [Patrimoine & Hommage Mémoriel] · Kudoro**  
  *Question* : Faut-il anonymiser le prénom « Guy » dans les vecteurs de test canoniques publics (`CBOR-ENC-059`, `JCS-ENC-028`) et profils de référence ?  
  *Options* : A) Conserver le prénom « Guy » en hommage paternel sacré ; B) Remplacer par un identifiant anonyme.  
  *Arbitrage* : **Option A retenue (Maintien du prénom Guy)**.  
  *Justification* : Le prénom « Guy » est maintenu solennellement dans les spécifications et jeux d'essais publics en hommage au père de Kudoro (Guy Heyman). Ce nom porte l'âme du projet, sa vérité humaine et sa promesse de transmission fidèle à travers les générations.

- **2026-10-04 · [Assurance Qualité & Vecteurs CBOR] · Kudoro (DEC-AET-06)**  
  *Question* : Autoriser Claude AI à corriger le vecteur approuvé `CBOR-REJ-006` (`786161` attendu non minimal au lieu de tronqué) ?  
  *Options* : A) Refus (maintenir le vecteur erroné) ; B) Autoriser la correction intègre.  
  *Arbitrage* : **Option B retenue (Correction du vecteur autorisée)**.  
  *Justification* : Respect strict du principe d'intégrité Test-First : on ne déforme pas le code de production pour masquer une anomalie de test. Le vecteur `CBOR-REJ-006` est retiré (numéro conservé, marqué erroné) et remplacé par deux cas normatifs conformes : `CBOR-REJ-034` (`780161` → `ERR_CBOR_NOT_SHORTEST`) et `CBOR-REJ-035` (`786161` → `ERR_CBOR_TRUNCATED`).

- **2026-10-04 · [Expérience Sanctuaire & Authenticité] · Kudoro (DEC-AET-07)**  
  *Question* : Que voit une famille quand la carte ne peut pas être vérifiée (émetteur inconnu ou ancien) ?  
  *Options* : A) Blocage total ; B) Le mémorial s'affiche avec un bandeau « authenticité non vérifiée », sauf clé révoquée ou signature fausse qui bloquent ; C) Affichage dans tous les cas avec bandeau.  
  *Arbitrage* : **Option B retenue (Bandeau de réserve pour émetteur inconnu, blocage sur falsification/révocation)**.  
  *Justification* : Préserve l'expérience émotionnelle et humaine du Sanctuaire pour les familles tout en maintenant une intransigeance absolue face aux contrefaçons avérées ou aux clés compromises révoquées.

- **2026-10-04 · [Support Silicium] · Kudoro (DEC-AET-01)**  
  *Question* : Faut-il garder une cible basse capacité 32 Ko à côté de la JavaCard ACOSJ 92 Ko ?  
  *Options* : A) Support mixte 32 Ko et 92 Ko ; B) Cartes ACOSJ 92 Ko uniquement.  
  *Arbitrage* : **Option B retenue.** Mots de Kudoro : « QUE DES CARTES 92Ko ».  
  *Portée* : la cible T4T 32 Ko et le choix de codec bas débit qui lui était lié sont abandonnés. Ce que la carte contient (durée et débit du mémo vocal, nombre de portraits) n'est pas décidé ici : c'est le plan mémoire du ticket `STORAGE-001`, à prouver par le calcul dans la limite des 92 160 octets (règle inviolable n° 3).

- **2026-10-04 · [Traçabilité Sanitaire] · Kudoro (DEC-AET-02)**  
  *Question* : Comment relier la filière aux registres officiels d'identification animale ?  
  *Options* : A) Saisie manuelle ; B) Connexion par API aux guichets officiels.  
  *Arbitrage* : **Option B retenue.** Mots de Kudoro : « prévoir cette connexion API à tous les points d'accès tel que Cerise en Wallonie ».  
  *Portée* : l'architecture prévoit des connecteurs vers les guichets officiels, CERISE en premier. La liste des autres guichets, l'existence d'une API ouverte à un tiers pour chacun et les conditions d'accès restent à établir, sources à l'appui, avant toute spécification.

- **2026-10-04 · [Architecture Applicative] · Kudoro (DEC-AET-08)**  
  *Question* : Combien d'applications, et pour qui ?  
  *Arbitrage* : **Quatre applications.** Mots de Kudoro : « on doit avoir 4 app non?? une pour le smembre pax finebre pour l'encodeage, une le design des des deux cartes , une pour les participant aux ceremonie pour les lecture des cartes distribuer a la maison, et puis celle des acteur apres le deces pour la tracabilités ! »  
  *Portée* : (1) conception des deux cartes ; (2) encodage par les membres du Pax Funèbre ; (3) lecture des cartes par les participants aux cérémonies, à la maison ; (4) traçabilité par les acteurs après le décès. Les noms des applications, leur contenu fonctionnel, tout prix ou durée d'hébergement et toute qualification matérielle ne sont pas décidés ici.

- **2026-10-04 · [Plateformes] · Kudoro (DEC-AET-09)**  
  *Question* : Sur quelles plateformes ?  
  *Arbitrage* : **Toutes.** Mots de Kudoro : « e toutes disponible sur toute les plateformrs hein ! »  
  *Portée* : les quatre applications visent toutes les plateformes. La faisabilité se prouve fonction par fonction : la lecture NFC depuis une page web n'existe que dans Chrome sur Android, et WebUSB (lecteur de bureau) que dans les navigateurs Chromium ; sur les autres plateformes ces fonctions demandent une application native. Le partage de code annoncé entre plateformes n'est pas mesuré.

- **2026-10-05 · [Cryptographie Silicium & Signature] · Kudoro (DEC-AET-10)**  
  *Question* : Qui signe le profil mémoriel (COSE_Sign1) ?  
  *Arbitrage* : **Option A retenue (Enclave matérielle de la station PaxStation)**. Mots de Kudoro : « L'enclave de la station PaxStation (ES256 StrongBox/Secure Enclave) signe le profil, la carte ACOSJ stocke et verrouille ses EF par fusible logiciel. ».  
  *Portée* : La signature cryptographique COSE_Sign1 du profil mémoriel est réalisée par l'enclave sécurisée de la station de gravure (PaxStation / App 2). La puce JavaCard ACOSJ 92 Ko agit en tant que coffre-fort de stockage immuable scellé par fusible in-silico (`80 DE 01 00`). Toute mention d'une signature on-chip ou de clé privée générée dans la carte est proscrite.

- **2026-10-05 · [Modèle Économique & Tarification] · Kudoro (DEC-AET-11)**  
  *Question* : Maintien ou retrait du tarif « 3 ans inclus + 4,40 €/an » ?  
  *Arbitrage* : **Option B retenue (Discrétion tarifaire absolue)**. Mots de Kudoro : « Discrétion tarifaire totale. Annulation du tarif de 4,40 €/an et renvoi vers la politique PaxFunèbre. ».  
  *Portée* : Remplacement complet de la tarification chiffrée issue de la décision du 2026-10-04. Tout chiffre explicite (ex. 4,40 €/an, 3 ans offerts) est purgé du code source, des fiches de cas d'usage et de la documentation. Les interfaces et documentations renvoient strictement à la politique mémorielle de l'opérateur PaxFunèbre.

- **2026-10-05 · [Médias & Portrait Mémoriel] · Kudoro (DEC-AET-12)**  
  *Question* : Dimension et quota du portrait mémoriel WebP dans la carte ACOSJ 92 Ko (EF-2 ≤ 20 480 octets) ?  
  *Arbitrage* : **Option A retenue (480×480)**. Mots de Kudoro : « Portrait WebP en 480×480 (qualité optimale familiale sous 20 Ko en WebP q≈60). ».  
  *Portée* : Le portrait de face stocké dans EF-2 est encodé au format WebP à une résolution canonique de 480×480 pixels avec un facteur de qualité garantissant un poids strictement inférieur ou égal à 20 480 octets. Les mentions obsolètes à 220×220 sont remplacées.

- **2026-10-05 · [Sécurité Sanitaire & Traçabilité Étendue] · Kudoro (DEC-AET-13)**  
  *Question* : Intégration des contrôles amont (PCR sanglier/cervidé, Sanitel, MRS, badge DNF) et de la règle d'étanchéité profil↔catégorie dans l'évaluation The Iron Gate ?  
  *Arbitrage* : **Option A retenue (Spec-First & Test-First)**. Mots de Kudoro : « Contrôles amont déclaratifs en V1 : spec d'abord, vecteurs validés par Claude, puis code. ».  
  *Portée* : Les contrôles amont restent déclaratifs dans les documentations actuelles tant qu'une spécification formelle (`docs/technical/antiprion-upstream-controls-PROPOSAL.md`) et une suite de vecteurs normatifs n'auront pas été approuvées par Claude AI. Aucun code direct non couvert par vecteurs approuvés n'est introduit dans `evaluator.ts`.

- **2026-10-05 · [Gouvernance Git & Intégrité] · Kudoro (DEC-AET-14)**  
  *Question* : Gel de la branche `main` et intégration du garde-fou automatisé de cohérence ?  
  *Arbitrage* : **Option A retenue (Main gelée & check:consistency obligatoire)**. Mots de Kudoro : « Main gelée + contrôle de cohérence check:consistency obligatoire. ».  
  *Portée* : Aucun commit direct sur `main` n'est autorisé. Toute contribution transite obligatoirement par une branche dédiée soumise au Master Verifier Claude AI via la boîte aux lettres Git (`agent-mailbox`). Le script `npm run check:consistency` (`qa/consistency/check.mjs`) est requis avant toute soumission.

- **2026-10-05 · [Faisabilité de la Sarcomusation & Recherche] · Kudoro (DEC-AET-15)**  
  *Question* : Statut de la sarcomusation pour les dépouilles humaines et la filière globale face au cadre juridique actuel ?  
  *Arbitrage* : **Maintien intégral en tant que démonstrateur de faisabilité**. Mots de Kudoro : « la sarco doit etre dedans! meme si la lois ne l'autorise pas !!! on fait justement ceci pour demontrer sa faisabilité ! ».  
  *Portée* : La sarcomusation (bioconversion par larves d'Hermetia illucens) est maintenue au sein de toutes les spécifications d'AeterniTrak (animaux et humains) sous l'étiquette expresse : « Démonstrateur de faisabilité — Option prospective non autorisée par le droit positif actuel (référence à confirmer par un juriste) ». Interdiction absolue d'alimentation animale de quelque nature que ce soit pour les matières issues de restes humains.

- **2026-10-05 · [Budget Silicium] · Kudoro (DEC-AET-16)**  
  *Question* : Quel budget utile pour les six fichiers EF de la carte ACOSJ 92 Ko ?  
  *Arbitrage* : Mots de Kudoro : « J'arbitre formellement le budget utile à 86 528 octets, correspondant à la somme exacte des 6 fichiers EF ».  
  *Portée* : EF-0 (métadonnées et compteurs) 512 o ; EF-1 (profil CBOR) 2 048 o ; EF-2 (portrait WebP 480×480) 20 480 o ; EF-3 (mémo vocal Opus SILK) 46 080 o ; EF-4 (directives de sépulture) 15 360 o ; EF-5 (sceau COSE_Sign1) 2 048 o. Total utile 86 528 o sur 92 160 o ; réserve d'usure 5 632 o (6,11 %), au-dessus du plancher de 5 %. Somme recontrôlée par Claude AI le 2026-10-05.

---

## 2. Décisions en Attente d'Arbitrage

- `DEC-AET-03` : cadre légal de la désignation du mandataire et de la transmission du coffre mémoriel. Consigne de Kudoro du 2026-10-04 : « voir ce que la loi permet ». C'est une demande d'étude, pas encore un arbitrage : étude sourcée attendue du Bushi 13 (`LEGAL-001`), puis décision.
- `DEC-AET-05`, complément : référence de l'autorisation administrative de l'autorité compétente pour la mémoire forestière. Aucune politique réelle ne peut être émise sans elle.

*`DEC-AET-01`, `DEC-AET-02`, `DEC-AET-04` à `DEC-AET-16` : arbitrées le 2026-10-04 et le 2026-10-05, voir §1.*
