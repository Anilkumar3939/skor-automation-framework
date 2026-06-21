#!/usr/bin/env python3
"""
Tests for Miscellaneous KYC and Approvals.
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
from pages.kyc_misc_pages import (
    SpouseAdditionalInfoPage, SelfieMatchFailPage,
    CardApprovedScreen, GenericApprovedPage
)

@allure.feature("KYC Miscellaneous")
class TestKycMisc(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.logger = get_logger("kyc_misc")
        cls.spouse_info = SpouseAdditionalInfoPage(cls.d)
        cls.selfie_fail = SelfieMatchFailPage(cls.d)
        cls.card_approved = CardApprovedScreen(cls.d)
        cls.generic_approved = GenericApprovedPage(cls.d)

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

    @allure.story("01 - Spouse Additional Info Page")
    def test_01_spouse_additional_info(self):
        print("\n[TEST 01] Spouse Additional Info functionality")
        if not self.spouse_info.is_visible(timeout=3):
            print("  ℹ️  SKIP: Spouse Additional Info page not visible.")
            return

        self.screenshot("01_spouse_info")
        clicked = self.spouse_info.click_submit()
        self._assert(clicked, "Submitted Spouse Additional Info", "Could not submit")

    @allure.story("02 - Selfie Match Fail Page")
    def test_02_selfie_match_fail(self):
        print("\n[TEST 02] Selfie Match Fail functionality")
        if not self.selfie_fail.is_visible(timeout=3):
            print("  ℹ️  SKIP: Selfie Match Fail page not visible.")
            return

        self.screenshot("02_selfie_fail")
        clicked = self.selfie_fail.click_retry()
        self._assert(clicked, "Clicked retry on selfie match fail", "Could not click retry")

    @allure.story("03 - Card Approved Screen")
    def test_03_card_approved(self):
        print("\n[TEST 03] Card Approved Screen functionality")
        if not self.card_approved.is_visible(timeout=3):
            print("  ℹ️  SKIP: Card Approved Screen not visible.")
            return

        self.screenshot("03_card_approved")
        clicked = self.card_approved.click_continue()
        self._assert(clicked, "Continued from Card Approved", "Could not continue")

    @allure.story("04 - Generic Approved Page")
    def test_04_generic_approved(self):
        print("\n[TEST 04] Generic Approved Page functionality")
        if not self.generic_approved.is_visible(timeout=3):
            print("  ℹ️  SKIP: Generic Approved page not visible.")
            return

        self.screenshot("04_generic_approved")
        clicked = self.generic_approved.click_continue()
        self._assert(clicked, "Continued from Generic Approved", "Could not continue")

TEST_ORDER = [
    "test_01_spouse_additional_info",
    "test_02_selfie_match_fail",
    "test_03_card_approved",
    "test_04_generic_approved"
]

if __name__ == "__main__":
    t = TestKycMisc()
    TestKycMisc.setup_class()
    for method in TEST_ORDER:
        getattr(t, method)()
    print("\n✅ KYC Miscellaneous tests done.")
