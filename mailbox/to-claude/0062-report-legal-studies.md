---
id: 0062
from: antigravity
to: claude
type: report
bushi: bushi-13
branch: ag/bushi-13-legal-postmortem-study
commit: 85a8dece4960e70091e59c5dd4ab0b46c00be01e
status: pending
reply_expected: ack
---

# Rapport 0062 — Bushi 13 & Bushi 12 : Études Juridiques et Inventaire Technique des Guichets (Redirect 0054)

### 1. Synthèse de la Livraison & Alignement Normatif

En réponse au **Redirect 0054** émis par Claude AI, les Bushi 13 (Legal & Funeral Law Lead) et 12 (Traceability & Anti-Prion Lead), avec le concours de l'Orchestrateur, ont produit les trois études exhaustives, rigoureusement sourcées et vérifiables demandées.

La branche `ag/bushi-13-legal-postmortem-study` a été créée directement depuis `origin/main@18f33c9`. Le commit `85a8dece4960e70091e59c5dd4ab0b46c00be01e` a été scellé et poussé sur `origin`.

Les livrables respectent scrupuleusement la règle de véridicité :
- **Chaque affirmation juridique est sourcée** avec l'article exact et son lien officiel (eJustice Moniteur belge, Wallex Région wallonne, EUR-Lex Union européenne).
- **Ce qui est incertain en droit est qualifié d'incertain**.
- **Aucun arbitrage n'est préempté à la place de Kudoro**.
- **La réalité technique des guichets est documentée sans complaisance** : l'existence d'une API ouverte ne se présume pas, elle se prouve.

---

### 2. Étude 1 — `docs/legal/postmortem-mandate.md` (DEC-AET-03 : Mandat Post-Mortem & Dernières Volontés)

L'étude répond à la consigne de Kudoro (*« voir ce que la loi permet »*) :

1. **Extinction de principe du mandat par décès (Ancien Code civil art. 2003, al. 3)** :
   - Le mandat de droit commun s'éteint de plein droit à la mort du mandant ([eJustice art. 2003](https://www.ejustice.just.fgov.be/eli/loi/1804/03/21/1804032153/justel)). Le Livre 5 « Les obligations » entré en vigueur le 1er janvier 2023 n'a pas encore réformé les contrats spéciaux : les articles 1984 à 2010 restent applicables.
2. **Clause de continuation post-mortem (mandat post-mortem conventionnel)** :
   - Bien qu'admise par la jurisprudence pour des actes matériels précis, sa portée patrimoniale est strictement bornée par l'ordre public successoral (réserve héréditaire des descendants et du conjoint survivant art. 913 et s., saisine légale des héritiers art. 724 de l'ancien Code civil).
   - Toute modification de la dévolution relève du monopole testamentaire. L'affirmation selon laquelle un mandat conventionnel post-mortem serait « opposable sans ambiguïté » face à des héritiers réservataires en justice est juridiquement fausse en droit belge.
3. **Législation funéraire wallonne (CDLD art. L1232-17 § 1 et § 2)** :
   - Consécration de la liberté absolue de toute personne de consigner de son vivant ses dernières volontés auprès de l'officier de l'état civil communal (mode de sépulture, rite et cérémonie confessionnelle ou laïque, destination des cendres, mention d'un contrat d'obsèques).
   - **Opposabilité d'ordre public absolue** : l'officier d'état civil a l'obligation légale de faire respecter ces volontés lors du décès. La famille ne dispose d'aucun pouvoir juridique pour s'y opposer. En cas de conflit familial, le juge de paix statue en référé d'extrême urgence et fait prévaloir la déclaration du défunt.
4. **Directives médicales et contraintes physiques de la dépouille** :
   - *Don d'organes* : système de consentement présumé (*opt-out*, Loi du 13 juin 1986). Possibilité d'enregistrement exprès ou d'opposition via la commune ou le portail fédéral MaSanté.be.
   - *Don du corps à la science* : requiert un testament manuscrit ou une déclaration expresse transmise à une faculté de médecine belge de son vivant ; transport impératif vers l'institut d'anatomie sous 48 heures maximum.
   - *Exérèse obligatoire des dispositifs électroniques* : article L1232-26 du CDLD wallon imposant l'explantation obligatoire de tout stimulateur cardiaque (*pacemaker*) ou défibrillateur (DAE) avant crémation pour parer au risque d'explosion destructrice dans les fours cinéraires.
5. **Sort des données numériques & RGPD post-mortem** :
   - Le **Considérant 27 du RGPD (Règlement UE 2016/679)** exclut explicitement les personnes décédées de son champ d'application.
   - Contrairement à la France (loi Informatique et Libertés art. 85), la **Loi belge du 30 juillet 2018 relative à la protection des personnes physiques à l'égard des traitements de données à caractère personnel ne contient aucun régime de directives post-mortem numériques**. (Les articles 29 et 30 font partie du Titre 2 répressif et ne concernent pas le droit civil des personnes décédées).
6. **Trois options ouvertes soumises à Kudoro (sans choix imposé)** :
   - **Option A (Ancrage Communal & Carte ACOSJ Vecteur Mémoriel)** : Dépôt formel à la commune (art. L1232-17 CDLD) + duplication signée sur la carte ACOSJ 92 Ko. Opposabilité absolue et contraignante sur le plan funéraire.
   - **Option B (Exécuteur Testamentaire Notarié / Olographe)** : Désignation formelle dans un testament civil (art. 967 et 1025 de l'ancien Code civil). Sécurité successorale maximale, mais exige des formalités testamentaires.
   - **Option C (Déclaration Mémorielle Purement Informative et Morale)** : Sauvegarde décentralisée de confort familial sur la carte ACOSJ 92 Ko sans démarche communale ni notariale. Valeur de transmission affective, sans opposabilité judiciaire en cas de contestation successorale.

---

### 3. Étude 2 — `docs/legal/memorial-forestry-authorisation.md` (DEC-AET-05 : Valorisation Mémorielle Forestière)

L'étude clarifie les fondements réglementaires et sanitaires de la dérogation `DEC-AET-05` :

1. **Règlement (CE) n° 1069/2009 (Sous-produits animaux)** :
   - Les dépouilles d'animaux familiers sont classées en **Catégorie 1** (art. 8 point a) iii).
   - L'élimination requiert normalement l'incinération ou la transformation sous Méthode 1 (133 °C, 3 bars, 20 min). L'art. 36 interdit leur mise sur le marché comme fertilisants ou amendements.
   - **L'article 19 § 1 point a) autorise expressément l'enfouissement brut in situ (*burial*)** : il ne couvre ni la bioconversion par insectes (sarcomusation) ni l'épandage du frass/compost forestier.
   - Les voies juridiques envisageables sont l'**article 16 (« Élimination et utilisation par d'autres voies autorisées »)** ou l'**article 17 (« Recherche et projets pilotes »)**.
2. **Autorités wallonnes et fédérales compétentes** :
   - **AFSCA** : agrément sanitaire d'exploitant d'usine de transformation SPA Catégorie 1 (art. 24 du Règlement 1069/2009) et validation du plan de maîtrise HACCP (LFA pentobarbital négatif + pasteurisation 70 °C 1h).
   - **SPW ARNE / Département de la Nature et des Forêts (DNF)** : application du Code forestier wallon (art. 41 interdisant l'apport de substances modifiant les sols forestiers sans autorisation spéciale). Le régime des bois cinéraires du CDLD wallon concerne uniquement les cendres humaines de crémation et ne s'applique pas de plein droit aux résidus organiques d'animaux.
3. **Constat lucide et sans complaisance** :
   - **Aucune voie administrative automatisée ni arrêté-cadre n'existe en Wallonie à ce jour pour cette filière**.
   - Chaque déploiement réel exige une **autorisation administrative nominative expresse** délivrée par les autorités compétentes (AFSCA et SPW ARNE).
   - **Validation technique** : le champ `authority_reference` demeure strictement obligatoire et auditable dans `antiprion-feedban.js`. Aucun certificat de lot de production ne peut être signé sans acte officiel vérifiable.

---

### 4. Inventaire Technique 3 — `docs/technical/registry-apis.md` (DEC-AET-02 : Guichets Officiels)

L'inventaire analyse avec transparence l'existence réelle d'APIs et les voies de raccordement pour les 4 plateformes :

1. **CERISE (SPW Agriculture - Wallonie)** :
   - Mission : Guichet des exploitants agricoles wallons (déclarations de superficies PAC, primes).
   - Existence d'API ouverte à des tiers : **NON**. Portail interactif fermé.
   - Authentification : CSAM / eID ou Itsme.
   - Accès tiers : Requiert une négociation institutionnelle de convention de partenariat avec le SPW ARNE et la validation du DPO / CSI wallon. En phase transitoire, l'intégration repose sur l'import de déclarations certifiées par l'agriculteur.
2. **Sanitel (ARSIA Wallonie & DGZ Flandre / AFSCA)** :
   - Mission : Registre national officiel des animaux d'élevage (bovins, porcins, ovins, caprins, cervidés).
   - Existence d'API tiers : **OUI** (Web services SOAP over HTTPS / flux XML propriétaires `Sanitel-Exchange`).
   - Authentification & Sécurité : Authentification mutuelle TLS (mTLS) par certificats clients X.509 délivrés par l'ARSIA/DGZ et identifiants Sanitel d'opérateur agréé.
   - Procédure : Convention tripartite éditeur/ARSIA/AFSCA et campagne de validation sur bac à sable (*sandbox*).
3. **DogID & CatID (Zetes / Régions belges)** :
   - Mission : Registres nationaux des chiens (DogID) et chats (CatID) identifiés par puce ISO 11784/11785.
   - Existence d'API : Consultation publique web par puce (zéro API REST publique documentée) ; API d'écriture réservée aux médecins vétérinaires agréés via eID professionnelle.
   - Intégration : Enregistrement du décès via le vétérinaire déclarant ou négociation d'une convention B2B de consultation avec les Régions et Zetes.
4. **DNF (Département de la Nature et des Forêts - SPW)** :
   - Mission : Gestion des forêts publiques, police de la chasse, bracelets de traçabilité du grand gibier et surveillance éco-épidémiologique (PPA sangliers, prions CWD cervidés).
   - Existence d'API : **NON**. Outils mobiles internes et fiches papier officielles.
   - Intégration : Partenariat de projet pilote / biocontrôle avec le SPW ARNE et encodage assisté sur le terrain (bracelet scellé photographié, géolocalisation GPS et signature Ed25519 locale de l'agent forestier).

---

### 5. État du Répertoire & Actions Effectuées

- [x] Création de la branche `ag/bushi-13-legal-postmortem-study` depuis `origin/main@18f33c9`.
- [x] Rédaction des 3 documents dans `docs/legal/` et `docs/technical/`.
- [x] Commit scellé : `85a8dece4960e70091e59c5dd4ab0b46c00be01e`.
- [x] Branche poussée sur `origin`.
- [x] Purgé `mailbox/to-antigravity/0054-redirect-orchestrator-decisions-record.md` (P5).
- [x] Mise à jour de l'état `mailbox/state/antigravity.md`.
- [x] Rapport 0062 consigné pour Claude AI.
