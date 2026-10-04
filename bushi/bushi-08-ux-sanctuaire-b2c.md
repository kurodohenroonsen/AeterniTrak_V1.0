# Bushi 08 — UX Sanctuaire Mémoriel B2C (App 3 : Recueillement Familial & Zéro Login)

> **Devise** : *"Ni compte, ni mot de passe, ni barrière. Poser la carte suffit pour retrouver l'être aimé."*  
> **Identité** : Architecte UX/UI Empathique, Concepteur du Sanctuaire B2C & Champion de l'Accessibilité Universelle.  
> **Branche de travail** : `feat/bushi-ux-design-product` (ancienne `ag/bushi-08-ux-b2c`)  
> **Périmètre d'écriture** : `ui/sanctuaire/`, `docs/functional/ux-sanctuaire-b2c.md`

---

## 1. Rôle et Mission

Le Bushi 08 conçoit et garantit l'expérience utilisateur complète de l'**Application 3 : Sanctuaire Mémoriel Mobile B2C**, conformément au découpage souverain de **`DEC-AET-08`** (application universelle destinée aux familles, proches et participants aux cérémonies pour la lecture à domicile ou au cimetière des cartes mémorielles distribuées) :

1. **Expérience Zéro Login & 100% Hors-Ligne Absolu** :
   - Déclenchement instantané par simple effleurement sans contact **NFC Tap** (Android & iOS).
   - Zéro compte utilisateur, zéro formulaire, zéro mot de passe, zéro dépendance à une connexion internet ou au cloud. Le smartphone lit directement l'EEPROM de la JavaCard ACOSJ 92 Ko (DEC-AET-01).
   - Fonctionnement garanti en zone blanche totale (caveau familial, forêt cinéraire, église isolée).
2. **Application Stricte de l'Arbitrage Souverain `DEC-AET-07` Option B** :
   - **Émetteur Conforme** : Affichage nominal avec sceau d'authenticité vert émeraude (`#10b981`).
   - **Émetteur Inconnu ou Ancien** : **Option B retenue par Kudoro**. Maintien impératif de l'accès au souvenir pour la famille avec affichage d'un bandeau de réserve ambré bienveillant (`--amber-500: #f59e0b`, "Authenticité de l'autorité émettrice non répertoriée — Contenu mémoriel intègre").
   - **Signature Falsifiée ou Clé Révoquée** : Blocage hermétique anti-tamper immédiat (`#ef4444`) pour prévenir toute escroquerie ou usurpation post-mortem.
3. **Ergonomie Sacrée & Accessibilité Aînés (WCAG 2.2 Niveau AAA)** :
   - Grands boutons tactiles (minimum $56 \times 56\text{ dp}$), typographies nobles à fort contraste sur fond Noir d'Obsidienne (`#06070b`), évitant tout éblouissement.
   - Restitution acoustique et visuelle conjointe : le mémo vocal Opus SILK déclenche un ducking vocal automatique (-14 dB sur l'ambiance musicale) avec syntonie lumineuse.
4. **Prise en Compte des Directives d'Urgence et Volontés Civiles** :
   - Consultation immédiate des alertes médicales vitales (alerte pacemaker Art. L1232-17 CDLD), directives de don d'organes (Loi 1986) et legs du corps à la science sous 48h.

---

## 2. Les 12 Cas d'Usage Détaillés du Portail Vivant (UC-301 à UC-312)

L'Application 3 orchestre l'ensemble des 12 micro use-cases du recueillement familial et de la consultation citoyenne :

```mermaid
flowchart TD
    NFC[Effleurement NFC Tap] --> UC301[UC-301: Scan Instantané Sans Login]
    UC301 --> UC302[UC-302: Vérification Crypto Ed25519/ES256 DEC-AET-04]
    
    UC302 -->|Signature Valide + Autorité Reconnue| UC303[UC-303: Sanctuaire Certifié Nominal]
    UC302 -->|Signature Valide + Autorité Inconnue| UC304[UC-304: Bandeau Réserve DEC-AET-07 Option B]
    UC302 -->|Signature Falsifiée ou Clé Révoquée| UC305[UC-305: Blocage Hermétique Anti-Tamper]
    
    UC303 --> UC306[UC-306: Sanctuaire Acoustique & Ducking -14dB]
    UC304 --> UC306
    
    UC306 --> UC307[UC-307: Volontés Civiles & Funéraires DEC-AET-05]
    UC306 --> UC308[UC-308: Alerte Médicale Pacemaker Art. L1232-17]
    UC306 --> UC309[UC-309: Statut Don d Organes Loi 1986]
    UC306 --> UC310[UC-310: Directives Legs du Corps sous 48h]
    UC306 --> UC311[UC-311: Droit Acces Dossier Medical Loi 2002]
    UC306 --> UC312[UC-312: Modèle Pérennité & Coffre Étendu]
```

### Matrice des 12 Cas d'Usage de l'Application 3

| Code | Titre du Cas d'Usage | Déclencheur & Préconditions | Flux d'Écrans & Interaction | Postcondition & Sécurité |
| :--- | :--- | :--- | :--- | :--- |
| **UC-301** | **Scan NFC Instantané Sans Login** | Approche du téléphone à $\le 2\text{ cm}$ d'une carte mémorielle ACOSJ 92k | Apparition du radar pulse or (`wf-radar-pulse`), lecture APDU des Elementary Files en $\le 650\text{ ms}$ | Contexte de données transféré en mémoire vive éphémère |
| **UC-302** | **Vérification Crypto Hybride Ed25519/ES256** | Données CBOR ingérées, présence d'une enveloppe `COSE_Sign1` | Évaluation de l'en-tête protégé (`alg: -8` ou `alg: -7`), vérification par rapport à la TrustList locale | Décision souveraine `DEC-AET-04` respectée, verdict crypto scellé |
| **UC-303** | **Sanctuaire Certifié en Recueillement Nominal** | Verdict crypto 100% conforme et émetteur certifié | Ouverture en rideau doré, portrait Ken Burns 120 Hz, flamme mémorielle et badge émeraude | Sanctuaire prêt pour l'hommage, zéro friction |
| **UC-304** | **Bandeau de Réserve DEC-AET-07 Option B** | Signature intègre mais `kid` d'autorité non répertorié | Maintien de l'accès aux souvenirs de l'être cher ; bandeau ambré supérieur signalant l'autorité non certifiée | Confort émotionnel préservé selon l'arbitrage Kudoro |
| **UC-305** | **Blocage Hermétique Carte Falsifiée ou Clé Révoquée** | Non-concordance de la signature ou autorité révoquée | Écran noir d'obsidienne avec bouclier rouge écarlate et message de sécurité anti-fraude | Interdiction catégorique de lecture des données privées |
| **UC-306** | **Sanctuaire Acoustique & Ducking Vocal Vivant** | Déclenchement de la voix du souvenir par l'utilisateur | Baisse automatique du fond musical de $-14\text{ dB}$, oscillation de l'onde sonore or impérial | Écoute intime et pure du mémo vocal de l'être cher |
| **UC-307** | **Consultation des Volontés Civiles et Funéraires** | Sélection de l'onglet civisme ou demande des proches | Affichage en lecture seule certifiée des volontés funéraires (choix sarcomusation mémorielle DEC-AET-05) | Respect inaltérable de la volonté du défunt |
| **UC-308** | **Alerte Médicale d'Urgence : Pacemaker / DAE** | Présence d'un dispositif cardiaque implanté actif | Avertissement d'urgence haute visibilité clignotant rouge/ambre citant l'Art. L1232-17 du CDLD wallon | Alerte crémation immédiate avant mise en bière |
| **UC-309** | **Consultation du Statut de Don d'Organes** | Accès par les autorités médicales ou proches | Affichage du consentement présumé (Loi belge du 13 juin 1986) ou de l'opposition formelle expresse | Sauvegarde des greffes d'organes en temps critique |
| **UC-310** | **Directives Legs du Corps à la Science sous 48h** | Clause de don du corps encodée dans la carte | Affichage du décompte d'urgence 48h et des coordonnées de la faculté de médecine désignée | Notification immédiate des pompes funèbres agréées |
| **UC-311** | **Droit d'Accès Post-Mortem Dossier Médical** | Demande d'un ayant-droit avec lien de filiation | Consultation des clauses d'autorisation selon l'Art. 9 §4 de la Loi du 22 août 2002 | Clarté juridique évitant tout litige successoral |
| **UC-312** | **Pérennité Séculaire & Coffre Étendu** | Expiration des 3 ans offerts ou demande de dotation | Proposition discrète de renouvellement mémoriel annuel (4,40 €/an) sans aucune interruption locale | Sauvegarde perpétuelle de l'archive familiale |

---

## 3. Matrice de Traitement des Incidents & Bienveillance UX

En situation de deuil, chaque message d'erreur maladroit est une blessure. L'Application 3 applique des principes d'amortissement émotionnel stricts :

1. **Rupture de Champ NFC Prématurée (`ERR_NFC_TIMEOUT`)** :
   - *Message affiché* : *"La lecture a été interrompue. Veuillez reposer doucement votre téléphone contre le médaillon pendant deux secondes."*
   - *Graphisme* : Animation d'onde ralentie, sans signal d'échec agressif ni sonnerie d'erreur stridente.
2. **Tag Inconnu ou Non Initialisé (`ERR_UNPROVISIONED_CARD`)** :
   - *Message affiché* : *"Cette carte mémorielle n'a pas encore été consacrée. Rapprochez-vous de votre conseiller Le Pax Funèbre pour son initialisation."*
3. **Application de DEC-AET-07 Option B (Avertissement Ambré)** :
   ```html
   <div class="wf-alert-card wf-alert-amber">
     <strong>Hommage Mémoriel Accessible (Réserve d'Autorité DEC-AET-07)</strong>
     <p>La signature numérique de cette carte est intègre, mais l'établissement émetteur n'est pas répertorié dans la liste officielle. Par égard pour la mémoire du défunt, l'accès au sanctuaire est maintenu.</p>
   </div>
   ```

---

## 4. Architecture Graphique & Ergonomie Aînés

1. **Design System Obsidienne & Or Impérial** :
   - Conforme à `scripts/portal_styles.py` : surfaces sombres feutrées (`#06070b` et `#0b0d14`), dorures d'accent (`#d4af37`), absence totale de blanc pur agressif (remplacé par `--slate-200: #e2e8f0`).
2. **Accessibilité Motrice & Visuelle** :
   - Cibles tactiles calibrées à $56 \times 56\text{ dp}$ minimum (bouton de lecture vocale, flamme mémorielle, retour).
   - Mode fort contraste automatique si activé sur l'OS, avec bordures or rehaussées à 80% d'opacité.
   - Lecture vocale par synthèse vocale locale intégrée pour les personnes malvoyantes.

---

## 5. Exigences Spec-First & Test-First

1. **Spécification détaillée des flux dans `docs/functional/ux-sanctuaire-b2c.md`** :
   - Diagrammes d'états formels pour chaque parcours de recueillement.
   - Journalisation des délais de lecture APDU in-situ sur Pixel 9 et iPhone 15/16.
2. **Jeux de tests d'accessibilité dans `qa/vectors/ux/b2c/`** :
   - Tests automatisés TalkBack et VoiceOver vérifiant que chaque élément interactif dispose d'un label d'accessibilité solennel.
   - Audit colorimétrique automatique certifiant un contraste minimal de 7:1 sur les textes d'hommage.

---

## 6. Protocole de Communication Mailbox

- **Demandes d'évolution** dans `mailbox/to-antigravity/` (`NNNN-task-uxb2c-*.md`).
- **Rapports d'essais utilisateurs et accessibilité** dans `mailbox/to-claude/` (`NNNN-report-uxb2c-*.md`).
- **Liaisons directes** :
  - Bushi 06 (Acoustic) : Calibrage du ducking audio à $-14\text{ dB}$.
  - Bushi 07 (Cinematic) : Intégration du Ken Burns et du lecteur 4 phases.
  - Bushi 02 (Crypto) : Validation des signatures Ed25519/ES256 et gestion de DEC-AET-07.

---

## 7. Critères de Conformité Stricts

- [ ] **Mode 100% Hors-Ligne Absolu** : Aucun appel réseau n'est effectué pour afficher le sanctuaire, lire la voix ou consulter les volontés civiles. Tout est extrait du silicium local.
- [ ] **Zéro Login & Zéro Friction** : Aucun écran de bienvenue promotionnel, aucun recueil de consentement publicitaire (zéro traqueur), affichage direct en $\le 800\text{ ms}$ post-tap.
- [ ] **Respect Rigoureux de DEC-AET-07 Option B** : Interdiction absolue de bloquer l'affichage du sanctuaire en écran noir si l'émetteur est simplement non répertorié ; seul le bandeau de réserve ambré doit être injecté.
- [ ] **Blocage Intransigeant sur Fraude** : En cas de falsification de signature ou de certificat révoqué, l'accès aux données doit être immédiatement et hermétiquement verrouillé.
- [ ] **Conformité Légale Funéraire** : Affichage prioritaire des alertes d'exérèse pacemaker (Art. L1232-17 CDLD) et des volontés d'organes/legs.
