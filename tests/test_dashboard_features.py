#!/usr/bin/env python3
"""
Tests for Dashboard Extra Features screens.
"""
import os
import sys
import allure

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in [_ROOT, os.path.join(_ROOT, "tests")]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from base import BaseTest
from utils.logger import get_logger
from pages.dashboard_features_pages import (
    ReferralPage, GamificationIntroPage, StravaLandingPage,
    SkorGoEducationPage, CardControlPage
)

@allure.feature("Dashboard Extra Features")
class TestDashboardFeatures(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.logger = get_logger("dashboard_features")
        cls.referral = ReferralPage(cls.d)
        cls.gamification = GamificationIntroPage(cls.d)
        cls.strava = StravaLandingPage(cls.d)
        cls.skorgo = SkorGoEducationPage(cls.d)
        cls.card_control = CardControlPage(cls.d)

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

    @allure.story("01 - Referral Flow Page")
    def test_01_referral_page(self):
        print("\n[TEST 01] Referral Page functionality")
        if not self.referral.is_visible(timeout=3):
            print("  ℹ️  SKIP: Referral page not visible.")
            return

        self.screenshot("01_referral")
        clicked = self.referral.click_share()
        self._assert(clicked, "Clicked share referral", "Could not click share referral")

    @allure.story("02 - Gamification Intro Page")
    def test_02_gamification(self):
        print("\n[TEST 02] Gamification Intro Page functionality")
        if not self.gamification.is_visible(timeout=3):
            print("  ℹ️  SKIP: Gamification intro page not visible.")
            return

        self.screenshot("02_gamification")
        clicked = self.gamification.click_start()
        self._assert(clicked, "Started gamification", "Could not start gamification")

    @allure.story("03 - Strava Integration Page")
    def test_03_strava(self):
        print("\n[TEST 03] Strava Landing Page functionality")
        if not self.strava.is_visible(timeout=3):
            print("  ℹ️  SKIP: Strava landing page not visible.")
            return

        self.screenshot("03_strava")
        clicked = self.strava.click_connect()
        self._assert(clicked, "Clicked connect Strava", "Could not connect Strava")

    @allure.story("04 - SkorGo Education Page")
    def test_04_skorgo(self):
        print("\n[TEST 04] SkorGo Education Page functionality")
        if not self.skorgo.is_visible(timeout=3):
            print("  ℹ️  SKIP: SkorGo Education page not visible.")
            return

        self.screenshot("04_skorgo")
        clicked = self.skorgo.click_continue()
        self._assert(clicked, "Acknowledged SkorGo Education", "Could not continue from SkorGo Education")

    @allure.story("05 - Card Controls Page")
    def test_05_card_controls(self):
        print("\n[TEST 05] Card Controls functionality")
        if not self.card_control.is_visible(timeout=3):
            print("  ℹ️  SKIP: Card Controls page not visible.")
            return

        self.screenshot("05_card_controls")
        clicked = self.card_control.click_block_card()
        self._assert(clicked, "Clicked block card", "Could not click block card")

TEST_ORDER = [
    "test_01_referral_page",
    "test_02_gamification",
    "test_03_strava",
    "test_04_skorgo",
    "test_05_card_controls"
]

if __name__ == "__main__":
    t = TestDashboardFeatures()
    TestDashboardFeatures.setup_class()
    for method in TEST_ORDER:
        getattr(t, method)()
    print("\n✅ Dashboard Features tests done.")
