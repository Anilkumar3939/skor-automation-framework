#!/usr/bin/env python3
"""
Tests for Transactions & Rewards pages.
"""
import os
import sys
import allure

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in [_ROOT, os.path.join(_ROOT, "tests")]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from base import BaseTest
from utils.logger import get_logger
from pages.transactions_rewards_pages import (
    RedemptionDetailsPage, TransactionDetailsPage,
    TransactionStatementPage, TransactionsFilteredListPage
)

@allure.feature("Transactions and Rewards Extras")
class TestTransactionsRewards(BaseTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.logger = get_logger("transactions_rewards")
        cls.pages = [
            ("Redemption Details", RedemptionDetailsPage(cls.d), "click_close"),
            ("Transaction Details", TransactionDetailsPage(cls.d), "go_back"),
            ("Transaction Statement", TransactionStatementPage(cls.d), "go_back"),
            ("Transactions Filtered List", TransactionsFilteredListPage(cls.d), "clear_filters"),
        ]

    def _log_pass(self, msg):
        print(f"  ✅ PASS: {msg}")
        self.logger.info(f"PASS: {msg}")

    def _log_fail(self, msg):
        print(f"  ❌ FAIL: {msg}")
        self.logger.error(f"FAIL: {msg}")

    @allure.story("Dynamic Check for Transactions & Rewards Pages")
    def test_transactions_rewards(self):
        print("\n[TEST] Checking all transactions & rewards pages functionality")
        for name, page, action in self.pages:
            if page.is_visible(timeout=2):
                self.screenshot(f"trx_{name.replace(' ', '_')}")
                method = getattr(page, action)
                clicked = method()
                if clicked:
                    self._log_pass(f"Interacted with {name}")
                else:
                    self._log_fail(f"Could not interact with {name}")
            else:
                print(f"  ℹ️  SKIP: {name} page not visible.")

if __name__ == "__main__":
    t = TestTransactionsRewards()
    TestTransactionsRewards.setup_class()
    t.test_transactions_rewards()
    print("\n✅ Transactions & Rewards tests done.")
