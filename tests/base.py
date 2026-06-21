#!/usr/bin/env python3
"""
BaseTest — foundation for all Skorcard test classes.

Compatible with both:
  • Custom runner  (python3 run_tests.py) — calls cls.setup_class() then cls()
  • pytest + Allure (pytest tests/)        — pytest calls setup_class() once per class
"""
import uiautomator2 as u2
import time
import os
from datetime import datetime

SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

APP_PACKAGE  = "app.skor.card"
APP_PASSCODE = os.environ.get("TEST_PASSCODE", "112233")


class BaseTest:
    """
    Device is connected ONCE per test class (via setup_class) and stored as a
    class attribute.  Instance attribute access (`self.d`) falls through to the
    class attribute, so every test method in the same class shares one connection.
    """

    # ------------------------------------------------------------------ #
    #  pytest lifecycle hooks  (also called explicitly by the custom runner)
    # ------------------------------------------------------------------ #
    _data = {}

    @classmethod
    def setup_class(cls):
        """Connect to the device.  Called once per class by pytest and by run_tests.py."""
        print(f"\nConnecting to device for {cls.__name__}...")
        cls.d = u2.connect()
        cls.d.implicitly_wait(10)
        info = cls.d.device_info
        print(f"Connected: {info.get('brand')} {info.get('model')}")

    @classmethod
    def teardown_class(cls):
        """Optional cleanup after all tests in the class."""
        pass

    # ------------------------------------------------------------------ #
    #  Screenshot
    # ------------------------------------------------------------------ #

    def screenshot(self, name: str):
        ts   = datetime.now().strftime("%H%M%S")
        path = os.path.join(SCREENSHOTS_DIR, f"{ts}_{name}.png")
        self.d.screenshot(path)
        print(f"  📸 {name}")
        return path

    # ------------------------------------------------------------------ #
    #  Tap helpers
    # ------------------------------------------------------------------ #

    def tap(self, description=None, text=None, coords=None, timeout=8):
        try:
            if description:
                el = self.d(description=description)
                if not el.exists(timeout=timeout):
                    print(f"  ⚠️  tap: '{description}' not found")
                    return False
                el.click()
            elif text:
                el = self.d(text=text)
                if not el.exists(timeout=timeout):
                    print(f"  ⚠️  tap: text='{text}' not found")
                    return False
                el.click()
            elif coords:
                self.d.click(*coords)
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"  ⚠️  tap exception: {e}")
            return False

    # ------------------------------------------------------------------ #
    #  Wait helpers
    # ------------------------------------------------------------------ #

    def wait_for(self, description=None, text=None, timeout=10):
        if description:
            return self.d(description=description).exists(timeout=timeout)
        elif text:
            return self.d(text=text).exists(timeout=timeout)
        return False

    # ------------------------------------------------------------------ #
    #  Input
    # ------------------------------------------------------------------ #

    def set_phone(self, number: str):
        """Set phone number directly without opening keyboard (avoids scroll)."""
        el = self.d(className="android.widget.EditText")
        if not el.exists(timeout=8):
            print("  ⚠️  set_phone: EditText not found")
            return
        el.set_text(number)
        time.sleep(0.5)

    # ------------------------------------------------------------------ #
    #  Assertions
    # ------------------------------------------------------------------ #

    def assert_visible(self, description=None, text=None, msg="", timeout=8):
        if description:
            exists = self.d(description=description).exists(timeout=timeout)
        else:
            exists = self.d(text=text).exists(timeout=timeout)
        label = description or text
        if exists:
            print(f"  ✅ PASS: '{label}' visible")
        else:
            print(f"  ❌ FAIL: '{label}' not found — {msg}")
        return exists

    def assert_not_visible(self, description=None, text=None, msg=""):
        if description:
            exists = self.d(description=description).exists(timeout=3)
        else:
            exists = self.d(text=text).exists(timeout=3)
        label = description or text
        if not exists:
            print(f"  ✅ PASS: '{label}' not visible (expected)")
        else:
            print(f"  ❌ FAIL: '{label}' should NOT be visible — {msg}")
        return not exists

    # ------------------------------------------------------------------ #
    #  App lifecycle
    # ------------------------------------------------------------------ #

    def _reconnect(self):
        try:
            self.__class__.d = u2.connect()
            self.__class__.d.implicitly_wait(10)
            print("  🔄 Reconnected")
        except Exception as e:
            print(f"  ⚠️  Reconnect failed: {e}")

    def dismiss_all(self):
        """Press back up to 5 times to close any open sheets/keyboards."""
        for _ in range(5):
            self.d.press("back")
            time.sleep(0.4)
            if self.d(description="Continue").exists(timeout=1):
                return True
        return False

    def reset_to_splash(self):
        """Ensure app is on the splash phone-input screen with an empty phone field."""
        self.dismiss_all()

        # Scroll up in case Continue is above the visible area
        if not self.d(description="Continue").exists(timeout=2):
            self.d.swipe(500, 500, 500, 1500, 0.4)
            time.sleep(0.4)

        on_splash = (
            self.d(description="Continue").exists(timeout=3) and
            self.d(className="android.widget.EditText").exists(timeout=2)
        )
        if not on_splash:
            self.launch_app()
            return
        el = self.d(className="android.widget.EditText")
        if el.exists(timeout=1):
            el.set_text("")
        time.sleep(0.3)

    # ------------------------------------------------------------------ #
    #  Passcode / PIN
    # ------------------------------------------------------------------ #

    def _is_passcode_screen(self) -> bool:
        return (
            self.d(textContains="Enter Passcode").exists(timeout=2) or
            self.d(textContains="Masukkan Passcode").exists(timeout=1) or
            self.d(textContains="Masukkan kode").exists(timeout=1)
        )

    def enter_passcode(self, code: str = None):
        code = code or APP_PASSCODE
        print(f"  🔑 Entering passcode ({len(code)} digits)...", end="", flush=True)
        for digit in code:
            btn = self.d(text=digit)
            if btn.exists(timeout=3):
                btn.click()
            else:
                self.d(description=digit).click()
            time.sleep(0.25)
        time.sleep(1.5)
        print(" done")

    def restart_app(self):
        """
        Fully stop then restart the app — guarantees a clean initial state.
        Use this when you need the very first splash screen (e.g. invitation-code tests).
        """
        try:
            self.d.app_start(APP_PACKAGE, stop=True)
        except Exception:
            self._reconnect()
            self.d.app_start(APP_PACKAGE, stop=True)

        print("  ⏳ Restarting app...", end="", flush=True)
        time.sleep(3)

        if self._is_passcode_screen():
            print(" 🔐 passcode screen detected")
            self.screenshot("passcode_screen")
            self.enter_passcode()
            self.screenshot("after_passcode")

        phone_ready = self.d(className="android.widget.EditText").exists(timeout=35)

        if not self.d(description="Continue").exists(timeout=2) and \
           not self.d(description="Proceed").exists(timeout=2):
            self.d.swipe(500, 500, 500, 1500, 0.4)
            time.sleep(0.5)

        btn_ready = (
            self.d(description="Continue").exists(timeout=5) or
            self.d(description="Proceed").exists(timeout=5)
        )
        if phone_ready and btn_ready:
            print(" ✅ ready")
        else:
            print(" ⚠️  phone input not ready — check screenshot")

    def launch_app(self):
        """Cold-start the app, handle passcode, then wait for the phone-input screen."""
        try:
            self.d.app_start(APP_PACKAGE, stop=False)
        except Exception:
            self._reconnect()
            self.d.app_start(APP_PACKAGE, stop=False)

        print("  ⏳ Waiting for app...", end="", flush=True)
        time.sleep(3)

        if self._is_passcode_screen():
            print(" 🔐 passcode screen detected")
            self.screenshot("passcode_screen")
            self.enter_passcode()
            self.screenshot("after_passcode")

        phone_ready = self.d(className="android.widget.EditText").exists(timeout=35)

        # Continue button can be hidden below the keyboard / top of screen — scroll up first
        if not self.d(description="Continue").exists(timeout=2) and \
           not self.d(description="Proceed").exists(timeout=2):
            self.d.swipe(500, 500, 500, 1500, 0.4)   # scroll up
            time.sleep(0.5)

        btn_ready = (
            self.d(description="Continue").exists(timeout=5) or
            self.d(description="Proceed").exists(timeout=5)
        )
        if phone_ready and btn_ready:
            print(" ✅ ready")
        else:
            print(" ⚠️  phone input not ready — check screenshot")

    def close_app(self):
        """Send app to background without clearing state."""
        self.d.press("home")
        time.sleep(1)
