#!/usr/bin/env python3
"""
Page Objects for Dashboard extra features (Referral, Gamification, Strava, SkorGo, Card Controls).
"""
import time
from pages.base_page import BasePage

class ReferralPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Referral").exists(timeout=timeout) or
            self.d(textContains="Invite").exists(timeout=timeout) or
            self.d(textContains="Undang").exists(timeout=timeout)
        )

    def click_share(self):
        for txt in ["Share", "Bagikan", "Invite Now", "Undang Sekarang"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class GamificationIntroPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Game").exists(timeout=timeout) or
            self.d(textContains="Play").exists(timeout=timeout) or
            self.d(textContains="Main").exists(timeout=timeout)
        )

    def click_start(self):
        for txt in ["Start", "Mulai", "Play Now", "Main Sekarang"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class StravaLandingPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Strava").exists(timeout=timeout) or
            self.d(textContains="Connect").exists(timeout=timeout)
        )

    def click_connect(self):
        for txt in ["Connect", "Hubungkan", "Link"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class SkorGoEducationPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="SkorGo").exists(timeout=timeout) or
            self.d(textContains="Education").exists(timeout=timeout)
        )

    def click_continue(self):
        for txt in ["Got it", "Mengerti", "Continue", "Lanjut"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False

class CardControlPage(BasePage):
    def is_visible(self, timeout=5):
        return (
            self.d(textContains="Card Control").exists(timeout=timeout) or
            self.d(textContains="Pengaturan Kartu").exists(timeout=timeout)
        )

    def click_block_card(self):
        for txt in ["Block", "Blokir", "Freeze", "Bekukan"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                time.sleep(1)
                return True
        return False
