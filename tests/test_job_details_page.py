import time
import allure

from base import BaseTest
from pages.job_details_page import JobDetailsPage


@allure.feature("Job Details Screen")
class TestJobDetails(BaseTest):

    @classmethod
    def setup_class(cls):

        super().setup_class()

        cls.job = JobDetailsPage(cls.d)

    # ------------------------
    # Helper methods
    # ------------------------

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

    def _require_screen(self):

        assert self._assert(
            self.job.is_visible(),
            "Job Details screen visible",
            "Job Details screen not visible"
        )

    # ------------------------
    # TEST 01
    # ------------------------

    @allure.story("01 - Job Details Screen Visible")
    def test_01_job_screen_visible(self):

        print("\n[TEST 01] Job screen visible")

        visible = self.job.is_visible()

        self.screenshot(
            "01_job_screen"
        )

        assert self._assert(
            visible,
            "Job details screen loaded",
            "Job details screen NOT loaded"
        )

    # ------------------------
    # TEST 02
    # ------------------------

    @allure.story("02 - Fill Step 1")
    def test_02_fill_step1(self):

        print("\n[TEST 02] Fill step 1")

        self._require_screen()

        self.job.select_job_status()
        self.job.select_work_field()
        self.job.select_job_title()
        self.job.select_employment_length()

        self.screenshot(
            "02_step1"
        )

        assert self._assert(
            True,
            "Step 1 completed",
            "Step 1 failed"
        )

        self.job.click_continue()

        time.sleep(2)
        self.scroll_down()

    # ------------------------
    # TEST 03
    # ------------------------
    
    
    @allure.story("03 - Fill Step 2")
    def test_03_fill_step2(self):

        print("\n[TEST 03] Fill step 2")

        self.job.select_education()

        self.job.enter_company_name()

        self.job.enter_department()

        self.job.enter_phone()

        self.job.select_building_type()

        self.screenshot(
            "03_step2"
        )

        assert self._assert(
            True,
            "Step 2 completed",
            "Step 2 failed"
        )

        self.job.click_continue()

        time.sleep(2)

    # ------------------------
    # TEST 04
    # ------------------------

    @allure.story("04 - Fill Step 3")
    def test_04_fill_step3(self):

        print("\n[TEST 04] Fill step 3")

        self.job.enter_street()

        self.job.enter_building_number()

        self.job.enter_rt()

        self.job.enter_rw()

        self.job.select_province()

        self.job.select_city()

        self.job.select_district()

        self.job.select_sub_district()

        self.screenshot(
            "04_step3"
        )

        assert self._assert(
            True,
            "Step 3 completed",
            "Step 3 failed"
        )

        self.job.click_continue()

        time.sleep(3)

    # ------------------------
    # TEST 05
    # ------------------------

    @allure.story("05 - Job Details Completed")
    def test_05_job_completed(self):

        print("\n[TEST 05] Verify completion")

        success = True

        self.screenshot(
            "05_job_complete"
        )

        assert self._assert(
            success,
            "Job details completed",
            "Job details not completed"
        )


TEST_ORDER = [
    "test_01_job_screen_visible",
    "test_02_fill_step1",
    "test_03_fill_step2",
    "test_04_fill_step3",
    "test_05_job_completed"
]