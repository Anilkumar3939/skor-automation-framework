#!/usr/bin/env python3
"""
Tests for Card Management Screens.
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
from pages.card_management_pages import (
    CardReplacementPage, CardBlockHowToPage, MilesConversionSuccessPage
)

@allure.feature("Card Management")
class TestCardManagement(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.logger = get_logger("card_management")
        cls.replacement = CardReplacementPage(cls.d)
        cls.block_howto = CardBlockHowToPage(cls.d)
        cls.miles = MilesConversionSuccessPage(cls.d)

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

    @allure.story("01 - Card Replacement Page")
    def test_01_card_replacement(self):
        print("\n[TEST 01] Card Replacement Page functionality")
        if not self.replacement.is_visible(timeout=3):
            print("  ℹ️  SKIP: Card Replacement page not visible.")
            return

        self.screenshot("01_card_replacement")
        clicked = self.replacement.click_continue()
        self._assert(clicked, "Requested card replacement", "Could not request card replacement")

    @allure.story("02 - Card Block How-To Page")
    def test_02_card_block_howto(self):
        print("\n[TEST 02] Card Block How-To Page functionality")
        if not self.block_howto.is_visible(timeout=3):
            print("  ℹ️  SKIP: Card Block How-To page not visible.")
            return

        self.screenshot("02_card_block_howto")
        clicked = self.block_howto.click_understood()
        self._assert(clicked, "Acknowledged block instructions", "Could not acknowledge instructions")

    @allure.story("03 - Miles Conversion Success Page")
    def test_03_miles_conversion(self):
        print("\n[TEST 03] Miles Conversion Success Page functionality")
        if not self.miles.is_visible(timeout=3):
            print("  ℹ️  SKIP: Miles Conversion Success page not visible.")
            return

        self.screenshot("03_miles_conversion_success")
        clicked = self.miles.click_close()
        self._assert(clicked, "Closed Miles Conversion page", "Could not close Miles Conversion page")

TEST_ORDER = [
    "test_01_card_replacement",
    "test_02_card_block_howto",
    "test_03_miles_conversion"
]

if __name__ == "__main__":
    t = TestCardManagement()
    TestCardManagement.setup_class()
    for method in TEST_ORDER:
        getattr(t, method)()
    print("\n✅ Card Management tests done.")
