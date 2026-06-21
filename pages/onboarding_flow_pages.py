#!/usr/bin/env python3
"""
Page Objects for the extended Onboarding Flow pages.
Includes: Pre-UW Loading, Pre-Approved, Email, Office/Job, KTP, Home Address,
Liveness, Delivery, Manual Verification/Gatekeeper, Gatekeeper Address.
"""
import os
import time
from pages.base_page import BasePage
from tests.base import APP_PACKAGE
from tests.test_registration_login import VALID_PHONE
from pages.otp_page import OTPPage
from pages.registartion_login import RegistrationLogin
from utils.db_helper import DBHelper
from utils.queries import insert_sc_user_ktp_address,update_kyc_details,update_document_status,insert_kyc_facematch_trans

class PreUWLoadingPage(BasePage):
    def is_visible(self, timeout=10):
        # Using common text that might appear on loading screens
        return (
            self.d(textContains="loading").exists(timeout=timeout) or
            self.d(textContains="Loading").exists(timeout=timeout) or
            self.d(textContains="analyzing").exists(timeout=timeout) or
            self.d(textContains="Please wait").exists(timeout=timeout) or
            self.d(textContains="Tunggu").exists(timeout=timeout)
        )
    
    def wait_until_disappears(self, timeout=30):
        return self.d(textContains="loading").wait_gone(timeout=timeout)

class PreApprovedPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Pre-approved").exists(timeout=timeout) or
            self.d(textContains="approved").exists(timeout=timeout) or
            self.d(textContains="Selamat").exists(timeout=timeout) or
            self.d(descriptionContains="approved").exists(timeout=timeout)
        )

    def click_continue(self):
        for txt in ["Continue", "Lanjut", "Next", "Selanjutnya"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class EmailPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Email").exists(timeout=timeout) or
            self.d(descriptionContains="Email").exists(timeout=timeout)
        )

    def enter_email(self, email):
        el = self.d(className="android.widget.EditText")
        if el.exists(timeout=3):
            el.set_text(email)
            time.sleep(0.5)
            return True
        return False

    def click_submit(self):
        for txt in ["Verify", "Submit", "Continue", "Lanjut", "Verifikasi"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class JobInformationPage(BasePage):
    def is_visible(self, timeout=5):
        print("  👉 Checking if Job Information page is visible...")
        return self.d(description="Let’s fill your job information").exists(timeout=timeout)

    def fill_job_information(self):
        print("  👉 Filling job information with test data...")
        job_types = ["Professional", "Private employees", "Entrepreneur", "Civil employees"]
        for jt in job_types:
            if self.d(description=jt).exists(timeout=1):
                self.d(description=jt).click()
                break
        time.sleep(0.5)
        
        fields = ["Trading", "Tech/IT", "Financial/Banking", "Services"]
        for f in fields:
            if self.d(description=f).exists(timeout=1):
                self.d(description=f).click()
                break
        time.sleep(0.5)
        
        titles = ["Director/Vice President", "Manager", "Staff", "Owner"]
        for t in titles:
            if self.d(description=t).exists(timeout=1):
                self.d(description=t).click()
                break
        time.sleep(0.5)
        
        lengths = ["2-5 Year", "<2 Year", "6-8 Year", "9-10 Year", ">10 Year"]
        for l in lengths:
            if self.d(description=l).exists(timeout=1):
                self.d(description=l).click()
                break
        time.sleep(1)

        self.scroll_down()

        higher_education = ["Junior School", "High School", "Diploma", "Bachelor", "Master", "Doctoral"]
        for he in higher_education:
            if self.d(description=he).exists(timeout=1):
                self.d(description=he).click()
                break
        time.sleep(0.5)
        self.scroll_down()

    # def click_continue(self):
    #     for txt in ["Continue application", "Continue", "Lanjut", "Next", "Selanjutnya"]:
    #         el = self.d(textContains=txt)
    #         if el.exists(timeout=1):
    #             el.click()
    #             time.sleep(1)
    #             return True
    #     return False

class CompanyDetailsPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(description="Company details").exists(timeout=timeout)

    def fill_company_details(
            self,
            company_name="skor",
            department="product",
            phone="8434854"
    ):

        time.sleep(2)

        fields = self.d(className="android.widget.EditText")

        count = fields.count
        print(f"👉 Found {count} input fields")

        if count >= 1:
            print("Entering company name")
            fields[0].click()
            time.sleep(.5)
            fields[0].clear_text()
            fields[0].set_text(company_name)

        if count >= 2:
            print("Entering department")
            fields[1].click()
            time.sleep(.5)
            fields[1].clear_text()
            fields[1].set_text(department)

        if count >= 3:

            print("Entering phone")

            self.scroll_down()
            time.sleep(1)

            fields = self.d(className="android.widget.EditText")

            fields[2].click()
            time.sleep(.5)

            fields[2].clear_text()
            fields[2].set_text(phone)

            time.sleep(1)

            # click outside to remove focus
            clickSomeWhere = self.d.xpath(
                '//android.view.View[@content-desc=">10 Year"]'
            )

            if clickSomeWhere.exists:
                clickSomeWhere.click()

        time.sleep(2)

        self.scroll_down()

        if self.d(description="Standalone building").exists(timeout=2):
            self.d(description="Standalone building").click()

        elif self.d(description="Office tower").exists(timeout=2):
            self.d(description="Office tower").click()

        time.sleep(1)
    # def click_continue(self):
    #     for txt in ["Continue application", "Continue", "Lanjut", "Next", "Selanjutnya"]:
    #         el = self.d(textContains=txt)
    #         if el.exists(timeout=1):
    #             el.click()
    #             time.sleep(1)
    #             return True
    #     return False

class CompanyAddressDetailsPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(description="Address details").exists(timeout=timeout)

    def fill_address_details(self, street="Jl. Test", block="Blok A", building="12", rt="01", rw="02"):
        # Scroll to make sure fields are visible
        self.d(scrollable=True).scroll.toEnd()

        fields = [
            '//android.widget.ScrollView/android.view.View[8]/android.view.View[2]/android.widget.EditText',
            '//android.widget.ScrollView/android.view.View[8]/android.view.View[3]/android.widget.EditText',
            '//android.widget.ScrollView/android.view.View[8]/android.view.View[4]/android.widget.EditText',
            '//android.widget.ScrollView/android.view.View[8]/android.view.View[5]/android.widget.EditText',
            '//android.widget.ScrollView/android.view.View[8]/android.view.View[6]/android.widget.EditText',
        ]

        values = [street, block, building, rt, rw]

        for i in range(len(fields)):
            el = self.d.xpath(fields[i])
            if el.exists:
                el.click()
                time.sleep(2)
                el.set_text(values[i])
            else:
                print(f"❌ Field {i+1} not found")

        company_address_details_province = '//android.widget.ScrollView/android.view.View[8]/android.view.View[6]'

        if self.d.xpath(company_address_details_province).exists:
            self.d.xpath(company_address_details_province).click()
            time.sleep(1)
        else:            
            print("❌ Province dropdown not found")

        locations = [
            "Bali",
            "Denpasar",
            "Denpasar Utara",
            "Ubung Kaja"
        ]

        for loc in locations:
            print(f"Checking for location: {loc}")

            xpath = f'//android.view.View[@content-desc="{loc}"]'

            el = self.d.xpath(xpath)

            if el.wait(timeout=3):
                print(f"Found: {loc}")

                el.click()
                time.sleep(1)

            else:
                print(f"❌ {loc} not found")
            

        
        self.scroll_down()
        # if self.d(description="Drop at receptionist").exists(timeout=1):
        #     self.d(description="Drop at receptionist").click()
        # elif self.d(description="Leave at receptionist").exists(timeout=1):
        #     self.d(description="Leave at receptionist").click()
            
        # time.sleep(1)



    def click_continue(self):

        el = self.d.xpath(
            '//android.view.View[@content-desc="Continue application"]'
        )

        if el.wait(timeout=3):
            print("✅ Continue button found")

            el.click()
            time.sleep(2)

            return True

        print("❌ Continue button not found")

        return False

class KtpPage(BasePage):
    def is_visible(self, timeout=5):
        print("  👉 Checking if KTP page is visible...")
        return (
            self.d(description="Verify identity and personal details").exists(timeout=timeout) or
            self.d(description="KTP").exists(timeout=timeout)
        )

    def click_camera(self):
        for txt in ["Open camera", "Take Photo", "Ambil Foto", "Camera", "Kamera"]:
            el = self.d(description=txt)
            print(f"Checking for camera button with description: {txt}")
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

    def is_camera_opened(self, timeout=5):
        camera_text = self.d.xpath('//android.view.View[@content-desc="Ensure that your KTP is clearly readable and aligned with the indicator box"]')

        if camera_text.wait(timeout=timeout):
            print("✓ Camera opened successfully")
            return True

        return False
    
    def capture_photo(self):
        capture_btn = self.d.xpath(
            '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]'
        )

        crop_btn = self.d.xpath(
            '//android.widget.Button[@content-desc="Crop"]'
        )

        # Capture image
        if not capture_btn.wait(timeout=5):
            print("✗ Capture button not found")
            return False
        


        capture_btn.click()
        time.sleep(8)
        print("✓ Photo captured")

        # Confirm crop
        if not crop_btn.wait(timeout=5):
            print("✗ Crop button not found")
            return False

        crop_btn.click()
        time.sleep(2)
        print("✓ Crop confirmed")

        return True

    def click_camera_back(self):
        back_btn = self.d.xpath('//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.ImageView[2]')

        if back_btn.wait(timeout=3):
            back_btn.click()
            time.sleep(1)
            print("✓ Returned from camera")
            return True

        return False
    

    def fill_mothers_maiden_name(self, name="Jane Doe"):
        el = self.d(className="android.widget.EditText")

        if el.exists(timeout=2):
            el.set_text(name)
            time.sleep(1)
            return True

        return False

    def click_continue(self):
        for txt in ["Continue", "Lanjut", "Next", "Selanjutnya"]:
            el = self.d(description=txt)

            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True

        return False
class HomeAddressPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(description="Your current address").exists(timeout=timeout) or
            self.d(description="Residence type").exists(timeout=timeout) or
            self.d(description ="Address").exists(timeout=timeout)
        )

    def fill_address(self, street="Jl. Jend. Sudirman", block="Blok B", house_no="No. 1", rt="01", rw="02"):
    #     if self.d(description="Landed house/Kost").exists(timeout=1):
    #         self.d(description="Landed house/Kost").click()
    #     elif self.d(description="Apartment").exists(timeout=1):
    #         self.d(description="Apartment").click()
            
    #     el_list = self.d(className="android.widget.EditText")
    #     if el_list.exists(timeout=2):
    #         if len(el_list) >= 1:
    #             el_list[0].set_text(street)
    #         if len(el_list) >= 2:
    #             el_list[1].set_text(block)
    #         if len(el_list) >= 3:
    #             el_list[2].set_text(house_no)
    #         if len(el_list) >= 4:
    #             el_list[3].set_text(rt)
    #         if len(el_list) >= 5:
    #             el_list[4].set_text(rw)
    #     time.sleep(1)


        fields = [
            '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[6]/android.view.View[1]',
            '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[6]/android.view.View[2]',
            '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[6]/android.view.View[3]',
            '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[6]/android.view.View[4]',
            '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[6]/android.view.View[5]',
        ]

        values = [street, block, house_no, rt, rw]

        for i in range(len(fields)):
            el = self.d.xpath(fields[i])
            if el.wait:
                time.sleep(2)
                el.set_text(values[i])
                self.d(description="Your current address").click()  # click outside to remove focus
                time.sleep(1)
            else:
                print(f"❌ Field {i+1} not found")

        click_province = '//android.widget.ScrollView/android.view.View[7]'

        if self.d.xpath(click_province).exists:
            self.d.xpath(click_province).click()
            time.sleep(1)
        else:            
            print("❌ Province dropdown not found")

        locations = [
            "Bali",
            "Denpasar",
            "Denpasar Utara",
            "Ubung Kaja"
        ]

        for loc in locations:
            print(f"Checking for location: {loc}")

            xpath = f'//android.view.View[@content-desc="{loc}"]'

            el = self.d.xpath(xpath)

            if el.wait(timeout=3):
                print(f"Found: {loc}")

                el.click()
                time.sleep(1)

            else:
                print(f"❌ {loc} not found")
    def click_submit(self):
        for txt in ["Continue", "Lanjut", "Next", "Selanjutnya", "Submit", "Simpan"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class LivenessPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Almost done We need your selfie").exists(timeout=timeout)
        )

    def click_continue(self):
        for txt in ["Continue", "Lanjut", "Start", "Mulai", "Take Selfie", "Ambil Selfie"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

# class DeliveryPage(BasePage):
#     def is_visible(self, timeout=5):
#         return (
#             self.d(textContains="Where should we send your card").exists(timeout=timeout) or
#             self.d(textContains="Delivery location").exists(timeout=timeout) or
#             self.d(textContains="Delivery").exists(timeout=timeout) or
#             self.d(textContains="Pengiriman").exists(timeout=timeout)
#         )

    def select_address(self):
        # Click the first available address card or radio button
        for txt in ["Home", "Rumah", "Office", "Kantor"]:
            el = self.d(description=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(0.5)
                return True
        return False

    def click_confirm(self):
        for txt in ["Deliver to this address", "Confirm", "Konfirmasi", "Continue", "Lanjut"]:
            el = self.d(description=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class ManualVerificationPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Manual Verification").exists(timeout=timeout) or
            self.d(textContains="Verifikasi Manual").exists(timeout=timeout) or
            self.d(textContains="Gatekeeper").exists(timeout=timeout) or
            self.d(textContains="Review").exists(timeout=timeout)
        )

    def click_continue(self):
        for txt in ["Continue", "Lanjut", "Understood", "Mengerti"]:
            el = self.d(description=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class GatekeeperAddressPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Additional Address").exists(timeout=timeout) or
            self.d(textContains="Gatekeeper").exists(timeout=timeout) or
            self.d(textContains="Confirm Address").exists(timeout=timeout)
        )

    def fill_address(self, address="Additional Gatekeeper Address"):
        el = self.d(className="android.widget.EditText")
        if el.exists(timeout=2):
            el.set_text(address)
            time.sleep(1)

    def click_submit(self):
        for txt in ["Continue", "Lanjut", "Submit", "Simpan"]:
            el = self.d(description=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class ReferenceContactsPage(BasePage):
    """Page for entering reference contacts during onboarding"""
    def is_visible(self, timeout=5):
        return (
            self.d(descriptionContains="Add reference contacts").exists(timeout=timeout) or
            self.d(descriptionContains="reference contact").exists(timeout=timeout)
        )

    def fill_details(self, name1="John Doe", phone1="8123456789", name2="Jane Doe", phone2="8987654321"):
        print("  👉 Filling reference contact details...")
        el_list = self.d(className="android.widget.EditText")
        if el_list.exists(timeout=2):
            if len(el_list) >= 1:
                el_list[0].click()
                time.sleep(.5)
                el_list[0].set_text(name1)
            if len(el_list) >= 2:
                el_list[1].click()
                time.sleep(.5)
                el_list[1].set_text(phone1)
            if len(el_list) >= 3:
                el_list[2].click()
                time.sleep(.5)
                el_list[2].set_text(name2)
            if len(el_list) >= 4:
                el_list[3].click()
                time.sleep(.5)
                el_list[3].set_text(phone2)
            time.sleep(1)

    def fill_relationship(self, relation1="Parent", relation2="Relative"):
        self.scroll_down()
        print("  👉 Filling reference contact relationships...")
        relation1_element = self.d.xpath(f'(//android.view.View[@content-desc="{relation1}"])[1]')
        relation2_element = self.d.xpath(f'(//android.view.View[@content-desc="{relation2}"])[2]')
        if relation1_element.wait(timeout=2):
            relation1_element.click()
            time.sleep(0.5)
        if relation2_element.wait(timeout=2):
            relation2_element.click()
            time.sleep(0.5)  


    def click_continue(self):
        for txt in ["Continue", "Lanjut", "Submit", "Simpan"]:
            el = self.d(descriptionContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False
    
class BypassKTPAndLivenessPage(BasePage):    
    def bypass_ktp_and_liveness_state(self):
        db = DBHelper()
        # user_id = self._data.get("user_id")
        user_id = 'SC062026000105'
        insert_sc_user_ktp_address(db,user_id)
        update_kyc_details(db,user_id)
        update_document_status(db,user_id)
        insert_kyc_facematch_trans(db,user_id)
        return True
        time.sleep(10)
    def navigated_to_checkpoints(self):
        return self.d(descriptionContains="Welcome back").exists(timeout=3)
    def click_continue(self):
        for txt in ["Continue", "Lanjut", "Next", "Selanjutnya"]:
            el = self.d(descriptionContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False
    def reached_delivery_page(self):
        return self.d(descriptionContains="Choose your card delivery destination").exists(timeout=3)
            


