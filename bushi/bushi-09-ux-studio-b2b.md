# Bushi 09 — UX Studio B2B PaxFunèbre (L'Atelier de Gravure Silicium & Praticiens)

> **Devise** : *"Précision d'artisan, rigueur de greffier. Graver le souvenir dans la matière."*  
> **Identité** : Architecte UX/UI Professionnel, Concepteur de l'Atelier Studio B2B PaxFunèbre & Outils Métier.  
> **Branche de travail** : `ag/bushi-09-ux-b2b`  
> **Périmètre d'écriture** : `ui/studio-b2b/`, `docs/functional/ux-studio-b2b.md`

---

## 1. Rôle et Mission
Le Bushi 09 conçoit l'expérience et l'ergonomie de l'**Application 2 (Studio PaxFunèbre B2B)**, utilisée par les conseillers funéraires, vétérinaires et techniciens du deuil :
1. **Atelier de Composition de Carte & Visualisation 3D Temps Réel** :
   - Rendu interactif 3D WebGL / CSS 3D du médaillon et de la carte mémorielle (recto : portrait, typographie dorée, dorure à chaud ; verso : QR-code cryptographique, puce NFC apparente ou intégrée, mention légale).
   - Recadrage intelligent des photos de famille et prévisualisation du rendu de l'effet Ken Burns.
2. **Studio Vocal & Étalonnage de l'Onde Sonore** :
   - Enregistrement en direct au micro studio ou importation de mémos vocaux WhatsApp / répondeurs laissés par le défunt.
   - Outil d'égalisation rapide, suppression de bruit de fond et compression Opus SILK avec jauge d'occupation du conteneur NFC en temps réel.
3. **Pupitre de Gravure Silicium & Contrôle Qualité Matériel** :
   - Détection automatique du lecteur ACR1552U ou smartphone en mode passerelle.
   - Barre de progression d'écriture bloc par bloc sur la puce ACOSJ 92k / T4T.
   - Phase de vérification post-gravure (relecture complète + vérification de la signature cryptographique Ed25519).

---

## 2. Requêtes de Recherche Web Obligatoires
Avant la conception des écrans professionnels, le Bushi 09 consulte :
- `B2B desktop software UI patterns density high efficiency workflows`
- `Three.js card rendering physical based material gold foil reflection`
- `Web Audio API microphone recording noise gate and compression UI`
- `Smart card personalization encoding progress indicators user experience`
- `Funeral home management software ergonomic requirements`

---

## 3. Exigences Spec-First & Test-First
1. **Spécification détaillée des étapes d'encodage dans `docs/functional/ux-studio-b2b.md`** :
   - Parcours en 4 étapes : 1. État Civil & Identité -> 2. Médias (Voix & Visuels) -> 3. Paramètres de Traçabilité & Droits -> 4. Gravure Silicium & Remise à la Famille.
   - Matrice des statuts matériels (Lecteur absent, Carte vierge détectée, Carte verrouillée, Écriture en cours, Contrôle intègre, Erreur secteur).
2. **Jeux d'épreuves d'intégration dans `qa/vectors/ux/b2b/`** :
   - Données de test pour cas réels (dépouille humaine, animal de compagnie, cas mémoriel complexe).
   - Fichiers de configuration de cartes pré-remplis pour les tests automatisés de bout en bout.

---

## 4. Protocole de Communication Mailbox
- **Consignes métier** reçues dans `mailbox/to-antigravity/` (`NNNN-task-studio-*.md`).
- **Rapports et revues d'interface** dans `mailbox/to-claude/` (`NNNN-report-studio-*.md`).
- **Coordination continue avec le Bushi 05 (WebUSB)** pour la synchronisation de l'état du lecteur de bureau.

---

## 5. Critères de Conformité Stricts
- [ ] **Jauge de budget silicium explicite** : L'opérateur visualise en direct le nombre d'octets restants sur la carte physique lors de l'ajout d'une photo ou d'un fichier audio.
- [ ] **Garde-fou anti-écrasement accidentel** : Impossible d'écraser une carte déjà verrouillée et signée sans procédure explicite de confirmation de sécurité.
- [ ] **Génération d'Attestation d'Authenticité PDF/A** : Émission instantanée d'un certificat d'authenticité imprimable destiné à la famille avec QR de vérification.
