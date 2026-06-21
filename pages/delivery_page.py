import time


class DeliveryPage():
    def __init__(self, driver):
        self.driver = driver

    def is_visible_start(self, timeout=5):
        return (self.driver(descriptionContains="Choose your card delivery destination").exists(timeout=timeout) and
                self.driver(descriptionContains="Home").exists(timeout=2) and 
                self.driver(descriptionContains="Workplace").exists(timeout=2))
    
    def is_visible(self, timeout=5):
        return (self.driver(descriptionContains="Where should we send your card?").exists(timeout=timeout) and
                self.driver(descriptionContains="Home").exists(timeout=2) and 
                self.driver(descriptionContains="Workplace").exists(timeout=2))
    
    def scroll_to_bottom(self):
        """Scroll down to reveal T&C checkbox and submit button."""
        self.driver.swipe(500, 1400, 500, 400, 0.4)
        time.sleep(0.4)


    def select_delivery_option(self, option):
        el = self.driver(descriptionContains=option)
        if el.exists(timeout=5):
            el.click()
        else:
            raise Exception(f"{option} delivery option not found")
        
    def home_delivery_elements_visible(self):
        return (self.driver(descriptionContains="Input your current home address").exists(timeout=3))
    
    
    def entering_province_city_district_subDistrict(self, locations):
        click_province = self.driver(descriptionContains="Province, City, District, Subdistrict")

        if click_province.exists(timeout=5):
            click_province.click()
            time.sleep(1)
        else:            
            print("❌ Province dropdown not found")
            raise Exception('field missed')
    

        for loc in locations:
            print(f"Checking for location: {loc}")

            xpath = f'//android.view.View[@content-desc="{loc}"]'

            el = self.driver.xpath(xpath)

            if el.wait(timeout=3):
                print(f"Found: {loc}")

                el.click()
                time.sleep(1)

            else:
                print(f"❌ {loc} not found")
                raise Exception(f"{loc} not found")
    def fill_home_address(self, type,address,locations):
        self.entering_province_city_district_subDistrict(locations)
        homeType = self.driver(descriptionContains=type)
        if homeType.exists(timeout=5):
            homeType.click()
        else:
            raise Exception("Home address type not found")
        el = self.driver.xpath('//android.widget.ScrollView/android.view.View[8]/android.widget.EditText')
        if el.exists:
            el.set_text(address)
        else:
            raise Exception("Home address field not found")
        rt = self.driver.xpath('//android.widget.ScrollView/android.view.View[11]/android.widget.EditText')

        if rt.exists:
            rt.set_text("001")

        rw = self.driver.xpath('//android.widget.ScrollView/android.view.View[12]/android.widget.EditText')
        if rw.exists:
            rw.set_text("001")
        
    def fill_workplace_address(self, type,address,locations):
        self.entering_province_city_district_subDistrict(locations)
        workPlaceType = self.driver(descriptionContains=type)

        if workPlaceType.exists(timeout=5):
            workPlaceType.click()
        else:
            raise Exception("Workplace address type not found")
        

        el = self.driver.xpath('//android.widget.ScrollView/android.view.View[8]/android.widget.EditText')
        if el.exists:
            el.set_text(address)
        else:
            raise Exception("Workplace address field not found")
        
    def click_continue(self):
        el = self.driver(descriptionContains="Continue")
        if el.exists(timeout=5):
            el.click()
        else:
            raise Exception("Continue button not found")




    def workplace_delivery_elements_visible(self):
        return self.driver(
            descriptionContains="Input your current workplace address"
        ).exists(timeout=3)

    def is_input_remaining_address_page_visible(self):
        return (
            self.driver(
                descriptionContains="Last step. Complete other address"
            ).exists(timeout=5)
        )


    def fill_other_address(self, address, locations):
        """
        Remaining address page
        """

        self.entering_province_city_district_subDistrict(locations)

        full_address = self.driver.xpath('//android.widget.EditText')

        if full_address.exists:
            full_address.set_text(address)
        else:
            raise Exception("Full address field not found")
        
        self.scroll_to_bottom()
        

        rt = self.driver.xpath('//android.widget.ScrollView/android.view.View[15]/android.widget.EditText')

        if rt.exists:
            rt.set_text("001")
        else:
            raise Exception("rt not found")

        rw = self.driver.xpath('//android.widget.ScrollView/android.view.View[16]/android.widget.EditText')
        if rw.exists:
            rw.set_text("001")
        else:
            raise Exception("rw not found")
        self.scroll_to_bottom()


    def click_submit(self):
        el = self.driver(descriptionContains="Submit")

        if el.exists(timeout=5):
            el.click()
        else:
            raise Exception("Submit button not found")

    def is_submission_success_page_visible(self):
        """
        Replace locator after seeing actual success page
        """

        # TODO:
        # Add actual success page locator

        return (
            self.driver(
                descriptionContains="Data Submitted"
            ).exists(timeout=10)
        )

    def get_selected_delivery_option(self):
        """
        Optional verification
        """

        # TODO:
        # Add actual locator if selected tab has different state

        pass

    def is_submission_success_page_visible(self):
        return self.driver(
            descriptionContains="your application has been submitted"
        ).exists(timeout=10)