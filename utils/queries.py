#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# SQL queries — ported from appium-project/dataBase/queries.py
# All queries use %s placeholders (psycopg2 style).
# ---------------------------------------------------------------------------



CHECK_PHONE_EXISTS = """
SELECT 1 FROM "SC_USER" WHERE phone = %s;
"""

GET_USER_ID = """
SELECT user_id FROM "SC_USER" WHERE phone = %s;
"""

GET_USER_DETAILS = """
SELECT * FROM "SC_USER" WHERE phone = %s ORDER BY customer_id DESC;
"""

GET_USER_SETTINGS = """
SELECT * FROM "SC_USER_SETTINGS" WHERE user_id = %s;
"""

GET_DEVICE_DETAILS = """
SELECT * FROM "SC_USER_DEVICE_DETAILS" WHERE user_id = %s;
"""

GET_LOCATION_DETAILS = """
SELECT * FROM "SC_USER_LOCATION_DETAILS" WHERE user_id = %s;
"""

GET_APPSFLYER = """
SELECT * FROM "SC_USER_APPSFLYER" WHERE user_id = %s AND type = %s;
"""

GET_OTP_VERIFIED = """
SELECT otp_verified FROM "SC_USER" WHERE user_id = %s;
"""

GET_USER_PRODUCT_MAPPING = """
SELECT upm.*
FROM "SC_USER_PRODUCT_MAPPING" upm
JOIN "SC_MASTER_PRODUCT"      mp  ON upm.product_id = mp.id
JOIN "SC_MASTER_ORGANIZATION" mo  ON mp.org_id      = mo.id
WHERE upm.user_id = %s AND mo.org_code = %s
ORDER BY mp.id ASC
LIMIT 1;
"""

GET_STATE = """
SELECT state FROM "SC_STATE_MACHINE" WHERE user_id = %s;
"""

GET_STATE_AUDIT = """
SELECT *
FROM "SC_STATE_MACHINE_AUDIT"
WHERE user_id = %s
ORDER BY created_at desc limit 1;
"""

GET_CAMPAIGN = """
SELECT * FROM "SC_USER_CAMPAIGN" WHERE user_id = %s;
"""

GET_REFERRAL = """
SELECT * FROM "SC_USER_REFERRAL"
WHERE user_id = %s
ORDER BY id DESC
LIMIT 1;
"""

GET_UW_USER_TARAN = """
SELECT * FROM "SC_UW_USER_TARAN" WHERE user_id = %s and uw_type = %s;
"""

GET_UW_USER = """
SELECT * FROM "SC_UW_USER" WHERE user_id = %s;
"""

# ---------------------------------------------------------------------------
# State Machine Queries
# ---------------------------------------------------------------------------

GET_STATE_MACHINE = """
SELECT *
FROM "SC_STATE_MACHINE"
WHERE user_id = %s;
"""


GET_ONBOARDING_TO_PRE_MANUAL_VERIFICATION = """
SELECT *
FROM "SC_STATE_MACHINE_AUDIT"
WHERE user_id = %s
  AND previous_state = 'ONBOARDING'
  AND current_state = 'PRE_MANUAL_VERIFICATION';
"""



# ---------------------------------------------------------------------------
# Acquisition Queries
# ---------------------------------------------------------------------------

GET_USER_ACQUISITION = """
SELECT *
FROM "SC_USER_ACQUISITION"
WHERE user_id = %s;
"""

GET_KYC_DETAILS = """
SELECT *
FROM "SC_KYC_DETAILS"
WHERE user_id = %s;
"""

GET_KYC_STATUS = """
SELECT *
FROM "SC_KYC_STATUS"
WHERE user_id = %s
  AND org_id = (
      SELECT id
      FROM "SC_MASTER_ORGANIZATION"
      WHERE org_code = 'BMI'
  );
"""

GET_KTP_ADDRESS = """
SELECT ua.*
FROM "SC_USER_ADDRESS" ua
JOIN "SC_MASTER" m
  ON m.id = ua.address_type_id
WHERE ua.user_id = %s
  AND m.category = 'ADDRESS_TYPE'
  AND m.org_description = 'KTP';
"""

GET_BUREAU_CONSENT = """
SELECT *
FROM "SC_USER_CONSENT"
WHERE user_id = %s
  AND consent_type = 'BUREAU_CONSENT';
"""


# ---------------------------------------------------------------------------
# Pre Underwriting Queries
# ---------------------------------------------------------------------------


GET_MSI_SUCCESS_STATUS = """
SELECT *
FROM "SC_UW_USER_CREDIT_STATUS"
WHERE user_id = %s
  AND status = 'MSI_SUCCESS'
  AND bank = 'BMI';
"""


UPDATE_LIMIT_AND_CARD_TYPE = """

UPDATE "SC_UW_USER_TARAN"
SET credit_limit = %s,
    product_type = %s
WHERE user_id = %s
"""



INSERT_SC_USER_KTP_ADDRESS = """
INSERT INTO "SC_USER_ADDRESS"
  ("user_id","address_type_id","address","address_1","address_2","address_3","address_4",
   "town","district","sub_district","province","zipcode","country","alias_address",
   "complete_address","delivery_note","delivery","rt","rw","additional_details",
   "latitude","longitude","same_as_ktp","retool_latitude","retool_longitude","retool_address",
   "is_user_opted_delivery","building_type","building_number","street_number","building_name",
   "building_tower","building_unit_number","building_floor","house_number","updated_at","created_at")
VALUES
  (%s,19,'JL. PASTI CEPAT A7/66','JL. PASTI CEPAT A7/66','','','','Denpasar','Denpasar Utara','Ubung Kaja','Bali','80116', 'ID','', '', '', FALSE,'007','008',NULL,0,0,FALSE,0,0,'',NULL,NULL,'','','','','','','',NOW(),NOW())
ON CONFLICT ("user_id","address_type_id") DO UPDATE
SET
  "address" = EXCLUDED."address",
  "address_1" = EXCLUDED."address_1",
  "town" = EXCLUDED."town",
  "district" = EXCLUDED."district",
  "sub_district" = EXCLUDED."sub_district",
  "province" = EXCLUDED."province",
  "zipcode" = EXCLUDED."zipcode",
  "country" = EXCLUDED."country",
  "alias_address" = EXCLUDED."alias_address",
  "rt" = EXCLUDED."rt",
  "rw" = EXCLUDED."rw",
  "complete_address" = EXCLUDED."complete_address",
  "additional_details" = EXCLUDED."additional_details",
  "updated_at" = EXCLUDED."updated_at"
RETURNING "id","created_at";
"""

UPDATE_KYC_DETAILS = """
UPDATE "SC_KYC_DETAILS"
SET
  "nik" = 3171234567890123,
  "full_name" = 'Anil Kumar',
  "dob" = '2004-02-01 00:00:00',
  "address" = 'JL. PASTI CEPAT A7/66',
  "blood_group" = 'B',
  "city" = 'JAKARTA BARAT',
  "district" = 'KALIDERES',
  "gender" = 'PEREMPUAN',
  "marital_status" = 'KAWIN',
  "nationality" = 'WNI',
  "occupation" = 'KARYAWAN SWASTA',
  "place_of_birth" = 'JAKARTA',
  "province" = 'DKI JAKARTA',
  "religion" = 'Islam',
  "rt_rw" = '007/008',
  "valid_till" = '2017-02-22',           -- was '22-02-2017'
  "village" = 'PEGADUNGAN',
  "spouse_name" = 'NA',
  "ocr_trans_id" = '2533c235-0035-4ffc-8c5c-0ad1d50c4abf',
  "updated_at" = NOW(),
  "kyc_mode" = 'INIT'
WHERE user_id = %s;

"""

UPDATE_DOCUMENT_STATUS = """
UPDATE "SC_USER_ADDITIONAL_DOCUMENT_AUDIT"
SET status = true
WHERE user_id = %s
"""

INSERT_KYC_FACEMATCH_TRANS = """
insert into "SC_KYC_FACEMATCH_TRANS" (user_id,partner_request_id, image_path,status,facematch_type,liveness_type) values (%s,gen_random_uuid(),'2026/06/15/SC062026000093_ba04b057-6e53-4374-a7d0-3c3677296f5b.jpg', 'PENDING','ON_BOARDING', 'IPROOV')
"""

GET_USER_SSO_AUDIT = """
select * from "SC_USER_SSO_AUDIT" where user_id = %s;
"""





# ---------------------------------------------------------------------------
# Helper functions (same API as appium-project/dataBase/queries.py)
# ---------------------------------------------------------------------------

def check_phone_exists(db, phone):
    return len(db.execute_query(CHECK_PHONE_EXISTS, (phone,))) > 0


def get_user_id(db, phone):
    rows = db.execute_query(GET_USER_ID, (phone,))
    return rows[0].get('user_id') if rows else None


def get_user_details(db, phone):
    return db.execute_query(GET_USER_DETAILS, (phone,))


def get_user_settings(db, user_id):
    return db.execute_query(GET_USER_SETTINGS, (user_id,))


def get_device_details(db, user_id):
    return db.execute_query(GET_DEVICE_DETAILS, (user_id,))


def get_location_details(db, user_id):
    return db.execute_query(GET_LOCATION_DETAILS, (user_id,))


def get_appsflyer(db, user_id, source_type):
    return db.execute_query(GET_APPSFLYER, (user_id, source_type))


def get_otp_verified(db, user_id):
    rows = db.execute_query(GET_OTP_VERIFIED, (user_id,))
    return rows[0].get('otp_verified') if rows else None


def get_user_product_mapping(db, user_id, org_code):
    return db.execute_query(GET_USER_PRODUCT_MAPPING, (user_id, org_code))


def get_state(db, user_id):
    rows = db.execute_query(GET_STATE, (user_id,))
    return rows[0].get('state') if rows else None


def get_state_audit(db, user_id):
    return db.execute_query(GET_STATE_AUDIT, (user_id,))


def get_campaign(db, user_id):
    return db.execute_query(GET_CAMPAIGN, (user_id,))


def get_referral(db, user_id):
    return db.execute_query(GET_REFERRAL, (user_id,))

def get_uw_user_taran(db, user_id, uw_type):
    return db.execute_query(GET_UW_USER_TARAN, (user_id, uw_type))

def get_sc_uw_user(db,user_id):
    return db.execute_query(GET_UW_USER, (user_id,))

def get_user_sso_audit(db, user_id):
    return db.execute_query(GET_USER_SSO_AUDIT, (user_id,))


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_state_machine(db, user_id):
    return db.execute_query(GET_STATE_MACHINE, (user_id,))


def get_onboarding_to_pre_manual_verification(db, user_id):
    return db.execute_query(GET_ONBOARDING_TO_PRE_MANUAL_VERIFICATION, (user_id,))


def get_user_acquisition(db, user_id):
    return db.execute_query(GET_USER_ACQUISITION, (user_id,))


def get_kyc_details(db, user_id):
    return db.execute_query(GET_KYC_DETAILS, (user_id,))


def get_kyc_status(db, user_id):
    return db.execute_query(GET_KYC_STATUS, (user_id,))


def get_ktp_address(db, user_id):
    return db.execute_query(GET_KTP_ADDRESS, (user_id,))


def get_bureau_consent(db, user_id):
    return db.execute_query(GET_BUREAU_CONSENT, (user_id,))


def get_msi_success_status(db, user_id):
    return db.execute_query(GET_MSI_SUCCESS_STATUS, (user_id,))


def update_limit_and_card_type(db, user_id, credit_limit, product_type):
    return db.execute_query(UPDATE_LIMIT_AND_CARD_TYPE, (credit_limit, product_type, user_id))

def insert_sc_user_ktp_address(db, user_id):
    return db.execute_query(INSERT_SC_USER_KTP_ADDRESS, (user_id,))

def update_kyc_details(db, user_id):
    return db.execute_query(UPDATE_KYC_DETAILS, (user_id,))

def update_document_status(db, user_id):
    return db.execute_query(UPDATE_DOCUMENT_STATUS, (user_id,))

def insert_kyc_facematch_trans(db, user_id):
    return db.execute_query(INSERT_KYC_FACEMATCH_TRANS, (user_id,))