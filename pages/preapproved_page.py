import time


class PreApprovedPage:
    def __init__(self, d):
        self.d = d

    # ───────────────────────────────────────────────
    # PAGE IDENTIFICATION
    # ───────────────────────────────────────────────

    def is_displayed(self, timeout=5):
        return (
            self.d(descriptionContains="pre-approved").exists(timeout=timeout) or
            self.d(descriptionContains="Continue application").exists(timeout=timeout)
        )
    
    def is_email_page_displayed(self, timeout=5):
        return (
            self.d(textContains="Email").exists(timeout=timeout) or
            self.d(descriptionContains="Email").exists(timeout=timeout)
        )

    # ───────────────────────────────────────────────
    # CONTINUE BUTTON
    # ───────────────────────────────────────────────

    def is_continue_visible(self):
        return self.d(descriptionContains="Continue").exists(timeout=5)

    def click_continue(self):
        print("  👉 Clicking Continue button")

        btn = self.d(descriptionContains="Continue application")
        if btn.exists(timeout=5):
            btn.click()
        else:
            raise Exception("Continue button not found")

        time.sleep(1)

    # ───────────────────────────────────────────────
    # T&C LINKS
    # ───────────────────────────────────────────────

    def click_privacy(self):
        print("  👉 Clicking Privacy Policy")

        el = self.d(descriptionContains="Privacy")
        if el.exists(timeout=5):
            el.click()
        else:
            raise Exception("Privacy link not found")

    def click_terms(self):
        print("  👉 Clicking Terms & Conditions")

        el = self.d(descriptionContains="Terms")
        if el.exists(timeout=5):
            el.click()
        else:
            raise Exception("Terms link not found")

    def is_webview_opened(self):
        """
        Basic check for webview screen
        """
        return (
            self.d(className="android.webkit.WebView").exists(timeout=5) or
            self.d(descriptionContains="webview").exists(timeout=2)
        )

    # ───────────────────────────────────────────────
    # CHIPS (BOTTOM SHEETS)
    # ───────────────────────────────────────────────

    def pre_approved_limit_visible(self):
        return self.d(descriptionContains="Rp49.000.000").exists(timeout=5)

    def click_secure_chip(self):
        print("  👉 Clicking Secure chip")

        el = self.d(descriptionContains="Secure")
        if el.exists(timeout=5):
            el.click()
        else:
            raise Exception("Secure chip not found")

    def is_secure_modal_visible(self):
        return self.d(descriptionContains="Secure").exists(timeout=5)

    def click_privacy_chip(self):
        print("  👉 Clicking Privacy chip")

        el = self.d(descriptionContains="privacy")
        if not el.exists(timeout=3):
            el = self.d(descriptionContains="Privacy")

        if el.exists(timeout=5):
            el.click()
        else:
            raise Exception("Privacy chip not found")

    def is_privacy_modal_visible(self):
        return (
            self.d(descriptionContains="privacy").exists(timeout=5) or
            self.d(descriptionContains="data").exists(timeout=3)
        )

    # ───────────────────────────────────────────────
    # CONFETTI (OPTIONAL)
    # ───────────────────────────────────────────────

    def is_confetti_visible(self):
        """
        Lottie animations are tricky → detect by generic view presence
        """
        return (
            self.d(className="android.view.View").exists(timeout=2)
        )