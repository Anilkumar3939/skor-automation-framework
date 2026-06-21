# pages/otp_page.py

import re
import time

from pages.base_page import BasePage


class OTPPage(BasePage):

    OTP_SCREEN_TEXTS = ["OTP", "Verification", "verification", "Verifikasi", "Kode",
                        "kode", "Enter code", "Enter Code"]
    WRONG_OTP_TEXTS  = ["wrong", "Wrong", "incorrect", "Invalid", "salah", "tidak valid",
                        "Salah", "Incorrect"]
    RESEND_TEXTS     = ["Resend", "resend", "Resend Code", "Kirim ulang", "Kirim Ulang"]

    def is_visible(self, timeout=5):
        for txt in self.OTP_SCREEN_TEXTS:
            if self.d(textContains=txt).exists(timeout=min(timeout, 3)):
                return True
            if self.d(descriptionContains=txt).exists(timeout=1):
                return True
        return False

    def _extract_six_digit_otp(self, raw_text):
        if not raw_text:
            return None
        match = re.search(r"\b(\d{6})\b", raw_text)
        return match.group(1) if match else None

    def get_otp_from_notification(self, timeout=3):
        """
        Try to read a 6-digit OTP from an Android notification/toast element
        whose description or text contains a "code sent" success marker.
        """
        success_markers = [
            "Code successfully sent", "Kode berhasil", "successfully sent",
            "berhasil dikirim", "successfully", "berhasil",
        ]
        end = time.time() + timeout
        while time.time() < end:
            for marker in success_markers:
                for el in [self.d(descriptionContains=marker),
                           self.d(textContains=marker)]:
                    if el.exists(timeout=0.1):
                        info = el.info or {}
                        raw = (info.get("content-desc", "") or
                               info.get("contentDescription", "") or
                               info.get("text", ""))
                        otp = self._extract_six_digit_otp(raw)
                        if otp:
                            return otp
            time.sleep(0.2)
        return None

    def enter_otp(self, otp: str, delay=0.35):
        for digit in str(otp):
            self.d.shell(f"input keyevent {int(digit) + 7}")
            time.sleep(delay)

    def enter_wrong_otp(self, otp="000000"):
        self.enter_otp(otp, delay=0.25)

    def clear_otp_field(self):
        """Delete all digits from the OTP input field."""
        for _ in range(8):           # 8 > 6 to be safe with focus issues
            self.d.shell("input keyevent 67")   # KEYCODE_DEL
            time.sleep(0.15)
        time.sleep(0.4)

    def is_wrong_otp_error_visible(self, timeout=5):
        t = min(timeout, 0.3)
        for txt in self.WRONG_OTP_TEXTS:
            if self.d(textContains=txt).exists(timeout=t):
                return True
            if self.d(descriptionContains=txt).exists(timeout=t):
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

    def is_resend_visible(self, timeout=5):
        for txt in self.RESEND_TEXTS:
            if self.d(descriptionContains=txt).exists(timeout=min(timeout, 3)):
                return True
            if self.d(descriptionContains=txt).exists(timeout=2):
                return True
        return False

    def is_resend_enabled(self, timeout=3):
        """True when the Resend element is present AND clickable (no countdown active)."""
        for txt in self.RESEND_TEXTS:
            el = self.d(descriptionContains=txt)
            if el.exists(timeout=min(timeout, 2)):
                info = el.info
                # During countdown the element is NOT clickable
                if info.get("clickable", False):
                    return True
        return False

    def tap_resend(self):
        """Tap Resend Code. Returns True if the element was found and tapped."""
        for txt in self.RESEND_TEXTS:
            el = self.d(descriptionContains=txt)
            if el.exists(timeout=3):
                el.click()
                time.sleep(1)
                return True
        return False

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