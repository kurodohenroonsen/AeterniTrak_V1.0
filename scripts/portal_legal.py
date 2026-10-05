#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeterniTrak V1.0 — Référentiel des Textes Juridiques Applicables
"""

LEGAL_TEXTS = [
    {
        "jurisdiction": "🇧🇪 Région Wallonne",
        "ref": "Art. L1232-17 §2 CDLD (référence à confirmer par un juriste)",
        "official_title": "Code de la démocratie locale et de la décentralisation — Exérèse préalable des stimulateurs cardiaques (référence à confirmer par un juriste)",
        "disposition": "L'article L1232-17 §2 dispose que préalablement à toute crémation ou mise en bière, les stimulateurs cardiaques (pacemakers) et défibrillateurs automatiques implantables (DAE) doivent être obligatoirement retirés du corps par un médecin ou un chirurgien pour parer au risque majeur d'explosion thermique.",
        "project_choice": "Intégration d'un blocage logiciel inviolable dans PaxStudio et PaxStation : alerte prioritaire rouge et impossibilité absolue d'encodage sur le silicium sans attestation médicale nominative d'exérèse (INAMI du praticien).",
        "url": "#section-legal",
        "portal_url": None,
        "portal_name": None
    },
    {
        "jurisdiction": "🇧🇪 Belgique Fédérale",
        "ref": "Loi du 13 juin 1986 (référence à confirmer par un juriste)",
        "official_title": "Loi du 13 juin 1986 sur le prélèvement et la transplantation d'organes — Consentement présumé (référence à confirmer par un juriste)",
        "disposition": "Le système belge repose sur le principe du consentement présumé (opt-out) : tout citoyen belge ou résidant depuis plus de 6 mois est présumé donneur d'organes après son décès, sauf s'il a formellement acté son opposition de son vivant auprès de sa commune ou de son médecin traitant.",
        "project_choice": "Gravure des volontés de don d'organes directement dans l'EEPROM de la carte ACOSJ (EF-2 Profil) : confirmation expresse ou opposition enregistrée, consultable instantanément par les coordinateurs hospitaliers via simple tap NFC sans aucun mot de passe.",
        "url": "#section-legal",
        "portal_url": None,
        "portal_name": None
    },
    {
        "jurisdiction": "🇧🇪 Belgique Fédérale",
        "ref": "Loi du 20 juillet 1971 (référence à confirmer par un juriste)",
        "official_title": "Loi du 20 juillet 1971 sur les funérailles et sépultures — Primauté des dernières volontés (référence à confirmer par un juriste)",
        "disposition": "L'article 2 énonce que toute personne a le droit de déterminer de son vivant le mode et les conditions de ses funérailles (inhumation, crémation, cérémonie cultuelle ou laïque), s'imposant impérativement à la famille et aux exécuteurs testamentaires.",
        "project_choice": "Scellement cryptographique inaltérable des volontés sous format CBOR déterministe signé par la clé officielle de l'opérateur de pompes funèbres, conférant une valeur probante infalsifiable face aux contestations familiales.",
        "url": "#section-legal",
        "portal_url": None,
        "portal_name": None
    },
    {
        "jurisdiction": "🇧🇪 Belgique Fédérale",
        "ref": "Loi du 22 août 2002 (référence à confirmer par un juriste)",
        "official_title": "Loi du 22 août 2002 relative aux droits du patient — Accès post-mortem au dossier médical (art. 9 §4) (référence à confirmer par un juriste)",
        "disposition": "L'article 9 §4 dispose qu'après le décès du patient, les ayants droit peuvent accéder au dossier médical par l'intermédiaire d'un praticien professionnel désigné, pour autant que la demande soit motivée et que le patient ne s'y soit pas expressément opposé.",
        "project_choice": "Ségrégation cryptographique des champs médicaux sensibles sur la carte silicium : le compartiment des directives médicales est isolé et n'est déverrouillé que par présentation conjointe de la carte et du jeton professionnel du médecin désigné.",
        "url": "#section-legal",
        "portal_url": None,
        "portal_name": None
    },
    {
        "jurisdiction": "🇧🇪 Région Wallonne",
        "ref": "Décret wallon du 15 juillet 2008 (référence à confirmer par un juriste)",
        "official_title": "Décret wallon du 15 juillet 2008 relatif au Code forestier (art. 41) — Amendements du sol (référence à confirmer par un juriste)",
        "disposition": "L'article 41 dispose que le Gouvernement peut fixer les conditions d'épandage des amendements et fertilisants du sol forestier. Les articles suivants fixent les missions de police administrative et sylvicole des agents assermentés du Département de la Nature et des Forêts (DNF).",
        "project_choice": "Conditionnement des résidus cinéraires de sarcomusation pasteurisés sous forme d'amendements au pied d'arbres mémoriels identifiés (sous dérogation souveraine DEC-AET-05), et application mobile Biocontrôle DNF dotée de géolocalisation GPS submétrique et signature par badge agent.",
        "url": "#section-legal",
        "portal_url": "https://environnement.wallonie.be/",
        "portal_name": "Portail SPW"
    },
    {
        "jurisdiction": "🇧🇪 Région Wallonne",
        "ref": "Décret wallon du 6 mars 2009 (référence à confirmer par un juriste)",
        "official_title": "Décret wallon du 6 mars 2009 modifiant le CDLD (funérailles et sépultures) — Sécurité des opérateurs (référence à confirmer par un juriste)",
        "disposition": "Modification du CDLD prescrivant le renforcement des obligations de sécurité pour les agents des crématoriums et opérateurs funéraires, incluant la responsabilité du contrôle pré-opératoire des corps.",
        "project_choice": "Check-list automatisée de sécurité dans PaxStudio et PaxStation imposant le contrôle systématique des implants métalliques et des dispositifs actifs avant tout ordre de fabrication et d'impression thermique.",
        "url": "#section-legal",
        "portal_url": None,
        "portal_name": None
    },
    {
        "jurisdiction": "🇧🇪 Belgique Fédérale",
        "ref": "Loi du 30 juillet 2018 (référence à confirmer par un juriste)",
        "official_title": "Loi du 30 juillet 2018 relative à la protection des données à caractère personnel — Transposition RGPD (référence à confirmer par un juriste)",
        "disposition": "Transposition du RGPD (Règlement UE 2016/679) en droit belge, encadrant les principes de licéité, de transparence et de minimisation stricte des traitements (art. 5 RGPD) et régissant la protection des données associées aux personnes physiques.",
        "project_choice": "Architecture 100% hors-ligne (local-first, zéro serveur distant obligatoire), stockage exclusif des volontés et médias sur carte physique JavaCard ACOSJ 92 Ko sous contrôle direct des familles, garantissant une souveraineté et minimisation intégrales des données sans aucun compte cloud.",
        "url": "#section-legal",
        "portal_url": None,
        "portal_name": None
    }
]
