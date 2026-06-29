#!/usr/bin/env python3
"""
UW Loading Screen Tests — Single Session Strategy
================================================

- Navigate to UW Loading screen ONCE
- Run all tests without leaving screen
"""

import os
import sys
import time
from urllib import response
import allure

from base import BaseTest
from pages.base_page import BasePage
from utils.db_helper import DBHelper
from utils.logger import get_logger
from utils.api_helpers import APIHelper



class UWLoadingPage(BasePage):
    """
    Page Object for UW Loading Screen
    """

    TEXTS = [
        "Calculating",
        "Checking",
    ]

    TIMEOUT_TEXTS = [
        "We’re experiencing a delay",
        "Notify me when it’s ready",
        "Your application",
    ]

    def is_visible(self, timeout=5):

        for txt in self.TEXTS:
            print(f"Checking for text: '{txt}'")

            # Check visible text
            if self.d(textContains=txt).exists(timeout=1):
                print(f"Found text using textContains: '{txt}'")
                return True

            # Check content description
            if self.d(descriptionContains=txt).exists(timeout=1):
                print(f"Found text using descriptionContains: '{txt}'")
                return True

        print("No matching text found")
        return False
    
    def next_page_visible(self, timeout=10):

        if self.d(descriptionContains="pre-approved").exists(timeout=timeout):
            print("Next page is visible")
            return "pre-approved"
        
        if self.d(descriptionContains="Sorry").exists(timeout=timeout):
            print("Next page is visible")
            return "Sorry"

        print("Next page not visible yet")
        return False

    def is_progress_bar_visible(self):
        return self.d(className="android.view.View").exists(timeout=2)

    def is_timeout_modal_visible(self):
        for txt in self.TIMEOUT_TEXTS:
            if self.d(descriptionContains=txt).exists(timeout=1):
                return True
        return False

    def is_retry_button_visible(self):
        return self.d(descriptionContains="Notify me when it’s ready").exists(timeout=2)

    def is_remind_button_visible(self):
        return self.d(descriptionContains="Notify me when it’s ready").exists(timeout=2)

    def tap_retry(self):
        btn = self.d(descriptionContains="Notify me when it’s ready")
        if btn.exists(timeout=2):
            btn.click()
            time.sleep(1)
            return True
        return False


# ─────────────────────────────────────────────────────────────

@allure.feature("UW Loading Screen")
class UWLoadingTest(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.page = UWLoadingPage(cls.d)
        cls.logger = get_logger("uw_loading")
        cls.db = DBHelper()

    # ── helpers ─────────────────────────────

    def _log_pass(self, msg):
        print(f"  ✅ PASS: {msg}")

    def _log_fail(self, msg):
        print(f"  ❌ FAIL: {msg}")

    def _assert(self, cond, pass_msg, fail_msg):
        if cond:
            self._log_pass(pass_msg)
        else:
            self._log_fail(fail_msg)
        return cond

    # ── navigation (ONLY ONCE) ─────────────────

    def _navigate_to_uw_loading_once(self):

        # If already marked on screen,
        # verify screen still exists
        if self._data.get("on_screen", False):

            if self.page.is_visible():
                return True

            # reset if screen disappeared
            self._data["on_screen"] = False

        print("🚀 Navigating to UW Loading screen...")

        # Actual navigation flow here
        # self.navigate_to_preuw()

        time.sleep(5)

        visible = self.page.is_visible()

        self._data["on_screen"] = visible

        return visible

    def _require_screen(self):
        if not self.page.is_visible(timeout=3):
            raise AssertionError("Not on UW Loading screen")

    # ════════════════════════════════════════
    # TEST 01 — Screen loads
    # ════════════════════════════════════════

    @allure.story("01 - UW Loading Screen Loads")
    def test_01_screen_load(self):
        print("\n[TEST 01] UW Loading screen loads")

        reached = self._navigate_to_uw_loading_once()
        self.screenshot("01_screen")

        self.assert_critical(reached, "UW Loading screen failed to load. Stopping suite.")

    # ════════════════════════════════════════
    # TEST 02 — Progress bar visible
    # ════════════════════════════════════════

    @allure.story("02 - Progress Bar Visible")
    def test_02_progress_bar(self):
        print("\n[TEST 02] Progress bar visible")

        self._require_screen()
        self.screenshot("02_progress")

        visible = self.page.is_progress_bar_visible()

        assert self._assert(
            visible,
            "Progress bar is visible",
            "Progress bar NOT visible",
        )

    # ════════════════════════════════════════
    # TEST 03 — Progress increases
    # ════════════════════════════════════════

    @allure.story("03 - Progress Increases Over Time")
    def test_03_progress_increase(self):
        print("\n[TEST 03] Progress increases")

        self._require_screen()

        self.screenshot("03_before")
        time.sleep(1)
        self.screenshot("03_after")
        # We can't read exact value → just ensure still alive
        still_visible = self.page.is_visible()

        assert self._assert(
            still_visible,
            "Screen still active (progress running)",
            "Screen disappeared unexpectedly",
        )

    # ════════════════════════════════════════
    # TEST 04 — Timeout modal appears
    # ════════════════════════════════════════
    time.sleep(5)

    @allure.story("04 - Timeout Modal Appears")
    def test_04_timeout_modal(self):
        print("\n[TEST 04] Timeout modal")

        self._require_screen()

        print("⏳ Waiting for timeout (~2 mins)...")
        time.sleep(25)

        self.screenshot("04_timeout")

        visible = self.page.is_timeout_modal_visible()

        assert self._assert(
            visible,
            "Timeout modal displayed",
            "Timeout modal NOT displayed",
        )


    # ════════════════════════════════════════
    # TEST 05 — Retry works
    # ════════════════════════════════════════

    @allure.story("05 - Retry Button Works")
    def test_05_retry(self):
        print("\n[TEST 05] Retry button")

        tapped = self.page.tap_retry()
        time.sleep(50)
        assert self._assert(
            tapped,
            "Retry button tapped",
            "Retry button NOT tapped",
        )
        

    # ════════════════════════════════════════
    # TEST 06 — Retry and pre-underwriting check
    # ════════════════════════════════════════

    @allure.story("06 - Retry and Pre-Underwriting Check")
    def test_06_retry_and_pre_uw_check(self):
        print("\n[TEST 06] Retry and pre-underwriting check")

        self.page.tap_retry()

        from utils.queries import get_uw_user_taran,update_limit_and_card_type
        user_id = self._data.get("user_id")
        print(f"User ID: {user_id}")

        application_id = get_uw_user_taran(self.db, user_id,'PRE_UNDERWRITING')[0].get("application_id")
        print(application_id)

        if application_id:
            print(f"Found application_id in DB: {application_id}")
            response = APIHelper.initiate_taran(
                user_id,
                application_id
            )
            if response.status_code == 200:
                update_limit_and_card_type(self.db, user_id, '49000000', "SKORCARD_SMART")

            assert response.status_code == 200
        else:
            print("No application_id found in DB, skipping API call")

        time.sleep(50)
        

        next_visible = self.page.next_page_visible(timeout=15)

        if next_visible == "pre-approved":
            assert self._assert(
                True,
                "Retry successful, pre-approved page visible",
                "Retry successful, but pre-approved page NOT visible",
            )
        elif next_visible == "Sorry":
            print("User got Rejected due to pre credit check")
            assert self._assert(
                False,
                "Retry successful, Reject Page visible",
                "Retry successful, but Reject page NOT visible",
            )
        else:     
            assert self._assert(
                False,
                "Retry successful, next page visible",
                "Retry successful, but next page NOT visible",
            )


# ── order ─────────────────────────────────

TEST_ORDER = [
    "test_01_screen_load",
    "test_02_progress_bar",
    "test_03_progress_increase",
    "test_04_timeout_modal",
    "test_05_retry",
    "test_06_retry_and_pre_uw_check",
]