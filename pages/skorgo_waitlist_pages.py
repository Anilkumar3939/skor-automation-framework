#!/usr/bin/env python3
"""
Page Objects for SkorGo and Waitlist Screens.
"""
import time
from pages.base_page import BasePage

class SkorGoNotInterestedPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Not Interested").exists(timeout=timeout) or
            self.d(textContains="Tidak Tertarik").exists(timeout=timeout)
        )

    def click_confirm(self):
        for txt in ["Confirm", "Konfirmasi", "Sure", "Yakin"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class SkorGoApprovedPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="SkorGo").exists(timeout=timeout) and
            (self.d(textContains="Approved").exists(timeout=timeout) or
             self.d(textContains="Disetujui").exists(timeout=timeout))
        )

    def click_continue(self):
        for txt in ["Continue", "Lanjut", "Activate", "Aktivasi"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class WaitlistConfirmationPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Waitlist").exists(timeout=timeout) and
            (self.d(textContains="Confirmed").exists(timeout=timeout) or
             self.d(textContains="Dikonfirmasi").exists(timeout=timeout) or
             self.d(textContains="Joined").exists(timeout=timeout))
        )

    def click_done(self):
        for txt in ["Done", "Selesai", "Got it", "Mengerti"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class WaitlistOpenSkorlifePage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Waitlist").exists(timeout=timeout) and
            self.d(textContains="Skorlife").exists(timeout=timeout)
        )

    def click_open(self):
        for txt in ["Open Skorlife", "Buka Skorlife", "Continue", "Lanjut"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False
