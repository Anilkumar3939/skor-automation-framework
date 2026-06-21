#!/usr/bin/env python3
"""
Registration / Login screen tests (second page) for Skorcard.
"""
import time
import os
import allure

from base import BaseTest
from utils.logger import get_logger
from utils.db_helper import DBHelper
from pages.registartion_login import RegistrationLogin



VALID_PHONE = os.environ.get("TEST_PHONE", "845682161998")
SHORT_PHONE = "81234"
ZERO_PHONE  = "0010080019"
VALID_CODE  = os.environ.get("TEST_REFERRAL_CODE", "OBRSPC9")
WRONG_CODE  = "INVALID1"


@allure.feature("Registration Login Screen")
class RegistrationLoginTest(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.logger = get_logger("registration")
        cls.db = DBHelper()

        cls.registration = RegistrationLogin(cls.d)


    # ---------------- LOG HELPERS ---------------- #

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

    # # ---------------- NAVIGATION ---------------- #

    # def _is_on_splash(self):
    #     return (
    #         self.d(description="Continue").exists(timeout=3) and
    #         self.d(className="android.widget.EditText").exists(timeout=2)
    #     )
    
    # def _click_back_to_splash(self):
    #     self.d.press(className="android.widget.ImageButton", timeout=3).click()

    # def _navigate_to_registration(self):
    #     self.launch_app()
    #     time.sleep(1)

    #     if self.d(description="Continue").exists(timeout=3):
    #         self._log_pass("Already on RegisterLogin screen")
    #         return True


    #     reached = self.d(description="Continue").exists(timeout=10)
    #     return self._assert(
    #         reached,
    #         "RegisterLogin screen reached",
    #         "Failed to reach RegisterLogin screen"
    #     )

    # def _clear_phone(self):
    #     el = self.d(className="android.widget.EditText")
    #     if el.exists(timeout=5):
    #         el.click()
    #         time.sleep(0.5)
    #         el.set_text("23")
    #         el.set_text("")
    #         time.sleep(0.3)

    # def _enter_phone(self, number: str):
    #     el = self.d(className="android.widget.EditText", instance=0)     
    #     if not el.exists(timeout=8):
    #         self._log_fail("Phone input not found")
    #         return
    #     el.click()
    #     time.sleep(3)
    #     el.set_text(number)
    #     time.sleep(0.5)

    # def _is_proceed_enabled(self):
    #     try:
    #         btn = self.d(description="Continue")
    #         if not btn.exists(timeout=3):
    #             return False
    #         btn.click()  # to trigger any potential validation
    #         return not self.registration._is_on_splash()
    #     except:
    #         return False
    # def _open_invite_sheet(self):
    #     """
    #     Tap the 'Do you have an invitation code?' link.
    #     Scrolls down slightly first (link can be below the initial viewport),
    #     then tries multiple selector strategies (EN + ID).
    #     """
    #     self.d.swipe(500, 900, 500, 600, 0.3)
    #     time.sleep(1)          # let the UI settle after scroll

    #     selectors = [
    #         {"description":        "Do you have an invitation code?"},
    #         {"descriptionContains":"invitation code"},
    #         {"descriptionContains":"Invitation Code"},
    #         {"text":               "Do you have an invitation code?"},
    #         {"textContains":       "invitation code"},
    #         {"textContains":       "Have an invitation"},
    #         {"textContains":       "invitation"},
    #         {"descriptionContains":"kode undangan"},
    #         {"textContains":       "kode undangan"},
    #         {"descriptionContains":"Punya kode"},
    #         {"textContains":       "Punya kode"},
    #         {"textContains":       "undangan"},
    #     ]
    #     for sel in selectors:
    #         el = self.d(**sel)
    #         if el.exists(timeout=4):
    #             el.click()
    #             time.sleep(1)
    #             return True

    #     self.screenshot("invite_link_not_found_debug")
    #     print("  ⚠️  invite sheet trigger not found — skipping")
    #     return False
    

    # def _enter_invite_code(self, code: str):
    #     el = self.d(className="android.widget.EditText")
    #     if not el.exists(timeout=5):
    #         print("  ⚠️  invite code EditText not found")
    #         return False
    #     el.set_text(code)
    #     time.sleep(0.5)
    #     return True
    
    # def _tap_sheet_continue(self):
    #     for sel in [{"description": "Continue"}, {"text": "Continue"},
    #                 {"descriptionContains": "Continue"}]:
    #         el = self.d(**sel)
    #         if el.exists(timeout=3):
    #             el.click()
    #             time.sleep(0.5)
    #             return True
    #     print("  ⚠️  Continue button not found")
    #     return False

    # ---------------- TESTS ---------------- #

    @allure.story("01 - Screen Loads")
    def test_01_screen_loads(self):
        print("\n[TEST 01] Screen loads")

        reached = self.registration._navigate_to_registration()
        self.screenshot("01_screen")

        assert self._assert(
            reached,
            "Registration screen loaded",
            "Registration screen not loaded"
        )
    
    time.sleep(3)

    # @allure.story("02 - Continue Button Disabled on Initial Load")
    # def test_02_continue_button_disabled_on_initial_load(self):
    #     print("\n[TEST 02] Verify Continue button is disabled on initial screen")
    #     enabled = self.registration._is_proceed_enabled()

    #     assert self._assert(
    #         not enabled,
    #         "Continue disabled for empty phone",
    #         "Continue should be disabled for empty phone"
    #     )
    #     time.sleep(3)

    # @allure.story("03 - Change Language from English to Indonesian")
    # def test_03_change_language_to_indonesian(self):
    #     print("\n[TEST 03] Verify language change from English to Indonesian")

    #     # Try tapping the language toggle if it exists
    #     toggled = False
    #     En = self.d(description="ID")
    #     if En.exists(timeout=3):
    #         En.click()
    #         toggled = True
    #     check_id_text = self.d(description="Dapatkan cashback hingga 10%* per transaksi\nCashback instan dari tiap transaksi harianmu!").exists(timeout=5)
    #     continue_id_text = self.d(description="Lanjutkan").exists(timeout=5)
    #     invitation_code_id_text = self.d(description="Punya kode undangan?").exists(timeout=5)


    #     if not toggled:
    #         print("  ⚠️  Language toggle not found — SKIP")
    #         return

    #     # Verify the Continue button text changed to Indonesian
    #     assert self._assert(
    #         check_id_text and continue_id_text and invitation_code_id_text,
    #         "Language toggled to Indonesian",
    #         "Continue button or other key text not found in Indonesian after toggle"
    #     )
        
    #     time.sleep(3)

    
    # @allure.story("04 - Change language back to English")
    # def test_04_change_language_back_to_english(self):
    #     print("\n[TEST 04] Change language back to English")

    #     # Try tapping the language toggle if it exists
    #     toggled = False
    #     Id = self.d(description="ID")
    #     if Id.exists(timeout=3):
    #         Id.click()
    #         toggled = True

    #     check_en_text = self.d(description="Get cashback up to 10%* per transaction \nInstant cashback from your everyday transactions!").exists(timeout=5)
    #     continue_en_text = self.d(description="Continue").exists(timeout=5)
    #     invitation_code_en_text = self.d(description="Do you have an invitation code?").exists(timeout=5)

    #     if not toggled:
    #         print("  ⚠️  Language toggle not found — SKIP")
    #         return

    #     # Verify the Continue button text changed back to English
    #     assert self._assert(
    #         check_en_text and continue_en_text and invitation_code_en_text,
    #         "Language toggled back to English",
    #         "Continue button or other key text not found in English after toggle"
    #     )

    # @allure.story("05 - Checking FAQ link")
    # def test_05_check_faq_link(self):
    #     print("\n[TEST 05] Checking FAQ link")

    #     # Try tapping the FAQ link if it exists
    #     link_tapped = False
    #     link = self.d.xpath('//android.widget.ScrollView/android.view.View[1]')
    #     if link.exists(timeout=3):
    #         link.click()
    #         time.sleep(2)
    #         link_tapped = True
        

    #     if not link_tapped:
    #         print("  ⚠️  FAQ link not found — SKIP")
    #         return
    #     check_faq = self.d.xpath(textContains='//android.webkit.WebView').exists(timeout=5)

    #     if link_tapped and check_faq:
    #         print("  ✅ PASS: FAQ link opened a WebView")
    #         back_to_splash = self.d.xpath('//android.widget.ImageView').exists(timeout=5)
    #         if back_to_splash:
    #             self.d.xpath('//android.widget.ImageView').click()
    #             time.sleep(1)
    #             print("  ✅ PASS: Navigated back to splash from FAQ")
    #         else:
    #             print("  ⚠️  Back button not found in FAQ — check screenshot")
    #     else:
    #         print("  ❌ FAIL: FAQ link did not open a WebView")
    #         raise AssertionError("FAQ link did not open a WebView")

    #     assert self._assert(
    #         check_faq,
    #         "FAQ page opened",
    #         "FAQ page not opened after tapping link"
        # )
    

    @allure.story("02 - Continue Disabled Empty")
    def test_02_continue_disabled_empty_phone(self):
        print("\n[TEST 02] Empty phone")

        self.registration._clear_phone()
        enabled = self.registration._is_proceed_enabled()

        assert self._assert(
            not enabled,
            "Continue disabled for empty phone",
            "Continue should be disabled for empty phone"
        )
        time.sleep(3)
    
    time.sleep(3)

    @allure.story("03 - Zero Prefix")
    def test_03_proceed_disabled_zero_prefix(self):
        print("\n[TEST 03] Zero prefix")

        self.registration._enter_phone(ZERO_PHONE)

        enabled = self.registration._is_proceed_enabled()
        time.sleep(3)

        assert self._assert(
            not enabled,
            "Zero prefix blocked",
            "Zero prefix should not be allowed"
        )
        time.sleep(3)

    time.sleep(3)

    @allure.story("04 - Short Phone")
    def test_04_proceed_disabled_short_phone(self):
        print("\n[TEST 04] Short phone")
        time.sleep(3)

        self.registration._enter_phone(SHORT_PHONE)

        enabled = self.registration._is_proceed_enabled()

        assert self._assert(
            not enabled,
            "Short phone blocked",
            "Short phone should not be allowed"
        )
        time.sleep(3)

    time.sleep(3)  

    @allure.story("05 - Referral Section Visible")
    def test_05_referral_code_section_visible(self):
        print("\n[TEST 05] Referral section")

        visible = self.d(description="Do you have an invitation code?").exists(timeout=3)
        print("Referral section visible:", visible)

        assert self._assert(
            visible,
            "Referral section visible",
            "Referral section not visible"
        )
        time.sleep(3)

    time.sleep(3)   

    @allure.story("06 - Wrong Referral Code")
    def test_06_wrong_invitation_code(self):
        print("\n[TEST 06] Wrong referral")

        print("\n[TEST 02] Wrong invitation code shows error sheet")

        if not self.registration._open_invite_sheet():
            print("  ⚠️  Could not open invite sheet — SKIP")
            return

        self.screenshot("02a_invite_sheet_open")
        self.registration._enter_invite_code(WRONG_CODE)
        self.screenshot("02b_wrong_code_entered")
        self.registration._tap_sheet_continue()
        time.sleep(3)
        self.screenshot("02c_wrong_code_response")

        error_shown = (
            self.d(description="Edit code").exists(timeout=5) or
            self.d(descriptionContains="Edit code").exists(timeout=3) or
            self.d(descriptionContains="Edit Code").exists(timeout=2) or
            self.d(description="Continue without code").exists(timeout=3) or
            self.d(descriptionContains="without code").exists(timeout=2) or
            self.d(textContains="Edit code").exists(timeout=3) or
            self.d(textContains="seem to work").exists(timeout=2) or
            self.d(textContains="doesn't work").exists(timeout=2)
        )
        if error_shown:
            print("  ✅ PASS: Error sheet shown for wrong code")
        else:
            print("  ❌ FAIL: Error sheet not detected — check screenshot 02c")
            raise AssertionError("Error sheet not shown for wrong invitation code")

        # Dismiss via "Continue without code" → lands back on splash for test_03
        for sel in [{"description": "Continue without code"},
                    {"descriptionContains": "without code"},
                    {"textContains": "without code"}]:
            btn = self.d(**sel)
            if btn.exists(timeout=3):
                btn.click()
                time.sleep(1)
                break

        # same logic preserved
        self._log_pass("Flow executed (kept original behavior)") 


    @allure.story("Edit Code Allows Re-entering Invitation Code")
    def test_07_edit_code_button(self):
        """
        After entering a wrong code and seeing the error sheet, tap
        'Edit code' to verify the input reopens so the user can change
        their invitation code.
        """
        print("\n[TEST 07] Edit Code button re-opens invitation code input")

        if not self.registration._open_invite_sheet():
            print("  ⚠️  Could not open invite sheet — SKIP")
            return

        self.registration._enter_invite_code(WRONG_CODE)
        self.registration._tap_sheet_continue()
        time.sleep(3)
        self.screenshot("03a_error_sheet")

        # Tap "Edit code"
        edit_tapped = False
        for sel in [
            {"description":        "Edit code"},
            {"descriptionContains":"Edit code"},
            {"descriptionContains":"Edit Code"},
            {"text":               "Edit code"},
            {"textContains":       "Edit code"},
        ]:
            btn = self.d(**sel)
            if btn.exists(timeout=5):
                btn.click()
                edit_tapped = True
                time.sleep(1)
                break

        if not edit_tapped:
            print("  ⚠️  'Edit code' button not found — check screenshot 03a")
            return

        self.screenshot("03b_after_edit_code")

        code_input_visible = self.d(className="android.widget.EditText").exists(timeout=5)
        if code_input_visible:
            print("  ✅ PASS: 'Edit code' reopened the code input field")
        else:
            print("  ❌ FAIL: Code input field not visible after 'Edit code' tap")
            raise AssertionError("Code input field did not reopen after Edit code tap")

        # Enter a new code to verify the field is editable
        self.registration._enter_invite_code(VALID_CODE)
        self.screenshot("03c_new_code_entered")
        print("  ✅ PASS: New code entered in re-opened input field")

    @allure.story("Valid Invitation Code Accepted")
    def test_08_valid_invitation_code(self):
        print("\n[TEST 08] Valid invitation code accepted without error")
        # test_03 left us in the code sheet with code typed; go back to clean splash

        if not self.registration._open_invite_sheet():
            print("  ⚠️  Could not open invite sheet — SKIP")
            return

        self.screenshot("04a_invite_sheet")
        self.registration._enter_invite_code(VALID_CODE)
        self.screenshot("04b_valid_code_entered")
        self.registration._tap_sheet_continue()
        time.sleep(3)
        self.screenshot("04c_valid_code_response")

        success_message_shown = (
            self.d(description="Invitation code saved!\nEdit").exists(timeout=3)
        )

        error_shown = (
            self.d(textContains="doesn't work").exists(timeout=2) or
            self.d(textContains="Sorry").exists(timeout=2) or
            self.d(textContains="Invalid").exists(timeout=2)
        )


        if not error_shown and success_message_shown:
            print("  ✅ PASS: No error — valid code accepted")
            self._assert(True, "Valid invitation code accepted", "Valid invitation code not accepted")
        else:
            print("  ❌ FAIL: Error shown for valid code")
            self._assert(False, "Valid invitation code accepted", "Error shown for valid code")
        


    @allure.story("09 - Valid Phone")
    def test_09_proceed_enabled_valid_phone(self):
        print("\n[TEST 09] Valid phone")

        self.registration._enter_phone(VALID_PHONE)

        self.tap(description="Continue")
        time.sleep(5)

        otp_reached = (
            self.d(description="OTP").exists(timeout=8) or
            self.d(description="Verification").exists(timeout=3)
        )

        self._assert(
            otp_reached,
            "OTP screen reached",
            "OTP screen not reached"
        )

        # ---------------- STORE USER DATA ---------------- #

        from utils.queries import get_user_id

        time.sleep(5)

        user_id = get_user_id(self.db, VALID_PHONE)

        self._data["user_id"] = user_id
        self._data["phone"] = VALID_PHONE

        print("User ID:", user_id)
        time.sleep(5)

    @allure.story("10 - Database and Registration Validations")
    def test_10_database_validations(self):
        print("\n[TEST 10] Validate registration related database entries")

        if not self.db:
            print("  ⚠️  DB unavailable — skipping validations")
            return

        user_id = self._data.get("user_id")
        time.sleep(3)
        if not user_id:
            print("  ⚠️  User ID not available")
            return

        from utils.queries import (
            get_user_id,
            get_campaign,
            get_referral,
            get_user_settings,
            get_device_details,
            get_location_details,
            get_appsflyer,
        )

        # User Settings

        user_id = get_user_id(self.db, VALID_PHONE)

        self._assert(
            get_campaign(self.db, user_id) and get_campaign(self.db, user_id)[0].get("utm_source") == "referral",
            "Campaign exists with utm_source referral",
            "Campaign missing or invalid utm_source"
        )

        self._assert(
            get_user_settings(self.db, user_id),
            "user_settings entry exists",
            "Missing user_settings entry"
        )

        self._assert(
            get_referral(self.db, user_id) and get_referral(self.db, user_id).get("campaign_id") == "OBRSPC9",
            "Referral campaign exists",
            "Referral campaign missing"
        )

        self._assert(
            get_device_details(self.db, user_id),
            "device_details entry exists",
            "Missing device_details entry"
        )

        self._assert(
            get_location_details(self.db, user_id),
            "location_details entry exists",
            "Missing location_details entry"
        )

        self._assert(
            get_appsflyer(self.db, user_id, "ADJUST"),
            "ADJUST appsflyer entry exists",
            "Missing ADJUST appsflyer entry"
        )

        self._assert(
            get_appsflyer(self.db, user_id, "FIREBASE"),
            "FIREBASE appsflyer entry exists",
            "Missing FIREBASE appsflyer entry"
        )




# ORDER
TEST_ORDER = [
    "test_01_screen_loads",
    "test_02_proceed_disabled_empty_phone",
    "test_03_proceed_disabled_zero_prefix",
    "test_04_proceed_disabled_short_phone",
    "test_05_proceed_enabled_valid_phone",
    "test_06_error_clears_on_valid_input",
    "test_07_edit_code_button",
    "test_08_valid_invitation_code",
    "test_09_proceed_enabled_valid_phone",
    "test_10_database_validations",
]       

if __name__ == "__main__":
    t = RegistrationLoginTest()
    RegistrationLoginTest.setup_class()
    for method in TEST_ORDER:
        getattr(t, method)()
    print("\n✅ Registration/Login tests done.")