#!/usr/bin/env python3
"""
Page Objects for KYC Additional Information screens.
Includes: Mother's Name, Spouse Name, Consent, Selfie Initial, VKYC, Phone/Email Change.
"""
import time
from pages.base_page import BasePage

class MothersNamePage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Mother").exists(timeout=timeout) or
            self.d(textContains="Ibu").exists(timeout=timeout)
        )

    def fill_name(self, name="Siti Aminah"):
        el = self.d(className="android.widget.EditText")
        if el.exists(timeout=2):
            el.set_text(name)
            time.sleep(0.5)

    def click_submit(self):
        for txt in ["Continue", "Lanjut", "Next", "Submit"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class SpouseNamePage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Spouse").exists(timeout=timeout) or
            self.d(textContains="Pasangan").exists(timeout=timeout)
        )

    def fill_name(self, name="Budi Santoso"):
        el = self.d(className="android.widget.EditText")
        if el.exists(timeout=2):
            el.set_text(name)
            time.sleep(0.5)

    def click_submit(self):
        for txt in ["Continue", "Lanjut", "Next", "Submit"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class SkorlifeConsentPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Consent").exists(timeout=timeout) or
            self.d(textContains="Persetujuan").exists(timeout=timeout) or
            self.d(textContains="Agreement").exists(timeout=timeout)
        )

    def check_consent(self):
        el = self.d(className="android.widget.CheckBox")
        if el.exists(timeout=2):
            el.click()
            time.sleep(0.5)

    def click_submit(self):
        for txt in ["Agree", "Setuju", "Continue", "Lanjut"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class SelfieInitialPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Take Selfie").exists(timeout=timeout) or
            self.d(textContains="Ambil Selfie").exists(timeout=timeout) or
            self.d(textContains="Face").exists(timeout=timeout)
        )

    def click_start(self):
        for txt in ["Start", "Mulai", "Continue", "Lanjut"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class VkycInformationPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Video").exists(timeout=timeout) or
            self.d(textContains="VKYC").exists(timeout=timeout)
        )

    def click_start(self):
        for txt in ["Start Video", "Mulai Video", "Call", "Panggil"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class PhoneEmailChangePage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Change Phone").exists(timeout=timeout) or
            self.d(textContains="Ubah Nomor").exists(timeout=timeout) or
            self.d(textContains="Change Email").exists(timeout=timeout) or
            self.d(textContains="Ubah Email").exists(timeout=timeout)
        )

    def click_submit(self):
        for txt in ["Update", "Perbarui", "Save", "Simpan"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False
