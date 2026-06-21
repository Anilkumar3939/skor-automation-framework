#!/usr/bin/env python3
"""
Tests for Final Catch-All Miscellaneous Screens.
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
from pages.final_catchall_pages import (
    ErrorInfoPage, ErrorReasonViewPage, GeneralErrorPage,
    SkorlifeWaitlistPage, UnderwritingErrorCarouselPage,
    CardOnFileMerchantsPage, DashboardApprovalV2Page,
    KycSuccessVerificationV2Page, EmergencyContactV2Page,
    SelfieCameraImagePreviewPage, WaitlistInfoViewPage
)

@allure.feature("Final Catch-All Miscellaneous Screens")
class TestFinalCatchall(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.logger = get_logger("final_catchall")
        cls.pages = [
            ("Error Info", ErrorInfoPage(cls.d), "click_close"),
            ("Error Reason View", ErrorReasonViewPage(cls.d), "click_close"),
            ("General Error", GeneralErrorPage(cls.d), "click_retry"),
            ("Skorlife Waitlist", SkorlifeWaitlistPage(cls.d), "click_continue"),
            ("Underwriting Error Carousel", UnderwritingErrorCarouselPage(cls.d), "swipe_carousel"),
            ("Card On File Merchants", CardOnFileMerchantsPage(cls.d), "go_back"),
            ("Dashboard Approval V2", DashboardApprovalV2Page(cls.d), "click_continue"),
            ("KYC Success Verification V2", KycSuccessVerificationV2Page(cls.d), "click_continue"),
            ("Emergency Contact V2", EmergencyContactV2Page(cls.d), "click_submit"),
            ("Selfie Camera Image Preview", SelfieCameraImagePreviewPage(cls.d), "click_retake"),
            ("Waitlist Info View", WaitlistInfoViewPage(cls.d), "click_close"),
        ]

    def _log_pass(self, msg):
        print(f"  ✅ PASS: {msg}")
        self.logger.info(f"PASS: {msg}")

    def _log_fail(self, msg):
        print(f"  ❌ FAIL: {msg}")
        self.logger.error(f"FAIL: {msg}")

    @allure.story("Dynamic Check for Final Catch-All Pages")
    def test_final_catchall_pages(self):
        print("\n[TEST] Checking all final catch-all pages functionality")
        for name, page, action in self.pages:
            if page.is_visible(timeout=2):
                self.screenshot(f"catchall_{name.replace(' ', '_')}")
                method = getattr(page, action)
                clicked = method()
                if clicked:
                    self._log_pass(f"Interacted with {name}")
                else:
                    self._log_fail(f"Could not interact with {name}")
            else:
                print(f"  ℹ️  SKIP: {name} page not visible.")

if __name__ == "__main__":
    t = TestFinalCatchall()
    TestFinalCatchall.setup_class()
    t.test_final_catchall_pages()
    print("\n✅ Final Catch-All tests done.")
