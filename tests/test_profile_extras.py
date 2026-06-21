#!/usr/bin/env python3
"""
Tests for Profile Extras.
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
from pages.profile_extras_pages import (
    CardChargesPage, ChangeLanguagePage, HelpCenterPage,
    ResetCreditCardPinPage, GenericWebViewPage
)

@allure.feature("Profile Extras and Settings")
class TestProfileExtras(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.logger = get_logger("profile_extras")
        cls.pages = [
            ("Card Charges", CardChargesPage(cls.d), "go_back"),
            ("Change Language", ChangeLanguagePage(cls.d), "go_back"),
            ("Help Center", HelpCenterPage(cls.d), "go_back"),
            ("Reset Credit Card PIN", ResetCreditCardPinPage(cls.d), "go_back"),
            ("Generic Web View", GenericWebViewPage(cls.d), "go_back"),
        ]

    def _log_pass(self, msg):
        print(f"  ✅ PASS: {msg}")
        self.logger.info(f"PASS: {msg}")

    def _log_fail(self, msg):
        print(f"  ❌ FAIL: {msg}")
        self.logger.error(f"FAIL: {msg}")

    @allure.story("Dynamic Check for Profile & Settings Pages")
    def test_profile_extras(self):
        print("\n[TEST] Checking all profile & settings pages functionality")
        for name, page, action in self.pages:
            if page.is_visible(timeout=2):
                self.screenshot(f"prof_{name.replace(' ', '_')}")
                method = getattr(page, action)
                clicked = method()
                if clicked:
                    self._log_pass(f"Interacted with {name}")
                else:
                    self._log_fail(f"Could not interact with {name}")
            else:
                print(f"  ℹ️  SKIP: {name} page not visible.")

if __name__ == "__main__":
    t = TestProfileExtras()
    TestProfileExtras.setup_class()
    t.test_profile_extras()
    print("\n✅ Profile Extras tests done.")
