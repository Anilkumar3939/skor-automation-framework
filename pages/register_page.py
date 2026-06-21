#!/usr/bin/env python3
"""
RegisterPage — Page Object for the Splash / Phone-entry screen.
Ported from appium-project/pages/register_page.py and adapted for
uiautomator2 (no Appium server required).

Key differences from original:
  - XPath locators replaced with content-desc / className selectors
  - PIL color check replaced with button enabled/clickable check
  - OTP entry uses ADB shell keycodes (same logic as Appium press_keycode)
  - All methods return a value or bool; none raise on missing elements
"""
import re
import time

from pages.base_page import BasePage


class RegisterPage(BasePage):

    # Accessibility descriptions used throughout the splash/register screen
    CONTINUE        = "Continue"
    INVITATION_CODE = "Do you have an invitation code?"

    # Validation message descriptions (from the Flutter app)
    VAL_START_8     = "Phone number needs to start with the digit 8"
    VAL_MIN_DIGITS  = "Phone number needs to start with the digit 8 and consist of a minimum of 9 digits"
    VAL_SAME_DIGITS = "Numbers can't be same"

    # System permission resource IDs
    RES_ALLOW_NOTIF    = "com.android.permissioncontroller:id/permission_allow_button"
    RES_ALLOW_LOCATION = "com.android.permissioncontroller:id/permission_allow_foreground_only_button"

    # ------------------------------------------------------------------ #
    #  Permissions
    # ------------------------------------------------------------------ #

    def allow_app_notifications(self):
        """Grant the system notification permission dialog."""
        if self.tap_res_id(self.RES_ALLOW_NOTIF, timeout=5):
            time.sleep(0.5)

    def allow_app_location(self):
        """Tap the app-level location 'Continue' button."""
        self.tap_desc(self.CONTINUE, timeout=5)
        time.sleep(0.5)

    def allow_mobile_location(self):
        """Grant the system location permission dialog."""
        if self.tap_res_id(self.RES_ALLOW_LOCATION, timeout=5):
            time.sleep(0.5)

    # ------------------------------------------------------------------ #
    #  Page state
    # ------------------------------------------------------------------ #

    def elements_visible(self):
        """True when all key splash elements are present on screen."""
        return (
            self.exists_desc(self.CONTINUE) and
            self.d(className="android.widget.EditText").exists(timeout=5) and
            self.exists_desc(self.INVITATION_CODE)
        )

    def is_continue_enabled(self):
        """
        True when the Continue button is present AND enabled/clickable.
        Replaces the original PIL pixel-colour check.
        """
        try:
            btn = self.d(description=self.CONTINUE)
            if not btn.exists(timeout=3):
                return False
            info = btn.info
            return info.get("enabled", False) and info.get("clickable", False)
        except Exception:
            return False

    # ------------------------------------------------------------------ #
    #  Phone input
    # ------------------------------------------------------------------ #

    def clear_phone(self):
        self.set_edit_text("", instance=0)

    def enter_phone(self, phone):
        print(f"  📱 Entering phone: {phone}")

        field = self.d(className="android.widget.EditText", instance=0)

        if not field.exists(timeout=5):
            raise Exception("❌ Phone input field not found")

        field.click()              # 🔥 IMPORTANT
        time.sleep(0.5)

        field.clear_text()
        field.set_text(phone)
        time.sleep(1)

        # verify
        entered = field.info.get("text", "")
        print("📲 Entered value:", entered)

    def validate_phone(self, phone):
        """
        Enter *phone*, inspect the resulting validation message, and return:
          - "Valid"         if the phone passes all rules
          - A specific message string matching the app's validation text
          - "Blocked"       if blocked by an unrecognised error
        Mirrors the logic in the original RegisterPage.validate_phone_numbers().
        """
        self.clear_phone()
        self.enter_phone(phone)
        time.sleep(0.5)

        if not phone:
            if self.exists_desc(self.VAL_START_8):
                return self.VAL_START_8
            return "Blocked"

        if phone[0] != "8":
            msg = self.VAL_MIN_DIGITS if len(phone) > 1 else self.VAL_START_8
            if self.exists_desc(msg, timeout=2):
                return msg
            return "Blocked"

        if len(phone) >= 8 and len(set(phone[:8])) == 1:
            if self.exists_desc(self.VAL_SAME_DIGITS, timeout=2):
                return self.VAL_SAME_DIGITS
            return "Blocked"

        if len(phone) < 9:
            if self.exists_desc(self.VAL_MIN_DIGITS, timeout=2):
                return self.VAL_MIN_DIGITS
            return "TooShort"

        return "Valid"

    # ------------------------------------------------------------------ #
    #  Continue / navigation
    # ------------------------------------------------------------------ #

    def click_continue(self):
        return self.tap_desc(self.CONTINUE)

    # ------------------------------------------------------------------ #
    #  Invitation / referral code
    # ------------------------------------------------------------------ #

    def open_invitation_sheet(self):
        """Tap the invitation code row to open the bottom sheet."""
        self.tap_desc(self.INVITATION_CODE)
        time.sleep(1)

    def enter_invitation_code(self, code):
        """Enter code inside the invitation sheet (second EditText)."""
        self.set_edit_text(code, instance=0)

    # ------------------------------------------------------------------ #
    #  OTP
    # ------------------------------------------------------------------ #

    def get_otp_from_screen(self):
        """
        Read the OTP from the element whose content-desc contains
        'Code successfully sent'.  Returns digit-only string or None.
        Replaces the original AppiumBy.ANDROID_UIAUTOMATOR selector.
        """
        el = self._by_desc_contains("Code successfully sent", timeout=15)
        if el:
            desc = el.info.get("contentDescription", "")
            digits = re.sub(r"\D", "", desc)
            return digits if digits else None
        return None

    def enter_otp(self, otp):
        """
        Enter OTP digit-by-digit using ADB keycode events.
        Android keycode for digit d = d + 7  (same formula as Appium press_keycode).
        """
        print(f"  🔢 Entering OTP: {otp}")
        for digit in str(otp):
            keycode = int(digit) + 7
            self.d.shell(f"input keyevent {keycode}")
            time.sleep(0.35)
        time.sleep(1)

    # ------------------------------------------------------------------ #
    #  DB-backed assertions (pass db=None to skip gracefully)
    # ------------------------------------------------------------------ #

    def check_otp_verified_db(self, db, user_id):
        if not db:
            return None
        from utils.queries import get_otp_verified
        return get_otp_verified(db, user_id)

    def check_state_db(self, db, user_id):
        if not db:
            return None
        from utils.queries import get_state
        return get_state(db, user_id)
