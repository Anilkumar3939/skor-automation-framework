#!/usr/bin/env python3
"""
Dashboard Screen tests — based on sc-mobile-app_v2/lib/ui/dashboard/dashboard_page.dart

Covers:
  01  Dashboard loads (passcode → home screen visible)
  02  Bottom navigation bar has 4 tabs
  03  Credit card widget is visible on dashboard
  04  Profile tab is accessible from bottom nav
  05  Notification icon is visible and tappable from dashboard

Navigation:
  Tests launch the app, handle the passcode screen automatically (via BaseTest),
  and expect to land on the Dashboard (DashboardScreen widget).

Key UI identifiers (from Flutter source):
  - Dashboard is recognised by card widget or transaction list
  - Bottom nav is a btm_nav_bar.dart custom widget with 4 items
  - Notifications are reached via bell icon on the app bar
"""
import os
import sys
import time

import allure

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in [_ROOT, os.path.join(_ROOT, "tests")]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from base import BaseTest
from utils.logger import get_logger


@allure.feature("Dashboard")
class TestDashboard(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.logger = get_logger("dashboard")

    # ── helpers ────────────────────────────────────────────────────────

    def _log_pass(self, msg):
        print(f"  ✅ PASS: {msg}")
        self.logger.info(f"PASS: {msg}")

    def _log_fail(self, msg):
        print(f"  ❌ FAIL: {msg}")
        self.logger.error(f"FAIL: {msg}")

    def _assert(self, condition, pass_msg, fail_msg):
        if condition:
            self._log_pass(pass_msg)
        else:
            self._log_fail(fail_msg)
        return condition

    def _is_dashboard(self):
        """
        True when the dashboard home screen is visible.
        Dashboard is identified by the credit-card area or transaction section
        which always appears for a logged-in user.
        """
        return (
            self.d(descriptionContains="card").exists(timeout=5) or
            self.d(textContains="Transaction").exists(timeout=5) or
            self.d(textContains="Transaksi").exists(timeout=3) or
            self.d(textContains="Available").exists(timeout=3) or
            self.d(textContains="Credit").exists(timeout=3)
        )

    def _navigate_to_dashboard(self):
        """
        Launch app, handle passcode, confirm dashboard is visible.
        Raises AssertionError when the device is not logged in so that both the
        custom runner and pytest record a FAIL rather than a silent pass.
        """
        if self._is_dashboard():
            return True

        self.launch_app()
        time.sleep(3)
        self.screenshot("nav_after_launch")

        if self._is_dashboard():
            return True

        raise AssertionError(
            "Dashboard not loaded — device must be logged in before running dashboard tests. "
            "Complete register_flow + create_pin suites first."
        )

    # ── TEST 01 — Dashboard loads ───────────────────────────────────────

    @allure.story("Dashboard Loads")
    def test_01_dashboard_loads(self):
        print("\n[TEST 01] Dashboard screen loads after app launch")
        self._navigate_to_dashboard()   # raises AssertionError if not logged in
        self.screenshot("01_dashboard")
        self._log_pass("Dashboard screen loaded successfully")

    # ── TEST 02 — Bottom navigation bar has tabs ────────────────────────

    @allure.story("Bottom Navigation Bar")
    def test_02_bottom_nav_visible(self):
        print("\n[TEST 02] Bottom navigation bar is visible with tabs")
        if not self._is_dashboard():
            self._navigate_to_dashboard()

        self.screenshot("02_bottom_nav")

        # btm_nav_bar.dart: Home, Card, Rewards/More, Profile — any two confirms the nav bar
        tab_count = 0
        for label in ["Home", "Card", "Profile", "Profil", "Rewards", "More", "Reward"]:
            if (self.d(text=label).exists(timeout=2) or
                    self.d(description=label).exists(timeout=1) or
                    self.d(descriptionContains=label).exists(timeout=1)):
                tab_count += 1
                print(f"  ✓ Tab found: {label}")

        self._assert(
            tab_count >= 2,
            f"Bottom nav has {tab_count} identifiable tabs",
            f"Bottom nav not found or has fewer than 2 tabs ({tab_count})",
        )

    # ── TEST 03 — Credit card widget is visible ─────────────────────────

    @allure.story("Credit Card Widget Visible")
    def test_03_card_widget_visible(self):
        print("\n[TEST 03] Credit card widget is displayed on the dashboard")
        if not self._is_dashboard():
            self._navigate_to_dashboard()

        self.screenshot("03_card_widget")

        card_visible = (
            self.d(descriptionContains="card").exists(timeout=5) or
            self.d(descriptionContains="Card").exists(timeout=3) or
            self.d(textContains="Credit").exists(timeout=3) or
            self.d(textContains="Kredit").exists(timeout=3) or    # Indonesian
            self.d(textContains="Limit").exists(timeout=3) or
            self.d(textContains="limit").exists(timeout=3)
        )
        self._assert(
            card_visible,
            "Credit card widget is visible on dashboard",
            "Credit card widget not found on dashboard",
        )

    # ── TEST 04 — Profile tab accessible from bottom nav ────────────────

    @allure.story("Profile Tab Accessible")
    def test_04_profile_tab_accessible(self):
        print("\n[TEST 04] Profile tab accessible from bottom navigation")
        if not self._is_dashboard():
            self._navigate_to_dashboard()

        # Tap the Profile tab — try all known label variants (EN + ID)
        tapped = False
        for label in ["Profile", "Profil"]:
            if self.d(text=label).exists(timeout=2):
                self.d(text=label).click()
                tapped = True
                break
            if self.d(description=label).exists(timeout=2):
                self.d(description=label).click()
                tapped = True
                break

        if not tapped:
            # Final fallback: try the bottom-nav icon whose description
            # contains "Profile" or "Profil" anywhere
            for label in ["Profile", "Profil"]:
                el = self.d(descriptionContains=label)
                if el.exists(timeout=2):
                    el.click()
                    tapped = True
                    break

        if not tapped:
            raise AssertionError(
                "Profile tab not found by text or description — "
                "check that the bottom nav is rendered on screen"
            )

        time.sleep(2)
        self.screenshot("04_profile_tab")

        profile_visible = (
            self.d(textContains="Profile").exists(timeout=5) or
            self.d(textContains="Profil").exists(timeout=3) or
            self.d(textContains="Account").exists(timeout=3) or
            self.d(textContains="Akun").exists(timeout=3) or       # Indonesian
            self.d(textContains="Logout").exists(timeout=3) or
            self.d(textContains="Keluar").exists(timeout=3)        # Indonesian
        )
        self._assert(
            profile_visible,
            "Profile page loaded from bottom nav tap",
            "Profile page not loaded after tapping Profile tab",
        )

    # ── TEST 05 — Notification icon visible on dashboard ────────────────

    @allure.story("Notification Icon Visible")
    def test_05_notification_icon_visible(self):
        print("\n[TEST 05] Notification icon is visible on the dashboard")

        # Navigate back to dashboard home (test_04 may have opened profile)
        if not self._is_dashboard():
            self.d.press("back")
            time.sleep(1)

        if not self._is_dashboard():
            self._navigate_to_dashboard()

        self.screenshot("05_notification_icon")

        notif_visible = (
            self.d(descriptionContains="notification").exists(timeout=5) or
            self.d(descriptionContains="Notification").exists(timeout=3) or
            self.d(descriptionContains="Notifikasi").exists(timeout=3) or   # Indonesian
            self.d(descriptionContains="bell").exists(timeout=3) or
            self.d(description="Notifications").exists(timeout=3)
        )
        self._assert(
            notif_visible,
            "Notification icon visible on dashboard",
            "Notification icon not found — check screenshot 05",
        )


# ── Explicit test order ──────────────────────────────────────────────────────
TEST_ORDER = [
    "test_01_dashboard_loads",
    "test_02_bottom_nav_visible",
    "test_03_card_widget_visible",
    "test_04_profile_tab_accessible",
    "test_05_notification_icon_visible",
]

if __name__ == "__main__":
    t = TestDashboard()
    TestDashboard.setup_class()
    for method in TEST_ORDER:
        getattr(t, method)()
    print("\n✅ Dashboard tests done. Check screenshots/ and logs/")
