#!/usr/bin/env python3
"""
Page Objects for KYC Extra Flows (Marital, Religion, Political).
"""
import time
from pages.base_page import BasePage

class CardSelectionPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Select Card").exists(timeout=timeout) or self.d(textContains="Pilih Kartu").exists(timeout=timeout)
    def click_continue(self):
        for txt in ["Continue", "Lanjut"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False

class MartialReligionFlowPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Religion").exists(timeout=timeout) or self.d(textContains="Agama").exists(timeout=timeout)
    def click_submit(self):
        for txt in ["Continue", "Lanjut", "Save", "Simpan"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False

class PhoneNumberChangeFlowPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Change Phone").exists(timeout=timeout) or self.d(textContains="Ubah Nomor").exists(timeout=timeout)
    def click_submit(self):
        for txt in ["Update", "Perbarui", "Save", "Simpan"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False

class PoliticalPersonSelectionPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Political").exists(timeout=timeout) or self.d(textContains="Politik").exists(timeout=timeout)
    def click_submit(self):
        for txt in ["Submit", "Kirim", "Continue", "Lanjut"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False
