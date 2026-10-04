# Inventaire Technique des Guichets Officiels d'Identification Animale et Agricole (DEC-AET-02)

> **Auteurs** : Bushi 15 (Lead Intégrations) / Bushi 11 (Bio-Traçabilité) / Orchestrateur Antigravity  
> **Date de rédaction** : 4 octobre 2026  
> **Contexte de la saisine** : Exécution de l'arbitrage souverain `DEC-AET-02` prononcé par Kudoro : *« prévoir cette connexion API à tous les points d'accès tel que Cerise en Wallonie »*.  
> **Objet du document** : Inventaire technique sourcé, rigoureux et vérifiable de l'existence réelle d'APIs publiques ou partenaires, des protocoles de télé-déclaration, des conditions d'accès, des contraintes d'authentification et des démarches de conventionnement pour les 4 guichets cibles belges et wallons.  
> **Statut du document** : État de l'art technique et feuille de route d'interfaçage.

---

## 1. Contexte & Principes d'Intégration AeterniTrak

L'architecture AeterniTrak V1.0 assure la traçabilité intégrale de la dépouille depuis le point de collecte jusqu'à la destination finale (mémorielle, technique ou cimenterie). Pour garantir l'intégrité des données d'entrée sans double saisie humaine propice aux erreurs ou à la fraude, le système doit se connecter aux bases de données officielles de référence.

Conformément à la consigne de Kudoro (`DEC-AET-02`), cet inventaire dresse la réalité technique exacte du terrain : **l'existence d'une API ouverte à des tiers ne se présume pas, elle se prouve**. Lorsque aucune API publique n'existe, les démarches institutionnelles et les protocoles de conventionnement requis sont documentés de manière transparente.

---

## 2. Synthèse Comparative des 4 Guichets Cibles

| Guichet / Organisme | Périmètre Métier & Espèces | Existence d'une API Tiers Ouverte | Protocole Technique / Format | Authentification Requise | Démarche d'Accès pour AeterniTrak |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **CERISE** *(SPW Agriculture)* | Agriculteurs wallons, déclarations PAC, parcelles, cheptels. | **NON** *(Portail Web fermé)* | Aucun point d'accès public documenté. | CSAM (eID citoyen / Itsme). | Négociation d'une convention d'échange de données avec le SPW ARNE et accord DPO. |
| **Sanitel** *(ARSIA / DGZ)* | Élevage national (bovins, porcins, ovins, caprins, cervidés). | **OUI** *(Sous convention stricte)* | Web Services SOAP over HTTPS / flux XML propriétaires. | Certificats clients X.509 + Identifiants d'établissement agréé. | Agrément éditeur logiciel ARSIA/DGZ, convention tripartite avec l'AFSCA. |
| **DogID & CatID** *(Zetes / Régions)* | Chiens et chats domestiques identifiés par puce ISO 11784/11785. | **OUI** *(Usage vétérinaire exclusif)* | Formulaires web / Web Services REST/SOAP vétérinaires. | Carte d'identité eID vétérinaire agréé ou certificat professionnel. | Intermédiation via le vétérinaire traitant ou convention de délégation régionale. |
| **DNF** *(SPW ARNE)* | Faune sauvage, bracelets gibier, tirs sanitaires (PPA, prions CWD). | **NON** *(Intranet de police forestière)* | Applications mobiles internes SPW / fiches de bord papier. | Identifiants agents assermentés de la Région wallonne. | Protocole d'accord de recherche / projet pilote avec le SPW et encodage assisté. |

---

## 3. Analyse Détaillée par Plateforme

### 3.1 CERISE (SPW Agriculture — Région Wallonne)
- **Autorité de tutelle** : Service Public de Wallonie — Agriculture, Ressources Naturelles et Environnement (SPW ARNE), Direction générale opérationnelle de l'Agriculture (DGARNE).
- **Missions de la plateforme** : CERISE est le guichet électronique unique destiné aux exploitants agricoles de la Région wallonne. Il permet la télédéclaration annuelle des parcelles agricoles (déclaration de superficie PAC), la gestion des primes et aides à l'investissement, ainsi que la consultation de l'inventaire des troupeaux.
- **Portail officiel** : [https://cerise.wallonie.be](https://cerise.wallonie.be)
- **Existence d'une API tierce** : **NON**.  
  À ce jour, le SPW Agriculture ne met à disposition aucune API publique (REST, OpenAPI, GraphQL ou SOAP) permettant à des progiciels tiers ou plateformes privées d'interroger directement la base ou d'injecter des données par voie programmatique. L'accès est conçu exclusivement comme une application web interactive pour l'agriculteur.
- **Sécurité et Authentification** :  
  L'accès au portail CERISE est protégé par la passerelle d'authentification fédérale belge **CSAM** (gestion des accès des agents de l'État et des citoyens). L'accès requiert soit une carte d'identité électronique belge (eID) avec lecteur de carte et code PIN, soit l'application d'identité numérique souveraine **Itsme**.
- **Démarches et feuille de route pour AeterniTrak** :
  1. Déposer une demande de convention de partenariat auprès de la Direction de l'Économie agricole du SPW ARNE.
  2. Présenter un dossier d'évaluation d'impact sur la protection des données (DPIA / AIPD) au DPO du SPW et au Comité de Sécurité de l'Information (CSI) wallon.
  3. Dans l'attente d'une passerelle API régionale (sur la plateforme d'interopérabilité *Wallonie E-Business*), l'intégration V1.0 doit reposer sur l'import des déclarations de parcelles et attestations d'exploitation signées numériquement par l'exploitant au format PDF/A ou CSV officiel exporté de CERISE.
- **Contacts institutionnels** :  
  SPW Agriculture, Ressources Naturelles et Environnement  
  Chaussée de Louvain 14, 5000 Namur (Belgique)  
  *Support technique CERISE* : `cerise@spw.wallonie.be` / *Helpdesk agricole* : `agriculture.spw@spw.wallonie.be`

---

### 3.2 Sanitel / ARSIA (Wallonie) & DGZ (Flandre)
- **Autorités responsables** :  
  - Tutelle sanitaire : Agence Fédérale pour la Sécurité de la Chaîne Alimentaire (AFSCA).
  - Gestion opérationnelle : **ARSIA** (*Association Régionale de Santé et d'Identification Animales*, en Wallonie) et **DGZ** (*Dierengezondheidszorg Vlaanderen*, en Flandre).
- **Missions de la plateforme** : Sanitel est le système d'information national officiel d'enregistrement des animaux de rente (bovins, porcs, moutons, chèvres, cervidés d'élevage, volailles). Il gère le cycle de vie de chaque boucle auriculaire officielle, les enregistrements de naissance, les mouvements entre exploitations (acheminement, abattoir, décès) et les statuts épidémiologiques sanitaires (IBR, BVD, etc.).
- **Portails officiels** :  
  - ARSIA Wallonie : [https://www.arsia.be](https://www.arsia.be)
  - DGZ Flandre : [https://www.dgz.be](https://www.dgz.be)
  - Portail Sanitel-AFSCA : [https://www.favv-afsca.be](https://www.favv-afsca.be)
- **Existence d'une API tierce** : **OUI (Système d'échange B2B sécurisé)**.  
  L'ARSIA et la DGZ disposent d'interfaces de télé-déclaration machine-to-machine opérationnelles (`Sanitel-Exchange` / `ARSIA-Net Web Services`), exploitées par les éditeurs de logiciels de gestion de troupeau, les laboratoires vétérinaires et les systèmes d'abattoirs agréés.
- **Spécifications techniques & Sécurité** :
  - **Protocole** : Web Services SOAP 1.2 over HTTPS / MTOM, avec schémas de validation XSD stricts.
  - **Authentification** : Authentification mutuelle TLS (mTLS) par certificats clients X.509 délivrés par l'autorité de certification de l'ARSIA/DGZ, combinée à une clé d'accès partenaire (API Token) et à un numéro Sanitel d'opérateur d'équarrissage ou de centre de traitement agréé.
  - **Fonctionnalités disponibles** : Notification de sortie de troupeau pour cause de mort, déclaration d'enlèvement de carcasse, vérification en temps réel de l'existence et du statut sanitaire d'un numéro d'identification individuel (ex. boucle belge `BE 123456789`).
- **Démarches et conventionnement pour AeterniTrak** :
  1. Solliciter un agrément en tant qu'éditeur de logiciel de traçabilité auprès du département informatique de l'ARSIA.
  2. Signer la convention d'interopérabilité Sanitel et l'accord de confidentialité des données sanitaires d'élevage.
  3. Réaliser la campagne de tests d'intégration sur l'environnement de bac à sable (*sandbox*) de l'ARSIA avant délivrance du certificat client de production.
- **Contacts institutionnels** :  
  ARSIA asbl — Allée du Carmel 1, 5590 Ciney (Belgique)  
  *Support informatique & interfaces partenaires* : `support@arsia.be` / Tél : +32 (0)83 23 05 11  
  DGZ vzw — Industrieweg 242, 8800 Roeselare (Belgique) — `info@dgz.be`

---

### 3.3 CatID & DogID (Registres Nationaux des Animaux de Compagnie)
- **Autorités de tutelle** : Les 3 Régions administratives belges (Région wallonne - Bien-être animal, Région Flamande, Région de Bruxelles-Capitale). La gestion opérationnelle et technique des bases de données est concédée à la société technologique **Zetes SA**.
- **Missions des registres** :
  - **DogID** : Identification obligatoire des chiens depuis 1998.
  - **CatID** : Identification et enregistrement obligatoires des chats depuis le 1er novembre 2017.
  - Gestion des numéros de puces électroniques sous-cutanées (transpondeurs passifs conformes aux normes ISO 11784 et ISO 11785, encodés sur 15 chiffres, débutant par `056` pour la Belgique).
- **Portails officiels** :  
  - DogID : [https://www.dogid.be](https://www.dogid.be)
  - CatID : [https://www.catid.be](https://www.catid.be)
- **Existence d'une API tierce** :
  - **Volet consultation publique** : Aucun endpoint API REST ouvert. La consultation s'effectue via un moteur de recherche web protégé par captcha sur `dogid.be` et `catid.be`. Les résultats affichent uniquement le nom de l'animal, la race et le statut d'enregistrement (zéro donnée personnelle affichée, sauf consentement explicite préalable du propriétaire).
  - **Volet professionnel (Écriture & Mutation)** : OUI, mais strictement réservé aux vétérinaires agréés et aux refuges reconnus. L'interfaçage est intégré nativement dans les progiciels de gestion vétérinaire agréés (ex. Corilus, Veteasy).
- **Sécurité et Authentification** :  
  Authentification forte obligatoire via eID du médecin vétérinaire inscrit à l'Ordre des Médecins Vétérinaires (NGV/CRMV). Tout acte d'encodage (notamment la déclaration officielle de décès de l'animal sur DogID/CatID) engage la responsabilité légale du praticien.
- **Démarches et feuille de route pour AeterniTrak** :
  1. *Option opérationnelle immédiate* : L'enregistrement du décès dans CatID/DogID est opéré par le médecin vétérinaire lors de l'euthanasie ou du constat de décès. L'application AeterniTrak invite le vétérinaire à scanner la puce et à signer l'attestation de clôture via son certificat ou l'application mobile.
  2. *Option conventionnelle B2B* : Demande d'un accès en lecture seule par API partenaire auprès de Zetes et des administrations régionales du Bien-être animal pour valider automatiquement l'authenticité d'un numéro de puce lors de la prise en charge mémorielle.
- **Contacts institutionnels** :  
  DogID & CatID — Service Gestion des Enregistrements  
  Boîte Postale 20000, 1070 Bruxelles (Belgique)  
  *Contact technique* : `info@dogid.be` / `info@catid.be`

---

### 3.4 DNF (Département de la Nature et des Forêts — SPW ARNE)
- **Autorité responsable** : Service Public de Wallonie — Agriculture, Ressources Naturelles et Environnement (SPW ARNE), Département de la Nature et des Forêts (DNF).
- **Missions** : Gestion durable du patrimoine forestier public wallon, police de la chasse et de la faune sauvage, préservation de la biodiversité. Le DNF supervise le système officiel de pose des **bracelets de traçabilité cynégétique** pour le grand gibier (cerfs, sangliers, chevreuils) et assure la veille sanitaire éco-épidémiologique sur les zoonoses et épizooties majeures :
  - Peste Porcine Africaine (PPA) chez le sanglier ;
  - Maladie du Dépérissement Chronique des Cervidés (*Chronic Wasting Disease* - CWD / prions) chez les cervidés.
- **Portail d'information** : [https://environnement.wallonie.be/dnf](https://environnement.wallonie.be/dnf)
- **Existence d'une API tierce** : **NON**.  
  Le DNF ne propose aucune interface API machine-to-machine ouverte au public ou à des opérateurs privés.
- **Fonctionnement opérationnel réel** :  
  - Les agents assermentés du DNF (gardes-forestiers et chefs de cantonnement) disposent d'outils mobiles internes au SPW pour saisir les constats de tir, associer le numéro de scellé/bracelet officiel et renseigner les prélèvements d'échantillons biologiques pour analyse virologique ou sérologique (transmis à Sciensano et au laboratoire départemental).
  - La traçabilité physique repose sur le bracelet plastique inviolable numéroté fixé au tarse ou à la carcasse de l'animal et sur le document d'accompagnement du gibier sauvage abattu.
- **Démarches et feuille de route pour AeterniTrak** :
  - Pour intégrer les carcasses de faune sauvage (Profil 2 : Catégorie 1/2 Biocontrôle DNF) dans la filière de bioconversion avec méthode de stérilisation 1 (133 °C, 3 bars, 20 min), AeterniTrak doit opérer dans le cadre d'un **partenariat expérimental officiel / projet pilote** avec la Direction de la Chasse et de la Pêche du DNF.
  - Dans l'application mobile de terrain AeterniTrak, l'agent de collecte capture le numéro du bracelet DNF, prend une photographie géolocalisée (GPS) du scellé et enregistre le badge de l'agent forestier avec signature Ed25519 locale.
- **Contacts institutionnels** :  
  SPW ARNE — Département de la Nature et des Forêts  
  Avenue Prince de Liège 15, 5100 Jambes (Namur, Belgique)  
  *Direction de la Conservation de la Nature et de la Chasse* : `dnf.dgarne@spw.wallonie.be`

---

## 4. Recommandations d'Architecture pour l'Orchestrateur & Roadmap Technique

Sur la base de cet inventaire exhaustif, le tableau d'ingénierie suivant définit les connecteurs à implémenter dans le module `bio-traceability` :

1. **Connecteur Sanitel (Priorité B2B Élevée)** :  
   Développer le module client SOAP/XML sécurisé pour dialoguer avec les serveurs de test de l'ARSIA dès contractualisation. Ce connecteur traitera les flux de déclaration de cadavres d'élevage (bovins, porcins Catégorie 2).
2. **Connecteur DogID / CatID (Priorité B2C Mémoriel)** :  
   Implémenter le validateur d'intégrité de code puce ISO 11784/11785 (vérification checksum, format à 15 chiffres, code pays `056`) et structurer l'interface d'attestation vétérinaire locale dans l'application mobile.
3. **Module CERISE & DNF (Mode Déclaratif Sécurisé avec Preuve Cryptographique)** :  
   Dans l'attente de conventions bilatérales d'accès API, l'intégration repose sur le système de preuve AeterniTrak : signature cryptographique locale du déclarant (agriculteur ou garde DNF) attestant du numéro de dossier ou de bracelet, horodatage certifié RFC 3161 et attachement de la pièce justificative scellée dans l'enveloppe COSE.
