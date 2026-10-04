> « Avertissement de gouvernance : Ces études sont rédigées par des agents techniques. Elles préparent une question à poser à un juriste ou à l'autorité compétente ; elles ne la remplacent pas. »

# Inventaire Technique des Guichets Officiels d'Identification Animale et Agricole (DEC-AET-02)

> **Auteurs** : Bushi 15 (Lead Intégrations) / Bushi 11 (Bio-Traçabilité) / Orchestrateur Antigravity  
> **Date de rédaction** : 4 octobre 2026 (révision v2.0)  
> **Contexte de la saisine** : Exécution de l'arbitrage souverain `DEC-AET-02` prononcé par Kudoro : *« prévoir cette connexion API à tous les points d'accès tel que Cerise en Wallonie »*.  
> **Objet du document** : Inventaire technique sourcé, rigoureux et vérifiable de l'existence réelle d'APIs publiques ou partenaires, des portails d'accès officiels, des conditions d'accès et des démarches de conventionnement pour les 4 guichets cibles belges et wallons.  
> **Statut du document** : Étude technique préparatoire, exclusion des suppositions non documentées et feuille de route d'interfaçage.

---

## 1. Contexte & Principes d'Intégration AeterniTrak

L'architecture AeterniTrak V1.0 assure la traçabilité intégrale de la dépouille depuis le point de collecte jusqu'à la destination finale (mémorielle, technique ou cimenterie). Pour garantir l'intégrité des données d'entrée sans double saisie humaine propice aux erreurs ou à la fraude, le système doit se connecter aux bases de données officielles de référence.

Conformément à la consigne de Kudoro (`DEC-AET-02`) et aux exigences de vérification de Claude AI (Redirect 0068) : **l'existence d'une API ne se présume pas, elle se prouve**. Aucune spécification technique (telle que SOAP, REST, MTOM, mTLS) n'est affirmée si elle n'est pas adossée à une documentation officielle publique accessible en ligne. Lorsque aucune API publique n'est documentée, le document le stipule honnêtement et recense les contacts officiels pour solliciter une convention bilatérale partenaire.

---

## 2. Synthèse Comparative des 4 Guichets Cibles

| Guichet / Organisme | Périmètre Métier & Espèces | Existence d'une API Publique Ouverte | Documentation Publique Disponible | Statut Technique Réel & Démarche d'Accès |
| :--- | :--- | :---: | :--- | :--- |
| **CERISE** *(SPW Agriculture)* | Agriculteurs wallons, déclarations PAC, parcelles, cheptels. | **NON** *(Portail Web fermé)* | Aucune documentation d'API publique disponible en ligne. | **Non établi publiquement** : intégration sous convention partenaire à solliciter auprès du SPW Agriculture via ses portails officiels. Accès usager réservé via CSAM (eID/itsme). |
| **Sanitel** *(ARSIA / DGZ / AFSCA)* | Élevage national (bovins, porcins, ovins, caprins, cervidés). | **NON** *(Filière fermée)* | Aucune spécification technique d'API (WSDL/OpenAPI) publiée en libre accès. | **Non établi publiquement** : intégration sous convention partenaire à solliciter auprès de l'ARSIA et de la DGZ. Échanges réservés aux opérateurs conventionnés. |
| **DogID & CatID** *(Zetes / Régions)* | Chiens et chats domestiques identifiés par puce ISO 11784/11785. | **NON** *(Portail vétérinaire)* | Recherche web publique par numéro de puce (sans API documentée). | **Non établi publiquement** : intégration sous convention partenaire à solliciter auprès des gestionnaires des registres. Encodage réservé aux vétérinaires agréés via eID. |
| **DNF** *(SPW ARNE)* | Faune sauvage, bracelets gibier, veille sanitaire PPA/CWD. | **NON** *(Intranet administratif)* | Aucune interface de programmation publique existante. | **Non établi publiquement** : intégration sous convention partenaire / protocole pilote à solliciter auprès du SPW ARNE — DNF. Traçabilité sur bracelet physique scellé. |

---

## 3. Analyse Détaillée par Plateforme

### 3.1 CERISE (SPW Agriculture — Région Wallonne)
- **Autorité de tutelle** : Service Public de Wallonie — Agriculture, Ressources Naturelles et Environnement (SPW ARNE).
- **Missions de la plateforme** : CERISE est le guichet électronique destiné aux exploitants agricoles wallons pour la gestion des déclarations de superficie (aides PAC), des primes et de l'inventaire d'exploitation.
- **Portails institutionnels racine** : [https://cerise.arsia.be/](https://cerise.arsia.be/) (Portail web de télédéclaration CERISE géré par l'ARSIA pour les démarches et l'identification d'élevage) et [https://agriculture.wallonie.be/](https://agriculture.wallonie.be/) (Portail officiel de l'Agriculture en Wallonie).
- **Existence d'une API publique** : **NON**.  
  Une inspection minutieuse des portails régionaux wallons et des catalogues de données ouvertes (Open Data Wallonie-Bruxelles) confirme qu'il n'existe aucune API publique documentée pour CERISE. L'application est strictement conçue comme une interface web interactive avec authentification fédérale CSAM (carte eID ou application itsme).
- **Statut d'intégration AeterniTrak** :  
  **Non établi publiquement : intégration sous convention partenaire à demander auprès du SPW Agriculture, Ressources Naturelles et Environnement.**
- **Coordonnées et portails institutionnels racine** :  
  SPW ARNE — Direction générale opérationnelle de l'Agriculture  
  Chaussée de Louvain 14, 5000 Namur (Belgique)  
  Portails web institutionnels : [https://cerise.arsia.be/](https://cerise.arsia.be/) et [https://agriculture.wallonie.be/](https://agriculture.wallonie.be/)

---

### 3.2 Sanitel / ARSIA (Wallonie) & DGZ (Flandre)
- **Autorités responsables** :  
  - Tutelle sanitaire : Agence Fédérale pour la Sécurité de la Chaîne Alimentaire (AFSCA) (Loi du 4 février 2000 relative à la création de l'Agence fédérale pour la Sécurité de la chaîne alimentaire — référence à confirmer par un juriste).
  - Gestion déléguée : **ARSIA** (*Association Régionale de Santé et d'Identification Animales*, en Wallonie) et **DGZ** (*Dierengezondheidszorg Vlaanderen*, en Flandre).
- **Missions de la plateforme** : Sanitel est le registre national officiel d'identification et de suivi des animaux de rente (bovins, porcs, ovins, caprins, cervidés, volailles). Il enregistre les naissances, les mouvements, les décès et les statuts sanitaires officiels.
- **Portails institutionnels racine** :  
  - ARSIA Wallonie : [https://www.arsia.be/](https://www.arsia.be/)
  - DGZ Flandre : [https://www.dgz.be/](https://www.dgz.be/)
  - Portail AFSCA : [https://www.favv-afsca.be/](https://www.favv-afsca.be/)
- **Existence d'une API publique** : **NON**.  
  Aucune spécification d'API ouverte (documentation REST OpenAPI, fichiers WSDL ou schémas XSD) n'est mise à disposition du public en ligne. Si des flux d'échange automatisés existent pour les logiciels de gestion d'élevage et les abattoirs, ces passerelles relèvent exclusivement d'accords d'interopérabilité bilatéraux soumis à agrément préalable et accord de confidentialité.
- **Statut d'intégration AeterniTrak** :  
  **Non établi publiquement : intégration sous convention partenaire à demander auprès de l'ARSIA asbl et de la DGZ vzw.**
- **Coordonnées et portails institutionnels racine** :  
  - ARSIA asbl : Allée du Carmel 1, 5590 Ciney (Belgique) — Portail : [https://www.arsia.be/](https://www.arsia.be/)  
  - DGZ vzw : Industrieweg 242, 8800 Roeselare (Belgique) — Portail : [https://www.dgz.be/](https://www.dgz.be/)  
  - AFSCA : Boulevard du Jardin Botanique 55, 1000 Bruxelles — Portail : [https://www.favv-afsca.be/](https://www.favv-afsca.be/)

---

### 3.3 CatID & DogID (Registres Nationaux des Animaux de Compagnie)
- **Autorités de tutelle** : Les 3 Régions administratives belges (Région wallonne, Région flamande, Région de Bruxelles-Capitale - Bien-être animal). Opérateur technique désigné : **Zetes SA**.
- **Missions des registres** : Centralisation des identifications par transpondeurs électroniques sous-cutanés (micro-puces ISO 11784/11785) pour les chiens (DogID) et les chats (CatID).
- **Portails institutionnels racine** :  
  - DogID : [https://www.dogid.be/](https://www.dogid.be/)
  - CatID : [https://www.catid.be/](https://www.catid.be/)
- **Existence d'une API publique** : **NON**.  
  Les sites grand public proposent uniquement un formulaire web de recherche ponctuelle d'un numéro de puce (avec contrôle anti-robot captcha), sans point d'accès API documenté. L'accès d'encodage professionnel (enregistrement de puce, changement de propriétaire, déclaration de décès) est strictement réservé aux vétérinaires agréés s'authentifiant par carte d'identité électronique belge (eID).
- **Statut d'intégration AeterniTrak** :  
  **Non établi publiquement : intégration sous convention partenaire à demander auprès de Zetes SA / Services DogID & CatID et des autorités régionales du Bien-être animal.**
- **Coordonnées et portails institutionnels racine** :  
  DogID & CatID — Service Gestion des Enregistrements  
  Boîte Postale 20000, 1070 Bruxelles (Belgique)  
  Portails web officiels : [https://www.dogid.be/](https://www.dogid.be/) et [https://www.catid.be/](https://www.catid.be/)

---

### 3.4 DNF (Département de la Nature et des Forêts — SPW ARNE)
- **Autorité responsable** : Service Public de Wallonie — Agriculture, Ressources Naturelles et Environnement (SPW ARNE), Département de la Nature et des Forêts (DNF).
- **Missions** : Gestion du domaine forestier public régional, surveillance de la faune sauvage, attribution et contrôle des bracelets cynégétiques de traçabilité du grand gibier abattu ou trouvé mort, veille éco-épidémiologique (PPA chez le sanglier, CWD chez le cerf).
- **Portail institutionnel racine** : [https://environnement.wallonie.be/](https://environnement.wallonie.be/) (Portail officiel de l'Environnement et des Forêts en Wallonie - SPW).
- **Existence d'une API publique** : **NON**.  
  Le DNF ne dispose d'aucune interface informatique ouverte à des tiers. Les opérations de terrain s'appuient sur des applications internes réservées aux agents assermentés et sur la pose de scellés physiques numérotés (bracelets inviolables).
- **Statut d'intégration AeterniTrak** :  
  **Non établi publiquement : intégration sous convention partenaire / protocole pilote à demander auprès du SPW ARNE — Département de la Nature et des Forêts.**
- **Coordonnées et portail institutionnel racine** :  
  SPW ARNE — Département de la Nature et des Forêts  
  Avenue Prince de Liège 15, 5100 Jambes (Namur, Belgique)  
  Portail officiel : [https://environnement.wallonie.be/](https://environnement.wallonie.be/)

---

## 4. Stratégie d'Ingénierie pour AeterniTrak V1.0 en l'Absence d'APIs Publiques

Constatant qu'**aucun des quatre guichets ne propose d'API publique ouverte**, l'architecture technique d'AeterniTrak V1.0 ne doit pas reposer sur des suppositions technologiques infondées. Elle s'organise autour d'une stratégie réaliste et robuste en deux temps :

1. **Phase Immédiate V1.0 (Mode Déclaratif Sécurisé à Preuve Cryptographique Locale)** :
   - *Ferme (Sanitel)* : Capture photographique de la boucle auriculaire officielle `BE xxxxxxxxx`, saisie du numéro Sanitel et signature cryptographique locale (Ed25519 ou ES256) du collecteur attestant de l'identité de l'animal.
   - *Compagnie (CatID / DogID)* : Lecture RFID de la puce ISO 11784/11785 par transpondeur NFC/RFID standard, capture du code 15 chiffres, vérification algorithmique du préfixe pays `056` et signature numérique du vétérinaire ou du refuge lors de la remise de la dépouille.
   - *Faune Sauvage (DNF)* : Saisie du numéro de scellé/bracelet DNF officiel, géolocalisation GPS du prélèvement et badge d'agent forestier scellé dans l'enveloppe COSE.
   - *Agriculture (CERISE)* : Import des pièces justificatives officielles (extraits PDF/A certifiés générés depuis le portail web CERISE de l'agriculteur), scellés par empreinte SHA-256 dans la revendication de lot.

2. **Phase Conventionnelle (Mise en Place de Conventions de Partenariat)** :
   Les flux techniques d'échange post-mortem relèvent exclusivement de conventions de partenariat à établir formellement avec chaque autorité compétente (SPW ARNE, ARSIA/DGZ, gestionnaires DogID/CatID). En l'absence de protocoles documentés publiquement, aucune interface automatisée n'est présumée et tout raccordement futur fera l'objet d'un accord bilatéral spécifique.
