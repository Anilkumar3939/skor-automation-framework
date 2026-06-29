#!/usr/bin/env python3
"""
Skorcard Android Test Runner
============================

Custom runner (no pytest needed):
    python3 run_tests.py                                # run all suites (in order below)
    python3 run_tests.py --suite splash                 # splash screen only
    python3 run_tests.py --suite otp                    # OTP screen
    python3 run_tests.py --suite register_flow          # full registration flow
    python3 run_tests.py --suite create_pin             # Create PIN screen  ← before onboarding
    python3 run_tests.py --suite onboarding             # KYC onboarding page ← after create_pin
    python3 run_tests.py --suite dashboard              # Dashboard screen
    python3 run_tests.py --suite profile                # Profile page
    python3 run_tests.py --suite notifications          # Notifications screen

Suite execution order (when running all):
    splash → otp → register_flow → create_pin → onboarding → dashboard → profile → notifications

With Allure HTML report (requires: pip3 install allure-pytest + allure CLI):
    python3 run_tests.py --allure                       # run all + open Allure report
    python3 run_tests.py --suite splash --allure        # single suite + Allure

  Or run via pytest directly:
    pytest tests/ --alluredir=allure-results
    allure serve allure-results

Environment variable overrides:
    TEST_PHONE=8812345600      python3 run_tests.py
    DB_PASS=secret             python3 run_tests.py --suite register_flow
    TEST_PASSCODE=112233       python3 run_tests.py
"""
import sys
import os
import time
import argparse
import importlib.util
from datetime import datetime

# Add tests/ to path so base.py is importable
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests"))

# Suite registry: name → (file, class, ordered_test_list or None for alphabetical)
SUITES = {
    # ── Registration / authentication flow (run in this order) ──────────
    "splash": {
        "file": "test_splash.py",
        "class": "SplashScreenTest",
        "order": "TEST_ORDER",
    },
    "otp": {
        "file": "test_otp.py",
        "class": "OTPScreenTest",
        "order": "TEST_ORDER",
    },
    "register_flow": {
        "file": "test_register_flow.py",
        "class": "TestRegisterFlow",
        "order": "TEST_ORDER",
    },
    # create_pin MUST come before onboarding —
    # the onboarding form is only reachable after PIN creation.
    "create_pin": {
        "file": "test_create_pin.py",
        "class": "TestCreatePin",
        "order": "TEST_ORDER",
    },
    "onboarding": {
        "file": "test_onboarding.py",
        "class": "TestOnboarding",
        "order": "TEST_ORDER",
    },
    # ── Post-login screens ────────────────────────────────────────────────
    "dashboard": {
        "file": "test_dashboard.py",
        "class": "TestDashboard",
        "order": "TEST_ORDER",
    },
    "profile": {
        "file": "test_profile.py",
        "class": "TestProfile",
        "order": "TEST_ORDER",
    },
    "notifications": {
        "file": "test_notifications.py",
        "class": "TestNotifications",
        "order": "TEST_ORDER",
    },
}

RESULTS = []


def load_suite(suite_cfg):
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "tests", suite_cfg["file"]
    )
    spec = importlib.util.spec_from_file_location("suite_mod", file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cls = getattr(mod, suite_cfg["class"])

    # setup_class connects the device and initialises page objects once.
    # (pytest calls this automatically; we do it explicitly here.)
    cls.setup_class()

    instance = cls()

    # Get test order
    if suite_cfg["order"] and hasattr(mod, suite_cfg["order"]):
        test_methods = getattr(mod, suite_cfg["order"])
    else:
        test_methods = sorted(m for m in dir(instance) if m.startswith("test_"))

    return instance, test_methods


def run_suite(suite_name, suite_cfg):
    print(f"\n{'='*55}")
    print(f"  SUITE: {suite_name.upper()}")
    print(f"{'='*55}")

    try:
        instance, test_methods = load_suite(suite_cfg)
    except Exception as e:
        print(f"  ❌ Failed to load suite: {e}")
        return 0, 1

    passed = failed = 0
    for method_name in test_methods:
        start = time.time()
        try:
            getattr(instance, method_name)()
            passed += 1
            RESULTS.append({
                "suite": suite_name,
                "test": method_name,
                "status": "PASS",
                "duration": time.time() - start,
            })
        except Exception as e:
            failed += 1
            print(f"  ❌ EXCEPTION in {method_name}: {e}")
            RESULTS.append({
                "suite": suite_name,
                "test": method_name,
                "status": "FAIL",
                "error": str(e),
                "duration": time.time() - start,
            })

    print(f"\n  Suite: {passed} passed, {failed} failed")
    return passed, failed


def print_report():
    print(f"\n{'='*55}")
    print("  FINAL REPORT")
    print(f"{'='*55}")

    for r in RESULTS:
        icon = "✅" if r["status"] == "PASS" else "❌"
        print(f"  {icon} [{r['suite']}] {r['test']}  ({r['duration']:.1f}s)")
        if r["status"] == "FAIL" and "error" in r:
            print(f"       → {r['error']}")

    total_pass = sum(1 for r in RESULTS if r["status"] == "PASS")
    total_fail = sum(1 for r in RESULTS if r["status"] == "FAIL")
    print(f"\n  Total: {total_pass} passed, {total_fail} failed")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"report_{ts}.txt")
    with open(report_path, "w") as f:
        f.write(f"Skorcard Test Report — {ts}\n")
        f.write("=" * 55 + "\n")
        for r in RESULTS:
            f.write(f"{r['status']} | {r['suite']} | {r['test']} | {r['duration']:.1f}s | {r.get('error','')}\n")
        f.write(f"\nTotal: {total_pass} passed, {total_fail} failed\n")

    print(f"\n  Report:      {report_path}")
    print(f"  Screenshots: {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screenshots/')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Skorcard Android Test Runner")
    parser.add_argument("--suite", choices=list(SUITES.keys()), help="Run a specific suite")
    parser.add_argument(
        "--allure", action="store_true",
        help="After run, generate and open Allure report (requires allure CLI installed)"
    )
    args = parser.parse_args()

    suites_to_run = {args.suite: SUITES[args.suite]} if args.suite else SUITES
    total_pass = total_fail = 0

    for name, cfg in suites_to_run.items():
        p, f = run_suite(name, cfg)
        total_pass += p
        total_fail += f

    print_report()

    # ── Allure report ───────────────────────────────────────────────────────
    if args.allure:
        import subprocess
        suite_flag = ["--suite", args.suite] if args.suite else []
        allure_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "allure-results")
        print(f"\n  📊 Generating Allure report via pytest...")
        print(f"     (re-running tests through pytest to populate allure-results/)")
        pytest_cmd = [
            sys.executable, "-m", "pytest", "tests/",
            f"--alluredir={allure_dir}", "-v", "--tb=short",
        ]
        if args.suite:
            # Map suite name to test file for targeted pytest run
            suite_file = SUITES[args.suite]["file"]
            pytest_cmd[4] = f"tests/{suite_file}"
        try:
            subprocess.run(pytest_cmd, cwd=os.path.dirname(os.path.abspath(__file__)))
            print(f"\n  🌐 Opening Allure report...")
            subprocess.run(["allure", "serve", allure_dir])
        except FileNotFoundError:
            print("\n  ⚠️  allure CLI not found.")
            print("     Install: brew install allure  (macOS)")
            print("     Or:      npm install -g allure-commandline")
            print(f"     Results saved to: {allure_dir}")
            print("     Run manually: allure serve allure-results")

    sys.exit(1 if total_fail > 0 else 0)
