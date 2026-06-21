#!/usr/bin/env python3
"""
Page Objects for Underwriting Status and VKYC Scheduling screens.
"""
import time
from pages.base_page import BasePage

class PhoneVerificationPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Phone Verification").exists(timeout=timeout) or self.d(textContains="Verifikasi Telepon").exists(timeout=timeout)
    def click_continue(self):
        for txt in ["Continue", "Lanjut"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False

class PhoneVerificationBookedPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Booked").exists(timeout=timeout) and self.d(textContains="Phone").exists(timeout=timeout)
    def click_done(self):
        for txt in ["Done", "Selesai"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False

class VerifyingDataPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Verifying Data").exists(timeout=timeout) or self.d(textContains="Memverifikasi Data").exists(timeout=timeout)
    def click_refresh(self):
        for txt in ["Refresh", "Muat Ulang"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False

class VkycVerificationBookedPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="VKYC").exists(timeout=timeout) and self.d(textContains="Booked").exists(timeout=timeout)
    def click_done(self):
        for txt in ["Done", "Selesai"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False

class VkycVerificationCompletedPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="VKYC").exists(timeout=timeout) and self.d(textContains="Completed").exists(timeout=timeout)
    def click_continue(self):
        for txt in ["Continue", "Lanjut"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False

class VkycVerificationPendingPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="VKYC").exists(timeout=timeout) and self.d(textContains="Pending").exists(timeout=timeout)
    def click_refresh(self):
        for txt in ["Refresh", "Muat Ulang"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False

class CardActivationPendingPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Activation Pending").exists(timeout=timeout)
    def click_ok(self):
        for txt in ["OK", "Mengerti"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False

class ContinueApplicationPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Continue Application").exists(timeout=timeout) or self.d(textContains="Lanjutkan Aplikasi").exists(timeout=timeout)
    def click_continue(self):
        for txt in ["Continue", "Lanjut"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False

class ReachedLimitForCardNumberPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Reached Limit").exists(timeout=timeout) or self.d(textContains="Batas Maksimum").exists(timeout=timeout)
    def click_close(self):
        for txt in ["Close", "Tutup", "Mengerti"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False

class PinResetSuccessPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="PIN Reset Success").exists(timeout=timeout) or self.d(textContains="Reset PIN Berhasil").exists(timeout=timeout)
    def click_done(self):
        for txt in ["Done", "Selesai"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False
