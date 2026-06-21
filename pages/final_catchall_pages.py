#!/usr/bin/env python3
"""
Page Objects for final catch-all miscellaneous screens (Errors, Merchants, Success variants).
"""
import time
from pages.base_page import BasePage

class ErrorInfoPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Error Info").exists(timeout=timeout) or self.d(textContains="Informasi Error").exists(timeout=timeout)
    def click_close(self):
        for txt in ["Close", "Tutup", "Okay"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False

class ErrorReasonViewPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Reason").exists(timeout=timeout) or self.d(textContains="Alasan").exists(timeout=timeout)
    def click_close(self):
        for txt in ["Close", "Tutup", "Okay", "Mengerti"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False

class GeneralErrorPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="General Error").exists(timeout=timeout) or self.d(textContains="Terjadi Kesalahan").exists(timeout=timeout)
    def click_retry(self):
        for txt in ["Retry", "Coba Lagi", "Kembali"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False

class SkorlifeWaitlistPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Waitlist").exists(timeout=timeout) and self.d(textContains="Skorlife").exists(timeout=timeout)
    def click_continue(self):
        for txt in ["Continue", "Lanjut"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False

class UnderwritingErrorCarouselPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Underwriting").exists(timeout=timeout) and self.d(textContains="Error").exists(timeout=timeout)
    def swipe_carousel(self):
        self.d.swipe_ext("left", scale=0.8)
        time.sleep(1)
        return True

class CardOnFileMerchantsPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Merchants").exists(timeout=timeout) or self.d(textContains="Merchant").exists(timeout=timeout)
    def go_back(self):
        self.d.press("back")
        time.sleep(1)
        return True

class DashboardApprovalV2Page(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Approval").exists(timeout=timeout) or self.d(textContains="Persetujuan").exists(timeout=timeout)
    def click_continue(self):
        for txt in ["Continue", "Lanjut", "Activate", "Aktivasi"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False

class KycSuccessVerificationV2Page(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="KYC Success").exists(timeout=timeout) or self.d(textContains="KYC Berhasil").exists(timeout=timeout)
    def click_continue(self):
        for txt in ["Continue", "Lanjut", "Next"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False

class EmergencyContactV2Page(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Emergency Contact").exists(timeout=timeout) or self.d(textContains="Kontak Darurat").exists(timeout=timeout)
    def click_submit(self):
        for txt in ["Submit", "Simpan", "Continue", "Lanjut"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False

class SelfieCameraImagePreviewPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Preview").exists(timeout=timeout) or self.d(textContains="Pratinjau").exists(timeout=timeout)
    def click_retake(self):
        for txt in ["Retake", "Foto Ulang"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False

class WaitlistInfoViewPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Waitlist Info").exists(timeout=timeout) or self.d(textContains="Info Waitlist").exists(timeout=timeout)
    def click_close(self):
        for txt in ["Close", "Tutup", "Mengerti"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False
