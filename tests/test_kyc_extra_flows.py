#!/usr/bin/env python3
"""
Tests for KYC Extra Flows.
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
from pages.kyc_extra_flows_pages import (
    CardSelectionPage, MartialReligionFlowPage,
    PhoneNumberChangeFlowPage, PoliticalPersonSelectionPage
)

@allure.feature("KYC Extra Flows")
class TestKycExtraFlows(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.logger = get_logger("kyc_extra_flows")
        cls.pages = [
            ("Card Selection", CardSelectionPage(cls.d), "click_continue"),
            ("Marital & Religion", MartialReligionFlowPage(cls.d), "click_submit"),
            ("Phone Number Change", PhoneNumberChangeFlowPage(cls.d), "click_submit"),
            ("Political Person", PoliticalPersonSelectionPage(cls.d), "click_submit"),
        ]

    def _log_pass(self, msg):
        print(f"  ✅ PASS: {msg}")
        self.logger.info(f"PASS: {msg}")

    def _log_fail(self, msg):
        print(f"  ❌ FAIL: {msg}")
        self.logger.error(f"FAIL: {msg}")

    @allure.story("Dynamic Check for KYC Extra Flows")
    def test_kyc_extra_flows(self):
        print("\n[TEST] Checking all KYC extra flows pages functionality")
        for name, page, action in self.pages:
            if page.is_visible(timeout=2):
                self.screenshot(f"kyc_{name.replace(' ', '_')}")
                method = getattr(page, action)
                clicked = method()
                if clicked:
                    self._log_pass(f"Interacted with {name}")
                else:
                    self._log_fail(f"Could not interact with {name}")
            else:
                print(f"  ℹ️  SKIP: {name} page not visible.")

if __name__ == "__main__":
    t = TestKycExtraFlows()
    TestKycExtraFlows.setup_class()
    t.test_kyc_extra_flows()
    print("\n✅ KYC Extra Flows tests done.")
