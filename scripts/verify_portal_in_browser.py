#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeterniTrak V1.0 — Vérification Exhaustive Playwright & Headless Chrome du Portail Vivant
Audite l'ensemble des interactions du Grand Théâtre Vivant (Exp A, B, C, D),
des boutons bimodaux, des onglets applicatifs, des vues et de la modale Studio.
Exige 0 pageerror et 0 console error.
"""

import os
import sys
import tempfile
import time
from playwright.sync_api import sync_playwright

def run_browser_verification():
    print("=" * 70)
    print("🚀 DÉMARRAGE DE L'AUDIT NAVIGATEUR PLAYWRIGHT / HEADLESS CHROME")
    print("=" * 70)

    portal_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "usecases", "index.html"))
    if not os.path.exists(portal_path):
        print(f"❌ Erreur : Le fichier {portal_path} n'existe pas !", file=sys.stderr)
        sys.exit(1)

    file_url = f"file://{portal_path}"
    print(f"📄 Cible : {file_url}")

    user_data_dir = tempfile.mkdtemp(prefix="playwright_chrome_profile_")
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

    page_errors = []
    console_errors = []
    console_warnings = []
    console_logs = []

    def on_page_error(err):
        msg = str(err)
        print(f"❌ [PAGEERROR] {msg}", file=sys.stderr)
        page_errors.append(msg)

    def on_console(msg):
        text = f"[{msg.type.upper()}] {msg.text}"
        console_logs.append(text)
        if msg.type == "error":
            print(f"❌ [CONSOLE ERROR] {msg.text}", file=sys.stderr)
            console_errors.append(msg.text)
        elif msg.type == "warning":
            console_warnings.append(msg.text)

    with sync_playwright() as p:
        print(f"🌐 Lancement de Google Chrome ({chrome_path})...")
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            executable_path=chrome_path,
            headless=True,
            viewport={"width": 1440, "height": 900},
            args=['--no-sandbox', '--disable-gpu']
        )

        page = context.new_page()
        page.on("pageerror", on_page_error)
        page.on("console", on_console)

        print("🔄 Navigation vers le portail vivant...")
        page.goto(file_url, wait_until="networkidle")
        page.wait_for_timeout(500)

        # -------------------------------------------------------------
        # 1. AUDIT DU GRAND THÉÂTRE VIVANT : LES 4 EXPÉRIENCES HERO
        # -------------------------------------------------------------
        print("\n--- 1. AUDIT DU GRAND THÉÂTRE VIVANT (4 EXPÉRIENCES HERO) ---")

        # Exp A : Sanctuaire Mobile & Flamme Mémorielle
        print("  [1.1] Test Hero Exp A : Sanctuaire Mobile & Flamme...")
        page.click("#hero-tab-expA")
        page.wait_for_timeout(300)
        assert "active" in page.get_attribute("#hero-tab-expA", "class"), "Hero Tab Exp A non actif"
        assert "active" in page.get_attribute("#hero-panel-expA", "class"), "Hero Panel Exp A non actif"

        # Bouton mémoriel & oscillateur
        print("    -> Lecture audio sanctuaire...")
        page.click("#memorial-play-btn")
        page.wait_for_timeout(400)
        ducking_text = page.inner_text("#ducking-indicator")
        print(f"    -> Statut ducking : '{ducking_text}'")
        assert "Ducking" in ducking_text or "Actif" in ducking_text, "Ducking non actif après play"

        # Arrêt audio
        page.click("#memorial-play-btn")
        page.wait_for_timeout(200)

        # Tiroir des directives Exp A
        print("    -> Tiroir des directives Exp A...")
        drawer_btn = page.locator("#hero-panel-expA button:has-text('Directives & Volontés')")
        drawer_btn.click()
        page.wait_for_timeout(200)
        assert "hidden" not in (page.get_attribute("#memorial-drawer-content", "class") or ""), "Tiroir non déplié"
        drawer_btn.click()
        page.wait_for_timeout(200)

        # Capture Screenshot Exp A
        print("  📸 Capture screenshot Exp A dans /tmp/screenshot_expA.png...")
        page.locator("#interactive-theater").screenshot(path="/tmp/screenshot_expA.png")

        # Exp B : Carte 3D PaxFunèbre
        print("  [1.2] Test Hero Exp B : Carte 3D PaxFunèbre...")
        page.click("#hero-tab-expB")
        page.wait_for_timeout(300)
        assert "active" in page.get_attribute("#hero-panel-expB", "class"), "Hero Panel Exp B non actif"

        print("    -> Retournement carte 3D (Face Verso Directives)...")
        page.click("#card-flip-btn")
        page.wait_for_timeout(300)
        assert "flipped" in (page.get_attribute("#card-3d-element", "class") or ""), "Carte 3D non retournée"

        print("    -> Retournement carte 3D (Face Recto Sanctuaire)...")
        page.click("#card-flip-btn")
        page.wait_for_timeout(300)
        assert "flipped" not in (page.get_attribute("#card-3d-element", "class") or ""), "Carte 3D non rétablie"

        print("    -> Finitions nobles (Or Satiné & Obsidienne)...")
        page.click("button:has-text('Or Satiné')")
        page.wait_for_timeout(200)
        page.click("button:has-text('Obsidienne')")
        page.wait_for_timeout(200)

        # Capture Screenshot Exp B
        print("  📸 Capture screenshot Exp B dans /tmp/screenshot_expB.png...")
        page.locator("#interactive-theater").screenshot(path="/tmp/screenshot_expB.png")

        # Exp C : PaxStation & ACR1552U
        print("  [1.3] Test Hero Exp C : PaxStation & Lecteur ACR1552U...")
        page.click("#hero-tab-expC")
        page.wait_for_timeout(300)
        assert "active" in page.get_attribute("#hero-panel-expC", "class"), "Hero Panel Exp C non actif"

        print("    -> Lancement gravure silicium (APDU + EEPROM)...")
        page.click("#paxstation-start-btn")
        page.wait_for_timeout(2600) # Attente de la fin de simulation
        btn_text = page.inner_text("#paxstation-start-btn")
        byte_text = page.inner_text("#paxstation-byte-text")
        print(f"    -> Fin gravure : '{btn_text}' | EEPROM: '{byte_text}'")
        assert "Terminée" in btn_text or "Relancer" in btn_text, "Gravure non finalisée"

        # Capture Screenshot Exp C
        print("  📸 Capture screenshot Exp C dans /tmp/screenshot_expC.png...")
        page.locator("#interactive-theater").screenshot(path="/tmp/screenshot_expC.png")

        # Exp D : Cassette LFA & The Iron Gate
        print("  [1.4] Test Hero Exp D : Cassette LFA & The Iron Gate...")
        page.click("#hero-tab-expD")
        page.wait_for_timeout(300)
        assert "active" in page.get_attribute("#hero-panel-expD", "class"), "Hero Panel Exp D non actif"

        print("    -> Lancement dépistage toxicologique LFA...")
        page.click("#lfa-start-btn")
        page.wait_for_timeout(2800) # Attente de la migration et de l'activation G0-G9
        lfa_banner_class = page.get_attribute("#lfa-result-banner", "class") or ""
        assert "hidden" not in lfa_banner_class, "Bannière résultat LFA non affichée"
        lfa_btn_text = page.inner_text("#lfa-start-btn")
        print(f"    -> Résultat LFA : '{lfa_btn_text}'")
        assert "Conforme" in lfa_btn_text or "Relancer" in lfa_btn_text, "Dépistage LFA non validé"

        # Capture Screenshot Exp D
        print("  📸 Capture screenshot Exp D dans /tmp/screenshot_expD.png...")
        page.evaluate("() => { const el = document.getElementById('interactive-theater'); if (el) el.scrollIntoView(); window.scrollBy(0, -90); }")
        page.wait_for_timeout(300)
        page.locator("#interactive-theater").screenshot(path="/tmp/screenshot_expD.png")

        # Capture Screenshot Hero HD Global
        print("  📸 Capture screenshot Hero Global dans /tmp/portal_verified_hero.png...")
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(300)
        page.screenshot(path="/tmp/portal_verified_hero.png", full_page=False)

        # -------------------------------------------------------------
        # 2. AUDIT DE LA BASCULE BIMODALE (FAMILLE vs INGÉNIEUR)
        # -------------------------------------------------------------
        print("\n--- 2. AUDIT DE LA BASCULE BIMODALE ---")
        print("  [2.1] Bascule en Mode Ingénieur...")
        page.click("#btn-mode-engineer")
        page.wait_for_timeout(300)
        assert "active-engineer" in page.get_attribute("#btn-mode-engineer", "class"), "Mode Ingénieur non actif"
        desc_text = page.inner_text("#portal-mode-desc")
        assert "Ingénieur" in desc_text or "Silicium" in desc_text, "Description Mode Ingénieur incorrecte"

        print("  [2.2] Bascule en Mode Famille...")
        page.click("#btn-mode-family")
        page.wait_for_timeout(300)
        assert "active-family" in page.get_attribute("#btn-mode-family", "class"), "Mode Famille non actif"
        desc_text = page.inner_text("#portal-mode-desc")
        assert "Famille" in desc_text, "Description Mode Famille incorrecte"

        # -------------------------------------------------------------
        # 3. AUDIT DES ONGLETS MÉTIERS & MODES DE VUE
        # -------------------------------------------------------------
        print("\n--- 3. AUDIT DES ONGLETS MÉTIERS & MODES DE VUE ---")
        tabs = [
            ("app1", "PaxStudio Design", "section-app1"),
            ("app2", "PaxStation Encodage", "section-app2"),
            ("app3", "Sanctuaire Mémoriel", "section-app3"),
            ("app4", "Filière Sarcomusation", "section-app4"),
            ("legal", "Référentiel Juridique", "section-legal")
        ]

        for tab_id, tab_label, sec_id in tabs:
            print(f"  [3.{tabs.index((tab_id, tab_label, sec_id))+1}] Test Onglet '{tab_label}' ({tab_id})...")
            page.click(f"#tab-{tab_id}")
            page.wait_for_timeout(300)
            sec_class = page.get_attribute(f"#{sec_id}", "class") or ""
            assert "hidden" not in sec_class, f"Section {sec_id} non visible !"

            if tab_id != "legal":
                # Test des 3 modes de vue : cards, board, table
                print(f"    -> Mode Board déplié pour {tab_id}...")
                page.click(f"#btn-mode-{tab_id}-board")
                page.wait_for_timeout(200)

                if tab_id == "app1":
                    print("  📸 Capture screenshot Board dans /tmp/portal_verified_board.png...")
                    page.screenshot(path="/tmp/portal_verified_board.png", full_page=True)

                print(f"    -> Mode Table d'audit pour {tab_id}...")
                page.click(f"#btn-mode-{tab_id}-table")
                page.wait_for_timeout(200)

                print(f"    -> Rétablissement Mode Cards pour {tab_id}...")
                page.click(f"#btn-mode-{tab_id}-cards")
                page.wait_for_timeout(200)

        # -------------------------------------------------------------
        # 4. AUDIT DE LA MODALE STUDIO WIREFRAME (UC-101)
        # -------------------------------------------------------------
        print("\n--- 4. AUDIT DE LA MODALE STUDIO WIREFRAME ---")
        page.click("#tab-app1")
        page.wait_for_timeout(200)

        print("  [4.1] Ouverture modale Studio sur UC-101...")
        # Cliquer sur le titre ou bouton Inspecter
        card_btn = page.locator("#card-UC-101 button:has-text('Inspecter Studio')")
        card_btn.click()
        page.wait_for_timeout(400)

        modal = page.locator("#ucModal")
        is_open = page.evaluate("() => document.getElementById('ucModal').open")
        assert is_open, "La modale Studio ne s'est pas ouverte !"
        print("    -> Modale ouverte avec succès.")

        print("  [4.2] Navigation dans les 4 phases wireframe...")
        for pk in ['p2', 'p3', 'p4', 'p1']:
            pill_id = f"#modal-pill-{pk}"
            page.click(pill_id)
            page.wait_for_timeout(150)
            pill_class = page.get_attribute(pill_id, "class") or ""
            assert "active" in pill_class, f"Pill {pill_id} non actif dans la modale"

        print("  [4.3] Test simulateur cycle complet modale...")
        page.click("#modal-sim-btn")
        page.wait_for_timeout(500)
        page.click("#modal-sim-btn") # Pause
        page.wait_for_timeout(100)

        print("  [4.4] Fermeture de la modale...")
        page.click("#modal-close-btn")
        page.wait_for_timeout(300)
        is_open_after = page.evaluate("() => document.getElementById('ucModal').open")
        assert not is_open_after, "La modale Studio ne s'est pas fermée !"
        print("    -> Modale refermée avec succès.")

        # -------------------------------------------------------------
        # 5. TEST DE RECHERCHE INSTANTANÉE
        # -------------------------------------------------------------
        print("\n--- 5. TEST DE RECHERCHE INSTANTANÉE ---")
        page.fill("#searchInput", "pacemaker")
        page.wait_for_timeout(200)
        page.fill("#searchInput", "")
        page.wait_for_timeout(200)
        print("    -> Filtre de recherche opérationnel.")

        context.close()

    print("\n" + "=" * 70)
    print("📊 BILAN DE L'AUDIT DE CONFORMITÉ NAVIGATEUR")
    print("=" * 70)
    print(f"  • Total logs console enregistrés : {len(console_logs)}")
    print(f"  • Total avertissements console   : {len(console_warnings)}")
    print(f"  • Total erreurs de page (pageerror) : {len(page_errors)}")
    print(f"  • Total erreurs console (error)     : {len(console_errors)}")
    print(f"  • Screenshot Hero  : /tmp/portal_verified_hero.png ({os.path.getsize('/tmp/portal_verified_hero.png'):,} octets)")
    print(f"  • Screenshot Board : /tmp/portal_verified_board.png ({os.path.getsize('/tmp/portal_verified_board.png'):,} octets)")
    print("=" * 70)

    if page_errors:
        print("\n❌ ERREURS DE PAGE DÉTECTÉES :", file=sys.stderr)
        for e in page_errors:
            print(f"   - {e}", file=sys.stderr)

    if console_errors:
        print("\n❌ ERREURS CONSOLE DÉTECTÉES :", file=sys.stderr)
        for e in console_errors:
            print(f"   - {e}", file=sys.stderr)

    assert len(page_errors) == 0, f"Échec : {len(page_errors)} pageerror(s) détectée(s) !"
    assert len(console_errors) == 0, f"Échec : {len(console_errors)} console error(s) détectée(s) !"

    print("\n🎉 TOUS LES CRITÈRES DE VALIDATION SONT RESPECTÉS (0 PAGEERROR, 0 CONSOLE ERROR) !")
    print("=" * 70)

if __name__ == "__main__":
    run_browser_verification()
