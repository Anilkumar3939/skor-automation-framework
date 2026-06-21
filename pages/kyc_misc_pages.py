#!/usr/bin/env python3
"""
Page Objects for Miscellaneous KYC and Approvals.
"""
import time
from pages.base_page import BasePage

class SpouseAdditionalInfoPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Spouse").exists(timeout=timeout) and
            (self.d(textContains="Additional").exists(timeout=timeout) or
             self.d(textContains="Tambahan").exists(timeout=timeout))
        )

    def click_submit(self):
        for txt in ["Submit", "Simpan", "Continue", "Lanjut"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class SelfieMatchFailPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Selfie").exists(timeout=timeout) and
            (self.d(textContains="Failed").exists(timeout=timeout) or
             self.d(textContains="Gagal").exists(timeout=timeout) or
             self.d(textContains="Match").exists(timeout=timeout))
        )

    def click_retry(self):
        for txt in ["Try Again", "Coba Lagi", "Retry"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class CardApprovedScreen(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Card Approved").exists(timeout=timeout) or
            self.d(textContains="Kartu Disetujui").exists(timeout=timeout)
        )

    def click_continue(self):
        for txt in ["Continue", "Lanjut", "Activate", "Aktivasi"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class GenericApprovedPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Approved").exists(timeout=timeout) or
            self.d(textContains="Disetujui").exists(timeout=timeout)
        )

    def click_continue(self):
        for txt in ["Continue", "Lanjut", "Next", "Selanjutnya"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False
