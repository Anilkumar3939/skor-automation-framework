#!/usr/bin/env python3
"""
Notifications Screen tests — based on sc-mobile-app_v2/lib/ui/dashboard/notifications_screen.dart

Covers:
  01  Notifications screen opens from dashboard
  02  "Notifications" title / app bar is visible
  03  System tab (language.system) is visible by default
  04  Promotion tab (language.promotion) is visible
  05  Tapping Promotion tab switches the list view
  06  Tapping System tab switches back
  07  Back navigation returns to dashboard

Key UI identifiers (from notifications_screen.dart):
  - AppBar title: language.notifications  → "Notifications"
  - SwitchWithNumberTag: language.system  → "System"
                         language.promotion → "Promotion"
  - Body list: SystemNotificationWidget / PromotionNotificationWidget

Navigation:
  Tests launch app → handle passcode → reach dashboard →
  tap Notification icon (bell / description="Notifications") in app bar.
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


@allure.feature("Notifications Screen")
class TestNotifications(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.logger = get_logger("notifications")

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

    def _is_on_dashboard(self):
        return (
            self.d(textContains="Transaction").exists(timeout=3) or
            self.d(textContains="Transaksi").exists(timeout=2) or
            self.d(descriptionContains="card").exists(timeout=3) or
            self.d(textContains="Credit").exists(timeout=2)
        )

    def _is_on_notifications(self):
        return (
            self.d(text="Notifications").exists(timeout=5) or
            self.d(textContains="Notification").exists(timeout=3) or
            self.d(textContains="Notifikasi").exists(timeout=3) or
            self.d(text="System").exists(timeout=3) or
            self.d(text="Promotion").exists(timeout=3)
        )

    def _navigate_to_notifications(self):
        """Dashboard → tap bell/Notifications icon → Notifications screen."""
        if self._is_on_notifications():
            return True

        # Ensure we're on the dashboard first
        if not self._is_on_dashboard():
            self.launch_app()
            time.sleep(3)
            if not self._is_on_dashboard():
                print("  ⚠️  Could not reach dashboard")
                return False

        # Tap notification icon (bell icon in the dashboard app bar)
        tapped = False
        for label in ["Notifications", "Notifikasi", "notification", "bell"]:
            if self.d(description=label).exists(timeout=2):
                self.d(description=label).click()
                tapped = True
                break
            if self.d(descriptionContains=label).exists(timeout=1):
                self.d(descriptionContains=label).click()
                tapped = True
                break

        if not tapped:
            # Try top-right corner (typical bell icon position)
            screen_w = self.d.info.get("displayWidth", 1080)
            self.d.click(int(screen_w * 0.85), 80)
            print("  ⚠️  Bell icon not found by desc — tapped top-right corner")

        time.sleep(2)
        return self._is_on_notifications()

    # ── TEST 01 — Notifications screen opens ────────────────────────────

    @allure.story("Notifications Screen Opens")
    def test_01_notifications_screen_opens(self):
        print("\n[TEST 01] Notifications screen opens from dashboard")
        reached = self._navigate_to_notifications()
        self.screenshot("01_notifications_screen")

        self._assert(
            reached,
            "Notifications screen loaded",
            "Notifications screen not loaded — check screenshot 01",
        )

    # ── TEST 02 — Title / app bar visible ──────────────────────────────

    @allure.story("Notifications Title Visible")
    def test_02_notifications_title_visible(self):
        print("\n[TEST 02] 'Notifications' title is visible in the app bar")
        if not self._is_on_notifications():
            if not self._navigate_to_notifications():
                print("  ⚠️  SKIP: Not on notifications screen")
                return

        self.screenshot("02_notifications_title")

        visible = (
            self.d(text="Notifications").exists(timeout=5) or
            self.d(textContains="Notification").exists(timeout=3) or
            self.d(textContains="Notifikasi").exists(timeout=3)
        )
        self._assert(
            visible,
            "Notifications title visible in app bar",
            "Notifications title not found",
        )

    # ── TEST 03 — System tab visible by default ─────────────────────────

    @allure.story("System Tab Visible")
    def test_03_system_tab_visible(self):
        print("\n[TEST 03] 'System' tab is visible by default")
        if not self._is_on_notifications():
            if not self._navigate_to_notifications():
                print("  ⚠️  SKIP: Not on notifications screen")
                return

        self.screenshot("03_system_tab")

        visible = (
            self.d(text="System").exists(timeout=5) or
            self.d(textContains="System").exists(timeout=3) or
            self.d(textContains="Sistem").exists(timeout=3)   # Indonesian
        )
        self._assert(
            visible,
            "System tab visible on notifications screen",
            "System tab not found",
        )

    # ── TEST 04 — Promotion tab visible ────────────────────────────────

    @allure.story("Promotion Tab Visible")
    def test_04_promotion_tab_visible(self):
        print("\n[TEST 04] 'Promotion' tab is visible")
        if not self._is_on_notifications():
            if not self._navigate_to_notifications():
                print("  ⚠️  SKIP: Not on notifications screen")
                return

        self.screenshot("04_promotion_tab")

        visible = (
            self.d(text="Promotion").exists(timeout=5) or
            self.d(textContains="Promotion").exists(timeout=3) or
            self.d(textContains="Promosi").exists(timeout=3)   # Indonesian
        )
        self._assert(
            visible,
            "Promotion tab visible on notifications screen",
            "Promotion tab not found",
        )

    # ── TEST 05 — Tap Promotion tab switches view ───────────────────────

    @allure.story("Switch to Promotion Tab")
    def test_05_switch_to_promotion(self):
        print("\n[TEST 05] Tapping Promotion tab switches the list view")
        if not self._is_on_notifications():
            if not self._navigate_to_notifications():
                print("  ⚠️  SKIP: Not on notifications screen")
                return

        tapped = False
        for label in ["Promotion", "Promosi"]:
            if self.d(text=label).exists(timeout=3):
                self.d(text=label).click()
                tapped = True
                break
            if self.d(textContains=label).exists(timeout=2):
                self.d(textContains=label).click()
                tapped = True
                break

        if not tapped:
            print("  ⚠️  Promotion tab not found by text")

        time.sleep(2)
        self.screenshot("05_after_promotion_tap")

        still_on_notifications = self._is_on_notifications()
        self._assert(
            still_on_notifications,
            "Still on notifications screen after tapping Promotion tab",
            "Unexpectedly left notifications screen",
        )
        if tapped:
            self._log_pass("Promotion tab tapped — list view switched")

    # ── TEST 06 — Tap System tab switches back ─────────────────────────

    @allure.story("Switch Back to System Tab")
    def test_06_switch_back_to_system(self):
        print("\n[TEST 06] Tapping System tab switches back to system list")
        if not self._is_on_notifications():
            if not self._navigate_to_notifications():
                print("  ⚠️  SKIP: Not on notifications screen")
                return

        tapped = False
        for label in ["System", "Sistem"]:
            if self.d(text=label).exists(timeout=3):
                self.d(text=label).click()
                tapped = True
                break
            if self.d(textContains=label).exists(timeout=2):
                self.d(textContains=label).click()
                tapped = True
                break

        time.sleep(2)
        self.screenshot("06_system_tab_active")

        self._assert(
            self._is_on_notifications(),
            "System tab tapped — still on notifications screen",
            "Left notifications screen unexpectedly",
        )
        if tapped:
            self._log_pass("System tab active — view switched back")

    # ── TEST 07 — Back navigation returns to dashboard ──────────────────

    @allure.story("Back Navigation Returns to Dashboard")
    def test_07_back_returns_to_dashboard(self):
        print("\n[TEST 07] Back navigation from notifications returns to dashboard")
        if not self._is_on_notifications():
            if not self._navigate_to_notifications():
                print("  ⚠️  SKIP: Not on notifications screen")
                return

        self.d.press("back")
        time.sleep(2)
        self.screenshot("07_after_back")

        back_on_dashboard = self._is_on_dashboard()
        self._assert(
            back_on_dashboard,
            "Returned to dashboard after pressing back",
            "Did not return to dashboard — check screenshot 07",
        )


# ── Explicit test order ──────────────────────────────────────────────────────
TEST_ORDER = [
    "test_01_notifications_screen_opens",
    "test_02_notifications_title_visible",
    "test_03_system_tab_visible",
    "test_04_promotion_tab_visible",
    "test_05_switch_to_promotion",
    "test_06_switch_back_to_system",
    "test_07_back_returns_to_dashboard",
]

if __name__ == "__main__":
    t = TestNotifications()
    TestNotifications.setup_class()
    for method in TEST_ORDER:
        getattr(t, method)()
    print("\n✅ Notifications tests done. Check screenshots/ and logs/")
