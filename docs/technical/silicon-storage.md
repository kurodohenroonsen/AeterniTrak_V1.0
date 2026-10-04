# Spécification Technique : Plan Mémoire Silicium ACOSJ 92 Ko, Partitionnement & Persistance Décentralisée

> **Auteurs** : Bushi 10 (Silicon Storage) & Bushi 03 (Lead Android Hardware & NFC)  
> **Date** : 2026-10-05  
> **Statut** : Validé pour Ingénierie & Soumis à l'Arbitrage Kudoro  
> **Conformité** : `DEC-AET-01` (ACOSJ 92 Ko exclusif, 92 160 octets), `DEC-AET-04` (Agilité COSE ES256/Ed25519), `DEC-AET-07` (Consultation sous réserve)

---

## 1. Budget Silicium Inviolable ACOSJ 92 Ko (92 160 octets)

En vertu de la décision `DEC-AET-01` de Kudoro (*« QUE DES CARTES 92Ko »*), la mémoire non-volatile de la carte JavaCard ACOSJ 92 Ko est allouée avec une précision d'orfèvre :

| Bloc | Désignation Métier | Format Données | Taille Allouée | % Silicium | Mode d'Accès |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **0** | **En-tête Silicium & Métadonnées** | TLV binaire | **512 o** | 0,55 % | Applet IsoDep (`A00000084501`) |
| **1** | **Profil Civil & Scellé Mémoriel** | CBOR / COSE_Sign1 | **2 048 o** | 2,22 % | **Dual-AID** (IsoDep & Type 4 Tag `E104`) |
| **2** | **Portrait Visuel Éternel** | WebP (480x480) | **20 480 o** (20 Ko) | 22,22 % | Applet IsoDep (Extended APDU) |
| **3** | **Mémo Vocal Inaltérable** | Opus SILK (16 kHz) | **46 080 o** (45 Ko) | 50,00 % | Applet IsoDep (Extended APDU) |
| **4** | **Registre d'Hommages / Arbre** | CBOR compressé | **15 360 o** (15 Ko) | 16,67 % | Applet IsoDep (Extended APDU) |
| **5** | **Réserve Matérielle Anti-Usure** | EEPROM Vierge | **7 680 o** (7,5 Ko) | 8,33 % | *Inviolable (> 5% imposé par Bushi 10)* |
| **TOTAL** | **Capacité Totale ACOSJ 92k** | — | **92 160 o** | **100,00 %** | — |

---

## 2. Le Miroir Silicium NDEF Type 4 Tag (Zero-Copy Architecture)

Pour permettre la lecture instantanée par Google Chrome sur Android via **Web NFC** sans consommer le moindre octet supplémentaire dans l'EEPROM de 92 Ko :
1. L'Applet Standard NFC Forum Type 4 Tag (AID `D2760000850101`) instancie le fichier NDEF `E104` non pas comme une copie, mais comme un **pointeur direct (Shareable Interface Object)** sur la plage mémoire du **Bloc 1**.
2. Les deux premiers octets du Bloc 1 contiennent le préfixe de longueur `NLEN` (2 octets, Big-Endian).
3. Le payload du fichier `E104` héberge le message NDEF MIME (`application/aeternitrak-profile+cbor`), encapsulant l'enveloppe `COSE_Sign1`.
4. Lors de l'émission de la commande de scellement par fusible (`80 DE 01 00`) en atelier funéraire, l'accès en écriture du fichier NDEF est commuté de façon permanente à `0xFF` (verrouillage matériel en lecture seule).

---

## 3. Persistance Locale & Cache Sanctuaire (IndexedDB)

Sur le smartphone (navigateur Web Chrome ou App native), les données lues sur le silicium sont mises en cache dans une base IndexedDB chiffrée :
- **Clé de dérivation locale** : Web Crypto API `PBKDF2` (100 000 itérations SHA-256) ancrée sur l'identifiant matériel de la carte (`event.serialNumber`).
- **Chiffrement au repos** : `AES-GCM-256` avec vecteur d'initialisation aléatoire de 12 octets par enregistrement.
- **Règle d'oubli mémoriel** : Aucune donnée biométrique ou vocale n'est transmise à un serveur centralisé sans accord explicite de la famille.
