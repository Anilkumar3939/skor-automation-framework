#!/usr/bin/env python3
import os

# ---------------------------------------------------------------------------
# Phone numbers
# Override via env vars so CI can inject different numbers without editing code
# ---------------------------------------------------------------------------
VALID_PHONE   = os.environ.get("TEST_PHONE",    "86217777389")   # 11 digits, starts with 8
PASSCODE      = os.environ.get("TEST_PASSCODE", "112233")
REFERRAL_CODE = os.environ.get("TEST_REFERRAL_CODE", "OBRSPC9")

# Phone validation edge-cases used in parametrised tests
PHONE_TEST_CASES = [
    ("12345",       False),   # starts with 1, too short
    ("88888888",    False),   # all same digits
    ("81233422",    False),   # only 8 digits (minimum is 9)
    ("86217777331", True),    # valid 11-digit number
]
VALID_EMAIL = "anilkumar3939104@gmail.com"

def get_phone():
    return VALID_PHONE


def get_passcode():
    return PASSCODE


def get_referral_code():
    return REFERRAL_CODE
