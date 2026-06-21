#!/usr/bin/env python3
"""
pytest conftest — shared hooks for Allure reporting.

What this does:
  • On any test failure, captures a screenshot from the device and attaches
    it to the Allure report automatically (same behaviour as appium-project).
  • Adds the tests/ directory to sys.path so base.py / page objects import cleanly.

Usage:
    pytest tests/ --alluredir=allure-results
    allure serve allure-results
"""
import os
import sys
from datetime import datetime

import pytest

# Make tests/ and root importable
_ROOT = os.path.dirname(os.path.abspath(__file__))
for _p in [_ROOT, os.path.join(_ROOT, "tests")]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

SCREENSHOTS_DIR = os.path.join(_ROOT, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a failure screenshot to the Allure report."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            import allure
            instance = item.instance
            if instance and hasattr(instance, "d"):
                ts = datetime.now().strftime("%H%M%S")
                path = os.path.join(SCREENSHOTS_DIR, f"{ts}_FAIL_{item.name}.png")
                instance.d.screenshot(path)
                with open(path, "rb") as f:
                    allure.attach(
                        f.read(),
                        name=f"FAIL — {item.name}",
                        attachment_type=allure.attachment_type.PNG,
                    )
        except Exception:
            pass
