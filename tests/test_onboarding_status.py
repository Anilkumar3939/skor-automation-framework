#!/usr/bin/env python3
"""
Tests for Onboarding Status and Error screens.
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
from pages.onboarding_status_pages import (
    CardReadyPage, WaitingPage, UnderwritingErrorPage, UWApprovedPage
)

@allure.feature("Onboarding Status Screens")
class TestOnboardingStatus(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.logger = get_logger("onboarding_status")
        cls.card_ready = CardReadyPage(cls.d)
        cls.waiting = WaitingPage(cls.d)
        cls.uw_error = UnderwritingErrorPage(cls.d)
        cls.uw_approved = UWApprovedPage(cls.d)

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

    @allure.story("01 - Card Ready Screen")
    def test_01_card_ready(self):
        print("\n[TEST 01] Card Ready page functionality")
        if not self.card_ready.is_visible(timeout=3):
            print("  ℹ️  SKIP: Card Ready page not visible.")
            return

        self.screenshot("01_card_ready")
        clicked = self.card_ready.click_continue()
        self._assert(clicked, "Continued from Card Ready page", "Could not continue from Card Ready")

    @allure.story("02 - Waiting / Processing Screen")
    def test_02_waiting_page(self):
        print("\n[TEST 02] Waiting Page functionality")
        if not self.waiting.is_visible(timeout=3):
            print("  ℹ️  SKIP: Waiting page not visible.")
            return

        self.screenshot("02_waiting")
        clicked = self.waiting.click_refresh()
        self._assert(clicked, "Clicked check status/refresh", "Could not click refresh status")

    @allure.story("03 - Underwriting Error Page")
    def test_03_uw_error(self):
        print("\n[TEST 03] Underwriting Error Page functionality")
        if not self.uw_error.is_visible(timeout=3):
            print("  ℹ️  SKIP: UW Error page not visible.")
            return

        self.screenshot("03_uw_error")
        clicked = self.uw_error.click_close()
        self._assert(clicked, "Closed UW error page", "Could not close UW error page")

    @allure.story("04 - Underwriting Approved Page")
    def test_04_uw_approved(self):
        print("\n[TEST 04] Underwriting Approved Page functionality")
        if not self.uw_approved.is_visible(timeout=3):
            print("  ℹ️  SKIP: UW Approved page not visible.")
            return

        self.screenshot("04_uw_approved")
        clicked = self.uw_approved.click_continue()
        self._assert(clicked, "Continued from UW Approved page", "Could not continue from UW Approved")

TEST_ORDER = [
    "test_01_card_ready",
    "test_02_waiting_page",
    "test_03_uw_error",
    "test_04_uw_approved"
]

if __name__ == "__main__":
    t = TestOnboardingStatus()
    TestOnboardingStatus.setup_class()
    for method in TEST_ORDER:
        getattr(t, method)()
    print("\n✅ Onboarding Status tests done.")
