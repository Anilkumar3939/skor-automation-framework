#!/usr/bin/env python3
"""
Page Objects for Card Management Screens.
Includes: Card Replacement, Card Block How-To, Miles Conversion Success.
"""
import time
from pages.base_page import BasePage

class CardReplacementPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Replacement").exists(timeout=timeout) or
            self.d(textContains="Ganti Kartu").exists(timeout=timeout)
        )

    def click_continue(self):
        for txt in ["Continue", "Lanjut", "Request", "Minta"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class CardBlockHowToPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="How to block").exists(timeout=timeout) or
            self.d(textContains="Cara blokir").exists(timeout=timeout) or
            self.d(textContains="Help").exists(timeout=timeout)
        )

    def click_understood(self):
        for txt in ["Understood", "Mengerti", "Close", "Tutup"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class MilesConversionSuccessPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Conversion Success").exists(timeout=timeout) or
            self.d(textContains="Berhasil").exists(timeout=timeout) or
            self.d(textContains="Miles").exists(timeout=timeout)
        )

    def click_close(self):
        for txt in ["Back to Home", "Kembali ke Beranda", "Close", "Tutup", "Done", "Selesai"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False
