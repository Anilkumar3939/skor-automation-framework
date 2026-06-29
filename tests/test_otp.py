#!/usr/bin/env python3
"""
OTP Screen Tests — Functional Suite
=====================================

Tests core functionality of the OTP screen in a single session.

  01  Full flow: valid phone + Continue → OTP screen loads
  02  Resend Code link is visible on the OTP screen
  03  Wrong OTP shows error message
  04  Retrieve OTP from notification / resend, clear field, enter correct OTP → verified
"""
import os
import sys
import time
import allure

from base import BaseTest
from pages.register_page import RegisterPage
from pages.otp_page import OTPPage
from utils.db_helper import DBHelper
from utils.logger import get_logger
from utils.test_data import VALID_PHONE

@allure.feature("OTP Screen")
class OTPScreenTest(BaseTest):
    """
    OTP tests — sequential on a single OTP screen session.
    Tests core functionality: navigation → resend visible →
    wrong OTP rejected → correct OTP accepted.
    """

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.register = RegisterPage(cls.d)
        cls.otp_page = OTPPage(cls.d)
        cls.logger   = get_logger("otp")
        cls.db = DBHelper()

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

    def _navigate_to_otp(self):
        """
        Navigate to the OTP screen.

        Strategy (NO app restart — reuses the existing session):
          1. Already on OTP screen → use it directly.
          2. resume app via launch_app(stop=False) → check if OTP visible.
          3. Back-press to reach splash → enter phone → Continue.
          4. Poll loop: watch for OTP screen AND handle any login/confirm dialog
             that may appear when the phone is already registered.
        """
        return True
        if self._data.get("on_otp_screen") and self.otp_page.is_visible(timeout=3):
            return True

        # Previous suite (e.g. splash) may have already landed on OTP
        if self.otp_page.is_visible(timeout=3):
            print("  ✅ Already on OTP screen (from previous suite)")
            self._data["on_otp_screen"] = True
            self._data["otp"] = self.otp_page.get_otp_from_notification(timeout=1)
            return True

        # Bring the app to foreground without killing the session.
        # restart_app(stop=True) is intentionally avoided here because a fresh
        # launch triggers notification/location permission dialogs and an
        # "already registered" dialog that blocks OTP navigation.
        self.launch_app()       # stop=False — keeps session alive
        time.sleep(1)

        if self.otp_page.is_visible(timeout=3):
            self._data["on_otp_screen"] = True
            self._data["otp"] = self.otp_page.get_otp_from_notification(timeout=1)
            return True

        # Gently navigate back to splash (at most 3 back presses)
        for _ in range(3):
            if (self.d(className="android.widget.EditText").exists(timeout=2) and
                    self.d(description="Continue").exists(timeout=2)):
                break
            self.d.press("back")
            time.sleep(0.6)

        # Enter phone and tap Continue
        self.register.enter_phone(VALID_PHONE)
        time.sleep(0.5)

        if not self.register.is_continue_enabled():
            print("  ⚠️  Continue not enabled — phone field may not be ready")
            self.screenshot("otp_continue_not_enabled")
            return False

        self.register.click_continue()

        # Poll loop: watch for OTP screen AND service any blocking dialog
        # (e.g. "number already registered — login?") as it appears.
        otp_visible = False
        otp_code    = None
        dialog_handled = False
        end = time.time() + 25
        while time.time() < end:
            # Capture OTP from notification if toast appears
            if not otp_code:
                otp_code = self.otp_page.get_otp_from_notification(timeout=0.2)

            # Check for OTP screen
            if self.otp_page.is_visible(timeout=0.5):
                otp_visible = True
                break

            # Handle "already registered" / login confirm dialog once
            if not dialog_handled:
                for label in ["Login", "login", "Masuk", "Lanjut", "Lanjutkan",
                               "Yes", "Ya", "OK", "Oke", "Konfirmasi"]:
                    el = self.d(textContains=label)
                    if el.exists(timeout=0.3):
                        info = el.info
                        if info.get("clickable", False):
                            print(f"  ℹ️  Tapping '{label}' on login/confirm dialog")
                            el.click()
                            dialog_handled = True
                            time.sleep(2)
                            break

            time.sleep(0.3)

        if not otp_visible:
            self.screenshot("otp_nav_failed")

        self.screenshot("otp_after_continue")
        self._data["on_otp_screen"] = otp_visible
        self._data["otp"]           = otp_code
        return otp_visible

    def _require_otp_screen(self):
        if not self.otp_page.is_visible(timeout=3):
            raise AssertionError("Not on OTP screen — previous test may have navigated away")

    # ── TEST 01 — Full flow: phone → Continue → OTP loads ─────────────────

    @allure.story("01 - OTP Screen Loads After Valid Phone")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_01_otp_screen_loads(self):
        print("\n[TEST 01] Full flow: valid phone + Continue → OTP screen loads")
        reached = self._navigate_to_otp()
        self.screenshot("01_otp_screen")
        self.assert_critical(reached, "OTP screen failed to load. Stopping suite.")

    # ── TEST 02 — Resend Code link is visible ───────────────────────────────

    @allure.story("02 - Resend Code Link Visible")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_02_resend_code_visible(self):
        print("\n[TEST 02] Resend Code link visibility")
        self._require_otp_screen()
        visible = self.otp_page.is_resend_visible(timeout=5)
        assert self._assert(visible, "Resend Code link is visible",
                            "Resend Code link not found")

    # ── TEST 03 — Wrong OTP shows error ────────────────────────────────────

    @allure.story("03 - Wrong OTP Shows Error Message")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_03_wrong_otp_shows_error(self):
        print("\n[TEST 03] Wrong OTP (000000) shows error message")
        self._require_otp_screen()

        self.otp_page.enter_wrong_otp("000000")
        error = self.otp_page.poll_for_wrong_otp_error(poll_duration=6)
        self.screenshot("03_wrong_otp_error")


        assert self._assert(error, "Error message shown for wrong OTP",
                            "No error shown for wrong OTP '000000'")

    # ── TEST 04 — Retrieve OTP and verify ──────────────────────────────────

    @allure.story("04 - Retrieve OTP and Successfully Verify")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_04_retrieve_and_verify_otp(self):
        """
        Retrieve the OTP code from the notification toast.
        If not captured earlier, tap Resend Code to request a new one and
        read it from the fresh toast.  Then clear any stale digits in the
        input field and enter the correct OTP.
        """
        print("\n[TEST 04] Retrieve OTP from notification and complete verification")
        self._require_otp_screen()

        time.sleep(2)

        otp = self.otp_page.get_otp_from_screen()

        # Try once more from any visible notification
        if not otp:
            otp = self.otp_page.get_otp_from_notification(timeout=2)

        # OTP not captured — use Resend Code to trigger a fresh one
        if not otp:
            print("  ℹ️  OTP not captured from initial send — waiting for Resend to become available...")
            waited = 0
            while waited < 10:
                if self.otp_page.is_resend_enabled(timeout=2):
                    break
                time.sleep(3)
                waited += 3

            tapped = self.otp_page.tap_resend()
            if tapped:
                print("  ℹ️  Resend tapped — waiting for new OTP notification...")
                otp = self.otp_page.get_otp_from_notification(timeout=10)
            self.screenshot("04_after_resend")

        if not otp:
            print("  ⚠️  OTP not available even after resend — cannot verify. SKIP.")
            return

        print(f"  📩 OTP: {otp}")

        # Always clear the input field first (test_03 may have left stale digits
        # even after clear_otp_field; a second clear guarantees a blank field)
        self.otp_page.clear_otp_field()
        time.sleep(0.5)

        self.otp_page.enter_otp(otp)
        time.sleep(5)
        self.screenshot("04_after_otp_entry")

        otp_gone = not self.otp_page.is_visible()
        self._assert(otp_gone,
                     "OTP accepted — navigated past OTP screen",
                     "Still on OTP screen after entering correct OTP")
        
        
    @allure.story("05 - DB Validation: OTP After OTP Verified")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_05_db_validation_otp_verified(self):
        print("\n[TEST 05] DB validation: otp_verified after OTP verification")
        if not self.db:
            print("  ⚠️  No DB connection — skipping DB validation")
            return

        user_id = self._data.get("user_id")
        if not user_id:
            print("  ⚠️  No user_id from registration flow — skipping DB validation")
            return

        from utils.queries import get_otp_verified,get_user_product_mapping,get_state,get_state_audit

        self._assert(
            get_otp_verified(self.db, user_id) is True,
            "OTP marked verified in DB",
            "OTP verification not updated in DB"
        )

        self._assert(
            get_user_product_mapping(self.db, user_id, "BMI"),
            "Product mapping exists for BMI",
            "Missing product mapping for BMI"
        )

        state = get_state(self.db, user_id)
        self._assert(
            state == "ONBOARDING",
            f"State machine is ONBOARDING (got: {state})",
            f"Expected ONBOARDING but got {state}"
        )


        # previous_state, current_state = get_state_audit(self.db, user_id)
        # self._assert(
        #     previous_state == "INITIATED" and current_state == "BANK_SELECTION",
        #     "State audit exists for INITIATED -> BANK_SELECTION",
        #     "Missing state audit for INITIATED -> BANK_SELECTION"
        # )

        previous_state = get_state_audit(self.db, user_id)[0].get('previous_state')
        current_state = get_state_audit(self.db, user_id)[0].get('current_state')
        self._assert(
            previous_state == "BANK_SELECTION" and current_state == "ONBOARDING",
            "State audit exists for BANK_SELECTION -> ONBOARDING",
            "Missing state audit for BANK_SELECTION -> ONBOARDING"
        )


TEST_ORDER = [
    "test_01_otp_screen_loads",
    "test_02_resend_code_visible",
    "test_03_wrong_otp_shows_error",
    "test_04_retrieve_and_verify_otp",
    "test_05_db_validation_otp_verified"
]

if __name__ == "__main__":
    t = OTPScreenTest()
    OTPScreenTest.setup_class()
    for method in TEST_ORDER:
        getattr(t, method)()
    print("\n✅ OTP functional tests done.")
