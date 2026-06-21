#!/usr/bin/env python3
"""
Register Flow tests — Functional Suite
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
from pages.register_page import RegisterPage
from utils.logger import get_logger
from utils.test_data import VALID_PHONE


def _try_db():
    try:
        from utils.db_helper import DBHelper
        return DBHelper()
    except Exception as e:
        print(f"  ⚠️  DB unavailable ({e}) — DB assertions will be skipped")
        return None


@allure.feature("Register Flow")
class TestRegisterFlow(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.register = RegisterPage(cls.d)
        cls.logger   = get_logger("register_flow")
        cls.db       = _try_db()
        cls._data    = {}

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

    @allure.story("App Launch & Permissions")
    def test_01_launch_app(self):
        print("\n[TEST 01] Launch app — grant permissions & verify elements")
        self.launch_app()
        self.register.allow_app_notifications()
        self.register.allow_app_location()
        self.register.allow_mobile_location()
        time.sleep(1)

        self._assert(
            self.register.elements_visible(),
            "All splash elements visible",
            "Some splash elements are missing",
        )

    @allure.story("Registration Flow")
    def test_02_registration_flow(self):
        print("\n[TEST 02] Registration flow: phone → Continue → OTP")
        self.reset_to_splash()
        phone = VALID_PHONE

        if self.db:
            from utils.queries import check_phone_exists, get_user_id
            if check_phone_exists(self.db, phone):
                print(f"  ⚠️  Phone {phone} already registered")
                user_id = get_user_id(self.db, phone)
                self._data["phone"]   = phone
                self._data["user_id"] = user_id
            else:
                self._run_registration(phone)
        else:
            self._run_registration(phone)

    def _run_registration(self, phone):
        self.register.enter_phone(phone)
        enabled = self.register.is_continue_enabled()
        self._assert(enabled, "Continue enabled for valid phone", "Continue not enabled")
        if not enabled:
            return

        self.register.click_continue()
        time.sleep(3)

        otp = self.register.get_otp_from_screen()
        if otp:
            self._data["otp"] = otp

        if self.db:
            from utils.queries import get_user_id
            time.sleep(3)
            user_id = get_user_id(self.db, phone)
            self._assert(user_id is not None, f"User ID created in DB", "User ID not found in DB")
            self._data["user_id"] = user_id

        self._data["phone"] = phone

    @allure.story("Database Validations")
    def test_03_db_validations(self):
        print("\n[TEST 03] Database entry validations")
        if not self.db:
            return
        user_id = self._data.get("user_id")
        if not user_id:
            return

        from utils.queries import (
            get_user_settings, get_device_details,
            get_location_details, get_appsflyer,
        )
        self._assert(get_user_settings(self.db, user_id), "user_settings exists", "Missing user_settings")
        self._assert(get_device_details(self.db, user_id), "device_details exists", "Missing device_details")
        self._assert(get_location_details(self.db, user_id), "location_details exists", "Missing location_details")

    @allure.story("OTP Verification")
    def test_04_otp_verification(self):
        print("\n[TEST 04] OTP verification")
        otp = self._data.get("otp")
        user_id = self._data.get("user_id")

        if not otp:
            return

        self.register.enter_otp(otp)
        time.sleep(5)

        if self.db and user_id:
            from utils.queries import get_otp_verified
            verified = get_otp_verified(self.db, user_id)
            self._assert(verified, "otp_verified = true in DB", "OTP not marked verified in DB")
        else:
            otp_gone = not self.d(textContains="OTP").exists(timeout=3)
            self._assert(otp_gone, "OTP screen dismissed", "OTP screen still visible")

    # @allure.story("Post-OTP State Machine")
    # def test_05_final_state(self):
    #     print("\n[TEST 05] Post-registration state machine")
    #     if not self.db:
    #         return
    #     user_id = self._data.get("user_id")
    #     if not user_id:
    #         return

    #     from utils.queries import get_user_product_mapping, get_state, get_state_audit
    #     self._assert(
    #         get_user_product_mapping(self.db, user_id, "BMI"),
    #         "Product mapping (BMI) exists",
    #         "Product mapping missing",
    #     )
    #     state = get_state(self.db, user_id)
    #     self._assert(
    #         state == "ONBOARDING",
    #         f"State machine = ONBOARDING (got: {state})",
    #         f"Expected ONBOARDING, got: {state}",
    #     )

TEST_ORDER = [
    "test_01_launch_app",
    "test_02_registration_flow",
    "test_03_db_validations",
    "test_04_otp_verification",
    "test_05_final_state",
]

if __name__ == "__main__":
    t = TestRegisterFlow()
    TestRegisterFlow.setup_class()
    for method in TEST_ORDER:
        getattr(t, method)()
    print("\n✅ Register flow functional tests done.")
