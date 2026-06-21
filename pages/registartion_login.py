import time
from  tests.base import APP_PACKAGE
from pages.base_page import BasePage

class RegistrationLogin(BasePage):

    # ---------------- NAVIGATION ---------------- #

    def _is_on_splash(self):
        return (
            self.d(description="Continue").exists(timeout=3) and
            self.d(className="android.widget.EditText").exists(timeout=2)
        )
    
    def _click_back_to_splash(self):
        self.d.press(className="android.widget.ImageButton", timeout=3).click()

    def _navigate_to_registration(self):
        self.d.app_start(APP_PACKAGE)
        time.sleep(1)

        if self.d(description="Continue").exists(timeout=3):
            return True

        return self.d(description="Continue").exists(timeout=10)

    def _clear_phone(self):
        el = self.d(className="android.widget.EditText")
        if el.exists(timeout=5):
            el.click()
            time.sleep(0.5)
            el.set_text("23")
            el.set_text("")
            time.sleep(0.3)

    def _enter_phone(self, number: str):
        el = self.d(className="android.widget.EditText", instance=0)     
        if not el.exists(timeout=8):
            self._log_fail("Phone input not found")
            return
        el.click()
        time.sleep(3)
        el.set_text(number)
        time.sleep(0.5)

    def _is_proceed_enabled(self):
        try:
            btn = self.d(description="Continue")
            if not btn.exists(timeout=3):
                return False
            btn.click()  # to trigger any potential validation
            return not self._is_on_splash()
        except:
            return False
    def _open_invite_sheet(self):
        """
        Tap the 'Do you have an invitation code?' link.
        Scrolls down slightly first (link can be below the initial viewport),
        then tries multiple selector strategies (EN + ID).
        """
        self.d.swipe(500, 900, 500, 600, 0.3)
        time.sleep(1)          # let the UI settle after scroll

        selectors = [
            {"description":        "Do you have an invitation code?"},
            {"descriptionContains":"invitation code"},
            {"descriptionContains":"Invitation Code"},
            {"text":               "Do you have an invitation code?"},
            {"textContains":       "invitation code"},
            {"textContains":       "Have an invitation"},
            {"textContains":       "invitation"},
            {"descriptionContains":"kode undangan"},
            {"textContains":       "kode undangan"},
            {"descriptionContains":"Punya kode"},
            {"textContains":       "Punya kode"},
            {"textContains":       "undangan"},
        ]
        for sel in selectors:
            el = self.d(**sel)
            if el.exists(timeout=4):
                el.click()
                time.sleep(1)
                return True

        self.screenshot("invite_link_not_found_debug")
        print("  ⚠️  invite sheet trigger not found — skipping")
        return False
    

    def _enter_invite_code(self, code: str):
        el = self.d(className="android.widget.EditText")
        if not el.exists(timeout=5):
            print("  ⚠️  invite code EditText not found")
            return False
        el.set_text(code)
        time.sleep(0.5)
        return True
    
    def _tap_sheet_continue(self):
        for sel in [{"description": "Continue"}, {"text": "Continue"},
                    {"descriptionContains": "Continue"}]:
            el = self.d(**sel)
            if el.exists(timeout=3):
                el.click()
                time.sleep(0.5)
                return True
        print("  ⚠️  Continue button not found")
        return False