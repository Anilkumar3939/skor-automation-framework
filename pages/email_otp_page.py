import re
import time
from pages.base_page import BasePage


class EmailOTPPage(BasePage):

    EMAIL_OTP_TEXTS = [
        "Enter the OTP code",
        "Verification",
        "Email Verification",
        "OTP CODE"
    ]

    WRONG_OTP_TEXTS = [
        "wrong",
        "incorrect",
        "invalid"
    ]

    RESEND_TEXTS = [
        "Resend",
        "Resend Code"
    ]

    def is_visible(self, timeout=5):

        for txt in self.EMAIL_OTP_TEXTS:

            if self.d(textContains=txt).exists(timeout=1):
                return True

            if self.d(descriptionContains=txt).exists(timeout=1):
                return True

        return False
    

    def poll_for_wrong_otp_error(self, poll_duration=5):
        error_xpath = '//android.view.View[@content-desc="OTP code is incorrect."]'
        close_xpath = '//android.view.View[@content-desc="OTP code is incorrect."]/android.widget.ImageView[2]'

        end = time.time() + poll_duration

        while time.time() < end:
            error_el = self.d.xpath(error_xpath)

            if error_el.exists:
                # click cross icon to clear OTP field
                close_el = self.d.xpath(close_xpath)

                if close_el.exists:
                    close_el.click()
                    time.sleep(0.5)

                return True

            time.sleep(0.15)

        return False

    def enter_otp(self, otp):

        for digit in str(otp):
            self.d.shell(
                f"input keyevent {int(digit)+7}"
            )
            time.sleep(0.2)

    def clear_otp_field(self):

        for _ in range(8):
            self.d.shell("input keyevent 67")
            time.sleep(.1)

    def tap_resend(self):

        for txt in self.RESEND_TEXTS:

            el = self.d(textContains=txt)

            if el.exists(timeout=2):
                el.click()
                return True

        return False
    