#!/usr/bin/env python3
"""
Page Objects for Onboarding status and error screens.
Includes: Card Ready, Waiting Page, Underwriting Errors, UW Approved.
"""
import time
from pages.base_page import BasePage

class CardReadyPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Card Ready").exists(timeout=timeout) or
            self.d(textContains="Kartu Siap").exists(timeout=timeout) or
            self.d(textContains="Ready to use").exists(timeout=timeout)
        )

    def click_continue(self):
        for txt in ["Continue", "Lanjut", "Activate", "Aktivasi", "Go to Dashboard", "Ke Beranda"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class WaitingPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Waiting").exists(timeout=timeout) or
            self.d(textContains="Menunggu").exists(timeout=timeout) or
            self.d(textContains="Review").exists(timeout=timeout)
        )

    def click_refresh(self):
        for txt in ["Refresh", "Muat Ulang", "Check Status", "Cek Status"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class UnderwritingErrorPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Sorry").exists(timeout=timeout) or
            self.d(textContains="Maaf").exists(timeout=timeout) or
            self.d(textContains="Failed").exists(timeout=timeout) or
            self.d(textContains="Gagal").exists(timeout=timeout)
        )

    def click_close(self):
        for txt in ["Close", "Tutup", "Back to Home", "Kembali ke Beranda", "Ok", "Mengerti"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class UWApprovedPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Approved").exists(timeout=timeout) or
            self.d(textContains="Disetujui").exists(timeout=timeout) or
            self.d(textContains="Congratulations").exists(timeout=timeout) or
            self.d(textContains="Selamat").exists(timeout=timeout)
        )

    def click_continue(self):
        for txt in ["Continue", "Lanjut", "See limit", "Lihat limit"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False
