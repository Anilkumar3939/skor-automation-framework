from logging import Logger

import allure

from pages.delivery_page import DeliveryPage
from base import APP_PACKAGE, BaseTest

class TestDeliveryPage(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.delivery_page = DeliveryPage(cls.d)
        cls.logger = Logger(TestDeliveryPage)

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

    # @allure.story("Delivery Page Load")
    # def test_delivery_page_loads(self):
    #     print("\n[TEST] Delivery page loads correctly")

    #     visible = self.delivery_page.is_visible_start()

    #     assert visible, "Delivery page not visible"

    #     print("✅ PASS: Delivery page is visible")

    # @allure.story("Switch Home To Workplace")
    # def test_switch_home_to_workplace(self):

    #     print("\n[TEST] Switch Home To Workplace")

    #     self.delivery_page.select_delivery_option("Home")

    #     assert self.delivery_page.home_delivery_elements_visible(), \
    #         "Home section not visible"

    #     self.delivery_page.select_delivery_option("Workplace")

    #     assert self.delivery_page.workplace_delivery_elements_visible(), \
    #         "Workplace section not visible"

    #     print("✅ PASS: Switched Home → Workplace")

    # @allure.story("Switch Workplace To Home")
    # def test_switch_workplace_to_home(self):

    #     print("\n[TEST] Switch Workplace To Home")

    #     self.delivery_page.select_delivery_option("Workplace")

    #     assert self.delivery_page.workplace_delivery_elements_visible(), \
    #         "Workplace section not visible"

    #     self.delivery_page.select_delivery_option("Home")

    #     assert self.delivery_page.home_delivery_elements_visible(), \
    #         "Home section not visible"

    #     print("✅ PASS: Switched Workplace → Home")

    # @allure.story("Continue Without Address")
    # def test_continue_without_address(self):

    #     print("\n[TEST] Continue Without Address")

    #     self.delivery_page.select_delivery_option("Home")

    #     self.delivery_page.click_continue()

    #     still_on_page = self.delivery_page.is_visible()

    #     assert still_on_page, \
    #         "User navigated without entering address"

    #     print("✅ PASS: User cannot continue without address")

    # @allure.story("Address Maximum Length")
    # def test_address_max_length(self):

    #     print("\n[TEST] Address Maximum Length")

    #     long_address = "A" * 120

    #     locations = [
    #         "DKI Jakarta",
    #         "Jakarta Selatan",
    #         "Kebayoran Baru",
    #         "Senayan"
    #     ]

    #     self.delivery_page.select_delivery_option("Home")

    #     self.delivery_page.fill_home_address(
    #         "Apartment",
    #         long_address,
    #         locations
    #     )

    #     print("✅ PASS: Maximum length address entered")

    # @allure.story("Special Characters In Address")
    # def test_special_characters_in_address(self):

    #     print("\n[TEST] Special Characters In Address")

    #     special_address = "Jl.@#$%^&*()_+ Block-A/12"

    #     locations = [
    #         "DKI Jakarta",
    #         "Jakarta Selatan",
    #         "Kebayoran Baru",
    #         "Senayan"
    #     ]

    #     self.delivery_page.select_delivery_option("Home")

    #     self.delivery_page.fill_home_address(
    #         "Apartment",
    #         special_address,
    #         locations
    #     )

    #     print("✅ PASS: Special characters accepted")

    # @allure.story("Home Delivery Flow")
    # def test_home_delivery_flow(self):

    #     print("\n[TEST] Home Delivery Flow")

    #     locations = [
    #         "DKI Jakarta",
    #         "Jakarta Selatan",
    #         "Kebayoran Baru",
    #         "Senayan"
    #     ]

    #     self.delivery_page.select_delivery_option("Home")

    #     visible = self.delivery_page.home_delivery_elements_visible()

    #     assert visible, "Home address form not displayed"

    #     self.delivery_page.fill_home_address(
    #         "Apartment",
    #         "Jl Test Home Address",
    #         locations
    #     )

    #     self.delivery_page.click_continue()

    #     assert self.delivery_page.is_input_remaining_address_page_visible(), \
    #         "Remaining address page not displayed"

    #     print("✅ PASS: Home delivery flow")



    @allure.story("Remaining Address Page Load")
    def test_remaining_address_page_load(self):

        print("\n[TEST] Remaining Address Page Load")

        visible = self.delivery_page.is_input_remaining_address_page_visible()

        assert visible, "Remaining address page not visible"

        print("✅ PASS: Remaining address page visible")




    @allure.story("Submit Without Other Address")
    def test_submit_without_other_address(self):

        print("\n[TEST] Submit Without Other Address")

        self.delivery_page.click_submit()

        success = self.delivery_page.is_submission_success_page_visible()

        assert not success, \
            "Submission succeeded with empty address"

        print("✅ PASS: Empty other address blocked")





    @allure.story("Fill Other Address")
    def test_fill_other_address(self):

        print("\n[TEST] Fill Other Address")

        locations = [
            "DKI Jakarta",
            "Jakarta Selatan",
            "Kebayoran Baru",
            "Senayan"
        ]

        self.delivery_page.fill_other_address(
            "Jl Kemang Timur No.18",
            locations
        )

        print("✅ PASS: Other address entered")





    @allure.story("Submit Button Enabled After Mandatory Fields")
    def test_submit_button_enabled_after_mandatory_fields(self):

        print("\n[TEST] Submit Button Enabled")
        submit_btn = self.delivery_page.driver(
            descriptionContains="Submit"
        )

        assert submit_btn.exists(timeout=5), \
            "Submit button not visible"

        print("✅ PASS: Submit available after mandatory fields")

    @allure.story("Submit Remaining Address")
    def test_submit_other_address(self):

        print("\n[TEST] Submit Other Address")

        self.delivery_page.click_submit()

        print("✅ PASS: Submit clicked")

    @allure.story("Delivery Address Submitted")
    def test_delivery_address_submission_success(self):

        print("\n[TEST] Verify Submission Success")

        success = (
            self.delivery_page.is_submission_success_page_visible()
        )

        assert success, "Submission success page not visible"

        print("✅ PASS: Delivery address submitted")

    # @allure.story("Complete Delivery Flow")
    # def test_complete_delivery_flow(self):

    #     print("\n[TEST] Complete Delivery Flow")

    #     locations = [
    #         "DKI Jakarta",
    #         "Jakarta Selatan",
    #         "Kebayoran Baru",
    #         "Senayan"
    #     ]

    #     self.delivery_page.select_delivery_option("Home")

    #     self.delivery_page.fill_home_address(
    #         "Apartment",
    #         "Jl Test Home Address",
    #         locations
    #     )

    #     self.delivery_page.click_continue()

    #     assert self.delivery_page.is_input_remaining_address_page_visible(), \
    #         "Remaining address page not displayed"

    #     self.delivery_page.fill_other_address(
    #         "Jl Kemang Timur No.18",
    #         locations
    #     )

    #     self.delivery_page.click_submit()

    #     assert self.delivery_page.is_submission_success_page_visible(), \
    #         "Submission failed"

    #     print("✅ PASS: End-to-End Delivery Flow Successful")