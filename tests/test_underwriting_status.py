#!/usr/bin/env python3
"""
Tests for Underwriting Status and VKYC Scheduling screens.
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
from pages.underwriting_pages import (
    PhoneVerificationPage, PhoneVerificationBookedPage, VerifyingDataPage,
    VkycVerificationBookedPage, VkycVerificationCompletedPage,
    VkycVerificationPendingPage, CardActivationPendingPage,
    ContinueApplicationPage, ReachedLimitForCardNumberPage, PinResetSuccessPage
)

@allure.feature("Underwriting and VKYC Status")
class TestUnderwritingStatus(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.logger = get_logger("underwriting_status")
        cls.pages = [
            ("Phone Verification", PhoneVerificationPage(cls.d), "click_continue"),
            ("Phone Verification Booked", PhoneVerificationBookedPage(cls.d), "click_done"),
            ("Verifying Data", VerifyingDataPage(cls.d), "click_refresh"),
            ("VKYC Verification Booked", VkycVerificationBookedPage(cls.d), "click_done"),
            ("VKYC Verification Completed", VkycVerificationCompletedPage(cls.d), "click_continue"),
            ("VKYC Verification Pending", VkycVerificationPendingPage(cls.d), "click_refresh"),
            ("Card Activation Pending", CardActivationPendingPage(cls.d), "click_ok"),
            ("Continue Application", ContinueApplicationPage(cls.d), "click_continue"),
            ("Reached Limit For Card Number", ReachedLimitForCardNumberPage(cls.d), "click_close"),
            ("PIN Reset Success", PinResetSuccessPage(cls.d), "click_done"),
        ]

    def _log_pass(self, msg):
        print(f"  ✅ PASS: {msg}")
        self.logger.info(f"PASS: {msg}")

    def _log_fail(self, msg):
        print(f"  ❌ FAIL: {msg}")
        self.logger.error(f"FAIL: {msg}")

    @allure.story("Dynamic Check for Underwriting Status Pages")
    def test_underwriting_pages(self):
        print("\n[TEST] Checking all underwriting status pages functionality")
        for name, page, action in self.pages:
            if page.is_visible(timeout=2):
                self.screenshot(f"underwriting_{name.replace(' ', '_')}")
                method = getattr(page, action)
                clicked = method()
                if clicked:
                    self._log_pass(f"Interacted with {name}")
                else:
                    self._log_fail(f"Could not interact with {name}")
            else:
                print(f"  ℹ️  SKIP: {name} page not visible.")

if __name__ == "__main__":
    t = TestUnderwritingStatus()
    TestUnderwritingStatus.setup_class()
    t.test_underwriting_pages()
    print("\n✅ Underwriting status tests done.")
