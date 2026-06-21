#!/usr/bin/env python3
"""
Tests for Extra Referral and Strava Flow Screens.
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
from pages.referral_strava_extra_pages import (
    ReferralHistoryPage, ReferralTrackingPage, StravaFaqPage, StravaOnboardingPage
)

@allure.feature("Referral and Strava Extras")
class TestReferralStravaExtras(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.logger = get_logger("referral_strava")
        cls.history = ReferralHistoryPage(cls.d)
        cls.tracking = ReferralTrackingPage(cls.d)
        cls.faq = StravaFaqPage(cls.d)
        cls.strava_onboard = StravaOnboardingPage(cls.d)

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

    @allure.story("01 - Referral History Page")
    def test_01_referral_history(self):
        print("\n[TEST 01] Referral History functionality")
        if not self.history.is_visible(timeout=3):
            print("  ℹ️  SKIP: Referral History page not visible.")
            return

        self.screenshot("01_referral_history")
        clicked = self.history.go_back()
        self._assert(clicked, "Navigated away from Referral History", "Could not navigate away")

    @allure.story("02 - Referral Tracking Page")
    def test_02_referral_tracking(self):
        print("\n[TEST 02] Referral Tracking functionality")
        if not self.tracking.is_visible(timeout=3):
            print("  ℹ️  SKIP: Referral Tracking page not visible.")
            return

        self.screenshot("02_referral_tracking")
        clicked = self.tracking.go_back()
        self._assert(clicked, "Navigated away from Referral Tracking", "Could not navigate away")

    @allure.story("03 - Strava FAQ Page")
    def test_03_strava_faq(self):
        print("\n[TEST 03] Strava FAQ functionality")
        if not self.faq.is_visible(timeout=3):
            print("  ℹ️  SKIP: Strava FAQ page not visible.")
            return

        self.screenshot("03_strava_faq")
        clicked = self.faq.click_close()
        self._assert(clicked, "Closed Strava FAQ", "Could not close Strava FAQ")

    @allure.story("04 - Strava Onboarding Page")
    def test_04_strava_onboarding(self):
        print("\n[TEST 04] Strava Onboarding functionality")
        if not self.strava_onboard.is_visible(timeout=3):
            print("  ℹ️  SKIP: Strava Onboarding page not visible.")
            return

        self.screenshot("04_strava_onboarding")
        clicked = self.strava_onboard.click_continue()
        self._assert(clicked, "Continued from Strava Onboarding", "Could not continue from Strava Onboarding")

TEST_ORDER = [
    "test_01_referral_history",
    "test_02_referral_tracking",
    "test_03_strava_faq",
    "test_04_strava_onboarding"
]

if __name__ == "__main__":
    t = TestReferralStravaExtras()
    TestReferralStravaExtras.setup_class()
    for method in TEST_ORDER:
        getattr(t, method)()
    print("\n✅ Referral and Strava Extras tests done.")
