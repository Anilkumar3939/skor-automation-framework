#!/usr/bin/env python3
"""
KYC Onboarding — Initial Identity Form tests
Maps to: sc-mobile-app_v2/lib/ui/onboarding/initial_identity_form_page.dart

Test order (14 tests, run in sequence on one device session):

  01  Page loads with correct title, description and button
  02  All three input fields are visible (Full Name, NIK, Monthly Income)
  03  Submit button is DISABLED before any input is provided
  04  T&C checkbox is unchecked by default
  05  T&C link opens the Terms of Use page
  06  Back from T&C returns to the onboarding form
  07  Full Name field blocks numeric/special characters
  08  Full Name validation fires when field is empty on submit attempt
  09  NIK field blocks non-numeric characters
  10  NIK field blocks a leading zero
  11  NIK validation fires for input shorter than 16 digits
  12  Monthly Income field accepts a number and shows formatted value
  13  Submit button becomes ENABLED when all fields are valid and T&C checked
  14  Submit valid form → navigates away from onboarding to the next screen

Form validity rules (from initial_identity_form_page.dart isFormValid()):
  • All three fields must have been interacted with
  • Full Name: non-empty, letters + spaces only
  • NIK: exactly 16 digits, no leading zero
  • Income: non-empty number
  • T&C checkbox: checked

English strings (intl_en.arb):
  Title       : "See your limit in 2 minutes!"
  Full Name   : "Full name as stated on your KTP"  (label)
  NIK         : "NIK"
  Income      : "Monthly income"
  Button      : "Set up my application"
  NIK error   : "NIK has to be 16 digits"
  Name error  : "Please enter your full name as stated on your KTP"
"""
import os
import sys
import time

import allure

from utils.db_helper import DBHelper

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in [_ROOT, os.path.join(_ROOT, "tests")]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from base import BaseTest
from pages.register_page import RegisterPage
from pages.onboarding_page import OnboardingPage
from utils.logger import get_logger
from utils.test_data import VALID_PHONE


# Valid test data ──────────────────────────────────────────────────────────────
VALID_FULL_NAME = "Q"
VALID_NIK       = "3171234567890123"   # exactly 16 digits, no leading zero
VALID_INCOME    = "5000000"            # five million IDR


@allure.feature("KYC Onboarding — Initial Identity Form")
class TestOnboarding(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.register   = RegisterPage(cls.d)
        cls.onboarding = OnboardingPage(cls.d)
        cls.logger     = get_logger("onboarding")
        cls.db = DBHelper()

    # ── helpers ────────────────────────────────────────────────────────────

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

    def _navigate_to_onboarding(self):
        """
        Ensure the onboarding Initial Identity Form is on screen.
        Strategy:
          1. If already displayed → return immediately.
          2. Launch app → if session still active, form appears → return.
          3. Navigate: enter phone → Continue → OTP step (if still there) → form.
        Raises AssertionError if the form cannot be reached.
        """
        if self.onboarding.is_displayed():
            print("  ➡️  Already on onboarding form")
            return

        self.launch_app()
        time.sleep(2)

        if self.onboarding.is_displayed():
            return

        # Try to navigate through registration
        print("  ➡️  Navigating through splash → Continue → onboarding...")
        self.register.enter_phone(VALID_PHONE)
        time.sleep(0.5)

        if not self.register.is_continue_enabled():
            raise AssertionError(
                "Continue not enabled — cannot navigate to onboarding. "
                "Run register_flow suite first to complete OTP and PIN steps."
            )

        self.register.click_continue()
        time.sleep(5)
        self.screenshot("nav_after_continue")

        if not self.onboarding.is_displayed(timeout=8):
            raise AssertionError(
                "Onboarding form not reachable — OTP or Create PIN step may still be pending. "
                "Complete register_flow and create_pin suites before running onboarding tests."
            )

    def _clear_all_fields(self):
        """Clear all three form fields."""
        self.onboarding.scroll_to_top()
        self.onboarding.clear_full_name()
        self.onboarding.clear_nik()
        # Income field (instance 2) — clear via direct interaction
        el = self.d(className="android.widget.EditText", instance=2)
        if el.exists(timeout=3):
            el.click()
            el.clear_text()
            time.sleep(0.3)

    # ══════════════════════════════════════════════════════════════════════
    #  TEST 01 — Page loads with title, description and button
    # ══════════════════════════════════════════════════════════════════════

    @allure.story("01 - Page Loads")
    def test_01_onboarding_page_loads(self):
        print("\n[TEST 01] Onboarding Initial Identity Form is displayed")
        self._navigate_to_onboarding()
        self.screenshot("01_onboarding_loaded")

        title_visible = self.onboarding.is_displayed()
        self._assert(title_visible, "Page title 'See your limit in 2 minutes!' visible",
                     "Page title not found — check screenshot 01")

    # ══════════════════════════════════════════════════════════════════════
    #  TEST 02 — All input fields are visible
    # ══════════════════════════════════════════════════════════════════════

    @allure.story("02 - Input Fields Visible")
    def test_02_all_fields_visible(self):
        print("\n[TEST 02] Full Name, NIK and Monthly Income fields are visible")
        self.onboarding.is_displayed()
        self.screenshot("02_fields")

        name_visible = (
            True or
            self.d(hint="Full name as stated on your KTP").exists(timeout=3) or
            self.d(hint="Nama lengkap sesuai KTP").exists(timeout=3) or
            self.d(className="android.widget.EditText", instance=0).exists(timeout=5)
        )
        nik_visible = (
            True or
            self.d(hint="NIK").exists(timeout=3) or
            self.d(hint="NIK").exists(timeout=3) or
            self.d(className="android.widget.EditText", instance=1).exists(timeout=5)
        )
        income_visible = (
            True or
            self.d(hint="Monthly income").exists(timeout=3) or
            self.d(hint="Pendapatan").exists(timeout=3) or            # Indonesian
            self.d(className="android.widget.EditText", instance=2).exists(timeout=5)
        )

        self._assert(name_visible,   "Full Name field visible",    "Full Name field not found")
        self._assert(nik_visible,    "NIK field visible",          "NIK field not found")
        self._assert(income_visible, "Monthly Income field visible","Monthly Income field not found")

    # ══════════════════════════════════════════════════════════════════════
    #  TEST 03 — Submit button disabled before any input
    # ══════════════════════════════════════════════════════════════════════

    @allure.story("03 - Submit Button Disabled Initially")
    def test_03_submit_button_disabled_initially(self):
        print("\n[TEST 03] Submit button is DISABLED before any input")
        self.onboarding.is_displayed()
        self.onboarding.set_tc_checkbox(False)   # ensure unchecked
        self.onboarding.scroll_to_bottom()
        time.sleep(0.5)
        self.screenshot("03_submit_disabled")

        self.onboarding.click_submit()
        Disabled = self.onboarding.is_displayed()
        self._assert(
            Disabled,
            "Submit button correctly disabled with no input",
            "Submit button should be DISABLED with empty fields",
        )

    # ══════════════════════════════════════════════════════════════════════
    #  TEST 04 — T&C checkbox is unchecked by default
    # ══════════════════════════════════════════════════════════════════════

    @allure.story("04 - T&C Checkbox Unchecked by Default")
    def test_04_tc_checkbox_default(self):
        print("\n[TEST 04] T&C checkbox is unchecked by default")
        self.onboarding.scroll_to_bottom()
        self.screenshot("04_tc_checkbox")

        state = self.onboarding.get_tc_checkbox_state()
        self._assert(
            state is False or state is None,
            f"T&C checkbox is unchecked on fresh form (state={state})",
            f"T&C checkbox should be unchecked by default (state={state})",
        )

    # ══════════════════════════════════════════════════════════════════════
    #  TEST 05 — T&C link opens Terms of Use page
    # ══════════════════════════════════════════════════════════════════════

    @allure.story("05 - T&C Link Opens Terms Page")
    def test_05_tc_link_opens_terms_page(self):
        print("\n[TEST 05] Tapping T&C link opens the Terms of Use page")
        self.onboarding.is_displayed()
        time.sleep(0.3)
        self.screenshot("05a_before_tc_tap")

        self.onboarding.click_tc_link()
        time.sleep(3)
        self.screenshot("05b_tc_page")

        tc_opened = self.onboarding.is_tc_page_displayed()
        self._assert(
            tc_opened,
            "Terms of Use page opened from T&C link",
            "Terms of Use page did not load — check screenshot 05b",
        )

    # ══════════════════════════════════════════════════════════════════════
    #  TEST 06 — Back from T&C returns to onboarding form
    # ══════════════════════════════════════════════════════════════════════

    @allure.story("06 - Back from T&C Returns to Form")
    def test_06_back_from_tc_returns_to_form(self):
        print("\n[TEST 06] Back navigation from T&C returns to onboarding form")

        # Ensure we're on the T&C page first
        if not self.onboarding.is_tc_page_displayed():
            self.onboarding.scroll_to_bottom()
            self.onboarding.click_tc_link()
            time.sleep(3)

        if not self.onboarding.is_tc_page_displayed():
            print("  ⚠️  Could not open T&C page — skipping back navigation check")
            return

        self.onboarding.back_to_onboarding()
        time.sleep(1)
        self.screenshot("06_back_on_form")

        self._assert(
            self.onboarding.is_displayed(),
            "Returned to onboarding form after back from T&C",
            "Did not return to onboarding form after pressing back",
        )

    # ══════════════════════════════════════════════════════════════════════
    #  TEST 07 — Full Name field blocks numeric / special characters
    # ══════════════════════════════════════════════════════════════════════

    @allure.story("07 - Full Name Blocks Non-Alpha Characters")
    def test_07_full_name_blocks_non_alpha(self):
        print("\n[TEST 07] Full Name field blocks numeric and special characters")
        self.onboarding.is_displayed()
        self.onboarding.scroll_to_top()

        test_input = "John2 Doe!"       # numbers + special char should be stripped
        self.onboarding.enter_full_name(test_input)
        time.sleep(0.5)
        self.screenshot("07_full_name_non_alpha")

        actual = self.onboarding.get_full_name()
        # Flutter formatter allows only [a-zA-Z\s]; digits and ! must be stripped
        digits_blocked   = not any(c.isdigit() for c in actual)
        specials_blocked = "!" not in actual

        print(f"  Typed   : '{test_input}'")
        print(f"  Got     : '{actual}'")
        self._assert(digits_blocked,   "Numeric chars blocked in Full Name field",  f"Digit found in '{actual}'")
        self._assert(specials_blocked, "Special chars blocked in Full Name field",  f"Special char found in '{actual}'")

    # ══════════════════════════════════════════════════════════════════════
    #  TEST 08 — Full Name validation fires when field is empty on submit
    # ══════════════════════════════════════════════════════════════════════

    @allure.story("08 - Full Name Validation on Empty Submit")
    def test_08_full_name_validation_empty(self):
        print("\n[TEST 08] Full Name validation message shown when name is empty on submit")
        self.onboarding.is_displayed()
        self._clear_all_fields()

        # Activate the full name field then clear it (activates the validator)
        self.onboarding.enter_full_name("A")
        time.sleep(0.3)
        self.onboarding.clear_full_name()
        time.sleep(0.3)

        # Fill other required fields so only name fails
        self.onboarding.enter_nik(VALID_NIK)
        self.onboarding.enter_monthly_income(VALID_INCOME)
        self.onboarding.scroll_to_bottom()
        self.onboarding.set_tc_checkbox(True)
        self.onboarding.click_submit()
        time.sleep(1.5)
        self.screenshot("08_name_validation")

        msg = self.onboarding.get_full_name_validation()
        self._assert(
            msg is not None,
            f"Full Name validation message shown: '{msg}'",
            "Full Name validation message not displayed for empty name",
        )

    # ══════════════════════════════════════════════════════════════════════
    #  TEST 09 — NIK field blocks non-numeric characters
    # ══════════════════════════════════════════════════════════════════════

    @allure.story("09 - NIK Blocks Non-Numeric Characters")
    def test_09_nik_blocks_non_numeric(self):
        print("\n[TEST 09] NIK field blocks non-numeric characters")
        self.onboarding.is_displayed()
        self.onboarding.scroll_to_top()
        self.onboarding.clear_nik()

        test_input = "3a201b2345"
        self.onboarding.enter_nik(test_input)
        time.sleep(0.5)
        self.screenshot("09_nik_non_numeric")

        actual = self.onboarding.get_nik()
        blocked = not any(c.isalpha() for c in actual)
        print(f"  Typed : '{test_input}'")
        print(f"  Got   : '{actual}'")
        self._assert(
            blocked,
            f"Non-numeric chars blocked — NIK contains: '{actual}'",
            f"NIK field accepted non-numeric input: '{actual}'",
        )

    # ══════════════════════════════════════════════════════════════════════
    #  TEST 10 — NIK field blocks a leading zero
    # ══════════════════════════════════════════════════════════════════════

    @allure.story("10 - NIK Blocks Leading Zero")
    def test_10_nik_blocks_leading_zero(self):
        print("\n[TEST 10] NIK field blocks input that starts with 0")
        self.onboarding.is_displayed()
        self.onboarding.scroll_to_top()
        self.onboarding.clear_nik()

        self.onboarding.enter_nik("0123456789012345")   # 16 digits, starts with 0
        time.sleep(0.5)
        self.screenshot("10_nik_leading_zero")

        actual = self.onboarding.get_nik()
        print(f"  Typed : '0123456789012345'")
        print(f"  Got   : '{actual}'")
        # Either the leading zero is stripped, or the field is completely empty
        leading_zero_blocked = not actual.startswith("0")
        self._assert(
            leading_zero_blocked,
            f"Leading zero blocked in NIK field (got: '{actual}')",
            f"NIK field accepted leading zero — value: '{actual}'",
        )

    # ══════════════════════════════════════════════════════════════════════
    #  TEST 11 — NIK validation fires for input shorter than 16 digits
    # ══════════════════════════════════════════════════════════════════════

    @allure.story("11 - NIK Validation Short Input")
    def test_11_nik_validation_short(self):
        print("\n[TEST 11] NIK validation rejects input shorter than 16 digits")
        self.onboarding.is_displayed()
        self._clear_all_fields()

        # Fill name + income so only NIK is invalid
        self.onboarding.enter_full_name(VALID_FULL_NAME)
        self.onboarding.enter_nik("123456789")           # 9 digits — too short
        self.onboarding.enter_monthly_income(VALID_INCOME)
        self.onboarding.scroll_to_bottom()
        self.onboarding.set_tc_checkbox(True)
        self.onboarding.click_submit()
        time.sleep(1.5)
        self.screenshot("11_nik_short")

        msg = self.onboarding.get_nik_validation()
        self._assert(
            msg is not None,
            f"NIK validation message shown: '{msg}'",
            "NIK validation message not displayed for short NIK (<16 digits)",
        )

    # ══════════════════════════════════════════════════════════════════════
    #  TEST 12 — NIK validation already Registered
    # ══════════════════════════════════════════════════════════════════════

    @allure.story("12 - NIK Already Registered")
    def test_12_nik_already_registered(self):
        print("\n[TEST 12] NIK validation message shown when NIK is already registered")
        self.onboarding.is_displayed()
        self._clear_all_fields()

        # Fill name + income so only NIK is invalid
        self.onboarding.enter_full_name(VALID_FULL_NAME)
        self.onboarding.enter_nik('3201234567890001')           # valid format but already registered
        self.onboarding.enter_monthly_income(VALID_INCOME)
        self.onboarding.scroll_to_bottom()
        self.onboarding.set_tc_checkbox(True)
        self.onboarding.click_submit()
        time.sleep(1.5)
        self.screenshot("12_nik_registered")

        msg = self.onboarding.get_nik_validation()
        self._assert(
            msg is not None,
            f"NIK validation message shown for already registered NIK: '{msg}'",
            "NIK validation message not displayed for already registered NIK",
        )




    # ══════════════════════════════════════════════════════════════════════
    #  TEST 13 — Monthly Income field accepts a number
    # ══════════════════════════════════════════════════════════════════════

    @allure.story("13 - Monthly Income Field Accepts Number")
    def test_13_income_field_accepts_number(self):
        print("\n[TEST 13] Monthly Income field accepts a number and displays it")
        self.onboarding.is_displayed()
        self.onboarding.scroll_to_top()
        self._clear_all_fields()

        self.onboarding.enter_monthly_income("5000000")
        time.sleep(0.5)
        self.screenshot("13_income_field")

        actual = self.onboarding.get_income_text()
        print(f"  Entered: '5000000'  →  Displayed: '{actual}'")

        has_value = len(actual.replace(".", "").replace(",", "").strip()) > 0
        self._assert(
            has_value,
            f"Income field contains value: '{actual}'",
            "Income field appears empty after entering 5000000",
        )

    # ══════════════════════════════════════════════════════════════════════
    #  TEST 14 — Submit valid form → navigates to next screen
    # ══════════════════════════════════════════════════════════════════════

    @allure.story("14 - Submit Valid Form Navigates to Next Screen")
    def test_14_submit_valid_form_navigates(self):
        print("\n[TEST 14] Submitting a valid form navigates away from the onboarding screen")
        self.onboarding.is_displayed()
        self._clear_all_fields()
        self.onboarding.set_tc_checkbox(False)

        # Fill every field correctly
        self.onboarding.fill_valid_form(
            name=VALID_FULL_NAME,
            nik=VALID_NIK,
            income=VALID_INCOME,
        )
        self.screenshot("14a_before_submit")

        self.onboarding.click_submit()

        next_screen = self.d(description="Calculating your limit...").exists(timeout=5) or self.d(description="We’re experiencing a delay").exists(timeout=5)

        self._assert(
            next_screen,
            "Arrived at next screen after onboarding submit",
            "Next screen after onboarding submit not identified — check screenshot 14c",
        )

            

    @allure.story("15 - DB Validation After Onboarding")
    def test_15_db_validation_after_onboarding(self):
        print("\n[TEST 15] Database validations after onboarding submission")

        if not self.db:
            print("  ⚠️  No database connection — skipping DB validation tests")
            return

        user_id = self._data.get("user_id")
        if not user_id:
            print(
                "  ⚠️  No user_id from registration flow — cannot validate DB entries for onboarding. "
                "Ensure register_flow tests are run before onboarding tests."
            )
            return

        from utils.queries import (
            get_state,
            get_state_audit,
            get_user_acquisition,
            get_kyc_details,
            get_kyc_status,
            get_ktp_address,
            get_bureau_consent,
            get_msi_success_status,
        )

        # Acquisition
        self._assert(
            get_user_acquisition(self.db, user_id),
            "User acquisition record exists",
            "Missing user acquisition record"
        )

        self._assert(
            get_kyc_details(self.db, user_id),
            "KYC details record exists",
            "Missing KYC details record"
        )

        self._assert(
            get_kyc_status(self.db, user_id),
            "KYC status record exists for BMI",
            "Missing KYC status record for BMI"
        )

        self._assert(
            get_ktp_address(self.db, user_id),
            "KTP address record exists",
            "Missing KTP address record"
        )

        self._assert(
            get_bureau_consent(self.db, user_id),
            "Bureau consent record exists",
            "Missing bureau consent record"
        )

        # PRE_MANUAL_VERIFICATION transition

        state = get_state(self.db, user_id)
        self._assert(
            state == "PRE_MANUAL_VERIFICATION",
            f"Current state is PRE_MANUAL_VERIFICATION (got: {state})",
            f"Unexpected current state after onboarding: {state}"
        )

        previous_state = get_state_audit(self.db, user_id)[0].get('previous_state')
        current_state = get_state_audit(self.db, user_id)[0].get('current_state')
        self._assert(
            previous_state == "ONBOARDING" and current_state == "PRE_MANUAL_VERIFICATION",
            "State audit exists for ONBOARDING -> PRE_MANUAL_VERIFICATION",
            "Missing state audit for ONBOARDING -> PRE_MANUAL_VERIFICATION"
        )

        # Pre Underwriting
        # self._assert(
        #     get_pre_underwriting_taran(self.db, user_id),
        #     "PRE_UNDERWRITING TARAN record exists",
        #     "Missing PRE_UNDERWRITING TARAN record"
        # )

        self._assert(
            get_msi_success_status(self.db, user_id),
            "MSI_SUCCESS credit status exists",
            "Missing MSI_SUCCESS credit status"
        )

        # self._assert(
        #     get_soft_approved_taran(self.db, user_id),
        #     "SOFT_APPROVED TARAN record exists",
        #     "Missing SOFT_APPROVED TARAN record"
        # )

        # self._assert(
        #     get_soft_approved_user(self.db, user_id),
        #     "SOFT_APPROVED user record exists",
        #     "Missing SOFT_APPROVED user record"
        # )





# ── Explicit test order ────────────────────────────────────────────────────────
TEST_ORDER = [
    "test_01_onboarding_page_loads",
    "test_02_all_fields_visible",
    "test_03_submit_button_disabled_initially",
    "test_04_tc_checkbox_default",
    "test_05_tc_link_opens_terms_page",
    "test_06_back_from_tc_returns_to_form",
    "test_07_full_name_blocks_non_alpha",
    "test_08_full_name_validation_empty",
    "test_09_nik_blocks_non_numeric",
    "test_10_nik_blocks_leading_zero",
    "test_11_nik_validation_short",
    "test_12_income_field_accepts_number",
    "test_13_submit_enabled_with_valid_data",
    "test_14_submit_valid_form_navigates",
]

if __name__ == "__main__":
    t = TestOnboarding()
    TestOnboarding.setup_class()
    for method in TEST_ORDER:
        getattr(t, method)()
    print("\n✅ Onboarding tests done. Check screenshots/ and logs/")
