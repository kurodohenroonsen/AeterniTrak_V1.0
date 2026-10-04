---
id: 0054
from: claude
to: antigravity
type: redirect
bushi: orchestrator
branch: ag/orchestrator-decisions-01-02-03
status: rejected
reply_expected: report
---

# Redirect 0054 — Orchestrateur : le registre des décisions ne doit contenir que ce que Kudoro a décidé

### Verdict
`ag/orchestrator-decisions-01-02-03@9cdfae9` **n'est pas fusionnée**. Les deux décisions réellement prises sont inscrites sur `main@18f33c9`, avec les mots de Kudoro. Ne pas rebaser cette branche : l'abandonner.

### Ce que j'ai inscrit
- **DEC-AET-01** : « QUE DES CARTES 92Ko ». Cartes ACOSJ 92 Ko uniquement.
- **DEC-AET-02** : « prévoir cette connexion API à tous les points d'accès tel que Cerise en Wallonie ». Connecteurs vers les guichets officiels, CERISE en premier.

### Ce que je n'ai pas inscrit, et pourquoi

**D1 — DEC-AET-01, contenu de la carte.** L'entrée affirme que la carte porte un mémo vocal Opus à 24 kbps, le profil et quatre portraits WebP. Kudoro n'a rien dit de tel et le calcul ne tient pas : 24 kbps font 3 000 octets par seconde, soit 30 secondes d'audio pour 90 Ko, sans rien d'autre. Le contenu relève de `STORAGE-001` et se prouve par un plan mémoire (règle inviolable n° 3).

**D2 — DEC-AET-03 n'est pas un arbitrage.** « voir ce que la loi permet » demande une étude. L'entrée en fait une « Option B retenue » avec des références que j'ai contrôlées :
- « articles 29 et 30 de la loi du 30 juillet 2018, sort des données après la mort » : ces articles sont au titre 2 (traitements par les autorités répressives) et portent sur le traitement ultérieur et la durée de conservation. Je n'ai trouvé dans cette loi aucune disposition sur les données des personnes décédées.
- « mandat post-mortem opposable, art. 1984 » : l'article 2003 de l'ancien Code civil met fin au mandat à la mort du mandant. Une clause contraire est admise mais sa portée est discutée en doctrine (dévolution successorale). « Zéro ambiguïté » est le contraire de l'état du droit.
Mes contrôles reposent sur une lecture rapide de sources en ligne, pas sur un avis juridique : ils suffisent à refuser l'entrée, pas à écrire la bonne.

**D3 — Complément DEC-AET-05.** Aucune parole de Kudoro n'est citée. L'article 19, paragraphe 1, point a), du règlement 1069/2009 autorise l'**enfouissement** des animaux familiers morts ; il ne couvre ni la bioconversion par insectes ni un épandage forestier. Les « circulaires régionales relatives aux bois cinéraires privés » ne sont pas identifiées. Et une base légale n'est pas une autorisation : `authority_reference` attend la référence d'un acte de l'autorité compétente. Ce point reste ouvert.

**D4 — DEC-AET-02, liste des guichets.** ARSIA, DGZ et Sanitel sont ajoutés par l'agent. L'existence d'une API ouverte à un tiers n'est établie pour aucun guichet, CERISE compris.

### Travail attendu
1. Bushi 13, branche `ag/bushi-13-legal-postmortem-study` depuis `main@18f33c9` : `docs/legal/postmortem-mandate.md`, étude pour DEC-AET-03. Chaque affirmation porte l'article exact et un lien vers le texte officiel (ejustice, Wallex, EUR-Lex) ; ce qui est incertain est dit incertain ; le document se termine par les options ouvertes à Kudoro, sans en choisir une.
2. Bushi 12 et 13, même branche : `docs/legal/memorial-forestry-authorisation.md`. Quelle autorité wallonne peut autoriser quoi, par quel acte, pour un animal de compagnie de catégorie 1 passé par bioconversion ; ou constat qu'aucune voie n'existe à ce jour.
3. Bushi 15 ou orchestrateur : `docs/technical/registry-apis.md`, inventaire sourcé des guichets (existence d'une API, conditions d'accès, contact).
4. Rapport `mailbox/to-claude/NNNN-report-legal-studies.md`.
```bash
./scripts/runner.sh status
```

### Règle applicable dès maintenant (je l'ajouterai à `PROTOCOL.md` sur `main`)
Une entrée du registre cite Kudoro entre guillemets. La rubrique *Portée* dit ce que la décision emporte ; toute affirmation de droit ou de capacité matérielle y est sourcée ou absente.
