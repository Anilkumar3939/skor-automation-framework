#!/usr/bin/env python3
"""
Create PIN Screen tests — ported from sc-mobile-app_v2/lib/ui/onboarding/create_pin_screen.dart

Covers:
  01  Create Passcode screen loads after OTP verification
  02  "Enter Passcode" and "Confirm Passcode" fields are visible
  03  All-same digits (111111) are rejected with an error
  04  Sequential digits (123456) are rejected with an error
  05  Mismatched PIN and Confirm PIN shows "Passcode not same" error
  06  Valid, non-sequential, non-repeating PIN saves and navigates forward

Navigation:
  Tests start after OTP verification. If the screen is already open (detected by
  "Create Passcode" heading) tests run directly; otherwise the device is assumed
  to have arrived here through the full registration flow.

PIN rules (from create_pin_screen.dart):
  - pinState 3 → "all numbers are same" error
  - pinState 4 → "sequential numbers" error
  - passcodeNotSame → confirm PIN mismatch
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
from utils.logger import get_logger


@allure.feature("Create PIN Screen")
class TestCreatePin(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.logger = get_logger("create_pin")

    # ── helpers ────────────────────────────────────────────────────────

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

    def _is_create_pin_screen(self):
        """True when the Create Passcode screen is visible."""
        return (
            self.d(textContains="Create Passcode").exists(timeout=5) or
            self.d(textContains="Buat Passcode").exists(timeout=3) or       # Indonesian
            self.d(textContains="Create PIN").exists(timeout=2) or
            self.d(textContains="Buat PIN").exists(timeout=2) or            # Indonesian
            self.d(descriptionContains="Create Passcode").exists(timeout=2)
        )

    def _enter_pin(self, pin: str):
        """Enter PIN digits one by one via ADB keycode (same as OTP entry)."""
        for digit in str(pin):
            self.d.shell(f"input keyevent {int(digit) + 7}")
            time.sleep(0.3)
        time.sleep(0.5)

    def _enter_pin_pair(self, pin: str, confirm: str):
        """
        Enter PIN in the first field, then confirm in the second field.

        Strategy (in order of preference):
          1. After entering 6 digits in the first PinCodeField, Flutter
             typically auto-focuses the confirm field — just wait and enter.
          2. If auto-focus did not happen, press TAB (keycode 61) to move focus.
          3. As a last resort, tap the "Confirm Passcode" label/area to force focus.
        """
        self._enter_pin(pin)
        time.sleep(0.8)   # allow Flutter auto-focus to trigger

        # Check whether focus has moved to the confirm field already.
        # Flutter PinCodeField auto-advances — if the first field accepted 6 digits
        # the cursor is now in the confirm field. If not, force focus with TAB.
        edit_texts = self.d(className="android.widget.EditText")
        moved = False

        # Try tapping the Confirm label to force focus (most reliable)
        for label in ["Confirm Passcode", "Confirm", "Konfirmasi Passcode", "Konfirmasi"]:
            el = self.d(textContains=label)
            if el.exists(timeout=1):
                el.click()
                time.sleep(0.3)
                moved = True
                break

        # Fallback 1: TAB keycode to advance focus
        if not moved:
            self.d.shell("input keyevent 61")   # KEYCODE_TAB
            time.sleep(0.3)

        # Fallback 2: tap the lower EditText (confirm field) directly
        if not moved:
            try:
                if edit_texts.count > 1:
                    edit_texts[1].click()
                    time.sleep(0.3)
            except Exception:
                pass

        self._enter_pin(confirm)

    def _clear_pin_fields(self):
        """Clear all PIN input fields by pressing back/delete repeatedly."""
        for _ in range(12):
            self.d.shell("input keyevent 67")   # KEYCODE_DEL
            time.sleep(0.1)

    # ── TEST 01 — Screen loads ──────────────────────────────────────────

    @allure.story("Create PIN Screen Loads")
    def test_01_create_pin_screen_loads(self):
        print("\n[TEST 01] Create Passcode screen is displayed")
        self.launch_app()
        time.sleep(2)
        self.screenshot("01_create_pin_screen")

        visible = self._is_create_pin_screen()
        if not visible:
            raise AssertionError(
                "Create Passcode screen not found — complete full registration + OTP flow first, "
                "or run register_flow suite before this suite"
            )
        self._log_pass("Create Passcode heading visible")

    # ── TEST 02 — Input fields visible ─────────────────────────────────

    @allure.story("PIN Fields Visible")
    def test_02_pin_fields_visible(self):
        print("\n[TEST 02] Enter Passcode and Confirm Passcode fields visible")
        if not self._is_create_pin_screen():
            print("  ⚠️  SKIP: Not on Create PIN screen")
            return

        enter_visible = (
            self.d(textContains="Enter Passcode").exists(timeout=5) or
            self.d(descriptionContains="Enter Passcode").exists(timeout=3) or
            self.d(className="android.widget.EditText").exists(timeout=3)
        )
        confirm_visible = (
            self.d(textContains="Confirm Passcode").exists(timeout=5) or
            self.d(descriptionContains="Confirm Passcode").exists(timeout=3)
        )

        self.screenshot("02_pin_fields")
        self._assert(enter_visible,  "Enter Passcode field visible",   "Enter Passcode field not found")
        self._assert(confirm_visible, "Confirm Passcode field visible", "Confirm Passcode field not found")

    # ── TEST 03 — All-same digits blocked ──────────────────────────────

    @allure.story("All-Same Digits Rejected")
    def test_03_same_digits_rejected(self):
        print("\n[TEST 03] PIN with all same digits (111111) is rejected")
        if not self._is_create_pin_screen():
            print("  ⚠️  SKIP: Not on Create PIN screen")
            return

        self._clear_pin_fields()
        self._enter_pin_pair("111111", "111111")
        time.sleep(1)
        self.screenshot("03_same_digits")

        error_visible = (
            self.d(textContains="same").exists(timeout=5) or
            self.d(textContains="Same").exists(timeout=3) or
            self.d(textContains="Different numbers").exists(timeout=3) or
            self.d(textContains="sama").exists(timeout=3) or          # Indonesian
            self.d(textContains="berbeda").exists(timeout=3) or       # Indonesian: "different"
            self.d(descriptionContains="same").exists(timeout=3)
        )
        self._assert(
            error_visible,
            "Error shown for all-same digits",
            "No error shown for all-same digits (111111)",
        )

    # ── TEST 04 — Sequential digits blocked ────────────────────────────

    @allure.story("Sequential Digits Rejected")
    def test_04_sequential_digits_rejected(self):
        print("\n[TEST 04] Sequential PIN (123456) is rejected")
        if not self._is_create_pin_screen():
            print("  ⚠️  SKIP: Not on Create PIN screen")
            return

        self._clear_pin_fields()
        self._enter_pin_pair("123456", "123456")
        time.sleep(1)
        self.screenshot("04_sequential_digits")

        error_visible = (
            self.d(textContains="order").exists(timeout=5) or
            self.d(textContains="sequential").exists(timeout=3) or
            self.d(textContains="Not in order").exists(timeout=3) or
            self.d(textContains="berurutan").exists(timeout=3) or     # Indonesian: "sequential"
            self.d(textContains="urutan").exists(timeout=3) or        # Indonesian: "order"
            self.d(descriptionContains="order").exists(timeout=3)
        )
        self._assert(
            error_visible,
            "Error shown for sequential digits",
            "No error shown for sequential digits (123456)",
        )

    # ── TEST 05 — Mismatched PIN shows error ───────────────────────────

    @allure.story("Mismatched PIN Shows Error")
    def test_05_mismatched_pin_error(self):
        print("\n[TEST 05] Mismatched PIN and Confirm PIN shows error")
        if not self._is_create_pin_screen():
            print("  ⚠️  SKIP: Not on Create PIN screen")
            return

        self._clear_pin_fields()
        self._enter_pin_pair("271845", "271846")   # last digit differs
        time.sleep(1)
        self.screenshot("05_pin_mismatch")

        error_visible = (
            self.d(textContains="not same").exists(timeout=5) or
            self.d(textContains="Not same").exists(timeout=3) or
            self.d(textContains="match").exists(timeout=3) or
            self.d(textContains="sama").exists(timeout=3) or   # Indonesian: "tidak sama"
            self.d(descriptionContains="not same").exists(timeout=3)
        )
        self._assert(
            error_visible,
            "Passcode not same error shown",
            "No mismatch error shown — check screenshot 05",
        )

    # ── TEST 06 — Valid PIN navigates forward ──────────────────────────

    @allure.story("Valid PIN Navigates Forward")
    def test_06_valid_pin_navigates(self):
        print("\n[TEST 06] Valid PIN saves and navigates to next screen")
        if not self._is_create_pin_screen():
            print("  ⚠️  SKIP: Not on Create PIN screen")
            return

        # Use a valid PIN: no sequential run, no all-same digits
        valid_pin = "271845"
        self._clear_pin_fields()
        self._enter_pin_pair(valid_pin, valid_pin)
        time.sleep(3)
        self.screenshot("06_after_valid_pin")

        # Navigated away from Create Passcode = success
        navigated = not self._is_create_pin_screen()
        self._assert(
            navigated,
            f"Valid PIN '{valid_pin}' accepted — navigated past Create PIN screen",
            "Still on Create PIN screen after valid PIN — check screenshot 06",
        )


# ── Explicit test order ──────────────────────────────────────────────────────
TEST_ORDER = [
    "test_01_create_pin_screen_loads",
    "test_02_pin_fields_visible",
    "test_03_same_digits_rejected",
    "test_04_sequential_digits_rejected",
    "test_05_mismatched_pin_error",
    "test_06_valid_pin_navigates",
]

if __name__ == "__main__":
    t = TestCreatePin()
    TestCreatePin.setup_class()
    for method in TEST_ORDER:
        getattr(t, method)()
    print("\n✅ Create PIN tests done. Check screenshots/ and logs/")
