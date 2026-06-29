#!/usr/bin/env python3
"""
Pre-Approved Limit Page Tests
Maps to: pre_approved_limit_page.dart

Test order:

  01  Page loads with limit and UI elements
  02  Continue button is visible
  03  Clicking Continue navigates to Create PIN page
  04  Privacy Policy link opens webview
  05  Terms & Conditions link opens webview
  06  Secure chip opens bottom sheet
  07  Privacy chip opens bottom sheet
  08  Confetti animation visible (if present)
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
from pages.preapproved_page import PreApprovedPage
from utils.logger import get_logger
from utils.db_helper import DBHelper


@allure.feature("Pre-Approved Limit Page")
class TestPreApprovedLimit(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.page = PreApprovedPage(cls.d)
        cls.logger = get_logger("preapproved")
        cls.db = DBHelper()

    # ───────────────────────────────────────────────
    # HELPERS
    # ───────────────────────────────────────────────

    def _log_pass(self, msg):
        print(f"  ✅ PASS: {msg}")
        self.logger.info(msg)

    def _log_fail(self, msg):
        print(f"  ❌ FAIL: {msg}")
        self.logger.error(msg)

    def _assert(self, cond, pass_msg, fail_msg):
        if cond:
            self._log_pass(pass_msg)
        else:
            self._log_fail(fail_msg)
        return cond

    def _ensure_on_page(self):
        if not self.page.is_displayed():
            raise AssertionError(
                "Pre-approved page not visible. Ensure previous flow (UW success) is completed."
            )
        time.sleep(1)

    # ══════════════════════════════════════════════
    # TEST 01 — Page loads
    # ══════════════════════════════════════════════

    @allure.story("01 - Page Loads")
    def test_01_page_loads(self):
        print("\n[TEST 01] Pre-approved limit page loads correctly")
        self._ensure_on_page()
        visible = self.page.is_displayed()
        self.assert_critical(visible, "Pre-approved limit page failed to load. Stopping suite.")

    # ══════════════════════════════════════════════
    # TEST 02 — Continue button visible
    # ══════════════════════════════════════════════

    @allure.story("02 - Continue Button Visible")
    def test_02_continue_button_visible(self):
        print("\n[TEST 02] Continue button is visible")
        self._ensure_on_page()

        visible = self.page.is_continue_visible()
        self._assert(
            visible,
            "Continue button visible",
            "Continue button not found"
        )

    @allure.story("03 - pre-approved limit visible")
    def test_03_pre_approved_limit_visible(self):
        print("\n[TEST 03] Pre-approved limit is visible")
        self._ensure_on_page()

        visible = self.page.pre_approved_limit_visible()
        self._assert(
            visible,
            "Pre-approved limit visible",
            "Pre-approved limit not found"
        )

    # ══════════════════════════════════════════════
    # TEST 04 — Privacy Policy link
    # ══════════════════════════════════════════════

    @allure.story("04 - Privacy Link")
    def test_04_privacy_link(self):
        print("\n[TEST 04] Privacy Policy link opens webview")
        self._ensure_on_page()

        self.page.click_privacy()
        time.sleep(3)
        opened = self.page.is_webview_opened()
        self._assert(
            opened,
            "Privacy webview opened",
            "Privacy link not working"
        )

        self.d.press("back")
        time.sleep(1)

    # ══════════════════════════════════════════════
    # TEST 05 — Terms & Conditions link
    # ══════════════════════════════════════════════

    @allure.story("05 - Terms Link")
    def test_05_terms_link(self):
        print("\n[TEST 05] Terms link opens webview")
        self._ensure_on_page()

        self.page.click_terms()
        time.sleep(3)

        opened = self.page.is_webview_opened()
        self._assert(
            opened,
            "Terms webview opened",
            "Terms link not working"
        )

        self.d.press("back")
        time.sleep(1)

    # ══════════════════════════════════════════════
    # TEST 06 — Secure chip modal
    # ══════════════════════════════════════════════

    @allure.story("06 - Secure Chip Modal")
    def test_06_secure_chip(self):
        print("\n[TEST 06] Secure chip opens modal")
        self._ensure_on_page()

        self.page.click_secure_chip()
        time.sleep(2)

        visible = self.page.is_secure_modal_visible()
        self._assert(
            visible,
            "Secure modal displayed",
            "Secure modal not shown"
        )

        self.d.press("back")

    # ══════════════════════════════════════════════
    # TEST 07 — Privacy chip modal
    # ══════════════════════════════════════════════

    @allure.story("07 - Privacy Chip Modal")
    def test_07_privacy_chip(self):
        print("\n[TEST 07] Privacy chip opens modal")
        self._ensure_on_page()

        self.page.click_privacy_chip()
        time.sleep(2)

        visible = self.page.is_privacy_modal_visible()
        self._assert(
            visible,
            "Privacy modal displayed",
            "Privacy modal not shown"
        )

        self.d.press("back")

    # ══════════════════════════════════════════════
    # TEST 08 — Confetti animation
    # ══════════════════════════════════════════════

    @allure.story("08 - Confetti Animation")
    def test_08_confetti(self):
        print("\n[TEST 08] Confetti animation visible")
        self._ensure_on_page()

        visible = self.page.is_confetti_visible()
        self._assert(
            visible,
            "Confetti animation visible",
            "Confetti animation not found"
        )


     # ══════════════════════════════════════════════
    # TEST 09 — DB Validations in pre-underwriting approved page
    # ══════════════════════════════════════════════

    @allure.story("09 - DB Validations in pre-underwriting approved page")
    def test_09_db_validations(self):
        print("\n[TEST 09] DB Validations in pre-underwriting approved page")
        from utils.queries import (
            get_uw_user_taran,
            get_sc_uw_user,
            get_state_audit,
            get_state,
            get_msi_success_status
        )
        user_id = self._data.get("user_id")
        result1 = get_uw_user_taran(self.db, user_id, 'PRE_UNDERWRITING')

        if result1:
            decision = result1[0].get("decision")
            stage = result1[0].get("stage")
        else:
            decision = None
            stage = None
        self._assert(
            decision == "SOFT_APPROVED" and stage == "FINISHED",
            f'SELECT * FROM "SC_UW_USER_TARAN" WHERE user_id={user_id} and decision={decision} and stage={stage} --> Passed',
            f'SELECT * FROM "SC_UW_USER_TARAN" WHERE user_id={user_id} and decision={decision} and stage={stage} --> Failed'
        )


        result2 = get_sc_uw_user(self.db, user_id)
        if result2:
            bank = result2[0].get("bank")
            status = result2[0].get("status")
        else:
            bank = None
            status = None
        self._assert(
            bank == "BMI" and status == "SOFT_APPROVED",
            f'SELECT * FROM "SC_UW_USER" WHERE user_id={user_id} and bank={bank} and status = {status} --> Passed',
            f'SELECT * FROM "SC_UW_USER" WHERE user_id={user_id} and bank={bank} and status = {status} --> Failed'
        )

        result3 = get_state(self.db, user_id)
        if result3:
            state = result3[0].get("state")
        else:
            state = None
        self._assert(
            state == "PRE_UW_APPROVED",
            f'SELECT * FROM "SC_STATE_MACHINE" WHERE user_id={user_id} and state={state} --> Passed',
            f'SELECT * FROM "SC_STATE_MACHINE" WHERE user_id={user_id} and state={state} --> Failed'
        )

        result4 = get_state_audit(self.db, user_id)
        if result4:
            previous_state = result4[0].get("previous_state")
            current_state = result4[0].get("current_state")
        else:
            previous_state = None
            current_state = None
        self._assert(
            previous_state == "PRE_UW_APPROVED" and current_state == "PRE_MANUAL_VERIFICATION",
            f'SELECT * FROM "SC_STATE_MACHINE_AUDIT" WHERE user_id={user_id} and previous_state={previous_state} and current_state={current_state} --> Passed',
            f'SELECT * FROM "SC_STATE_MACHINE_AUDIT" WHERE user_id={user_id} and previous_state={previous_state} and current_state={current_state} --> Failed'
        )





    # ══════════════════════════════════════════════
    # TEST 10 — Continue navigates to Email Page
    # ══════════════════════════════════════════════

    @allure.story("10 - Continue Navigation")
    def test_09_continue_navigates(self):
        print("\n[TEST 10] Clicking Continue navigates to next screen")
        self._ensure_on_page()

        self.page.click_continue()
        time.sleep(4)

        navigated = self.page.is_email_page_displayed()
        self._assert(
            navigated,
            "Navigated away after clicking Continue",
            "Still on same page after Continue"
        )


        from utils.queries import get_user_settings,get_state,get_state_audit
        user_id = self._data.get("user_id")
        result1 = get_user_settings(self.db, user_id)
        if result1:
            pre_uw_accepted = result1[0].get("pre_uw_accepted")
        else:
            pre_uw_accepted = None
        self._assert(
            pre_uw_accepted,
            "Pre UW accepted",
            "Pre UW not accepted"
        )

        result2 = get_state(self.db, user_id)
        if result2:
            state = result2[0].get("state")
        else:
            state = None
        self._assert(
            state == "EMAIL",
            f'SELECT * FROM "SC_STATE_MACHINE" WHERE user_id={user_id} and state={state} --> Passed',
            f'SELECT * FROM "SC_STATE_MACHINE" WHERE user_id={user_id} and state={state} --> Failed'
        )

        result3 = get_state_audit(self.db, user_id)
        if result3:
            previous_state = result3[0].get("previous_state")
            current_state = result3[0].get("current_state")
        else:
            previous_state = None
            current_state = None
        self._assert(
            previous_state == "PRE_UW_APPROVED" and current_state == "EMAIL",
            f'SELECT * FROM "SC_STATE_MACHINE_AUDIT" WHERE user_id={user_id} and previous_state={previous_state} and current_state={current_state} --> Passed',
            f'SELECT * FROM "SC_STATE_MACHINE_AUDIT" WHERE user_id={user_id} and previous_state={previous_state} and current_state={current_state} --> Failed'
        )



# ───────────────────────────────────────────────
# ORDER
# ───────────────────────────────────────────────

TEST_ORDER = [
    "test_01_page_loads",
    "test_02_continue_button_visible",
    "test_03_pre_approved_limit_visible",
    "test_04_privacy_link",
    "test_05_terms_link",
    "test_06_secure_chip",
    "test_07_privacy_chip",
    "test_08_confetti",
    "test_09_db_validations",
    "test_10_continue_navigates"
]


if __name__ == "__main__":
    t = TestPreApprovedLimit()
    TestPreApprovedLimit.setup_class()

    for method in TEST_ORDER:
        getattr(t, method)()

    print("\n✅ Pre-approved limit tests completed")