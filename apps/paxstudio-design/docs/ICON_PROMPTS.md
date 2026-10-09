# Pictogrammes de la Carte 1 « Dernières volontés » — prompts de génération

La Carte 1 affiche **l'intégralité du PAVS** (formulaire officiel du Réseau Santé Wallon, conçu par UNESSA) sur
85,60 × 53,98 mm. Les libellés sont remplacés par des pictogrammes ; les cases à cocher deviennent des
**matrices de pictogrammes** (coché = vif + pastille, non coché = estompé). Les versions actuelles sont dessinées à la
main dans `js/ornaments.js` (`ICONS`, grille 24 × 24, trait). Ce document sert à produire un jeu homogène de qualité
supérieure avec un générateur d'images, puis à le vectoriser.

## 1. Charte commune (à préfixer à chaque prompt)

> **Style prompt (EN)** — *Minimal monoline pictogram, single continuous stroke weight 1.5 px on a 24 × 24 px grid,
> 2 px safe padding, rounded caps and joins, no fill, no shading, no text, no letters, no gradient, pure black on
> pure white, geometric and calm, dignified funeral-and-healthcare tone, readable at 2.5 mm printed size,
> consistent with the other icons of the same set, centered, flat vector style, SVG-ready.*

Contraintes de livraison :
- **SVG** uniquement (un `<path>` par icône, `stroke="currentColor"`, `fill="none"`), `viewBox="0 0 24 24"` ;
  aucune image matricielle (règle « 100 % CSS et SVG »).
- Lisible à **2,5 mm** de côté imprimé : 3 à 6 traits maximum, pas de détails < 1,5 px.
- Pas de symbole religieux spécifique (croix, croissant, étoile de David…) sauf demande explicite :
  les rites restent neutres.
- Pas de code-barres, pas de puce à contacts, pas de logo de marque.
- Remplacer la chaîne correspondante dans `ICONS` (même identifiant) ; la légende se met à jour seule.

## 2. Pastilles de réponse (superposées en bas à droite)

| id | Sens | Prompt (sujet) |
|---|---|---|
| `yes` | Oui / coché | small solid green disc with a white check mark |
| `no` | Non / refusé | small solid dark-red disc with a white diagonal cross |
| `presumed` | Sans préférence | small solid blue disc with a white double wavy line (≈) |
| `alert` | Alerte | small solid red disc with a white exclamation mark |

## 3. Identité

| id | Rubrique | Prompt (sujet) |
|---|---|---|
| `genderF` | Femme | female symbol: circle with a short cross below |
| `genderM` | Homme | male symbol: circle with an arrow pointing up-right |
| `genderX` | Genre X | circle containing a diagonal X |
| `birth` | Date et lieu de naissance | small layered birthday cake with a single candle flame |
| `phone` | Téléphone | classic telephone handset, angled |
| `idcard` | N° de registre national | identity card with a head-and-shoulders silhouette on the left and two text lines on the right |
| `calendar` | Date d'enregistrement | calendar page with two binder rings and a header band |
| `archive` | Lieu de conservation du PSPA | archive box with lid and a horizontal handle slot |

## 4. Contacts (Institution(s) et/ou personne(s) à contacter)

| id | Rubrique | Prompt (sujet) |
|---|---|---|
| `institution` | Institution(s) | two-volume building, rest home or hospital of reference, with small windows |
| `physician` | Médecin traitant | stethoscope with ear tips and chest piece |
| `contact` | Personne(s) à contacter | person bust with two sound-wave arcs on the right |
| `proxyHealth` | Mandataire (soins de santé) | protective shield with a medical plus sign |
| `proxyLegal` | Mandataire extrajudiciaire | balanced scales of justice |
| `trusted` | Personne(s) de confiance | open hand holding a small heart above it |
| `keyAdmin` | Administrateur de biens et/ou de la personne | old key with round bow and two teeth |

## 5. Mon projet de soins

| id | Rubrique | Prompt (sujet) |
|---|---|---|
| `gauge` | Projet global (intensité des soins) | semicircular gauge with a needle |
| `careMax` | Soins maximums | bedside monitor screen showing a heartbeat line |
| `careUsual` | Soins usuels | medical clipboard with a plus sign |
| `careComfort` | Soins de confort/palliatifs | cloak or mantle wrapping a small heart (from Latin *palliare*, « couvrir d'un manteau ») |
| `euthanasia` | Déclaration anticipée d'euthanasie signée | signed document with folded corner and a small heart near the bottom |
| `ban` | Thérapies refusées | circle with diagonal bar (prohibition sign) |
| `antibiotic` | Antibiothérapie | two-part capsule pill, diagonal |
| `hydration` | Perfusion hydratante | infusion bag containing a water drop, with tube |
| `tubeNose` | Alimentation entérale (sonde par le nez) | face profile with a thin feeding tube entering the nostril |
| `ivDrip` | Alimentation parentérale (en intraveineuse) | IV bag on a stand line ending in a needle |
| `gastro` | Sonde de gastrostomie (dans le ventre) | stomach outline with a short tube exiting the abdomen |
| `dialysis` | Dialyse | two stacked filter cartridges linked by parallel lines |
| `oxygen` | Oxygénothérapie | round oxygen bubble with a small subscript-2 shape (no letters: an "O" ring and a tiny "2"-like curve) |
| `mask` | Ventilation non invasive (VNI) | full face breathing mask with side straps |
| `intubation` | Intubation | curved endotracheal tube with an arrow at its end |
| `sedation` | Sédation palliative | closed eye with lashes and a crescent moon |
| `consciousness` | Traitement altérant l'état de conscience | open eye with a spiral iris |
| `bed` | À soins égaux je préfère être | single bed seen from the side with a pillow |
| `home` | à mon domicile | simple house with door |
| `hospital` | à l'hôpital | hospital building with a cross on the facade |
| `palliativeUnit` | en unité de soins palliatifs | bed with a small heart above the pillow |
| `reanimation` | Hospitalisation avec / sans réanimation | heart with a lightning bolt inside |
| `fracture` | Hospitalisation exceptionnelle (fracture, occlusion…) | bone broken in two with a jagged gap |
| `bubble` | Commentaires | speech bubble with a tail |

## 6. Mes souhaits de fin de vie

| id | Rubrique | Prompt (sujet) |
|---|---|---|
| `home` | Fin de vie dans mon lieu de vie habituel | (même pictogramme que « à mon domicile ») |
| `psych` | Accompagnement psychologique | head profile with a small question-curve inside |
| `book` | Accompagnement philosophique | open book with a center spine |
| `candle` | Accompagnement religieux | lit candle on a base (neutral, no religious symbol) |
| `lotus` | Accompagnement spirituel | lotus flower with three petals |
| `star` | Accompagnement autre / « je souhaite en particulier » | five-pointed outline star |
| `none` | Aucun accompagnement | circle with a horizontal bar |
| `quote` | Pour moi, l'essentiel c'est | pair of opening quotation marks |
| `feather` | Mes autres souhaits (fin de vie) | writing feather quill |

## 7. Mes volontés pour l'après-décès

| id | Rubrique | Prompt (sujet) |
|---|---|---|
| `scroll` | Volontés après décès / autres souhaits | rolled scroll with text lines |
| `heart` | J'accepte de donner mes organes | heart outline |
| `science` | Je donne mon corps à la science | laboratory flask (Erlenmeyer) with liquid line |
| `flame` | Incinéré(e) | single calm flame |
| `stone` | Inhumé(e) | rounded headstone on the ground line |
| `disposition` | Sans préférence | circle with a question mark |
| `pacemaker` | J'ai un pacemaker | heart outline crossed by an ECG pulse line |
| `relatives` | Je laisse à mes proches le choix | person bust beside a question mark |
| `insurance` | Assurance obsèques | shield with a check mark |
| `rite` | Rite(s) / rituel(s) | neutral standing stele or obelisk on a base |
| `funeralHome` | Pompes funèbres | small chapel-like building with a pitched roof |
| `paperclip` | Annexe(s) éventuelle(s) | paperclip, diagonal |

## 8. Compléments AeterniTrak (hors formulaire officiel)

| id | Rubrique | Prompt (sujet) |
|---|---|---|
| `lawn` | Dispersion sur pelouse cinéraire | grass blades on a ground line with three small dots above |
| `columbarium` | Columbarium | 3 × 3 grid of niches |
| `sea` | Dispersion en mer | three parallel waves |
| `urn` | Urne / cavurne | funeral urn with lid and base |
| `vault` | Caveau | small vault with an arched door |
| `tree` | Humusation | tree with round crown |
| `pin` | Destination | map pin with a hole |
| `coffin` | Cercueil | hexagonal coffin seen from above |
| `radiation` | Radio-isotopes actifs | radiation trefoil |
| `biohazard` | Risque biologique | biohazard symbol simplified |
| `camera` | Photos | camera body with lens |
| `mic` | Message vocal | studio microphone on a stand |
| `music` | Musique | two beamed eighth notes |
| `doc` | Permis d'inhumation / transport | document with folded corner and lines |
| `nfc` | Puce NFC sans contact | three concentric contactless arcs and a dot |
