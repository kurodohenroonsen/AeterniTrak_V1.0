# PaxStudio Design — Application 1 (`DEC-AET-08`)

Studio de conception des deux cartes ID-1 AeterniTrak et de saisie du PAVS.
Vanilla ES6 + CSS + SVG, sans étape de build ni dépendance d'exécution, 100 % hors-ligne (polices OFL embarquées dans `fonts/`).

## Lancer

Ouvrir `index.html` dans un navigateur récent, ou, pour que l'export SVG embarque les polices :

```bash
cd apps/paxstudio-design && python3 -m http.server 8000   # puis http://localhost:8000
```

## Espaces de travail

| Onglet | Contenu |
| --- | --- |
| **Carte 1 · Volontés** | **Intégralité du PAVS** sur les deux faces, sans donnée dominante. Recto : identité (vignette photo, NISS + modulo 97), 7 contacts + lieu de conservation, projet de soins en matrices de pictogrammes (intensité, 11 thérapies refusées, lieux de soins, hospitalisation), commentaires, bandeau pyrotechnique. Verso : fin de vie et après-décès en matrices, puis tous les textes libres en deux colonnes, multimédia, permis, cible NFC. Corps de texte **unique** auto-ajusté (≤ 1,3 mm) ; le statut indique le corps retenu et toute rubrique qui ne tiendrait pas. |
| **Carte 2 · Mémorial** | Recto : 5 gabarits (A Majestueux, B Diptyque, C Triptyque, D Mosaïque, E Typographie pure), insigne colombe ou rameau de chêne. Verso : onde sonore 20 barres (pulsation optionnelle), tonalité, mémo vocal, appel NFC « 38 ms », n° d'exemplaire et empreinte SHA-256 réelle du dossier. |
| **PAVS · Mes volontés** | Réplique du formulaire officiel « Ajouter un PAVS (mes volontés) » du Réseau Santé Wallon (conçu par UNESSA) : mêmes rubriques, cases et options, annexes (3 fichiers, 6 Mo), date d'enregistrement, **Publier / Annuler**. Les boutons **?** ouvrent en fenêtre modale la synthèse des fiches didactiques UNESSA (représentation, type de soins, euthanasie, alimentation artificielle, aide à la respiration, sédation, dons). Une section « Compléments AeterniTrak » distingue ce qui n'est pas dans le formulaire officiel. |

Le sélecteur en haut à droite donne accès aux 44 cas de référence et aux PAVS personnels. Toute modification (panneau latéral ou formulaire PAVS) met à jour les deux cartes en direct.

## Règles appliquées (`js/rules.js`)

- **NISS** : contrôle modulo 97 (constante 2 000 000 000 dès 2000), cohérence avec la date de naissance, parité de séquence et genre.
- **Verrou pyrotechnique** : modes 3 à 12 (crémation et sarcomusation) bloqués si un stimulateur est présent sans PV d'exérèse ; inhumation tolérée.
- **Statut B.A.T.** : pyrotechnie → radio-isotopes → prion × humusation → identité incomplète. Reproduit à l'identique `bat_status` des 44 cas.
- **Sarcomusation** : chaque option porte la mention de `DEC-AET-15` (démonstrateur de faisabilité, option prospective).
- **Carte 1** : aucune date de décès imprimée ; aucune puce à contacts ; aucun code-barres.
- **Portrait** : recadré en WebP 480×480, qualité ajustée pour tenir dans EF-2 (≤ 20 480 o, `DEC-AET-12`) ; sinon camée vectoriel.

## Pictogrammes

86 pictogrammes vectoriels (`js/ornaments.js`) ; légende dans le panneau latéral et sur le B.A.T.
Les prompts de génération d'un jeu homogène (charte commune + sujet par icône) sont dans [`docs/ICON_PROMPTS.md`](docs/ICON_PROMPTS.md).

Les 44 cas de référence sont migrés à l'ouverture vers le schéma du formulaire officiel (`normalizePavs`, idempotent) ; le statut B.A.T. reste identique.

## Export & impression

- **SVG recto / verso** : coordonnées en millimètres (`viewBox` = mm), dimensions physiques 85,60 × 53,98 mm, polices embarquées en base64.
- **Imprimer le B.A.T.** : planche A4 à l'échelle 1:1 avec fond perdu 2 mm, traits de coupe 5 mm, repères de centrage, ligne de découpe, zone de sécurité 3 mm en option et règle de contrôle de 100 mm. Imprimer à 100 %.

## Tests

```bash
node apps/paxstudio-design/tests/rules.test.mjs   # ou : npm run test:paxstudio
```
