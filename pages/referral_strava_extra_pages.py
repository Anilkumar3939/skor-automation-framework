#!/usr/bin/env python3
"""
Page Objects for Extra Referral and Strava Flow Screens.
"""
import time
from pages.base_page import BasePage

class ReferralHistoryPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Referral History").exists(timeout=timeout) or
            self.d(textContains="Riwayat").exists(timeout=timeout)
        )

    def go_back(self):
        self.d.press("back")
        time.sleep(1)
        return True

class ReferralTrackingPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Tracking").exists(timeout=timeout) or
            self.d(textContains="Pelacakan").exists(timeout=timeout)
        )

    def go_back(self):
        self.d.press("back")
        time.sleep(1)
        return True

class StravaFaqPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="FAQ").exists(timeout=timeout) or
            self.d(textContains="Questions").exists(timeout=timeout) or
            self.d(textContains="Pertanyaan").exists(timeout=timeout)
        )

    def click_close(self):
        for txt in ["Close", "Tutup", "Done", "Selesai"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class StravaOnboardingPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Strava").exists(timeout=timeout) and
            (self.d(textContains="Welcome").exists(timeout=timeout) or
             self.d(textContains="Selamat datang").exists(timeout=timeout))
        )

    def click_continue(self):
        for txt in ["Continue", "Lanjut", "Connect", "Hubungkan"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False
