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

- **2026-10-04 · [Modèle Économique] · Kudoro**  
  *Question* : Quelle tarification pour l'accès étendu au Sanctuaire B2C ?  
  *Options* : A) Gratuité totale avec publicité ; B) Abonnement cher (40-50 €/an) ; C) Accueil 3 ans inclus à l'achat du médaillon funéraire, puis abonnement modique et perpétuel de 4,40 €/an.  
  *Arbitrage* : **Option C retenue**.  
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

---

- **2026-10-04 · [Support Silicium & Audio] · Kudoro (DEC-AET-01)**  
  *Question* : Faut-il maintenir une cible basse capacité 32 Ko avec compression audio agressive ou standardiser sur la JavaCard ACOSJ 92 Ko ?  
  *Options* : A) Support mixte 32 Ko (Opus 8 kbps / ADPCM) et 92 Ko ; B) Standardisation exclusive sur cartes JavaCard ACOSJ 92 Ko.  
  *Arbitrage* : **Option B retenue (Standardisation exclusive sur cartes 92 Ko ACOSJ)**.  
  *Justification* : Kudoro a tranché formellement : « QUE DES CARTES 92Ko ». Cela élimine tout compromis destructeur sur la fidélité acoustique ou le budget mémoire. La carte ACOSJ 92 Ko permet d'embarquer en autonomie totale le mémo vocal Opus SILK haute fidélité (16k / 24 kbps), le profil mémoriel CBOR certifié et jusqu'à 4 portraits WebP haute définition, sans aucune dépendance au réseau ni au cloud.

- **2026-10-04 · [Traçabilité Sanitaire & APIs Agricoles] · Kudoro (DEC-AET-02)**  
  *Question* : Comment interfacer la filière AeterniTrak avec les registres d'identification animale et de traçabilité ?  
  *Options* : A) Saisie manuelle des boucles et passeports ; B) Connexion API directe à tous les guichets de référence régionaux et fédéraux (CERISE SPW en Wallonie, Sanitel AFSCA, ARSIA, DGZ en Flandre).  
  *Arbitrage* : **Option B retenue (Connexion API multi-guichets : CERISE, Sanitel, ARSIA, DGZ)**.  
  *Justification* : Kudoro a tranché : « prévoir cette connexion API à tous les points d'accès tel que Cerise en Wallonie ». L'outil de traçabilité intégrera les connecteurs vers les guichets officiels régionaux (CERISE pour le SPW Agriculture wallon, ARSIA) et fédéraux (Sanitel bovin/porcin/ovin via l'AFSCA) pour automatiser la vérification des boucles auriculaires, des temps d'attente médicamenteux et des documents de transport sanitaires.

- **2026-10-04 · [Transmission & Mandat Notarial Post-Mortem] · Kudoro (DEC-AET-03)**  
  *Question* : Quel cadre légal retenir pour la désignation du mandataire et la transmission du coffre mémoriel familial ?  
  *Options* : A) Gestion purement applicative sans assise légale ; B) Alignement strict sur le droit notarial belge (mandat post-mortem art. 1984 C. civ., testament enregistré au CRT / Fednot, et Loi du 30 juillet 2018 relative aux données post-mortem).  
  *Arbitrage* : **Option B retenue (Cadre notarial opposable : mandat post-mortem & CRT / Fednot)**.  
  *Justification* : Kudoro a tranché : « voir ce que la loi permet ». Le coffre mémoriel et la clé de délégation familiale s'inscrivent dans le mandat post-mortem opposable aux tiers et le testament enregistré auprès du Registre Central des Testaments (CRT géré par Fednot), combiné aux articles 29 et 30 de la Loi belge du 30 juillet 2018 sur le sort des données numériques après la mort. Zéro ambiguïté sur la dévolution des souvenirs et le respect des dernières volontés.

- **2026-10-04 · [Filière Mémorielle Forestière — Base Légale] · Kudoro (Complément DEC-AET-05)**  
  *Question* : Quelle référence administrative fonde la dérogation mémorielle forestière des dépouilles de compagnie en Wallonie / Belgique ?  
  *Arbitrage* : **Règlement (CE) n° 1069/2009 article 19 §1 (a) combiné au Code wallon de l'environnement (D. 27 mai 2004) et aux circulaires régionales relatives aux bois cinéraires privés.**  
  *Justification* : L'article 19 §1 (a) du Règlement européen 1069/2009 autorise expressément l'autorité compétente à déroger à l'élimination standard pour les animaux de compagnie morts. Combiné au Code wallon de l'environnement et aux conditions sanitaires strictes (dépistage LFA pentobarbital négatif, pasteurisation 70°C/1h, absence totale de ruminants), cette base permet l'amendement cinéraire forestier commémoratif sous contrôle biologique, tout en maintenant l'interdiction absolue de toute réintroduction dans la chaîne trophique (feed ban).

---

## 2. Décisions en Attente d'Arbitrage

*(Aucune décision en attente à ce jour. L'intégralité des décisions DEC-AET-01 à DEC-AET-07 a été souverainement arbitrée par Kudoro).*

