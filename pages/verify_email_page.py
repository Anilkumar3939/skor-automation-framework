import time


class VerifyEmailPage:
    def __init__(self, d):
        self.d = d

    # ───────────────────────────────────────────────
    # PAGE IDENTIFICATION
    # ───────────────────────────────────────────────

    def is_displayed(self, timeout=5):
        """
        Verify Email screen detection
        Strategy:
          - Heading text
          - OR presence of Gmail / Apple button
        """
        return (
            self.d(descriptionContains="Let’s connect your email").exists(timeout=timeout) and
            self.d(descriptionContains="Continue with Google").exists(timeout=2) and
            self.d(descriptionContains="Continue with Apple").exists(timeout=2) and
            self.d(descriptionContains="Continue manually").exists(timeout=2)
        )

    # ───────────────────────────────────────────────
    # BUTTON VISIBILITY
    # ───────────────────────────────────────────────

    def is_google_visible(self):
        return (
            self.d(descriptionContains="Continue with Google").exists(timeout=5)
        )

    def is_apple_visible(self):
        return self.d(descriptionContains="Continue with Apple").exists(timeout=5)

    def is_manual_email_visible(self):
        return (
            self.d(descriptionContains="Continue manually").exists(timeout=5)
        )
    def is_manual_email_page_visible(self):
        return (
            self.d(descriptionContains="Input email address").exists(timeout=5)
        )

    # ───────────────────────────────────────────────
    # CLICK ACTIONS
    # ───────────────────────────────────────────────

    def click_google(self):
        print("  👉 Clicking Continue with Google")

        el = self.d(descriptionContains="Continue with Google")

        if el.exists(timeout=5):
            el.click()
        else:
            raise Exception("Google button not found")

        time.sleep(1)

    def click_apple(self):
        print("  👉 Clicking Continue with Apple")

        el = self.d(descriptionContains="Apple")
        if el.exists(timeout=5):
            el.click()
        else:
            raise Exception("Apple button not found")

        time.sleep(1)

    def click_manual_email(self):
        print("  👉 Clicking Manual Email option")

        el = self.d(descriptionContains="Continue manually")
        if not el.exists(timeout=3):
            el = self.d(descriptionContains="Enter")

        if el.exists(timeout=5):
            el.click()
        else:
            raise Exception("Manual Email option not found")

        time.sleep(1)
    
    def Enter_email(self, email):
        print(f"  ✉️ Entering email: {email}")

        input_field = self.d(className="android.widget.EditText")
        if input_field.exists(timeout=5):
            input_field.set_text(email)
        else:
            raise Exception("Email input field not found")

        time.sleep(1)

    def Enter_otp(self, otp):
        print(f"  🔢 Entering OTP: {otp}")

        input_field = self.d(className="android.widget.EditText")
        if input_field.exists(timeout=5):
            input_field.set_text(otp)
        else:
            raise Exception("OTP input field not found")

        time.sleep(1)



    # ───────────────────────────────────────────────
    # NAVIGATION CHECKS
    # ───────────────────────────────────────────────

    def is_google_flow_opened(self):
        """
        Detect Google OAuth screen (best-effort)
        """
        return (
            self.d(textContains="Choose an account").exists(timeout=5) or
            self.d(descriptionContains="Sign in").exists(timeout=2)
        )

    def is_apple_flow_opened(self):
        """
        Detect Apple login screen (best-effort)
        """
        return (
            self.d(descriptionContains="Apple ID").exists(timeout=5) or
            self.d(descriptionContains="Sign in with Apple").exists(timeout=2)
        )

    def is_manual_email_page_opened(self):
        """
        Detect manual email entry screen
        """
        return (
            self.d(descriptionContains="Input email address").exists(timeout=5) and
            self.d(className="android.widget.EditText").exists(timeout=3) and
            self.d(descriptionContains="Continue").exists(timeout=3)
        )

    # ───────────────────────────────────────────────
    # GENERIC HELPERS
    # ───────────────────────────────────────────────

    def press_back(self):
        print("  🔙 Pressing back")
        self.d.press("back")
        time.sleep(1)