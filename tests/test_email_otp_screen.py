import time
import allure

from base import BaseTest
from pages.email_otp_page import EmailOTPPage
from utils.email_utils import EmailReader


@allure.feature("Email OTP Screen")
class EmailOTPTest(BaseTest):

    @classmethod
    def setup_class(cls):

        super().setup_class()

        cls.email_otp = EmailOTPPage(cls.d)

    # ---------------------------
    # helper methods
    # ---------------------------

    def _log_pass(self, msg):
        print(f"  ✅ PASS: {msg}")

    def _log_fail(self, msg):
        print(f"  ❌ FAIL: {msg}")

    def _assert(self, condition, pass_msg, fail_msg):

        if condition:
            self._log_pass(pass_msg)
        else:
            self._log_fail(fail_msg)

        return condition

    def _navigate_to_email_otp(self):

        visible = self.email_otp.is_visible()

        return visible

    def _require_email_otp_screen(self):

        assert self._assert(
            self.email_otp.is_visible(),
            "Email OTP screen visible",
            "Email OTP screen not visible"
        )

    # ---------------------------
    # TEST 01
    # ---------------------------

    @allure.story("Email OTP Load")
    def test_01_email_otp_screen(self):

        print("\n[TEST 01] Email OTP screen load")

        visible = self._navigate_to_email_otp()

        self.screenshot("01_email_otp_screen")

        assert self._assert(
            visible,
            "Email OTP screen loaded",
            "Email OTP screen not loaded"
        )

    # ---------------------------
    # TEST 02
    # ---------------------------

    @allure.story("Wrong Email OTP")
    def test_02_wrong_email_otp(self):

        print("\n[TEST 02] Wrong email OTP")

        self._require_email_otp_screen()

        self.email_otp.clear_otp_field()

        self.email_otp.enter_otp(
            "000000"
        )

        time.sleep(2)

        error = self.email_otp.poll_for_wrong_otp_error(
            poll_duration=6
        )

        self.screenshot(
            "02_wrong_otp_error"
        )

        assert self._assert(
            error,
            "Error shown for wrong OTP",
            "No error shown for wrong OTP"
        )

    # ---------------------------
    # TEST 03
    # ---------------------------

    @allure.story("Correct Email OTP")
    def test_03_verify_email_otp(self):

        print("\n[TEST 03] Verify correct OTP")

        self._require_email_otp_screen()

        otp = EmailReader.get_latest_otp()

        assert self._assert(
            otp is not None,
            f"OTP fetched: {otp}",
            "OTP not received"
        )

        print(f"📩 OTP = {otp}")

        self.email_otp.clear_otp_field()

        self.email_otp.enter_otp(
            otp
        )

        success = False

        end = time.time() + 10

        while time.time() < end:

            # screen disappeared
            if not self.email_otp.is_visible():
                success = True
                break

            # success page indicators
            if self.d(
                    textContains="Welcome"
            ).exists(timeout=.3):

                success = True
                break

            if self.d(
                    descriptionContains="Home"
            ).exists(timeout=.3):

                success = True
                break

            if self.d(
                    descriptionContains="Dashboard"
            ).exists(timeout=.3):

                success = True
                break

            time.sleep(.5)

        self.screenshot(
            "03_email_otp_verified"
        )

        assert self._assert(
            success,
            "OTP verified successfully",
            "OTP verification failed"
        )

    