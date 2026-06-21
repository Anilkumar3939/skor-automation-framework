#!/usr/bin/env python3
"""
Extended Onboarding Flow Tests — Functional Suite.

Covers the following pages requested by the user:
1. Pre-UW loading page
2. Pre-approved page
3. Email page
4. Office address and job details page
5. KTP page
6. Home address page
7. Liveness page
8. Delivery page
9. Manual verification + gatekeeper page
10. Gatekeeper Address page
11. Emergency Contact (Additional)
"""
import os
import sys
import time
import allure

from utils.db_helper import DBHelper
from pages.registartion_login import RegistrationLogin
from pages.otp_page import OTPPage

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in [_ROOT, os.path.join(_ROOT, "tests")]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from base import APP_PACKAGE, BaseTest
from utils.logger import get_logger
from pages.onboarding_flow_pages import (
    PreUWLoadingPage, PreApprovedPage, EmailPage, JobInformationPage,
    CompanyDetailsPage, CompanyAddressDetailsPage,
    KtpPage, HomeAddressPage, LivenessPage,
    ManualVerificationPage, GatekeeperAddressPage, ReferenceContactsPage, BypassKTPAndLivenessPage
)

@allure.feature("Extended Onboarding Flow")
class TestExtendedOnboarding(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.logger = get_logger("extended_onboarding")
        cls.registration = RegistrationLogin(cls.d)
        cls.otp_page = OTPPage(cls.d)
        cls.pre_uw = PreUWLoadingPage(cls.d)
        cls.pre_approved = PreApprovedPage(cls.d)
        cls.email = EmailPage(cls.d)
        cls.job_info = JobInformationPage(cls.d)
        cls.company_details = CompanyDetailsPage(cls.d)
        cls.company_address = CompanyAddressDetailsPage(cls.d)
        cls.ktp = KtpPage(cls.d)
        cls.home_addr = HomeAddressPage(cls.d)
        cls.liveness = LivenessPage(cls.d)
        cls.manual_verif = ManualVerificationPage(cls.d)
        cls.gatekeeper_addr = GatekeeperAddressPage(cls.d)
        cls.reference_contacts = ReferenceContactsPage(cls.d)
        cls.bypass_ktp_and_liveness = BypassKTPAndLivenessPage(cls.d)
        cls.db = DBHelper()
    

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
            raise AssertionError(fail_msg)

        return condition


    # @allure.story("01a - Job Information Page")
    # def test_01a_job_information_page(self):
    #     print("\n[TEST 01a] Job Information functionality")

    #     assert self.job_info.is_visible(timeout=5), \
    #         "❌ Job Information page NOT visible"

    #     self.screenshot("01a1_job_info_page")

    #     print("  ℹ️  Filling job information with test data...")
    #     self.job_info.fill_job_information()

    #     print("  ℹ️  Job information filled.")
    #     self.screenshot("01a2_job_info_filled")
    #     time.sleep(3)
    #     self._assert(True, "Job information filled successfully", "Failed to fill job information")     

    # @allure.story("01b - Company Details Page")
    # def test_01b_company_details_page(self):
    #     print("\n[TEST 01b] Company Details functionality")

    #     assert self.company_details.is_visible(timeout=5), \
    #         "❌ Company Details page NOT visible"

    #     self.screenshot("01b1_company_details_page")

    #     self.company_details.fill_company_details()

    #     self.screenshot("01b2_company_details_filled")
    #     time.sleep(3)
    #     clicked = self.company_address.click_continue()
    #     assert clicked, "❌ Could not submit company address details"

    # @allure.story("02 - Reference Contacts Page")
    # def test_02_reference_contacts(self):
    #     print("\n[TEST 02] Reference Contacts functionality")
    #     if not self.reference_contacts.is_visible(timeout=3):
    #         print("  ℹ️  SKIP: Reference Contacts page not visible.")
    #         return

    #     self.screenshot("02a_reference_contacts")
    #     self.reference_contacts.fill_details()
    #     self.reference_contacts.fill_relationship()
    #     self.screenshot("02b_reference_contacts_filled")
    #     user_id = 'SC062026000099'
    #     clicked = self.reference_contacts.click_continue()
    #     self._assert(clicked, "Submitted Reference Contacts", "Could not submit Reference Contacts")

    @allure.story("03 - BYPASS KTP and Liveness")
    def test_03_bypass_ktp_and_liveness(self):
        print("\n[TEST 03] BYPASS KTP and Liveness functionality")
        self.d.app_stop(APP_PACKAGE)
        bypassed = self.bypass_ktp_and_liveness.bypass_ktp_and_liveness_state()
        time.sleep(10)
        self.d.app_start(APP_PACKAGE)
        time.sleep(10)
        self._assert(bypassed, "Bypassed KTP and Liveness", "Failed to bypass KTP and Liveness")
        reached_checkpoints = self.bypass_ktp_and_liveness.navigated_to_checkpoints()
        self._assert(reached_checkpoints, "Navigated to checkpoints", "Failed to navigate to checkpoints")
        clicked = self.bypass_ktp_and_liveness.click_continue()
        self._assert(clicked, "Clicked continue", "Failed to click continue")
        reached_delivery = self.bypass_ktp_and_liveness.reached_delivery_page()
        self._assert(reached_delivery, "Reached delivery page", "Failed to reach delivery page")







    # @allure.story("03 - KTP Capture Page")
    # def test_03_ktp_page(self):
    #     print("\n[TEST 03] KTP page functionality")

    #     if not self.ktp.is_visible(timeout=3):
    #         self._assert(False, "", "KTP page not visible")
    #         return

    #     self.screenshot("03_ktp_page")

    #     self.ktp.click_camera()

    #     if self.ktp.is_camera_opened():
    #         self.ktp.capture_photo()
    #         self.screenshot("03_ktp_captured")
    #         self._assert(True, "Camera interaction successful", "")
    #     else:
    #         self._assert(
    #             False,
    #             "",
    #             "Camera screen did not open"
    #         )
    #         return
        
    #     self.ktp.fill_mothers_maiden_name()
    #     self.ktp.click_continue()
    #     user_id = self._data.get("user_id")
    #     self.ktp.bypass_ktp_state(user_id=user_id)


    #     self._assert(
    #         True,
    #         "KTP capture interaction completed",
    #         "KTP capture failed"
    #     )



    # @allure.story("08 - Delivery Address Page")
    # def test_08_delivery_page(self):
    #     print("\n[TEST 08] Card delivery address functionality")
    #     if not self.delivery.is_visible(timeout=3):
    #         print("  ℹ️  SKIP: Delivery page not visible.")
    #         return

    #     self.screenshot("08a_delivery_page")
    #     self.delivery.select_address()
    #     self.screenshot("08b_delivery_selected")
    #     clicked = self.delivery.click_confirm()
    #     self._assert(clicked, "Confirmed delivery address", "Could not confirm delivery address")

    # @allure.story("09 - Manual Verification / Gatekeeper Page")
    # def test_09_manual_verification(self):
    #     print("\n[TEST 09] Manual Verification / Gatekeeper functionality")
    #     if not self.manual_verif.is_visible(timeout=3):
    #         print("  ℹ️  SKIP: Manual Verification page not visible.")
    #         return

    #     self.screenshot("09_manual_verification")
    #     clicked = self.manual_verif.click_continue()
    #     self._assert(clicked, "Acknowledged manual verification", "Could not interact with manual verification")

    # @allure.story("10 - Gatekeeper Address Page")
    # def test_10_gatekeeper_address(self):
    #     print("\n[TEST 10] Gatekeeper Address functionality")
    #     if not self.gatekeeper_addr.is_visible(timeout=3):
    #         print("  ℹ️  SKIP: Gatekeeper Address page not visible.")
    #         return

    #     self.screenshot("10a_gatekeeper_address")
    #     self.gatekeeper_addr.fill_address()
    #     self.screenshot("10b_gatekeeper_address_filled")
    #     clicked = self.gatekeeper_addr.click_submit()
    #     self._assert(clicked, "Submitted Gatekeeper Address", "Could not submit Gatekeeper Address")




TEST_ORDER = [
    "test_01_pre_uw_loading",
    "test_02_pre_approved",
    "test_03_email_page",
    "test_04a_job_information_page",
    "test_04b_company_details_page",
    "test_04c_company_address_details_page",
    "test_05_ktp_page",
    "test_06_home_address",
    "test_07_liveness_page",
    "test_08_delivery_page",
    "test_09_manual_verification",
    "test_10_gatekeeper_address",
    "test_11_reference_contacts"
]

if __name__ == "__main__":
    t = TestExtendedOnboarding()
    TestExtendedOnboarding.setup_class()
    for method in TEST_ORDER:
        getattr(t, method)()
    print("\n✅ Extended onboarding functional tests done.")
