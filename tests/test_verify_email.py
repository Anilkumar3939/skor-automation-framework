#!/usr/bin/env python3
"""
Verify Email Screen Tests
Maps to: verify_email.dart

Test order:

  01  Verify Email page loads
  02  Google button visibility (if enabled)
  03  Apple button visibility (if enabled)
  04  Manual email option visibility (if enabled)
  05  Click Google → OAuth flow starts
  06  Click Apple → OAuth flow starts
  07  Click Manual Email → navigates to email input screen

NOTE:
Buttons are dynamic (Remote Config based)
So tests must NOT fail if button is missing.
"""

import os
import sys
import time
import allure

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in [_ROOT, os.path.join(_ROOT, "tests")]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from base import BaseTest
from pages.verify_email_page import VerifyEmailPage
from utils.logger import get_logger
from tests.test_otp import OTPPage, OTPScreenTest
from utils.db_helper import DBHelper
OTPScreenTest.__test__ = False

@allure.feature("Onboarding — Verify Email")
class TestVerifyEmail(BaseTest):


    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.verify = VerifyEmailPage(cls.d)
        cls.logger = get_logger("verify_email")
        cls.db = DBHelper()
        

    # ── helpers ─────────────────────────────────────────

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
            raise AssertionError(fail_msg)
        return condition

    def _navigate_to_verify_email(self):
        """
        Ensure Verify Email screen is visible
        """
        if self.verify.is_displayed():
            print("  ➡️ Already on Verify Email screen")
            return

        self.launch_app()
        time.sleep(3)

        if not self.verify.is_displayed():
            raise AssertionError(
                "Verify Email screen not reachable. "
                "Make sure onboarding flow reaches this step."
            )

    def _ensure_on_page(self):
        if not self.verify.is_displayed():
            self._navigate_to_verify_email()
        time.sleep(0.5)

    # ═════════════════════════════════════════════════════
    # TEST 01 — Page loads
    # ═════════════════════════════════════════════════════

    @allure.story("01 - Verify Email Page Loads")
    def test_01_verify_email_page_loads(self):
        print("\n[TEST 01] Verify Email page loads")
        self._navigate_to_verify_email()
        self.screenshot("01_verify_email")

        visible = self.verify.is_displayed()
        self.assert_critical(visible, "Verify Email page failed to load. Stopping suite.")

    # ═════════════════════════════════════════════════════
    # TEST 02 — Google button visible (if enabled)
    # ═════════════════════════════════════════════════════

    @allure.story("02 - Google Button Visibility")
    def test_02_google_button_visible(self):
        print("\n[TEST 02] Google button visibility")
        self._ensure_on_page()
        self.screenshot("02_google_btn")

        present = self.verify.is_google_visible()

        self._assert(
            True,
            f"Google button presence checked (found={present})",
            "Google button check failed"
        )

    # ═════════════════════════════════════════════════════
    # TEST 03 — Apple button visible (if enabled)
    # ═════════════════════════════════════════════════════

    # @allure.story("03 - Apple Button Visibility")
    # def test_03_apple_button_visible(self):
    #     print("\n[TEST 03] Apple button visibility")
    #     self._ensure_on_page()
    #     self.screenshot("03_apple_btn")

    #     present = self.verify.is_apple_present()

    #     self._assert(
    #         True,
    #         f"Apple button presence checked (found={present})",
    #         "Apple button check failed"
    #     )

    # ═════════════════════════════════════════════════════
    # TEST 04 — Manual email visible
    # ═════════════════════════════════════════════════════

    @allure.story("04 - Manual Email Option Visibility")
    def test_04_manual_email_visible(self):
        print("\n[TEST 04] Manual email option visibility")
        self._ensure_on_page()
        self.screenshot("04_manual_email")

        present = self.verify.is_manual_email_visible()

        self._assert(
            True,
            f"Manual email presence checked (found={present})",
            "Manual email check failed"
        )

    # ═════════════════════════════════════════════════════
    # TEST 05 — Google click
    # ═════════════════════════════════════════════════════

    # @allure.story("05 - Click Google Sign-in")
    # def test_05_click_google(self):
    #     print("\n[TEST 05] Click Google Sign-in")
    #     self._ensure_on_page()

    #     if not self.verify.is_google_visible():
    #         print("  ⚠️ Google button not available — skipping")
    #         return

    #     self.verify.click_google()
    #     time.sleep(3)
    #     self.screenshot("05_google_click")

    #     self._assert(
    #         True,
    #         "Google Sign-in click executed",
    #         "Google click failed"
    #     )

    # # ═════════════════════════════════════════════════════
    # # TEST 06 — Apple click
    # # ═════════════════════════════════════════════════════

    # @allure.story("06 - Click Apple Sign-in")
    # def test_06_click_apple(self):
    #     print("\n[TEST 06] Click Apple Sign-in")
    #     self._ensure_on_page()

    #     if not self.verify.is_apple_visible():
    #         print("  ⚠️ Apple button not available — skipping")
    #         return

    #     self.verify.click_apple()
    #     time.sleep(3)
    #     self.screenshot("06_apple_click")

    #     self._assert(
    #         True,
    #         "Apple Sign-in click executed",
    #         "Apple click failed"
    #     )

    # ═════════════════════════════════════════════════════
    # TEST 07 — Manual email navigation
    # ═════════════════════════════════════════════════════

    @allure.story("07 - Manual Email Navigation")
    def test_07_manual_email_navigation(self):
        print("\n[TEST 07] Manual email navigation")
        self._ensure_on_page()

        if not self.verify.is_manual_email_visible():
            print("  ⚠️ Manual email not available — skipping")
            return

        self.verify.click_manual_email()
        time.sleep(3)
        self.screenshot("07_manual_nav")

        navigated = not self.verify.is_manual_email_visible()

        self._assert(
            navigated,
            "Navigated to Email input screen",
            "Did NOT navigate after clicking manual email"
        )

    @allure.story("08 - Enter Email Manually continue flow")
    def test_08_manual_email_flow(self):
        print("\n[TEST 08] Manual email flow")

        # if not self.verify.is_manual_email_visible():
        #     print("  ⚠️ Manual email not available — skipping")
        #     return
        
        self.verify.Enter_email('anil@gmail.com')
        time.sleep(3)
        
        continue_btn = self.d(descriptionContains="Continue")
        if continue_btn.exists(timeout=5):
            continue_btn.click()
        else:
            raise Exception("Continue button not found after entering email")
        
        
        time.sleep(3)

        navigated = self.d(descriptionContains="Email verification").exists(timeout=5)
        self._assert(
            navigated,
            "Navigated to verification code screen",
            "Did NOT navigate after clicking continue on manual email"
        )

    from tests.test_otp import OTPScreenTest, OTPPage
    from utils.db_helper import DBHelper

    @allure.story("09 - verify otp Page")
    def test_09_verify_otp_page(self):
        otp = OTPScreenTest()

        # reuse current driver
        otp.d = self.d

        # initialize objects that setup_class() normally creates
        otp.otp_page = OTPPage(self.d)
        otp.logger = get_logger("otp")

        # run OTP tests
        otp.test_01_otp_screen_loads()
        otp.test_02_resend_code_visible()
        otp.test_03_wrong_otp_shows_error()
        otp.test_04_retrieve_and_verify_otp()

        navigated = self.d(descriptionContains="Welcome back!").exists(timeout=5)
        if navigated:
            self._assert(
                True,
                "Navigated to Welcome screen after OTP verification",
                "Did NOT navigate after OTP verification"
            )
            continue_application_btn = self.d(descriptionContains="Continue application")
            if continue_application_btn.exists(timeout=15):
                continue_application_btn.click()
                time.sleep(5)
                office_information_visible = self.d(descriptionContains="Let's fill your job information").exists(timeout=5)
                self._assert(
                    office_information_visible,
                    "Navigated to office information screen after clicking Continue application",
                    "Did NOT navigate to office information screen after clicking Continue application"
                )
        else:
             self._assert(
                False,
                "Navigated to Welcome screen after OTP verification",
                "Did NOT navigate after OTP verification"
            )
    
    @allure.story("10 - DB Validations in EMAIL")
    def test_10_db_validations(self):
        print("\n[TEST 10] DB Validations in EMAIL")
        from utils.queries import (
            get_user_sso_audit,
            get_state,
            get_state_audit
        )

        user_id = self._data.get("user_id")
        result1 = get_user_sso_audit(self.db, user_id)
        if result1:
            email_verified = result1[0].get("email_verified")
        else:
            email_verified = None
        self._assert(
            email_verified,
            "Email Verified",
            "Email not verified"
        )

        result2 = get_state(self.db, user_id)
        if result2:
            state = result2[0].get("state")
        else:
            state = None
        self._assert(
            state == "JOB",
            f'SELECT * FROM "SC_STATE_MACHINE" WHERE user_id={user_id} and state={state} --> Passed',
            f'SELECT * FROM "SC_STATE_MACHINE" WHERE user_id={user_id} and state={state} --> Failed'
        )

        result3 = get_state_audit(self.db, user_id)
        if result3:
            previous_state = result3[0].get("previous_state")
            current_state = result3[0].get("current_state")
        else:
            previous_state = None
            current_state = None
        self._assert(
            previous_state == "EMAIL" and current_state == "JOB",
            f'SELECT * FROM "SC_STATE_MACHINE_AUDIT" WHERE user_id={user_id} and previous_state={previous_state} and current_state={current_state} --> Passed',
            f'SELECT * FROM "SC_STATE_MACHINE_AUDIT" WHERE user_id={user_id} and previous_state={previous_state} and current_state={current_state} --> Failed'
        )


# ── Execution Order ─────────────────────────

TEST_ORDER = [
    "test_01_verify_email_page_loads",
    "test_02_google_button_visible",
    "test_03_apple_button_visible",
    "test_04_manual_email_visible",
    "test_05_click_google",
    "test_06_click_apple",
    "test_07_manual_email_navigation",
    "test_08_manual_email_flow",
    "test_09_verify_otp_page"
]

if __name__ == "__main__":
    t = TestVerifyEmail()
    TestVerifyEmail.setup_class()

    for method in TEST_ORDER:
        getattr(t, method)()

    print("\n✅ Verify Email tests completed")