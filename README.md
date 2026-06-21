# Skorcard Android Test Automation

Automated UI tests for the **Skorcard** Android app using **uiautomator2** (no Appium server required).  
Supports two run modes: a fast custom runner and a full **pytest + Allure** pipeline for HTML reports.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running Tests](#running-tests)
  - [Custom Runner](#1-custom-runner-recommended)
  - [Pytest + Allure Report](#2-pytest--allure-report)
- [Test Suites](#test-suites)
- [Environment Variables](#environment-variables)
- [Outputs](#outputs)
- [Troubleshooting](#troubleshooting)

---

## Project Structure

```
test_automation/
│
├── run_tests.py              # Main test runner — no pytest needed
├── conftest.py               # pytest hooks (auto-screenshot on failure for Allure)
├── pytest.ini                # pytest + Allure configuration
├── requirements.txt          # Python dependencies
│
├── tests/
│   ├── base.py               # BaseTest — device connection, launch, passcode handling
│   ├── test_splash.py        # Splash screen tests (phone input, invitation code)
│   ├── test_registration_login.py  # Registration/Login screen tests
│   ├── test_otp.py           # OTP screen tests
│   ├── test_register_flow.py # Full registration flow (ported from appium-project)
│   └── test_onboarding.py    # KYC onboarding page tests
│
├── pages/
│   ├── base_page.py          # BasePage — shared uiautomator2 helpers
│   ├── register_page.py      # RegisterPage — splash/phone-entry page object
│   └── onboarding_page.py    # OnboardingPage — KYC onboarding page object
│
├── utils/
│   ├── db_helper.py          # PostgreSQL connection (psycopg2)
│   ├── queries.py            # SQL query functions for DB validation
│   ├── logger.py             # File + console logger
│   └── test_data.py          # Test constants (phone, passcode, referral code)
│
├── screenshots/              # Auto-saved screenshots (created on first run)
├── allure-results/           # Allure raw results (created when using --allure)
└── logs/                     # Test log files (created on first run)
```

---

## Prerequisites

| Requirement | Notes |
|---|---|
| **Python 3.9+** | Check: `python3 --version` |
| **ADB** | Android Debug Bridge — `brew install android-platform-tools` |
| **Android device** | Physical device or emulator with USB debugging enabled |
| **uiautomator2 server** | Auto-installed on first run |
| **Allure CLI** *(optional)* | Only needed for HTML reports — `brew install allure` |

### Device Setup

1. Enable **Developer Options** on the Android device
2. Turn on **USB Debugging**
3. Connect the device via USB
4. Verify it is detected:
   ```bash
   adb devices
   ```
   You should see your device listed (not `unauthorized`)

---

## Installation

```bash
# 1. Clone / open the project
cd /path/to/test_automation

# 2. Install all Python dependencies
pip3 install -r requirements.txt

# 3. (Optional) Install Allure CLI for HTML reports
brew install allure        # macOS
# or: npm install -g allure-commandline
```

The packages installed are:

| Package | Version | Purpose |
|---|---|---|
| `uiautomator2` | ≥ 3.0.0 | Android UI automation (no Appium server) |
| `psycopg2-binary` | ≥ 2.9.0 | PostgreSQL database connection |
| `pytest` | ≥ 7.4.0 | Test framework (for Allure integration) |
| `allure-pytest` | ≥ 2.13.0 | Allure report generation |

---

## Running Tests

### 1. Custom Runner (Recommended)

The custom runner does **not** require pytest. It runs suites in order, prints coloured pass/fail output, saves screenshots, and writes a timestamped text report.

```bash
# Run all suites
python3 run_tests.py

# Run a single suite
python3 run_tests.py --suite splash
python3 run_tests.py --suite otp
python3 run_tests.py --suite register_flow
python3 run_tests.py --suite create_pin      # must run before onboarding
python3 run_tests.py --suite onboarding      # requires create_pin to have run first
python3 run_tests.py --suite dashboard
python3 run_tests.py --suite profile
python3 run_tests.py --suite notifications

# Run all suites AND open Allure HTML report afterwards
python3 run_tests.py --allure

# Run one suite AND open Allure report
python3 run_tests.py --suite register_flow --allure
```

**Example output:**
```
=======================================================
  SUITE: SPLASH
=======================================================

[TEST 01] Continue button enables only for valid phone
  📸 01a_splash_initial
  ✅ PASS: Disabled with empty phone
  ✅ PASS: Invalid phone starting with 0 blocked
  ✅ PASS: Disabled with short phone
  ✅ PASS: Enabled with valid phone
...

=======================================================
  FINAL REPORT
=======================================================
  ✅ [splash] test_01_continue_button_validation  (12.3s)
  ✅ [splash] test_02_wrong_invitation_code       (18.7s)
  ...
  Total: 29 passed, 0 failed

  Report:      report_20260429_143022.txt
  Screenshots: screenshots/
```

---

### 2. Pytest + Allure Report

Run tests via pytest to generate a rich interactive HTML report.

```bash
# Run all tests and generate Allure results
python3 -m pytest tests/ --alluredir=allure-results

# Run a specific suite file
python3 -m pytest tests/test_register_flow.py --alluredir=allure-results

# Open the HTML report in a browser
allure serve allure-results
```

The Allure report includes:
- Pass/fail status per test with duration
- Grouped by **Feature** (suite) and **Story** (test scenario)
- **Failure screenshots** automatically attached (via `conftest.py`)
- Step-by-step navigation

---

## Test Suites

| Suite flag | File | Tests | Screens covered |
|---|---|---|---|
| `splash` | `test_splash.py` | 4 | Splash: valid phone, wrong code error, Edit Code re-entry, valid code accepted |
| `otp` | `test_otp.py` | 4 | OTP screen: full flow loads, resend visible, wrong OTP error, verify correct OTP |
| `register_flow` | `test_register_flow.py` | 5 | Full flow: launch → register → DB verification → OTP verify → state machine |
| `create_pin` | `test_create_pin.py` | 6 | Create PIN: fields, same-digit/sequential/mismatch validation, valid PIN |
| `onboarding` | `test_onboarding.py` | 11 | KYC onboarding: page loads, field visibility, T&C, name/NIK validation, valid submit |
| `dashboard` | `test_dashboard.py` | 5 | Dashboard: loads, bottom nav, card widget, profile tab, notification icon |
| `profile` | `test_profile.py` | 7 | Profile: My Account, Logout, Help Center, Biometrics, Language, About |
| `notifications` | `test_notifications.py` | 7 | Notifications: title, System/Promotion tabs, tab switching, back nav |

### What each suite validates

**splash** — 4 tests
- Continue button enabled for valid phone (starts with 8, 8+ digits)
- Wrong invitation code → error sheet shown
- Edit Code button on error sheet re-opens code input for re-entry
- Valid invitation code (OBRSPC9) accepted without error

**otp** — 4 tests
- Full flow: valid phone + Continue → OTP screen loads (navigation test)
- Resend Code link is visible on the OTP screen
- Wrong OTP (000000) shows error message
- OTP retrieved from notification toast (or via Resend), field cleared, correct OTP entered → verified

**register_flow** — 5 tests
- App launch and permission dialogs
- Registration with phone → Continue → DB user_id created
- DB rows: user_settings, device_details, location_details
- OTP verification and DB flag update
- State machine confirms ONBOARDING state

**onboarding** — 11 tests
- Onboarding page loads with correct title, description and button
- All three input fields visible (Full Name, NIK, Monthly Income)
- Submit button disabled before any input
- T&C checkbox unchecked by default
- T&C link opens Terms of Use page
- Back button returns to onboarding form
- Full Name validation message shown when name is empty on submit
- NIK validation rejects input shorter than 16 digits
- Monthly Income field accepts a number and displays formatted value
- Submit button enabled when all fields are valid and T&C checked
- Valid form submission navigates to next screen

**create_pin** — 6 tests
- Create Passcode screen loads after OTP
- Enter Passcode and Confirm Passcode fields are visible
- All-same digits (111111) rejected with error
- Sequential digits (123456) rejected with error
- Mismatched PIN / Confirm shows "Passcode not same" error
- Valid PIN saves and navigates to next screen

**dashboard** — 5 tests
- Dashboard loads after app launch (passcode handled automatically)
- Bottom navigation bar has identifiable tabs
- Credit card widget is visible
- Profile tab accessible from bottom nav
- Notification icon visible on dashboard

**profile** — 7 tests
- Profile page loads from dashboard bottom nav
- "My Account" section header visible
- Logout option visible (scroll to bottom)
- Help Center menu item present
- Biometrics toggle visible
- Language selection option visible
- About Skorcard menu item visible

**notifications** — 7 tests
- Notifications screen opens from dashboard
- "Notifications" app bar title visible
- System tab visible by default
- Promotion tab visible
- Tapping Promotion tab switches the list
- Tapping System tab switches back
- Back navigation returns to dashboard

---

## Environment Variables

All credentials and test data can be overridden without changing code:

```bash
# Override phone number used in tests
TEST_PHONE=8812345678 python3 run_tests.py

# Override the app passcode (default: 112233)
TEST_PASSCODE=999999 python3 run_tests.py

# Override invitation/referral code
TEST_REFERRAL_CODE=MYCODE python3 run_tests.py --suite splash

# Database credentials (default: SIT environment)
DB_HOST=sit-rds.skorcard.app \
DB_NAME=skorcard \
DB_USER=sc_lead_user \
DB_PASS=your_password \
DB_PORT=5432 \
python3 run_tests.py --suite register_flow

# Combined example
TEST_PHONE=8611111111 TEST_PASSCODE=112233 python3 run_tests.py
```

> **Note:** DB tests (`register_flow` tests 05–07) are automatically **skipped** when the database is unreachable. The rest of the suite still runs.

---

## Outputs

After a run you will find:

```
test_automation/
├── screenshots/
│   ├── 143022_01a_splash_initial.png
│   ├── 143025_01b_phone_starts_zero.png
│   └── ...                               ← one per test step
│
├── logs/
│   └── register_flow_20260429.log        ← per-suite debug logs
│
├── report_20260429_143022.txt            ← plain-text summary
│
└── allure-results/                       ← populated when using --allure or pytest
    ├── *.json
    └── attachments/
```

Screenshot names follow the pattern `HHMMSS_<step_name>.png`.  
Failure screenshots are prefixed `HHMMSS_FAIL_<test_name>.png`.

---

## Troubleshooting

**`adb: command not found`**
```bash
brew install android-platform-tools
```

**Device shows as `unauthorized` in `adb devices`**  
Unlock the device, accept the RSA fingerprint prompt, then re-run `adb devices`.

**App does not start / times out**  
The app package is `app.skor.card`. Confirm it is installed:
```bash
adb shell pm list packages | grep skor
```

**Passcode screen blocks tests**  
Tests enter the default passcode `112233` automatically. If your device uses a different passcode:
```bash
TEST_PASSCODE=your_code python3 run_tests.py
```

**`psycopg2` import error**
```bash
pip3 install psycopg2-binary
```

**`allure: command not found`**
```bash
brew install allure
# or
npm install -g allure-commandline
```

**Tests fail with `-32002` selector error**  
This is a stale device connection. The runner will auto-reconnect. If it persists, ensure no other ADB session is open.

**`pytest` collects 0 tests**  
Make sure you are running from the project root:
```bash
cd /path/to/test_automation
python3 -m pytest tests/
```
