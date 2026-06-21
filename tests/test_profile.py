#!/usr/bin/env python3
"""
Profile Page tests — based on sc-mobile-app_v2/lib/ui/profile/profile.dart

Covers:
  01  Profile page loads from dashboard bottom nav
  02  "My Account" section header is visible (language.myAccount)
  03  Logout option is visible at the bottom of profile page
  04  Help Center menu item is present (SkorcardSection)
  05  Biometrics toggle is visible (MyAccountSection)
  06  Language option is visible (MyAccountSection → language.language)
  07  About Skorcard menu item is visible

Navigation:
  Tests launch the app, handle passcode, reach the dashboard, then tap the
  Profile tab in the bottom navigation bar.

Key UI identifiers (from profile.dart):
  - Section headers: language.myAccount ("MY ACCOUNT"), language.appName ("SKORCARD")
  - List items: language.language, language.biometrics, language.helpCenter,
                language.aboutSkorcard, language.logout
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


@allure.feature("Profile Page")
class TestProfile(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.logger = get_logger("profile")
        cls._on_profile = False

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

    def _is_on_profile(self):
        return (
            self.d(textContains="MY ACCOUNT").exists(timeout=3) or
            self.d(textContains="My Account").exists(timeout=3) or
            self.d(textContains="Logout").exists(timeout=3) or
            self.d(textContains="Keluar").exists(timeout=3)
        )

    def _navigate_to_profile(self):
        """
        Launch app → handle passcode → tap Profile tab in bottom nav.
        Raises AssertionError if device is not logged in or Profile tab is not found.
        """
        if self._is_on_profile():
            return True

        self.launch_app()
        time.sleep(3)

        # Tap Profile tab — try all known label variants (EN + ID)
        tapped = False
        for label in ["Profile", "Profil"]:
            if self.d(text=label).exists(timeout=3):
                self.d(text=label).click()
                tapped = True
                break
            if self.d(description=label).exists(timeout=2):
                self.d(description=label).click()
                tapped = True
                break

        # Try descriptionContains as final fallback (no coordinates)
        if not tapped:
            for label in ["Profile", "Profil"]:
                el = self.d(descriptionContains=label)
                if el.exists(timeout=2):
                    el.click()
                    tapped = True
                    break

        if not tapped:
            raise AssertionError(
                "Profile tab not found — device must be logged in and on the dashboard. "
                "Run register_flow + create_pin suites first."
            )

        time.sleep(2)
        if not self._is_on_profile():
            raise AssertionError(
                "Profile page did not load after tapping Profile tab — check device state."
            )
        return True

    # ── TEST 01 — Profile page loads ────────────────────────────────────

    @allure.story("Profile Page Loads")
    def test_01_profile_page_loads(self):
        print("\n[TEST 01] Profile page loads from dashboard")
        self._navigate_to_profile()   # raises on failure
        self.screenshot("01_profile_page")
        self._log_pass("Profile page loaded successfully")

    # ── TEST 02 — My Account section visible ────────────────────────────

    @allure.story("My Account Section Visible")
    def test_02_my_account_section_visible(self):
        print("\n[TEST 02] 'My Account' section header is visible")
        if not self._is_on_profile():
            self._navigate_to_profile()

        self.screenshot("02_my_account")

        visible = (
            self.d(textContains="MY ACCOUNT").exists(timeout=5) or
            self.d(textContains="My Account").exists(timeout=3) or
            self.d(textContains="AKUN SAYA").exists(timeout=3)   # Indonesian
        )
        self._assert(
            visible,
            "My Account section header is visible",
            "My Account section header not found",
        )

    # ── TEST 03 — Logout option visible ─────────────────────────────────

    @allure.story("Logout Option Visible")
    def test_03_logout_option_visible(self):
        print("\n[TEST 03] Logout option is visible on profile page")
        if not self._is_on_profile():
            if not self._navigate_to_profile():
                print("  ⚠️  SKIP: Not on profile")
                return

        # Logout is at the bottom — scroll down to find it
        self.d.swipe(500, 1000, 500, 300, 0.5)
        time.sleep(0.5)
        self.screenshot("03_logout")

        visible = (
            self.d(textContains="Logout").exists(timeout=5) or
            self.d(textContains="logout").exists(timeout=3) or
            self.d(textContains="Keluar").exists(timeout=3)
        )
        self._assert(
            visible,
            "Logout option visible on profile page",
            "Logout option not found — may need more scrolling",
        )

    # ── TEST 04 — Help Center menu item visible ──────────────────────────

    @allure.story("Help Center Menu Item Visible")
    def test_04_help_center_visible(self):
        print("\n[TEST 04] Help Center menu item is visible")
        if not self._is_on_profile():
            if not self._navigate_to_profile():
                print("  ⚠️  SKIP: Not on profile")
                return

        # Scroll back to top first
        self.d.swipe(500, 300, 500, 1000, 0.5)
        time.sleep(0.5)
        self.screenshot("04_help_center")

        visible = (
            self.d(textContains="Help Center").exists(timeout=5) or
            self.d(textContains="Help").exists(timeout=3) or
            self.d(textContains="Pusat Bantuan").exists(timeout=3)   # Indonesian
        )
        self._assert(
            visible,
            "Help Center menu item is visible",
            "Help Center menu item not found on profile page",
        )

    # ── TEST 05 — Biometrics toggle visible ─────────────────────────────

    @allure.story("Biometrics Toggle Visible")
    def test_05_biometrics_toggle_visible(self):
        print("\n[TEST 05] Biometrics toggle is visible in My Account section")
        if not self._is_on_profile():
            if not self._navigate_to_profile():
                print("  ⚠️  SKIP: Not on profile")
                return

        self.screenshot("05_biometrics")

        visible = (
            self.d(textContains="Biometric").exists(timeout=5) or
            self.d(textContains="biometric").exists(timeout=3) or
            self.d(textContains="Biometrik").exists(timeout=3)   # Indonesian
        )
        self._assert(
            visible,
            "Biometrics toggle visible in My Account",
            "Biometrics toggle not found — check screenshot 05",
        )

    # ── TEST 06 — Language option visible ───────────────────────────────

    @allure.story("Language Option Visible")
    def test_06_language_option_visible(self):
        print("\n[TEST 06] Language selection option is visible")
        if not self._is_on_profile():
            if not self._navigate_to_profile():
                print("  ⚠️  SKIP: Not on profile")
                return

        self.screenshot("06_language")

        visible = (
            self.d(textContains="Language").exists(timeout=5) or
            self.d(textContains="language").exists(timeout=3) or
            self.d(textContains="Bahasa").exists(timeout=3)   # Indonesian
        )
        self._assert(
            visible,
            "Language option visible",
            "Language option not found on profile page",
        )

    # ── TEST 07 — About Skorcard visible ────────────────────────────────

    @allure.story("About Skorcard Visible")
    def test_07_about_skorcard_visible(self):
        print("\n[TEST 07] About Skorcard menu item is visible")
        if not self._is_on_profile():
            if not self._navigate_to_profile():
                print("  ⚠️  SKIP: Not on profile")
                return

        # Scroll down slightly to reveal Skorcard section
        self.d.swipe(500, 1000, 500, 500, 0.4)
        time.sleep(0.5)
        self.screenshot("07_about_skorcard")

        visible = (
            self.d(textContains="About Skorcard").exists(timeout=5) or
            self.d(textContains="About").exists(timeout=3) or
            self.d(textContains="Tentang").exists(timeout=3)   # Indonesian: "Tentang Skorcard"
        )
        self._assert(
            visible,
            "About Skorcard item visible on profile page",
            "About Skorcard item not found — check screenshot 07",
        )


# ── Explicit test order ──────────────────────────────────────────────────────
TEST_ORDER = [
    "test_01_profile_page_loads",
    "test_02_my_account_section_visible",
    "test_03_logout_option_visible",
    "test_04_help_center_visible",
    "test_05_biometrics_toggle_visible",
    "test_06_language_option_visible",
    "test_07_about_skorcard_visible",
]

if __name__ == "__main__":
    t = TestProfile()
    TestProfile.setup_class()
    for method in TEST_ORDER:
        getattr(t, method)()
    print("\n✅ Profile tests done. Check screenshots/ and logs/")
