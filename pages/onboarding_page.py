#!/usr/bin/env python3
"""
OnboardingPage — Page Object for the KYC Initial Identity Form screen.
Maps to: sc-mobile-app_v2/lib/ui/onboarding/initial_identity_form_page.dart

English strings (from intl_en.arb):
  Page title  : "See your limit in 2 minutes!"
  Description : "Fill out the form below to see your application approval"
  Full Name   : "Full name as stated on your KTP"     (label text)
  NIK label   : "NIK"
  Income label: "Monthly income"
  Submit btn  : "Set up my application"
  T&C snippet : "T&Cs, "                              (tappable span)
  T&C page    : "Terms of Use of Skorcard"
  Validation  : "Please enter your full name as stated on your KTP"
                "NIK has to be 16 digits"
                "Make sure the NIK you enter matches your KTP details"
                "Invalid Characters"

Field rules (from Flutter source):
  Full Name : letters + spaces only (FilteringTextInputFormatter.allow([a-zA-Z\\s]))
  NIK       : digits only, max 16, no leading zero
  Income    : digits only, max 12, displayed with dot separators (1.000.000)
  Checkbox  : must be checked for the form to be valid
"""
import time

from pages.base_page import BasePage


class OnboardingPage(BasePage):

    # ── Accessibility / text identifiers ────────────────────────────────
    TITLE       = "See your limit in 2 minutes!"
    TITLE_ID    = "Lihat limit kamu dalam 2 menit!"   # Indonesian

    SUBMIT_BTN  = "Set up my application"
    SUBMIT_BTN_ID = "Atur aplikasi saya"               # Indonesian

    TC_LINK     = "T&Cs, "                             # tappable RichText span
    TC_LINK_ALT = "T&C"
    TC_TITLE    = "Terms of Use of Skorcard"
    TC_TITLE_ID = "Syarat dan Ketentuan Skorcard"

    BACK_ICON   = "Navigate up"

    # Field label texts (floating labels in SCTextField)
    LABEL_FULL_NAME = "Full name as stated on your KTP"
    LABEL_NIK       = "NIK"
    LABEL_INCOME    = "Monthly income"

    # Validation messages
    VAL_FULL_NAME     = "Please enter your full name as stated on your KTP"
    VAL_NIK_16        = "NIK has to be 16 digits"
    VAL_NIK_INVALID   = "Make sure the NIK you enter matches your KTP details"
    VAL_NIK_DUP       = "The NIK you entered is already registered"
    VAL_INVALID_CHARS = "Invalid Characters"

    # EditText instance indices on the form (0-based, top to bottom)
    IDX_FULL_NAME = 0
    IDX_NIK       = 1
    IDX_INCOME    = 2

    # ── Page detection ───────────────────────────────────────────────────

    def is_displayed(self, timeout=3):
        """True when the onboarding initial identity form is on screen."""
        return (
            self.d(description=self.TITLE).exists(timeout=timeout)
        )

    def get_title_text(self):
        """Return the visible page title text (useful for assertion messages)."""
        for title in [self.TITLE, self.TITLE_ID]:
            if self.d(description=title).exists(timeout=3):
                return title
        return ""

    # ── Scroll helpers ───────────────────────────────────────────────────

    def dismiss_keyboard(self):
        """Tap outside the fields to close the keyboard."""
        el = self._by_class("android.widget.ScrollView", timeout=3)
        if el:
            el.click()
            time.sleep(0.4)

    def scroll_to_bottom(self):
        """Scroll down to reveal T&C checkbox and submit button."""
        self.d.swipe(500, 1400, 500, 400, 0.4)
        time.sleep(0.4)

    def scroll_to_top(self):
        """Scroll up to reveal the top of the form."""
        self.d.swipe(500, 400, 500, 1400, 0.4)
        time.sleep(0.4)

    # ── Submit button ────────────────────────────────────────────────────

    # def is_submit_enabled(self):
    #     """
    #     True when the submit button is active (form fully valid).
    #     The button color changes but the element is always present.
    #     We check enabled + clickable attributes.
    #     """
    #     for label in [self.SUBMIT_BTN, self.SUBMIT_BTN_ID]:
    #         el = self.d(description=label)
    #         if el.exists(timeout=3):
    #             info = el.info
    #             return info.get("enabled", False) and info.get("clickable", False)

    #     return False

    def click_submit(self):
        """Tap the submit button. Scrolls down first if needed."""
        self.scroll_to_bottom()
        time.sleep(0.3)
        for label in [self.SUBMIT_BTN, self.SUBMIT_BTN_ID]:
            if self.tap_text(label):
                return True
            if self.tap_desc(label):
                return True
        return False

    # ── T&C checkbox ────────────────────────────────────────────────────

    def get_tc_checkbox_state(self):
        """Return True/False/None for checked state."""
        try:
            el = self._by_class("android.widget.CheckBox", timeout=5)
            if el:
                return bool(el.info.get("checked"))
        except Exception:
            pass
        return None

    def set_tc_checkbox(self, checked=True):
        """Ensure the T&C checkbox is in the requested state."""
        el = self._by_class("android.widget.CheckBox", timeout=5)
        if not el:
            return False
        current = bool(el.info.get("checked"))
        if current != checked:
            el.click()
            time.sleep(0.4)
        refreshed = self._by_class("android.widget.CheckBox", timeout=2)
        return bool(refreshed.info.get("checked")) == checked if refreshed else False

    def click_tc_link(self):
        """Tap the T&C hyperlink inside the agreement text."""
        for label in [self.TC_LINK, self.TC_LINK_ALT, "T&C", "T&Cs"]:
            if self.tap_desc(label, timeout=3):
                return True
            if self.tap_text(label, timeout=3):
                return True
        # Fallback: tap the agreement text area (contains the T&C link)
        el = self.d(description="T&C, ")
        if el.exists(timeout=3):
            el.click()
            time.sleep(0.4)
            return True
        return False

    def is_tc_page_displayed(self):
        """True when the Terms of Use webview page is open."""
        return (
            self.exists_desc(self.TC_TITLE, timeout=10) or
            self.d(description="Terms of Use of Skorcard").exists(timeout=5) or
            self.d(description="Syarat dan Ketentuan").exists(timeout=3)
        )

    def back_to_onboarding(self):
        """Navigate back from T&C / sub-page to the onboarding form."""
        if not self.tap_desc(self.BACK_ICON, timeout=3):
            self.back()
        time.sleep(0.5)

    # ── Field: Full Name ─────────────────────────────────────────────────

    def enter_full_name(self, name: str):
        """
        Enter full name. Uses set_text; falls back to ADB input for restricted fields.
        Clears the field first.
        """
        el = self._by_class("android.widget.EditText", self.IDX_FULL_NAME, timeout=8)
        if not el:
            print("  ⚠️  Full name field not found")
            return
        try:
            el.click()
            time.sleep(0.3)
            el.clear_text()
            el.set_text(name)
        except Exception as exc:
            print(f"  ⚠️  set_text failed, using ADB fallback: {exc}")
            safe = name.replace(" ", "%s")
            self.d.shell(f"input text {safe}")
        time.sleep(0.4)

    def clear_full_name(self):
        el = self._by_class("android.widget.EditText", self.IDX_FULL_NAME, timeout=5)
        if el:
            el.click()
            el.clear_text()
            time.sleep(0.3)

    def get_full_name(self):
        return self.get_edit_text(self.IDX_FULL_NAME)

    def get_full_name_placeholder(self):
        return self.get_edit_hint(self.IDX_FULL_NAME)

    # ── Field: NIK ───────────────────────────────────────────────────────

    def enter_nik(self, nik: str):
        el = self._by_class("android.widget.EditText", self.IDX_NIK, timeout=8)
        if el:
            el.click()
            time.sleep(0.3)
            el.clear_text()
            el.set_text(nik)
            time.sleep(0.3)

    def clear_nik(self):
        el = self._by_class("android.widget.EditText", self.IDX_NIK, timeout=5)
        if el:
            el.click()
            el.clear_text()
            time.sleep(0.3)

    def get_nik(self):
        return self.get_edit_text(self.IDX_NIK)

    def get_nik_placeholder(self):
        return self.get_edit_hint(self.IDX_NIK)

    # ── Field: Monthly Income ────────────────────────────────────────────

    def enter_monthly_income(self, amount: str):
        """
        Enter monthly income. The field uses dot-separated formatting (e.g. 5.000.000).
        Pass a plain digit string; the app formats it automatically.
        """
        el = self._by_class("android.widget.EditText", self.IDX_INCOME, timeout=8)
        if el:
            el.click()
            time.sleep(0.3)
            el.clear_text()
            el.set_text(amount)
            time.sleep(0.4)

    def get_income_placeholder(self):
        return self.get_edit_hint(self.IDX_INCOME)

    def get_income_text(self):
        return self.get_edit_text(self.IDX_INCOME)

    # ── Validation messages ──────────────────────────────────────────────

    def get_full_name_validation(self):
        """Return validation message text if visible, else None."""
        for msg in [self.VAL_FULL_NAME, self.VAL_INVALID_CHARS]:
            if (self.exists_desc(msg, timeout=3) or
                    self.d(textContains=msg[:30]).exists(timeout=2)):
                return msg
        return None

    def get_nik_validation(self):
        for msg in [self.VAL_NIK_16, self.VAL_NIK_INVALID, self.VAL_NIK_DUP]:
            if (self.exists_desc(msg, timeout=3) or
                    self.d(textContains=msg[:30]).exists(timeout=2)):
                return msg
        return None

    def get_nik_duplicate_validation(self):
        for msg in [self.VAL_NIK_DUP]:
            if (self.exists_desc(msg, timeout=3) or
                    self.d(textContains="already registered").exists(timeout=2) or
                    self.d(textContains="sudah terdaftar").exists(timeout=2)):
                return msg
        return None

    # ── Convenience: fill the whole form ────────────────────────────────

    def fill_valid_form(self, name="Qaisar Bashir", nik="3171234567890123",
                        income="5000000"):
        """
        Fill all three fields with valid data and check the T&C box.
        NIK must be exactly 16 digits and not start with 0.
        """
        self.enter_full_name(name)
        self.enter_nik(nik)
        self.enter_monthly_income(income)

        if not self.get_tc_checkbox_state():
            self.scroll_to_bottom()
            self.set_tc_checkbox(True)
