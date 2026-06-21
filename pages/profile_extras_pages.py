#!/usr/bin/env python3
"""
Page Objects for Profile Extras.
"""
import time
from pages.base_page import BasePage

class CardChargesPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Charges").exists(timeout=timeout) or self.d(textContains="Biaya").exists(timeout=timeout)
    def go_back(self):
        self.d.press("back")
        time.sleep(1)
        return True

class ChangeLanguagePage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Language").exists(timeout=timeout) or self.d(textContains="Bahasa").exists(timeout=timeout)
    def go_back(self):
        self.d.press("back")
        time.sleep(1)
        return True

class HelpCenterPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Help Center").exists(timeout=timeout) or self.d(textContains="Pusat Bantuan").exists(timeout=timeout)
    def go_back(self):
        self.d.press("back")
        time.sleep(1)
        return True

class ResetCreditCardPinPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Reset PIN").exists(timeout=timeout)
    def go_back(self):
        self.d.press("back")
        time.sleep(1)
        return True

class GenericWebViewPage(BasePage):
    def is_visible(self, timeout=5):
        # WebViews are usually identifiable by class name
        return self.d(className="android.webkit.WebView").exists(timeout=timeout)
    def go_back(self):
        self.d.press("back")
        time.sleep(1)
        return True
