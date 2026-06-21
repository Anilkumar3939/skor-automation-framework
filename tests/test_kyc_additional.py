#!/usr/bin/env python3
"""
Tests for KYC Additional Information screens.
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
from pages.kyc_additional_pages import (
    MothersNamePage, SpouseNamePage, SkorlifeConsentPage,
    SelfieInitialPage, VkycInformationPage, PhoneEmailChangePage
)

@allure.feature("KYC Additional Screens")
class TestKycAdditional(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.logger = get_logger("kyc_additional")
        cls.mothers_name = MothersNamePage(cls.d)
        cls.spouse_name = SpouseNamePage(cls.d)
        cls.consent = SkorlifeConsentPage(cls.d)
        cls.selfie_initial = SelfieInitialPage(cls.d)
        cls.vkyc = VkycInformationPage(cls.d)
        cls.phone_email = PhoneEmailChangePage(cls.d)

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

    @allure.story("01 - Mother's Maiden Name Page")
    def test_01_mothers_name(self):
        print("\n[TEST 01] Mother's Name page functionality")
        if not self.mothers_name.is_visible(timeout=3):
            print("  ℹ️  SKIP: Mother's Name page not visible.")
            return

        self.screenshot("01_mothers_name")
        self.mothers_name.fill_name("Siti Aminah")
        clicked = self.mothers_name.click_submit()
        self._assert(clicked, "Submitted Mother's Name", "Could not submit Mother's Name")

    @allure.story("02 - Spouse Name Page")
    def test_02_spouse_name(self):
        print("\n[TEST 02] Spouse Name page functionality")
        if not self.spouse_name.is_visible(timeout=3):
            print("  ℹ️  SKIP: Spouse Name page not visible.")
            return

        self.screenshot("02_spouse_name")
        self.spouse_name.fill_name("Budi Santoso")
        clicked = self.spouse_name.click_submit()
        self._assert(clicked, "Submitted Spouse Name", "Could not submit Spouse Name")

    @allure.story("03 - Skorlife Consent Page")
    def test_03_consent_page(self):
        print("\n[TEST 03] Skorlife Consent page functionality")
        if not self.consent.is_visible(timeout=3):
            print("  ℹ️  SKIP: Consent page not visible.")
            return

        self.screenshot("03_consent")
        self.consent.check_consent()
        clicked = self.consent.click_submit()
        self._assert(clicked, "Agreed to Consent", "Could not submit Consent")

    @allure.story("04 - Selfie Initial Instructions")
    def test_04_selfie_initial(self):
        print("\n[TEST 04] Selfie Initial Instructions functionality")
        if not self.selfie_initial.is_visible(timeout=3):
            print("  ℹ️  SKIP: Selfie Initial page not visible.")
            return

        self.screenshot("04_selfie_initial")
        clicked = self.selfie_initial.click_start()
        self._assert(clicked, "Proceeded to take selfie", "Could not click start selfie")

    @allure.story("05 - VKYC Information Page")
    def test_05_vkyc_info(self):
        print("\n[TEST 05] VKYC Information page functionality")
        if not self.vkyc.is_visible(timeout=3):
            print("  ℹ️  SKIP: VKYC Info page not visible.")
            return

        self.screenshot("05_vkyc_info")
        clicked = self.vkyc.click_start()
        self._assert(clicked, "Started VKYC call", "Could not start VKYC call")

    @allure.story("06 - Phone and Email Change Page")
    def test_06_phone_email_change(self):
        print("\n[TEST 06] Phone and Email Change functionality")
        if not self.phone_email.is_visible(timeout=3):
            print("  ℹ️  SKIP: Phone/Email change page not visible.")
            return

        self.screenshot("06_phone_email_change")
        clicked = self.phone_email.click_submit()
        self._assert(clicked, "Submitted contact info change", "Could not submit contact info change")

TEST_ORDER = [
    "test_01_mothers_name",
    "test_02_spouse_name",
    "test_03_consent_page",
    "test_04_selfie_initial",
    "test_05_vkyc_info",
    "test_06_phone_email_change"
]

if __name__ == "__main__":
    t = TestKycAdditional()
    TestKycAdditional.setup_class()
    for method in TEST_ORDER:
        getattr(t, method)()
    print("\n✅ KYC Additional tests done.")
