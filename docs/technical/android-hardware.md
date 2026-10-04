# Spécification Technique : Pilote Android Hardware, Passerelle Web NFC & Silicium JavaCard ACOSJ 92 Ko

> **Auteurs** : Bushi 03 (Lead Android Hardware & NFC) & Bushi 10 (Silicon Storage)  
> **Date** : 2026-10-05  
> **Statut** : Validé pour Ingénierie & Soumis à l'Arbitrage Kudoro  
> **Conformité** : `DEC-AET-01` (ACOSJ 92 Ko exclusif), `DEC-AET-04` (Agilité COSE ES256/Ed25519), `DEC-AET-07` (Consultation sous réserve), `DEC-AET-08` (4 Apps), `DEC-AET-09` (Universalité multi-plateformes)

---

## 1. Synthèse Exécutive : La Vision Stratégique Kudoro

Kudoro a posé une interrogation stratégique déterminante :  
*« L'utilisation d'une WebApp (Web NFC) : Si l'utilisateur a déjà ouvert un site internet spécifique sur son navigateur (Google Chrome sur Android uniquement), ce site peut utiliser l'API Web NFC pour lire le contenu textuel ou HTML brut de la carte et l'injecter dynamiquement dans la page ouverte. Est-ce révolutionnaire ? »*

### Le Verdict Technique Conjoint Bushi 03 / Bushi 10
**Oui, cette approche est une percée majeure pour l'expérience utilisateur funéraire (B2C), mais elle exigeait de résoudre une contradiction physique fondamentale entre la carte et le navigateur web.**

1. **La Friction Majeure Éliminée** :  
   Lors d'une cérémonie funéraire ou d'un hommage au cimetière, exiger d'une famille ou de personnes âgées qu'elles téléchargent une application de 50 Mo sur le Google Play Store, acceptent des conditions générales et s'authentifient avec un mot de passe constitue un obstacle critique à l'émotion.  
   Grâce à **Web NFC** sur Google Chrome Android, un simple effleurement de la carte ouvre le Sanctuaire directement dans le navigateur, extrait le profil certifié scellé dans la puce et affiche l'hommage en moins de 100 millisecondes. **Zéro application à installer, zéro compte, zéro friction.**

2. **Le Défi Silicium Résolu (La Passerelle Hybride Dual-Applet)** :  
   L'API Web NFC du W3C ne sait **pas** envoyer d'APDU ISO 7816-4 bruts ni communiquer avec une applet propriétaire IsoDep (`A00000084501`). Si la carte JavaCard ACOSJ 92 Ko n'était configurée qu'avec son applet propriétaire, Chrome Android renverrait une erreur systématique.  
   **La solution souveraine conçue par Bushi 03 et Bushi 10 consiste en une architecture silicium hybride Dual-Applet sur ACOSJ 92 Ko** :
   - Une **Applet Standard NFC Forum Type 4 Tag (AID `D2760000850101`)**, lisible universellement par Web NFC dans Chrome sans aucune application.
   - Une **Applet Sécurisée AeterniTrak IsoDep (AID `A00000084501`)**, accessible par l'application native Android et les stations professionnelles PaxStation pour les opérations cryptographiques avancées (scellement par fusible `80 DE`, signature in-silico ES256, lecture Extended APDU des 92 Ko).
   - Les deux applets partagent la même EEPROM physique sans duplication de mémoire via une interface partagée (`Shareable Interface Object`).

---

## 2. Analyse Approfondie de l'API Web NFC W3C (`NDEFReader`, `NDEFWriter`)

### 2.1 Écosystème & Compatibilité Matérielle
L'API Web NFC est normalisée par le W3C / WICG (*Web NFC Community Group Report*).
- **Navigateurs Compatibles** : Google Chrome pour Android (depuis Chromium 89, mars 2021), Edge Android, Samsung Internet (v15+), Opera Android.
- **Plateformes Exclues** :
  - **Apple iOS / Safari** : Refus catégorique et permanent de WebKit d'implémenter Web NFC pour des motifs de sécurité matérielle et de confinement de l'App Store. Sur iPhone, la lecture NFC de la carte exige l'application native iOS (Bushi 04 / CoreNFC) ou le tap système redirigeant vers Safari.
  - **Navigateurs Desktop (macOS / Windows / Linux)** : Web NFC n'est pas supporté. Sur ordinateur de bureau, la liaison avec le lecteur sans contact ACR1552U s'opère via **WebUSB / WebHID** (Bushi 05).

### 2.2 Prérequis Techniques et Règles de Sécurité W3C
Pour que l'appel `new NDEFReader().scan()` fonctionne, le navigateur Android impose six verrous stricts :

1. **Contexte Cryptographique Sécurisé (Secure Context)** :  
   `window.isSecureContext === true`. L'application WebApp Sanctuaire doit obligatoirement être servie via **HTTPS** avec un certificat TLS valide (ou `localhost` en développement).
2. **Geste Utilisateur Préalable (User Activation)** :  
   L'initialisation de `ndef.scan()` doit obligatoirement résulter d'un événement utilisateur direct (`click`, `touchend`). Tout appel automatique au chargement (`window.onload`) est bloqué par le navigateur avec l'exception `NotAllowedError`.
3. **Contrôle de Permission Système (`navigator.permissions`)** :  
   Le navigateur sollicite la permission NFC (`name: 'nfc'`). Une invite native Android s'affiche lors de la première interaction : *« sanctuaire.paxfunebre.be souhaite accéder à votre lecteur NFC »*.
4. **État Matériel & Écran Allumé** :  
   L'appareil Android doit avoir sa puce NFC active dans les paramètres du système d'exploitation. L'écran doit impérativement être **allumé et déverrouillé**.
5. **Visibilité de la Page (Page Visibility API)** :  
   L'écoute NFC est active uniquement lorsque le document est au premier plan (`document.visibilityState === 'visible'`). Si la famille verrouille l'écran ou change d'onglet, l'écoute est suspendue et reprend automatiquement au retour sur l'onglet.
6. **Politique d'Autorisation (Permissions-Policy)** :  
   Si le composant est encapsulé dans une `<iframe>`, la balise parente doit déclarer `allow="nfc"`.

### 2.3 Capacités NDEF de l'API
Web NFC opère exclusivement au niveau des messages NDEF (*NFC Data Exchange Format*) :
- Détection d'un événement `reading` contenant un objet `NDEFMessage`.
- Accès à l'UID matériel de la puce : `event.serialNumber` (ex: `"04:5a:32:8f:1c:7b:80"`).
- Typage fin des enregistrements (`NDEFRecord`) :
  - `recordType: "text"` : Texte UTF-8/UTF-16 avec code langue.
  - `recordType: "url"` : URL absolue.
  - `recordType: "mime"` : **Le pilier technique AeterniTrak**.
    - Type MIME personnalisé : `"application/aeternitrak-profile+cbor"` (ou repli `"application/octet-stream"`).
    - Accès binaire direct : la propriété `record.data` est une instance de `DataView`.
    - Conversion directe sans encodage intermédiaire :
      ```javascript
      const rawBytes = new Uint8Array(record.data.buffer, record.data.byteOffset, record.data.byteLength);
      ```
    - Ces octets constituent exactement l'enveloppe binaire `COSE_Sign1` (Bloc 1 du Sanctuaire).

### 2.4 Limites Infranchissables de Web NFC
Ce que Web NFC ne peut physiquement **pas** faire en raison de son abstraction de haut niveau :
- **Aucun envoi d'APDU ISO/IEC 7816-4** :  
  Aucune méthode `transceive()` n'est exposée. Impossible d'envoyer `SELECT AID`, `VERIFY PIN`, ou les commandes de calcul de signature on-chip.
- **Incompatibilité avec les puces JavaCard non-NDEF** :  
  Une carte JavaCard sans applet d'émulation NFC Forum Type 4 Tag est invisible pour Chrome Android.
- **Volume unitaire restreint (Budget de transmission RF)** :  
  Bien que la spécification Type 4 Tag supporte des fichiers jusqu'à 32 Ko, le contrôleur NFC Android est optimisé pour des charges NDEF rapides (< 4 Ko). Tenter de transférer 92 Ko d'un seul bloc via NDEF dans une page web entraînerait un risque inacceptable de rupture radiofréquence lors d'un léger tremblement de la main de la famille.
- **Absence de Mode Silencieux** :  
  En natif Android, Bushi 03 active `FLAG_READER_NO_PLATFORM_SOUNDS` pour supprimer le bip sonore strident d'Android. En Web NFC, Chrome émet le son système Android par défaut.

---

## 3. La Passerelle Silicium Hybride : Émulation NDEF Type 4 Tag sur ACOSJ 92 Ko

En application de la directive souveraine de Kudoro `DEC-AET-01` (*« QUE DES CARTES 92Ko »*), l'architecture repose exclusivement sur la puce JavaCard **ACOSJ 92 Ko** (ACS Technologies, microcontrôleur sécurisé Common Criteria EAL5+).

### 3.1 Architecture Silicium Dual-Applet (Coopération In-Silico)
Pour marier l'inviolabilité cryptographique funéraire et la lecture web instantanée, la puce ACOSJ 92 Ko embarque deux applets Java Card coopératives :

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CARTE JAVACARD ACOSJ 92 Ko (EEPROM 92 160 octets)         │
├──────────────────────────────────────┬──────────────────────────────────────┤
│  APPLET 1 : AeterniTrak IsoDep       │  APPLET 2 : NFC Forum Type 4 Tag     │
│  AID: A0 00 00 08 45 01              │  AID: D2 76 00 00 85 01 01           │
│  (Mode B2B / Station / App Native)   │  (Mode B2C Famille / Web NFC Chrome) │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ • APDUs Propriétaires ISO 7816-4     │ • Fichier Capability Container (CC)  │
│ • Génération Bi-clé ES256 (-7)       │   EF E103 (15 octets fixes)          │
│ • Scellement Fusible 80 DE 01 00     │ • Fichier NDEF EF E104               │
│ • Extended APDU (Jusqu'à 64 Ko/trame)│   (Miroir mémoire du Bloc 1 mémoriel)│
│ • Accès Blocs 0, 1, 2, 3, 4          │ • Lecture seule stricte après scel   │
├──────────────────────────────────────┴──────────────────────────────────────┤
│                ESPACE PHYSIQUE EEPROM UNIQUE (Zéro Duplication)             │
│  ┌───────────────┬───────────────────────────┬──────────────┬─────────────┐ │
│  │ Bloc 0 (512 o)│ Bloc 1 : COSE_Sign1 (2 Ko)│ Bloc 2 (20Ko)│ Bloc 3 (45Ko│ │
│  │ Méta / Clés   │ Profil Civil / Hashs SHA  │ Portrait WebP│ Audio SILK  │ │
│  └───────────────┴─────────────┬─────────────┴──────────────┴─────────────┘ │
│                                │ Pointeur Partagé SIO                       │
│                                └─────────────────────────┐                  │
│                                                          ▼                  │
│                             Fichier NDEF (EF E104) : [NLEN 2o] + [COSE 2Ko] │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Spécification des Fichiers NFC Forum Type 4 Tag (Applet 2)

#### Fichier Capability Container (CC File - EF `E103`)
Taille fixe de 15 octets exposant la configuration du transpondeur :
- **CCLEN** (`00 0F`) : Longueur totale de 15 octets.
- **Mapping Version** (`20`) : Version 2.0 de la spécification NFC Forum Type 4 Tag.
- **MLe** (`7F FF` ou `00 FF`) : Taille maximale d'une réponse R-APDU (32 767 octets en Extended APDU, ou 255 octets en standard).
- **MLc** (`7F FF` ou `00 FF`) : Taille maximale d'une commande C-APDU.
- **NDEF File Control TLV** :
  - `Tag = 04` (Enregistrement de contrôle de fichier NDEF).
  - `Length = 06` (6 octets de paramètres).
  - `File Identifier = E1 04` (Identifiant du fichier NDEF hébergeant le message).
  - `Max NDEF Size = 08 00` (2 048 octets alloués pour le Bloc 1 du Sanctuaire).
  - `Read Access = 00` (Lecture libre sans mot de passe : accès universel sans login).
  - `Write Access = FF` (Écriture verrouillée / interdite après scellement funéraire).

#### Structure du Fichier NDEF (EF `E104`)
Le fichier NDEF est constitué des deux premiers octets de longueur `NLEN` (Big-Endian), suivis du message NDEF standard :
1. **Octets 0..1 (`NLEN`)** : Longueur exacte du message NDEF (ex: `0x03 0x82` pour 898 octets).
2. **Record 1 : Record MIME Profil Mémoriel (`application/aeternitrak-profile+cbor`)** :
   - Header NDEF : `MB=1, ME=1, CF=0, SR=1, IL=0, TNF=0x02` (MIME Media Type).
   - Type Length : `0x24` (36 octets).
   - Type String : `"application/aeternitrak-profile+cbor"`.
   - Payload : L'enveloppe binaire `COSE_Sign1` complète (≤ 2 048 octets), comprenant :
     - En-tête protégé : Algorithme `alg: -7` (ES256) ou `alg: -8` (Ed25519) + Type de contenu `typ: 16`.
     - Identifiant de clé : `kid` (empreinte de l'émetteur funéraire).
     - Charge utile CBOR : Données civiles du défunt, épitaphe, pays ISO, dates Tag 100, et empreintes SHA-256 du portrait (Bloc 2) et du mémo vocal (Bloc 3).
     - Signature cryptographique matérielle de 64 octets.

### 3.3 Cycle de Vie Transactionnel : Du Scellement B2B à la Consultation B2C

```
[ÉTAPE 1 : Agence Funéraire / PaxStation (Applet A00000084501)]
  │ 1. Écriture des Blocs 0, 1, 2, 3, 4 via APDU ISO 7816-4
  │ 2. Calcul de la signature matérielle ES256 on-chip
  │ 3. Commande de scellement irréversible : APDU 80 DE 01 00 (Fusible)
  │    └── Action in-silico :
  │        • Le COMMIT_FLAG passe à 0x01 (Permanent)
  │        • L'Applet Type 4 Tag est activée
  │        • Le fichier EF E104 pointe sur le Bloc 1
  │        • Write Access passe définitivement à 0xFF (Lecture seule)
  ▼
[ÉTAPE 2 : Famille en Recueillement / Google Chrome Android]
  │ 1. Ouverture de https://sanctuaire.paxfunebre.be
  │ 2. Appui sur le bouton "Recueillement sans contact"
  │ 3. Effleurement de la carte ACOSJ 92 Ko contre le dos du smartphone
  │    └── Action radiofréquence :
  │        • Le contrôleur NFC Android envoie SELECT AID D2760000850101
  │        • L'Applet Type 4 Tag répond 0x9000
  │        • Android lit le CC File E103 puis le NDEF File E104
  │        • Chrome transmet le record MIME à la page web
  ▼
[ÉTAPE 3 : Validation Cryptographique Locale dans Chrome]
  │ 1. Extraction du Uint8Array depuis record.data
  │ 2. Exécution de coseOpen() (AeterniCore)
  │ 3. Vérification de la signature ECDSA P-256 via Web Crypto API
  │ 4. Décodage CBOR et affichage instantané de l'hommage
```

---

## 4. Spécification APDU Formelle ISO/IEC 7816-4 (Applet AeterniTrak IsoDep)

### 4.1 Table Normative des Commandes APDU
Les commandes suivantes sont utilisées par l'application native Android (Bushi 03) et le lecteur de bureau WebUSB ACR1552U (Bushi 05) pour dialoguer avec l'Applet propriétaire AeterniTrak :

| Commande | CLA | INS | P1 | P2 | Lc | Data Payload | Le | Description Métier |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :---: | :--- |
| **SELECT AID** | `00` | `A4` | `04` | `00` | `06` | `A0 00 00 08 45 01` | `00` | Sélectionne l'Applet Mémorielle Souveraine |
| **SELECT AID T4T** | `00` | `A4` | `04` | `00` | `07` | `D2 76 00 00 85 01 01` | `00` | Sélectionne l'Applet Standard NFC Forum Type 4 Tag |
| **SELECT FILE CC** | `00` | `A4` | `00` | `0C` | `02` | `E1 03` | — | Sélectionne le fichier Capability Container |
| **SELECT FILE NDEF**| `00` | `A4` | `00` | `0C` | `02` | `E1 04` | — | Sélectionne le fichier NDEF mémoriel |
| **READ BINARY** | `00` | `B0` | `Offset High` | `Offset Low` | — | Aucun | `00` / `Le` | Lit jusqu'à 255 octets (Standard) ou 64 Ko (Extended) |
| **UPDATE BINARY** | `00` | `D6` | `Offset High` | `Offset Low` | `Lc` | Octets bruts | — | Écrit une tranche dans le bloc spécifié (si non scellé) |
| **GET CHALLENGE** | `00` | `84` | `00` | `00` | — | Aucun | `10` | Obtient 16 octets d'aléa pour l'authentification mutuelle |
| **INTERNAL AUTH** | `00` | `88` | `00` | `00` | `20` | Hash SHA-256 (32 octets) | `40` | Signe in-silico en ES256 (génère 64 octets $r \parallel s$) |
| **FUSE SEAL** | `80` | `DE` | `01` | `00` | `00` | Aucun | — | **Scellement Définitif Irréversible** : grille le fusible logique |

### 4.2 Codes d'État Normalisés (Status Words SW1-SW2)

| SW1-SW2 | Désignation Normative | Traduction Système | Directive d'Empathie UI Famille (Éléonore) |
| :---: | :--- | :--- | :--- |
| `0x9000` | `SW_NO_ERROR` | Succès de l'opération | *Affichage serein de l'hommage.* |
| `0x6A82` | `SW_FILE_NOT_FOUND` | Fichier ou Applet introuvable | *« La carte présentée n'est pas reconnue. »* |
| `0x6B00` | `SW_WRONG_OFFSET` | Offset d'adressage hors limites | *« Le contact avec la mémoire a été interrompu. »* |
| `0x6700` | `SW_WRONG_LENGTH` | Longueur $L_c$ ou $L_e$ invalide | *« Données incomplètes. Posez à nouveau la carte. »* |
| `0x6982` | `SW_SECURITY_STATUS_NOT_SATISFIED` | Fusible déjà grillé / Écriture interdite | *« Cette mémoire est scellée pour l'éternité. »* |
| `0x6282` | `SW_EOF_REACHED` | Fin de fichier prématurée atteinte | *« Lecture achevée avec succès. »* |

---

## 5. Budget Mémoire Silicium ACOSJ 92 Ko (Bushi 10 & Bushi 03)

Sur la capacité brute de **92 160 octets**, le partitionnement physique est calculé au bit près afin de garantir la longévité de l'EEPROM et le respect de la marge de sécurité matérielle de 5% :

```
Capacité Silicium ACOSJ : 92 160 octets (100 %)
├── Bloc 0 : Métadonnées carte, version protocole, clés publiques  ───>     512 o   (0.55 %)
├── Bloc 1 : Dossier d'identité canonique CBOR / COSE_Sign1 (T4T) ───>   2 048 o   (2.22 %)  <-- EXPOSÉ WEB NFC
├── Bloc 2 : Portrait visuel optimisé WebP (480x480) ───────────────>  20 480 o  (22.22 %)
├── Bloc 3 : Mémo vocal éternel Opus SILK (16 kHz, ~20 s) ──────────>  46 080 o  (50.00 %)
├── Bloc 4 : Registre des hommages de famille & traçabilité ─────────>  15 360 o  (16.67 %)
└── Réserve d'Usure EEPROM (Wear-Leveling & Sécurité 8.3%) ─────────>   7 680 o   (8.33 %)  (> 4 600 o requis)
```

**Observation Fiscale du Bushi 10** :  
L'exposition NDEF Type 4 Tag ne consomme **aucun octet additionnel**. Le fichier NDEF pointe physiquement sur la plage mémoire du **Bloc 1** via le système de fichiers JavaCard. Le message NDEF est scellé en lecture seule dès confirmation du `COMMIT_FLAG`.

---

## 6. Démonstrateur Client Vanilla JS : Intégration Sanctuaire Web NFC

Voici le snippet standard d'implémentation client, zéro dépendance superflue, exécutable dans Google Chrome sur Android au sein de l'application Sanctuaire B2C :

```javascript
/**
 * AeterniTrak V1.0 — Démonstrateur Sanctuaire Web NFC (Vanilla JS)
 * Conforme : W3C Web NFC API, DEC-AET-01 (ACOSJ 92k), DEC-AET-07 (Option B)
 */

import { coseOpen } from './core/cose/open.ts';
import { validateProfile } from './core/profile/validator.ts';
import { decodeToCborValue } from './core/cbor/decoder.ts';

// Registre de confiance scellé (KID -> Clé publique ES256 / Ed25519)
const TRUST_STORE = {
  // Clés des opérateurs funéraires assermentés PaxFunèbre
  "urn:paxfunebre:operator:belgium-liege-01": {
    crv: "P-256",
    x: new Uint8Array([/* 32 octets coordonnée X */]),
    y: new Uint8Array([/* 32 octets coordonnée Y */]),
    revoked: false
  }
};

/**
 * Lance la session de scan Web NFC avec retour haptique et gestion des erreurs.
 * @param {HTMLElement} uiContainer - Élément DOM où afficher le sanctuaire.
 */
export async function startSanctuaryNfcSession(uiContainer) {
  // 1. Contrôle de compatibilité matérielle et navigateur
  if (!('NDEFReader' in window)) {
    renderFallbackUI(uiContainer, "Web NFC non supporté sur ce navigateur. Veuillez utiliser Google Chrome sur Android ou télécharger l'application Sanctuaire.");
    return;
  }

  try {
    const ndef = new NDEFReader();
    
    // Déclenchement du scan (requiert un contexte HTTPS et un geste utilisateur préalable)
    await ndef.scan();
    
    updateScanStatus(uiContainer, "En attente du mémorial... Approchez délicatement la carte de l'antenne.");

    // 2. Écoute de l'événement de détection RF
    ndef.onreading = async (event) => {
      // Retour haptique doux si supporté par le matériel
      if (navigator.vibrate) {
        navigator.vibrate(40); // Vibration subtile de 40 ms
      }

      console.log(`[AeterniTrak NFC] Carte détectée. UID: ${event.serialNumber}`);
      
      const message = event.message;
      let cborEnvelopeBytes = null;

      // 3. Recherche du payload MIME AeterniTrak
      for (const record of message.records) {
        if (
          record.recordType === "mime" &&
          (record.mediaType === "application/aeternitrak-profile+cbor" ||
           record.mediaType === "application/octet-stream")
        ) {
          // Extraction binaire directe depuis le DataView
          cborEnvelopeBytes = new Uint8Array(
            record.data.buffer,
            record.data.byteOffset,
            record.data.byteLength
          );
          break;
        }
      }

      if (!cborEnvelopeBytes) {
        displayGracefulMessage(uiContainer, "Carte reconnue, mais aucun hommage mémoriel n'y est gravé.");
        return;
      }

      // 4. Traitement Cryptographique et Décodage In-Silico
      try {
        updateScanStatus(uiContainer, "Lecture de la mémoire éternelle...");

        // Ouverture de l'enveloppe COSE_Sign1 selon le modèle DEC-AET-07 Option B
        const openResult = await coseOpen(cborEnvelopeBytes, "application/aeternitrak-profile+cbor", TRUST_STORE);

        if (openResult.status === "BLOCKED") {
          displaySecurityAlert(uiContainer, "Scellé d'authenticité corrompu ou signature invalide. Accès refusé.");
          return;
        }

        // Validation structurelle et sémantique du profil CBOR
        validateProfile(openResult.payload);
        const profile = decodeToCborValue(openResult.payload);

        // 5. Affichage solennel du Sanctuaire
        renderSanctuary(uiContainer, profile, openResult.status === "UNVERIFIED");

      } catch (cryptoErr) {
        console.error("[AeterniTrak Crypto]", cryptoErr);
        displayGracefulMessage(uiContainer, "Le souvenir s'est estompé lors du décodage. Posez à nouveau la carte.");
      }
    };

    // Gestion des incidents de rupture radiofréquence
    ndef.onreadingerror = () => {
      displayGracefulMessage(uiContainer, "Le contact s'est estompé. Posez à nouveau délicatement le souvenir.");
    };

  } catch (err) {
    handleNfcError(err, uiContainer);
  }
}

/**
 * Gestionnaire d'erreurs respectant la dignité du deuil et les codes W3C.
 */
function handleNfcError(err, container) {
  console.warn("[Web NFC Status]", err.name, err.message);

  switch (err.name) {
    case 'NotAllowedError':
      displayGracefulMessage(container, "L'accès au lecteur sans contact a été refusé. Veuillez autoriser le NFC dans les paramètres.");
      break;
    case 'NotFoundError':
      displayGracefulMessage(container, "Aucun lecteur sans contact actif détecté sur cet appareil.");
      break;
    case 'NotSupportedError':
      displayGracefulMessage(container, "Cette opération requiert une connexion sécurisée (HTTPS).");
      break;
    case 'AbortError':
      displayGracefulMessage(container, "La lecture a été suspendue.");
      break;
    default:
      displayGracefulMessage(container, "Le contact s'est estompé. Posez à nouveau délicatement le souvenir.");
      break;
  }
}

function updateScanStatus(container, msg) {
  container.innerHTML = `<div class="aeterni-scanning"><div class="pulse-ring"></div><p>${msg}</p></div>`;
}

function displayGracefulMessage(container, msg) {
  container.innerHTML = `<div class="aeterni-graceful-msg"><p class="solemn-text">${msg}</p></div>`;
}

function displaySecurityAlert(container, msg) {
  container.innerHTML = `<div class="aeterni-alert"><p class="alert-text">${msg}</p></div>`;
}

function renderSanctuary(container, profileData, isUnverified) {
  // Rendu solennel du Sanctuaire mémoriel
  container.innerHTML = `
    <article class="sanctuary-memorial">
      ${isUnverified ? '<div class="memorial-warning">Authenticité en cours de validation par le Pax Funèbre</div>' : ''}
      <header class="memorial-header">
        <h1 class="subject-name">${profileData.usage_name || "Âme Chérie"}</h1>
        <p class="dates">${profileData.birth_date || ""} — ${profileData.death_date || ""}</p>
      </header>
      <blockquote class="epitaph">${profileData.epitaph || ""}</blockquote>
      <div class="memorial-seal">Scellé au Silicium • AeterniTrak ACOSJ 92 Ko</div>
    </article>
  `;
}
```

---

## 7. Matrice Stratégique : Web NFC (Chrome Android) vs Application Native (Android/iOS)

| Critère d'Évaluation | Web NFC (Google Chrome Android) | Application Native (Bushi 03 & 04) |
| :--- | :--- | :--- |
| **Parcours Utilisateur** | **Zéro Clic / Zéro Installation** (Instantané) | Téléchargement Store (50 Mo), installation requise |
| **Plateformes Compatibles** | Android uniquement (Chrome, Edge, Samsung) | **Toutes plateformes** (iOS CoreNFC, Android IsoDep) |
| **Volume de Données Accessible** | **Bloc 1 uniquement (≤ 2 Ko)** via Type 4 Tag | **Intégralité des 92 Ko in-silico** (WebP 20Ko, SILK 45Ko) |
| **Commandes APDU de Bas Niveau** | **Impossible** (Abstraction NDEF stricte) | **Pleine puissance ISO 7816-4** (Extended Length) |
| **Scellement & Fusible Matériel** | Impossible (Lecture seule) | Commande fusible `80 DE 01 00` exécutable |
| **Calcul Cryptographique On-Chip** | Impossible | Commande `INTERNAL AUTHENTICATE` disponible |
| **Haptique & Contrôle Sonore** | Bip Android système imposé | **Silence solennel absolu** (`SKIP_SOUNDS`) + haptique Pixel 9 |
| **Fonctionnement Hors-Ligne** | Possible via Service Worker / PWA en cache | **100% autonome hors-ligne garanti** sans aucun réseau |

---

## 8. Recommandations Décisionnelles pour Kudoro

1. **Valider l'Architecture Silicium Hybride Dual-Applet sur ACOSJ 92 Ko** :  
   Cette conception respecte rigoureusement la décision `DEC-AET-01` (*« QUE DES CARTES 92Ko »*) tout en débloquant l'accès instantané Web NFC pour des millions d'utilisateurs Android sans rien sacrifier à l'inviolabilité de la puce.
2. **Adopter le Double Parcours B2C dans le Sanctuaire** :
   - **Parcours Découverte Éphémère (Web NFC)** : La famille ou les proches effleurent la carte avec Chrome Android lors de la cérémonie. Le profil civil et l'épitaphe s'affichent immédiatement.
   - **Parcours Sanctuaire Perpétuel (App Mobile)** : Pour écouter le mémo vocal de 45 Ko et contempler les portraits haute résolution gravés dans les blocs 2 et 3 sans dépendre d'Internet, l'application mobile native prend le relais.
3. **Pérenniser la Spécification Type 4 Tag dans le Masque de Production ACOSJ** :  
   Intégrer les fichiers CC (`E103`) et NDEF (`E104`) dans les scripts d'initialisation GlobalPlatform (`scripts/init_acosj_92k.gp`) des puces commandées chez ACS.
