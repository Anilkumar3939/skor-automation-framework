import time
from pages.base_page import BasePage


class JobDetailsPage(BasePage):

    def __init__(self, driver):
        self.d = driver

    # ---------- SCREEN CHECK ----------
    def is_visible(self, timeout=5):

        texts = [
            "Job Information",
            "job information",
            "Job",
            "Employment",
            "Work Information"
        ]

        for txt in texts:

            print(f"Checking: {txt}")

            if self.d(descriptionContains=txt).exists(timeout=1):
                print(f"Found text: {txt}")
                return True

            if self.d(descriptionContains=txt).exists(timeout=1):
                print(f"Found desc: {txt}")
                return True

        print("Job screen not detected")

        return False

    # ---------- STEP 1 ----------
    def select_job_status(self, value="Professional"):
        self.d(descriptionContains=value).click()

    def select_work_field(self, value="Trading"):
        self.d(descriptionContains=value).click()

    def select_job_title(self, value="Director/Vice President"):
        self.d(descriptionContains=value).click()

    def select_employment_length(self, value="2-5 Year"):
        self.d(descriptionContains=value).click()

    def click_continue(self):
        self.d(descriptionContains="Continue application").click()
    

    # ---------- STEP 2 ----------
    def select_education(self, value="High School"):
        self.d(descriptionContains=value).click()

    def enter_company_name(self, name="skor"):
        self.d(className="android.widget.EditText")[0].set_text(name)

    def enter_department(self, dept="product"):
        self.d(className="android.widget.EditText")[1].set_text(dept)

    def enter_phone(self, phone="843485454"):
        self.d(className="android.widget.EditText")[2].set_text(phone)

    def select_building_type(self):
        self.d(textContains="Standalone").click()

    # ---------- STEP 3 ----------
    def enter_street(self, value="MG Road"):
        self.d(descriptionContains="Street name").click()
        self.d(className="android.widget.EditText").set_text(value)

    def enter_building_number(self, value="123"):
        self.d(descriptionContains="Building No.").click()
        self.d(className="android.widget.EditText").set_text(value)

    def enter_rt(self, value="01"):
        self.d(descriptionContains="RT").click()
        self.d(className="android.widget.EditText").set_text(value)

    def enter_rw(self, value="02"):
        self.d(descriptionContains="RW").click()
        self.d(className="android.widget.EditText").set_text(value)

    def select_province(self):
        self.d(descriptionContains="Province").click()
        self.d(className="android.widget.TextView")[0].click()

    def select_city(self):
        self.d(descriptionContains="City").click()
        self.d(className="android.widget.TextView")[0].click()

    def select_district(self):
        self.d(descriptionContains="District").click()
        self.d(className="android.widget.TextView")[0].click()

    def select_sub_district(self):
        self.d(descriptionContains="Sub-district").click()
        self.d(className="android.widget.TextView")[0].click()

    # ---------- COMPLETE FLOW ----------
    def fill_job_details(self):
        # Step 1
        self.select_job_status()
        self.select_work_field()
        self.select_job_title()
        self.select_employment_length()
        self.click_continue()

        time.sleep(2)

        # Step 2
        self.select_education()
        self.enter_company_name()
        self.enter_department()
        self.enter_phone()
        self.select_building_type()
        self.click_continue()

        time.sleep(2)

        # Step 3
        self.enter_street()
        self.enter_building_number()
        self.enter_rt()
        self.enter_rw()
        self.select_province()
        self.select_city()
        self.select_district()
        self.select_sub_district()
        self.click_continue()