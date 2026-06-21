#!/usr/bin/env python3
"""
BasePage — uiautomator2 equivalent of an Appium Page Object base class.
All page classes inherit from here and receive the live device handle.
"""
import time


class BasePage:

    def __init__(self, device):
        self.d = device   # uiautomator2 device instance

    # ------------------------------------------------------------------ #
    #  Element finders — return element or None (never raise)
    # ------------------------------------------------------------------ #

    def _by_desc(self, description, timeout=5):
        el = self.d(description=description)
        return el if el.exists(timeout=timeout) else None

    def _by_text(self, text, timeout=5):
        el = self.d(text=text)
        return el if el.exists(timeout=timeout) else None

    def _by_desc_contains(self, partial, timeout=5):
        el = self.d(descriptionContains=partial)
        return el if el.exists(timeout=timeout) else None

    def _by_text_contains(self, partial, timeout=5):
        el = self.d(textContains=partial)
        return el if el.exists(timeout=timeout) else None

    def _by_class(self, class_name, instance=0, timeout=5):
        el = self.d(className=class_name, instance=instance)
        return el if el.exists(timeout=timeout) else None

    def _by_res_id(self, resource_id, timeout=5):
        el = self.d(resourceId=resource_id)
        return el if el.exists(timeout=timeout) else None

    # ------------------------------------------------------------------ #
    #  Existence checks
    # ------------------------------------------------------------------ #

    def exists_desc(self, description, timeout=5):
        return self.d(description=description).exists(timeout=timeout)

    def exists_text(self, text, timeout=3):
        return self.d(text=text).exists(timeout=timeout)

    def exists_text_contains(self, partial, timeout=3):
        return self.d(textContains=partial).exists(timeout=timeout)

    def exists_desc_contains(self, partial, timeout=5):
        return self.d(descriptionContains=partial).exists(timeout=timeout)

    # ------------------------------------------------------------------ #
    #  Tap helpers — return True/False, never raise
    # ------------------------------------------------------------------ #

    def tap_desc(self, description, timeout=8):
        try:
            el = self.d(description=description)
            if el.exists(timeout=timeout):
                el.click()
                time.sleep(0.4)
                return True
            return False
        except Exception:
            return False

    def tap_text(self, text, timeout=8):
        try:
            el = self.d(text=text)
            if el.exists(timeout=timeout):
                el.click()
                time.sleep(0.4)
                return True
            return False
        except Exception:
            return False

    def tap_res_id(self, resource_id, timeout=8):
        try:
            el = self.d(resourceId=resource_id)
            if el.exists(timeout=timeout):
                el.click()
                time.sleep(0.4)
                return True
            return False
        except Exception:
            return False

    # ------------------------------------------------------------------ #
    #  Text / attribute reads
    # ------------------------------------------------------------------ #

    def get_content_desc(self, description, timeout=5):
        """Return the contentDescription attribute of an element."""
        try:
            el = self._by_desc(description, timeout)
            if el:
                return el.info.get("contentDescription", "")
        except Exception:
            pass
        return ""

    def get_edit_text(self, instance=0, timeout=5):
        """Return the current text of an EditText by instance index."""
        try:
            el = self._by_class("android.widget.EditText", instance, timeout)
            if el:
                return el.get_text() or ""
        except Exception:
            pass
        return ""

    def get_edit_hint(self, instance=0, timeout=5):
        """Return the hint/placeholder of an EditText."""
        try:
            el = self._by_class("android.widget.EditText", instance, timeout)
            if el:
                info = el.info
                return info.get("hint", info.get("text", ""))
        except Exception:
            pass
        return ""

    # ------------------------------------------------------------------ #
    #  Input — always uses set_text (no keyboard open = no scroll bug)
    # ------------------------------------------------------------------ #

    def set_edit_text(self, text, instance=0, timeout=5):
        """Set text on an EditText by instance index (no keyboard, no scroll)."""
        try:
            el = self._by_class("android.widget.EditText", instance, timeout)
            if el:
                el.set_text(text)
                time.sleep(0.4)
                return True
        except Exception:
            pass
        return False

    def clear_edit_text(self, instance=0, timeout=5):
        return self.set_edit_text("", instance, timeout)

    # ------------------------------------------------------------------ #
    #  Navigation / scroll
    # ------------------------------------------------------------------ #

    def back(self):
        self.d.press("back")
        time.sleep(0.5)

    def scroll_down(self):
        self.d.swipe(500, 1500, 500, 500, 0.4)
        time.sleep(0.3)

    def scroll_up(self):
        self.d.swipe(500, 500, 500, 1500, 0.4)
        time.sleep(0.3)
