#!/usr/bin/env python3
"""
Page Objects for Transactions & Rewards pages.
"""
import time
from pages.base_page import BasePage

class RedemptionDetailsPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Redemption").exists(timeout=timeout) or self.d(textContains="Penukaran").exists(timeout=timeout)
    def click_close(self):
        for txt in ["Close", "Tutup", "Done", "Selesai"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False

class TransactionDetailsPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Transaction Details").exists(timeout=timeout) or self.d(textContains="Detail Transaksi").exists(timeout=timeout)
    def go_back(self):
        self.d.press("back")
        time.sleep(1)
        return True

class TransactionStatementPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Statement").exists(timeout=timeout) or self.d(textContains="Tagihan").exists(timeout=timeout)
    def go_back(self):
        self.d.press("back")
        time.sleep(1)
        return True

class TransactionsFilteredListPage(BasePage):
    def is_visible(self, timeout=5):
        return self.d(textContains="Filter").exists(timeout=timeout) and (self.d(textContains="Transactions").exists(timeout=timeout) or self.d(textContains="Transaksi").exists(timeout=timeout))
    def clear_filters(self):
        for txt in ["Clear", "Hapus", "Reset"]:
            el = self.d(textContains=txt)
            if el.exists(timeout=1):
                el.click()
                return True
        return False
